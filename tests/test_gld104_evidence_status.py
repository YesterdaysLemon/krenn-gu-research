"""Evidence-status and integrity tests for the proved GLD104 composition."""

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
    "GLD104_A0_P8_NONZERO_OFFSET_COMPOSITION_CERTIFICATE.json"
)
PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_"
    "a0_p8_nonzero_offset_closure.py"
)
AUDIT = BASE / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_"
    "a0_p8_nonzero_offset_closure.py"
)
OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_P8_"
    "NONZERO_OFFSET_CLOSURE_THEOREM.md"
)
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_P8_"
    "NONZERO_OFFSET_CLOSURE_REVIEW_2026-08-31.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"
README = BASE / "README.md"
PARENT_ATTEMPT = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_A0_"
    "RESIDUAL_FACTOR_PARENT_ATTEMPT_2026-08-30.md"
)

EXPECTED_CERTIFICATE_LF_SHA256 = (
    "7a68ae95177c50f96725849ca73f01fba5eba18a121e4500acf5d22a6dc282e5"
)
EXPECTED_SELECTOR_DETERMINANT_SHA256 = (
    "c8b675268458576454cf3eeab5fe38c4ef468a2113c94febfd471c0cfc6d6431"
)
SIX = ["T0", "T1", "T2", "T3", "Y1", "X3"]
P8 = ["T0", "T1", "T2", "T3", "D0", "Y0", "Y1", "X3"]
FACTORS = ["p-1", "p", "p^2+1", "P", "H2", "R4", "R8", "R110"]


def lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


class GLD104EvidenceStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.raw = CERTIFICATE.read_bytes()
        cls.payload = json.loads(cls.raw.decode("utf-8"))

    def test_certificate_pin_scope_and_external_acceptance(self) -> None:
        self.assertEqual(lf_sha256(CERTIFICATE), EXPECTED_CERTIFICATE_LF_SHA256)
        self.assertEqual(self.payload["schema_version"], 1)
        self.assertEqual(
            self.payload["certificate_id"],
            "GLD104-A0-P8-nonzero-offset-composition",
        )
        self.assertEqual(
            self.payload["status"],
            "proved_exact_scoped_characteristic_zero_composition",
        )
        self.assertEqual(self.payload["global_conjecture"], "UNRESOLVED")
        self.assertEqual(
            self.payload["external_consolidation"],
            {
                "candidate_commit": "75da0298a535888e7a84257b7bfd6a556a3267b2",
                "candidate_tree": "86fae29848c52c7ccd3236c84e156aedb3f02b78",
                "required_before_promotion": True,
                "request_event_id": "kgc_01M1BXKGZ8F86B6XWK1J6Q3DMF",
                "receipts": {
                    "Juniper": "kgc_01M1BXV18D8NZQ22BDEXDXJWTP",
                    "Mycelium": "kgc_01M1BYMJPC3VD2N7ENK20RXE3B",
                },
                "status": "accepted_2_of_2",
                "frontier_update_allowed": True,
                "theorem_ledger_update_allowed": True,
            },
        )

    def test_selector_surface_and_offset_cover_are_exact(self) -> None:
        selectors = self.payload["selector_sets"]
        self.assertEqual(selectors["six_selector"], SIX)
        self.assertEqual(selectors["p8"], P8)
        self.assertLess(set(SIX), set(P8))
        self.assertIn("D0 and Y0", selectors["relation"])
        self.assertEqual(
            self.payload["offset_cover"]["sets"],
            ["D(B)", "V(B) intersect D(C)"],
        )
        self.assertEqual(
            self.payload["offset_cover"]["exhaustive_for"],
            "(B,C)!=(0,0)",
        )

    def test_norm_support_and_dispositions_are_exhaustive(self) -> None:
        support = self.payload["norm_support"]
        self.assertEqual([item["label"] for item in support], FACTORS)
        dispositions = {item["label"]: item["disposition"] for item in support}
        self.assertEqual(dispositions["P"], "excluded_because_P_divides_Delta")
        self.assertEqual(
            dispositions["H2"], "excluded_by_declared_D(H2)_open"
        )
        self.assertEqual(
            dispositions["R110"],
            "closed_by_R110_P8_B_open_eight_minor_leaf",
        )

    def test_all_29_child_source_pins_replay(self) -> None:
        pins = self.payload["source_pins_lf_sha256"]
        self.assertEqual(len(pins), 29)
        for relative, expected in pins.items():
            with self.subTest(relative=relative):
                path = ROOT / relative
                self.assertTrue(path.is_file())
                self.assertFalse(Path(relative).is_absolute())
                self.assertEqual(lf_sha256(path), expected)

    def test_selected_minor_norm_bridge_is_explicit(self) -> None:
        primary = PRIMARY.read_text(encoding="utf-8")
        audit = AUDIT.read_text(encoding="utf-8")
        for source in (primary, audit):
            self.assertIn("nonzero", source.lower())
        self.assertIn(EXPECTED_SELECTOR_DETERMINANT_SHA256, audit)
        self.assertIn("SIX_NAMES", primary)
        self.assertIn('module.EXPECTED_SIX_NORM["expression_sha256"]', primary)
        self.assertIn("module.SIX_COLUMNS", primary)
        self.assertIn("(0, 0) not in terms", primary)
        self.assertIn("terms <= set(module.SIX_COLUMNS)", primary)
        self.assertIn("monomial_vector", primary)
        self.assertIn("coefficient-matrix construction", audit)
        self.assertIn("nonzero vector gate", audit)

    def test_independent_audit_imports_no_repository_verifier(self) -> None:
        source = AUDIT.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")
        self.assertFalse(any("verify_four_root_torus" in name for name in imports))
        self.assertNotIn("importlib", imports)
        self.assertNotIn("load_module", source)
        self.assertIn("restricted_assignment", source)
        self.assertIn("audit_selected_minor_norm_bridge_source", source)

    def test_theorem_documents_preserve_status_and_nonclaims(self) -> None:
        owner = OWNER.read_text(encoding="utf-8")
        review = REVIEW.read_text(encoding="utf-8")
        status = owner.split("## Status", 1)[1].split("##", 1)[0]
        self.assertIn("Proved exact scoped characteristic-zero", status)
        self.assertNotRegex(status, re.compile(r"\b(candidate|pending)\b", re.I))
        self.assertIn(
            "Verdict: PASS for the exact scoped GLD104 P8 composition",
            review,
        )
        for event_id in (
            "kgc_01M1BXKGZ8F86B6XWK1J6Q3DMF",
            "kgc_01M1BXV18D8NZQ22BDEXDXJWTP",
            "kgc_01M1BYMJPC3VD2N7ENK20RXE3B",
        ):
            self.assertIn(event_id, owner)
            self.assertIn(event_id, review)
        for text in (owner, review):
            self.assertIn("UNRESOLVED", text)
            self.assertRegex(text, re.compile(r"\bP6\b"))
            self.assertIn("B=C=0", text)
            self.assertRegex(text, re.compile(r"full.{0,8}E31", re.I))
            self.assertIn("global", text.lower())

    def test_live_surfaces_record_only_the_scoped_theorem(self) -> None:
        frontier = FRONTIER.read_text(encoding="utf-8")
        self.assertIn('GLD104["Equal-leaf H4 Q6 a=0 P8', frontier)
        self.assertIn("GLD101 -->|eight-factor P8 composition", frontier)
        self.assertIn("| `GLD104` |", frontier)
        self.assertIn("global status remains **UNRESOLVED**", frontier)

        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        entries = [entry for entry in ledger["entries"] if "(GLD104)" in entry["name"]]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertIn("UNRESOLVED", entry["note"])

        readme = README.read_text(encoding="utf-8")
        parent = PARENT_ATTEMPT.read_text(encoding="utf-8")
        self.assertIn("[`GLD104`]", readme)
        self.assertRegex(
            parent,
            re.compile(r"received accepted\s+`2/2`\s+external consolidation"),
        )

    def test_theorem_files_have_no_machine_or_run_dependency(self) -> None:
        for path in (CERTIFICATE, PRIMARY, AUDIT, OWNER, REVIEW):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotRegex(text, re.compile(r"[A-Za-z]:[\\/]"))
                self.assertNotIn(".research-runs", text)
                self.assertNotIn("run.log", text)

    def test_primary_and_independent_audit_execute(self) -> None:
        cases = (
            (PRIMARY, "GLD104 P8/nonzero-offset composition verifier: PASS"),
            (AUDIT, "Independent GLD104 composition audit: PASS"),
        )
        for script, marker in cases:
            with self.subTest(script=script.name):
                completed = subprocess.run(
                    [sys.executable, str(script)],
                    cwd=ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertIn(marker, completed.stdout)


if __name__ == "__main__":
    unittest.main()
