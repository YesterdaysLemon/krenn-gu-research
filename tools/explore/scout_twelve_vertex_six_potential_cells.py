"""Scout one deterministic port realization per order-twelve type cell.

This is deliberately not a full port census.  It enumerates the complete
connected cubic catalogue, every distinguished Kotzig colouring, and all
eight normal-type assignments, then tests only the first reciprocal
cubic port realization found in each feasible cell under all six
permuted positive potentials.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import time

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from analyze_ten_vertex_degree_six_kotzig_port_survivors import (
    enumerate_coloured_matchings,
)
from analyze_ten_vertex_permuted_potential_survivors import (
    permuted_potential,
)
from explore_eight_vertex_degree_six_kotzig_ports import (
    balanced_allowed_entries,
    decode_graph6,
    edge,
    kotzig_colourings,
    normal_types,
)

NormalType = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def connected_cubic_catalogue() -> tuple[str, ...]:
    resolved = Path.cwd().resolve()
    posix = resolved.as_posix()
    if len(posix) < 3 or posix[1:3] != ":/":
        raise AssertionError(
            "the bundled nauty command expects a Windows drive path"
        )
    workspace = (
        f"/mnt/{posix[0].lower()}/{posix[3:]}"
    )
    command = (
        f'cd "{workspace}" && '
        "./tmp/nauty2_9_3/geng -cq -d3 -D3 12"
    )
    result = subprocess.run(
        ["wsl", "bash", "-lc", command],
        check=True,
        capture_output=True,
        text=True,
    )
    return tuple(
        row.strip()
        for row in result.stdout.splitlines()
        if row.strip()
    )


def first_port_realization(
    order: int,
    colouring,
    normals: tuple[NormalType, ...],
) -> tuple[tuple[int, int, int, int, bool, str, int], ...] | None:
    diagonal = set().union(
        *(set(matching) for matching in colouring)
    )
    stubs = tuple(
        (vertex, colour)
        for vertex in range(order)
        for colour in range(3)
    )
    stub_id = {stub: index for index, stub in enumerate(stubs)}
    options: list[tuple[int, ...]] = []
    for vertex, colour in stubs:
        partner_colour = normals[vertex][colour]
        options.append(
            tuple(
                stub_id[partner, partner_colour]
                for partner in range(order)
                if (
                    partner != vertex
                    and normals[partner][partner_colour]
                    == colour
                    and edge(vertex, partner) not in diagonal
                    and (
                        (
                            partner_colour,
                            colour,
                        )
                        if vertex < partner
                        else (
                            colour,
                            partner_colour,
                        )
                    )
                    in balanced_allowed_entries(
                        normals[min(vertex, partner)],
                        normals[max(vertex, partner)],
                    )
                )
            )
        )

    remaining = set(range(3 * order))
    used_pairs = set()
    chosen = []

    def search() -> bool:
        if not remaining:
            return True
        first = min(
            remaining,
            key=lambda stub: sum(
                (
                    other in remaining
                    and edge(
                        stubs[stub][0], stubs[other][0]
                    )
                    not in used_pairs
                )
                for other in options[stub]
            ),
        )
        left_vertex, left_colour = stubs[first]
        for second in options[first]:
            if second not in remaining:
                continue
            right_vertex, right_colour = stubs[second]
            pair = edge(left_vertex, right_vertex)
            if pair in used_pairs:
                continue
            if pair[0] == left_vertex:
                half_colours = (right_colour, left_colour)
            else:
                half_colours = (left_colour, right_colour)
            remaining.remove(first)
            remaining.remove(second)
            used_pairs.add(pair)
            chosen.append(
                (
                    pair[0],
                    pair[1],
                    half_colours[0],
                    half_colours[1],
                    True,
                    "K",
                    0,
                )
            )
            if search():
                return True
            chosen.pop()
            used_pairs.remove(pair)
            remaining.add(second)
            remaining.add(first)
        return False

    return tuple(chosen) if search() else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-theorem",
        type=Path,
        default=REPO_ROOT / "claims" / "arbitrary-order" / "THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md",
    )
    parser.add_argument(
        "--potential-lemma",
        type=Path,
        default=REPO_ROOT / "SIX_PERMUTED_POTENTIALS_LEMMA.md",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_cells_scouted.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    order = 12

    rows = connected_cubic_catalogue()
    if len(rows) != 85 or len(set(rows)) != 85:
        raise AssertionError(
            "order-twelve connected cubic catalogue changed"
        )
    permutations = tuple(itertools.permutations(range(3)))
    graph_records = []
    total_colourings = 0
    total_cells = 0
    feasible_cells = 0
    infeasible_cells = 0
    success_count_histogram: Counter[int] = Counter()
    all_six_survivors = []

    for graph_index, graph6 in enumerate(rows):
        diagonal = set(decode_graph6(graph6))
        colourings = kotzig_colourings(range(order), diagonal)
        total_colourings += len(colourings)
        graph_cells = 0
        graph_feasible = 0
        graph_survivors = 0
        for colouring_index, colouring in enumerate(colourings):
            assignments = normal_types(
                range(order), colouring
            )
            if len(assignments) != 8:
                raise AssertionError(
                    "order-twelve type-assignment count changed"
                )
            for type_index, normals in enumerate(assignments):
                total_cells += 1
                graph_cells += 1
                ports = first_port_realization(
                    order, colouring, normals
                )
                if ports is None:
                    infeasible_cells += 1
                    continue
                feasible_cells += 1
                graph_feasible += 1
                guaranteed = list(ports)
                for colour, matching in enumerate(colouring):
                    for left, right in matching:
                        guaranteed.append(
                            (
                                left,
                                right,
                                colour,
                                colour,
                                True,
                                "D",
                                0,
                            )
                        )
                counts, _first, _forced = (
                    enumerate_coloured_matchings(
                        order, tuple(guaranteed)
                    )
                )
                mixed = {
                    row: count
                    for row, count in counts.items()
                    if len(set(row)) > 1
                }
                successes = 0
                signatures = []
                for permutation_index, permutation in enumerate(
                    permutations
                ):
                    potentials = tuple(
                        permuted_potential(
                            normal, permutation
                        )
                        for normal in normals
                    )
                    minimum = min(
                        sum(
                            potentials[vertex][colour]
                            for vertex, colour in enumerate(row)
                        )
                        for row in mixed
                    )
                    minimum_counts = [
                        count
                        for row, count in mixed.items()
                        if sum(
                            potentials[vertex][colour]
                            for vertex, colour in enumerate(row)
                        )
                        == minimum
                    ]
                    signature = tuple(
                        sorted(Counter(minimum_counts).items())
                    )
                    signatures.append(
                        [
                            permutation_index,
                            minimum,
                            [
                                [key, value]
                                for key, value in signature
                            ],
                        ]
                    )
                    if 1 in minimum_counts:
                        successes += 1
                success_count_histogram[successes] += 1
                if successes == 0:
                    graph_survivors += 1
                    all_six_survivors.append(
                        {
                            "graph_index": graph_index,
                            "colouring_index": colouring_index,
                            "type_index": type_index,
                            "signatures": signatures,
                        }
                    )
        graph_records.append(
            {
                "graph_index": graph_index,
                "graph6": graph6,
                "kotzig_colourings": len(colourings),
                "type_cells": graph_cells,
                "feasible_first_port_cells": graph_feasible,
                "all_six_potential_survivors": graph_survivors,
            }
        )

    if total_cells != 8 * total_colourings:
        raise AssertionError("type-cell total changed")
    payload = {
        "verified": True,
        "status": "exploratory_one_port_per_type_cell",
        "scope": (
            "complete order-twelve connected cubic and distinguished "
            "Kotzig/type-cell domain, but only the first deterministic "
            "reciprocal port realization in each feasible cell"
        ),
        "catalogue_provenance": "nauty geng -cq -d3 -D3 12",
        "catalogue_rows": len(rows),
        "catalogue_graph6": list(rows),
        "graphs": graph_records,
        "labelled_kotzig_colourings": total_colourings,
        "normal_type_cells": total_cells,
        "feasible_first_port_cells": feasible_cells,
        "cells_without_a_port_realization": infeasible_cells,
        "successful_potential_count_histogram": {
            str(key): value
            for key, value in sorted(
                success_count_histogram.items()
            )
        },
        "sampled_all_six_potential_survivors": len(
            all_six_survivors
        ),
        "survivor_records": all_six_survivors,
        "sampling_complete_for_port_graphs": False,
        "order_twelve_branch_excluded": False,
        "base_theorem": str(args.base_theorem),
        "base_theorem_sha256": sha256(args.base_theorem),
        "potential_lemma": str(args.potential_lemma),
        "potential_lemma_sha256": sha256(
            args.potential_lemma
        ),
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
