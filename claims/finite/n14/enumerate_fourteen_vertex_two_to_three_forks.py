"""Enumerate nested matching sets giving a stable C4 two-to-three fork."""

from __future__ import annotations

import argparse
import functools
import itertools
import json
import time
from collections import Counter
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    canonical_json_sha256,
    contiguous_cycles,
)
from explore_random_even_cycle_forks import cycle_edges, perfect_matchings

Edge = tuple[int, int]
ALL_VERTICES = (1 << N) - 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", default="3+3+4+4")
    parser.add_argument("--minimum-rich-size", type=int, default=3)
    parser.add_argument("--maximum-rich-size", type=int, default=6)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_to_three_forks.json"
        ),
    )
    args = parser.parse_args()
    lengths = tuple(map(int, args.partition.split("+")))
    if sum(lengths) != N:
        raise ValueError("cycle partition must sum to 14")
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

    @functools.lru_cache(maxsize=None)
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
            for item_id in range(start, len(eligible_edges)):
                item_mask = edge_vertex_masks[item_id]
                if item_mask & used_vertices:
                    continue
                chosen.append(item_id)
                yield from visit(
                    item_id + 1, used_vertices | item_mask
                )
                chosen.pop()

        yield from visit(0, 0)

    c4_edge_sets = {
        component: frozenset(cycle_edges(cycle))
        for component, cycle in enumerate(cycles)
        if len(cycle) == 4
    }
    started = time.perf_counter()
    rich_histogram: Counter[int] = Counter()
    pairs: set[tuple[int, int, int]] = set()
    rich_scanned = {}
    for rich_size in range(
        args.minimum_rich_size, args.maximum_rich_size + 1
    ):
        scanned = 0
        rich_count = 0
        for rich_ids in matching_id_sets(rich_size):
            scanned += 1
            count = support_count(rich_ids)
            rich_histogram[count] += 1
            if count != 3:
                continue
            rich_count += 1
            rich_edges = {
                eligible_edges[item_id] for item_id in rich_ids
            }
            rich_matchings = perfect_matchings(
                N, set(full_edges) | rich_edges
            )
            if len(rich_matchings) != 3:
                raise AssertionError("rich matching count mismatch")
            for sparse_size in range(1, rich_size):
                for sparse_ids in itertools.combinations(
                    rich_ids, sparse_size
                ):
                    if support_count(sparse_ids) != 2:
                        continue
                    sparse_edges = {
                        eligible_edges[item_id]
                        for item_id in sparse_ids
                    }
                    sparse_matchings = perfect_matchings(
                        N, set(full_edges) | sparse_edges
                    )
                    if len(sparse_matchings) != 2:
                        raise AssertionError(
                            "sparse matching count mismatch"
                        )
                    symmetric = (
                        set(sparse_matchings[0])
                        ^ set(sparse_matchings[1])
                    )
                    component = next(
                        (
                            component
                            for component, c4_edges
                            in c4_edge_sets.items()
                            if symmetric == set(c4_edges)
                        ),
                        None,
                    )
                    if component is None:
                        continue
                    sparse_mask = sum(
                        1 << item_id for item_id in sparse_ids
                    )
                    rich_mask = sum(
                        1 << item_id for item_id in rich_ids
                    )
                    pairs.add(
                        (sparse_mask, rich_mask, int(component))
                    )
        rich_scanned[str(rich_size)] = {
            "matching_sets": scanned,
            "three_matching_sets": rich_count,
        }
        print(
            f"size={rich_size} scanned={scanned} "
            f"three_matching={rich_count} forks={len(pairs)}",
            flush=True,
        )

    rows = [
        {
            "sparse_mask": sparse,
            "rich_mask": rich,
            "alternating_c4_component": component,
        }
        for sparse, rich, component in sorted(pairs)
    ]
    payload = {
        "status": "two_to_three_fork_catalogue_complete",
        "partition": list(lengths),
        "eligible_edges": [list(item) for item in eligible_edges],
        "rich_scan_by_size": rich_scanned,
        "rich_support_count_histogram": dict(
            sorted(rich_histogram.items())
        ),
        "two_to_three_forks": len(rows),
        "fork_rows": rows,
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
                if key not in {
                    "fork_rows",
                    "rich_support_count_histogram",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
