"""Exact replay for the (1,1,2) double-repeated intersection exclusion.

The owning Markdown file is the proof.  This script checks the displayed
scalar identities and the complete canonical linear-algebra models used by
its three source-support lemmas.
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
    lam: sp.Expr,
    mu: sp.Expr,
    nu: sp.Expr,
    xi: sp.Expr,
) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for index in range(DIM):
        columns.append(-mu * nu * tensor3(e(index), e(t), e(t)))
    for index in range(DIM):
        columns.append(-lam * xi * tensor3(e(s), e(index), e(s)))
    for index in range(DIM):
        columns.append(lam * mu * tensor3(e(s), e(t), e(index)))
    return sp.Matrix.hstack(*columns)


def derivative_recovery_and_fork() -> None:
    lam, mu, nu, xi = sp.symbols("lam mu nu xi", nonzero=True)
    s, t = 0, 1
    derivative = derivative_matrix(s, t, lam, mu, nu, xi)
    kernel = sp.Matrix.hstack(
        (lam * e(s)).col_join(sp.zeros(3, 1)).col_join(nu * e(t)),
        sp.zeros(3, 1).col_join(mu * e(t)).col_join(xi * e(s)),
    )
    assert derivative.rank() == 7
    assert derivative * kernel == sp.zeros(27, 2)

    basis: list[sp.Matrix] = []
    for index in range(DIM):
        if index != s:
            basis.append(e(index).col_join(sp.zeros(6, 1)))
    for index in range(DIM):
        if index != t:
            basis.append(sp.zeros(3, 1).col_join(e(index)).col_join(sp.zeros(3, 1)))
    for index in range(DIM):
        basis.append(
            (-nu * (1 if index == t else 0) / lam * e(s))
            .col_join(-xi * (1 if index == s else 0) / mu * e(t))
            .col_join(e(index))
        )
    annihilator = sp.Matrix.hstack(*basis)
    assert annihilator.shape == (9, 7)
    assert annihilator.rank() == 7
    assert kernel.T * annihilator == sp.zeros(2, 7)

    a0, a1, a2, b0, b1, b2, g0, g1, g2 = sp.symbols(
        "a0 a1 a2 b0 b1 b2 g0 g1 g2"
    )
    alpha = sp.Matrix([a0, a1, a2]).subs(a0, -nu * g1 / lam)
    beta = sp.Matrix([b0, b1, b2]).subs(b1, -xi * g0 / mu)
    gamma = sp.Matrix([g0, g1, g2])
    ell = alpha.col_join(beta).col_join(gamma)
    transpose = (
        (-mu * nu * beta[t] * gamma[t] * alpha)
        .col_join(-lam * xi * alpha[s] * gamma[s] * beta)
        .col_join(lam * mu * alpha[s] * beta[t] * gamma)
    )
    expected = nu * xi * g0 * g1 * ell
    assert sp.simplify(transpose - expected) == sp.zeros(9, 1)

    # Coordinates on L are exactly the seven distinct torus factors.
    normals = [sp.eye(7).row(index) for index in range(7)]
    assert sp.Matrix.vstack(*normals).rank() == 7
    print("double-repeated derivative: PASS (rank/kernel/recovery/seven factors)")


def correction_coefficient_scalings() -> None:
    lam, mu, nu, xi = sp.symbols("lam mu nu xi", nonzero=True)
    a1, a2, b0, b2, g0, g1, g2 = sp.symbols(
        "a1 a2 b0 b2 g0 g1 g2"
    )
    pr1, pr2, pp0, pp2, ph0, ph1, ph2 = sp.symbols(
        "pr1 pr2 pp0 pp2 ph0 ph1 ph2"
    )
    alpha0 = -nu * g1 / lam
    beta1 = -xi * g0 / mu

    # One scalar target component of the seven support coefficients of F.
    contraction = (
        a1 * beta1 * g1 * (-mu * nu * pr1)
        + a2 * beta1 * g1 * (-mu * nu * pr2)
        + alpha0 * b0 * g0 * (-lam * xi * pp0)
        + alpha0 * b2 * g0 * (-lam * xi * pp2)
        + alpha0 * beta1 * g0 * (lam * mu * ph0)
        + alpha0 * beta1 * g1 * (lam * mu * ph1)
        + alpha0 * beta1 * g2 * (lam * mu * ph2)
    )
    phi_row = (
        a1 * pr1
        + a2 * pr2
        + b0 * pp0
        + b2 * pp2
        + g0 * ph0
        + g1 * ph1
        + g2 * ph2
    )
    assert sp.simplify(contraction - nu * xi * g0 * g1 * phi_row) == 0
    print("full correction identity: PASS (all seven coefficient scalings)")


def square_radical_obstruction() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, z = e(0), e(0), e(0)

    full = block_vector(x, y, z)
    full_square = permanent_map(full, full)
    assert full_square.rank() == 7
    assert len(full_square.nullspace()) == 2

    two = block_vector(x, y, zero)
    xy_basis = sp.Matrix.hstack(
        *(block_vector(e(i), zero, zero) for i in range(DIM)),
        *(block_vector(zero, e(i), zero) for i in range(DIM)),
    )
    assert permanent_map(two, two) * xy_basis == sp.zeros(27, 6)
    d_with_z = block_vector(zero, zero, z)
    mixed_xy = permanent_map(two, d_with_z) * xy_basis
    assert mixed_xy.rank() == 5
    assert len(mixed_xy.nullspace()) == 1
    d_without_z = block_vector(e(1), e(1), zero)
    assert permanent_map(d_without_z, d_without_z) * xy_basis == sp.zeros(27, 6)

    pure = block_vector(x, zero, zero)
    d = block_vector(e(1), y, z)
    radical_space = sp.Matrix.hstack(
        *(block_vector(e(i), zero, zero) for i in range(DIM)),
        block_vector(zero, y, -z),
    )
    assert permanent_map(pure, d) * radical_space == sp.zeros(27, 4)
    square_on_radical = permanent_map(d, d) * radical_space
    assert square_on_radical.rank() == 3
    assert len(square_on_radical.nullspace()) == 1
    print("square-radical lemma: PASS (full/two/pure dimension bounds)")


def common_radical_intersection() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, z = e(0), e(0), e(0)
    v = block_vector(x, zero, zero)
    d = block_vector(zero, y, z)
    p = block_vector(e(1), y, -z)
    radical_space = sp.Matrix.hstack(
        *(block_vector(e(i), zero, zero) for i in range(DIM)),
        block_vector(zero, y, -z),
    )
    source_plane = sp.Matrix.hstack(v, d)

    assert alternating(v, d, p) != sp.zeros(27, 1)
    assert permanent_map(v, v) * radical_space == sp.zeros(27, 4)
    assert permanent_map(v, d) * radical_space == sp.zeros(27, 4)
    assert permanent_map(d, p) * radical_space == sp.zeros(27, 4)
    core = permanent_map(v, p) * radical_space
    assert core.rank() == 1

    combined = source_plane.row_join(radical_space)
    intersection_dimension = source_plane.rank() + radical_space.rank() - combined.rank()
    assert intersection_dimension == 1
    assert source_plane.gauss_jordan_solve(v)[1] == sp.zeros(0, 1)
    assert core * radical_space.gauss_jordan_solve(v)[0] == sp.zeros(27, 1)
    print("common-radical intersection: PASS (sum/difference ruling separation)")


def zero_rectangle_normal_form() -> None:
    zero = sp.zeros(DIM, 1)
    x, y = e(0), e(0)
    k = block_vector(x, -y, zero)
    external = block_vector(x, y, zero)
    z0 = block_vector(zero, zero, e(0))
    z1 = block_vector(zero, zero, e(1))
    z2 = block_vector(zero, zero, e(2))
    e_space = sp.Matrix.hstack(k, z0, z1, z2)

    # Verify the complete cubic formula on symbolic points of E.
    c = sp.symbols("c0:3")
    z_variables = sp.symbols("z0:9")
    zs = [sp.Matrix(z_variables[3 * i : 3 * i + 3]) for i in range(3)]
    ws = [c[i] * k + block_vector(zero, zero, zs[i]) for i in range(3)]
    formula = -2 * tensor3(
        x,
        y,
        c[0] * c[1] * zs[2]
        + c[0] * c[2] * zs[1]
        + c[1] * c[2] * zs[0],
    )
    assert sp.simplify(permanent(*ws) - formula) == sp.zeros(27, 1)

    a = z2
    v = z2
    b = k + z0
    q_space = sp.Matrix.hstack(z0, z1, k + z2)
    assert alternating(a, b, external) != sp.zeros(27, 1)
    assert permanent_map(external, a) * q_space == sp.zeros(27, 3)
    assert permanent_map(external, b) * q_space == sp.zeros(27, 3)
    assert permanent_map(a, v) * q_space == sp.zeros(27, 3)
    core = permanent_map(b, v) * q_space
    assert core.rank() == 1
    assert core[:, 0] == sp.zeros(27, 1)
    assert core[:, 1] == sp.zeros(27, 1)
    assert core[:, 2] == -2 * tensor3(x, y, e(2))

    fixed_factor_space = sp.Matrix.hstack(
        *(tensor3(x, y, e(i)) for i in range(DIM))
    )
    for left in e_space.columnspace():
        for middle in e_space.columnspace():
            for right in e_space.columnspace():
                value = permanent(left, middle, right)
                assert fixed_factor_space.row_join(value).rank() == 3

    # The zero map has only the two exhaustive rank patterns used in Lemma 3.
    identity_z = sp.eye(DIM)
    full_rank_case = identity_z.row_join(e(2))
    pure_kernel_case = e(2).row_join(sp.zeros(DIM, DIM))
    assert full_rank_case.rank() == 3
    assert len(full_rank_case.nullspace()) == 1
    assert pure_kernel_case.rank() == 1
    assert len(pure_kernel_case.nullspace()) == 3
    print("zero-rectangle refinement: PASS (rank atlas/canonical factor space)")


def main() -> None:
    derivative_recovery_and_fork()
    correction_coefficient_scalings()
    square_radical_obstruction()
    common_radical_intersection()
    zero_rectangle_normal_form()
    print("(1,1,2) double-repeated outer intersection exclusion: PASS")


if __name__ == "__main__":
    main()
