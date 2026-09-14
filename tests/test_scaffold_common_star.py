"""Physical and boundary controls for the common-star source obstruction."""
from __future__ import annotations

import copy
import importlib.util
from itertools import product
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "common_star_control", ROOT / "claims/arbitrary-order/verify_protected_scaffold_common_star_control.py"
)
CONTROL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CONTROL)


class ProtectedCommonStarTests(unittest.TestCase):
    def test_source_identity_on_every_word_of_three_small_graphs(self):
        for graph in (CONTROL.forest_control(), CONTROL.cycle_control(), CONTROL.triangle_control()):
            for word in product(range(3), repeat=graph["n"]):
                with self.subTest(n=graph["n"], word=word):
                    physical = CONTROL.physical_amplitude(graph, word)
                    self.assertEqual(physical, CONTROL.reduced_amplitudes(graph, word)[0])

    def test_actual_singleton_cancellations_and_double_failure(self):
        graph = CONTROL.forest_control()
        self.assertEqual(CONTROL.edge_rows(graph, 0)["values"], (0, 0, 1))
        for c in range(3):
            self.assertEqual(CONTROL.physical_amplitude(graph, (c,) * 4), 1)
        for edge_index in range(len(graph["edges"])):
            rows = CONTROL.edge_rows(graph, edge_index)
            self.assertEqual(rows["residual"], rows["q"])

    def test_cycle_cross_matchings_invalidate_ordinary_matching_formula(self):
        graph, word = CONTROL.cycle_control(), (0, 1, 0, 1)
        self.assertEqual(CONTROL.physical_amplitude(graph, word), 9)
        self.assertEqual(CONTROL.reduced_amplitudes(graph, word), (9, 7))

    def test_triangle_boundary_cancels_isolated_edge_residual(self):
        graph = CONTROL.triangle_control()
        with self.assertRaisesRegex(ValueError, "triangle-free"):
            CONTROL.validate_graph(graph, triangle_free=True)
        rows = CONTROL.edge_rows(graph, 0)
        self.assertEqual(rows["values"], (0, 0, 0))
        self.assertNotEqual(rows["residual"], rows["q"])

    def test_weight_edge_and_label_mutations_change_the_physical_source(self):
        word = (0, 1, 2, 2)
        graph = CONTROL.forest_control()
        changed = copy.deepcopy(graph)
        changed["edges"][0] = (0, 1, 0, 1, 1, 2)
        self.assertEqual(CONTROL.physical_amplitude(changed, word), 2)
        changed = copy.deepcopy(graph)
        del changed["edges"][0]
        self.assertEqual(CONTROL.physical_amplitude(changed, word), 0)
        changed = copy.deepcopy(graph)
        changed["edges"][0] = (0, 1, 1, 0, 1, 1)
        self.assertEqual(CONTROL.physical_amplitude(changed, word), 0)

    def test_unique_port_normalizations_expose_both_spoke_cases(self):
        for original, expected in ((CONTROL.forest_control(), -1), (CONTROL.triangle_control(), -2)):
            graph = {"n": original["n"], "edges": [
                (u, v, a, b, 1, -1) for u, v, a, b, _, _ in original["edges"]]}
            rows = CONTROL.edge_rows(graph, 0)
            self.assertEqual(rows["values"], (0, 0, expected))
            central_singleton = (0,) + (1,) * (graph["n"] - 1)
            self.assertEqual(CONTROL.physical_amplitude(graph, central_singleton), 0)
if __name__ == "__main__":
    unittest.main()
