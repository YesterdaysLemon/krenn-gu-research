#!/usr/bin/env python3
"""Independent no-import audit of the order-twelve isotropic P6 curve."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from functools import lru_cache

import sympy as sp


def edge_weight(left: int, right: int) -> Fraction:
    first, second = sorted((left, right))
    return Fraction((first + 2) * (second + 5) + 3, 7)


def hafnian(vertices: tuple[int, ...], weights) -> Fraction:
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


def weighted_partition() -> dict[str, str]:
    common = tuple(range(4))
    a, b = 4, 5
    blockers = tuple(range(6, 12))
    matrix = [[Fraction(0) for _ in range(12)] for _ in range(12)]
    for left in range(12):
        for right in range(left + 1, 12):
            common_forbidden = (left in common or right in common) and not (
                (left in common and right in blockers)
                or (right in common and left in blockers)
            )
            value = Fraction(0) if common_forbidden else edge_weight(left, right)
            matrix[left][right] = matrix[right][left] = value
    weights = tuple(tuple(row) for row in matrix)
    full = hafnian(tuple(range(12)), weights)

    permanent = Fraction(0)
    for assignment in itertools.permutations(blockers):
        term = Fraction(1)
        for root, blocker in zip((*common, a, b), assignment):
            term *= weights[root][blocker]
        permanent += term

    cofactor = Fraction(0)
    for leftover in itertools.combinations(blockers, 2):
        used = tuple(vertex for vertex in blockers if vertex not in leftover)
        root_permanent = Fraction(0)
        for assignment in itertools.permutations(used):
            term = Fraction(1)
            for root, blocker in zip(common, assignment):
                term *= weights[root][blocker]
            root_permanent += term
        cofactor += weights[a][b] * weights[leftover[0]][leftover[1]] * root_permanent
    assert full == permanent + cofactor
    return {
        "full": str(full),
        "permanent": str(permanent),
        "cross_cofactor": str(cofactor),
    }


def independent_symbolic_curve() -> None:
    beta, delta, parameter = sp.symbols("b d s", nonzero=True)
    first = sp.Matrix([1, parameter])
    second = sp.Matrix([delta * parameter, -beta])
    pairing = beta * first[0] * second[0] + delta * first[1] * second[1]
    assert sp.factor(pairing) == 0

    corners = sp.symbols("q00 q01 q10 q11")
    direct = sp.expand(
        first[0] * second[0] * corners[0]
        + first[0] * second[1] * corners[1]
        + first[1] * second[0] * corners[2]
        + first[1] * second[1] * corners[3]
    )
    asserted = (
        -beta * corners[1]
        + parameter * (delta * corners[0] - beta * corners[3])
        + delta * parameter**2 * corners[2]
    )
    assert sp.expand(direct - asserted) == 0

    # A separate exact target frame checks that the full-span branch is
    # nonempty and that the determinant split is substantive.
    x_a = (Fraction(2), Fraction(3), Fraction(5))
    z_a = (Fraction(7), Fraction(11), Fraction(13))
    x_b = (Fraction(17), Fraction(19), Fraction(23))
    z_b = (Fraction(29), Fraction(31), Fraction(37))
    sample_beta, sample_delta = Fraction(3), Fraction(5)

    def product(left, right):
        return tuple(a * b for a, b in zip(left, right))

    v01 = product(x_a, z_b)
    v10 = product(z_a, x_b)
    middle = tuple(
        sample_delta * value_x - sample_beta * value_z
        for value_x, value_z in zip(product(x_a, x_b), product(z_a, z_b))
    )

    def determinant(columns):
        matrix = tuple(zip(*columns))
        return (
            matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        )

    assert determinant((v01, v10, middle)) != 0


def subset_permanent(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    states = {0: Fraction(1)}
    for column in range(6):
        next_states = {}
        for mask, value in states.items():
            for row in range(6):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, Fraction(0)) + (
                    value * matrix[row][column]
                )
        states = next_states
    return states[63]


def local_model_corner() -> dict[str, int]:
    e0, e1, e2 = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (
            Fraction(0),
            Fraction(1),
            Fraction(0),
        ),
        (Fraction(0), Fraction(0), Fraction(1)),
    )

    def linear(*terms):
        return tuple(
            sum(Fraction(scale) * row[index] for scale, row in terms)
            for index in range(3)
        )

    roots = (
        (e1, e2, linear((1, e1), (1, e2)), linear((1, e1), (2, e2))),
        (e0, e2, linear((1, e0), (1, e2)), linear((1, e0), (2, e2))),
        (e0, e1, linear((1, e0), (1, e1)), linear((1, e0), (2, e1))),
        (e0, e1, e2, (Fraction(1), Fraction(1), Fraction(1))),
        (e0, e1, e2, (Fraction(1), Fraction(1), Fraction(1))),
        (e0, e1, e2, (Fraction(1), Fraction(1), Fraction(1))),
    )
    port_a = tuple(
        tuple(map(Fraction, row))
        for row in (
            (0, 1, 2),
            (2, 0, 1),
            (1, 2, 0),
            (1, 1, 2),
            (2, 1, 1),
            (1, 2, 1),
        )
    )
    port_b = tuple(
        tuple(map(Fraction, row))
        for row in (
            (1, 1, 0),
            (0, 1, 1),
            (1, 0, 1),
            (2, 1, 1),
            (1, 3, 1),
            (1, 1, 4),
        )
    )
    word = (0, 0, 0, 0, 0, 1)
    matrix = tuple(
        tuple(
            (*roots[mode], port_a[mode], port_b[mode])[row][word[mode]]
            for mode in range(6)
        )
        for row in range(6)
    )
    coefficient = subset_permanent(matrix)
    assert coefficient == 18

    x, z_a, z_b = (1, 1, 1), (1, 2, 3), (1, 3, 2)
    alpha_a = (2, -1, 0)
    alpha_b = (Fraction(3, 2), Fraction(-1, 2), Fraction(0))
    beta = sum(x[index] * alpha_a[index] for index in range(3)) * sum(
        x[index] * alpha_b[index] for index in range(3)
    )
    delta = sum(z_a[index] * alpha_a[index] for index in range(3)) * sum(
        z_b[index] * alpha_b[index] for index in range(3)
    )
    assert beta == 1 and delta == 0
    return {
        "beta": int(beta),
        "delta": int(delta),
        "off_diagonal_coefficient": int(coefficient),
    }


def main() -> None:
    independent_symbolic_curve()
    partition = weighted_partition()
    local = local_model_corner()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "no-import weighted hafnian and separate corner permanent",
                "field": "rational characteristic zero",
                "weighted_partition": partition,
                "local_model_nonextension": local,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
