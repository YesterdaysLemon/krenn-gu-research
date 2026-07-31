#!/usr/bin/env python3
"""Independent DP-permanent audit of the corrected star obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def permanent_dp(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    target = mask | (1 << column)
                    next_states[target] = next_states.get(target, 0) + coefficient * entry
        states = next_states
    return sp.expand(states[15])


def main() -> None:
    L, z = sp.symbols("L z")
    polynomials = (
        z**2 - 2 * z + 1 / L,
        z**2 - 2 * z / L + 1 / L,
        z**2 - 1 / L,
    )
    resultants = [
        sp.factor(sp.resultant(left, right, z))
        for left, right in itertools.combinations(polynomials, 2)
    ]
    assert all(value != 0 for value in resultants)

    a = sp.Matrix((1, 1, 0, 0))
    abar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    bbar = sp.Matrix((0, 0, 1, -1))
    p, q, beta = sp.symbols("p q beta")
    support_two_words = (
        permanent_dp((a, a, b + p * abar, b + q * abar)),
        permanent_dp((a, a + beta * bbar, b + p * abar, b + q * abar)),
    )
    assert support_two_words == (4, 4)

    r1, r2, r3, s1, s2, s3 = sp.symbols("r1 r2 r3 s1 s2 s3")
    center_y = a + b
    leaves = tuple(
        (a + b - rr * bbar - ss * abar, b - ss * abar)
        for rr, ss in ((r1, s1), (r2, s2), (r3, s3))
    )
    E = s1 * s2 + s1 * s3 + s2 * s3
    first = sp.factor(permanent_dp((center_y, leaves[0][1], leaves[1][1], leaves[2][1])))
    second = sp.factor(permanent_dp((center_y, leaves[0][0], leaves[1][1], leaves[2][1])))
    assert sp.expand(first + 4 * E) == 0
    assert sp.expand(second + 4 * (E - 1)) == 0
    assert sp.expand(second - first - 4) == 0

    active = sp.Matrix((0, 0, 1, L))
    assert permanent_dp((active, active, active, active)) == 0

    result = {
        "independent_permanent": "subset dynamic programming",
        "rank_drop_resultants": [str(value) for value in resultants],
        "support_two_constant_words": [int(value) for value in support_two_words],
        "full_support_2+2_word_difference": 4,
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
