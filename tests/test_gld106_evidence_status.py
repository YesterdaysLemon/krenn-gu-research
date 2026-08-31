"""Evidence-status and integrity tests for the proved GLD106 corollary."""

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
    "cb482133a56922695030ca850caa1135b480be8a93e23331fe8316e26741f377"
)


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class GLD106EvidenceStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))

    def test_certificate_is_pinned_and_externally_accepted(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(self.payload["schema_version"], 1)
        self.assertEqual(
            self.payload["certificate_id"],
            "GLD100-B0-Copen-arbitrary-a-corollary",
        )
        self.assertEqual(
            self.payload["status"],
            "proved_exact_scoped_characteristic_zero_composition",
        )
        self.assertEqual(self.payload["global_conjecture"], "UNRESOLVED")
        self.assertEqual(
            self.payload["external_consolidation"],
            {
                "required_before_promotion": True,
                "candidate_commit": "8001f3435702d642ccb86e10893000379cca7ae5",
                "candidate_tree": "8b4b38f92c143aa557e039661ab7ecf046539181",
                "candidate_diff_bytes": 43128,
                "candidate_diff_sha256": (
                    "b8b33767bd74677b4e09a3a78bdaece657e90a5dbcb681452ae0ff3ca3c5f915"
                ),
                "request_event_id": "kgc_01M1C3T5Y83KSKVKG22HK0TCAH",
                "receipts": {
                    "Juniper": "kgc_01M1C3VG98735EV4JM8TEVE02V",
                    "Kestrel": "kgc_01M1C468KR8XX1C8XC0EMEXPM3",
                },
                "status": "accepted_2_of_2",
                "frontier_update_allowed": True,
                "theorem_ledger_update_allowed": True,
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
        self.assertIn("Proved exact scoped", owner)
        self.assertIn("Verdict: PASS for the exact scoped GLD106", review)
        self.assertIn("No `E31` hypothesis occurs", owner)
        for event_id in (
            "kgc_01M1C3T5Y83KSKVKG22HK0TCAH",
            "kgc_01M1C3VG98735EV4JM8TEVE02V",
            "kgc_01M1C468KR8XX1C8XC0EMEXPM3",
        ):
            self.assertIn(event_id, owner)
            self.assertIn(event_id, review)

    def test_live_surfaces_record_only_the_scoped_theorem(self) -> None:
        frontier = FRONTIER.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertIn('GLD106["Equal-leaf H4 Q6 B=0 C-open', frontier)
        self.assertIn("GLD100 -->|B=0 residual gamma/fibre closure", frontier)
        self.assertIn("| `GLD106` |", frontier)
        self.assertIn("global status remains **UNRESOLVED**", frontier)
        self.assertIn("[`GLD106`]", readme)
        entries = [entry for entry in ledger["entries"] if "(GLD106)" in entry["name"]]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["document_sha256_16"], "12ea2a4ad4d06f5b")
        self.assertEqual(entry["document_sha256_16"], lf_sha256(OWNER)[:16])
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertIn("UNRESOLVED", entry["note"])

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

    def test_theorem_files_have_no_machine_or_run_dependency(self) -> None:
        for path in (CERTIFICATE, OWNER, PRIMARY, AUDIT, REVIEW):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, re.compile(r"[A-Za-z]:[\\/]"))
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("run.log", text)

    def test_primary_and_independent_audit_execute(self) -> None:
        cases = (
            (PRIMARY, "GLD106 B=0 C-open composition verifier: PASS"),
            (AUDIT, "Independent GLD106 B=0 C-open composition audit: PASS"),
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
