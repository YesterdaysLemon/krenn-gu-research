#!/usr/bin/env python3
"""Verify exclusion of the rank-two-M single-gate H31 branch."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT
THEOREM = HERE / "P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md"
REDUCTION = (
    REPO_ROOT / "claims" / "p5" / "h31" / "single-gate-p3"
    / "P5_H31_SINGLE_GATE_P3_REDUCTION.md"
)
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(
                rows[row][permutation[row]]
                for row in range(size)
            )
            for permutation in itertools.permutations(range(size))
        )
    )


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    output = []
    for bits in BITS3:
        selected: list[tuple[sp.Expr, ...] | None] = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if bits[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                sp.Integer(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis
                        if other == mode
                        else selected[other]  # type: ignore[arg-type]
                        for other in range(4)
                    )
                )
            )
        output.append(coefficient_row)
    return sp.Matrix(output)


def binary_extension_system(
    A: sp.Expr,
    B: sp.Expr,
    v0: sp.Expr,
    v1: sp.Expr,
    v2: sp.Expr,
    variables: tuple[sp.Symbol, ...],
) -> tuple[sp.Matrix, sp.Matrix]:
    t, x1, x2, x3, y1, y2, y3 = variables
    alpha = (
        (0, 0, 0, 1),
        (-B, 0, 1, x1),
        (A, 1, 0, x2),
        (A, 1, 0, x3),
    )
    beta = (
        (v0, v1, v2, t),
        (-A, 1, 0, y1),
        (B, 0, 1, y2),
        (0, B, A, y3),
    )
    coefficients = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows = tuple(
            beta[mode] if bits[mode] else alpha[mode]
            for mode in range(4)
        )
        coefficients["".join(map(str, bits))] = permanent(rows)
    contraction = {
        word[1:]: value
        for word, value in coefficients.items()
        if word[0] == "1"
    }
    unwanted = tuple(
        word for word in contraction if word != "111"
    )
    matrix = sp.Matrix(
        [
            [
                sp.diff(contraction[word], variable)
                for variable in variables
            ]
            for word in unwanted
        ]
    )
    desired = sp.Matrix(
        [[
            sp.diff(contraction["111"], variable)
            for variable in variables
        ]]
    )
    return matrix, desired


def main() -> None:
    A = sp.symbols("A", nonzero=True)
    B, v0, v1, v2 = sp.symbols("B v0 v1 v2")
    h, r, k, q = sp.symbols("h r k q")
    t, x1, x2, x3, y1, y2, y3 = sp.symbols(
        "t x1 x2 x3 y1 y2 y3"
    )
    variables = (t, x1, x2, x3, y1, y2, y3)
    matrix, desired = binary_extension_system(
        A,
        B,
        v0,
        v1,
        v2,
        variables,
    )

    alpha = (
        (0, 0, 0, 1),
        (-B, 0, 1, x1),
        (A, 1, 0, x2),
        (A, 1, 0, x3),
    )
    beta = (
        (v0, v1, v2, t),
        (-A, 1, 0, y1),
        (B, 0, 1, y2),
        (0, B, A, y3),
    )
    marked = {
        mode: one_marked_map(mode, alpha, beta)
        for mode in range(4)
    }

    alpha_zero = (
        (0, 0, 0, 0),
        (-B, 0, 1, 0),
        (A, 1, 0, 0),
        (A, 1, 0, 0),
    )
    beta_zero = (
        (v0, v1, v2, 0),
        (-A, 1, 0, 0),
        (B, 0, 1, 0),
        (0, B, A, 0),
    )
    transverse_columns = {
        mode: one_marked_map(
            mode,
            alpha_zero,
            beta_zero,
        )[:, 3]
        for mode in range(4)
    }

    D = v0 - A * v1
    S = v0 + A * v1
    P = v0 - B * v2
    Q = v0 + B * v2
    branch_data = [
        {
            "name": "B0_S_nonzero_v2_nonzero",
            "sub": {
                B: 0,
                t: v2 * h / A,
                x1: -h / A,
                x2: 0,
                x3: 0,
                y1: 0,
                y2: h / A,
                y3: h,
            },
            "mode": 3,
            "rows": (0, 3, 4, 7),
            "minor": 4 * h * D * S,
            "transverse_index": 4,
            "transverse": S,
            "desired": 2 * h * D,
        },
        {
            "name": "B0_S_nonzero_v2_zero",
            "sub": {
                B: 0,
                v2: 0,
                t: r * S**2 / (A * D),
                x1: -h / A,
                x2: -r * S / D,
                x3: -r * S / D,
                y1: r,
                y2: h / A,
                y3: h,
            },
            "mode": 3,
            "rows": (0, 3, 4, 7),
            "minor": 4 * h * D * S,
            "transverse_index": 4,
            "transverse": S,
            "desired": 2 * h * D,
        },
        {
            "name": "B0_S0_v2_nonzero",
            "sub": {
                B: 0,
                v0: -A * v1,
                t: -v2 * k,
                x1: k,
                x2: 0,
                x3: 0,
                y1: 0,
                y2: q,
                y3: h,
            },
            "mode": 1,
            "rows": (0, 1, 4, 7),
            "minor": 8 * A**4 * v1 * v2 * (A * q + h),
            "transverse_index": 4,
            "transverse": 2 * A * v2,
            "desired": -2 * A * v1 * (A * q + h),
        },
        {
            "name": "B0_deep_y1_nonzero",
            "sub": {
                B: 0,
                v0: -A * v1,
                v2: 0,
                t: 0,
                x1: k,
                x2: 0,
                x3: 0,
                y1: r,
                y2: q,
                y3: h,
            },
            "mode": 0,
            "rows": (0, 4, 5, 7),
            "minor": 8 * A**4 * r**2 * (A * q + h),
            "transverse_index": 0,
            "transverse": 2 * A,
            "desired": -2 * A * v1 * (A * q + h),
        },
        {
            "name": "v1_zero_generic",
            "sub": {
                v1: 0,
                t: v2 * h * P / (A * Q),
                x1: -h * P / (A * Q),
                x2: 0,
                x3: 0,
                y1: 0,
                y2: h / A,
                y3: h,
            },
            "mode": 3,
            "rows": (0, 3, 4, 7),
            "minor": 4 * h * v0 * P,
            "transverse_index": 4,
            "transverse": P,
            "desired": 2 * v0 * h,
        },
        {
            "name": "v1_zero_P_zero",
            "sub": {
                v1: 0,
                v0: B * v2,
                t: 0,
                x1: 0,
                x2: k,
                x3: 0,
                y1: 0,
                y2: q,
                y3: h,
            },
            "mode": 1,
            "rows": (0, 1, 4, 7),
            "minor": -8 * A**3 * B * h * v2**2,
            "transverse_index": 4,
            "transverse": 2 * A * v2,
            "desired": 2 * B * v2 * h,
        },
        {
            "name": "v1_v2_zero",
            "sub": {
                v1: 0,
                v2: 0,
                t: -v0 * (A * q - h) / (A * B),
                x1: -q,
                x2: (A * q - h) / B,
                x3: (A * q - h) / B,
                y1: -(A * q - h) / B,
                y2: q,
                y3: h,
            },
            "mode": 3,
            "rows": (0, 3, 4, 7),
            "minor": 4 * h * v0**2,
            "transverse_index": 4,
            "transverse": v0,
            "desired": 2 * v0 * h,
        },
        {
            "name": "v2_zero_generic",
            "sub": {
                v2: 0,
                t: h * S**2 / (A * B * D),
                x1: 0,
                x2: -h * S / (B * D),
                x3: -h * S / (B * D),
                y1: h / B,
                y2: 0,
                y3: h,
            },
            "mode": 3,
            "rows": (0, 3, 4, 7),
            "minor": 4 * h * v0 * S,
            "transverse_index": 4,
            "transverse": S,
            "desired": 2 * v0 * h,
        },
        {
            "name": "v2_zero_S_zero",
            "sub": {
                v2: 0,
                v0: -A * v1,
                t: 0,
                x1: k,
                x2: 0,
                x3: 0,
                y1: r,
                y2: 0,
                y3: h,
            },
            "mode": 2,
            "rows": (0, 3, 5, 7),
            "minor": 8 * A**4 * B * h * v1**2,
            "transverse_index": 5,
            "transverse": -2 * A * B * v1,
            "desired": -2 * A * v1 * h,
        },
        {
            "name": "component_IV",
            "sub": {
                v0: -A * v1 + B * v2,
                t: 0,
                x1: 0,
                x2: 0,
                x3: 0,
                y1: 0,
                y2: 0,
                y3: h,
            },
            "mode": 2,
            "rows": (0, 3, 5, 7),
            "minor": (
                8
                * A**3
                * B
                * h
                * v1
                * (A * v1 - B * v2)
            ),
            "transverse_index": 5,
            "transverse": -2 * A * B * v1,
            "desired": 2 * v0 * h,
        },
    ]

    verified_branches = []
    for branch in branch_data:
        substitutions = branch["sub"]
        candidate = sp.Matrix(
            [substitutions[variable] for variable in variables]
        )
        assert (matrix.subs(substitutions) * candidate).applyfunc(
            sp.factor
        ) == sp.zeros(7, 1), branch["name"]
        assert sp.factor(
            (desired.subs(substitutions) * candidate)[0]
            - sp.sympify(branch["desired"]).subs(substitutions)
        ) == 0, branch["name"]
        mode = int(branch["mode"])
        rows = list(branch["rows"])
        minor = sp.factor(
            marked[mode].subs(substitutions)[rows, :].det()
        )
        assert sp.factor(
            minor - sp.sympify(branch["minor"]).subs(substitutions)
        ) == 0, branch["name"]
        transverse = sp.factor(
            transverse_columns[mode].subs(substitutions)[
                int(branch["transverse_index"])
            ]
        )
        assert sp.factor(
            transverse
            - sp.sympify(branch["transverse"]).subs(substitutions)
        ) == 0, branch["name"]
        verified_branches.append(str(branch["name"]))

    X, U, W, x, u, w = sp.symbols("X U W x u w")
    alpha_s = (
        (0, 0, 0, 0),
        (0, 0, 1, X),
        (A, 1, 0, 0),
        (A, 1, 0, 0),
    )
    beta_s = (
        (-A, 1, 0, 0),
        (-A, 1, 0, 0),
        (0, 0, 1, U),
        (0, 0, A, W),
    )
    alpha_p = (
        (0, 0, 0, 1),
        (0, 0, 1, x),
        (A, 1, 0, 0),
        (A, 1, 0, 0),
    )
    beta_p = (
        (-A, 1, 0, 0),
        (-A, 1, 0, 0),
        (0, 0, 1, u),
        (0, 0, A, w),
    )

    deepest_kernels = {}
    for mode, kernel, expected_minor in (
        (2, sp.Matrix([0, 0, -A, W, w]), -8 * A**6),
        (3, sp.Matrix([0, 0, -1, U, u]), -8 * A**3),
    ):
        marked_s = one_marked_map(mode, alpha_s, beta_s)
        marked_p = one_marked_map(mode, alpha_p, beta_p)
        combined = (
            marked_s[:, :3]
            .row_join(marked_s[:, 3])
            .row_join(sp.zeros(8, 1))
            .col_join(
                marked_p[:, :3]
                .row_join(sp.zeros(8, 1))
                .row_join(marked_p[:, 3])
            )
        )
        assert (combined * kernel).applyfunc(
            sp.factor
        ) == sp.zeros(16, 1)
        witness_minor = sp.factor(
            combined[
                [7, 8, 11, 15],
                [0, 1, 3, 4],
            ].det()
        )
        assert witness_minor == expected_minor
        deepest_kernels[str(mode)] = list(map(str, kernel))

    gamma2_s = (0, 0, -A, W)
    gamma3_s = (0, 0, -1, U)
    mixed = sp.factor(
        permanent(
            (
                beta_s[0],
                beta_s[1],
                gamma2_s,
                gamma3_s,
            )
        )
    )
    assert mixed == 2 * A * (A * U + W)
    beta_diagonal_s = sp.factor(permanent(beta_s))
    assert beta_diagonal_s == -2 * A * (A * U + W)

    output = {
        "verified": True,
        "field": "C",
        "binary_strata_verified": verified_branches,
        "transverse_kernel_cases": len(verified_branches),
        "deepest_combined_kernel_dimensions": {
            "mode_2": 1,
            "mode_3": 1,
        },
        "deepest_kernel_vectors": deepest_kernels,
        "deepest_mixed_coefficient": "2*A*(A*U+W)",
        "rank_two_M_single_gate_H31_lift_possible": False,
        "all_single_gate_H31_excluded": False,
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "dependency": {
            "file": REDUCTION.name,
            "sha256": sha256(REDUCTION),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_single_gate_rank_two_m_exclusion_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
