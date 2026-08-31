"""Candidate-status and integrity tests for the GLD105 composition package."""

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
CERTIFICATE = BASE / "certificates" / (
    "GLD105_A0_H4_Q6_PHYSICAL_INCIDENCE_COMPOSITION_CERTIFICATE.json"
)
PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_"
    "a0_physical_incidence_exclusion.py"
)
AUDIT = BASE / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_"
    "a0_physical_incidence_exclusion.py"
)
OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_"
    "PHYSICAL_INCIDENCE_EXCLUSION_THEOREM.md"
)
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_"
    "PHYSICAL_INCIDENCE_EXCLUSION_REVIEW_2026-08-31.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"
README = BASE / "README.md"

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "6816d2ae686ae841664a92a761c6e4df484103e66b16d183e8a372c0f2b0361f"
)


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class GLD105CandidatePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))

    def test_certificate_is_pinned_candidate_not_live(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(self.payload["schema_version"], 1)
        self.assertEqual(
            self.payload["certificate_id"],
            "GLD105-A0-H4-Q6-physical-incidence-parent-composition",
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

    def test_scope_and_case_split_are_exact(self) -> None:
        scope = self.payload["mathematical_scope"]
        self.assertEqual(scope["field"], "C")
        self.assertEqual(
            scope["set_statement"],
            "B_incidence intersect V(I_7(A)) intersect V(a,Q6) "
            "intersect D(Omega*Delta) = empty",
        )
        split = self.payload["case_split"]
        self.assertEqual(split["polynomial"], "H2deg=2*p^2-2*p+1")
        self.assertEqual(split["exhaustive_cases"], ["H2deg!=0", "H2deg=0"])
        self.assertEqual(split["H2deg_open"]["offset_handler"], "GLD104")
        self.assertEqual(split["H2deg_open"]["endpoint_handler"], "GLD95")
        self.assertIn("physical low-rank incidence", split["H2deg_open"]["endpoint_conclusion"])
        self.assertEqual(split["H2deg_zero"]["handler"], "GLD99")
        self.assertIn("arbitrary a", split["H2deg_zero"]["scope"])
        self.assertEqual(len(self.payload["proof_topology"]), 8)

    def test_overloaded_notation_is_fenced(self) -> None:
        notation = self.payload["notation_fences"]
        self.assertIn("not the scalar offset B", notation["B_incidence"])
        self.assertIn("not the scalar offset C", notation["C_center"])
        self.assertTrue(notation["H2deg"].startswith("2*p^2-2*p+1"))
        self.assertIn("p-s=L1/(p+q-1)", notation["GLD86_H2_collision"])
        for path in (OWNER, REVIEW):
            text = path.read_text(encoding="utf-8")
            self.assertIn("H2deg", text)
            self.assertIn("p-s = L1/d0", text)

    def test_all_19_upstream_source_pins_replay(self) -> None:
        pins = self.payload["source_pins_lf_sha256"]
        self.assertEqual(len(pins), 19)
        for relative, expected in pins.items():
            with self.subTest(relative=relative):
                self.assertFalse(Path(relative).is_absolute())
                path = ROOT / relative
                self.assertTrue(path.is_file())
                self.assertEqual(lf_sha256(path), expected)

    def test_owner_and_review_preserve_endpoint_qualifiers_and_nonclaims(self) -> None:
        owner = OWNER.read_text(encoding="utf-8")
        review = REVIEW.read_text(encoding="utf-8")
        status = owner.split("## Status", 1)[1].split("##", 1)[0]
        self.assertIn("Candidate exact scoped", status)
        self.assertNotIn("Proved exact scoped", status)
        self.assertRegex(review, re.compile(r"not yet for\s+live promotion"))
        for text in (owner, review):
            self.assertIn("UNRESOLVED", text)
            self.assertIn("D(Omega Delta)", text)
            self.assertIn("B_incidence intersect V(I_7(A)) intersect F88", text)
            self.assertRegex(text, re.compile(r"does not say.*F88", re.I | re.S))
            self.assertIn("P6", text)
            self.assertIn("Omega=0", text)
            self.assertIn("Delta=0", text)
            self.assertRegex(text, re.compile(r"full.{0,8}E31", re.I))
            self.assertIn("Fitting", text)
            self.assertIn("global", text.lower())

    def test_candidate_is_absent_from_live_surfaces(self) -> None:
        frontier = FRONTIER.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertNotIn('GLD105["', frontier)
        self.assertNotIn("| `GLD105` |", frontier)
        self.assertNotIn("[`GLD105`]", readme)
        entries = [entry for entry in ledger["entries"] if "(GLD105)" in entry["name"]]
        self.assertEqual(entries, [])

    def test_audit_imports_no_repository_verifier(self) -> None:
        for path in (PRIMARY, AUDIT):
            source = path.read_text(encoding="utf-8")
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
            with self.subTest(path=path.name):
                self.assertFalse(any("verify_four_root" in name for name in imports))
                self.assertNotIn("importlib", imports)
                self.assertNotIn("load_module", calls)
                if path == AUDIT:
                    self.assertFalse(
                        any(name == "sympy" or name.startswith("sympy.") for name in imports)
                    )
        audit_source = AUDIT.read_text(encoding="utf-8")
        self.assertIn("validate_h2_notation_without_sympy", audit_source)

    def test_candidate_files_have_no_machine_or_run_dependency(self) -> None:
        for path in (CERTIFICATE, PRIMARY, AUDIT, OWNER, REVIEW):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, re.compile(r"[A-Za-z]:[\\/]"))
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("run.log", text)

    def test_primary_and_independent_audit_execute(self) -> None:
        cases = (
            (
                PRIMARY,
                "GLD105 physical-incidence parent composition verifier: PASS",
            ),
            (
                AUDIT,
                "Independent GLD105 physical-incidence composition audit: PASS",
            ),
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
