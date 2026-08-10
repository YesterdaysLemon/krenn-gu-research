"""Regression tests for the two-even-cycle transport SAT compiler."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n14")

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
from krenn_gu.explore_random_even_cycle_forks import cycle_edges


def fixture_path(relative: str) -> Path:
    """Resolve a historically root-relative fixture from any caller CWD."""
    return REPO_ROOT / relative


class TwoEvenCycleRuleSatTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_10_support_samples425.json"
            ).read_text(encoding="utf-8")
        )
        self.analysis = json.loads(
            fixture_path(
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
