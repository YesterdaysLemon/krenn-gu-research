"""Focused checks for the common-star resource-alignment countercontrol."""

from __future__ import annotations

from collections import Counter, deque
import copy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "common_star_resource_alignment_control"
SPEC = importlib.util.spec_from_file_location(
    MODULE_NAME,
    ROOT
    / "claims/arbitrary-order"
    / "verify_common_star_resource_alignment_control.py",
)
CONTROL = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = CONTROL
assert SPEC.loader is not None
SPEC.loader.exec_module(CONTROL)


class CommonStarResourceAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(CONTROL.DEFAULT_FIXTURE.read_text(encoding="utf-8"))
        cls.states, cls.edges = CONTROL.local_data(cls.fixture)
        cls.matrix_counts = CONTROL.local_matrix_checks(cls.states, cls.edges)
        # The cover replay includes the one relatively expensive 2,880-vertex
        # scalar decomposition.  Share it across the focused assertions.
        cls.cover = CONTROL.cover(cls.states, cls.edges, cls.fixture)

    def test_exact_cloned_matrix_identities_in_every_orientation(self):
        self.assertEqual(
            self.matrix_counts,
            {
                "S1_rows_and_columns": 72,
                "same_color_S2_entries": 180,
                "distinct_color_S2_entries": 216,
            },
        )

    def test_reversing_the_01_base_orientation_breaks_the_identities(self):
        changed = copy.deepcopy(self.fixture)
        changed["pair_base_matrices"]["01"] = "A"
        with self.assertRaises(AssertionError):
            CONTROL.local_data(changed)

    def test_local_state_resource_is_connected_and_noncomplete(self):
        adjacency = {state: set() for state in range(len(self.states))}
        by_color_pair = Counter()
        for (u, v), _factors in self.edges.items():
            adjacency[u].add(v)
            adjacency[v].add(u)
            colors = tuple(sorted((self.states[u][0], self.states[v][0])))
            by_color_pair[colors] += 1

        seen = {0}
        queue = deque((0,))
        while queue:
            for neighbor in adjacency[queue.popleft()]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)

        self.assertEqual(len(seen), 18)
        self.assertEqual(
            by_color_pair, {(0, 1): 36, (0, 2): 12, (1, 2): 36}
        )
        self.assertEqual(len(self.edges), 84)
        self.assertLess(len(self.edges), self.cover["complete_K666_edges"])

    def test_cover_is_legal_and_every_component_triangle_is_coherent(self):
        self.assertEqual(self.cover["resources"], 120)
        self.assertEqual(self.cover["components"], 720)
        self.assertEqual(self.cover["physical_vertices"], 2880)
        self.assertEqual(self.cover["gadgets"], 10080)
        self.assertTrue(self.cover["simple_one_label_component_graph"])
        self.assertEqual(self.cover["global_S1_port_sums_checked"], 4320)
        self.assertEqual(self.cover["ports_by_multiplicity"], {2: 1440, 6: 2880})
        self.assertEqual(self.cover["physical_component_triangles"], 8640)
        self.assertTrue(self.cover["all_physical_component_triangles_coherent"])
        self.assertEqual(self.cover["state_components"], 120)
        self.assertTrue(self.cover["state_components_noncomplete"])

    def test_bad_word_has_the_literal_local_and_global_scalar_amplitudes(self):
        selected = [
            index
            for index, (color, _base, clone) in enumerate(self.states)
            if (color, clone) in ((0, 0), (2, 1))
        ]
        self.assertEqual(len(selected), 6)
        self.assertEqual(
            CONTROL.local_physical(self.states, self.edges, selected),
            CONTROL.E(Fraction(1, 8)),
        )
        self.assertEqual(
            self.cover["full_failure_scalar_components"], {2: 720, 4: 360}
        )
        self.assertEqual(self.cover["full_failure_amplitude"], "2^(-360)")
        self.assertEqual(self.cover["full_failure_matching_count"], str(2**360))
        self.assertTrue(self.cover["physical_failure_replayed"])


if __name__ == "__main__":
    unittest.main()
