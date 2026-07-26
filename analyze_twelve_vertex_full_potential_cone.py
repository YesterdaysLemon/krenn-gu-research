"""Apply the complete admissible potential cone to order-twelve residuals."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    EntryEdge,
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)
from verify_full_admissible_potential_cone import EXTREME_RAYS


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cells",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_port_cell_orbits_counted.json"
        ),
    )
    parser.add_argument(
        "--exhaustion",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_six_potential_orbits_exhausted.json"
        ),
    )
    parser.add_argument(
        "--residuals",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_six_potential_orbits_residuals.tsv"
        ),
    )
    parser.add_argument(
        "--cone-verification",
        type=Path,
        default=Path(
            "tmp", "full_admissible_potential_cone_verified.json"
        ),
    )
    parser.add_argument(
        "--cone-theorem",
        type=Path,
        default=Path("FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_full_potential_cone_analyzed.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    cells_payload = json.loads(args.cells.read_text(encoding="utf-8"))
    exhaustion = json.loads(
        args.exhaustion.read_text(encoding="utf-8")
    )
    cone = json.loads(
        args.cone_verification.read_text(encoding="utf-8")
    )
    cells = cells_payload["cell_representatives"]
    residual_lines = tuple(
        tuple(map(int, line.split()))
        for line in args.residuals.read_text(
            encoding="utf-8"
        ).splitlines()
    )
    if (
        cone.get("verified") is not True
        or cone.get("D_neutrality_nullity") != 6
        or cone.get("extreme_ray_rank") != 6
        or exhaustion.get("all_six_potential_survivors")
        != len(residual_lines)
        or len(residual_lines) != 395
    ):
        raise AssertionError("full-cone input binding changed")

    permutations = tuple(itertools.permutations(range(3)))
    interior = (1, 1, 1, 1, 1, 1)
    success_count_histogram: Counter[int] = Counter()
    success_mask_histogram: Counter[int] = Counter()
    witness_records = []
    survivors = []

    for residual_index, fields in enumerate(residual_lines):
        cell_id = fields[0]
        architecture = str(fields[3])
        cell = cells[cell_id]
        normals = tuple(
            tuple(map(int, row)) for row in cell["normal_types"]
        )
        edges: list[EntryEdge] = []
        for colour, matching in enumerate(
            cell["diagonal_matchings"]
        ):
            for left, right in matching:
                edges.append(
                    (
                        int(left),
                        int(right),
                        colour,
                        colour,
                        True,
                        "D",
                        0,
                    )
                )
        for offset in range(4, len(fields), 4):
            left, right, cu, cv = fields[offset : offset + 4]
            edges.append(
                (left, right, cu, cv, True, "K", 0)
            )
        counts, first_matchings, _forced = (
            enumerate_coloured_matchings(12, tuple(edges))
        )
        mixed_counts = {
            colouring: count
            for colouring, count in counts.items()
            if len(set(colouring)) > 1
        }
        potentials = tuple(
            tuple(
                tuple(
                    permuted_potential(normal, permutation)[colour]
                    for permutation in permutations
                )
                for colour in range(3)
            )
            for normal in normals
        )
        signatures = {
            colouring: tuple(
                sum(
                    potentials[vertex][colour][ray]
                    for vertex, colour in enumerate(colouring)
                )
                for ray in range(6)
            )
            for colouring in mixed_counts
        }

        mask = 0
        ray_witnesses = []
        for ray_index, ray in enumerate(EXTREME_RAYS):
            keys = {
                colouring: (
                    dot(value, ray),
                    dot(value, interior),
                )
                for colouring, value in signatures.items()
            }
            minimum = min(keys.values())
            singleton = next(
                (
                    colouring
                    for colouring, count in sorted(
                        mixed_counts.items()
                    )
                    if count == 1 and keys[colouring] == minimum
                ),
                None,
            )
            if singleton is None:
                continue
            mask |= 1 << ray_index
            matching = first_matchings[singleton]
            ray_witnesses.append(
                {
                    "extreme_ray_index": ray_index,
                    "lexicographic_minimum": list(minimum),
                    "unique_colouring": list(singleton),
                    "unique_matching": [
                        {
                            "edge": [
                                edges[edge_id][0],
                                edges[edge_id][1],
                            ],
                            "half_colours": [
                                edges[edge_id][2],
                                edges[edge_id][3],
                            ],
                            "kind": edges[edge_id][5],
                        }
                        for edge_id in matching
                    ],
                }
            )

        success_mask_histogram[mask] += 1
        success_count_histogram[mask.bit_count()] += 1
        if mask == 0:
            survivors.append(
                {
                    "residual_index": residual_index,
                    "cell_id": cell_id,
                    "architecture_hash": architecture,
                }
            )
        else:
            witness_records.append(
                {
                    "residual_index": residual_index,
                    "cell_id": cell_id,
                    "architecture_hash": architecture,
                    "success_mask": mask,
                    "ray_witnesses": ray_witnesses,
                }
            )

    payload = {
        "verified": not survivors,
        "status": "finite_order_twelve_full_cone_analysis",
        "scope": (
            "the 395 survivors of the six original potential rays, "
            "tested against all six extreme-ray/interior lexicographic "
            "directions of the complete admissible local cone"
        ),
        "cells": str(args.cells),
        "cells_sha256": sha256(args.cells),
        "exhaustion": str(args.exhaustion),
        "exhaustion_sha256": sha256(args.exhaustion),
        "residuals": str(args.residuals),
        "residuals_sha256": sha256(args.residuals),
        "cone_verification": str(args.cone_verification),
        "cone_verification_sha256": sha256(args.cone_verification),
        "cone_theorem": str(args.cone_theorem),
        "cone_theorem_sha256": sha256(args.cone_theorem),
        "original_six_ray_residuals": len(residual_lines),
        "full_cone_success_count_histogram": {
            str(key): value
            for key, value in sorted(
                success_count_histogram.items()
            )
        },
        "full_cone_success_mask_histogram": {
            str(key): value
            for key, value in sorted(
                success_mask_histogram.items()
            )
        },
        "full_cone_contradictions": len(witness_records),
        "witness_records": witness_records,
        "survivors": len(survivors),
        "survivor_records": survivors,
        "order_twelve_pairwise_disjoint_exact_degree_six_excluded": (
            not survivors
        ),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": payload["verified"],
                "original_six_ray_residuals": len(residual_lines),
                "full_cone_success_count_histogram": (
                    payload["full_cone_success_count_histogram"]
                ),
                "survivors": len(survivors),
                "elapsed_seconds": payload["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
