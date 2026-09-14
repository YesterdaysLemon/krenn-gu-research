"""Tests for the exact boundary-quotient probe on the 134-entry support."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SUPPORT = HERE / "fixtures" / "recursive_physical_support_n8_four_cut_survivor_134.json"
EXPECTED = HERE / "fixtures" / "eight_vertex_physical_boundary_quotient_134.json"
PROBE = REPO_ROOT / "tools" / "explore" / "probe_physical_boundary_quotient_134.py"
AUDIT = (
    REPO_ROOT
    / "claims"
    / "finite"
    / "n08"
    / "audit_eight_vertex_physical_boundary_quotient_134.py"
)


def run_python(*arguments: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *(str(argument) for argument in arguments)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


class PhysicalBoundaryQuotient134Tests(unittest.TestCase):
    def test_probe_reproduces_frozen_result_exactly(self) -> None:
        completed = run_python(PROBE, SUPPORT, "--expected", EXPECTED)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["outcome"],
            "NO_EXCLUSION_BY_THIS_BOUNDARY_QUOTIENT_MECHANISM",
        )
        self.assertFalse(result["exact_support_exclusion"])
        self.assertEqual(result["boundary_orbit"]["applicable_placements"], 2)
        self.assertEqual(
            result["full_word_census"]["mixed_fibres_with_at_most_two_terms"],
            [],
        )

    def test_independent_audit_reconstructs_identity_and_census(self) -> None:
        completed = run_python(AUDIT, "--support", SUPPORT, "--expected", EXPECTED)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["distinct_live_relation"], "g88*g91 = g82*g97")
        self.assertEqual(result["directly_related_matching_monomial_pairs"], 0)
        self.assertFalse(result["exact_support_exclusion_claimed"])
        self.assertFalse(result["weight_realization_claimed"])

    def test_changed_frozen_outcome_is_rejected(self) -> None:
        mutated = json.loads(EXPECTED.read_text(encoding="utf-8"))
        mutated["outcome"] = "MUTATED"
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "mutated.json"
            path.write_text(json.dumps(mutated), encoding="utf-8")
            completed = run_python(PROBE, SUPPORT, "--expected", path)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("computed result differs", completed.stderr)


if __name__ == "__main__":
    unittest.main()
