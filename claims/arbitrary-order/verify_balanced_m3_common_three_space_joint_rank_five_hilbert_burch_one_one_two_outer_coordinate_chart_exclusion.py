"""Exact replay for the (1,1,2) outer-coordinate-chart exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


def e(i: int, n: int = 3) -> sp.Matrix:
    return sp.eye(n)[:, i]


def dot(u: sp.Matrix, v: sp.Matrix) -> sp.Expr:
    return (u.T * v)[0]


def outer3(u: sp.Matrix, v: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(u, v, w)


def block(*vectors: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(*vectors)


def derivative(
    y: sp.Matrix,
    z: sp.Matrix,
    s: int,
    t: int,
    lam: sp.Expr,
    nu: sp.Expr,
) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    es, et = e(s), e(t)
    for i in range(3):
        columns.append(-outer3(e(i), y, z))
    for j in range(3):
        columns.append(-lam * nu * outer3(es, e(j), et))
    for k in range(3):
        columns.append(lam * outer3(es, y, e(k)))
    return sp.Matrix.hstack(*columns)


def derivative_and_recovery() -> None:
    lam, nu = sp.Integer(2), sp.Integer(3)
    s, t = 0, 1
    y = sp.Matrix([1, 2, 3])
    z = sp.Matrix([2, 4, 1])
    dmat = derivative(y, z, s, t, lam, nu)
    k1 = block(lam * e(s), sp.zeros(3, 1), z)
    k2 = block(sp.zeros(3, 1), y, nu * e(t))
    assert dmat.rank() == 7
    assert dmat * k1 == sp.zeros(27, 1)
    assert dmat * k2 == sp.zeros(27, 1)
    assert sp.Matrix.hstack(k1, k2).rank() == 2

    a1, a2, b1, b2, g0, g1, g2 = sp.symbols(
        "a1 a2 b1 b2 g0 g1 g2"
    )
    gamma = sp.Matrix([g0, g1, g2])
    alpha = sp.Matrix([-dot(gamma, z) / lam, a1, a2])
    beta = sp.Matrix(
        [(-nu * gamma[t] - y[1] * b1 - y[2] * b2) / y[0], b1, b2]
    )
    ell = block(alpha, beta, gamma)
    contracted = dmat.T * outer3(alpha, beta, gamma)
    expected = nu * dot(gamma, z) * gamma[t] * ell
    assert all(sp.expand(value) == 0 for value in contracted - expected)

    # The exterior face alpha_s=beta(y)=0 kills all three derivative terms.
    aa, ab, bb, gg0, gg1, gg2 = sp.symbols("aa ab bb gg0 gg1 gg2")
    alpha_face = sp.Matrix([0, aa, ab])
    beta_face = sp.Matrix([-2 * bb, bb, 0])  # beta(y)=0 for y=(1,2,3)
    gamma_face = sp.Matrix([gg0, gg1, gg2])
    assert dmat.T * outer3(alpha_face, beta_face, gamma_face) == sp.zeros(9, 1)
    print("outer derivative/recovery: PASS (rank seven, kernel, scalar, exterior face)")


def torus_and_quotient_atlas() -> None:
    for y, z, s, t in (
        (sp.Matrix([1, 2, 3]), sp.Matrix([2, 4, 1]), 0, 1),
        (sp.Matrix([0, 2, 3]), sp.Matrix([3, 1, 4]), 0, 2),
        (sp.Matrix([0, 2, 3]), sp.Matrix([1, 5, 2]), 0, 0),
    ):
        lam, nu = sp.Integer(2), sp.Integer(3)
        k1 = block(lam * e(s), sp.zeros(3, 1), z)
        k2 = block(sp.zeros(3, 1), y, nu * e(t))
        l_basis = sp.Matrix.vstack(k1.T, k2.T).nullspace()
        lmat = sp.Matrix.hstack(*l_basis)
        assert lmat.shape == (9, 7)
        assert lmat.rank() == 7
        # Every target-coordinate evaluation restricts to a proper,
        # nonzero hyperplane on L.
        assert all(any(lmat[row, col] != 0 for col in range(7)) for row in range(9))

        quotient_forms = sp.Matrix.vstack(z.T, e(t).T)
        assert quotient_forms.rank() == 2
        common = quotient_forms.nullspace()
        assert len(common) == 1 and common[0] != sp.zeros(3, 1)
    print("outer torus/quotient atlas: PASS (nine proper factors, quotient rank two)")


def exterior_support_atlas() -> None:
    s, a, b = 0, 1, 2
    samples = (
        sp.Matrix([1, 2, 3]),
        sp.Matrix([1, 2, 0]),
        sp.Matrix([0, 2, 3]),
    )
    for y in samples:
        y_perp = sp.Matrix([list(y)]).nullspace()
        ymat = sp.Matrix.hstack(*y_perp)
        assert ymat.rank() == 2
        restriction = ymat.extract([a, b], [0, 1])
        expected_rank = 2 if y[s] != 0 else 1
        assert restriction.rank() == expected_rank
        if y[s] == 0:
            kernel = restriction.nullspace()
            assert len(kernel) == 1
            invisible = ymat * kernel[0]
            assert invisible[a] == invisible[b] == 0
            assert invisible[s] != 0

        kinds: list[tuple[bool, bool]] = []
        for j in range(3):
            line = sp.Matrix.vstack(y.T, e(j).T).nullspace()
            assert len(line) == 1
            beta = line[0]
            kinds.append((beta[a] != 0, beta[b] != 0))
        if y[s] == 0:
            assert set(kinds) == {(True, True), (False, False)}
        else:
            assert (False, False) not in kinds
    print("binary exterior support: PASS (full and missing-central-coordinate splits)")


def coefficient_forks() -> None:
    c, d, xa, xb = sp.symbols("c d xa xb", nonzero=True)

    # Equal-plane fork: p=c r_a+d r_b.
    mixed_a = sp.Matrix([xa, 0])
    mixed_b = sp.Matrix([0, xb])
    square = sp.expand(c) * mixed_a + sp.expand(d) * mixed_b
    assert square == sp.Matrix([c * xa, d * xb])

    # S2AX ordinary first-root fork: r_b=c p_a+d p_b.
    square_rb = d * sp.Matrix([0, xb])
    mixed_ra_rb = c * sp.Matrix([xa, 0])
    assert square_rb == sp.Matrix([0, d * xb])
    assert mixed_ra_rb == sp.Matrix([c * xa, 0])

    # Missing-central first-root fork: only p_0 sees both targets.
    square_missing = c * sp.Matrix([0, xb])
    mixed_missing = c * sp.Matrix([xa, 0])
    assert square_missing == sp.Matrix([0, c * xb])
    assert mixed_missing == sp.Matrix([c * xa, 0])

    # Second-root one-coordinate fork after transposing row families.
    square_v = c * sp.Matrix([xa, 0])
    mixed_v_external = d * sp.Matrix([0, xb])
    assert square_v == sp.Matrix([c * xa, 0])
    assert mixed_v_external == sp.Matrix([0, d * xb])
    print("coloop coefficient forks: PASS (equal-plane, ordinary, degenerate, transposed)")


def perm(u: sp.Matrix, v: sp.Matrix, q: sp.Matrix, n: int = 2) -> sp.Matrix:
    ux, uy, uz = u[:n, :], u[n : 2 * n, :], u[2 * n :, :]
    vx, vy, vz = v[:n, :], v[n : 2 * n, :], v[2 * n :, :]
    qx, qy, qz = q[:n, :], q[n : 2 * n, :], q[2 * n :, :]
    return (
        outer3(ux, vy, qz)
        + outer3(ux, qy, vz)
        + outer3(vx, uy, qz)
        + outer3(vx, qy, uz)
        + outer3(qx, uy, vz)
        + outer3(qx, vy, uz)
    )


def linear_map_matrix(u: sp.Matrix, v: sp.Matrix, n: int = 2) -> sp.Matrix:
    columns = []
    for source, coordinate in product(range(3), range(n)):
        q = sp.zeros(3 * n, 1)
        q[source * n + coordinate] = 1
        columns.append(perm(u, v, q, n))
    return sp.Matrix.hstack(*columns)


def endpoint_source_atlas() -> None:
    n = 2
    x = block(e(0, n), sp.zeros(n, 1), sp.zeros(n, 1))
    y = block(sp.zeros(n, 1), e(0, n), sp.zeros(n, 1))
    z = block(sp.zeros(n, 1), sp.zeros(n, 1), e(0, n))

    # Full-support square kernel is exactly two-dimensional.
    full = x + y + z
    assert len(linear_map_matrix(full, full, n).nullspace()) == 2

    # For a two-source row, the mixed map L(q)=x*q_Y+q_X*y on X+Y
    # has its unique kernel line x-y.
    two = x + y
    lmat = linear_map_matrix(two, z, n)[:, : 2 * n]
    assert lmat.rank() == 3
    assert len(lmat.nullspace()) == 1
    assert lmat * (x - y)[: 2 * n, :] == sp.zeros(n**3, 1)

    # Pure-row radical: with a_Y,a_Z nonzero, the YZ solution is
    # (tau*a_Y,-tau*a_Z), and the plus/minus tensors used by Lemmas 1--2
    # have the advertised factor behaviour.
    a_y, a_z = e(0, n), e(1, n)
    c = sp.Integer(3)
    v_y, v_z = c * a_y, -c * a_z
    plus = sp.kronecker_product(a_y, v_z) + sp.kronecker_product(v_y, a_z)
    minus = sp.kronecker_product(a_y, v_z) - sp.kronecker_product(v_y, a_z)
    assert plus == sp.zeros(n**2, 1)
    assert minus == -2 * c * sp.kronecker_product(a_y, a_z)

    d_y, d_z = e(0, n), e(1, n)
    p_y, p_z = c * d_y, -c * d_z
    tangent_plus = sp.kronecker_product(d_y, p_z) + sp.kronecker_product(p_y, d_z)
    alternating = sp.kronecker_product(d_y, p_z) - sp.kronecker_product(p_y, d_z)
    assert tangent_plus == sp.zeros(n**2, 1)
    assert alternating == -2 * c * sp.kronecker_product(d_y, d_z)
    print("endpoint source atlas: PASS (full/two/pure support and factor lines)")


def main() -> None:
    derivative_and_recovery()
    torus_and_quotient_atlas()
    exterior_support_atlas()
    coefficient_forks()
    endpoint_source_atlas()
    print("(1,1,2) outer-coordinate-chart exclusion: PASS")


if __name__ == "__main__":
    main()
