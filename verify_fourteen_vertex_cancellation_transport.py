"""Independently verify an order-14 cancellation-transport certificate."""

from __future__ import annotations

import argparse
import json
from functools import lru_cache
from pathlib import Path
from typing import Sequence

from analyze_fourteen_vertex_full_direct_motifs import (
    FULL_EDGES,
    N,
    edge,
)

Edge = tuple[int, int]


def enumerate_perfect_matchings(edges: set[Edge]) -> list[tuple[Edge, ...]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)

    @lru_cache(maxsize=None)
    def recurse(remaining: int) -> tuple[tuple[Edge, ...], ...]:
        if remaining == 0:
            return ((),)
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        output: list[tuple[Edge, ...]] = []
        candidates = remaining & ~((1 << (first + 1)) - 1)
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            if second not in adjacency[first]:
                continue
            rest = remaining ^ first_bit ^ second_bit
            for suffix in recurse(rest):
                output.append(((first, second),) + suffix)
        return tuple(output)

    return sorted(recurse((1 << N) - 1))


def decode_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def active_matching_ids(
    matchings: Sequence[Sequence[Edge]],
    full_edges: set[Edge],
    labels: dict[Edge, int],
    colouring: Sequence[int],
) -> list[int]:
    return [
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item in full_edges
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        )
    ]


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("matching misses the changed vertex")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("analysis", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_cancellation_transport_verified.json"
        ),
    )
    args = parser.parse_args()
    candidate = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    if analysis["status"] not in {
        "cancellation_transport_contradiction",
        "matching_fork_contradiction",
    }:
        raise AssertionError("analysis does not claim a transport")
    if Path(analysis["candidate"]) != args.candidate:
        raise AssertionError("analysis is bound to another candidate")
    if list(map(int, analysis["full_cycle_type"])) != [3, 4, 7]:
        raise AssertionError("unexpected full-factor type")

    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in matching)
        for matching in candidate["best_singleton_matchings"]
    ]
    if len(singleton_matchings) != 3:
        raise AssertionError("expected three singleton colour classes")
    expected_vertices = set(range(N))
    singleton_edges: set[Edge] = set()
    for matching in singleton_matchings:
        if len(matching) != N // 2:
            raise AssertionError("singleton class has the wrong size")
        if {vertex for item in matching for vertex in item} != expected_vertices:
            raise AssertionError("singleton class is not a perfect matching")
        if singleton_edges.intersection(matching):
            raise AssertionError("singleton colour classes overlap")
        singleton_edges.update(matching)
    full_edges = set(FULL_EDGES)
    if full_edges.intersection(singleton_edges):
        raise AssertionError("full and singleton blocks overlap")
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = enumerate_perfect_matchings(full_edges | singleton_edges)
    if len(matchings) != int(analysis["skeleton_perfect_matchings"]):
        raise AssertionError("perfect-matching count mismatch")

    certificate = analysis["certificate"]
    changed = int(certificate["changed_vertex"])
    partner = int(certificate["common_partner"])
    sparse_index = int(certificate["sparse_equation_index"])
    rich_index = int(certificate["rich_equation_index"])
    sparse_colouring = decode_colouring(sparse_index)
    rich_colouring = decode_colouring(rich_index)
    if list(sparse_colouring) != list(certificate["sparse_colouring"]):
        raise AssertionError("sparse coloring/index mismatch")
    if list(rich_colouring) != list(certificate["rich_colouring"]):
        raise AssertionError("rich coloring/index mismatch")
    changed_vertices = [
        vertex
        for vertex in range(N)
        if sparse_colouring[vertex] != rich_colouring[vertex]
    ]
    if changed_vertices != [changed]:
        raise AssertionError("the colorings do not differ at exactly x")
    if len(set(sparse_colouring)) == 1 or len(set(rich_colouring)) == 1:
        raise AssertionError("transport colorings must be forbidden")

    sparse_activity = active_matching_ids(
        matchings, full_edges, labels, sparse_colouring
    )
    rich_activity = active_matching_ids(
        matchings, full_edges, labels, rich_colouring
    )
    if sparse_activity != list(certificate["sparse_activity"]):
        raise AssertionError("sparse activity mismatch")
    if rich_activity != list(certificate["rich_activity"]):
        raise AssertionError("rich activity mismatch")
    if not sparse_activity:
        raise AssertionError("transport set must be nonempty")
    extra = int(certificate["extra_matching"])
    if set(rich_activity) != set(sparse_activity) | {extra}:
        raise AssertionError("rich activity is not S plus one matching")
    if extra in sparse_activity:
        raise AssertionError("extra matching was already active")
    if any(
        partner_at(matchings[matching_id], changed) != partner
        for matching_id in sparse_activity
    ):
        raise AssertionError("old matchings do not share the x-y edge")
    common_edge = edge(changed, partner)
    if common_edge != tuple(certificate["common_full_edge"]):
        raise AssertionError("reported common edge mismatch")
    if common_edge not in full_edges:
        raise AssertionError("common transport edge is not a full block")
    if analysis["status"] == "matching_fork_contradiction":
        target = {
            edge(*map(int, item))
            for item in certificate["singleton_target"]
        }
        removed = edge(
            *map(int, certificate["removed_singleton_edge"])
        )
        if removed not in target:
            raise AssertionError("removed edge is absent from target")
        if labels[removed] != int(
            certificate["removed_singleton_colour"]
        ):
            raise AssertionError("removed edge colour mismatch")
        sparse_singletons = {
            item
            for item, colour in labels.items()
            if (
                sparse_colouring[item[0]]
                == sparse_colouring[item[1]]
                == colour
            )
        }
        rich_singletons = {
            item
            for item, colour in labels.items()
            if (
                rich_colouring[item[0]]
                == rich_colouring[item[1]]
                == colour
            )
        }
        if sparse_singletons != target - {removed}:
            raise AssertionError("sparse singleton activation mismatch")
        if rich_singletons != target:
            raise AssertionError("rich singleton activation mismatch")

    payload = {
        "verified": True,
        "candidate": str(args.candidate),
        "analysis": str(args.analysis),
        "full_cycle_type": [3, 4, 7],
        "skeleton_perfect_matchings": len(matchings),
        "sparse_equation_index": sparse_index,
        "rich_equation_index": rich_index,
        "changed_vertex": changed,
        "common_partner": partner,
        "transport_set_size": len(sparse_activity),
        "extra_matching": extra,
        "logical_check": (
            "the sparse forbidden equation cancels S; changing only x "
            "multiplies every S monomial by the same nonzero x-y entry "
            "ratio, so the rich forbidden equation leaves the extra "
            "supported monomial nonzero"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
