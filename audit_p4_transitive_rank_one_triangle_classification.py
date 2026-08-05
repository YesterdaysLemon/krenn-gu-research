#!/usr/bin/env python3
"""Independent rational audit of the transitive rank-one triangle."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
WORDS = tuple(itertools.product((0, 1), repeat=4))


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
    return state[15]


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


def determinant(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work)) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            factor = work[row][column] / value
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[column], strict=True)
            ]
    return result


def add(left, right):
    return tuple(Fraction(a) + Fraction(b) for a, b in zip(left, right, strict=True))


def scale(scalar, vector):
    return tuple(Fraction(scalar) * Fraction(entry) for entry in vector)


def contraction_covector(rows):
    identity = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
    return tuple(permanent_dp((identity[coordinate], *rows)) for coordinate in range(4))


def product_vector(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def pair_rank(left, right):
    columns = [product_vector(first, second) for first in left for second in right]
    return rank([list(row) for row in zip(*columns, strict=True)])


def pluecker(plane):
    return tuple(
        plane[0][i] * plane[1][j] - plane[0][j] * plane[1][i]
        for i, j in PAIRS
    )


def proportional(left, right):
    return all(
        left[i] * right[j] == left[j] * right[i]
        for i, j in itertools.combinations(range(6), 2)
    )


def main():
    alpha, delta, b2, b3, d2, d3 = map(Fraction, (2, 3, 5, 7, 11, 13))
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    b = (0, 0, b2, b3)
    d = (0, 0, d2, d3)
    leaves = (
        (c, add(scale(alpha, a), b)),
        (c, a),
        (add(scale(delta, c), d), a),
    )
    covectors = {
        bits: contraction_covector(tuple(leaves[mode][bits[mode]] for mode in range(3)))
        for bits in itertools.product((0, 1), repeat=3)
    }
    expected = {
        (0, 0, 0): (0, 0, -2 * d3, -2 * d2),
        (1, 0, 0): (
            -b2 * d3 - b3 * d2,
            b2 * d3 + b3 * d2,
            -2 * b3 * delta,
            -2 * b2 * delta,
        ),
        (1, 1, 0): (
            b2 * d3 + b3 * d2,
            b2 * d3 + b3 * d2,
            2 * alpha * d3,
            2 * alpha * d2,
        ),
        (1, 1, 1): (0, 0, 2 * b3, 2 * b2),
    }
    assert {bits: value for bits, value in covectors.items() if any(value)} == expected

    forbidden = [expected[bits] for bits in ((0, 0, 0), (1, 0, 0), (1, 1, 0))]
    minors = tuple(
        determinant([[row[column] for column in columns] for row in forbidden])
        for columns in itertools.combinations(range(4), 3)
    )
    cross_sum = b2 * d3 + b3 * d2
    cross_difference = b2 * d3 - b3 * d2
    assert minors == (
        4 * d3 * cross_sum**2,
        4 * d2 * cross_sum**2,
        4 * delta * cross_difference * cross_sum,
        4 * delta * cross_difference * cross_sum,
    )

    # Independently check the same-support singleton boundary.  Its desired
    # active covector is the negative of the forbidden all-kernel covector.
    singleton = (
        (c, add(scale(Fraction(2), a), (0, 0, 1, 0))),
        (c, a),
        (add(scale(Fraction(3), c), (0, 0, 1, 0)), a),
    )
    singleton_covectors = {
        bits: contraction_covector(
            tuple(singleton[mode][bits[mode]] for mode in range(3))
        )
        for bits in itertools.product((0, 1), repeat=3)
    }
    assert singleton_covectors[(1, 1, 1)] == tuple(
        -entry for entry in singleton_covectors[(0, 0, 0)]
    )
    assert tuple(
        pair_rank(singleton[left], singleton[right])
        for left, right in ((0, 1), (0, 2), (1, 2))
    ) == (3, 3, 3)

    p, q, alpha = map(Fraction, (2, 3, 2))
    b_plus = (0, 0, 1, 1)
    b_minus = (0, 0, 1, -1)
    family = (
        (add(a, scale(p, b_plus)), add(c, scale(q, b_plus))),
        (c, add(scale(alpha, a), b_plus)),
        (c, a),
        (b_minus, a),
    )
    tensor = {
        word: permanent_dp(tuple(family[mode][word[mode]] for mode in range(4)))
        for word in WORDS
    }
    assert {word: value for word, value in tensor.items() if value} == {
        (0, 1, 1, 1): 4 * p,
        (1, 1, 1, 1): 4 * q,
    }
    profile = tuple(pair_rank(family[left], family[right]) for left, right in PAIRS)
    assert profile == (4, 3, 4, 3, 3, 3)

    # Replay one punctured component-eleven arc and its limit.
    epsilon = Fraction(1, 5)
    target = (
        (add(a, scale(q, b_plus)), add(c, scale(p, b_plus))),
        (a, add(scale(alpha, c), b_plus)),
        (a, c),
        (b_minus, c),
    )
    arc = (
        target[0],
        target[1],
        (a, add(scale(alpha, c), scale(epsilon, b_plus))),
        target[3],
    )
    component_eleven = (
        target[0],
        target[1],
        (a, add(scale(alpha / epsilon, c), b_plus)),
        target[3],
    )
    assert all(proportional(pluecker(left), pluecker(right)) for left, right in zip(arc, component_eleven, strict=True))
    limit = (target[0], target[1], (a, scale(alpha, c)), target[3])
    assert all(proportional(pluecker(left), pluecker(right)) for left, right in zip(limit, target, strict=True))

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP contractions and rational Pluecker arc",
                "determinantal_factor_value": str(cross_sum),
                "surviving_pair_profile": profile,
                "component_eleven_arc_replayed": True,
                "support_one_boundary_zero": True,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
