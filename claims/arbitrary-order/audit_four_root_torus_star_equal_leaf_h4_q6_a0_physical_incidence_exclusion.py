#!/usr/bin/env python3
"""Independent no-repository-import audit of candidate GLD105.

This audit imports neither the GLD105 primary nor any repository verifier.  It
uses an independently frozen source-pin manifest, checks the four theorem
interfaces directly, reconstructs the overloaded-H2 polynomial identity with
a tiny standard-library polynomial representation, and audits the exhaustive
two-branch implication and promotion gates.
"""

from __future__ import annotations

import ast
import hashlib
import json
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / (
    "GLD105_A0_H4_Q6_PHYSICAL_INCIDENCE_COMPOSITION_CERTIFICATE.json"
)
PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_"
    "a0_physical_incidence_exclusion.py"
)
GLD104_CERTIFICATE = BASE / "certificates" / (
    "GLD104_A0_P8_NONZERO_OFFSET_COMPOSITION_CERTIFICATE.json"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "6816d2ae686ae841664a92a761c6e4df484103e66b16d183e8a372c0f2b0361f"
)
EXPECTED_SOURCE_PINS = {
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_P8_NONZERO_OFFSET_CLOSURE_THEOREM.md": "a7ab76be0ccd3b65631464c683178156180329755ea0563cc135a7a51798526f",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_p8_nonzero_offset_closure.py": "80a77326fd4a74aeda206796f922d013c22affcd64258960d9cb68b5cb6e8e22",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_p8_nonzero_offset_closure.py": "3a26559327dc1dd633250ce9f4f896a80a0ac5550a5046fb63babef632eddbae",
    "claims/arbitrary-order/certificates/GLD104_A0_P8_NONZERO_OFFSET_COMPOSITION_CERTIFICATE.json": "7a68ae95177c50f96725849ca73f01fba5eba18a121e4500acf5d22a6dc282e5",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_P8_NONZERO_OFFSET_CLOSURE_REVIEW_2026-08-31.md": "b279e1f07aa39278cf000ada4f96433628a68a4c4bcae7760bb440a094bbe158",
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md": "f5fd49a6ff039f128f83b89bc3a7019c201001c54ba33223b2ac71e3e2289708",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py": "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py": "d41178a72731eff4d1d0eeb63d70224a58cea62b1f1336f0aa6d123120226e48",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_SIX_MINOR_OFFSET_EXCLUSION_REVIEW_2026-08-29.md": "1bd76cb185ea4acc8a49c4f41bf18d1cf1b88c501e1b74bbb1d4de4362344a6d",
    "tests/test_gld99_evidence_status.py": "38733a97e3257ed61ac542c0c798694c720e9b65274759558a63a8bb06f89d28",
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_EXCLUSION_THEOREM.md": "1c7074a3a6c6e740832f58c37757be8231f104fa8661c05476a516302e79e1c8",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py": "2eef9d94f251dce77b36f8d4dde479928d43087828583c3d59e52dae58c280a1",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_finite_common_minor_exclusion.py": "425ca5238bc86f566cfa370be78688d7232bf1a1da13358bb67a677c6db0778f",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_FINITE_COMMON_MINOR_EXCLUSION_REVIEW_2026-08-27.md": "e77ff35052b2ae6ccebcfea4aa0004d2764cf0d08c9f5d72f400be2f3913dba0",
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_THEOREM.md": "202c758ca9b7fcbf268f8ceefb425a0189cf3f7830a3a342d1546417fa103ff8",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py": "396b66f731f9d6ae67cc941fe77f57dfb09a9126c7231da4cd463264c4b9d991",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_at_most_six_syndrome_boundary_containment.py": "313f4902c5ca699612491c807d8768c511b87c8957213756f0a0e152fc4d8799",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_RANK_AT_MOST_SIX_SYNDROME_BOUNDARY_CONTAINMENT_REVIEW_2026-08-27.md": "07f1b7f0df8fb3cb1949aa5bca577f6809c382f466fe3e5688c10d30aa753e6b",
    "claims/arbitrary-order/four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json": "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57",
}

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


class AuditError(AssertionError):
    """Raised when the independent GLD105 audit fails closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def lf_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    require(b"\r" not in data, f"bare carriage return: {path}")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_frozen_inputs(payload: dict[str, Any]) -> None:
    require(lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256, "certificate")
    require(
        payload.get("source_pins_lf_sha256") == EXPECTED_SOURCE_PINS,
        "independent source-pin manifest",
    )
    for relative, expected in EXPECTED_SOURCE_PINS.items():
        path = ROOT / relative
        require(path.is_file(), f"missing source: {relative}")
        require(lf_sha256(path) == expected, f"source drift: {relative}")


def validate_candidate_status(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == 1, "schema")
    require(
        payload.get("certificate_id")
        == "GLD105-A0-H4-Q6-physical-incidence-parent-composition",
        "id",
    )
    require(
        payload.get("status")
        == "candidate_exact_scoped_characteristic_zero_composition",
        "status",
    )
    require(payload.get("global_conjecture") == "UNRESOLVED", "global")
    external = payload.get("external_consolidation", {})
    require(
        external
        == {
            "required_before_promotion": True,
            "candidate_commit": None,
            "candidate_tree": None,
            "request_event_id": None,
            "receipts": {},
            "status": "pending",
            "frontier_update_allowed": False,
            "theorem_ledger_update_allowed": False,
        },
        "external gate",
    )
    statement = payload["mathematical_scope"]["set_statement"]
    require("V(a,Q6)" in statement, "a=0 and Q6 scope")
    require("D(Omega*Delta)" in statement, "open scope")
    require(statement.endswith("= empty"), "emptiness conclusion")


def validate_interfaces_independently() -> dict[str, int]:
    required = {
        "GLD104": (
            "V(a,Q6) intersect D(H2*Delta)",
            "rank M(G)<=6",
            "is contained in {B=C=0}",
            "endpoint `B=C=0`",
        ),
        "GLD99": (
            "H2 = 2p^2-2p+1 = 0",
            "full GLD71 `37 x 9` syndrome has rank at most six",
            "corresponding rank-at-most-six incidence is empty on",
            "`D(Omega Delta)`",
        ),
        "GLD95": (
            "rational three-parameter family `F88`",
            "B intersect V(I_7(A)) intersect F88 intersect V(Q6)",
            "intersect D(Omega Delta) = empty",
            "The `H2` row requires a separate argument",
        ),
        "GLD86": (
            "C_8=1",
            "B=0 iff M(G)C=0",
            "rank A(z) = rank M(G)[:,0:8]",
            "column-replacement",
        ),
    }
    counts: dict[str, int] = {}
    for label, markers in required.items():
        text = OWNER_PATHS[label].read_text(encoding="utf-8")
        for marker in markers:
            require(marker in text, f"{label} marker: {marker}")
        require("UNRESOLVED" in text, f"{label} global fence")
        counts[label] = len(markers)

    gld104 = load_json(GLD104_CERTIFICATE)
    accepted = gld104.get("external_consolidation", {})
    require(accepted.get("status") == "accepted_2_of_2", "GLD104 accepted")
    require(
        accepted.get("receipts")
        == {
            "Juniper": "kgc_01M1BXV18D8NZQ22BDEXDXJWTP",
            "Mycelium": "kgc_01M1BYMJPC3VD2N7ENK20RXE3B",
        },
        "GLD104 mathematical-candidate receipts",
    )
    return counts


Poly = dict[tuple[int, int], int]


def add(left: Poly, right: Poly, scale: int = 1) -> Poly:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def multiply(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for (lp, lq), lc in left.items():
        for (rp, rq), rc in right.items():
            monomial = (lp + rp, lq + rq)
            result[monomial] = result.get(monomial, 0) + lc * rc
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def validate_h2_notation_without_sympy(payload: dict[str, Any]) -> dict[str, Poly]:
    one: Poly = {(0, 0): 1}
    p: Poly = {(1, 0): 1}
    q: Poly = {(0, 1): 1}
    d0 = add(add(p, q), one, scale=-1)
    s_numerator = add(add(p, q), multiply(p, q), scale=-1)
    cross_numerator = add(multiply(p, d0), s_numerator, scale=-1)
    L1: Poly = {(2, 0): 1, (1, 1): 2, (1, 0): -2, (0, 1): -1}
    H2deg: Poly = {(2, 0): 2, (1, 0): -2, (0, 0): 1}
    require(cross_numerator == L1, "(p-s)*d0=L1")
    require(H2deg != L1, "H2deg differs from GLD86 collision divisor")

    notation = payload["notation_fences"]
    require(notation["H2deg"].startswith("2*p^2-2*p+1"), "H2deg text")
    require(notation["GLD86_H2_collision"].startswith("p-s=L1/"), "collision text")
    require("not the scalar offset B" in notation["B_incidence"], "B overload")
    require("not the scalar offset C" in notation["C_center"], "C overload")
    return {"H2deg": H2deg, "L1": L1}


def validate_implication_truth_table(payload: dict[str, Any]) -> dict[str, str]:
    split = payload["case_split"]
    require(split["exhaustive_cases"] == ["H2deg!=0", "H2deg=0"], "case list")
    outcomes: dict[str, str] = {}
    for zero in (True, False):
        if zero:
            branch = split["H2deg_zero"]
            require(branch["handler"] == "GLD99", "zero handler")
            require("arbitrary a" in branch["scope"], "a=0 specialization")
            outcomes["zero"] = "GLD99 contradiction"
        else:
            branch = split["H2deg_open"]
            chain = (
                branch["upstream_incidence_bridge"],
                branch["offset_handler"],
                branch["endpoint_handler"],
            )
            require(chain == ("GLD75/GLD86", "GLD104", "GLD95"), "open chain")
            require(branch["offset_conclusion"] == "B_offset=C_offset=0", "endpoint identification")
            outcomes["nonzero"] = "GLD86 -> GLD104 -> GLD95 contradiction"
    require(set(outcomes) == {"zero", "nonzero"}, "truth-table exhaustion")
    return outcomes


def validate_primary_independence_boundary() -> list[str]:
    source = PRIMARY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    require(not any("verify_four_root" in name for name in imports), "primary repository import")
    require("importlib" not in imports, "primary dynamic import")
    require("load_module" not in source, "primary module execution")
    return sorted(imports)


def check() -> dict[str, Any]:
    started = time.monotonic()
    payload = load_json(CERTIFICATE)
    validate_frozen_inputs(payload)
    validate_candidate_status(payload)
    markers = validate_interfaces_independently()
    polynomials = validate_h2_notation_without_sympy(payload)
    outcomes = validate_implication_truth_table(payload)
    imports = validate_primary_independence_boundary()
    return {
        "status": "independent_candidate_GLD105_composition_audit_pass",
        "global_conjecture": "UNRESOLVED",
        "source_pins_checked": len(EXPECTED_SOURCE_PINS),
        "interface_marker_counts": markers,
        "H2deg_terms": len(polynomials["H2deg"]),
        "GLD86_L1_terms": len(polynomials["L1"]),
        "H2_notations_distinct": True,
        "case_outcomes": outcomes,
        "primary_imports": imports,
        "repository_verifiers_imported_or_executed": 0,
        "external_consolidation": "pending",
        "frontier_or_ledger_promotion_allowed": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("Independent GLD105 physical-incidence composition audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
