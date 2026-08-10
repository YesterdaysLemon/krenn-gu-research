#!/usr/bin/env python3
"""Verify one finite-weight component-21 extension-kernel normal."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_FINITE_WEIGHT_EXTENSION_KERNEL_RATIONAL_NORMAL_OBSTRUCTION.md"
MIXED_ROWS = tuple(range(1, 15)) + tuple(range(17, 31))
MIXED_WITNESS_ROWS = (2, 3, 7, 17, 18, 21, 23)
MIXED_WITNESS_COLUMNS = (0, 1, 2, 3, 5, 7, 12)
AUGMENTED_WITNESS_ROWS = (*MIXED_WITNESS_ROWS, 31)
AUGMENTED_WITNESS_COLUMNS = (0, 1, 2, 3, 4, 5, 7, 12)


def main() -> None:
    p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
    extension = sp.symbols("z0:8")
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )
    leading = sp.Matrix((-2, 0, 0, 0, -3, 0, 1, 0))
    parameters = (p, q, kappa, ell, slope)
    centre = {p: 2, q: 3, kappa: 5, ell: 7, slope: 1}
    specialized = matrix.subs(centre)
    assert specialized * leading == sp.zeros(32, 1)
    assert specialized.rank() == 7

    parameter_columns = sp.Matrix.hstack(
        *(sp.diff(matrix * leading, parameter).subs(centre) for parameter in parameters)
    )
    normal = specialized.row_join(parameter_columns)
    mixed = normal.extract(MIXED_ROWS, range(13))
    assert mixed.rank() == 7
    mixed_minor = mixed.extract(
        tuple(MIXED_ROWS.index(row) for row in MIXED_WITNESS_ROWS),
        MIXED_WITNESS_COLUMNS,
    ).det()
    assert mixed_minor == 5549064192

    kernel = sp.Matrix.hstack(*mixed.nullspace())
    assert kernel.shape == (13, 6)
    diagonal_rows = (0, 15, 16, 31)
    diagonal_map = normal.extract(diagonal_rows, range(13)) * kernel
    assert diagonal_map.rank() == 1
    assert diagonal_map[:3, :] == sp.zeros(3, 6)
    assert diagonal_map[3, :] != sp.zeros(1, 6)

    augmented_minor = normal.extract(
        AUGMENTED_WITNESS_ROWS, AUGMENTED_WITNESS_COLUMNS
    ).det()
    assert augmented_minor == -22196256768

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero rational first-normal theorem",
        "not that locus in general",
        "remain **UNRESOLVED**",
        "No finite-field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "component": 21,
                "point": [2, 3, 5, 7, 1],
                "leading_extension_kernel": [-2, 0, 0, 0, -3, 0, 1, 0],
                "mixed_rank": 7,
                "mixed_kernel_dimension": 6,
                "mixed_minor": int(mixed_minor),
                "diagonal_pattern": [0, 0, 0, "possibly nonzero"],
                "augmented_minor": int(augmented_minor),
                "finite_weight_locus_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
