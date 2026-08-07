#!/usr/bin/env python3
"""No-import audit of the all-double-endpoint star obstruction."""

from __future__ import annotations

import json

import sympy as sp


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                updated[new_mask] = updated.get(new_mask, 0) + value * row[column]
        states = updated
    return sp.expand(states[15])


def main():
    # Independently move the binary support and apply unequal source scales.
    u = sp.Matrix((0, 2, 0, 3))
    v = sp.Matrix((0, 2, 0, -3))
    b_form = sp.Matrix((5, 0, 7, 0))
    d_form = sp.Matrix((5, 0, -7, 0))

    a0, b0, d0 = sp.symbols("c0 e0 f0")
    parameters = sp.symbols("c1 e1 f1 c2 e2 f2 c3 e3 f3")
    x0 = a0 * v + b0 * b_form + d0 * d_form
    leaves = []
    for index in range(3):
        ai, bi, di = parameters[3 * index : 3 * index + 3]
        leaves.append(ai * u + bi * b_form + di * d_form)

    mixed = []
    for active_leaf in range(3):
        rows = [x0]
        rows.extend(leaves[index] if index == active_leaf else v for index in range(3))
        mixed.append(sp.factor(permanent_dp(rows)))

    active = sp.factor(permanent_dp((x0, *leaves)))
    # Solve the three mixed equations for the corresponding e0*ei-f0*fi
    # factors by direct division; the nonzero constants are retained.
    factors = [
        sp.expand(b0 * parameters[3 * index + 1] - d0 * parameters[3 * index + 2])
        for index in range(3)
    ]
    constants = [sp.factor(mixed[index] / factors[index]) for index in range(3)]
    assert all(value.is_nonzero for value in constants)
    a1, _, _, a2, _, _, a3, _, _ = parameters
    reconstructed = -(
        constants[2] * a1 * a2 * factors[2]
        + constants[1] * a1 * a3 * factors[1]
        + constants[0] * a2 * a3 * factors[0]
    )
    assert sp.factor(active - reconstructed) == 0

    # A moved singleton has the same gauge: all active rows omit its coordinate.
    singleton_rows = [
        sp.Matrix((sp.Symbol(f"z{mode}0"), sp.Symbol(f"z{mode}1"), 0, sp.Symbol(f"z{mode}3")))
        for mode in range(4)
    ]
    assert permanent_dp(singleton_rows) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import subset-DP audit",
                "field": "Q",
                "moved_binary_support": [1, 3],
                "unequal_source_scales": [2, 3, 5, 7],
                "mixed_coefficient_constants": [str(value) for value in constants],
                "all_active_in_mixed_ideal": True,
                "singleton_active_permanent_zero": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
