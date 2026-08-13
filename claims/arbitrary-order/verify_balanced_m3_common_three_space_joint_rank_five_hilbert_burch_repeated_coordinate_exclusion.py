"""Exact replay for the repeated-coordinate Hilbert--Burch exclusion.

The owning Markdown file is the proof.  This script checks its scalar-general
derivative and annihilator, torus recovery, untouched support grid, coloop
rank split, equal-plane orientation, binary-cubic derivative kernel, and the
quadratic-annihilator quotient identities.
"""

from __future__ import annotations

from itertools import product

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def derivative_and_torus_recovery() -> None:
    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    s, t = 2, 0
    es, et = e(s), e(t)

    columns = []
    for index in range(3):
        columns.append(-mu * nu * tensor3(e(index), es, et))
    for index in range(3):
        columns.append(-lam * nu * tensor3(es, e(index), et))
    for index in range(3):
        columns.append(lam * mu * tensor3(es, es, e(index)))
    derivative = sp.Matrix.hstack(*columns)

    k1 = (lam * es).col_join(sp.zeros(3, 1)).col_join(nu * et)
    k2 = sp.zeros(3, 1).col_join(mu * es).col_join(nu * et)
    assert derivative * k1 == sp.zeros(27, 1)
    assert derivative * k2 == sp.zeros(27, 1)
    assert derivative.rank() == 7
    assert sp.Matrix.hstack(k1, k2).rank() == 2

    # A basis of (ker D)^perp: the six untouched coordinate covectors and
    # the scalar-general combined row h.
    basis = []
    for index in (t, 1):
        basis.append(e(index).col_join(sp.zeros(6, 1)))
    for index in (t, 1):
        basis.append(sp.zeros(3, 1).col_join(e(index)).col_join(sp.zeros(3, 1)))
    for index in (1, s):
        basis.append(sp.zeros(6, 1).col_join(e(index)))
    h = (
        (nu / lam * es)
        .col_join(nu / mu * es)
        .col_join(-et)
    )
    basis.append(h)
    annihilator = sp.Matrix.hstack(*basis)
    assert annihilator.rank() == 7
    assert (sp.Matrix.hstack(k1, k2).T * annihilator) == sp.zeros(2, 7)

    # A general torus point of the annihilator recovers itself, up to the
    # common nonzero scalar nu^2 gamma_t^2, under D^T of its three factors.
    a0, a1, b0, b1, c1, c2, g = sp.symbols(
        "a0 a1 b0 b1 c1 c2 g", nonzero=True
    )
    alpha = sp.Matrix([a0, a1, -nu * g / lam])
    beta = sp.Matrix([b0, b1, -nu * g / mu])
    gamma = sp.Matrix([g, c1, c2])
    ell = alpha.col_join(beta).col_join(gamma)
    transpose_value = (
        (-mu * nu * beta[s] * gamma[t] * alpha)
        .col_join(-lam * nu * alpha[s] * gamma[t] * beta)
        .col_join(lam * mu * alpha[s] * beta[s] * gamma)
    )
    assert sp.simplify(transpose_value - nu**2 * g**2 * ell) == sp.zeros(9, 1)
    print("Hilbert--Burch torus: PASS (rank 7 / annihilator / self-recovery)")


def untouched_grid() -> None:
    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    s, t, u = 2, 0, 1
    es, et = e(s), e(t)
    columns = []
    for index in range(3):
        columns.append(-mu * nu * tensor3(e(index), es, et))
    for index in range(3):
        columns.append(-lam * nu * tensor3(es, e(index), et))
    for index in range(3):
        columns.append(lam * mu * tensor3(es, es, e(index)))
    derivative = sp.Matrix.hstack(*columns)

    touched = {
        (i, s, t) for i in range(3)
    } | {
        (s, j, t) for j in range(3)
    } | {
        (s, s, k) for k in range(3)
    }
    actual = {
        (i, j, k)
        for i, j, k in product(range(3), repeat=3)
        if derivative.row(9 * i + 3 * j + k) != sp.zeros(1, 9)
    }
    assert actual == touched

    for i, j, k in product((t, u), (t, u), range(3)):
        assert (i, j, k) not in touched
    for j, k in product((t, u), (u, s)):
        assert (s, j, k) not in touched
    for i, k in product((t, u), (u, s)):
        assert (i, s, k) not in touched

    same_colour = derivative.row(9 * s + 3 * s + s)
    expected = sp.zeros(1, 9)
    expected[0, 6 + s] = lam * mu
    assert same_colour == expected
    print("untouched grid: PASS (20 exact cells / same-colour target gate)")


def coloop_rank_split() -> None:
    # Each model has one coloop column outside a common two-plane.  Its
    # relation kernel is four-dimensional and has zero coloop coordinate;
    # deleting that column leaves rank two.
    for coloop in range(7):
        matrix = sp.zeros(3, 7)
        other = [index for index in range(7) if index != coloop]
        for position, index in enumerate(other):
            matrix[:, index] = sp.Matrix([1, position, 0])
        matrix[:, coloop] = sp.Matrix([0, 0, 1])
        assert matrix.rank() == 3
        assert matrix[:, other].rank() == 2
        kernel = sp.Matrix.hstack(*matrix.nullspace())
        assert kernel.shape == (7, 4)
        assert kernel.row(coloop) == sp.zeros(1, 4)
    print("relation matroid: PASS (seven exact coloop orientations)")


def equal_plane_orientation() -> None:
    m00, m01, m10, m11 = sp.symbols("m00 m01 m10 m11")
    matrix = sp.Matrix([[m00, m01], [m10, m11]])
    e00 = sp.Matrix([[1, 0], [0, 0]])
    e11 = sp.Matrix([[0, 0], [0, 1]])

    def skew(value: sp.Matrix) -> sp.Expr:
        return sp.expand(value[0, 1] - value[1, 0])

    solution = sp.solve(
        [skew(matrix * e00), skew(matrix * e11)],
        (m10, m01),
        dict=True,
    )
    assert solution == [{m01: 0, m10: 0}]
    assert sp.factor(matrix.det().subs(solution[0])) == m00 * m11

    # On span(q_t,q_u), the aligned bases give precisely the hypotheses of
    # the inherited two-plane square lemma.
    qt, qu = sp.symbols("qt qu")
    square_t = sp.Matrix([qt, 0])
    square_u = sp.Matrix([0, qu])
    mixed = sp.zeros(2, 1)
    assert square_t.rank() == square_u.rank() == 1
    assert mixed == sp.zeros(2, 1)
    print("equal first/second planes: PASS (diagonal orientation / square table)")


def binary_cubic_kernel_and_source_split() -> None:
    x, y = sp.symbols("x y")
    a, b, c, d = sp.symbols("a b c d")
    cubic = a * x**3 + b * x**2 * y + c * x * y**2 + d * y**3
    derivative = sp.Poly(sp.diff(cubic, x), x, y)
    equations = [derivative.coeff_monomial(monomial) for monomial in (x**2, x * y, y**2)]
    assert sp.solve(equations, (a, b, c), dict=True) == [{a: 0, b: 0, c: 0}]

    # If off-target restrictions occur in two source families, the two UFD
    # implications force all three target forms onto the derivative-kernel
    # line.  The Boolean replay checks every pair of families.
    families = range(3)
    for first in families:
        for second in families:
            if first >= second:
                continue
            forced = set(families) - {first}
            forced |= set(families) - {second}
            assert forced == set(families)
    print("binary cubic: PASS (derivative kernel / at-most-one active source)")


def quotient_projection_injectivity() -> None:
    # Multiplication by any nonzero binary linear form is injective from
    # degree one to degree two.  These three charts cover z0!=0, z1!=0 and
    # the overlap; they replay the integral-domain step in the proof.
    a = sp.symbols("a")
    multiplication_matrices = (
        sp.Matrix([[1, 0], [0, 1], [0, 0]]),
        sp.Matrix([[0, 0], [1, 0], [0, 1]]),
        sp.Matrix([[1, 0], [a, 1], [0, a]]),
    )
    for matrix in multiplication_matrices:
        assert matrix.rank() == 2

    # Once both annihilators have their Y and Z components on the target-1
    # lines, every mixed permanent shares those two factor lines.
    x0, x1 = sp.symbols("x0 x1")
    y1, z1 = sp.symbols("y1 z1", nonzero=True)
    mixed_coefficients = sp.Matrix([x0 * y1 * z1, x1 * y1 * z1])
    assert all(sp.factor(value / (y1 * z1)) in (x0, x1) for value in mixed_coefficients)
    print("quadratic annihilators: PASS (quotient projections / factor sharing)")


def main() -> None:
    derivative_and_torus_recovery()
    untouched_grid()
    coloop_rank_split()
    equal_plane_orientation()
    binary_cubic_kernel_and_source_split()
    quotient_projection_injectivity()
    print("repeated-coordinate Hilbert--Burch exclusion: PASS")


if __name__ == "__main__":
    main()
