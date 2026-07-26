"""Regression tests for the two-even-cycle transport SAT compiler."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    validate_simple_certificate,
)
from explore_fourteen_vertex_equality_factor_family import (
    contiguous_cycles,
)
from explore_random_even_cycle_forks import cycle_edges


class TwoEvenCycleRuleSatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            Path(
                "tmp/fourteen_vertex_c4_10_support_samples425.json"
            ).read_text(encoding="utf-8")
        )
        self.analysis = json.loads(
            Path(
                "tmp/fourteen_vertex_c4_10_sample425_0_fork.json"
            ).read_text(encoding="utf-8")
        )
        self.cycles = contiguous_cycles((4, 10))
        self.full_edges = {
            item
            for cycle in self.cycles
            for item in cycle_edges(cycle)
        }

    def test_existing_simple_certificate_replays(self) -> None:
        factors, colourings = validate_simple_certificate(
            self.analysis,
            self.manifest["survivors"][0],
            self.cycles,
            self.full_edges,
        )
        self.assertEqual(tuple(map(len, factors)), (7, 7, 7))
        self.assertEqual(len(colourings), 3)

    def test_changed_target_activity_is_rejected(self) -> None:
        changed = copy.deepcopy(self.analysis)
        changed["certificate"]["alternatives"][0][
            "target_activity"
        ][-1] += 1
        with self.assertRaisesRegex(
            AssertionError, "target activity changed"
        ):
            validate_simple_certificate(
                changed,
                self.manifest["survivors"][0],
                self.cycles,
                self.full_edges,
            )


if __name__ == "__main__":
    unittest.main()
