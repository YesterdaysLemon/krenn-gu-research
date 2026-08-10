"""Find connected equality-support triples from a factor-orbit census."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    completion_tables,
    contiguous_cycles,
    factor_safe,
)
from explore_random_even_cycle_forks import cycle_edges, perfect_matchings

Edge = tuple[int, int]
Factor = tuple[Edge, ...]


def connected(edges: set[Edge]) -> bool:
    reached = {0}
    changed = True
    while changed:
        changed = False
        for first, second in edges:
            if first in reached and second not in reached:
                reached.add(second)
                changed = True
            elif second in reached and first not in reached:
                reached.add(first)
                changed = True
    return len(reached) == N


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_connected_samples.json"
        ),
    )
    args = parser.parse_args()
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    vertex_component = {
        vertex: component
        for component, cycle in enumerate(cycles)
        for vertex in cycle
    }
    tables = completion_tables(cycles)
    factors = perfect_matchings(N, set(eligible_edges))
    safe_factors = [
        factor
        for factor in factors
        if factor_safe(
            factor, cycles, vertex_component, tables
        )
    ]
    edge_id = {
        item: position for position, item in enumerate(eligible_edges)
    }

    def mask(factor: Factor) -> int:
        return sum(1 << edge_id[item] for item in factor)

    factor_masks = [mask(factor) for factor in safe_factors]
    rows = []
    for orbit_id, orbit in enumerate(census["factor_orbits"]):
        first = tuple(
            tuple(map(int, item)) for item in orbit["representative"]
        )
        first_mask = mask(first)
        connected_sample = None
        seconds_examined = 0
        thirds_examined = 0
        for second_id, second in enumerate(safe_factors):
            second_mask = factor_masks[second_id]
            if first_mask & second_mask:
                continue
            seconds_examined += 1
            selected_mask = first_mask | second_mask
            selected_edges = full_edges | set(first) | set(second)
            for third_id, third in enumerate(safe_factors):
                if selected_mask & factor_masks[third_id]:
                    continue
                thirds_examined += 1
                if connected(selected_edges | set(third)):
                    connected_sample = {
                        "first": [list(item) for item in first],
                        "second": [list(item) for item in second],
                        "third": [list(item) for item in third],
                    }
                    break
            if connected_sample is not None:
                break
        rows.append(
            {
                "orbit_id": orbit_id,
                "orbit_size": int(orbit["orbit_size"]),
                "seconds_examined": seconds_examined,
                "thirds_examined": thirds_examined,
                "connected_support_found": connected_sample is not None,
                "connected_support": connected_sample,
            }
        )
        print(
            f"orbit={orbit_id} connected={connected_sample is not None} "
            f"seconds={seconds_examined} thirds={thirds_examined}",
            flush=True,
        )

    payload = {
        "status": "connectivity_probe_complete",
        "necessary_conditions_only": True,
        "partition": list(lengths),
        "eligible_singleton_factors": len(factors),
        "individually_one_term_free_factors": len(safe_factors),
        "factor_orbits": len(census["factor_orbits"]),
        "orbits_with_connected_support": sum(
            row["connected_support_found"] for row in rows
        ),
        "survivors": [
            row["connected_support"]
            for row in rows
            if row["connected_support"] is not None
        ],
        "orbit_rows": rows,
        "exploratory_only": True,
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
                if key != "orbit_rows"
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
