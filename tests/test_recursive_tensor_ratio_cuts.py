"""Actual-source and sharp local controls for coloured ratio-slot clauses."""

from __future__ import annotations

import itertools
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
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.recursive_tensor_ratio_cuts import add_tensor_ratio_consistency  # noqa: E402
from tests.test_recursive_tensor_support import actual_support  # noqa: E402


class RecursiveTensorRatioCutsTests(unittest.TestCase):
    def test_counts_include_cross_colour_slots_but_no_same_vertex_fibres(self):
        instance = build_recursive_tensor_support_cnf(4)
        before_vars, before_clauses = instance.cnf.nv, len(instance.cnf.clauses)
        counts = add_tensor_ratio_consistency(instance, component_closure=True)
        self.assertEqual(counts, {
            "parity_variables": 324, "component_variables": 810,
            "parity_clauses": 972, "component_clauses": 5670,
        })
        self.assertEqual(instance.cnf.nv - before_vars, 1134)
        self.assertEqual(len(instance.cnf.clauses) - before_clauses, 6642)

    def test_integer_and_gaussian_integer_sources_admit_all_auxiliaries(self):
        rng = random.Random(20400913)
        for n in (4, 6):
            instance = build_recursive_tensor_support_cnf(
                n, impose_target=False, column_killers=False, fix_root_killers=False,
            )
            base_variables = instance.cnf.nv
            add_tensor_ratio_consistency(instance, component_closure=True)
            with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
                for sample in range(8):
                    choices = (-2, -1, 0, 0, 1, 2) if sample < 4 else (0, 0, 1, -1, 1j, -1j, 1+1j)
                    values = {key: rng.choice(choices) for key in instance.entries}
                    positive, _numeric = actual_support(instance, values)
                    assumptions = [v if v in positive else -v for v in range(1, base_variables + 1)]
                    self.assertTrue(solver.solve(assumptions=assumptions), (n, sample))

    def test_three_coloured_four_fibres_pass_recursion_but_fail_parity(self):
        instance = build_recursive_tensor_support_cnf(
            6, impose_target=False, column_killers=False, fix_root_killers=False,
        )
        neighbours = ((0, 2), (2, 0), (4, 0))
        assumptions = [-instance.entry(1, 3, 0, 2)]
        for neighbour, colour in neighbours:
            assumptions.extend((instance.entry(1, neighbour, 0, colour),
                                instance.entry(3, neighbour, 2, colour)))
        for (i, gamma), (j, delta) in itertools.combinations(neighbours, 2):
            colours = {1: 0, 3: 2, i: gamma, j: delta}
            vertices = tuple(sorted(colours))
            word = tuple(colours[v] for v in vertices)
            assumptions.append(-instance.coefficients[(vertices, word)])
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve(assumptions=assumptions))
        add_tensor_ratio_consistency(instance)
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertFalse(solver.solve(assumptions=assumptions))

    def test_known_ghz_four_keeps_full_component_closure(self):
        instance = build_recursive_tensor_support_cnf(4)
        base_variables = instance.cnf.nv
        values = dict.fromkeys(instance.entries, 0)
        for colour, matching in enumerate((((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))):
            for u, v in matching:
                values[(u, v, colour, colour)] = 1
        positive, _numeric = actual_support(instance, values)
        add_tensor_ratio_consistency(instance, component_closure=True)
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve(assumptions=[
                v if v in positive else -v for v in range(1, base_variables + 1)
            ]))


if __name__ == "__main__":
    unittest.main()
