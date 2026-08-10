#!/usr/bin/env python3
"""Verify component 25's global exceptional-weight opposite-diagonal divisor."""

from __future__ import annotations

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

    def extensions(w, z6):
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
        return (
            z0,
            z1,
            scale(slope - 1, w),
            lift(z3),
            scale(-(slope + 1), w),
            z5,
            z6,
            z7,
        )

    def projected(w, z6, direction):
        ext = extensions(w, z6)

        def project(row, extra):
            if direction == "D01":
                return (
                    add(scale(slope, row[0]), row[1]),
                    row[2],
                    row[3],
                    extra,
                )
            return (
                row[0],
                row[1],
                add(scale(slope, row[2]), row[3]),
                extra,
            )

        return (
            tuple(project(alpha[index], ext[index]) for index in range(4)),
            tuple(project(beta[index], ext[index + 4]) for index in range(4)),
        )

    def permanent(rows):
        total = zero
        for permutation in itertools.permutations(range(4)):
            term = one
            for index in range(4):
                term = multiply(term, rows[index][permutation[index]])
            total = add(total, term)
        return total

    def residuals(w, z6):
        alpha_rows, beta_rows = projected(w, z6, "D01")

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
            subtract(
                multiply(c123, multiply(c0, c0)),
                multiply(multiply(c1, c2), c3),
            ),
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

    alpha_01, beta_01 = projected(w_solution, z6_solution, "D01")
    c0_binary = permanent(alpha_01)
    marking = tuple(
        divide(
            negate(
                permanent(
                    tuple(
                        beta_01[index] if index == mode else alpha_01[index]
                        for index in range(4)
                    )
                )
            ),
            c0_binary,
        )
        for mode in range(4)
    )
    marked_01 = tuple(
        tuple(
            add(
                beta_01[index][column],
                multiply(marking[index], alpha_01[index][column]),
            )
            for column in range(4)
        )
        for index in range(4)
    )
    opposite_diagonal = divide(permanent(marked_01), c0_binary)
    assert opposite_diagonal[0] == base.zero
    opposite_numerator, _opposite_denominator = sp.together(
        opposite_diagonal[1].as_expr()
    ).as_numer_denom()
    e_symbol = e.as_expr()
    j_symbol = j.as_expr()
    s_symbol = s.as_expr()
    slope_symbol = slope.as_expr()
    new_opposite_factor = sp.cancel(
        opposite_numerator
        / (-j_symbol * (slope_symbol + 1) * r.as_expr())
    )
    assert sp.denom(new_opposite_factor) == 1
    parameter_field = sp.QQ.frac_field(e_symbol, j_symbol, s_symbol)
    exceptional_polynomial = sp.Poly(
        exceptional_weight.as_expr(), slope_symbol, domain=parameter_field
    )
    opposite_polynomial = sp.Poly(
        new_opposite_factor, slope_symbol, domain=parameter_field
    )
    reduced_opposite = opposite_polynomial.rem(exceptional_polynomial)
    a_symbol, b_symbol = sp.symbols("a b")
    lambda_symbol = slope_symbol
    g4 = (
        a_symbol**3 * (b_symbol - 1) ** 2
        + a_symbol**2 * (-b_symbol**3 + 3 * b_symbol - 2)
        - a_symbol * (b_symbol - 1) ** 2
        + b_symbol**3
        - 3 * b_symbol
        + 2
    )
    g3 = (
        2 * a_symbol**3 * b_symbol**2
        - 2 * a_symbol**3
        + 2 * a_symbol**2 * b_symbol**3
        + 4 * a_symbol**2 * b_symbol**2
        - 6 * a_symbol**2 * b_symbol
        - 6 * a_symbol * b_symbol**2
        + 8 * a_symbol * b_symbol
        - 2 * a_symbol
        - 2 * b_symbol**3
        - 2 * b_symbol
        + 4
    )
    g2 = (
        -6 * a_symbol**3 * b_symbol**2
        + 2 * a_symbol**3
        - 2 * a_symbol**2 * b_symbol**3
        - 2 * a_symbol**2 * b_symbol
        + 6 * a_symbol * b_symbol**2
        - 2 * a_symbol
        + 2 * b_symbol**3
        + 2 * b_symbol
    )
    g1 = (
        2 * a_symbol**3 * b_symbol**2
        - 2 * a_symbol**3
        + 2 * a_symbol**2 * b_symbol**3
        - 4 * a_symbol**2 * b_symbol**2
        - 6 * a_symbol**2 * b_symbol
        - 6 * a_symbol * b_symbol**2
        - 8 * a_symbol * b_symbol
        - 2 * a_symbol
        - 2 * b_symbol**3
        - 2 * b_symbol
        - 4
    )
    g0 = (
        a_symbol**3 * (b_symbol + 1) ** 2
        + a_symbol**2 * (-b_symbol**3 + 3 * b_symbol + 2)
        - a_symbol * (b_symbol + 1) ** 2
        + b_symbol**3
        - 3 * b_symbol
        - 2
    )
    normalized_opposite_factor = (
        g4 * lambda_symbol**4
        + g3 * lambda_symbol**3
        + g2 * lambda_symbol**2
        + g1 * lambda_symbol
        + g0
    )
    assert sp.factor(
        new_opposite_factor.subs(
            {e_symbol: a_symbol, j_symbol: b_symbol, s_symbol: 1}
        )
        - normalized_opposite_factor
    ) == 0
    assert sp.factor(
        normalized_opposite_factor
        + lambda_symbol**4
        * normalized_opposite_factor.subs(
            {
                a_symbol: -a_symbol,
                b_symbol: -b_symbol,
                lambda_symbol: 1 / lambda_symbol,
            },
            simultaneous=True,
        )
    ) == 0

    a2_normalized = (
        (a_symbol + 1)
        * (b_symbol - 1)
        * (
            3 * a_symbol**2 * b_symbol**2
            + a_symbol**2 * b_symbol
            - a_symbol**2
            - a_symbol * b_symbol**3
            - 2 * a_symbol * b_symbol**2
            - a_symbol * b_symbol
            + b_symbol**3
        )
    )
    a1_normalized = -2 * (
        3 * a_symbol**3 * b_symbol**3
        - 2 * a_symbol**3 * b_symbol
        - a_symbol**2 * b_symbol**4
        + a_symbol**2 * b_symbol**2
        - a_symbol**2
        - a_symbol * b_symbol
        + b_symbol**4
    )
    a0_normalized = (
        (a_symbol - 1)
        * (b_symbol + 1)
        * (
            3 * a_symbol**2 * b_symbol**2
            - a_symbol**2 * b_symbol
            - a_symbol**2
            - a_symbol * b_symbol**3
            + 2 * a_symbol * b_symbol**2
            - a_symbol * b_symbol
            - b_symbol**3
        )
    )
    n_normalized = (
        a2_normalized * lambda_symbol**2
        + a1_normalized * lambda_symbol
        + a0_normalized
    )
    residual_hypersurface = (
        5 * a_symbol**6 * b_symbol**5
        - 5 * a_symbol**6 * b_symbol**3
        + a_symbol**6 * b_symbol
        - 4 * a_symbol**5 * b_symbol**6
        + 12 * a_symbol**5 * b_symbol**4
        - 10 * a_symbol**5 * b_symbol**2
        + 2 * a_symbol**5
        - a_symbol**4 * b_symbol**7
        - a_symbol**4 * b_symbol**5
        - 2 * a_symbol**4 * b_symbol**3
        + a_symbol**4 * b_symbol
        + 8 * a_symbol**3 * b_symbol**6
        - 14 * a_symbol**3 * b_symbol**4
        + 6 * a_symbol**3 * b_symbol**2
        + 2 * a_symbol**2 * b_symbol**7
        - 2 * a_symbol**2 * b_symbol**5
        + 3 * a_symbol**2 * b_symbol**3
        - 4 * a_symbol * b_symbol**6
        + 4 * a_symbol * b_symbol**4
        - b_symbol**7
    )
    expected_resultant = (
        64
        * a_symbol
        * (a_symbol - b_symbol) ** 3
        * (a_symbol + b_symbol) ** 5
        * (a_symbol - 1)
        * (a_symbol + 1)
        * (b_symbol - 1) ** 2
        * (b_symbol + 1) ** 2
        * residual_hypersurface
    )
    actual_resultant = sp.factor(
        sp.resultant(n_normalized, normalized_opposite_factor, lambda_symbol)
    )
    assert actual_resultant == expected_resultant
    factor_unit, irreducible_factors = sp.factor_list(residual_hypersurface)
    assert factor_unit == 1
    assert irreducible_factors == [(residual_hypersurface, 1)]
    assert sp.degree(reduced_opposite.as_expr(), slope_symbol) == 1
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
                "normalized_opposite_factor_degree": 4,
                "opposite_mod_exceptional_degree": 1,
                "opposite_resultant_factorization": str(expected_resultant),
                "new_residual_hypersurface": "U(a,b)=0",
                "new_residual_hypersurface_irreducible": True,
                "opposite_diagonal_divisor_classified": True,
                "finite_field_evidence_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
