"""Static integrity tests for the scoped GLD101 R110 P8 portable leaf."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "certificates" / (
    "GLD101_A0_R110_P8_BOPEN_PORTABLE_CERTIFICATE.json"
)
PRIMARY = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_a0_r110_p8_bopen_portable.py"
)
AUDIT = ROOT / "claims" / "arbitrary-order" / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_a0_r110_p8_bopen_portable.py"
)
NOTE = ROOT / "docs" / "audits" / (
    "GLD101_A0_R110_P8_BOPEN_PORTABLE_LEAF_PACKAGE_2026-08-31.md"
)

EXPECTED_CERTIFICATE_SHA256 = (
    "bdf84e09be8e4d7f76a0d05b050957acd2ef9b95d1e55a6fafe3f9d465c1c32b"
)
EXPECTED_SOURCE_SHA256 = (
    "a8b84e4d8cf2cd7768ab4d945a403ac80200adef0019de6a793bb565756b3bd5"
)
EXPECTED_GENERATOR_DIGEST = (
    "8ce1f9037e428291f123237df7782968b07ee230f4e39856b25e889c0a06359b"
)
EIGHT_NAMES = ["T0", "T1", "T2", "T3", "D0", "Y0", "Y1", "X3"]


class GLD101R110P8PortableCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CERTIFICATE.read_bytes()
        cls.normalized = cls.raw.replace(b"\r\n", b"\n")
        cls.payload = json.loads(cls.raw.decode("utf-8"))

    def test_certificate_is_canonical_json_with_exact_lf_pin(self) -> None:
        self.assertEqual(
            hashlib.sha256(self.normalized).hexdigest(),
            EXPECTED_CERTIFICATE_SHA256,
        )
        rendered = json.dumps(self.payload, indent=2, sort_keys=True) + "\n"
        self.assertEqual(self.normalized, rendered.encode("utf-8"))
        self.assertLess(len(self.raw), 512 * 1024)

    def test_scope_is_exactly_eight_minor_b_open_leaf(self) -> None:
        payload = self.payload
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["certificate_id"],
            "GLD101-A0-R110-P8-B-open-portable-unit-leaf",
        )
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        scope = payload["mathematical_scope"]
        self.assertEqual(scope["load_bearing_chart"], "B-open")
        self.assertIn("not a dependency", scope["corroborative_only"])
        self.assertEqual(
            payload["actual_minors"]["eight_actual_minor_names"], EIGHT_NAMES
        )
        self.assertEqual(
            payload["singular_standard_basis"]["inverse_equation"], "z*B-1"
        )
        self.assertIn("P6", " ".join(scope["nonclaims"]))
        self.assertIn("global", " ".join(scope["nonclaims"]).lower())

    def test_nine_table_seam_and_r110_gates_are_pinned(self) -> None:
        actual = self.payload["actual_minors"]
        self.assertEqual(
            actual["generator_order"],
            ["T0", "T1", "T2", "T3", "D0", "D2", "Y0", "Y1", "X3"],
        )
        self.assertEqual(actual["coefficient_tables"]["D2"], {})
        self.assertEqual(actual["direct_generator_digest"], EXPECTED_GENERATOR_DIGEST)
        self.assertEqual(self.payload["r110"]["degree"], 110)
        self.assertEqual(self.payload["six_selector"]["r110_multiplicity"], 1)
        self.assertTrue(self.payload["r110"]["mod41_irreducible"])
        self.assertEqual(self.payload["r110"]["excluded_gate_gcd_degree"], 0)
        self.assertTrue(self.payload["r110"]["delta_is_unit"])
        self.assertTrue(
            self.payload["r110"]["all_actual_minor_denominators_are_units"]
        )
        self.assertEqual(
            set(self.payload["r110"]["actual_minor_denominator_gcd_degrees"]),
            set(EIGHT_NAMES),
        )
        self.assertEqual(
            set(self.payload["r110"]["actual_minor_denominator_gcd_degrees"].values()),
            {0},
        )

    def test_solver_source_contract_is_regenerated_not_committed(self) -> None:
        source = self.payload["singular_standard_basis"]
        self.assertEqual(source["source_sha256"], EXPECTED_SOURCE_SHA256)
        self.assertEqual(source["source_line_count"], 52)
        self.assertEqual(source["chart"], "B")
        self.assertTrue(source["fresh_bounded_run_required"])
        self.assertFalse(source["large_source_committed"])
        self.assertFalse(source["solver_log_committed"])
        self.assertIn("QSUB_J_SIZE=9", source["expected_markers"])
        self.assertIn("QSUB_G_SIZE=1", source["expected_markers"])
        self.assertIn("QSUB_UNIT=1", source["expected_markers"])

    def test_invalid_and_inconclusive_history_is_explicit_non_evidence(self) -> None:
        quarantined = self.payload["evidence_lineage"]["quarantined_non_evidence"]
        self.assertEqual(
            [entry["event_id"] for entry in quarantined],
            [
                "kgc_01M1B8SW50MBK7D38NJGBB2GE8",
                "kgc_01M1B9217RNZSEHP8Y1GPHH3BH",
                "kgc_01M1BBB92WYJ1FBNB3N3E7YTYD",
            ],
        )
        reasons = " ".join(entry["reason"] for entry in quarantined)
        self.assertIn("v1", reasons)
        self.assertIn("v2", reasons)
        self.assertIn("P6", reasons)
        self.assertIn("inconclusive", reasons)

    def test_package_contains_no_machine_path_or_archived_run_dependency(self) -> None:
        for path in (CERTIFICATE, PRIMARY, AUDIT, NOTE):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, re.compile(r"[A-Za-z]:[\\/]"))
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("run.log", text)
        self.assertEqual(self.payload["independence"]["external_runtime_inputs"], [])
        for source in self.payload["portable_inputs"]["canonical_sources"].values():
            self.assertFalse(Path(source["path"]).is_absolute())

    def test_direct_audit_imports_no_primary_or_quotient_verifier(self) -> None:
        tree = ast.parse(AUDIT.read_text(encoding="utf-8"))
        imported_modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported_modules.append(node.module or "")
        self.assertFalse(
            any("verify_four_root_torus" in name for name in imported_modules)
        )
        source = AUDIT.read_text(encoding="utf-8")
        self.assertNotIn("load_base", source)
        self.assertIn("load_gld71", source)
        self.assertIn("direct_minors", source)
        self.assertIn('det(method="domain-ge")', source)


if __name__ == "__main__":
    unittest.main()
