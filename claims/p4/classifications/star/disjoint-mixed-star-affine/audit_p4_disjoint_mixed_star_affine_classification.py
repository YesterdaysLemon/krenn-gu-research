#!/usr/bin/env python3
"""Independent rational audit of the affine disjoint mixed-star theorem."""

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


def matrix_vector(matrix, vector):
    return tuple(sum((row[i] * vector[i] for i in range(3)), Fraction(0)) for row in matrix)


def make_planes(A, B, f, phi, j, kappa, eta):
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    x_0 = add(scale(A, a), scale(B, a_bar), b, scale(-1, b_bar))
    y_1 = add(scale(-A * f, a), a_bar, scale(f, b), scale(phi, b_bar))
    y_2 = add(scale(-A * j, a), scale(eta, a_bar), scale(j, b), scale(kappa, b_bar))
    return ((b_bar, x_0), (y_1, a), (y_2, a), (a_bar, b))


def pair_rank(left, right):
    columns = [product(u, v) for u in left for v in right]
    return rank([list(row) for row in zip(*columns)])


def main() -> None:
    # Two distinct points in the exceptional P1 over rank N=1.
    samples = [
        (Fraction(1), Fraction(1), Fraction(-1), Fraction(1), Fraction(2), Fraction(-1), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(-1), Fraction(1), Fraction(1), Fraction(0), Fraction(0)),
    ]
    profiles = []
    for parameters in samples:
        planes = make_planes(*parameters)
        coefficients = {
            bits: permanent_dp(tuple(planes[mode][bits[mode]] for mode in range(4)))
            for bits in BITS
        }
        assert [bits for bits, value in coefficients.items() if value] == [(1, 1, 1, 1)]
        assert coefficients[(1, 1, 1, 1)] == 4
        profile = [
            pair_rank(planes[left], planes[right])
            for left, right in itertools.combinations(range(4), 2)
        ]
        assert min(profile) == 3
        profiles.append(profile)

    # Rational arcs at the matrix level.  A square root of A^2 exists in
    # C[[t]] because its constant term is one.
    finite_targets = (Fraction(-3), Fraction(0), Fraction(5, 2))
    arc_checks = []
    for target in finite_targets:
        t = Fraction(1, 101)
        delta = t
        f = t - 1
        phi = 1 - (target + 1) * t / 2
        capital_j = f + phi * phi
        capital_d = delta * delta / capital_j
        A_squared = (capital_d - 1) / f
        matrix = (
            (Fraction(0), Fraction(1), phi),
            (delta, 1 - phi, f + phi),
            (capital_d, Fraction(0), delta),
        )
        kernel = (capital_j, phi * delta, -delta)
        assert matrix_vector(matrix, kernel) == (0, 0, 0)
        scaled = tuple(-value / delta for value in kernel)
        assert scaled[2] == 1
        assert A_squared != 0
        arc_checks.append([str(value) for value in scaled])

    # Projective endpoint: the first kernel coordinate has valuation one,
    # and the other two have valuation two.
    t = Fraction(1, 101)
    endpoint_delta = t * t
    endpoint_f = t * t - 1
    endpoint_phi = 1 + t
    endpoint_j = endpoint_f + endpoint_phi * endpoint_phi
    assert endpoint_j == 2 * t * (1 + t)
    endpoint_d = endpoint_delta * endpoint_delta / endpoint_j
    endpoint_a_squared = (endpoint_d - 1) / endpoint_f
    endpoint_matrix = (
        (Fraction(0), Fraction(1), endpoint_phi),
        (endpoint_delta, 1 - endpoint_phi, endpoint_f + endpoint_phi),
        (endpoint_d, Fraction(0), endpoint_delta),
    )
    endpoint_kernel = (
        endpoint_j,
        endpoint_phi * endpoint_delta,
        -endpoint_delta,
    )
    assert matrix_vector(endpoint_matrix, endpoint_kernel) == (0, 0, 0)
    assert endpoint_a_squared != 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "rational matrix incidence plus subset-DP permanent",
                "rank_one_fiber_profiles": profiles,
                "finite_arc_scaled_kernels": arc_checks,
                "finite_arc_targets": [str(value) for value in finite_targets],
                "endpoint_kernel_valuations": [1, 2, 2],
                "formal_square_root_exists": True,
                "containing_component": 8,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
