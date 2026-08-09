#!/usr/bin/env python3
"""Independent modular audit of the unique four-gate obstruction."""

from __future__ import annotations

import itertools
import json

CYCLE_EDGES = ((1, 2), (2, 3), (3, 4), (4, 1))
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
UNIQUE_GATES = (0, 3, 5, 9)

VECTORS = {
    "x01": (0, -1, -1, 0, 0),
    "x02": (1, 0, 0, 0, -2),
    "x10": (0, 0, 0, -1, 1),
    "x12": (-1, 0, 1, 0, 0),
    "x20": (-1, 1, 0, 0, 0),
    "x21": (1, 0, 0, 2, 0),
}
BAD_NAMES = (
    ("x10", "x21"),
    ("x12", "x20"),
    ("x12", "x21"),
    ("x01", "x20"),
    ("x02", "x20"),
    ("x02", "x21"),
    ("x01", "x10"),
    ("x01", "x12"),
    ("x02", "x10"),
)
K_BASIS_INDICES = (0, 1, 2, 4, 6)
PAIRS = tuple(itertools.combinations(range(5), 2))


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = pow(work[pivot_row][column], prime - 2, prime)
        work[pivot_row] = [entry * scale % prime for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def determinant_three(matrix: list[list[int]], prime: int) -> int:
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % prime


def product_two(left: tuple[int, ...], right: tuple[int, ...]) -> list[int]:
    return [
        left[first] * right[second] + left[second] * right[first]
        for first, second in PAIRS
    ]


def catalecticant_value(
    k_basis: list[list[int]], left_index: int, right_index: int
) -> list[list[int]]:
    result = [[0] * 5 for _ in range(5)]
    for row, quadratic in enumerate(k_basis):
        for source_coordinate in range(5):
            if len({source_coordinate, left_index, right_index}) < 3:
                continue
            complement = tuple(
                index
                for index in range(5)
                if index not in {source_coordinate, left_index, right_index}
            )
            result[row][source_coordinate] = quadratic[PAIRS.index(complement)]
    return result


def minimal_hitting_sets() -> list[int]:
    minimal = []
    for mask in range(1, 1 << 16):
        if not all(any(mask & (1 << vertex) for vertex in edge) for edge in HYPEREDGES):
            continue
        if any(old & mask == old for old in minimal):
            continue
        minimal.append(mask)
    return minimal


def main() -> None:
    independent_sets = []
    vertices = (1, 2, 3, 4)
    for size in range(5):
        for subset in itertools.combinations(vertices, size):
            if all(not ({left, right} <= set(subset)) for left, right in CYCLE_EDGES):
                independent_sets.append(subset)
    assert [subset for subset in independent_sets if len(subset) == 2] == [
        (1, 3),
        (2, 4),
    ]

    covers = minimal_hitting_sets()
    four_covers = [
        tuple(index for index in range(16) if mask & (1 << index))
        for mask in covers
        if mask.bit_count() == 4
    ]
    assert four_covers == [UNIQUE_GATES]
    assert len(covers) == 53

    bad = [product_two(VECTORS[left], VECTORS[right]) for left, right in BAD_NAMES]
    k_basis = [bad[index] for index in K_BASIS_INDICES]
    even_value = catalecticant_value(k_basis, 0, 2)
    odd_value = catalecticant_value(k_basis, 0, 1)

    results = []
    for prime in (5, 7, 11):
        assert rank_mod(even_value, prime) == 3
        assert rank_mod(odd_value, prime) == 3
        even_submatrix = [
            [even_value[row][column] for column in (1, 3, 4)] for row in (0, 3, 4)
        ]
        odd_submatrix = [
            [odd_value[row][column] for column in (2, 3, 4)] for row in (0, 2, 4)
        ]
        even_minor = determinant_three(even_submatrix, prime)
        odd_minor = determinant_three(odd_submatrix, prime)
        assert even_minor == -4 % prime
        assert odd_minor == 4 % prime
        results.append(
            {
                "prime": prime,
                "even_rank": 3,
                "odd_rank": 3,
                "even_minor": even_minor,
                "odd_minor": odd_minor,
            }
        )

    print(
        json.dumps(
            {
                "status": "audited",
                "method": "independent cycle combinatorics and modular matrices",
                "unique_four_gate_cover": list(UNIQUE_GATES),
                "remaining_minimal_covers": 52,
                "results": results,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
