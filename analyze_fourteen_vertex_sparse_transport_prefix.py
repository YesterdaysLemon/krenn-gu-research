"""Search sparse one/three-binomial transports in a colouring prefix."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

import numpy as np

from explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)
from explore_random_minimal_singleton_sets import contiguous_cycles

N = 14
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


def oriented_signature(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
    def entries(matching: Sequence[Edge]) -> list[int]:
        output = []
        for item in matching:
            if item in full_edges:
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

    vector: Counter[int] = Counter(entries(first))
    vector.subtract(entries(second))
    return tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in vector.items()
            if coefficient
        )
    )


def add(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    output: Counter[int] = Counter(dict(first))
    output.update(dict(second))
    return tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in output.items()
            if coefficient
        )
    )


def subtract(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    output: Counter[int] = Counter(dict(first))
    output.subtract(dict(second))
    return tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in output.items()
            if coefficient
        )
    )


def negate(
    signature: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    return tuple(
        (variable, -coefficient)
        for variable, coefficient in signature
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--prefix", type=int, default=100000)
    parser.add_argument(
        "--max-pair-sum-relations",
        type=int,
        default=1000,
        help="materialize pair sums only below this signed relation count",
    )
    parser.add_argument(
        "--max-stream-checks",
        type=int,
        default=5_000_000,
        help="maximum streamed 3-sum dictionary probes",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_sparse_transport_prefix.json"
        ),
    )
    args = parser.parse_args()
    if not 1 <= args.prefix <= 3**N:
        raise ValueError("prefix must lie in [1,3^14]")
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    singleton_matchings = [
        tuple(tuple(map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = perfect_matchings(N, full_edges | set(labels))
    started = time.perf_counter()
    indices = np.arange(args.prefix, dtype=np.int64)
    colours = np.empty((args.prefix, N), dtype=np.uint8)
    for vertex in range(N):
        colours[:, vertex] = (indices // (3**vertex)) % 3
    counts = np.zeros(args.prefix, dtype=np.int16)
    slots = [
        np.full(args.prefix, -1, dtype=np.int16)
        for _ in range(3)
    ]
    for matching_id, matching in enumerate(matchings):
        active = np.ones(args.prefix, dtype=bool)
        for item in matching:
            if item not in labels:
                continue
            colour = labels[item]
            active &= colours[:, item[0]] == colour
            active &= colours[:, item[1]] == colour
        for position in range(3):
            slots[position][active & (counts == position)] = matching_id
        counts += active
    monochromatic = np.all(colours == colours[:, :1], axis=1)
    binomials = np.flatnonzero((counts == 2) & ~monochromatic)
    trinomials = np.flatnonzero((counts == 3) & ~monochromatic)
    grouped: dict[
        tuple[int, int],
        dict[tuple[tuple[int, int], ...], int],
    ] = {}
    for equation in binomials:
        first = int(slots[0][equation])
        second = int(slots[1][equation])
        signature = oriented_signature(
            matchings[first],
            matchings[second],
            colours[equation],
            full_edges,
            labels,
        )
        grouped.setdefault((first, second), {}).setdefault(
            signature, int(equation)
        )

    certificate = None
    pair_relation_counts: dict[str, int] = {}
    pair_sum_cache: dict[
        tuple[int, int],
        dict[
            tuple[tuple[int, int], ...],
            tuple[
                tuple[tuple[int, int], ...],
                tuple[int, int],
                tuple[tuple[int, int], ...],
                tuple[int, int],
            ],
        ],
    ] = {}
    signed_cache: dict[
        tuple[int, int],
        dict[tuple[tuple[int, int], ...], tuple[int, int]],
    ] = {}
    stream_checks = 0
    stream_limit_reached = False
    for target in trinomials:
        activity = [int(slot[target]) for slot in slots]
        for first, second in itertools.combinations(activity, 2):
            pair = (first, second)
            relations = grouped.get(pair)
            if not relations:
                continue
            target_signature = oriented_signature(
                matchings[first],
                matchings[second],
                colours[target],
                full_edges,
                labels,
            )
            signed = signed_cache.get(pair)
            if signed is None:
                signed = {}
                for signature, origin in relations.items():
                    signed.setdefault(signature, (origin, 1))
                    signed.setdefault(negate(signature), (origin, -1))
                signed_cache[pair] = signed
                pair_relation_counts[
                    f"{first},{second}"
                ] = len(relations)
            if target_signature in signed:
                origin, sign = signed[target_signature]
                origins = [(origin, sign)]
            else:
                origins = []
                if len(signed) <= args.max_pair_sum_relations:
                    pair_sums = pair_sum_cache.get(pair)
                    if pair_sums is None:
                        pair_sums = {}
                        items = list(signed.items())
                        for first_signature, first_origin in items:
                            for second_signature, second_origin in items:
                                pair_sums.setdefault(
                                    add(
                                        first_signature,
                                        second_signature,
                                    ),
                                    (
                                        first_signature,
                                        first_origin,
                                        second_signature,
                                        second_origin,
                                    ),
                                )
                        pair_sum_cache[pair] = pair_sums
                    for third_signature, third_origin in signed.items():
                        needed = subtract(
                            target_signature, third_signature
                        )
                        if needed not in pair_sums:
                            continue
                        (
                            _first_signature,
                            first_origin,
                            _second_signature,
                            second_origin,
                        ) = pair_sums[needed]
                        origins = [
                            first_origin,
                            second_origin,
                            third_origin,
                        ]
                        break
                else:
                    signed_items = list(signed.items())
                    for third_signature, third_origin in signed_items:
                        needed_two = subtract(
                            target_signature, third_signature
                        )
                        for first_signature, first_origin in signed_items:
                            stream_checks += 1
                            second_signature = subtract(
                                needed_two, first_signature
                            )
                            if second_signature in signed:
                                origins = [
                                    first_origin,
                                    signed[second_signature],
                                    third_origin,
                                ]
                                break
                            if stream_checks >= args.max_stream_checks:
                                stream_limit_reached = True
                                break
                        if origins or stream_limit_reached:
                            break
            if not origins:
                continue
            survivor_id = next(
                item for item in activity if item not in {first, second}
            )
            certificate = {
                "certificate_mode": (
                    "one_binomial_pair_trinomial"
                    if len(origins) == 1
                    else "three_binomial_transport_pair_trinomial"
                ),
                "transport_binomial_equation_indices": [
                    int(origin) for origin, _sign in origins
                ],
                "transport_relation_signs": [
                    int(sign) for _origin, sign in origins
                ],
                "transport_binomial_activities": [
                    [
                        int(slots[0][origin]),
                        int(slots[1][origin]),
                    ]
                    for origin, _sign in origins
                ],
                "target_equation_index": int(target),
                "target_colouring": list(
                    map(int, colours[target])
                ),
                "target_activity": activity,
                "paired_matching_indices": [first, second],
                "surviving_matching_index": survivor_id,
                "target_relation_signature": [
                    list(item) for item in target_signature
                ],
            }
            break
        if certificate is not None:
            break
        if stream_limit_reached:
            break
    payload = {
        "status": (
            "direct_sparse_transport_contradiction"
            if certificate is not None
            else "prefix_transport_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "prefix": args.prefix,
        "skeleton_perfect_matchings": len(matchings),
        "binomial_forbidden_colourings": len(binomials),
        "trinomial_forbidden_colourings": len(trinomials),
        "binomial_matching_pairs": len(grouped),
        "pair_relation_counts_examined": pair_relation_counts,
        "stream_dictionary_checks": stream_checks,
        "stream_limit_reached": stream_limit_reached,
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
