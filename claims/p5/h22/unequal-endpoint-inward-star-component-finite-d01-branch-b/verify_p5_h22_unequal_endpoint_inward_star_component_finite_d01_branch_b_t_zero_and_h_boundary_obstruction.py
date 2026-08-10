#!/usr/bin/env python3
"""Verify the full-K T=0 obstruction and the empty H=0 boundary."""

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
    base, e, j, s, w0, w1, z60, z61 = sp.polys.fields.field(
        "e,j,s,w0,w1,z60,z61", sp.QQ
    )
    q = e + j
    r = 1 + e * j * s**2
    p = q**2 / r
    k2 = p - e * j
    slope = (j * s + 1) / (j * s - 1)
    zero = (base.zero, base.zero)
    one = (base.one, base.zero)
    k = (base.zero, base.one)
    inverse_k = (base.zero, 1 / k2)

    def lift(value):
        if hasattr(value, "field"):
            return (value, base.zero)
        return (base.from_expr(sp.sympify(value)), base.zero)

    def add(left, right):
        return (left[0] + right[0], left[1] + right[1])

    def negate(value):
        return (-value[0], -value[1])

    def multiply(left, right):
        return (
            left[0] * right[0] + k2 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    def scale(coefficient, value):
        return (coefficient * value[0], coefficient * value[1])

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

    t = (j * s - 1) * slope - (j * s + 1)
    assert t == 0
    h = (slope + 1) * r - (slope - 1) * s * q
    assert h == 2 * e * s * (j * s + 1)
    branch_denominator = (slope - 1) * s * p - (slope + 1) * q
    assert branch_denominator == -q * h / r
    z3 = s / (2 * p * branch_denominator)
    assert 2 * p * branch_denominator * z3 - s == 0

    # These four independent scalar parameters make w,z6 arbitrary elements
    # of the full quadratic field, rather than base-descending coordinates.
    w = (w0, w1)
    z6 = (z60, z61)
    z5 = add(z6, scale(-z3, k))
    z1 = add(
        add(scale(q, z6), scale(-p * s * (slope - 1), w)),
        scale(-j * (k2 - e**2) * z3, inverse_k),
    )
    z7 = scale(
        1 / (k2 - e**2),
        add(
            add(scale(p, z6), scale(-k2 * q * (slope - 1) * s, w)),
            scale(-e, z1),
        ),
    )
    half = base.from_expr(sp.Rational(1, 2))
    z0 = multiply(
        add(
            lift(p**2 * z3 - half / (slope - 1)),
            scale(-(q**2) * (slope + 1), multiply(k, w)),
        ),
        scale(1 / q, inverse_k),
    )
    extension = (
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

    alpha_rows = tuple(project(alpha[index], extension[index]) for index in range(4))
    beta_rows = tuple(project(beta[index], extension[index + 4]) for index in range(4))

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
                beta_rows[index] if bit else alpha_rows[index]
                for index, bit in enumerate(word)
            )
        )

    c0 = coefficient((0, 0, 0, 0))
    c1 = coefficient((0, 1, 0, 0))
    c3 = coefficient((0, 0, 0, 1))
    c13 = coefficient((0, 1, 0, 1))
    segre_13 = add(multiply(c13, c0), negate(multiply(c1, c3)))
    d0 = e**2 * j**2 * s**2 - e**2 - e * j - j**2
    expected = (
        base.zero,
        j * q * r / (e * (j * s - 1) * (j * s + 1) * d0),
    )
    assert segre_13 == expected

    # On H=0 the original B equation reduces to -s=0.  Then H=lambda+1,
    # so the only such point is the already excluded endpoint lambda=-1.
    slope_symbol = sp.symbols("lambda")
    assert (
        sp.expand(
            (
                (slope_symbol + 1)
                * (1 + e.as_expr() * j.as_expr() * sp.Symbol("s") ** 2)
                - (slope_symbol - 1) * sp.Symbol("s") * (e.as_expr() + j.as_expr())
            ).subs(sp.Symbol("s"), 0)
        )
        == slope_symbol + 1
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "C(e,j,s)[k]/((ej+k^2)R-Q^2)",
                "T_zero_weight": "lambda=(js+1)/(js-1)",
                "arbitrary_full_K_extensions": ["w0+w1*k", "z60+z61*k"],
                "S13_on_T_zero": "k*j*Q*R/[e(js-1)(js+1)D0]",
                "S13_independent_of_extensions": True,
                "T_zero_branch_empty_on_standing_chart": True,
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
