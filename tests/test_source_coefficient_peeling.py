"""Solver-free source derivations, forged-fact controls, and support guard tests."""

from __future__ import annotations

import copy
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
from krenn_gu.full_tensor_cancellation import FullTensorCancellation  # noqa: E402
from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf  # noqa: E402
from krenn_gu.source_coefficient_peeling import SourceCoefficientPeeling  # noqa: E402

EIGHT_QUOTIENT_SURVIVOR = frozenset((
    7,11,27,28,29,30,31,32,33,34,35,36,40,46,47,48,49,50,51,52,53,
    54,55,56,57,58,59,60,61,62,63,64,70,71,72,73,76,79,86,91,92,93,
    94,95,96,98,99,100,101,102,104,109,111,112,114,115,116,117,120,
    127,128,129,130,131,132,133,134,135,142,145,146,147,148,149,150,
    151,152,153,155,158,161,167,170,172,175,176,177,178,179,180,185,
    187,188,189,193,195,199,205,216,223,226,227,228,235,245,248,251,
))


class SourceCoefficientPeelingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instance = build_recursive_tensor_support_cnf(8)
        cls.support = [v if v in EIGHT_QUOTIENT_SURVIVOR else -v
                       for v in cls.instance.entries.values()]
        cls.audit = SourceCoefficientPeeling(cls.instance)
        cls.certificate, cls.diagnostic = cls.audit.find_obstruction(cls.support)

    def test_full_recursive_and_quotient_survivor_has_forced_subset_circuit(self):
        with Cadical195(bootstrap_with=self.instance.cnf.clauses) as solver:
            self.assertTrue(solver.solve(assumptions=self.support))
        self.assertIsNone(FullTensorCancellation(self.instance).find_obstruction(self.support))
        self.assertEqual(self.diagnostic["forced_binomials"], 19)
        self.assertEqual(len(self.certificate["derivations"]), 24)
        self.assertEqual(len(self.certificate["binomials"]), 3)
        self.assertEqual(len(self.certificate["cut"]), 57)
        self.assertTrue(self.audit.replay(self.support, self.certificate))

    def test_forged_parents_derivations_and_circuits_are_rejected(self):
        for mutation in ("none_parent", "boolean_parent", "missing_step", "fact", "coefficient", "cut"):
            certificate = copy.deepcopy(self.certificate)
            if mutation in ("none_parent", "boolean_parent"):
                parents = list(certificate["derivations"][0]["parents"])
                self.assertTrue(parents)
                parents[0] = (parents[0][0], None if mutation == "none_parent" else bool(parents[0][1]))
                certificate["derivations"][0]["parents"] = parents
            elif mutation == "missing_step":
                certificate["derivations"].pop(0)
            elif mutation == "fact":
                certificate["derivations"][0]["value"] ^= 1
            elif mutation == "coefficient":
                certificate["binomials"][0]["coefficient"] += 1
            else:
                certificate["cut"] = certificate["cut"][:-1]
            self.assertFalse(self.audit.replay(self.support, certificate), mutation)

    def test_certificate_depends_only_on_guarded_physical_entries(self):
        guarded = {abs(v) for v in self.certificate["cut"]}
        unguarded = [v for v in self.instance.entries.values() if v not in guarded]
        for variable in unguarded[:8]:
            modified = [-v if abs(v) == variable else v for v in self.support]
            self.assertTrue(self.audit.replay(modified, self.certificate), variable)
        for variable in sorted(guarded)[:8]:
            modified = [-v if abs(v) == variable else v for v in self.support]
            self.assertFalse(self.audit.replay(modified, self.certificate), variable)

    def test_order_four_ghz_control_is_not_excluded(self):
        instance = build_recursive_tensor_support_cnf(4)
        positive = set()
        for colour, matching in enumerate((((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))):
            positive.update(instance.entry(u, v, colour, colour) for u, v in matching)
        support = [v if v in positive else -v for v in instance.entries.values()]
        certificate, _diagnostic = SourceCoefficientPeeling(instance).find_obstruction(support)
        self.assertIsNone(certificate)


if __name__ == "__main__":
    unittest.main()
