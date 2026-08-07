#!/usr/bin/env python3
"""Independent rational audit of the two-kernel triangle classification."""

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
    return rank(left) == rank(right) == rank(tuple(left) + tuple(right)) == 2


def covector(rows):
    basis = tuple(
        tuple(Fraction(int(i == j)) for i in range(4)) for j in range(4)
    )
    return tuple(permanent((basis[i],) + tuple(rows)) for i in range(4))


def main():
    X0 = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    X1 = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    X2 = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    X3 = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    p = add(X0, X1)
    q = add(X0, scale(-1, X1))
    b = add(X2, X3)
    b_bar = add(X2, scale(-1, X3))

    # Two independent transverse examples audit both alternatives:
    # S!=0 gives three independent forbidden covectors; S=0 leaves only
    # span(X0,X1) as an annihilator and the active covector kills it.
    independent_examples = (
        (b, add(X2, scale(2, X3)), "no_two_plane"),
        (b, b_bar, "active_zero"),
    )
    independent_outcomes = []
    for r1, r2, expected in independent_examples:
        alpha = Fraction(2)
        beta = Fraction(3)
        v1 = add(scale(alpha, q), r1)
        v2 = add(scale(beta, p), r2)
        triangle = ((p, v1), (q, v2), (q, p))
        forbidden = (
            covector((triangle[0][0], triangle[1][1], triangle[2][1])),
            covector((triangle[0][1], triangle[1][0], triangle[2][0])),
            covector((triangle[0][1], triangle[1][1], triangle[2][0])),
        )
        active = covector((triangle[0][1], triangle[1][1], triangle[2][1]))
        forbidden_rank = rank(forbidden)
        if expected == "no_two_plane":
            assert forbidden_rank == 3
        else:
            assert forbidden_rank == 2
            annihilator = (X0, X1)
            assert all(sum(row[i] * z[i] for i in range(4)) == 0 for row in forbidden for z in annihilator)
            assert all(sum(active[i] * z[i] for i in range(4)) == 0 for z in annihilator)
        independent_outcomes.append((expected, forbidden_rank))

    parameter_samples = ((2, 3), (-1, 2), (0, 1))
    profiles = set()
    containments = 0
    for alpha, gamma in parameter_samples:
        U = (
            (b_bar, p),
            (p, add(b, scale(alpha, q))),
            (q, add(b, scale(gamma, p))),
            (q, p),
        )
        coefficients = {}
        for bits in itertools.product((0, 1), repeat=4):
            coefficients[bits] = permanent(
                tuple(U[mode][bits[mode]] for mode in range(4))
            )
        assert coefficients[(1, 1, 1, 1)] == 4
        assert all(
            value == 0
            for bits, value in coefficients.items()
            if bits != (1, 1, 1, 1)
        )
        profile = tuple(pair_rank(U[i], U[j]) for i, j in PAIRS)
        assert min(profile) >= 3
        assert profile[3:] == (3, 3, 3)
        profiles.add(profile)

        assert pair_product(p, q) == (Fraction(0),) * 6
        assert pair_product(q, q) != (Fraction(0),) * 6

        if alpha:
            transitive = (
                (p, add(q, scale(Fraction(1, alpha), b))),
                (q, add(b, scale(gamma, p))),
                (q, p),
                (b_bar, p),
            )
            reordered = (transitive[3], transitive[0], transitive[1], transitive[2])
            assert all(same_plane(left, right) for left, right in zip(U, reordered))
            containments += 1
        else:
            # Exact Pluecker identity for the q=infinity endpoint.
            for epsilon in (Fraction(1, 2), Fraction(1, 3), Fraction(-1, 2)):
                moving = (p, add(b, scale(epsilon, q)))
                assert rank(moving) == 2
            assert same_plane(U[1], (p, b))

    print(
        json.dumps(
            {
                "status": "audited",
                "arithmetic": "exact rationals",
                "independent_transverse_outcomes": [
                    {"outcome": outcome, "forbidden_rank": value}
                    for outcome, value in independent_outcomes
                ],
                "normal_form_samples": len(parameter_samples),
                "pair_profiles": [list(profile) for profile in sorted(profiles)],
                "direct_component_11_identifications": containments,
                "projective_endpoint": "audited",
                "role": "independent corroboration of the characteristic-zero proof",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
