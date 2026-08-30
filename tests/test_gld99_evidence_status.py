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
BASE = ROOT / "claims" / "arbitrary-order"
OWNER = BASE / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_"
    "SIX_MINOR_OFFSET_EXCLUSION_THEOREM.md"
)
PRIMARY = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_"
    "six_minor_offset_exclusion.py"
)
AUDIT = BASE / (
    "audit_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_"
    "six_minor_offset_exclusion.py"
)
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_H2_DEGREE_DROP_"
    "SIX_MINOR_OFFSET_EXCLUSION_REVIEW_2026-08-29.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
ROOT_README = ROOT / "README.md"
README = BASE / "README.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"

SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
GENERATOR_HASHES = {
    1: {
        "T0": "c66046efa2e34a5cff341e5edb6deccc0fab008fd5fe4ff89f458abf5ebc2e4e",
        "T1": "106ebfdaf5c6aea5f4f5d844ad170d3be4be45dcb10a73cedd57721c1754d83f",
        "T2": "7e562e95ae2a740d76469338204cf942903d025c264c81987d5a7cc687c52adb",
        "T3": "f5576f4d76055fe5cea933ca4bd2fa9b2a4279a0f92155b8b5143fd60938019f",
        "D0": "463c8a46c7583204a8cbefa5fb0dae6c46af86105d45a5f2d27658e183ed9ace",
        "D2": "e311a0588bc91f96530de1799ee05a829fce5999ed246a3cfc3cea926ee9e936",
    },
    -1: {
        "T0": "aab9bf74f768c5e8aabadf988e7a795556a432a2c7b3b808eb4c08c71f6d8aa7",
        "T1": "8c3b58a67a46f3159c64fe42e2902a8eb973db07a869dc41a37136dbf5db935b",
        "T2": "68c0a116dfc57bbb4ac72c5750f3d821977cbd78b168ce27de2a116d1f43c06d",
        "T3": "0fd46d37b59d76b6a3224a1a15006a80fbc2e862e634ae6d8b7be29ea7229bbf",
        "D0": "af0791f41ea378e8045902b90ced9167af1551633cfe94fe8e62f50bc5c3b3f3",
        "D2": "856831444749d5b033247401445313384fc4789ab9184c97e19b13f130324445",
    },
}
CERTIFICATE_HASHES = {
    1: {
        "B": "da5154181e031400a933d6ecb2e4b82dbaf6c3d9b7c11dc557cf20740546b9e3",
        "C": "e52ba0af1cc4c2b65a9849bebe6c8414f75eb64dbb42ae4879464d3ee3213e35",
    },
    -1: {
        "B": "837adda0446d760cc959890eef072b600fc93dc9ca3f2a837bbd256a8be82cf0",
        "C": "7143e9974307c5855ebe438433ffe0776cc187b05883f0453ae5672efd94774a",
    },
}
RANK_SIGNATURE = {"rows": 158, "columns": 144, "rank": 140}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_support_digest(gld71) -> str:
    encoded = [
        [
            row,
            [[list(indices), coefficient] for indices, coefficient in gld71.SPARSE_RELATIONS[row]],
        ]
        for row in (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
    ]
    return hashlib.sha256(
        json.dumps(encoded, separators=(",", ":")).encode()
    ).hexdigest()


def staged_index_hash(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()[:16]


class GLD99EvidenceStatusTests(unittest.TestCase):
    def test_owner_and_review_are_promoted_only_at_scoped_status(self) -> None:
        owner = read(OWNER)
        status = owner.split("## Status and exact scope", 1)[1].split("##", 1)[0]
        self.assertIn(
            "**Proved exact scoped characteristic-zero theorem (`GLD99`).**",
            status,
        )
        self.assertNotRegex(status, re.compile(r"\bcandidate\b", re.I))
        self.assertRegex(
            status,
            re.compile(r"global Krenn--Gu\s+conjecture remains \*\*UNRESOLVED\*\*"),
        )

        review = read(REVIEW)
        self.assertIn("Verdict: PASS for the exact `GLD99` scope", review)
        self.assertRegex(
            review,
            re.compile(r"global\s+Krenn--Gu conjecture remains \*\*UNRESOLVED\*\*"),
        )

    def test_copied_inputs_match_canonical_gld71_gld88_and_gld96(self) -> None:
        primary = load_module(PRIMARY, "gld99_primary_input_test")
        audit = load_module(AUDIT, "gld99_audit_input_test")
        gld71 = load_module(
            BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py",
            "gld71_gld99_input_test",
        )
        gld88 = load_module(
            BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py",
            "gld88_gld99_input_test",
        )
        gld96 = load_module(
            BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py",
            "gld96_gld99_input_test",
        )

        for row, support in audit.PINNED_RELATIONS.items():
            with self.subTest(row=row):
                self.assertEqual(tuple(gld71.SPARSE_RELATIONS[row]), support)
        self.assertEqual(canonical_support_digest(gld71), SUPPORT_DIGEST)
        self.assertEqual(audit.support_digest(), SUPPORT_DIGEST)
        self.assertEqual(primary.SUPPORT_ROWS, audit.SUPPORT_ROWS)

        p, q, a = sp.symbols("p q a")
        canonical_family = gld88.h4_family(p, q, a)
        copied_family = audit.h4_family(p, q, a)
        for key in ("s", "b", "c", "u", "v"):
            with self.subTest(family_key=key):
                self.assertEqual(sp.cancel(canonical_family[key] - copied_family[key]), 0)
        self.assertEqual(
            sp.expand(primary.q6_polynomial(p, q) - gld96.q6_polynomial(p, q)),
            0,
        )
        self.assertEqual(
            sp.expand(audit.q6_polynomial(p, q) - gld96.q6_polynomial(p, q)),
            0,
        )

        self.assertEqual(audit.PIVOT_ROWS, gld96.PIVOT_ROWS)
        self.assertEqual(audit.PIVOT_COLUMNS, gld96.PIVOT_COLUMNS)
        expected_minors = {
            name: (tuple((*gld96.PIVOT_ROWS, row)), tuple((*gld96.PIVOT_COLUMNS, column)))
            for name, (row, column) in zip(
                ("T0", "T1", "T2", "T3"),
                gld96.TARGETS,
                strict=True,
            )
        }
        for name, selection in expected_minors.items():
            self.assertEqual(audit.MINORS[name], selection)
            self.assertEqual(primary.MINORS[name], selection)

    def test_support_generator_certificate_and_rank_hashes_are_pinned(self) -> None:
        primary = load_module(PRIMARY, "gld99_primary_hash_test")
        audit = load_module(AUDIT, "gld99_audit_hash_test")
        for module in (primary, audit):
            with self.subTest(module=module.__name__):
                self.assertEqual(module.EXPECTED_SUPPORT_DIGEST, SUPPORT_DIGEST)
                self.assertEqual(module.EXPECTED_GENERATOR_HASHES, GENERATOR_HASHES)
                self.assertEqual(module.EXPECTED_CERTIFICATE_HASHES, CERTIFICATE_HASHES)
        self.assertEqual(primary.EXPECTED_MULTIPLIER_SIGNATURE, RANK_SIGNATURE)
        self.assertEqual(audit.EXPECTED_RANK_SIGNATURE, RANK_SIGNATURE)

        review = read(REVIEW)
        for digest in [SUPPORT_DIGEST, *[value for branch in GENERATOR_HASHES.values() for value in branch.values()], *[value for branch in CERTIFICATE_HASHES.values() for value in branch.values()]]:
            with self.subTest(digest=digest):
                self.assertIn(digest, review)

    def test_scope_repairs_and_no_shortcuts_are_recorded(self) -> None:
        primary = read(PRIMARY)
        audit = read(AUDIT)
        review = read(REVIEW)
        for text in (primary, audit):
            self.assertIn("bc_total_degree", text)
            self.assertNotIn('"bc_total_degree": 4', text)
            self.assertIn("158", text)
            self.assertIn("144", text)
            self.assertIn("rank", text)
        self.assertIn("genuine `C^2`", review)
        self.assertIn("degree-four claim", review)
        self.assertIn("kernel counter", review)
        self.assertIn("Matrix indexing", review)
        self.assertIn("tuple-add residual", review)
        self.assertIn("branch-specific", review)
        self.assertIn("optional hash bypass", review)
        self.assertIn("T-only", review)
        self.assertRegex(review, re.compile(r"failed runs are\s+not evidence"))

    def test_frontier_and_readmes_record_the_exact_live_wall(self) -> None:
        frontier = read(FRONTIER)
        node = next(line for line in frontier.splitlines() if line.startswith('  GLD99["'))
        self.assertIn("<br/>PROVED", node)
        self.assertIn("GLD96 -->|H2=Q6=0 degree-drop", frontier)
        self.assertIn("GLD99 -->|Omega=0 / arbitrary H4 Q6 outside", frontier)
        self.assertIn("GLD96 -->|E31/g0/Delta exceptional", frontier)
        self.assertNotIn("GLD96 -->|E31/g0/H2/Delta exceptional", frontier)
        self.assertIn("The global Krenn–Gu conjecture is **UNRESOLVED**", frontier)

        for path in (README, ROOT_README):
            text = read(path)
            self.assertIn("GLD99", text)
            self.assertIn("H2=Q6=0", text)
            self.assertIn("global", text.lower())
            self.assertIn("UNRESOLVED", text)

    def test_ledger_entry_has_verified_status_and_staged_owner(self) -> None:
        ledger = json.loads(read(LEDGER))
        entries = [item for item in ledger["entries"] if "(GLD99)" in item["name"]]
        self.assertEqual(
            len(entries),
            1,
            "root integration must add exactly one verified GLD99 ledger entry",
        )
        entry = entries[0]
        self.assertEqual(entry["document_sha256_16"], staged_index_hash(OWNER))
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertIn("UNRESOLVED", entry["note"])


if __name__ == "__main__":
    unittest.main()
