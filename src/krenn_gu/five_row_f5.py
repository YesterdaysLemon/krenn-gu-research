"""Pure finite-field primitives for five-row projective F5 censuses."""

from __future__ import annotations


PRIME = 5
ZERO = (0, 0, 0)
COORDINATES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def rank_mod(rows: object) -> int:
    matrix = [
        [int(value) % PRIME for value in row]
        for row in rows
        if any(int(value) % PRIME for value in row)
    ]
    pivot_row = 0
    for column in range(3):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, PRIME)
        matrix[pivot_row] = [
            value * inverse % PRIME for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    if not any(value % PRIME for value in vector):
        return ZERO
    first = next(value % PRIME for value in vector if value % PRIME)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in vector)


def pair_contains_coordinate(
    left: tuple[int, ...], right: tuple[int, ...]
) -> bool:
    pair_rank = rank_mod((left, right))
    return any(
        rank_mod((left, right, coordinate)) == pair_rank
        for coordinate in COORDINATES
    )


__all__ = [
    "COORDINATES",
    "PRIME",
    "ZERO",
    "canonical",
    "pair_contains_coordinate",
    "rank_mod",
]
