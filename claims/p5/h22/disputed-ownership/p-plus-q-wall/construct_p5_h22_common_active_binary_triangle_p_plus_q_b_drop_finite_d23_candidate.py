#!/usr/bin/env python3
"""Exact construction certificate for the generic B_drop finite-D23 survivor."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
from verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial import (
    build_model,
    marked_matrix,
)



import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_B_DROP_FINITE_D23_CANDIDATE.md"
)
PARTIAL = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
HELPER = ROOT / "verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py"

a, r, t, cap_x, cap_y = sp.symbols("a r t X Y")
s0 = 2 * a + 1
q0 = 2 * r * s0 - 1
EXTENSIONS = tuple(sp.symbols("z0:8"))
RANK6_ROWS = (1, 2, 3, 4, 6, 9)
RANK6_COLUMNS = (0, 1, 2, 3, 4, 5)
RANK7_SELECTIONS = (
    ((1, 2, 3, 4, 6, 9, 11), (0, 1, 2, 3, 4, 5, 6)),
    ((1, 2, 3, 6, 9, 11, 12), (0, 1, 2, 3, 4, 5, 6)),
    ((1, 3, 4, 6, 9, 10, 11), (0, 1, 2, 3, 4, 5, 6)),
)


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


def assert_zero(entries: sp.MatrixBase) -> None:
    assert all(sp.factor(entry) == 0 for entry in entries)


def sheet_data(sheet: str) -> tuple[tuple[sp.Expr, ...], int]:
    if sheet == "S1":
        return (0, 0, t, 0), 2
    if sheet == "S2":
        return (0, t, 0, 0), 1
    raise ValueError(sheet)


def generic_vector(sheet: str) -> sp.Matrix:
    if sheet == "S1":
        return sp.Matrix(
            (
                t * (a + 1) * s0 * (2 * a * r + 1) / (a * q0),
                -1,
                -1,
                0,
                0,
                -t * (a + 1) * (2 * a * r + 1) / (a * q0),
                t * (2 * a**2 * r - 2 * a - 1) / (a * q0),
                1,
            )
        )
    return sp.Matrix(
        (
            a * t * s0 * (2 * r * (a + 1) + 1) / ((a + 1) * q0),
            -1,
            -1,
            0,
            0,
            t
            * (2 * a**2 * r + 4 * a * r - 2 * a + 2 * r - 1)
            / ((a + 1) * q0),
            -a * t * (2 * r * (a + 1) + 1) / ((a + 1) * q0),
            1,
        )
    )


def generic_certificate(sheet: str) -> dict[str, object]:
    shifts, marked_mode = sheet_data(sheet)
    model = build_model("B_drop", "23", a, sp.Integer(0), r, shifts)
    mixed = model["mixed"]
    assert isinstance(mixed, sp.MatrixBase)
    vector = generic_vector(sheet)
    substitution = dict(zip(model["extensions"], vector))
    assert_zero(mixed * vector)

    first = sp.factor(model["diagonal_a"].subs(substitution))
    second = sp.factor(model["diagonal_b"].subs(substitution))
    assert_equal(first, -2 * s0)
    if sheet == "S1":
        expected_second = -2 * t * s0 * (2 * a * r - 1) * (r * (a + 1) - 1) / (a * q0)
        marked_scale = r * t * (a + 1) * (2 * a * r + 1)
        right_kernel = sp.Matrix(
            (-marked_scale, -a * q0, -a * r * q0, marked_scale)
        )
        three_minor_expected = (
            -4
            * r
            * t**2
            * (a + 1) ** 3
            * s0**2
            * (2 * a * r + 1) ** 2
            * (r * (a + 1) - 1)
            / (a**2 * q0**2)
        )
        genuine_conditions = ("t!=0", "2*a*r-1!=0", "r*(a+1)-1!=0")
    else:
        expected_second = (
            -2
            * t
            * s0
            * (a * r - 1)
            * (2 * r * (a + 1) - 1)
            / ((a + 1) * q0)
        )
        marked_scale = a * r * t * (2 * r * (a + 1) + 1)
        right_kernel = sp.Matrix(
            (
                -marked_scale,
                -(a + 1) * q0,
                -r * (a + 1) * q0,
                marked_scale,
            )
        )
        three_minor_expected = (
            -4
            * a**3
            * r
            * t**2
            * s0**2
            * (a * r - 1)
            * (2 * r * (a + 1) + 1) ** 2
            / ((a + 1) ** 2 * q0**2)
        )
        genuine_conditions = ("t!=0", "a*r-1!=0", "2*r*(a+1)-1!=0")
    assert_equal(second, expected_second)

    expected_minors = (
        -4
        * a**3
        * r
        * (a + 1) ** 3
        * s0
        * (2 * a * r + 1)
        * (2 * r * (a + 1) + 1)
        * q0,
        -4
        * a**3
        * r
        * (a + 1)
        * s0
        * (2 * r * (a + 1) - 1)
        * (2 * r * (a + 1) + 1)
        * q0,
        4
        * a
        * r
        * (a + 1) ** 3
        * s0
        * (2 * a * r - 1)
        * (2 * a * r + 1)
        * q0,
    )
    rank_minors = []
    for selection, expected in zip(RANK7_SELECTIONS, expected_minors):
        determinant = sp.factor(mixed.extract(*selection).det())
        assert_equal(determinant, expected)
        rank_minors.append(str(determinant))
    coefficient_field = sp.QQ.frac_field(a)
    polynomial_minors = [
        sp.Poly(determinant, r, domain=coefficient_field)
        for determinant in expected_minors
    ]
    gcd = sp.gcd(sp.gcd(polynomial_minors[0], polynomial_minors[1]), polynomial_minors[2])
    assert_equal(gcd.monic().as_expr(), r * (r - 1 / (2 * s0)))

    marked = marked_matrix(model, marked_mode).subs(substitution)
    assert_zero(marked * right_kernel)
    three_minor = sp.factor(marked.extract((0, 3, 7), (0, 1, 2)).det())
    assert_equal(three_minor, three_minor_expected)

    return {
        "sheet": sheet,
        "stratum": "r!=0 and Q!=0",
        "Q": str(q0),
        "complete_kernel_basis": [[str(sp.factor(entry)) for entry in vector]],
        "mixed_rank": 7,
        "rank_witness_minor_gcd_over_Q(a)[r]": str(gcd.monic().as_expr()),
        "rank_witness_minors": rank_minors,
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "genuine_extension_conditions": list(genuine_conditions),
        "marked_mode": marked_mode,
        "marked_right_kernel": [str(sp.factor(entry)) for entry in right_kernel],
        "marked_rank_at_most": 3,
        "generic_nonzero_three_minor": str(three_minor),
    }


def zero_slope_certificate(sheet: str) -> dict[str, object]:
    shifts, marked_mode = sheet_data(sheet)
    model = build_model("B_drop", "23", a, sp.Integer(0), sp.Integer(0), shifts)
    mixed = model["mixed"]
    assert isinstance(mixed, sp.MatrixBase)
    vector0 = sp.Matrix((-a - 1, 0, 0, -1 / a, 1 / a, (a + 1) / a, 1, 0))
    if sheet == "S1":
        vector1 = sp.Matrix(
            (
                0,
                -1,
                -1,
                t * s0 / a**2,
                -t * s0 / a**2,
                -t * (a + 1) ** 2 / a**2,
                0,
                1,
            )
        )
    else:
        vector1 = sp.Matrix(
            (
                -a**2 * t / (a + 1),
                -1,
                -1,
                t / (a + 1),
                -t / (a + 1),
                a * t / (a + 1),
                0,
                1,
            )
        )
    assert_zero(mixed * vector0)
    assert_zero(mixed * vector1)
    rank_witness = sp.factor(mixed.extract(RANK6_ROWS, RANK6_COLUMNS).det())
    assert_equal(rank_witness, 2 * a**4 * (a + 1) ** 3 * s0)

    vector = cap_x * vector0 + cap_y * vector1
    substitution = dict(zip(model["extensions"], vector))
    first = sp.factor(model["diagonal_a"].subs(substitution))
    second = sp.factor(model["diagonal_b"].subs(substitution))
    assert_equal(first, -2 * cap_y * s0)
    if sheet == "S1":
        expected_second = -2 * s0 * (-cap_x * a + cap_y * t * (a + 1)) / a**2
        right_kernel = sp.Matrix(
            (-cap_x * a + cap_y * t * s0, cap_y * a**2, 0, 0)
        )
        three_minor_expected = (
            -4
            * cap_y
            * (a + 1) ** 2
            * s0**2
            * (-cap_x * a + cap_y * t * (a + 1))
            / a**2
        )
        witness_substitution = {cap_x: (t * (a + 1) - 1) / a, cap_y: 1}
    else:
        expected_second = 2 * cap_x * s0 / a
        right_kernel = sp.Matrix(
            (-cap_x * (a + 1) + cap_y * a * t, cap_y * a * (a + 1), 0, 0)
        )
        three_minor_expected = 4 * cap_x * cap_y * a * s0**2
        witness_substitution = {cap_x: 1, cap_y: 1}
    assert_equal(second, expected_second)

    marked = marked_matrix(model, marked_mode).subs(substitution)
    assert_zero(marked * right_kernel)
    three_minor = sp.factor(marked.extract((0, 3, 7), (0, 2, 3)).det())
    assert_equal(three_minor, three_minor_expected)
    witness_first = sp.factor(first.subs(witness_substitution))
    witness_second = sp.factor(second.subs(witness_substitution))
    assert witness_first != 0 and witness_second != 0

    return {
        "sheet": sheet,
        "stratum": "r=0",
        "complete_kernel_basis": [
            [str(sp.factor(entry)) for entry in vector0],
            [str(sp.factor(entry)) for entry in vector1],
        ],
        "mixed_rank": 6,
        "rank_witness": str(rank_witness),
        "all_alpha_diagonal": str(first),
        "all_beta_diagonal": str(second),
        "uniform_actuality_witness": {
            "X": str(witness_substitution[cap_x]),
            "Y": str(witness_substitution[cap_y]),
            "A": str(witness_first),
            "B": str(witness_second),
        },
        "every_t_is_actual": True,
        "marked_mode": marked_mode,
        "marked_right_kernel": [str(sp.factor(entry)) for entry in right_kernel],
        "marked_rank": 3,
        "genuine_forces_three_minor_nonzero": str(three_minor),
    }


def exceptional_slope_certificate(sheet: str) -> dict[str, object]:
    shifts, _ = sheet_data(sheet)
    exceptional_r = 1 / (2 * s0)
    model = build_model("B_drop", "23", a, sp.Integer(0), exceptional_r, shifts)
    mixed = model["mixed"]
    assert isinstance(mixed, sp.MatrixBase)
    vector0 = sp.Matrix((-s0, 0, 0, 0, 0, 1, 1, 0))
    assert_zero(mixed * vector0)
    substitution0 = dict(zip(model["extensions"], vector0))
    assert_equal(model["diagonal_a"].subs(substitution0), 0)
    assert_equal(model["diagonal_b"].subs(substitution0), 1)

    rank7_rows = (1, 2, 3, 4, 6, 9, 11)
    rank7_columns = (0, 1, 2, 3, 4, 5, 7)
    rank7_witness = sp.factor(mixed.extract(rank7_rows, rank7_columns).det())
    if sheet == "S1":
        expected_rank7 = (
            -2 * a**2 * t * (a + 1) ** 4 * (3 * a + 1) ** 2 * (3 * a + 2) / s0**3
        )
    else:
        expected_rank7 = (
            -2 * a**4 * t * (a + 1) ** 2 * (3 * a + 1) * (3 * a + 2) ** 2 / s0**3
        )
    assert_equal(rank7_witness, expected_rank7)

    origin_model = build_model(
        "B_drop", "23", a, sp.Integer(0), exceptional_r, (0, 0, 0, 0)
    )
    origin_mixed = origin_model["mixed"]
    vector1 = sp.Matrix((0, -1, -1, 0, 0, 0, 0, 1))
    assert_zero(origin_mixed * vector0)
    assert_zero(origin_mixed * vector1)
    rank6_witness = sp.factor(
        origin_mixed.extract(RANK6_ROWS, RANK6_COLUMNS).det()
    )
    expected_rank6 = (
        2 * a**4 * (a + 1) ** 4 * (3 * a + 1) ** 2 * (3 * a + 2) ** 2 / s0**4
    )
    assert_equal(rank6_witness, expected_rank6)

    vector = cap_x * vector0 + cap_y * vector1
    substitution = dict(zip(origin_model["extensions"], vector))
    first = sp.factor(origin_model["diagonal_a"].subs(substitution))
    second = sp.factor(origin_model["diagonal_b"].subs(substitution))
    assert_equal(first, -2 * cap_y * s0)
    assert_equal(second, cap_x)
    marked_right_kernel = sp.Matrix(
        (-cap_x, 2 * cap_y * s0, cap_y, cap_x * cap_y)
    )
    marked_data = {}
    for marked_mode, expected_minor in (
        (1, cap_x**2 * cap_y * a * (3 * a + 2)),
        (2, cap_x**2 * cap_y * (a + 1) * (3 * a + 1)),
    ):
        marked = marked_matrix(origin_model, marked_mode).subs(substitution)
        assert_zero(marked * marked_right_kernel)
        three_minor = sp.factor(marked.extract((0, 3, 7), (0, 1, 2)).det())
        assert_equal(three_minor, expected_minor)
        marked_data[str(marked_mode)] = {
            "right_kernel": [str(sp.factor(entry)) for entry in marked_right_kernel],
            "generic_nonzero_three_minor": str(three_minor),
            "rank": 3,
        }

    return {
        "sheet": sheet,
        "stratum": "Q=0",
        "slope": str(exceptional_r),
        "t_nonzero": {
            "complete_kernel_basis": [[str(entry) for entry in vector0]],
            "mixed_rank": 7,
            "rank_witness": str(rank7_witness),
            "A": "0",
            "B": "1",
            "genuine_extension_exists": False,
        },
        "t_zero_origin": {
            "complete_kernel_basis": [
                [str(entry) for entry in vector0],
                [str(entry) for entry in vector1],
            ],
            "mixed_rank": 6,
            "rank_witness": str(rank6_witness),
            "A": str(first),
            "B": str(second),
            "genuine_condition": "X*Y!=0",
            "marked_modes": marked_data,
        },
    }


def main() -> None:
    generic = [generic_certificate(sheet) for sheet in ("S1", "S2")]
    zero_slope = [zero_slope_certificate(sheet) for sheet in ("S1", "S2")]
    exceptional = [exceptional_slope_certificate(sheet) for sheet in ("S1", "S2")]
    result = {
        "status": "pass",
        "claim_label": "CANDIDATE",
        "role": "construction",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": "generic B_drop finite-D23 fibres over Q(a) on the p+q=0 diagonal-DVR wall",
        "inputs": {
            PARTIAL.name: sha256(PARTIAL),
            HELPER.name: sha256(HELPER),
        },
        "method": "exact kernel stratification at r=0, r*Q!=0, and Q=0; three targeted rank minors and explicit marked right kernels",
        "command": 'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/construct_p5_h22_common_active_binary_triangle_p_plus_q_b_drop_finite_d23_candidate.py',
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "limitations": "candidate pending independent replay; over Q(a), so direct a-specializations are not classified; D23 alone does not establish a weighted-H22 pair; D01, arbitrary-order gluing, and the global conjecture are outside this claim",
        "marking_axes": {
            "S1": "h=(0,0,t,0)",
            "S2": "h=(0,t,0,0)",
            "actual_locus_equals_both_axes": True,
            "actuality_reason": "the r=0 certificates give a genuine extension for every t",
        },
        "generic_nonexceptional_strata": generic,
        "zero_slope_strata": zero_slope,
        "exceptional_Q_zero_strata": exceptional,
        "finite_field_computation_used": False,
        "broad_brute_force_used": False,
        "independent_verifier_complete": False,
        "weighted_H22_pair_established": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
