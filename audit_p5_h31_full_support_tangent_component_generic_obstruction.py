#!/usr/bin/env python3
"""Independent F_11 audit of the component-fourteen H31 obstruction."""

from __future__ import annotations

import itertools
import json


PRIME = 11
PARAMETERS = (2, 4)
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def permanent3(rows):
    return sum(
        rows[0][permutation[0]]
        * rows[1][permutation[1]]
        * rows[2][permutation[2]]
        for permutation in PERMUTATIONS3
    ) % PRIME


def normalized_bases():
    p, q = PARAMETERS
    e = (1, 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, p, q)
    s1 = (1 - p, 1 + q, -p - q, 0)
    s2 = (1 - q, 1 + p, 0, -p - q)
    cap_s = p + q + 1
    alpha = (
        e,
        e,
        tuple(cap_s * e[index] - u[index] for index in range(4)),
        tuple(
            (q - 1) * s1[index] - (p - 1) * s2[index]
            for index in range(4)
        ),
    )
    beta = (w, w, e, s1)
    return (
        tuple(tuple(entry % PRIME for entry in row) for row in alpha),
        tuple(tuple(entry % PRIME for entry in row) for row in beta),
    )


def shifted(alpha, beta, shifts):
    return tuple(
        tuple(
            (beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            % PRIME
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def coefficient_row(bits, distinguished, alpha, beta):
    common = tuple(index for index in range(4) if index != distinguished)
    selected = tuple(
        beta[mode] if bits[mode] else alpha[mode] for mode in range(4)
    )
    result = [0] * 8
    for mode in range(4):
        rows = tuple(
            tuple(selected[other][coordinate] for coordinate in common)
            for other in range(4)
            if other != mode
        )
        result[(4 if bits[mode] else 0) + mode] = permanent3(rows)
    return tuple(result)


def extension_matrices(distinguished, alpha, beta):
    rows = {
        bits: coefficient_row(bits, distinguished, alpha, beta)
        for bits in BITS4
    }
    mixed = tuple(
        rows[bits]
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )
    return mixed, rows[(0, 0, 0, 0)], rows[(1, 1, 1, 1)]


def rref(matrix):
    work = [[entry % PRIME for entry in row] for row in matrix]
    pivots = []
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                candidate
                for candidate in range(row, len(work))
                if work[candidate][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], -1, PRIME)
        work[row] = [(entry * inverse) % PRIME for entry in work[row]]
        for other in range(len(work)):
            if other == row or not work[other][column]:
                continue
            factor = work[other][column]
            work[other] = [
                (left - factor * right) % PRIME
                for left, right in zip(work[other], work[row], strict=True)
            ]
        pivots.append(column)
        row += 1
        if row == len(work):
            break
    return work, tuple(pivots)


def rank(matrix):
    return len(rref(matrix)[1])


def nullspace(matrix):
    reduced, pivots = rref(matrix)
    free = tuple(column for column in range(8) if column not in pivots)
    result = []
    for free_column in free:
        vector = [0] * 8
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free_column]) % PRIME
        result.append(tuple(vector))
    return tuple(result)


def dot(left, right):
    return sum(a * b for a, b in zip(left, right, strict=True)) % PRIME


def projective_vectors(dimension):
    for pivot in range(dimension):
        for tail in itertools.product(range(PRIME), repeat=dimension - pivot - 1):
            yield (0,) * pivot + (1,) + tail


def linear_combination(coefficients, basis):
    return tuple(
        sum(
            coefficients[index] * basis[index][column]
            for index in range(len(basis))
        )
        % PRIME
        for column in range(8)
    )


def marked_map(distinguished, extension, alpha, beta, marked_mode):
    common = tuple(index for index in range(4) if index != distinguished)
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (extension[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode in range(4)
    )
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    rows = []
    for bits in BITS3:
        selected = tuple(
            beta_p[mode] if bits[index] else alpha_p[mode]
            for index, mode in enumerate(other_modes)
        )
        rows.append(
            tuple(
                permanent3(
                    tuple(
                        tuple(row[coordinate] for coordinate in range(4) if coordinate != missing)
                        for row in selected
                    )
                )
                for missing in range(4)
            )
        )
    return rows


def quotient(value):
    return value % PRIME


def expected_sheets():
    p, q = PARAMETERS
    cap_s = quotient(p + q + 1)
    data = {
        1: (
            cap_s * pow(quotient(p + q), -1, PRIME) % PRIME,
            q
            * pow(quotient((p - q) * (p + q - 1)), -1, PRIME)
            % PRIME,
        ),
        2: (
            cap_s * pow(quotient(q + 1), -1, PRIME) % PRIME,
            q
            * (q + 1)
            * pow(
                quotient((p + q) * (q - 1) * (p - q - 1)),
                -1,
                PRIME,
            )
            % PRIME,
        ),
        3: (
            cap_s * pow(quotient(p + 1), -1, PRIME) % PRIME,
            q
            * pow(quotient((p + q) * (p - q + 1)), -1, PRIME)
            % PRIME,
        ),
    }
    return {
        distinguished: {
            (shift, 0, 0, t3),
            (0, shift, 0, t3),
        }
        for distinguished, (shift, t3) in data.items()
    }


def main():
    alpha, canonical_beta = normalized_bases()
    expected = expected_sheets()
    observed = {}
    extension_count = 0
    for distinguished in range(4):
        observed[distinguished] = set()
        for shifts in itertools.product(range(PRIME), repeat=4):
            beta = shifted(alpha, canonical_beta, shifts)
            mixed, diagonal_a, diagonal_b = extension_matrices(
                distinguished, alpha, beta
            )
            kernel = nullspace(mixed)
            genuine = (
                any(dot(diagonal_a, vector) for vector in kernel)
                and any(dot(diagonal_b, vector) for vector in kernel)
            )
            if genuine:
                observed[distinguished].add(shifts)
        assert observed[distinguished] == expected.get(distinguished, set())

    for distinguished, sheets in expected.items():
        for shifts in sheets:
            beta = shifted(alpha, canonical_beta, shifts)
            mixed, diagonal_a, diagonal_b = extension_matrices(
                distinguished, alpha, beta
            )
            kernel = nullspace(mixed)
            assert len(kernel) == 2
            for projective in projective_vectors(2):
                extension = linear_combination(projective, kernel)
                if not dot(diagonal_a, extension) or not dot(diagonal_b, extension):
                    continue
                extension_count += 1
                ranks = tuple(
                    rank(
                        marked_map(
                            distinguished,
                            extension,
                            alpha,
                            beta,
                            marked_mode,
                        )
                    )
                    for marked_mode in range(4)
                )
                assert max(ranks) == 4

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "F_11",
                "component_parameters": {"p": 2, "q": 4},
                "marking_counts": {
                    str(distinguished): len(sheets)
                    for distinguished, sheets in observed.items()
                },
                "total_marking_sheets": sum(map(len, observed.values())),
                "genuine_projective_extensions": extension_count,
                "every_extension_has_a_rank_four_marked_map": True,
                "role": "independent corroboration, not the characteristic-zero proof",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
