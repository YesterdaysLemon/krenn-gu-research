from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import subprocess
import unittest
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OWNER = ROOT / "claims" / "arbitrary-order" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P2_"
    "SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md"
)
PRIMARY = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_p2_"
    "six_minor_offset_exclusion.py"
)
AUDIT = ROOT / "claims" / "arbitrary-order" / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_p2_"
    "six_minor_offset_exclusion.py"
)
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P2_"
    "SIX_MINOR_OFFSET_EXCLUSION_REVIEW_2026-08-29.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"

BASIS_HASH = "da8b07d04dfb0dbc9935345320722fb21f9e711bb9166f82db9fb23b0f7f585f"
REDUCED_HASHES = {
    "e726ee5fd5406059d95043969ad5860eda1463540696d7e4e8cf5420543508d3",
    "2fd8891db047195270f87c09c7024b5dbde4f8ed27014648ee487b27031e6ca6",
    "f84a890c3d52c92f0af7a7f753310d59c3cc9bb11ea32433c83a7d3e9bb9764e",
    "fbe10197fe9898c98389e97e4e58584d9ccf9b61bc2cbc51e959082ccfb11186",
    "652f5a57dbe12daf26a3336e8924cab9c84f607ca60f330aa2f6c54ec99a19a1",
    "2cc8f30090e21531f595608185becbb6449ee90f8f8d7b6c36e51c9b4cfc40b2",
}


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


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GLD97EvidenceStatusTests(unittest.TestCase):
    def test_owner_and_review_are_promoted_only_at_scoped_status(self) -> None:
        owner = read(OWNER)
        status = owner.split("## Status and exact scope", 1)[1].split("##", 1)[0]
        self.assertIn("**Proved exact scoped characteristic-zero theorem (GLD97).**", status)
        self.assertNotRegex(status, re.compile(r"\bcandidate\b", re.I))
        self.assertIn("global conjecture remains **UNRESOLVED**", status)

        review = read(REVIEW)
        self.assertIn("Verdict: PASS for the exact `GLD97` scope", review)
        self.assertIn("global conjecture remains **UNRESOLVED**", review)

    def test_frontier_records_proved_node_and_retained_global_wall(self) -> None:
        frontier = read(FRONTIER)
        node = next(
            line for line in frontier.splitlines() if line.startswith('  GLD97["')
        )
        self.assertIn("<br/>PROVED", node)
        self.assertIn("GLD97 -->|arbitrary p", frontier)
        self.assertIn("The global Krenn–Gu conjecture is **UNRESOLVED**", frontier)

    def test_primary_and_audit_pin_the_same_exact_certificate(self) -> None:
        primary = read(PRIMARY)
        audit = read(AUDIT)
        for digest in REDUCED_HASHES | {BASIS_HASH}:
            with self.subTest(digest=digest):
                self.assertIn(digest, primary)
                self.assertIn(digest, audit)
        self.assertIn('"R31_generator_included": False', primary)
        self.assertIn('"global_conjecture": "UNRESOLVED"', primary)
        self.assertIn('"global_conjecture": "UNRESOLVED"', audit)

    def test_ledger_hash_and_evidence_links_are_current(self) -> None:
        ledger = json.loads(read(LEDGER))
        entry = next(item for item in ledger["entries"] if "(GLD97)" in item["name"])
        owner_hash = index_hash(OWNER)
        self.assertEqual(entry["document_sha256_16"], owner_hash)
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())

    def test_copied_inputs_match_committed_canonical_sources(self) -> None:
        primary = load_module(PRIMARY, "gld97_primary_input_test")
        audit = load_module(AUDIT, "gld97_audit_input_test")
        base = ROOT / "claims" / "arbitrary-order"
        gld71 = load_module(
            base
            / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py",
            "gld71_gld97_input_test",
        )
        gld88 = load_module(
            base
            / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py",
            "gld88_gld97_input_test",
        )
        gld96 = load_module(
            base
            / "verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py",
            "gld96_gld97_input_test",
        )

        for row, support in audit.PINNED_RELATIONS.items():
            self.assertEqual(tuple(gld71.SPARSE_RELATIONS[row]), support)

        p, q, a = sp.symbols("p q a")
        canonical_family = gld88.h4_family(p, q, a)
        copied_family = audit.h4_family(p, q, a)
        for key in ("s", "b", "c"):
            self.assertEqual(sp.cancel(canonical_family[key] - copied_family[key]), 0)
        self.assertEqual(
            sp.expand(primary.q6_polynomial(p, q) - gld96.q6_polynomial(p, q)),
            0,
        )
        self.assertEqual(sp.expand(audit.q6(p, q) - gld96.q6_polynomial(p, q)), 0)


if __name__ == "__main__":
    unittest.main()
