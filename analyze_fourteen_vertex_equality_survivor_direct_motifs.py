"""Run the exact 3^14 direct-motif scan on a generic order-14 survivor."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np

import analyze_fourteen_vertex_full_direct_motifs as engine
from explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--survivor-key", default="survivors")
    parser.add_argument(
        "--maximum-certificates",
        type=int,
        default=1,
        help="maximum direct transports to save; use 0 to save all",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_survivor_direct_motifs.json"
        ),
    )
    args = parser.parse_args()
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration[args.survivor_key][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    # The mature scanner is parameterized through these module-level factor
    # constants.  N, the equation cube, and the complete-edge index stay 14.
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = full_edges
    singleton_matchings = [
        tuple(engine.edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = engine.perfect_matchings(set(full_edges) | set(labels))
    started = time.perf_counter()
    counts, first, second, third, total_extensions = (
        engine.activity_arrays(matchings, labels)
    )
    monochromatic = np.array(
        [
            sum(
                colour * (3**vertex)
                for vertex in range(engine.N)
            )
            for colour in range(3)
        ],
        dtype=np.int64,
    )
    counts[monochromatic] = -1
    activity_histogram = {
        str(activity): int(np.count_nonzero(counts == activity))
        for activity in range(int(counts.max()) + 1)
        if np.any(counts == activity)
    }
    one_term = np.flatnonzero(counts == 1)
    binomial = np.flatnonzero(counts == 2)
    trinomial = np.flatnonzero(counts == 3)
    if len(one_term):
        equation = int(one_term[0])
        matching_id = int(first[equation])
        colouring = engine.indexed_colouring(equation)
        certificate = {
            "certificate_mode": "forbidden_one_term",
            "target_equation_index": equation,
            "target_colouring": list(colouring),
            "active_matching": matching_id,
            "active_matching_edges": [
                list(item) for item in matchings[matching_id]
            ],
            "active_singleton_edges": [
                list(item)
                for item, colour in labels.items()
                if colouring[item[0]] == colouring[item[1]] == colour
            ],
        }
        origins = {}
        certificates = [certificate]
    else:
        origins = engine.unique_relation_origins(
            binomial, first, second, matchings, labels
        )
        certificates = []
        id_arrays = (first, second, third)
        seen = set()
        for left_position, right_position in itertools.combinations(
            range(3), 2
        ):
            targets = engine.unique_relation_origins(
                trinomial,
                id_arrays[left_position],
                id_arrays[right_position],
                matchings,
                labels,
            )
            for signature, equation in targets.items():
                if signature not in origins:
                    continue
                origin = int(origins[signature])
                equation = int(equation)
                key = (
                    origin,
                    equation,
                    left_position,
                    right_position,
                )
                if key in seen:
                    continue
                seen.add(key)
                activity = [
                    int(first[equation]),
                    int(second[equation]),
                    int(third[equation]),
                ]
                paired = [
                    activity[left_position],
                    activity[right_position],
                ]
                survivor_id = next(
                    item for item in activity if item not in paired
                )
                certificates.append(
                    {
                        "origin_equation_index": origin,
                        "target_equation_index": equation,
                        "target_activity": activity,
                        "target_paired_matchings": paired,
                        "target_surviving_matching": survivor_id,
                        "relation_signature": [
                            list(item) for item in signature
                        ],
                    }
                )
                if (
                    args.maximum_certificates
                    and len(certificates)
                    >= args.maximum_certificates
                ):
                    break
            if (
                args.maximum_certificates
                and len(certificates) >= args.maximum_certificates
            ):
                break
        certificate = certificates[0] if certificates else None
    payload = {
        "status": (
            "direct_contradiction"
            if certificate is not None
            else "full_direct_motif_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": engine.EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "forbidden_activity_histogram": activity_histogram,
        "zero_term_forbidden_colourings": int(
            np.count_nonzero(counts == 0)
        ),
        "one_term_forbidden_colourings": int(
            len(one_term)
        ),
        "binomial_forbidden_colourings": len(binomial),
        "trinomial_forbidden_colourings": len(trinomial),
        "distinct_binomial_relations": len(origins),
        "direct_certificate_count": len(certificates),
        "elapsed_seconds": time.perf_counter() - started,
        "certificate": certificate,
        "certificates": certificates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
