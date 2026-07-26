"""Enumerate n=10 C4+C6 equality supports modulo their natural symmetry."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

from explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)

N = 10
CYCLES = (tuple(range(4)), tuple(range(4, 10)))
FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(ALL_EDGES)}


def matching_mask(matching: Sequence[Edge]) -> int:
    return sum(1 << EDGE_INDEX[item] for item in matching)


def mask_edges(mask: int) -> list[list[int]]:
    return [
        list(item)
        for index, item in enumerate(ALL_EDGES)
        if mask & (1 << index)
    ]


def dihedral_maps(cycle: Sequence[int]) -> list[dict[int, int]]:
    size = len(cycle)
    output: list[dict[int, int]] = []
    for reflection in (False, True):
        for rotation in range(size):
            output.append(
                {
                    int(cycle[index]): int(
                        cycle[
                            (
                                rotation - index
                                if reflection
                                else rotation + index
                            )
                            % size
                        ]
                    )
                    for index in range(size)
                }
            )
    return output


def automorphisms() -> list[tuple[int, ...]]:
    output: list[tuple[int, ...]] = []
    for first in dihedral_maps(CYCLES[0]):
        for second in dihedral_maps(CYCLES[1]):
            merged = {**first, **second}
            output.append(tuple(merged[vertex] for vertex in range(N)))
    if len(set(output)) != 96:
        raise AssertionError("C4+C6 automorphism group is not size 96")
    return sorted(set(output))


def transform_mask(mask: int, permutation: Sequence[int]) -> int:
    output = 0
    for index, (first, second) in enumerate(ALL_EDGES):
        if not mask & (1 << index):
            continue
        image = tuple(
            sorted((int(permutation[first]), int(permutation[second])))
        )
        output |= 1 << EDGE_INDEX[image]
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_support_orbits.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    candidates = [
        matching
        for matching in perfect_matchings(N)
        if not (set(matching) & set(FULL_EDGES))
    ]
    masks = [matching_mask(matching) for matching in candidates]
    permutations = automorphisms()
    transformed = {
        mask: tuple(
            transform_mask(mask, permutation)
            for permutation in permutations
        )
        for mask in masks
    }
    canonical_counts: Counter[tuple[int, int, int]] = Counter()
    raw_triples = 0
    for first_index, first in enumerate(masks):
        for second_index in range(first_index + 1, len(masks)):
            second = masks[second_index]
            if first & second:
                continue
            for third in masks[second_index + 1 :]:
                if first & third or second & third:
                    continue
                raw_triples += 1
                canonical = min(
                    tuple(
                        sorted(
                            (
                                transformed[first][permutation_index],
                                transformed[second][permutation_index],
                                transformed[third][permutation_index],
                            )
                        )
                    )
                    for permutation_index in range(len(permutations))
                )
                canonical_counts[canonical] += 1
    if raw_triples != 446_592:
        raise AssertionError(
            f"ordered enumeration changed: {raw_triples}"
        )
    rows = [
        {
            "orbit_index": orbit_index,
            "orbit_size_uncoloured": count,
            "singleton_matching_masks": list(key),
            "singleton_matchings": [
                mask_edges(mask) for mask in key
            ],
        }
        for orbit_index, (key, count) in enumerate(
            sorted(canonical_counts.items())
        )
    ]
    if sum(int(row["orbit_size_uncoloured"]) for row in rows) != raw_triples:
        raise AssertionError("orbit sizes do not cover raw triples")
    orbit_histogram = Counter(
        int(row["orbit_size_uncoloured"]) for row in rows
    )
    payload = {
        "verified": True,
        "scope": (
            "all unordered triples of edge-disjoint perfect matchings "
            "disjoint from a fixed labelled C4+C6 2-factor, modulo the "
            "96 automorphisms of that factor"
        ),
        "n": N,
        "d": 3,
        "full_cycles": [list(cycle) for cycle in CYCLES],
        "full_edges": [list(item) for item in sorted(FULL_EDGES)],
        "factor_automorphisms": len(permutations),
        "candidate_singleton_matchings": len(candidates),
        "raw_uncoloured_factorizations": raw_triples,
        "support_orbits": len(rows),
        "orbit_size_histogram": dict(sorted(orbit_histogram.items())),
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
