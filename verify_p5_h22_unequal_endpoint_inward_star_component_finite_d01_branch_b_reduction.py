#!/usr/bin/env python3
"""Staged quadratic-field reduction of the finite-D01 B branch."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp


def main():
    started = time.perf_counter()
    base, e, j, s, slope, w, z6 = sp.polys.fields.field("e,j,s,lambda,w,z6", sp.QQ)
    cross = e + j
    leading = 1 + e * j * s**2
    pivot = cross**2 / leading
    k_squared = pivot - e * j
    half = base.from_expr(sp.Rational(1, 2))

    def scalar(value):
        if hasattr(value, "field"):
            return (value, base.zero)
        return (base.from_expr(sp.sympify(value)), base.zero)

    k = (base.zero, base.one)

    def add(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def negate(value):
        return (-value[0], -value[1])

    def multiply(left, right):
        return (
            left[0] * right[0] + left[1] * right[1] * k_squared,
            left[0] * right[1] + left[1] * right[0],
        )

    def scale(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def divide_scalar(value, denominator):
        return (value[0] / denominator, value[1] / denominator)

    inverse_k = (base.zero, 1 / k_squared)

    def row_add(*rows):
        result = []
        for coordinate in range(4):
            value = scalar(0)
            for row in rows:
                value = add(value, row[coordinate])
            result.append(value)
        return tuple(result)

    def row_scale(coefficient, row):
        return tuple(scale(coefficient, value) for value in row)

    def row_multiply(value, row):
        return tuple(multiply(value, entry) for entry in row)

    cap_a = tuple(map(scalar, (1, 1, 0, 0)))
    cap_c = tuple(map(scalar, (1, -1, 0, 0)))
    cap_b = tuple(map(scalar, (0, 0, 1, 1)))
    cap_d = tuple(map(scalar, (0, 0, 1, -1)))
    alpha = (
        row_add(row_scale(cross, cap_a), row_scale(-pivot, cap_b)),
        row_add(
            row_scale(cross, row_add(cap_a, row_multiply(k, cap_d))),
            row_scale(-pivot, row_add(cap_b, row_scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        row_add(cap_a, row_multiply(k, cap_d)),
        row_add(cap_a, row_scale(e, cap_b), row_scale(-1, row_multiply(k, cap_d))),
        row_add(cap_a, row_scale(-s * j, cap_c), row_scale(j, cap_b)),
    )

    branch_denominator = (slope - 1) * s * pivot - (slope + 1) * cross
    z3 = s / (2 * pivot * branch_denominator)
    z5 = add(scalar(z6), scale(-z3, k))
    z1 = add(
        scalar(cross * z6 - pivot * s * (slope - 1) * w),
        scale(-j * (k_squared - e**2) * z3, inverse_k),
    )
    z7 = divide_scalar(
        add(
            scalar(pivot * z6 - k_squared * cross * (slope - 1) * s * w),
            scale(-e, z1),
        ),
        k_squared - e**2,
    )
    z0 = multiply(
        add(
            scalar(pivot**2 * z3 - half / (slope - 1)),
            scale(-(cross**2) * (slope + 1) * w, k),
        ),
        scale(1 / cross, inverse_k),
    )
    extension = (
        z0,
        z1,
        scalar((slope - 1) * w),
        scalar(z3),
        scalar(-(slope + 1) * w),
        z5,
        scalar(z6),
        z7,
    )

    def project(row, extra):
        return (
            add(scale(slope, row[0]), row[1]),
            row[2],
            row[3],
            extra,
        )

    alpha_projected = tuple(
        project(alpha[index], extension[index]) for index in range(4)
    )
    beta_projected = tuple(
        project(beta[index], extension[4 + index]) for index in range(4)
    )

    def permanent(rows):
        total = scalar(0)
        for permutation in itertools.permutations(range(4)):
            term = scalar(1)
            for index in range(4):
                term = multiply(term, rows[index][permutation[index]])
            total = add(total, term)
        return total

    def coefficient(word):
        return permanent(
            tuple(
                beta_projected[index] if word[index] else alpha_projected[index]
                for index in range(4)
            )
        )

    empty = coefficient((0, 0, 0, 0))
    c1 = coefficient((0, 1, 0, 0))
    c2 = coefficient((0, 0, 1, 0))
    c3 = coefficient((0, 0, 0, 1))
    c13 = coefficient((0, 1, 0, 1))
    c23 = coefficient((0, 0, 1, 1))
    segre_13 = add(multiply(c13, empty), negate(multiply(c1, c3)))
    segre_23 = add(multiply(c23, empty), negate(multiply(c2, c3)))

    base_discriminant = e**2 * j**2 * s**2 - e**2 - e * j - j**2
    chart_factor = (
        e * j * (slope + 1) * s**2
        - e * (slope - 1) * s
        - j * (slope - 1) * s
        + slope
        + 1
    )
    weight_factor = (j * s - 1) * slope - (j * s + 1)
    weight_quadratic = (
        s**2 * (e**2 * j**2 * s**2 - e**2 - j**2) * (slope - 1) ** 2
        + 4 * e * j * slope * s**2
        + (slope + 1) ** 2
    )
    expected_13 = (
        2
        * cross**3
        * (slope - 1)
        * ((slope + 1) * w + z6)
        * weight_factor
        / (leading * chart_factor),
        j * leading * weight_quadratic / (base_discriminant * chart_factor**2),
    )
    assert segre_13 == expected_13

    z6_symbol = z6.as_expr()
    z6_relation = -(slope.as_expr() + 1) * w.as_expr()
    reduced_23 = tuple(
        sp.factor(sp.cancel(value.as_expr().subs(z6_symbol, z6_relation)))
        for value in segre_23
    )
    expected_23 = (
        16 * e * j * slope * s**2 * w * cross**4 / leading**2,
        2
        * e
        * j**2
        * s
        * (e * s - 1)
        * (e * s + 1)
        * leading
        * weight_factor
        / (base_discriminant * chart_factor),
    )
    expected_23_expr = tuple(value.as_expr() for value in expected_23)
    assert all(
        sp.cancel(actual - expected) == 0
        for actual, expected in zip(reduced_23, expected_23_expr)
    )

    # The S13 k-coefficient forces weight_quadratic=0.  Away from the
    # explicit factors in S23, the S23 k-coefficient forces
    # weight_factor=0.  Evaluating the former on the latter's linear root
    # gives the exact residual base divisor without a Groebner computation.
    weight_root = (j * s + 1) / (j * s - 1)
    quadratic_at_root = (
        s**2 * (e**2 * j**2 * s**2 - e**2 - j**2) * (weight_root - 1) ** 2
        + 4 * e * j * weight_root * s**2
        + (weight_root + 1) ** 2
    )
    resultant_identity = (
        j * s - 1
    ) ** 2 * quadratic_at_root == 4 * e * s**2 * cross * (j * s - 1) * (j * s + 1)
    assert resultant_identity

    # Record the two linear sheets of the palindromic weight quadratic over
    # the same quadratic function field.  The factor a0=0 is kept as a
    # separate base boundary rather than silently divided out.
    quadratic_core = s**2 * (e**2 * j**2 * s**2 - e**2 - j**2)
    a0 = quadratic_core + 1
    middle = -quadratic_core + 2 * e * j * s**2 + 1
    sheet_product = multiply(
        (a0 * slope + middle, -2 * s * leading),
        (a0 * slope + middle, 2 * s * leading),
    )
    assert sheet_product == (a0 * weight_quadratic, base.zero)

    reduced_13 = tuple(sp.factor(value.as_expr()) for value in segre_13)

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "PASS",
                "field_representation": "C(e,j,s,lambda,w,z6)[k]/(k^2-Q^2/R+ej)",
                "B_branch_z3": "s/[2P((lambda-1)sP-(lambda+1)Q)]",
                "S13_coefficients_in_basis_1_k": list(map(str, reduced_13)),
                "S23_coefficients_after_z6_relation": list(map(str, reduced_23)),
                "weight_resultant_identity": "(js-1)^2 G((js+1)/(js-1)) = 4 e s^2 Q (js-1)(js+1)",
                "weight_quadratic_sheet_factorization": "a0 G=(a0 lambda+V-2sRk)(a0 lambda+V+2sRk)",
                "generic_B_branch_empty": True,
                "special_base_factor_cover": "e*j*s*(e^2*s^2-1)*(j*s+1)=0",
                "theorem_claimed": "generic characteristic-zero obstruction only",
                "finite_field_evidence_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
