"""Candidate-status and integrity tests for the GLD100 C-open corollary."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
CERTIFICATE = BASE / "certificates" / "GLD100_B0_COPEN_COROLLARY_CERTIFICATE.json"
OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_B0_COPEN_OFFSET_EXCLUSION_COROLLARY.md"
)
PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_b0_copen_offset_exclusion.py"
)
AUDIT = BASE / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_b0_copen_offset_exclusion.py"
)
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_"
    "B0_COPEN_OFFSET_EXCLUSION_REVIEW_2026-08-31.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"
README = BASE / "README.md"

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "c4a2ba5389e428de8b8b961e19ca6449b52d15266a2a7f3418892d5969744394"
)


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class GLD100B0CopenCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))

    def test_certificate_is_pinned_candidate_not_live(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(self.payload["schema_version"], 1)
        self.assertEqual(
            self.payload["certificate_id"],
            "GLD100-B0-Copen-arbitrary-a-corollary",
        )
        self.assertEqual(
            self.payload["status"],
            "candidate_exact_scoped_characteristic_zero_composition",
        )
        self.assertEqual(self.payload["global_conjecture"], "UNRESOLVED")
        self.assertEqual(
            self.payload["external_consolidation"],
            {
                "required_before_promotion": True,
                "candidate_commit": None,
                "candidate_tree": None,
                "request_event_id": None,
                "receipts": {},
                "status": "pending",
                "frontier_update_allowed": False,
                "theorem_ledger_update_allowed": False,
            },
        )

    def test_scope_and_exhaustive_split_are_exact(self) -> None:
        scope = self.payload["mathematical_scope"]
        self.assertEqual(scope["field"], "C")
        self.assertEqual(
            scope["set_statement"],
            "V(B_offset,Q6) intersect D(C_offset*Delta) "
            "intersect {rank M(G)<=6} = empty",
        )
        self.assertIn("a is arbitrary", scope["assumptions"])
        self.assertIn("D(B_offset*H2deg*Delta)", scope["downstream_reduction"])
        split = self.payload["case_split"]
        self.assertEqual(split["polynomial"], "H2deg=2*p^2-2*p+1")
        self.assertEqual(split["exhaustive_cases"], ["H2deg!=0", "H2deg=0"])
        self.assertFalse(split["H2deg_open"]["E31_required"])
        self.assertTrue(split["H2deg_zero"]["handler"].startswith("GLD99"))
        self.assertEqual(len(self.payload["proof_topology"]), 7)

    def test_all_upstream_source_pins_replay(self) -> None:
        pins = self.payload["source_pins_lf_sha256"]
        self.assertEqual(len(pins), 9)
        for relative, expected in pins.items():
            with self.subTest(relative=relative):
                self.assertFalse(Path(relative).is_absolute())
                path = ROOT / relative
                self.assertTrue(path.is_file())
                self.assertEqual(lf_sha256(path), expected)

    def test_owner_and_review_preserve_scope_and_nonclaims(self) -> None:
        owner = OWNER.read_text(encoding="utf-8")
        review = REVIEW.read_text(encoding="utf-8")
        for text in (owner, review):
            self.assertIn("UNRESOLVED", text)
            self.assertIn("B_offset", text)
            self.assertIn("C_offset", text)
            self.assertIn("H2deg", text)
            self.assertIn("E31", text)
            self.assertIn("D(B_offset)", text)
            self.assertIn("Delta=0", text)
            self.assertIn("Omega=0", text)
            self.assertIn("Fitting", text)
            self.assertIn("global", text.lower())
        self.assertIn("Candidate exact scoped", owner)
        self.assertRegex(review, re.compile(r"not yet for\s+live promotion", re.I))
        self.assertIn("No `E31` hypothesis occurs", owner)

    def test_candidate_is_absent_from_live_surfaces(self) -> None:
        frontier = FRONTIER.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        token = "GLD100-B0-Copen-arbitrary-a-corollary"
        self.assertNotIn(token, frontier)
        self.assertNotIn(token, readme)
        self.assertFalse(any(token in entry.get("name", "") for entry in ledger["entries"]))

    def test_independent_audit_imports_no_repository_verifier(self) -> None:
        source = AUDIT.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports: list[str] = []
        calls: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        self.assertFalse(any("g0_gate_removal" in name for name in imports))
        self.assertFalse(any("h2_degree_drop" in name for name in imports))
        self.assertFalse(any(name == "sympy" or name.startswith("sympy.") for name in imports))
        self.assertNotIn("importlib", imports)
        self.assertNotIn("load_module", calls)
        self.assertIn("audit_owner_dependency_boundary", source)

    def test_candidate_files_have_no_machine_or_run_dependency(self) -> None:
        for path in (CERTIFICATE, OWNER, PRIMARY, AUDIT, REVIEW):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, re.compile(r"[A-Za-z]:[\\/]"))
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("run.log", text)

    def test_primary_and_independent_audit_execute(self) -> None:
        cases = (
            (PRIMARY, "GLD100 B=0 C-open composition verifier: PASS"),
            (AUDIT, "Independent GLD100 B=0 C-open composition audit: PASS"),
        )
        for script, marker in cases:
            with self.subTest(script=script.name):
                completed = subprocess.run(
                    [sys.executable, str(script)],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(marker, completed.stdout)


if __name__ == "__main__":
    unittest.main()
