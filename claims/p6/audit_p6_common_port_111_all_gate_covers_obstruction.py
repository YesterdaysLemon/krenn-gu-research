#!/usr/bin/env python3
"""No-SymPy audit of all non-four gate-cover perfect pairings."""

from __future__ import annotations

import json

HYPEREDGES = (
    (0, 1, 2),
    (1, 3, 4),
    (4, 5, 6),
    (0, 7, 8),
    (7, 9, 10),
    (5, 10, 11),
    (0, 12, 13),
    (5, 14, 15),
    (6, 7, 9),
    (1, 3, 11),
    (5, 6, 11),
    (1, 3, 15),
    (5, 6, 15),
    (7, 9, 15),
    (5, 11, 15),
    (0, 2, 8),
    (2, 9, 10),
    (3, 4, 8),
    (0, 2, 12),
    (3, 4, 12),
    (0, 8, 12),
    (9, 10, 12),
)
UNIQUE_FOUR_COVER = (0, 3, 5, 9)
SIGN_FLIPS = {
    (2, 3, 6, 7, 10, 12, 15): 6,
    (1, 4, 8, 9, 11, 12, 15): 1,
    (1, 2, 4, 6, 8, 10, 13, 15): 2,
}
EXPECTED_DETERMINANTS = {
    (0, 1, 4, 5, 9): 3,
    (0, 3, 5, 7, 10): 13,
    (0, 1, 4, 5, 7, 10): -54,
    (2, 3, 5, 7, 12): 3,
    (1, 2, 4, 5, 7, 12): -102,
    (1, 2, 5, 7, 8, 12): -30,
    (1, 5, 8, 9, 12): 1,
    (2, 3, 5, 8, 9, 12): 16,
    (1, 5, 7, 8, 10, 12): -102,
    (2, 3, 5, 8, 9, 13): 8,
    (1, 2, 4, 5, 8, 9, 13): 2,
    (2, 3, 5, 7, 8, 10, 13): 30,
    (1, 2, 4, 5, 7, 8, 10, 13): 32,
    (0, 3, 6, 9, 11, 14): 4,
    (0, 1, 4, 6, 9, 11, 14): 9,
    (0, 3, 6, 7, 10, 11, 14): 79,
    (0, 1, 4, 6, 7, 10, 11, 14): -8,
    (2, 3, 6, 7, 11, 12, 14): -45,
    (1, 2, 4, 6, 7, 11, 12, 14): -80,
    (1, 2, 6, 7, 8, 11, 12, 14): 40,
    (1, 6, 8, 9, 11, 12, 14): 115,
    (2, 3, 6, 8, 9, 11, 12, 14): -68,
    (1, 6, 7, 8, 10, 11, 12, 14): 48,
    (2, 3, 6, 8, 9, 11, 13, 14): -32,
    (1, 2, 4, 6, 8, 9, 11, 13, 14): 60,
    (2, 3, 6, 7, 8, 10, 11, 13, 14): 156,
    (1, 2, 4, 6, 7, 8, 10, 11, 13, 14): 108,
    (0, 3, 6, 10, 15): 1,
    (0, 1, 4, 6, 10, 15): -5,
    (0, 4, 9, 11, 15): 3,
    (0, 3, 6, 9, 11, 15): 16,
    (0, 4, 6, 10, 11, 15): 36,
    (0, 4, 7, 10, 11, 15): 9,
    (2, 3, 6, 7, 10, 12, 15): 72,
    (1, 2, 4, 6, 7, 10, 12, 15): -95,
    (1, 6, 8, 10, 12, 15): 1,
    (2, 3, 6, 8, 10, 12, 15): -25,
    (2, 4, 7, 11, 12, 15): -3,
    (2, 3, 6, 7, 11, 12, 15): -107,
    (1, 2, 6, 7, 8, 11, 12, 15): -72,
    (1, 4, 8, 9, 11, 12, 15): -8,
    (2, 4, 8, 9, 11, 12, 15): 33,
    (1, 6, 8, 9, 11, 12, 15): -25,
    (2, 3, 6, 8, 9, 11, 12, 15): -192,
    (2, 4, 6, 8, 10, 11, 12, 15): 84,
    (1, 4, 7, 8, 10, 11, 12, 15): -77,
    (2, 3, 6, 8, 10, 13, 15): -1,
    (1, 2, 4, 6, 8, 10, 13, 15): 16,
    (2, 4, 8, 9, 11, 13, 15): 5,
    (2, 3, 6, 8, 9, 11, 13, 15): -24,
    (2, 4, 6, 8, 10, 11, 13, 15): 24,
    (2, 4, 7, 8, 10, 11, 13, 15): 96,
}

# Each entry is (scalar, ell, m) for
#   g_i(x,x) = scalar * ell(x) * m(x).
# The constructed integer matrix is 2*M_i, independently avoiding the
# half-integral coefficients in several canonical gate matrices.
FACTOR_ENDPOINTS = (
    (2, (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)),
    (1, (0, 1, 0, 0, 0), (2, 0, 2, 1, -1)),
    (1, (0, 0, 0, 0, 1), (2, 2, -2, 1, 0)),
    (2, (0, 1, 0, 0, 0), (0, 0, 0, 0, 1)),
    (1, (0, 0, 0, 0, 1), (2, -2, -2, -1, 0)),
    (2, (0, 1, 0, 0, 0), (0, 0, 1, 0, 0)),
    (1, (0, 1, 0, 0, 0), (2, 0, -2, 1, 1)),
    (1, (0, 0, 1, 0, 0), (2, 2, 0, 1, -1)),
    (1, (0, 0, 0, 1, 0), (2, -2, 2, 0, -1)),
    (2, (0, 0, 1, 0, 0), (0, 0, 0, 1, 0)),
    (1, (0, 0, 0, 1, 0), (2, -2, -2, 0, 1)),
    (1, (0, 0, 1, 0, 0), (2, -2, 0, -1, -1)),
    (2, (0, 0, 0, 1, -1), (1, 1, 1, 0, 0)),
    (1, (0, 1, -1, 0, 0), (2, 0, 0, 1, -1)),
    (2, (0, 0, 0, 1, 1), (1, -1, -1, 0, 0)),
    (1, (0, 1, 1, 0, 0), (2, 0, 0, -1, 1)),
)


def minimal_hitting_sets() -> list[tuple[int, ...]]:
    minimal_masks = []
    for mask in range(1, 1 << 16):
        if not all(any(mask & (1 << vertex) for vertex in edge) for edge in HYPEREDGES):
            continue
        if any(old & mask == old for old in minimal_masks):
            continue
        minimal_masks.append(mask)
    return [
        tuple(index for index in range(16) if mask & (1 << index))
        for mask in minimal_masks
    ]


def gate_matrix_times_two(
    endpoint: tuple[int, tuple[int, ...], tuple[int, ...]],
) -> list[list[int]]:
    scalar, left, right = endpoint
    return [
        [
            scalar * (left[row] * right[column] + right[row] * left[column])
            for column in range(5)
        ]
        for row in range(5)
    ]


def linear_combination(
    matrices: list[list[list[int]]],
    cover: tuple[int, ...],
    coefficients: list[int],
) -> list[list[int]]:
    return [
        [
            sum(
                coefficient * matrices[gate][row][column]
                for gate, coefficient in zip(cover, coefficients, strict=True)
            )
            for column in range(5)
        ]
        for row in range(5)
    ]


def determinant_bareiss(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    denominator = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size) if work[row][pivot_index]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row],
                work[pivot_index],
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % denominator == 0
                work[row][column] = numerator // denominator
        denominator = pivot
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
    return sign * work[-1][-1]


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, len(work)):
            scale = work[row][column] * inverse % prime
            for index in range(column, len(work)):
                work[row][index] = (
                    work[row][index] - scale * work[column][index]
                ) % prime
    return result % prime


def main() -> None:
    covers = minimal_hitting_sets()
    assert len(covers) == 53
    assert [cover for cover in covers if len(cover) == 4] == [UNIQUE_FOUR_COVER]
    nonfour_covers = [cover for cover in covers if cover != UNIQUE_FOUR_COVER]
    assert set(nonfour_covers) == set(EXPECTED_DETERMINANTS)

    matrices = [gate_matrix_times_two(endpoint) for endpoint in FACTOR_ENDPOINTS]
    assert len(matrices) == 16
    results = []
    for cover in nonfour_covers:
        flipped_gate = SIGN_FLIPS.get(cover)
        coefficients = [-1 if gate == flipped_gate else 1 for gate in cover]
        witness = linear_combination(matrices, cover, coefficients)
        determinant_times_32 = determinant_bareiss(witness)
        expected = EXPECTED_DETERMINANTS[cover]
        assert determinant_times_32 == 32 * expected
        assert determinant_times_32 != 0
        for prime in (101, 103):
            assert determinant_mod(witness, prime) == determinant_times_32 % prime
        results.append(
            {
                "cover": list(cover),
                "coefficients": coefficients,
                "determinant": expected,
            }
        )

    print(
        json.dumps(
            {
                "status": "audited",
                "method": "hardcoded factor endpoints, Bareiss, and modular elimination",
                "minimal_cover_count": len(covers),
                "nonfour_cover_count": len(nonfour_covers),
                "perfect_pairing_certificates": results,
                "scaled_matrix_convention": "audit matrix = 2 * canonical gate matrix",
                "all_nonfour_covers_excluded": True,
                "coefficient_search_used": False,
                "sympy_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
