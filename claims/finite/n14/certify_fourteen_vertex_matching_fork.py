"""Certify a cancellation fork without scanning the 3^14 colour cube.

For a skeleton perfect matching Q, let U be its singleton edges.  Removing
one edge f = xz from U can leave a nonempty family S of perfect matchings,
while adding f creates exactly Q.  If every member of S pairs x with one
common full-edge neighbour, an exact adjacent-activation construction turns
this purely combinatorial fork into a cancellation-transport contradiction.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Sequence

from analyze_fourteen_vertex_full_direct_motifs import (
    FULL_EDGES,
    N,
    edge,
    perfect_matchings,
)

Edge = tuple[int, int]


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("perfect matching misses a vertex")


def adjacent_activation(
    target: frozenset[Edge],
    removed: Edge,
    changed_vertex: int,
    labels: dict[Edge, int],
    singleton_matchings: Sequence[Sequence[Edge]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    removed_colour = labels[removed]
    fixed_vertex = (
        removed[1] if removed[0] == changed_vertex else removed[0]
    )
    sparse_target = target - {removed}
    colours: list[int | None] = [None] * N
    for item in sparse_target:
        colour = labels[item]
        for vertex in item:
            if colours[vertex] not in (None, colour):
                raise AssertionError("target is not a matching")
            colours[vertex] = colour
    if colours[changed_vertex] is not None:
        raise AssertionError("removed edge is not disjoint from the target")
    if colours[fixed_vertex] is not None:
        raise AssertionError("removed edge is not disjoint from the target")
    colours[fixed_vertex] = removed_colour

    other_colours = [
        colour for colour in range(3) if colour != removed_colour
    ]
    uncoloured = {
        vertex for vertex, colour in enumerate(colours) if colour is None
    }
    adjacency = {vertex: [] for vertex in uncoloured}
    for colour in other_colours:
        for first, second in singleton_matchings[colour]:
            if first in uncoloured and second in uncoloured:
                adjacency[first].append(second)
                adjacency[second].append(first)
    for start in sorted(uncoloured):
        if colours[start] is not None:
            continue
        colours[start] = other_colours[0]
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            current = int(colours[vertex])
            next_colour = (
                other_colours[1]
                if current == other_colours[0]
                else other_colours[0]
            )
            for neighbour in adjacency[vertex]:
                if colours[neighbour] is None:
                    colours[neighbour] = next_colour
                    queue.append(neighbour)
                elif colours[neighbour] != next_colour:
                    raise AssertionError(
                        "two singleton factors should be bipartite"
                    )
    sparse = tuple(int(colour) for colour in colours)
    rich = list(sparse)
    rich[changed_vertex] = removed_colour
    return sparse, tuple(rich)


def active_singletons(
    colouring: Sequence[int], labels: dict[Edge, int]
) -> frozenset[Edge]:
    return frozenset(
        item
        for item, colour in labels.items()
        if colouring[item[0]] == colouring[item[1]] == colour
    )


def equation_index(colouring: Sequence[int]) -> int:
    return sum(
        int(colour) * (3**vertex)
        for vertex, colour in enumerate(colouring)
    )


def find_fork(
    matchings: Sequence[Sequence[Edge]],
    full_edges: set[Edge],
    labels: dict[Edge, int],
    singleton_matchings: Sequence[Sequence[Edge]],
) -> dict[str, object] | None:
    singleton_sets = [
        frozenset(item for item in matching if item in labels)
        for matching in matchings
    ]
    candidates: list[
        tuple[
            int,
            int,
            int,
            Edge,
            int,
            int,
            list[int],
            list[int],
            frozenset[Edge],
        ]
    ] = []
    for rich_matching_id, target in enumerate(singleton_sets):
        if (
            len(target) == N // 2
            and len({labels[item] for item in target}) == 1
        ):
            # The adjacent rich activation would be monochromatic and its
            # amplitude is prescribed to be one rather than zero.
            continue
        for removed in target:
            sparse_target = target - {removed}
            sparse_activity = [
                matching_id
                for matching_id, singleton_set in enumerate(singleton_sets)
                if singleton_set <= sparse_target
            ]
            if not sparse_activity:
                continue
            rich_activity = [
                matching_id
                for matching_id, singleton_set in enumerate(singleton_sets)
                if singleton_set <= target
            ]
            extras = set(rich_activity) - set(sparse_activity)
            if extras != {rich_matching_id}:
                continue
            for changed_vertex in removed:
                partners = {
                    partner_at(matchings[item], changed_vertex)
                    for item in sparse_activity
                }
                if len(partners) != 1:
                    continue
                partner = next(iter(partners))
                if edge(changed_vertex, partner) not in full_edges:
                    continue
                candidates.append(
                    (
                        len(sparse_activity),
                        len(target),
                        rich_matching_id,
                        removed,
                        changed_vertex,
                        partner,
                        sparse_activity,
                        rich_activity,
                        target,
                    )
                )
    if not candidates:
        return None
    (
        _,
        _,
        rich_matching_id,
        removed,
        changed_vertex,
        partner,
        sparse_activity,
        rich_activity,
        target,
    ) = min(candidates)
    sparse_colouring, rich_colouring = adjacent_activation(
        target,
        removed,
        changed_vertex,
        labels,
        singleton_matchings,
    )
    if active_singletons(sparse_colouring, labels) != target - {removed}:
        raise AssertionError("sparse activation construction failed")
    if active_singletons(rich_colouring, labels) != target:
        raise AssertionError("rich activation construction failed")
    return {
        "singleton_target": [list(item) for item in sorted(target)],
        "removed_singleton_edge": list(removed),
        "removed_singleton_colour": labels[removed],
        "changed_vertex": changed_vertex,
        "common_partner": partner,
        "common_full_edge": list(edge(changed_vertex, partner)),
        "sparse_equation_index": equation_index(sparse_colouring),
        "sparse_colouring": list(sparse_colouring),
        "sparse_activity": sparse_activity,
        "rich_equation_index": equation_index(rich_colouring),
        "rich_colouring": list(rich_colouring),
        "rich_activity": rich_activity,
        "extra_matching": rich_matching_id,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/fourteen_vertex_matching_fork.json"),
    )
    args = parser.parse_args()
    candidate = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in matching)
        for matching in candidate["best_singleton_matchings"]
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    full_edges = set(FULL_EDGES)
    matchings = perfect_matchings(full_edges | set(labels))
    certificate = find_fork(
        matchings,
        full_edges,
        labels,
        singleton_matchings,
    )
    payload = {
        "status": (
            "matching_fork_contradiction"
            if certificate is not None
            else "matching_fork_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "candidate": str(args.candidate),
        "full_cycle_type": [3, 4, 7],
        "skeleton_perfect_matchings": len(matchings),
        "certificate": certificate,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
