"""Tests for the exact 25-literal physical-hafnian identity."""

from __future__ import annotations

import copy
import json
import sys as _bootstrap_sys
import unittest
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.eight_vertex_physical_hafnian_identity import (  # noqa: E402
    analyze_pattern_orbit,
    entry_id,
    perfect_matchings,
    replay_eight_vertex_physical_hafnian_identity,
)


class EightVertexPhysicalHafnianIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            (HERE / "fixtures" / "eight_vertex_physical_hafnian_identity_25_literal.json").read_text(
                encoding="utf-8"
            )
        )

    def test_independent_integer_polynomial_replay(self) -> None:
        result = replay_eight_vertex_physical_hafnian_identity(self.payload)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["full_word_monomial_counts_after_zeros"], [9, 8, 10, 8])
        self.assertEqual(result["rhs_coefficient"], 1)
        self.assertFalse(result["proof_uses_division"])
        self.assertFalse(result["parent_coverage_claimed"])
        self.assertEqual(len(result["physical_cut"]), 25)

    def test_entry_numbering_and_matching_cover(self) -> None:
        self.assertEqual(entry_id(0, 5, 0, 1), 38)
        self.assertEqual(entry_id(5, 0, 1, 0), 38)
        self.assertEqual(entry_id(6, 7, 1, 0), 247)
        self.assertEqual(len(perfect_matchings(tuple(range(8)))), 105)

    def test_mutated_or_weakly_typed_patterns_are_rejected(self) -> None:
        mutations = {}
        for name in (
            "boolean_id",
            "duplicate_id",
            "missing_literal",
            "wrong_word",
            "restored_removed_requirement",
            "scope_flag",
        ):
            mutations[name] = copy.deepcopy(self.payload)
        mutations["boolean_id"]["zero_entry_ids"][0] = True
        mutations["duplicate_id"]["nonzero_entry_ids"][-1] = 38
        mutations["missing_literal"]["physical_cut"].pop()
        mutations["wrong_word"]["target_words"][0] = "00000000"
        mutations["restored_removed_requirement"]["nonzero_entry_ids"].append(172)
        mutations["scope_flag"]["all_unspecified_entries_arbitrary"] = False
        for name, payload in mutations.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                replay_eight_vertex_physical_hafnian_identity(payload)

    def test_preserved_parent_survivor_avoids_every_orbit_image(self) -> None:
        support = json.loads(
            (HERE / "fixtures" / "recursive_physical_support_n8_four_cut_survivor_134.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(len(support["nonzero_entry_ids"]), 134)
        result = analyze_pattern_orbit(self.payload, support["nonzero_entry_ids"])
        self.assertEqual(result["images_including_duplicates"], 241920)
        self.assertEqual(result["minimum_guard_failures"], 1)
        self.assertEqual(len(result["closest_images"]), 3)
        self.assertEqual(
            {row["failed_literals"][0] for row in result["closest_images"]},
            {-226, 97, 122},
        )


if __name__ == "__main__":
    unittest.main()
