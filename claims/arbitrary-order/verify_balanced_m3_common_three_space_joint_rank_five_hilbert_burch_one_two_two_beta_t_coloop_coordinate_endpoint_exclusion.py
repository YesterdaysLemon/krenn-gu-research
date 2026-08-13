"""Exact replay for the (1,2,2) beta_t-coloop coordinate endpoints."""

from __future__ import annotations

import itertools

import sympy as sp

SOURCE_DIM = 3
ROW_DIM = 3 * SOURCE_DIM
TENSOR_DIM = SOURCE_DIM**3


def source(source_id: int, index: int) -> sp.Matrix:
    vector = sp.zeros(ROW_DIM, 1)
    vector[source_id * SOURCE_DIM + index] = 1
    return vector


def component(vector: sp.Matrix, source_id: int) -> sp.Matrix:
    start = source_id * SOURCE_DIM
    return vector[start : start + SOURCE_DIM, :]


def tensor3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def permanent(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    vectors = (left, middle, right)
    out = sp.zeros(TENSOR_DIM, 1)
    for permutation in itertools.permutations(range(3)):
        out += tensor3(
            component(vectors[permutation[0]], 0),
            component(vectors[permutation[1]], 1),
            component(vectors[permutation[2]], 2),
        )
    return out


def linear_map(factors: list[sp.Matrix]) -> sp.Matrix:
    return sp.Matrix.hstack(*factors)


def target_coefficients(
    alpha: sp.Matrix, beta: sp.Matrix, gamma: sp.Matrix
) -> sp.Matrix:
    return sp.Matrix([alpha[i] * beta[i] * gamma[i] for i in range(3)])


def endpoint_single_cell_table() -> None:
    eye = sp.eye(3)
    for t in range(3):
        for a in range(3):
            if a == t:
                continue
            b = next(i for i in range(3) if i not in (a, t))
            for i in range(3):
                alpha = eye[:, i]
                assert target_coefficients(alpha, eye[:, a], eye[:, b]) == sp.zeros(
                    3, 1
                )
                assert target_coefficients(alpha, eye[:, a], eye[:, t]) == sp.zeros(
                    3, 1
                )
                assert target_coefficients(alpha, eye[:, b], eye[:, t]) == sp.zeros(
                    3, 1
                )
                expected = sp.zeros(3, 1)
                if i == b:
                    expected[b] = 1
                assert target_coefficients(alpha, eye[:, b], eye[:, b]) == expected
    print("endpoint target face: PASS (all six colour orientations)")


def full_source_case() -> None:
    basis = [sp.eye(ROW_DIM)[:, i] for i in range(ROW_DIM)]
    x, y, z = source(0, 0), source(1, 0), source(2, 0)
    p = x + y + z

    square = linear_map([permanent(p, p, q) for q in basis])
    assert square.rank() == 7
    radical = sp.Matrix.hstack(x - y, x - z)
    assert radical.rank() == 2
    assert square * radical == sp.zeros(TENSOR_DIM, 2)

    common = linear_map(
        [
            sp.Matrix.vstack(
                permanent(v, p, x - y),
                permanent(v, p, x - z),
            )
            for v in basis
        ]
    )
    assert common.rank() == 8
    assert common * p == sp.zeros(2 * TENSOR_DIM, 1)
    print("single-cell atlas: PASS (full support collapses S to span(p))")


def two_source_case() -> None:
    basis = [sp.eye(ROW_DIM)[:, i] for i in range(ROW_DIM)]
    x, y, z = source(0, 0), source(1, 0), source(2, 0)
    p = x + y

    square = linear_map([permanent(p, p, q) for q in basis])
    assert square.rank() == SOURCE_DIM
    xy_basis = basis[: 2 * SOURCE_DIM]
    assert all(square * q == sp.zeros(TENSOR_DIM, 1) for q in xy_basis)

    mixed = linear_map([permanent(z, p, q) for q in xy_basis])
    assert mixed.rank() == 2 * SOURCE_DIM - 1
    assert mixed * sp.Matrix([1, 0, 0, -1, 0, 0]) == sp.zeros(TENSOR_DIM, 1)

    for left in xy_basis:
        for middle in xy_basis:
            for right in xy_basis:
                assert permanent(left, middle, right) == sp.zeros(TENSOR_DIM, 1)
    print("single-cell atlas: PASS (two-source fork is line-or-zero)")


def pure_source_case() -> None:
    basis = [sp.eye(ROW_DIM)[:, i] for i in range(ROW_DIM)]
    x = source(0, 0)
    q_y = source(1, 0)
    mixed_y = linear_map([permanent(v, x, q_y) for v in basis])
    assert mixed_y.rank() == SOURCE_DIM
    assert all(
        mixed_y * v == sp.zeros(TENSOR_DIM, 1)
        for v in basis[: 2 * SOURCE_DIM]
    )

    d = source(0, 0) + 2 * source(1, 1) - 3 * source(2, 2)
    q_0, q_1 = source(0, 1), source(0, 2)
    map_0 = linear_map([permanent(v, d, q_0) for v in basis])
    map_1 = linear_map([permanent(v, d, q_1) for v in basis])
    combined = sp.Matrix.vstack(map_0, map_1)
    assert map_0.rank() == map_1.rank() == combined.rank()
    print("single-cell atlas: PASS (pure partner maps have the same kernel)")


def main() -> None:
    endpoint_single_cell_table()
    full_source_case()
    two_source_case()
    pure_source_case()
    print("beta_t-coloop coordinate-endpoint exclusion: PASS")


if __name__ == "__main__":
    main()
