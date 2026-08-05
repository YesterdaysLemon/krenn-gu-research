#!/usr/bin/env python3
"""Verify the full-support tangent-pair P4 component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pair_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def main() -> None:
    a, b, c, d, t = sp.symbols("a b c d t")
    f1 = a * d + b * c
    f2 = b + d
    f3 = a + c
    l1 = 2 * b**2 * (a - c)
    l2 = 2 * a**2 * (b - d)
    energy = 2 * (a * b + b * c + a * d)

    planes = (
        ((1, 0, 0, 0), (0, 1, a, b)),
        ((1, 0, 0, 0), (0, 1, a, b)),
        ((1, 0, 0, 0), (0, 1, c, d)),
        ((t * l1, f2, -f1, 0), (t * l2, f3, 0, -f1)),
    )
    coefficients = {
        bits: permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    expected = {
        (1, 1, 0, 0): l1,
        (1, 1, 0, 1): l2,
        (1, 1, 1, 0): t * energy * l1,
        (1, 1, 1, 1): t * energy * l2,
    }
    for bits, value in coefficients.items():
        assert sp.factor(value - expected.get(bits, 0)) == 0

    # Row-reduced last-plane chart.
    last = sp.Matrix(planes[3])
    reduced_last = sp.simplify(last[:, [0, 1]].inv() * last)
    expected_last = sp.Matrix(
        [
            [1, 0, -(a + c) / (2 * t * (a * d - b * c)), (b + d) / (2 * t * (a * d - b * c))],
            [0, 1, a**2 * (b - d) / (a * d - b * c), b**2 * (c - a) / (a * d - b * c)],
        ]
    )
    assert sp.simplify(reduced_last - expected_last) == sp.zeros(2, 4)

    parameters = (a, b, c, d, t)
    chart_coordinates = sp.Matrix(
        [
            0, 0, a, b,
            0, 0, a, b,
            0, 0, c, d,
            reduced_last[0, 2], reduced_last[0, 3],
            reduced_last[1, 2], reduced_last[1, 3],
        ]
    )
    sample_parameters = {a: 1, b: 1, c: 2, d: 3, t: 1}
    family_jacobian = chart_coordinates.jacobian(parameters).subs(sample_parameters)
    family_rows = [2, 3, 10, 11, 12]
    family_minor = family_jacobian.extract(family_rows, range(5)).det()
    assert family_minor == sp.Rational(3, 2)

    # Universal pivot-01 Segre incidence.
    x = sp.symbols("x0:16")
    z = sp.symbols("z0:4")
    universal_planes = []
    for mode in range(4):
        x0, x1, x2, x3 = x[4 * mode : 4 * mode + 4]
        universal_planes.append(((1, 0, x0, x1), (0, 1, x2, x3)))
    universal_coefficients = {
        bits: permanent(tuple(universal_planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    anchor = (1, 1, 0, 0)
    equations = sp.Matrix(
        [
            universal_coefficients[bits]
            - universal_coefficients[anchor]
            * sp.prod(z[i] for i in range(4) if bits[i] != anchor[i])
            for bits in BITS
            if bits != anchor
        ]
    )
    variables = list(x + z)
    sample = [
        0, 0, 1, 1,
        0, 0, 1, 1,
        0, 0, 2, 3,
        sp.Rational(-3, 2), 2, -2, 1,
        0, 0, 12, 0,
    ]
    substitution = dict(zip(variables, sample))
    assert equations.subs(substitution) == sp.zeros(15, 1)
    incidence_jacobian = equations.jacobian(variables).subs(substitution)
    incidence_rows = list(range(2, 15))
    incidence_columns = list(range(12)) + [19]
    incidence_minor = incidence_jacobian.extract(incidence_rows, incidence_columns).det()
    assert incidence_minor == -34560
    assert incidence_jacobian.rank() == 13

    right_kernel = sp.Matrix.hstack(*incidence_jacobian.nullspace())
    left_kernel = sp.Matrix.hstack(*incidence_jacobian.T.nullspace())
    assert right_kernel.shape == (20, 7)
    assert left_kernel.shape == (15, 2)
    tau = sp.symbols("tau0:7")
    direction = right_kernel * sp.Matrix(tau)
    quadrics = []
    for cokernel_index in range(2):
        quadric = 0
        for equation, weight in zip(equations, left_kernel[:, cokernel_index]):
            if weight:
                hessian = sp.hessian(equation, variables).subs(substitution)
                quadric += weight * (direction.T * hessian * direction)[0] / 2
        quadrics.append(sp.factor(quadric))
    assert quadrics == [
        -tau[4] * tau[5],
        -(tau[4] - tau[5]) ** 2,
    ]
    assert sp.gcd(quadrics[0], quadrics[1]) == 1

    rational_planes = tuple(
        tuple(tuple(sp.sympify(entry).subs(sample_parameters) for entry in row) for row in plane)
        for plane in planes
    )
    pair_profile = [
        pair_matrix(rational_planes[i], rational_planes[j]).rank()
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert pair_profile == [2, 3, 4, 3, 4, 4]
    tangent_kernel = pair_matrix(rational_planes[0], rational_planes[1]).nullspace()
    assert [sp.Matrix(2, 2, vector).rank() for vector in tangent_kernel] == [1, 2]

    print(
        json.dumps(
            {
                "status": "pass",
                "family_tangent_minor": str(family_minor),
                "incidence_rank": int(incidence_jacobian.rank()),
                "incidence_minor": int(incidence_minor),
                "quadratic_initial_forms": [str(value) for value in quadrics],
                "quadratic_gcd": str(sp.gcd(quadrics[0], quadrics[1])),
                "local_dimension": 5,
                "pair_profile": [int(value) for value in pair_profile],
                "component_number": 14,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
