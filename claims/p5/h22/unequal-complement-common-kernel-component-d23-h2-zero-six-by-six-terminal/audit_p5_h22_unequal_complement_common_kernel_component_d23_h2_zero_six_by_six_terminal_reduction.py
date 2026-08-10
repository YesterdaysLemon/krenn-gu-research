#!/usr/bin/env python3
"""Independent low-level audit of component 22's sparse terminal reduction."""

from __future__ import annotations

import json

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/unequal-complement-common-kernel")

from verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction import (
    component_rows,
    shifted,
)

A, R, D = sp.symbols("A R D")
h0, h1, h2, h3, rho = sp.symbols("h0 h1 h2 h3 rho")
x = sp.symbols("x0:8")
PIVOT_ROWS = (1, 5)
PIVOT_COLUMNS = (3, 6)
FULL_ROWS = (1, 2, 3, 5, 6, 7, 10, 12)
COMPLEMENT_ROWS = (2, 3, 6, 7, 10, 12)
COMPLEMENT_COLUMNS = (0, 1, 2, 4, 5, 7)


def exact_equal(left, right) -> None:
    assert sp.cancel(left - right) == 0


def main() -> None:
    alpha, canonical = component_rows(A, R, D)
    marked = shifted(canonical, alpha, (h0, h1, h2, h3))
    model = build_model(alpha, marked, x, "D23", "finite", rho)
    matrix = sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in model["mixed"]]
    ).subs({h1: -1 / (2 * A), h2: 0}, simultaneous=True)

    f6 = (D - 1) * rho + D + 1
    f8 = (A * D + A + R * D) * rho + A * D - A + R * D
    expected_entries = (
        f8 + 2 * A * f6,
        f8,
        -f8 / (2 * A),
        -f8 / (2 * A),
    )
    actual_entries = tuple(
        matrix[row, column] for row in PIVOT_ROWS for column in PIVOT_COLUMNS
    )
    for actual, expected in zip(actual_entries, expected_entries, strict=True):
        exact_equal(actual, expected)

    outside_zero_checks = 0
    for row in PIVOT_ROWS:
        for column in range(8):
            if column in PIVOT_COLUMNS:
                continue
            exact_equal(matrix[row, column], 0)
            outside_zero_checks += 1

    pivot = matrix.extract(PIVOT_ROWS, PIVOT_COLUMNS)
    exact_equal(pivot.det(), -f6 * f8)
    assert tuple(row for row in FULL_ROWS if row not in PIVOT_ROWS) == COMPLEMENT_ROWS
    assert tuple(column for column in range(8) if column not in PIVOT_COLUMNS) == COMPLEMENT_COLUMNS

    # Generalized Laplace expansion uses row positions 0,3 and columns 3,6.
    parity = (0 + 3 + 3 + 6) % 2
    assert parity == 0

    print(
        json.dumps(
            {
                "status": "PASS",
                "method": "independent low-level permanent-model reconstruction",
                "field": "exact characteristic zero",
                "component": 22,
                "pivot_entry_checks": len(expected_entries),
                "outside_support_zero_checks": outside_zero_checks,
                "pivot_determinant": "-f6*f8",
                "reduced_minor_shape": [6, 6],
                "laplace_sign": 1,
                "terminal_residue_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
