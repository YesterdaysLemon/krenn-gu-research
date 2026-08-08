#!/usr/bin/env python3
"""Independent small-field audit for the generic H31 directed triangles."""

from __future__ import annotations

import itertools
import json


PRIME = 7
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


def add(left, right, scalar=1):
    return tuple((a + scalar * b) % PRIME for a, b in zip(left, right, strict=True))


def pure_bases(kind):
    u, v = 2, 3
    if kind == "star":
        planes = (
            ((1 - u, 1, 0, u), (1 - v, 0, 1, v)),
            ((0, 1, 1, 0), (0, 0, 1, 1)),
            ((1, 0, -1, 0), (0, 1, -1, 0)),
            ((0, 0, 1, -1), (1, 0, 1, 0)),
        )
        alpha = tuple(plane[0] for plane in planes)
        beta = tuple(plane[1] for plane in planes)
    elif kind == "path":
        planes = (
            ((-1 - u, 1, 0, u), (1 - v, 0, 1, v)),
            ((1, 1, 0, 0), (0, 0, 1, 1)),
            ((1, 0, -1, 0), (1, -1, 0, 0)),
            ((0, 0, 1, -1), (1, 0, 1, 0)),
        )
        alpha = (add(planes[0][0], planes[0][1]),) + tuple(
            plane[0] for plane in planes[1:]
        )
        beta = (planes[0][1],) + tuple(plane[1] for plane in planes[1:])
    else:
        raise ValueError(kind)
    return (
        tuple(tuple(entry % PRIME for entry in row) for row in alpha),
        tuple(tuple(entry % PRIME for entry in row) for row in beta),
    )


def shifted(alpha, beta, shifts):
    return tuple(
        add(beta[mode], alpha[mode], shifts[mode]) for mode in range(4)
    )


def coefficient_row(bits, distinguished, alpha, beta):
    common = tuple(index for index in range(4) if index != distinguished)
    selected = tuple(beta[mode] if bits[mode] else alpha[mode] for mode in range(4))
    result = [0] * 8
    for mode in range(4):
        rows = tuple(
            tuple(selected[other][coordinate] for coordinate in common)
            for other in range(4)
            if other != mode
        )
        value = permanent3(rows)
        result[(4 if bits[mode] else 0) + mode] = value
    return result


def extension_matrices(distinguished, alpha, beta):
    rows = {
        bits: coefficient_row(bits, distinguished, alpha, beta)
        for bits in BITS4
    }
    mixed = [
        rows[bits]
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
    return mixed, rows[(0, 0, 0, 0)], rows[(1, 1, 1, 1)]


def rref(matrix):
    work = [[entry % PRIME for entry in row] for row in matrix]
    pivots = []
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (candidate for candidate in range(row, len(work)) if work[candidate][column]),
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
    free = tuple(column for column in range(len(matrix[0])) if column not in pivots)
    result = []
    for free_column in free:
        vector = [0] * len(matrix[0])
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
        sum(coefficients[index] * basis[index][column] for index in range(len(basis)))
        % PRIME
        for column in range(len(basis[0]))
    )


def one_marked_map(distinguished, extension, alpha, beta, marked_mode):
    common = tuple(index for index in range(4) if index != distinguished)
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common) + (extension[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common) + (extension[4 + mode],)
        for mode in range(4)
    )
    rows = []
    for bits in BITS3:
        selected = []
        bit_index = 0
        for mode in range(4):
            if mode == marked_mode:
                selected.append(None)
            else:
                selected.append(beta_p[mode] if bits[bit_index] else alpha_p[mode])
                bit_index += 1
        coefficient_row = []
        for missing_coordinate in range(4):
            coordinates = tuple(index for index in range(4) if index != missing_coordinate)
            coefficient_row.append(
                permanent3(
                    tuple(
                        tuple(selected[mode][coordinate] for coordinate in coordinates)
                        for mode in range(4)
                        if mode != marked_mode
                    )
                )
            )
        rows.append(coefficient_row)
    return rows


def expected_marking(kind, distinguished, t):
    t0, t1, t2, t3 = t
    u, v = 2, 3
    if (kind, distinguished) == ("star", 0):
        equations = (t3, u * t1 - v * t2 - v, t0, (t2 + 1) * (v * t2 + u + v))
    elif (kind, distinguished) == ("star", 1):
        equations = (t2, (u - v) * t1 + (1 - u) * t3 + u - v, u * t0 + v, t3 * (t3 + 1))
    elif (kind, distinguished) == ("star", 2):
        equations = (t3, t2, t1)
    elif (kind, distinguished) == ("star", 3):
        equations = (t2 + (v - 1) * (t3 + 1), t1, (u - 1) * t0 + v - 1, (t3 + 1) * ((v - 1) * t3 + v - 2))
    elif (kind, distinguished) == ("path", 0):
        equations = (t3, t2, t1)
    elif (kind, distinguished) == ("path", 1):
        return False
    elif (kind, distinguished) == ("path", 2):
        equations = (t3, t1, t0 * t2)
    elif (kind, distinguished) == ("path", 3):
        equations = ((u + v) * t3 + u + v - 1, t2, t1, (u + v - 1) * t0 + v - 1)
    else:
        raise ValueError((kind, distinguished))
    return all(equation % PRIME == 0 for equation in equations)


def main():
    marking_counts = {}
    genuine_direction_count = 0
    for kind in ("star", "path"):
        alpha, beta = pure_bases(kind)
        for distinguished in range(4):
            observed = []
            for shifts in itertools.product(range(PRIME), repeat=4):
                marked_beta = shifted(alpha, beta, shifts)
                mixed, diagonal_a, diagonal_b = extension_matrices(
                    distinguished, alpha, marked_beta
                )
                kernel = nullspace(mixed)
                a_nonzero = any(dot(diagonal_a, vector) for vector in kernel)
                b_nonzero = any(dot(diagonal_b, vector) for vector in kernel)
                genuine_marking = a_nonzero and b_nonzero
                assert genuine_marking == expected_marking(kind, distinguished, shifts)
                if not genuine_marking:
                    continue
                observed.append(shifts)
                for projective in projective_vectors(len(kernel)):
                    extension = linear_combination(projective, kernel)
                    if not dot(diagonal_a, extension) or not dot(diagonal_b, extension):
                        continue
                    genuine_direction_count += 1
                    assert any(
                        rank(
                            one_marked_map(
                                distinguished,
                                extension,
                                alpha,
                                marked_beta,
                                mode,
                            )
                        )
                        == 4
                        for mode in range(4)
                    )
            marking_counts[f"{kind}_q{distinguished}"] = len(observed)

    assert marking_counts == {
        "star_q0": 2,
        "star_q1": 2,
        "star_q2": 7,
        "star_q3": 2,
        "path_q0": 7,
        "path_q1": 0,
        "path_q2": 13,
        "path_q3": 1,
    }
    assert genuine_direction_count > 0
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP finite-field marking and extension census",
                "prime": PRIME,
                "component_point": {"u": 2, "v": 3},
                "marking_counts": marking_counts,
                "genuine_projective_extensions_checked": genuine_direction_count,
                "all_have_a_rank_four_marked_mode": True,
                "role": "corroboration of the characteristic-zero symbolic proof",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
