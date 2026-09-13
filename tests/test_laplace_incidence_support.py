from functools import lru_cache
from itertools import combinations, product
import random
import unittest
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import sympy as sp

from krenn_gu.laplace_incidence_support import (
    find_incidence_obstruction, incidence_identity_cuts, verify_incidence_obstruction,
)
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf
from krenn_gu.recursive_tensor_quotient import RecursiveTensorQuotient


class LaplaceIncidenceTests(unittest.TestCase):
    def test_graph_search_against_exact_rref(self):
        # Independent linear-algebra characterization over Q. Over the infinite
        # field C, an affine space avoids all coordinate hyperplanes iff no
        # individual coordinate vanishes identically on it.
        for n in range(1, 6):
            pairs = tuple(combinations(range(n), 2))
            for bits in product((False, True), repeat=len(pairs)):
                edges = tuple(edge for edge, bit in zip(pairs, bits) if bit)
                for nonzero in (False, True):
                    matrix = sp.Matrix([[int(v in edge) for edge in edges] + [int(nonzero)] for v in range(n)])
                    reduced, pivots = matrix.rref()
                    feasible = len(edges) not in pivots
                    if feasible:
                        free = set(range(len(edges))) - set(pivots)
                        for row, column in enumerate(pivots):
                            if reduced[row, -1] == 0 and all(reduced[row, j] == 0 for j in free):
                                feasible = False
                    certificate = find_incidence_obstruction(n, edges, nonzero)
                    self.assertEqual(certificate is None, feasible, (n, edges, nonzero))
                    if certificate is not None:
                        self.assertTrue(verify_incidence_obstruction(n, edges, nonzero, certificate))

    def test_actual_integer_hafnians_and_identity_clauses(self):
        rng = random.Random(130913)
        for n in (4, 6):
            vertices = tuple(range(n))
            pairs = tuple(combinations(vertices, 2))
            for _ in range(16):
                weights = {edge: rng.randrange(-2, 3) for edge in pairs}

                @lru_cache(None)
                def haf(subset):
                    if not subset:
                        return 1
                    v = subset[-1]
                    return sum(weights[tuple(sorted((u, v)))] * haf(tuple(w for w in subset if w not in (u, v)))
                               for u in subset[:-1])

                for size in range(4, n+1, 2):
                    for subset in combinations(vertices, size):
                        positions = {v: i for i, v in enumerate(subset)}
                        terms = {(positions[u], positions[v]): weights[u, v] * haf(tuple(w for w in subset if w not in (u, v)))
                                 for u, v in combinations(subset, 2)}
                        edges = tuple(edge for edge, value in terms.items() if value)
                        nonzero = bool(haf(subset))
                        self.assertIsNone(find_incidence_obstruction(size, edges, nonzero))
                        ids = {edge: i for i, edge in enumerate(terms, 2)}
                        true = {1} if nonzero else set()
                        true.update(ids[edge] for edge in edges)
                        for potential in product((-1, 0, 1), repeat=size):
                            self.assertEqual(sum((potential[u]+potential[v])*value for (u, v), value in terms.items()),
                                             sum(potential)*haf(subset))
                            for clause in incidence_identity_cuts(1, ids, potential):
                                self.assertTrue(any((lit > 0) == (abs(lit) in true) for lit in clause))

    def test_strict_recursive_and_binomial_control(self):
        instance = build_recursive_tensor_support_cnf(6, impose_target=False, column_killers=False, fix_root_killers=False)
        positive = {v for (u, w, a, b), v in instance.entries.items() if a == b == 0}
        whole = set(range(6))
        for (vertices, word), variable in instance.coefficients.items():
            if any(word):
                continue
            if len(vertices) == 6:
                positive.add(variable)
            else:
                complement = sorted(whole-set(vertices))
                if (complement[0] < 2) != (complement[1] < 2):
                    positive.add(variable)
        for (state, edge), variable in instance.products.items():
            if all(factor in positive for factor in instance.product_factors(state, edge)):
                positive.add(variable)
        self.assertTrue(all(any((lit > 0) == (abs(lit) in positive) for lit in clause)
                            for clause in instance.cnf.clauses))
        model = [v if v in positive else -v for v in range(1, instance.cnf.nv+1)]
        certificate, diagnostic = RecursiveTensorQuotient(instance).find_obstruction(model)
        self.assertIsNone(certificate)
        self.assertEqual(diagnostic['raw_relations'], 0)
        edges = tuple((u, v) for u in range(2) for v in range(2, 6))
        certificate = find_incidence_obstruction(6, edges, True)
        self.assertEqual(certificate['kind'], 'nonzero_result')
        self.assertTrue(verify_incidence_obstruction(6, edges, True, certificate))
        # This is a Boolean local mechanism countermodel, NOT a GHZ witness.

    def test_bad_certificates_rejected(self):
        edges = ((0, 1), (1, 2))
        certificate = find_incidence_obstruction(3, edges, True)
        self.assertTrue(verify_incidence_obstruction(3, edges, True, certificate))
        self.assertFalse(verify_incidence_obstruction(3, edges, True, {**certificate, 'potential': [0, 0, 0]}))
        self.assertFalse(verify_incidence_obstruction(3, edges, True, {**certificate, 'potential': [True, -1, 1]}))
        self.assertFalse(verify_incidence_obstruction(3, edges, True, {'kind': 'nonzero_term', 'edge': [0, 1], 'potential': [1, 0, 0]}))
        self.assertFalse(verify_incidence_obstruction(3, ((0, 4),), True, certificate))
        self.assertFalse(verify_incidence_obstruction(3, edges, True, {'kind': 'invented', 'potential': [1, -1, 1]}))


if __name__ == '__main__':
    unittest.main()
