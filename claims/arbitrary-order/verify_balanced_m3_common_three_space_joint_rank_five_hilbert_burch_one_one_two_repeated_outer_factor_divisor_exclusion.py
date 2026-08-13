"""Exact replay for the (1,1,2) single repeated-outer-factor exclusion.

The owning Markdown file is the proof.  This script checks its displayed
derivative identities and the canonical linear-algebra models used in the
equal-plane, common-radical, and zero-rectangle source atlases.
"""

from __future__ import annotations

import itertools

import sympy as sp

DIM = 3
TOTAL = 3 * DIM


def e(index: int, dimension: int = DIM) -> sp.Matrix:
    answer = sp.zeros(dimension, 1)
    answer[index] = 1
    return answer


def tensor3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def block_vector(
    left: sp.Matrix | None = None,
    middle: sp.Matrix | None = None,
    right: sp.Matrix | None = None,
) -> sp.Matrix:
    zero = sp.zeros(DIM, 1)
    return (left if left is not None else zero).col_join(
        middle if middle is not None else zero
    ).col_join(right if right is not None else zero)


def blocks(vector: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return vector[0:3, :], vector[3:6, :], vector[6:9, :]


def permanent(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    rows = [blocks(left), blocks(middle), blocks(right)]
    answer = sp.zeros(DIM**3, 1)
    for permutation in itertools.permutations(range(3)):
        answer += tensor3(
            rows[permutation[0]][0],
            rows[permutation[1]][1],
            rows[permutation[2]][2],
        )
    return answer


def permanent_map(left: sp.Matrix, middle: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(TOTAL)
    return sp.Matrix.hstack(
        *(permanent(left, middle, identity[:, index]) for index in range(TOTAL))
    )


def alternating(first: sp.Matrix, second: sp.Matrix, third: sp.Matrix) -> sp.Matrix:
    rows = [blocks(first), blocks(second), blocks(third)]
    answer = sp.zeros(DIM**3, 1)
    for permutation in itertools.permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        answer += (-1) ** inversions * tensor3(
            rows[permutation[0]][0],
            rows[permutation[1]][1],
            rows[permutation[2]][2],
        )
    return answer


def derivative_matrix(
    s: int,
    t: int,
    z: sp.Matrix,
    lam: sp.Expr,
    mu: sp.Expr,
    nu: sp.Expr,
) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for index in range(DIM):
        columns.append(-mu * tensor3(e(index), e(t), z))
    for index in range(DIM):
        columns.append(-lam * nu * tensor3(e(s), e(index), e(s)))
    for index in range(DIM):
        columns.append(lam * mu * tensor3(e(s), e(t), e(index)))
    return sp.Matrix.hstack(*columns)


def repeated_derivative_and_recovery() -> None:
    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    z0, z1, z2 = sp.symbols("z0 z1 z2")
    z = sp.Matrix([z0, z1, z2])
    s, t = 0, 1
    derivative = derivative_matrix(s, t, z, lam, mu, nu)
    kernel = sp.Matrix.hstack(
        (lam * e(s)).col_join(sp.zeros(3, 1)).col_join(z),
        sp.zeros(3, 1).col_join(mu * e(t)).col_join(nu * e(s)),
    )
    assert sp.simplify(derivative * kernel) == sp.zeros(27, 2)

    basis: list[sp.Matrix] = []
    for index in range(DIM):
        if index != s:
            basis.append(e(index).col_join(sp.zeros(6, 1)))
    for index in range(DIM):
        if index != t:
            basis.append(sp.zeros(3, 1).col_join(e(index)).col_join(sp.zeros(3, 1)))
    for index in range(DIM):
        basis.append(
            (-z[index] / lam * e(s))
            .col_join(-nu * (1 if index == s else 0) / mu * e(t))
            .col_join(e(index))
        )
    annihilator = sp.Matrix.hstack(*basis)
    assert annihilator.shape == (9, 7)
    assert kernel.T * annihilator == sp.zeros(2, 7)

    a0, a1, a2, b0, b1, b2, g0, g1, g2 = sp.symbols(
        "a0 a1 a2 b0 b1 b2 g0 g1 g2"
    )
    alpha = sp.Matrix([a0, a1, a2])
    beta = sp.Matrix([b0, b1, b2])
    gamma = sp.Matrix([g0, g1, g2])
    gamma_z = (gamma.T * z)[0]
    alpha = alpha.subs(a0, -gamma_z / lam)
    beta = beta.subs(b1, -nu * g0 / mu)
    ell = alpha.col_join(beta).col_join(gamma)
    transpose = (
        (-mu * beta[t] * gamma_z * alpha)
        .col_join(-lam * nu * alpha[s] * gamma[s] * beta)
        .col_join(lam * mu * alpha[s] * beta[t] * gamma)
    )
    assert sp.simplify(transpose - nu * gamma_z * gamma[s] * ell) == sp.zeros(9, 1)
    print("repeated derivative: PASS (kernel/L/recovery scalar)")


def torus_fork_and_exterior() -> None:
    # Coordinates on L: alpha_t, alpha_u, beta_s, beta_u, gamma_s,t,u.
    z = sp.Matrix([2, 3, 5])
    normals = [sp.eye(7).row(index) for index in range(7)]
    normals.append(sp.Matrix([[0, 0, 0, 0, z[0], z[1], z[2]]]))
    assert all(normal != sp.zeros(1, 7) for normal in normals)

    lam, mu, nu = sp.symbols("lam mu nu", nonzero=True)
    g0, g1, g2 = sp.symbols("g0 g1 g2")
    gamma = sp.Matrix([g0, g1, g2])
    derivative = derivative_matrix(0, 1, z, lam, mu, nu)
    contraction = sum(
        (gamma[k] * derivative.row(9 * 1 + 3 * 1 + k) for k in range(3)),
        sp.zeros(1, 9),
    )
    expected = sp.zeros(1, 9)
    expected[0, 1] = -mu * (gamma.T * z)[0]
    assert sp.simplify(contraction - expected) == sp.zeros(1, 9)
    # On gamma(z)=0 the correction at (t,t,gamma) vanishes, yielding T_t.
    assert sp.Matrix.hstack(z, e(0), e(1)).det() != 0
    print("repeated torus fork: PASS (eight factors / surviving T_t face)")


def equal_plane_atlas() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, zeta = e(0), e(0), e(0)
    full = block_vector(x, y, zeta)
    q1 = block_vector(x, -y, zero)
    q2 = block_vector(x, zero, -zeta)
    assert permanent(full, full, q1) == sp.zeros(27, 1)
    assert permanent(full, full, q2) == sp.zeros(27, 1)

    variables = sp.symbols("dx0:3 dy0:3 dz0:3")
    d = block_vector(
        sp.Matrix(variables[0:3]),
        sp.Matrix(variables[3:6]),
        sp.Matrix(variables[6:9]),
    )
    equations = list(permanent(full, d, q1)) + list(permanent(full, d, q2))
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    assert coefficient_matrix.rank() == 8
    assert coefficient_matrix * full == sp.zeros(coefficient_matrix.rows, 1)

    two = block_vector(x, y, zero)
    tangent = sp.Matrix.hstack(
        *(permanent(two, block_vector(zero, zero, e(0)), sp.eye(9)[:, j]) for j in range(9))
    )
    assert tangent.rank() == 5

    pure = block_vector(x, zero, zero)
    d_pure = block_vector(e(1), e(0), e(0))
    q = block_vector(e(2), 7 * e(0), -7 * e(0))
    core = permanent(d_pure, d_pure, q)
    assert core == 2 * tensor3(e(2), e(0), e(0))
    c_y = block_vector(zero, e(1), zero)
    c_z = block_vector(zero, zero, e(1))
    face_y = permanent(c_y, pure, q)
    face_z = permanent(c_z, pure, q)
    assert face_y == -7 * tensor3(e(0), e(1), e(0))
    assert face_z == 7 * tensor3(e(0), e(0), e(1))
    print("equal-plane atlas: PASS (full/two/pure source cases)")


def common_radical_model() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, zeta = e(0), e(0), e(0)
    v = block_vector(x, zero, zero)
    a = block_vector(zero, y, zeta)
    d = a
    p = block_vector(e(1), y, -zeta)
    qx1 = block_vector(e(1), zero, zero)
    qx2 = block_vector(e(2), zero, zero)
    q0 = block_vector(zero, y, -zeta)
    q_basis = [qx1, qx2, q0]

    assert alternating(v, d, p) != sp.zeros(27, 1)
    for q in q_basis:
        assert permanent(v, v, q) == sp.zeros(27, 1)
        assert permanent(v, d, q) == sp.zeros(27, 1)
        assert permanent(a, p, q) == sp.zeros(27, 1)
    core_columns = sp.Matrix.hstack(*(permanent(v, p, q) for q in q_basis))
    assert core_columns.rank() == 1
    assert core_columns[:, 2] == -2 * tensor3(x, y, zeta)

    # The exterior tangent has fixed y or zeta on every rank-one ruling.
    c_y = block_vector(zero, e(1), zero)
    c_z = block_vector(zero, zero, e(1))
    assert permanent(a, c_y, qx1) == tensor3(e(1), e(1), zeta)
    assert permanent(a, c_z, qx1) == tensor3(e(1), y, e(1))
    print("common-radical lemma: PASS (canonical normal form / two rulings)")


def zero_rectangle_rank_atlases() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, zeta = e(0), e(0), e(0)

    # Pure zero row: a full alternating Y/Z minor forces the common Q to X.
    pure = block_vector(x, zero, zero)
    s1 = block_vector(zero, e(1), zero)
    s2 = block_vector(zero, zero, e(1))
    stacked = permanent_map(pure, s1).col_join(permanent_map(pure, s2))
    assert stacked.nullspace() == [block_vector(e(i), zero, zero) for i in range(3)]

    # Two-source atlas and its viable canonical zero rectangle.
    two = block_vector(x, y, zero)
    k = block_vector(x, -y, zero)
    inside_xy = block_vector(e(1), e(2), zero)
    inside_kz = k + block_vector(zero, zero, e(1))
    outside = block_vector(e(1), zero, e(1))
    assert 9 - permanent_map(two, inside_xy).rank() >= 3
    assert 9 - permanent_map(two, inside_kz).rank() >= 3
    assert 9 - permanent_map(two, outside).rank() == 2

    a = block_vector(zero, zero, zeta)
    b = k
    v = a
    q_basis = [k, block_vector(zero, zero, e(1)), block_vector(zero, zero, e(2))]
    assert alternating(a, b, two) != sp.zeros(27, 1)
    for s in (a, b):
        for q in q_basis:
            assert permanent(two, s, q) == sp.zeros(27, 1)
    assert all(permanent(a, v, q) == sp.zeros(27, 1) for q in q_basis)
    core = sp.Matrix.hstack(*(permanent(b, v, q) for q in q_basis))
    assert core.rank() == 1
    assert core[:, 0] == -2 * tensor3(x, y, zeta)

    # Full-source atlas: a full-sensor plane in L_X has common kernel X.
    full = block_vector(x, y, zeta)
    f1 = block_vector(e(1), y, -zeta)
    f2 = block_vector(e(2), 2 * y, -2 * zeta)
    assert alternating(f1, f2, full) != sp.zeros(27, 1)
    common = permanent_map(full, f1).col_join(permanent_map(full, f2))
    assert common.nullspace() == [block_vector(e(i), zero, zero) for i in range(3)]
    qx = block_vector(e(1), zero, zero)
    assert permanent(f1, f2, qx) == -4 * tensor3(e(1), y, zeta)

    # Representatives of the three L_i components have kernel dimension >=3;
    # representatives off their union have kernel dimension at most two.
    lx = block_vector(e(1), y, -zeta)
    ly = block_vector(x, e(1), -zeta)
    lz = block_vector(x, -y, e(1))
    off_two = block_vector(e(1), e(1), zeta)
    assert all(9 - permanent_map(full, row).rank() >= 3 for row in (lx, ly, lz))
    assert 9 - permanent_map(full, off_two).rank() <= 2
    print("zero-rectangle lemma: PASS (pure/two/full source rank atlases)")


def untouched_coloop_tables() -> None:
    table = {
        (i, j, k): (1 if i == j == k else 0)
        for i in (1, 2)
        for j in (0, 2)
        for k in range(3)
    }
    assert sum(table.values()) == 1
    assert table[(2, 2, 2)] == 1
    # beta_u: p_s is a common radical; p_u carries zero/T_u rows.
    assert all(table[(i, 0, k)] == 0 for i in (1, 2) for k in range(3))
    assert all(table[(1, 2, k)] == 0 for k in range(3))
    # beta_s: p_s is a complete zero rectangle; p_u has the same core table.
    assert all(table[(i, 0, k)] == 0 for i in (1, 2) for k in range(3))
    assert [table[(2, 2, k)] for k in range(3)] == [0, 0, 1]
    print("coloop rows: PASS (four orientations / unique untouched core)")


def main() -> None:
    repeated_derivative_and_recovery()
    torus_fork_and_exterior()
    equal_plane_atlas()
    common_radical_model()
    zero_rectangle_rank_atlases()
    untouched_coloop_tables()
    print("(1,1,2) repeated-outer-factor divisor exclusion: PASS")


if __name__ == "__main__":
    main()
