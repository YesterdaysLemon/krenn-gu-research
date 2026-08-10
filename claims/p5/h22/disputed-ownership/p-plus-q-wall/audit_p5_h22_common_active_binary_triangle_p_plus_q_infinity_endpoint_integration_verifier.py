#!/usr/bin/env python3
"""No-import verifier of the off-wall endpoint finite-slope integration."""

from __future__ import annotations

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
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INTEGRATION_VERIFICATION.md"
)
P4_BOUNDARY = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H31_ENDPOINT = (
    ROOT
    / "claims"
    / "p5"
    / "h31"
    / "common-active-binary-triangle"
    / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md"
)
ENDPOINT_AUDIT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INDEPENDENT_VERIFICATION.md"
)
ENDPOINT_AUDIT_SCRIPT = (
    ROOT
    / "audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate_verifier.py"
)
COMPATIBILITY_AUDIT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md"
)
COMPATIBILITY_AUDIT_SCRIPT = (
    ROOT
    / "audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]


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


def permanent(rows):
    """Squarefree subset-DP permanent."""

    size = len(rows)
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if not mask & bit:
                    target = mask | bit
                    updated[target] = updated.get(target, 0) + value * entry
        states = {mask: sp.expand(value) for mask, value in updated.items()}
    return states[(1 << size) - 1]


def planes(axis, cap_t):
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


def contract(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    raise ValueError(direction)


def model(axis, cap_t, direction, slope):
    alpha, beta = planes(axis, cap_t)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_rows = tuple(
        contract(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        rows = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        coefficients[word] = permanent(rows)
    mixed = sp.Matrix(
        [
            [coefficients[word].coeff(extension) for extension in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "extensions": extensions,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def assert_equal(left, right, label):
    assert sp.factor(left - right) == 0, (label, sp.factor(left), right)


def assert_zero(values, label):
    assert all(sp.factor(value) == 0 for value in values), label


def substitute(data, vector):
    return dict(zip(data["extensions"], vector))


def axis_certificate(axis):
    cap_t, slope_s, slope_r, cap_c = sp.symbols("T s r C")
    d01 = model(axis, cap_t, "D01", slope_s)
    d23 = model(axis, cap_t, "D23", slope_r)
    if axis == 0:
        kernel = sp.Matrix((-1, -1, 0, -2 * cap_t, 2 * cap_t, cap_t, 1, 0))
    else:
        kernel = sp.Matrix((-1, -1, 0, -2 * cap_t, cap_t, 2 * cap_t, 1, 0))
    assert_zero(d01["mixed"] * kernel, "D01 kernel")
    rows01 = (3, 4, 5, 7, 9, 12, 13)
    columns01 = (0, 1, 2, 3, 4, 5, 7)
    witness01 = sp.factor(d01["mixed"].extract(rows01, columns01).det())
    assert_equal(witness01, -16 * slope_s**6, "D01 witness")
    assert d01["mixed"].rank() == 7 and len(d01["mixed"].nullspace()) == 1

    compatibility = tuple(sp.factor(value) for value in d23["mixed"] * kernel)
    expected = tuple(sp.Integer(0) for _ in range(13)) + (-12 * cap_t * slope_r,)
    assert compatibility == expected, (axis, compatibility)
    # This proves M23(r)k=0 iff T*r=0 directly: the only equation is the
    # nonzero scalar multiple -12*T*r.

    shared = cap_c * kernel
    sub01 = substitute(d01, shared)
    sub23 = substitute(d23, shared)
    a01 = sp.factor(d01["A"].subs(sub01))
    b01 = sp.factor(d01["B"].subs(sub01))
    a23 = sp.factor(d23["A"].subs(sub23))
    b23 = sp.factor(d23["B"].subs(sub23))
    assert_equal(a01, -4 * cap_c * slope_s, "A01")
    assert_equal(b01, 4 * cap_c * (cap_t * slope_s + 1), "B01")
    assert_equal(a23, 4 * cap_c, "A23")
    assert_equal(b23, 4 * cap_c * cap_t * (2 * slope_r + 1), "B23")

    # Fail-closed D01 slope-zero boundary.
    d01_zero = model(axis, cap_t, "D01", 0)
    assert d01_zero["mixed"].rank() == 1
    zero_kernel = d01_zero["mixed"].nullspace()
    assert len(zero_kernel) == 7
    assert all(
        sp.factor(d01_zero["A"].subs(substitute(d01_zero, vector))) == 0
        for vector in zero_kernel
    )

    # Fail-closed Ts+1=0 boundary on the complete D01 line.
    d01_beta_zero = model(axis, cap_t, "D01", -1 / cap_t)
    assert d01_beta_zero["mixed"].rank() == 7
    beta_zero_kernel = d01_beta_zero["mixed"].nullspace()
    assert len(beta_zero_kernel) == 1
    assert (
        sp.factor(
            d01_beta_zero["B"].subs(substitute(d01_beta_zero, beta_zero_kernel[0]))
        )
        == 0
    )

    # At T=0, both axes are the same origin. Compatibility holds for every r,
    # but the D23 beta diagonal vanishes on the complete shared line.
    origin01 = model(axis, 0, "D01", slope_s)
    origin23 = model(axis, 0, "D23", slope_r)
    origin_kernel = sp.Matrix((-1, -1, 0, 0, 0, 0, 1, 0))
    assert_zero(origin01["mixed"] * origin_kernel, "origin D01")
    assert_zero(origin23["mixed"] * origin_kernel, "origin D23")
    assert origin01["mixed"].rank() == 7
    origin_sub = substitute(origin23, cap_c * origin_kernel)
    assert_equal(origin23["B"].subs(origin_sub), 0, "origin B23")

    # At r=0, rebuild the complete D23 plane and check exact agreement with
    # the independently verified compatibility theorem's frozen frame.
    d23_zero = model(axis, cap_t, "D23", 0)
    second = sp.Matrix((0, 0, 1, -1, 1, 1, 0, 1))
    assert_zero(d23_zero["mixed"] * kernel, "r0 shared generator")
    assert_zero(d23_zero["mixed"] * second, "r0 second generator")
    assert d23_zero["mixed"].rank() == 6
    rows23 = (3, 4, 5, 7, 9, 13)
    columns23 = (0, 1, 2, 3, 4, 5)
    witness23 = sp.factor(d23_zero["mixed"].extract(rows23, columns23).det())
    assert_equal(witness23, -4, "r0 D23 witness")

    return {
        "axis": f"h{axis}",
        "marking": ["T" if mode == axis else "0" for mode in range(4)],
        "D01_complete_kernel": {
            "generator": [str(value) for value in kernel],
            "mixed_rank": 7,
            "rank_witness": str(witness01),
        },
        "M23_r_on_D01_generator": [str(value) for value in compatibility],
        "compatibility_iff": "T*r=0",
        "shared_diagonals": {
            "A01": str(a01),
            "B01": str(b01),
            "A23": str(a23),
            "B23": str(b23),
        },
        "common_genuine_finite_finite_iff": "r=0 and C*s*T*(T*s+1)!=0",
        "boundary_attacks": {
            "s=0": "A01 zero on complete rank-one mixed fibre",
            "T*s+1=0": "B01 zero on complete rank-seven line",
            "T=0": "B23 zero on complete shared line, including axis intersection",
            "r=-1/2": "either mixed-incompatible when T!=0 or B23 zero when T=0",
        },
        "r_zero_reduction": {
            "D23_mixed_rank": 6,
            "D23_rank_witness": str(witness23),
            "D23_kernel_frame": [
                [str(kernel[row]), str(second[row])] for row in range(8)
            ],
            "matches_verified_compatibility_scope": True,
        },
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
        "scope": "finite-slope integration on the gamma=0 off-wall component-14 endpoint: arbitrary finite D23 slope over the complete finite-D01 kernels on both axes",
        "inputs": {
            path.name: sha256(path)
            for path in (
                P4_BOUNDARY,
                H31_ENDPOINT,
                ENDPOINT_AUDIT,
                ENDPOINT_AUDIT_SCRIPT,
                COMPATIBILITY_AUDIT,
                COMPATIBILITY_AUDIT_SCRIPT,
            )
        },
        "method": "fresh subset-DP permanent reconstruction; complete finite-D01 kernels; exact shared-coordinate multiplication by arbitrary finite-D23 mixed matrix; direct boundary fibres",
        "command": "uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_integration_verifier.py",
        "outputs": {REPORT.name: sha256(REPORT), script.name: sha256(script)},
        "limitations": "VERIFIED finite-slope integration only; infinity subclaims are cited precisely from an independent audit rather than recomputed; no on-wall, non-diagonal, arbitrary-order, or global claim",
        "imports_prior_derivations_or_helpers": False,
        "axis_certificates": axes,
        "arbitrary_finite_D23_compatibility": "VERIFIED: M23(r)k=0 iff T*r=0",
        "common_genuine_finite_finite_reduction": "VERIFIED: r=0 and C*s*T*(T*s+1)!=0",
        "reduction_to_verified_r_zero_compatibility_obstruction": True,
        "infinity_boundary_citation": {
            "source": ENDPOINT_AUDIT.name,
            "source_overall_label": "REFUTED for unrelated finite-rank exactness",
            "cited_verified_subclaims_only": [
                "off-wall D01 infinity rank-four obstructed",
                "off-wall D23 infinity projected ideal is unit",
            ],
            "recomputed_here": False,
        },
        "failed_or_timeout_branches": [],
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
