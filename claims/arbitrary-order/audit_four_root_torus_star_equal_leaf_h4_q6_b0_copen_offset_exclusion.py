#!/usr/bin/env python3
"""Independent no-repository-import audit of the proved GLD106 corollary."""

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
GLD99_OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_"
    "H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md"
)
PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_b0_copen_offset_exclusion.py"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "cb482133a56922695030ca850caa1135b480be8a93e23331fe8316e26741f377"
)
EXPECTED_SOURCE_PINS = {
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md": "2d989620d82554197ce7f85d603269122d58dfe07c36a9ab46121a2261aabcff",
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_G0_GATE_REMOVAL_THEOREM.md": "0c893a4d96a980d2b9845d55a5e5dfbf9b901da5dda267424aae470be39887df",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py": "415b6963b37b6e2e8c15bc9b0e08f4206bff164e9e563a12d5fa06ec44cbd028",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_g0_gate_removal.py": "ac1420548ea7de8ea4130b083f47c06e61cd1dd3c4e66bdffd65325563b8c4dc",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_G0_GATE_REMOVAL_REVIEW_2026-08-29.md": "9818e17e28cbf16e7d6b3012f648da6de4add5827ad6fc676f59127a4b49db4a",
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md": "f5fd49a6ff039f128f83b89bc3a7019c201001c54ba33223b2ac71e3e2289708",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py": "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py": "d41178a72731eff4d1d0eeb63d70224a58cea62b1f1336f0aa6d123120226e48",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_REVIEW_2026-08-29.md": "1bd76cb185ea4acc8a49c4f41bf18d1cf1b88c501e1b74bbb1d4de4362344a6d",
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def normalized(text: str) -> str:
    return " ".join(text.replace("`", "").split())


def load_payload() -> dict[str, Any]:
    require(lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256, "certificate hash")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(payload.get("certificate_id") == "GLD100-B0-Copen-arbitrary-a-corollary", "id")
    require(
        payload.get("status") == "proved_exact_scoped_characteristic_zero_composition",
        "proved scoped status",
    )
    require(payload.get("global_conjecture") == "UNRESOLVED", "global status")
    require(payload.get("source_pins_lf_sha256") == EXPECTED_SOURCE_PINS, "frozen manifest")
    require(
        payload.get("external_consolidation")
        == {
            "required_before_promotion": True,
            "candidate_commit": "8001f3435702d642ccb86e10893000379cca7ae5",
            "candidate_tree": "8b4b38f92c143aa557e039661ab7ecf046539181",
            "candidate_diff_bytes": 43128,
            "candidate_diff_sha256": "b8b33767bd74677b4e09a3a78bdaece657e90a5dbcb681452ae0ff3ca3c5f915",
            "request_event_id": "kgc_01M1C3T5Y83KSKVKG22HK0TCAH",
            "receipts": {
                "Juniper": "kgc_01M1C3VG98735EV4JM8TEVE02V",
                "Kestrel": "kgc_01M1C468KR8XX1C8XC0EMEXPM3",
            },
            "status": "accepted_2_of_2",
            "frontier_update_allowed": True,
            "theorem_ledger_update_allowed": True,
        },
        "external gate",
    )
    return payload


def validate_frozen_sources() -> None:
    for relative, expected in EXPECTED_SOURCE_PINS.items():
        path = ROOT / relative
        require(path.is_file(), f"missing source {relative}")
        require(lf_sha256(path) == expected, f"source drift {relative}")


def owner_section(text: str, start: str, end: str) -> str:
    require(start in text, f"missing section {start}")
    tail = text.split(start, 1)[1]
    require(end in tail, f"missing section end {end}")
    return tail.split(end, 1)[0]


def audit_owner_dependency_boundary() -> dict[str, Any]:
    gld96 = normalized(GLD96_OWNER.read_text(encoding="utf-8"))
    gld100_raw = GLD100_OWNER.read_text(encoding="utf-8")
    gld99 = normalized(GLD99_OWNER.read_text(encoding="utf-8"))

    require("Ttilde_i=D_i*T_i" in gld96, "GLD96 clearing relation")
    require("Ttilde_i = f_i(B) + C*g_i(B)" in gld96, "GLD96 residual form")
    require("f_i(0)=0" in gld96, "GLD96 common-kernel specialization")
    require("C*g_0(0)=0" in gld96, "GLD96 B=0 first residual")

    algebra = owner_section(
        gld100_raw,
        "## 2. Exact necessary pair-resultant cover",
        "## 4. Proof route",
    )
    require("E31" not in algebra, "E31 leaked into GLD100 B=0 algebra sections")
    algebra_normalized = normalized(algebra)
    for marker in (
        "Q6 = gamma0 = gamma1 = gamma2 = gamma3 = 0.",
        "Thus the eight factors in S are a necessary case cover",
        "The direct seven-minor calculation gives",
        "D0 = 192*(1-p)*Coff^2",
        "The remaining common-a test is empty",
        "D2 = (243/128)*(p-1)",
    ):
        require(marker.lower() in algebra_normalized.lower(), f"GLD100 algebra marker {marker}")

    require("retain a,B,C as formal coordinates" in gld99, "GLD99 arbitrary-a interface")
    require(
        re.search(
            r"every geometric point at which the full GLD71 37 x 9 syndrome has rank at most six has B=C=0",
            gld99,
        )
        is not None,
        "GLD99 rank-to-offset interface",
    )
    return {
        "GLD96_reversible_cleared_residual_form": True,
        "GLD100_B0_algebra_section_E31_mentions": 0,
        "GLD100_factor_and_direct_minor_markers": 6,
        "GLD99_arbitrary_a_rank_interface": True,
    }


def audit_case_exhaustion(payload: dict[str, Any]) -> dict[str, str]:
    split = payload["case_split"]
    require(split["exhaustive_cases"] == ["H2deg!=0", "H2deg=0"], "case partition")
    require(split["H2deg_open"]["E31_required"] is False, "E31-free branch")
    require("impossible" in split["H2deg_open"]["conclusion"], "open contradiction")
    require("impossible" in split["H2deg_zero"]["conclusion"], "zero contradiction")
    return {
        "H2deg!=0": "GLD96 residual form -> GLD100 B=0 gamma/fibre contradiction",
        "H2deg=0": "GLD99 forces B_offset=C_offset=0",
    }


def validate_primary_independence_boundary() -> list[str]:
    source = PRIMARY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    require(not any("g0_gate_removal" in name for name in imports), "primary imports upstream checker")
    require(not any("h2_degree_drop" in name for name in imports), "primary imports GLD99 checker")
    require("sympy" not in imports, "composition primary unexpectedly uses SymPy")
    return imports


def check() -> dict[str, Any]:
    started = time.monotonic()
    payload = load_payload()
    validate_frozen_sources()
    dependency = audit_owner_dependency_boundary()
    cases = audit_case_exhaustion(payload)
    primary_imports = validate_primary_independence_boundary()
    return {
        "status": "independent_proved_GLD106_B0_Copen_corollary_audit_pass",
        "global_conjecture": "UNRESOLVED",
        "field": "C",
        "source_pins_checked": len(EXPECTED_SOURCE_PINS),
        "dependency_boundary": dependency,
        "case_outcomes": cases,
        "primary_imports": primary_imports,
        "repository_verifiers_imported_or_executed": 0,
        "E31_wall_D_B_closed": False,
        "frontier_or_ledger_promotion_allowed": True,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("Independent GLD106 B=0 C-open composition audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
