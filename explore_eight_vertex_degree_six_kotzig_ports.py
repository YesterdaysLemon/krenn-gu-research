"""Explore the exact-degree-six Kotzig/reciprocal-port boundary at order eight.

This is a finite combinatorial scout, not a proof of the global conjecture.
It assumes the strongest residual branch currently left by the analytic
reductions:

* the diagonal graph D is cubic;
* the three selected monochromatic matchings partition D;
* every pair of those matchings is a Hamiltonian cycle;
* the three coordinate-primary singleton ports at each vertex use a
  disjoint cubic graph K.

At order eight, D union K is 6-regular, so the edges outside D split as K
and one unused perfect matching.  The script exhausts that finite boundary
over the connected cubic graph6 catalogue in ``tmp/cub08.g6``.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Iterable

from eight_vertex_degree4_support import decode_graph6

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
NormalType = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def perfect_matchings(vertices: Iterable[int], edges: set[Edge]) -> list[Matching]:
    remaining = tuple(sorted(vertices))

    def visit(active: tuple[int, ...]) -> list[Matching]:
        if not active:
            return [()]
        first = active[0]
        output: list[Matching] = []
        for index in range(1, len(active)):
            second = active[index]
            pair = edge(first, second)
            if pair not in edges:
                continue
            rest = active[1:index] + active[index + 1 :]
            for tail in visit(rest):
                output.append((pair, *tail))
        return output

    return visit(remaining)


def connected(vertices: range, edges: set[Edge]) -> bool:
    if not vertices:
        return True
    seen = {vertices[0]}
    stack = [vertices[0]]
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    while stack:
        current = stack.pop()
        for neighbour in adjacency[current]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return len(seen) == len(vertices)


def kotzig_colourings(vertices: range, diagonal: set[Edge]) -> list[tuple[Matching, ...]]:
    matchings = perfect_matchings(vertices, diagonal)
    output: set[tuple[Matching, ...]] = set()
    for first in matchings:
        first_set = set(first)
        remaining = diagonal - first_set
        for second in perfect_matchings(vertices, remaining):
            second_set = set(second)
            third_set = remaining - second_set
            if len(third_set) != len(vertices) // 2:
                continue
            if any(
                sum(vertex in pair for pair in third_set) != 1
                for vertex in vertices
            ):
                continue
            triple = (
                tuple(sorted(first_set)),
                tuple(sorted(second_set)),
                tuple(sorted(third_set)),
            )
            if all(
                connected(vertices, set(triple[a]) | set(triple[b]))
                for a, b in ((0, 1), (0, 2), (1, 2))
            ):
                output.add(triple)
    return sorted(output)


def flip_assignment(vertices: range, flip_edges: set[Edge]) -> tuple[int, ...]:
    adjacency = {vertex: [] for vertex in vertices}
    for u, v in flip_edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    values = [-1] * len(vertices)
    values[0] = 0
    stack = [0]
    while stack:
        current = stack.pop()
        for neighbour in adjacency[current]:
            expected = 1 - values[current]
            if values[neighbour] == -1:
                values[neighbour] = expected
                stack.append(neighbour)
            elif values[neighbour] != expected:
                raise AssertionError("flip graph is not bipartite")
    if any(value == -1 for value in values):
        raise AssertionError("flip graph is disconnected")
    return tuple(values)


def normal_types(
    vertices: range, colouring: tuple[Matching, ...]
) -> list[tuple[NormalType, ...]]:
    bit_bases = []
    for bit in range(3):
        flip_edges = set().union(
            *(set(colouring[colour]) for colour in range(3) if colour != bit)
        )
        bit_bases.append(flip_assignment(vertices, flip_edges))

    assignments = []
    for complements in itertools.product((0, 1), repeat=3):
        types = []
        for vertex in vertices:
            b0, b1, b2 = (
                bit_bases[bit][vertex] ^ complements[bit] for bit in range(3)
            )
            types.append(
                (
                    1 if b0 == 0 else 2,
                    0 if b1 == 0 else 2,
                    0 if b2 == 0 else 1,
                )
            )
        assignments.append(tuple(types))
    return assignments


def port_options(left: NormalType, right: NormalType) -> tuple[tuple[int, int], ...]:
    """Return admissible reciprocal target-colour pairs for an oriented edge.

    If the target tasks are ``(c,r)`` then the inherited half-colours on
    the oriented physical edge are ``(r,c)``.  Reciprocity alone is only
    necessary; the swapped physical unit must also survive the complete
    balanced-bridge table.
    """

    output = []
    for left_target in range(3):
        right_target = left[left_target]
        physical_unit = (right_target, left_target)
        if (
            right[right_target] == left_target
            and physical_unit in balanced_allowed_entries(left, right)
        ):
            output.append((left_target, right_target))
    return tuple(output)


def realize_ports(
    vertices: range, ports: set[Edge], types: tuple[NormalType, ...]
) -> tuple[dict[Edge, tuple[int, int]], ...]:
    options = {
        pair: port_options(types[pair[0]], types[pair[1]]) for pair in ports
    }
    if any(not candidates for candidates in options.values()):
        return ()

    ordered = sorted(ports, key=lambda pair: (len(options[pair]), pair))
    used = [0] * len(vertices)
    chosen: dict[Edge, tuple[int, int]] = {}
    solutions: list[dict[Edge, tuple[int, int]]] = []

    def visit(index: int) -> None:
        if index == len(ordered):
            if all(mask == 0b111 for mask in used):
                solutions.append(dict(sorted(chosen.items())))
            return
        u, v = ordered[index]
        for left_target, right_target in options[(u, v)]:
            left_bit = 1 << left_target
            right_bit = 1 << right_target
            if used[u] & left_bit or used[v] & right_bit:
                continue
            used[u] |= left_bit
            used[v] |= right_bit
            # Target tasks live at the opposite ends of the actual
            # singleton: target pair (c,r) gives half-colours (r,c).
            chosen[(u, v)] = (right_target, left_target)
            visit(index + 1)
            del chosen[(u, v)]
            used[u] ^= left_bit
            used[v] ^= right_bit

    visit(0)
    return tuple(solutions)


def balanced_allowed_entries(
    left: NormalType, right: NormalType
) -> set[tuple[int, int]]:
    return {
        (row, column)
        for row in range(3)
        for column in range(3)
        if all(
            (row, column) == (colour, colour)
            or row == left[colour]
            or column == right[colour]
            for colour in range(3)
        )
    }


def maximal_unique_mixed_contradiction(
    vertices: range,
    complete_matchings: list[Matching],
    colouring: tuple[Matching, ...],
    types: tuple[NormalType, ...],
    port_realization: dict[Edge, tuple[int, int]],
) -> dict[str, object] | None:
    support: dict[Edge, set[tuple[int, int]]] = {}
    guaranteed: dict[Edge, set[tuple[int, int]]] = {}
    for colour, matching in enumerate(colouring):
        for pair in matching:
            u, v = pair
            diagonal = {(colour, colour)}
            allowed_off_diagonal = {
                entry
                for entry in balanced_allowed_entries(types[u], types[v])
                if entry[0] != entry[1]
            }
            support[pair] = diagonal | allowed_off_diagonal
            guaranteed[pair] = diagonal
    for pair, targets in port_realization.items():
        singleton = {targets}
        support[pair] = singleton
        guaranteed[pair] = singleton

    for vertex_colours in itertools.product(range(3), repeat=len(vertices)):
        if len(set(vertex_colours)) == 1:
            continue
        compatible = []
        for matching in complete_matchings:
            if all(
                (vertex_colours[u], vertex_colours[v]) in support.get(pair, set())
                for pair in matching
                for u, v in (pair,)
            ):
                compatible.append(matching)
                if len(compatible) > 1:
                    break
        if len(compatible) != 1:
            continue
        matching = compatible[0]
        if all(
            (vertex_colours[u], vertex_colours[v])
            in guaranteed.get(pair, set())
            for pair in matching
            for u, v in (pair,)
        ):
            return {
                "vertex_colours": list(vertex_colours),
                "unique_matching": [list(pair) for pair in matching],
            }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--graph6",
        type=Path,
        default=Path("tmp", "cub08.g6"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp", "eight_vertex_degree_six_kotzig_ports_explored.json"
        ),
    )
    parser.add_argument(
        "--theorem",
        type=Path,
        default=Path("EIGHT_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md"),
    )
    args = parser.parse_args()
    started = time.perf_counter()

    rows = tuple(
        row.strip()
        for row in args.graph6.read_text(encoding="ascii").splitlines()
        if row.strip()
    )
    vertices = range(8)
    complete = {edge(u, v) for u in vertices for v in vertices if u < v}
    complete_matchings = perfect_matchings(vertices, complete)
    if len(complete_matchings) != 105:
        raise AssertionError("unexpected order-eight perfect-matching count")

    graph_records = []
    total_colourings = 0
    total_type_assignments = 0
    total_unused_matchings = 0
    total_port_tests = 0
    total_port_realizations = 0
    maximal_unique_contradictions = 0
    contradiction_records = []
    survivors = []

    for graph_index, graph6 in enumerate(rows):
        diagonal = set(decode_graph6(graph6))
        colourings = kotzig_colourings(vertices, diagonal)
        total_colourings += len(colourings)
        graph_record = {
            "graph_index": graph_index,
            "graph6": graph6,
            "kotzig_colourings": len(colourings),
        }
        graph_records.append(graph_record)

        complement = complete - diagonal
        unused_matchings = perfect_matchings(vertices, complement)
        for colouring_index, colouring in enumerate(colourings):
            assignments = normal_types(vertices, colouring)
            total_type_assignments += len(assignments)
            for type_index, types in enumerate(assignments):
                for unused_index, unused in enumerate(unused_matchings):
                    total_unused_matchings += 1
                    ports = complement - set(unused)
                    if any(
                        sum(vertex in pair for pair in ports) != 3
                        for vertex in vertices
                    ):
                        raise AssertionError("port graph is not cubic")
                    total_port_tests += 1
                    realizations = realize_ports(vertices, ports, types)
                    total_port_realizations += len(realizations)
                    for realization_index, realization in enumerate(realizations):
                        contradiction = maximal_unique_mixed_contradiction(
                            vertices,
                            complete_matchings,
                            colouring,
                            types,
                            realization,
                        )
                        if contradiction is not None:
                            maximal_unique_contradictions += 1
                            contradiction_records.append(
                                {
                                    "graph_index": graph_index,
                                    "colouring_index": colouring_index,
                                    "type_index": type_index,
                                    "unused_matching_index": unused_index,
                                    "port_realization_index": realization_index,
                                    **contradiction,
                                }
                            )
                            continue
                        survivors.append(
                            {
                                "graph_index": graph_index,
                                "colouring_index": colouring_index,
                                "type_index": type_index,
                                "diagonal_matchings": [
                                    [list(pair) for pair in matching]
                                    for matching in colouring
                                ],
                                "normal_types": [list(item) for item in types],
                                "unused_matching": [
                                    list(pair) for pair in unused
                                ],
                                "port_realization": [
                                    {
                                        "edge": list(pair),
                                        "half_colours": list(targets),
                                    }
                                    for pair, targets in realization.items()
                                ],
                            }
                        )

    payload = {
        "verified": True,
        "status": "finite_combinatorial_exploration",
        "scope": (
            "order-eight exact-degree-six pairwise-disjoint cubic diagonal "
            "Kotzig branch with a disjoint reciprocal-primary-port cubic graph"
        ),
        "graph6": str(args.graph6),
        "graph6_sha256": sha256(args.graph6),
        "theorem": str(args.theorem),
        "theorem_sha256": sha256(args.theorem),
        "graph6_rows": len(rows),
        "graphs": graph_records,
        "labelled_kotzig_colourings": total_colourings,
        "normal_type_assignments": total_type_assignments,
        "unused_matching_tests": total_unused_matchings,
        "reciprocal_port_tests": total_port_tests,
        "reciprocal_port_realizations": total_port_realizations,
        "maximal_support_unique_mixed_contradictions": (
            maximal_unique_contradictions
        ),
        "contradiction_records": contradiction_records,
        "survivors": len(survivors),
        "survivor_records": survivors,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    payload["output"] = str(args.output)
    payload["output_sha256"] = sha256(args.output)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
