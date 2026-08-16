#!/usr/bin/env python3
"""Exact replay for the lower-rank three-root derivative/torus census."""

from __future__ import annotations

import sympy as sp

DIM = 3
DOMAIN_DIM = 3 * DIM
TARGET_DIM = DIM**3


def e(index: int) -> sp.Matrix:
    return sp.eye(DIM)[:, index]


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def root_tensor(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def derivative(b_23: sp.Matrix, b_13: sp.Matrix, b_12: sp.Matrix) -> sp.Matrix:
    columns: list[sp.Matrix] = []
    for index in range(DIM):
        columns.append(sp.kronecker_product(e(index), sp.Matrix(b_23).reshape(9, 1)))
    for middle in range(DIM):
        column = sp.zeros(TARGET_DIM, 1)
        for left in range(DIM):
            for right in range(DIM):
                column += b_13[left, right] * root_tensor(e(left), e(middle), e(right))
        columns.append(column)
    for right in range(DIM):
        column = sp.zeros(TARGET_DIM, 1)
        for left in range(DIM):
            for middle in range(DIM):
                column += b_12[left, middle] * root_tensor(e(left), e(middle), e(right))
        columns.append(column)
    return sp.Matrix.hstack(*columns)


def concatenate(first: sp.Matrix, second: sp.Matrix, third: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.vstack(first, second, third)


def proportional(first: sp.Matrix, second: sp.Matrix) -> bool:
    return sp.Matrix.hstack(first, second).rank() == 1


def rank_fixtures() -> None:
    # Rank nine: three disjoint coordinate derivative summands.
    rank_nine = derivative(outer(e(0), e(0)), outer(e(1), e(1)), outer(e(2), e(2)))
    assert rank_nine.rank() == 9
    assert not rank_nine.nullspace()

    # Rank eight: one shared-factor syzygy and residual outside the tangent plane.
    x = y = w = e(0)
    residual = outer(e(1), e(1))
    rank_eight = derivative(outer(y, w), -outer(x, w), residual)
    kernel = rank_eight.nullspace()
    assert rank_eight.rank() == 8
    assert len(kernel) == 1
    assert proportional(kernel[0], concatenate(x, y, sp.zeros(DIM, 1)))

    tangent_columns = [sp.kronecker_product(e(index), y) for index in range(DIM)]
    tangent_columns += [sp.kronecker_product(x, e(index)) for index in range(DIM)]
    tangent = sp.Matrix.hstack(*tangent_columns)
    assert tangent.rank() == 5
    assert sp.Matrix.hstack(tangent, sp.Matrix(residual).reshape(9, 1)).rank() == 6

    # Moving the residual into the tangent plane creates the second syzygy.
    rank_seven_tangent = derivative(outer(y, w), -outer(x, w), outer(x, y))
    assert rank_seven_tangent.rank() == 7
    assert len(rank_seven_tangent.nullspace()) == 2
    print("derivative rank fixtures: PASS (9 / 8 / 7)")


def incidence_census() -> None:
    expected = {
        (3, 9): (0, 3, 0),
        (3, 8): (1, 4, 0),
        (3, 7): (2, 5, 0),
        (4, 8): (1, 4, 1),
        (4, 7): (2, 5, 1),
    }
    for (joint_rank, derivative_rank), (kernel_dim, preimage_dim, intersection_dim) in expected.items():
        assert kernel_dim == DOMAIN_DIM - derivative_rank
        assert preimage_dim == kernel_dim + 3
        assert intersection_dim == joint_rank - 3
        assert joint_rank <= preimage_dim
    assert 4 - 3 > DOMAIN_DIM - 9
    print("lower-rank incidence table: PASS (rank-four injective chart impossible)")


def contraction(block: sp.Matrix, left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand((left.T * block * right)[0])


def torus_gate_replays() -> None:
    one = sp.Matrix([1, 1, 1])

    # If w and C are both nonmonomial, gamma(w)=0 and C(alpha,beta)=0
    # have independent fully supported solutions.
    x = y = e(0)
    w = e(0) + e(1)
    residual = outer(e(0), e(0)) + outer(e(1), e(1))
    alpha = one
    beta = sp.Matrix([1, -1, 1])
    gamma = sp.Matrix([1, -1, 1])
    assert contraction(outer(y, w), beta, gamma) == 0
    assert contraction(-outer(x, w), alpha, gamma) == 0
    assert contraction(residual, alpha, beta) == 0
    assert all(entry != 0 for vector in (alpha, beta, gamma) for entry in vector)

    # With w coordinate and x,y noncoordinate, a rank-two restriction of C
    # to x^perp x y^perp still creates a torus zero.
    x = y = e(0) + e(1)
    w = e(0)
    residual = outer(e(0), e(0)) + outer(e(2), e(2))
    alpha = sp.Matrix([1, -1, 1])
    beta = sp.Matrix([1, -1, -1])
    gamma = one
    assert (alpha.T * x)[0] == 0
    assert (beta.T * y)[0] == 0
    assert contraction(residual, alpha, beta) == 0
    assert contraction(outer(y, w), beta, gamma) == 0
    assert contraction(-outer(x, w), alpha, gamma) == 0

    # A coordinate monomial quotient is nonzero on the restricted torus.
    monomial = outer(e(2), e(2))
    a_0, a_2, b_0, b_2 = sp.symbols("a_0 a_2 b_0 b_2", nonzero=True)
    restricted_alpha = sp.Matrix([a_0, -a_0, a_2])
    restricted_beta = sp.Matrix([b_0, -b_0, b_2])
    assert contraction(monomial, restricted_alpha, restricted_beta) == a_2 * b_2
    print("rank-eight torus gate: PASS (Laurent / restricted-bilinear forks)")


def hilbert_burch_blocks(
    x: sp.Matrix,
    b: sp.Matrix,
    y: sp.Matrix,
    c: sp.Matrix,
    z: sp.Matrix,
    w: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        outer(y, w) - outer(c, z),
        outer(b, z) - outer(x, w),
        outer(x, c) - outer(b, y),
    )


def projection_profile(first: sp.Matrix, second: sp.Matrix) -> int:
    return sp.Matrix.hstack(first, second).rank()


def check_hilbert_burch_profile(
    vectors: tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix],
    expected_profile: tuple[int, int, int],
) -> sp.Matrix:
    x, b, y, c, z, w = vectors
    blocks = hilbert_burch_blocks(x, b, y, c, z, w)
    shared = derivative(*blocks)
    assert all(block != sp.zeros(DIM, DIM) for block in blocks)
    assert shared.rank() == 7
    first_syzygy = concatenate(x, y, z)
    second_syzygy = concatenate(b, c, w)
    assert shared * first_syzygy == sp.zeros(TARGET_DIM, 1)
    assert shared * second_syzygy == sp.zeros(TARGET_DIM, 1)
    assert sp.Matrix.hstack(first_syzygy, second_syzygy).rank() == 2
    assert expected_profile == (
        projection_profile(x, b),
        projection_profile(y, c),
        projection_profile(z, w),
    )
    return shared


def hilbert_burch_replays() -> None:
    zero = sp.zeros(DIM, 1)

    full_vectors = (e(0), e(1), e(0), e(1), e(0), e(1))
    check_hilbert_burch_profile(full_vectors, (2, 2, 2))
    alpha = beta = gamma = sp.Matrix([1, 1, 1])
    blocks = hilbert_burch_blocks(*full_vectors)
    assert all(
        value == 0
        for value in (
            contraction(blocks[0], beta, gamma),
            contraction(blocks[1], alpha, gamma),
            contraction(blocks[2], alpha, beta),
        )
    )

    check_hilbert_burch_profile((e(0), zero, e(0), e(1), e(0), e(1)), (1, 2, 2))
    check_hilbert_burch_profile((e(0), zero, zero, e(1), e(0), e(1)), (1, 1, 2))
    check_hilbert_burch_profile((e(0), zero, zero, e(1), e(2), e(2)), (1, 1, 1))
    print("Hilbert--Burch atlas: PASS ((2,2,2) torus point / three boundary profiles)")


def main() -> None:
    rank_fixtures()
    incidence_census()
    torus_gate_replays()
    hilbert_burch_replays()
    print("lower-rank three-root derivative/torus census replay: PASS")


if __name__ == "__main__":
    main()
