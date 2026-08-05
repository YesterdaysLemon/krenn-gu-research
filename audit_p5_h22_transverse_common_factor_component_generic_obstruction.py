#!/usr/bin/env python3
"""Independent subset-DP audit of the twelfth component's H22 obstruction."""

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
    r, k = sp.symbols("r k")
    lam, mu = sp.symbols("lambda mu")
    t0, t1, t2, t3 = sp.symbols("t0:4")
    x0, x1, x2, x3 = sp.symbols("x0:4")
    c0, c1, c2, c3 = sp.symbols("c0:4")

    # Independent reconstruction with arbitrary rescaling of all four kernel
    # rows.  The merged entries of rows zero and three are retained even
    # though the saturated cut makes them irrelevant.
    rows = (
        (
            -c0 * lam * t0 * (k - 1) * (r + 2),
            -c0 * t2,
            c0 * k * t3,
            x0,
        ),
        (c1 * (lam * t0 + mu * t1), 0, 0, x1),
        (c2 * (lam * t0 + mu * t1), 0, 0, x2),
        (
            c3 * mu * t1 * (r + 2) * (k + 1),
            c3 * t2,
            c3 * k * t3,
            x3,
        ),
    )
    residual = sp.factor(rows[0][1] * rows[3][2] + rows[0][2] * rows[3][1])
    diagonal = subset_permanent(rows)
    assert residual == 0
    assert diagonal == 0

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
