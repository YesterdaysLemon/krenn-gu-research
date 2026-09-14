"""Controls for integer discovery and lifting to original recursive equations."""

from __future__ import annotations

import copy
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
from krenn_gu.recursive_tensor_binomials import (  # noqa: E402
    RecursiveTensorBinomials, TensorBinomial, TensorLaplaceOrigin, sparse_integer_circuit,
)
from tests.test_recursive_tensor_support import actual_support  # noqa: E402


class RecursiveTensorBinomialTests(unittest.TestCase):
    def test_sparse_discovery_preserves_complex_torsion_control(self):
        origin = TensorLaplaceOrigin((), (), 0)
        rows = [TensorBinomial(((1, 2),), 1, origin)]
        vector, diagnostic = sparse_integer_circuit(rows)
        self.assertIsNone(vector)  # x^2=-1 is possible over C.
        self.assertEqual(diagnostic["status"], "NO_CIRCUIT_FOUND_NOT_SATURATED")
        rows.append(TensorBinomial(((1, 4),), 1, origin))
        vector, diagnostic = sparse_integer_circuit(rows)
        self.assertIsNotNone(vector)  # But x^4=-1 contradicts that equation.
        self.assertEqual(sum(k * dict(r.exponents)[1] for k, r in zip(vector, rows)), 0)
        self.assertEqual(sum(vector) % 2, 1)

    def test_actual_integer_sources_do_not_produce_a_false_circuit(self):
        rng = random.Random(23000913)
        instance = build_recursive_tensor_support_cnf(
            6, impose_target=False, column_killers=False, fix_root_killers=False,
        )
        audit = RecursiveTensorBinomials(instance)
        for _sample in range(4):
            values = {key: rng.choice((-1, 0, 0, 1)) for key in instance.entries}
            positive, _numeric = actual_support(instance, values)
            model = [v if v in positive else -v for v in range(1, instance.cnf.nv + 1)]
            certificate, _diagnostic = audit.find_obstruction(model)
            self.assertIsNone(certificate)

    def test_theta_circuit_lifts_through_one_term_cofactors(self):
        instance = build_recursive_tensor_support_cnf(
            8, impose_target=False, column_killers=False, fix_root_killers=False,
        )
        paths = ((0, 2, 3, 1), (0, 4, 5, 1), (0, 6, 7, 1))
        edges = {tuple(sorted((u, v))) for path in paths for u, v in zip(path, path[1:])}
        assumptions = [variable if (u, v) in edges and a == b == 0 else -variable
                       for (u, v, a, b), variable in instance.entries.items()]
        for first, second in itertools.combinations(paths, 2):
            vertices = tuple(sorted(set(first) | set(second)))
            assumptions.append(-instance.coefficients[(vertices, (0,) * len(vertices))])
        assumptions.append(instance.coefficients[(tuple(range(8)), (0,) * 8)])
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve(assumptions=assumptions))
            model = solver.get_model()
        audit = RecursiveTensorBinomials(instance)
        certificate, diagnostic = audit.find_obstruction(model)
        self.assertIsNotNone(certificate)
        self.assertGreater(diagnostic["substitutions"], 0)
        self.assertTrue(any(len(item["vertices"]) == 4 for item in certificate["equations"]))
        self.assertTrue(audit.verify_certificate(model, certificate))
        for mutation in ("coefficient", "cut", "orientation", "word"):
            changed = copy.deepcopy(certificate)
            if mutation == "coefficient":
                changed["equations"][0]["coefficient"] += 1
            elif mutation == "cut":
                changed["cut"] = changed["cut"][:-1]
            elif mutation == "orientation":
                changed["equations"][0]["orientation"] = 2
            else:
                changed["equations"][0]["word"] = (2,) * len(changed["equations"][0]["vertices"])
            self.assertFalse(audit.verify_certificate(model, changed), mutation)
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            solver.add_clause(certificate["cut"])
            self.assertFalse(solver.solve(assumptions=model))


if __name__ == "__main__":
    unittest.main()
