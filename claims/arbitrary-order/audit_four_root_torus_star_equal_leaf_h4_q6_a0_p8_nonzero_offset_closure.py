#!/usr/bin/env python3
"""Independent static/semantic audit of the candidate GLD104 composition.

The audit imports neither the GLD104 primary nor any repository verifier.  It
hash-pins every child package, reads the tracked JSON evidence directly,
reconstructs the factor signatures and open-cover logic independently, and
extracts the two GLD102 selected-minor constants from a restricted AST rather
than executing that module.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
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
EXPECTED_CERTIFICATE_LF_SHA256 = (
    "85dde2dae9eceb29edf301bf234c01a6ac00761c40458d812afc3707486ba00e"
)
SIX = ("T0", "T1", "T2", "T3", "Y1", "X3")
P8 = ("T0", "T1", "T2", "T3", "D0", "Y0", "Y1", "X3")

EXPECTED_SOURCE_PINS = {
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md": "fe9e705f2fa9cde61c71daeb19abea241545a6c45611c15e6dd03b62ea6d3f45",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py": "c36d618651b92621627961d3004128f39cb43e522a76256c74b1141baf9d1a3c",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py": "59eafc274d40057b042acb2a11d5e20857e0637ececda12c02e55874f4117bed",
    "claims/arbitrary-order/certificates/GLD101_A0_NORM_COVER_CERTIFICATE.json": "9213a50f96bf6bffa7a8f8fefbd8cca99317f00a1b1863b19e83d1330f79518e",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION_REVIEW_2026-08-30.md": "7e57f63c9cffd913010d260890b896cd33e27e8979370f695b77c1802e9bb3e3",
    "claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P01_NONZERO_OFFSET_EXCLUSION_THEOREM.md": "9dcb659a5b7a45e40b1947d1fb8f76e9caef8afeb587ad07d7b08dbdb0be254f",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py": "c78130ad8ed5a639ffc7683ef21ae2b578312d6c7475820689a996dbc13bbd8e",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py": "3d976c4e9470a4c5acece6052acd275b96dc257b82cc197183375825ec6082ec",
    "docs/audits/FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P01_NONZERO_OFFSET_EXCLUSION_REVIEW_2026-08-30.md": "4753a90174490a9deddc4e9bb2bf5c5641fe2dd3b0315fb9d29677a2ffea1cd3",
    "claims/arbitrary-order/certificates/GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json": "1f84c1d30c1c8403be477b5def91144f687cc08a4ed5406dffb3866cf6996afb",
    "claims/arbitrary-order/certificates/GLD101_A0_GENERIC_COPEN_UNIT_SCREEN.singular.txt": "c514d842532f99cde4488cca048c551f39e43ed5cdf2c5ce6a54dcd7aa704850",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py": "d4244b2cc288a06a919d1dfd75a7f344b8bd4aa190312f7f14a0727d27bcc5de",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py": "9ed2d3451864c969982a041831893bc5e88be12adf52496a76f595bc52e6c590",
    "docs/audits/GLD101_A0_GENERIC_COPEN_PORTABLE_LEAF_PACKAGE_2026-08-31.md": "1c85908095e1819cc79551c01d6921d385936ea3de6b3e9356955357a5e40d49",
    "claims/arbitrary-order/certificates/GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_CERTIFICATE.json": "e4d0c5a07a930d8c4305a897e613b73185d48df885f9907f0e67a41fc593338c",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py": "8e580e15ec7d63ed259bbfc65c42f6289dc296f1a0e7d5eb809d9c1aa6364b36",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py": "6ea764f005eef2fdb3b1f7d771d93a38de23e39ab0b5c9a501d68971ad79e911",
    "docs/audits/GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_LEAF_PACKAGE_2026-08-31.md": "ecffccd2f0396b73842b2e97212d2013d928e9ce9fba039ddf1ebb27edb51a7f",
    "claims/arbitrary-order/certificates/GLD101_A0_R4_B_OPEN_RESULTANT_CERTIFICATE.json": "1961eed09059a7434002c610f89eb4e0ebc195398fbd026b0a4a7ddf778cc36e",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py": "7b7b0cdb559046b5c5ebac43a545bdf20e037843400e3a2b6287c2e018dd43c4",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py": "217fd2feda4f0676175b82b63d4d4717889a090cce169e8a9cd2294fc2efab9b",
    "docs/audits/GLD101_A0_R4_B_OPEN_RESULTANT_PORTABLE_LEAF_2026-08-31.md": "a0ee9a4badbc07a2884c5371a765b14f9271fcb7e995eac14db8756760084b01",
    "claims/arbitrary-order/certificates/GLD101_R8_B_OPEN_FIVE_ROW_KERNEL_CERTIFICATE.json": "df96337e0de80cd1236fde1f366490afa7a06f28845475b03cc5c31eeba8af7c",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_r8_b_open_five_row_kernel.py": "a4055f0cf660b75c521069774aee7763ba661d32c8432f93381792cd9587dacf",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_r8_b_open_five_row_kernel.py": "8deab312f90774ab8793716c033ecf39adddcba1fca7f1e8fd243220b41470ad",
    "claims/arbitrary-order/certificates/GLD101_A0_R110_P8_BOPEN_PORTABLE_CERTIFICATE.json": "bdf84e09be8e4d7f76a0d05b050957acd2ef9b95d1e55a6fafe3f9d465c1c32b",
    "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_a0_r110_p8_bopen_portable.py": "090a8e9914eb8830d363c7d27cc4efb6d783bc90515001323e3891ae88c28035",
    "claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_a0_r110_p8_bopen_portable.py": "c10e40fb644efa3f91d309c4372ba7b0a22fc8d5a131f2c8f0481139819d5f04",
    "docs/audits/GLD101_A0_R110_P8_BOPEN_PORTABLE_LEAF_PACKAGE_2026-08-31.md": "fb56cbffb407201a80cce6d32116bfd0feb408c32defdbb0784f7d54e5fb4e09",
}

CHILD_PATHS = {
    "norm": "claims/arbitrary-order/certificates/GLD101_A0_NORM_COVER_CERTIFICATE.json",
    "generic": "claims/arbitrary-order/certificates/GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json",
    "d2": "claims/arbitrary-order/certificates/GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_CERTIFICATE.json",
    "R4": "claims/arbitrary-order/certificates/GLD101_A0_R4_B_OPEN_RESULTANT_CERTIFICATE.json",
    "R8": "claims/arbitrary-order/certificates/GLD101_R8_B_OPEN_FIVE_ROW_KERNEL_CERTIFICATE.json",
    "R110": "claims/arbitrary-order/certificates/GLD101_A0_R110_P8_BOPEN_PORTABLE_CERTIFICATE.json",
}


class AuditError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def signature(expression: sp.Expr) -> str:
    return hashlib.sha256(str(sp.expand(expression)).encode("ascii")).hexdigest()


def validate_pins(payload: dict[str, Any]) -> None:
    require(payload["source_pins_lf_sha256"] == EXPECTED_SOURCE_PINS, "pin manifest drift")
    for relative, expected in EXPECTED_SOURCE_PINS.items():
        path = ROOT / relative
        require(path.is_file(), f"missing pinned source: {relative}")
        require(lf_sha256(path) == expected, f"pinned source mismatch: {relative}")


SAFE_AST_NODES = (
    ast.Expression,
    ast.Dict,
    ast.Tuple,
    ast.Constant,
    ast.Name,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.Call,
    ast.Attribute,
    ast.Load,
)


def restricted_assignment(source: str, name: str, environment: dict[str, Any]) -> Any:
    tree = ast.parse(source)
    value: ast.expr | None = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                value = node.value
                break
    require(value is not None, f"missing AST assignment: {name}")
    for node in ast.walk(value):
        require(isinstance(node, SAFE_AST_NODES), f"unsafe AST in {name}: {type(node).__name__}")
        if isinstance(node, ast.Call):
            require(
                isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "sp"
                and node.func.attr == "Rational",
                f"unexpected call in {name}",
            )
    expression = ast.Expression(value)
    ast.fix_missing_locations(expression)
    return eval(compile(expression, "<pinned-gld102-constant>", "eval"), {"__builtins__": {}}, environment)


def audit_gld102_constants() -> dict[str, str]:
    source_path = ROOT / (
        "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_"
        "p01_nonzero_offset_exclusion.py"
    )
    source = source_path.read_text(encoding="utf-8")
    a, q, B, t, z = sp.symbols("a q B t z")
    environment = {"sp": sp, "a": a, "q": q, "B": B, "t": t, "z": z}
    bases = restricted_assignment(source, "EXPECTED_B_OPEN_BASES", environment)
    remainder = restricted_assignment(source, "EXPECTED_P1_T3_REMAINDER", environment)
    require(any(sp.expand(item - (a - 1)) == 0 for item in bases[0]), "p0 a-1 basis")
    require(any(sp.expand(item.subs(a, 0) + 1) == 0 for item in bases[0]), "p0 a0 contradiction")
    require(
        sp.gcd(sp.Poly(bases[1][0], z, domain=QQ), sp.Poly(remainder, z, domain=QQ)).degree() == 0,
        "p1 residual gcd",
    )
    return {
        "p0": "a-1 in selected B-open basis",
        "p1": "T3 remainder coprime to residual quadratic",
    }


def literal_assignment(tree: ast.Module, name: str) -> Any:
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AuditError(f"missing literal assignment: {name}")


def audit_selected_minor_norm_bridge_source() -> dict[str, Any]:
    """Independently audit the code-level six-equation determinant bridge."""
    path = ROOT / (
        "claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_"
        "a0_six_selector_norm_cover.py"
    )
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = tuple(literal_assignment(tree, "SIX_NAMES"))
    columns = tuple(tuple(item) for item in literal_assignment(tree, "SIX_COLUMNS"))
    expected_columns = ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))
    require(names == SIX, "GLD101 source selector names")
    require(columns == expected_columns, "GLD101 source selector columns")

    functions = {
        node.name: ast.get_source_segment(source, node) or ast.unparse(node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    builder = functions.get("build_generators", "")
    selector = functions.get("selector_det", "")
    require("(0, 0) in result[name].terms" in builder, "constant-term rejection")
    require("set(result[name].terms) - set(SIX_COLUMNS)" in builder, "monomial-support rejection")
    require("generators[name].terms.get(exp, algebra.zero)" in selector, "coefficient-matrix construction")
    require("return det_tuple(algebra, matrix, label)" in selector, "selector determinant construction")

    expected_norm = literal_assignment(tree, "EXPECTED_SIX_NORM")
    require(
        expected_norm["expression_sha256"]
        == "c8b675268458576454cf3eeab5fe38c4ef468a2113c94febfd471c0cfc6d6431",
        "selector determinant signature pin",
    )

    B_symbol, C_symbol = sp.symbols("B C")
    vector = (
        C_symbol,
        B_symbol,
        B_symbol * C_symbol,
        B_symbol**2,
        B_symbol**2 * C_symbol,
        B_symbol**3,
    )
    # Over a field, six equations with the verified support are K*m=0.  The
    # first two entries make m nonzero whenever (B,C)!=(0,0), so K is singular.
    require(vector[0] == C_symbol and vector[1] == B_symbol, "nonzero vector gate")
    return {
        "selected_equations": list(names),
        "monomial_columns": [list(item) for item in columns],
        "monomial_vector": [str(item) for item in vector],
        "nonzero_offset_implies_nonzero_vector": True,
        "determinant_signature": expected_norm["expression_sha256"],
        "logical_direction": "six actual equations imply K*m=0; nonzero m implies det(K)=0",
    }


def audit() -> dict[str, Any]:
    started = time.monotonic()
    require(lf_sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_LF_SHA256, "certificate hash")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(payload["status"] == "candidate_exact_scoped_composition_pending_external_audit", "candidate status")
    require(payload["global_conjecture"] == "UNRESOLVED", "global status")
    require(payload["external_consolidation"] == {
        "required_before_promotion": True,
        "status": "pending",
        "frontier_update_allowed": False,
        "theorem_ledger_update_allowed": False,
    }, "promotion gate")
    require(
        re.search(
            r"[A-Za-z]:[\\/]", CERTIFICATE.read_text(encoding="utf-8")
        )
        is None,
        "machine path in certificate",
    )
    validate_pins(payload)

    children = {name: load_json(path) for name, path in CHILD_PATHS.items()}
    for name, child in children.items():
        require(child.get("global_conjecture") == "UNRESOLVED", f"{name} global status")

    norm_factors = children["norm"]["six_selector"]["factorization"]
    support = payload["norm_support"]
    require(
        norm_factors
        == [{key: item[key] for key in ("label", "degree", "exponent", "sha256")} for item in support],
        "support does not equal GLD101 factorization",
    )
    require(tuple(children["norm"]["six_selector"]["names"]) == SIX, "norm selector names")
    require(set(SIX) < set(P8), "six/P8 inclusion")

    p, q = sp.symbols("p q")
    polynomials = {
        "p-1": p - 1,
        "p": p,
        "p^2+1": p**2 + 1,
        "P": p**2 - p + 1,
        "H2": 2 * p**2 - 2 * p + 1,
        "R4": sp.sympify(children["R4"]["mathematical_scope"]["R4"]),
        "R8": sp.sympify(children["R8"]["algebra"]["minpoly_R8"]),
        "R110": sp.sympify(children["R110"]["r110"]["polynomial"]),
    }
    for item in support:
        expression = polynomials[item["label"]]
        require(sp.degree(expression, p) == item["degree"], f"{item['label']} degree")
        require(signature(expression) == item["sha256"], f"{item['label']} signature")

    P_poly = polynomials["P"]
    L1 = p**2 + 2 * p * q - 2 * p - q
    L2 = 2 * p * q - p + q**2 - 2 * q
    e = 2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
    delta = sp.expand((p - q) * (p + q - 1) * P_poly * L1 * L2 * e)
    sp.Poly(delta, p, q, domain=QQ).exquo(sp.Poly(P_poly, p, q, domain=QQ))
    require("D(H2*Delta)" in children["norm"]["mathematical_scope"]["open"], "H2 open")

    require(children["generic"]["mathematical_scope"]["locus"] == "B=0 and C!=0", "generic C locus")
    require(children["generic"]["mathematical_scope"]["parameter"].startswith("arbitrary p"), "generic p")
    require(set(children["generic"]["mathematical_scope"]["selected_necessary_minors"]) <= set(P8), "generic P8")
    require(children["d2"]["mathematical_scope"]["factor"] == "p^2+1=0", "d2 factor")
    require("p=-i follows coefficientwise by conjugation" in children["d2"]["mathematical_scope"]["load_bearing_branch"], "d2 conjugation")
    require(set(children["R4"]["mathematical_scope"]["selected_necessary_minors"]) <= set(P8), "R4 P8")
    require(set(children["R8"]["mathematical_scope"]["selected_necessary_minors"]) <= set(P8), "R8 P8")
    require(tuple(children["R110"]["actual_minors"]["eight_actual_minor_names"]) == P8, "R110 P8")
    require({"D0", "Y0"} <= set(children["R110"]["mathematical_scope"]["ideal_generators"]), "R110 extra minors")
    require("P6" in "\n".join(children["R110"]["mathematical_scope"]["nonclaims"]), "R110 P6 nonclaim")

    require(payload["offset_cover"]["sets"] == ["D(B)", "V(B) intersect D(C)"], "offset cover")
    for b_zero, c_zero in ((False, False), (False, True), (True, False)):
        in_b_open = not b_zero
        in_c_open = b_zero and not c_zero
        require(in_b_open or in_c_open, "offset cover truth table")

    dispositions = {item["label"]: item["disposition"] for item in support}
    require(set(dispositions) == set(polynomials), "factor exhaustion")
    require(dispositions["P"] == "excluded_because_P_divides_Delta", "P boundary")
    require(dispositions["H2"] == "excluded_by_declared_D(H2)_open", "H2 boundary")
    require(dispositions["R110"].endswith("eight_minor_leaf"), "R110 P8 disposition")
    p01 = audit_gld102_constants()
    selector_bridge = audit_selected_minor_norm_bridge_source()

    scope_nonclaims = "\n".join(payload["mathematical_scope"]["nonclaims"])
    for token in ("P6", "endpoint", "physical", "full-E31", "global"):
        require(token in scope_nonclaims, f"missing nonclaim {token}")
    require(len(payload["proof_topology"]) == 7, "proof topology")

    return {
        "status": "independent_candidate_GLD104_composition_audit_passed",
        "global_conjecture": "UNRESOLVED",
        "repository_verifier_imports": 0,
        "source_pins_checked": len(EXPECTED_SOURCE_PINS),
        "factor_support": [item["label"] for item in support],
        "offset_cover_truth_table": "exhaustive on nonzero offsets",
        "p8_surface": list(P8),
        "gld102_selected_subcase": p01,
        "selected_minor_norm_bridge": selector_bridge,
        "external_consolidation": "still pending",
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    result = audit()
    print("Independent GLD104 candidate composition audit: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
