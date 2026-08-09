"""Finite semantic audit of the all-odd one-term proof mechanism.

The arbitrary-order theorem is analytic.  This script independently checks
its construction on every colour-labelled equality support over the fixed
order-8 full factor C3+C5.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

from explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)

N = 8
CYCLES = ((0, 1, 2), (3, 4, 5, 6, 7))
FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)


def exact_activation_colouring(
    singleton_matchings: Sequence[Sequence[Edge]],
    target: frozenset[Edge],
) -> tuple[int, ...]:
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    colouring: list[int | None] = [None] * N
    for item in target:
        colour = labels[item]
        for vertex in item:
            if colouring[vertex] not in {None, colour}:
                raise AssertionError("target is not a matching")
            colouring[vertex] = colour

    uncoloured = {
        vertex for vertex, colour in enumerate(colouring) if colour is None
    }
    adjacency = {vertex: set() for vertex in uncoloured}
    for matching in singleton_matchings[1:]:
        for first, second in matching:
            if first in uncoloured and second in uncoloured:
                adjacency[first].add(second)
                adjacency[second].add(first)
    unseen = set(uncoloured)
    components: list[dict[int, int]] = []
    while unseen:
        start = min(unseen)
        sides = {start: 0}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in adjacency[vertex]:
                expected = 1 - sides[vertex]
                if other in sides:
                    if sides[other] != expected:
                        raise AssertionError("S1 union S2 is not bipartite")
                    continue
                sides[other] = expected
                stack.append(other)
        unseen -= set(sides)
        components.append(sides)
    for component in components:
        for vertex, side in component.items():
            colouring[vertex] = 1 + side

    result = tuple(int(colour) for colour in colouring)
    if len(set(result)) == 1:
        isolated = next(
            (
                vertex
                for vertex in uncoloured
                if not adjacency[vertex]
            ),
            None,
        )
        if isolated is None:
            raise AssertionError("failed to make the colouring forbidden")
        changed = list(result)
        changed[isolated] = 3 - changed[isolated]
        result = tuple(changed)
    active_singletons = {
        item
        for item, colour in labels.items()
        if result[item[0]] == result[item[1]] == colour
    }
    if active_singletons != set(target):
        raise AssertionError("exact activation lemma failed")
    if len(set(result)) == 1:
        raise AssertionError("constructed colouring is monochromatic")
    return result


def active(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> bool:
    return all(
        item in FULL_EDGES
        or (
            colouring[item[0]]
            == colouring[item[1]]
            == labels[item]
        )
        for item in matching
    )


def certify_support(
    singleton_matchings: Sequence[Sequence[Edge]],
) -> dict[str, int]:
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    if len(labels) != 3 * N // 2:
        raise AssertionError("singleton colour classes overlap")
    skeleton = set(FULL_EDGES) | set(labels)
    matchings = perfect_matchings(N, skeleton)
    singleton_counts = [
        sum(item in labels for item in matching)
        for matching in matchings
    ]
    minimum = min(singleton_counts)
    if minimum == 0:
        raise AssertionError("all-odd factor acquired a full-only matching")
    if minimum < N // 2:
        matching_id = singleton_counts.index(minimum)
    else:
        matching_id = next(
            (
                index
                for index, matching in enumerate(matchings)
                if len({labels[item] for item in matching}) >= 2
            ),
            None,
        )
        if matching_id is None:
            raise AssertionError("singleton graph has no mixed matching")
    matching = matchings[matching_id]
    target = frozenset(item for item in matching if item in labels)
    colouring = exact_activation_colouring(singleton_matchings, target)
    activity = [
        index
        for index, candidate in enumerate(matchings)
        if active(candidate, colouring, labels)
    ]
    if activity != [matching_id]:
        raise AssertionError("constructed forbidden amplitude is not unary")
    return {
        "skeleton_perfect_matchings": len(matchings),
        "minimum_singleton_edges": minimum,
        "equation_index": sum(
            colouring[vertex] * (3**vertex) for vertex in range(N)
        ),
    }


def main() -> None:
    candidates = [
        matching
        for matching in perfect_matchings(N)
        if not (set(matching) & set(FULL_EDGES))
    ]
    unordered = [
        (first, second, third)
        for first_index, first in enumerate(candidates)
        for second_index in range(first_index + 1, len(candidates))
        for second in (candidates[second_index],)
        if not (set(first) & set(second))
        for third in candidates[second_index + 1 :]
        if not (set(first) & set(third))
        and not (set(second) & set(third))
    ]
    rows = []
    minimum_histogram: Counter[int] = Counter()
    for triple in unordered:
        for labelled in itertools.permutations(triple):
            result = certify_support(labelled)
            minimum_histogram[result["minimum_singleton_edges"]] += 1
            rows.append(result)
    payload = {
        "verified": True,
        "scope": (
            "all colour-labelled n=8 equality supports over the fixed "
            "all-odd C3+C5 full factor"
        ),
        "claim_scope": (
            "finite semantic audit of the analytic construction, not an "
            "independent proof of the arbitrary-order matching bound"
        ),
        "candidate_singleton_matchings": len(candidates),
        "raw_uncoloured_factorizations": len(unordered),
        "colour_labelled_supports": len(rows),
        "minimum_singleton_edge_histogram": {
            str(key): value
            for key, value in sorted(minimum_histogram.items())
        },
        "minimum_skeleton_perfect_matchings": min(
            row["skeleton_perfect_matchings"] for row in rows
        ),
        "maximum_skeleton_perfect_matchings": max(
            row["skeleton_perfect_matchings"] for row in rows
        ),
        "verified_one_term_certificates": len(rows),
    }
    output = Path(
        "tmp/odd_full_factor_one_term_mechanism_n8_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
