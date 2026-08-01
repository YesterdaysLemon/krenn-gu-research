#!/usr/bin/env python3
"""Independent subset-DP audit of the strict all-center star obstruction."""

from __future__ import annotations

import json

import sympy as sp


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column in range(4):
                if not mask & (1 << column):
                    new_mask = mask | (1 << column)
                    updated[new_mask] = updated.get(new_mask, 0) + value * row[column]
        states = updated
    return sp.expand(states[15])


def transform(row):
    permutation = (2, 0, 3, 1)
    scales = tuple(map(sp.Rational, (2, 3, 5, 7)))
    return sp.Matrix([row[permutation[index]] * scales[index] for index in range(4)])


def main():
    center_active = transform(sp.Matrix((2, 3, 5, 7)))
    for polar in (sp.Matrix((1, 0, 0, 0)), sp.Matrix((2, -3, 0, 0))):
        moved_polar = transform(polar)
        assert permanent_dp(
            (center_active, moved_polar, moved_polar, moved_polar)
        ) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent subset-DP rational audit",
                "field": "Q",
                "source_permutation": [2, 0, 3, 1],
                "source_scales": [2, 3, 5, 7],
                "singleton_and_binary_polar_cubes_zero": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
