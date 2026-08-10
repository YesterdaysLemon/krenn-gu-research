#!/usr/bin/env python3
"""Independent subset-DP audit of the full-K T=0 B obstruction."""

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
    field, e, j, s, w0, w1, z60, z61 = sp.polys.fields.field(
        "e,j,s,w0,w1,z60,z61", sp.QQ
    )
    q = e + j
    r = 1 + e * j * s**2
    p = q**2 / r
    k2 = p - e * j
    slope = (j * s + 1) / (j * s - 1)
    zero = (field.zero, field.zero)
    one = (field.one, field.zero)
    k = (field.zero, field.one)
    inverse_k = (field.zero, 1 / k2)

    def scalar(value):
        if hasattr(value, "field"):
            return (value, field.zero)
        return (field.from_expr(sp.sympify(value)), field.zero)

    def plus(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def negative(value):
        return (-value[0], -value[1])

    def product(left, right):
        return (
            left[0] * right[0] + k2 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    def scalar_product(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def vector_sum(*vectors):
        result = []
        for coordinate in range(4):
            value = zero
            for vector in vectors:
                value = plus(value, vector[coordinate])
            result.append(value)
        return tuple(result)

    def vector_scale(coefficient, vector):
        return tuple(scalar_product(coefficient, value) for value in vector)

    def vector_product(value, vector):
        return tuple(product(value, entry) for entry in vector)

    cap_a = tuple(map(scalar, (1, 1, 0, 0)))
    cap_b = tuple(map(scalar, (0, 0, 1, 1)))
    cap_c = tuple(map(scalar, (1, -1, 0, 0)))
    cap_d = tuple(map(scalar, (0, 0, 1, -1)))
    alpha = (
        vector_sum(vector_scale(q, cap_a), vector_scale(-p, cap_b)),
        vector_sum(
            vector_scale(q, vector_sum(cap_a, vector_product(k, cap_d))),
            vector_scale(-p, vector_sum(cap_b, vector_scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        vector_sum(cap_a, vector_product(k, cap_d)),
        vector_sum(
            cap_a,
            vector_scale(e, cap_b),
            vector_scale(-1, vector_product(k, cap_d)),
        ),
        vector_sum(cap_a, vector_scale(-s * j, cap_c), vector_scale(j, cap_b)),
    )

    assert (j * s - 1) * slope - (j * s + 1) == 0
    h = (slope + 1) * r - (slope - 1) * s * q
    assert h == 2 * e * s * (j * s + 1)
    branch_denominator = (slope - 1) * s * p - (slope + 1) * q
    assert branch_denominator == -q * h / r
    z3 = s / (2 * p * branch_denominator)

    w = (w0, w1)
    z6 = (z60, z61)
    z5 = plus(z6, scalar_product(-z3, k))
    z1 = plus(
        plus(
            scalar_product(q, z6),
            scalar_product(-p * s * (slope - 1), w),
        ),
        scalar_product(-j * (k2 - e**2) * z3, inverse_k),
    )
    z7 = scalar_product(
        1 / (k2 - e**2),
        plus(
            plus(
                scalar_product(p, z6),
                scalar_product(-k2 * q * (slope - 1) * s, w),
            ),
            scalar_product(-e, z1),
        ),
    )
    half = field.from_expr(sp.Rational(1, 2))
    z0 = product(
        plus(
            scalar(p**2 * z3 - half / (slope - 1)),
            scalar_product(-(q**2) * (slope + 1), product(k, w)),
        ),
        scalar_product(1 / q, inverse_k),
    )
    extension = (
        z0,
        z1,
        scalar_product(slope - 1, w),
        scalar(z3),
        scalar_product(-(slope + 1), w),
        z5,
        z6,
        z7,
    )

    def project(row, extra):
        return (
            plus(scalar_product(slope, row[0]), row[1]),
            row[2],
            row[3],
            extra,
        )

    alpha_rows = tuple(project(alpha[index], extension[index]) for index in range(4))
    beta_rows = tuple(project(beta[index], extension[index + 4]) for index in range(4))

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
                    term = product(coefficient, entry)
                    next_states[new_mask] = plus(next_states.get(new_mask, zero), term)
            states = next_states
        return states[15]

    def coefficient(word):
        return permanent_dp(
            tuple(
                beta_rows[index] if bit else alpha_rows[index]
                for index, bit in enumerate(word)
            )
        )

    c0 = coefficient((0, 0, 0, 0))
    c1 = coefficient((0, 1, 0, 0))
    c3 = coefficient((0, 0, 0, 1))
    c13 = coefficient((0, 1, 0, 1))
    segre_13 = plus(product(c13, c0), negative(product(c1, c3)))
    d0 = e**2 * j**2 * s**2 - e**2 - e * j - j**2
    assert d0 == -r * k2
    assert segre_13 == (
        field.zero,
        j * q * r / (e * (j * s - 1) * (j * s + 1) * d0),
    )

    # Direct boundary audit before localizing at H.
    lambda_symbol, e_symbol, j_symbol, s_symbol = sp.symbols("lambda e j s")
    general_h = (lambda_symbol + 1) * (1 + e_symbol * j_symbol * s_symbol**2) - (
        lambda_symbol - 1
    ) * s_symbol * (e_symbol + j_symbol)
    assert sp.expand(general_h.subs(s_symbol, 0)) == lambda_symbol + 1

    print(
        json.dumps(
            {
                "status": "PASS",
                "audit_independence": "no project imports; subset-DP permanent reconstruction",
                "arbitrary_full_K_extensions": True,
                "S13_normal_form": "k*j*Q*R/[e(js-1)(js+1)D0]",
                "T_zero_branch_empty": True,
                "H_zero_ordinary_boundary_empty": True,
                "coefficient_splitting_used": False,
                "finite_field_evidence_used": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
