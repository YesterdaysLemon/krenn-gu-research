#!/usr/bin/env python3
"""Fresh exact audit of the two embedded-P3 r0=0 H22 weight endpoints.

This verifier imports neither construction code nor its algebra.  It rebuilds
the permanent contractions in the original coordinates and replays the exact
characteristic-zero H31 dependencies as separate processes.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_VERIFICATION.md"
)
CANDIDATE = ROOT / (
    "P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_"
    "ENDPOINTS_OBSTRUCTION_CANDIDATE.md"
)
PRIMARY = ROOT / (
    "derive_p5_h22_embedded_p3_component_r_zero_t_nonzero_"
    "weight_endpoints_obstruction_candidate.py"
)
H31_R_ZERO_NOTE = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md"
)
H31_R_ZERO_PRIMARY = (
    REPO_ROOT / "claims/p5/h31/embedded-p3/verify_p5_h31_embedded_p3_component_r_zero_boundary.py"
)
H31_NORMALIZED_NOTE = REPO_ROOT / "claims/p5/h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md"
H31_NORMALIZED_PRIMARY = REPO_ROOT / "claims/p5/h31/embedded-p3/verify_p5_h31_embedded_p3_component_normalized_boundary.py"

WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


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


def permanent4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def original_bases(cap_s, cap_u, t0, markings):
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta0 = (
        (1, 0, 0, t0),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    beta = tuple(
        tuple(sp.expand(beta0[i][j] + markings[i] * alpha[i][j]) for j in range(4))
        for i in range(4)
    )
    return alpha, beta


def normalized_bases(cap_s, cap_u, markings):
    """The exact normalized r=1, T=0 chart used by the H31 theorem."""
    alpha = (
        (0, 1, cap_s, cap_u),
        (0, -1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
    )
    beta0 = (
        (1, 0, 1, 0),
        (0, -1, 0, 1),
        (0, 1, 1, 0),
        (0, -1, 0, 1),
    )
    beta = tuple(
        tuple(sp.expand(beta0[i][j] + markings[i] * alpha[i][j]) for j in range(4))
        for i in range(4)
    )
    return alpha, beta


def project(row, extension, direction, rho, sigma):
    if direction == "D01":
        return (
            sp.expand(rho * row[0] + sigma * row[1]),
            row[2],
            row[3],
            extension,
        )
    if direction == "D23":
        return (
            row[0],
            row[1],
            sp.expand(rho * row[2] + sigma * row[3]),
            extension,
        )
    if direction == "delete0":
        return (row[1], row[2], row[3], extension)
    raise ValueError(direction)


def contraction(
    alpha,
    beta,
    extensions,
    direction,
    rho=0,
    sigma=1,
):
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction, rho, sigma) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], direction, rho, sigma) for i in range(4)
    )
    coefficients = {
        word: permanent4(
            tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        )
        for word in WORDS
    }
    return {
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "A": coefficients[(0, 0, 0, 0)],
        "B": coefficients[(1, 1, 1, 1)],
    }


def source_swap(row):
    return (row[0], row[1], -row[3], -row[2])


def scale_coordinate_zero(row, factor):
    return (factor * row[0], row[1], row[2], row[3])


def endpoint_reconstruction():
    cap_s, cap_u = sp.symbols("S U")
    t0 = sp.symbols("t0", nonzero=True)
    markings = sp.symbols("h0:4")
    ext01 = sp.symbols("x0:8")
    ext23 = sp.symbols("y0:8")
    alpha, beta = original_bases(cap_s, cap_u, t0, markings)

    data = {}
    for label, rho, sigma in (
        ("0_1", sp.Integer(0), sp.Integer(1)),
        ("1_0", sp.Integer(1), sp.Integer(0)),
    ):
        data[(label, "D01")] = contraction(alpha, beta, ext01, "D01", rho, sigma)
        data[(label, "D23")] = contraction(alpha, beta, ext23, "D23", rho, sigma)

    # Every original alpha row has coordinate zero equal to zero.  At weight
    # infinity both contractions retain that coordinate as a target column.
    # At weight zero D23 retains it as well.
    for key in (("1_0", "D01"), ("1_0", "D23"), ("0_1", "D23")):
        assert all(row[0] == 0 for row in data[key]["alpha_rows"])
        assert sp.expand(data[key]["A"]) == 0

    # Weight zero D01 is literally source-coordinate-zero deletion, including
    # all eight extension coordinates and both diagonals.
    deletion_zero = contraction(alpha, beta, ext01, "delete0")
    for key in ("alpha_rows", "beta_rows", "coefficients", "A", "B"):
        assert data[("0_1", "D01")][key] == deletion_zero[key]

    # Projective representatives can be rescaled without changing the result:
    # the rescaling is a nonzero monomial target change in each direction.
    kappa, rho, sigma, x0, x1, x2, x3, e = sp.symbols(
        "kappa rho sigma X0 X1 X2 X3 e", nonzero=True
    )
    row = (x0, x1, x2, x3)
    d01_scaled = project(row, e, "D01", kappa * rho, kappa * sigma)
    d01_unscaled = project(row, e, "D01", rho, sigma)
    d23_scaled = project(row, e, "D23", kappa * rho, kappa * sigma)
    d23_unscaled = project(row, e, "D23", rho, sigma)
    expected_d01_scaled = (
        kappa * d01_unscaled[0],
        d01_unscaled[1],
        d01_unscaled[2],
        d01_unscaled[3],
    )
    expected_d23_scaled = (
        d23_unscaled[0],
        d23_unscaled[1],
        kappa * d23_unscaled[2],
        d23_unscaled[3],
    )
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(d01_scaled, expected_d01_scaled, strict=True)
    )
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(d23_scaled, expected_d23_scaled, strict=True)
    )

    return {
        "symbols": (cap_s, cap_u, t0, markings, ext01, ext23),
        "alpha": alpha,
        "beta": beta,
        "data": data,
        "deletion_zero": deletion_zero,
        "projective_weight_scaling_checked": True,
    }


def signed_swap_audit(reconstruction):
    cap_s, cap_u, t0, markings, ext01, _ = reconstruction["symbols"]
    alpha = reconstruction["alpha"]
    beta = reconstruction["beta"]
    rprime = -t0

    # The swap acts differently on the two weighted directions.  This records
    # the endpoint exchange that invalidates a shared-weight H22 transport.
    rho, sigma, x0, x1, x2, x3, e = sp.symbols("rho sigma q0 q1 q2 q3 qe")
    row = (x0, x1, x2, x3)
    swapped = source_swap(row)
    d01_after = project(swapped, e, "D01", rho, sigma)
    d01_before = project(row, e, "D01", rho, sigma)
    assert d01_after == (
        d01_before[0],
        -d01_before[2],
        -d01_before[1],
        d01_before[3],
    )
    d23_after = project(swapped, e, "D23", rho, sigma)
    d23_reversed = project(row, e, "D23", sigma, rho)
    assert d23_after == (
        d23_reversed[0],
        d23_reversed[1],
        -d23_reversed[2],
        d23_reversed[3],
    )

    # Normalize the transformed component exactly.  The source-coordinate-zero
    # scale is invertible precisely because t0 != 0.  Interchange old modes 1
    # and 2 after the signed swap.
    order = (0, 2, 1, 3)
    transformed_alpha = tuple(
        scale_coordinate_zero(source_swap(alpha[i]), rprime) for i in order
    )
    transformed_beta = tuple(
        scale_coordinate_zero(source_swap(beta[i]), rprime) for i in order
    )

    normalized_markings = (
        markings[0] / rprime,
        markings[2],
        markings[1],
        -(1 + markings[3]),
    )
    normalized_alpha, normalized_beta = normalized_bases(
        -cap_u, -cap_s, normalized_markings
    )
    alpha_factors = (sp.Integer(1), -sp.Integer(1), -sp.Integer(1), -sp.Integer(1))
    beta_factors = (rprime, -sp.Integer(1), -sp.Integer(1), sp.Integer(1))
    for i in range(4):
        assert transformed_alpha[i] == tuple(
            sp.expand(alpha_factors[i] * value) for value in normalized_alpha[i]
        )
        assert transformed_beta[i] == tuple(
            sp.expand(beta_factors[i] * value) for value in normalized_beta[i]
        )

    # Extension coordinates follow the same nonzero row rescalings.  Check all
    # sixteen deletion-zero coefficients, not only the projected rows.
    normalized_extensions = (
        ext01[0],
        -ext01[2],
        -ext01[1],
        -ext01[3],
        ext01[4] / rprime,
        -ext01[6],
        -ext01[5],
        ext01[7],
    )
    normalized_deletion = contraction(
        normalized_alpha,
        normalized_beta,
        normalized_extensions,
        "delete0",
    )
    original_deletion = reconstruction["deletion_zero"]
    for word in WORDS:
        old_word = (word[0], word[2], word[1], word[3])
        factor = sp.prod(
            beta_factors[i] if word[i] else alpha_factors[i] for i in range(4)
        )
        difference = sp.factor(
            normalized_deletion["coefficients"][word]
            - original_deletion["coefficients"][old_word] / factor
        )
        assert difference == 0, (word, difference)

    assert sp.factor(normalized_deletion["A"] + original_deletion["A"]) == 0
    assert sp.factor(normalized_deletion["B"] - original_deletion["B"] / rprime) == 0

    # The marking and extension changes are bijective exactly on t0 != 0.
    marking_jacobian = sp.factor(
        sp.Matrix(normalized_markings).jacobian(markings).det()
    )
    assert marking_jacobian == 1 / rprime
    extension_jacobian = sp.factor(
        sp.Matrix(normalized_extensions).jacobian(ext01).det()
    )
    assert extension_jacobian == -1 / rprime

    return {
        "D01_weight_after_signed_swap": "[rho:sigma]",
        "D23_weight_after_signed_swap": "[sigma:rho]",
        "D01_endpoint_0_1_preserved": True,
        "D23_endpoint_0_1_sent_to_1_0": True,
        "D01_endpoint_1_0_preserved": True,
        "D23_endpoint_1_0_sent_to_0_1": True,
        "normalized_parameters": {"S": "-U", "U": "-S", "T": "0"},
        "normalized_markings": [str(value) for value in normalized_markings],
        "marking_jacobian": str(marking_jacobian),
        "extension_jacobian": str(extension_jacobian),
        "all_sixteen_deletion_zero_coefficients_transported": True,
        "deletion_zero_diagonal_scaling": {
            "A_normalized_over_A_original": "-1",
            "B_normalized_over_B_original": str(1 / rprime),
        },
        "uses_t0_nonzero_only_for_invertible_normalization": True,
        "shared_weight_H22_transport_used": False,
    }


def replay_json(script: Path) -> dict[str, object]:
    completed = subprocess.run(
        (sys.executable, str(script)),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=120,
        check=False,
    )
    assert completed.returncode == 0, (
        script.name,
        completed.stdout,
        completed.stderr,
    )
    assert not completed.stderr.strip(), (script.name, completed.stderr)
    return json.loads(completed.stdout)


def h31_dependency_audit():
    normalized = replay_json(H31_NORMALIZED_PRIMARY)
    assert normalized["verified"] is True
    assert normalized["field"] == "C"
    assert normalized["complete_normalized_chart_marked_H31_fibre_empty"] is True
    assert normalized["theorem_sha256"] == sha256(H31_NORMALIZED_NOTE)

    r_zero = replay_json(H31_R_ZERO_PRIMARY)
    assert r_zero["verified"] is True
    assert r_zero["field"] == "C"
    assert r_zero["r_zero_A_nonzero_H31_fibre_empty"] is True
    assert r_zero["signed_swap_transports_t_nonzero_to_r_nonzero"] is True
    assert r_zero["theorem_sha256"] == sha256(H31_R_ZERO_NOTE)
    assert r_zero["dependencies"][H31_NORMALIZED_NOTE.name] == sha256(
        H31_NORMALIZED_NOTE
    )

    return {
        "normalized_exact_replay_verified": True,
        "r_zero_exact_replay_verified": True,
        "normalized_binary_survivor_families": normalized[
            "binary_survivor_marked_families"
        ],
        "normalized_deepest_stacked_determinant": normalized[
            "deepest_stacked_determinant"
        ],
        "r_zero_boundary_family_count": len(r_zero["verified_boundary_families"]),
        "finite_field_audit_used_as_proof": False,
    }


def main():
    reconstruction = endpoint_reconstruction()
    transport = signed_swap_audit(reconstruction)
    h31 = h31_dependency_audit()
    data = reconstruction["data"]

    payload = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "scope": (
            "embedded-P3 free-plane r0=0, t0!=0 weighted-H22 fibres "
            "at [rho:sigma]=[0:1] and [1:0]"
        ),
        "inputs": {
            path.name: sha256(path)
            for path in (
                CANDIDATE,
                PRIMARY,
                H31_R_ZERO_NOTE,
                H31_R_ZERO_PRIMARY,
                H31_NORMALIZED_NOTE,
                H31_NORMALIZED_PRIMARY,
            )
        },
        "method": (
            "fresh no-import original-coordinate permanent reconstruction; "
            "exact signed-swap and normalization transport; separate exact "
            "characteristic-zero H31 replays"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py'
        ),
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "endpoint_1_0": {
            "D01_all_alpha_diagonal": str(data[("1_0", "D01")]["A"]),
            "D23_all_alpha_diagonal": str(data[("1_0", "D23")]["A"]),
            "verdict": "both directions fail the genuine-binary condition",
        },
        "endpoint_0_1": {
            "D23_all_alpha_diagonal": str(data[("0_1", "D23")]["A"]),
            "D01_equals_deletion_zero_coefficientwise": True,
            "verdict": (
                "D23 cannot be binary; a binary D01 would be an H31 lift "
                "excluded by the exact normalized-chart theorem"
            ),
        },
        "projective_weight_scaling_checked": reconstruction[
            "projective_weight_scaling_checked"
        ],
        "signed_swap_and_normalization": transport,
        "H31_dependency": h31,
        "both_endpoint_fibres_obstructed": True,
        "finite_field_computation_used_as_proof": False,
        "broad_brute_force_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
        "limitations": (
            "exactly the two stated t0!=0 homogeneous weight endpoints on "
            "this embedded-P3 r0=0 chart; relies on the separately replayed "
            "exact H31 theorem; no component exhaustiveness, arbitrary-order "
            "reduction, prize graph, or global Krenn-Gu conclusion"
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
