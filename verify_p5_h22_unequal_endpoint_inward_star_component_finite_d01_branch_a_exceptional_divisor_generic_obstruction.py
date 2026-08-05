#!/usr/bin/env python3
"""Verify the generic obstruction on the finite-D01 A exceptional divisor."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    project,
)
from verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction import (
    pure_basis,
)

PERMUTATIONS = tuple(itertools.permutations(range(4)))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def permanent(rows):
    return sum(
        sp.prod(rows[index][permutation[index]] for index in range(4))
        for permutation in PERMUTATIONS
    )


def add(*rows):
    return tuple(sum(row[index] for row in rows) for index in range(4))


def scale(coefficient, row):
    return tuple(coefficient * value for value in row)


def quotient_normal_numerator(expression, k, k_squared, parameters):
    numerator = sp.fraction(sp.together(expression))[0]
    domain = sp.QQ.frac_field(*parameters)
    polynomial = sp.Poly(sp.expand(numerator), k, domain=domain)
    modulus = sp.Poly(k**2 - k_squared, k, domain=domain)
    return sp.factor(polynomial.rem(modulus).as_expr())


def one_marked_rows(mode, row_indices, alpha, beta):
    result = []
    for row_index in row_indices:
        bits = BITS3[row_index]
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        result.append(coefficient_row)
    return sp.Matrix(result)


def main():
    started = time.perf_counter()
    e, j, k, s = sp.symbols("e j k s")
    cross = e + j
    leading = 1 + e * j * s**2

    # Work directly in the quadratic component field.  These are exactly the
    # reductions of P=ej+k^2 and e^2-k^2 modulo F=P*R-Q^2.
    k_squared = cross**2 / leading - e * j
    pivot = cross**2 / leading
    e2_minus_k2 = j * cross * (e**2 * s**2 - 1) / leading

    slope = (j * s + 1) / (j * s - 1)
    w = -((j * s - 1) ** 2) * leading / (16 * s * (e - j) * cross**2 * k)
    z3 = -(j * s - 1) / (4 * e2_minus_k2 * pivot)
    z6 = -j * (j * s - 1) * leading / (8 * k * cross**2 * (e - j))
    z5 = sp.together(z6 - k * z3)
    z1 = sp.together(
        cross * z6 - pivot * s * (slope - 1) * w - j * (k_squared - e**2) * z3 / k
    )
    z7 = sp.together(
        (pivot * z6 - k_squared * cross * (slope - 1) * s * w - e * z1)
        / (k_squared - e**2)
    )
    z0 = sp.together(
        (
            pivot**2 * z3
            - k * cross**2 * (slope + 1) * w
            - sp.Rational(1, 2) / (slope - 1)
        )
        / (k * cross)
    )
    extension = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)

    alpha_raw, beta_raw = pure_basis(e, j, k, s)
    alpha = tuple(
        tuple(sp.together(sp.sympify(value).subs(k**2, k_squared)) for value in row)
        for row in alpha_raw
    )
    beta = tuple(
        tuple(sp.together(sp.sympify(value).subs(k**2, k_squared)) for value in row)
        for row in beta_raw
    )
    alpha_01 = tuple(
        project(alpha[index], extension[index], "D01", "finite", slope)
        for index in range(4)
    )
    beta_01 = tuple(
        project(beta[index], extension[4 + index], "D01", "finite", slope)
        for index in range(4)
    )

    assert (
        quotient_normal_numerator(permanent(alpha_01) - 1, k, k_squared, (e, j, s)) == 0
    )
    singleton_coefficients = []
    for mode in range(4):
        rows = list(alpha_01)
        rows[mode] = beta_01[mode]
        singleton_coefficients.append(permanent(tuple(rows)))
    expected_marking = (
        0,
        -e / e2_minus_k2,
        -j * s,
        -j * (2 * e**2 * j**2 * s**2 - e**2 - j**2) / (k * (e - j) * leading),
    )
    for singleton, marking in zip(singleton_coefficients, expected_marking):
        assert (
            quotient_normal_numerator(singleton + marking, k, k_squared, (e, j, s)) == 0
        )

    alpha_23 = tuple(
        project(alpha[index], extension[index], "D23", "finite", slope)
        for index in range(4)
    )
    beta_23 = tuple(
        project(beta[index], extension[4 + index], "D23", "finite", slope)
        for index in range(4)
    )
    beta_23_marked = tuple(
        add(beta_23[index], scale(expected_marking[index], alpha_23[index]))
        for index in range(4)
    )
    matrix = one_marked_rows(1, (0, 4, 5, 6), alpha_23, beta_23_marked)
    determinant = sp.expand(matrix.det(method="domain-ge"))
    expected_determinant = (
        (j * k * s - e)
        * (j * s - 1)
        * (j * s + 1)
        * leading**2
        / (4 * k**3 * s**2 * (e - j) ** 2 * cross**4 * e2_minus_k2)
    )
    assert (
        quotient_normal_numerator(
            determinant - expected_determinant, k, k_squared, (e, j, s)
        )
        == 0
    )
    point = {e: -5, j: 2, k: 3, s: -1}
    assert sp.cancel(determinant.subs(point)) == sp.Rational(-1, 28224)

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_generic_exceptional_divisor_obstruction",
                "field": "C(e,j,s)[k]/(F)",
                "component": 25,
                "pair_orbit": "finite D01 A exceptional divisor",
                "normalization_C0000": "1",
                "forced_marking": [
                    "0",
                    "-e/(e^2-k^2)",
                    "-js",
                    "-j*(2e^2j^2s^2-e^2-j^2)/(k*(e-j)*R)",
                ],
                "uniform_D01_diagonal_checked_by": "independent no-import audit",
                "paired_D23_minor": {
                    "mode": 1,
                    "rows": [0, 4, 5, 6],
                    "reduced_numerator": "(jks-e)*(js-1)*(js+1)*R^2",
                    "denominator": "4*k^3*s^2*(e-j)^2*Q^4*(e^2-k^2)",
                    "internal_zero_divisors_after_chart_units": ["js+1", "jks-e"],
                },
                "rational_witness_minor": "-1/28224",
                "B_branch_tested": False,
                "special_component_divisors_tested": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
