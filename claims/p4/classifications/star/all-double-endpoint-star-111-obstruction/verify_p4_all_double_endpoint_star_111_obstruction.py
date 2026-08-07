#!/usr/bin/env python3
"""Verify the all-double-endpoint star-(1,1,1) obstruction."""

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
    # Singleton support.  Kernel-row shifts put every active row in a
    # three-coordinate hyperplane, so its four-row permanent vanishes.
    singleton = sp.Matrix((1, 0, 0, 0))
    singleton_active = [
        sp.Matrix((0, *sp.symbols(f"s{mode}_1:4"))) for mode in range(4)
    ]
    assert squarefree_product(singleton, singleton) == sp.zeros(6, 1)
    assert permanent(singleton_active) == 0

    # Genuine binary support in an adapted hyperbolic basis.
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    assert squarefree_product(A, C) == sp.zeros(6, 1)

    a0, b0, d0 = sp.symbols("a0 b0 d0")
    leaf_parameters = sp.symbols("a1 b1 d1 a2 b2 d2 a3 b3 d3")
    x0 = a0 * C + b0 * B + d0 * D
    leaves = []
    for index in range(3):
        ai, bi, di = leaf_parameters[3 * index : 3 * index + 3]
        leaves.append(ai * A + bi * B + di * D)

    e_values = [
        sp.expand(b0 * leaf_parameters[3 * index + 1] - d0 * leaf_parameters[3 * index + 2])
        for index in range(3)
    ]
    mixed = [
        permanent((x0, leaves[0] if index == 0 else C,
                   leaves[1] if index == 1 else C,
                   leaves[2] if index == 2 else C))
        for index in range(3)
    ]
    assert all(
        sp.factor(mixed[index] + 4 * e_values[index]) == 0 for index in range(3)
    )

    a1, _, _, a2, _, _, a3, _, _ = leaf_parameters
    active = permanent((x0, *leaves))
    syzygy = 4 * (a2 * a3 * e_values[0] + a1 * a3 * e_values[1] + a1 * a2 * e_values[2])
    assert sp.factor(active - syzygy) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation": "all three selected star spokes kernel--kernel",
                "zero_divisor_supports": [1, 2],
                "binary_mixed_coefficients": [str(sp.factor(value)) for value in mixed],
                "all_active_syzygy": str(sp.factor(syzygy)),
                "nonzero_pure_stratum_empty": True,
                "partial_double_endpoint_orientations_classified": False,
                "star_111_cell_complete": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
