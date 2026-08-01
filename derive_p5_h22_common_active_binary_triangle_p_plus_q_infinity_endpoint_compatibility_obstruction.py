#!/usr/bin/env python3
"""Construct an exact compatibility obstruction for the off-wall endpoint pair."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
SOURCE = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_CANDIDATE.md"
REPORT = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_CANDIDATE.md"
INDEPENDENT_REPORT = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md"
INDEPENDENT_VERIFIER = ROOT / "audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py"

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(word for word in WORDS4 if word not in ((0, 0, 0, 0), (1, 1, 1, 1)))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
PERMUTATIONS5 = tuple(itertools.permutations(range(5)))

cap_t, cap_c, slope = sp.symbols("T C s")
extensions = tuple(sp.symbols("z0:8"))


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


def permanent4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def permanent5(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(5))
            for permutation in PERMUTATIONS5
        )
    )


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def assert_zero(entries: sp.MatrixBase) -> None:
    assert all(sp.factor(entry) == 0 for entry in entries)


def endpoint_bases(axis: int) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    e = (sp.Integer(1), 0, 0, 0)
    w = (0, sp.Integer(1), 1, 1)
    u = (0, sp.Integer(1), -1, 0)
    v1 = (0, sp.Integer(1), 1, 0)
    v2 = (0, 0, 0, sp.Integer(1))
    alpha = (
        e,
        e,
        tuple(-entry for entry in u),
        tuple(2 * v2[index] - v1[index] for index in range(4)),
    )
    canonical_beta = (w, w, e, v1)
    beta = tuple(
        tuple(
            canonical_beta[mode][coordinate]
            + (cap_t if mode == axis else 0) * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def project_row(
    row: tuple[sp.Expr, ...], extension: sp.Expr, direction: str
) -> tuple[sp.Expr, ...]:
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23_zero":
        return (row[0], row[1], row[3], extension)
    raise ValueError(direction)


def binary_model(axis: int, direction: str) -> dict[str, object]:
    alpha, beta = endpoint_bases(axis)
    projected_alpha = tuple(
        project_row(alpha[mode], extensions[mode], direction) for mode in range(4)
    )
    projected_beta = tuple(
        project_row(beta[mode], extensions[4 + mode], direction) for mode in range(4)
    )
    coefficients = {
        word: permanent4(
            tuple(
                projected_beta[mode] if word[mode] else projected_alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS4
    }
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], extension) for extension in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "alpha": alpha,
        "beta": beta,
        "projected_alpha": projected_alpha,
        "projected_beta": projected_beta,
        "coefficients": coefficients,
        "mixed": mixed,
    }


def one_marked(model: dict[str, object], mode: int) -> sp.Matrix:
    alpha = model["projected_alpha"]
    beta = model["projected_beta"]
    assert isinstance(alpha, tuple) and isinstance(beta, tuple)
    rows = []
    for word in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if word[bit_index] else alpha[other])
                bit_index += 1
        rows.append(
            [
                permanent4(
                    tuple(
                        tuple(int(coordinate == column) for coordinate in range(4))
                        if other == mode
                        else selected[other]
                        for other in range(4)
                    )
                )
                for column in range(4)
            ]
        )
    return sp.Matrix(rows)


def full_one_marked(
    mode: int,
    contraction: tuple[sp.Expr, ...],
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    source_basis = tuple(
        tuple(int(left == right) for right in range(5)) for left in range(5)
    )
    rows = []
    for word in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if word[bit_index] else alpha[other])
                bit_index += 1
        rows.append(
            [
                permanent5(
                    tuple(
                        source_basis[column] if other == mode else selected[other]
                        for other in range(4)
                    )
                    + (contraction,)
                )
                for column in range(5)
            ]
        )
    return sp.Matrix(rows)


def axis_certificate(axis: int) -> dict[str, object]:
    d01 = binary_model(axis, "D01")
    d23 = binary_model(axis, "D23_zero")
    d01_mixed = d01["mixed"]
    d23_mixed = d23["mixed"]
    assert isinstance(d01_mixed, sp.MatrixBase) and isinstance(d23_mixed, sp.MatrixBase)

    beta_extensions = (2 * cap_t, cap_t, 1, 0) if axis == 0 else (cap_t, 2 * cap_t, 1, 0)
    kernel = sp.Matrix((-1, -1, 0, -2 * cap_t, *beta_extensions))
    second_d23 = sp.Matrix((0, 0, 1, -1, 1, 1, 0, 1))
    assert_zero(d01_mixed * kernel)
    assert_zero(d23_mixed * kernel)
    assert_zero(d23_mixed * second_d23)

    d01_rank_rows = (3, 4, 5, 7, 9, 12, 13)
    d01_rank_columns = (0, 1, 2, 3, 4, 5, 7)
    d01_rank_witness = sp.factor(
        d01_mixed.extract(d01_rank_rows, d01_rank_columns).det()
    )
    assert_equal(d01_rank_witness, -16 * slope**6)
    d23_rank_rows = (3, 4, 5, 7, 9, 13)
    d23_rank_columns = (0, 1, 2, 3, 4, 5)
    d23_rank_witness = sp.factor(
        d23_mixed.extract(d23_rank_rows, d23_rank_columns).det()
    )
    assert_equal(d23_rank_witness, -4)
    assert sp.Matrix.hstack(kernel, second_d23).rank() == 2

    shared = cap_c * kernel
    substitution = dict(zip(extensions, shared))
    d01_coefficients = d01["coefficients"]
    d23_coefficients = d23["coefficients"]
    assert isinstance(d01_coefficients, dict) and isinstance(d23_coefficients, dict)
    d01_a = sp.factor(d01_coefficients[(0, 0, 0, 0)].subs(substitution))
    d01_b = sp.factor(d01_coefficients[(1, 1, 1, 1)].subs(substitution))
    d23_a = sp.factor(d23_coefficients[(0, 0, 0, 0)].subs(substitution))
    d23_b = sp.factor(d23_coefficients[(1, 1, 1, 1)].subs(substitution))
    assert_equal(d01_a, -4 * cap_c * slope)
    assert_equal(d01_b, 4 * cap_c * (cap_t * slope + 1))
    assert_equal(d23_a, 4 * cap_c)
    assert_equal(d23_b, 4 * cap_c * cap_t)

    # The source candidate checked only the axis-mode map.  Mode two supplies
    # a fixed transverse rank-four obstruction on the complete D01 kernel.
    d01_mode_axis = one_marked(d01, axis).subs(substitution)
    d23_mode_axis = one_marked(d23, axis).subs(substitution)
    assert d01_mode_axis.rank() == 3
    assert d23_mode_axis.rank() == 3
    transverse = one_marked(d01, 2).subs(substitution)
    transverse_minor = sp.factor(
        transverse.extract((0, 1, 2, 7), range(4)).det()
    )
    assert_equal(
        transverse_minor,
        -32 * cap_c**3 * slope**2 * (cap_t * slope + 1),
    )

    # Reconstruct the common two-slice map before either weighted projection.
    alpha4, beta4 = endpoint_bases(axis)
    alpha5 = tuple(alpha4[mode] + (shared[mode],) for mode in range(4))
    beta5 = tuple(beta4[mode] + (shared[4 + mode],) for mode in range(4))
    q01 = (1, slope, 0, 0, 0)
    q23 = (0, 0, 1, 0, 0)
    stacked = full_one_marked(axis, q01, alpha5, beta5).col_join(
        full_one_marked(axis, q23, alpha5, beta5)
    )
    stacked_rows = (0, 6, 7, 8, 14)
    stacked_minor = sp.factor(stacked.extract(stacked_rows, range(5)).det())
    assert_equal(stacked_minor, 64 * cap_c**4 * (cap_t * slope + 1))

    scale = sp.Symbol("lambda", nonzero=True)
    scaled_substitution = {
        extension: scale * value for extension, value in substitution.items()
    }
    scaled_minor = sp.factor(
        one_marked(d01, 2)
        .subs(scaled_substitution)
        .extract((0, 1, 2, 7), range(4))
        .det()
    )
    assert_equal(scaled_minor, scale**3 * transverse_minor)

    return {
        "marking_axis": f"h{axis}",
        "marking": ["T" if mode == axis else "0" for mode in range(4)],
        "D01": {
            "complete_kernel_basis": [[str(sp.factor(entry)) for entry in kernel]],
            "mixed_rank": 7,
            "rank_witness": str(d01_rank_witness),
            "A": str(d01_a),
            "B": str(d01_b),
        },
        "D23_at_r_zero": {
            "complete_kernel_basis": [
                [str(sp.factor(entry)) for entry in kernel],
                [str(sp.factor(entry)) for entry in second_d23],
            ],
            "mixed_rank": 6,
            "rank_witness": str(d23_rank_witness),
            "A_on_shared_kernel": str(d23_a),
            "B_on_shared_kernel": str(d23_b),
        },
        "shared_kernel_basis": [[str(sp.factor(entry)) for entry in kernel]],
        "shared_extension_complete": True,
        "common_genuine_condition": "C*s*T*(T*s+1)!=0",
        "axis_mode_individual_ranks": {"D01": 3, "D23": 3},
        "transverse_D01_mode": 2,
        "transverse_minor_rows": [0, 1, 2, 7],
        "transverse_minor": str(transverse_minor),
        "transverse_rank": 4,
        "stacked_mode": axis,
        "stacked_contraction_rows": [list(map(str, q01)), list(map(str, q23))],
        "stacked_minor_rows": list(stacked_rows),
        "stacked_minor": str(stacked_minor),
        "stacked_rank": 5,
        "common_ternary_H22_lift_exists": False,
        "projective_scaling_checked": True,
    }


def main() -> None:
    axes = [axis_certificate(axis) for axis in (0, 1)]
    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "construction",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": "only the off-wall gamma=0 component-14 infinity-endpoint finite-D01 plus finite-D23,r=0 surviving pair on both marking axes",
        "inputs": {
            path.name: sha256(path)
            for path in (SOURCE, INDEPENDENT_REPORT, INDEPENDENT_VERIFIER)
        },
        "method": "independent mixed-kernel reconstruction, shared-extension intersection, fixed transverse minor, and full two-contraction stacked map",
        "command": "uv run --with sympy python derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction.py",
        "outputs": {SCRIPT.name: sha256(SCRIPT), REPORT.name: sha256(REPORT)},
        "limitations": "VERIFIED only after a fresh no-import replay of the displayed off-wall endpoint pair and its mode-swapped axis; no on-wall, other D23 slopes, non-diagonal, arbitrary-order, or global claim",
        "axis_certificates": axes,
        "compatibility_obstruction": "shared extensions force the D01 kernel line; a transverse D01 marked map has rank four and the common two-slice stack has rank five",
        "off_wall_finite_finite_pair_H22_lift_exists": False,
        "independent_verifier_complete": True,
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
