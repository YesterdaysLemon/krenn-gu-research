"""Enumerate larger one-term matching sets for an order-14 full factor."""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import time
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    canonical_json_sha256,
    contiguous_cycles,
)
from explore_random_even_cycle_forks import cycle_edges

Edge = tuple[int, int]
ALL_VERTICES = (1 << N) - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", default="3+3+4+4")
    parser.add_argument("--minimum-size", type=int, default=3)
    parser.add_argument("--maximum-size", type=int, default=6)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_larger_one_term_catalogue.json"
        ),
    )
    args = parser.parse_args()
    lengths = tuple(map(int, args.partition.split("+")))
    if sum(lengths) != N:
        raise ValueError("cycle partition must sum to 14")
    if not 1 <= args.minimum_size <= args.maximum_size <= N // 2:
        raise ValueError("invalid matching-size interval")

    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    edge_vertex_masks = tuple(
        (1 << first) | (1 << second)
        for first, second in eligible_edges
    )
    full_adjacency = [0] * N
    for first, second in full_edges:
        full_adjacency[first] |= 1 << second
        full_adjacency[second] |= 1 << first

    @functools.lru_cache(maxsize=None)
    def full_completion(remaining: int) -> int:
        if not remaining:
            return 1
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = full_adjacency[first] & remaining
        total = 0
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            total += full_completion(
                remaining ^ first_bit ^ second_bit
            )
        return total

    completion_by_deleted = tuple(
        full_completion(ALL_VERTICES ^ deleted)
        for deleted in range(1 << N)
    )

    def support_count(item_ids: tuple[int, ...]) -> int:
        deleted_masks = [0] * (1 << len(item_ids))
        total = completion_by_deleted[0]
        for subset in range(1, 1 << len(item_ids)):
            lowest = subset & -subset
            position = lowest.bit_length() - 1
            deleted_masks[subset] = (
                deleted_masks[subset ^ lowest]
                | edge_vertex_masks[item_ids[position]]
            )
            total += completion_by_deleted[deleted_masks[subset]]
        return total

    def matching_id_sets(size: int):
        chosen: list[int] = []

        def visit(start: int, used_vertices: int):
            if len(chosen) == size:
                yield tuple(chosen)
                return
            remaining_edges = size - len(chosen)
            for item_id in range(start, len(eligible_edges)):
                if len(eligible_edges) - item_id < remaining_edges:
                    break
                item_mask = edge_vertex_masks[item_id]
                if item_mask & used_vertices:
                    continue
                chosen.append(item_id)
                yield from visit(
                    item_id + 1, used_vertices | item_mask
                )
                chosen.pop()

        yield from visit(0, 0)

    started = time.perf_counter()
    rows: dict[str, list[int]] = {}
    scanned: dict[str, int] = {}
    for size in range(args.minimum_size, args.maximum_size + 1):
        masks = []
        count = 0
        for item_ids in matching_id_sets(size):
            count += 1
            if support_count(item_ids) == 1:
                masks.append(sum(1 << item_id for item_id in item_ids))
        rows[str(size)] = masks
        scanned[str(size)] = count
        print(
            f"size={size} scanned={count} one_term={len(masks)}",
            flush=True,
        )

    payload = {
        "status": "larger_one_term_catalogue_complete",
        "partition": list(lengths),
        "eligible_edges": [list(item) for item in eligible_edges],
        "matching_sets_scanned_by_size": scanned,
        "one_term_masks_by_size": rows,
        "one_term_counts_by_size": {
            size: len(masks) for size, masks in rows.items()
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    payload["canonical_sha256_without_self"] = canonical_json_sha256(
        payload
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key != "one_term_masks_by_size"
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
