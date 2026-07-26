"""Exhaust the order-ten exact-degree-six Kotzig/port minimum layer.

This finite computation assumes the arbitrary-order reductions in
``THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md``:

* the selected monochromatic matchings form a distinguished Kotzig
  three-edge-colouring of a cubic diagonal graph D;
* the remaining three support edges at every vertex form a disjoint
  cubic graph K of reciprocal primary singleton ports;
* optional off-diagonal entries on D cannot contribute to a
  minimum-potential nonmonochromatic guaranteed colouring.

For every connected cubic graph on ten vertices, every distinguished
Kotzig colouring, every compatible normal-type assignment, and every
simple reciprocal port realization, the script enumerates the
guaranteed perfect matchings.  A minimum-potential mixed colouring with
one guaranteed matching is an immediate contradiction: its monomial is
nonzero, and the potential theorem excludes every optional-D monomial
from that coefficient.

This is a finite branch computation, not a proof of the global
Krenn--Gu conjecture.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import time
from pathlib import Path

from explore_eight_vertex_degree_six_kotzig_ports import (
    balanced_allowed_entries,
    decode_graph6,
    edge,
    kotzig_colourings,
    normal_types,
)

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
NormalType = tuple[int, int, int]
GuaranteedEdge = tuple[int, int, int, int, int, str]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def transition_potential(
    normal: NormalType, colour: int
) -> int:
    b0 = int(normal[0] == 2)
    b1 = int(normal[1] == 2)
    b2 = int(normal[2] == 1)
    return (
        1 - 2 * b2,
        2 * (b2 - b0),
        2 * (b0 + b1 - 1),
    )[colour]


def port_options(
    vertices: range,
    diagonal: set[Edge],
    normals: tuple[NormalType, ...],
) -> tuple[
    tuple[tuple[int, int], ...],
    tuple[tuple[int, ...], ...],
]:
    stubs = tuple(
        (vertex, colour)
        for vertex in vertices
        for colour in range(3)
    )
    stub_id = {stub: index for index, stub in enumerate(stubs)}
    options: list[tuple[int, ...]] = []
    for vertex, colour in stubs:
        other_colour = normals[vertex][colour]
        options.append(
            tuple(
                stub_id[other_vertex, other_colour]
                for other_vertex in vertices
                if (
                    other_vertex != vertex
                    and normals[other_vertex][other_colour] == colour
                    and edge(vertex, other_vertex) not in diagonal
                    and (
                        (
                            other_colour,
                            colour,
                        )
                        if vertex < other_vertex
                        else (
                            colour,
                            other_colour,
                        )
                    )
                    in balanced_allowed_entries(
                        normals[min(vertex, other_vertex)],
                        normals[max(vertex, other_vertex)],
                    )
                )
            )
        )
    return stubs, tuple(options)


def minimum_layer(
    vertices: range,
    diagonal_edges: tuple[GuaranteedEdge, ...],
    port_edges: tuple[GuaranteedEdge, ...],
) -> dict[str, object]:
    edges = diagonal_edges + port_edges
    adjacency: list[list[int]] = [[] for _ in vertices]
    for edge_id, (left, right, _a, _b, _weight, _kind) in enumerate(
        edges
    ):
        adjacency[left].append(edge_id)
        adjacency[right].append(edge_id)

    best_potential: int | None = None
    minimum_colourings: Counter[tuple[int, ...]] = Counter()
    perfect_matchings = 0
    nonmonochromatic_matchings = 0
    colours: list[int | None] = [None] * len(vertices)

    def visit(remaining: int, potential: int) -> None:
        nonlocal best_potential
        nonlocal perfect_matchings
        nonlocal nonmonochromatic_matchings
        if remaining == 0:
            perfect_matchings += 1
            colouring = tuple(int(colour) for colour in colours)
            if len(set(colouring)) == 1:
                return
            nonmonochromatic_matchings += 1
            if best_potential is None or potential < best_potential:
                best_potential = potential
                minimum_colourings.clear()
            if potential == best_potential:
                minimum_colourings[colouring] += 1
            return

        low_bit = remaining & -remaining
        left = low_bit.bit_length() - 1
        for edge_id in adjacency[left]:
            u, v, left_colour, right_colour, weight, _kind = edges[
                edge_id
            ]
            if u != left:
                u, v = v, u
                left_colour, right_colour = right_colour, left_colour
            if not (remaining & (1 << v)):
                continue
            colours[u] = left_colour
            colours[v] = right_colour
            visit(
                remaining ^ (1 << u) ^ (1 << v),
                potential + weight,
            )
            colours[u] = None
            colours[v] = None

    visit((1 << len(vertices)) - 1, 0)
    if best_potential is None:
        raise AssertionError(
            "Kotzig diagonal graph lost every mixed guaranteed matching"
        )
    if best_potential > 0:
        raise AssertionError(
            "minimum mixed potential exceeds the zero-potential D layer"
        )

    multiplicities = Counter(minimum_colourings.values())
    unique_colourings = sum(
        count
        for multiplicity, count in multiplicities.items()
        if multiplicity == 1
    )
    witness = next(
        (
            list(colouring)
            for colouring, count in minimum_colourings.items()
            if count == 1
        ),
        None,
    )
    return {
        "perfect_matchings": perfect_matchings,
        "nonmonochromatic_matchings": nonmonochromatic_matchings,
        "minimum_potential": best_potential,
        "minimum_colouring_multiplicity_histogram": {
            str(key): value
            for key, value in sorted(multiplicities.items())
        },
        "minimum_unique_colourings": unique_colourings,
        "unique_minimum_witness": witness,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6",
        type=Path,
        default=Path("tmp", "cub10.g6"),
    )
    parser.add_argument(
        "--theorem",
        type=Path,
        default=Path(
            "THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "ten_vertex_degree_six_kotzig_ports_explored.json",
        ),
    )
    parser.add_argument("--progress-every", type=int, default=25_000)
    args = parser.parse_args()
    started = time.perf_counter()

    rows = tuple(
        row.strip()
        for row in args.graph6.read_text(encoding="ascii").splitlines()
        if row.strip()
    )
    if len(rows) != 19:
        raise AssertionError(
            "connected order-ten cubic graph catalogue must have 19 rows"
        )

    vertices = range(10)
    graph_records: list[dict[str, object]] = []
    total_colourings = 0
    total_type_assignments = 0
    total_port_realizations = 0
    contradictions = 0
    total_guaranteed_matchings = 0
    total_mixed_guaranteed_matchings = 0
    minimum_potential_histogram: Counter[int] = Counter()
    minimum_multiplicity_histogram: Counter[
        tuple[tuple[int, int], ...]
    ] = Counter()
    survivor_records: list[dict[str, object]] = []

    for graph_index, graph6 in enumerate(rows):
        diagonal = set(decode_graph6(graph6))
        if (
            len(diagonal) != 15
            or any(
                sum(vertex in pair for pair in diagonal) != 3
                for vertex in vertices
            )
        ):
            raise AssertionError("catalogue row is not cubic")
        colourings = kotzig_colourings(vertices, diagonal)
        total_colourings += len(colourings)
        graph_port_realizations = 0
        graph_contradictions = 0

        for colouring_index, colouring in enumerate(colourings):
            diagonal_edges = tuple(
                (
                    pair[0],
                    pair[1],
                    colour,
                    colour,
                    0,
                    "D",
                )
                for colour, matching in enumerate(colouring)
                for pair in matching
            )
            assignments = normal_types(vertices, colouring)
            if len(assignments) != 8:
                raise AssertionError(
                    "Kotzig colouring lost its eight type assignments"
                )
            total_type_assignments += len(assignments)

            for type_index, normals in enumerate(assignments):
                stubs, options = port_options(
                    vertices, diagonal, normals
                )
                if any(not candidates for candidates in options):
                    continue
                remaining = set(range(len(stubs)))
                used_pairs: set[Edge] = set()
                chosen: list[GuaranteedEdge] = []

                def realize() -> None:
                    nonlocal graph_port_realizations
                    nonlocal graph_contradictions
                    nonlocal total_port_realizations
                    nonlocal contradictions
                    nonlocal total_guaranteed_matchings
                    nonlocal total_mixed_guaranteed_matchings

                    if not remaining:
                        total_port_realizations += 1
                        graph_port_realizations += 1
                        layer = minimum_layer(
                            vertices,
                            diagonal_edges,
                            tuple(chosen),
                        )
                        total_guaranteed_matchings += int(
                            layer["perfect_matchings"]
                        )
                        total_mixed_guaranteed_matchings += int(
                            layer["nonmonochromatic_matchings"]
                        )
                        minimum_potential_histogram[
                            int(layer["minimum_potential"])
                        ] += 1
                        multiplicity_key = tuple(
                            (int(key), int(value))
                            for key, value in dict(
                                layer[
                                    "minimum_colouring_multiplicity_histogram"
                                ]
                            ).items()
                        )
                        minimum_multiplicity_histogram[
                            multiplicity_key
                        ] += 1
                        if int(layer["minimum_unique_colourings"]) > 0:
                            contradictions += 1
                            graph_contradictions += 1
                        else:
                            survivor_records.append(
                                {
                                    "graph_index": graph_index,
                                    "colouring_index": colouring_index,
                                    "type_index": type_index,
                                    "diagonal_matchings": [
                                        [list(pair) for pair in matching]
                                        for matching in colouring
                                    ],
                                    "normal_types": [
                                        list(item) for item in normals
                                    ],
                                    "port_edges": [
                                        {
                                            "edge": [item[0], item[1]],
                                            "half_colours": [
                                                item[2],
                                                item[3],
                                            ],
                                            "potential": item[4],
                                        }
                                        for item in chosen
                                    ],
                                    "minimum_layer": layer,
                                }
                            )
                        if (
                            args.progress_every > 0
                            and total_port_realizations
                            % args.progress_every
                            == 0
                        ):
                            print(
                                "ports",
                                total_port_realizations,
                                "survivors",
                                len(survivor_records),
                                "elapsed",
                                round(time.perf_counter() - started, 1),
                                flush=True,
                            )
                        return

                    first = min(
                        remaining,
                        key=lambda stub: sum(
                            (
                                other in remaining
                                and edge(
                                    stubs[stub][0],
                                    stubs[other][0],
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
                            oriented_colours = (
                                right_colour,
                                left_colour,
                            )
                        else:
                            oriented_colours = (
                                left_colour,
                                right_colour,
                            )
                        potential = (
                            transition_potential(
                                normals[pair[0]],
                                oriented_colours[0],
                            )
                            + transition_potential(
                                normals[pair[1]],
                                oriented_colours[1],
                            )
                        )
                        chosen.append(
                            (
                                pair[0],
                                pair[1],
                                oriented_colours[0],
                                oriented_colours[1],
                                potential,
                                "K",
                            )
                        )
                        remaining.remove(first)
                        remaining.remove(second)
                        used_pairs.add(pair)
                        realize()
                        used_pairs.remove(pair)
                        remaining.add(second)
                        remaining.add(first)
                        chosen.pop()

                realize()

        graph_records.append(
            {
                "graph_index": graph_index,
                "graph6": graph6,
                "kotzig_colourings": len(colourings),
                "reciprocal_port_realizations": (
                    graph_port_realizations
                ),
                "unique_minimum_contradictions": (
                    graph_contradictions
                ),
            }
        )

    payload = {
        "verified": len(survivor_records) == 0,
        "status": "finite_combinatorial_exploration",
        "scope": (
            "order-ten exact-degree-six pairwise-disjoint cubic "
            "Kotzig diagonal branch with a disjoint reciprocal-primary-"
            "port cubic graph, tested on its minimum potential layer"
        ),
        "catalogue_provenance": "nauty geng -cq -d3 -D3 10",
        "graph6": str(args.graph6),
        "graph6_sha256": sha256(args.graph6),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "graph6_rows": len(rows),
        "graphs": graph_records,
        "labelled_kotzig_colourings": total_colourings,
        "normal_type_assignments": total_type_assignments,
        "reciprocal_port_realizations": total_port_realizations,
        "unique_minimum_contradictions": contradictions,
        "total_guaranteed_matchings": total_guaranteed_matchings,
        "total_nonmonochromatic_guaranteed_matchings": (
            total_mixed_guaranteed_matchings
        ),
        "minimum_potential_histogram": {
            str(key): value
            for key, value in sorted(
                minimum_potential_histogram.items()
            )
        },
        "minimum_colouring_multiplicity_histogram": [
            {
                "multiplicities": {
                    str(key): value for key, value in signature
                },
                "realizations": count,
            }
            for signature, count in sorted(
                minimum_multiplicity_histogram.items()
            )
        ],
        "survivors": len(survivor_records),
        "survivor_records": survivor_records,
        "finite_branch_excluded": len(survivor_records) == 0,
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
