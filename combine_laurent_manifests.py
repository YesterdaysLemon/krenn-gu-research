"""Combine independently replayed Laurent conflicts onto another base CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from eight_vertex_degree4_cegar import (
    full_equations,
    write_augmented_cnf,
)
from search_witness import EquationSystem
from verify_laurent_batch_manifest import (
    audit_conflict,
    structural_zero_indices,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_conflicts(
    manifest: dict[str, object],
) -> list[dict[str, object]]:
    conflicts = list(manifest.get("conflicts", []))
    if not conflicts and "used_equation_indices" in manifest:
        conflicts = [manifest]
    return conflicts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, required=True)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=4,
    )
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    equations, names, name_to_flat = full_equations(system)
    structural_zero = structural_zero_indices(
        system, args.center_degree
    )

    clauses: set[tuple[int, ...]] = set()
    conflict_count = 0
    sources: list[dict[str, object]] = []
    for path in args.manifest:
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if int(manifest.get("center_degree", 4)) != args.center_degree:
            raise AssertionError(
                f"{path} belongs to a different center degree"
            )
        conflicts = manifest_conflicts(manifest)
        reconstructed: set[tuple[int, ...]] = set()
        for conflict in conflicts:
            reconstructed.update(
                audit_conflict(
                    system,
                    equations,
                    names,
                    name_to_flat,
                    structural_zero,
                    conflict,
                    center_degree=args.center_degree,
                )
            )
        recorded_field = manifest.get("learned_clauses")
        recorded = (
            {
                tuple(map(int, clause))
                for clause in recorded_field
            }
            if isinstance(recorded_field, list)
            else None
        )
        if recorded is not None and reconstructed != recorded:
            raise AssertionError(
                f"{path} clauses do not match its exact conflicts"
            )
        clauses.update(reconstructed)
        conflict_count += len(conflicts)
        sources.append(
            {
                "path": str(path),
                "sha256": sha256(path),
                "conflicts": len(conflicts),
                "clauses": len(reconstructed),
            }
        )

    ordered_clauses = sorted(clauses)
    write_augmented_cnf(
        args.base_cnf, args.output_cnf, ordered_clauses
    )
    payload = {
        "scope": (
            "replayed exact Laurent support no-goods transferred "
            "to a support CNF"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "center_degree": args.center_degree,
        "source_manifests": sources,
        "conflicts": conflict_count,
        "distinct_learned_clauses": len(ordered_clauses),
        "learned_clauses": [
            list(clause) for clause in ordered_clauses
        ],
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
    }
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
