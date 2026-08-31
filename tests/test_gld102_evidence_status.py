from __future__ import annotations

import ast
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
OWNER = BASE / "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P01_NONZERO_OFFSET_EXCLUSION_THEOREM.md"
PRIMARY = BASE / "verify_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py"
AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py"
REVIEW = ROOT / "docs" / "audits" / (
    "FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_H4_Q6_P01_NONZERO_OFFSET_"
    "EXCLUSION_REVIEW_2026-08-30.md"
)
FRONTIER = ROOT / "docs" / "current-frontier.md"
LEDGER = ROOT / "catalog" / "theorem-ledger.json"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"

EXPECTED_EQUATION_HASHES = {
    "6698570ba9b983a03eb59e9bf33516dacd34806ebee1b49affb8cf10bd791bad",
    "c946ddf2793058f6c374230b7a11b997c34a5f930980f38e99f64eb3989b9f47",
    "eb247f55987cf51ac3056eb3b6b592155f5d7f38e42638f26ed864b644d36d0b",
    "50ea1f5f1f99449f97d083171a1c19379d610c7028fd6aec509504a6b725126f",
    "f58c27e889af1743689fbac7508212ce232d5ea9f627625fc5cd08d09d947cc8",
    "bec33400e8a096f815fc2313bf8c79730192b6b0aa07be6863247f6d0748436f",
    "0ef9b6e45dfe83211b11257929815cdef76de590e58171e698ed876c6abdd75a",
    "3c78c42206d3649f2b6206a4745dad2ad2284c3241a7e76ab25148d0a02d6f67",
    "f749ac6c9baf18f561550a0c11c8ce491aee07a38dfa4b4d211b11e3427688f4",
    "d52b7380f8724c57c9628e26340bb30235970d599bcd2669cdedd08624bb8893",
    "635d8d441511e8685ec961569f55021521d1489da199c53a795490936ddaf481",
    "71c0db85421a3ec2e5243fbdfb60b4b35059704b70a663a6e98060c425abfc05",
    "6f5db0d7e894c8dccee64b38e57ca831cbe36abdfbcd9dbf3e1949d4678db44a",
    "ee90b3a38619597c81ef424da576efb196d4370e5cc6bc5d6df6e7117549147d",
    "21ccb7e208b186ad567b01d474d544cf5188787b25505ae2ee9a18b2d6d0a88a",
    "1f12748b26196289948f9fdcade5f1378085294db2b646159f7174dfc5d70054",
    "1c4ca6991ea9cf416bc16aac62ed24d209161a4694d5618b43bc0e9b48ccd2e9",
    "1c866717a84aa6efa9eb1a0c8e445e980ca6f26148f24c4be27e6e18c2a81831",
    "c80794afcf47d3c2531ad978736f07abaee4170dc48cd12a88ab3d1028de3e2b",
    "c4aea8a643fcba39845ffb2d0604de0ad84c7c5f8ddd956fb07e1f4b83750876",
    "900cafb2918de28db8c5188d0935251c662f88d3c46122543464167af232d74c",
    "dae01bb49c4ea2b669ab9a331c578aa4084ac0e83b530887ceb095bdda0cef4d",
    "f3d6843358ed572dbddeaba098cd7061fc270c1138a113d020d83da1bd1ce65a",
    "e563ef704fbedbacdaa08ba0e94797604d3446519bcc428c07284f36372c2425",
}
BASIS_HASHES = {
    "9537b7269b6d1ca5d1782213313dc45c70b7b5357ec363b2b849ee754c86556f",
    "949dbbd7cb669602c03400612c7636dfdc0666127a99e8fa84591d3897ff60f3",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def staged_index_hash(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    blob = subprocess.run(
        ["git", "show", f":{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(blob).hexdigest()[:16]


class GLD102EvidenceStatusTests(unittest.TestCase):
    def test_owner_review_and_frontier_preserve_scoped_status(self) -> None:
        owner = read(OWNER)
        status = owner.split("## Status and exact scope", 1)[1].split("##", 1)[0]
        self.assertIn(
            "**Proved exact scoped characteristic-zero theorem (GLD102).**",
            status,
        )
        self.assertNotRegex(status, re.compile(r"\b(candidate|experimental)\b", re.I))
        self.assertIn("rank M(G) <= 6", status)
        self.assertIn("B=C=0", status)
        self.assertIn("global Krenn--Gu conjecture remains **UNRESOLVED**", status)

        review = read(REVIEW)
        self.assertIn("Verdict: PASS for the exact scoped GLD102 implication", review)
        self.assertIn("not an endpoint exclusion", review)
        self.assertIn("global Krenn--Gu conjecture remains **UNRESOLVED**", review)

        frontier = read(FRONTIER)
        node = next(line for line in frontier.splitlines() if line.startswith('  GLD102["'))
        self.assertIn("PROVED", node)
        self.assertIn("GLD101 -->|p=0,1 supports", frontier)
        self.assertIn("GLD102 -->|B=C=0 endpoint", frontier)
        self.assertIn("The global Krenn–Gu conjecture is **UNRESOLVED**", frontier)

    def test_primary_and_audit_pin_identical_exact_equations(self) -> None:
        primary = read(PRIMARY)
        audit = read(AUDIT)
        for digest in EXPECTED_EQUATION_HASHES:
            with self.subTest(digest=digest):
                self.assertIn(digest, primary)
                self.assertIn(digest, audit)
        for digest in BASIS_HASHES:
            self.assertIn(digest, read(OWNER))
        self.assertIn('"global_conjecture": "UNRESOLVED"', primary)
        self.assertIn('"global_conjecture": "UNRESOLVED"', audit)
        self.assertIn("rank_to_selector_direction_only", primary)
        self.assertIn("rank_to_selector_direction_only", audit)

    def test_audit_has_no_project_import_and_copied_inputs_match(self) -> None:
        audit_tree = ast.parse(read(AUDIT), filename=str(AUDIT))
        imported = set()
        for node in ast.walk(audit_tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
        self.assertNotIn("importlib", imported)
        self.assertFalse(any("krenn" in name.lower() or "gld" in name.lower() for name in imported))

        audit = load_module(AUDIT, "gld102_audit_input_test")
        gld71 = load_module(GLD71, "gld71_for_gld102_input_test")
        gld88 = load_module(GLD88, "gld88_for_gld102_input_test")
        for row, support in audit.PINNED_RELATIONS.items():
            self.assertEqual(tuple(gld71.SPARSE_RELATIONS[row]), support)

        p, q, a = sp.symbols("p q a")
        canonical = gld88.h4_family(p, q, a)
        copied = audit.h4_family(p, q, a)
        for key in ("s", "b", "c"):
            with self.subTest(key=key):
                self.assertEqual(sp.cancel(canonical[key] - copied[key]), 0)

    def test_primary_source_pins_and_selector_definitions_match(self) -> None:
        primary = load_module(PRIMARY, "gld102_primary_static_test")
        audit = load_module(AUDIT, "gld102_audit_static_test")
        self.assertEqual(primary.SELECTORS, audit.SELECTORS)
        self.assertEqual(primary.SUPPORT_ROWS, audit.SUPPORT_ROWS)
        self.assertEqual(primary.EXPECTED_SUPPORT_DIGEST, audit.EXPECTED_SUPPORT_DIGEST)
        self.assertEqual(primary.EXPECTED_B_OPEN_HASHES[0], audit.EXPECTED_HASHES[0]["B"])
        self.assertEqual(primary.EXPECTED_B_OPEN_HASHES[1], audit.EXPECTED_HASHES[1]["B"])
        self.assertEqual(primary.EXPECTED_C_OPEN_HASHES[0], audit.EXPECTED_HASHES[0]["C"])
        self.assertEqual(primary.EXPECTED_C_OPEN_HASHES[1], audit.EXPECTED_HASHES[1]["C"])

    def test_ledger_hash_and_evidence_links_are_current(self) -> None:
        ledger = json.loads(read(LEDGER))
        entries = [item for item in ledger["entries"] if "(GLD102)" in item["name"]]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry["document"], OWNER.relative_to(ROOT).as_posix())
        self.assertEqual(entry["document_sha256_16"], staged_index_hash(OWNER))
        self.assertEqual(entry["status"], "verified")
        self.assertEqual(entry["primary_verifier"], PRIMARY.relative_to(ROOT).as_posix())
        self.assertEqual(entry["independent_audit"], AUDIT.relative_to(ROOT).as_posix())
        self.assertEqual(entry["review"], REVIEW.relative_to(ROOT).as_posix())
        self.assertEqual(entry["external_binaries"], [])
        self.assertIn("p=0", entry["note"])
        self.assertIn("p=1", entry["note"])
        self.assertIn("B=C=0 endpoint", entry["note"])
        self.assertIn("UNRESOLVED", entry["note"])


if __name__ == "__main__":
    unittest.main()
