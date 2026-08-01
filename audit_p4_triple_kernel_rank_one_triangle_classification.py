#!/usr/bin/env python3
"""Independent exact-rational audit of the triple-kernel triangle arc."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

PAIRS = tuple(itertools.combinations(range(4), 2))


def add(*vectors):
    return tuple(sum((vector[i] for vector in vectors), Fraction(0)) for i in range(4))


def scale(value, vector):
    value = Fraction(value)
    return tuple(value * coordinate for coordinate in vector)


def permanent(rows):
    total = Fraction(0)
    for permutation in itertools.permutations(range(4)):
        term = Fraction(1)
        for row in range(4):
            term *= rows[row][permutation[row]]
        total += term
    return total


def pair_product(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def rank(rows):
    matrix = [list(map(Fraction, row)) for row in rows]
    if not matrix:
        return 0
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(row, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        value = matrix[row][column]
        matrix[row] = [entry / value for entry in matrix[row]]
        for i in range(len(matrix)):
            if i == row or not matrix[i][column]:
                continue
            value = matrix[i][column]
            matrix[i] = [x - value * y for x, y in zip(matrix[i], matrix[row])]
        row += 1
    return row


def pair_rank(left, right):
    return rank([pair_product(u, v) for u in left for v in right])


def same_plane(left, right):
    return rank(list(left)) == rank(list(right)) == rank(list(left) + list(right)) == 2


def main():
    A = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    B = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    e = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    C = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))

    v1 = add(B, scale(-1, C))
    v2 = add(A, scale(-1, B))
    v3 = add(A, C)
    assert pair_product(v1, v2) == pair_product(v1, v3)
    assert pair_product(v1, v2) == scale(-1, pair_product(v2, v3))
    assert permanent((e, v1, v2, v3)) == 2

    w_a = add(A, B)
    w_c = add(B, C)
    opposite_parameters = (
        (1, 2, 3, 5),
        (2, -1, 1, 3),
        (1, 0, 0, 1),
    )
    epsilon_values = (Fraction(1, 2), Fraction(2), Fraction(-3))
    target_profiles = set()
    audited_arcs = 0

    for p, q, r, s in opposite_parameters:
        assert p * s - q * r != 0
        y0 = add(scale(p, w_a), scale(q, w_c))
        w0 = add(scale(r, w_a), scale(s, w_c))
        x0 = add(e, w0)
        target = ((y0, x0), (e, v1), (e, v2), (e, v3))

        coefficients = {}
        for bits in itertools.product((0, 1), repeat=4):
            rows = tuple(target[mode][bits[mode]] for mode in range(4))
            coefficients[bits] = permanent(rows)
        assert coefficients[(1, 1, 1, 1)] == 2
        assert all(
            value == 0
            for bits, value in coefficients.items()
            if bits != (1, 1, 1, 1)
        )
        profile = tuple(pair_rank(target[i], target[j]) for i, j in PAIRS)
        assert min(profile) >= 3
        assert profile[3:] == (3, 3, 3)
        target_profiles.add(profile)

        for epsilon in epsilon_values:
            k1 = add(e, scale(epsilon, B))
            k2 = add(e, scale(-epsilon, A))
            k3 = add(e, scale(-epsilon, C))
            kernels = (k1, k2, k3)

            lifted_y0 = y0
            lifted_x0 = add(x0, scale(epsilon, A))
            lifted = (
                (lifted_y0, lifted_x0),
                (k1, v1),
                (k2, v2),
                (k3, v3),
            )

            for row in (lifted_y0, lifted_x0):
                g = row[0] - row[1] + row[3] - epsilon * row[2]
                assert g == 0

            coefficients = {}
            for bits in itertools.product((0, 1), repeat=4):
                rows = tuple(lifted[mode][bits[mode]] for mode in range(4))
                coefficients[bits] = permanent(rows)
            assert coefficients[(1, 1, 1, 1)] == 2
            assert all(
                value == 0
                for bits, value in coefficients.items()
                if bits != (1, 1, 1, 1)
            )

            # Rebuild the source-scaled support-star planes independently.
            star_1 = (add(e, scale(epsilon, B)), add(e, scale(epsilon, C)))
            star_2 = (add(scale(epsilon, A), scale(-1, e)), add(scale(epsilon, B), scale(-1, e)))
            star_3 = (add(e, scale(-epsilon, C)), add(scale(epsilon, A), e))
            assert same_plane(lifted[1], star_1)
            assert same_plane(lifted[2], star_2)
            assert same_plane(lifted[3], star_3)

            # The limiting kernel rows and opposite plane are exact.
            assert tuple(add(kernels[i], scale(-1, e)) for i in range(3)) == (
                scale(epsilon, B),
                scale(-epsilon, A),
                scale(-epsilon, C),
            )
            audited_arcs += 1

    print(
        json.dumps(
            {
                "status": "audited",
                "arithmetic": "exact rationals",
                "opposite_planes": len(opposite_parameters),
                "nonzero_arc_parameters": len(epsilon_values),
                "audited_arcs": audited_arcs,
                "target_pair_profiles": [list(profile) for profile in sorted(target_profiles)],
                "component_16_row_span_checks": 3 * audited_arcs,
                "role": "independent corroboration of the characteristic-zero identities",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
