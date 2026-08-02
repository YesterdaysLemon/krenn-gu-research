#!/usr/bin/env python3
"""No-import audit of the finite-D01 residual factor cover."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent_dp(square):
    states = {0: sp.Integer(1)}
    for row in square:
        next_states = {}
        for mask, coefficient in states.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + coefficient * row[column]
                )
        states = next_states
    return sp.expand(states[15])


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * value) for value in row)


def bases(e, j, k, s):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    pivot = e * j + k**2
    cross = e + j
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
    return alpha, beta


def projected(row, extension, slope):
    return (slope * row[0] + row[1], row[2], row[3], extension)


def tensor(alpha, beta, extensions, slope):
    alpha_rows = tuple(
        projected(alpha[index], extensions[index], slope) for index in range(4)
    )
    beta_rows = tuple(
        projected(beta[index], extensions[4 + index], slope) for index in range(4)
    )
    return {
        word: permanent_dp(
            tuple(
                beta_rows[index] if word[index] else alpha_rows[index]
                for index in range(4)
            )
        )
        for word in WORDS
    }


def main():
    started = time.perf_counter()
    e, j, k, s, slope, w = sp.symbols("e j k s lambda w")
    z0, z1, _, z3, _, z5, z6, z7 = sp.symbols("z0:8")
    pivot = e * j + k**2
    cross = e + j
    extensions = (z0, z1, (slope - 1) * w, z3, -(slope + 1) * w, z5, z6, z7)
    alpha, beta = bases(e, j, k, s)
    coefficients = tensor(alpha, beta, extensions, slope)

    assert all(
        sp.factor(coefficients[word]) == 0
        for word in ((1, 0, 0, 0), (1, 0, 0, 1), (1, 1, 0, 0), (1, 1, 0, 1))
    )
    empty = coefficients[(0, 0, 0, 0)]
    assert sp.factor(empty.subs(slope, 1)) == 0

    solution = {
        z5: z6 - k * z3,
        z1: cross * z6 - pivot * s * (slope - 1) * w - j * (k**2 - e**2) * z3 / k,
    }
    solution[z7] = (
        pivot * z6 - k**2 * cross * (slope - 1) * s * w - e * solution[z1]
    ) / (k**2 - e**2)
    solution[z0] = (
        pivot**2 * z3 - k * cross**2 * (slope + 1) * w - 1 / (2 * (slope - 1))
    ) / (k * cross)
    forced = (
        coefficients[(1, 0, 1, 0)],
        coefficients[(1, 0, 1, 1)],
        coefficients[(1, 1, 1, 0)],
        empty - 1,
    )
    assert all(sp.factor(sp.cancel(value.subs(solution))) == 0 for value in forced)

    c1 = coefficients[(0, 1, 0, 0)]
    c2 = coefficients[(0, 0, 1, 0)]
    first_toric = sp.cancel(
        (coefficients[(0, 1, 1, 0)] * empty - c1 * c2).subs(solution)
    )
    factor_a = 1 + 2 * (slope - 1) * (e**2 - k**2) * pivot * z3
    factor_b = 2 * pivot * ((slope - 1) * s * pivot - (slope + 1) * cross) * z3 - s
    assert (
        sp.factor(sp.cancel(first_toric - pivot * factor_a * factor_b / cross**2)) == 0
    )

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_factor_cover",
                "role": "independent no-import subset-DP symbolic audit",
                "field": "characteristic zero",
                "lambda_one_binary_incidence_empty": True,
                "ordinary_weight_factor_count": 2,
                "ordinary_factor_branches_closed": False,
                "lambda_minus_one_closed": False,
                "finite_D01_residual_closed": False,
                "finite_D23_closed": False,
                "generic_weighted_H22_fibre_empty": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
