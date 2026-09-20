"""Scientific controls for full-cut localization; no finite proof extrapolation."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'binary_cycle_localization',
    ROOT / 'claims/arbitrary-order/verify_common_star_binary_cycle_localization.py',
)
CONTROL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CONTROL)


class BinaryCycleLocalizationTests(unittest.TestCase):
    def test_deletion_keeps_exterior_terms_and_rejects_a_second_column(self):
        self.assertTrue(CONTROL.symbolic_deletion()['invalid_second_column_rejected'])

    def test_actual_factors_realize_face_and_fail_global_target(self):
        result = CONTROL.face_control()
        self.assertEqual(result['face_words_checked'], 8)
        self.assertEqual(result['full_exterior_value'], 0)
        self.assertEqual(result['failed_global_word'], '00010')
        self.assertEqual(result['failed_global_value'], 1)
        self.assertEqual(result['status'], 'ONE_FACE_CONTROL_NOT_FB')

    def test_incorrect_cycle_factor_breaks_the_face_target(self):
        a, b = CONTROL.control_matrices(cycle_leaf=sp.Integer(-1))
        self.assertNotEqual(CONTROL.binary_amplitude(a, b, (1, 0, 0, 0, 0)), 0)
        with patch.object(CONTROL, 'control_matrices', return_value=(a, b)):
            with self.assertRaises(AssertionError):
                CONTROL.face_control()

    def test_nonfactorizing_top_defect_is_load_bearing(self):
        s = (-3 + sp.sqrt(-3)) / 6
        q = -1 - s
        a, b = CONTROL.control_matrices(s)
        actual = CONTROL.local_source(a, b, (3, 4), (0, 1, 2))
        naive = (1 + s)**3
        self.assertEqual(sp.simplify(actual), 0)
        self.assertNotEqual(sp.simplify(naive), 0)
        self.assertEqual(sp.simplify(actual - naive - q**3), 0)

    def test_hamilton_cycle_is_a_full_binary_sharp_control(self):
        self.assertEqual(sum(CONTROL.cycle_control(k) for k in (3, 4, 5)), 56)

    def test_general_face_control_keeps_both_factorials(self):
        result = CONTROL.arbitrary_length_control_identities()
        self.assertEqual(result['moment_sizes_checked'], 4)
        # One factorial instead of two changes the second compound moment.
        s = sp.Symbol('s')
        wrong_moment = sp.factorial(2)**2 * s**2 / sp.factorial(2)
        self.assertNotEqual(sp.expand(wrong_moment - s**2), 0)


if __name__ == '__main__':
    unittest.main()
