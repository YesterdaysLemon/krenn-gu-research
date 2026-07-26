"""Independent audit of an n=14 support with no one-term amplitude.

This refutes only a proposed extension of the one-term theorem to mixed
odd/even full factors.  It is not a Krenn--Gu witness.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

N = 14
Edge = tuple[int, int]
CYCLES = (
    (0, 1, 2),
    (3, 4, 5, 6),
    (7, 8, 9, 10, 11, 12, 13),
)


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def perfect_matchings(
    allowed: set[Edge],
) -> list[tuple[Edge, ...]]:
    adjacency = {
        vertex: {
            other
            for other in range(N)
            if other != vertex and edge(vertex, other) in allowed
        }
        for vertex in range(N)
    }
    output: list[tuple[Edge, ...]] = []

    def visit(remaining: frozenset[int], chosen: tuple[Edge, ...]) -> None:
        if not remaining:
            output.append(chosen)
            return
        first = min(remaining)
        for second in sorted(adjacency[first] & remaining):
            visit(
                remaining - {first, second},
                (*chosen, edge(first, second)),
            )

    visit(frozenset(range(N)), ())
    return output


def is_perfect_matching(items: Sequence[Edge]) -> bool:
    return (
        len(items) == N // 2
        and sorted(vertex for item in items for vertex in item)
        == list(range(N))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path(
            "tmp/minimal_singleton_counterexample_search_small.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_no_one_term_support_verified.json"
        ),
    )
    args = parser.parse_args()
    candidate = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    if candidate.get("full_cycle_type") != [3, 4, 7]:
        raise AssertionError("candidate full-factor type changed")
    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in matching)
        for matching in candidate["best_singleton_matchings"]
    ]
    if len(singleton_matchings) != 3:
        raise AssertionError("candidate has the wrong number of colours")
    if any(
        not is_perfect_matching(matching)
        for matching in singleton_matchings
    ):
        raise AssertionError("singleton colour class is not a matching")
    singleton_edges = {
        item
        for matching in singleton_matchings
        for item in matching
    }
    if len(singleton_edges) != 3 * N // 2:
        raise AssertionError("singleton colour classes overlap")
    if singleton_edges & set(FULL_EDGES):
        raise AssertionError("singleton and full edges overlap")
    skeleton = set(FULL_EDGES) | singleton_edges
    if any(
        sum(vertex in item for item in skeleton) != 5
        for vertex in range(N)
    ):
        raise AssertionError("support skeleton is not 5-regular")

    matchings = perfect_matchings(skeleton)
    representatives: dict[
        frozenset[Edge], tuple[Edge, ...]
    ] = {}
    for matching in matchings:
        target = frozenset(set(matching) & singleton_edges)
        representatives.setdefault(target, matching)
    feasible = set(representatives)
    minimal = {
        target
        for target in feasible
        if not any(other < target for other in feasible)
    }
    cycle_sets = [set(cycle) for cycle in CYCLES]

    def touch_pattern(target: frozenset[Edge]) -> tuple[bool, ...]:
        vertices = {
            vertex for item in target for vertex in item
        }
        return tuple(bool(vertices & cycle) for cycle in cycle_sets)

    if len(matchings) != 267:
        raise AssertionError("skeleton perfect-matching count changed")
    if len(feasible) != 242:
        raise AssertionError("feasible singleton-set count changed")
    if len(minimal) != 9:
        raise AssertionError("minimal singleton-set count changed")
    if {len(target) for target in minimal} != {1}:
        raise AssertionError("minimal sets are no longer unary")
    if {touch_pattern(target) for target in minimal} != {
        (True, False, True)
    }:
        raise AssertionError("minimal touch pattern changed")

    alternative_modes: Counter[str] = Counter()
    for matching in matchings:
        target = frozenset(set(matching) & singleton_edges)
        if target in minimal:
            # The untouched C4 has two alternating full-edge matchings.
            cycle = CYCLES[1]
            cycle_set = set(cycle_edges(cycle))
            used = set(matching) & cycle_set
            if len(used) != 2:
                raise AssertionError("minimal matching does not span C4")
            alternative = tuple(
                sorted((set(matching) - used) | (cycle_set - used))
            )
            mode = "untouched_even_cycle_flip"
        else:
            smaller = next(
                other for other in feasible if other < target
            )
            alternative = representatives[smaller]
            mode = "proper_feasible_singleton_subset"
        if tuple(sorted(matching)) == tuple(sorted(alternative)):
            raise AssertionError("alternative matching did not change")
        if not is_perfect_matching(alternative):
            raise AssertionError("constructed alternative is not perfect")
        if not set(alternative) <= set(FULL_EDGES) | set(target):
            raise AssertionError(
                "alternative is not active whenever the target is active"
            )
        alternative_modes[mode] += 1

    payload = {
        "verified": True,
        "scope": (
            "one explicit n=14,d=3 C3+C4+C7 equality support has no "
            "forbidden one-term amplitude"
        ),
        "claim_scope": (
            "refutes only the proposed universal one-term extension; "
            "does not satisfy the Krenn--Gu equations and is not a "
            "counterexample to the conjecture"
        ),
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "full_cycle_type": [3, 4, 7],
        "skeleton_perfect_matchings": len(matchings),
        "distinct_feasible_singleton_sets": len(feasible),
        "inclusion_minimal_singleton_sets": len(minimal),
        "minimal_singleton_set_sizes": sorted(
            {len(target) for target in minimal}
        ),
        "minimal_touch_patterns": [
            list(pattern)
            for pattern in sorted(
                {touch_pattern(target) for target in minimal}
            )
        ],
        "verified_matching_alternatives": len(matchings),
        "alternative_modes": dict(sorted(alternative_modes.items())),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
