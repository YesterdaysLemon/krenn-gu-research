"""Actual-source, torsion, and serialized source-transport controls."""

from __future__ import annotations

import copy
import json
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
from krenn_gu.recursive_tensor_binomials import (  # noqa: E402
    TensorBinomial, TensorLaplaceOrigin, RecursiveTensorBinomials,
)
from krenn_gu.recursive_tensor_quotient import (  # noqa: E402
    UnitSignedQuotient, RecursiveTensorQuotient,
)
from krenn_gu.recursive_tensor_ratio_cuts import add_tensor_ratio_consistency  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from tests.test_recursive_tensor_support import actual_support  # noqa: E402


class RecursiveTensorQuotientTests(unittest.TestCase):
    def test_unit_transport_and_nonunit_torsion_are_distinct(self):
        origin = TensorLaplaceOrigin((), (), 0)
        rows = [TensorBinomial(((1, 1), (2, -1)), 1, origin),
                TensorBinomial(((2, 1), (3, -1)), 1, origin)]
        quotient = UnitSignedQuotient(rows)
        self.assertIsNone(quotient.kernel)
        self.assertEqual(quotient.signature({1: 1}), quotient.signature({3: 1}))
        coordinates = quotient.coordinates({1: 1, 3: -1})
        self.assertEqual(coordinates, {0: 1, 1: 1})
        torsion = UnitSignedQuotient([TensorBinomial(((1, 2),), 1, origin)])
        self.assertEqual(len(torsion.residual), 1)
        self.assertIsNone(torsion.kernel)
        self.assertNotEqual(torsion.signature({1: 2}), torsion.signature({}))
        inconsistent = UnitSignedQuotient([TensorBinomial(((1, 1),), 0, origin),
                                          TensorBinomial(((1, 1),), 1, origin)])
        self.assertIsNotNone(inconsistent.kernel)

    def test_actual_integer_sources_are_not_excluded(self):
        rng = random.Random(13052026)
        for n in (4, 6):
            instance = build_recursive_tensor_support_cnf(
                n, impose_target=False, column_killers=False, fix_root_killers=False,
            )
            audit = RecursiveTensorQuotient(instance)
            for _sample in range(4):
                values = {key: rng.choice((-2, -1, 0, 0, 1, 2)) for key in instance.entries}
                positive, _numeric = actual_support(instance, values)
                model = [v if v in positive else -v for v in range(1, instance.cnf.nv + 1)]
                certificate, _diagnostic = audit.find_obstruction(model)
                self.assertIsNone(certificate)

    def test_genuine_four_vertex_ghz_is_retained(self):
        instance = build_recursive_tensor_support_cnf(4)
        values = dict.fromkeys(instance.entries, 0)
        for colour, matching in enumerate((((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))):
            for u, v in matching:
                values[(u, v, colour, colour)] = 1
        positive, _numeric = actual_support(instance, values)
        model = [v if v in positive else -v for v in range(1, instance.cnf.nv + 1)]
        certificate, _diagnostic = RecursiveTensorQuotient(instance).find_obstruction(model)
        self.assertIsNone(certificate)

    def test_eight_vertex_survivor_needs_larger_sum_transport(self):
        # Frozen physical support, not a physical weight assignment. The solver
        # supplies its full Boolean cofactor assignment; every clause is checked.
        positive_entries = set((
            1, 4, 7, 11, 14, 17, 21, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
            37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
            54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
            71, 72, 74, 77, 80, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 94, 97,
            100, 101, 102, 103, 104, 105, 106, 107, 108, 111, 114, 117, 118,
            119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131,
            132, 133, 134, 135, 136, 139, 142, 147, 150, 153, 161, 166, 172,
            173, 174, 175, 176, 177, 178, 179, 180, 186, 191, 205, 214, 215,
            216, 219, 222, 225, 226, 239, 244, 245, 246, 247, 248, 249, 250,
            251, 252,
        ))
        self.assertEqual(len(positive_entries), 136)
        instance = build_recursive_tensor_support_cnf(8)
        add_tensor_ratio_consistency(instance, component_closure=True)
        instance.cnf.extend([v if v in positive_entries else -v] for v in instance.entries.values())
        with Cadical195(bootstrap_with=instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve())
            model = solver.get_model()
        positive = {v for v in model if v > 0}
        self.assertTrue(all(any((v > 0) == (abs(v) in positive) for v in clause)
                            for clause in instance.cnf.clauses))
        prior, _diagnostic = RecursiveTensorBinomials(instance).find_obstruction(model)
        self.assertIsNone(prior)
        audit = RecursiveTensorQuotient(instance)
        certificate, diagnostic = audit.find_obstruction(model)
        self.assertIsNotNone(certificate)
        self.assertEqual(diagnostic["nonunit_residual_rows"], 0)
        self.assertEqual(certificate["kind"], "recursive_quotient_singleton")
        certificate = json.loads(json.dumps(certificate))
        self.assertTrue(audit.verify_certificate(model, certificate))
        self.assertFalse(any((v > 0) == (abs(v) in positive) for v in certificate["cut"]))
        for mutation in ("coefficient", "sign", "target", "relation", "cut", "partition"):
            changed = copy.deepcopy(certificate)
            if mutation == "coefficient":
                changed["transports"][0]["coefficients"][0] += 1
            elif mutation == "sign":
                changed["transports"][0]["sign"] *= -1
            elif mutation == "target":
                changed["target"]["word"] = [2] * len(changed["target"]["word"])
            elif mutation == "relation":
                changed["relations"][0]["orientation"] = 0
            elif mutation == "cut":
                changed["cut"] = changed["cut"][:-1]
            else:
                changed["transports"][0]["to"] = changed["transports"][0]["from"]
            self.assertFalse(audit.verify_certificate(model, changed), mutation)


if __name__ == "__main__":
    unittest.main()
