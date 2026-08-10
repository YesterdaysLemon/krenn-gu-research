#!/usr/bin/env python3
"""No-import audit of the generic component-25 exceptional-divisor obstruction."""

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

PERMUTATIONS = tuple(itertools.permutations(range(4)))


def permanent(rows):
    return sum(
        sp.prod(rows[index][permutation[index]] for index in range(4))
        for permutation in PERMUTATIONS
    )


def add(*rows):
    return tuple(sum(row[index] for row in rows) for index in range(4))


def scale(coefficient, row):
    return tuple(coefficient * value for value in row)


def project(row, extension, slope):
    return (slope * row[0] + row[1], row[2], row[3], extension)


def quotient_normal_numerator(expression, k, k_squared, parameters):
    numerator = sp.fraction(sp.together(expression))[0]
    domain = sp.QQ.frac_field(*parameters)
    polynomial = sp.Poly(sp.expand(numerator), k, domain=domain)
    modulus = sp.Poly(k**2 - k_squared, k, domain=domain)
    return sp.factor(polynomial.rem(modulus).as_expr())


def main():
    started = time.perf_counter()
    e, j, k, s = sp.symbols("e j k s")
    cross = e + j
    leading = 1 + e * j * s**2
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

    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    alpha = (
        add(scale(cross, cap_a), scale(-pivot, cap_b)),
        add(
            scale(cross, add(cap_a, scale(k, cap_d))),
            scale(-pivot, add(cap_b, scale(s, cap_c))),
        ),
        cap_c,
        cap_d,
    )
    beta = (
        cap_a,
        add(cap_a, scale(k, cap_d)),
        add(cap_a, scale(e, cap_b), scale(-k, cap_d)),
        add(cap_a, scale(-s * j, cap_c), scale(j, cap_b)),
    )
    alpha_01 = tuple(
        project(alpha[index], extension[index], slope) for index in range(4)
    )
    beta_01 = tuple(
        project(beta[index], extension[4 + index], slope) for index in range(4)
    )

    assert (
        quotient_normal_numerator(permanent(alpha_01) - 1, k, k_squared, (e, j, s)) == 0
    )
    singleton_coefficients = []
    for mode in range(4):
        rows = list(alpha_01)
        rows[mode] = beta_01[mode]
        singleton_coefficients.append(permanent(tuple(rows)))
    marking = (
        0,
        -e / e2_minus_k2,
        -j * s,
        -j * (2 * e**2 * j**2 * s**2 - e**2 - j**2) / (k * (e - j) * leading),
    )
    for singleton, marked_shift in zip(singleton_coefficients, marking):
        assert (
            quotient_normal_numerator(singleton + marked_shift, k, k_squared, (e, j, s))
            == 0
        )

    marked_01 = tuple(
        add(beta_01[index], scale(marking[index], alpha_01[index]))
        for index in range(4)
    )
    assert quotient_normal_numerator(permanent(marked_01), k, k_squared, (e, j, s)) == 0

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_generic_exceptional_divisor_obstruction",
                "role": "independent no-import exact quadratic-field audit",
                "field": "C(e,j,s)[k]/(F)",
                "normalization_C0000": "1",
                "forced_marking_verified": True,
                "marked_D01_all_beta_diagonal_normal_form": "0",
                "paired_D23_minor_checked_by": "primary verifier",
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
