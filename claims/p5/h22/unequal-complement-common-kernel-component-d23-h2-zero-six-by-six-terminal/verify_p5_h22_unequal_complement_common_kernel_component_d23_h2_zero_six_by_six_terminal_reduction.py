#!/usr/bin/env python3
"""Verify component 22's exact sparse 8x8-to-6x6 terminal reduction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / (
    "P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2_ZERO_"
    "SIX_BY_SIX_TERMINAL_REDUCTION.md"
)
PIVOT_ROWS = (1, 5)
PIVOT_COLUMNS = (3, 6)
FULL_ROWS = (1, 2, 3, 5, 6, 7, 10, 12)
COMPLEMENT_ROWS = (2, 3, 6, 7, 10, 12)
COMPLEMENT_COLUMNS = (0, 1, 2, 4, 5, 7)


def exact_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.cancel(left - right) == 0


def main() -> None:
    base = V.mixed_matrix.subs(
        {V.h1: -1 / (2 * V.A), V.h2: 0}, simultaneous=True
    )
    pivot = base.extract(PIVOT_ROWS, PIVOT_COLUMNS)

    for row in PIVOT_ROWS:
        assert all(
            sp.cancel(base[row, column]) == 0
            for column in range(8)
            if column not in PIVOT_COLUMNS
        )

    expected = sp.Matrix(
        (
            (V.f8 + 2 * V.A * V.f6, V.f8),
            (-V.f8 / (2 * V.A), -V.f8 / (2 * V.A)),
        )
    )
    for actual, target in zip(pivot, expected, strict=True):
        exact_equal(actual, target)
    exact_equal(pivot.det(), -V.f6 * V.f8)

    assert tuple(row for row in FULL_ROWS if row not in PIVOT_ROWS) == COMPLEMENT_ROWS
    assert tuple(column for column in range(8) if column not in PIVOT_COLUMNS) == COMPLEMENT_COLUMNS
    zero_based_shuffle_parity = (
        sum(FULL_ROWS.index(row) for row in PIVOT_ROWS) + sum(PIVOT_COLUMNS)
    ) % 2
    assert zero_based_shuffle_parity == 0

    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero structural reduction",
        "This is a reduction, not a closure theorem",
        "remain **UNRESOLVED**",
        "No finite field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "exact characteristic zero",
                "component": 22,
                "slice": "H=0, h2=0",
                "pivot_rows": PIVOT_ROWS,
                "pivot_columns": PIVOT_COLUMNS,
                "pivot_determinant": "-f6*f8",
                "complement_rows": COMPLEMENT_ROWS,
                "complement_columns": COMPLEMENT_COLUMNS,
                "laplace_sign": 1,
                "terminal_residue_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
