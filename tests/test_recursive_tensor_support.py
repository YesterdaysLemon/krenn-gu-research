"""Independent matching-sum controls for the unrestricted recursive encoder."""

from __future__ import annotations

import itertools
import math
import random
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

from pysat.solvers import Cadical195  # noqa: E402
from krenn_gu.recursive_tensor_support import (  # noqa: E402
    build_recursive_tensor_support_cnf,
)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first, *rest = vertices
    for index, second in enumerate(rest):
        for matching in matchings(tuple(rest[:index] + rest[index + 1:])):
            yield ((first, second), *matching)


def actual_support(instance, values):
    """Enumerate complete matching sums, not the encoder's Laplace expansions."""
    numeric = {variable: values[key] for key, variable in instance.entries.items()}
    matching_cache = {}
    for (vertices, word), variable in instance.coefficients.items():
        if vertices not in matching_cache:
            matching_cache[vertices] = tuple(matchings(vertices))
        colours = dict(zip(vertices, word, strict=True))
        numeric[variable] = sum(math.prod(
            values[(u, v, colours[u], colours[v])] for u, v in matching
        ) for matching in matching_cache[vertices])
    positive = {variable for variable, value in numeric.items() if value != 0}
    for (state, edge), variable in instance.products.items():
        first, second = instance.product_factors(state, edge)
        if numeric[first] * numeric[second] != 0:
            positive.add(variable)
    for (vertex, colour, neighbour), variable in instance.killers.items():
        inside = [instance.entry(vertex, neighbour, row, colour) for row in range(3)]
        outside = [instance.entry(vertex, neighbour, row, column)
                   for row in range(3) for column in range(3) if column != colour]
        if any(entry in positive for entry in inside) and not any(
            entry in positive for entry in outside
        ):
            positive.add(variable)
    return positive, numeric


def holds(clause, positive):
    return any((literal > 0) == (abs(literal) in positive) for literal in clause)


class RecursiveTensorSupportTests(unittest.TestCase):
    def test_entry_orientation_and_pair_alias(self):
        instance = build_recursive_tensor_support_cnf(4)
        self.assertEqual(instance.entry(3, 1, 2, 0), instance.entry(1, 3, 0, 2))
        self.assertNotEqual(instance.entry(3, 1, 2, 0), instance.entry(1, 3, 2, 0))
        self.assertEqual(instance.coefficient((1, 3), (0, 2)),
                         instance.entry(1, 3, 0, 2))
        self.assertIsNone(instance.coefficient((), ()))
        with self.assertRaises(ValueError):
            instance.coefficient((3, 1), (0, 2))

    def test_product_has_truthful_equivalence(self):
        instance = build_recursive_tensor_support_cnf(4)
        state = ((0, 1, 2, 3), (2, 0, 1, 2))
        product = instance.products[(state, (0, 2))]
        first, second = instance.product_factors(state, (0, 2))
        self.assertEqual(first, instance.entry(0, 2, 2, 1))
        self.assertEqual(second, instance.entry(1, 3, 0, 2))
        allowed = {first, second, product}
        clauses = [clause for clause in instance.cnf.clauses
                   if product in map(abs, clause) and set(map(abs, clause)) <= allowed]
        self.assertEqual(len(clauses), 3)
        for bits in itertools.product((False, True), repeat=3):
            positive = {variable for variable, bit in zip(
                (first, second, product), bits, strict=True) if bit}
            self.assertEqual(all(holds(clause, positive) for clause in clauses),
                             bits[2] == (bits[0] and bits[1]))

    def test_killer_definition_all_512_blocks_both_orientations(self):
        instance = build_recursive_tensor_support_cnf(4, fix_root_killers=False)
        for vertex, neighbour in ((0, 1), (1, 0)):
            for colour in range(3):
                killer = instance.killers[(vertex, colour, neighbour)]
                block = [instance.entry(vertex, neighbour, row, column)
                         for row in range(3) for column in range(3)]
                allowed = {*block, killer}
                clauses = [clause for clause in instance.cnf.clauses
                           if killer in map(abs, clause)
                           and set(map(abs, clause)) <= allowed]
                self.assertEqual(len(clauses), 10)
                for bits in itertools.product((False, True), repeat=9):
                    positive = {entry for entry, bit in zip(block, bits, strict=True) if bit}
                    expected = any(bits[3 * row + colour] for row in range(3)) and all(
                        not bits[3 * row + column] for row in range(3)
                        for column in range(3) if column != colour
                    )
                    for bit in (False, True):
                        assigned = positive | ({killer} if bit else set())
                        self.assertEqual(all(holds(clause, assigned) for clause in clauses),
                                         bit == expected)

    def test_integer_block_coefficients_satisfy_every_recursion(self):
        rng = random.Random(20260913)
        for n in (4, 6):
            instance = build_recursive_tensor_support_cnf(
                n, impose_target=False, column_killers=False, fix_root_killers=False,
            )
            for _sample in range(8):
                values = {key: rng.choice((-2, -1, 0, 0, 1, 2)) for key in instance.entries}
                positive, _numeric = actual_support(instance, values)
                self.assertTrue(all(holds(clause, positive) for clause in instance.cnf.clauses))
            self.assertEqual(sum(instance.clause_counts.values()), len(instance.cnf.clauses))

    def test_known_ghz_four_obeys_killers_and_root_symmetry(self):
        instance = build_recursive_tensor_support_cnf(4)
        values = dict.fromkeys(instance.entries, 0)
        for colour, matching in enumerate((((0, 1), (2, 3)),
                                             ((0, 2), (1, 3)),
                                             ((0, 3), (1, 2)))):
            for u, v in matching:
                values[(u, v, colour, colour)] = 1
        positive, numeric = actual_support(instance, values)
        for word in itertools.product(range(3), repeat=4):
            self.assertEqual(numeric[instance.coefficients[((0, 1, 2, 3), word)]],
                             int(len(set(word)) == 1))
        self.assertTrue(all(holds(clause, positive) for clause in instance.cnf.clauses))
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve())

    def test_dense_boolean_control_without_killers(self):
        instance = build_recursive_tensor_support_cnf(
            6, column_killers=False, fix_root_killers=False,
        )
        positive = set(instance.entries.values()) | set(instance.products.values())
        positive.update(variable for (vertices, word), variable in instance.coefficients.items()
                        if len(vertices) < 6 or len(set(word)) == 1)
        self.assertTrue(all(holds(clause, positive) for clause in instance.cnf.clauses))


if __name__ == "__main__":
    unittest.main()
