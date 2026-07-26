"""Independent audit of the order-twelve Kotzig/type cell quotient."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json
from pathlib import Path

import networkx as nx

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Normal = tuple[int, int, int]
Cell = tuple[tuple[Matching, ...], tuple[Normal, ...]]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pair(left: int, right: int) -> Edge:
    return (left, right) if left < right else (right, left)


def decode_graph6(row: str) -> tuple[int, set[Edge]]:
    graph = nx.from_graph6_bytes(row.encode("ascii"))
    return graph.number_of_nodes(), {
        pair(int(left), int(right)) for left, right in graph.edges()
    }


def matchings(
    active: tuple[int, ...], graph_edges: set[Edge]
) -> tuple[Matching, ...]:
    if not active:
        return ((),)
    left = active[0]
    output = []
    for position, right in enumerate(active[1:], start=1):
        edge = pair(left, right)
        if edge not in graph_edges:
            continue
        remaining = active[1:position] + active[position + 1 :]
        for tail in matchings(remaining, graph_edges):
            output.append((edge, *tail))
    return tuple(output)


def hamiltonian(order: int, graph_edges: set[Edge]) -> bool:
    if len(graph_edges) != order:
        return False
    degrees = [0] * order
    adjacency = [[] for _ in range(order)]
    for left, right in graph_edges:
        degrees[left] += 1
        degrees[right] += 1
        adjacency[left].append(right)
        adjacency[right].append(left)
    if any(degree != 2 for degree in degrees):
        return False
    seen = {0}
    stack = [0]
    while stack:
        for other in adjacency[stack.pop()]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen) == order


def kotzig_cells(order: int, graph_edges: set[Edge]) -> tuple[
    tuple[Matching, ...], ...
]:
    all_matchings = matchings(tuple(range(order)), graph_edges)
    output = set()
    for first in all_matchings:
        first_set = set(first)
        for second in all_matchings:
            second_set = set(second)
            if first_set & second_set:
                continue
            third_set = graph_edges - first_set - second_set
            if len(third_set) != order // 2:
                continue
            if any(
                sum(vertex in edge for edge in third_set) != 1
                for vertex in range(order)
            ):
                continue
            triple = (
                tuple(sorted(first_set)),
                tuple(sorted(second_set)),
                tuple(sorted(third_set)),
            )
            if all(
                hamiltonian(
                    order, set(triple[left]) | set(triple[right])
                )
                for left, right in ((0, 1), (0, 2), (1, 2))
            ):
                output.add(triple)
    return tuple(sorted(output))


def bipartition(
    order: int, graph_edges: set[Edge]
) -> tuple[int, ...]:
    adjacency = [[] for _ in range(order)]
    for left, right in graph_edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    values = [-1] * order
    values[0] = 0
    stack = [0]
    while stack:
        vertex = stack.pop()
        for other in adjacency[vertex]:
            expected = 1 - values[vertex]
            if values[other] == -1:
                values[other] = expected
                stack.append(other)
            elif values[other] != expected:
                raise AssertionError("flip graph is not bipartite")
    if any(value == -1 for value in values):
        raise AssertionError("flip graph is disconnected")
    return tuple(values)


def normal_assignments(
    order: int, colouring: tuple[Matching, ...]
) -> tuple[tuple[Normal, ...], ...]:
    bases = tuple(
        bipartition(
            order,
            set().union(
                *(
                    set(colouring[colour])
                    for colour in range(3)
                    if colour != bit
                )
            ),
        )
        for bit in range(3)
    )
    output = []
    for complements in itertools.product((0, 1), repeat=3):
        rows = []
        for vertex in range(order):
            b0, b1, b2 = tuple(
                bases[bit][vertex] ^ complements[bit]
                for bit in range(3)
            )
            rows.append(
                (
                    1 if b0 == 0 else 2,
                    0 if b1 == 0 else 2,
                    0 if b2 == 0 else 1,
                )
            )
        output.append(tuple(rows))
    return tuple(output)


def automorphisms(order: int, graph_edges: set[Edge]) -> tuple[
    tuple[int, ...], ...
]:
    graph = nx.Graph()
    graph.add_nodes_from(range(order))
    graph.add_edges_from(graph_edges)
    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
    return tuple(
        tuple(int(mapping[vertex]) for vertex in range(order))
        for mapping in matcher.isomorphisms_iter()
    )


def transform(
    cell: Cell,
    vertex_map: tuple[int, ...],
    colour_map: tuple[int, int, int],
) -> Cell:
    colouring, normals = cell
    transformed_matchings: list[list[Edge]] = [[], [], []]
    for colour, matching in enumerate(colouring):
        image_colour = colour_map[colour]
        transformed_matchings[image_colour].extend(
            pair(vertex_map[left], vertex_map[right])
            for left, right in matching
        )
    transformed_normals: list[Normal | None] = [None] * len(normals)
    for vertex, normal in enumerate(normals):
        row = [-1, -1, -1]
        for colour in range(3):
            row[colour_map[colour]] = colour_map[normal[colour]]
        transformed_normals[vertex_map[vertex]] = tuple(row)
    if any(normal is None for normal in transformed_normals):
        raise AssertionError("normal transformation lost a vertex")
    return (
        tuple(
            tuple(sorted(matching))
            for matching in transformed_matchings
        ),
        tuple(
            normal
            for normal in transformed_normals
            if normal is not None
        ),
    )


def canonical(
    cell: Cell,
    graph_automorphisms: tuple[tuple[int, ...], ...],
) -> Cell:
    return min(
        transform(cell, vertex_map, colour_map)
        for vertex_map in graph_automorphisms
        for colour_map in itertools.permutations(range(3))
    )


def main() -> None:
    scout_path = Path(
        "tmp", "twelve_vertex_six_potential_cells_scouted.json"
    )
    primary_path = Path(
        "tmp", "twelve_vertex_port_cell_orbits_counted.json"
    )
    scout = json.loads(scout_path.read_text(encoding="utf-8"))
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    rows = tuple(scout["catalogue_graph6"])
    if len(rows) != 85:
        raise AssertionError("catalogue size changed")

    graph_audits = []
    total_colourings = 0
    total_cells = 0
    total_orbits = 0
    primary_graphs = {
        int(record["graph_index"]): record
        for record in primary["graphs"]
    }
    primary_representatives: dict[int, list[dict[str, object]]] = (
        defaultdict(list)
    )
    for record in primary["cell_representatives"]:
        primary_representatives[int(record["graph_index"])].append(
            record
        )

    for graph_index, graph6 in enumerate(rows):
        order, graph_edges = decode_graph6(graph6)
        if order != 12 or len(graph_edges) != 18:
            raise AssertionError("cubic catalogue row changed")
        colourings = kotzig_cells(order, graph_edges)
        automorphism_rows = automorphisms(order, graph_edges)
        cells = tuple(
            (colouring, normals)
            for colouring in colourings
            for normals in normal_assignments(order, colouring)
        )
        by_key = Counter(
            canonical(cell, automorphism_rows) for cell in cells
        )
        expected_graph = primary_graphs[graph_index]
        expected_representatives = primary_representatives[graph_index]
        if (
            len(colourings)
            != int(expected_graph["labelled_kotzig_colourings"])
            or len(cells) != int(expected_graph["labelled_type_cells"])
            or len(by_key) != int(expected_graph["cell_orbits"])
            or len(automorphism_rows)
            != int(expected_graph["automorphisms"])
            or sorted(by_key.values())
            != sorted(
                int(record["orbit_size"])
                for record in expected_representatives
            )
        ):
            raise AssertionError(
                f"independent cell quotient disagrees on graph {graph_index}"
            )
        group_size = 6 * len(automorphism_rows)
        expected_stabilizers = sorted(
            group_size // orbit_size for orbit_size in by_key.values()
        )
        if expected_stabilizers != sorted(
            int(record["stabilizer_size"])
            for record in expected_representatives
        ):
            raise AssertionError(
                f"independent stabilizers disagree on graph {graph_index}"
            )
        total_colourings += len(colourings)
        total_cells += len(cells)
        total_orbits += len(by_key)
        graph_audits.append(
            {
                "graph_index": graph_index,
                "automorphisms": len(automorphism_rows),
                "labelled_kotzig_colourings": len(colourings),
                "labelled_type_cells": len(cells),
                "cell_orbits": len(by_key),
            }
        )

    if (
        total_colourings != 336
        or total_cells != 2_688
        or total_orbits != 154
    ):
        raise AssertionError("independent global cell quotient changed")
    payload = {
        "verified": True,
        "status": "independent_order_twelve_cell_orbit_audit",
        "scope": (
            "independent graph6 decoding, perfect-matching and Kotzig "
            "enumeration, bit propagation, NetworkX automorphisms, and "
            "cell orbit/stabilizer reconstruction"
        ),
        "scout": str(scout_path),
        "scout_sha256": sha256(scout_path),
        "primary": str(primary_path),
        "primary_sha256": sha256(primary_path),
        "connected_cubic_classes": len(rows),
        "labelled_kotzig_colourings": total_colourings,
        "labelled_type_cells": total_cells,
        "cell_orbits": total_orbits,
        "graph_audits": graph_audits,
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "twelve_vertex_port_cell_orbits_audited.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": True,
                "connected_cubic_classes": len(rows),
                "labelled_kotzig_colourings": total_colourings,
                "labelled_type_cells": total_cells,
                "cell_orbits": total_orbits,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
