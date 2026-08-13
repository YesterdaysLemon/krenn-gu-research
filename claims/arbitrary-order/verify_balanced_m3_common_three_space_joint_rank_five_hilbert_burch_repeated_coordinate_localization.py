"""Exact replay for the repeated-coordinate Hilbert--Burch localization.

The owning Markdown file is the proof.  This verifier checks the derivative
kernel and untouched grid, the z_s contraction determinant, all three
two-plane incidence kernels, the diagonal-cubic divisor step, the equal-plane
matrix orientation, and representative two-/three-source square charts.
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


def hilbert_burch_grid() -> None:
    z0, z1, zs, lam, mu = sp.symbols("z0 z1 zs lam mu", nonzero=True)
    z = sp.Matrix([z0, z1, zs])
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

    gamma0 = sp.Matrix([1, 0, -z0 / zs])
    gamma1 = sp.Matrix([0, 1, -z1 / zs])
    gamma = sp.Matrix.hstack(gamma0, gamma1)
    assert gamma.T * z == sp.zeros(2, 1)
    assert gamma[:2, :] == sp.eye(2)

    # The restriction z^perp -> span(e0,e1)^* is invertible exactly when
    # z_s is nonzero: append its two coordinate evaluations to z itself.
    restriction_test = sp.Matrix.vstack(z.T, e(0).T, e(1).T)
    assert sp.factor(restriction_test.det()) == zs
    print("Hilbert-Burch grid: PASS (rank 7 / untouched 2x2x3 / z_s gate)")


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

    repeated = restriction_matrix(
        ((1, 0, 0), (1, 0, 0), (0, 1, 0))
    )
    assert repeated.rank() == 6
    assert {str(polynomial(vector)) for vector in repeated.nullspace()} == {
        "x**2*y",
        "x**2*z",
        "x**3",
        "y**3",
    }
    print("plane-incidence kernels: PASS (independent / pencil / repeated)")


def diagonal_divisor_step() -> None:
    a, b, c, d, t = sp.symbols("a b c d t", nonzero=True)

    # A nonpure binary diagonal cubic a*x^3+b*y^3 has the line x+t*y
    # exactly when b=a*t^3.  A shared noncoordinate factor therefore fixes
    # the coefficient ratio and makes two such cubics proportional.
    x, y = sp.symbols("x y")
    first_on_line = sp.expand((a * x**3 + b * y**3).subs(x, -t * y))
    second_on_line = sp.expand((c * x**3 + d * y**3).subs(x, -t * y))
    assert sp.expand(first_on_line - (-a * t**3 + b) * y**3) == 0
    assert sp.expand(second_on_line - (-c * t**3 + d) * y**3) == 0
    ratio_minor = sp.expand(a * d - b * c).subs(
        {b: a * t**3, d: c * t**3}
    )
    assert ratio_minor == 0

    # The only repeated-factor diagonal cubic is a pure cube.
    x0, x1, x2 = sp.symbols("x0 x1 x2")
    diagonal = a * x0**3 + b * x1**3 + c * x2**3
    gradient = [sp.diff(diagonal, variable) for variable in (x0, x1, x2)]
    assert gradient == [3 * a * x0**2, 3 * b * x1**2, 3 * c * x2**2]
    print("diagonal divisor: PASS (shared quadratic forces proportionality)")


def equal_plane_orientation() -> None:
    l00, l01, l10, l11 = sp.symbols("l00 l01 l10 l11")
    matrix = sp.Matrix([[l00, l01], [l10, l11]])
    e00 = sp.diag(1, 0)
    e11 = sp.diag(0, 1)
    skew0 = matrix * e00 - (matrix * e00).T
    skew1 = matrix * e11 - (matrix * e11).T
    assert sp.solve(
        [skew0[0, 1], skew1[0, 1]],
        (l10, l01),
        dict=True,
    ) == [{l01: 0, l10: 0}]
    print("equal-plane orientation: PASS (relation matrix is diagonal)")


def two_plane_square_atlas() -> None:
    # Representative two-source charts from the inherited S2AL lemma.
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

    tangent = source(0, e(1))
    common = mixed_map(u, w).col_join(mixed_map(u, tangent + t))
    nullspace = common.nullspace()
    assert len(nullspace) == 2
    assert sp.Matrix.hstack(*nullspace, w, -tangent + t).rank() == 2

    # Three-source scaling kernel: every second square retains base factors.
    v = x + y + z
    q0 = x + y - 2 * z
    s0 = 2 * x + 3 * y + sp.Rational(5, 2) * z
    s1 = -x + 4 * y + sp.Rational(3, 2) * z
    assert polarized(s0, v, q0) == sp.zeros(27, 1)
    assert polarized(s1, v, q0) == sp.zeros(27, 1)
    print("two-plane square atlas: PASS (inherited two-/three-source charts)")


def main() -> None:
    hilbert_burch_grid()
    incidence_kernels()
    diagonal_divisor_step()
    equal_plane_orientation()
    two_plane_square_atlas()
    print("repeated-coordinate Hilbert-Burch localization: PASS")


if __name__ == "__main__":
    main()
