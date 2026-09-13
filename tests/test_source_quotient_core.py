"""Exact small-core replay and rejection controls, without any SAT solver."""

from __future__ import annotations

import copy
import json
import sys as _bootstrap_sys
import unittest
from pathlib import Path as _BootstrapPath
from unittest.mock import patch

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.source_quotient_core import (  # noqa: E402
    replay_source_quotient_core,
    rup_conflict,
    unit_propagation_core,
)


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
        self.assertIsNone(unit_propagation_core([(1, 2), (-1, -2)]))
        core = unit_propagation_core([(1,), (-1, 2), (-2,), (8, 9)])
        self.assertEqual(core, [(1,), (-1, 2), (-2,)])

    def test_source_algebra_and_264_clause_core_replay(self):
        result = replay_source_quotient_core(self.instance, self.packet)
        self.assertEqual(result["physical_guard_count"], 54)
        self.assertEqual(result["base_recursive_clauses"], 209)
        self.assertEqual(result["core_clauses"], 264)
        self.assertEqual(result["rup_additions"], 3)
        self.assertFalse(result["killers_or_ratio_clauses"])

    def test_second_source_projects_with_one_plain_rup_step(self):
        packet = json.loads((HERE / "fixtures" / "recursive_source_quotient_n8_second_core.json").read_text())
        result = replay_source_quotient_core(self.instance, packet)
        self.assertEqual(result["physical_guard_count"], 38)
        self.assertEqual(result["base_recursive_clauses"], 161)
        self.assertEqual(result["core_clauses"], 200)
        self.assertEqual(result["rup_additions"], 1)
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

    def test_third_source_projects_with_one_plain_rup_step(self):
        packet = json.loads((HERE / "fixtures" / "recursive_source_quotient_n8_third_core.json").read_text())
        result = replay_source_quotient_core(self.instance, packet)
        self.assertEqual(result["physical_guard_count"], 32)
        self.assertEqual(result["base_recursive_clauses"], 157)
        self.assertEqual(result["core_clauses"], 190)
        self.assertEqual(result["rup_additions"], 1)
        self.assertFalse(result["killers_or_ratio_clauses"])

    def test_row_space_clause_projects_through_the_typed_boundary(self):
        instance = build_recursive_tensor_support_cnf(
            6,
            column_killers=False,
            fix_root_killers=False,
        )
        packet = json.loads(
            (HERE / "fixtures" / "recursive_row_space_n6_source_core.json").read_text()
        )
        with patch(
            "krenn_gu.recursive_tensor_quotient.UnitSignedQuotient",
            side_effect=AssertionError("row-space discovery called during replay"),
        ):
            result = replay_source_quotient_core(instance, packet)
        self.assertEqual(result["algebra_certificate_kind"], "recursive_laurent_row_space")
        self.assertEqual(result["physical_guard_count"], 43)
        self.assertEqual(result["base_recursive_clauses"], 102)
        self.assertEqual(result["core_clauses"], 146)
        self.assertEqual(result["rup_additions"], 1)

        for mutation in ("certificate_kind", "missing_coefficient", "extra_coefficient"):
            changed = copy.deepcopy(packet)
            if mutation == "certificate_kind":
                changed["algebra_certificate"]["schema"] = "caller-verified-v0"
            elif mutation == "missing_coefficient":
                changed["coefficient_support"].pop()
            else:
                used = {row[0] for row in changed["coefficient_support"]}
                extra = next(
                    variable
                    for variable in instance.coefficients.values()
                    if variable not in used
                )
                changed["coefficient_support"].append([extra, 0])
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                replay_source_quotient_core(instance, changed)

    def test_latest_136_entry_support_has_a_checked_27_literal_cut(self):
        packet = json.loads(
            (
                HERE
                / "fixtures"
                / "recursive_source_quotient_n8_latest136_core.json"
            ).read_text()
        )
        result = replay_source_quotient_core(self.instance, packet)
        self.assertEqual(result["algebra_certificate_kind"], "recursive_quotient_singleton")
        self.assertEqual(result["physical_guard_count"], 27)
        self.assertEqual(result["base_recursive_clauses"], 107)
        self.assertEqual(result["core_clauses"], 135)
        self.assertEqual(result["rup_additions"], 1)


if __name__ == "__main__":
    unittest.main()
