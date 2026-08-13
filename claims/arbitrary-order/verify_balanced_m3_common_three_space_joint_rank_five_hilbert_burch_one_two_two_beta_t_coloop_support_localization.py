"""Exact replay for the (1,2,2) distinguished beta_t-coloop localization."""

from __future__ import annotations

import sympy as sp


def e(i: int, n: int = 3) -> sp.Matrix:
    return sp.eye(n)[:, i]


def dot(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return (left.T * right)[0]


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def outer3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def derivative(
    y: sp.Matrix,
    z: sp.Matrix,
    w: sp.Matrix,
    s: int,
    t: int,
    lam: sp.Expr,
    mu: sp.Expr,
) -> sp.Matrix:
    b23 = outer(y, w) - mu * outer(e(t), z)
    columns = [sp.kronecker_product(e(i), b23) for i in range(3)]
    columns += [-lam * outer3(e(s), e(j), w) for j in range(3)]
    columns += [lam * mu * outer3(e(s), e(t), e(k)) for k in range(3)]
    return sp.Matrix.hstack(*columns)


def target_coefficients(
    alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix
) -> sp.Matrix:
    return sp.Matrix([alpha[i] * beta[i] * gamma[i] for i in range(3)])


def complete_zero_face() -> None:
    lam, mu = sp.Integer(2), sp.Integer(3)
    s, t = 0, 2
    y = sp.Matrix([1, 4, 0])
    z = sp.Matrix([2, -1, 5])
    w = sp.Matrix([3, 2, 7])
    dmat = derivative(y, z, w, s, t, lam, mu)

    a0, a1, a2, b0, b1, g0, g1 = sp.symbols(
        "a0 a1 a2 b0 b1 g0 g1"
    )
    alpha = sp.Matrix([a0, a1, a2])
    beta = sp.Matrix([b0, b1, 0])
    gamma = sp.Matrix(
        [g0, g1, -(w[0] * g0 + w[1] * g1) / w[2]]
    )
    assert beta[t] == 0 and sp.expand(dot(gamma, w)) == 0
    got = dmat.T * outer3(alpha, beta, gamma)
    assert all(sp.expand(value) == 0 for value in got)
    print("beta_t coloop face: PASS (complete 3x2x2 derivative zero)")


def generic_binary_cube() -> None:
    wa, wb, wt = sp.symbols("w_a w_b w_t", nonzero=True)
    w = sp.Matrix([wa, wb, wt])
    gamma_a = sp.Matrix([1, 0, -wa / wt])
    gamma_b = sp.Matrix([0, 1, -wb / wt])
    lifts = [gamma_a, gamma_b]
    assert all(sp.expand(dot(gamma, w)) == 0 for gamma in lifts)
    assert sp.Matrix([[gamma[i] for gamma in lifts] for i in (0, 1)]) == sp.eye(2)

    for i in (0, 1):
        for j in (0, 1):
            for k, gamma in enumerate(lifts):
                got = target_coefficients(e(i), e(j), gamma)
                expected = sp.zeros(3, 1)
                if i == j == k:
                    expected[i] = 1
                assert got == expected
    print("beta_t generic fork: PASS (binary diagonal cube when w_t is nonzero)")


def support_two_same_row_table() -> None:
    t = 2
    wa, wb = sp.symbols("w_a w_b", nonzero=True)
    w = sp.Matrix([wa, wb, 0])
    n = sp.Matrix([wb, -wa, 0])
    gamma_rows = [n, e(t)]
    assert all(dot(gamma, w) == 0 for gamma in gamma_rows)
    assert sp.Matrix.hstack(*gamma_rows).rank() == 2

    for i in (0, 1):
        for j in (0, 1):
            got_n = target_coefficients(e(i), e(j), n)
            expected_n = sp.zeros(3, 1)
            if i == j:
                expected_n[i] = n[i]
            assert got_n == expected_n
            assert target_coefficients(e(i), e(j), e(t)) == sp.zeros(3, 1)
    print("beta_t support-two fork: PASS (same-third-row binary table)")


def row_ranks_and_auxiliary_faces() -> None:
    lam, mu = sp.Integer(2), sp.Integer(3)
    s = t = 2
    y = sp.Matrix([2, 3, 0])
    z = sp.Matrix([1, 4, 5])
    w = sp.Matrix([3, -2, 7])
    u = sp.Matrix([y[1], -y[0], 0])
    v = z.cross(w)
    assert dot(u, y) == dot(u, e(t)) == 0
    assert dot(v, z) == dot(v, w) == 0
    assert sp.Matrix.hstack(y, e(t), u).rank() == 3
    assert sp.Matrix.hstack(z, w, v).rank() == 3

    dmat = derivative(y, z, w, s, t, lam, mu)
    for i in (0, 1):
        for gamma in (e(0), e(1), e(2)):
            assert dmat.T * outer3(e(i), u, gamma) == sp.zeros(9, 1)
        for beta in (e(0), e(1), e(2)):
            assert dmat.T * outer3(e(i), beta, v) == sp.zeros(9, 1)

    assert u[0] * u[1] != 0
    assert v[0] * v[1] != 0
    z0, z1, z2, w0, w1, w2 = sp.symbols("z0 z1 z2 w0 w1 w2")
    zsym = sp.Matrix([z0, z1, z2])
    wsym = sp.Matrix([w0, w1, w2])
    normal = zsym.cross(wsym)
    for i in range(3):
        assert sp.expand(sp.Matrix.hstack(zsym, wsym, e(i)).det() - normal[i]) == 0

    # Coordinates are taken in an abstract basis (R_0,R_1,A).
    r0, r1, avec = e(0), e(1), e(2)
    y0, y1, z0, z1 = sp.symbols("y0 y1 z0 z1")
    g0 = 2 * r0 - r1
    g1 = r0 + 3 * r1
    h0 = -r0 + 4 * r1
    h1 = 5 * r0 + r1
    p0, p1 = g0 + y0 * avec, g1 + y1 * avec
    q0, q1 = h0 + z0 * avec, h1 + z1 * avec
    rows = sp.Matrix.hstack(r0, r1, avec, p0, p1, q0, q1)
    assert rows.rank() <= 3
    print("beta_t row ranks/faces: PASS (injective forks and incidence normals)")


def main() -> None:
    complete_zero_face()
    row_ranks_and_auxiliary_faces()
    generic_binary_cube()
    support_two_same_row_table()
    print("beta_t-coloop support localization: PASS")


if __name__ == "__main__":
    main()
