"""Exact replay of the m=3 common-shore compatibility interface.

The written theorem proves the universal matching decomposition.  This
verifier checks its indices symbolically, then checks the exact normalized
Latin-plane full-row separator and its no-axis-line certificate.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

DIM = 3
NONROOTS = ("x", "y", "r")
WORDS = tuple(product(range(DIM), repeat=DIM))
ROW = {word: index for index, word in enumerate(WORDS)}
X = sp.symbols("x0:3")
Y = sp.symbols("y0:3")
R = sp.symbols("r0:3")
GROUPS = (X, Y, R)
VARIABLES = X + Y + R
COLUMN_DEGREES = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))


def basis_tensor(word: tuple[int, int, int]) -> sp.Matrix:
    """Return the coordinate tensor supported at one root word."""
    answer = sp.zeros(DIM**3, 1)
    answer[ROW[word], 0] = 1
    return answer


def symbolic_singleton_interface() -> None:
    """Check the shared-factor formula against the direct matching sum."""
    b12 = sp.Matrix(DIM, DIM, lambda a, b: sp.Symbol(f"b12_{a}{b}"))
    b13 = sp.Matrix(DIM, DIM, lambda a, c: sp.Symbol(f"b13_{a}{c}"))
    b23 = sp.Matrix(DIM, DIM, lambda b, c: sp.Symbol(f"b23_{b}{c}"))
    vectors = tuple(
        sp.Matrix(
            DIM,
            1,
            lambda a, _, root=i: sp.Symbol(f"h{root + 1}_{a}"),
        )
        for i in range(DIM)
    )

    direct = sp.zeros(DIM**3, 1)
    shared_factor = sp.zeros(DIM**3, 1)
    for word in WORDS:
        a, b, c = word
        # Directly enumerate the chosen cross root.  The other two roots have
        # the unique internal perfect matching.
        direct[ROW[word], 0] = (
            vectors[0][a] * b23[b, c]
            + vectors[1][b] * b13[a, c]
            + vectors[2][c] * b12[a, b]
        )
        # Independently assemble the three tensor-cylinder summands.
        shared_factor += (
            vectors[0][a] * b23[b, c]
            + b13[a, c] * vectors[1][b]
            + b12[a, b] * vectors[2][c]
        ) * basis_tensor(word)

    assert direct == shared_factor


def permanent3(matrix: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Return the sign-free 3 by 3 permanent."""
    return sp.expand(
        sum(
            sp.prod(matrix[i][sigma[i]] for i in range(DIM))
            for sigma in permutations(range(DIM))
        )
    )


def symbolic_empty_permanent_interface() -> None:
    """Check that the empty sensor column is the six-term cross permanent."""
    # Fix arbitrary nonroot colours.  The 27 covector entries below are
    # algebraically independent, so the coefficient check is universal.
    h = {
        (root, nonroot, colour): sp.Symbol(
            f"q{root + 1}{nonroot}_{colour}"
        )
        for root in range(DIM)
        for nonroot in range(DIM)
        for colour in range(DIM)
    }
    direct = sp.zeros(DIM**3, 1)
    for sigma in permutations(range(DIM)):
        for word in WORDS:
            direct[ROW[word], 0] += sp.prod(
                h[(root, sigma[root], word[root])] for root in range(DIM)
            )

    by_permanent = sp.zeros(DIM**3, 1)
    for word in WORDS:
        matrix = tuple(
            tuple(h[(root, nonroot, word[root])] for nonroot in range(DIM))
            for root in range(DIM)
        )
        by_permanent[ROW[word], 0] = permanent3(matrix)

    assert direct.applyfunc(sp.expand) == by_permanent
    assert len(tuple(permutations(range(DIM)))) == 6


def ghz_target() -> sp.Matrix:
    """Return the contracted ternary GHZ target."""
    target = sp.zeros(DIM**3, 1)
    for colour in range(DIM):
        target[ROW[(colour, colour, colour)], 0] = (
            X[colour] * Y[colour] * R[colour]
        )
    return target


def latin_slice(nonroot: int, colour: int) -> sp.Matrix:
    """Return the Latin-plane slice e_(c,u,-c-u)."""
    return basis_tensor((colour, nonroot, (-colour - nonroot) % DIM))


def group_degrees(expression: sp.Expr) -> set[tuple[int, int, int]]:
    """Return group multidegrees of the nonzero monomials."""
    polynomial = sp.Poly(expression, *VARIABLES)
    return {
        (
            sum(monomial[:3]),
            sum(monomial[3:6]),
            sum(monomial[6:]),
        )
        for monomial, coefficient in polynomial.terms()
        if coefficient
    }


def latin_full_row_separator() -> tuple[sp.Expr, set[tuple[int, int, int]]]:
    """Check target consistency, rank four, degrees, and the ruling obstruction."""
    pair_sections = []
    for nonroot, variables in enumerate(GROUPS):
        section = sp.zeros(DIM**3, 1)
        for colour, variable in enumerate(variables):
            section += variable * latin_slice(nonroot, colour)
        pair_sections.append(section)

    # Standard even-deck order: (xy,xr,yr,empty).  Its companion labels are
    # respectively r, y, x, and xyz.
    gamma = sp.Matrix.hstack(
        pair_sections[2],
        pair_sections[1],
        pair_sections[0],
        ghz_target(),
    )
    solution = sp.Matrix([0, 0, 0, 1])
    target = ghz_target()
    assert gamma * solution == target

    for column, expected in enumerate(COLUMN_DEGREES):
        for entry in gamma[:, column]:
            if entry != 0:
                assert group_degrees(entry) == {expected}

    selected_words = ((0, 2, 1), (0, 1, 2), (1, 0, 2), (0, 0, 0))
    selected = gamma.extract([ROW[word] for word in selected_words], range(4))
    determinant = sp.factor(selected.det())
    assert determinant == X[0] * X[1] * Y[0] ** 2 * R[0] ** 2

    slices = [
        latin_slice(nonroot, colour)
        for nonroot in range(DIM)
        for colour in range(DIM)
    ]
    slice_matrix = sp.Matrix.hstack(*slices)
    assert slice_matrix.rank() == 9

    latin_support = {
        (colour, nonroot, (-colour - nonroot) % DIM)
        for nonroot in range(DIM)
        for colour in range(DIM)
    }
    assert len(latin_support) == 9
    assert all(sum(word) % DIM == 0 for word in latin_support)

    # A coordinate subspace contains A tensor w_BC only if every coordinate
    # line over each nonzero coefficient of w_BC is present.  The Latin plane
    # meets every axis-parallel line in exactly one point, never all three.
    for axis in range(DIM):
        other_axes = tuple(index for index in range(DIM) if index != axis)
        for fixed in product(range(DIM), repeat=2):
            line = {
                tuple(
                    value
                    if index == axis
                    else fixed[other_axes.index(index)]
                    for index in range(DIM)
                )
                for value in range(DIM)
            }
            assert len(line & latin_support) == 1

    return determinant, latin_support


def main() -> None:
    """Run the exact common-shore interface and separator replay."""
    symbolic_singleton_interface()
    symbolic_empty_permanent_interface()
    determinant, support = latin_full_row_separator()
    print("m=3 singleton shared-factor interface: PASS")
    print("empty sensor column six-term permanent: PASS")
    print(f"Latin-plane slice rank: PASS ({len(support)}/9)")
    print(f"full-rank minor: {determinant}")
    print("common-shore realization of Latin separator: EXCLUDED")
    print("S2M eight-control realization: NOT DECIDED")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
