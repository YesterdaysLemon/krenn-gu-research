"""Count reciprocal port realizations on order-twelve cell orbits.

The complete connected cubic/Kotzig/normal-type domain has many labelled
duplicates.  This script quotients the 2,688 cells by automorphisms of the
underlying cubic graph together with global colour permutations, then
counts every simple reciprocal cubic port realization in each cell
representative.  It does not yet test matching amplitudes.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.bootstrap import expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/finite/n08/degree-six-kotzig-port")

from explore_eight_vertex_degree_six_kotzig_ports import (
    balanced_allowed_entries,
    decode_graph6,
    edge,
    kotzig_colourings,
    normal_types,
)

Edge = tuple[int, int]
NormalType = tuple[int, int, int]
Permutation = tuple[int, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def graph_automorphisms(
    order: int, edges: set[Edge]
) -> tuple[Permutation, ...]:
    adjacency = [
        [False] * order for _ in range(order)
    ]
    for left, right in edges:
        adjacency[left][right] = True
        adjacency[right][left] = True
    mapping: dict[int, int] = {}
    inverse: dict[int, int] = {}
    answers = []

    def search() -> None:
        if len(mapping) == order:
            answers.append(
                tuple(mapping[vertex] for vertex in range(order))
            )
            return
        unmapped = [
            vertex
            for vertex in range(order)
            if vertex not in mapping
        ]
        source = max(
            unmapped,
            key=lambda vertex: sum(
                (
                    other in mapping
                    and adjacency[vertex][other]
                )
                for other in range(order)
            ),
        )
        for target in range(order):
            if target in inverse:
                continue
            if not all(
                adjacency[source][other]
                == adjacency[target][mapping[other]]
                for other in mapping
            ):
                continue
            mapping[source] = target
            inverse[target] = source
            search()
            del inverse[target]
            del mapping[source]

    search()
    if not answers:
        raise AssertionError("graph lost its identity automorphism")
    return tuple(sorted(answers))


def transformed_cell(
    order: int,
    colouring,
    normals: tuple[NormalType, ...],
    vertex_permutation: Permutation,
    colour_permutation: tuple[int, int, int],
) -> tuple[
    tuple[tuple[int, int, int], ...],
    tuple[NormalType, ...],
]:
    coloured_edges = []
    for colour, matching in enumerate(colouring):
        for left, right in matching:
            image = edge(
                vertex_permutation[left],
                vertex_permutation[right],
            )
            coloured_edges.append(
                (image[0], image[1], colour_permutation[colour])
            )
    transformed_normals: list[NormalType | None] = [
        None
    ] * order
    for vertex in range(order):
        row = [-1] * 3
        for colour in range(3):
            row[colour_permutation[colour]] = (
                colour_permutation[normals[vertex][colour]]
            )
        transformed_normals[vertex_permutation[vertex]] = tuple(
            row
        )
    if any(item is None for item in transformed_normals):
        raise AssertionError("cell transformation lost a vertex")
    return (
        tuple(sorted(coloured_edges)),
        tuple(item for item in transformed_normals if item is not None),
    )


def representative_cells(
    order: int, graph6_rows: tuple[str, ...]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    colour_permutations = tuple(
        itertools.permutations(range(3))
    )
    representatives = []
    graph_records = []
    for graph_index, graph6 in enumerate(graph6_rows):
        diagonal = set(decode_graph6(graph6))
        colourings = kotzig_colourings(
            range(order), diagonal
        )
        if not colourings:
            graph_records.append(
                {
                    "graph_index": graph_index,
                    "graph6": graph6,
                    "automorphisms": len(
                        graph_automorphisms(order, diagonal)
                    ),
                    "labelled_kotzig_colourings": 0,
                    "labelled_type_cells": 0,
                    "cell_orbits": 0,
                }
            )
            continue
        automorphisms = graph_automorphisms(order, diagonal)
        by_key: dict[
            tuple[
                tuple[tuple[int, int, int], ...],
                tuple[NormalType, ...],
            ],
            list[tuple[int, int, object, tuple[NormalType, ...]]],
        ] = {}
        for colouring_index, colouring in enumerate(colourings):
            assignments = normal_types(
                range(order), colouring
            )
            for type_index, normals in enumerate(assignments):
                canonical = min(
                    transformed_cell(
                        order,
                        colouring,
                        normals,
                        automorphism,
                        colour_permutation,
                    )
                    for automorphism in automorphisms
                    for colour_permutation in colour_permutations
                )
                by_key.setdefault(canonical, []).append(
                    (
                        colouring_index,
                        type_index,
                        colouring,
                        normals,
                    )
                )

        for cell_index, (canonical, members) in enumerate(
            sorted(by_key.items())
        ):
            (
                colouring_index,
                type_index,
                colouring,
                normals,
            ) = members[0]
            base = transformed_cell(
                order,
                colouring,
                normals,
                tuple(range(order)),
                (0, 1, 2),
            )
            stabilizer = sum(
                transformed_cell(
                    order,
                    colouring,
                    normals,
                    automorphism,
                    colour_permutation,
                )
                == base
                for automorphism in automorphisms
                for colour_permutation in colour_permutations
            )
            representatives.append(
                {
                    "graph_index": graph_index,
                    "graph6": graph6,
                    "cell_index": cell_index,
                    "colouring_index": colouring_index,
                    "type_index": type_index,
                    "orbit_size": len(members),
                    "stabilizer_size": stabilizer,
                    "diagonal_matchings": [
                        [list(pair) for pair in matching]
                        for matching in colouring
                    ],
                    "normal_types": [
                        list(item) for item in normals
                    ],
                    "canonical_key_sha256": hashlib.sha256(
                        repr(canonical).encode("ascii")
                    ).hexdigest(),
                }
            )
        graph_records.append(
            {
                "graph_index": graph_index,
                "graph6": graph6,
                "automorphisms": len(automorphisms),
                "labelled_kotzig_colourings": len(colourings),
                "labelled_type_cells": 8 * len(colourings),
                "cell_orbits": len(by_key),
            }
        )
    return representatives, graph_records


def reciprocal_port_count(
    order: int,
    colouring,
    normals: tuple[NormalType, ...],
) -> int:
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
    used_pairs: set[Edge] = set()
    count = 0

    def search() -> None:
        nonlocal count
        if not remaining:
            count += 1
            return
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
        left_vertex = stubs[first][0]
        for second in options[first]:
            if second not in remaining:
                continue
            pair = edge(
                left_vertex, stubs[second][0]
            )
            if pair in used_pairs:
                continue
            remaining.remove(first)
            remaining.remove(second)
            used_pairs.add(pair)
            search()
            used_pairs.remove(pair)
            remaining.add(second)
            remaining.add(first)

    search()
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalogue-source",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_cells_scouted.json",
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_port_cell_orbits_counted.json",
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    source = json.loads(
        args.catalogue_source.read_text(encoding="utf-8")
    )
    rows = tuple(source["catalogue_graph6"])
    if len(rows) != 85:
        raise AssertionError(
            "order-twelve catalogue row count changed"
        )
    representatives, graph_records = representative_cells(
        12, rows
    )
    if (
        sum(
            int(record["labelled_type_cells"])
            for record in graph_records
        )
        != 2_688
        or len(representatives) != 154
    ):
        raise AssertionError(
            "order-twelve cell-orbit census changed"
        )

    total_representative_ports = 0
    total_labelled_ports = 0
    zero_port_cells = 0
    port_count_histogram: Counter[int] = Counter()
    for index, record in enumerate(representatives):
        colouring = tuple(
            tuple(
                tuple(map(int, pair))
                for pair in matching
            )
            for matching in record["diagonal_matchings"]
        )
        normals = tuple(
            tuple(map(int, item))
            for item in record["normal_types"]
        )
        port_count = reciprocal_port_count(
            12, colouring, normals
        )
        record["reciprocal_port_realizations"] = port_count
        total_representative_ports += port_count
        total_labelled_ports += (
            port_count * int(record["orbit_size"])
        )
        port_count_histogram[port_count] += 1
        zero_port_cells += int(port_count == 0)
        print(
            "cell",
            index + 1,
            "/",
            len(representatives),
            "ports",
            port_count,
            "representative_total",
            total_representative_ports,
            "elapsed",
            round(time.perf_counter() - started, 1),
            flush=True,
        )

    payload = {
        "verified": True,
        "status": "complete_cell_orbit_and_port_count",
        "scope": (
            "complete order-twelve connected cubic, distinguished "
            "Kotzig, normal-type cell orbits and every simple reciprocal "
            "cubic port realization count; no amplitude test"
        ),
        "catalogue_source": str(args.catalogue_source),
        "catalogue_source_sha256": sha256(
            args.catalogue_source
        ),
        "catalogue_provenance": source[
            "catalogue_provenance"
        ],
        "connected_cubic_classes": len(rows),
        "labelled_kotzig_colourings": sum(
            int(record["labelled_kotzig_colourings"])
            for record in graph_records
        ),
        "labelled_type_cells": 2_688,
        "cell_orbits": len(representatives),
        "zero_port_cell_orbits": zero_port_cells,
        "representative_port_realizations": (
            total_representative_ports
        ),
        "labelled_cell_port_realizations": (
            total_labelled_ports
        ),
        "port_count_histogram": [
            {
                "port_realizations": key,
                "cell_orbits": value,
            }
            for key, value in sorted(
                port_count_histogram.items()
            )
        ],
        "graphs": graph_records,
        "cell_representatives": representatives,
        "amplitudes_tested": False,
        "order_twelve_branch_excluded": False,
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
