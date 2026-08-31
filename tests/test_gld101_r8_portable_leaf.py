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
CERTIFICATE = BASE / "certificates" / "GLD101_R8_B_OPEN_FIVE_ROW_KERNEL_CERTIFICATE.json"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_a0_r8_b_open_five_row_kernel.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_a0_r8_b_open_five_row_kernel.py"

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "df96337e0de80cd1236fde1f366490afa7a06f28845475b03cc5c31eeba8af7c"
)
SELECTORS = ("T1", "T2", "T3", "Y1", "X3")
COLUMNS = ("t", "1", "B*t", "B", "B^2*t", "B^2")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GLD101R8PortableLeafTests(unittest.TestCase):
    def test_certificate_is_hash_pinned_and_scoped(self) -> None:
        self.assertEqual(
            hashlib.sha256(
                CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
            ).hexdigest(),
            EXPECTED_CERTIFICATE_LF_SHA256,
        )
        payload = json.loads(read(CERTIFICATE))
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(
            payload["certificate_id"], "GLD101-R8-B-open-five-row-kernel"
        )
        self.assertEqual(
            payload["status"], "scoped_exact_selected_minor_leaf_certificate"
        )
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        scope = payload["mathematical_scope"]
        self.assertEqual(scope["factor"], "R8=0")
        self.assertIn("D(B*H2*Delta)", scope["open"])
        self.assertEqual(tuple(scope["selected_necessary_minors"]), SELECTORS)
        self.assertIn("rank(M)<=6", scope["bridge"])
        self.assertIn("cancel the common B factor", scope["bridge"])
        joined_nonclaims = " ".join(scope["nonclaims"])
        for phrase in (
            "no converse",
            "no claim on B=0",
            "no claim for P6",
            "no global",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, joined_nonclaims)

    def test_matrix_and_selector_definitions_are_complete(self) -> None:
        payload = json.loads(read(CERTIFICATE))
        algebra = payload["algebra"]
        self.assertEqual(tuple(algebra["columns"]), COLUMNS)
        self.assertEqual(tuple(algebra["matrix"]), SELECTORS)
        self.assertEqual(set(payload["selector_definitions"]), set(SELECTORS))
        for selector in SELECTORS:
            with self.subTest(selector=selector):
                self.assertEqual(len(algebra["matrix"][selector]), 6)
                self.assertTrue(all(algebra["matrix"][selector]))
                definition = payload["selector_definitions"][selector]
                self.assertEqual(len(definition["rows"]), 7)
                self.assertEqual(len(definition["columns"]), 7)

    def test_package_has_no_machine_or_ignored_artifact_dependency(self) -> None:
        for path in (CERTIFICATE, PRIMARY, AUDIT):
            with self.subTest(path=path.name):
                text = read(path)
                self.assertNotIn("C:\\Users\\", text)
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("OneDrive", text)

        commands = json.loads(read(CERTIFICATE))["reproducible_commands"]
        self.assertEqual(len(commands), 2)
        self.assertTrue(all(command.startswith("python claims/") for command in commands))

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
                "sympy",
            },
        )
        self.assertNotIn("importlib", imported)
        self.assertNotIn(PRIMARY.stem, imported)

    def test_invalid_single_pivot_probe_is_quarantined(self) -> None:
        quarantine = json.loads(read(CERTIFICATE))["quarantined_non_evidence"]
        self.assertEqual(len(quarantine), 1)
        self.assertEqual(quarantine[0]["disposition"], "invalid_non_evidence")
        self.assertIn("need not contain", quarantine[0]["reason"])

    def test_primary_exact_checker_replays_from_tracked_payload(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PRIMARY)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(
            payload["status"],
            "exact_scoped_r8_five_row_kernel_certificate_verified",
        )
        self.assertEqual(payload["global_conjecture"], "UNRESOLVED")
        self.assertEqual(payload["matrix_shape"], [5, 6])
        self.assertEqual(payload["kernel_rows_zero"], 5)
        self.assertEqual(payload["common_residual_degree"], 1)
        self.assertEqual(
            payload["certificate_lf_sha256"], EXPECTED_CERTIFICATE_LF_SHA256
        )


if __name__ == "__main__":
    unittest.main()
