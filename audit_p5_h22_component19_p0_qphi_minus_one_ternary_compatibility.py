#!/usr/bin/env python3
"""Independent exact compatibility audit on the q*phi=-1 p=0 survivors.

This script starts from the regular p=0 component rows and reconstructs the
two Y=0 extension axes directly.  It does not import a construction program.
For each local mode it builds the two full 8 x 5 one-marked maps belonging to
the D01 and D23 contraction rows and tests their common row-space rank.
"""

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
SOURCE = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
PRIOR_AUDIT = ROOT / "audit_p5_h22_component19_p0_qphi_minus_one_axes.py"
PRIOR_REPORT = ROOT / "P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md"
REPORT = (
    ROOT
    / "P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md"
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit():
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def permanent(rows):
    """Permanent by squarefree subset dynamic programming."""

    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if not mask & bit:
                    new_mask = mask | bit
                    next_states[new_mask] = (
                        next_states.get(new_mask, 0) + coefficient * entry
                    )
        states = {
            mask: sp.expand(value) for mask, value in next_states.items()
        }
    return sp.expand(states[(1 << len(rows)) - 1])


def complementary_permanent(rows, omitted_column):
    retained = tuple(
        column for column in range(len(rows) + 1) if column != omitted_column
    )
    return permanent(
        tuple(tuple(row[column] for column in retained) for row in rows)
    )


def full_one_marked(alpha5, beta5, mode, contraction):
    """The full 8 x 5 coefficient map before either source contraction."""

    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for word in WORDS3:
        selected = tuple(
            beta5[index] if word[position] else alpha5[index]
            for position, index in enumerate(other)
        ) + (contraction,)
        rows.append(
            tuple(
                complementary_permanent(selected, column)
                for column in range(5)
            )
        )
    return sp.Matrix(rows)


def projected_one_marked(alpha5, beta5, mode, projection):
    alpha4 = tuple(
        tuple((projection * sp.Matrix(row))[i] for i in range(4))
        for row in alpha5
    )
    beta4 = tuple(
        tuple((projection * sp.Matrix(row))[i] for i in range(4))
        for row in beta5
    )
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for word in WORDS3:
        selected = tuple(
            beta4[index] if word[position] else alpha4[index]
            for position, index in enumerate(other)
        )
        rows.append(
            tuple(
                complementary_permanent(selected, column)
                for column in range(4)
            )
        )
    return sp.Matrix(rows)


def projected_coefficients(alpha5, beta5, projection):
    alpha4 = tuple(tuple(projection * sp.Matrix(row)) for row in alpha5)
    beta4 = tuple(tuple(projection * sp.Matrix(row)) for row in beta5)
    return {
        word: sp.factor(
            permanent(
                tuple(
                    beta4[mode] if word[mode] else alpha4[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS4
    }


def regular_p0_rows(phi, t, extension):
    q = -1 / phi
    cap_a = (1, 1, 0, 0)
    cap_abar = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_bbar = (0, 0, 1, -1)
    alpha4 = (cap_abar, cap_b, cap_bbar, cap_abar)
    beta4 = (
        tuple(cap_bbar[j] + q * cap_b[j] for j in range(4)),
        cap_a,
        tuple(cap_a[j] + t * cap_bbar[j] for j in range(4)),
        tuple(cap_b[j] + phi * cap_bbar[j] for j in range(4)),
    )
    alpha5 = tuple(alpha4[mode] + (extension[mode],) for mode in range(4))
    beta5 = tuple(beta4[mode] + (extension[4 + mode],) for mode in range(4))
    return alpha5, beta5


def audit_axis(axis):
    phi, t, coordinate = sp.symbols("phi t C", nonzero=True)
    denominator = phi**2 + 1
    if axis == "X_zero":
        extension = sp.Matrix(
            (0, -coordinate / denominator, -coordinate * phi / denominator, 0,
             0, 0, 0, coordinate)
        )
    elif axis == "Z_zero":
        extension = sp.Matrix(
            (0, coordinate * phi / denominator,
             -coordinate * phi**2 / denominator, 0,
             coordinate, 0, 0, 0)
        )
    else:
        raise ValueError(axis)

    alpha5, beta5 = regular_p0_rows(phi, t, extension)
    q01 = (1, 1, 0, 0, 0)
    q23 = (0, 0, 1, 1, 0)
    projection01 = sp.Matrix(
        ((1, 1, 0, 0, 0), (0, 0, 1, 0, 0),
         (0, 0, 0, 1, 0), (0, 0, 0, 0, 1))
    )
    projection23 = sp.Matrix(
        ((1, 0, 0, 0, 0), (0, 1, 0, 0, 0),
         (0, 0, 1, 1, 0), (0, 0, 0, 0, 1))
    )

    coefficients01 = projected_coefficients(alpha5, beta5, projection01)
    coefficients23 = projected_coefficients(alpha5, beta5, projection23)
    mixed_words = WORDS4[1:-1]
    assert all(coefficients01[word] == 0 for word in mixed_words)
    assert all(coefficients23[word] == 0 for word in mixed_words)
    diagonals = (
        coefficients01[WORDS4[0]],
        coefficients01[WORDS4[-1]],
        coefficients23[WORDS4[0]],
        coefficients23[WORDS4[-1]],
    )
    if axis == "X_zero":
        expected_diagonals = (
            0,
            -4 * coordinate * t,
            4 * coordinate * phi / denominator,
            -4 * coordinate / phi,
        )
    else:
        expected_diagonals = (
            0,
            -4 * coordinate * phi * t,
            4 * coordinate * phi**2 / denominator,
            4 * coordinate,
        )
    assert all(
        sp.cancel(actual - expected) == 0
        for actual, expected in zip(diagonals, expected_diagonals)
    )

    if axis == "X_zero":
        witness_specs = {
            0: (
                (3, 5, 7, 8, 11),
                (0, 1, 2, 3, 4),
                256
                * coordinate**4
                * phi**4
                * t
                * (phi - 1)
                * (phi + 1)
                / denominator**3,
            ),
            1: (
                (7, 8, 9, 15),
                (0, 1, 2, 3),
                64 * coordinate**4 * phi / denominator**2,
            ),
            2: (
                (7, 8, 9, 15),
                (0, 1, 2, 3),
                -64 * coordinate**4 * phi / denominator**2,
            ),
            3: (
                (4, 5, 7, 8),
                (0, 1, 2, 4),
                128
                * coordinate**3
                * t
                * (phi + 1)
                / denominator**3,
            ),
        }
        expected_stack_ranks = (5, 4, 4, 4)
    else:
        witness_specs = {
            0: (
                (1, 3, 7, 8),
                (0, 1, 2, 4),
                128
                * coordinate**3
                * phi**6
                * t
                * (phi - 1)
                / denominator**3,
            ),
            1: (
                (7, 8, 9, 15),
                (0, 1, 2, 3),
                -64 * coordinate**4 * phi**5 / denominator**2,
            ),
            2: (
                (7, 8, 9, 15),
                (0, 1, 2, 3),
                -64 * coordinate**4 * phi**3 / denominator**2,
            ),
            3: (
                (5, 6, 7, 8, 13),
                (0, 1, 2, 3, 4),
                256
                * coordinate**4
                * phi**4
                * t
                * (phi - 1)
                * (phi + 1)
                / denominator**3,
            ),
        }
        expected_stack_ranks = (4, 4, 4, 5)

    records = []
    for mode in range(4):
        full01 = full_one_marked(alpha5, beta5, mode, q01)
        full23 = full_one_marked(alpha5, beta5, mode, q23)
        projected01 = projected_one_marked(alpha5, beta5, mode, projection01)
        projected23 = projected_one_marked(alpha5, beta5, mode, projection23)
        # Laplace expansion along the contraction row gives these identities.
        assert all(sp.cancel(value) == 0 for value in full01 - projected01 * projection01)
        assert all(sp.cancel(value) == 0 for value in full23 - projected23 * projection23)
        stack = full01.col_join(full23)
        rank01 = full01.rank()
        rank23 = full23.rank()
        stack_rank = stack.rank()
        assert (rank01, rank23) == (
            (3, 3) if mode in (0, 3) else ((1, 3) if mode in (1, 2) else None)
        )
        assert stack_rank == expected_stack_ranks[mode]
        rows, columns, expected = witness_specs[mode]
        witness = sp.factor(stack.extract(rows, columns).det())
        assert sp.cancel(witness - expected) == 0
        records.append(
            {
                "mode": mode,
                "individual_ranks": {"D01": rank01, "D23": rank23},
                "stack_rank": stack_rank,
                "witness_rows": list(rows),
                "witness_columns": list(columns),
                "witness_determinant": str(witness),
            }
        )
    return {
        "axis": axis,
        "extension": [str(value) for value in extension],
        "diagonals_A01_B01_A23_B23": [str(value) for value in diagonals],
        "required_nonzero_diagonals": "B01*A23*B23!=0",
        "open": "C*t*phi*(phi^2-1)*(phi^2+1)!=0",
        "modes": records,
        "common_three_column_factorization_exists": False,
    }


def main():
    axes = [audit_axis(axis) for axis in ("X_zero", "Z_zero")]
    script = Path(__file__).resolve()
    inputs = {
        path.name: sha256(path) for path in (SOURCE, PRIOR_AUDIT, PRIOR_REPORT)
    }
    outputs = {script.name: sha256(script)}
    if REPORT.exists():
        outputs[REPORT.name] = sha256(REPORT)
    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "component 19 p=0, q=-1/phi, lambda=1, h=(0,0,t,0), "
            "Y=0 survivor axes X=0 and Z=0 on "
            "C*t*phi*(phi^2-1)*(phi^2+1)!=0"
        ),
        "inputs": inputs,
        "method": (
            "fresh regular-basis reconstruction, subset-DP permanents, "
            "full 8x5 complementary-cofactor maps, exact projection "
            "identities, and fixed two-slice Fitting minors"
        ),
        "command": (
            "uv run --with sympy python "
            "audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py"
        ),
        "outputs": outputs,
        "limitations": (
            "finite ordinary q=-1/phi chart only; excludes phi=0, "
            "phi^2=1, phi^2=-1, t=0, and zero extension; no projective "
            "weight boundary, other component, arbitrary-order, or global claim"
        ),
        "factorization_equations": (
            "N_D01,i=U_D01,i*R_i and N_D23,i=U_D23,i*R_i with one "
            "shared R_i in Mat(3,5), equivalently rank([N_D01,i;N_D23,i])<=3"
        ),
        "axes": axes,
        "all_eight_individual_rank_conditions_hold": True,
        "all_eight_individual_maps_pair_compatibly": False,
        "normalized_weighted_H22_lift_exists_on_either_survivor": False,
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
