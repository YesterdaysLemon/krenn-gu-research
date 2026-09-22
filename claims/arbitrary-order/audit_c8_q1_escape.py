#!/usr/bin/env python3
"""Independent finite replay of the same-component C8/split q1 escape.

The all-order proof is the matching-sector argument in RESULT.md.  This
checker builds literal two-K4 color-regular supports for every affine lift,
every orientation of the M_a edge, and every b--a layer permutation.  It
uses symbolic nonzero edge names and directly enumerates compatible physical
perfect matchings.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path


PORTS = tuple(range(4))
COLORS = (0, 1, 2)
A_VECTOR, B_VECTOR, C_VECTOR = 1, 2, 3
COLOR_VECTOR = (A_VECTOR, B_VECTOR, C_VECTOR)


State = tuple[int, int]


@dataclass(frozen=True, order=True)
class Edge:
    left: State
    right: State
    symbol: str
    kind: str
    layer: str


def matching(vector: int) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset((u, u ^ vector))
        for u in PORTS
    )


MATCHING = {vector: matching(vector) for vector in (1, 2, 3)}


def matching_action(port_map: tuple[int, ...], vector: int) -> int:
    image = frozenset(
        frozenset((port_map[u], port_map[v]))
        for edge in MATCHING[vector]
        for u, v in (tuple(edge),)
    )
    targets = [target for target, target_edges in MATCHING.items() if image == target_edges]
    assert len(targets) == 1
    return targets[0]


def affine_lifts() -> tuple[tuple[int, ...], ...]:
    result = []
    for port_map in permutations(PORTS):
        action = tuple(
            matching_action(port_map, vector)
            for vector in (A_VECTOR, B_VECTOR, C_VECTOR)
        )
        if action == (B_VECTOR, C_VECTOR, A_VECTOR):
            result.append(tuple(port_map))
    assert len(result) == 4
    return tuple(result)


def canonical_edge(
    left: State, right: State, symbol: str, kind: str, layer: str
) -> Edge:
    assert left[0] != right[0]
    if right < left:
        left, right = right, left
    return Edge(left, right, symbol, kind, layer)


def build_support(
    pi: tuple[int, ...], ba_map: tuple[int, ...]
) -> tuple[Edge, ...]:
    edges: dict[tuple[State, State], Edge] = {}

    def add(
        left: State, right: State, symbol: str, kind: str, layer: str
    ) -> None:
        edge = canonical_edge(left, right, symbol, kind, layer)
        key = (edge.left, edge.right)
        assert key not in edges
        edges[key] = edge

    # Arbitrary nonzero protected weights are represented by distinct symbols.
    for shore in (0, 4):
        for color, vector in enumerate(COLOR_VECTOR):
            for pair in MATCHING[vector]:
                u, v = sorted(pair)
                add(
                    (shore + u, color),
                    (shore + v, color),
                    f"p_{shore}_{color}_{u}{v}",
                    "protected",
                    f"p{color}",
                )

    sigma = tuple(pi[u ^ B_VECTOR] for u in PORTS)
    maps = {
        (0, 2): pi,                     # the a--c C8
        (1, 2): sigma,                  # its opposite b--c split
        (0, 1): (0, 1, 2, 3),          # disabled in the q1 word
        (1, 0): ba_map,                 # the only alternative sector
        (2, 0): (1, 0, 3, 2),          # disabled: no c state on A
        (2, 1): (2, 3, 0, 1),          # disabled: no c state on A
    }
    for (left_color, right_color), port_map in maps.items():
        assert set(port_map) == set(PORTS)
        for u, target in enumerate(port_map):
            add(
                (u, left_color),
                (4 + target, right_color),
                f"x_{left_color}{right_color}_{u}",
                "crossing",
                f"{left_color}->{right_color}",
            )
    return tuple(sorted(edges.values()))


def verify_color_regular(edges: tuple[Edge, ...]) -> None:
    neighbors = {(vertex, color): [] for vertex in range(8) for color in COLORS}
    for edge in edges:
        if edge.kind != "crossing":
            continue
        neighbors[edge.left].append(edge.right)
        neighbors[edge.right].append(edge.left)
    assert {len(value) for value in neighbors.values()} == {2}
    for state, values in neighbors.items():
        assert {neighbor[1] for neighbor in values} == set(COLORS) - {state[1]}


def compatible_matchings(
    edges: tuple[Edge, ...], word: tuple[int, ...]
) -> tuple[tuple[tuple[tuple[int, int], ...], tuple[str, ...], tuple[str, ...]], ...]:
    by_vertex = {vertex: [] for vertex in range(8)}
    for edge in edges:
        u, color_u = edge.left
        v, color_v = edge.right
        if word[u] != color_u or word[v] != color_v:
            continue
        by_vertex[u].append(edge)
        by_vertex[v].append(edge)

    terms = []

    def recurse(remaining: frozenset[int], chosen: tuple[Edge, ...]) -> None:
        if not remaining:
            physical = tuple(
                sorted(tuple(sorted((edge.left[0], edge.right[0]))) for edge in chosen)
            )
            terms.append(
                (
                    physical,
                    tuple(edge.symbol for edge in chosen),
                    tuple(edge.layer for edge in chosen),
                )
            )
            return
        u = min(remaining)
        for edge in by_vertex[u]:
            v = edge.right[0] if edge.left[0] == u else edge.left[0]
            if v not in remaining:
                continue
            recurse(remaining - {u, v}, chosen + (edge,))

    recurse(frozenset(range(8)), ())
    return tuple(terms)


def q_value(word: tuple[int, ...], background: int) -> int:
    vector = COLOR_VECTOR[background]
    return sum(
        word[shore + u] != background and word[shore + v] != background
        for shore in (0, 4)
        for pair in MATCHING[vector]
        for u, v in (tuple(pair),)
    )


def verify() -> dict[str, object]:
    lifts = affine_lifts()
    cases = 0
    alternative_lane_compatible = 0
    direct_matching_shapes = set()
    direct_layer_shapes = set()

    for pi in lifts:
        sigma = tuple(pi[u ^ B_VECTOR] for u in PORTS)
        inverse_pi = {target: source for source, target in enumerate(pi)}
        for u in PORTS:
            v = u ^ A_VECTOR
            x = pi[u]
            y = sigma[v]
            assert x ^ y == A_VECTOR
            w = inverse_pi[y]
            assert w == (v ^ B_VECTOR)
            assert w not in (u, v)
            stranded = w ^ A_VECTOR
            assert stranded not in (u, v, w)

            for ba_map in permutations(PORTS):
                edges = build_support(pi, tuple(ba_map))
                verify_color_regular(edges)
                word = [0] * 8
                word[v] = 1
                word[4 + x] = 2
                word[4 + y] = 2
                literal_word = tuple(word)
                assert q_value(literal_word, 0) == 1

                terms = compatible_matchings(edges, literal_word)
                assert len(terms) == 1
                physical, symbols, layers = terms[0]
                expected_physical = tuple(
                    sorted(
                        (
                            tuple(sorted((u, 4 + x))),
                            tuple(sorted((v, 4 + y))),
                            tuple(sorted(tuple(set(PORTS) - {u, v}))),
                            tuple(
                                sorted(
                                    (4 + port for port in set(PORTS) - {x, y})
                                )
                            ),
                        )
                    )
                )
                assert physical == expected_physical
                assert "0->2" in layers and "1->2" in layers
                assert len([layer for layer in layers if layer.startswith("p")]) == 2
                direct_matching_shapes.add(physical)
                direct_layer_shapes.add(tuple(sorted(layers)))

                # If the b--a lane is compatible, the only non-direct local
                # sector would pair v through it and y back to w.  Direct
                # enumeration has already proved that sector cannot complete.
                z = ba_map[v]
                if z not in (x, y):
                    alternative_lane_compatible += 1
                    assert any(
                        edge.layer == "1->0"
                        and {edge.left[0], edge.right[0]} == {v, 4 + z}
                        for edge in edges
                    )
                    assert not any("1->0" in term_layers for _, _, term_layers in terms)
                cases += 1

    assert cases == 4 * 4 * 24 == 384
    assert alternative_lane_compatible == 192
    return {
        "status": "INDEPENDENT_SAME_COMPONENT_C8_REPAIR_Q1_PASS",
        "affine_lifts": len(lifts),
        "oriented_Ma_edges_per_lift": 4,
        "ba_layer_permutations_per_orientation": 24,
        "literal_supports_checked": cases,
        "supports_with_compatible_alternative_ba_lane": alternative_lane_compatible,
        "matching_count_in_every_case": 1,
        "distinct_direct_physical_matchings": len(direct_matching_shapes),
        "direct_layer_shapes": [list(shape) for shape in sorted(direct_layer_shapes)],
        "scope": (
            "finite port/support replay of the all-order matching-sector proof; "
            "not the proof and not a full-source construction"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional JSON receipt path")
    args = parser.parse_args()
    rendered = json.dumps(verify(), indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)


if __name__ == "__main__":
    main()
