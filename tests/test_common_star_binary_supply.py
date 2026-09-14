"""Focused checks for the common-star binary-resource supply control."""

from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "common_star_binary_resource_supply_control"
SPEC = importlib.util.spec_from_file_location(
    MODULE_NAME,
    ROOT / "claims/arbitrary-order" / "verify_common_star_binary_resource_supply_control.py",
)
CONTROL = importlib.util.module_from_spec(SPEC)
sys.modules[MODULE_NAME] = CONTROL
assert SPEC.loader is not None
SPEC.loader.exec_module(CONTROL)


class CommonStarBinarySupplyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = CONTROL.read_fixture()
        cls.data = CONTROL.base_data(cls.fixture)
        cls.states, cls.edges = CONTROL.local_data(cls.fixture, cls.data)
        # This is the one expensive finite-cover replay shared by all tests.
        cls.cover = CONTROL.finite_cover(cls.states, cls.edges, cls.fixture)

    def test_exact_seed_dual_product_and_tensor_supply(self):
        self.assertEqual(len(self.data["M"]), 5)
        self.assertEqual(len(self.data["Q"]), 5)
        self.assertTrue(CONTROL.times(self.data["Q"], CONTROL.transpose(self.data["Q"])) == CONTROL.identity(5))
        self.assertEqual(self.data["r"], CONTROL.E(2, 1))
        self.assertEqual(len(self.states), 150)
        self.assertEqual(len(self.edges), 2604)

    def test_full_cover_counts_and_coherent_triangles(self):
        self.assertEqual(self.cover["resources"], 120)
        self.assertEqual(self.cover["components"], 6000)
        self.assertEqual(self.cover["physical_vertices"], 24000)
        self.assertEqual(self.cover["gadgets"], 312480)
        self.assertEqual(self.cover["physical_component_triangles"], 423360)
        self.assertTrue(self.cover["all_component_triangles_coherent"])

    def test_each_binary_pair_has_only_noncomplete_connected_components(self):
        self.assertEqual(
            self.cover["binary_components"],
            {
                "01": [{"color_part_sizes": [50, 50], "edges": 1764, "components": 120}],
                "02": [{"color_part_sizes": [10, 10], "edges": 84, "components": 600}],
                "12": [{"color_part_sizes": [10, 10], "edges": 84, "components": 600}],
            },
        )
        self.assertTrue(self.cover["no_binary_pair_is_a_biclique_union"])

    def test_full_failure_receipt_has_600_scalar_cores_and_isolated_edges(self):
        self.assertEqual(self.cover["full_failure_scalar_components"], {2: 6000, 20: 600})
        self.assertEqual(self.cover["full_failure_core_amplitude"], "-463/2592")
        self.assertEqual(self.cover["full_failure_core_supported_matchings"], 6130)
        self.assertEqual(self.cover["full_failure_amplitude"], "(-463/2592)^600")
        self.assertTrue(self.cover["physical_failure_replayed"])

    def test_material_fixture_mutations_are_rejected(self):
        bad_group = copy.deepcopy(self.fixture)
        bad_group["group_prime"] = 7
        with self.assertRaises(AssertionError):
            CONTROL.finite_cover(self.states, self.edges, bad_group)

        bad_seed = copy.deepcopy(self.fixture)
        bad_seed["seed_a"][0][1] = "1"
        with self.assertRaises(AssertionError):
            CONTROL.base_data(bad_seed)


if __name__ == "__main__":
    unittest.main()
