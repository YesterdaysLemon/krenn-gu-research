#!/usr/bin/env python3
"""Independent F_7 audit of the directed-triangle H22 obstruction."""

from __future__ import annotations

import itertools
import json


PRIME = 7
SLOPES = tuple(range(PRIME)) + ("inf",)
WORDS = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))


def permanent3(rows, columns=(0, 1, 2)):
    return sum(
        rows[0][columns[permutation[0]]]
        * rows[1][columns[permutation[1]]]
        * rows[2][columns[permutation[2]]]
        for permutation in PERMUTATIONS3
    ) % PRIME


def add(left, right, scalar=1):
    return tuple(
        (a + scalar * b) % PRIME
        for a, b in zip(left, right, strict=True)
    )


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


def transformed(row, direction, slope):
    if direction == "01":
        if slope == "inf":
            return (row[0], row[2], row[3])
        return ((slope * row[0] + row[1]) % PRIME, row[2], row[3])
    if direction == "23":
        if slope == "inf":
            return (row[0], row[1], row[2])
        return (row[0], row[1], (slope * row[2] + row[3]) % PRIME)
    raise ValueError(direction)


def coefficient_row(bits, alpha, beta, direction, slope):
    selected = tuple(
        beta[mode] if bits[mode] else alpha[mode] for mode in range(4)
    )
    projected = tuple(transformed(row, direction, slope) for row in selected)
    result = [0] * 8
    for mode in range(4):
        value = permanent3(
            tuple(projected[other] for other in range(4) if other != mode)
        )
        result[(4 if bits[mode] else 0) + mode] = value
    return tuple(result)


def extension_matrices(alpha, beta, direction, slope):
    rows = {
        bits: coefficient_row(bits, alpha, beta, direction, slope)
        for bits in WORDS
    }
    mixed = tuple(
        rows[bits]
        for bits in WORDS
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


def genuine_data(alpha, beta, direction, slope):
    mixed, diagonal_a, diagonal_b = extension_matrices(
        alpha, beta, direction, slope
    )
    kernel = nullspace(mixed)
    a_nonzero = any(dot(diagonal_a, vector) for vector in kernel)
    b_nonzero = any(dot(diagonal_b, vector) for vector in kernel)
    return a_nonzero and b_nonzero, kernel, diagonal_a, diagonal_b


def marked_map(alpha, beta, direction, slope, extension, marked_mode):
    alpha_d = tuple(
        transformed(alpha[mode], direction, slope) + (extension[mode],)
        for mode in range(4)
    )
    beta_d = tuple(
        transformed(beta[mode], direction, slope) + (extension[4 + mode],)
        for mode in range(4)
    )
    other_modes = tuple(mode for mode in range(4) if mode != marked_mode)
    rows = []
    for bits in BITS3:
        selected = tuple(
            beta_d[mode] if bits[index] else alpha_d[mode]
            for index, mode in enumerate(other_modes)
        )
        rows.append(
            tuple(
                permanent3(
                    selected,
                    tuple(
                        coordinate
                        for coordinate in range(4)
                        if coordinate != marked_coordinate
                    ),
                )
                for marked_coordinate in range(4)
            )
        )
    return rows


def marking_union(kind, direction):
    alpha, canonical_beta = pure_bases(kind)
    result = set()
    counts = {}
    for slope in SLOPES:
        slope_points = set()
        for shifts in itertools.product(range(PRIME), repeat=4):
            beta = shifted(alpha, canonical_beta, shifts)
            genuine, _, _, _ = genuine_data(alpha, beta, direction, slope)
            if genuine:
                slope_points.add(shifts)
        counts[str(slope)] = len(slope_points)
        result.update(slope_points)
    return result, counts


def path_extension_census():
    alpha, canonical_beta = pure_bases("path")
    genuine_markings = 0
    genuine_extensions = 0
    maximum_kernel_dimension = 0
    for direction in ("01", "23"):
        for slope in SLOPES:
            for h in range(PRIME):
                beta = shifted(alpha, canonical_beta, (h, 0, 0, 0))
                genuine, kernel, diagonal_a, diagonal_b = genuine_data(
                    alpha, beta, direction, slope
                )
                if not genuine:
                    continue
                genuine_markings += 1
                maximum_kernel_dimension = max(maximum_kernel_dimension, len(kernel))
                for projective in projective_vectors(len(kernel)):
                    extension = linear_combination(projective, kernel)
                    if not dot(diagonal_a, extension) or not dot(diagonal_b, extension):
                        continue
                    genuine_extensions += 1
                    ranks = tuple(
                        rank(
                            marked_map(
                                alpha,
                                beta,
                                direction,
                                slope,
                                extension,
                                marked_mode,
                            )
                        )
                        for marked_mode in range(4)
                    )
                    assert max(ranks) == 4
    return {
        "genuine_markings": genuine_markings,
        "genuine_projective_extensions": genuine_extensions,
        "maximum_kernel_dimension": maximum_kernel_dimension,
        "every_genuine_extension_has_a_rank_four_marked_map": True,
    }


def main():
    unions = {}
    counts = {}
    for kind in ("star", "path"):
        for direction in ("01", "23"):
            union, slope_counts = marking_union(kind, direction)
            unions[(kind, direction)] = union
            counts[f"{kind}_{direction}"] = slope_counts

    star_intersection = unions[("star", "01")] & unions[("star", "23")]
    path_intersection = unions[("path", "01")] & unions[("path", "23")]
    expected_path_line = {(h, 0, 0, 0) for h in range(PRIME)}
    assert not star_intersection
    assert path_intersection == expected_path_line

    extension_census = path_extension_census()
    print(
        json.dumps(
            {
                "status": "verified",
                "field": "F_7",
                "component_parameters": {"u": 2, "v": 3},
                "projective_slopes": [str(slope) for slope in SLOPES],
                "slope_marking_counts": counts,
                "star_common_markings": 0,
                "path_common_markings": len(path_intersection),
                "path_common_marking_set": sorted(path_intersection),
                "path_extension_census": extension_census,
                "role": "independent corroboration, not the characteristic-zero proof",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
