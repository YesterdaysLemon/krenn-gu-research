#!/usr/bin/env python3
"""Exact verified replay for the generic D01-infinity weighted-H22 obstruction."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

from verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial import (
    build_model,
    marked_matrix,
)

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_OBSTRUCTION.md"
)
PARTIAL = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
HELPER = ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"
B_FULL_AUDIT = (
    ROOT
    / "audit_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_verifier.py"
)
B_DROP_AUDIT = (
    ROOT
    / "audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py"
)
RANK_ROWS = (1, 2, 3, 4, 6, 9)
RANK_COLUMNS = (0, 1, 2, 3, 4, 5)
MINOR_ROWS = (0, 1, 4, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def certificate(chart: str, sheet: str) -> dict[str, object]:
    a, lam, t, cap_x, cap_y = sp.symbols("a lambda t X Y")
    if chart == "B_full":
        shifts = (0, 0, 0, 0)
        vector0 = sp.Matrix(
            (-a - 1, 0, 0, 1 / a, lam / a, (a + 1) / a, 1, 0)
        )
        vector1 = sp.Matrix((0, -1, -1, 0, 1, 0, 0, 1))
    elif sheet == "S1":
        shifts = (0, 0, t, 0)
        vector0 = sp.Matrix(
            (-a - 1, 0, 0, 1 / a, 1 / a, (a + 1) / a, 1, 0)
        )
        vector1 = sp.Matrix(
            (
                0,
                -1,
                -1,
                -t * (2 * a + 1) / a**2,
                -t * (2 * a + 1) / a**2,
                -t * (a + 1) ** 2 / a**2,
                0,
                1,
            )
        )
    else:
        shifts = (0, t, 0, 0)
        vector0 = sp.Matrix(
            (-a - 1, 0, 0, 1 / a, 1 / a, (a + 1) / a, 1, 0)
        )
        vector1 = sp.Matrix(
            (
                -a**2 * t / (a + 1),
                -1,
                -1,
                -t / (a + 1),
                -t / (a + 1),
                a * t / (a + 1),
                0,
                1,
            )
        )

    model = build_model(chart, "01_inf", a, lam, sp.Integer(0), shifts)
    mixed = model["mixed"]
    extensions = model["extensions"]
    diagonal_a = model["diagonal_a"]
    diagonal_b = model["diagonal_b"]
    assert isinstance(mixed, sp.MatrixBase)
    assert isinstance(extensions, tuple)
    assert isinstance(diagonal_a, sp.Expr) and isinstance(diagonal_b, sp.Expr)

    assert all(sp.factor(entry) == 0 for entry in mixed * vector0)
    assert all(sp.factor(entry) == 0 for entry in mixed * vector1)
    assert sp.Matrix.hstack(vector0, vector1).rank() == 2
    rank_witness = sp.factor(mixed.extract(RANK_ROWS, RANK_COLUMNS).det())
    assert_equal(rank_witness, 2 * a**4 * (a + 1) ** 3 * (2 * a + 1))

    vector = cap_x * vector0 + cap_y * vector1
    substitution = dict(zip(extensions, vector))
    first = sp.factor(diagonal_a.subs(substitution))
    second = sp.factor(diagonal_b.subs(substitution))
    assert_equal(first, -2 * cap_y * (2 * a + 1))
    if chart == "B_full":
        expected_second = -2 * (2 * a + 1) * (cap_x * lam + cap_y * a) / a
        expected_ratio = -2 * cap_y * a**2 * lam
    elif sheet == "S1":
        expected_second = (
            2
            * (2 * a + 1)
            * (-cap_x * a + cap_y * t * (a + 1))
            / a**2
        )
        expected_ratio = -2 * cap_y * a**2
    else:
        expected_second = -2 * cap_x * (2 * a + 1) / a
        expected_ratio = -2 * cap_y * a**2
    assert_equal(second, expected_second)

    marked = marked_matrix(model, mode=3).subs(substitution)
    determinant = sp.factor(marked[list(MINOR_ROWS), :].det())
    ratio = sp.factor(sp.cancel(determinant / (first * second)))
    assert_equal(ratio, expected_ratio)

    scale = sp.Symbol("c", nonzero=True)
    scaled = {extension: scale * entry for extension, entry in substitution.items()}
    scaled_first = sp.factor(diagonal_a.subs(scaled))
    scaled_second = sp.factor(diagonal_b.subs(scaled))
    scaled_determinant = sp.factor(
        marked_matrix(model, mode=3).subs(scaled)[list(MINOR_ROWS), :].det()
    )
    assert_equal(scaled_first, scale * first)
    assert_equal(scaled_second, scale * second)
    assert_equal(scaled_determinant, scale**3 * determinant)

    return {
        "chart": chart,
        "marking_fibre": sheet,
        "direction": "D01 infinity",
        "kernel_basis": [
            [str(sp.factor(entry)) for entry in vector0],
            [str(sp.factor(entry)) for entry in vector1],
        ],
        "mixed_rank": 6,
        "kernel_dimension": 2,
        "rank_witness_rows": list(RANK_ROWS),
        "rank_witness_columns": list(RANK_COLUMNS),
        "rank_witness": str(rank_witness),
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "marked_mode": 3,
        "minor_rows": list(MINOR_ROWS),
        "minor_over_diagonal_product": str(ratio),
        "genuineness_forces_Y_nonzero": True,
        "every_genuine_projective_extension_has_marked_rank_four": True,
        "projective_scaling_checked": True,
    }


def main() -> None:
    certificates = [
        certificate("B_full", "origin"),
        certificate("B_drop", "S1"),
        certificate("B_drop", "S2"),
    ]
    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "proof_b",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": "generic D01-infinity weighted-H22 fibres on B_full and B_drop",
        "inputs": {
            PARTIAL.name: sha256(PARTIAL),
            HELPER.name: sha256(HELPER),
            B_FULL_AUDIT.name: sha256(B_FULL_AUDIT),
            B_DROP_AUDIT.name: sha256(B_DROP_AUDIT),
        },
        "method": "complete exact mixed kernels, fixed rank witness, diagonals, and one marked minor",
        "command": "uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_obstruction.py",
        "outputs": {THEOREM.name: sha256(THEOREM)},
        "limitations": "verified generic diagonal-DVR charts only; a=0,-1, projective lower-pair/infinity strata, non-diagonal GL4, local-to-global, and global conjecture open",
        "certificates": certificates,
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "fresh_independent_verifier_complete": True,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
