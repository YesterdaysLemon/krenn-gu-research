#!/usr/bin/env python3
"""Independent literal audit of the four-K4 reciprocal orphan control."""

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
VECTORS = {0: 1, 1: 2, 2: 3}
LAYERS = {
    (0, 1): (7, 5, 8, 4, 0, 2, 3, 12, 1, 13, 14, 15, 6, 9, 10, 11),
    (0, 2): (4, 7, 5, 8, 2, 12, 0, 3, 1, 13, 14, 15, 6, 9, 10, 11),
    (1, 2): (5, 4, 6, 8, 0, 12, 3, 1, 2, 13, 14, 15, 7, 9, 10, 11),
}
NEGATIVE_SOURCES = {(0, 1): {1, 5}, (0, 2): {1, 7}, (1, 2): {2, 6}}
FIRST_TEMPLATE = ((1, 0), (1, 3), (1, 1), (2, 0))
SECOND_TEMPLATE = ((1, 1), (1, 0), (1, 2), (2, 0))


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
    entries: dict[tuple[int, int, int, int], Edge] = {}

    def add(edge: Edge) -> None:
        key = (edge.u, edge.cu, edge.v, edge.cv)
        assert key not in entries
        entries[key] = edge

    for base in range(0, 16, 4):
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

    for (first, second), mapping in LAYERS.items():
        assert sorted(mapping) == list(range(16))
        for source, target in enumerate(mapping):
            assert source // 4 != target // 4
            weight = -1 if source in NEGATIVE_SOURCES[(first, second)] else 1
            add(
                canonical(
                    source,
                    first,
                    target,
                    second,
                    weight,
                    f"X{first}{second}:{source}>{target}",
                    "crossing",
                )
            )
    return tuple(entries.values())


def inverse_map(mapping: tuple[int, ...]) -> tuple[int, ...]:
    inverse = [0] * len(mapping)
    for source, target in enumerate(mapping):
        inverse[target] = source
    return tuple(inverse)


def crossing_neighbor(vertex: int, source_color: int, target_color: int) -> tuple[int, int]:
    pair = tuple(sorted((source_color, target_color)))
    mapping = LAYERS[pair]
    if source_color < target_color:
        underlying_source = vertex
        neighbor = mapping[vertex]
    else:
        neighbor = inverse_map(mapping)[vertex]
        underlying_source = neighbor
    weight = -1 if underlying_source in NEGATIVE_SOURCES[pair] else 1
    return neighbor, weight


def is_resource(vertices: tuple[int, int], color: int) -> bool:
    left, right = vertices
    return (
        left // 4 == right // 4
        and tuple(sorted((left % 4, right % 4)))
        in {tuple(sorted(pair)) for pair in MATCHINGS[color]}
    )


def audit_six_incidents() -> list[dict[str, object]]:
    receipt = []
    for background in range(3):
        first_foreground = (background + 1) % 3
        second_foreground = (background + 2) % 3
        change = {
            0: 0,
            VECTORS[first_foreground]: 1,
            VECTORS[second_foreground]: 2,
            VECTORS[background]: 3,
        }
        assert len(change) == 4
        for foreground, expected in (
            (first_foreground, FIRST_TEMPLATE),
            (second_foreground, SECOND_TEMPLATE),
        ):
            target_by_canonical_source: list[tuple[int, int] | None] = [None] * 4
            targets_by_source: dict[int, tuple[int, int]] = {}
            for source_port in range(4):
                target, weight = crossing_neighbor(source_port, foreground, background)
                target_by_canonical_source[change[source_port]] = (
                    target // 4,
                    change[target % 4],
                )
                targets_by_source[source_port] = (target, weight)
            assert tuple(target_by_canonical_source) == expected

            paired = []
            orphan = []
            for source_pair in MATCHINGS[foreground]:
                targets = tuple(targets_by_source[port][0] for port in source_pair)
                if is_resource(targets, background):
                    paired.append((source_pair, targets))
                else:
                    orphan.append((source_pair, targets))
            assert len(paired) == 1 and len(orphan) == 1
            paired_source, paired_targets = paired[0]
            orphan_source, orphan_targets = orphan[0]
            paired_product = 1
            for port in paired_source:
                paired_product *= targets_by_source[port][1]
            assert paired_product == -1
            assert orphan_targets[0] // 4 != orphan_targets[1] // 4
            assert not is_resource(orphan_targets, background)
            receipt.append(
                {
                    "foreground": foreground,
                    "background": background,
                    "paired_source_ports": list(paired_source),
                    "paired_target_vertices": list(paired_targets),
                    "paired_product": paired_product,
                    "orphan_source_ports": list(orphan_source),
                    "orphan_target_vertices": list(orphan_targets),
                    "canonical_target_table": [list(item) for item in expected],
                }
            )
    assert len(receipt) == 6
    return receipt


def compatible_matchings(
    word: tuple[int, ...], edges: tuple[Edge, ...]
) -> tuple[tuple[int, tuple[str, ...]], ...]:
    incident: dict[int, list[Edge]] = {vertex: [] for vertex in range(16)}
    for edge in edges:
        if word[edge.u] == edge.cu and word[edge.v] == edge.cv:
            incident[edge.u].append(edge)
            incident[edge.v].append(edge)

    terms: list[tuple[int, tuple[str, ...]]] = []

    def visit(remaining: frozenset[int], weight: int, names: tuple[str, ...]) -> None:
        if not remaining:
            terms.append((weight, tuple(sorted(names))))
            return
        vertex = min(
            remaining,
            key=lambda u: sum(
                (edge.v if edge.u == u else edge.u) in remaining
                for edge in incident[u]
            ),
        )
        for edge in incident[vertex]:
            neighbor = edge.v if edge.u == vertex else edge.u
            if neighbor in remaining:
                visit(
                    remaining - {vertex, neighbor},
                    weight * edge.weight,
                    names + (edge.name,),
                )

    visit(frozenset(range(16)), 1, ())
    return tuple(sorted(terms))


def verify_degree(edges: tuple[Edge, ...]) -> None:
    crossings = tuple(edge for edge in edges if edge.kind == "crossing")
    assert len(crossings) == 48
    neighbors = {(vertex, color): [] for vertex in range(16) for color in range(3)}
    for edge in crossings:
        assert edge.u // 4 != edge.v // 4
        neighbors[(edge.u, edge.cu)].append((edge.v, edge.cv))
        neighbors[(edge.v, edge.cv)].append((edge.u, edge.cu))
    for (_, color), values in neighbors.items():
        assert len(values) == 2
        assert {neighbor_color for _, neighbor_color in values} == {0, 1, 2} - {color}


def verify() -> dict[str, object]:
    edges = build_array()
    verify_degree(edges)
    incident_receipt = audit_six_incidents()

    row_count = 0
    supported_by_background: dict[str, dict[str, list[int]]] = {}
    for background in range(3):
        supported: dict[str, list[int]] = {}
        for local in product(range(3), repeat=4):
            word = tuple(local) + (background,) * 12
            terms = compatible_matchings(word, edges)
            value = sum(weight for weight, _ in terms)
            assert value == int(local == (background,) * 4), (
                background,
                local,
                value,
                terms,
            )
            if terms:
                supported["".join(map(str, local))] = [weight for weight, _ in terms]
            row_count += 1
        expected = {
            "0000": [1] if background == 0 else [-1, 1],
            "1111": [1] if background == 1 else [-1, 1],
            "2222": [1] if background == 2 else [-1, 1],
        }
        assert supported == expected
        supported_by_background[str(background)] = supported
    assert row_count == 243

    failure_word = (0,) * 4 + (1, 2, 0, 0) + (0,) * 8
    failure_terms = compatible_matchings(failure_word, edges)
    assert len(failure_terms) == 1
    assert failure_terms[0][0] == 1

    return {
        "status": "INDEPENDENT_PARTIAL_ORPHAN_RECIPROCAL_PASS",
        "physical_vertices": 16,
        "protected_entries": sum(edge.kind == "protected" for edge in edges),
        "crossing_entries": sum(edge.kind == "crossing" for edge in edges),
        "state_crossing_degree": 2,
        "ordered_A_incidents_checked": len(incident_receipt),
        "incident_receipt": incident_receipt,
        "local_uniform_background_rows_checked": row_count,
        "supported_rows_by_background": supported_by_background,
        "outside_failure_word": "0000|1200|0000|0000",
        "outside_failure_coefficient": 1,
        "outside_failure_term_count": len(failure_terms),
        "outside_failure_edges": list(failure_terms[0][1]),
        "scope": (
            "local mechanism countercontrol only; not a full source; "
            "macro-source status not tested"
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
