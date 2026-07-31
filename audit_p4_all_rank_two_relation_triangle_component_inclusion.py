#!/usr/bin/env python3
"""Independent rational audit of the rank-two triangle containment."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def add(left, right):
    return tuple(Fraction(left[i]) + Fraction(right[i]) for i in range(4))


def scale(scalar, vector):
    return tuple(Fraction(scalar) * Fraction(value) for value in vector)


def product(left, right):
    return tuple(
        Fraction(left[i]) * Fraction(right[j])
        + Fraction(left[j]) * Fraction(right[i])
        for i, j in PAIRS
    )


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


def rref(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return work


def rank(matrix):
    return sum(any(entry for entry in row) for row in rref(matrix))


def pair_matrix(left, right):
    columns = [product(u, v) for u in left for v in right]
    return [list(row) for row in zip(*columns)]


def null_vector_rank(matrix):
    reduced = rref(matrix)
    pivots = []
    for row in reduced:
        pivot = next((index for index, value in enumerate(row) if value), None)
        if pivot is not None:
            pivots.append(pivot)
    free = next(index for index in range(4) if index not in pivots)
    vector = [Fraction(0)] * 4
    vector[free] = 1
    for row, pivot in zip(reduced, pivots):
        vector[pivot] = -row[free]
    return 1 if vector[0] * vector[3] == vector[1] * vector[2] else 2


def main() -> None:
    # Use a normalization different from the primary sample.
    alpha_1, alpha_2, alpha_3 = map(Fraction, (2, 3, 5))
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    target = [
        (b_bar, a_bar),
        (a, add(b, scale(alpha_1, a_bar))),
        (a, add(b, scale(alpha_2, a_bar))),
        (a, add(b, scale(alpha_3, a_bar))),
    ]

    transformed = []
    for plane in target:
        transformed.append(
            tuple(
                (row[0], row[1], alpha_1 * row[2], alpha_1 * row[3])
                for row in plane
            )
        )

    r = alpha_2 / alpha_1
    q = alpha_1 / alpha_3
    component = [
        (a, add(a_bar, scale(q, b))),
        (a, add(a_bar, b)),
        (a, add(scale(r, a_bar), b)),
        (b_bar, a_bar),
    ]
    reordered = [component[3], component[1], component[2], component[0]]
    assert all(rref(left) == rref(right) for left, right in zip(transformed, reordered))

    coefficients = {
        bits: permanent_dp(tuple(target[mode][bits[mode]] for mode in range(4)))
        for bits in BITS
    }
    support = [bits for bits, value in coefficients.items() if value]
    assert support == [(1, 1, 1, 1)]
    assert coefficients[(1, 1, 1, 1)] == -4 * (alpha_1 + alpha_2 + alpha_3)
    assert 1 + q * (r + 1) == (alpha_1 + alpha_2 + alpha_3) / alpha_3

    profile = []
    relation_ranks = []
    for i, j in itertools.combinations(range(4), 2):
        matrix = pair_matrix(target[i], target[j])
        profile.append(rank(matrix))
        relation_ranks.append(null_vector_rank(matrix))
    assert profile == [3, 3, 3, 3, 3, 3]
    assert relation_ranks == [1, 1, 1, 2, 2, 2]

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "rational row spaces plus subset-DP permanent",
                "sample_alphas": [2, 3, 5],
                "component_parameters": {"p": 0, "r": str(r), "q": str(q)},
                "row_spaces_identical": True,
                "pure_support": ["1111"],
                "pair_profile": profile,
                "relation_ranks": relation_ranks,
                "containing_component": 11,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
