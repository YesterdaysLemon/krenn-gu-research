#!/usr/bin/env python3
"""Verify the candidate GLD100 B=0 C-open composition corollary."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / "GLD100_B0_COPEN_COROLLARY_CERTIFICATE.json"
GLD96_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_"
    "R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md"
)
GLD100_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_G0_GATE_REMOVAL_THEOREM.md"
)
GLD100_PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py"
)
GLD100_AUDIT = BASE / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py"
)
GLD99_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_"
    "H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "c4a2ba5389e428de8b8b961e19ca6449b52d15266a2a7f3418892d5969744394"
)
EXPECTED_SOURCE_PIN_COUNT = 9

PRIMARY_CORE_FUNCTIONS = (
    "reconstruct_gammas",
    "pair_projection",
    "projection_cover",
    "q_fibre",
    "gamma_a_fibre",
    "check_fibres",
)
AUDIT_CORE_FUNCTIONS = (
    "generic_gamma_atlas",
    "pair_resultant",
    "specialized_q_fibre_report",
    "generic_pair_resultant_bridge",
    "gamma_branch",
    "verify_branch_geometry",
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").replace("`", "").split())


def validate_certificate(payload: dict[str, Any]) -> None:
    require(lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256, "certificate hash")
    require(payload.get("schema_version") == 1, "schema")
    require(
        payload.get("certificate_id") == "GLD100-B0-Copen-arbitrary-a-corollary",
        "certificate id",
    )
    require(
        payload.get("status")
        == "candidate_exact_scoped_characteristic_zero_composition",
        "candidate status",
    )
    require(payload.get("global_conjecture") == "UNRESOLVED", "global status")

    scope = payload.get("mathematical_scope", {})
    require(scope.get("field") == "C", "field")
    require(
        scope.get("set_statement")
        == "V(B_offset,Q6) intersect D(C_offset*Delta) intersect {rank M(G)<=6} = empty",
        "set statement",
    )
    assumptions = scope.get("assumptions", [])
    for expected in (
        "B_offset=0",
        "C_offset!=0",
        "Q6=0",
        "Delta!=0",
        "complete GLD71 syndrome rank at most six",
        "a is arbitrary",
    ):
        require(expected in assumptions, f"assumption {expected}")
    require("D(B_offset*H2deg*Delta)" in scope.get("downstream_reduction", ""), "D(B) reduction")

    split = payload.get("case_split", {})
    require(split.get("polynomial") == "H2deg=2*p^2-2*p+1", "H2deg polynomial")
    require(split.get("exhaustive_cases") == ["H2deg!=0", "H2deg=0"], "case cover")
    require(split["H2deg_open"].get("E31_required") is False, "E31-free open case")
    require(split["H2deg_zero"].get("handler", "").startswith("GLD99"), "GLD99 handoff")
    require(len(payload.get("proof_topology", [])) == 7, "proof topology")

    external = payload.get("external_consolidation", {})
    require(external.get("required_before_promotion") is True, "external gate required")
    require(external.get("candidate_commit") is None, "candidate commit unset")
    require(external.get("candidate_tree") is None, "candidate tree unset")
    require(external.get("request_event_id") is None, "request unset")
    require(external.get("receipts") == {}, "receipts unset")
    require(external.get("status") == "pending", "external gate pending")
    require(external.get("frontier_update_allowed") is False, "frontier gate")
    require(external.get("theorem_ledger_update_allowed") is False, "ledger gate")


def validate_source_pins(payload: dict[str, Any]) -> dict[str, str]:
    pins = payload.get("source_pins_lf_sha256", {})
    require(len(pins) == EXPECTED_SOURCE_PIN_COUNT, "source pin count")
    for relative, expected in pins.items():
        path = ROOT / relative
        require(not Path(relative).is_absolute(), f"absolute source pin {relative}")
        require(path.is_file(), f"missing source pin {relative}")
        require(lf_sha256(path) == expected, f"source drift {relative}")
    return pins


def function_nodes(path: Path) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def node_mentions_e31(node: ast.AST) -> bool:
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and "e31" in child.id.lower():
            return True
        if isinstance(child, ast.Constant) and isinstance(child.value, str):
            if "e31" in child.value.lower():
                return True
    return False


def validate_no_e31_core() -> dict[str, list[str]]:
    reports: dict[str, list[str]] = {}
    for label, path, expected_names in (
        ("primary", GLD100_PRIMARY, PRIMARY_CORE_FUNCTIONS),
        ("independent_audit", GLD100_AUDIT, AUDIT_CORE_FUNCTIONS),
    ):
        nodes = function_nodes(path)
        checked: list[str] = []
        for name in expected_names:
            require(name in nodes, f"missing {label} core function {name}")
            require(not node_mentions_e31(nodes[name]), f"hidden E31 use in {label}.{name}")
            checked.append(name)
        reports[label] = checked
    return reports


def validate_upstream_interfaces() -> list[str]:
    gld96 = normalized_text(GLD96_OWNER)
    gld100 = normalized_text(GLD100_OWNER)
    gld99 = normalized_text(GLD99_OWNER)

    for marker in (
        "Ttilde_i=D_i*T_i",
        "f_i(0)=0",
        "111 GLD88 common-kernel identities",
        "The first residual then reads",
        "C*g_0(0)=0",
    ):
        require(marker in gld96, f"GLD96 interface: {marker}")

    for marker in (
        "On D(H2*Delta), let",
        "gamma0,...,gamma3",
        "Q6 = gamma0 = gamma1 = gamma2 = gamma3 = 0.",
        "The exact necessary pair-resultant cover puts",
        "p in one of the eight factors",
        "Consequently C=0, so the point lies on F88.",
    ):
        require(marker in gld100, f"GLD100 interface: {marker}")
    require(re.search(r"D0 = 192\*\(1-p\)\*Coff\^2", gld100) is not None, "GLD100 D0 fibre")
    require("D2 = (243/128)*(p-1)" in gld100, "GLD100 D2 fibre")

    for marker in (
        "retain a,B,C as formal coordinates",
        "On the denominator-safe open D(Delta), every geometric point",
        "full GLD71 37 x 9 syndrome has rank at most six has B=C=0",
    ):
        require(marker in gld99, f"GLD99 interface: {marker}")
    return ["GLD96", "GLD100", "GLD99"]


def validate_case_logic(payload: dict[str, Any]) -> dict[str, str]:
    split = payload["case_split"]
    outcomes = {
        "H2deg!=0": split["H2deg_open"]["conclusion"],
        "H2deg=0": split["H2deg_zero"]["conclusion"],
    }
    require(set(outcomes) == {"H2deg!=0", "H2deg=0"}, "case keys")
    require(all("impossible" in result for result in outcomes.values()), "case contradictions")
    return outcomes


def check() -> dict[str, Any]:
    started = time.monotonic()
    payload = load_json(CERTIFICATE)
    validate_certificate(payload)
    pins = validate_source_pins(payload)
    interfaces = validate_upstream_interfaces()
    core = validate_no_e31_core()
    cases = validate_case_logic(payload)
    return {
        "status": "candidate_GLD100_B0_Copen_corollary_verified",
        "global_conjecture": "UNRESOLVED",
        "field": "C",
        "scope": "normalized arbitrary-a B_offset=0 C_offset-open rank exclusion on D(Delta)",
        "source_pins_checked": len(pins),
        "upstream_interfaces": interfaces,
        "E31_core_mentions": 0,
        "core_functions_checked": {key: len(value) for key, value in core.items()},
        "exhaustive_cases": cases,
        "external_consolidation": "pending",
        "frontier_or_ledger_promotion_allowed": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("GLD100 B=0 C-open composition verifier: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
