"""Frozen original-source row-space replay and hostile mutation controls."""
import copy
import json
import sys as _bootstrap_sys
import unittest
from pathlib import Path as _BootstrapPath
from unittest.mock import patch

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository

REPO_ROOT, HERE = _bootstrap_repository(__file__)

from krenn_gu.recursive_tensor_support import build_recursive_tensor_support_cnf
from krenn_gu.recursive_tensor_row_space import replay_recursive_row_space


class RecursiveRowSpaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instance = build_recursive_tensor_support_cnf(6, column_killers=False, fix_root_killers=False)
        cls.fixture = json.loads((HERE / "fixtures" / "recursive_row_space_n6.json").read_text())

    def test_exact_replay_without_quotient_discovery(self):
        with patch('krenn_gu.recursive_tensor_quotient.UnitSignedQuotient', side_effect=AssertionError('discovery called')):
            result = replay_recursive_row_space(self.instance, self.fixture['model'], self.fixture['certificate'])
        self.assertEqual(result['relations'], 10)
        self.assertEqual(result['dag_nodes'], 6)
        self.assertEqual(result['guard_literals'], 60)

    def test_forged_transports_fibres_and_operations_rejected(self):
        for mutation in ('sign', 'coefficient', 'drop_term', 'orientation', 'zero_scalar',
                         'future_parent', 'nonzero_variable', 'cut', 'wrong_order', 'non_singleton'):
            certificate = copy.deepcopy(self.fixture['certificate'])
            first = certificate['dag'][0]
            if mutation == 'sign':
                first['transports'][0]['sign'] *= -1
            elif mutation == 'coefficient':
                first['transports'][0]['coefficients'][0] += 1
            elif mutation == 'drop_term':
                first['transports'].pop()
            elif mutation == 'orientation':
                first['origin']['orientation'] = True
            elif mutation == 'zero_scalar':
                certificate['dag'][1]['scalar'] = 0
            elif mutation == 'future_parent':
                certificate['dag'][1]['parent'] = 124
            elif mutation == 'nonzero_variable':
                first['transports'][0]['monomial'][0][0] = 2
            elif mutation == 'cut':
                certificate['cut'].pop()
            elif mutation == 'wrong_order':
                certificate['n'] = 8
            else:
                certificate['contradiction_node'] = 0
            with self.assertRaises((ValueError, KeyError), msg=mutation):
                replay_recursive_row_space(self.instance, self.fixture['model'], certificate)

    def test_typed_model_and_duplicate_nodes_rejected(self):
        model = list(self.fixture['model'])
        model[0] = True
        with self.assertRaises(ValueError):
            replay_recursive_row_space(self.instance, model, self.fixture['certificate'])
        certificate = copy.deepcopy(self.fixture['certificate'])
        certificate['dag'].append(copy.deepcopy(certificate['dag'][-1]))
        with self.assertRaises(ValueError):
            replay_recursive_row_space(self.instance, self.fixture['model'], certificate)


if __name__ == '__main__':
    unittest.main()
