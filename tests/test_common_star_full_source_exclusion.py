"""Scientific tests for the common-star full-source exclusion companion."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "common_star_full_source_exclusion",
    ROOT / "claims/arbitrary-order/verify_common_star_full_source_exclusion.py",
)
CONTROL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = CONTROL
SPEC.loader.exec_module(CONTROL)


class CommonStarFullSourceExclusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = CONTROL.exact_fixtures()

    def test_all_ab_words_match_literal_physical_source_at_k2_k3(self):
        self.assertEqual(CONTROL.compare_all_ab_words(2, self.fixtures[2]), 81)
        self.assertEqual(CONTROL.compare_all_ab_words(3, self.fixtures[3]), 729)

    def test_odd_component_word_contraction_uses_no_ab_extension(self):
        self.assertEqual(
            CONTROL.diagonal_component_contraction(3, self.fixtures[3]),
            0,
        )
        self.assertEqual(CONTROL.odd_target_closed_form(3), -6)
        for k in range(3, 14, 2):
            self.assertEqual(CONTROL.odd_target_closed_form(k), 2 - 2**k)
            self.assertNotEqual(CONTROL.odd_target_closed_form(k), 0)

    def test_four_crossed_orthogonal_probes_give_outer_product_at_k2_k4(self):
        for k in (2, 4):
            with self.subTest(k=k):
                receipt = CONTROL.even_probe_certificate(k, self.fixtures[k])
                self.assertEqual(receipt["source"], receipt["outer"])
                self.assertEqual(receipt["source_determinant"], 0)
                expected = CONTROL.even_target_closed_form(k)
                self.assertEqual(receipt["target"], expected["matrix"])
                self.assertEqual(receipt["target_determinant"], expected["determinant"])
                self.assertNotEqual(receipt["target_determinant"], 0)

    def test_even_target_minor_closed_form_for_arbitrary_checked_lengths(self):
        for k in range(2, 42, 2):
            with self.subTest(k=k):
                result = CONTROL.even_target_closed_form(k)
                self.assertEqual(
                    CONTROL.determinant_2x2(result["matrix"]),
                    1 + 2 ** (k - 1),
                )

    def test_k1_is_a_valid_full_ghz_exception(self):
        self.assertEqual(CONTROL.k1_full_ghz_check(), 81)
        self.assertEqual(CONTROL.odd_target_closed_form(1), 0)

    def test_dropping_one_cross_orthogonality_breaks_the_rank_argument(self):
        rows, leaves = CONTROL.canonical_even_probes(2)
        mutated_rows = [list(system) for system in rows]
        mutated_leaves = [list(system) for system in leaves]

        # Break only the crossed global pair (p,q)=(0,0), at both sites,
        # while keeping the other three crossed probe pairs orthogonal.
        mutated_leaves[0][0] = (
            CONTROL.Fraction(1),
            CONTROL.Fraction(0),
            CONTROL.Fraction(1),
        )
        mutated_rows[0][1] = (
            CONTROL.Fraction(1),
            CONTROL.Fraction(0),
            CONTROL.Fraction(1),
        )
        mutated_rows = tuple(tuple(system) for system in mutated_rows)
        mutated_leaves = tuple(tuple(system) for system in mutated_leaves)

        broken_global_pairs = {
            (p, q)
            for p in range(2)
            for q in range(2)
            if any(
                CONTROL.dot(mutated_rows[p][component], mutated_leaves[q][component])
                != 0
                for component in range(2)
            )
        }
        self.assertEqual(broken_global_pairs, {(0, 0)})

        with self.assertRaisesRegex(ValueError, "all four crossed probe pairs"):
            CONTROL.validate_cross_orthogonality(mutated_rows, mutated_leaves)

        # If validation is deliberately bypassed, the empty active set
        # survives in entry (0,0), so the full-layer outer product is false.
        receipt = CONTROL.even_probe_certificate(
            2,
            self.fixtures[2],
            row_systems=mutated_rows,
            leaf_systems=mutated_leaves,
            require_orthogonality=False,
        )
        self.assertNotEqual(receipt["source"], receipt["outer"])
        directly_contracted_target = tuple(
            tuple(
                sum(
                    CONTROL.Fraction(
                        mutated_rows[p][0][color]
                        * mutated_leaves[q][0][color]
                        * mutated_rows[p][1][color]
                        * mutated_leaves[q][1][color]
                    )
                    for color in CONTROL.COLORS
                )
                for q in range(2)
            )
            for p in range(2)
        )
        self.assertEqual(receipt["target"], directly_contracted_target)
        self.assertNotEqual(receipt["target"], CONTROL.even_target_probe_matrix(2))

    def test_off_family_center_leaf_entry_breaks_the_hafnian_formula(self):
        mutation = CONTROL.off_family_center_leaf_mutation()
        self.assertEqual(mutation["formula"], 0)
        self.assertEqual(mutation["literal"], 1001)
        self.assertNotEqual(mutation["literal"], mutation["formula"])

    def test_primary_receipt_preserves_scope(self):
        receipt = CONTROL.run_primary_replay()
        self.assertEqual(receipt["ab_words_checked"], 810)
        self.assertEqual(receipt["k1_full_words_checked"], 81)
        self.assertEqual(
            receipt["status"],
            "ODD_COMPONENT_TARGET_AND_EVEN_CSFULL_EXCLUSION_REPLAY",
        )


if __name__ == "__main__":
    unittest.main()
