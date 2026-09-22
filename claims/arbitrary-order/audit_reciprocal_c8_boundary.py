#!/usr/bin/env python3
"""Independent exact audit of the reciprocal all-background C8 control.

This standard-library replay reconstructs the eight-vertex scalar array from
the displayed permutation rules.  It uses a symmetric colored-state edge
table and a recursive coefficient evaluator, not the primary verifier's
precomputed physical matching list.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from pathlib import Path


COLORS = (0, 1, 2)
PORTS = tuple(range(4))
VERTICES = tuple(range(8))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
P = (0, 2, 3, 1)


State = tuple[int, int]


@dataclass(frozen=True, order=True)
class Edge:
    left: State
    right: State
    weight: int
    kind: str


def matching_mate(color: int) -> tuple[int, ...]:
    mate = [-1] * 4
    for u, v in MATCHINGS[color]:
        mate[u] = v
        mate[v] = u
    assert set(mate) == set(PORTS)
    return tuple(mate)


MATES = tuple(matching_mate(color) for color in COLORS)


def canonical_edge(
    u: int, color_u: int, v: int, color_v: int, weight: int, kind: str
) -> Edge:
    assert u != v
    left = (u, color_u)
    right = (v, color_v)
    if right < left:
        left, right = right, left
    return Edge(left, right, weight, kind)


def build_array() -> tuple[Edge, ...]:
    edges: dict[tuple[State, State], Edge] = {}

    def add(u: int, cu: int, v: int, cv: int, weight: int, kind: str) -> None:
        edge = canonical_edge(u, cu, v, cv, weight, kind)
        key = (edge.left, edge.right)
        assert key not in edges
        edges[key] = edge

    for shore in (0, 4):
        for color, matching in enumerate(MATCHINGS):
            for u, v in matching:
                add(shore + u, color, shore + v, color, 1, "protected")

    for background in COLORS:
        c8_source = (background + 1) % 3
        split_source = (background - 1) % 3
        for u, weight in enumerate((1, 1, 1, -1)):
            add(u, c8_source, 4 + P[u], background, weight, "crossing")

        split_map = tuple(P[MATES[split_source][u]] for u in PORTS)
        split_weights = [0] * 4
        for u, v in MATCHINGS[split_source]:
            split_weights[u] = 1
            split_weights[v] = -1
        for u in PORTS:
            add(
                u,
                split_source,
                4 + split_map[u],
                background,
                split_weights[u],
                "crossing",
            )

    return tuple(sorted(edges.values()))


EDGES = build_array()


def symmetric_weight_table(edges: tuple[Edge, ...]) -> dict[tuple[State, State], int]:
    table: dict[tuple[State, State], int] = {}
    for edge in edges:
        assert (edge.left, edge.right) not in table
        assert (edge.right, edge.left) not in table
        table[(edge.left, edge.right)] = edge.weight
        table[(edge.right, edge.left)] = edge.weight
    for (left, right), weight in table.items():
        assert table[(right, left)] == weight
    return table


WEIGHT = symmetric_weight_table(EDGES)


def coefficient(
    word: tuple[int, ...]
) -> tuple[int, int, tuple[tuple[int, int], ...] | None]:
    assert len(word) == 8

    @lru_cache(maxsize=None)
    def recurse(mask: int) -> tuple[int, int]:
        if mask == 0:
            return 1, 1
        low = mask & -mask
        u = low.bit_length() - 1
        value = 0
        count = 0
        remaining = mask ^ (1 << u)
        for v in VERTICES:
            if not (remaining & (1 << v)):
                continue
            weight = WEIGHT.get(((u, word[u]), (v, word[v])))
            if weight is None:
                continue
            child_value, child_count = recurse(remaining ^ (1 << v))
            value += weight * child_value
            count += child_count
        return value, count

    full_mask = (1 << len(VERTICES)) - 1
    value, count = recurse(full_mask)
    if count != 1:
        return value, count, None
    matching: list[tuple[int, int]] = []
    mask = full_mask
    while mask:
        low = mask & -mask
        u = low.bit_length() - 1
        remaining = mask ^ (1 << u)
        choices = []
        for v in VERTICES:
            if not (remaining & (1 << v)):
                continue
            if ((u, word[u]), (v, word[v])) not in WEIGHT:
                continue
            _, child_count = recurse(remaining ^ (1 << v))
            if child_count:
                choices.append(v)
        assert len(choices) == 1
        v = choices[0]
        matching.append((u, v))
        mask = remaining ^ (1 << v)
    return value, count, tuple(matching)


def verify_matching_action() -> dict[int, int]:
    action = {}
    for color, matching in enumerate(MATCHINGS):
        image = {frozenset((P[u], P[v])) for u, v in matching}
        targets = [
            target
            for target, target_matching in enumerate(MATCHINGS)
            if image == {frozenset(edge) for edge in target_matching}
        ]
        assert len(targets) == 1
        action[color] = targets[0]
    assert action == {0: 1, 1: 2, 2: 0}
    return action


def layer_edges(source_color: int, target_color: int) -> tuple[Edge, ...]:
    result = []
    for edge in EDGES:
        if edge.kind != "crossing":
            continue
        states = {edge.left, edge.right}
        if any(vertex < 4 and color == source_color for vertex, color in states) and any(
            vertex >= 4 and color == target_color for vertex, color in states
        ):
            result.append(edge)
    assert len(result) == 4
    return tuple(result)


def cycle_lengths_for_layer(
    foreground_shore: int, foreground_color: int, background: int
) -> tuple[int, ...]:
    local_vertices = tuple(range(4)) if foreground_shore == 0 else tuple(range(4, 8))
    exterior_vertices = tuple(range(4, 8)) if foreground_shore == 0 else tuple(range(4))
    adjacency = {vertex: set() for vertex in VERTICES}

    for u, v in MATCHINGS[foreground_color]:
        x, y = local_vertices[u], local_vertices[v]
        adjacency[x].add(y)
        adjacency[y].add(x)
    for u, v in MATCHINGS[background]:
        x, y = exterior_vertices[u], exterior_vertices[v]
        adjacency[x].add(y)
        adjacency[y].add(x)

    source_color, target_color = (
        (foreground_color, background)
        if foreground_shore == 0
        else (background, foreground_color)
    )
    for edge in layer_edges(source_color, target_color):
        u, v = edge.left[0], edge.right[0]
        adjacency[u].add(v)
        adjacency[v].add(u)
    assert set(map(len, adjacency.values())) == {2}

    unseen = set(VERTICES)
    lengths = []
    while unseen:
        start = min(unseen)
        stack = [start]
        component = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        lengths.append(len(component))
    return tuple(sorted(lengths))


def verify_array_ledger() -> dict[str, object]:
    protected = [edge for edge in EDGES if edge.kind == "protected"]
    crossing = [edge for edge in EDGES if edge.kind == "crossing"]
    assert len(protected) == 12
    assert len(crossing) == 24
    assert len(EDGES) == 36
    assert all(edge.left[0] // 4 == edge.right[0] // 4 for edge in protected)
    assert all(edge.left[0] // 4 != edge.right[0] // 4 for edge in crossing)
    assert all(edge.left[1] != edge.right[1] for edge in crossing)

    crossing_neighbors: dict[State, list[State]] = defaultdict(list)
    total_degree = Counter()
    for edge in EDGES:
        total_degree[edge.left] += 1
        total_degree[edge.right] += 1
        if edge.kind == "crossing":
            crossing_neighbors[edge.left].append(edge.right)
            crossing_neighbors[edge.right].append(edge.left)
    all_states = {(vertex, color) for vertex in VERTICES for color in COLORS}
    assert set(crossing_neighbors) == all_states
    assert {len(crossing_neighbors[state]) for state in all_states} == {2}
    assert set(total_degree.values()) == {3}
    for state in all_states:
        assert {neighbor[1] for neighbor in crossing_neighbors[state]} == set(COLORS) - {
            state[1]
        }

    layers = {}
    for source, target in product(COLORS, repeat=2):
        if source == target:
            continue
        entries = layer_edges(source, target)
        left_ports = {edge.left[0] for edge in entries}
        right_ports = {edge.right[0] for edge in entries}
        assert left_ports == set(range(4))
        assert right_ports == set(range(4, 8))
        layers[f"{source}->{target}"] = {
            "weights": [edge.weight for edge in sorted(entries, key=lambda item: item.left)],
            "product": product_value(edge.weight for edge in entries),
        }

    canonical = json.dumps(
        [
            {
                "left": edge.left,
                "right": edge.right,
                "weight": edge.weight,
                "kind": edge.kind,
            }
            for edge in EDGES
        ],
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return {
        "protected_entries": len(protected),
        "crossing_entries": len(crossing),
        "crossing_degree": 2,
        "total_state_degree": 3,
        "one_crossing_neighbor_per_foreign_color": True,
        "transpose_consistency": True,
        "layers": layers,
        "canonical_array_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def product_value(values) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def verify_cycle_and_split_layers() -> dict[str, object]:
    result = {}
    for shore, foreground, background in product((0, 1), COLORS, COLORS):
        if foreground == background:
            continue
        lengths = cycle_lengths_for_layer(shore, foreground, background)
        # On shore A, foreground=background+1 is the displayed C8.  Reversing
        # shores reverses this cyclic orientation.
        expected = (
            (8,)
            if (
                (shore == 0 and foreground == (background + 1) % 3)
                or (shore == 1 and foreground == (background - 1) % 3)
            )
            else (4, 4)
        )
        assert lengths == expected
        result[f"shore{shore}:foreground{foreground}|background{background}"] = list(
            lengths
        )
    return result


def verify_displayed_layer_formulas() -> dict[int, dict[str, object]]:
    result = {}
    for background in COLORS:
        c8_source = (background + 1) % 3
        c8_edges = layer_edges(c8_source, background)
        c8_by_port = {edge.left[0]: edge for edge in c8_edges}
        assert set(c8_by_port) == set(PORTS)
        c8_map = tuple(c8_by_port[u].right[0] - 4 for u in PORTS)
        c8_weights = tuple(c8_by_port[u].weight for u in PORTS)
        assert c8_map == P
        assert c8_weights == (1, 1, 1, -1)
        assert product_value(c8_weights) == -1

        split_source = (background - 1) % 3
        split_edges = layer_edges(split_source, background)
        split_by_port = {edge.left[0]: edge for edge in split_edges}
        assert set(split_by_port) == set(PORTS)
        split_map = tuple(split_by_port[u].right[0] - 4 for u in PORTS)
        split_weights = tuple(split_by_port[u].weight for u in PORTS)
        expected_map = tuple(P[MATES[split_source][u]] for u in PORTS)
        assert split_map == expected_map
        pair_products = tuple(
            split_weights[u] * split_weights[v]
            for u, v in MATCHINGS[split_source]
        )
        assert pair_products == (-1, -1)

        result[background] = {
            "c8_source": c8_source,
            "c8_map": c8_map,
            "c8_weights": c8_weights,
            "c8_product": -1,
            "split_source": split_source,
            "split_map": split_map,
            "split_weights": split_weights,
            "split_pair_products": pair_products,
        }
    return result


def paired_depth(word: tuple[int, ...], color: int) -> int:
    return sum(
        word[shore + u] != color and word[shore + v] != color
        for shore in (0, 4)
        for u, v in MATCHINGS[color]
    )


def verify_rows() -> dict[str, object]:
    slice_rows = 0
    distinct_slice_words = set()
    for nonuniform_shore, background, local_word in product(
        (0, 1), COLORS, product(COLORS, repeat=4)
    ):
        word = (
            tuple(local_word) + (background,) * 4
            if nonuniform_shore == 0
            else (background,) * 4 + tuple(local_word)
        )
        value, _, _ = coefficient(word)
        target = int(tuple(local_word) == (background,) * 4)
        assert value == target
        slice_rows += 1
        distinct_slice_words.add(word)
    assert slice_rows == 486
    assert len(distinct_slice_words) == 477

    macro_coefficients = {}
    for left_color, right_color in product(COLORS, repeat=2):
        word = (left_color,) * 4 + (right_color,) * 4
        value, _, _ = coefficient(word)
        target = int(left_color == right_color)
        assert value == target
        macro_coefficients[f"{left_color}|{right_color}"] = value

    failures = []
    low_depth_failures = []
    for word in product(COLORS, repeat=8):
        value, term_count, matching = coefficient(word)
        target = int(len(set(word)) == 1)
        if value == target:
            continue
        depths = tuple(paired_depth(word, color) for color in COLORS)
        record = {
            "word": word,
            "coefficient": value,
            "term_count": term_count,
            "q": depths,
            "unique_matching": matching,
        }
        failures.append(record)
        if min(depths) <= 1:
            low_depth_failures.append(record)
    assert len(failures) == 195
    assert len(low_depth_failures) == 171

    first = low_depth_failures[0]
    assert first == {
        "word": tuple(map(int, "00010022")),
        "coefficient": -1,
        "term_count": 1,
        "q": (1, 3, 2),
        "unique_matching": ((0, 1), (2, 7), (3, 6), (4, 5)),
    }
    first_word = first["word"]
    first_matching = first["unique_matching"]
    assert first_matching is not None
    factors = [
        WEIGHT[((u, first_word[u]), (v, first_word[v]))]
        for u, v in first_matching
    ]
    assert factors == [1, 1, -1, 1]
    assert product_value(factors) == -1

    return {
        "slice_row_specifications": slice_rows,
        "distinct_slice_words": len(distinct_slice_words),
        "macro_coefficients": macro_coefficients,
        "full_source_error_words": len(failures),
        "min_q_le_one_error_words": len(low_depth_failures),
        "first_q1_failure": {
            "word": "0001|0022",
            "coefficient": first["coefficient"],
            "term_count": first["term_count"],
            "q": first["q"],
            "matching": first_matching,
            "matching_factors": factors,
        },
    }


def verify() -> dict[str, object]:
    return {
        "status": "INDEPENDENT_RECIPROCAL_ALL_BACKGROUND_CONTROL_PASS",
        "matching_action": verify_matching_action(),
        "array_ledger": verify_array_ledger(),
        "displayed_layer_formulas": verify_displayed_layer_formulas(),
        "local_layer_cycle_types": verify_cycle_and_split_layers(),
        "row_replay": verify_rows(),
        "scope": (
            "exact finite obstruction to one-component/uniform-background row "
            "sufficiency; not a full source or degree-two counterexample"
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
