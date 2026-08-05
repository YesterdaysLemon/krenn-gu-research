#!/usr/bin/env python3
"""Audit of local lemmas in a withdrawn overstrong star theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def permanent_dp(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    new_mask = mask | (1 << column)
                    next_states[new_mask] = next_states.get(new_mask, 0) + value * entry
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
    # Pairwise intersection occurs only at the excluded cross-ratio L=1.
    numerators = [sp.together(value).as_numer_denom()[0] for value in resultants]
    assert all(sp.factor(value).subs(L, 1) == 0 for value in numerators)
    assert all(sp.factor(value / (L - 1) ** 2) != 0 for value in numerators)
    discriminants = [sp.factor(sp.discriminant(poly, z)) for poly in polynomials]
    assert discriminants[0].subs(L, 1) == 0
    assert discriminants[1].subs(L, 1) == 0
    assert discriminants[2].subs(L, 1) != 0
    assert all(value != 0 for value in discriminants)

    # Crossed balanced partition {0,2}|{1,3}.
    a = sp.Matrix((1, 0, 1, 0))
    a_bar = sp.Matrix((1, 0, -1, 0))
    b = sp.Matrix((0, 1, 0, 1))
    b_bar = sp.Matrix((0, 1, 0, -1))
    p, q, r = sp.symbols("p q r")
    rows = (
        tuple(a),
        tuple(a + p * b_bar),
        tuple(b + q * a_bar),
        tuple(b + r * a_bar),
    )
    forbidden = sp.factor(permanent_dp(rows))
    assert forbidden == 4

    # The one-infinite pencil point has no finite rank-drop partner:
    # no two leading factors can vanish for L(L-1)!=0.
    u = sp.symbols("u")
    leading = (L * u, L * u - 1, L * (u - 1))
    leading_resultants = [
        sp.solve((left, right), (u, L), dict=True)
        for left, right in itertools.combinations(leading, 2)
    ]
    assert leading_resultants[0] == []
    assert leading_resultants[1] == [{L: 0}]
    assert leading_resultants[2] == [{L: 1, u: 1}]

    result = {
        "rank_drop_pair_resultants": [str(value) for value in resultants],
        "rank_drop_matching_discriminants": [str(value) for value in discriminants],
        "infinite_parameter_pair_checks": [str(value) for value in leading_resultants],
        "crossed_partition_forbidden_coefficient": int(forbidden),
        "conclusion": "no rank-two-relation star",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
