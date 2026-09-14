"""Focused replay and RUP controls for the full scaffold source exclusion."""

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

from krenn_gu.scaffold_source import build  # noqa: E402
from krenn_gu.source_quotient_core import rup_conflict  # noqa: E402
from claims.finite.n08.verify_eight_vertex_scaffold_full_source_exclusion import (  # noqa: E402
    replay,
)
from claims.finite.n08.verify_eight_vertex_scaffold_subsystem_controls import (  # noqa: E402
    FIXTURE as CONTROL_FIXTURE,
    replay as replay_controls,
)


class ScaffoldFullSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture_path = HERE / "fixtures" / "eight_vertex_scaffold_full_source_rup.json"
        cls.payload = json.loads(cls.fixture_path.read_text(encoding="utf-8"))
        cls.generated = build("full")

    def test_exact_full_proof_replay(self) -> None:
        result = replay(self.payload, generated=self.generated)
        self.assertEqual(result["status"], "EXACT_FULL_SCAFFOLD_RUP_PASS")
        self.assertEqual(result["word_count"], 6561)
        self.assertEqual(result["variable_count"], 33792)
        self.assertTrue(result["empty_clause_derived"])
        self.assertEqual(result["global_status"], "UNRESOLVED")

    def test_certificate_integrity_and_proof_controls(self) -> None:
        wrong_hash = copy.deepcopy(self.payload)
        wrong_hash["equation_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "certificate equation_sha256 mismatch"):
            replay(wrong_hash, generated=self.generated)

        invalid_index = copy.deepcopy(self.payload)
        invalid_index["core_clause_indices"][0] = len(self.generated[0].clauses)
        with self.assertRaisesRegex(ValueError, "invalid original clause index"):
            replay(invalid_index, generated=self.generated)

        missing_final_empty = copy.deepcopy(self.payload)
        missing_final_empty["rup_additions"].pop()
        with self.assertRaisesRegex(ValueError, "proof must end with empty clause"):
            replay(missing_final_empty, generated=self.generated)

        false_lemma = copy.deepcopy(self.payload)
        false_lemma["rup_additions"].insert(0, [1])
        with self.assertRaisesRegex(ValueError, "RUP step 0 is not implied"):
            replay(false_lemma, generated=self.generated)

        necessary_omission = copy.deepcopy(self.payload)
        necessary_omission["rup_additions"].pop(1)
        with self.assertRaisesRegex(ValueError, "RUP step 1 is not implied"):
            replay(necessary_omission, generated=self.generated)

    def test_rup_conflict_direct_controls(self) -> None:
        self.assertTrue(rup_conflict([(1,)], assumptions=(-1,)))
        self.assertTrue(rup_conflict([(1,), (2,)], assumptions=(-1, -2)))
        self.assertFalse(rup_conflict([(1,)], assumptions=(2,)))

    def test_physical_subsystem_controls_and_broken_support(self) -> None:
        controls = json.loads(CONTROL_FIXTURE.read_text(encoding="utf-8"))
        result = replay_controls(controls)
        self.assertEqual([f["exact_subsystem_words"] for f in result["families"]],
                         [477, 1065, 1869])
        mutated = copy.deepcopy(controls)
        mutated["families"][0]["supports"][0][1] = [2, 2]
        with self.assertRaisesRegex(ValueError, "subsystem failure"):
            replay_controls(mutated)

    def test_independent_portable_audit(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "claims/finite/n08/audit_eight_vertex_scaffold_full_source_exclusion.py")],
            cwd=REPO_ROOT, capture_output=True, text=True, encoding="utf-8",
            timeout=30, check=True,
        )
        result = json.loads(proc.stdout)
        self.assertEqual(result["status"], "PASS_PORTABLE_RUP_REPLAY")
        self.assertEqual(result["rup_additions"], 108)
        self.assertTrue(result["proof_checked_by_this_audit"])

if __name__ == "__main__":
    unittest.main()
