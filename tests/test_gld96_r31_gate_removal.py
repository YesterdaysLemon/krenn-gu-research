from __future__ import annotations

import hashlib
import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "claims" / "arbitrary-order" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_THEOREM.md"
)
PRIMARY = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py"
)
AUDIT = ROOT / "claims" / "arbitrary-order" / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py"
)
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GATE_REMOVAL_REVIEW_2026-08-29.md"
)
README = ROOT / "claims" / "arbitrary-order" / "README.md"
ROOT_README = ROOT / "README.md"
GLD97_OWNER = ROOT / "claims" / "arbitrary-order" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P2_SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md"
)
GLD97_PRIMARY = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py"
)
GLD97_AUDIT = ROOT / "claims" / "arbitrary-order" / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py"
)
HISTORICAL_REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_R31_GENERIC_RESULTANT_EXCLUSION_REVIEW_2026-08-28.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def index_hash(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()[:16]


class GLD96R31GateRemovalTests(unittest.TestCase):
    def test_owner_states_the_strengthened_scoped_theorem(self) -> None:
        owner = read(OWNER)
        status = owner.split("## Status and exact scope", 1)[1].split("##", 1)[0]
        self.assertIn("strengthened", status)
        self.assertIn("D(E31 * H2 * g0 * Delta)", status)
        self.assertNotIn("D(R31 * E31", status)
        self.assertIn("global", status.lower())
        self.assertIn("UNRESOLVED", status)

        self.assertIn("This is an identity in the polynomial ring", owner)
        self.assertIn("It remains valid when `R31=0`", owner)

    def test_primary_and_independent_audit_use_no_r31_gate(self) -> None:
        primary = read(PRIMARY)
        audit = read(AUDIT)
        self.assertIn('"open": "D(E31*H2*g0*Delta)"', primary)
        self.assertIn('"required_as_gate": False', primary)
        self.assertIn("assert sp.cancel(schur - direct_bordered) == 0", primary)
        self.assertNotIn('"open": "D(R31*E31', primary)

        self.assertIn('"R31_gate_used": False', audit)
        self.assertIn("global polynomial identity, including R31=0", audit)
        self.assertNotRegex(
            audit,
            re.compile(r"on D\(R31\).*bordered determinant", re.I),
        )

    def test_review_frontier_and_readme_retain_exact_walls(self) -> None:
        review = read(REVIEW)
        self.assertIn("Verdict: PASS for the strengthened exact `GLD96` scope", review)
        self.assertIn("D(E31 H2 g0 Delta)", review)
        self.assertIn("Krenn--Gu remains **UNRESOLVED**", review)

        frontier = read(FRONTIER)
        node = next(
            line for line in frontier.splitlines() if line.startswith('  GLD96["')
        )
        self.assertIn("R31-free", node)
        self.assertIn("D(E31 H2 g0 Delta)", frontier)
        self.assertNotIn("D(R31*E31*H2*g0*Delta)", frontier)
        self.assertIn("The global Krenn–Gu conjecture is **UNRESOLVED**", frontier)

        readme = read(README)
        self.assertIn("R31-free generic continuation", readme)
        self.assertIn("E31=0", readme)
        self.assertIn("no global status change", readme)

        root_readme = read(ROOT_README)
        self.assertIn("R31-free generic localization", root_readme)
        self.assertNotIn("D(R31*E31*H2*g0*Delta)", root_readme)

        ledger = json.loads(read(LEDGER))
        problem_entry = next(
            item for item in ledger["entries"] if item["document"] == "README.md"
        )
        self.assertEqual(problem_entry["document_sha256_16"], index_hash(ROOT_README))

    def test_downstream_gld97_description_is_reconciled(self) -> None:
        owner = read(GLD97_OWNER)
        primary = read(GLD97_PRIMARY)
        audit = read(GLD97_AUDIT)
        self.assertIn("strengthened GLD96 generic resultant proof", owner)
        self.assertIn("'D(E31 H2 g0 Delta)'", owner)
        self.assertNotIn("'D(R31 E31 H2 g0 Delta)'", owner)
        self.assertNotIn(
            "No arbitrary-p R31/double-pivot theorem is claimed",
            primary,
        )
        self.assertNotIn("R31-open E31/g0 localization", audit)

        historical_review = read(HISTORICAL_REVIEW)
        self.assertIn("Historical scope note (2026-08-29)", historical_review)
        self.assertIn("R31 gate-removal review", historical_review)

    def test_ledger_points_to_current_strengthened_owner(self) -> None:
        ledger = json.loads(read(LEDGER))
        entry = next(item for item in ledger["entries"] if "(GLD96)" in item["name"])
        owner_hash = index_hash(OWNER)
        self.assertEqual(entry["document_sha256_16"], owner_hash)
        self.assertEqual(entry["status"], "verified")
        self.assertIn("R31-free", entry["name"])
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertIn("UNRESOLVED", entry["note"])


if __name__ == "__main__":
    unittest.main()
