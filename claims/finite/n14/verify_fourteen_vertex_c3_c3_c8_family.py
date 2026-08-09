"""Independent proof audit for the order-14 C3+C3+C8 equality family.

The finite part exhausts every singleton perfect matching in the complement
of a fixed C3+C3+C8 factor.  It checks directly that every factor avoiding a
forbidden one-term amplitude preserves the vertex split

    {0,...,5} | {6,...,13}.

Consequently any equality support assembled from three such factors is
disconnected.  The final contradiction is then analytic: hafnian
coefficients factor across the two components, while the target tensor has
nonzero same-colour coefficients and zero different-colour component
coefficients.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

N = 14
Edge = tuple[int, int]
PARTITION = (3, 3, 8)
CYCLES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8, 9, 10, 11, 12, 13),
)
LEFT = frozenset(range(6))
RIGHT = frozenset(range(6, 14))


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
    allowed: Iterable[Edge],
) -> list[tuple[Edge, ...]]:
    """Enumerate perfect matchings by a fresh smallest-vertex recursion."""
    allowed_set = set(allowed)
    adjacency = {
        vertex: tuple(
            other
            for other in range(N)
            if other != vertex and edge(vertex, other) in allowed_set
        )
        for vertex in range(N)
    }
    output: list[tuple[Edge, ...]] = []

    def visit(remaining: int, chosen: tuple[Edge, ...]) -> None:
        if not remaining:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        for second in adjacency[first]:
            second_bit = 1 << second
            if remaining & second_bit:
                visit(
                    remaining ^ first_bit ^ second_bit,
                    (*chosen, edge(first, second)),
                )

    visit((1 << N) - 1, ())
    return output


def support_matching_masks(factor: Sequence[Edge]) -> Counter[int]:
    """Count support perfect matchings by their exact singleton-edge set."""
    factor_positions = {
        item: position for position, item in enumerate(factor)
    }
    adjacency: dict[int, list[tuple[int, int]]] = {
        vertex: [] for vertex in range(N)
    }
    for item in set(FULL_EDGES) | set(factor):
        factor_bit = (
            1 << factor_positions[item]
            if item in factor_positions
            else 0
        )
        first, second = item
        adjacency[first].append((second, factor_bit))
        adjacency[second].append((first, factor_bit))
    for rows in adjacency.values():
        rows.sort()

    exact: Counter[int] = Counter()

    def visit(remaining: int, singleton_mask: int) -> None:
        if not remaining:
            exact[singleton_mask] += 1
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        for second, factor_bit in adjacency[first]:
            second_bit = 1 << second
            if remaining & second_bit:
                visit(
                    remaining ^ first_bit ^ second_bit,
                    singleton_mask | factor_bit,
                )

    visit((1 << N) - 1, 0)
    return exact


def activated_matching_counts(
    exact: Counter[int],
) -> list[int]:
    """Zeta transform exact edge-use masks into activation-set counts."""
    totals = [exact.get(mask, 0) for mask in range(1 << (N // 2))]
    for bit in range(N // 2):
        for mask in range(1 << (N // 2)):
            if mask & (1 << bit):
                totals[mask] += totals[mask ^ (1 << bit)]
    return totals


def component_profile(factor: Sequence[Edge]) -> tuple[int, int, int, int]:
    """Return T0-T1, T0-C8, T1-C8, and internal-C8 edge counts."""
    first_triangle = set(CYCLES[0])
    second_triangle = set(CYCLES[1])
    even_cycle = set(CYCLES[2])
    counts = [0, 0, 0, 0]
    for first, second in factor:
        endpoints = {first, second}
        if endpoints & first_triangle and endpoints & second_triangle:
            counts[0] += 1
        elif endpoints & first_triangle and endpoints & even_cycle:
            counts[1] += 1
        elif endpoints & second_triangle and endpoints & even_cycle:
            counts[2] += 1
        elif endpoints <= even_cycle:
            counts[3] += 1
        else:
            raise AssertionError("unexpected singleton-factor edge")
    return tuple(counts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--census",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_3_8_factor_orbit_census.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c3_c8_family_verified.json"
        ),
    )
    args = parser.parse_args()

    eligible_edges = {
        edge(first, second)
        for first in range(N)
        for second in range(first + 1, N)
        if edge(first, second) not in FULL_EDGES
    }
    factors = perfect_matchings(eligible_edges)
    safe_factors: list[tuple[Edge, ...]] = []
    unsafe_witness_histogram: Counter[int] = Counter()
    support_matching_histogram: Counter[int] = Counter()

    for factor in factors:
        exact = support_matching_masks(factor)
        totals = activated_matching_counts(exact)
        bad_masks = [
            mask
            for mask in range(1, (1 << (N // 2)) - 1)
            if totals[mask] == 1
        ]
        support_matching_histogram[sum(exact.values())] += 1
        if bad_masks:
            unsafe_witness_histogram[min(map(int.bit_count, bad_masks))] += 1
        else:
            safe_factors.append(factor)

    safe_set = set(safe_factors)
    decomposed_factors = {
        factor
        for factor in factors
        if all(
            ({first, second} <= LEFT)
            or ({first, second} <= RIGHT)
            for first, second in factor
        )
    }
    if len(factors) != 44_250:
        raise AssertionError("eligible singleton-factor count changed")
    if len(safe_factors) != 186:
        raise AssertionError("one-term-free singleton-factor count changed")
    if safe_set != decomposed_factors:
        raise AssertionError(
            "one-term-free factors are not exactly the disconnected ones"
        )
    if {component_profile(factor) for factor in safe_factors} != {
        (3, 0, 0, 4)
    }:
        raise AssertionError("safe-factor component profile changed")

    triangle_parts = {
        tuple(item for item in factor if set(item) <= LEFT)
        for factor in safe_factors
    }
    even_parts = {
        tuple(item for item in factor if set(item) <= RIGHT)
        for factor in safe_factors
    }
    factor_products = {
        (
            tuple(item for item in factor if set(item) <= LEFT),
            tuple(item for item in factor if set(item) <= RIGHT),
        )
        for factor in safe_factors
    }
    if len(triangle_parts) != 6 or len(even_parts) != 31:
        raise AssertionError("decomposed factor counts changed")
    if len(factor_products) != len(triangle_parts) * len(even_parts):
        raise AssertionError("safe factors are not the full product family")
    if any(
        item[0] in LEFT and item[1] in RIGHT
        for item in FULL_EDGES
    ):
        raise AssertionError("the full factor crosses the claimed split")

    census = json.loads(args.census.read_text(encoding="utf-8"))
    expected_census = {
        "partition": list(PARTITION),
        "eligible_singleton_factors": len(factors),
        "individually_one_term_free_factors": len(safe_factors),
    }
    for key, expected in expected_census.items():
        if census.get(key) != expected:
            raise AssertionError(f"census mismatch for {key}")

    payload = {
        "verified": True,
        "status": "all_c3_c3_c8_equality_supports_closed",
        "scope": (
            "no n=14,d=3 equality-architecture witness whose full "
            "factor has cycle type C3+C3+C8"
        ),
        "claim_scope": (
            "complete for C3+C3+C8 equality supports; not the remaining "
            "order-14 factor types or the global conjecture"
        ),
        "census": str(args.census),
        "census_sha256": sha256(args.census),
        "full_cycle_type": list(PARTITION),
        "eligible_singleton_factors": len(factors),
        "one_term_unsafe_singleton_factors": (
            len(factors) - len(safe_factors)
        ),
        "one_term_free_singleton_factors": len(safe_factors),
        "one_term_witness_minimum_size_histogram": dict(
            sorted(unsafe_witness_histogram.items())
        ),
        "support_matching_count_histogram": dict(
            sorted(support_matching_histogram.items())
        ),
        "safe_factor_component_profile": [3, 0, 0, 4],
        "triangle_bijection_factors": len(triangle_parts),
        "c8_internal_factors": len(even_parts),
        "safe_factor_cartesian_product": len(factor_products),
        "preserved_vertex_split": [
            sorted(LEFT),
            sorted(RIGHT),
        ],
        "disconnected_tensor_contradiction": {
            "factorization": (
                "T(a_left,a_right)=T_left(a_left)*T_right(a_right)"
            ),
            "required_nonzero": (
                "T_left(c^6)*T_right(c^8)=1 for every colour c"
            ),
            "forbidden_nonzero": (
                "for c!=d, both factors in "
                "T_left(c^6)*T_right(d^8) are nonzero"
            ),
            "target_value": 0,
        },
        "logical_check": (
            "every admissible singleton factor preserves the same "
            "nontrivial vertex split, so every candidate skeleton is "
            "disconnected; component factorization contradicts the "
            "monochromatic target tensor"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
