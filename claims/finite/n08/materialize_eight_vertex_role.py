"""Materialize one canonical eight-vertex skeleton role as DIMACS units."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from eight_vertex_degree4_cegar import write_augmented_cnf
from eight_vertex_skeleton_batch import (
    canonical_degree_three_role_skeletons,
    canonical_minimum_five_skeletons,
    canonical_normalized_killer_skeletons,
    canonical_role_skeletons,
    ordered_role_skeletons,
)
from eight_vertex_sparse_exact import local_allowed_edges


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--target-edges", type=int)
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        required=True,
    )
    parser.add_argument("--role-index", type=int, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[args.center_degree]
    roles, catalogue = builder(
        args.graph6, target_edges=args.target_edges
    )
    ordered = ordered_role_skeletons(roles)
    if not 0 <= args.role_index < len(ordered):
        raise ValueError(
            f"role index {args.role_index} is outside "
            f"0..{len(ordered) - 1}"
        )

    skeleton = ordered[args.role_index]
    present = set(skeleton)
    allowed = local_allowed_edges(args.center_degree)
    first_block_variable = 1 + 9 * len(allowed)
    units = [
        (
            first_block_variable + edge_index
            if edge in present
            else -(first_block_variable + edge_index)
        ,)
        for edge_index, edge in enumerate(allowed)
    ]
    write_augmented_cnf(args.base_cnf, args.output_cnf, units)

    payload = {
        "scope": "one fixed canonical eight-vertex skeleton role",
        "center_degree": args.center_degree,
        "target_edges": args.target_edges,
        "role_index": args.role_index,
        **catalogue,
        "skeleton_edges": [list(edge) for edge in skeleton],
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "unit_clauses": [list(clause) for clause in units],
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
