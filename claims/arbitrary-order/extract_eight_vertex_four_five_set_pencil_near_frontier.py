#!/usr/bin/env python3
"""Extract the canonical generic S3CCD systems with q <= a threshold.

This imports the accepted finite census implementation, recomputes its exact
rank cache, and records the small near-frontier subset for rank-degeneracy
analysis.  Generated outputs are reproducible evidence and normally stay under
``.research-runs``; the independently pinned q<=22 audit input is tracked
separately.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402


ROOT, HERE = bootstrap(__file__)
SOURCE = (
    ROOT
    / "claims/arbitrary-order/verify_eight_vertex_four_five_set_pencil_support_segre_generic_rank_census.py"
)


def load_primary():
    spec = importlib.util.spec_from_file_location("s3ccd_primary", SOURCE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def signature(module, left_state, right_state):
    left_partition, left_masks, _ = left_state
    right_partition, right_masks, _ = right_state
    edge_set = tuple(
        sorted(
            {
                (left_partition[chart], right_partition[chart])
                for chart in range(4)
            }
        )
    )
    return (left_masks, right_masks, edge_set)


def extract(module, threshold: int, progress_enabled: bool):
    maps = module.selector_maps()
    map_supports = module.support_masks(maps)
    representatives, selector_hash = module.selector_orbits(maps, progress_enabled)
    partition_list = module.restricted_growth_partitions()
    signatures, state_cache, pair_instances = module.collect_signatures(
        representatives, map_supports, partition_list, progress_enabled
    )
    ranks, rank_histogram, modularly_deficient = module.rank_cache(
        signatures, progress_enabled
    )
    del signatures

    records = []
    histogram: Counter[int] = Counter()
    full_systems = 0
    for rep_index, quadruple in enumerate(representatives, start=1):
        states = [
            module.state_cache_for_supports(
                partition_list,
                state_cache,
                tuple(map_supports[quadruple[chart]][vertex] for chart in range(4)),
            )
            for vertex in module.COMMON_VERTICES
        ]
        pair_matrices = {}
        for left, right in module.PAIR_ORDER:
            matrix = np.empty((len(states[left]), len(states[right])), dtype=np.int8)
            for left_index, left_state in enumerate(states[left]):
                for right_index, right_state in enumerate(states[right]):
                    matrix[left_index, right_index] = ranks[
                        signature(module, left_state, right_state)
                    ]
            pair_matrices[(left, right)] = matrix

        delta = [
            np.array([state[2] for state in vertex_states], dtype=np.int16)
            for vertex_states in states
        ]
        values = (
            delta[0][:, None, None, None]
            + delta[1][None, :, None, None]
            + delta[2][None, None, :, None]
            + delta[3][None, None, None, :]
        )
        values = values + (
            pair_matrices[(0, 1)][:, :, None, None]
            + pair_matrices[(0, 2)][:, None, :, None]
            + pair_matrices[(0, 3)][:, None, None, :]
            + pair_matrices[(1, 2)][None, :, :, None]
            + pair_matrices[(1, 3)][None, :, None, :]
            + pair_matrices[(2, 3)][None, None, :, :]
        )
        local_values, local_counts = np.unique(values, return_counts=True)
        histogram.update(
            {int(value): int(count) for value, count in zip(local_values, local_counts)}
        )
        full_systems += int(values.size)
        for position in np.argwhere(values <= threshold):
            index = tuple(int(value) for value in position)
            selected = tuple(states[vertex][index[vertex]] for vertex in range(4))
            pair_indices = (
                (index[0], index[1]),
                (index[0], index[2]),
                (index[0], index[3]),
                (index[1], index[2]),
                (index[1], index[3]),
                (index[2], index[3]),
            )
            six_ranks = tuple(
                int(pair_matrices[pair][pair_index])
                for pair, pair_index in zip(
                    module.PAIR_ORDER, pair_indices, strict=True
                )
            )
            records.append(
                {
                    "q": int(values[index]),
                    "selector_ids": list(quadruple),
                    "selectors": [list(maps[value]) for value in quadruple],
                    "partitions": [list(state[0]) for state in selected],
                    "support_masks_by_vertex_block": [list(state[1]) for state in selected],
                    "delta_by_vertex": [int(state[2]) for state in selected],
                    "ranks_01_02_03_12_13_23": list(six_ranks),
                }
            )
        if progress_enabled and rep_index % 5_000 == 0:
            print(
                "near frontier",
                rep_index,
                len(records),
                full_systems,
                flush=True,
            )

    assert full_systems == module.EXPECTED_FULL_PARTITION_SYSTEMS
    assert dict(histogram) == module.EXPECTED_Q_HISTOGRAM
    assert len(records) == sum(
        count for q, count in module.EXPECTED_Q_HISTOGRAM.items() if q <= threshold
    )
    return {
        "status": "exact_s3ccd_near_frontier_extract",
        "global_conjecture": "UNRESOLVED",
        "threshold": threshold,
        "selector_hash": selector_hash,
        "pair_instances": pair_instances,
        "rank_histogram": {
            f"{cardinality},{rank}": count
            for (cardinality, rank), count in sorted(rank_histogram.items())
        },
        "modularly_deficient_signatures": modularly_deficient,
        "full_partition_systems": full_systems,
        "near_frontier_count": len(records),
        "near_frontier_histogram": dict(sorted(Counter(r["q"] for r in records).items())),
        "records": records,
        "scope_limit": (
            "generic exact-partition systems only; rank-degenerate components, "
            "B_all, target equations, and multi-pencil compatibility remain open"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--threshold", type=int, default=22)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    module = load_primary()
    result = extract(module, args.threshold, not args.quiet)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "threshold",
                    "near_frontier_count",
                    "near_frontier_histogram",
                    "full_partition_systems",
                    "global_conjecture",
                )
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
