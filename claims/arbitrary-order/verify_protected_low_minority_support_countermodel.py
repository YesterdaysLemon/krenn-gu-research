#!/usr/bin/env python3
"""Exact finite verifier for the 18-K4 bipartite P1 support control.

This script is self-contained and uses only the Python standard library.  It
checks the literal K_(6,12) support, its component-constant macro cover, the
three whole-port DAGs, and the one-component state taxonomy used by the
separate analytic q<=1 proof.  It deliberately does not enumerate 3^72
physical words and does not claim a weighted full-source witness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Iterable


COLORS = (0, 1, 2)
CENTER = 0
LEAVES = (1, 2, 3)
LEFT_COMPONENTS = tuple(range(6))
RIGHT_COMPONENTS = tuple(range(6, 18))
COMPONENTS = LEFT_COMPONENTS + RIGHT_COMPONENTS
EXPECTED_LABELS = {
    (0, 1),
    (0, 2),
    (1, 0),
    (1, 2),
    (2, 0),
    (2, 1),
}

# Literal twelve-column greedy cover.  Each row is one right component and
# each position is one left component.  No generator or sibling checker is
# imported.
COLUMN_TEXT = (
    ("01", "02", "10", "12", "20", "21"),
    ("10", "12", "20", "21", "01", "02"),
    ("20", "21", "01", "02", "10", "12"),
    ("10", "01", "20", "02", "21", "12"),
    ("01", "10", "02", "20", "12", "21"),
    ("20", "02", "21", "10", "12", "01"),
    ("21", "20", "10", "01", "02", "12"),
    ("01", "21", "12", "20", "02", "10"),
    ("02", "10", "01", "12", "21", "20"),
    ("20", "12", "01", "10", "21", "02"),
    ("12", "10", "20", "01", "02", "21"),
    ("01", "10", "12", "02", "20", "21"),
)
COLUMNS = tuple(
    tuple((int(label[0]), int(label[1])) for label in column)
    for column in COLUMN_TEXT
)


Port = tuple[int, int]


@dataclass(frozen=True, order=True)
class Entry:
    """One supported scalar with colors attached to its ordered endpoints."""

    u: Port
    v: Port
    color_u: int
    color_v: int
    kind: str


def leaf(color: int) -> int:
    return color + 1


def protected_pairs(color: int) -> tuple[frozenset[int], frozenset[int]]:
    other = tuple(value for value in COLORS if value != color)
    return (
        frozenset((CENTER, leaf(color))),
        frozenset((leaf(other[0]), leaf(other[1]))),
    )


PROTECTED_EDGE_COLOR = {
    pair: color
    for color in COLORS
    for pair in protected_pairs(color)
}
assert len(PROTECTED_EDGE_COLOR) == 6


def partner(local_vertex: int, color: int) -> int:
    for pair in protected_pairs(color):
        if local_vertex in pair:
            return next(iter(pair - {local_vertex}))
    raise AssertionError("every local K4 vertex has a protected partner")


def protected_entries(component: int) -> list[Entry]:
    entries: list[Entry] = []
    for color in COLORS:
        for pair in protected_pairs(color):
            x, y = sorted(pair)
            entries.append(
                Entry((component, x), (component, y), color, color, "protected")
            )
    return entries


def gadget_entries(
    left_component: int,
    right_component: int,
    left_color: int,
    right_color: int,
) -> tuple[Entry, Entry]:
    assert left_color != right_color
    return (
        Entry(
            (left_component, CENTER),
            (right_component, CENTER),
            left_color,
            right_color,
            "cross_center",
        ),
        Entry(
            (left_component, leaf(left_color)),
            (right_component, leaf(right_color)),
            left_color,
            right_color,
            "cross_leaf",
        ),
    )


def build_main_support() -> tuple[Entry, ...]:
    entries = [entry for component in COMPONENTS for entry in protected_entries(component)]
    for column_index, column in enumerate(COLUMNS):
        right_component = RIGHT_COMPONENTS[column_index]
        for left_component, (left_color, right_color) in zip(
            LEFT_COMPONENTS, column, strict=True
        ):
            entries.extend(
                gadget_entries(
                    left_component, right_component, left_color, right_color
                )
            )
    return tuple(entries)


def entry_support_key(entry: Entry) -> tuple[Port, Port, int, int]:
    return entry.u, entry.v, entry.color_u, entry.color_v


def verify_literal_construction(entries: tuple[Entry, ...]) -> dict[str, object]:
    protected = tuple(entry for entry in entries if entry.kind == "protected")
    crossing = tuple(entry for entry in entries if entry.kind != "protected")
    assert len(entries) == 252
    assert len(protected) == 108 == 18 * 6
    assert len(crossing) == 144 == 72 * 2
    assert len({entry_support_key(entry) for entry in entries}) == len(entries)

    for component in COMPONENTS:
        local = [
            entry
            for entry in protected
            if entry.u[0] == component and entry.v[0] == component
        ]
        assert len(local) == 6
        observed = {
            (frozenset((entry.u[1], entry.v[1])), entry.color_u, entry.color_v)
            for entry in local
        }
        expected = {
            (pair, color, color)
            for color in COLORS
            for pair in protected_pairs(color)
        }
        assert observed == expected

    by_component_pair: dict[tuple[int, int], list[Entry]] = defaultdict(list)
    for entry in crossing:
        left, right = entry.u[0], entry.v[0]
        assert left in LEFT_COMPONENTS
        assert right in RIGHT_COMPONENTS
        by_component_pair[(left, right)].append(entry)

    assert set(by_component_pair) == set(product(LEFT_COMPONENTS, RIGHT_COMPONENTS))
    assert len(by_component_pair) == 72
    labels: dict[tuple[int, int], tuple[int, int]] = {}
    literal_macro_matchings = 0
    for pair, pair_entries in by_component_pair.items():
        assert len(pair_entries) == 2
        label_set = {(entry.color_u, entry.color_v) for entry in pair_entries}
        assert len(label_set) == 1
        label = next(iter(label_set))
        assert label in EXPECTED_LABELS
        labels[pair] = label
        left, right = pair
        expected_ports = {
            ((left, CENTER), (right, CENTER)),
            ((left, leaf(label[0])), (right, leaf(label[1]))),
        }
        assert {(entry.u, entry.v) for entry in pair_entries} == expected_ports

        # Both gadget factors plus the protected complementary leaf edge at
        # each endpoint are a literal perfect matching on these two K4s.  Its
        # local words are constant in the gadget endpoint colors.
        chosen = list(pair_entries)
        for component, color in ((left, label[0]), (right, label[1])):
            x, y = sorted(protected_pairs(color)[1])
            protected_match = [
                entry
                for entry in protected
                if (entry.u, entry.v, entry.color_u, entry.color_v)
                == ((component, x), (component, y), color, color)
            ]
            assert len(protected_match) == 1
            chosen.extend(protected_match)
        used: dict[Port, int] = {}
        for entry in chosen:
            assert entry.u not in used and entry.v not in used
            used[entry.u] = entry.color_u
            used[entry.v] = entry.color_v
        assert set(used) == {
            (component, local)
            for component in pair
            for local in range(4)
        }
        assert {used[(left, local)] for local in range(4)} == {label[0]}
        assert {used[(right, local)] for local in range(4)} == {label[1]}
        literal_macro_matchings += 1

    for column_index, column in enumerate(COLUMNS):
        right = RIGHT_COMPONENTS[column_index]
        assert {labels[(left, right)] for left in LEFT_COMPONENTS} == EXPECTED_LABELS
        assert tuple(labels[(left, right)] for left in LEFT_COMPONENTS) == column

    # The literal component graph is K_(6,12), hence is simple and bipartite.
    component_adjacency = {component: set() for component in COMPONENTS}
    for left, right in by_component_pair:
        component_adjacency[left].add(right)
        component_adjacency[right].add(left)
    assert all(len(component_adjacency[left]) == 12 for left in LEFT_COMPONENTS)
    assert all(len(component_adjacency[right]) == 6 for right in RIGHT_COMPONENTS)
    assert all(
        not (component_adjacency[u] & component_adjacency[v])
        for u, v in combinations(COMPONENTS, 2)
        if v in component_adjacency[u]
    )

    return {
        "components": len(COMPONENTS),
        "left_components": len(LEFT_COMPONENTS),
        "right_components": len(RIGHT_COMPONENTS),
        "component_edges": len(by_component_pair),
        "protected_entries": len(protected),
        "crossing_entries": len(crossing),
        "total_entries": len(entries),
        "single_label_component_pairs": len(labels),
        "literal_macro_matchings_checked": literal_macro_matchings,
        "component_graph": "K_(6,12)",
        "bipartite": True,
        "triangle_free": True,
    }


def physical_digraph(
    entries: Iterable[Entry], background: int
) -> set[tuple[Port, Port]]:
    arcs: set[tuple[Port, Port]] = set()
    for entry in entries:
        if entry.color_v == background and entry.color_u != background:
            arcs.add(
                (
                    entry.u,
                    (entry.v[0], partner(entry.v[1], background)),
                )
            )
        if entry.color_u == background and entry.color_v != background:
            arcs.add(
                (
                    entry.v,
                    (entry.u[0], partner(entry.u[1], background)),
                )
            )
    return arcs


def dag_longest_path(vertices: tuple[Port, ...], arcs: set[tuple[Port, Port]]) -> int:
    outgoing = {vertex: set() for vertex in vertices}
    indegree = {vertex: 0 for vertex in vertices}
    for source, target in arcs:
        if target not in outgoing[source]:
            outgoing[source].add(target)
            indegree[target] += 1
    ready = deque(vertex for vertex in vertices if indegree[vertex] == 0)
    distance = {vertex: 0 for vertex in vertices}
    removed = 0
    while ready:
        source = ready.popleft()
        removed += 1
        for target in outgoing[source]:
            distance[target] = max(distance[target], distance[source] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    assert removed == len(vertices)
    return max(distance.values())


def verify_dags(entries: tuple[Entry, ...]) -> dict[int, dict[str, object]]:
    vertices = tuple((component, local) for component in COMPONENTS for local in range(4))
    result: dict[int, dict[str, object]] = {}
    for background in COLORS:
        arcs = physical_digraph(entries, background)

        def layer(port: Port) -> int:
            local = port[1]
            if local == CENTER:
                return 1
            if local == leaf(background):
                return 2
            return 0

        assert all(layer(source) < layer(target) for source, target in arcs)
        longest_path_edges = dag_longest_path(vertices, arcs)
        assert longest_path_edges == 2
        layer_histogram = Counter(layer(vertex) for vertex in vertices)
        assert layer_histogram == Counter({0: 36, 1: 18, 2: 18})
        assert len(arcs) == 96
        result[background] = {
            "arc_count": len(arcs),
            "layer_histogram": dict(sorted(layer_histogram.items())),
            "maximum_path_edges": longest_path_edges,
            "acyclic": True,
        }
    return result


def blocked_colors(
    column: tuple[tuple[int, int], ...], left_word: tuple[int, ...]
) -> frozenset[int]:
    return frozenset(
        right_color
        for left_color, (label_left, right_color) in zip(
            left_word, column, strict=True
        )
        if left_color == label_left
    )


def verify_macro_cover() -> dict[str, object]:
    assert len(COLUMNS) == 12
    assert len(set(COLUMNS)) == len(COLUMNS)
    assert all(len(column) == 6 and set(column) == EXPECTED_LABELS for column in COLUMNS)

    nonconstant_words: list[tuple[int, ...]] = []
    witness_counts = [0] * len(COLUMNS)
    for left_word in product(COLORS, repeat=6):
        blocks = tuple(blocked_colors(column, left_word) for column in COLUMNS)
        if len(set(left_word)) == 1:
            color = left_word[0]
            assert all(block == set(COLORS) - {color} for block in blocks)
            # Therefore every right component has exactly the same sole
            # gadget-avoiding color, proving constant forcing without a
            # 3^12 enumeration of right assignments.
            assert all(set(COLORS) - block == {color} for block in blocks)
        else:
            nonconstant_words.append(left_word)
            witnesses = [index for index, block in enumerate(blocks) if block == set(COLORS)]
            assert witnesses
            for index in witnesses:
                witness_counts[index] += 1

    assert len(nonconstant_words) == 726

    exclusive_counts: list[int] = []
    for selected_index, selected in enumerate(COLUMNS):
        count = 0
        for left_word in nonconstant_words:
            if blocked_colors(selected, left_word) != set(COLORS):
                continue
            if all(
                other_index == selected_index
                or blocked_colors(other, left_word) != set(COLORS)
                for other_index, other in enumerate(COLUMNS)
            ):
                count += 1
        exclusive_counts.append(count)
    assert exclusive_counts == [17, 40, 29, 29, 14, 26, 22, 15, 13, 12, 7, 2]

    cover_literal = "\n".join(" ".join(column) for column in COLUMN_TEXT).encode()
    return {
        "left_words_checked": 3**6,
        "constant_left_words": 3,
        "nonconstant_left_words": len(nonconstant_words),
        "covered_nonconstant_left_words": len(nonconstant_words),
        "constant_forcing": True,
        "column_witness_counts": witness_counts,
        "exclusive_witness_counts": exclusive_counts,
        "cover_literal_sha256": hashlib.sha256(cover_literal).hexdigest(),
    }


def q_value(word: tuple[int, ...], background: int) -> int:
    return sum(
        all(word[vertex] != background for vertex in pair)
        for pair in protected_pairs(background)
    )


def complete_minority_pairs(
    word: tuple[int, ...], background: int
) -> tuple[frozenset[int], ...]:
    return tuple(
        pair
        for pair in protected_pairs(background)
        if all(word[vertex] != background for vertex in pair)
    )


def local_states() -> list[dict[str, object]]:
    states: list[dict[str, object]] = []
    all_vertices = frozenset(range(4))
    for crossing_count in (0, 2, 4):
        for crossed_tuple in combinations(range(4), crossing_count):
            crossed = frozenset(crossed_tuple)
            internal = all_vertices - crossed
            if len(internal) == 4:
                internal_colors: tuple[int | None, ...] = COLORS
            elif len(internal) == 2 and internal in PROTECTED_EDGE_COLOR:
                internal_colors = (PROTECTED_EDGE_COLOR[internal],)
            elif not internal:
                internal_colors = (None,)
            else:
                continue

            center_colors: tuple[int | None, ...] = (
                COLORS if CENTER in crossed else (None,)
            )
            for internal_color, center_color in product(internal_colors, center_colors):
                word: list[int | None] = [None] * 4
                if internal_color is not None:
                    for vertex in internal:
                        word[vertex] = internal_color
                for vertex in crossed:
                    word[vertex] = center_color if vertex == CENTER else vertex - 1
                assert all(color is not None for color in word)
                literal_word = tuple(int(color) for color in word)
                if crossing_count == 0:
                    kind = "uniform"
                elif crossing_count == 2 and CENTER in crossed:
                    kind = "AB"
                elif crossing_count == 2:
                    kind = "BB"
                else:
                    kind = "degree4"
                states.append(
                    {
                        "kind": kind,
                        "crossed": tuple(sorted(crossed)),
                        "internal_color": internal_color,
                        "center_color": center_color,
                        "word": literal_word,
                        "q": tuple(q_value(literal_word, color) for color in COLORS),
                    }
                )
    return states


def verify_local_taxonomy() -> dict[str, object]:
    states = local_states()
    kind_histogram = Counter(state["kind"] for state in states)
    assert len(states) == 18
    assert kind_histogram == Counter(
        {"uniform": 3, "AB": 9, "BB": 3, "degree4": 3}
    )

    by_background: dict[int, dict[str, object]] = {}
    for background in COLORS:
        q_histogram = Counter(state["q"][background] for state in states)
        assert q_histogram == Counter({0: 4, 1: 8, 2: 6})
        q0 = [state for state in states if state["q"][background] == 0]
        q1 = [state for state in states if state["q"][background] == 1]
        assert all(
            (
                state["kind"] == "uniform"
                and state["word"] == (background,) * 4
            )
            or (
                state["kind"] == "AB"
                and state["word"][1:] == (background,) * 3
            )
            for state in q0
        )
        q1_kinds = Counter(state["kind"] for state in q1)
        assert q1_kinds == Counter({"AB": 2, "BB": 3, "degree4": 3})
        assert all(
            state["word"][0] == background
            and len(set(state["word"][1:])) == 1
            and state["word"][1] != background
            for state in q1
            if state["kind"] == "AB"
        )
        expected_root = protected_pairs(background)[1]
        for state in q1:
            assert complete_minority_pairs(state["word"], background) == (
                expected_root,
            )
            assert protected_pairs(background)[0] not in complete_minority_pairs(
                state["word"], background
            )
        by_background[background] = {
            "q_histogram": dict(sorted(q_histogram.items())),
            "q0_states": len(q0),
            "q1_states": len(q1),
            "q1_by_kind": dict(q1_kinds),
            "unique_q1_minority_pair": sorted(expected_root),
        }

    return {
        "state_count": len(states),
        "kind_histogram": dict(kind_histogram),
        "by_background": by_background,
    }


def find_entry(
    entries: Iterable[Entry],
    u: Port,
    v: Port,
    color_u: int,
    color_v: int,
) -> Entry:
    matches = [
        entry
        for entry in entries
        if (entry.u, entry.v, entry.color_u, entry.color_v)
        == (u, v, color_u, color_v)
    ]
    assert len(matches) == 1
    return matches[0]


def matching_word(
    matching: Iterable[Entry], component_count: int
) -> tuple[tuple[int, int, int, int], ...]:
    colors: dict[Port, int] = {}
    for entry in matching:
        assert entry.u not in colors and entry.v not in colors
        colors[entry.u] = entry.color_u
        colors[entry.v] = entry.color_v
    expected_ports = {
        (component, local)
        for component in range(component_count)
        for local in range(4)
    }
    assert set(colors) == expected_ports
    return tuple(
        tuple(colors[(component, local)] for local in range(4))
        for component in range(component_count)
    )


def total_q(word: tuple[tuple[int, ...], ...], background: int) -> int:
    return sum(q_value(component_word, background) for component_word in word)


def verify_sharp_mutations() -> dict[str, object]:
    # Remove triangle-freeness while retaining one label per component pair.
    triangle_entries = [
        entry for component in range(3) for entry in protected_entries(component)
    ]
    triangle_entries.extend(gadget_entries(0, 1, 1, 0))
    triangle_entries.extend(gadget_entries(0, 2, 2, 0))
    triangle_entries.extend(gadget_entries(1, 2, 1, 2))
    triangle_matching = (
        find_entry(triangle_entries, (0, 0), (0, 1), 0, 0),
        find_entry(triangle_entries, (1, 2), (1, 3), 0, 0),
        find_entry(triangle_entries, (2, 2), (2, 3), 0, 0),
        find_entry(triangle_entries, (0, 2), (1, 1), 1, 0),
        find_entry(triangle_entries, (0, 3), (2, 1), 2, 0),
        find_entry(triangle_entries, (1, 0), (2, 0), 1, 2),
    )
    triangle_word = matching_word(triangle_matching, 3)
    assert triangle_word == ((0, 0, 1, 2), (1, 0, 0, 0), (2, 0, 0, 0))
    assert total_q(triangle_word, 0) == 1

    # Remove the one-label condition while retaining a triangle-free component
    # graph: two labels on the same component pair support the AB q1 root.
    second_label_entries = [
        entry for component in range(2) for entry in protected_entries(component)
    ]
    second_label_entries.extend(gadget_entries(0, 1, 1, 0))
    second_label_entries.extend(gadget_entries(0, 1, 0, 2))
    second_label_matching = (
        find_entry(second_label_entries, (0, 1), (0, 3), 1, 1),
        find_entry(second_label_entries, (1, 2), (1, 3), 0, 0),
        find_entry(second_label_entries, (0, 2), (1, 1), 1, 0),
        find_entry(second_label_entries, (0, 0), (1, 0), 0, 2),
    )
    second_label_word = matching_word(second_label_matching, 2)
    assert second_label_word == ((0, 1, 1, 1), (2, 0, 0, 0))
    assert total_q(second_label_word, 0) == 1

    return {
        "triangle_mutation": {
            "components": 3,
            "component_edges": 3,
            "one_label_per_pair": True,
            "triangle_free": False,
            "background": 0,
            "supported_word": [list(part) for part in triangle_word],
            "q": total_q(triangle_word, 0),
        },
        "second_label_mutation": {
            "components": 2,
            "component_edges": 1,
            "labels_on_component_pair": 2,
            "triangle_free": True,
            "one_label_per_pair": False,
            "background": 0,
            "supported_word": [list(part) for part in second_label_word],
            "q": total_q(second_label_word, 0),
        },
    }


def verify() -> dict[str, object]:
    entries = build_main_support()
    receipt = {
        "status": "P1_BIPARTITE_18K4_FINITE_REPLAY_PASSED",
        "scope": (
            "finite support construction, macro CSP, physical DAGs, local taxonomy, "
            "and sharp hypothesis mutations; global q<=1 absence remains the "
            "separate analytic proof"
        ),
        "construction": verify_literal_construction(entries),
        "dags": verify_dags(entries),
        "macro_cover": verify_macro_cover(),
        "local_taxonomy": verify_local_taxonomy(),
        "sharp_mutations": verify_sharp_mutations(),
    }
    canonical_entries = json.dumps(
        [asdict(entry) for entry in entries],
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    receipt["construction_sha256"] = hashlib.sha256(canonical_entries).hexdigest()
    receipt["limitations"] = [
        "does not enumerate 3^72 physical words",
        "does not replace the analytic all-order q<=1 proof",
        "does not assert a weighted full-source witness",
        "does not resolve the Krenn-Gu conjecture",
    ]
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional JSON receipt path")
    args = parser.parse_args()
    receipt = verify()
    rendered = json.dumps(receipt, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8", newline="\n")
    print(rendered)


if __name__ == "__main__":
    main()
