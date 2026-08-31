from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / "GLD101_A0_R4_B_OPEN_RESULTANT_CERTIFICATE.json"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_a0_r4_b_open_resultant.py"
DOCUMENT = ROOT / "docs" / "audits" / (
    "GLD101_A0_R4_B_OPEN_RESULTANT_PORTABLE_LEAF_2026-08-31.md"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "1961eed09059a7434002c610f89eb4e0ebc195398fbd026b0a4a7ddf778cc36e"
)
EXPECTED_DETERMINANT_SHA256 = (
    "f0b194b39ae1a5638defb64e3eb664400b69d423d7ac85db0c62ce3cd549db48"
)
SELECTORS = ("T3", "Y1", "X3")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class GLD101R4BOpenResultantPortableLeafTests(unittest.TestCase):
    def test_certificate_is_hash_pinned_and_scoped(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        payload = json.loads(read(CERTIFICATE))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["certificate_id"],
            "GLD101-a0-R4-B-open-T3-Y1-X3-resultant-unit",
        )
        self.assertEqual(
            payload["status"],
            "scoped_exact_selected_necessary_minor_leaf_certificate",
        )
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        scope = payload["mathematical_scope"]
        self.assertIn("R4=0 and Q6=0", scope["branch"])
        self.assertIn("D(B*H2*Delta)", scope["open"])
        self.assertEqual(tuple(scope["selected_necessary_minors"]), SELECTORS)
        self.assertIn("rank(M)<=6", scope["bridge"])
        joined = " ".join(scope["nonclaims"])
        for phrase in (
            "no converse",
            "no claim on B=0",
            "no claim for another residual factor",
            "no live-frontier",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, joined)

    def test_factor_and_resultant_unit_records_are_complete(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        factors = payload["factor_checks"]
        self.assertTrue(factors["R4_irreducible_over_QQ"])
        self.assertEqual(factors["resultant_R4_H2"], "145")
        self.assertTrue(factors["H2_unit_on_R4"])
        self.assertEqual(len(factors["fibre_algebra_basis"]), 16)

        proof = payload["resultant_proof"]
        self.assertEqual(set(proof["t_resultants"]), {"T3_X3", "Y1_X3"})
        self.assertTrue(all(record["degree"] == 4 for record in proof["t_resultants"].values()))
        self.assertEqual(proof["B_sylvester_matrix_shape"], [8, 8])
        self.assertEqual(proof["multiplication_matrix_shape"], [16, 16])
        self.assertEqual(
            proof["multiplication_determinant_sha256"],
            EXPECTED_DETERMINANT_SHA256,
        )
        self.assertEqual(proof["determinant_numerator_digits"], 3429)
        self.assertEqual(proof["determinant_denominator_digits"], 252)
        self.assertTrue(proof["B_resultant_is_unit"])

    def test_actual_minor_and_denominator_metadata_is_pinned(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        self.assertEqual(tuple(payload["selectors"]), SELECTORS)
        expected_hashes = {
            "T3": "26e97ac75a6ab5d9b99e75b1b1821a2a57a08db29f77a2f63f6cc6c62f93549a",
            "Y1": "fb7921836c64fc06cbce60126ffd1c95b339cccdda0ccde9ad3e3d4dbbc4ec73",
            "X3": "442b967240ac7034927719f5eaf1fecde86647cbc6c599238018ab72b337c5c3",
        }
        for selector in SELECTORS:
            with self.subTest(selector=selector):
                record = payload["selectors"][selector]
                self.assertEqual(len(record["rows"]), 7)
                self.assertEqual(len(record["columns"]), 7)
                self.assertTrue(record["common_B_factor_after_C_equals_Bt"])
                self.assertTrue(record["denominator_factors"])
                self.assertEqual(record["equation"]["sha256"], expected_hashes[selector])
                self.assertEqual(record["equation"]["degrees"]["t"], 1)
                self.assertLessEqual(record["equation"]["degrees"]["B"], 2)

    def test_historical_transcript_is_not_a_package_dependency(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        provenance = payload["provenance"]
        self.assertIn("not inputs", provenance["historical_transcript_role"])
        self.assertIn("50 MB", provenance["historical_transcript_role"])
        self.assertEqual(
            provenance["historical_source_sha256"],
            "fad9adaa23e2f94093b7b6db7875981ed0c7961791d2d01a4ab7a908fcab6cc1",
        )
        for path in (CERTIFICATE, PRIMARY, AUDIT, DOCUMENT):
            with self.subTest(path=path.name):
                text = read(path)
                self.assertNotIn("C:\\Users\\", text)
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("OneDrive", text)
                self.assertNotIn("krenn-gu-instance-commons", text)
        self.assertFalse(any(ROOT.rglob("*.sing")))

    def test_audit_imports_no_repository_module_or_primary(self) -> None:
        tree = ast.parse(read(AUDIT), filename=str(AUDIT))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertLessEqual(
            imported,
            {
                "__future__",
                "ast",
                "functools",
                "hashlib",
                "json",
                "sys",
                "pathlib",
                "typing",
                "sympy",
            },
        )
        self.assertNotIn("importlib", imported)
        self.assertNotIn(PRIMARY.stem, imported)
        forbidden_calls = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"eval", "exec"}
        }
        self.assertEqual(forbidden_calls, set())

    def test_primary_exact_regeneration(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PRIMARY)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["status"], "exact_scoped_R4_B_open_resultant_unit_verified"
        )
        self.assertEqual(result["global_conjecture"], "UNRESOLVED")
        self.assertEqual(result["certificate_lf_sha256"], EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(result["multiplication_determinant_sha256"], EXPECTED_DETERMINANT_SHA256)
        self.assertTrue(result["B_resultant_is_unit"])

    def test_independent_no_import_audit(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(AUDIT)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["status"],
            "independent_no_repository_import_R4_B_open_resultant_audit_passed",
        )
        self.assertEqual(result["global_conjecture"], "UNRESOLVED")
        self.assertEqual(result["repository_modules_imported"], 0)
        self.assertTrue(result["B_resultant_recomputed_by_recursive_Laplace"])
        self.assertTrue(result["multiplication_determinant_recomputed_in_reversed_basis"])
        self.assertEqual(result["multiplication_determinant_sha256"], EXPECTED_DETERMINANT_SHA256)
        self.assertTrue(result["B_resultant_is_unit"])


if __name__ == "__main__":
    unittest.main()
