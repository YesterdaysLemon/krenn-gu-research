"""Sample equality supports for direct even-cycle amplitude forks.

For an equality support, three coloured diagonal singleton perfect matchings
are disjoint from a full-block 2-factor.  If the 2-factor has ``k`` even
cycles, a colouring with only the ``2^k`` full-only matchings factors into
``k`` alternating-cycle choices.

One such choice is ruled out by a colouring with exactly one additional
non-full matching and the same colours on that cycle: the full-only terms
cancel in pairs and the extra nonzero monomial survives.  This exploratory
script tests whether a base colouring exists for which every cycle choice
has such a unary obstruction.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import time
from pathlib import Path
from typing import Sequence

import numpy as np

Edge = tuple[int, int]


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def perfect_matchings(
    n: int, allowed: set[Edge] | None = None
) -> list[tuple[Edge, ...]]:
    adjacency = {
        vertex: {
            other
            for other in range(n)
            if other != vertex
            and (
                allowed is None
                or edge(vertex, other) in allowed
            )
        }
        for vertex in range(n)
    }
    result: list[tuple[Edge, ...]] = []

    def visit(remaining: frozenset[int], chosen: tuple[Edge, ...]) -> None:
        if not remaining:
            result.append(chosen)
            return
        first = min(remaining)
        for second in sorted(adjacency[first] & remaining):
            visit(
                remaining - {first, second},
                (*chosen, edge(first, second)),
            )

    visit(frozenset(range(n)), ())
    return result


def random_singletons(
    n: int,
    full_edges: frozenset[Edge],
    rng: random.Random,
) -> tuple[tuple[Edge, ...], ...]:
    candidates = [
        matching
        for matching in perfect_matchings(n)
        if not (set(matching) & set(full_edges))
    ]
    for _attempt in range(10_000):
        first = rng.choice(candidates)
        second_candidates = [
            matching
            for matching in candidates
            if not (set(matching) & set(first))
        ]
        if not second_candidates:
            continue
        second = rng.choice(second_candidates)
        third_candidates = [
            matching
            for matching in second_candidates
            if not (set(matching) & set(second))
        ]
        if third_candidates:
            return first, second, rng.choice(third_candidates)
    raise RuntimeError("failed to sample three disjoint singleton matchings")


def colouring_table(n: int) -> np.ndarray:
    indices = np.arange(3**n, dtype=np.int64)
    table = np.empty((3**n, n), dtype=np.int8)
    for vertex in range(n):
        table[:, vertex] = (indices // (3**vertex)) % 3
    return table


def local_codes(
    colourings: np.ndarray, cycle: Sequence[int]
) -> np.ndarray:
    code = np.zeros(len(colourings), dtype=np.int32)
    for position, vertex in enumerate(cycle):
        code += (
            colourings[:, int(vertex)].astype(np.int32)
            * (3**position)
        )
    return code


def two_matching_base_indices(
    n: int,
    singletons: Sequence[Sequence[Edge]],
) -> list[int]:
    """Return bipartition colourings for every pair of singleton colours."""
    indices: set[int] = set()
    for first_colour, second_colour in itertools.combinations(range(3), 2):
        adjacency = {vertex: set() for vertex in range(n)}
        for matching in (
            singletons[first_colour],
            singletons[second_colour],
        ):
            for first, second in matching:
                adjacency[first].add(second)
                adjacency[second].add(first)
        unseen = set(range(n))
        components: list[dict[int, int]] = []
        while unseen:
            start = min(unseen)
            sides = {start: 0}
            stack = [start]
            while stack:
                vertex = stack.pop()
                for other in adjacency[vertex]:
                    expected = 1 - sides[vertex]
                    if other in sides:
                        if sides[other] != expected:
                            raise AssertionError(
                                "two perfect matchings have an odd component"
                            )
                        continue
                    sides[other] = expected
                    stack.append(other)
            unseen -= set(sides)
            components.append(sides)
        for flips in itertools.product((0, 1), repeat=len(components)):
            colouring = [0] * n
            for flip, component in zip(
                flips, components, strict=True
            ):
                for vertex, side in component.items():
                    colouring[vertex] = (
                        first_colour
                        if side ^ flip == 0
                        else second_colour
                    )
            indices.add(
                sum(
                    colouring[vertex] * (3**vertex)
                    for vertex in range(n)
                )
            )
    return sorted(indices)


def analyze_support(
    n: int,
    cycles: Sequence[Sequence[int]],
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
    colourings: np.ndarray,
) -> dict[str, object]:
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    if len(labels) != 3 * n // 2:
        raise AssertionError("singleton matchings overlap")
    skeleton = set(full_edges) | set(labels)
    if any(
        sum(vertex in item for item in skeleton) != 5
        for vertex in range(n)
    ):
        raise AssertionError("sampled skeleton is not 5-regular")
    matchings = perfect_matchings(n, skeleton)
    active_count = np.zeros(len(colourings), dtype=np.int16)
    full_only = 0
    viable_nonfull = 0
    for matching in matchings:
        requirements: dict[int, int] = {}
        viable = True
        for item in matching:
            if item not in labels:
                continue
            colour = labels[item]
            for vertex in item:
                if (
                    vertex in requirements
                    and requirements[vertex] != colour
                ):
                    viable = False
                    break
                requirements[vertex] = colour
            if not viable:
                break
        if not viable:
            continue
        mask = np.ones(len(colourings), dtype=bool)
        for vertex, colour in requirements.items():
            mask &= colourings[:, vertex] == colour
        active_count += mask
        if not requirements:
            full_only += 1
        else:
            viable_nonfull += 1
    expected_full_only = 2 ** len(cycles)
    if full_only != expected_full_only:
        raise AssertionError(
            f"expected {expected_full_only} full-only matchings, got "
            f"{full_only}"
        )
    monochromatic = np.all(
        colourings == colourings[:, :1], axis=1
    )
    unary_mask = (active_count == full_only + 1) & ~monochromatic
    base_mask = (active_count == full_only) & ~monochromatic
    codes = [local_codes(colourings, cycle) for cycle in cycles]
    forbidden: list[np.ndarray] = []
    for cycle, code in zip(cycles, codes, strict=True):
        values = np.zeros(3 ** len(cycle), dtype=bool)
        values[np.unique(code[unary_mask])] = True
        forbidden.append(values)
    fork_mask = base_mask.copy()
    for code, values in zip(codes, forbidden, strict=True):
        fork_mask &= values[code]
    fork_indices = np.flatnonzero(fork_mask)
    structured_indices = two_matching_base_indices(n, singletons)
    if any(not base_mask[index] for index in structured_indices):
        raise AssertionError(
            "two-matching bipartition did not suppress singleton edges"
        )
    structured_forks = [
        index for index in structured_indices if fork_mask[index]
    ]
    witness: dict[str, object] | None = None
    if len(fork_indices):
        base = int(fork_indices[0])
        alternatives: list[dict[str, object]] = []
        for cycle, code, values in zip(
            cycles, codes, forbidden, strict=True
        ):
            local_code = int(code[base])
            candidates = np.flatnonzero(
                unary_mask & (code == local_code)
            )
            if not len(candidates) or not values[local_code]:
                raise AssertionError("fork alternative disappeared")
            target = int(candidates[0])
            alternatives.append(
                {
                    "cycle": list(map(int, cycle)),
                    "target_colouring_index": target,
                    "target_colouring": list(
                        map(int, colourings[target])
                    ),
                }
            )
        witness = {
            "base_colouring_index": base,
            "base_colouring": list(map(int, colourings[base])),
            "alternatives": alternatives,
        }
    return {
        "skeleton_perfect_matchings": len(matchings),
        "viable_nonfull_matchings": viable_nonfull,
        "full_only_matchings": full_only,
        "base_colouring_count": int(np.count_nonzero(base_mask)),
        "one_extra_colouring_count": int(
            np.count_nonzero(unary_mask)
        ),
        "fork_colouring_count": int(np.count_nonzero(fork_mask)),
        "structured_base_colourings": len(structured_indices),
        "structured_fork_colourings": len(structured_forks),
        "fork_found": witness is not None,
        "fork": witness,
    }


def cycle_partition(n: int, lengths: Sequence[int]) -> list[list[int]]:
    if sum(lengths) != n:
        raise ValueError("cycle lengths do not sum to n")
    output: list[list[int]] = []
    start = 0
    for length in lengths:
        output.append(list(range(start, start + length)))
        start += length
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--cycles", default="4,6")
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/random_even_cycle_forks.json"),
    )
    args = parser.parse_args()
    lengths = tuple(map(int, args.cycles.split(",")))
    if any(length % 2 or length < 4 for length in lengths):
        raise ValueError("all sampled cycles must be even and at least four")
    cycles = cycle_partition(args.n, lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    rng = random.Random(args.seed)
    colourings = colouring_table(args.n)
    rows: list[dict[str, object]] = []
    started = time.perf_counter()
    for sample in range(args.samples):
        singletons = random_singletons(args.n, full_edges, rng)
        row = analyze_support(
            args.n, cycles, full_edges, singletons, colourings
        )
        row["sample"] = sample
        row["singleton_matchings"] = [
            [list(item) for item in matching]
            for matching in singletons
        ]
        rows.append(row)
        print(
            f"sample={sample + 1}/{args.samples} "
            f"fork={row['fork_found']} "
            f"bases={row['base_colouring_count']} "
            f"forks={row['fork_colouring_count']}",
            flush=True,
        )
    payload = {
        "scope": (
            "exploratory random equality-support census for direct "
            "even-cycle amplitude forks"
        ),
        "necessary_conditions_only": True,
        "n": args.n,
        "d": 3,
        "cycle_type": list(lengths),
        "samples": len(rows),
        "forks_found": sum(bool(row["fork_found"]) for row in rows),
        "seed": args.seed,
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
