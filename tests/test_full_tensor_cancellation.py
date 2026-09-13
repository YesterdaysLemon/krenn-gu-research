"""Exact quotient, certificate-tamper, and full-support survivor controls."""

from __future__ import annotations

import copy
import itertools
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
from krenn_gu.integer_signed_lattice import IntegerSignedLattice  # noqa: E402
from krenn_gu.full_tensor_cancellation import FullTensorCancellation  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402

SIX_SURVIVOR = frozenset((
    1,17,21,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,
    46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,71,78,
    85,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,
    114,115,116,117,120,134,
))


class FullTensorCancellationTests(unittest.TestCase):
    def test_quotient_signatures_keep_torsion(self):
        lattice = IntegerSignedLattice([[2]], sign_bits=[1])
        self.assertEqual(lattice.signed_quotient_signature([0]), ((0,), 1))
        self.assertEqual(lattice.signed_quotient_signature([1]), ((1,), 1))
        self.assertEqual(lattice.signed_quotient_signature([2]), ((0,), -1))
        self.assertEqual(lattice.signed_quotient_signature([-1]), ((1,), -1))
        self.assertFalse(lattice.has_inconsistent_kernel)

    def test_quotient_signatures_match_integer_transport(self):
        for rows, signs in (([[1, -1, 0], [0, 1, -1]], [1, 1]),
                            ([[2, 0], [0, 3]], [1, 0]),
                            ([[2, 2, 0], [0, 2, 2]], [1, 1])):
            lattice = IntegerSignedLattice(rows, signs)
            vectors = list(itertools.product(range(-1, 2), repeat=len(rows[0])))
            for first in vectors:
                key1, sign1 = lattice.signed_quotient_signature(first)
                for second in vectors:
                    key2, sign2 = lattice.signed_quotient_signature(second)
                    difference = [a - b for a, b in zip(first, second, strict=True)]
                    transported = lattice.transported_sign(difference)
                    self.assertEqual(key1 == key2, transported is not None)
                    if transported is not None:
                        self.assertEqual(sign1 * sign2, transported)

    def test_full_six_survivor_needs_quotient_not_odd_kernel(self):
        instance = build_recursive_tensor_support_cnf(6)
        model = [variable if variable in SIX_SURVIVOR else -variable
                 for variable in instance.entries.values()]
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve(assumptions=model))
            assignment = solver.get_model()
            positive = {literal for literal in assignment if literal > 0}
            self.assertTrue(all(any((literal > 0) == (abs(literal) in positive)
                                    for literal in clause) for clause in instance.cnf.clauses))
        audit = FullTensorCancellation(instance)
        certificate = audit.find_obstruction(model)
        self.assertIsNotNone(certificate)
        self.assertEqual(certificate["kind"], "quotient_singleton")
        self.assertEqual(certificate["word"], (0, 0, 0, 0, 0, 1))
        self.assertEqual(len(certificate["terms"]), 3)
        self.assertTrue(audit.verify_certificate(model, certificate))
        for mutation in ("coefficient", "sign", "origin", "term", "cut", "group"):
            altered = copy.deepcopy(certificate)
            if mutation == "coefficient":
                values = list(altered["transports"][0]["coefficients"])
                values[0] += 1
                altered["transports"][0]["coefficients"] = values
            elif mutation == "sign":
                altered["transports"][0]["sign"] *= -1
            elif mutation == "origin":
                altered["relations"][0]["word"] = (0,) * 6
            elif mutation == "term":
                altered["terms"] = altered["terms"][:-1]
            elif mutation == "cut":
                altered["cut"] = altered["cut"][:-1]
            else:
                altered["group_sums"] = []
            self.assertFalse(audit.verify_certificate(model, altered), mutation)
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            solver.add_clause(certificate["cut"])
            self.assertFalse(solver.solve(assumptions=model))

    def test_missing_and_contradictory_supports_rejected(self):
        instance = build_recursive_tensor_support_cnf(4)
        audit = FullTensorCancellation(instance)
        with self.assertRaises(ValueError):
            audit.find_obstruction([1])
        with self.assertRaises(ValueError):
            audit.find_obstruction([1, -1])

    def test_known_four_vertex_ghz_support_has_no_obstruction(self):
        instance = build_recursive_tensor_support_cnf(4)
        positive = set()
        for colour, matching in enumerate((((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))):
            positive.update(instance.entry(u, v, colour, colour) for u, v in matching)
        model = [variable if variable in positive else -variable for variable in instance.entries.values()]
        self.assertIsNone(FullTensorCancellation(instance).find_obstruction(model))


if __name__ == "__main__":
    unittest.main()
