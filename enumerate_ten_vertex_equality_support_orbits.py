"""Enumerate one ten-vertex equality factor type modulo natural symmetry."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

from explore_random_even_cycle_forks import Edge, perfect_matchings

N = 10
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def components(lengths: Sequence[int]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    start = 0
    for length in lengths:
        result.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise ValueError("cycle lengths must sum to ten")
    return result


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def matching_mask(matching: Sequence[Edge]) -> int:
    return sum(1 << EDGE_INDEX[item] for item in matching)


def mask_edges(mask: int) -> list[list[int]]:
    return [
        list(item)
        for index, item in enumerate(ALL_EDGES)
        if mask & (1 << index)
    ]


def component_permutations(
    cycles: Sequence[Sequence[int]],
) -> list[tuple[int, ...]]:
    groups: dict[int, list[int]] = {}
    for index, cycle in enumerate(cycles):
        groups.setdefault(len(cycle), []).append(index)
    choices = [
        list(itertools.permutations(indices))
        for _length, indices in sorted(groups.items())
    ]
    output: list[tuple[int, ...]] = []
    for selected in itertools.product(*choices):
        image = list(range(len(cycles)))
        for (_length, indices), permutation in zip(
            sorted(groups.items()), selected, strict=True
        ):
            for source, target in zip(indices, permutation, strict=True):
                image[source] = target
        output.append(tuple(image))
    return output


def factor_automorphisms(
    cycles: Sequence[Sequence[int]],
) -> list[tuple[int, ...]]:
    result: set[tuple[int, ...]] = set()
    for component_image in component_permutations(cycles):
        local_choices = [
            [
                (shift, reflection)
                for shift in range(len(cycle))
                for reflection in (False, True)
            ]
            for cycle in cycles
        ]
        for local in itertools.product(*local_choices):
            permutation = [0] * N
            for source_index, source in enumerate(cycles):
                target = cycles[component_image[source_index]]
                shift, reflection = local[source_index]
                for position, vertex in enumerate(source):
                    target_position = (
                        shift - position
                        if reflection
                        else shift + position
                    ) % len(source)
                    permutation[vertex] = target[target_position]
            result.add(tuple(permutation))
    return sorted(result)


def transform_mask(mask: int, permutation: Sequence[int]) -> int:
    output = 0
    for index, (first, second) in enumerate(ALL_EDGES):
        if mask & (1 << index):
            image = edge(permutation[first], permutation[second])
            output |= 1 << EDGE_INDEX[image]
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    lengths = tuple(map(int, args.cycles.split(",")))
    cycles = components(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    started = time.perf_counter()
    candidates = [
        matching
        for matching in perfect_matchings(N)
        if not (set(matching) & set(full_edges))
    ]
    masks = [matching_mask(matching) for matching in candidates]
    automorphisms = factor_automorphisms(cycles)
    transformed = {
        mask: tuple(
            transform_mask(mask, permutation)
            for permutation in automorphisms
        )
        for mask in masks
    }
    counts: Counter[tuple[int, int, int]] = Counter()
    raw = 0
    for first_index, first in enumerate(masks):
        for second_index in range(first_index + 1, len(masks)):
            second = masks[second_index]
            if first & second:
                continue
            for third in masks[second_index + 1 :]:
                if first & third or second & third:
                    continue
                raw += 1
                representative = min(
                    tuple(
                        sorted(
                            (
                                transformed[first][group_index],
                                transformed[second][group_index],
                                transformed[third][group_index],
                            )
                        )
                    )
                    for group_index in range(len(automorphisms))
                )
                counts[representative] += 1
    rows = [
        {
            "orbit_index": index,
            "orbit_size_uncoloured": count,
            "singleton_matching_masks": list(representative),
            "singleton_matchings": [
                mask_edges(mask) for mask in representative
            ],
        }
        for index, (representative, count) in enumerate(
            sorted(counts.items())
        )
    ]
    if sum(int(row["orbit_size_uncoloured"]) for row in rows) != raw:
        raise AssertionError("orbit sizes do not cover raw factorizations")
    payload = {
        "status": "complete",
        "scope": (
            "unordered triples of edge-disjoint perfect matchings "
            f"disjoint from a fixed factor of type {list(lengths)}"
        ),
        "n": N,
        "d": 3,
        "full_cycle_type": list(lengths),
        "full_cycles": [list(cycle) for cycle in cycles],
        "full_edges": [list(item) for item in sorted(full_edges)],
        "factor_automorphisms": len(automorphisms),
        "candidate_singleton_matchings": len(candidates),
        "raw_uncoloured_factorizations": raw,
        "support_orbits": len(rows),
        "orbit_size_histogram": dict(
            sorted(
                Counter(
                    int(row["orbit_size_uncoloured"]) for row in rows
                ).items()
            )
        ),
        "rows": rows,
        "enumerate_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
