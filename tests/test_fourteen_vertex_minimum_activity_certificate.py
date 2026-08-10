"""Regression tests for generalized minimum-activity transport rules."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n14")


import json
import unittest
from pathlib import Path

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    full_automorphisms,
    validate_simple_certificate,
)
from run_fourteen_vertex_c4_c4_c6_rule_sat_incremental import (
    certificate_no_goods,
    minimum_condition_no_goods,
)


def fixture_path(relative: str) -> Path:
    """Resolve a historically root-relative fixture from any caller CWD."""
    return REPO_ROOT / relative


class MinimumActivityCertificateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analysis = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_c4_c6_rule_sat_incremental_"
                "batch39alow_r0_5_0_factor_fork.json"
            ).read_text(encoding="utf-8")
        )
        self.minimum = json.loads(
            fixture_path(
                "tmp/c4_c4_c6_minimum_activity_smoke.json"
            ).read_text(encoding="utf-8")
        )
        self.audit = json.loads(
            fixture_path(
                "tmp/c4_c4_c6_minimum_activity_smoke_verified.json"
            ).read_text(encoding="utf-8")
        )

    def test_generalized_certificate_was_independently_verified(
        self,
    ) -> None:
        self.assertEqual(self.minimum["partition"], [4, 4, 6])
        self.assertEqual(
            self.minimum["status"],
            "fourteen_vertex_minimum_activity_certificate",
        )
        self.assertTrue(self.audit["verified"])
        self.assertEqual(
            self.audit["activation_constraint_score"],
            self.minimum["activation_constraint_score"],
        )

    def test_minimum_transport_is_a_stronger_subclause(
        self,
    ) -> None:
        factors, colourings = validate_simple_certificate(self.analysis)
        selector = 10_000
        representative_id = {factors[0]: 0}
        actions = full_automorphisms()
        full_clauses = certificate_no_goods(
            factors,
            colourings,
            representative_id,
            [selector],
            actions,
        )
        minimum_clauses = minimum_condition_no_goods(
            factors,
            self.minimum["activation_conditions"],
            representative_id,
            [selector],
            actions,
        )
        self.assertTrue(minimum_clauses)
        self.assertLess(
            max(map(len, minimum_clauses)),
            max(map(len, full_clauses)),
        )
        for minimum_clause in minimum_clauses:
            minimum_literals = set(minimum_clause)
            self.assertTrue(
                any(
                    minimum_literals.issubset(full_clause)
                    for full_clause in map(set, full_clauses)
                )
            )

    def test_structural_scope_removes_impossible_blockers(
        self,
    ) -> None:
        structural = json.loads(
            fixture_path(
                "tmp/c4_10_structural_minimum_activity_smoke.json"
            ).read_text(encoding="utf-8")
        )
        audit = json.loads(
            fixture_path(
                "tmp/c4_10_structural_minimum_activity_smoke_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            structural["activity_scope"],
            "perfect_matching_edge_disjoint",
        )
        self.assertEqual(structural["activation_constraint_score"], 3)
        self.assertEqual(audit["minimum_false_premises"], 0)
        self.assertTrue(audit["verified"])

    def test_connected_structural_scope_is_independently_verified(
        self,
    ) -> None:
        connected = json.loads(
            fixture_path(
                "tmp/c4_c4_c6_connected_structural_"
                "minimum_activity_smoke2.json"
            ).read_text(encoding="utf-8")
        )
        audit = json.loads(
            fixture_path(
                "tmp/c4_c4_c6_connected_structural_"
                "minimum_activity_smoke2_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            connected["activity_scope"],
            "connected_perfect_matching_edge_disjoint",
        )
        self.assertEqual(connected["activation_constraint_score"], 3)
        self.assertTrue(audit["verified"])

    def test_three_connected_scope_is_independently_verified(
        self,
    ) -> None:
        certificate = json.loads(
            fixture_path(
                "tmp/c6_8_three_connected_minimum_activity_smoke.json"
            ).read_text(encoding="utf-8")
        )
        audit = json.loads(
            fixture_path(
                "tmp/c6_8_three_connected_"
                "minimum_activity_smoke_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            certificate["activity_scope"],
            "three_connected_perfect_matching_edge_disjoint",
        )
        self.assertTrue(audit["verified"])

    def test_multiple_certificates_are_learned_per_support(
        self,
    ) -> None:
        chain = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_10_"
                "multi_certificate_driver_smoke_chain.json"
            ).read_text(encoding="utf-8")
        )
        row = chain["iterations"][0]
        self.assertEqual(row["certificate_candidates_used"], 4)
        self.assertEqual(row["minimum_activity_scores"], [3] * 4)
        self.assertGreater(row["new_no_goods"], 32)

    def test_multiple_c4_c4_c6_certificates_are_learned(
        self,
    ) -> None:
        chain = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_c4_c6_"
                "multi_certificate_driver_smoke_chain.json"
            ).read_text(encoding="utf-8")
        )
        row = chain["iterations"][0]
        self.assertEqual(row["certificate_candidates_used"], 4)
        self.assertEqual(len(row["minimum_activity_scores"]), 4)
        self.assertGreater(row["new_no_goods"], 128)

    def test_one_extra_core_activation_is_minimized_and_verified(
        self,
    ) -> None:
        certificate = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_10_orbit2_"
                "one_extra_direct_loop_3_minimum_activity.json"
            ).read_text(encoding="utf-8")
        )
        audit = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_10_orbit2_"
                "one_extra_direct_loop_3_minimum_activity_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            certificate["activity_scope"],
            "three_connected_perfect_matching_edge_disjoint",
        )
        self.assertEqual(certificate["activation_constraint_score"], 3)
        self.assertGreater(
            certificate["source_full_mask_score"],
            certificate["activation_constraint_score"],
        )
        self.assertTrue(audit["verified"])
        self.assertEqual(
            audit["activation_constraint_score"],
            certificate["activation_constraint_score"],
        )

    def test_multiple_one_extra_cores_are_learned_per_support(
        self,
    ) -> None:
        chain = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c6_8_"
                "multicore_driver_smoke_chain.json"
            ).read_text(encoding="utf-8")
        )
        row = chain["iterations"][0]
        self.assertEqual(row["cores_replayed"], 8)
        self.assertEqual(len(row["core_candidates"]), 8)
        self.assertGreaterEqual(row["new_no_goods"], 8)
        self.assertEqual(chain["verified_cores"], 8)

    def test_three_cycle_one_extra_batch_is_reconstructed(
        self,
    ) -> None:
        augmentation = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_c4_c6_orbit6_"
                "one_extra_multicore_augmentation.json"
            ).read_text(encoding="utf-8")
        )
        audit = json.loads(
            fixture_path(
                "tmp/fourteen_vertex_c4_c4_c6_orbit6_"
                "one_extra_multicore_augmentation_verified.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(len(augmentation["certificate_records"]), 8)
        self.assertEqual(augmentation["new_no_goods"], 192)
        self.assertTrue(audit["verified"])
        self.assertTrue(audit["sat"])


if __name__ == "__main__":
    unittest.main()
