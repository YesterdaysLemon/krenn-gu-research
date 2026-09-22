#!/usr/bin/env python3
"""Independent physical reconstruction of the partial-pair/orphan control."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import product
from pathlib import Path


MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
    2: ((0, 3), (1, 2)),
}


@dataclass(frozen=True)
class Edge:
    u: int
    cu: int
    v: int
    cv: int
    weight: int
    name: str
    kind: str


def canonical(
    u: int, cu: int, v: int, cv: int, weight: int, name: str, kind: str
) -> Edge:
    if (v, cv) < (u, cu):
        u, cu, v, cv = v, cv, u, cu
    return Edge(u, cu, v, cv, weight, name, kind)


def build_array() -> tuple[Edge, ...]:
    edges: dict[tuple[int, int, int, int], Edge] = {}

    def add(edge: Edge) -> None:
        key = (edge.u, edge.cu, edge.v, edge.cv)
        assert key not in edges
        edges[key] = edge

    for base in (0, 4, 8):
        for color, pairs in MATCHINGS.items():
            for left, right in pairs:
                add(
                    canonical(
                        base + left,
                        color,
                        base + right,
                        color,
                        1,
                        f"P{base // 4}:{color}:{left}{right}",
                        "protected",
                    )
                )

    layers = (
        (
            0,
            2,
            (4, 7, 5, 8, 9, 10, 11, 0, 1, 2, 3, 6),
            (1, -1, 1, 1) + (1,) * 8,
        ),
        (
            1,
            2,
            (5, 4, 6, 8, 9, 10, 11, 0, 1, 2, 3, 7),
            (1, 1, -1, 1) + (1,) * 8,
        ),
        (
            0,
            1,
            (4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 2, 3),
            (1,) * 12,
        ),
    )
    for color_left, color_right, mapping, weights in layers:
        assert sorted(mapping) == list(range(12))
        for source, (target, weight) in enumerate(zip(mapping, weights)):
            assert source // 4 != target // 4
            add(
                canonical(
                    source,
                    color_left,
                    target,
                    color_right,
                    weight,
                    f"X{color_left}{color_right}:{source}>{target}",
                    "crossing",
                )
            )

    return tuple(edges.values())


def compatible_matchings(
    word: tuple[int, ...], edges: tuple[Edge, ...]
) -> tuple[tuple[int, tuple[str, ...]], ...]:
    """Enumerate recursively from the word-specific compatibility graph."""
    incident: dict[int, list[Edge]] = {vertex: [] for vertex in range(12)}
    for edge in edges:
        if word[edge.u] == edge.cu and word[edge.v] == edge.cv:
            incident[edge.u].append(edge)
            incident[edge.v].append(edge)

    terms: list[tuple[int, tuple[str, ...]]] = []

    def visit(remaining: frozenset[int], weight: int, names: tuple[str, ...]) -> None:
        if not remaining:
            terms.append((weight, tuple(sorted(names))))
            return
        u = min(
            remaining,
            key=lambda vertex: sum(
                (edge.v if edge.u == vertex else edge.u) in remaining
                for edge in incident[vertex]
            ),
        )
        for edge in incident[u]:
            v = edge.v if edge.u == u else edge.u
            if v in remaining:
                visit(
                    remaining - {u, v},
                    weight * edge.weight,
                    names + (edge.name,),
                )

    visit(frozenset(range(12)), 1, ())
    return tuple(sorted(terms))


def verify_degree(edges: tuple[Edge, ...]) -> None:
    crossings = tuple(edge for edge in edges if edge.kind == "crossing")
    assert len(crossings) == 36
    neighbors: dict[tuple[int, int], list[tuple[int, int]]] = {
        (vertex, color): [] for vertex in range(12) for color in range(3)
    }
    for edge in crossings:
        assert edge.u // 4 != edge.v // 4
        assert edge.cu != edge.cv
        neighbors[(edge.u, edge.cu)].append((edge.v, edge.cv))
        neighbors[(edge.v, edge.cv)].append((edge.u, edge.cu))
    for (vertex, color), values in neighbors.items():
        del vertex
        assert len(values) == 2
        assert {neighbor_color for _, neighbor_color in values} == {0, 1, 2} - {color}


def verify_orphans(edges: tuple[Edge, ...]) -> dict[str, object]:
    by_name = {edge.name: edge for edge in edges}
    pair_02 = (by_name["X02:0>4"], by_name["X02:1>7"])
    orphan_02 = (by_name["X02:2>5"], by_name["X02:3>8"])
    pair_12 = (by_name["X12:0>5"], by_name["X12:2>6"])
    orphan_12 = (by_name["X12:1>4"], by_name["X12:3>8"])

    def targets(lanes: tuple[Edge, Edge], source_component: int = 0) -> tuple[int, int]:
        result = []
        for edge in lanes:
            result.append(edge.v if edge.u // 4 == source_component else edge.u)
        return tuple(result)

    def is_m2_resource(vertices: tuple[int, int]) -> bool:
        u, v = vertices
        return u // 4 == v // 4 and (u % 4, v % 4) in {
            tuple(sorted(pair)) for pair in MATCHINGS[2]
        }

    targets_02 = targets(pair_02)
    targets_12 = targets(pair_12)
    orphans_02 = targets(orphan_02)
    orphans_12 = targets(orphan_12)
    assert is_m2_resource(tuple(sorted(targets_02)))
    assert is_m2_resource(tuple(sorted(targets_12)))
    assert pair_02[0].weight * pair_02[1].weight == -1
    assert pair_12[0].weight * pair_12[1].weight == -1
    assert orphans_02[0] // 4 != orphans_02[1] // 4
    assert orphans_12[0] // 4 != orphans_12[1] // 4
    assert not is_m2_resource(tuple(sorted(orphans_02)))
    assert not is_m2_resource(tuple(sorted(orphans_12)))
    return {
        "layer_02_resource_targets": list(sorted(targets_02)),
        "layer_02_orphan_targets": list(sorted(orphans_02)),
        "layer_12_resource_targets": list(sorted(targets_12)),
        "layer_12_orphan_targets": list(sorted(orphans_12)),
    }


def verify() -> dict[str, object]:
    edges = build_array()
    verify_degree(edges)
    orphan_receipt = verify_orphans(edges)

    supported_rows: dict[str, list[int]] = {}
    for local in product(range(3), repeat=4):
        word = tuple(local) + (2,) * 8
        terms = compatible_matchings(word, edges)
        value = sum(weight for weight, _ in terms)
        assert value == int(local == (2, 2, 2, 2)), (local, value, terms)
        if terms:
            supported_rows["".join(map(str, local))] = [weight for weight, _ in terms]
    assert supported_rows == {"0000": [-1, 1], "1111": [-1, 1], "2222": [1]}

    macro_word = (0,) * 4 + (1,) * 4 + (2,) * 4
    macro_terms = compatible_matchings(macro_word, edges)
    macro_value = sum(weight for weight, _ in macro_terms)
    assert macro_value == 3

    return {
        "status": "INDEPENDENT_PARTIAL_PAIR_ORPHAN_CONTROL_PASS",
        "physical_vertices": 12,
        "protected_entries": sum(edge.kind == "protected" for edge in edges),
        "crossing_entries": sum(edge.kind == "crossing" for edge in edges),
        "crossing_degree_per_state": 2,
        "foreign_colors_per_state": 2,
        "local_rows_checked": 81,
        "local_supported_term_weights": supported_rows,
        "orphan_structure": orphan_receipt,
        "macro_word": "0000|1111|2222",
        "macro_coefficient": macro_value,
        "macro_term_count": len(macro_terms),
        "macro_terms": [
            {"weight": weight, "edges": list(names)} for weight, names in macro_terms
        ],
        "scope": (
            "exact local tensor countercontrol only; not a macro source and not a full source"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(verify(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)


if __name__ == "__main__":
    main()
