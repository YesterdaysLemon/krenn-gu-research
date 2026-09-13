"""Focused tests for the recursive hafnian zero-pattern encoding."""

from __future__ import annotations

import itertools
import copy
import json
import sys as _bootstrap_sys
import tempfile
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
from tools.explore.replay_recursive_hafnian_drat import (  # noqa: E402
    expected_cover,
    regenerate_cnf,
    validate_cover,
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


def stabilizer_map(first, second):
    """Construct an explicit alternating-walk map, not just a cycle label.

    Each walk traverses a first-matching edge and then a second-matching
    edge.  Consecutive pairs therefore map to standard first-matching edges;
    the links between them map to the canonical second matching.
    """

    partners = []
    for matching in (first, second):
        row = {}
        for u, v in matching:
            row[u], row[v] = v, u
        partners.append(row)
    unseen = set(partners[0])
    walks = []
    while unseen:
        start = min(unseen)
        current = start
        walk = []
        while True:
            other = partners[0][current]
            walk.extend((current, other))
            unseen.difference_update((current, other))
            current = partners[1][other]
            if current == start:
                break
        walks.append(tuple(walk))
    walks.sort(key=lambda walk: (-len(walk), walk))
    return {
        vertex: image
        for image, vertex in enumerate(itertools.chain.from_iterable(walks))
    }


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

    def test_stabilizer_maps_all_945_matchings_to_canonical_pairs(self) -> None:
        first, _ = canonical_matching_pair(10, (5,))
        count = 0
        for second in perfect_matchings(tuple(range(10))):
            permutation = stabilizer_map(first, second)
            self.assertEqual(set(permutation), set(range(10)))
            self.assertEqual(set(permutation.values()), set(range(10)))

            def image(matching):
                return tuple(sorted(
                    tuple(sorted((permutation[u], permutation[v])))
                    for u, v in matching
                ))

            cycle = alternating_cycle_type(first, second)
            canonical_first, canonical_second = canonical_matching_pair(10, cycle)
            self.assertEqual(image(first), canonical_first)
            self.assertEqual(image(second), canonical_second)
            # This same permutation fixes both selected matchings when the
            # first two colours share M0, proving the third-colour subsplit.
            count += 1
        self.assertEqual(count, 945)

    def test_replay_manifest_has_exact_typed_cover(self) -> None:
        path = REPO_ROOT / "docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        validate_cover(manifest["cases"])
        expected = expected_cover()
        self.assertEqual(len(expected), 13)
        for mutation in ("missing", "duplicate", "wrong_branch", "weakened", "bad_type"):
            cases = copy.deepcopy(manifest["cases"])
            if mutation == "missing":
                cases.pop()
            elif mutation == "duplicate":
                cases[-1] = cases[0]
            elif mutation == "wrong_branch":
                cases[0]["parameters"]["matching_cycle_type"] = [4, 1]
            elif mutation == "weakened":
                cases[0]["parameters"]["no_singleton_cancellation"] = True
            else:
                cases[0]["parameters"]["two_part_only"] = 0
            with self.subTest(mutation=mutation), self.assertRaises(RuntimeError):
                validate_cover(cases)

    def test_replay_regenerates_frozen_top_five_bytes_portably(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = _BootstrapPath(temporary) / "regenerated.cnf"
            result = regenerate_cnf(expected_cover()["top-5"], output)
            self.assertEqual(result["variables"], 18678)
            self.assertEqual(result["clauses"], 107908)
            self.assertEqual(result["identity"], {
                "bytes": 2504545,
                "sha256": "98f013336a427ee0899df85423636ab30b6d609036c2bd6ee162dec3009c1a51",
            })
            raw = output.read_bytes()
            self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"))

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
