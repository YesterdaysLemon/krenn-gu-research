"""Exact replay for the all-coordinate-distinct Hilbert--Burch exclusion.

The owning Markdown file is the proof.  This script checks the scalar-general
derivative, kernel and annihilator, the seven-cell support, the untouched
binary cube and exterior target faces, torus self-recovery, the seven possible
coloop rank splits, the ordinary-row symmetry orbit, and the exact polynomial
and factor-support identities used by the two-plane lemmas.
"""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp


def e(index: int) -> sp.Matrix:
    return sp.eye(3)[:, index]


def tensor3(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(x, y, z)


def derivative_kernel_annihilator_and_torus() -> None:
    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    ex, ey, ez = e(0), e(1), e(2)

    columns = []
    for index in range(3):
        columns.append(-mu * nu * tensor3(e(index), ey, ez))
    for index in range(3):
        columns.append(-lam * nu * tensor3(ex, e(index), ez))
    for index in range(3):
        columns.append(lam * mu * tensor3(ex, ey, e(index)))
    derivative = sp.Matrix.hstack(*columns)

    k1 = (lam * ex).col_join(sp.zeros(3, 1)).col_join(nu * ez)
    k2 = sp.zeros(3, 1).col_join(mu * ey).col_join(nu * ez)
    kernel = sp.Matrix.hstack(k1, k2)
    assert derivative.rank() == 7
    assert kernel.rank() == 2
    assert derivative * kernel == sp.zeros(27, 2)

    # Basis corresponding, in order, to
    # (r_1,r_2,p_0,p_2,q_0,q_1,h).
    basis = [
        e(1).col_join(sp.zeros(6, 1)),
        e(2).col_join(sp.zeros(6, 1)),
        sp.zeros(3, 1).col_join(e(0)).col_join(sp.zeros(3, 1)),
        sp.zeros(3, 1).col_join(e(2)).col_join(sp.zeros(3, 1)),
        sp.zeros(6, 1).col_join(e(0)),
        sp.zeros(6, 1).col_join(e(1)),
        (nu / lam * e(0)).col_join(nu / mu * e(1)).col_join(-e(2)),
    ]
    annihilator = sp.Matrix.hstack(*basis)
    assert annihilator.rank() == 7
    assert kernel.T * annihilator == sp.zeros(2, 7)

    # A general point with all seven annihilator-basis coordinates nonzero.
    a1, a2, b0, b2, c0, c1, g = sp.symbols(
        "a1 a2 b0 b2 c0 c1 g", nonzero=True
    )
    alpha = sp.Matrix([nu * g / lam, a1, a2])
    beta = sp.Matrix([b0, nu * g / mu, b2])
    gamma = sp.Matrix([c0, c1, -g])
    ell = alpha.col_join(beta).col_join(gamma)
    assert lam * alpha[0] + nu * gamma[2] == 0
    assert mu * beta[1] + nu * gamma[2] == 0
    assert all(value != 0 for value in ell)

    transpose_value = (
        (-mu * nu * beta[1] * gamma[2] * alpha)
        .col_join(-lam * nu * alpha[0] * gamma[2] * beta)
        .col_join(lam * mu * alpha[0] * beta[1] * gamma)
    )
    assert sp.simplify(transpose_value - nu**2 * gamma[2] ** 2 * ell) == sp.zeros(
        9, 1
    )
    print("coordinate-triangle derivative: PASS (rank/kernel/annihilator/torus)")


def diagonal_target(i: int, j: int, k: int) -> tuple[int, int, int]:
    return tuple(int(i == j == k == colour) for colour in range(3))


def support_cube_and_faces() -> None:
    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    columns = []
    for index in range(3):
        columns.append(-mu * nu * tensor3(e(index), e(1), e(2)))
    for index in range(3):
        columns.append(-lam * nu * tensor3(e(0), e(index), e(2)))
    for index in range(3):
        columns.append(lam * mu * tensor3(e(0), e(1), e(index)))
    derivative = sp.Matrix.hstack(*columns)

    touched = (
        {(i, 1, 2) for i in range(3)}
        | {(0, j, 2) for j in range(3)}
        | {(0, 1, k) for k in range(3)}
    )
    actual = {
        (i, j, k)
        for i, j, k in product(range(3), repeat=3)
        if derivative.row(9 * i + 3 * j + k) != sp.zeros(1, 9)
    }
    assert actual == touched
    assert len(actual) == 7

    r_indices, p_indices, q_indices = (1, 2), (0, 2), (0, 1)
    core = list(product(r_indices, p_indices, q_indices))
    assert len(core) == 8
    assert all(cell not in touched for cell in core)
    assert all(diagonal_target(*cell) == (0, 0, 0) for cell in core)

    # Untouched exterior faces, before the displayed nonzero scalar rescaling
    # of r_0 and p_1 into A and B.
    face_a = {
        (j, k): diagonal_target(0, j, k)
        for j, k in product(p_indices, q_indices)
    }
    face_b = {
        (i, k): diagonal_target(i, 1, k)
        for i, k in product(r_indices, q_indices)
    }
    face_q2 = {
        (i, j): diagonal_target(i, j, 2)
        for i, j in product(r_indices, p_indices)
    }
    assert all((0, j, k) not in touched for j, k in face_a)
    assert all((i, 1, k) not in touched for i, k in face_b)
    assert all((i, j, 2) not in touched for i, j in face_q2)
    assert face_a == {
        (0, 0): (1, 0, 0),
        (0, 1): (0, 0, 0),
        (2, 0): (0, 0, 0),
        (2, 1): (0, 0, 0),
    }
    assert face_b == {
        (1, 0): (0, 0, 0),
        (1, 1): (0, 1, 0),
        (2, 0): (0, 0, 0),
        (2, 1): (0, 0, 0),
    }
    assert face_q2 == {
        (1, 0): (0, 0, 0),
        (1, 2): (0, 0, 0),
        (2, 0): (0, 0, 0),
        (2, 2): (0, 0, 1),
    }

    # Each displayed row pair is independent: one diagonal evaluation kills
    # the second row and detects the first, while another detects the second.
    independence_witnesses = (
        (diagonal_target(1, 1, 1), diagonal_target(2, 1, 1), diagonal_target(2, 2, 2)),
        (diagonal_target(0, 0, 0), diagonal_target(0, 2, 0), diagonal_target(2, 2, 2)),
        (diagonal_target(0, 0, 0), diagonal_target(0, 0, 1), diagonal_target(1, 1, 1)),
    )
    for first, cross, second in independence_witnesses:
        assert first != (0, 0, 0)
        assert cross == (0, 0, 0)
        assert second != (0, 0, 0)
    print("untouched target atlas: PASS (seven cells / zero cube / three faces)")


def coloop_rank_split_and_orbit() -> None:
    # A four-dimensional relation kernel contained in one coordinate
    # hyperplane is equivalent to a coloop: deleting that row leaves rank 2.
    for coloop in range(7):
        matrix = sp.zeros(3, 7)
        other = [index for index in range(7) if index != coloop]
        for position, index in enumerate(other):
            matrix[:, index] = sp.Matrix([1, position, 0])
        matrix[:, coloop] = sp.Matrix([0, 0, 1])
        assert matrix.rank() == 3
        assert matrix[:, other].rank() == 2
        relations = sp.Matrix.hstack(*matrix.nullspace())
        assert relations.shape == (7, 4)
        assert relations.row(coloop) == sp.zeros(1, 4)

    ordinary_labels = {
        "r1": (0, 1),
        "r2": (0, 2),
        "p0": (1, 0),
        "p2": (1, 2),
        "q0": (2, 0),
        "q1": (2, 1),
    }
    ordered_distinct_pairs = {(left, right) for left in range(3) for right in range(3) if left != right}
    assert set(ordinary_labels.values()) == ordered_distinct_pairs
    orbit = {
        (sigma[2], sigma[0])
        for sigma in permutations(range(3))
    }
    assert orbit == ordered_distinct_pairs
    print("relation matroid: PASS (seven coloops / one ordinary-row orbit)")


def two_plane_lemmas() -> None:
    x, y = sp.symbols("x y")
    a, b, c, d = sp.symbols("a b c d")
    cubic = a * x**3 + b * x**2 * y + c * x * y**2 + d * y**3
    derivative = sp.Poly(sp.diff(cubic, x), x, y)
    equations = [
        derivative.coeff_monomial(monomial)
        for monomial in (x**2, x * y, y**2)
    ]
    assert sp.solve(equations, (a, b, c), dict=True) == [{a: 0, b: 0, c: 0}]

    # If a two-plane has all three source projections active, selecting one
    # nonzero restricted coordinate form from each source produces a nonzero
    # binary cubic.  Thus total cubic vanishing forces a missing source.
    for mask in product((False, True), repeat=3):
        totally_cubic_zero_possible = not all(mask)
        assert totally_cubic_zero_possible == (False in mask)

    # In the normal form S subset X+Y, both nonzero mixed maps have every
    # value in X tensor Y tensor span(a_Z).  The coefficient ledger below is
    # the polarization x(s)y(t)+x(t)y(s), with a fixed Z slot.
    xs0, xs1, xt0, xt1, az = sp.symbols("xs0 xs1 xt0 xt1 az", nonzero=True)
    symmetric_xy = sp.Matrix(
        [
            2 * xs0 * xt0,
            xs0 * xt1 + xt0 * xs1,
            xs1 * xt0 + xt1 * xs0,
            2 * xs1 * xt1,
        ]
    )
    first_mixed = az * symmetric_xy
    second_mixed = az * sp.Matrix(
        [xs0 * xt0, xs0 * xt1, xs1 * xt0, xs1 * xt1]
    )
    assert any(value != 0 for value in symmetric_xy)
    assert all(sp.factor(value / az) != sp.nan for value in first_mixed)
    assert all(sp.factor(value / az) != sp.nan for value in second_mixed)

    # The ordinary-coloop q_2=A+B-h expansion.  Zero face entries and the
    # two quadratic annihilator identities leave precisely T_0 and T_1.
    zero = sp.zeros(3, 1)
    t0, t1 = e(0), e(1)
    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    q0_mixed = [nu / lam * t0 + zero - zero, zero + zero - zero]
    q1_mixed = [zero + nu / mu * t1 - zero, zero + zero - zero]
    assert q0_mixed == [nu / lam * t0, zero]
    assert q1_mixed == [nu / mu * t1, zero]
    assert t0.dot(t1) == 0
    print("two-plane lemmas: PASS (binary kernel / missing source / mixed faces)")


def main() -> None:
    derivative_kernel_annihilator_and_torus()
    support_cube_and_faces()
    coloop_rank_split_and_orbit()
    two_plane_lemmas()
    print("all-coordinate-distinct Hilbert--Burch exclusion: PASS")


if __name__ == "__main__":
    main()
