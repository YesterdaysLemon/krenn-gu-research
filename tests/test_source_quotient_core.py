"""Exact small-core replay and rejection controls, without any SAT solver."""

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
else:
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.source_quotient_core import replay_source_quotient_core, rup_conflict  # noqa: E402


class SourceQuotientCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instance = build_recursive_tensor_support_cnf(8, column_killers=False, fix_root_killers=False)
        cls.packet = json.loads((HERE / "fixtures" / "recursive_source_quotient_n8_core.json").read_text())

    def test_plain_unit_propagation_rejects_false_empty_proofs(self):
        self.assertFalse(rup_conflict([(1, 2)]))
        self.assertFalse(rup_conflict([(1, 2)], [-1]))
        self.assertTrue(rup_conflict([(1, 2)], [-1, -2]))
        self.assertTrue(rup_conflict([(1,), (-1,)]))
        self.assertTrue(rup_conflict([(1,), (-1, 2), (-2,)]))
        self.assertFalse(rup_conflict([(1, 2), (-1, -2)]))

    def test_source_algebra_and_264_clause_core_replay(self):
        result = replay_source_quotient_core(self.instance, self.packet)
        self.assertEqual(result["physical_guard_count"], 54)
        self.assertEqual(result["base_recursive_clauses"], 209)
        self.assertEqual(result["core_clauses"], 264)
        self.assertEqual(result["rup_additions"], 3)
        self.assertFalse(result["killers_or_ratio_clauses"])

    def test_forged_premise_proof_and_scope_are_rejected(self):
        for mutation in ("premise", "false_empty", "physical_cut", "template", "schema"):
            changed = copy.deepcopy(self.packet)
            if mutation == "premise":
                changed["core_clauses"][0] = [self.instance.cnf.nv + 1]
            elif mutation == "false_empty":
                changed["rup_additions"] = [[]]
            elif mutation == "physical_cut":
                changed["physical_cut"].pop()
            elif mutation == "template":
                changed["coefficient_support"][0][1] = None
            else:
                changed["schema"] = "unchecked-v0"
            with self.assertRaises(ValueError, msg=mutation):
                replay_source_quotient_core(self.instance, changed)


if __name__ == "__main__":
    unittest.main()
