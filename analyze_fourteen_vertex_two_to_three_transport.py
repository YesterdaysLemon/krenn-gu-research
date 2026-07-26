"""Scan all order-14 colourings for an exact 2-to-3 transport fork."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Sequence

import numpy as np

from analyze_fourteen_vertex_full_direct_motifs import (
    EQUATIONS,
    FULL_EDGES,
    N,
    activity_arrays,
    edge,
    indexed_colouring,
    perfect_matchings,
)

Edge = tuple[int, int]


def two_to_three_hits_prefix(
    n: int,
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
    prefix: int,
) -> tuple[int, int, int]:
    """Return distinct fork shapes, raw forks, and matching count in a prefix."""
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    matchings = perfect_matchings(set(full_edges) | set(labels))
    equation_indices = np.arange(prefix, dtype=np.int64)
    counts = np.zeros(prefix, dtype=np.int16)
    first = np.full(prefix, -1, dtype=np.int16)
    second = np.full(prefix, -1, dtype=np.int16)
    third = np.full(prefix, -1, dtype=np.int16)
    for matching_id, matching in enumerate(matchings):
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        mask = np.ones(prefix, dtype=bool)
        for vertex, colour in requirements.items():
            mask &= (
                (equation_indices // (3**vertex)) % 3
            ) == colour
        first[mask & (counts == 0)] = matching_id
        second[mask & (counts == 1)] = matching_id
        third[mask & (counts == 2)] = matching_id
        counts += mask

    partners = np.empty((len(matchings), n), dtype=np.int16)
    for matching_id, matching in enumerate(matchings):
        for left, right in matching:
            partners[matching_id, left] = right
            partners[matching_id, right] = left

    distinct_keys: list[np.ndarray] = []
    raw_hits = 0
    ids = (first, second, third)
    for vertex in range(n):
        weight = 3**vertex
        digits = (equation_indices // weight) % 3
        for left_colour, right_colour in ((0, 1), (0, 2), (1, 2)):
            left = equation_indices[digits == left_colour]
            right = left + (right_colour - left_colour) * weight
            in_prefix = right < prefix
            left = left[in_prefix]
            right = right[in_prefix]
            for rich_rows, sparse_rows in ((left, right), (right, left)):
                eligible = (
                    (counts[sparse_rows] == 2)
                    & (counts[rich_rows] == 3)
                )
                sparse_first = first[sparse_rows]
                sparse_second = second[sparse_rows]
                rich_values = tuple(item[rich_rows] for item in ids)
                eligible &= (
                    (sparse_first == rich_values[0])
                    | (sparse_first == rich_values[1])
                    | (sparse_first == rich_values[2])
                )
                eligible &= (
                    (sparse_second == rich_values[0])
                    | (sparse_second == rich_values[1])
                    | (sparse_second == rich_values[2])
                )
                positions = np.flatnonzero(eligible)
                if not len(positions):
                    continue
                sparse_first = sparse_first[positions]
                sparse_second = sparse_second[positions]
                common_partner = partners[sparse_first, vertex]
                same_partner = (
                    common_partner
                    == partners[sparse_second, vertex]
                )
                if not np.any(same_partner):
                    continue
                positions = positions[same_partner]
                sparse_first = sparse_first[same_partner]
                sparse_second = sparse_second[same_partner]
                common_partner = common_partner[same_partner]
                rich_first = rich_values[0][positions]
                rich_second = rich_values[1][positions]
                rich_third = rich_values[2][positions]
                extra = (
                    rich_first
                    + rich_second
                    + rich_third
                    - sparse_first
                    - sparse_second
                )
                low = np.minimum(sparse_first, sparse_second)
                high = np.maximum(sparse_first, sparse_second)
                matching_count = len(matchings)
                key = (
                    (
                        (
                            (
                                vertex * n + common_partner
                            )
                            * matching_count
                            + low
                        )
                        * matching_count
                        + high
                    )
                    * matching_count
                    + extra
                ).astype(np.int64)
                distinct_keys.append(key)
                raw_hits += len(key)
    if distinct_keys:
        distinct = len(np.unique(np.concatenate(distinct_keys)))
    else:
        distinct = 0
    return distinct, raw_hits, len(matchings)


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("perfect matching misses a vertex")


def find_two_to_three(
    counts: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    third: np.ndarray,
    matchings: Sequence[Sequence[Edge]],
) -> dict[str, object] | None:
    indices = np.arange(EQUATIONS, dtype=np.int64)
    monochromatic = {
        sum(colour * (3**vertex) for vertex in range(N))
        for colour in range(3)
    }
    ids = (first, second, third)
    for vertex in range(N):
        weight = 3**vertex
        zero = indices[((indices // weight) % 3) == 0]
        rows = (zero, zero + weight, zero + 2 * weight)
        for first_colour, second_colour in ((0, 1), (0, 2), (1, 2)):
            for rich_rows, sparse_rows in (
                (rows[first_colour], rows[second_colour]),
                (rows[second_colour], rows[first_colour]),
            ):
                eligible = (
                    (counts[sparse_rows] == 2)
                    & (counts[rich_rows] == 3)
                )
                sparse_first = first[sparse_rows]
                sparse_second = second[sparse_rows]
                rich_values = tuple(item[rich_rows] for item in ids)
                eligible &= (
                    (sparse_first == rich_values[0])
                    | (sparse_first == rich_values[1])
                    | (sparse_first == rich_values[2])
                )
                eligible &= (
                    (sparse_second == rich_values[0])
                    | (sparse_second == rich_values[1])
                    | (sparse_second == rich_values[2])
                )
                for position in np.flatnonzero(eligible):
                    rich_index = int(rich_rows[position])
                    sparse_index = int(sparse_rows[position])
                    if (
                        rich_index in monochromatic
                        or sparse_index in monochromatic
                    ):
                        continue
                    sparse_activity = [
                        int(first[sparse_index]),
                        int(second[sparse_index]),
                    ]
                    partners = {
                        partner_at(matchings[item], vertex)
                        for item in sparse_activity
                    }
                    if len(partners) != 1:
                        continue
                    partner = next(iter(partners))
                    common_edge = edge(vertex, partner)
                    if common_edge not in FULL_EDGES:
                        raise AssertionError(
                            "common edge cannot be a singleton"
                        )
                    rich_activity = [
                        int(first[rich_index]),
                        int(second[rich_index]),
                        int(third[rich_index]),
                    ]
                    extras = set(rich_activity) - set(sparse_activity)
                    if len(extras) != 1:
                        raise AssertionError("not an exact 2-to-3 fork")
                    return {
                        "changed_vertex": vertex,
                        "common_partner": partner,
                        "common_full_edge": list(common_edge),
                        "sparse_equation_index": sparse_index,
                        "sparse_colouring": list(
                            indexed_colouring(sparse_index)
                        ),
                        "sparse_activity": sparse_activity,
                        "rich_equation_index": rich_index,
                        "rich_colouring": list(
                            indexed_colouring(rich_index)
                        ),
                        "rich_activity": rich_activity,
                        "extra_matching": next(iter(extras)),
                    }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_to_three_transport.json"
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
    matchings = perfect_matchings(set(FULL_EDGES) | set(labels))
    started = time.perf_counter()
    counts, first, second, third, total_extensions = activity_arrays(
        matchings, labels
    )
    certificate = find_two_to_three(
        counts, first, second, third, matchings
    )
    payload = {
        "status": (
            "cancellation_transport_contradiction"
            if certificate is not None
            else "two_to_three_transport_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "candidate": str(args.candidate),
        "full_cycle_type": [3, 4, 7],
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "zero_term_forbidden_colourings": int(
            np.count_nonzero(counts == 0)
        ),
        "one_term_forbidden_colourings": int(
            np.count_nonzero(counts == 1)
        ),
        "two_term_forbidden_colourings": int(
            np.count_nonzero(counts == 2)
        ),
        "three_term_forbidden_colourings": int(
            np.count_nonzero(counts == 3)
        ),
        "certificate": certificate,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
