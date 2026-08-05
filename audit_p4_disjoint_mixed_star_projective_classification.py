#!/usr/bin/env python3
"""Independent rational audit of the projective mixed-star boundary."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def add(*vectors):
    return tuple(sum((Fraction(vector[i]) for vector in vectors), Fraction(0)) for i in range(4))


def scale(scalar, vector):
    return tuple(Fraction(scalar) * Fraction(value) for value in vector)


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


def product(left, right):
    return tuple(
        Fraction(left[i]) * Fraction(right[j])
        + Fraction(left[j]) * Fraction(right[i])
        for i, j in PAIRS
    )


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    result = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(result, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        value = work[result][column]
        work[result] = [entry / value for entry in work[result]]
        for row in range(len(work)):
            if row == result or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right for left, right in zip(work[row], work[result])]
        result += 1
    return result


def make_planes(A, B, h, g, p, j, kappa, eta):
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    x_0 = add(scale(A, a), scale(B, a_bar), b, scale(-1, b_bar))
    y_1 = add(scale(-A * g, a), scale(h, a_bar), scale(g, b), scale(p, b_bar))
    y_2 = add(scale(-A * j, a), scale(eta, a_bar), scale(j, b), scale(kappa, b_bar))
    return ((b_bar, x_0), (y_1, a), (y_2, a), (a_bar, b))


def pair_rank(left, right):
    columns = [product(u, v) for u in left for v in right]
    return rank([list(row) for row in zip(*columns)])


def matrix_rank(A, B, h, g, p):
    matrix = (
        (0, h, p),
        (B * g + h, h - B * p, g + p),
        (A * A * g + B * h, 0, B * g + h),
    )
    return rank(matrix)


def main() -> None:
    representatives = [
        (2, 2, 1, Fraction(-1, 2), Fraction(1, 2)),
        (-2, 2, 1, Fraction(-1, 2), Fraction(-1, 2)),
        (2, 2, 0, 1, 0),
        (3, 0, 0, 0, 1),
        (0, 0, 0, 1, 2),
    ]
    assert all(matrix_rank(*sample) == 1 for sample in representatives)

    samples = [
        (1, 1, 0, 1, 0, 1, 2, -1),
        (1, 1, 0, 1, 0, 0, 1, 0),
        (0, 0, 0, 1, 2, 1, 2, 0),
    ]
    profiles = []
    for sample in samples:
        planes = make_planes(*map(Fraction, sample))
        assert all(rank(plane) == 2 for plane in planes)
        coefficients = {
            bits: permanent_dp(tuple(planes[mode][bits[mode]] for mode in range(4)))
            for bits in BITS
        }
        assert [bits for bits, value in coefficients.items() if value] == [(1, 1, 1, 1)]
        assert coefficients[(1, 1, 1, 1)] == 4
        profiles.append(
            [
                pair_rank(planes[left], planes[right])
                for left, right in itertools.combinations(range(4), 2)
            ]
        )
    assert [min(profile) for profile in profiles] == [3, 2, 3]

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "rational projective fibers plus subset-DP permanent",
                "rank_one_strata_replayed": len(representatives),
                "boundary_pair_profiles": profiles,
                "rank_one_base_plus_fiber_dimension": 2,
                "incidence_component_lower_bound": 3,
                "containing_component": 8,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
