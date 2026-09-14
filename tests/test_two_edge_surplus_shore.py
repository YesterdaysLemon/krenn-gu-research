"""Focused tests for the exact two-edge surplus-shore certificate."""

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

from krenn_gu.two_edge_surplus_shore import (  # noqa: E402
    four_patterns,
    make_pattern,
    replay,
)


class TwoEdgeSurplusShoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_path = HERE / "fixtures" / "eight_vertex_two_edge_surplus_shore.json"
        cls.payload = json.loads(cls.fixture_path.read_text(encoding="utf-8"))

    def test_fixture_replays_exactly(self) -> None:
        result = replay(self.payload)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["matching_count"], 105)
        self.assertEqual(result["source_term_counts"], [15, 15, 15, 15])
        self.assertEqual(result["physical_degree_bound"], 6)
        self.assertFalse(result["uses_rho"])
        self.assertEqual(result["cofactor_divisions"], 0)

    def test_fixture_matches_seed_generator_core_fields(self) -> None:
        generated = make_pattern(adjacent=False, same_alternates=False)
        for key in (
            "schema",
            "n",
            "shore",
            "covering_edges",
            "base_colour",
            "moving_vertices",
            "alternate_colours",
            "zero_entry_ids",
            "nonzero_entry_ids",
            "target_monomial",
            "sources",
        ):
            with self.subTest(key=key):
                self.assertEqual(self.payload[key], generated[key])

    def test_all_four_generated_patterns_replay(self) -> None:
        patterns = four_patterns()
        self.assertEqual(len(patterns), 4)
        self.assertEqual(
            [(p["covering_edges"], p["alternate_colours"]) for p in patterns],
            [
                ([[3, 5], [6, 7]], [2, 1]),
                ([[3, 5], [6, 7]], [1, 1]),
                ([[3, 5], [3, 7]], [2, 1]),
                ([[3, 5], [3, 7]], [1, 1]),
            ],
        )
        for pattern in patterns:
            with self.subTest(
                covering_edges=pattern["covering_edges"],
                alternate_colours=pattern["alternate_colours"],
            ):
                self.assertEqual(len(pattern["zero_entry_ids"]), 15)
                self.assertEqual(replay(pattern)["status"], "PASS")

    def test_polynomial_and_guard_mutations_are_rejected(self) -> None:
        wrong_sign = copy.deepcopy(self.payload)
        wrong_sign["sources"][0]["coefficient"] *= -1
        with self.assertRaisesRegex(ValueError, "polynomial residual"):
            replay(wrong_sign)

        omitted_source = copy.deepcopy(self.payload)
        omitted_source["sources"].pop(0)
        with self.assertRaisesRegex(ValueError, "polynomial residual"):
            replay(omitted_source)

        for identifier in self.payload["zero_entry_ids"]:
            relaxed = copy.deepcopy(self.payload)
            relaxed["zero_entry_ids"].remove(identifier)
            with self.subTest(omitted_zero=identifier), self.assertRaisesRegex(
                ValueError, "polynomial residual"
            ):
                replay(relaxed)

        missing_required_nonzero = copy.deepcopy(self.payload)
        missing_required_nonzero["nonzero_entry_ids"].remove(174)
        with self.assertRaisesRegex(ValueError, "target monomial"):
            replay(missing_required_nonzero)

    def test_source_multiplier_entries_may_also_be_zero(self) -> None:
        for identifier in (172, 244):
            specialized = copy.deepcopy(self.payload)
            specialized["zero_entry_ids"].append(identifier)
            with self.subTest(zero_multiplier=identifier):
                self.assertEqual(replay(specialized)["status"], "PASS")

    def test_independent_audit_reports_pass(self) -> None:
        audit = REPO_ROOT / "claims" / "finite" / "n08" / (
            "audit_eight_vertex_degree6_source_134.py"
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
        self.assertEqual(report["schema"], "eight-vertex-degree6-source-independent-audit-v1")
        self.assertEqual(report["global_krenn_gu_status"], "UNRESOLVED")


if __name__ == "__main__":
    unittest.main()
