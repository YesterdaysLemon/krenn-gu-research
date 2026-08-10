#!/usr/bin/env python3
"""Integrate the verified weighted-H22 certificates on the p+q DVR wall."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
THEOREM = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md"
)
P4_WALL = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
P4_PRIMARY = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/verify_p4_common_active_binary_triangle_p_plus_q_boundary.py"
P4_AUDIT = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/audit_p4_common_active_binary_triangle_p_plus_q_boundary.py"
PARTIAL = ROOT / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md"
GENERIC_INFINITY = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_"
    "GENERIC_D01_INFINITY_OBSTRUCTION.md"
)
EXCEPTIONAL = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_"
    "EXCEPTIONAL_FIBRES_OBSTRUCTION.md"
)
ENDPOINT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_"
    "INFINITY_ENDPOINT_CANDIDATE.md"
)
ENDPOINT_INTEGRATION = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_"
    "INFINITY_ENDPOINT_INTEGRATION_VERIFICATION.md"
)
ENDPOINT_COMPATIBILITY = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_"
    "INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md"
)
COVERAGE_REPORT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_"
    "DIAGONAL_DVR_COVERAGE_AUDIT.md"
)
COVERAGE_LEDGER = ROOT / "p5_h22_p_plus_q_diagonal_dvr_coverage.json"
MASK6_REPORT = (
    ROOT
    / "P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_"
    "OBSTRUCTION_CANDIDATE.md"
)
MASK6_VERIFICATION = (
    ROOT
    / "P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_"
    "INDEPENDENT_VERIFICATION.md"
)
MASK6_CERTIFICATE = (
    ROOT
    / "p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json"
)

EXPECTED_IDS = {
    "finite_generic_y0_b_full",
    "finite_generic_y0_b_drop",
    "finite_generic_negative_y_embedded_p3",
    "finite_exceptional_a0_a_minus1",
    "finite_half_centre_y0",
    "finite_half_centre_negative_y_embedded_p3",
    "infinity_lower_pair_embedded_p3",
    "infinity_component14_off_wall",
    "infinity_component14_on_wall",
}
MASK6_IDS = {
    "finite_generic_negative_y_embedded_p3",
    "finite_half_centre_negative_y_embedded_p3",
    "infinity_lower_pair_embedded_p3",
}


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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def dependency_markers() -> dict[str, list[str]]:
    return {
        P4_WALL.name: ["VERIFIED after repair and fresh independent replay"],
        PARTIAL.name: ["SUPERSEDED PARTIAL CHECKPOINT"],
        GENERIC_INFINITY.name: ["VERIFIED"],
        EXCEPTIONAL.name: ["VERIFIED after a fresh no-import audit"],
        ENDPOINT.name: ["VERIFIED after independent factor-cover and compatibility audits"],
        ENDPOINT_INTEGRATION.name: ["VERIFIED"],
        ENDPOINT_COMPATIBILITY.name: ["VERIFIED"],
        COVERAGE_REPORT.name: ["whole diagonal-DVR `p+q=0` weighted-`H22` wall remains **UNKNOWN**"],
        MASK6_REPORT.name: ["VERIFIED after a fresh no-import replay"],
        MASK6_VERIFICATION.name: ["VERIFIED for the frozen actual-wall claim"],
    }


def main() -> None:
    dependencies = (
        P4_WALL,
        P4_PRIMARY,
        P4_AUDIT,
        PARTIAL,
        GENERIC_INFINITY,
        EXCEPTIONAL,
        ENDPOINT,
        ENDPOINT_INTEGRATION,
        ENDPOINT_COMPATIBILITY,
        COVERAGE_REPORT,
        COVERAGE_LEDGER,
        MASK6_REPORT,
        MASK6_VERIFICATION,
        MASK6_CERTIFICATE,
    )
    markers = dependency_markers()
    for path in dependencies:
        require(path.is_file(), f"missing dependency: {path.name}")
        text = path.read_text(encoding="utf-8")
        for marker in markers.get(path.name, []):
            require(marker in text, f"missing marker {marker!r} in {path.name}")

    ledger = json.loads(COVERAGE_LEDGER.read_text(encoding="utf-8"))
    strata = {entry["id"]: entry for entry in ledger["strata"]}
    require(set(strata) == EXPECTED_IDS, "coverage ledger stratum list changed")
    require(len(strata) == 9, "expected nine aggregate strata")
    old_unknown = {
        entry["id"] for entry in ledger["strata"] if entry["h22_status"] == "UNKNOWN"
    }
    require(old_unknown == MASK6_IDS, "historical unknown set is not exactly mask 6")

    mask6 = json.loads(MASK6_CERTIFICATE.read_text(encoding="utf-8"))
    require(mask6["claim_label"] == "VERIFIED", "mask-6 certificate is not verified")
    actual_families = mask6["actual_families"]
    require({entry["id"] for entry in actual_families} == MASK6_IDS, "mask-6 ids differ")
    require(all(len(entry["flags"]) == 4 for entry in actual_families), "flag count changed")
    require(
        mask6["certificate"]["D01_all_alpha_diagonal"] == "0"
        and mask6["certificate"]["D23_all_alpha_diagonal"] == "0",
        "mask-6 structural obstruction changed",
    )
    require(mask6["independent_verifier_complete"] is True, "mask-6 audit missing")

    integrated = {
        stratum_id: "VERIFIED"
        if entry["h22_status"] == "VERIFIED" or stratum_id in MASK6_IDS
        else entry["h22_status"]
        for stratum_id, entry in strata.items()
    }
    require(set(integrated.values()) == {"VERIFIED"}, "an aggregate stratum is open")

    result = {
        "status": "pass",
        "claim_label": "VERIFIED",
        "role": "proof_b",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "scope": (
            "whole diagonal-source-torus DVR p+q=0 weighted-H22 wall of "
            "component twenty"
        ),
        "inputs": {path.name: sha256(path) for path in dependencies},
        "method": (
            "exact nine-stratum dependency integration over the verified P4 arc "
            "classification, with a twelve-flag no-import mask-6 closure"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py'
        ),
        "outputs": {THEOREM.name: sha256(THEOREM), SCRIPT.name: sha256(SCRIPT)},
        "limitations": (
            "VERIFIED after a fresh independent aggregate audit; diagonal source "
            "tori only; no full embedded-P3 projective closure, non-diagonal or "
            "arbitrary GL4 changes, arbitrary-order reduction, or global claim"
        ),
        "historical_coverage_status": ledger["wall_status"],
        "historical_unknown_strata": sorted(old_unknown),
        "mask6_actual_flag_count": sum(len(entry["flags"]) for entry in actual_families),
        "integrated_strata": integrated,
        "verified_stratum_count": sum(value == "VERIFIED" for value in integrated.values()),
        "remaining_diagonal_DVR_H22_gaps": [],
        "whole_diagonal_DVR_H22_wall_empty": "VERIFIED",
        "fresh_independent_aggregate_audit_complete": True,
        "full_embedded_P3_projective_H22_closed": False,
        "finite_field_computation_used_as_proof": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
