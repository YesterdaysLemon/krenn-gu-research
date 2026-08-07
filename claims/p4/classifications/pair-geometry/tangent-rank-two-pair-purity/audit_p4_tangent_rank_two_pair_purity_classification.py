#!/usr/bin/env python3
"""Independent exact audit of tangent rank-two pure representatives."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def product(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def rank(columns):
    matrix = [[columns[column][row] for column in range(len(columns))] for row in range(6)]
    result = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(result, 6) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[result], matrix[pivot] = matrix[pivot], matrix[result]
        value = matrix[result][column]
        matrix[result] = [entry / value for entry in matrix[result]]
        for row in range(6):
            if row == result or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right
                for left, right in zip(matrix[row], matrix[result])
            ]
        result += 1
    return result


def pair_rank(left, right):
    return rank([product(u, v) for u in left for v in right])


def permanent_dp(rows):
    state = {0: Fraction(1)}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, Fraction(0)) + value * entry
        state = following
    return state[(1 << 4) - 1]


def permute(row):
    order = (2, 0, 3, 1)
    return tuple(row[index] for index in order)


def audit(planes):
    rational = tuple(
        tuple(tuple(Fraction(value) for value in permute(row)) for row in plane)
        for plane in planes
    )
    coefficients = {
        bits: permanent_dp(tuple(rational[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    profile = [
        pair_rank(rational[i], rational[j])
        for i, j in itertools.combinations(range(4), 2)
    ]
    return {bits: value for bits, value in coefficients.items() if value}, profile


def main() -> None:
    full_planes = (
        ((1, 0, 0, 0), (0, 1, 1, 1)),
        ((1, 0, 0, 0), (0, 1, 1, 1)),
        ((1, 0, 0, 0), (0, 1, 2, 3)),
        ((-2, 4, -5, 0), (-4, 3, 0, -5)),
    )
    support_planes = (
        ((1, 0, 0, 0), (0, 1, 1, 0)),
        ((1, 0, 0, 0), (0, 1, 1, 0)),
        ((1, 1, -1, 0), (0, 1, 1, 1)),
        ((0, 1, -1, 0), (1, 1, 1, -1)),
    )
    full_coefficients, full_profile = audit(full_planes)
    support_coefficients, support_profile = audit(support_planes)

    assert len(full_coefficients) == 4
    anchor = full_coefficients[(1, 1, 0, 0)]
    assert full_coefficients[(1, 1, 0, 1)] == 2 * anchor
    assert full_coefficients[(1, 1, 1, 0)] == 12 * anchor
    assert full_coefficients[(1, 1, 1, 1)] == 24 * anchor
    assert full_profile == [2, 3, 4, 3, 4, 4]

    assert len(support_coefficients) == 2
    assert support_coefficients[(1, 1, 1, 1)] == -support_coefficients[(1, 1, 0, 1)]
    assert support_profile == [2, 4, 3, 4, 3, 4]

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "source-permuted subset-DP permanent",
                "full_support_nonzero_coefficients": len(full_coefficients),
                "full_support_pair_profile": full_profile,
                "support_two_nonzero_coefficients": len(support_coefficients),
                "support_two_pair_profile": support_profile,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
