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
CERTIFICATE = BASE / "certificates" / "GLD101_A0_GENERIC_COPEN_PORTABLE_CERTIFICATE.json"
SOURCE = BASE / "certificates" / "GLD101_A0_GENERIC_COPEN_UNIT_SCREEN.singular.txt"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_a0_generic_c_open.py"
DOCUMENT = ROOT / "docs" / "audits" / (
    "GLD101_A0_GENERIC_COPEN_PORTABLE_LEAF_PACKAGE_2026-08-31.md"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "1f84c1d30c1c8403be477b5def91144f687cc08a4ed5406dffb3866cf6996afb"
)
EXPECTED_SOURCE_LF_SHA256 = (
    "c514d842532f99cde4488cca048c551f39e43ed5cdf2c5ce6a54dcd7aa704850"
)
SELECTORS = ("T0", "T1", "T2", "T3", "Y1", "X3")


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GLD101GenericCOpenPortableLeafTests(unittest.TestCase):
    def test_certificate_is_hash_pinned_and_exactly_scoped(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        payload = json.loads(read(CERTIFICATE))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["certificate_id"],
            "GLD101-a0-generic-C-open-selected-minor-rank-cover",
        )
        self.assertEqual(
            payload["status"],
            "scoped_exact_selected_necessary_minor_leaf_certificate",
        )
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        scope = payload["mathematical_scope"]
        self.assertEqual(scope["locus"], "B=0 and C!=0")
        self.assertIn("D(H2*Delta)", scope["open"])
        self.assertEqual(tuple(scope["selected_necessary_minors"]), SELECTORS)
        self.assertIn("rank(M)<=6", scope["bridge"])
        joined = " ".join(scope["nonclaims"])
        for phrase in (
            "no converse",
            "no claim on B!=0",
            "no P8 parent theorem",
            "no global",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, joined)

    def test_source_is_durable_exact_data_not_a_transcript_dependency(self) -> None:
        self.assertEqual(lf_sha256(SOURCE), EXPECTED_SOURCE_LF_SHA256)
        text = read(SOURCE)
        self.assertIn(
            "ideal I=Q6,H_T0,H_T1,H_T2,H_T3,H_Y1,H_X3,z*H2*Delta-1;",
            text,
        )
        self.assertIn("int is_unit=(size(G)==1)&&(G[1]==1);", text)
        payload = json.loads(read(CERTIFICATE))
        provenance = payload["provenance"]
        self.assertIn("not required", provenance["tracked_Singular_source_role"])
        failed = provenance["failed_lineage"][0]
        self.assertEqual(failed["status"], "failed_non_evidence")
        self.assertEqual(
            failed["versions"],
            ["generic-copen-cross-audit-v1", "generic-copen-cross-audit-v2"],
        )

    def test_rank_cover_records_all_minors_and_exceptional_fibres(self) -> None:
        cover = json.loads(read(CERTIFICATE))["rank_cover"]
        self.assertEqual(cover["coefficient_matrix_shape"], [6, 4])
        self.assertEqual(cover["coefficient_order"], ["q^3", "q^2", "q", "1"])
        minors = cover["maximal_minors"]
        self.assertEqual(len(minors), 15)
        self.assertEqual(
            len({tuple(record["selectors"]) for record in minors}),
            15,
        )
        self.assertTrue(all(record["sha256"] for record in minors))
        self.assertEqual(
            cover["maximal_minor_gcd"]["factorization"],
            "p^15*(p-1)^6*(p+1)^2*(p^2-p+1)^11*(2*p^2-2*p+1)^14",
        )
        self.assertEqual(set(cover["special_fibres"]), {"-1", "0", "1"})
        self.assertEqual(
            cover["special_fibres"]["-1"]["disposition"],
            "no common q root",
        )
        for value in ("0", "1"):
            self.assertEqual(
                cover["special_fibres"][value]["disposition"],
                "every common Q6 root lies in Delta=0",
            )
        self.assertTrue(cover["no_common_zero_on_D(H2*Delta)"])

    def test_package_has_no_machine_or_ignored_run_dependency(self) -> None:
        for path in (CERTIFICATE, PRIMARY, AUDIT, DOCUMENT):
            with self.subTest(path=path.name):
                text = read(path)
                self.assertNotIn("C:\\Users\\", text)
                self.assertNotIn("OneDrive", text)
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("krenn-gu-instance-commons", text)
        commands = json.loads(read(CERTIFICATE))["reproducible_commands"]
        self.assertEqual(len(commands), 3)
        self.assertTrue(all(command.startswith("python ") for command in commands))

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
                "hashlib",
                "itertools",
                "json",
                "re",
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
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
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
            timeout=90,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["status"], "exact_scoped_generic_C_open_rank_cover_verified"
        )
        self.assertEqual(result["global_conjecture"], "UNRESOLVED")
        self.assertEqual(result["certificate_lf_sha256"], EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(result["maximal_minors_checked"], 15)
        self.assertEqual(result["special_fibres_checked"], ["-1", "0", "1"])
        self.assertTrue(result["no_common_zero_on_D(H2*Delta)"])

    def test_independent_no_import_audit(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(AUDIT)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=240,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["status"],
            "independent_no_repository_import_generic_C_open_audit_passed",
        )
        self.assertEqual(result["global_conjecture"], "UNRESOLVED")
        self.assertEqual(result["repository_modules_imported"], 0)
        self.assertEqual(result["maximal_minors_recomputed_by_explicit_Leibniz"], 15)
        self.assertTrue(result["no_common_zero_on_D(H2*Delta)"])


if __name__ == "__main__":
    unittest.main()
