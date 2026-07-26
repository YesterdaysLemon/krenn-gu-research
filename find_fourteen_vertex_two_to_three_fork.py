"""Find a colour-feasible stable-C4 two-to-three fork in one support."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path
from typing import Sequence

from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
)
from explore_random_even_cycle_forks import cycle_edges, perfect_matchings

Edge = tuple[int, int]


def indexed_colouring(colouring: Sequence[int]) -> int:
    return sum(
        int(colour) * (3**vertex)
        for vertex, colour in enumerate(colouring)
    )


def solve_colouring(
    labelled_edges: dict[Edge, int],
    active_edges: set[Edge],
    fixed: dict[int, int],
) -> tuple[int, ...] | None:
    assigned: list[int | None] = [None] * N
    for vertex, colour in fixed.items():
        assigned[vertex] = colour
    for item in active_edges:
        colour = labelled_edges[item]
        for vertex in item:
            if assigned[vertex] not in {None, colour}:
                return None
            assigned[vertex] = colour
    forbidden = [
        (first, second, colour)
        for (first, second), colour in labelled_edges.items()
        if (first, second) not in active_edges
    ]
    incident = {
        vertex: [
            constraint
            for constraint in forbidden
            if vertex in constraint[:2]
        ]
        for vertex in range(N)
    }

    def consistent(vertex: int) -> bool:
        return all(
            not (
                assigned[first] == assigned[second] == colour
            )
            for first, second, colour in incident[vertex]
            if assigned[first] is not None
            and assigned[second] is not None
        )

    if any(
        not consistent(vertex)
        for vertex in range(N)
        if assigned[vertex] is not None
    ):
        return None

    def visit() -> bool:
        unassigned = [
            vertex
            for vertex in range(N)
            if assigned[vertex] is None
        ]
        if not unassigned:
            return True
        vertex = max(
            unassigned,
            key=lambda item: sum(
                assigned[first if second == item else second]
                is not None
                for first, second, _colour in incident[item]
            ),
        )
        for colour in range(3):
            assigned[vertex] = colour
            if consistent(vertex) and visit():
                return True
        assigned[vertex] = None
        return False

    if not visit():
        return None
    return tuple(int(colour) for colour in assigned)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("support_manifest", type=Path)
    parser.add_argument("fork_catalogue", type=Path)
    parser.add_argument("--support-key", default="survivors")
    parser.add_argument("--support-index", type=int, default=0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_to_three_fork_found.json"
        ),
    )
    args = parser.parse_args()
    manifest = json.loads(
        args.support_manifest.read_text(encoding="utf-8")
    )
    catalogue = json.loads(
        args.fork_catalogue.read_text(encoding="utf-8")
    )
    support = manifest[args.support_key][args.support_index]
    lengths = tuple(map(int, manifest["partition"]))
    if tuple(map(int, catalogue["partition"])) != lengths:
        raise ValueError("fork catalogue partition mismatch")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        tuple(map(int, item)) for item in catalogue["eligible_edges"]
    )
    edge_id = {
        item: position for position, item in enumerate(eligible_edges)
    }
    factors = [
        tuple(tuple(map(int, item)) for item in support[key])
        for key in ("first", "second", "third")
    ]
    labelled_edges = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    support_mask = sum(
        1 << edge_id[item] for item in labelled_edges
    )

    started = time.perf_counter()
    contained = 0
    c4_assignments_scanned = 0
    certificate = None
    for row in catalogue["fork_rows"]:
        sparse_mask = int(row["sparse_mask"])
        rich_mask = int(row["rich_mask"])
        if rich_mask & support_mask != rich_mask:
            continue
        contained += 1
        sparse_edges = {
            eligible_edges[position]
            for position in range(len(eligible_edges))
            if sparse_mask & (1 << position)
        }
        rich_edges = {
            eligible_edges[position]
            for position in range(len(eligible_edges))
            if rich_mask & (1 << position)
        }
        component = int(row["alternating_c4_component"])
        c4_vertices = tuple(cycles[component])
        for c4_colours in itertools.product(range(3), repeat=4):
            c4_assignments_scanned += 1
            fixed = dict(zip(c4_vertices, c4_colours))
            origin = solve_colouring(
                labelled_edges, sparse_edges, fixed
            )
            if origin is None:
                continue
            target = solve_colouring(
                labelled_edges, rich_edges, fixed
            )
            if target is None:
                continue
            sparse_matchings = perfect_matchings(
                N, set(full_edges) | sparse_edges
            )
            rich_matchings = perfect_matchings(
                N, set(full_edges) | rich_edges
            )
            if len(sparse_matchings) != 2:
                raise AssertionError("sparse fork no longer has two terms")
            if len(rich_matchings) != 3:
                raise AssertionError("rich fork no longer has three terms")
            if not set(sparse_matchings) < set(rich_matchings):
                raise AssertionError("fork matching sets are not nested")
            symmetric = (
                set(sparse_matchings[0])
                ^ set(sparse_matchings[1])
            )
            if symmetric != set(cycle_edges(cycles[component])):
                raise AssertionError("sparse pair is not the stated C4 flip")
            surviving = next(
                matching
                for matching in rich_matchings
                if matching not in set(sparse_matchings)
            )
            certificate = {
                "certificate_mode": "stable_c4_two_to_three_fork",
                "sparse_singleton_edges": [
                    list(item) for item in sorted(sparse_edges)
                ],
                "rich_singleton_edges": [
                    list(item) for item in sorted(rich_edges)
                ],
                "alternating_c4_component": component,
                "alternating_c4_vertices": list(c4_vertices),
                "origin_colouring": list(origin),
                "target_colouring": list(target),
                "origin_equation_index": indexed_colouring(origin),
                "target_equation_index": indexed_colouring(target),
                "paired_matchings": [
                    [list(item) for item in matching]
                    for matching in sparse_matchings
                ],
                "surviving_matching": [
                    list(item) for item in surviving
                ],
            }
            break
        if certificate is not None:
            break

    payload = {
        "status": (
            "contradiction"
            if certificate is not None
            else "colour_feasible_two_to_three_fork_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "support_manifest": str(args.support_manifest),
        "support_key": args.support_key,
        "support_index": args.support_index,
        "partition": list(lengths),
        "singleton_matchings": {
            key: support[key]
            for key in ("first", "second", "third")
        },
        "catalogued_forks": len(catalogue["fork_rows"]),
        "contained_forks_scanned": contained,
        "c4_assignments_scanned": c4_assignments_scanned,
        "elapsed_seconds": time.perf_counter() - started,
        "certificate": certificate,
    }
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
                if key not in {"singleton_matchings", "certificate"}
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
