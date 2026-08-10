#!/usr/bin/env python3
"""Independent verifier for the off-wall endpoint compatibility obstruction."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
REPORT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md"
)
CANDIDATE = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_CANDIDATE.md"
)
CONSTRUCTION = (
    ROOT
    / "derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction.py"
)
P4_BOUNDARY = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H31_ENDPOINT = (
    REPO_ROOT / "claims/p5/h31/common-active-binary-triangle/P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md"
)

WORDS4 = tuple(itertools.product((0, 1), repeat=4))
MIXED4 = WORDS4[1:-1]
WORDS3 = tuple(itertools.product((0, 1), repeat=3))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def permanent_subset(rows):
    """Permanent by subset DP, independent of permutation enumeration."""

    size = len(rows)
    assert all(len(row) == size for row in rows)
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
        states = {mask: sp.expand(value) for mask, value in next_states.items()}
    return states[(1 << size) - 1]


def endpoint_planes(axis, cap_t):
    e = (sp.Integer(1), 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, -1, 0)
    v1 = (0, 1, 1, 0)
    v2 = (0, 0, 0, 1)
    alpha = (
        e,
        e,
        tuple(-value for value in u),
        tuple(2 * v2[index] - v1[index] for index in range(4)),
    )
    beta0 = (w, w, e, v1)
    beta = tuple(
        tuple(
            sp.expand(
                beta0[mode][column]
                + (cap_t if mode == axis else 0) * alpha[mode][column]
            )
            for column in range(4)
        )
        for mode in range(4)
    )
    return alpha, beta


def projected(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23_zero":
        return (row[0], row[1], row[3], extension)
    raise ValueError(direction)


def binary_model(axis, cap_t, direction, slope):
    alpha, beta = endpoint_planes(axis, cap_t)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        projected(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_rows = tuple(
        projected(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    coefficients = {}
    for word in WORDS4:
        rows = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        coefficients[word] = permanent_subset(rows)
    mixed = sp.Matrix(
        [
            [coefficients[word].coeff(extension) for extension in extensions]
            for word in MIXED4
        ]
    )
    return {
        "extensions": extensions,
        "alpha": alpha,
        "beta": beta,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "A": coefficients[WORDS4[0]],
        "B": coefficients[WORDS4[-1]],
    }


def complementary_permanent(rows, omitted_column):
    retained = tuple(
        column for column in range(len(rows) + 1) if column != omitted_column
    )
    square = tuple(tuple(row[column] for column in retained) for row in rows)
    return permanent_subset(square)


def one_marked(model, mode):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for word in WORDS3:
        selected = tuple(
            model["beta_rows"][index] if word[position] else model["alpha_rows"][index]
            for position, index in enumerate(other)
        )
        rows.append(
            tuple(complementary_permanent(selected, column) for column in range(4))
        )
    return sp.Matrix(rows)


def full_one_marked(alpha5, beta5, mode, contraction):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for word in WORDS3:
        selected = tuple(
            beta5[index] if word[position] else alpha5[index]
            for position, index in enumerate(other)
        ) + (contraction,)
        rows.append(
            tuple(complementary_permanent(selected, column) for column in range(5))
        )
    return sp.Matrix(rows)


def assert_equal(left, right, label):
    assert sp.factor(left - right) == 0, (label, sp.factor(left), right)


def assert_zero(values, label):
    assert all(sp.factor(value) == 0 for value in values), label


def substitution(model, vector):
    return dict(zip(model["extensions"], vector))


def no_genuine_at_s_zero(axis, cap_t):
    model = binary_model(axis, cap_t, "D01", 0)
    assert model["mixed"].rank() == 1
    kernel = model["mixed"].nullspace()
    assert len(kernel) == 7
    assert all(
        sp.factor(model["A"].subs(substitution(model, vector))) == 0
        for vector in kernel
    )
    return {"mixed_rank": 1, "kernel_dimension": 7, "A_on_complete_kernel": "zero"}


def axis_certificate(axis):
    cap_t, slope, cap_c = sp.symbols("T s C")
    d01 = binary_model(axis, cap_t, "D01", slope)
    d23 = binary_model(axis, cap_t, "D23_zero", 0)
    if axis == 0:
        kernel = sp.Matrix((-1, -1, 0, -2 * cap_t, 2 * cap_t, cap_t, 1, 0))
    else:
        kernel = sp.Matrix((-1, -1, 0, -2 * cap_t, cap_t, 2 * cap_t, 1, 0))
    second = sp.Matrix((0, 0, 1, -1, 1, 1, 0, 1))
    assert_zero(d01["mixed"] * kernel, "D01 generator")
    assert_zero(d23["mixed"] * kernel, "D23 shared generator")
    assert_zero(d23["mixed"] * second, "D23 second generator")

    d01_rows = (3, 4, 5, 7, 9, 12, 13)
    d01_columns = (0, 1, 2, 3, 4, 5, 7)
    witness01 = sp.factor(d01["mixed"].extract(d01_rows, d01_columns).det())
    assert_equal(witness01, -16 * slope**6, "D01 witness")
    d23_rows = (3, 4, 5, 7, 9, 13)
    d23_columns = (0, 1, 2, 3, 4, 5)
    witness23 = sp.factor(d23["mixed"].extract(d23_rows, d23_columns).det())
    assert_equal(witness23, -4, "D23 witness")
    assert d01["mixed"].rank() == 7 and len(d01["mixed"].nullspace()) == 1
    assert d23["mixed"].rank() == 6 and len(d23["mixed"].nullspace()) == 2
    assert sp.Matrix.hstack(kernel, second).rank() == 2
    # Since ker(D01) is the line <kernel> and kernel is in ker(D23), the
    # shared-coordinate intersection is exactly that line.

    shared = cap_c * kernel
    sub01 = substitution(d01, shared)
    sub23 = substitution(d23, shared)
    a01 = sp.factor(d01["A"].subs(sub01))
    b01 = sp.factor(d01["B"].subs(sub01))
    a23 = sp.factor(d23["A"].subs(sub23))
    b23 = sp.factor(d23["B"].subs(sub23))
    assert_equal(a01, -4 * cap_c * slope, "A01")
    assert_equal(b01, 4 * cap_c * (cap_t * slope + 1), "B01")
    assert_equal(a23, 4 * cap_c, "A23")
    assert_equal(b23, 4 * cap_c * cap_t, "B23")

    axis01 = one_marked(d01, axis).subs(sub01)
    axis23 = one_marked(d23, axis).subs(sub23)
    assert axis01.rank() == 3 and axis23.rank() == 3
    transverse = one_marked(d01, 2).subs(sub01)
    transverse_minor = sp.factor(transverse.extract((0, 1, 2, 7), range(4)).det())
    assert_equal(
        transverse_minor,
        -32 * cap_c**3 * slope**2 * (cap_t * slope + 1),
        "transverse minor",
    )

    alpha4, beta4 = endpoint_planes(axis, cap_t)
    alpha5 = tuple(alpha4[mode] + (shared[mode],) for mode in range(4))
    beta5 = tuple(beta4[mode] + (shared[4 + mode],) for mode in range(4))
    q01 = (1, slope, 0, 0, 0)
    q23 = (0, 0, 1, 0, 0)
    stacked = full_one_marked(alpha5, beta5, axis, q01).col_join(
        full_one_marked(alpha5, beta5, axis, q23)
    )
    stack_rows = (0, 6, 7, 8, 14)
    stack_minor = sp.factor(stacked.extract(stack_rows, range(5)).det())
    assert_equal(stack_minor, 64 * cap_c**4 * (cap_t * slope + 1), "stacked minor")

    projective_scale = sp.Symbol("lambda", nonzero=True)
    scaled = substitution(d01, projective_scale * shared)
    scaled_transverse = sp.factor(
        one_marked(d01, 2).subs(scaled).extract((0, 1, 2, 7), range(4)).det()
    )
    assert_equal(scaled_transverse, projective_scale**3 * transverse_minor, "scaling")

    zero_slope = no_genuine_at_s_zero(axis, cap_t)
    pole_model = binary_model(axis, cap_t, "D01", -1 / cap_t)
    assert pole_model["mixed"].rank() == 7
    pole_kernel = pole_model["mixed"].nullspace()
    assert len(pole_kernel) == 1
    assert (
        sp.factor(pole_model["B"].subs(substitution(pole_model, pole_kernel[0]))) == 0
    )

    origin01 = binary_model(axis, 0, "D01", slope)
    origin23 = binary_model(axis, 0, "D23_zero", 0)
    origin_kernel = sp.Matrix((-1, -1, 0, 0, 0, 0, 1, 0))
    origin_second = second
    assert_zero(origin01["mixed"] * origin_kernel, "origin D01")
    assert_zero(origin23["mixed"] * origin_kernel, "origin D23 line")
    assert_zero(origin23["mixed"] * origin_second, "origin D23 plane")
    assert origin01["mixed"].rank() == 7 and origin23["mixed"].rank() == 6
    origin_sub = substitution(origin23, cap_c * origin_kernel)
    assert_equal(origin23["B"].subs(origin_sub), 0, "origin B23")

    return {
        "axis": f"h{axis}",
        "marking": ["T" if mode == axis else "0" for mode in range(4)],
        "D01": {
            "mixed_rank": 7,
            "kernel_generator": [str(value) for value in kernel],
            "rank_witness": str(witness01),
            "A": str(a01),
            "B": str(b01),
        },
        "D23_r_zero": {
            "mixed_rank": 6,
            "kernel_frame": [[str(kernel[row]), str(second[row])] for row in range(8)],
            "rank_witness": str(witness23),
            "A_on_intersection": str(a23),
            "B_on_intersection": str(b23),
        },
        "shared_kernel": [str(value) for value in kernel],
        "shared_intersection_dimension": 1,
        "common_genuine_condition": "C*s*T*(T*s+1)!=0",
        "boundary_attacks": {
            "C=0": "zero extension",
            "s=0": zero_slope,
            "T*s+1=0": "B01 zero on complete kernel",
            "T=0": "B23 zero on complete shared line, including axis intersection",
        },
        "axis_mode_ranks": {"D01": 3, "D23": 3},
        "transverse_mode": 2,
        "transverse_minor_rows": [0, 1, 2, 7],
        "transverse_minor": str(transverse_minor),
        "transverse_rank_on_genuine_open": 4,
        "stacked_rows": list(stack_rows),
        "stacked_minor": str(stack_minor),
        "stacked_rank_on_genuine_open": 5,
        "projective_scaling_checked": True,
    }


def main():
    axes = [axis_certificate(axis) for axis in (0, 1)]
    script = Path(__file__).resolve()
    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": "off-wall gamma=0 endpoint finite-D01 plus finite-D23,r=0 compatibility obstruction on both marking axes and their T=0 intersection",
        "inputs": {
            path.name: sha256(path)
            for path in (P4_BOUNDARY, H31_ENDPOINT, CANDIDATE, CONSTRUCTION)
        },
        "method": "independent subset-DP permanents, complementary-column marked maps, complete mixed kernels, shared-coordinate intersection, fixed transverse and stacked minors",
        "command": 'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py',
        "outputs": {REPORT.name: sha256(REPORT), script.name: sha256(script)},
        "limitations": "VERIFIED only for the frozen gamma=0 finite-D01 plus D23,r=0 pair; no on-wall, other D23 slopes, non-diagonal changes, arbitrary-order gluing, or global claim",
        "imports_construction_or_prior_endpoint_derivation": False,
        "axis_certificates": axes,
        "common_genuineness_condition": "VERIFIED: C*s*T*(T*s+1)!=0",
        "axis_intersection_T_zero": "VERIFIED nongenuine because B23=0 on the complete shared line",
        "transverse_obstruction": "VERIFIED",
        "stacked_compatibility_obstruction": "VERIFIED",
        "frozen_common_ternary_lift_exists": False,
        "failed_or_timeout_branches": [],
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
