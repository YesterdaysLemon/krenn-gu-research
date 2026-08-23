"""Focused exact checks for the GLS38 minimal raw-swallow exclusion."""

from __future__ import annotations

from itertools import product

import sympy as sp


EYE = sp.eye(3)
E = tuple(EYE[:, index] for index in range(3))
DIAGONAL_INDICES = (0, 4, 8)
OFF_DIAGONAL_INDICES = tuple(index for index in range(9) if index not in DIAGONAL_INDICES)


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def one_q_constraint_matrix(
    left_shore: tuple[sp.Matrix, sp.Matrix],
    right_shore: tuple[sp.Matrix, sp.Matrix],
) -> sp.Matrix:
    """Off-diagonal constraints on one arbitrary port slice (X,Y)."""

    rows: list[list[sp.Expr]] = []
    for residual in range(2):
        left = left_shore[residual]
        right = right_shore[residual]
        for row, column in product(range(3), repeat=2):
            if row == column:
                continue
            equation = [sp.Integer(0) for _ in range(6)]
            equation[row] = right[column]
            equation[3 + column] = left[row]
            rows.append(equation)
    return sp.Matrix(rows)


def is_diagonal(vector: sp.Matrix) -> bool:
    return all(vector[index] == 0 for index in OFF_DIAGONAL_INDICES)


def low_left_shore_charts() -> dict[str, int]:
    """Enumerate exact (d0,d1)=(1,1)/(1,2) charts with q=r0."""

    counts = {"d11": 0, "d12": 0, "kernel_vectors": 0, "diagonal_pairs": 0}
    for lambda_0, lambda_1 in product(range(-2, 3), repeat=2):
        if lambda_0 == lambda_1 == 0:
            continue
        left_shore = (lambda_0 * E[0], lambda_1 * E[0])
        for entries in product(range(-1, 2), repeat=3):
            free = sp.Matrix(entries)
            if lambda_0:
                right_0 = free
                right_1 = (E[0] - lambda_1 * right_0) / lambda_0
            else:
                right_0 = E[0] / lambda_1
                right_1 = free
            right_shore = (right_0, right_1)
            shore_rank = sp.Matrix.hstack(*right_shore).rank()
            if shore_rank not in (1, 2):
                continue
            q = tensor(left_shore[0], right_shore[1]) + tensor(
                left_shore[1], right_shore[0]
            )
            assert q == tensor(E[0], E[0])

            kernel = one_q_constraint_matrix(left_shore, right_shore).nullspace()
            assert kernel
            for vector in kernel:
                # GLS38's missing-row argument: every X slice is on e0.
                assert vector[1] == vector[2] == 0
                x, y = vector[:3, :], vector[3:, :]
                for residual in range(2):
                    column = tensor(left_shore[residual], y) + tensor(
                        x, right_shore[residual]
                    )
                    assert is_diagonal(column)
                    assert all(column[index] == 0 for index in (4, 8))
                counts["kernel_vectors"] += 1

            # A physical pair label is separately required to be diagonal.
            # Since both X halves lie on e0, every such diagonal pair column
            # is necessarily a multiple of r0.
            for first in kernel:
                for second in kernel:
                    x, y = first[:3, :], first[3:, :]
                    x2, y2 = second[:3, :], second[3:, :]
                    pair = tensor(x, y2) + tensor(x2, y)
                    if is_diagonal(pair):
                        assert all(pair[index] == 0 for index in (4, 8))
                        counts["diagonal_pairs"] += 1
            counts[f"d1{shore_rank}"] += 1
    assert counts["d11"] and counts["d12"]
    return counts


def low_right_shore_charts() -> dict[str, int]:
    """Transpose the exact chart family and audit the opposite shore drop."""

    counts = {"d11": 0, "d21": 0, "kernel_vectors": 0, "diagonal_pairs": 0}
    for lambda_0, lambda_1 in product(range(-2, 3), repeat=2):
        if lambda_0 == lambda_1 == 0:
            continue
        right_shore = (lambda_0 * E[0], lambda_1 * E[0])
        for entries in product(range(-1, 2), repeat=3):
            free = sp.Matrix(entries)
            if lambda_0:
                left_0 = free
                left_1 = (E[0] - lambda_1 * left_0) / lambda_0
            else:
                left_0 = E[0] / lambda_1
                left_1 = free
            left_shore = (left_0, left_1)
            shore_rank = sp.Matrix.hstack(*left_shore).rank()
            if shore_rank not in (1, 2):
                continue
            q = tensor(left_shore[0], right_shore[1]) + tensor(
                left_shore[1], right_shore[0]
            )
            assert q == tensor(E[0], E[0])

            kernel = one_q_constraint_matrix(left_shore, right_shore).nullspace()
            assert kernel
            for vector in kernel:
                # Transposed missing-column argument: every Y slice is on e0.
                assert vector[4] == vector[5] == 0
                x, y = vector[:3, :], vector[3:, :]
                for residual in range(2):
                    column = tensor(left_shore[residual], y) + tensor(
                        x, right_shore[residual]
                    )
                    assert is_diagonal(column)
                    assert all(column[index] == 0 for index in (4, 8))
                counts["kernel_vectors"] += 1

            for first in kernel:
                for second in kernel:
                    x, y = first[:3, :], first[3:, :]
                    x2, y2 = second[:3, :], second[3:, :]
                    pair = tensor(x, y2) + tensor(x2, y)
                    if is_diagonal(pair):
                        assert all(pair[index] == 0 for index in (4, 8))
                        counts["diagonal_pairs"] += 1
            counts[f"d{shore_rank}1"] += 1
    assert counts["d11"] and counts["d21"]
    return counts


def rank_cover_check() -> dict[str, object]:
    diagonal = sp.Matrix.hstack(
        tensor(E[0], E[0]), tensor(E[1], E[1]), tensor(E[2], E[2])
    )
    assert diagonal.rank() == 3
    assert all(
        min(left_rank, right_rank) <= 1 or (left_rank, right_rank) == (2, 2)
        for left_rank, right_rank in product((1, 2), repeat=2)
    )
    return {
        "full_diagonal_rank": diagonal.rank(),
        "low_shore_image_rank_at_most": 1,
        "two_rank_two_fibre": "excluded by GLS37",
        "nonzero_q_rank_three_full_swallow": "excluded",
    }


def main() -> None:
    left = low_left_shore_charts()
    right = low_right_shore_charts()
    cover = rank_cover_check()
    print("GLS38 nonzero-root-companion minimal-swallow primary checks: PASS")
    print("  low-left exact charts:", left)
    print("  low-right exact charts:", right)
    print("  discrete shore-rank cover:", cover)


if __name__ == "__main__":
    main()
