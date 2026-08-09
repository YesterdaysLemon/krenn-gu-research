#!/usr/bin/env python3
"""Exact third-row compatibility obstruction on the two q*phi=-1 axes."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp

ROOT = HERE
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_COMPATIBILITY_OBSTRUCTION_CANDIDATE.md"
CERTIFICATE = ROOT / "p5_h22_component19_p0_qphi_minus_one_axes_compatibility_certificate.json"
SOURCE = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
FRAME_REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md"
H22_THEORY = ROOT / "P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md"

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED4 = WORDS4[1:-1]
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"), cwd=ROOT, text=True,
        capture_output=True, check=True, timeout=15,
    ).stdout.strip()


def add(*rows):
    return tuple(sp.factor(sum(row[i] for row in rows)) for i in range(len(rows[0])))


def scale(coefficient, row):
    return tuple(sp.factor(coefficient * value) for value in row)


def permanent(rows):
    """Subset-DP permanent over characteristic zero."""
    states = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not (mask >> column) & 1:
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = {mask: sp.expand(value) for mask, value in following.items()}
    return sp.factor(states[(1 << len(rows)) - 1])


def assert_zero(value):
    if isinstance(value, sp.MatrixBase):
        assert all(sp.cancel(entry) == 0 for entry in value)
    else:
        assert sp.cancel(value) == 0


def component_rows(q, phi, t):
    cap_a = (1, 1, 0, 0)
    abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    bbar = (0, 0, 1, -1)
    alpha = (abar, cap_b, bbar, abar)
    unmarked_beta = (
        add(bbar, scale(q, cap_b)),
        cap_a,
        cap_a,
        add(cap_b, scale(phi, bbar)),
    )
    beta = tuple(
        add(unmarked_beta[i], scale((0, 0, t, 0)[i], alpha[i]))
        for i in range(4)
    )
    return alpha, beta


def full_coefficient(alpha5, beta5, contraction, word):
    return permanent(tuple(
        beta5[i] if word[i] else alpha5[i] for i in range(4)
    ) + (contraction,))


def mixed_matrix(alpha4, beta4, contraction, extension_variables):
    alpha5 = tuple(tuple(alpha4[i]) + (extension_variables[i],) for i in range(4))
    beta5 = tuple(tuple(beta4[i]) + (extension_variables[4 + i],) for i in range(4))
    return sp.Matrix([
        [sp.diff(full_coefficient(alpha5, beta5, contraction, word), variable)
         for variable in extension_variables]
        for word in MIXED4
    ])


def one_marked(alpha5, beta5, mode, contraction):
    basis = tuple(
        tuple(int(i == j) for j in range(5)) for i in range(5)
    )
    rows = []
    for word in WORDS3:
        selected = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta5[other] if word[bit] else alpha5[other])
                bit += 1
        rows.append([
            permanent(tuple(
                basis[column] if other == mode else selected[other]
                for other in range(4)
            ) + (contraction,))
            for column in range(5)
        ])
    return sp.Matrix(rows)


def axis_certificate(axis, alpha4, beta4, extension, phi, t, coordinate):
    contraction01 = (1, 1, 0, 0, 0)
    contraction23 = (0, 0, 1, 1, 0)
    alpha5 = tuple(
        tuple(alpha4[i]) + (sp.factor(extension[i]),) for i in range(4)
    )
    beta5 = tuple(
        tuple(beta4[i]) + (sp.factor(extension[4 + i]),) for i in range(4)
    )

    # These are the actual linear reconstruction equations for the missing
    # target-colour row gamma_mode, not projected-rank surrogates.
    selected_mode = 0 if axis == "X=Y=0" else 3
    map01 = one_marked(alpha5, beta5, selected_mode, contraction01)
    map23 = one_marked(alpha5, beta5, selected_mode, contraction23)
    stacked = map01.col_join(map23)
    if axis == "X=Y=0":
        rows = (3, 5, 7, 8, 11)
    else:
        rows = (5, 6, 7, 8, 13)
    determinant = sp.factor(stacked.extract(rows, range(5)).det())
    expected = (
        256 * coordinate ** 4 * phi ** 4 * t
        * (phi - 1) * (phi + 1) / (phi ** 2 + 1) ** 3
    )
    assert_zero(determinant - expected)
    assert stacked.rank() == 5
    assert stacked.nullspace() == []

    # The binary mixed equations and diagonal open are reconstructed directly.
    mixed = {
        "D01": [
            sp.factor(full_coefficient(alpha5, beta5, contraction01, word))
            for word in MIXED4
        ],
        "D23": [
            sp.factor(full_coefficient(alpha5, beta5, contraction23, word))
            for word in MIXED4
        ],
    }
    assert all(value == 0 for values in mixed.values() for value in values)
    diagonals = {
        "A01": sp.factor(full_coefficient(alpha5, beta5, contraction01, WORDS4[0])),
        "B01": sp.factor(full_coefficient(alpha5, beta5, contraction01, WORDS4[-1])),
        "A23": sp.factor(full_coefficient(alpha5, beta5, contraction23, WORDS4[0])),
        "B23": sp.factor(full_coefficient(alpha5, beta5, contraction23, WORDS4[-1])),
    }
    if axis == "X=Y=0":
        wanted = {
            "A01": sp.Integer(0),
            "B01": -4 * t * coordinate,
            "A23": -4 * coordinate / (-1 / phi - phi),
            "B23": -4 * coordinate / phi,
        }
    else:
        wanted = {
            "A01": sp.Integer(0),
            "B01": -4 * phi * t * coordinate,
            "A23": -4 * phi * coordinate / (-1 / phi - phi),
            "B23": 4 * coordinate,
        }
    for key in wanted:
        assert_zero(diagonals[key] - wanted[key])

    # In normalized H22 coordinates alpha=E1, beta=E2, gamma=E0.
    # The D01 gamma^4 coefficient is lambda0 and must be nonzero.  Injectivity
    # of the shared one-gamma equations forces gamma_selected_mode=0, making
    # that diagonal zero before any two-gamma equation is considered.
    return {
        "axis": axis,
        "open": f"{coordinate}*t!=0 and phi*(phi^2-1)*(phi^2+1)!=0",
        "selected_third_row_mode": selected_mode,
        "contraction_rows": {
            "D01": list(contraction01),
            "D23": list(contraction23),
        },
        "binary_diagonals": {key: str(value) for key, value in diagonals.items()},
        "stacked_shape": [16, 5],
        "stacked_rows": list(rows),
        "stacked_determinant": str(determinant),
        "stacked_rank": 5,
        "third_row_kernel": [],
        "deduction": (
            f"gamma_{selected_mode}=0, so the required nonzero D01 gamma^4 "
            "diagonal vanishes"
        ),
        "actual_ternary_lift_exists": False,
    }


def main():
    phi, t, cap_x, cap_z = sp.symbols("phi t X Z", nonzero=True)
    q = -1 / phi
    r = q - phi
    alpha4, beta4 = component_rows(q, phi, t)
    extension_variables = sp.symbols("e0:8")
    contraction01 = (1, 1, 0, 0, 0)
    contraction23 = (0, 0, 1, 1, 0)
    combined = mixed_matrix(
        alpha4, beta4, contraction01, extension_variables
    ).col_join(mixed_matrix(
        alpha4, beta4, contraction23, extension_variables
    ))
    complete_rows = (2, 9, 10, 12, 15)
    complete_columns = (0, 1, 2, 3, 6)
    complete_minor = sp.factor(
        combined.extract(complete_rows, complete_columns).det()
    )
    expected_complete = 1024 * (phi ** 2 + 1) ** 2 / phi ** 3
    assert_zero(complete_minor - expected_complete)
    assert combined.rank() == 5

    vector_x = sp.Matrix((0, -1 / r, phi / r, 0, 1, 0, 0, 0))
    vector_y = sp.Matrix((0, 0, 0, 0, 0, 1, 0, 0))
    vector_z = sp.Matrix((0, -q / r, 1 / r, 0, 0, 0, 0, 1))
    for vector in (vector_x, vector_y, vector_z):
        assert_zero(combined * vector)
    assert sp.Matrix.hstack(vector_x, vector_y, vector_z).rank() == 3

    axes = (
        axis_certificate(
            "X=Y=0", alpha4, beta4, cap_z * vector_z,
            phi, t, cap_z,
        ),
        axis_certificate(
            "Z=Y=0", alpha4, beta4, cap_x * vector_x,
            phi, t, cap_x,
        ),
    )
    result = {
        "status": "pass",
        "role": "construction",
        "date_utc": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "CANDIDATE",
        "scope": "actual ternary weighted-H22 reconstruction on the two p=0, q*phi=-1, Y=0 residual axes",
        "inputs": {
            SOURCE.name: sha256(SOURCE),
            FRAME_REPORT.name: sha256(FRAME_REPORT),
            H22_THEORY.name: sha256(H22_THEORY),
        },
        "method": "direct source reconstruction, complete shared extension frame, and fixed full two-contraction third-row stack determinants",
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
            CERTIFICATE.name: sha256(CERTIFICATE),
        },
        "parameter_relation": "p=0, q=-1/phi",
        "parameter_open": "phi*(phi^2-1)*(phi^2+1)!=0",
        "shared_frame": {
            "mixed_rank": 5,
            "rank_witness": {
                "rows": list(complete_rows),
                "columns": list(complete_columns),
                "determinant": str(complete_minor),
            },
            "basis": [
                [str(sp.factor(value)) for value in vector]
                for vector in (vector_x, vector_y, vector_z)
            ],
        },
        "target_colour_identification": {
            "alpha": "E1",
            "beta": "E2",
            "missing_third_row_gamma": "E0",
            "required_D01_gamma_diagonal": "lambda0!=0",
        },
        "axes": list(axes),
        "higher_compatibility_obstruction": True,
        "actual_weighted_H22_lift_exists": False,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "limitations": [
            "Construction result remains CANDIDATE pending independent verification.",
            "Only the two verified Y=0 residual axes on q*phi=-1 are covered.",
            "The excluded phi^2=1 and phi^2=-1 fibres, other component boundaries, arbitrary-order reduction, and the global conjecture are not addressed.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
