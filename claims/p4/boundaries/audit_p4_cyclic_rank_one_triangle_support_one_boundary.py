#!/usr/bin/env python3
"""Independent exact audit of singleton cyclic rank-one triangle supports."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
LABELS = tuple((index,) for index in range(4)) + PAIRS


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(scalar, vector):
    return tuple(Fraction(scalar) * entry for entry in vector)


def permanent_dp(rows):
    states = {0: Fraction(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, Fraction(0)) + value * entry
        states = following
    return states[15]


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


def factors(label, gain):
    basis = tuple(tuple(Fraction(i == j) for j in range(4)) for i in range(4))
    if len(label) == 1:
        return basis[label[0]], basis[label[0]]
    left, right = label
    return add(basis[left], scale(gain, basis[right])), add(basis[left], scale(-gain, basis[right]))


def product(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def pair_rank(left, right):
    columns = [product(u, v) for u in left for v in right]
    return rank([list(row) for row in zip(*columns, strict=True)])


def cubic(rows):
    basis = tuple(tuple(Fraction(i == j) for j in range(4)) for i in range(4))
    return tuple(permanent_dp((basis[coordinate], *rows)) for coordinate in range(4))


def leaves(labels, gains):
    (u1, v1), (u2, v2), (u3, v3) = (
        factors(label, gain) for label, gain in zip(labels, gains, strict=True)
    )
    return ((u1, u3), (u2, v1), (v3, v2)), cubic((u1, u2, v3)), cubic((u3, v1, v2))


def canonical(labels):
    return min(
        tuple(sorted(tuple(sorted(permutation[index] for index in label)) for label in labels))
        for permutation in itertools.permutations(range(4))
    )


def main() -> None:
    # Independent rational specialization of the symbolic support census.
    gains = (Fraction(2), Fraction(3), Fraction(5))
    survivors = set()
    for ordered_labels in itertools.product(LABELS, repeat=3):
        if not any(len(label) == 1 for label in ordered_labels):
            continue
        planes, kernel_cubic, active_cubic = leaves(ordered_labels, gains)
        if any(rank(plane) < 2 for plane in planes):
            continue
        if min(pair_rank(planes[left], planes[right]) for left, right in ((0, 1), (0, 2), (1, 2))) < 3:
            continue
        independent = rank((kernel_cubic, active_cubic)) == 2
        if any(active_cubic) and (not any(kernel_cubic) or independent):
            survivors.add(canonical(ordered_labels))

    expected = {
        ((0,), (0, 1), (2, 3)),
        ((0,), (1, 2), (1, 3)),
        ((0,), (1,), (2, 3)),
    }
    assert survivors == expected

    # Replay each limiting leaf tuple at epsilon=0 and a punctured rational
    # point.  The punctured support degrees identify path, star, path.
    arc_data = (
        (((0, 2), (0, 1), (2, 3)), ((0,), (0, 1), (2, 3)), (2, 2, 1, 1)),
        (((0, 1), (1, 2), (1, 3)), ((0,), (1, 2), (1, 3)), (3, 1, 1, 1)),
        (((0, 2), (1, 3), (2, 3)), ((0,), (1,), (2, 3)), (2, 2, 1, 1)),
    )
    for index, (lifted_labels, target_labels, expected_degrees) in enumerate(arc_data):
        lifted_gains = list(gains)
        lifted_gains[0] = Fraction(1, 7)
        if index == 2:
            lifted_gains[1] = Fraction(1, 11)
        lifted, _, _ = leaves(lifted_labels, tuple(lifted_gains))
        target, kernel, active = leaves(target_labels, gains)
        limiting_gains = list(gains)
        limiting_gains[0] = Fraction(0)
        if index == 2:
            limiting_gains[1] = Fraction(0)
        limiting, limiting_kernel, limiting_active = leaves(
            lifted_labels, tuple(limiting_gains)
        )
        assert limiting == target
        assert limiting_kernel == kernel
        assert limiting_active == active
        assert all(rank(plane) == 2 for plane in lifted + target)
        assert rank((kernel, active)) == 2
        degrees = [0, 0, 0, 0]
        for left, right in lifted_labels:
            degrees[left] += 1
            degrees[right] += 1
        assert tuple(sorted(degrees, reverse=True)) == expected_degrees

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent rational subset-DP support census",
                "surviving_support_orbits": [str(orbit) for orbit in sorted(survivors, key=str)],
                "punctured_component_types": [17, 16, 17],
                "parameter_search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
