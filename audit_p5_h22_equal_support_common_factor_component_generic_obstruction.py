#!/usr/bin/env python3
"""Independent subset-DP audit of the eleventh component's H22 obstruction."""

from __future__ import annotations

import json

import sympy as sp


def subset_permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    table: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        nxt: dict[int, sp.Expr] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = sp.expand(nxt.get(target, 0) + coefficient * entry)
        table = nxt
    return sp.factor(table[15])


def main() -> None:
    p, q, r = sp.symbols("p q r")
    lam, mu = sp.symbols("lambda mu")
    t0, t1, t2, t3 = sp.symbols("t0:4")
    x0, x1, x2, x3 = sp.symbols("x0:4")
    c0, c1, c2, c3 = sp.symbols("c0:4")
    radius = r + 1
    Q = 1 + q * radius

    # This reconstruction is deliberately independent of the primary
    # component and weighted-row constructors.  The arbitrary c_i also audit
    # independent rescaling of all four marked kernel rows.
    rows = (
        (
            c0
            * (lam * t0 * (Q - p * radius) + mu * t1 * (Q + p * radius)),
            c0 * p * t2,
            c0 * p * t3,
            x0,
        ),
        (c1 * (lam * t0 + mu * t1), 0, 0, x1),
        (c2 * (lam * t0 + mu * t1), 0, 0, x2),
        (0, c3 * t2, -c3 * t3, x3),
    )
    residual = sp.factor(rows[0][1] * rows[3][2] + rows[0][2] * rows[3][1])
    diagonal = subset_permanent(rows)
    assert residual == 0
    assert diagonal == 0

    # Swapping both coordinates inside the exact-zero-divisor block changes
    # the sign row but preserves the cancellation.
    swapped = tuple((row[0], row[2], row[1], row[3]) for row in rows)
    assert subset_permanent(swapped) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP permanent with arbitrary row and source scalings",
                "residual_two_channel_permanent": str(residual),
                "all_kernel_diagonal": str(diagonal),
                "within_block_source_swap_checked": True,
                "homogeneous_merge_weights_checked": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
