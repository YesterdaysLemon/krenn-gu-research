"""Complete-fibre binomial extraction and exact guarded-circuit controls."""

from fractions import Fraction
from itertools import combinations
from pathlib import Path as _BootstrapPath
import sys as _bootstrap_sys
import unittest

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src/krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from pysat.solvers import Cadical195  # noqa: E402
from krenn_gu.recursive_hafnian_binomials import (  # noqa: E402
    RecursiveBinomial,
    circuit_support_cut,
    extract_recursive_binomials,
    find_integer_circuit,
    verify_integer_circuit,
)
from krenn_gu.recursive_hafnian_support import build_recursive_hafnian_support_cnf  # noqa: E402
from krenn_gu.recursive_hafnian_signed_cuts import (  # noqa: E402
    add_common_neighbor_parity_cuts,
    add_common_neighbor_closure_cuts,
)
from tests.test_hafnian_source_reduction_controls import hafnian_oracle  # noqa: E402

PATHS = ((0, 2, 3, 1), (0, 4, 5, 1), (0, 6, 7, 1))
THETA = {tuple(sorted(edge)) for path in PATHS for edge in zip(path, path[1:])}


def local_theta_instance():
    instance = build_recursive_hafnian_support_cnf(8)
    count = (instance.product_definition_clauses + instance.nonzero_accessibility_clauses
             + instance.singleton_cancellation_clauses)
    clauses = list(instance.cnf.clauses[:count])
    for (colour, edge), variable in instance.edge_variables.items():
        if colour == 0:
            clauses.append([variable if edge in THETA else -variable])
    for first, second in combinations(PATHS, 2):
        clauses.append([-instance.hafnian_variables[(0, frozenset(first + second))]])
    clauses.append([instance.hafnian_variables[(0, frozenset(range(8)))]])
    before = len(instance.cnf.clauses)
    add_common_neighbor_parity_cuts(instance)
    add_common_neighbor_closure_cuts(instance)
    clauses.extend(instance.cnf.clauses[before:])
    return instance, clauses


def exact_numeric_assignment(instance, weights):
    hafnian, _ = hafnian_oracle(instance.n, weights)
    values = {variable: weights.get(edge, 0) if colour == 0 else 0
              for (colour, edge), variable in instance.edge_variables.items()}
    values.update({variable: hafnian(tuple(sorted(subset))) if colour == 0 else 0
                   for (colour, subset), variable in instance.hafnian_variables.items()})
    for (colour, subset, edge), variable in instance.product_variables.items():
        edge_id = instance.edge_variables[(colour, edge)]
        remainder = instance.hafnian_literal(colour, subset - set(edge))
        values[variable] = values[edge_id] * (1 if remainder is None else values[remainder])
    return values, [variable if value else -variable for variable, value in values.items()]


class RecursiveHafnianBinomialTests(unittest.TestCase):
    def test_theta_survives_all_four_fibres_but_has_an_integer_circuit(self):
        instance, clauses = local_theta_instance()
        neighbours = {v: {u for edge in THETA if v in edge for u in edge if u != v}
                      for v in range(8)}
        self.assertTrue(all(len(neighbours[a] & neighbours[b]) <= 1
                            for a, b in combinations(range(8), 2)))
        with Cadical195(bootstrap_with=clauses) as solver:
            self.assertTrue(solver.solve())
            model = solver.get_model()
            model_set = set(model)
            self.assertTrue(all(any(literal in model_set for literal in clause) for clause in clauses))
            relations = extract_recursive_binomials(instance, model)
            vector = find_integer_circuit(relations)
            self.assertIsNotNone(vector)
            self.assertTrue(verify_integer_circuit(relations, vector))
            altered = list(vector)
            index = next(i for i, value in enumerate(vector) if value)
            altered[index] += 1
            self.assertFalse(verify_integer_circuit(relations, altered))
            cut = circuit_support_cut(instance, model, relations, vector)
            self.assertTrue(all(-literal in model_set for literal in cut))
            solver.add_clause(cut)
            self.assertFalse(solver.solve())

            # Same graph, but permit the third cycle hafnian to be nonzero.
            weights = {edge: 1 for edge in THETA}
            weights[(0, 4)] = weights[(0, 6)] = -1
            values, _ = exact_numeric_assignment(instance, weights)
            self.assertEqual(values[instance.hafnian_variables[(0, frozenset(range(8)))]], -1)
            self.assertTrue(any((literal > 0) == bool(values[abs(literal)]) for literal in cut))

    def test_extracted_relations_hold_on_actual_integer_weights(self):
        instance = build_recursive_hafnian_support_cnf(8)
        weights = {edge: 1 for edge in THETA}
        weights[(0, 4)] = weights[(0, 6)] = -1
        values, model = exact_numeric_assignment(instance, weights)
        relations = extract_recursive_binomials(instance, model)
        self.assertTrue(relations)
        for relation in relations:
            lhs = Fraction(1)
            for variable, exponent in relation.exponents:
                self.assertNotEqual(values[variable], 0)
                lhs *= Fraction(values[variable]) ** exponent
            self.assertEqual(lhs, (-1) ** relation.sign_bit)
        self.assertIsNone(find_integer_circuit(relations))

    def test_integer_arithmetic_not_binary_exponent_arithmetic(self):
        square = RecursiveBinomial(((1, 2),), 1, ())
        self.assertIsNone(find_integer_circuit((square,)))
        linear = RecursiveBinomial(((1, 1),), 1, ())
        relations = (linear, square)
        vector = find_integer_circuit(relations)
        self.assertTrue(verify_integer_circuit(relations, vector))
        with self.assertRaises(ValueError):
            find_integer_circuit(relations, max_relations=1)

    def test_incomplete_and_contradictory_supports_fail_closed(self):
        instance = build_recursive_hafnian_support_cnf(4)
        with self.assertRaises(ValueError):
            extract_recursive_binomials(instance, [])
        with self.assertRaises(ValueError):
            extract_recursive_binomials(instance, [1, -1])


if __name__ == "__main__":
    unittest.main()
