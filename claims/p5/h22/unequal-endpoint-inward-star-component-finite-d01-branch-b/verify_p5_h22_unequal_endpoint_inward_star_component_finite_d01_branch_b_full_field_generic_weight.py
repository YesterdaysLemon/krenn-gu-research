#!/usr/bin/env python3
"""Verify the corrected full-quadratic-field generic B obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import time

import sympy as sp


def main():
    started = time.perf_counter()
    base, e, j, s, slope = sp.polys.fields.field("e,j,s,lambda", sp.QQ)
    q = e + j
    r = 1 + e * j * s**2
    p = q**2 / r
    k2 = p - e * j
    zero = (base.zero, base.zero)
    one = (base.one, base.zero)
    k = (base.zero, base.one)

    def lift(value):
        if hasattr(value, "field"):
            return (value, base.zero)
        return (base.from_expr(sp.sympify(value)), base.zero)

    def add(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def negate(value):
        return (-value[0], -value[1])

    def subtract(left, right):
        return add(left, negate(right))

    def multiply(left, right):
        return (
            left[0] * right[0] + k2 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    def scale(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def inverse(value):
        norm = value[0] ** 2 - k2 * value[1] ** 2
        return (value[0] / norm, -value[1] / norm)

    def divide(left, right):
        return multiply(left, inverse(right))

    inverse_k = (base.zero, 1 / k2)

    def row_add(*rows):
        result = []
        for coordinate in range(4):
            value = zero
            for row in rows:
                value = add(value, row[coordinate])
            result.append(value)
        return tuple(result)

    def row_scale(coefficient, row):
        return tuple(scale(coefficient, value) for value in row)

    def row_multiply(value, row):
        return tuple(multiply(value, entry) for entry in row)

    cap_a = tuple(map(lift, (1, 1, 0, 0)))
    cap_b = tuple(map(lift, (0, 0, 1, 1)))
    cap_c = tuple(map(lift, (1, -1, 0, 0)))
    cap_d = tuple(map(lift, (0, 0, 1, -1)))
    alpha = (
        row_add(row_scale(q, cap_a), row_scale(-p, cap_b)),
        row_add(
            row_scale(q, row_add(cap_a, row_multiply(k, cap_d))),
            row_scale(-p, row_add(cap_b, row_scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        row_add(cap_a, row_multiply(k, cap_d)),
        row_add(
            cap_a,
            row_scale(e, cap_b),
            row_scale(-1, row_multiply(k, cap_d)),
        ),
        row_add(cap_a, row_scale(-s * j, cap_c), row_scale(j, cap_b)),
    )

    branch_denominator = (slope - 1) * s * p - (slope + 1) * q
    z3 = s / (2 * p * branch_denominator)
    half = base.from_expr(sp.Rational(1, 2))

    def residuals(w, z6):
        z5 = add(z6, scale(-z3, k))
        z1 = add(
            add(scale(q, z6), scale(-p * s * (slope - 1), w)),
            scale(-j * (k2 - e**2) * z3, inverse_k),
        )
        z7 = scale(
            1 / (k2 - e**2),
            add(
                add(
                    scale(p, z6),
                    scale(-k2 * q * (slope - 1) * s, w),
                ),
                scale(-e, z1),
            ),
        )
        z0 = multiply(
            add(
                lift(p**2 * z3 - half / (slope - 1)),
                scale(-(q**2) * (slope + 1), multiply(k, w)),
            ),
            scale(1 / q, inverse_k),
        )
        extensions = (
            z0,
            z1,
            scale(slope - 1, w),
            lift(z3),
            scale(-(slope + 1), w),
            z5,
            z6,
            z7,
        )

        def project(row, extra):
            return (
                add(scale(slope, row[0]), row[1]),
                row[2],
                row[3],
                extra,
            )

        alpha_rows = tuple(
            project(alpha[index], extensions[index]) for index in range(4)
        )
        beta_rows = tuple(
            project(beta[index], extensions[index + 4]) for index in range(4)
        )

        def permanent(rows):
            total = zero
            for permutation in itertools.permutations(range(4)):
                term = one
                for index in range(4):
                    term = multiply(term, rows[index][permutation[index]])
                total = add(total, term)
            return total

        def coefficient(word):
            return permanent(
                tuple(
                    beta_rows[index] if word[index] else alpha_rows[index]
                    for index in range(4)
                )
            )

        c0 = coefficient((0, 0, 0, 0))
        c1 = coefficient((0, 1, 0, 0))
        c2 = coefficient((0, 0, 1, 0))
        c3 = coefficient((0, 0, 0, 1))
        c13 = coefficient((0, 1, 0, 1))
        c23 = coefficient((0, 0, 1, 1))
        c123 = coefficient((0, 1, 1, 1))
        return (
            subtract(multiply(c13, c0), multiply(c1, c3)),
            subtract(multiply(c23, c0), multiply(c2, c3)),
            subtract(multiply(c123, multiply(c0, c0)), multiply(multiply(c1, c2), c3)),
        )

    at_zero = residuals(zero, zero)
    at_w = residuals(one, zero)
    at_z6 = residuals(zero, one)
    s13_w = subtract(at_w[0], at_zero[0])
    s13_z6 = subtract(at_z6[0], at_zero[0])
    s23_w = subtract(at_w[1], at_zero[1])
    s23_z6 = subtract(at_z6[1], at_zero[1])

    # Check linearity before solving the two Segre equations over the full
    # quadratic field.  No coefficient splitting in the basis 1,k is used.
    probe = residuals(scale(2, one), scale(3, one))
    assert probe[0] == add(at_zero[0], add(scale(2, s13_w), scale(3, s13_z6)))
    assert probe[1] == add(at_zero[1], add(scale(2, s23_w), scale(3, s23_z6)))

    determinant = subtract(multiply(s13_w, s23_z6), multiply(s13_z6, s23_w))
    chart_factor = (slope + 1) * r - (slope - 1) * s * q
    weight_factor = (j * s - 1) * slope - (j * s + 1)
    expected_determinant = (
        -32
        * e
        * j
        * slope
        * s**2
        * q**7
        * (slope - 1)
        * weight_factor
        / (r**3 * chart_factor),
        base.zero,
    )
    assert determinant == expected_determinant

    rhs_13 = negate(at_zero[0])
    rhs_23 = negate(at_zero[1])
    w_solution = divide(
        subtract(multiply(rhs_13, s23_z6), multiply(s13_z6, rhs_23)),
        determinant,
    )
    z6_solution = divide(
        subtract(multiply(s13_w, rhs_23), multiply(rhs_13, s23_w)),
        determinant,
    )
    solved = residuals(w_solution, z6_solution)
    assert solved[0] == zero
    assert solved[1] == zero

    d0 = e**2 * j**2 * s**2 - e**2 - e * j - j**2
    leading_coefficient = (
        (e * s + 1)
        * (j * s - 1)
        * (
            3 * e**2 * j**2 * s**2
            + e**2 * j * s
            - e**2
            - e * j**3 * s**2
            - 2 * e * j**2 * s
            - e * j
            + j**3 * s
        )
    )
    middle_coefficient = -2 * (
        3 * e**3 * j**3 * s**4
        - 2 * e**3 * j * s**2
        - e**2 * j**4 * s**4
        + e**2 * j**2 * s**2
        - e**2
        - e * j
        + j**4 * s**2
    )
    constant_coefficient = (
        (e * s - 1)
        * (j * s + 1)
        * (
            3 * e**2 * j**2 * s**2
            - e**2 * j * s
            - e**2
            - e * j**3 * s**2
            + 2 * e * j**2 * s
            - e * j
            - j**3 * s
        )
    )
    exceptional_weight = (
        leading_coefficient * slope**2
        + middle_coefficient * slope
        + constant_coefficient
    )
    expected_terminal = (
        base.zero,
        -(slope + 1)
        * r
        * exceptional_weight
        / (q * (slope - 1) * d0 * weight_factor * chart_factor),
    )
    assert solved[2] == expected_terminal
    assert exceptional_weight.subs(slope, 1) == (-4 * e * q * (j * s - 1) * (j * s + 1))

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "K=C(e,j,s)[k]/((ej+k^2)(1+ejs^2)-(e+j)^2)",
                "unknowns_solved_over_K": ["w", "z6"],
                "coefficient_splitting_used": False,
                "linear_system_determinant": str(sp.factor(determinant[0].as_expr())),
                "terminal_S123_basis_coefficients": [
                    str(sp.factor(value.as_expr())) for value in solved[2]
                ],
                "exceptional_weight_degree": 2,
                "generic_weight_obstruction": True,
                "finite_field_evidence_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
