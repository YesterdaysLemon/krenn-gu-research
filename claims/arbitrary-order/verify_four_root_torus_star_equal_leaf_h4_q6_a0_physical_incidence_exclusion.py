#!/usr/bin/env python3
"""Verify the proved GLD105 physical-incidence parent composition.

The mathematical proof is the exact two-case composition recorded in the
owner theorem.  This checker pins every upstream proof carrier, validates the
incidence/rank and endpoint interfaces, distinguishes the two unrelated H2
notations, and checks that the H2 degree-drop split is exhaustive.  It does
not rerun the expensive upstream algebra and does not claim a wider chart or
global result.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / (
    "GLD105_A0_H4_Q6_PHYSICAL_INCIDENCE_COMPOSITION_CERTIFICATE.json"
)
GLD104_CERTIFICATE = BASE / "certificates" / (
    "GLD104_A0_P8_NONZERO_OFFSET_COMPOSITION_CERTIFICATE.json"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "61fc3adc4288e6a31e5e332e4c4cb36436b1de0e453b208c4ba9690355d116cf"
)
EXPECTED_SOURCE_PIN_COUNT = 19

OWNER_PATHS = {
    "GLD104": BASE
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_P8_"
    "NONZERO_OFFSET_CLOSURE_THEOREM.md",
    "GLD99": BASE
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_"
    "SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md",
    "GLD95": BASE
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_"
    "COMMON_MINOR_EXCLUSION_THEOREM.md",
    "GLD86": BASE
    / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_"
    "SYNDROME_BOUNDARY_CONTAINMENT_THEOREM.md",
}


class CompositionError(AssertionError):
    """Raised when a load-bearing GLD105 composition seam drifts."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CompositionError(message)


def lf_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    require(b"\r" not in data, f"unsupported bare carriage return: {path}")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_certificate(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == 1, "schema version")
    require(
        payload.get("certificate_id")
        == "GLD105-A0-H4-Q6-physical-incidence-parent-composition",
        "certificate id",
    )
    require(
        payload.get("status")
        == "proved_exact_scoped_characteristic_zero_composition",
        "proved scoped status",
    )
    require(payload.get("global_conjecture") == "UNRESOLVED", "global status")

    scope = payload.get("mathematical_scope", {})
    require(scope.get("field") == "C", "field")
    require(
        scope.get("assumptions")
        == [
            "a=0",
            "Q6(p,q)=0",
            "Omega*Delta(p,q)!=0",
            "equal-leaf incidence equations vanish",
            "rank(A)<=6",
        ],
        "scope assumptions",
    )
    require(
        scope.get("set_statement")
        == "B_incidence intersect V(I_7(A)) intersect V(a,Q6) "
        "intersect D(Omega*Delta) = empty",
        "set statement",
    )
    nonclaims = "\n".join(scope.get("nonclaims", []))
    for token in (
        "P6",
        "Omega=0",
        "Delta=0",
        "arbitrary a",
        "full E31",
        "outside the written F88",
        "Fitting",
        "global Krenn-Gu",
    ):
        require(token in nonclaims, f"missing nonclaim: {token}")

    split = payload.get("case_split", {})
    require(
        split.get("polynomial") == "H2deg=2*p^2-2*p+1",
        "degree-drop polynomial",
    )
    require(
        split.get("exhaustive_cases") == ["H2deg!=0", "H2deg=0"],
        "exhaustive H2deg split",
    )
    require(split["H2deg_open"]["offset_handler"] == "GLD104", "open handler")
    require(split["H2deg_open"]["endpoint_handler"] == "GLD95", "endpoint handler")
    require(split["H2deg_zero"]["handler"] == "GLD99", "zero handler")

    external = payload.get("external_consolidation", {})
    require(external.get("required_before_promotion") is True, "audit gate")
    require(external.get("status") == "accepted_2_of_2", "audit acceptance")
    require(
        external.get("candidate_commit")
        == "e3ee8629856a5d24ca18d2f1197ac11a3dc2c18e",
        "candidate commit",
    )
    require(
        external.get("candidate_tree")
        == "f0b3d9f1ffdd92738ad20efc37b49a424ade76c7",
        "candidate tree",
    )
    require(
        external.get("request_event_id") == "kgc_01M1C11C0928AZS8DQ25B1Y8V8",
        "audit request",
    )
    require(
        external.get("receipts")
        == {
            "Juniper": "kgc_01M1C12WAXQYFG2SPBT3ZMBYD1",
            "Mycelium": "kgc_01M1C17H0G9E9DY99JR24Y2HWH",
        },
        "audit receipts",
    )
    require(external.get("frontier_update_allowed") is True, "frontier gate")
    require(
        external.get("theorem_ledger_update_allowed") is True,
        "ledger gate",
    )
    require(len(payload.get("proof_topology", [])) == 8, "proof topology")


def validate_source_pins(payload: dict[str, Any]) -> dict[str, str]:
    pins = payload.get("source_pins_lf_sha256")
    require(
        isinstance(pins, dict) and len(pins) == EXPECTED_SOURCE_PIN_COUNT,
        "source-pin manifest",
    )
    actual: dict[str, str] = {}
    for relative, expected in pins.items():
        relative_path = Path(relative)
        require(not relative_path.is_absolute(), f"absolute pin: {relative}")
        path = ROOT / relative_path
        require(path.is_file(), f"missing pin: {relative}")
        digest = lf_sha256(path)
        require(digest == expected, f"source-pin mismatch: {relative}")
        actual[relative] = digest
    return actual


def require_markers(label: str, text: str, markers: tuple[str, ...]) -> None:
    for marker in markers:
        require(marker in text, f"{label} interface marker: {marker}")


def validate_upstream_interfaces() -> dict[str, list[str]]:
    texts = {
        label: path.read_text(encoding="utf-8") for label, path in OWNER_PATHS.items()
    }
    markers = {
        "GLD104": (
            "Proved exact scoped characteristic-zero",
            "rank M(G)<=6",
            "is contained in {B=C=0}",
            "No converse from the eight selected minors",
            "D(H2*Delta)",
            "UNRESOLVED",
        ),
        "GLD99": (
            "Proved exact scoped characteristic-zero theorem (`GLD99`)",
            "H2 = 2p^2-2p+1 = 0",
            "B_incidence intersect V(I_7(A)) intersect H4",
            "intersect V(H2,Q6) intersect D(Omega Delta) = empty",
            "retain `a,B,C` as formal coordinates",
            "UNRESOLVED",
        ),
        "GLD95": (
            "V(Q6,F28,F31) intersect D(Delta) = empty",
            "B intersect V(I_7(A)) intersect F88 intersect V(Q6)",
            "intersect D(Omega Delta) = empty",
            "Thus a point of `B intersect V(I_7(A))` has syndrome rank at most six",
            "UNRESOLVED",
        ),
        "GLD86": (
            "C_8=1",
            "B=0 iff M(G)C=0",
            "rank A(z) = rank M(G)[:,0:8]",
            "UNRESOLVED",
        ),
    }
    for label, required in markers.items():
        require_markers(label, texts[label], required)

    gld104 = load_json(GLD104_CERTIFICATE)
    require(
        gld104.get("status")
        == "proved_exact_scoped_characteristic_zero_composition",
        "GLD104 promoted status",
    )
    external = gld104.get("external_consolidation", {})
    require(external.get("status") == "accepted_2_of_2", "GLD104 acceptance")
    require(
        external.get("request_event_id")
        == "kgc_01M1BXKGZ8F86B6XWK1J6Q3DMF",
        "GLD104 request",
    )
    require(
        set(external.get("receipts", {})) == {"Juniper", "Mycelium"},
        "GLD104 receipts",
    )
    return {label: list(required) for label, required in markers.items()}


def validate_notation_fences(payload: dict[str, Any]) -> dict[str, str]:
    notation = payload.get("notation_fences", {})
    require("not the scalar offset B" in notation.get("B_incidence", ""), "B fence")
    require("not the scalar offset C" in notation.get("C_center", ""), "C fence")
    require(
        notation.get("H2deg")
        == "2*p^2-2*p+1, the Q6 leading-coefficient/degree-drop polynomial",
        "H2deg fence",
    )

    p, q = sp.symbols("p q")
    d0 = p + q - 1
    s = (p + q - p * q) / d0
    L1 = p**2 + 2 * p * q - 2 * p - q
    H2deg = 2 * p**2 - 2 * p + 1
    require(sp.cancel(p - s - L1 / d0) == 0, "p-s identity")
    require(sp.expand(H2deg - L1) != 0, "H2 notational distinction")
    require("p-s=L1/(p+q-1)" in notation.get("GLD86_H2_collision", ""), "collision fence")
    return {
        "H2deg": str(H2deg),
        "GLD86_collision_divisor": "p-s=L1/(p+q-1)",
        "distinct_polynomials": "true",
    }


def validate_exhaustive_composition(payload: dict[str, Any]) -> dict[str, str]:
    split = payload["case_split"]
    outcomes: dict[str, str] = {}
    for h2deg_is_zero in (False, True):
        if h2deg_is_zero:
            require(split["H2deg_zero"]["handler"] == "GLD99", "zero branch")
            require(
                "arbitrary a" in split["H2deg_zero"]["scope"],
                "GLD99 a=0 specialization",
            )
            outcomes["H2deg=0"] = "excluded by GLD99"
        else:
            open_branch = split["H2deg_open"]
            require(open_branch["upstream_incidence_bridge"] == "GLD75/GLD86", "bridge")
            require(open_branch["offset_handler"] == "GLD104", "offset")
            require(
                open_branch["offset_conclusion"] == "B_offset=C_offset=0",
                "offset conclusion",
            )
            require(open_branch["endpoint_handler"] == "GLD95", "endpoint")
            outcomes["H2deg!=0"] = "GLD86 -> GLD104 -> GLD95 contradiction"
    require(set(outcomes) == {"H2deg=0", "H2deg!=0"}, "case exhaustion")
    return outcomes


def check() -> dict[str, Any]:
    started = time.monotonic()
    require(
        lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256,
        "certificate pin",
    )
    payload = load_json(CERTIFICATE)
    validate_certificate(payload)
    pins = validate_source_pins(payload)
    interfaces = validate_upstream_interfaces()
    notation = validate_notation_fences(payload)
    cases = validate_exhaustive_composition(payload)
    return {
        "status": "proved_GLD105_parent_composition_verified",
        "global_conjecture": "UNRESOLVED",
        "field": "C",
        "scope": "normalized a=0 H4/Q6 physical incidence on D(Omega*Delta)",
        "source_pins_checked": len(pins),
        "upstream_interfaces": sorted(interfaces),
        "notation_fences": notation,
        "exhaustive_cases": cases,
        "external_consolidation": "accepted_2_of_2",
        "frontier_or_ledger_promotion_allowed": True,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("GLD105 physical-incidence parent composition verifier: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
