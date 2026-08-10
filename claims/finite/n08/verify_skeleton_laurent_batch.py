"""Fail-closed audit of an incremental skeleton/Laurent batch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu.eight_vertex_degree4_cegar import full_equations
from eight_vertex_skeleton_batch import (
    canonical_degree_three_role_skeletons,
    canonical_minimum_five_skeletons,
    canonical_normalized_killer_skeletons,
    canonical_role_skeletons,
    ordered_role_skeletons,
)
from krenn_gu.search_witness import EquationSystem
from verify_laurent_batch_manifest import (
    audit_cnf,
    audit_conflict,
    structural_zero_indices,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    manifest = json.loads(
        args.manifest.read_text(encoding="utf-8")
    )
    center_degree = int(batch.get("center_degree", 4))
    if int(manifest.get("center_degree", 4)) != center_degree:
        raise AssertionError("batch and manifest center degrees differ")
    target_edges = batch.get("target_edges")
    if target_edges is not None:
        target_edges = int(target_edges)

    builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[center_degree]
    roles, catalogue = builder(
        args.graph6, target_edges=target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    if batch.get("status") != "complete":
        raise AssertionError("batch did not finish without fallback")
    if int(batch["fallback_count"]) != 0:
        raise AssertionError("batch contains exact fallbacks")
    if (
        int(batch["processed"]),
        int(batch["unsat_count"]),
        int(batch["canonical_role_skeletons"]),
    ) != (len(ordered_roles), len(ordered_roles), len(ordered_roles)):
        raise AssertionError("batch coverage count is inconsistent")
    for key, value in catalogue.items():
        if int(batch[key]) != value:
            raise AssertionError(f"catalogue field changed: {key}")

    rows = list(batch["rows"])
    if len(rows) != len(ordered_roles):
        raise AssertionError("batch row count is incomplete")
    seen_conflicts: list[int] = []
    for role_index, (row, skeleton) in enumerate(
        zip(rows, ordered_roles, strict=True)
    ):
        if int(row["role_index"]) != role_index:
            raise AssertionError("role indices are not contiguous")
        if row["skeleton_edges"] != [
            list(edge) for edge in skeleton
        ]:
            raise AssertionError("batch skeleton ordering changed")
        if row["status"] != "UNSAT":
            raise AssertionError("batch contains a non-UNSAT role")
        conflict_indices = list(map(int, row["conflict_indices"]))
        if int(row["support_models"]) != len(conflict_indices):
            raise AssertionError(
                "support-model and conflict counts differ in a role"
            )
        seen_conflicts.extend(conflict_indices)

    conflicts = list(manifest["conflicts"])
    if conflicts != list(batch["conflicts"]):
        raise AssertionError("batch and manifest conflicts differ")
    if seen_conflicts != list(range(len(conflicts))):
        raise AssertionError(
            "conflicts are not assigned exactly once in discovery order"
        )
    if (
        int(batch["support_models"]),
        int(batch["laurent_conflicts"]),
        int(manifest["support_models"]),
        int(manifest["laurent_conflicts"]),
    ) != (
        len(conflicts),
        len(conflicts),
        len(conflicts),
        len(conflicts),
    ):
        raise AssertionError("global conflict counts are inconsistent")
    expected_transport = sum(
        conflict.get("certificate_kind") == "cancellation_transport"
        for conflict in conflicts
    )
    for source in (batch, manifest):
        if (
            "transport_conflicts" in source
            and int(source["transport_conflicts"]) != expected_transport
        ):
            raise AssertionError("transport conflict count is inconsistent")

    system = EquationSystem(8, 3)
    equations, names, name_to_flat = full_equations(system)
    structural_zero = structural_zero_indices(
        system, center_degree
    )
    clauses: set[tuple[int, ...]] = set()
    for conflict_index, conflict in enumerate(conflicts):
        if int(conflict["conflict_index"]) != conflict_index:
            raise AssertionError("conflict indices changed")
        clauses.update(
            audit_conflict(
                system,
                equations,
                names,
                name_to_flat,
                structural_zero,
                conflict,
                center_degree=center_degree,
            )
        )
    ordered_clauses = sorted(clauses)
    recorded_clauses = [
        tuple(map(int, clause))
        for clause in manifest["learned_clauses"]
    ]
    if recorded_clauses != ordered_clauses:
        raise AssertionError("learned clause union changed")

    base_cnf = Path(str(manifest["base_cnf"]))
    learned_cnf = Path(str(manifest["learned_cnf"]))
    if sha256(base_cnf) != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash mismatch")
    if sha256(learned_cnf) != manifest["learned_cnf_sha256"]:
        raise AssertionError("learned CNF hash mismatch")
    if batch["learned_cnf_sha256"] != manifest[
        "learned_cnf_sha256"
    ]:
        raise AssertionError("batch learned CNF hash changed")
    audit_cnf(base_cnf, learned_cnf, ordered_clauses)

    payload = {
        "verified": True,
        "center_degree": center_degree,
        "target_edges": target_edges,
        **catalogue,
        "support_models": len(conflicts),
        "laurent_conflicts": len(conflicts),
        "transport_conflicts": expected_transport,
        "learned_clauses": len(ordered_clauses),
        "graph6_sha256": sha256(args.graph6),
        "base_cnf_sha256": manifest["base_cnf_sha256"],
        "learned_cnf_sha256": manifest["learned_cnf_sha256"],
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
