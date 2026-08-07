#!/usr/bin/env python3
"""Verify the strict all-center-kernel star-(1,1,1) obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def squarefree_product(left, right):
    return sp.Matrix(
        [
            left[i] * right[j] + left[j] * right[i]
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def main():
    a, b = sp.symbols("a b", nonzero=True)
    active_center = sp.Matrix(sp.symbols("c0:4"))

    singleton = sp.Matrix((1, 0, 0, 0))
    assert squarefree_product(singleton, singleton) == sp.zeros(6, 1)
    assert permanent((active_center, singleton, singleton, singleton)) == 0

    center_kernel = sp.Matrix((a, b, 0, 0))
    common_leaf_active = sp.Matrix((a, -b, 0, 0))
    assert squarefree_product(center_kernel, common_leaf_active) == sp.zeros(6, 1)
    assert permanent(
        (active_center, common_leaf_active, common_leaf_active, common_leaf_active)
    ) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation": "strict all-three-arrows-to-center star-(1,1,1)",
                "zero_divisor_supports": [1, 2],
                "common_polar_cube_zero": True,
                "nonzero_pure_stratum_empty": True,
                "double-endpoint_boundaries_classified": False,
                "star_111_cell_complete": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
