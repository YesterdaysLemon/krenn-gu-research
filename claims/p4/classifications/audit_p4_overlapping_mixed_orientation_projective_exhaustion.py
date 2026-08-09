#!/usr/bin/env python3
"""Independent finite-field audit of the projective mixed chart."""

from __future__ import annotations

import itertools
import json


PAIRS = tuple(itertools.combinations(range(4), 2))
PRIMES = (101, 103)


def permanent_dp(rows, prime):
    state = {0: 1}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = (
                    following.get(next_mask, 0) + value * entry
                ) % prime
        state = following
    return state[15]


def rank(matrix, prime):
    work = [[entry % prime for entry in row] for row in matrix]
    result = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(result, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        inverse = pow(work[result][column], -1, prime)
        work[result] = [entry * inverse % prime for entry in work[result]]
        for row in range(len(work)):
            if row == result or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[result], strict=True)
            ]
        result += 1
    return result


def nullspace(matrix, prime):
    work = [[entry % prime for entry in row] for row in matrix]
    pivot_columns = []
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [entry * inverse % prime for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % prime
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
    free_columns = [column for column in range(len(work[0])) if column not in pivot_columns]
    result = []
    for free in free_columns:
        vector = [0] * len(work[0])
        vector[free] = 1
        for row, pivot in reversed(tuple(enumerate(pivot_columns))):
            vector[pivot] = -sum(work[row][column] * vector[column] for column in free_columns) % prime
        result.append(vector)
    return result


def determinant(matrix, prime):
    size = len(matrix)
    work = [[entry % prime for entry in row] for row in matrix]
    result = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        value = work[column][column]
        result = result * value % prime
        inverse = pow(value, -1, prime)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % prime
            for offset in range(column, size):
                work[row][offset] = (work[row][offset] - factor * work[column][offset]) % prime
    return result % prime


def leaves(A, H, C, D, P, R, Q):
    return (
        ((0, 0, 1, 1), (A, H, C, D)),
        ((P, R, 0, Q), (-1, 0, 1, 0)),
        ((1, 0, 1, 0), (0, 0, -1, 1)),
    )


def contraction_data(parameters, prime):
    planes = leaves(*parameters)
    identity = tuple(tuple(int(row == column) for column in range(4)) for row in range(4))
    forbidden = []
    active = None
    for bits in itertools.product((0, 1), repeat=3):
        covector = tuple(
            permanent_dp(
                (
                    identity[coordinate],
                    planes[0][bits[0]],
                    planes[1][bits[1]],
                    planes[2][bits[2]],
                ),
                prime,
            )
            for coordinate in range(4)
        )
        if bits == (0, 0, 0):
            active = covector
        elif any(covector):
            forbidden.append(covector)
    return tuple(forbidden), active


def formula_data(parameters, prime):
    A, H, C, D, P, R, Q = parameters
    matrix = (
        (D * R + H * Q, A * Q + C * Q + D * P, D * R + H * Q, A * R + C * R + H * P),
        (C * R - D * R - H * Q, -A * Q + C * P - D * P, A * R + H * P, -A * R - H * P),
        (H, A - C + D, -H, H),
    )
    escape = (R, P + Q, R, R)
    return tuple(tuple(entry % prime for entry in row) for row in matrix), tuple(entry % prime for entry in escape)


def product_vector(left, right):
    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in PAIRS)


def pair_matrix(left, right):
    columns = [product_vector(first, second) for first in left for second in right]
    return [list(row) for row in zip(*columns, strict=True)]


def relation_ranks(planes, prime):
    result = []
    for left, right in ((0, 1), (0, 2), (1, 2)):
        kernel = nullspace(pair_matrix(planes[left], planes[right]), prime)
        assert len(kernel) == 1
        vector = kernel[0]
        result.append(rank((vector[:2], vector[2:]), prime))
    return tuple(result)


def pluecker(plane, prime):
    return tuple(
        (plane[0][i] * plane[1][j] - plane[0][j] * plane[1][i]) % prime
        for i, j in PAIRS
    )


def proportional(left, right, prime):
    return all(
        (left[i] * right[j] - left[j] * right[i]) % prime == 0
        for i, j in itertools.combinations(range(6), 2)
    )


def transform_path_plane(plane):
    permuted = tuple(tuple(row[column] for column in (3, 1, 2, 0)) for row in plane)
    signs = (-1, 1, 1, -1)
    return tuple(tuple(row[column] * signs[column] for column in range(4)) for row in permuted)


def main():
    generic_samples = (
        (2, 3, 5, 7, 11, 13, 17),
        (19, 23, 29, 31, 37, 41, 43),
        (-2, 5, -7, 11, -13, 17, -19),
        (1, -3, 4, -5, 6, -7, 8),
    )
    checked_formula_points = 0
    for prime in PRIMES:
        for sample in generic_samples:
            reconstructed = contraction_data(sample, prime)
            formula = formula_data(sample, prime)
            assert reconstructed == formula
            checked_formula_points += 1

        for sample in ((2, 3, 5, 7, 11, 0, 17), (-2, 5, -7, 11, -13, 0, 19)):
            A, H, C, D, P, R, Q = sample
            matrix, _ = formula_data(sample, prime)
            expected = (
                D * H**2 * (P - Q) * (P + Q),
                -C * H**2 * (P - Q) * (P + Q),
                -H**3 * (P - Q) * (P + Q),
                -A * H**2 * (P - Q) * (P + Q),
            )
            actual = tuple(
                determinant([[matrix[row][column] for column in columns] for row in range(3)], prime)
                for columns in itertools.combinations(range(4), 3)
            )
            assert actual == tuple(entry % prime for entry in expected)

        for sample in ((2, 0, 5, 7, 11, 13, 17), (-2, 0, -7, 11, -13, 19, 23)):
            A, H, C, D, P, R, Q = sample
            matrix, _ = formula_data(sample, prime)
            # Dehomogenize R to one before using the displayed H=0 factors.
            inverse_r = pow(R % prime, -1, prime)
            normalized = (A, 0, C, D, P * inverse_r, 1, Q * inverse_r)
            A0, _, C0, D0, _, _, _ = normalized
            normalized_matrix, _ = formula_data(normalized, prime)
            L = A0 - C0 + D0
            expected = (
                -D0 * L**2,
                C0 * L * (A0 + C0 - D0),
                0,
                -A0 * L * (A0 + C0 + D0),
            )
            actual = tuple(
                determinant(
                    [[normalized_matrix[row][column] for column in columns] for row in range(3)],
                    prime,
                )
                for columns in itertools.combinations(range(4), 3)
            )
            assert actual == tuple(entry % prime for entry in expected)

    for prime in PRIMES:
        t = 7
        lines = {
            "star": (0, 1, t, 0, -t, 1, 0),
            "path_A": (t, 1, 0, 0, -t, 1, 0),
            "path_D": (0, 1, 0, t, 0, 1, -t),
            "first_component": (t, 1, -t, -t, 0, 1, t),
        }
        expected_relation_ranks = {
            "star": (1, 1, 1),
            "path_A": (1, 1, 1),
            "path_D": (1, 1, 1),
            "first_component": (2, 1, 1),
        }
        for name, sample in lines.items():
            matrix, escape = formula_data(sample, prime)
            assert rank(matrix, prime) == 1
            assert rank((*matrix, escape), prime) == 2
            assert relation_ranks(leaves(*sample), prime) == expected_relation_ranks[name]

        path_A = leaves(*lines["path_A"])
        path_D = leaves(*lines["path_D"])
        transformed = tuple(transform_path_plane(plane) for plane in path_A)
        transformed = (transformed[1], transformed[0], transformed[2])
        assert all(
            proportional(pluecker(left, prime), pluecker(right, prime), prime)
            for left, right in zip(transformed, path_D, strict=True)
        )

        # Genuine H=0 branches have lower pair rank.
        for sample in (
            (1, 0, 0, -1, 3, 1, 4),
            (1, 0, -1, 0, 3, 1, 4),
        ):
            planes = leaves(*sample)
            assert rank(pair_matrix(planes[0], planes[2]), prime) == 2

        # At R=0, P=Q is genuine and has a lower pair; P=-Q has no escape.
        genuine_r = (2, 1, 3, 5, 1, 0, 1)
        zero_r = (2, 1, 3, 5, 1, 0, -1)
        assert rank(pair_matrix(leaves(*genuine_r)[1], leaves(*genuine_r)[2]), prime) == 2
        assert formula_data(zero_r, prime)[1] == (0, 0, 0, 0)

        # The projective corner is an embedded P3 suspension.
        corner = (-1, 0, 0, 1, 1, 0, 1)
        corner_matrix, corner_escape = formula_data(corner, prime)
        assert rank(corner_matrix, prime) == 0
        assert any(corner_escape)
        corner_leaves = leaves(*corner)
        assert all(all(row[1] == 0 for row in plane) for plane in corner_leaves)
        u_0 = ((0, 1, 0, 0), (1, 0, 0, 0))
        planes = (u_0, *corner_leaves)
        tensor = {
            word: permanent_dp(tuple(planes[mode][word[mode]] for mode in range(4)), prime)
            for word in itertools.product((0, 1), repeat=4)
        }
        nonzero = tuple(word for word, value in tensor.items() if value)
        assert nonzero == ((0, 0, 0, 0),)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP contractions and finite-field row reduction",
                "primes": PRIMES,
                "generic_formula_points": checked_formula_points,
                "affine_rank_one_lines": 4,
                "path_line_symmetry_replayed": True,
                "projective_boundaries_replayed": True,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
