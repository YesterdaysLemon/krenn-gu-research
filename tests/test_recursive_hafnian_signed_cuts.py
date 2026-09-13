"""Exact signed-patch controls, including the indispensable third-term escape."""

from __future__ import annotations

import itertools
import random
from functools import lru_cache
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

from krenn_gu.integer_signed_lattice import IntegerSignedLattice  # noqa: E402
from krenn_gu.recursive_hafnian_signed_cuts import (  # noqa: E402
    add_common_neighbor_closure_cuts,
    add_common_neighbor_parity_cuts,
    two_by_three_hafnian_cuts,
)
from krenn_gu.recursive_hafnian_support import (  # noqa: E402
    build_recursive_hafnian_support_cnf,
)


def ratio_patch_witness(states):
    """Construct exact weights, or detect a graph obstruction, on K2,4.

    States 0,1,2,3 mean (third support,hafnian support) = 00,01,10,11.
    This independent graph algorithm does not import or emulate CNF clauses.
    """

    pairs = tuple(itertools.combinations(range(4), 2))
    graph = {i: [] for i in range(4)}
    for (i, j), state in zip(pairs, states, strict=True):
        if state == 0:
            graph[i].append(j)
            graph[j].append(i)
    component, parity = {}, {}
    for start in range(4):
        if start in component:
            continue
        component[start], parity[start] = start, 0
        pending = [start]
        while pending:
            i = pending.pop()
            for j in graph[i]:
                if j in component:
                    if parity[j] == parity[i]:
                        return None
                else:
                    component[j], parity[j] = start, 1 - parity[i]
                    pending.append(j)
    for (i, j), state in zip(pairs, states, strict=True):
        if state in (1, 2) and component[i] == component[j] and parity[i] != parity[j]:
            return None
    ratios = {i: (-1) ** parity[i] * 2 ** component[i] for i in range(4)}
    weights = {(0, 1): 1}
    weights.update({(0, i + 2): ratios[i] for i in range(4)})
    weights.update({(1, i + 2): 1 for i in range(4)})
    for (i, j), state in zip(pairs, states, strict=True):
        cross_sum = ratios[i] + ratios[j]
        if state < 2:
            third = 0
        elif state == 2:
            third = -cross_sum
        else:
            third = 1 if cross_sum != -1 else 2
        assert bool(third) == bool(state // 2)
        assert bool(cross_sum + third) == bool(state % 2)
        weights[(i + 2, j + 2)] = third
    return weights


class SignedHafnianCutTests(unittest.TestCase):
    def test_actual_integer_hafnians_extend_to_parity_bits(self):
        rng = random.Random(20260913)
        for n in (6, 8):
            for trial in range(10):
                instance = build_recursive_hafnian_support_cnf(n)
                local_count = (instance.product_definition_clauses
                               + instance.nonzero_accessibility_clauses
                               + instance.singleton_cancellation_clauses)
                local = instance.cnf.clauses[:local_count]
                fixed = []
                for colour in range(3):
                    weights = {edge: rng.choice((-2, -1, 0, 1, 2))
                               for edge in itertools.combinations(range(n), 2)}

                    @lru_cache(None)
                    def hafnian(vertices):
                        if not vertices:
                            return 1
                        first = vertices[0]
                        return sum(
                            weights[(first, second)] * hafnian(
                                tuple(vertex for vertex in vertices[1:] if vertex != second)
                            )
                            for second in vertices[1:]
                        )

                    for (c, edge), literal in instance.edge_variables.items():
                        if c == colour:
                            fixed.append([literal if weights[edge] else -literal])
                    for (c, subset), literal in instance.hafnian_variables.items():
                        if c == colour:
                            fixed.append([literal if hafnian(tuple(sorted(subset))) else -literal])
                original_count = len(instance.cnf.clauses)
                add_common_neighbor_parity_cuts(instance)
                add_common_neighbor_closure_cuts(instance)
                parity = instance.cnf.clauses[original_count:]
                with self.subTest(n=n, trial=trial), Cadical195(
                    bootstrap_with=[*local, *fixed, *parity]
                ) as solver:
                    self.assertTrue(solver.solve())

    def test_integer_kernel_is_exact_not_mod_two(self):
        # In variables (x1,x2,x3,y1,y2,y3), d12 - d13 + d23 = 0.
        rows = ((1, -1, 0, -1, 1, 0), (1, 0, -1, -1, 0, 1),
                (0, 1, -1, 0, -1, 1))
        lattice = IntegerSignedLattice(rows)
        self.assertTrue(lattice.has_inconsistent_kernel)
        self.assertTrue(any(sum(vector) % 2 for vector in lattice.kernel_basis))
        # x^2=-1 has complex solutions although 2 is zero modulo two.
        self.assertFalse(IntegerSignedLattice(((2,),)).has_inconsistent_kernel)

    def test_exact_patch_weights_always_satisfy_guarded_clause(self):
        # Enumerate all nonzero +/-1 cross weights and 0,+/-1 same-shore
        # weights.  Direct hafnian evaluation is independent of the encoder.
        for cross in itertools.product((-1, 1), repeat=6):
            x, y = cross[:3], cross[3:]
            for same in itertools.product((-1, 0, 1), repeat=4):
                ab, *right_edges = same
                hafnians = [
                    x[i] * y[j] + x[j] * y[i] + ab * right
                    for (i, j), right in zip(
                        itertools.combinations(range(3), 2), right_edges, strict=True
                    )
                ]
                self.assertTrue(any(hafnians) or any(ab * right for right in right_edges))

    def test_third_matching_is_a_real_escape(self):
        # All six cross weights 1, ab=1, and every right-right edge -2.
        # Each of the three hafnians is 1+1-2=0; omitting b would be unsound.
        instance = build_recursive_hafnian_support_cnf(6)
        clause = next(two_by_three_hafnian_cuts(instance))
        live = set()
        for edge in itertools.combinations(range(5), 2):
            live.add(instance.edge_variables[(0, edge)])
        for i, j in itertools.combinations((2, 3, 4), 2):
            live.add(instance.product_variables[(0, frozenset((0, 1, i, j)), (0, 1))])
        self.assertTrue(any((literal > 0) == (abs(literal) in live) for literal in clause))
        unguarded = [literal for literal in clause if literal not in live or literal < 0]
        self.assertFalse(any((literal > 0) == (abs(literal) in live) for literal in unguarded))
        self.assertEqual([1 * 1 + 1 * 1 + 1 * (-2) for _ in range(3)], [0, 0, 0])

    def test_local_rzp_accepts_patch_rejected_by_signed_cut(self):
        instance = build_recursive_hafnian_support_cnf(8)
        local_count = (instance.product_definition_clauses
                       + instance.nonzero_accessibility_clauses
                       + instance.singleton_cancellation_clauses)
        # This is deliberately a one-colour local test: no global rainbow
        # axiom.  It proves strictness of the local mechanism, not a witness.
        local = instance.cnf.clauses[:local_count]
        fixed = []
        for edge in itertools.combinations(range(8), 2):
            cross = len(set(edge) & {0, 1}) == 1 and len(set(edge) & {2, 3, 4}) == 1
            outside = bool(set(edge) & {5, 6, 7})
            literal = instance.edge_variables[(0, edge)]
            fixed.append([literal if cross or outside else -literal])
        for i, j in itertools.combinations((2, 3, 4), 2):
            fixed.append([-instance.hafnian_variables[(0, frozenset((0, 1, i, j)))]])
        fixed.append([instance.hafnian_variables[(0, frozenset(range(8)))]])
        with Cadical195(bootstrap_with=[*local, *fixed]) as solver:
            self.assertTrue(solver.solve())
            solver.add_clause(next(two_by_three_hafnian_cuts(instance)))
            self.assertFalse(solver.solve())

    def test_five_cycle_survives_triangles_but_not_ratio_parity(self):
        instance = build_recursive_hafnian_support_cnf(8)
        local_count = (instance.product_definition_clauses
                       + instance.nonzero_accessibility_clauses
                       + instance.singleton_cancellation_clauses)
        local = instance.cnf.clauses[:local_count]
        fixed = []
        for edge in itertools.combinations(range(8), 2):
            cross = len(set(edge) & {0, 1}) == 1 and len(set(edge) & set(range(2, 7))) == 1
            literal = instance.edge_variables[(0, edge)]
            fixed.append([literal if cross else -literal])
        for i, j in itertools.combinations(range(2, 7), 2):
            cycle_edge = (j - i) in (1, 4)
            literal = instance.hafnian_variables[(0, frozenset((0, 1, i, j)))]
            fixed.append([-literal if cycle_edge else literal])
        triangles = list(two_by_three_hafnian_cuts(instance))
        original_count = len(instance.cnf.clauses)
        self.assertEqual(add_common_neighbor_parity_cuts(instance), 2520)
        parity = instance.cnf.clauses[original_count:]
        with Cadical195(bootstrap_with=[*local, *fixed, *triangles]) as solver:
            self.assertTrue(solver.solve())
            solver.append_formula(parity)
            self.assertFalse(solver.solve())

    def test_path_closure_transports_zero_and_live_third_term(self):
        for third_is_live in (False, True):
            instance = build_recursive_hafnian_support_cnf(6)
            local_count = (instance.product_definition_clauses
                           + instance.nonzero_accessibility_clauses
                           + instance.singleton_cancellation_clauses)
            local = instance.cnf.clauses[:local_count]
            fixed = []
            for edge in itertools.combinations(range(6), 2):
                cross = len(set(edge) & {0, 1}) == 1 and len(set(edge) & {2, 3, 4, 5}) == 1
                live = cross or (third_is_live and edge in ((0, 1), (2, 5)))
                literal = instance.edge_variables[(0, edge)]
                fixed.append([literal if live else -literal])
            for i, j in itertools.combinations(range(2, 6), 2):
                zero = (i, j) in ((2, 3), (3, 4), (4, 5))
                if (i, j) == (2, 5):
                    zero = third_is_live
                literal = instance.hafnian_variables[(0, frozenset((0, 1, i, j)))]
                fixed.append([-literal if zero else literal])
            before = len(instance.cnf.clauses)
            add_common_neighbor_parity_cuts(instance)
            parity = instance.cnf.clauses[before:]
            before = len(instance.cnf.clauses)
            add_common_neighbor_closure_cuts(instance)
            closure = instance.cnf.clauses[before:]
            with self.subTest(third_is_live=third_is_live), Cadical195(
                bootstrap_with=[*local, *fixed, *parity]
            ) as solver:
                self.assertTrue(solver.solve())
                solver.append_formula(closure)
                self.assertFalse(solver.solve())

    def test_all_4096_fixed_pair_patterns_match_constructive_oracle(self):
        instance = build_recursive_hafnian_support_cnf(6)
        local_count = (instance.product_definition_clauses
                       + instance.nonzero_accessibility_clauses
                       + instance.singleton_cancellation_clauses)
        local = instance.cnf.clauses[:local_count]
        before = len(instance.cnf.clauses)
        add_common_neighbor_parity_cuts(instance)
        add_common_neighbor_closure_cuts(instance)
        transport = instance.cnf.clauses[before:]
        fixed = [instance.edge_variables[(0, (0, 1))]]
        fixed.extend(instance.edge_variables[(0, (left, right))]
                     for left in (0, 1) for right in range(2, 6))
        counts = {False: 0, True: 0}
        with Cadical195(bootstrap_with=[*local, *transport]) as solver:
            for states in itertools.product(range(4), repeat=6):
                weights = ratio_patch_witness(states)
                assumptions = list(fixed)
                for (i, j), state in zip(itertools.combinations(range(2, 6), 2), states, strict=True):
                    edge = instance.edge_variables[(0, (i, j))]
                    hafnian = instance.hafnian_variables[(0, frozenset((0, 1, i, j)))]
                    assumptions.extend((edge if state // 2 else -edge,
                                        hafnian if state % 2 else -hafnian))
                expected = weights is not None
                self.assertEqual(solver.solve(assumptions=assumptions), expected, states)
                counts[expected] += 1
        self.assertEqual(sum(counts.values()), 4096)
        self.assertGreater(counts[False], 0)
        self.assertGreater(counts[True], 0)


if __name__ == "__main__":
    unittest.main()
