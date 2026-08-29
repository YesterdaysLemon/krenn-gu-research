from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "claims" / "arbitrary-order"
CENSUS = BASE / (
    "explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py"
)
GLD71 = BASE / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD96 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_r31_generic_resultant_exclusion.py"
)
GLD97 = BASE / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_p2_six_minor_offset_exclusion.py"
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GLD98MembershipCensusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.census = load_module(CENSUS, "gld98_census_test")

    def test_copied_inputs_match_canonical_sources(self) -> None:
        gld71 = load_module(GLD71, "gld71_gld98_test")
        gld88 = load_module(GLD88, "gld88_gld98_test")
        gld96 = load_module(GLD96, "gld96_gld98_test")
        gld97 = load_module(GLD97, "gld97_gld98_test")

        for row, support in self.census.PINNED_RELATIONS.items():
            self.assertEqual(tuple(gld71.SPARSE_RELATIONS[row]), support)
        self.assertEqual(
            self.census.support_digest(),
            self.census.EXPECTED_SUPPORT_DIGEST,
        )

        p, q, a = sp.symbols("p q a")
        canonical_family = gld88.h4_family(p, q, a)
        copied_family = self.census.h4_family(p, q, a)
        for key in ("s", "b", "c"):
            self.assertEqual(sp.cancel(canonical_family[key] - copied_family[key]), 0)
        self.assertEqual(
            sp.expand(
                self.census.q6_polynomial(p, q) - gld96.q6_polynomial(p, q)
            ),
            0,
        )
        self.assertEqual(self.census.MINORS, gld97.MINORS)
        self.assertEqual(self.census.PIVOT_ROWS, gld97.PIVOT_ROWS)
        self.assertEqual(self.census.PIVOT_COLUMNS, gld97.PIVOT_COLUMNS)

    def test_bc_monomial_basis_is_unique_and_complete(self) -> None:
        for degree in range(9):
            exponents = self.census.bc_exponents(degree)
            self.assertEqual(len(exponents), (degree + 1) * (degree + 2) // 2)
            self.assertEqual(len(exponents), len(set(exponents)))
            self.assertTrue(all(sum(exponent) <= degree for exponent in exponents))

        finite_algebra = self.census.QuotientAlgebra(self.census.q**2 + 1, 11)
        self.assertEqual(finite_algebra._coefficient(sp.Rational(1, 2)), 6)

    def test_subset_determinant_matches_direct_quotient_reduction(self) -> None:
        algebra = self.census.QuotientAlgebra(self.census.q**2 + 1, None)
        expressions = [
            [self.census.B + self.census.q * self.census.C, 1],
            [self.census.q, self.census.B - self.census.C],
        ]
        matrix = [
            [self.census.expression_to_bc(item, algebra, None) for item in row]
            for row in expressions
        ]
        actual = self.census.determinant_in_algebra(matrix).to_expr()
        direct = sp.det(sp.Matrix(expressions))
        expected = sp.Poly(
            direct,
            self.census.q,
            domain=sp.QQ.frac_field(self.census.B, self.census.C),
        ).rem(algebra.q6_poly)
        self.assertEqual(sp.expand(actual - expected.as_expr()), 0)

    def test_exact_p2_a0_fixed_fibre_membership(self) -> None:
        result = self.census.run_sample(
            {"id": "Q_p2_a0_test", "kind": "rational", "p": "2", "a": "0"},
            4,
        )
        self.assertEqual(result["status"], "regular_membership")
        self.assertTrue(result["gate"]["regular_chart_gate"])

        ideal = result["ideal"]
        self.assertTrue(ideal["B_membership"])
        self.assertTrue(ideal["C_membership"])
        self.assertEqual(
            ideal["basis_status"],
            "exact_fixed_fibre_equality_from_A_membership_and_zero_constants",
        )
        self.assertTrue(
            all(
                item["zero_in_A"]
                for item in ideal["generator_constant_terms"].values()
            )
        )

        signatures = ideal["macaulay"]["rank_signature"]
        self.assertEqual(ideal["macaulay"]["minimal_degree_BC"], 4)
        self.assertEqual(
            [
                (
                    item["degree_BC"],
                    item["rank"],
                    item["rank_with_B"],
                    item["rank_with_C"],
                    item["nonconstant_target_deficiency"],
                )
                for item in signatures
            ],
            [
                (1, 0, 1, 1, 8),
                (2, 0, 1, 1, 20),
                (3, 20, 21, 21, 16),
                (4, 48, 48, 48, 8),
            ],
        )
        self.assertTrue(result["minor_polynomials"]["D2"]["bc_support"]["zero"])

    def test_gate_overlap_control_is_not_treated_as_membership(self) -> None:
        result = self.census.run_sample(
            {"id": "Q_p0_a0_test", "kind": "rational", "p": "0", "a": "0"},
            4,
        )
        self.assertEqual(result["status"], "exceptional_gate_overlap")
        self.assertEqual(result["computation"], "skipped_before_quotient_algebra")
        self.assertTrue(
            any(
                reason.startswith("Q6_overlaps_chart_factor:")
                for reason in result["exceptional_reasons"]
            )
        )

    def test_finite_field_regular_sample_uses_exact_modular_rank(self) -> None:
        result = self.census.run_sample(
            {
                "id": "F11_p2_a0_test",
                "kind": "finite_field",
                "characteristic": 11,
                "p": 2,
                "a": 0,
            },
            4,
        )
        self.assertEqual(result["status"], "regular_membership")
        signature = result["ideal"]["macaulay"]["rank_signature"][-1]
        self.assertEqual(
            (
                signature["rank"],
                signature["rank_with_B"],
                signature["rank_with_C"],
            ),
            (46, 46, 46),
        )


if __name__ == "__main__":
    unittest.main()
