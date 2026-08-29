from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTIER = ROOT / "docs" / "current-frontier.md"
ARBITRARY_ORDER_README = ROOT / "claims" / "arbitrary-order" / "README.md"

CLAIMS = {
    "GLS66": {
        "owner": (
            "claims/arbitrary-order/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_TWO_TWO_"
            "SCALAR_AXIS_AND_COMMON_HYPERPLANE_EXCLUSION_THEOREM.md"
        ),
        "review": (
            "docs/audits/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ETA_ZERO_TWO_TWO_"
            "SCALAR_AXIS_AND_COMMON_HYPERPLANE_EXCLUSION_REVIEW_"
            "2026-08-28.md"
        ),
        "primary": (
            "claims/arbitrary-order/"
            "verify_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_"
            "scalar_axis_and_common_hyperplane_exclusion.py"
        ),
        "audit": (
            "claims/arbitrary-order/"
            "audit_maximal_root_surplus_two_zero_anchor_eta_zero_two_two_"
            "scalar_axis_and_common_hyperplane_exclusion.py"
        ),
    },
    "GLS67": {
        "owner": (
            "claims/arbitrary-order/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_"
            "CLASS_AND_P3_ORBIT_LOCALIZATION_THEOREM.md"
        ),
        "review": (
            "docs/audits/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_DEFICIENT_PAIR_"
            "CLASS_AND_P3_ORBIT_LOCALIZATION_REVIEW_2026-08-28.md"
        ),
        "primary": (
            "claims/arbitrary-order/"
            "verify_maximal_root_surplus_two_zero_anchor_three_deficient_"
            "pair_class_and_p3_orbit_localization.py"
        ),
        "audit": (
            "claims/arbitrary-order/"
            "audit_maximal_root_surplus_two_zero_anchor_three_deficient_"
            "pair_class_and_p3_orbit_localization.py"
        ),
    },
    "GLS68": {
        "owner": (
            "claims/arbitrary-order/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_DEFICIENT_PAIR_"
            "CLASS_AND_PROBE_DEPENDENT_FOUR_PORT_BOUNDARY_THEOREM.md"
        ),
        "review": (
            "docs/audits/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FOUR_DEFICIENT_PAIR_"
            "CLASS_AND_PROBE_DEPENDENT_FOUR_PORT_BOUNDARY_REVIEW_"
            "2026-08-28.md"
        ),
        "primary": (
            "claims/arbitrary-order/"
            "verify_maximal_root_surplus_two_zero_anchor_four_deficient_"
            "pair_class_and_probe_dependent_four_port_boundary.py"
        ),
        "audit": (
            "claims/arbitrary-order/"
            "audit_maximal_root_surplus_two_zero_anchor_four_deficient_"
            "pair_class_and_probe_dependent_four_port_boundary.py"
        ),
    },
    "GLS69": {
        "owner": (
            "claims/arbitrary-order/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_"
            "SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_"
            "THEOREM.md"
        ),
        "review": (
            "docs/audits/"
            "MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_"
            "SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_REVIEW_"
            "2026-08-28.md"
        ),
        "primary": (
            "claims/arbitrary-order/"
            "verify_maximal_root_surplus_two_zero_anchor_five_six_"
            "deficient_minimal_open_set_and_overlap_integrability_boundary.py"
        ),
        "audit": (
            "claims/arbitrary-order/"
            "audit_maximal_root_surplus_two_zero_anchor_five_six_"
            "deficient_minimal_open_set_and_overlap_integrability_boundary.py"
        ),
    },
}


def read(relative_path: str | Path) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class GLS66GLS69EvidenceReconciliationTests(unittest.TestCase):
    def test_owner_statuses_are_proved_not_candidate(self) -> None:
        for claim_id, paths in CLAIMS.items():
            with self.subTest(claim=claim_id):
                owner = read(paths["owner"])
                status = owner.split("## Status", 1)[1].split("##", 1)[0]
                self.assertIn("**Proved exact characteristic-zero", status)
                self.assertIn(f"(`{claim_id}`)", status)
                self.assertNotRegex(status, re.compile(r"\bcandidate\b", re.I))

    def test_exact_scope_reviews_are_pass(self) -> None:
        for claim_id, paths in CLAIMS.items():
            with self.subTest(claim=claim_id):
                review = read(paths["review"])
                self.assertIn(
                    f"Verdict: PASS for the exact `{claim_id}` scope",
                    review,
                )

    def test_frontier_records_proved_nodes_and_global_wall(self) -> None:
        frontier = FRONTIER.read_text(encoding="utf-8")
        authority = frontier.split("## Live proof topology", 1)[0]
        self.assertIn("**UNRESOLVED**", authority)
        for claim_id in CLAIMS:
            with self.subTest(claim=claim_id):
                node = next(
                    line
                    for line in frontier.splitlines()
                    if line.startswith(f'  {claim_id}["')
                )
                self.assertIn("<br/>PROVED", node)

    def test_replay_and_navigation_labels_are_not_stale(self) -> None:
        navigation = ARBITRARY_ORDER_README.read_text(encoding="utf-8")
        for claim_id, paths in CLAIMS.items():
            with self.subTest(claim=claim_id):
                combined = "\n".join(
                    [
                        navigation,
                        read(paths["owner"]),
                        read(paths["primary"]),
                        read(paths["audit"]),
                    ]
                )
                self.assertNotRegex(
                    combined,
                    re.compile(
                        rf"\b(?:candidate\s+{claim_id}|"
                        rf"{claim_id}\s+candidate)\b",
                        re.I,
                    ),
                )


if __name__ == "__main__":
    unittest.main()
