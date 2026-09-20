"""Exact scope and interference controls for the two-sided cycle construction."""

import importlib.util
from itertools import combinations
from pathlib import Path
import unittest

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "two_sided_cycle_control",
    ROOT / "claims/arbitrary-order/verify_common_star_two_sided_cycle_control.py",
)
CONTROL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CONTROL)


class TwoSidedCycleControlTests(unittest.TestCase):
    def test_parameter_tower_is_nonvacuous_and_failure_is_nonzero(self):
        CONTROL.check_nonzero_parameters()
        self.assertFalse(CONTROL.vanishes(1))
        self.assertFalse(CONTROL.vanishes((CONTROL.R**2 + 1) / (12 * CONTROL.R)))

    def test_actual_array_meets_exactly_the_claimed_subsystem(self):
        a, b = CONTROL.matrices()
        self.assertEqual(CONTROL.check_support(a, b), 27)
        CONTROL.check_s1(a, b)
        self.assertEqual(CONTROL.check_cut_identities(a, b), 72)
        self.assertEqual(CONTROL.check_two_sided_defects(a, b), 16)
        self.assertEqual(CONTROL.check_binary_s1_s2(a, b), 90)
        cut, value = CONTROL.check_global_failure(a, b)
        self.assertEqual(cut, (0, 1, 3))
        self.assertFalse(CONTROL.vanishes(value))

    def test_product_preserving_factor_mutation_breaks_double_cuts(self):
        a, b = CONTROL.matrices()
        products = a.multiply_elementwise(b)
        for row in (3, 4):
            for column in (5, 6):
                a[row, column] = 1
                b[row, column] = products[row, column]
        # S1 and both localized faces survive, so checking only those
        # constraints would not detect this scientific error.
        CONTROL.check_s1(a, b)
        self.assertEqual(CONTROL.check_two_sided_defects(a, b), 16)
        self.assertFalse(CONTROL.vanishes(CONTROL.cut_source(a, b, (3, 4))))

    def test_ordinary_matching_polynomial_drops_required_interference(self):
        a, b = CONTROL.matrices()
        products = a.multiply_elementwise(b)
        rows = (3, 4)
        columns = tuple(index for index in range(9) if index not in rows)
        diagonal_only = sum(
            CONTROL.permanent(products, selected_rows, selected_columns)
            for size in range(3)
            for selected_rows in combinations(rows, size)
            for selected_columns in combinations(columns, size)
        )
        self.assertFalse(CONTROL.vanishes(diagonal_only))
        self.assertTrue(CONTROL.vanishes(CONTROL.cut_source(a, b, rows)))

    def test_both_full_cycle_faces_have_their_literal_binary_sources(self):
        a, b = CONTROL.matrices()
        cycle = (0, 1, 2)
        exterior = (3, 4, 5, 6, 7, 8)
        for size in range(4):
            for selected in combinations(cycle, size):
                with self.subTest(selected=selected, outside=0):
                    expected = sp.Integer(size == 3)
                    value = CONTROL.cut_source(a, b, (*selected, *exterior))
                    self.assertTrue(CONTROL.equal_mod_ideal(value, expected))
                with self.subTest(selected=selected, outside=1):
                    expected = sp.Integer(size == 0)
                    value = CONTROL.cut_source(a, b, selected)
                    self.assertTrue(CONTROL.equal_mod_ideal(value, expected))


if __name__ == "__main__":
    unittest.main()
