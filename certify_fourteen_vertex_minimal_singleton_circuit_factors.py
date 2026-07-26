"""Classify order-14 singleton factors by the circuit-rectangle theorem.

For one fixed all-even full factor, enumerate every edge-disjoint singleton
perfect matching.  A factor is obstructed if it contains a proper,
positive-minimal feasible subset touching every full cycle which is not an
adjacent-port component cycle.

The output is a compact catalogue: factors are addressed by their index in
the independently reproducible lexicographic perfect-matching enumeration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def contiguous_cycles(lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    cycles = []
    start = 0
    for length in lengths:
        cycles.append(tuple(range(start, start + length)))
        start += length
    return tuple(cycles)


def cycle_edges(cycle: tuple[int, ...]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def perfect_matchings(n: int) -> list[Factor]:
    output: list[Factor] = []

    def visit(remaining: int, chosen: Factor) -> None:
        if not remaining:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        tail = remaining ^ first_bit
        candidates = tail
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                tail ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << n) - 1, ())
    return output


def eligible_factor_digest(factors: list[Factor]) -> str:
    digest = hashlib.sha256()
    for factor in factors:
        digest.update(
            (";".join(f"{a}-{b}" for a, b in factor) + "\n").encode()
        )
    return digest.hexdigest()


def local_data(cycle: tuple[int, ...]):
    positions = {vertex: index for index, vertex in enumerate(cycle)}
    feasible = set()
    adjacent = set()
    length = len(cycle)
    for mask in range(1 << length):
        deleted = [
            index for index in range(length) if mask & (1 << index)
        ]
        if not deleted or all(
            (
                (deleted[(index + 1) % len(deleted)] - deleted[index])
                % length
            )
            % 2
            for index in range(len(deleted))
        ):
            feasible.add(mask)
    for index in range(length):
        adjacent.add(
            (1 << index) | (1 << ((index + 1) % length))
        )
    return positions, feasible, adjacent


def classify_factor(
    factor: Factor,
    cycles: tuple[tuple[int, ...], ...],
    cycle_data,
) -> tuple[list[dict[str, int]], int, int, int]:
    edge_masks = [
        (1 << first) | (1 << second) for first, second in factor
    ]
    deleted_masks = [0] * (1 << len(factor))
    minimal_feasible: list[int] = []
    rectangle_records: list[dict[str, int]] = []
    rectangle_count = 0
    portal_count = 0
    full_minimal_count = 0
    full_subset = (1 << len(factor)) - 1
    for subset in range(1, 1 << len(factor)):
        last_bit = subset & -subset
        edge_id = last_bit.bit_length() - 1
        deleted_masks[subset] = (
            deleted_masks[subset ^ last_bit] | edge_masks[edge_id]
        )
        local_masks = []
        for positions, feasible, _adjacent in cycle_data:
            local_mask = 0
            for vertex, position in positions.items():
                if deleted_masks[subset] & (1 << vertex):
                    local_mask |= 1 << position
            if local_mask not in feasible:
                break
            local_masks.append(local_mask)
        else:
            if any(
                (previous & subset) == previous
                for previous in minimal_feasible
            ):
                continue
            minimal_feasible.append(subset)
            if any(local_mask == 0 for local_mask in local_masks):
                continue
            if subset == full_subset:
                full_minimal_count += 1
                continue
            exceptional = all(
                local_mask.bit_count() == 2
                and local_mask in adjacent
                for local_mask, (
                    _positions,
                    _feasible,
                    adjacent,
                ) in zip(local_masks, cycle_data, strict=True)
            )
            if exceptional:
                portal_count += 1
                continue
            rectangle_count += 1
            witness_cycle = next(
                cycle_id
                for cycle_id, (
                    local_mask,
                    (_positions, _feasible, adjacent),
                ) in enumerate(
                    zip(local_masks, cycle_data, strict=True)
                )
                if not (
                    local_mask.bit_count() == 2
                    and local_mask in adjacent
                )
            )
            if not rectangle_records:
                rectangle_records.append(
                    {
                        "subset_mask": subset,
                        "witness_cycle": witness_cycle,
                        "witness_deleted_mask": local_masks[
                            witness_cycle
                        ],
                    }
                )
    return (
        rectangle_records,
        rectangle_count,
        portal_count,
        full_minimal_count,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    lengths = tuple(map(int, args.partition.split(",")))
    if (
        sum(lengths) != 14
        or any(length < 4 or length % 2 for length in lengths)
    ):
        raise ValueError("partition must be all-even and sum to 14")
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    cycle_data = tuple(local_data(cycle) for cycle in cycles)

    started = time.perf_counter()
    all_matchings = perfect_matchings(14)
    factors = [
        factor
        for factor in all_matchings
        if not (set(factor) & set(full_edges))
    ]
    obstructed_records = []
    rectangle_certificates = 0
    portal_certificates = 0
    full_minimal_sets = 0
    factors_with_portals = 0
    for factor_index, factor in enumerate(factors):
        records, rectangles, portals, full_sets = classify_factor(
            factor, cycles, cycle_data
        )
        rectangle_certificates += rectangles
        portal_certificates += portals
        full_minimal_sets += full_sets
        factors_with_portals += bool(portals)
        if records:
            obstructed_records.append(
                {
                    "factor_index": factor_index,
                    **records[0],
                }
            )

    obstructed_indices = {
        int(record["factor_index"]) for record in obstructed_records
    }
    payload = {
        "status": (
            "fourteen_vertex_minimal_singleton_circuit_factor_census"
        ),
        "scope": (
            "every singleton perfect matching edge-disjoint from the "
            "pinned all-even full factor"
        ),
        "partition": list(lengths),
        "full_cycles": [list(cycle) for cycle in cycles],
        "full_edges": [list(item) for item in sorted(full_edges)],
        "all_k14_perfect_matchings": len(all_matchings),
        "eligible_singleton_factors": len(factors),
        "eligible_factor_enumeration": (
            "lexicographic low-vertex perfect-matching recursion, filtered "
            "by full-edge disjointness"
        ),
        "eligible_factor_sha256": eligible_factor_digest(factors),
        "rectangle_obstructed_factors": len(obstructed_records),
        "rectangle_safe_factors": len(factors) - len(obstructed_records),
        "factors_with_adjacent_port_circuits": factors_with_portals,
        "rectangle_minimal_sets": rectangle_certificates,
        "adjacent_port_minimal_sets": portal_certificates,
        "full_factor_minimal_sets_ignored": full_minimal_sets,
        "obstructed_factor_records": obstructed_records,
        "safe_factor_indices": [
            index
            for index in range(len(factors))
            if index not in obstructed_indices
        ],
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_verified": True,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key
                not in {
                    "obstructed_factor_records",
                    "safe_factor_indices",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
