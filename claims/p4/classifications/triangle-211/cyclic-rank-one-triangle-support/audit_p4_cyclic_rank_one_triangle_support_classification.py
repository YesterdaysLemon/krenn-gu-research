#!/usr/bin/env python3
"""Independent integer audit of cyclic rank-one support triangles."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
SIGNS = tuple(itertools.product((1, -1), repeat=3))


def root(edge, sign):
    result = [0, 0, 0, 0]
    result[edge[0]] = 1
    result[edge[1]] = sign
    return tuple(result)


def directed_triangle(labels, signs):
    positive = tuple(root(edge, sign) for edge, sign in zip(labels, signs, strict=True))
    negative = tuple(root(edge, -sign) for edge, sign in zip(labels, signs, strict=True))
    return (
        (positive[0], positive[1]),
        (positive[2], negative[0]),
        (negative[1], negative[2]),
    )


def squarefree_product(vectors):
    polynomial = {0: 1}
    for vector in vectors:
        following = {}
        for mask, coefficient in polynomial.items():
            for coordinate, entry in enumerate(vector):
                if not entry or mask & (1 << coordinate):
                    continue
                next_mask = mask | (1 << coordinate)
                following[next_mask] = following.get(next_mask, 0) + coefficient * entry
        polynomial = {mask: coefficient for mask, coefficient in following.items() if coefficient}
    return polynomial


def cubic_covector(vectors):
    polynomial = squarefree_product(vectors)
    return tuple(polynomial.get(15 ^ (1 << coordinate), 0) for coordinate in range(4))


def product_vector(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def rank(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
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
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[result], strict=True)
            ]
        result += 1
    return result


def pair_rank(left, right):
    columns = [product_vector(first, second) for first in left for second in right]
    return rank([list(row) for row in zip(*columns, strict=True)])


def pair_profile(planes):
    return tuple(pair_rank(planes[left], planes[right]) for left, right in ((0, 1), (0, 2), (1, 2)))


def permanent_dp(rows):
    state = {0: 1}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, 0) + value * entry
        state = following
    return state[15]


def switched(labels, signs, vertex_signs):
    return tuple(
        sign * vertex_signs[left] * vertex_signs[right]
        for (left, right), sign in zip(labels, signs, strict=True)
    )


def can_switch(labels, signs, target):
    return any(
        switched(labels, signs, vertex_signs) == target
        for vertex_signs in itertools.product((1, -1), repeat=4)
    )


def main():
    types = {
        "star": ((0, 1), (0, 2), (0, 3)),
        "path": ((0, 1), (1, 2), (2, 3)),
        "triangle": ((0, 1), (1, 2), (0, 2)),
    }
    summaries = {}
    for name, labels in types.items():
        profiles = []
        covector_ranks = []
        for signs in SIGNS:
            planes = directed_triangle(labels, signs)
            profile = pair_profile(planes)
            kernel = cubic_covector((planes[0][0], planes[1][0], planes[2][0]))
            active = cubic_covector((planes[0][1], planes[1][1], planes[2][1]))
            covector_rank = rank((kernel, active))
            profiles.append(profile)
            covector_ranks.append(covector_rank)

            if name in ("star", "path"):
                assert profile == (3, 3, 3)
                assert covector_rank == 2
                assert can_switch(labels, signs, (1, 1, 1))
            else:
                assert profile == (2, 2, 2)
                assert covector_rank == 1
                assert (not any(kernel)) != (not any(active))
                nonzero = active if not any(kernel) else kernel
                assert nonzero[:3] == (0, 0, 0)
                assert abs(nonzero[3]) == 2
                holonomy = signs[0] * signs[1] * signs[2]
                assert can_switch(labels, signs, (1, 1, holonomy))

        summaries[name] = {
            "sign_sheets": len(profiles),
            "pair_profile": profiles[0],
            "covector_rank": covector_ranks[0],
        }

    # Weighted support-triangle holonomy at lambda=2, mu=3.
    lam, mu = 2, 3
    for nu in (5, lam * mu):
        planes = (
            ((1, lam, 0, 0), (0, 1, mu, 0)),
            ((1, 0, nu, 0), (1, -lam, 0, 0)),
            ((0, 1, -mu, 0), (1, 0, -nu, 0)),
        )
        kernel = cubic_covector((planes[0][0], planes[1][0], planes[2][0]))
        active = cubic_covector((planes[0][1], planes[1][1], planes[2][1]))
        assert kernel == (0, 0, 0, nu - lam * mu)
        assert active == (0, 0, 0, -nu - lam * mu)
        if nu == lam * mu:
            assert pair_profile(planes) == (2, 2, 2)

    # Repeated adjacent support has identical kernel and escape covectors.
    nu = 5
    adjacent = (
        ((1, lam, 0, 0), (1, mu, 0, 0)),
        ((1, 0, nu, 0), (1, -lam, 0, 0)),
        ((1, -mu, 0, 0), (1, 0, -nu, 0)),
    )
    adjacent_kernel = cubic_covector((adjacent[0][0], adjacent[1][0], adjacent[2][0]))
    adjacent_active = cubic_covector((adjacent[0][1], adjacent[1][1], adjacent[2][1]))
    assert adjacent_kernel == adjacent_active == (0, 0, 0, nu * (lam - mu))

    # Repeated disjoint support opens exactly into a component-eight star.
    p, q, r = 2, 3, 2
    profiles = {}
    for k in (0, 5):
        opening = (
            ((1, 0, p, -p), (0, 1, q, -q)),
            ((1, 1, 0, 0), (1, r, 0, 0)),
            ((0, 0, 1, 1), (1, -1, 0, 0)),
            ((1, -r, 0, 0), (0, k, 1, -1)),
        )
        tensor = {
            word: permanent_dp(tuple(opening[mode][word[mode]] for mode in range(4)))
            for word in itertools.product((0, 1), repeat=4)
        }
        assert {word: value for word, value in tensor.items() if value} == {
            (0, 1, 1, 1): -2 * p * (r - 1),
            (1, 1, 1, 1): -2 * q * (r - 1),
        }
        profiles[k] = tuple(
            pair_rank(opening[left], opening[right]) for left, right in PAIRS
        )
    assert profiles == {0: (3, 4, 4, 3, 3, 3), 5: (3, 4, 4, 3, 3, 4)}

    repeated = (0, 1)
    for sign in (1, -1):
        planes = directed_triangle(
            (repeated, repeated, repeated),
            (sign, -sign, sign),
        )
        assert pair_profile(planes) == (1, 1, 1)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent squarefree multiplication and rational row reduction",
                "distinct_support_types": summaries,
                "weighted_triangle_holonomy_replayed": True,
                "repeated_adjacent_support": "zero or degenerate",
                "repeated_disjoint_profiles": profiles,
                "all_rank_three_survivors": ("star", "path", "component-eight boundary"),
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
