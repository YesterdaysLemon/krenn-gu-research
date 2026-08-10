#!/usr/bin/env python3
"""Audit the frozen dependency and stratum map for the p+q=0 H22 wall.

This is a coverage/dependency audit, not a mathematical replay of every cited
certificate.  It verifies frozen bytes, status markers, the exhaustive ledger
shape, and the elementary support-mask calculation used to identify the open
embedded-P3 arc families.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER_PATH = ROOT / "p5_h22_p_plus_q_diagonal_dvr_coverage.json"


REQUIRED_MARKERS = {
    "p4_boundary_classification": [
        "VERIFIED after repair and fresh independent replay",
        "E=0 iff",
    ],
    "half_and_generic_finite_d01": [
        "whole-wall `H22` remains UNKNOWN",
        "entire `a=-1/2` replacement family",
    ],
    "generic_d01_infinity": [
        "VERIFIED after two disjoint fresh replays",
        "D01` at infinity",
    ],
    "b_full_infinity_replay": [
        "**VERIFIED.**",
        "B_full,D01` infinity",
    ],
    "b_drop_infinity_replay": [
        "**VERIFIED**",
        "B_drop` `S1/S2` `D01`-infinity",
    ],
    "exceptional_fibres": [
        "**VERIFIED**",
        "actual lower-pair baseline/wall residue families",
    ],
    "infinity_endpoint_base_audit": [
        "claim_label: REFUTED",
        "gamma=2` on-wall face has no weighted-`H22` lift",
    ],
    "infinity_endpoint_compatibility": [
        "**VERIFIED**",
        "finite-`D23,r=0` pair",
    ],
    "infinity_endpoint_integration": [
        "**VERIFIED.**",
        "forced to have `D23` slope `r=0`",
    ],
    "embedded_p3_generic": [
        "exact characteristic-zero theorem",
        "omitted normalization/projective boundary",
    ],
    "embedded_p3_rank_two": [
        "exact characteristic-zero theorem",
        "rank-two",
    ],
    "embedded_p3_rank_one": [
        "exact characteristic-zero theorem",
        "rank-one",
    ],
    "embedded_p3_projective_audit": [
        "claim_label: REFUTED",
        "mask-6 matching transport",
    ],
    "embedded_p3_r_zero_audit": [
        "claim_label: REFUTED",
        "t0!=0",
    ],
    "embedded_p3_endpoint_verification": [
        "claim_label: VERIFIED",
        "VERIFIED for the frozen endpoint claim",
    ],
    "embedded_p3_endpoint_verifier": [
        "both_endpoint_fibres_obstructed",
        "shared_weight_H22_transport_used",
    ],
}


EXPECTED_STATUS = {
    "finite_generic_y0_b_full": "VERIFIED",
    "finite_generic_y0_b_drop": "VERIFIED",
    "finite_generic_negative_y_embedded_p3": "UNKNOWN",
    "finite_exceptional_a0_a_minus1": "VERIFIED",
    "finite_half_centre_y0": "VERIFIED",
    "finite_half_centre_negative_y_embedded_p3": "UNKNOWN",
    "infinity_lower_pair_embedded_p3": "UNKNOWN",
    "infinity_component14_off_wall": "VERIFIED",
    "infinity_component14_on_wall": "VERIFIED",
}


def sha256(path: Path) -> str:
    # Every pinned dependency is tracked text.  Git stores those blobs with
    # LF endings, while Windows checkouts may materialize CRLF.  Canonicalize
    # only that transport difference so one durable pin works on both.
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_actual_wall_mask() -> dict[str, object]:
    # The common hyperplane has basis (e,A,B).  A covector annihilating
    # <e,c1*A-c2*B> is (0,c2,c1); the same plane may use its negative normal.
    # A covector annihilating <e,c1*A+c2*B> is (0,-c2,c1).
    # These are exactly n1,n2,n3 for [C:A:B]=[0:c2:c1].
    c1, c2 = 5, 7
    n1 = (0, c2, c1)
    n2 = (0, -c2, -c1)
    n3 = (0, -c2, c1)
    sign_rectangle = ((0, c2, c1), (0, -c2, -c1), (0, -c2, c1))
    require((n1, n2, n3) == sign_rectangle, "normal/sign-rectangle mismatch")

    # Each normal annihilates the two claimed spanning rows.
    e = (1, 0, 0)
    lower = (0, c1, -c2)
    upper = (0, c1, c2)
    dot = lambda x, y: sum(a * b for a, b in zip(x, y))
    require(dot(n1, e) == dot(n1, lower) == 0, "n1 plane check failed")
    require(dot(n2, e) == dot(n2, lower) == 0, "n2 plane check failed")
    require(dot(n3, e) == dot(n3, upper) == 0, "n3 plane check failed")
    support_mask = (1 if 0 else 0) | (2 if c2 else 0) | (4 if c1 else 0)
    require(support_mask == 6, "actual wall must have normal support mask 6")
    return {
        "representative_c1_c2": [c1, c2],
        "normals": [list(n1), list(n2), list(n3)],
        "support_mask": support_mask,
        "status": "pass",
    }


def main() -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    require(ledger["claim_label"] == "UNKNOWN", "whole-wall label must remain UNKNOWN")
    require(ledger["wall_status"] == "UNKNOWN", "whole-wall status must remain UNKNOWN")

    checked_files = {}
    for key, dep in ledger["dependencies"].items():
        path = REPO_ROOT / dep["path"]
        require(path.is_file(), f"missing dependency: {dep['path']}")
        actual = sha256(path)
        require(actual == dep["sha256"], f"sha256 mismatch for {dep['path']}: {actual}")
        text = path.read_text(encoding="utf-8")
        for marker in REQUIRED_MARKERS[key]:
            require(marker in text, f"missing marker {marker!r} in {dep['path']}")
        checked_files[key] = actual

    strata = ledger["strata"]
    by_id = {entry["id"]: entry for entry in strata}
    require(len(by_id) == len(strata), "duplicate stratum id")
    require(set(by_id) == set(EXPECTED_STATUS), "stratum ledger is not the frozen exhaustive list")
    for stratum_id, expected in EXPECTED_STATUS.items():
        require(by_id[stratum_id]["h22_status"] == expected, f"status mismatch: {stratum_id}")
        for evidence_key in by_id[stratum_id]["evidence"]:
            require(evidence_key in ledger["dependencies"], f"unknown evidence key: {evidence_key}")

    unknown = [entry for entry in strata if entry["h22_status"] == "UNKNOWN"]
    require(len(unknown) == 3, "exactly three aggregate embedded-P3 strata must remain UNKNOWN")
    require(all(entry["normal_support_mask"] == 6 for entry in unknown), "every open stratum must be mask 6")
    require(
        ledger["closure_answer"]["does_new_r0_endpoint_verification_alone_close_the_diagonal_dvr_wall"] is False,
        "endpoint replay must not be promoted to whole-wall closure",
    )
    require(
        ledger["closure_answer"]["would_a_true_full_embedded_p3_projective_obstruction_close_the_remaining_wall"] is True,
        "a genuinely full embedded-P3 theorem should be recorded as sufficient for this restricted wall",
    )

    result = {
        "status": "pass",
        "claim_label": "UNKNOWN",
        "wall_status": "UNKNOWN",
        "ledger_sha256": sha256(LEDGER_PATH),
        "dependency_count": len(checked_files),
        "stratum_count": len(strata),
        "verified_stratum_count": sum(entry["h22_status"] == "VERIFIED" for entry in strata),
        "unknown_stratum_count": len(unknown),
        "unknown_strata": [entry["id"] for entry in unknown],
        "actual_wall_normal_mask": verify_actual_wall_mask(),
        "endpoint_verifier_replay": ledger["dependencies"]["embedded_p3_endpoint_verification"]["replay"],
        "new_r0_endpoint_verification_closes_wall": False,
        "finite_field_results_used_as_proof": False,
        "global_krenn_gu_resolved": False,
        "limitations": ledger["limitations"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
