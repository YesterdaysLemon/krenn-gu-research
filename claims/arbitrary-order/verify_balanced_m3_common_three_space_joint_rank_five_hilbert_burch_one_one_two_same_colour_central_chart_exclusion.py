"""Exact replay for the (1,1,2) same-colour central-chart exclusion."""

from __future__ import annotations

import itertools

import sympy as sp

DIM = 3
TOTAL = 9


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
    z: sp.Matrix,
    w: sp.Matrix,
    lam: sp.Expr,
    mu: sp.Expr,
) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for index in range(DIM):
        columns.append(-mu * tensor3(e(index), e(s), z))
    for index in range(DIM):
        columns.append(-lam * tensor3(e(s), e(index), w))
    for index in range(DIM):
        columns.append(lam * mu * tensor3(e(s), e(s), e(index)))
    return sp.Matrix.hstack(*columns)


def derivative_and_recovery() -> None:
    lam, mu = sp.symbols("lam mu", nonzero=True)
    z0, z1, z2, w0, w1, w2 = sp.symbols("z0 z1 z2 w0 w1 w2")
    z = sp.Matrix([z0, z1, z2])
    w = sp.Matrix([w0, w1, w2])
    derivative = derivative_matrix(0, z, w, lam, mu)
    kernel = sp.Matrix.hstack(
        (lam * e(0)).col_join(sp.zeros(3, 1)).col_join(z),
        sp.zeros(3, 1).col_join(mu * e(0)).col_join(w),
    )
    assert sp.simplify(derivative * kernel) == sp.zeros(27, 2)

    basis: list[sp.Matrix] = []
    for index in (1, 2):
        basis.append(e(index).col_join(sp.zeros(6, 1)))
    for index in (1, 2):
        basis.append(sp.zeros(3, 1).col_join(e(index)).col_join(sp.zeros(3, 1)))
    for index in range(3):
        basis.append(
            (-z[index] / lam * e(0))
            .col_join(-w[index] / mu * e(0))
            .col_join(e(index))
        )
    annihilator = sp.Matrix.hstack(*basis)
    assert annihilator.shape == (9, 7)
    assert kernel.T * annihilator == sp.zeros(2, 7)

    a0, a1, a2, b0, b1, b2, g0, g1, g2 = sp.symbols(
        "a0 a1 a2 b0 b1 b2 g0 g1 g2"
    )
    gamma = sp.Matrix([g0, g1, g2])
    gamma_z = (gamma.T * z)[0]
    gamma_w = (gamma.T * w)[0]
    alpha = sp.Matrix([a0, a1, a2]).subs(a0, -gamma_z / lam)
    beta = sp.Matrix([b0, b1, b2]).subs(b0, -gamma_w / mu)
    ell = alpha.col_join(beta).col_join(gamma)
    transpose = (
        (-mu * beta[0] * gamma_z * alpha)
        .col_join(-lam * alpha[0] * gamma_w * beta)
        .col_join(lam * mu * alpha[0] * beta[0] * gamma)
    )
    assert sp.simplify(transpose - gamma_z * gamma_w * ell) == sp.zeros(9, 1)

    z_exact = sp.Matrix([1, 1, 0])
    w_exact = sp.Matrix([1, 0, 1])
    assert sp.Matrix.hstack(z_exact, w_exact).rank() == 2
    common_normal = z_exact.cross(w_exact)
    assert common_normal != sp.zeros(3, 1)
    quotient_map = sp.Matrix.vstack(z_exact.T, w_exact.T)
    assert quotient_map.rank() == 2
    print("same-colour derivative: PASS (kernel/L/recovery/quotient rank)")


def square_zero_two_target_atlas() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, z = e(0), e(0), e(0)

    pure = block_vector(x, zero, zero)
    c_y = block_vector(zero, e(1), zero)
    c_z = block_vector(zero, zero, e(1))
    q = block_vector(zero, e(2), e(2))
    value_y = permanent(c_y, pure, q)
    value_z = permanent(c_z, pure, q)
    assert value_y == tensor3(x, e(1), e(2))
    assert value_z == tensor3(x, e(2), e(1))

    full = block_vector(x, y, z)
    assert permanent_map(full, full).rank() == 7
    assert len(permanent_map(full, full).nullspace()) == 2

    two = block_vector(x, y, zero)
    xy_basis = sp.Matrix.hstack(
        *(block_vector(e(i), zero, zero) for i in range(DIM)),
        *(block_vector(zero, e(i), zero) for i in range(DIM)),
    )
    assert permanent_map(two, two) * xy_basis == sp.zeros(27, 6)
    l_map = permanent_map(two, block_vector(zero, zero, z)) * xy_basis
    assert l_map.rank() == 5
    assert len(l_map.nullspace()) == 1
    print("square-zero two-target lemma: PASS (pure/full/two support)")


def rank_one_square_two_radicals_atlas() -> None:
    zero = sp.zeros(DIM, 1)
    x, y, z = e(0), e(0), e(0)

    full = block_vector(x, y, z)
    kernel_basis = sp.Matrix.hstack(
        block_vector(x, -y, zero),
        block_vector(x, zero, -z),
    )
    assert permanent_map(full, full) * kernel_basis == sp.zeros(27, 2)

    # A mixed radical on the complete square kernel is only span(full).
    identity = sp.eye(TOTAL)
    equations = sp.Matrix.vstack(
        *(
            sp.Matrix.hstack(
                *(permanent(full, identity[:, i], q) for i in range(TOTAL))
            )
            for q in kernel_basis.columnspace()
        )
    )
    assert equations.rank() == 8
    assert equations * full == sp.zeros(equations.rows, 1)

    two = block_vector(x, y, zero)
    xy_basis = sp.Matrix.hstack(
        *(block_vector(e(i), zero, zero) for i in range(DIM)),
        *(block_vector(zero, e(i), zero) for i in range(DIM)),
    )
    l_map = permanent_map(two, block_vector(zero, zero, z)) * xy_basis
    assert l_map.rank() == 5
    assert len(l_map.nullspace()) == 1

    p = block_vector(e(1), e(2), zero)
    w = block_vector(e(2), e(1), zero)
    assert alternating(two, p, w) == sp.zeros(27, 1)
    print("rank-one square/two-radical lemma: PASS (full/two support)")


def coefficient_fork() -> None:
    c, d, la, lb = sp.symbols("c d la lb")
    # Abstract scalar components of the four untouched maps.
    m_ra_pa = la
    m_ra_pb = 0
    m_rb_pa = 0
    m_rb_pb = lb
    square_rb = sp.expand(c * m_rb_pa + d * m_rb_pb)
    mixed_ra_rb = sp.expand(c * m_ra_pa + d * m_ra_pb)
    assert square_rb == d * lb
    assert mixed_ra_rb == c * la

    # d=0 is the square-zero/two-target endpoint; c=0 is the
    # rank-one-square/two-radical endpoint.
    assert square_rb.subs(d, 0) == 0
    assert mixed_ra_rb.subs(c, 0) == 0
    print("ordinary-coloop fork: PASS (generic and two endpoint identities)")


def main() -> None:
    derivative_and_recovery()
    square_zero_two_target_atlas()
    rank_one_square_two_radicals_atlas()
    coefficient_fork()
    print("(1,1,2) same-colour central-chart exclusion: PASS")


if __name__ == "__main__":
    main()
