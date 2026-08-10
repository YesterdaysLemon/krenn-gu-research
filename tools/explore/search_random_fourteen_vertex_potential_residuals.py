"""Randomly sample noncanonical order-fourteen reciprocal port graphs.

This exploratory search draws graph/factorization/type cells uniformly,
constructs randomized reciprocal exact covers, and tests the six original
potential rays plus the six extreme-ray/interior refinements.  It is a
counterexample search, not a finite-domain certificate.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)
from explore_eight_vertex_degree_six_kotzig_ports import (
    balanced_allowed_entries,
    decode_graph6,
    kotzig_colourings,
    normal_types,
)
from scout_kotzig_full_cone_cells import catalogue
from verify_full_admissible_potential_cone import EXTREME_RAYS

Normal = tuple[int, int, int]
Port = tuple[int, int, int, int, bool, str, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def randomized_port(
    order: int,
    colouring,
    normals: tuple[Normal, ...],
    generator: random.Random,
) -> tuple[Port, ...] | None:
    diagonal = set().union(
        *(set(matching) for matching in colouring)
    )
    stubs = tuple(
        (vertex, colour)
        for vertex in range(order)
        for colour in range(3)
    )
    stub_id = {stub: index for index, stub in enumerate(stubs)}
    options = []
    for vertex, colour in stubs:
        partner_colour = normals[vertex][colour]
        options.append(
            tuple(
                stub_id[(other, partner_colour)]
                for other in range(order)
                if (
                    other != vertex
                    and edge(vertex, other) not in diagonal
                    and normals[other][partner_colour] == colour
                    and (
                        (
                            partner_colour,
                            colour,
                        )
                        if vertex < other
                        else (
                            colour,
                            partner_colour,
                        )
                    )
                    in balanced_allowed_entries(
                        normals[min(vertex, other)],
                        normals[max(vertex, other)],
                    )
                )
            )
        )
    remaining = set(range(3 * order))
    used_pairs: set[tuple[int, int]] = set()
    chosen: list[Port] = []

    def visit() -> bool:
        if not remaining:
            return True
        candidate_counts = {}
        best = 3 * order + 1
        for stub in remaining:
            vertex = stubs[stub][0]
            available = tuple(
                other
                for other in options[stub]
                if (
                    other in remaining
                    and edge(vertex, stubs[other][0])
                    not in used_pairs
                )
            )
            candidate_counts[stub] = available
            best = min(best, len(available))
        if best == 0:
            return False
        tied = tuple(
            stub
            for stub, available in candidate_counts.items()
            if len(available) == best
        )
        first = generator.choice(tied)
        left_vertex, left_colour = stubs[first]
        candidates = list(candidate_counts[first])
        generator.shuffle(candidates)
        for second in candidates:
            right_vertex, right_colour = stubs[second]
            pair = edge(left_vertex, right_vertex)
            cu, cv = (
                (right_colour, left_colour)
                if pair[0] == left_vertex
                else (left_colour, right_colour)
            )
            remaining.remove(first)
            remaining.remove(second)
            used_pairs.add(pair)
            chosen.append(
                (
                    pair[0],
                    pair[1],
                    cu,
                    cv,
                    True,
                    "K",
                    0,
                )
            )
            if visit():
                return True
            chosen.pop()
            used_pairs.remove(pair)
            remaining.add(second)
            remaining.add(first)
        return False

    return tuple(sorted(chosen)) if visit() else None


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=25_000)
    parser.add_argument("--seed", type=int, default=20_260_726)
    parser.add_argument("--checkpoint-every", type=int, default=1_000)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "fourteen_vertex_random_potential_residual_search.json",
        ),
    )
    args = parser.parse_args()
    if args.samples < 1:
        raise ValueError("--samples must be positive")
    started = time.perf_counter()
    order = 14
    generator = random.Random(args.seed)
    rows = catalogue(order)
    cells = []
    for graph_index, graph6 in enumerate(rows):
        graph_edges = set(decode_graph6(graph6))
        for colouring_index, colouring in enumerate(
            kotzig_colourings(range(order), graph_edges)
        ):
            for type_index, normals in enumerate(
                normal_types(range(order), colouring)
            ):
                cells.append(
                    (
                        graph_index,
                        graph6,
                        colouring_index,
                        type_index,
                        colouring,
                        normals,
                    )
                )
    if len(rows) != 509 or len(cells) != 19_680:
        raise AssertionError("order-fourteen cell domain changed")

    permutations = tuple(itertools.permutations(range(3)))
    interior = (1, 1, 1, 1, 1, 1)
    old_success_histogram: Counter[int] = Counter()
    extreme_success_histogram: Counter[int] = Counter()
    combined_success_histogram: Counter[int] = Counter()
    old_residuals = []
    extreme_residuals = []
    combined_residuals = []
    seen: set[tuple[int, tuple[tuple[int, ...], ...]]] = set()
    duplicates = 0
    failed_covers = 0

    def payload(completed: int, final: bool) -> dict[str, object]:
        return {
            "verified": True,
            "status": (
                "exploratory_random_port_search_complete"
                if final
                else "exploratory_random_port_search_checkpoint"
            ),
            "scope": (
                "uniform random graph/factorization/type cells and "
                "randomized reciprocal exact covers; not exhaustive"
            ),
            "order": order,
            "seed": args.seed,
            "requested_samples": args.samples,
            "completed_draws": completed,
            "distinct_architectures": len(seen),
            "duplicate_architectures": duplicates,
            "failed_randomized_covers": failed_covers,
            "connected_cubic_classes": len(rows),
            "normal_type_cells": len(cells),
            "original_success_count_histogram": {
                str(key): value
                for key, value in sorted(old_success_histogram.items())
            },
            "extreme_success_count_histogram": {
                str(key): value
                for key, value in sorted(
                    extreme_success_histogram.items()
                )
            },
            "combined_success_count_histogram": {
                str(key): value
                for key, value in sorted(
                    combined_success_histogram.items()
                )
            },
            "original_six_ray_residuals": len(old_residuals),
            "extreme_refinement_residuals": len(extreme_residuals),
            "combined_twelve_direction_residuals": len(
                combined_residuals
            ),
            "original_residual_examples": old_residuals[:20],
            "extreme_residual_examples": extreme_residuals[:20],
            "combined_residual_examples": combined_residuals[:20],
            "sampling_complete_for_port_graphs": False,
            "order_fourteen_branch_excluded": False,
            "global_conjecture_resolved": False,
            "source": str(Path(__file__)),
            "source_sha256": sha256(Path(__file__)),
            "elapsed_seconds": time.perf_counter() - started,
        }

    completed = 0
    while completed < args.samples:
        cell_id = generator.randrange(len(cells))
        (
            graph_index,
            graph6,
            colouring_index,
            type_index,
            colouring,
            normals,
        ) = cells[cell_id]
        ports = randomized_port(
            order, colouring, normals, generator
        )
        completed += 1
        if ports is None:
            failed_covers += 1
            continue
        architecture_key = (
            cell_id,
            tuple(
                (port[0], port[1], port[2], port[3])
                for port in ports
            ),
        )
        if architecture_key in seen:
            duplicates += 1
            continue
        seen.add(architecture_key)

        edges = list(ports)
        for colour, matching in enumerate(colouring):
            edges.extend(
                (
                    left,
                    right,
                    colour,
                    colour,
                    True,
                    "D",
                    0,
                )
                for left, right in matching
            )
        counts, _first, _forced = enumerate_coloured_matchings(
            order, tuple(edges)
        )
        mixed_counts = {
            row: count
            for row, count in counts.items()
            if len(set(row)) > 1
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
            row: tuple(
                sum(
                    potentials[vertex][colour][ray]
                    for vertex, colour in enumerate(row)
                )
                for ray in range(6)
            )
            for row in mixed_counts
        }
        old_successes = 0
        for ray in range(6):
            minimum = min(
                value[ray] for value in signatures.values()
            )
            old_successes += any(
                mixed_counts[row] == 1
                and signatures[row][ray] == minimum
                for row in mixed_counts
            )
        extreme_successes = 0
        for extreme in EXTREME_RAYS:
            keys = {
                row: (
                    dot(value, extreme),
                    dot(value, interior),
                )
                for row, value in signatures.items()
            }
            minimum = min(keys.values())
            extreme_successes += any(
                mixed_counts[row] == 1 and keys[row] == minimum
                for row in mixed_counts
            )
        old_success_histogram[old_successes] += 1
        extreme_success_histogram[extreme_successes] += 1
        combined_success_histogram[
            old_successes + extreme_successes
        ] += 1
        record = {
            "sample": completed,
            "cell_id": cell_id,
            "graph_index": graph_index,
            "graph6": graph6,
            "colouring_index": colouring_index,
            "type_index": type_index,
            "original_successes": old_successes,
            "extreme_successes": extreme_successes,
            "normal_types": [list(normal) for normal in normals],
            "diagonal_matchings": [
                [list(pair) for pair in matching]
                for matching in colouring
            ],
            "port_edges": [
                {
                    "edge": [port[0], port[1]],
                    "half_colours": [port[2], port[3]],
                }
                for port in ports
            ],
        }
        if old_successes == 0:
            old_residuals.append(record)
        if extreme_successes == 0:
            extreme_residuals.append(record)
        if old_successes + extreme_successes == 0:
            combined_residuals.append(record)
            checkpoint(args.output, payload(completed, True))
            print(
                "combined residual found at sample",
                completed,
                flush=True,
            )
            return
        if (
            args.checkpoint_every > 0
            and completed % args.checkpoint_every == 0
        ):
            checkpoint(args.output, payload(completed, False))
            print(
                "samples",
                completed,
                "distinct",
                len(seen),
                "old residuals",
                len(old_residuals),
                "extreme residuals",
                len(extreme_residuals),
                "combined residuals",
                len(combined_residuals),
                "elapsed",
                round(time.perf_counter() - started, 1),
                flush=True,
            )

    checkpoint(args.output, payload(completed, True))
    print(
        json.dumps(
            {
                "completed_draws": completed,
                "distinct_architectures": len(seen),
                "original_six_ray_residuals": len(old_residuals),
                "extreme_refinement_residuals": len(extreme_residuals),
                "combined_twelve_direction_residuals": len(
                    combined_residuals
                ),
                "sampling_complete_for_port_graphs": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
