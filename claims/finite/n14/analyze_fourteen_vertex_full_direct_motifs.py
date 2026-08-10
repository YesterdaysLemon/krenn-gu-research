"""Scan all 3^14 colourings for direct binomial/trinomial transport.

The activity arrays are built from partial-assignment extensions rather than
testing every matching against every colouring.  Relation signatures are
deduplicated by matching pair and the colours on full-edge endpoints.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

import numpy as np

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from verify_fourteen_vertex_no_one_term_support import (
    CYCLES,
    FULL_EDGES,
    N,
    Edge,
    edge,
    perfect_matchings,
)

ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}
EQUATIONS = 3**N


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def relation_signature(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
    def variables(matching: Sequence[Edge]) -> list[int]:
        output = []
        for item in matching:
            if item in FULL_EDGES:
                first_colour = int(colouring[item[0]])
                second_colour = int(colouring[item[1]])
            else:
                first_colour = second_colour = labels[item]
            output.append(
                9 * EDGE_INDEX[item]
                + 3 * first_colour
                + second_colour
            )
        return output

    vector: Counter[int] = Counter(variables(first))
    vector.subtract(variables(second))
    direct = tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in vector.items()
            if coefficient
        )
    )
    negative = tuple(
        (entry, -coefficient) for entry, coefficient in direct
    )
    return min(direct, negative)


def extension_offsets(
    free_vertices: tuple[int, ...],
    cache: dict[tuple[int, ...], np.ndarray],
) -> np.ndarray:
    if free_vertices in cache:
        return cache[free_vertices]
    offsets = np.array([0], dtype=np.int64)
    for vertex in free_vertices:
        weight = 3**vertex
        offsets = np.concatenate(
            (offsets, offsets + weight, offsets + 2 * weight)
        )
    cache[free_vertices] = offsets
    return offsets


def activity_arrays(
    matchings: Sequence[Sequence[Edge]],
    labels: dict[Edge, int],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, int]:
    counts = np.zeros(EQUATIONS, dtype=np.int16)
    first = np.full(EQUATIONS, -1, dtype=np.int16)
    second = np.full(EQUATIONS, -1, dtype=np.int16)
    third = np.full(EQUATIONS, -1, dtype=np.int16)
    offset_cache: dict[tuple[int, ...], np.ndarray] = {}
    total_extensions = 0
    for matching_id, matching in enumerate(matchings):
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        base = sum(
            colour * (3**vertex)
            for vertex, colour in requirements.items()
        )
        free = tuple(
            vertex for vertex in range(N) if vertex not in requirements
        )
        indices = base + extension_offsets(free, offset_cache)
        old = counts[indices].copy()
        first[indices[old == 0]] = matching_id
        second[indices[old == 1]] = matching_id
        third[indices[old == 2]] = matching_id
        counts[indices] = old + 1
        total_extensions += len(indices)
    return counts, first, second, third, total_extensions


def relevant_vertices(
    first: Sequence[Edge],
    second: Sequence[Edge],
) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                vertex
                for item in itertools.chain(first, second)
                if item in FULL_EDGES
                for vertex in item
            }
        )
    )


def colour_codes(
    indices: np.ndarray,
    vertices: Sequence[int],
) -> np.ndarray:
    codes = np.zeros(len(indices), dtype=np.int64)
    for position, vertex in enumerate(vertices):
        codes += (
            (indices // (3**vertex)) % 3
        ) * (3**position)
    return codes


def unique_relation_origins(
    indices: np.ndarray,
    first_ids: np.ndarray,
    second_ids: np.ndarray,
    matchings: Sequence[Sequence[Edge]],
    labels: dict[Edge, int],
) -> dict[tuple[tuple[int, int], ...], int]:
    pair_keys = (
        first_ids[indices].astype(np.int32) * len(matchings)
        + second_ids[indices].astype(np.int32)
    )
    origins: dict[tuple[tuple[int, int], ...], int] = {}
    for pair_key in np.unique(pair_keys):
        pair_mask = pair_keys == pair_key
        pair_indices = indices[pair_mask]
        first = int(pair_key // len(matchings))
        second = int(pair_key % len(matchings))
        vertices = relevant_vertices(
            matchings[first], matchings[second]
        )
        codes = colour_codes(pair_indices, vertices)
        _, positions = np.unique(codes, return_index=True)
        for position in positions:
            equation = int(pair_indices[position])
            signature = relation_signature(
                matchings[first],
                matchings[second],
                indexed_colouring(equation),
                labels,
            )
            origins.setdefault(signature, equation)
    return origins


def find_target(
    indices: np.ndarray,
    first_ids: np.ndarray,
    second_ids: np.ndarray,
    third_ids: np.ndarray,
    matchings: Sequence[Sequence[Edge]],
    labels: dict[Edge, int],
    origins: dict[tuple[tuple[int, int], ...], int],
) -> dict[str, object] | None:
    id_arrays = (first_ids, second_ids, third_ids)
    for left_position, right_position in ((0, 1), (0, 2), (1, 2)):
        left = id_arrays[left_position][indices]
        right = id_arrays[right_position][indices]
        pair_keys = (
            left.astype(np.int32) * len(matchings)
            + right.astype(np.int32)
        )
        for pair_key in np.unique(pair_keys):
            pair_mask = pair_keys == pair_key
            pair_indices = indices[pair_mask]
            first = int(pair_key // len(matchings))
            second = int(pair_key % len(matchings))
            vertices = relevant_vertices(
                matchings[first], matchings[second]
            )
            codes = colour_codes(pair_indices, vertices)
            _, positions = np.unique(codes, return_index=True)
            for position in positions:
                equation = int(pair_indices[position])
                signature = relation_signature(
                    matchings[first],
                    matchings[second],
                    indexed_colouring(equation),
                    labels,
                )
                if signature not in origins:
                    continue
                activity = [
                    int(first_ids[equation]),
                    int(second_ids[equation]),
                    int(third_ids[equation]),
                ]
                survivor = next(
                    item
                    for item in activity
                    if item not in {first, second}
                )
                return {
                    "origin_equation_index": origins[signature],
                    "target_equation_index": equation,
                    "target_activity": activity,
                    "target_paired_matchings": [first, second],
                    "target_surviving_matching": survivor,
                    "relation_signature": [
                        list(item) for item in signature
                    ],
                }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_full_direct_motifs.json"
        ),
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
    skeleton = set(FULL_EDGES) | set(labels)
    matchings = perfect_matchings(skeleton)
    started = time.perf_counter()
    counts, first, second, third, total_extensions = activity_arrays(
        matchings, labels
    )
    monochromatic = np.array(
        [
            sum(colour * (3**vertex) for vertex in range(N))
            for colour in range(3)
        ],
        dtype=np.int64,
    )
    counts[monochromatic] = -1
    binomial = np.flatnonzero(counts == 2)
    trinomial = np.flatnonzero(counts == 3)
    origins = unique_relation_origins(
        binomial, first, second, matchings, labels
    )
    certificate = find_target(
        trinomial,
        first,
        second,
        third,
        matchings,
        labels,
        origins,
    )
    payload = {
        "status": (
            "direct_contradiction"
            if certificate is not None
            else "full_direct_motif_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "candidate": str(args.candidate),
        "full_cycle_type": [len(cycle) for cycle in CYCLES],
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "zero_term_forbidden_colourings": int(
            np.count_nonzero(counts == 0)
        ),
        "one_term_forbidden_colourings": int(
            np.count_nonzero(counts == 1)
        ),
        "binomial_forbidden_colourings": len(binomial),
        "trinomial_forbidden_colourings": len(trinomial),
        "distinct_binomial_relations": len(origins),
        "elapsed_seconds": time.perf_counter() - started,
        "certificate": certificate,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
