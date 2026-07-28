#!/usr/bin/env python3
"""Compute the first scalar-invariant search space for five qutrit modes."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter

from sympy import Integer, Matrix, Rational, eye, simplify, sqrt, zeros


SHAPE = (2, 2, 2)
DEGREE = 6
MODES = 5


def partitions(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    if maximum is None or maximum > total:
        maximum = total
    for first in range(maximum, 0, -1):
        for rest in partitions(total - first, first):
            yield (first, *rest)


def standard_tableaux() -> tuple[dict[tuple[int, int], int], ...]:
    cells = tuple(
        (row, column)
        for row, length in enumerate(SHAPE)
        for column in range(length)
    )
    output = []
    for values in itertools.permutations(range(1, DEGREE + 1)):
        tableau = dict(zip(cells, values, strict=True))
        rows_increase = all(
            column + 1 >= SHAPE[row]
            or tableau[row, column] < tableau[row, column + 1]
            for row, column in cells
        )
        columns_increase = all(
            row + 1 >= len(SHAPE)
            or column >= SHAPE[row + 1]
            or tableau[row, column] < tableau[row + 1, column]
            for row, column in cells
        )
        if rows_increase and columns_increase:
            output.append(tableau)
    return tuple(output)


def tableau_key(
    tableau: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    return tuple(
        tableau[row, column]
        for row, length in enumerate(SHAPE)
        for column in range(length)
    )


def adjacent_matrices(
    tableaux: tuple[dict[tuple[int, int], int], ...],
) -> tuple[Matrix, ...]:
    dimension = len(tableaux)
    index = {
        tableau_key(tableau): position
        for position, tableau in enumerate(tableaux)
    }
    output = []
    for adjacent in range(1, DEGREE):
        matrix = zeros(dimension)
        for position, tableau in enumerate(tableaux):
            coordinates = {
                value: cell for cell, value in tableau.items()
            }
            first_row, first_column = coordinates[adjacent]
            second_row, second_column = coordinates[adjacent + 1]
            axial_distance = (
                second_column
                - second_row
                - first_column
                + first_row
            )
            matrix[position, position] = Rational(1, axial_distance)
            if abs(axial_distance) != 1:
                swapped = dict(tableau)
                swapped[coordinates[adjacent]] = adjacent + 1
                swapped[coordinates[adjacent + 1]] = adjacent
                image = index[tableau_key(swapped)]
                matrix[image, position] = sqrt(
                    1 - Rational(1, axial_distance**2)
                )
        output.append(matrix)
    return tuple(output)


def representative_word(cycle_type: tuple[int, ...]) -> list[int]:
    permutation = list(range(DEGREE))
    start = 0
    for length in cycle_type:
        cycle = list(range(start, start + length))
        for left, right in zip(cycle, cycle[1:]):
            permutation[left] = right
        permutation[cycle[-1]] = cycle[0]
        start += length

    word = []
    current = list(permutation)
    for target in range(DEGREE - 1, -1, -1):
        position = current.index(target)
        while position < target:
            current[position], current[position + 1] = (
                current[position + 1],
                current[position],
            )
            word.append(position)
            position += 1
    if current != list(range(DEGREE)):
        raise AssertionError("adjacent word did not sort representative")
    return word


def class_size(cycle_type: tuple[int, ...]) -> int:
    centralizer = 1
    for length, multiplicity in Counter(cycle_type).items():
        centralizer *= (
            length**multiplicity * math.factorial(multiplicity)
        )
    return math.factorial(DEGREE) // centralizer


def character(
    cycle_type: tuple[int, ...],
    adjacent: tuple[Matrix, ...],
) -> int:
    representation = eye(adjacent[0].rows)
    for generator in representative_word(cycle_type):
        representation *= adjacent[generator]
    value = simplify(representation.trace())
    if value.is_Integer is not True:
        raise AssertionError(
            f"nonintegral character at {cycle_type}: {value}"
        )
    return int(value)


def main() -> None:
    tableaux = standard_tableaux()
    if len(tableaux) != 5:
        raise AssertionError("Specht (2,2,2) dimension changed")
    adjacent = adjacent_matrices(tableaux)
    identity = eye(len(tableaux))
    for matrix in adjacent:
        if simplify(matrix * matrix - identity) != zeros(len(tableaux)):
            raise AssertionError("Coxeter involution failed")
    for index in range(len(adjacent) - 1):
        left = (
            adjacent[index]
            * adjacent[index + 1]
            * adjacent[index]
        )
        right = (
            adjacent[index + 1]
            * adjacent[index]
            * adjacent[index + 1]
        )
        if simplify(left - right) != zeros(len(tableaux)):
            raise AssertionError("Coxeter braid relation failed")
    for left in range(len(adjacent)):
        for right in range(left + 2, len(adjacent)):
            if simplify(
                adjacent[left] * adjacent[right]
                - adjacent[right] * adjacent[left]
            ) != zeros(len(tableaux)):
                raise AssertionError("distant generators do not commute")

    rows = []
    for cycle_type in partitions(DEGREE):
        rows.append(
            {
                "cycle_type": cycle_type,
                "class_size": class_size(cycle_type),
                "character": character(cycle_type, adjacent),
            }
        )
    if sum(row["class_size"] for row in rows) != math.factorial(DEGREE):
        raise AssertionError("conjugacy classes do not cover S6")
    if (
        sum(
            row["class_size"] * row["character"] ** 2
            for row in rows
        )
        != math.factorial(DEGREE)
    ):
        raise AssertionError("character orthogonality failed")

    numerator = sum(
        row["class_size"] * row["character"] ** MODES
        for row in rows
    )
    invariant_dimension = numerator // math.factorial(DEGREE)
    if (
        numerator % math.factorial(DEGREE)
        or invariant_dimension != 11
    ):
        raise AssertionError("degree-six invariant dimension changed")

    print(
        json.dumps(
            {
                "verified": True,
                "local_group": "SL(3)^5",
                "tensor_modes": MODES,
                "degree_three_determinant_contraction": (
                    "identically zero for an odd number of modes"
                ),
                "first_natural_scalar_invariant_degree": DEGREE,
                "local_specht_shape": SHAPE,
                "local_specht_dimension": len(tableaux),
                "character_table": rows,
                "degree_six_scalar_invariant_dimension": (
                    invariant_dimension
                ),
                "separator_found": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
