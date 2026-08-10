"""Focused tests for the exact signed cycle-cover lattice check."""

from __future__ import annotations

import unittest

from analyze_fourteen_vertex_full_only_cycle_cover_cegar import (
    odd_kernel_conflict,
)
from analyze_fourteen_vertex_forced_slice_factor_cegar import (
    dense_relation,
    selected_lattice_conflict,
)
from analyze_fourteen_vertex_unforced_factor_choice_cegar import (
    build_dual_horn_index,
    dual_horn_forcing_core,
    dual_horn_unsat_core,
    is_forbidden_equation,
    one_extra_cycle_blocking_clauses,
)
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n14")

from verify_fourteen_vertex_unforced_factor_choice_core import (
    dual_horn_unsat,
)


class CycleCoverLatticeTests(unittest.TestCase):
    def test_single_even_exponent_is_consistent(self) -> None:
        self.assertIsNone(
            odd_kernel_conflict([0], [((0, 2),)], 1)
        )

    def test_duplicate_relation_is_consistent(self) -> None:
        self.assertIsNone(
            odd_kernel_conflict(
                [0, 1],
                [((0, 1),), ((0, 1),)],
                1,
            )
        )

    def test_relation_and_square_are_inconsistent(self) -> None:
        conflict = odd_kernel_conflict(
            [0, 1],
            [((0, 1),), ((0, 2),)],
            1,
        )
        self.assertIsNotNone(conflict)
        assert conflict is not None
        self.assertEqual(set(conflict["conflict_relation_ids"]), {0, 1})
        self.assertEqual(conflict["coefficient_sum"] % 2, 1)

    def test_relation_and_inverse_are_consistent(self) -> None:
        self.assertIsNone(
            odd_kernel_conflict(
                [0, 1],
                [((0, 1),), ((0, -1),)],
                1,
            )
        )

    def test_signed_lattice_conflict_uses_only_nonzero_basis_rows(
        self,
    ) -> None:
        relations = (
            ((0, 1),),
            ((1, 1),),
            ((2, 1),),
            ((0, 1), (2, 1)),
        )
        positions = {0: 0, 1: 1, 2: 2}
        rows = [
            dense_relation(relation, positions)
            for relation in relations
        ]
        conflict = selected_lattice_conflict(
            [0, 1, 2, 3],
            relations,
            rows,
            positions,
            [],
        )
        self.assertIsNotNone(conflict)
        assert conflict is not None
        self.assertEqual(
            conflict["certificate_mode"],
            "inconsistent_factor_sign",
        )
        self.assertEqual(conflict["basis_relation_ids"], [0, 2])
        self.assertEqual(conflict["target_relation_id"], 3)
        self.assertEqual(conflict["target_coordinates"], [1, 1])

    def test_literal_isolated_target_needs_no_lattice_basis(
        self,
    ) -> None:
        relations = (((0, 1),),)
        positions = {0: 0, 10: 1}
        rows = [
            dense_relation(relation, positions)
            for relation in relations
        ]
        conflict = selected_lattice_conflict(
            [0],
            relations,
            rows,
            positions,
            [(7, (42,), ((10,),))],
        )
        self.assertIsNotNone(conflict)
        assert conflict is not None
        self.assertEqual(
            conflict["certificate_mode"],
            "isolated_factor_lattice_class",
        )
        self.assertEqual(conflict["basis_relation_ids"], [])
        self.assertEqual(conflict["target_matching_ids"], [42])
        self.assertEqual(
            conflict["signed_class_coefficients"], [1]
        )

    def test_dual_horn_forcing_core_replays(self) -> None:
        clauses = [
            [1, 2],
            [-1, 3],
            [-2, 3],
            [-3, 4],
            [-4, 5],
            [-5, 6],
        ]
        index = build_dual_horn_index(clauses)
        proof = dual_horn_forcing_core(clauses, 6, index)
        self.assertIsNotNone(proof)
        assert proof is not None
        core = [
            clauses[index]
            for index in proof["core_factor_clause_indices"]
        ]
        self.assertIn([1, 2], core)
        self.assertIn([-2, 3], core)

    def test_one_extra_target_directly_blocks_cycle_factors(
        self,
    ) -> None:
        self.assertEqual(
            one_extra_cycle_blocking_clauses([5, 2, 5], 1),
            ((-3,), (-6,)),
        )
        self.assertEqual(
            one_extra_cycle_blocking_clauses([2, 5], 2),
            (),
        )

    def test_required_monochromatic_rows_are_not_forbidden(self) -> None:
        all_one = sum(3**vertex for vertex in range(14))
        self.assertFalse(is_forbidden_equation(0))
        self.assertFalse(is_forbidden_equation(all_one))
        self.assertFalse(is_forbidden_equation(2 * all_one))
        self.assertTrue(is_forbidden_equation(1))

    def test_dual_horn_negative_unit_is_propagated(self) -> None:
        clauses = [[-1], [1, 2], [-2, 3]]
        proof = dual_horn_forcing_core(clauses, 3)
        self.assertIsNotNone(proof)

    def test_dual_horn_base_unsat_core_replays(self) -> None:
        clauses = [[-1], [-2], [1, 2], [-3, 4]]
        proof = dual_horn_unsat_core(clauses)
        self.assertIsNotNone(proof)
        assert proof is not None
        core = [
            clauses[index]
            for index in proof["core_factor_clause_indices"]
        ]
        self.assertEqual(core, [[-1], [-2], [1, 2]])
        self.assertTrue(dual_horn_unsat(core))

    def test_independent_dual_horn_sat_core_survives(self) -> None:
        self.assertFalse(dual_horn_unsat([[-1], [1, 2]]))

    def test_dual_horn_nonforced_variable_survives(self) -> None:
        clauses = [[1, 2], [-2, 3]]
        self.assertIsNone(dual_horn_forcing_core(clauses, 1))

    def test_dual_horn_rejects_two_negative_literals(self) -> None:
        with self.assertRaises(ValueError):
            build_dual_horn_index([[-1, -2, 3]])


if __name__ == "__main__":
    unittest.main()
