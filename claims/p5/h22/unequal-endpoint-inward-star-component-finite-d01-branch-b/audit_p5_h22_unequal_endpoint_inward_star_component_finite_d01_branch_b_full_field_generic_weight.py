#!/usr/bin/env python3
"""Independent subset-DP audit of the corrected full-K B obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import json
import time

import sympy as sp


def main():
    started = time.perf_counter()
    field, e, j, s, slope = sp.polys.fields.field("e,j,s,lambda", sp.QQ)
    q = e + j
    r = 1 + e * j * s**2
    p = q**2 / r
    k_squared = p - e * j
    zero = (field.zero, field.zero)
    one = (field.one, field.zero)
    k = (field.zero, field.one)
    inverse_k = (field.zero, 1 / k_squared)

    def scalar(value):
        if hasattr(value, "field"):
            return (value, field.zero)
        return (field.from_expr(sp.sympify(value)), field.zero)

    def plus(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def minus(left, right):
        return (left[0] - right[0], left[1] - right[1])

    def times(left, right):
        return (
            left[0] * right[0] + k_squared * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    def scalar_times(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def quotient(left, right):
        norm = right[0] ** 2 - k_squared * right[1] ** 2
        conjugate = (right[0] / norm, -right[1] / norm)
        return times(left, conjugate)

    def vector_sum(*vectors):
        result = []
        for index in range(4):
            value = zero
            for vector in vectors:
                value = plus(value, vector[index])
            result.append(value)
        return tuple(result)

    def vector_scale(coefficient, vector):
        return tuple(scalar_times(coefficient, entry) for entry in vector)

    def vector_times(value, vector):
        return tuple(times(value, entry) for entry in vector)

    cap_a = tuple(map(scalar, (1, 1, 0, 0)))
    cap_b = tuple(map(scalar, (0, 0, 1, 1)))
    cap_c = tuple(map(scalar, (1, -1, 0, 0)))
    cap_d = tuple(map(scalar, (0, 0, 1, -1)))
    alpha = (
        vector_sum(vector_scale(q, cap_a), vector_scale(-p, cap_b)),
        vector_sum(
            vector_scale(q, vector_sum(cap_a, vector_times(k, cap_d))),
            vector_scale(-p, vector_sum(cap_b, vector_scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        vector_sum(cap_a, vector_times(k, cap_d)),
        vector_sum(
            cap_a,
            vector_scale(e, cap_b),
            vector_scale(-1, vector_times(k, cap_d)),
        ),
        vector_sum(cap_a, vector_scale(-s * j, cap_c), vector_scale(j, cap_b)),
    )

    b_denominator = (slope - 1) * s * p - (slope + 1) * q
    z3 = s / (2 * p * b_denominator)
    half = field.from_expr(sp.Rational(1, 2))

    def permanent_dp(rows):
        states = {0: one}
        for row in rows:
            next_states = {}
            for mask, coefficient in states.items():
                for column, entry in enumerate(row):
                    bit = 1 << column
                    if mask & bit:
                        continue
                    new_mask = mask | bit
                    term = times(coefficient, entry)
                    next_states[new_mask] = plus(next_states.get(new_mask, zero), term)
            states = next_states
        return states[15]

    def minors(w, z6):
        z5 = plus(z6, scalar_times(-z3, k))
        z1 = plus(
            plus(
                scalar_times(q, z6),
                scalar_times(-p * s * (slope - 1), w),
            ),
            scalar_times(-j * (k_squared - e**2) * z3, inverse_k),
        )
        z7 = scalar_times(
            1 / (k_squared - e**2),
            plus(
                plus(
                    scalar_times(p, z6),
                    scalar_times(-k_squared * q * (slope - 1) * s, w),
                ),
                scalar_times(-e, z1),
            ),
        )
        z0 = times(
            plus(
                scalar(p**2 * z3 - half / (slope - 1)),
                scalar_times(-(q**2) * (slope + 1), times(k, w)),
            ),
            scalar_times(1 / q, inverse_k),
        )
        extension = (
            z0,
            z1,
            scalar_times(slope - 1, w),
            scalar(z3),
            scalar_times(-(slope + 1), w),
            z5,
            z6,
            z7,
        )

        def project(row, extra):
            return (
                plus(scalar_times(slope, row[0]), row[1]),
                row[2],
                row[3],
                extra,
            )

        alpha_rows = tuple(
            project(alpha[index], extension[index]) for index in range(4)
        )
        beta_rows = tuple(
            project(beta[index], extension[index + 4]) for index in range(4)
        )

        def coordinate(word):
            return permanent_dp(
                tuple(
                    beta_rows[index] if bit else alpha_rows[index]
                    for index, bit in enumerate(word)
                )
            )

        c0 = coordinate((0, 0, 0, 0))
        c1 = coordinate((0, 1, 0, 0))
        c2 = coordinate((0, 0, 1, 0))
        c3 = coordinate((0, 0, 0, 1))
        return (
            minus(times(coordinate((0, 1, 0, 1)), c0), times(c1, c3)),
            minus(times(coordinate((0, 0, 1, 1)), c0), times(c2, c3)),
            minus(
                times(coordinate((0, 1, 1, 1)), times(c0, c0)),
                times(times(c1, c2), c3),
            ),
        )

    origin = minors(zero, zero)
    unit_w = minors(one, zero)
    unit_z6 = minors(zero, one)
    a11 = minus(unit_w[0], origin[0])
    a12 = minus(unit_z6[0], origin[0])
    a21 = minus(unit_w[1], origin[1])
    a22 = minus(unit_z6[1], origin[1])
    determinant = minus(times(a11, a22), times(a12, a21))

    h = (slope + 1) * r - (slope - 1) * s * q
    t = (j * s - 1) * slope - (j * s + 1)
    asserted_determinant = (
        -32 * e * j * slope * s**2 * q**7 * (slope - 1) * t / (r**3 * h),
        field.zero,
    )
    assert determinant == asserted_determinant

    rhs1 = scalar_times(-1, origin[0])
    rhs2 = scalar_times(-1, origin[1])
    w_solution = quotient(minus(times(rhs1, a22), times(a12, rhs2)), determinant)
    z6_solution = quotient(minus(times(a11, rhs2), times(rhs1, a21)), determinant)
    terminal = minors(w_solution, z6_solution)
    assert terminal[0] == zero and terminal[1] == zero

    d0 = e**2 * j**2 * s**2 - e**2 - e * j - j**2
    coefficient_2 = (
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
    coefficient_1 = -2 * (
        3 * e**3 * j**3 * s**4
        - 2 * e**3 * j * s**2
        - e**2 * j**4 * s**4
        + e**2 * j**2 * s**2
        - e**2
        - e * j
        + j**4 * s**2
    )
    coefficient_0 = (
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
    exceptional = coefficient_2 * slope**2 + coefficient_1 * slope + coefficient_0
    asserted_terminal = (
        field.zero,
        -(slope + 1) * r * exceptional / (q * (slope - 1) * d0 * t * h),
    )
    assert terminal[2] == asserted_terminal
    assert exceptional.subs(slope, 1) == (-4 * e * q * (j * s - 1) * (j * s + 1))

    print(
        json.dumps(
            {
                "status": "PASS",
                "audit_independence": "no project imports; subset-DP permanents",
                "solved_over_full_quadratic_field": True,
                "coefficient_splitting_used": False,
                "determinant_identity_checked": True,
                "terminal_exceptional_quadratic_checked": True,
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
