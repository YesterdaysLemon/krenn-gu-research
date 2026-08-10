"""Bounded parity guards for the Stage 33 admissible-cone extraction."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
import unittest

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.admissible_potential_cone import EXTREME_RAYS  # noqa: E402
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)

EXPECTED_RAYS = (
    (-4, 1, 1, 1, 6, -4),
    (-4, 1, 6, 1, 1, -4),
    (1, -4, 1, 1, -4, 6),
    (1, -4, 1, 6, -4, 1),
    (1, 6, -4, -4, 1, 1),
    (6, 1, -4, -4, 1, 1),
)

CONSUMERS = (
    "claims/arbitrary-order/verify_full_admissible_potential_cone.py",
    "claims/arbitrary-order/history/state-lift-cycle-fibre/verify_state_lift_cycle_fibres.py",
    "claims/finite/n12/history/degree-six-kotzig-port-legacy/analyze_twelve_vertex_full_potential_cone.py",
    "tools/explore/scout_kotzig_full_cone_cells.py",
    "tools/explore/search_adversarial_fourteen_vertex_potential_residuals.py",
    "tools/explore/search_random_fourteen_vertex_potential_residuals.py",
)

FINITE_LEAF_CORRECTIONS = {
    "eight_vertex_degree4_support.py":
        "claims/finite/n08/eight_vertex_degree4_support.py",
    "verify_fourteen_vertex_no_one_term_support.py":
        "claims/finite/n14/verify_fourteen_vertex_no_one_term_support.py",
    "verify_laurent_batch_manifest.py":
        "claims/finite/n08/verify_laurent_batch_manifest.py",
}

CORRECTED_CONSUMERS = (
    "claims/finite/n08/eight_vertex_skeleton_batch.py",
    "claims/finite/n08/verify_eight_vertex_16edge.py",
    "claims/finite/n08/verify_eight_vertex_4regular.py",
    "claims/finite/n08/degree-six-kotzig-port/explore_eight_vertex_degree_six_kotzig_ports.py",
    "claims/finite/n08/combine_laurent_manifests.py",
    "claims/finite/n08/learn_partial_support_singular_clauses.py",
    "claims/finite/n08/verify_cancellation_transport_manifest.py",
    "claims/finite/n08/verify_matching_rectangle_manifest.py",
    "claims/finite/n08/verify_singular_fallback_manifest.py",
    "claims/finite/n08/verify_skeleton_laurent_batch.py",
    "claims/finite/n14/analyze_fourteen_vertex_full_direct_motifs.py",
    "claims/finite/n14/certify_fourteen_vertex_binomial_trinomial.py",
    "claims/finite/n14/search_fourteen_vertex_direct_free.py",
    "claims/finite/n14/search_fourteen_vertex_no_three_extension.py",
    "tests/test_search_witness.py",
)


class Stage33InverseTaperTests(unittest.TestCase):
    def test_extreme_rays_match_frozen_payload(self) -> None:
        self.assertEqual(EXTREME_RAYS, EXPECTED_RAYS)
        payload = json.dumps(
            EXTREME_RAYS,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(payload).hexdigest(),
            "a1427e403346becad10e208946f9f0464fa86aec4b00f589e0857a72107464c5",
        )

    def test_all_consumers_use_the_narrow_shared_constant(self) -> None:
        for relative_path in CONSUMERS:
            with self.subTest(path=relative_path):
                tree = ast.parse(
                    (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                )
                imports = [
                    node
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ImportFrom)
                    and node.module == "krenn_gu.admissible_potential_cone"
                ]
                self.assertEqual(len(imports), 1)
                self.assertEqual(
                    [alias.name for alias in imports[0].names],
                    ["EXTREME_RAYS"],
                )

    def test_independent_audit_keeps_its_own_literal(self) -> None:
        path = REPO_ROOT / (
            "claims/finite/n12/history/degree-six-kotzig-port-legacy/"
            "audit_twelve_vertex_six_potential_residuals.py"
        )
        tree = ast.parse(path.read_text(encoding="utf-8"))
        shared_imports = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom)
            and node.module == "krenn_gu.admissible_potential_cone"
        ]
        self.assertEqual(shared_imports, [])
        assignments = [
            node
            for node in tree.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "EXTREME_RAYS"
                for target in node.targets
            )
        ]
        self.assertEqual(len(assignments), 1)

    def test_finite_leaf_audits_are_claim_owned(self) -> None:
        classification = json.loads(
            (REPO_ROOT / "catalog/layout-classification.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (REPO_ROOT / "catalog/moved-paths.json").read_text(
                encoding="utf-8"
            )
        )
        classified = {
            item["old_path"]: item for item in classification["entries"]
        }
        moved = {item["old_path"]: item for item in manifest["moves"]}
        for old_path, new_path in FINITE_LEAF_CORRECTIONS.items():
            with self.subTest(old_path=old_path):
                self.assertTrue((REPO_ROOT / new_path).is_file())
                self.assertFalse((REPO_ROOT / "src/krenn_gu" / old_path).exists())
                self.assertEqual(classified[old_path]["proposed_path"], new_path)
                self.assertEqual(classified[old_path]["category"], "claim_script")
                self.assertEqual(moved[old_path]["new_path"], new_path)
                self.assertEqual(
                    moved[old_path]["executed_batch"],
                    "finite-stage28-inverse-taper-correction-stage33",
                )

    def test_finite_leaf_consumers_do_not_import_src_aliases(self) -> None:
        forbidden = {
            "krenn_gu.eight_vertex_degree4_support",
            "krenn_gu.verify_fourteen_vertex_no_one_term_support",
            "krenn_gu.verify_laurent_batch_manifest",
        }
        for relative_path in CORRECTED_CONSUMERS:
            with self.subTest(path=relative_path):
                tree = ast.parse(
                    (REPO_ROOT / relative_path).read_text(encoding="utf-8")
                )
                modules = {
                    node.module
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ImportFrom)
                }
                self.assertTrue(forbidden.isdisjoint(modules))


if __name__ == "__main__":
    unittest.main()
