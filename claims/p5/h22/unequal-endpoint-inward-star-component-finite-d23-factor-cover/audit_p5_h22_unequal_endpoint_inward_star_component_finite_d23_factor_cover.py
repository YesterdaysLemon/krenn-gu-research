#!/usr/bin/env python3
"""No-import audit of the finite-D23 factor cover."""

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
    return (row[0], row[1], slope * row[2] + row[3], extension)


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
    e, j, k, s, slope = sp.symbols("e j k s lambda")
    extensions = sp.symbols("z0:8")
    z0, _, z2, z3, z4, z5, _, _ = extensions
    pivot = e * j + k**2
    cross = e + j
    alpha, beta = bases(e, j, k, s)
    coefficients = tensor(alpha, beta, extensions, slope)

    empty = coefficients[(0, 0, 0, 0)]
    c0001 = coefficients[(0, 0, 0, 1)]
    c0100 = coefficients[(0, 1, 0, 0)]
    c0101 = coefficients[(0, 1, 0, 1)]
    c1000 = coefficients[(1, 0, 0, 0)]
    c1100 = coefficients[(1, 1, 0, 0)]
    c1101 = coefficients[(1, 1, 0, 1)]
    divisor_a = (slope - 1) * z2
    divisor_g = (slope - 1) * (z0 - cross * z4) - pivot * (slope + 1) * z3
    divisor_j = j * s * (k * z3 - z5) - z2
    diagonal_gap = empty - cross * c1000
    coordinate_gap = c0101 - cross * c1101

    identities = (
        c0100 - cross * c1100,
        c1100 - 2 * divisor_a,
        c1000 - 2 * (slope - 1) * (pivot * s * z4 + cross * z2),
        diagonal_gap - 2 * pivot * s * divisor_g,
    )
    assert all(sp.factor(value) == 0 for value in identities)

    divisor_h = j * k * s * (slope - 1) * (z0 - cross * z4) - pivot * (slope + 1) * (
        j * s * z5 + z2
    )
    assert sp.factor(coordinate_gap - 2 * divisor_h) == 0
    assert (
        sp.factor(divisor_h - pivot * (slope + 1) * divisor_j - j * k * s * divisor_g)
        == 0
    )

    segre_01 = c1100 * empty - c1000 * c0100
    segre_13 = c0101 * empty - c0100 * c0001
    segre_013 = c1101 * empty**2 - c1000 * c0100 * c0001
    assert sp.factor(segre_01 - c1100 * diagonal_gap) == 0
    assert (
        sp.factor(
            empty * segre_13
            - cross * segre_013
            - empty**2 * coordinate_gap
            + diagonal_gap * c0100 * c0001
        )
        == 0
    )

    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass_with_factor_cover",
                "role": "independent no-import subset-DP symbolic audit",
                "field": "characteristic zero",
                "finite_D23_cover_branch_count": 3,
                "finite_D23_cover_branches_closed": False,
                "finite_D23_closed": False,
                "finite_D01_residual_closed": False,
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
