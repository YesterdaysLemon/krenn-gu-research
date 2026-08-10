#!/usr/bin/env python3
"""Independent audit of the finite-D01 B-branch descent-only identities."""

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
    field, e, j, s, slope, w, free_z6 = sp.polys.fields.field(
        "e,j,s,lambda,w,z6", sp.QQ
    )
    q = e + j
    r = 1 + e * j * s**2
    p = q**2 / r
    k2 = p - e * j
    zero = (field.zero, field.zero)
    one = (field.one, field.zero)

    def lift(value):
        if hasattr(value, "field"):
            return (value, field.zero)
        return (field.from_expr(sp.sympify(value)), field.zero)

    def qadd(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def qneg(value):
        return (-value[0], -value[1])

    def qmul(left, right):
        return (
            left[0] * right[0] + k2 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    def qscale(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

    def qdivide(value, denominator):
        return (value[0] / denominator, value[1] / denominator)

    k = (field.zero, field.one)
    inv_k = (field.zero, 1 / k2)

    def vector_sum(*vectors):
        return tuple(
            sum_entry(vector[index] for vector in vectors) for index in range(4)
        )

    def sum_entry(entries):
        total = zero
        for entry in entries:
            total = qadd(total, entry)
        return total

    def vector_scale(coefficient, vector):
        return tuple(qscale(coefficient, entry) for entry in vector)

    def vector_qmul(value, vector):
        return tuple(qmul(value, entry) for entry in vector)

    cap_a = tuple(map(lift, (1, 1, 0, 0)))
    cap_b = tuple(map(lift, (0, 0, 1, 1)))
    cap_c = tuple(map(lift, (1, -1, 0, 0)))
    cap_d = tuple(map(lift, (0, 0, 1, -1)))
    alpha = (
        vector_sum(vector_scale(q, cap_a), vector_scale(-p, cap_b)),
        vector_sum(
            vector_scale(q, vector_sum(cap_a, vector_qmul(k, cap_d))),
            vector_scale(-p, vector_sum(cap_b, vector_scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        vector_sum(cap_a, vector_qmul(k, cap_d)),
        vector_sum(
            cap_a, vector_scale(e, cap_b), vector_scale(-1, vector_qmul(k, cap_d))
        ),
        vector_sum(cap_a, vector_scale(-s * j, cap_c), vector_scale(j, cap_b)),
    )

    h = (slope + 1) * r - (slope - 1) * s * q
    b_denominator = (slope - 1) * s * p - (slope + 1) * q
    assert b_denominator == -q * h / r
    z3 = s / (2 * p * b_denominator)
    assert 2 * p * b_denominator * z3 - s == 0

    def extensions(z6):
        z5 = qadd(lift(z6), qscale(-z3, k))
        z1 = qadd(
            lift(q * z6 - p * s * (slope - 1) * w),
            qscale(-j * (k2 - e**2) * z3, inv_k),
        )
        z7 = qdivide(
            qadd(
                lift(p * z6 - k2 * q * (slope - 1) * s * w),
                qscale(-e, z1),
            ),
            k2 - e**2,
        )
        z0 = qmul(
            qadd(
                lift(p**2 * z3 - field.from_expr(sp.Rational(1, 2)) / (slope - 1)),
                qscale(-(q**2) * (slope + 1) * w, k),
            ),
            qscale(1 / q, inv_k),
        )
        return (
            z0,
            z1,
            lift((slope - 1) * w),
            lift(z3),
            lift(-(slope + 1) * w),
            z5,
            lift(z6),
            z7,
        )

    def projected_rows(z6):
        ext = extensions(z6)

        def project(row, extra):
            return (
                qadd(qscale(slope, row[0]), row[1]),
                row[2],
                row[3],
                extra,
            )

        return (
            tuple(project(alpha[index], ext[index]) for index in range(4)),
            tuple(project(beta[index], ext[index + 4]) for index in range(4)),
        )

    # Deliberately use subset dynamic programming, rather than the primary
    # verifier's permutation expansion, for an independent permanent audit.
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
                    term = qmul(coefficient, entry)
                    next_states[new_mask] = qadd(next_states.get(new_mask, zero), term)
            states = next_states
        return states[15]

    def coordinate(word, z6):
        alpha_rows, beta_rows = projected_rows(z6)
        return permanent_dp(
            tuple(
                beta_rows[index] if bit else alpha_rows[index]
                for index, bit in enumerate(word)
            )
        )

    def segre_13(z6):
        c0 = coordinate((0, 0, 0, 0), z6)
        c1 = coordinate((0, 1, 0, 0), z6)
        c3 = coordinate((0, 0, 0, 1), z6)
        c13 = coordinate((0, 1, 0, 1), z6)
        return qadd(qmul(c13, c0), qneg(qmul(c1, c3)))

    def segre_23(z6):
        c0 = coordinate((0, 0, 0, 0), z6)
        c2 = coordinate((0, 0, 1, 0), z6)
        c3 = coordinate((0, 0, 0, 1), z6)
        c23 = coordinate((0, 0, 1, 1), z6)
        return qadd(qmul(c23, c0), qneg(qmul(c2, c3)))

    t = (j * s - 1) * slope - (j * s + 1)
    d0 = e**2 * j**2 * s**2 - e**2 - e * j - j**2
    assert d0 == -r * k2
    u = s**2 * (e**2 * j**2 * s**2 - e**2 - j**2)
    g = u * (slope - 1) ** 2 + 4 * e * j * slope * s**2 + (slope + 1) ** 2

    audited_13 = segre_13(free_z6)
    asserted_13 = (
        2 * q**3 * (slope - 1) * ((slope + 1) * w + free_z6) * t / (r * h),
        j * r * g / (d0 * h**2),
    )
    assert audited_13 == asserted_13

    fixed_z6 = -(slope + 1) * w
    audited_23 = segre_23(fixed_z6)
    asserted_23 = (
        16 * e * j * slope * s**2 * w * q**4 / r**2,
        2 * e * j**2 * s * (e * s - 1) * (e * s + 1) * r * t / (d0 * h),
    )
    assert audited_23 == asserted_23

    t_root = (j * s + 1) / (j * s - 1)
    g_at_t_root = u * (t_root - 1) ** 2 + 4 * e * j * t_root * s**2 + (t_root + 1) ** 2
    assert (j * s - 1) ** 2 * g_at_t_root == (
        4 * e * s**2 * q * (j * s - 1) * (j * s + 1)
    )

    print(
        json.dumps(
            {
                "status": "PASS_IDENTITIES_ONLY",
                "audit_independence": "no project imports; subset-DP permanent reconstruction",
                "B_equation_checked": True,
                "S13_identity_checked": True,
                "S23_identity_checked": True,
                "linear_quadratic_resultant_checked": True,
                "generic_B_branch_empty": False,
                "descent_only_factor_cover": "e*j*s*(e^2*s^2-1)*(j*s+1)=0",
                "invalid_generic_inference": "quadratic-basis coefficients cannot be split at arbitrary K-points",
                "finite_field_evidence_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
