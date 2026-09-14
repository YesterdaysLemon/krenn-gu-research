"""Focused tests for the exact two-slice transfer identities."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.two_slice_transfer import (  # noqa: E402
    four_patterns,
    make_pattern,
    replay,
)


class TwoSliceTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_path = HERE / "fixtures" / "eight_vertex_two_slice_transfer.json"
        cls.payload = json.loads(cls.fixture_path.read_text(encoding="utf-8"))

    def test_fixture_replays_exactly(self) -> None:
        result = replay(self.payload)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["matching_count"], 105)
        self.assertEqual(result["source_term_counts"], [6, 6, 6, 6, 18, 18, 18, 18])
        self.assertEqual(result["physical_degree_bound"], 6)
        self.assertFalse(result["uses_rho"])
        self.assertEqual(result["cofactor_divisions"], 0)

    def test_fixture_matches_seed_generator_core_fields(self) -> None:
        generated = make_pattern(0, 0, 1)
        for key in (
            "schema",
            "n",
            "field",
            "family",
            "parameters",
            "entry_families",
            "zero_entry_ids",
            "nonzero_entry_ids",
            "target_monomial",
            "sources",
            "equation_convention",
            "identity",
            "uses_boundary_relation",
            "requires_nonzero_proper_cofactor",
            "cofactor_divisions",
        ):
            with self.subTest(key=key):
                self.assertEqual(self.payload[key], generated[key])

    def test_all_four_canonical_patterns_replay(self) -> None:
        patterns = four_patterns()
        self.assertEqual(len(patterns), 4)
        self.assertEqual(
            [(p["parameters"]["z_colour"], p["parameters"]["first_slice_colour"])
             for p in patterns],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
        )
        for pattern in patterns:
            with self.subTest(parameters=pattern["parameters"]):
                self.assertEqual(len(pattern["zero_entry_ids"]), 18)
                self.assertEqual(replay(pattern)["status"], "PASS")

    def test_mutations_are_rejected(self) -> None:
        wrong_sign = copy.deepcopy(self.payload)
        wrong_sign["sources"][0]["coefficient"] *= -1
        with self.assertRaisesRegex(ValueError, "polynomial residual"):
            replay(wrong_sign)

        omitted_row = copy.deepcopy(self.payload)
        omitted_row["sources"].pop(0)
        with self.assertRaisesRegex(ValueError, "polynomial residual"):
            replay(omitted_row)

        changed_pure_word = copy.deepcopy(self.payload)
        changed_pure_word["sources"][4]["word"] = "02222222"
        with self.assertRaisesRegex(ValueError, "polynomial residual"):
            replay(changed_pure_word)

        missing_nonzero = copy.deepcopy(self.payload)
        missing_nonzero["nonzero_entry_ids"].remove(47)
        with self.assertRaisesRegex(ValueError, "target monomial"):
            replay(missing_nonzero)

        bad_multiplier_degree = copy.deepcopy(self.payload)
        bad_multiplier_degree["sources"][0]["multiplier"].append(1)
        with self.assertRaisesRegex(ValueError, "invalid physical multiplier"):
            replay(bad_multiplier_degree)

        for identifier in self.payload["zero_entry_ids"]:
            relaxed = copy.deepcopy(self.payload)
            relaxed["zero_entry_ids"].remove(identifier)
            with self.subTest(omitted_zero=identifier), self.assertRaisesRegex(
                ValueError, "polynomial residual"
            ):
                replay(relaxed)

    def test_independent_audit_reports_pass(self) -> None:
        audit = REPO_ROOT / "claims" / "finite" / "n08" / (
            "audit_eight_vertex_two_slice_transfer.py"
        )
        completed = subprocess.run(
            [sys.executable, str(audit), "--fixture", str(self.fixture_path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        report = json.loads(completed.stdout)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["patterns"], 4)
        self.assertEqual(report["guard_size"], 18)
        self.assertEqual(report["global_krenn_gu_status"], "UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
