from __future__ import annotations

import ast
import hashlib
import importlib.util
import inspect
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
OWNER = BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION.md"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_a0_six_selector_norm_cover.py"
MANIFEST = BASE / "certificates" / "GLD101_A0_NORM_COVER_CERTIFICATE.json"
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_SIX_SELECTOR_NORM_COVER_REDUCTION_"
    "REVIEW_2026-08-30.md"
)
LEDGER = ROOT / "catalog" / "theorem-ledger.json"

GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
GLD99 = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py"

SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
SUPPORT_DIGEST = "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
Q6_SREPR_SHA256 = "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"
CERTIFICATE_SHA256 = "9213a50f96bf6bffa7a8f8fefbd8cca99317f00a1b1863b19e83d1330f79518e"

CANONICAL_SOURCE_LF_HASHES = {
    "GLD71": "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    "GLD88": "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    "GLD99": "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
}

EVIDENCE_SHA256 = {MANIFEST: CERTIFICATE_SHA256}

SELECTOR_ROWS_AND_COLUMNS = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}

FACTOR_SIGNATURE = [
    ("p-1", 1, 36, "fba95ee7da505d8883744a06a8933df8d8d7c4ac2cca316e4990626e92a17fed"),
    ("p", 1, 98, "148de9c5a7a44d19e56cd9ae1a554bf67847afb0c58f6e12fa29ac7ddfca9940"),
    ("p^2+1", 2, 2, "fae3e839d66db547d5697d6fa1a88aa81dfecd3e360d46204801b3b420f3d40b"),
    ("P", 2, 43, "ace5cff9ef6fef5a8a62e0a4bd98c3482a066949f3970663a5e446dae97247ca"),
    ("H2", 2, 99, "eeba65c990e66c56329c3f9ddd1b7623f5b84b11683828352e0cd96b0a928bf9"),
    ("R4", 4, 2, "59d876136007e0f768ece9df63d326ef21471d26d69a676013fb0eedab51c9eb"),
    ("R8", 8, 1, "19e8048b6aa1a654dd24c889b7c6aea895c31bb5bba60e3a038dbcbc961ad06d"),
    ("R110", 110, 1, "1ae5a3e502f686d484b757db27d6f70b3ff535792edb65ceb40c2bd455410016"),
]

R110_GUARDS = {
    "QSUB_R110_GATE_GCD_DEGREE=0",
    "QSUB_RESULTANT_IDENTITY_SHA256=1192e8cfe113b732e6b1dfa67f06c45ed6317437f14ccc520f5c3db5335f2790",
    "QSUB_DELTA_UNIT_BY_RESULTANT=1",
    "QSUB_GCD_DEGREE=1",
    "QSUB_RELATION_DIVIDES_Q6=1",
    "QSUB_RELATION_DIVIDES_SIX=1",
    "QSUB_C1_NONZERO=1",
    "QSUB_Q6_ZERO=1",
    "QSUB_SIX_ZERO=1",
    "QSUB_RELATION_ZERO=1",
    "QSUB_ROOTCHECK_OK=1",
    "QSUB_J_SIZE=9",
    "QSUB_REPLAY_J_SIZE=9",
    "QSUB_REPLAY_CERT_ROWS=8",
    "QSUB_REPLAY_CERTIFICATE_IDENTITY=1",
    "QSUB_REPLAY_CERTIFICATE_READY=1",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def staged_index_hash(path: Path) -> str:
    """Hash the index blob, matching the ledger's document_sha256_16 contract."""
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return sha256_bytes(blob)[:16]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(read(path), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def status_section(text: str) -> str:
    match = re.search(
        r"^## Status(?: and exact scope)?\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise AssertionError("GLD101 owner has no status section")
    return match.group(1)


class GLD101EvidenceStatusTests(unittest.TestCase):
    def test_owner_and_review_preserve_the_exact_scoped_status(self) -> None:
        owner = read(OWNER)
        status = status_section(owner)
        self.assertIn(
            "**Proved exact scoped characteristic-zero norm-cover reduction (GLD101).**",
            status,
        )
        self.assertNotRegex(
            status,
            re.compile(r"\b(candidate|experimental|pending)\b", re.IGNORECASE),
        )
        self.assertIn("D(H2*Delta)", status)
        self.assertRegex(
            status,
            re.compile(
                r"global Krenn--Gu\s+conjecture remains\s+\*\*UNRESOLVED\*\*",
                re.IGNORECASE,
            ),
        )

        review = read(REVIEW)
        self.assertIn("Verdict", review)
        self.assertIn("PASS for the exact GLD101 norm-cover reduction", review)
        self.assertIn("Do not promote offset exclusion", review)
        self.assertRegex(
            review,
            re.compile(
                r"global Krenn--Gu\s+conjecture remains\s+\*\*UNRESOLVED\*\*",
                re.IGNORECASE,
            ),
        )

        # The owner document explicitly keeps the one-way bridge and all
        # stronger downstream claims outside this entry.
        for nonclaim in (
            "B=C=0",
            "physical incidence",
            "Fitting-ideal emptiness",
            "global Krenn--Gu conjecture",
        ):
            with self.subTest(nonclaim=nonclaim):
                self.assertIn(nonclaim, owner)

    def test_manifest_pins_scope_selectors_norm_and_external_boundary(self) -> None:
        payload = json.loads(read(MANIFEST))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["certificate_id"], "GLD101-A0-six-selector-norm-cover")
        self.assertEqual(payload["status"], "scoped_norm_cover_evidence_manifest")
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")

        scope = payload["mathematical_scope"]
        self.assertEqual(scope["branch"], "a=0")
        self.assertEqual(scope["chart"], "GLD88 equal-leaf H4 offset chart")
        self.assertEqual(scope["quotient"], "QQ(p)[q]/(Q6)")
        self.assertEqual(
            scope["open"],
            "D(H2*Delta) together with the GLD88 chart gates",
        )
        self.assertIn("rank(M)<=6", scope["bridge"])
        self.assertIn("(B,C)!=(0,0)", scope["bridge"])
        self.assertTrue(
            all("norm" in item.lower() or "rank" in item.lower() or "offset" in item.lower() for item in scope["nonclaims"])
        )

        q6 = payload["q6"]
        self.assertEqual(q6["srepr_sha256"], Q6_SREPR_SHA256)
        self.assertEqual(q6["degree_q"], 4)
        self.assertEqual(q6["leading_coefficient"], "2*p**2 - 2*p + 1")

        selector = payload["six_selector"]
        self.assertEqual(selector["names"], ["T0", "T1", "T2", "T3", "Y1", "X3"])
        self.assertEqual(selector["columns"], [[0, 1], [1, 0], [1, 1], [2, 0], [2, 1], [3, 0]])
        self.assertEqual(selector["norm_numerator_degree_p"], 548)
        self.assertEqual(selector["norm_numerator_terms_p"], 451)
        self.assertEqual(
            selector["norm_numerator_sha256"],
            "582f782b1fb1a1824e5d22d8374f52cb25075aab1372f7d06b9607269add79e3",
        )
        actual_factors = [
            (item["label"], item["degree"], item["exponent"], item["sha256"])
            for item in selector["factorization"]
        ]
        self.assertEqual(actual_factors, FACTOR_SIGNATURE)

        external = payload["external_offset_evidence"]
        self.assertFalse(external["composed_into_GLD101"])
        self.assertFalse(external["external_sources_required_for_norm_cover"])
        self.assertTrue(external["external_sources_required_for_stronger_offset_claim"])
        self.assertFalse(external["clean_clone_contains_polynomial_identities"])
        self.assertTrue(external["timeout_or_failed_runs_are_not_evidence"])

        self.assertEqual(
            set(payload["r110_hardchecks"]["required_guards"]), R110_GUARDS
        )
        charts = payload["r110_hardchecks"]["charts"]
        self.assertEqual(set(charts), {"B", "C"})
        for name, inverse in (("B", "z*B-1"), ("C", "z*C-1")):
            with self.subTest(chart=name):
                chart = charts[name]
                self.assertEqual(chart["inverse_equation"], inverse)
                for field in ("source_sha256", "run_json_sha256", "run_log_sha256"):
                    self.assertRegex(chart[field], r"^[0-9a-f]{64}$")
                self.assertTrue(chart["run_id"])

    def test_primary_audit_and_manifest_pin_the_same_inputs(self) -> None:
        primary = load_module(PRIMARY, "gld101_primary_static_test")
        audit = load_module(AUDIT, "gld101_audit_static_test")
        payload = json.loads(read(MANIFEST))

        self.assertEqual(tuple(primary.SUPPORT_ROWS), SUPPORT_ROWS)
        self.assertEqual(tuple(audit.ALL_ROWS), tuple(range(37)))
        self.assertEqual(tuple(audit.SUPPORT_ROWS), SUPPORT_ROWS)
        self.assertEqual(primary.EXPECTED_SUPPORT_DIGEST, SUPPORT_DIGEST)
        self.assertEqual(audit.EXPECTED_SUPPORT_DIGEST, SUPPORT_DIGEST)
        self.assertEqual(primary.EXPECTED_Q6_SREPR_SHA256, Q6_SREPR_SHA256)
        self.assertEqual(audit.EXPECTED_Q6_SREPR_SHA256, Q6_SREPR_SHA256)
        self.assertEqual(primary.EXPECTED_CERTIFICATE_PAYLOAD_SHA256, CERTIFICATE_SHA256)
        self.assertEqual(audit.EXPECTED_CERTIFICATE_PAYLOAD_SHA256, CERTIFICATE_SHA256)

        selector = payload["six_selector"]
        self.assertEqual(tuple(primary.SIX_NAMES), tuple(selector["names"]))
        self.assertEqual(tuple(audit.SIX_NAMES), tuple(selector["names"]))
        self.assertEqual(
            tuple(primary.SIX_COLUMNS),
            tuple(tuple(item) for item in selector["columns"]),
        )
        self.assertEqual(
            tuple(audit.SIX_COLUMNS),
            tuple(tuple(item) for item in selector["columns"]),
        )

        for name, (rows, columns) in SELECTOR_ROWS_AND_COLUMNS.items():
            with self.subTest(selector=name):
                if name.startswith("T"):
                    self.assertEqual(primary.NAMED[name], (rows, columns))
                    self.assertEqual(audit.NAMED[name], (rows, columns))
                else:
                    self.assertEqual(primary.RSTAR, rows)
                    self.assertEqual(primary.EXTRA[name], columns)
                    self.assertEqual(audit.RSTAR, rows)
                    self.assertEqual(audit.EXTRA[name], columns)

        expected_primary_factors = [
            (item["degree"], item["exponent"], item["sha256"])
            for item in payload["six_selector"]["factorization"]
        ]
        self.assertEqual(list(primary.EXPECTED_SIX_NORM["factors"]), expected_primary_factors)
        self.assertEqual(list(audit.EXPECTED_NORM["factors"]), expected_primary_factors)
        self.assertEqual(
            primary.EXPECTED_SIX_NORM["norm_numerator_degree_p"],
            payload["six_selector"]["norm_numerator_degree_p"],
        )
        self.assertEqual(
            primary.EXPECTED_SIX_NORM["norm_numerator_terms_p"],
            payload["six_selector"]["norm_numerator_terms_p"],
        )
        self.assertEqual(
            primary.EXPECTED_SIX_NORM["norm_numerator_sha256"],
            payload["six_selector"]["norm_numerator_sha256"],
        )
        self.assertEqual(
            audit.EXPECTED_NORM["degree"],
            payload["six_selector"]["norm_numerator_degree_p"],
        )
        self.assertEqual(audit.EXPECTED_NORM["terms"], payload["six_selector"]["norm_numerator_terms_p"])
        self.assertEqual(
            audit.EXPECTED_NORM["numerator_sha256"],
            payload["six_selector"]["norm_numerator_sha256"],
        )
        expected_delta_resultant = (
            "27648*p**6*(p - 1)**6*(p**2 - p + 1)**19*(2*p**2 - 2*p + 1)"
        )
        self.assertEqual(primary.EXPECTED_DELTA_RESULTANT, expected_delta_resultant)
        self.assertEqual(audit.EXPECTED_RESULTANT, expected_delta_resultant)
        self.assertEqual(
            primary.EXPECTED_DELTA_RESULTANT_SREPR_SHA256,
            "73f9ddbc2342851b2bfd79edc880a0c089172ae7b7d6e97a37076eba94420459",
        )
        self.assertEqual(
            audit.EXPECTED_RESULTANT_SREPR_SHA256,
            primary.EXPECTED_DELTA_RESULTANT_SREPR_SHA256,
        )

    def test_canonical_source_and_evidence_hashes_are_pinned(self) -> None:
        primary = load_module(PRIMARY, "gld101_primary_hash_test")
        audit = load_module(AUDIT, "gld101_audit_hash_test")
        payload = json.loads(read(MANIFEST))

        canonical_paths = {"GLD71": GLD71, "GLD88": GLD88, "GLD99": GLD99}
        for name, path in canonical_paths.items():
            with self.subTest(source=name):
                expected_lf = CANONICAL_SOURCE_LF_HASHES[name]
                self.assertEqual(lf_sha256(path), expected_lf)
                self.assertEqual(
                    payload["provenance"]["canonical_sources"][f"{name}_lf_sha256"],
                    expected_lf,
                )
                self.assertEqual(primary.EXPECTED_SOURCE_PINS[name]["lf_sha256"], expected_lf)
                self.assertEqual(audit.EXPECTED_SOURCE_PINS[name][1], expected_lf)
                primary_raw = primary.EXPECTED_SOURCE_PINS[name]["sha256"]
                audit_raw = audit.EXPECTED_SOURCE_PINS[name][0]
                self.assertEqual(primary_raw, audit_raw)
                if primary_raw is not None:
                    self.assertEqual(sha256_bytes(path.read_bytes()), primary_raw)

        for path, expected in EVIDENCE_SHA256.items():
            with self.subTest(path=path.name):
                self.assertEqual(sha256_bytes(path.read_bytes()), expected)

    def test_clean_clone_defaults_are_non_strict_about_ignored_replays(self) -> None:
        primary = load_module(PRIMARY, "gld101_primary_defaults_test")
        audit = load_module(AUDIT, "gld101_audit_defaults_test")
        self.assertFalse(
            inspect.signature(primary.check).parameters[
                "require_external_fibre_evidence"
            ].default
        )
        self.assertFalse(
            inspect.signature(audit.check).parameters["require_external"].default
        )

        primary_text = read(PRIMARY)
        audit_text = read(AUDIT)
        self.assertIn(
            "check_external_offset_evidence(require_external_fibre_evidence)",
            primary_text,
        )
        self.assertIn("external_replays(certificate_payload, require_external)", audit_text)
        self.assertIn("if not require:", primary_text)
        self.assertIn("if not require:", audit_text)
        self.assertRegex(
            primary_text,
            re.compile(r"if require and load_bearing:\s*\n\s*raise AssertionError", re.MULTILINE),
        )
        self.assertRegex(
            audit_text,
            re.compile(r"if require:\s*\n\s*raise AssertionError", re.MULTILINE),
        )
        self.assertIn("--require-external-fibre-evidence", primary_text)
        self.assertIn("--require-external-fibre-evidence", audit_text)

    def test_audit_import_boundary_is_explicit_and_separate(self) -> None:
        primary_modules = imported_modules(PRIMARY)
        audit_modules = imported_modules(AUDIT)
        forbidden = re.compile(
            r"(?:verify|audit)_four_root_torus_star_equal_leaf_h4_q6",
            re.IGNORECASE,
        )
        self.assertFalse(any(forbidden.search(name) for name in primary_modules))
        self.assertFalse(any(forbidden.search(name) for name in audit_modules))
        self.assertNotIn("gld101_primary_static_test", audit_modules)
        self.assertIn("importlib.util", audit_modules)

        audit_tree = ast.parse(read(AUDIT), filename=str(AUDIT))
        loader_calls = [
            node
            for node in ast.walk(audit_tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "spec_from_file_location"
        ]
        self.assertEqual(len(loader_calls), 1)
        self.assertIsInstance(loader_calls[0].args[0], ast.Constant)
        self.assertEqual(loader_calls[0].args[0].value, "gld71_for_gld101_audit")
        self.assertNotIn("load_gld88", read(AUDIT))
        self.assertNotIn("load_gld99", read(AUDIT))
        self.assertNotIn("load_gld101", read(AUDIT))
        self.assertIn("37 by 9 syndrome matrix", read(AUDIT))
        self.assertIn('submatrix.det(method="domain-ge")', read(AUDIT))

    def test_ledger_has_one_verified_entry_with_index_blob_owner_hash(self) -> None:
        ledger = json.loads(read(LEDGER))
        entries = [item for item in ledger["entries"] if "(GLD101)" in item["name"]]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["document_sha256_16"], staged_index_hash(OWNER))
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertEqual(entry["dependencies"], [])
        self.assertEqual(entry["external_binaries"], [])
        self.assertEqual(entry["proof_variant"], "canonical")
        self.assertIsNone(entry["subpackage"])
        self.assertIn("D(H2*Delta)", entry["note"])
        self.assertIn("B=C=0", entry["note"])
        self.assertIn("physical", entry["note"])
        self.assertIn("UNRESOLVED", entry["note"])


if __name__ == "__main__":
    unittest.main()
