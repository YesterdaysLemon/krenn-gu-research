"""Exact replay for the repeated-coordinate HB support localization.

The owning Markdown file is the proof.  This verifier checks the scalar-
general derivative and untouched grid, the complementary support contraction,
the same-colour target gate, the two plane-incidence kernels, the diagonal
divisor step, and all equal-plane matrix orientations.
"""

from __future__ import annotations

from itertools import combinations_with_replacement, permutations, product
from math import factorial

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def source(group: int, vector: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(9, 1)
    out[3 * group : 3 * group + 3, 0] = vector
    return out


def components(vector: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return vector[:3, :], vector[3:6, :], vector[6:9, :]


def polarized(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix) -> sp.Matrix:
    forms = (components(u), components(v), components(q))
    out = sp.zeros(27, 1)
    for sigma in permutations(range(3)):
        out += tensor3(
            forms[sigma[0]][0],
            forms[sigma[1]][1],
            forms[sigma[2]][2],
        )
    return sp.simplify(out)


def mixed_map(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(polarized(u, v, sp.eye(9)[:, index]) for index in range(9))
    )


def target(index: int) -> sp.Matrix:
    return tensor3(e(index), e(index), e(index))


def grid_value(i: int, j: int, k: int) -> sp.Matrix:
    return target(k) if i == j == k else sp.zeros(27, 1)


def complementary_support_grid() -> None:
    a, b, lam, mu = sp.symbols("a b lam mu", nonzero=True)
    z = a * e(0) + b * e(1)
    es = e(2)

    columns = []
    for index in range(3):
        columns.append(-mu * tensor3(e(index), es, z))
    for index in range(3):
        columns.append(-lam * tensor3(es, e(index), z))
    for index in range(3):
        columns.append(lam * mu * tensor3(es, es, e(index)))
    derivative = sp.Matrix.hstack(*columns)

    k1 = (lam * es).col_join(sp.zeros(3, 1)).col_join(z)
    k2 = sp.zeros(3, 1).col_join(mu * es).col_join(z)
    assert derivative * k1 == sp.zeros(27, 1)
    assert derivative * k2 == sp.zeros(27, 1)
    assert derivative.rank() == 7
    assert sp.Matrix.hstack(k1, k2).rank() == 2

    for i, j, k in product((0, 1), (0, 1), range(3)):
        assert derivative.row(9 * i + 3 * j + k) == sp.zeros(1, 9)

    gamma = b * e(0) - a * e(1)
    assert (gamma.T * z)[0] == 0
    for i, j in product((0, 1), repeat=2):
        contracted = b * grid_value(i, j, 0) - a * grid_value(i, j, 1)
        expected = sp.zeros(27, 1)
        if i == j == 0:
            expected = b * target(0)
        elif i == j == 1:
            expected = -a * target(1)
        assert contracted == expected
        assert grid_value(i, j, 2) == sp.zeros(27, 1)

    # At z_s=0, the derivative's (s,s,s) coefficient is exactly
    # lambda*mu times the s coordinate of the third root input.  If q_s=0,
    # K has no such coordinate and neither J nor U can supply target T_s.
    same_colour_row = sp.zeros(1, 9)
    same_colour_row[0, 8] = lam * mu
    assert derivative.row(26) == same_colour_row
    print("support-two grid: PASS (rank 7 / contraction / same-colour gate)")


MONOMIALS = list(combinations_with_replacement(range(3), 3))


def plane_basis(normal: tuple[int, int, int]) -> list[sp.Matrix]:
    return [sp.Matrix(vector) for vector in sp.Matrix([normal]).nullspace()]


def symmetric_value(
    monomial: tuple[int, int, int],
    left: sp.Matrix,
    middle: sp.Matrix,
    right: sp.Matrix,
) -> sp.Expr:
    assignments = set(permutations(monomial))
    multiplicities = [monomial.count(index) for index in range(3)]
    multinomial = factorial(3)
    for multiplicity in multiplicities:
        multinomial //= factorial(multiplicity)
    return sp.simplify(
        sum(
            left[i] * middle[j] * right[k]
            for i, j, k in assignments
        )
        / multinomial
    )


def restriction_matrix(
    normals: tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ],
) -> sp.Matrix:
    bases = [plane_basis(normal) for normal in normals]
    return sp.Matrix(
        [
            [symmetric_value(monomial, r, p, q) for monomial in MONOMIALS]
            for r, p, q in product(*bases)
        ]
    )


def polynomial(vector: sp.Matrix) -> sp.Expr:
    x, y, z = sp.symbols("x y z")
    variables = (x, y, z)
    return sp.factor(
        sum(
            vector[index]
            * variables[monomial[0]]
            * variables[monomial[1]]
            * variables[monomial[2]]
            for index, monomial in enumerate(MONOMIALS)
        )
    )


def incidence_kernels() -> None:
    independent = restriction_matrix(
        ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    )
    assert independent.rank() == 7
    assert {str(polynomial(vector)) for vector in independent.nullspace()} == {
        "x**3",
        "y**3",
        "z**3",
    }

    pencil = restriction_matrix(
        ((1, 0, 0), (0, 1, 0), (1, 1, 0))
    )
    assert pencil.rank() == 7
    assert {str(polynomial(vector)) for vector in pencil.nullspace()} == {
        "x**3",
        "x*y*(x + y)",
        "y**3",
    }
    print("plane-incidence kernels: PASS (independent / pencil)")


def diagonal_divisor_step() -> None:
    a, b, c, d, t = sp.symbols("a b c d t", nonzero=True)
    x, y = sp.symbols("x y")
    first = sp.expand((a * x**3 + b * y**3).subs(x, -t * y))
    second = sp.expand((c * x**3 + d * y**3).subs(x, -t * y))
    assert sp.expand(first - (-a * t**3 + b) * y**3) == 0
    assert sp.expand(second - (-c * t**3 + d) * y**3) == 0
    assert sp.expand(a * d - b * c).subs(
        {b: a * t**3, d: c * t**3}
    ) == 0

    x0, x1, x2 = sp.symbols("x0 x1 x2")
    diagonal = a * x0**3 + b * x1**3 + c * x2**3
    assert [sp.diff(diagonal, variable) for variable in (x0, x1, x2)] == [
        3 * a * x0**2,
        3 * b * x1**2,
        3 * c * x2**2,
    ]
    print("diagonal divisor: PASS (shared quadratic fixes ratio)")


def equal_plane_orientations() -> None:
    l00, l01, l10, l11 = sp.symbols("l00 l01 l10 l11")
    matrix = sp.Matrix([[l00, l01], [l10, l11]])
    e00 = sp.Matrix([[1, 0], [0, 0]])
    e11 = sp.Matrix([[0, 0], [0, 1]])
    e10 = sp.Matrix([[0, 0], [1, 0]])

    def skew_entry(value: sp.Matrix) -> sp.Expr:
        return sp.expand(value[0, 1] - value[1, 0])

    # R=P: the two independent target coefficients separately force L
    # diagonal.
    assert sp.solve(
        [skew_entry(matrix * e00), skew_entry(matrix * e11)],
        (l10, l01),
        dict=True,
    ) == [{l01: 0, l10: 0}]

    # R=Q (and symmetrically P=Q): E00 and E10 kill the entire second row.
    solution = sp.solve(
        [skew_entry(matrix * e00), skew_entry(matrix * e10)],
        (l10, l11),
        dict=True,
    )
    assert solution == [{l10: 0, l11: 0}]
    assert sp.factor(matrix.det().subs(solution[0])) == 0
    print("equal-plane orientations: PASS (diagonal / singular cases)")


def inherited_square_atlas() -> None:
    x = source(0, e(0))
    y = source(1, e(0))
    z = source(2, e(0))
    t = source(2, e(1))
    u = x + y
    w = x - y

    nonconjugate = source(0, e(1))
    common = mixed_map(u, nonconjugate).col_join(mixed_map(u, t))
    nullspace = common.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(*nullspace, w).rank() == 1

    v = x + y + z
    q0 = x + y - 2 * z
    s0 = 2 * x + 3 * y + sp.Rational(5, 2) * z
    s1 = -x + 4 * y + sp.Rational(3, 2) * z
    assert polarized(s0, v, q0) == sp.zeros(27, 1)
    assert polarized(s1, v, q0) == sp.zeros(27, 1)
    print("two-plane square atlas: PASS (inherited two-/three-source charts)")


def main() -> None:
    complementary_support_grid()
    incidence_kernels()
    diagonal_divisor_step()
    equal_plane_orientations()
    inherited_square_atlas()
    print("repeated-coordinate support localization: PASS")


if __name__ == "__main__":
    main()
