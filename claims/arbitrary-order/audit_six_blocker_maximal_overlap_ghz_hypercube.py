#!/usr/bin/env python3
"""Independent no-import audit of the maximal-overlap GHZ hypercube."""

from __future__ import annotations

import itertools
import json
import math
from fractions import Fraction
from functools import lru_cache


def deterministic_weight(left: int, right: int, salt: int) -> Fraction:
    first, second = sorted((left, right))
    return Fraction((first + 2) * (second + 3) + 2 * salt + 1, salt + 2)


def hafnian(
    vertices: tuple[int, ...],
    weights: tuple[tuple[Fraction, ...], ...],
) -> Fraction:
    @lru_cache(None)
    def recurse(active: tuple[int, ...]) -> Fraction:
        if not active:
            return Fraction(1)
        first = active[0]
        total = Fraction(0)
        for index in range(1, len(active)):
            second = active[index]
            remaining = active[1:index] + active[index + 1 :]
            total += weights[first][second] * recurse(remaining)
        return total

    return recurse(vertices)


def weighted_case(q_size: int, salt: int) -> dict[str, str | int]:
    roots = tuple(range(4))
    blockers = tuple(range(4, 10))
    residual = tuple(range(10, 12 + q_size))
    size = 12 + q_size
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for left in range(size):
        for right in range(left + 1, size):
            root_forbidden = (left in roots or right in roots) and not (
                (left in roots and right in blockers)
                or (right in roots and left in blockers)
            )
            value = (
                Fraction(0)
                if root_forbidden
                else deterministic_weight(left, right, salt)
            )
            matrix[left][right] = matrix[right][left] = value
    weights = tuple(tuple(row) for row in matrix)
    full = hafnian(tuple(range(size)), weights)

    cofactor = Fraction(0)
    for unused in itertools.combinations(blockers, 2):
        used = tuple(blocker for blocker in blockers if blocker not in unused)
        root_permanent = Fraction(0)
        for assignment in itertools.permutations(used):
            term = Fraction(1)
            for root, blocker in zip(roots, assignment):
                term *= weights[root][blocker]
            root_permanent += term
        cofactor += root_permanent * hafnian((*residual, *unused), weights)
    assert full == cofactor

    # At the all-zero endpoint, residual[0]=a is the fifth root and all of
    # its edges to the other residual vertices vanish.
    endpoint_matrix = [list(row) for row in weights]
    root_a = residual[0]
    port_residual = residual[1:]
    for vertex in port_residual:
        endpoint_matrix[root_a][vertex] = Fraction(0)
        endpoint_matrix[vertex][root_a] = Fraction(0)
    endpoint_weights = tuple(tuple(row) for row in endpoint_matrix)
    endpoint_full = hafnian(tuple(range(size)), endpoint_weights)
    endpoint_p6 = Fraction(0)
    five_roots = (*roots, root_a)
    for assignment in itertools.permutations(blockers):
        term = Fraction(1)
        for root, blocker in zip(five_roots, assignment):
            term *= endpoint_weights[root][blocker]
        leftover = assignment[-1]
        endpoint_p6 += term * hafnian((leftover, *port_residual), endpoint_weights)
    assert endpoint_full == endpoint_p6

    return {
        "q_size": q_size,
        "full_value": str(full),
        "cofactor_value": str(cofactor),
        "endpoint_value": str(endpoint_full),
    }


def coefficient_cube(residual_vertices: int) -> dict[str, int]:
    common = (
        vector
        for vector in (
            (Fraction(2), Fraction(5), Fraction(7)),
            (Fraction(11), Fraction(13), Fraction(17)),
            (Fraction(19), Fraction(23), Fraction(29)),
            (Fraction(31), Fraction(37), Fraction(41)),
        )
    )
    common_vectors = tuple(common)
    choices = tuple(
        (
            tuple(Fraction(43 + 10 * index + colour) for colour in range(3)),
            tuple(Fraction(53 + 10 * index + 2 * colour) for colour in range(3)),
        )
        for index in range(residual_vertices)
    )
    values = {}
    for colour in range(3):
        base = math.prod(vector[colour] for vector in common_vectors)
        for bits in itertools.product((0, 1), repeat=residual_vertices):
            values[colour, bits] = Fraction(base) * math.prod(
                choices[index][bit][colour] for index, bit in enumerate(bits)
            )

    minors = 0
    for colour in range(3):
        for left, right in itertools.combinations(range(residual_vertices), 2):
            free = [
                index
                for index in range(residual_vertices)
                if index not in (left, right)
            ]
            for assignment in itertools.product((0, 1), repeat=len(free)):
                corners = []
                for bit_left, bit_right in ((0, 0), (1, 0), (0, 1), (1, 1)):
                    bits = [0] * residual_vertices
                    bits[left], bits[right] = bit_left, bit_right
                    for index, bit in zip(free, assignment):
                        bits[index] = bit
                    corners.append(values[colour, tuple(bits)])
                assert corners[0] * corners[3] == corners[1] * corners[2]
                minors += 1
    return {
        "residual_vertices": residual_vertices,
        "corners_per_colour": 2**residual_vertices,
        "square_minors_checked": minors,
    }


def main() -> None:
    weighted = tuple(
        weighted_case(q_size, salt) for q_size, salt in ((0, 3), (2, 5), (4, 7))
    )
    cubes = tuple(coefficient_cube(size) for size in (2, 4, 6))
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "no-import weighted hafnian and independent Segre data",
                "field": "rational characteristic zero",
                "weighted_matching_cases": weighted,
                "coefficient_cubes": cubes,
                "arbitrary_order_claim_from_written_proof": True,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
