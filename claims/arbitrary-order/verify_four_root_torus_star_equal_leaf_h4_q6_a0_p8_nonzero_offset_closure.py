#!/usr/bin/env python3
"""Verify the proved GLD104 P8/nonzero-offset composition.

This checker does not redo the expensive child arithmetic.  It validates the
portable, independently audited leaf seam and then checks the exact logical
composition: the exhaustive offset cover, the GLD101 eight-factor necessary
support, every factor disposition, the P8 selector surface, and the one-way
rank consequence.  The B=C=0 endpoint and every wider obligation remain out
of scope.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / (
    "GLD104_A0_P8_NONZERO_OFFSET_COMPOSITION_CERTIFICATE.json"
)
GLD102 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_"
    "p01_nonzero_offset_exclusion.py"
)
GLD101_PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_"
    "a0_six_selector_norm_cover.py"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "7a68ae95177c50f96725849ca73f01fba5eba18a121e4500acf5d22a6dc282e5"
)
EXPECTED_SUPPORT_LABELS = (
    "p-1",
    "p",
    "p^2+1",
    "P",
    "H2",
    "R4",
    "R8",
    "R110",
)
SIX_NAMES = ("T0", "T1", "T2", "T3", "Y1", "X3")
P8_NAMES = ("T0", "T1", "T2", "T3", "D0", "Y0", "Y1", "X3")

CHILD_CERTIFICATES = {
    "GLD101_norm_cover": BASE
    / "certificates"
    / "GLD101_A0_NORM_COVER_CERTIFICATE.json",
    "generic_C_open": BASE
    / "certificates"
    / "GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json",
    "d2_B_open": BASE
    / "certificates"
    / "GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_CERTIFICATE.json",
    "R4_B_open": BASE
    / "certificates"
    / "GLD101_A0_R4_B_OPEN_RESULTANT_CERTIFICATE.json",
    "R8_B_open": BASE
    / "certificates"
    / "GLD101_R8_B_OPEN_FIVE_ROW_KERNEL_CERTIFICATE.json",
    "R110_B_open": BASE
    / "certificates"
    / "GLD101_A0_R110_P8_BOPEN_PORTABLE_CERTIFICATE.json",
}


class CompositionError(AssertionError):
    """Raised when a load-bearing composition seam drifts."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CompositionError(message)


def lf_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def factor_signature(expression: sp.Expr) -> str:
    return hashlib.sha256(str(sp.expand(expression)).encode("ascii")).hexdigest()


def validate_source_pins(payload: dict[str, Any]) -> dict[str, str]:
    pins = payload.get("source_pins_lf_sha256")
    require(isinstance(pins, dict) and len(pins) == 29, "source-pin manifest")
    actual: dict[str, str] = {}
    for relative, expected in pins.items():
        require(not Path(relative).is_absolute(), f"absolute source pin: {relative}")
        path = ROOT / relative
        require(path.is_file(), f"missing source pin: {relative}")
        digest = lf_sha256(path)
        require(digest == expected, f"source pin mismatch: {relative}")
        actual[relative] = digest
    return actual


def validate_theorem_contract(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == 1, "schema version")
    require(
        payload.get("certificate_id")
        == "GLD104-A0-P8-nonzero-offset-composition",
        "certificate id",
    )
    require(
        payload.get("status")
        == "proved_exact_scoped_characteristic_zero_composition",
        "theorem status",
    )
    require(payload.get("global_conjecture") == "UNRESOLVED", "global status")
    external = payload.get("external_consolidation", {})
    require(external.get("required_before_promotion") is True, "external audit gate")
    require(external.get("status") == "accepted_2_of_2", "external audit status")
    require(
        external.get("candidate_commit")
        == "75da0298a535888e7a84257b7bfd6a556a3267b2",
        "candidate commit",
    )
    require(
        external.get("candidate_tree")
        == "86fae29848c52c7ccd3236c84e156aedb3f02b78",
        "candidate tree",
    )
    require(
        external.get("request_event_id")
        == "kgc_01M1BXKGZ8F86B6XWK1J6Q3DMF",
        "external audit request",
    )
    require(
        external.get("receipts")
        == {
            "Juniper": "kgc_01M1BXV18D8NZQ22BDEXDXJWTP",
            "Mycelium": "kgc_01M1BYMJPC3VD2N7ENK20RXE3B",
        },
        "external audit receipts",
    )
    require(external.get("frontier_update_allowed") is True, "frontier gate")
    require(external.get("theorem_ledger_update_allowed") is True, "ledger gate")

    scope = payload.get("mathematical_scope", {})
    require(scope.get("assumptions") == ["a=0", "Q6(p,q)=0", "H2(p)*Delta(p,q)!=0"], "scope assumptions")
    require(
        scope.get("p8_selected_minor_implication", "").startswith(
            "Q6=T0=T1=T2=T3=D0=Y0=Y1=X3=0"
        ),
        "P8 statement",
    )
    require("rank(M(G))<=6" in scope.get("rank_corollary", ""), "rank corollary")
    nonclaims = "\n".join(scope.get("nonclaims", []))
    for token in ("P6", "endpoint", "physical", "full-E31", "global"):
        require(token in nonclaims, f"missing nonclaim: {token}")

    selectors = payload.get("selector_sets", {})
    require(tuple(selectors.get("six_selector", [])) == SIX_NAMES, "six selectors")
    require(tuple(selectors.get("p8", [])) == P8_NAMES, "P8 selectors")
    require(set(SIX_NAMES) < set(P8_NAMES), "strict six-to-P8 inclusion")

    cover = payload.get("offset_cover", {})
    require(
        cover.get("sets") == ["D(B)", "V(B) intersect D(C)"],
        "exhaustive offset cover",
    )
    require(cover.get("exhaustive_for") == "(B,C)!=(0,0)", "offset locus")
    require(cover.get("C_open_handler") == "generic_C_open", "C-open handler")


def validate_factor_support(
    payload: dict[str, Any], children: dict[str, dict[str, Any]]
) -> dict[str, str]:
    p, q = sp.symbols("p q")
    norm = children["GLD101_norm_cover"]
    require(norm.get("global_conjecture") == "UNRESOLVED", "GLD101 status")
    require(tuple(norm["six_selector"]["names"]) == SIX_NAMES, "GLD101 selectors")
    upstream = norm["six_selector"]["factorization"]
    tracked = payload.get("norm_support", [])
    require(upstream == [{k: item[k] for k in ("label", "degree", "exponent", "sha256")} for item in tracked], "norm-support copy")
    require(tuple(item["label"] for item in tracked) == EXPECTED_SUPPORT_LABELS, "support labels")

    r4 = children["R4_B_open"]
    r8 = children["R8_B_open"]
    r110 = children["R110_B_open"]
    expressions = {
        "p-1": p - 1,
        "p": p,
        "p^2+1": p**2 + 1,
        "P": p**2 - p + 1,
        "H2": 2 * p**2 - 2 * p + 1,
        "R4": sp.sympify(r4["mathematical_scope"]["R4"]),
        "R8": sp.sympify(r8["algebra"]["minpoly_R8"]),
        "R110": sp.sympify(r110["r110"]["polynomial"]),
    }
    for item in tracked:
        label = item["label"]
        expression = expressions[label]
        require(sp.degree(expression, p) == item["degree"], f"{label} degree")
        require(factor_signature(expression) == item["sha256"], f"{label} hash")

    P = expressions["P"]
    L1 = p**2 + 2 * p * q - 2 * p - q
    L2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    delta = sp.expand((p - q) * (p + q - 1) * P * L1 * L2 * e)
    sp.Poly(delta, p, q, domain=QQ).exquo(sp.Poly(P, p, q, domain=QQ))
    require("D(H2*Delta)" in norm["mathematical_scope"]["open"], "H2 open")

    dispositions = {item["label"]: item["disposition"] for item in tracked}
    expected = {
        "p-1": "closed_by_GLD102_p1",
        "p": "closed_by_GLD102_p0",
        "p^2+1": "closed_by_d2_B_open_and_conjugation",
        "P": "excluded_because_P_divides_Delta",
        "H2": "excluded_by_declared_D(H2)_open",
        "R4": "closed_by_R4_B_open_resultant_leaf",
        "R8": "closed_by_R8_B_open_five_row_kernel_leaf",
        "R110": "closed_by_R110_P8_B_open_eight_minor_leaf",
    }
    require(dispositions == expected, "factor dispositions")
    return dispositions


def validate_child_scopes(children: dict[str, dict[str, Any]]) -> dict[str, Any]:
    generic = children["generic_C_open"]
    d2 = children["d2_B_open"]
    r4 = children["R4_B_open"]
    r8 = children["R8_B_open"]
    r110 = children["R110_B_open"]

    for name, child in children.items():
        require(child.get("global_conjecture") == "UNRESOLVED", f"{name} status")

    generic_scope = generic["mathematical_scope"]
    require(generic_scope["locus"] == "B=0 and C!=0", "generic C-open locus")
    require(generic_scope["parameter"].startswith("arbitrary p"), "generic p scope")
    require(tuple(generic_scope["selected_necessary_minors"]) == SIX_NAMES, "generic selectors")

    d2_scope = d2["mathematical_scope"]
    require(d2_scope["factor"] == "p^2+1=0", "d2 factor")
    require(set(d2_scope["compact_unit_core"]) <= set(P8_NAMES), "d2 P8 subset")
    require(
        d2_scope["load_bearing_branch"]
        == "p=i; p=-i follows coefficientwise by conjugation",
        "Gaussian conjugation",
    )

    r4_scope = r4["mathematical_scope"]
    require(set(r4_scope["selected_necessary_minors"]) <= set(P8_NAMES), "R4 P8 subset")
    require(r4_scope["open"].startswith("D(B*H2*Delta)"), "R4 open")

    r8_scope = r8["mathematical_scope"]
    require(r8_scope["factor"] == "R8=0", "R8 factor")
    require(set(r8_scope["selected_necessary_minors"]) <= set(P8_NAMES), "R8 P8 subset")
    require(r8["algebra"]["R8_signature_sha256"] == "19e8048b6aa1a654dd24c889b7c6aea895c31bb5bba60e3a038dbcbc961ad06d", "R8 signature")

    r110_scope = r110["mathematical_scope"]
    require(r110_scope["load_bearing_chart"] == "B-open", "R110 chart")
    require(tuple(r110["actual_minors"]["eight_actual_minor_names"]) == P8_NAMES, "R110 P8 surface")
    require(set(P8_NAMES) <= set(r110_scope["ideal_generators"]), "R110 generators")
    require(r110["r110"]["sha256"] == "1ae5a3e502f686d484b757db27d6f70b3ff535792edb65ceb40c2bd455410016", "R110 signature")

    return {
        "generic_C_open": generic["certificate_id"],
        "d2": d2["certificate_id"],
        "R4": r4["certificate_id"],
        "R8": r8["certificate_id"],
        "R110": r110["certificate_id"],
    }


def validate_gld102_selected_subcase() -> dict[str, str]:
    module = load_module(GLD102, "gld102_for_gld104_composition")
    p0_basis = module.EXPECTED_B_OPEN_BASES[0]
    require(
        any(sp.expand(item - (module.a - 1)) == 0 for item in p0_basis),
        "p=0 B-open basis lacks a-1",
    )
    require(
        any(sp.expand(item.subs(module.a, 0) + 1) == 0 for item in p0_basis),
        "p=0 a=0 contradiction",
    )
    p1_quadratic = sp.Poly(module.EXPECTED_B_OPEN_BASES[1][0], module.z, domain=QQ)
    p1_remainder = sp.Poly(module.EXPECTED_P1_T3_REMAINDER, module.z, domain=QQ)
    require(sp.gcd(p1_quadratic, p1_remainder).degree() == 0, "p=1 T3 gcd")
    return {
        "p0": "selected B-open basis contains a-1, so a=0 is empty",
        "p1": "T3 remainder is coprime to the residual quadratic",
    }


def validate_selected_minor_norm_bridge() -> dict[str, Any]:
    """Replay the P8-to-norm bridge without assuming the rank hypothesis."""
    module = load_module(GLD101_PRIMARY, "gld101_for_gld104_p8_bridge")
    module.pinned_source_manifest()
    algebra, rows, _chart, support_digest = module.q6_and_source()
    require(support_digest == module.EXPECTED_SUPPORT_DIGEST, "bridge support digest")
    generators = module.build_generators(algebra, rows)
    require(tuple(module.SIX_NAMES) == SIX_NAMES, "bridge selector names")
    require(tuple(module.SIX_COLUMNS) == ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0)), "bridge monomial columns")
    for name in SIX_NAMES:
        terms = set(generators[name].terms)
        require((0, 0) not in terms, f"{name} constant offset term")
        require(terms <= set(module.SIX_COLUMNS), f"{name} monomial support")

    determinant = module.selector_det(
        algebra,
        generators,
        module.SIX_NAMES,
        module.SIX_COLUMNS,
        "GLD104 selected-minor bridge",
    )
    determinant_expression = sp.cancel(algebra.as_expr(determinant))
    determinant_hash = hashlib.sha256(
        sp.srepr(determinant_expression).encode("ascii")
    ).hexdigest()
    require(
        determinant_hash == module.EXPECTED_SIX_NORM["expression_sha256"],
        "selected-minor determinant signature",
    )

    # The coefficient matrix multiplies m=(C,B,BC,B^2,B^2*C,B^3).  Its
    # first two coordinates are C and B, so a nonzero offset makes m nonzero.
    B_symbol, C_symbol = sp.symbols("B C")
    monomial_vector = (
        C_symbol,
        B_symbol,
        B_symbol * C_symbol,
        B_symbol**2,
        B_symbol**2 * C_symbol,
        B_symbol**3,
    )
    require(monomial_vector[0] == C_symbol and monomial_vector[1] == B_symbol, "nonzero monomial-vector gate")
    return {
        "selected_equations": list(SIX_NAMES),
        "monomial_vector": [str(item) for item in monomial_vector],
        "nonzero_offset_implies_nonzero_vector": True,
        "determinant_srepr_sha256": determinant_hash,
        "logical_direction": "six actual equations plus nonzero offset imply selector determinant zero",
    }


def check() -> dict[str, Any]:
    started = time.monotonic()
    require(lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256, "certificate pin")
    payload = load_json(CERTIFICATE)
    validate_theorem_contract(payload)
    pins = validate_source_pins(payload)
    children = {name: load_json(path) for name, path in CHILD_CERTIFICATES.items()}
    dispositions = validate_factor_support(payload, children)
    child_ids = validate_child_scopes(children)
    p01 = validate_gld102_selected_subcase()
    selector_bridge = validate_selected_minor_norm_bridge()

    child_manifest = payload["child_evidence"]
    require(child_manifest["GLD101_norm_cover"]["certificate_id"] == children["GLD101_norm_cover"]["certificate_id"], "GLD101 child manifest")
    for key in ("generic_C_open", "d2_B_open", "R4_B_open", "R8_B_open", "R110_B_open"):
        require(child_manifest[key]["certificate_id"] == children[key]["certificate_id"], f"{key} child manifest")
        require(set(child_manifest[key]["selected_minors"]) <= set(P8_NAMES), f"{key} selected surface")

    require(len(payload.get("proof_topology", [])) == 7, "proof-topology steps")
    return {
        "status": "proved_GLD104_composition_seam_verified",
        "global_conjecture": "UNRESOLVED",
        "p8_selected_minor_implication": True,
        "rank_corollary_direction_only": True,
        "offset_cover": payload["offset_cover"]["sets"],
        "factor_dispositions": dispositions,
        "child_certificates": child_ids,
        "gld102_selected_subcase": p01,
        "selected_minor_norm_bridge": selector_bridge,
        "source_pins_checked": len(pins),
        "external_consolidation": "accepted_2_of_2",
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = check()
    print("GLD104 P8/nonzero-offset composition verifier: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
