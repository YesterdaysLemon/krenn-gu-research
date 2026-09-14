"""Exact tests for the repeated-port common-star parent control."""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "common_star_repeated_port_control"
SPEC = importlib.util.spec_from_file_location(
    MODULE_NAME,
    ROOT
    / "claims/arbitrary-order"
    / "verify_protected_scaffold_common_star_repeated_port_control.py",
)
CONTROL = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = CONTROL
assert SPEC.loader is not None
SPEC.loader.exec_module(CONTROL)


class ProtectedCommonStarRepeatedPortTests(unittest.TestCase):
    def test_qsqrt3_inverse_is_exact(self):
        r = CONTROL.Q3(Fraction(2), Fraction(1))
        self.assertEqual(r.inverse(), CONTROL.Q3(Fraction(2), Fraction(-1)))
        self.assertEqual(r * r.inverse(), CONTROL.ONE)
        with self.assertRaises(ZeroDivisionError):
            CONTROL.ZERO.inverse()

    def test_all_constant_singleton_and_double_component_targets(self):
        result = CONTROL.check_target_layers()
        self.assertEqual(
            result["counts"], {"constant": 3, "singleton": 84, "double": 1092}
        )
        self.assertEqual(result["mismatches"], [])

    def test_binary_fiber_component_word_is_an_exact_global_failure(self):
        failure = CONTROL.binary_fiber_failure()
        self.assertEqual(failure["component_word"], "01" * 7)
        self.assertEqual(failure["component_source"], "1/128")
        self.assertEqual(failure["physical_source"], "1/128")
        self.assertEqual(failure["target"], "0")

    def test_explicit_u4_word_has_one_nonzero_matching_product(self):
        failure = CONTROL.find_u4_failure()
        self.assertEqual(failure["source"], "1/4")
        self.assertEqual(failure["nonzero_perfect_matching_terms"], 1)
        self.assertEqual(failure["unique_matching_product"], "1/4")
        self.assertEqual(failure["target"], "0")

    def test_all_64_coherent_k222_subsets_have_the_stated_partition(self):
        table, histogram = CONTROL.local_k222_table()
        self.assertEqual(len(table), 64)
        self.assertEqual(
            histogram,
            {
                "0": 27,
                "1/2": 12,
                "1": 10,
                "-1/2": 8,
                "4": 6,
                "-11": 1,
            },
        )
        self.assertEqual(sum(value != "0" for value in histogram.elements()), 37)

    def test_weight_mutation_is_detected_by_an_actual_target_row(self):
        edges = list(CONTROL.EDGES)
        u, v, a, b, center, leaf = edges[0]
        edges[0] = (u, v, a, b, center, 2 * leaf)
        result = CONTROL.check_target_layers(tuple(edges), stop_after=1)
        self.assertEqual(len(result["mismatches"]), 1)
        mismatch = result["mismatches"][0]
        self.assertEqual(mismatch["layer"], "singleton")
        self.assertNotEqual(mismatch["physical_source"], mismatch["target"])
        self.assertEqual(mismatch["physical_source"], mismatch["component_source"])


if __name__ == "__main__":
    unittest.main()
