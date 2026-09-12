"""Focused tests for the recursive hafnian zero-pattern encoding."""

from __future__ import annotations

import itertools
import sys as _bootstrap_sys
import unittest
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from pysat.solvers import Cadical195  # noqa: E402

from krenn_gu.recursive_hafnian_support import (  # noqa: E402
    build_recursive_hafnian_support_cnf,
    canonical_matching_pair,
)


def clause_value(clause: list[int], true_variables: set[int]) -> bool:
    return any(
        (literal > 0) == (abs(literal) in true_variables)
        for literal in clause
    )


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(remainder):
            yield ((first, second), *matching)


def alternating_cycle_type(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    partner_maps = []
    for matching in (first, second):
        partners = {}
        for u, v in matching:
            partners[u] = v
            partners[v] = u
        partner_maps.append(partners)
    unvisited = set(partner_maps[0])
    parts = []
    while unvisited:
        start = min(unvisited)
        current = start
        colour = 0
        component = set()
        while True:
            component.add(current)
            current = partner_maps[colour][current]
            colour = 1 - colour
            if current == start and colour == 0:
                break
        unvisited -= component
        parts.append(len(component) // 2)
    return tuple(sorted(parts, reverse=True))


class RecursiveHafnianSupportTests(unittest.TestCase):
    def test_canonical_cycle_type_pair(self) -> None:
        first, second = canonical_matching_pair(10, (3, 2))
        self.assertEqual(len(first), 5)
        self.assertEqual(len(second), 5)
        self.assertEqual(len({*first, *second}), 10)
        degree = {vertex: 0 for vertex in range(10)}
        for edge in (*first, *second):
            for vertex in edge:
                degree[vertex] += 1
        self.assertTrue(all(value == 2 for value in degree.values()))

    def test_shared_matching_cycle_type(self) -> None:
        first, second = canonical_matching_pair(10, (1, 1, 1, 1, 1))
        self.assertEqual(first, second)

    def test_third_cycle_split_requires_shared_first_pair(self) -> None:
        with self.assertRaises(ValueError):
            build_recursive_hafnian_support_cnf(
                10,
                matching_cycle_type=(3, 2),
                third_matching_cycle_type=(5,),
            )

    def test_third_cycle_split_adds_one_more_matching(self) -> None:
        instance = build_recursive_hafnian_support_cnf(
            4,
            matching_cycle_type=(1, 1),
            third_matching_cycle_type=(2,),
        )
        self.assertEqual(instance.symmetry_clauses, 6)

    def test_cycle_type_must_partition_half_order(self) -> None:
        with self.assertRaises(ValueError):
            canonical_matching_pair(10, (3, 1))

    def test_seven_cycle_types_exhaust_matching_pairs_at_order_ten(self) -> None:
        first, _second = canonical_matching_pair(10, (5,))
        observed = {
            alternating_cycle_type(first, matching)
            for matching in perfect_matchings(tuple(range(10)))
        }
        self.assertEqual(
            observed,
            {
                (5,),
                (4, 1),
                (3, 2),
                (3, 1, 1),
                (2, 2, 1),
                (2, 1, 1, 1),
                (1, 1, 1, 1, 1),
            },
        )

    def test_product_variable_is_a_full_equivalence(self) -> None:
        instance = build_recursive_hafnian_support_cnf(4)
        subset = frozenset(range(4))
        edge = (0, 1)
        product = instance.product_variables[(0, subset, edge)]
        edge_lit = instance.edge_variables[(0, edge)]
        remainder = instance.edge_variables[(0, (2, 3))]
        definition = [
            clause
            for clause in instance.cnf.clauses
            if product in map(abs, clause)
            and set(map(abs, clause)) <= {product, edge_lit, remainder}
        ]
        self.assertEqual(len(definition), 3)
        for g_value, remainder_value, product_value in itertools.product(
            (False, True), repeat=3
        ):
            true_variables = {
                variable
                for variable, value in (
                    (edge_lit, g_value),
                    (remainder, remainder_value),
                    (product, product_value),
                )
                if value
            }
            clauses_hold = all(
                clause_value(clause, true_variables)
                for clause in definition
            )
            self.assertEqual(
                clauses_hold,
                product_value == (g_value and remainder_value),
            )

    def test_zero_result_rejects_exactly_one_nonzero_term(self) -> None:
        instance = build_recursive_hafnian_support_cnf(4)
        subset = frozenset(range(4))
        result = instance.hafnian_variables[(0, subset)]
        terms = [
            instance.product_variables[(0, subset, (0, other))]
            for other in (1, 2, 3)
        ]
        relevant = [
            clause
            for clause in instance.cnf.clauses
            if -terms[0] in clause
            and result in clause
            and set(map(abs, clause)) <= {result, *terms}
        ]
        self.assertEqual(relevant, [[-terms[0], result, terms[1], terms[2]]])
        self.assertFalse(clause_value(relevant[0], {terms[0]}))
        self.assertTrue(clause_value(relevant[0], {terms[0], terms[1]}))
        self.assertTrue(clause_value(relevant[0], {terms[0], result}))

    def test_order_four_bogdanov_model_is_satisfiable(self) -> None:
        instance = build_recursive_hafnian_support_cnf(4)
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve())

    def test_missing_singleton_cancellation_is_a_real_relaxation(self) -> None:
        full = build_recursive_hafnian_support_cnf(4)
        relaxed = build_recursive_hafnian_support_cnf(
            4,
            no_singleton_cancellation=True,
        )
        self.assertGreater(
            len(full.cnf.clauses),
            len(relaxed.cnf.clauses),
        )
        self.assertGreater(full.singleton_cancellation_clauses, 0)
        self.assertEqual(relaxed.singleton_cancellation_clauses, 0)


if __name__ == "__main__":
    unittest.main()
