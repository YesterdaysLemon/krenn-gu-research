"""Primary checks for the balanced common-quadric mixed-word obstruction."""

from __future__ import annotations

from itertools import permutations

import sympy as sp


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield every labelled perfect matching recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, partner),) + tail


def permanent(matrix: list[list[sp.Expr | int]]) -> sp.Expr:
    """Expand a small permanent exactly."""
    size = len(matrix)
    return sp.expand(
        sum(
            sp.prod(matrix[row][order[row]] for row in range(size))
            for order in permutations(range(size))
        )
    )


def deterministic_cross_forms(
    m: int, variables: tuple[sp.Symbol, ...]
) -> list[list[sp.Expr]]:
    """Build a non-column-separable matrix of exact linear forms."""
    x, y, z = variables
    return [
        [
            (1 + (row + 1) * (column + 2)) * x
            + (2 + row + 2 * column) * y
            + (3 + 2 * row + column) * z
            for column in range(m)
        ]
        for row in range(m)
    ]


def full_repeated_root_contraction(
    m: int,
    quadratic: sp.Expr,
    cross_forms: list[list[sp.Expr]],
) -> sp.Expr:
    """Evaluate the full graph with arbitrary deterministic internal weights."""
    total = sp.Integer(0)
    for matching in perfect_matchings(tuple(range(2 * m))):
        term = sp.Integer(1)
        for left, right in matching:
            if right < m:
                scalar = 1 + left + 2 * right
                term *= scalar * quadratic
            elif left < m:
                term *= cross_forms[left][right - m]
            else:
                nonroot_left = left - m
                nonroot_right = right - m
                term *= 2 + 3 * nonroot_left + 5 * nonroot_right
        total += term
    return sp.expand(total)


def remainder_mod_quadratic(
    polynomial: sp.Expr,
    quadratic: sp.Expr,
    variables: tuple[sp.Symbol, ...],
) -> sp.Expr:
    """Return the exact multivariate polynomial remainder modulo Q."""
    _, remainder = sp.div(
        sp.Poly(polynomial, *variables),
        sp.Poly(quadratic, *variables),
    )
    return sp.expand(remainder.as_expr())


def assert_all_cross_residue() -> dict[int, tuple[int, int]]:
    """Check that arbitrary internal sectors vanish modulo the common Q."""
    variables = sp.symbols("x y z")
    x, y, z = variables
    quadratic = x**2 + y**2 + z**2
    ledger: dict[int, tuple[int, int]] = {}
    for m in range(2, 5):
        cross_forms = deterministic_cross_forms(m, variables)
        full = full_repeated_root_contraction(m, quadratic, cross_forms)
        all_cross = permanent(cross_forms)
        assert remainder_mod_quadratic(
            full - all_cross, quadratic, variables
        ) == 0
        full_remainder = remainder_mod_quadratic(full, quadratic, variables)
        cross_remainder = remainder_mod_quadratic(
            all_cross, quadratic, variables
        )
        assert full_remainder == cross_remainder
        ledger[m] = (
            len(tuple(perfect_matchings(tuple(range(2 * m))))),
            len(sp.Poly(full, *variables).terms()),
        )
    return ledger


def scalar_matrix(m: int) -> list[list[int]]:
    """Return a deterministic matrix with nonzero permanent."""
    return [
        [1 + (row + 1) * (column + 2) for column in range(m)]
        for row in range(m)
    ]


def assert_column_factorization() -> dict[int, int]:
    """Check the conformal permanent factor and its nonzero Q-remainder."""
    variables = sp.symbols("x y z")
    x, y, z = variables
    quadratic = x**2 + y**2 + z**2
    ledger: dict[int, int] = {}
    isotropic_point = {x: 1, y: sp.I, z: 0}
    for m in range(2, 7):
        scalars = scalar_matrix(m)
        linear_forms = [
            x + (column + 2) * y + (column + 3) * z
            for column in range(m)
        ]
        cross_forms = [
            [scalars[row][column] * linear_forms[column] for column in range(m)]
            for row in range(m)
        ]
        scalar_permanent = int(permanent(scalars))
        assert scalar_permanent != 0
        cross_permanent = permanent(cross_forms)
        expected = sp.expand(scalar_permanent * sp.prod(linear_forms))
        assert sp.expand(cross_permanent - expected) == 0
        remainder = remainder_mod_quadratic(
            cross_permanent, quadratic, variables
        )
        assert remainder != 0
        assert sp.expand(quadratic.subs(isotropic_point)) == 0
        assert sp.expand(cross_permanent.subs(isotropic_point)) != 0
        ledger[m] = scalar_permanent
    return ledger


def assert_target_coordinate_words() -> dict[str, int]:
    """Audit the zero/nonzero GHZ contractions used by the proof."""
    m = 5
    words = [
        (0,) * m,
        (1,) * m,
        (2,) * m,
        (0, 1, 0, 1, 2),
        (2, 2, 1, 2, 2),
    ]
    values = [int(len(set(word)) == 1) for word in words]
    assert values == [1, 1, 1, 0, 0]
    return {"constant": sum(values), "mixed_zero": len(values) - sum(values)}


def assert_zero_permanent_pure_branch() -> dict[int, int]:
    """Check that a zero cross permanent contradicts the pure residue."""
    variables = sp.symbols("x y z")
    x, y, z = variables
    quadratic = x**2 + y**2 + z**2
    zero_permanent_matrices = {
        2: [[1, 1], [1, -1]],
        3: [[-2, -2, -2], [-2, -2, -2], [-2, 1, 1]],
    }
    ledger: dict[int, int] = {}
    for m, scalars in zero_permanent_matrices.items():
        assert permanent(scalars) == 0
        nonroot_forms = [
            x + (column + 2) * y + (column + 4) * z
            for column in range(m)
        ]
        cross_forms = [
            [scalars[row][column] * nonroot_forms[column] for column in range(m)]
            for row in range(m)
        ]
        assert permanent(cross_forms) == 0
        graph = full_repeated_root_contraction(m, quadratic, cross_forms)
        assert remainder_mod_quadratic(graph, quadratic, variables) == 0

        root_forms = [
            (row + 2) * x + (2 * row + 1) * y + (row + 3) * z
            for row in range(m)
        ]
        pure_target = sp.expand(sp.prod(root_forms))
        pure_remainder = remainder_mod_quadratic(
            pure_target, quadratic, variables
        )
        assert pure_remainder != 0
        ledger[m] = len(sp.Poly(pure_remainder, *variables).terms())
    return ledger


def assert_degenerate_root_span() -> dict[int, int]:
    """Check the local covector span of diagonal forms of each possible rank."""
    ledger: dict[int, int] = {}
    for form_rank in range(4):
        diagonal = sp.diag(
            *[1 if index < form_rank else 0 for index in range(3)]
        )
        covectors = []
        for vector in (
            sp.Matrix([1, 0, 0]),
            sp.Matrix([0, 1, 0]),
            sp.Matrix([0, 0, 1]),
            sp.Matrix([1, 2, 3]),
        ):
            covectors.append(list(diagonal * vector))
        span_rank = sp.Matrix.hstack(
            *(sp.Matrix(covector) for covector in covectors)
        ).rank()
        assert span_rank == form_rank
        ledger[form_rank] = span_rank
    return ledger


def main() -> None:
    residues = assert_all_cross_residue()
    factors = assert_column_factorization()
    targets = assert_target_coordinate_words()
    zero_permanent = assert_zero_permanent_pure_branch()
    degenerate = assert_degenerate_root_span()
    print("balanced common-quadric mixed-permanent primary checks: PASS")
    print(f"  (matchings, monomials) full-contraction ledger: {residues}")
    print(f"  nonzero scalar permanents m=2..6: {factors}")
    print(f"  GHZ coordinate contractions: {targets}")
    print(f"  zero-permanent pure remainders: {zero_permanent}")
    print(f"  degenerate root covector spans: {degenerate}")


if __name__ == "__main__":
    main()
