"""Static and lightweight replay tests for the GLD101 d2 B-open leaf."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / (
    "GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_CERTIFICATE.json"
)
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_a0_d2_bopen_portable.py"
NOTE = ROOT / "docs" / "audits" / (
    "GLD101_A0_D2_BOPEN_T3_Y1_X3_PORTABLE_LEAF_PACKAGE_2026-08-31.md"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "e4d0c5a07a930d8c4305a897e613b73185d48df885f9907f0e67a41fc593338c"
)
EXPECTED_PRIMARY_LF_SHA256 = (
    "8e580e15ec7d63ed259bbfc65c42f6289dc296f1a0e7d5eb809d9c1aa6364b36"
)
EXPECTED_AUDIT_LF_SHA256 = (
    "6ea764f005eef2fdb3b1f7d771d93a38de23e39ab0b5c9a501d68971ad79e911"
)
EXPECTED_NOTE_LF_SHA256 = (
    "ecffccd2f0396b73842b2e97212d2013d928e9ce9fba039ddf1ebb27edb51a7f"
)
EXPECTED_SINGULAR_SOURCE_SHA256 = (
    "58530b32e87ff5a4198478c375755ed0452a4c6351ee234872796155c2dd4199"
)
SELECTORS = ("T0", "T1", "T2", "T3", "Y1", "X3")
COMPACT_CORE = ("T3", "Y1", "X3")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class GLD101D2BOpenPortableCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
        cls.payload = json.loads(cls.raw.decode("utf-8"))

    def test_package_files_are_exactly_hash_pinned(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(lf_sha256(PRIMARY), EXPECTED_PRIMARY_LF_SHA256)
        self.assertEqual(lf_sha256(AUDIT), EXPECTED_AUDIT_LF_SHA256)
        self.assertEqual(lf_sha256(NOTE), EXPECTED_NOTE_LF_SHA256)
        rendered = json.dumps(self.payload, indent=2, sort_keys=True) + "\n"
        self.assertEqual(self.raw, rendered.encode("utf-8"))

    def test_scope_and_nonclaims_are_exact(self) -> None:
        payload = self.payload
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["certificate_id"],
            "GLD101-A0-D2-B-open-T3-Y1-X3-portable-unit-leaf",
        )
        self.assertEqual(payload["status"], "scoped_exact_selected_minor_unit_leaf")
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        scope = payload["mathematical_scope"]
        self.assertEqual(scope["normalization"], "a=0")
        self.assertEqual(scope["factor"], "p^2+1=0")
        self.assertEqual(scope["variety"], "V(Q6)")
        self.assertEqual(scope["open"], "D(B*H2*Delta)")
        self.assertEqual(tuple(scope["actual_selected_minors"]), SELECTORS)
        self.assertEqual(tuple(scope["compact_unit_core"]), COMPACT_CORE)
        nonclaims = " ".join(scope["nonclaims"]).lower()
        for phrase in (
            "no selector converse",
            "no claim on b=0",
            "no p8 theorem",
            "no arbitrary-a",
            "no full-e31",
            "no global",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, nonclaims)

    def test_six_actual_selectors_and_equations_are_complete(self) -> None:
        self.assertEqual(set(self.payload["selector_definitions"]), set(SELECTORS))
        self.assertEqual(set(self.payload["selected_minor_equations"]), set(SELECTORS))
        for name in SELECTORS:
            with self.subTest(name=name):
                definition = self.payload["selector_definitions"][name]
                self.assertEqual(len(definition["rows"]), 7)
                self.assertEqual(len(definition["columns"]), 7)
                equation = self.payload["selected_minor_equations"][name]
                self.assertGreaterEqual(equation["terms"], 20)
                self.assertEqual(equation["degrees"], {"B": 2, "q": 3, "t": 1})
                self.assertEqual(len(equation["scaled_sha256"]), 64)
                self.assertTrue(equation["cleared_denominator_factors"])

    def test_gaussian_gates_and_solver_contract_are_pinned(self) -> None:
        quotient = self.payload["gaussian_quotient"]
        self.assertEqual(quotient["q6_squarefree_degree"], 4)
        self.assertTrue(quotient["delta_unit_mod_q6"])
        self.assertEqual(quotient["h2_p_i"], "-1-2*i")
        self.assertEqual(quotient["h2_gaussian_norm"], 5)
        solver = self.payload["singular_unit_lift"]
        self.assertEqual(solver["unit_core"], list(COMPACT_CORE))
        self.assertEqual(
            solver["ideal"], "Q6,H_T3,H_Y1,H_X3,z*B*Delta-1"
        )
        self.assertEqual(solver["source_sha256"], EXPECTED_SINGULAR_SOURCE_SHA256)
        self.assertEqual(solver["source_line_count"], 66)
        self.assertFalse(solver["solver_source_committed"])
        self.assertFalse(solver["large_solver_transcript_committed"])
        self.assertTrue(solver["fresh_bounded_replay_required"])
        expected = solver["historical_expected_runtime"]
        self.assertEqual(expected["basis_size"], 1)
        self.assertEqual(expected["unit_column"], 1)
        self.assertEqual(expected["nonzero_multipliers"], 5)
        self.assertEqual(expected["identity_sum_minus_one"], 0)

    def test_no_machine_path_or_archived_artifact_dependency(self) -> None:
        forbidden = re.compile(r"[A-Za-z]:[\\/]")
        for path in (CERTIFICATE, PRIMARY, AUDIT, NOTE):
            text = read(path)
            with self.subTest(path=path.name):
                self.assertNotRegex(text, forbidden)
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("OneDrive", text)
        self.assertEqual(self.payload["independence"]["external_runtime_inputs"], [])
        for source in self.payload["portable_inputs"]["canonical_sources"].values():
            self.assertFalse(Path(source["path"]).is_absolute())
        tracked = subprocess.run(
            ["git", "ls-files", "*.sing"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(tracked.stdout.strip(), "")

    def test_audit_imports_no_repository_module_or_primary(self) -> None:
        tree = ast.parse(read(AUDIT), filename=str(AUDIT))
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        self.assertLessEqual(
            imported_roots,
            {
                "__future__",
                "ast",
                "hashlib",
                "json",
                "pathlib",
                "re",
                "sys",
                "time",
                "typing",
                "sympy",
            },
        )
        source = read(AUDIT)
        self.assertNotIn("importlib", source)
        self.assertIn("extract_literal_assignment", source)
        self.assertIn("SPARSE_RELATIONS", source)
        self.assertIn('det(method="domain-ge")', source)
        self.assertNotIn(PRIMARY.stem, source)

    def test_invalid_and_corroborative_history_is_quarantined(self) -> None:
        quarantine = self.payload["evidence_lineage"]["quarantined_non_evidence"]
        self.assertEqual(len(quarantine), 3)
        dispositions = {entry["disposition"] for entry in quarantine}
        self.assertEqual(
            dispositions,
            {
                "invalid_non_evidence",
                "corroborative_only",
                "superseded_nonportable_evidence",
            },
        )
        reasons = " ".join(entry["reason"] for entry in quarantine).lower()
        self.assertIn("denominator inverse", reasons)
        self.assertIn("does not independently derive", reasons)
        self.assertIn("no large transcript is tracked", reasons)

    def test_primary_replay_and_source_emission(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PRIMARY)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        report = json.loads(completed.stdout)
        self.assertEqual(
            report["status"],
            "exact_scoped_gld101_d2_bopen_portable_certificate_verified",
        )
        self.assertEqual(report["global_conjecture"], "UNRESOLVED")
        self.assertEqual(tuple(report["actual_selected_minors"]), SELECTORS)
        self.assertEqual(tuple(report["compact_unit_core"]), COMPACT_CORE)
        self.assertEqual(
            report["singular_source_sha256"], EXPECTED_SINGULAR_SOURCE_SHA256
        )

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "d2-portable.sing"
            subprocess.run(
                [sys.executable, str(PRIMARY), "--emit-singular", str(target)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(
                hashlib.sha256(target.read_bytes()).hexdigest(),
                EXPECTED_SINGULAR_SOURCE_SHA256,
            )
            self.assertEqual(len(target.read_text(encoding="utf-8").splitlines()), 66)


if __name__ == "__main__":
    unittest.main()
