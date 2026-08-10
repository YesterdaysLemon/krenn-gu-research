"""Exhaust the complete C3+C4+C7 equality-support family at order 14."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)

N = 14
CYCLES = (
    tuple(range(0, 3)),
    tuple(range(3, 7)),
    tuple(range(7, 14)),
)
FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)
ELIGIBLE_EDGES = tuple(
    item
    for item in itertools.combinations(range(N), 2)
    if item not in FULL_EDGES
)
EDGE_ID = {
    item: index for index, item in enumerate(ELIGIBLE_EDGES)
}
LOW_64 = (1 << 64) - 1


def canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def edge_mask(edges: Iterable[Edge]) -> int:
    return sum(1 << EDGE_ID[item] for item in edges)


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("perfect matching misses a vertex")


def support_matchings(singletons: Iterable[Edge]) -> list[tuple[Edge, ...]]:
    return perfect_matchings(
        N, set(FULL_EDGES) | set(singletons)
    )


def cycle_completion_tables() -> list[dict[frozenset[int], int]]:
    def count_matchings(
        remaining: frozenset[int], allowed: set[Edge]
    ) -> int:
        if not remaining:
            return 1
        first = min(remaining)
        total = 0
        for item in allowed:
            if first not in item:
                continue
            second = item[1] if item[0] == first else item[0]
            if second in remaining:
                total += count_matchings(
                    remaining - {first, second}, allowed
                )
        return total

    tables: list[dict[frozenset[int], int]] = []
    for cycle in CYCLES:
        table: dict[frozenset[int], int] = {}
        for mask in range(1 << len(cycle)):
            deleted = frozenset(
                cycle[index]
                for index in range(len(cycle))
                if mask & (1 << index)
            )
            remaining = set(cycle) - set(deleted)
            remaining_edges = {
                item
                for item in cycle_edges(cycle)
                if item[0] in remaining and item[1] in remaining
            }
            table[deleted] = count_matchings(
                frozenset(remaining), remaining_edges
            )
        tables.append(table)
    return tables


def factor_has_one_term(
    factor: Sequence[Edge],
    tables: Sequence[dict[frozenset[int], int]],
) -> bool:
    exact = [0] * (1 << (N // 2))
    for mask in range(1 << (N // 2)):
        deleted = [set(), set(), set()]
        for edge_index, item in enumerate(factor):
            if not mask & (1 << edge_index):
                continue
            for vertex in item:
                component = 0 if vertex < 3 else 1 if vertex < 7 else 2
                deleted[component].add(vertex)
        exact[mask] = (
            tables[0][frozenset(deleted[0])]
            * tables[1][frozenset(deleted[1])]
            * tables[2][frozenset(deleted[2])]
        )
    totals = exact[:]
    for bit in range(N // 2):
        for mask in range(1 << (N // 2)):
            if mask & (1 << bit):
                totals[mask] += totals[mask ^ (1 << bit)]
    full_mask = (1 << (N // 2)) - 1
    return any(
        totals[mask] == 1 for mask in range(1, full_mask)
    )


def dihedral_actions(cycle: Sequence[int]) -> list[dict[int, int]]:
    length = len(cycle)
    return [
        {
            cycle[index]: cycle[
                (rotation + (-index if reflected else index)) % length
            ]
            for index in range(length)
        }
        for reflected in (False, True)
        for rotation in range(length)
    ]


def automorphisms() -> list[dict[int, int]]:
    return [
        {**first, **second, **third}
        for first, second, third in itertools.product(
            *(dihedral_actions(cycle) for cycle in CYCLES)
        )
    ]


def transform_factor(
    factor: Sequence[Edge], permutation: dict[int, int]
) -> tuple[Edge, ...]:
    return tuple(
        sorted(
            tuple(
                sorted(
                    (permutation[first], permutation[second])
                )
            )
            for first, second in factor
        )
    )


def orbit_representatives(
    factors: Iterable[tuple[Edge, ...]],
    actions: Sequence[dict[int, int]],
) -> list[tuple[tuple[Edge, ...], int]]:
    factor_set = set(factors)
    unseen = set(factor_set)
    output: list[tuple[tuple[Edge, ...], int]] = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform_factor(representative, action)
            for action in actions
        } & factor_set
        output.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    return output


def build_bad_pairs() -> tuple[list[int], list[tuple[Edge, Edge]]]:
    bad_masks = [0] * len(ELIGIBLE_EDGES)
    bad_pairs: list[tuple[Edge, Edge]] = []
    for first_id, first in enumerate(ELIGIBLE_EDGES):
        for second_id in range(first_id + 1, len(ELIGIBLE_EDGES)):
            second = ELIGIBLE_EDGES[second_id]
            if set(first).intersection(second):
                continue
            if len(support_matchings((first, second))) != 1:
                continue
            bad_masks[first_id] |= 1 << second_id
            bad_masks[second_id] |= 1 << first_id
            bad_pairs.append((first, second))
    return bad_masks, bad_pairs


def build_fork_triples() -> list[tuple[Edge, Edge, Edge]]:
    forks: set[frozenset[Edge]] = set()
    for target in itertools.combinations(ELIGIBLE_EDGES, 3):
        if len({vertex for item in target for vertex in item}) != 6:
            continue
        rich = support_matchings(target)
        rich_set = set(rich)
        for removed in target:
            sparse = support_matchings(
                item for item in target if item != removed
            )
            if (
                not sparse
                or len(rich) != len(sparse) + 1
                or len(rich_set - set(sparse)) != 1
            ):
                continue
            found = False
            for changed_vertex in removed:
                partners = {
                    partner_at(matching, changed_vertex)
                    for matching in sparse
                }
                if len(partners) != 1:
                    continue
                partner = next(iter(partners))
                if tuple(
                    sorted((changed_vertex, partner))
                ) in FULL_EDGES:
                    found = True
                    break
            if found:
                forks.add(frozenset(target))
                break
    return sorted(tuple(sorted(target)) for target in forks)


def obstruction_masks(
    bad_masks: Sequence[int],
    forks: Sequence[Sequence[Edge]],
) -> dict[tuple[int, int], int]:
    pair_completions: dict[tuple[int, int], int] = {}
    for target in forks:
        for pair in itertools.combinations(target, 2):
            third = next(item for item in target if item not in pair)
            key = tuple(sorted((EDGE_ID[pair[0]], EDGE_ID[pair[1]])))
            pair_completions[key] = (
                pair_completions.get(key, 0)
                | (1 << EDGE_ID[third])
            )
    return pair_completions


def bad_neighbour_mask(
    factor: Sequence[Edge], bad_masks: Sequence[int]
) -> int:
    output = 0
    for item in factor:
        output |= bad_masks[EDGE_ID[item]]
    return output


def completion_mask(
    factor_edges: Sequence[Edge],
    pair_completions: dict[tuple[int, int], int],
) -> int:
    ids = sorted(EDGE_ID[item] for item in factor_edges)
    output = 0
    for first, second in itertools.combinations(ids, 2):
        output |= pair_completions.get((first, second), 0)
    return output


def mask_row(
    factor: tuple[Edge, ...],
    bad_masks: Sequence[int],
    pair_completions: dict[tuple[int, int], int],
) -> tuple[int, int, int, tuple[Edge, ...]]:
    return (
        edge_mask(factor),
        bad_neighbour_mask(factor, bad_masks),
        completion_mask(factor, pair_completions),
        factor,
    )


def compatible(
    selected_edges: int,
    selected_bad: int,
    selected_completion: int,
    candidate_edges: int,
    candidate_completion: int = 0,
) -> bool:
    return (
        candidate_edges
        & (selected_edges | selected_bad | selected_completion)
        == 0
        and candidate_completion & selected_edges == 0
    )


def split_masks(rows: Sequence[tuple[int, int, int, tuple[Edge, ...]]]):
    edge_low = np.array(
        [row[0] & LOW_64 for row in rows], dtype=np.uint64
    )
    edge_high = np.array(
        [row[0] >> 64 for row in rows], dtype=np.uint64
    )
    completion_low = np.array(
        [row[2] & LOW_64 for row in rows], dtype=np.uint64
    )
    completion_high = np.array(
        [row[2] >> 64 for row in rows], dtype=np.uint64
    )
    return edge_low, edge_high, completion_low, completion_high


def vector_disjoint(mask: int, low: np.ndarray, high: np.ndarray):
    return (
        (low & np.uint64(mask & LOW_64)) == 0
    ) & ((high & np.uint64(mask >> 64)) == 0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c4_c7_obstruction_catalogue.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c4_c7_family_certificate.json"
        ),
    )
    args = parser.parse_args()

    eligible_factors = perfect_matchings(N, set(ELIGIBLE_EDGES))
    completion_tables = cycle_completion_tables()
    safety_rows: list[tuple[tuple[Edge, ...], int, bool]] = []
    safety_histogram: Counter[tuple[int, bool]] = Counter()
    safe_factors: list[tuple[Edge, ...]] = []
    for factor in eligible_factors:
        triangle_to_square = sum(
            first < 3 and 3 <= second < 7
            for first, second in factor
        )
        safe = not factor_has_one_term(factor, completion_tables)
        safety_rows.append((factor, triangle_to_square, safe))
        safety_histogram[(triangle_to_square, safe)] += 1
        if safe:
            safe_factors.append(factor)

    actions = automorphisms()
    exceptional = [
        factor
        for factor, count, safe in safety_rows
        if safe and count == 2
    ]
    exceptional_orbits = orbit_representatives(exceptional, actions)
    bad_masks, bad_pairs = build_bad_pairs()

    safe_mask_rows = [
        (
            edge_mask(factor),
            bad_neighbour_mask(factor, bad_masks),
            factor,
        )
        for factor in safe_factors
    ]
    exceptional_counts: list[dict[str, object]] = []
    for representative, orbit_size in exceptional_orbits:
        selected_edges = edge_mask(representative)
        selected_bad = bad_neighbour_mask(
            representative, bad_masks
        )
        seconds = [
            row
            for row in safe_mask_rows
            if row[0] & (selected_edges | selected_bad) == 0
        ]
        thirds = 0
        for second_edges, second_bad, _factor in seconds:
            banned = (
                selected_edges
                | selected_bad
                | second_edges
                | second_bad
            )
            thirds += sum(
                candidate_edges & banned == 0
                for candidate_edges, _candidate_bad, _candidate in safe_mask_rows
            )
        exceptional_counts.append(
            {
                "representative": [
                    list(item) for item in representative
                ],
                "orbit_size": orbit_size,
                "compatible_safe_second_factors": len(seconds),
                "compatible_safe_ordered_third_factors": thirds,
            }
        )

    forks = build_fork_triples()
    pair_completions = obstruction_masks(bad_masks, forks)
    all_triangle_to_seven = [
        factor
        for factor, count, _safe in safety_rows
        if count == 0
    ]
    fork_free_rows = []
    for factor in all_triangle_to_seven:
        row = mask_row(factor, bad_masks, pair_completions)
        if row[0] & row[2] == 0:
            fork_free_rows.append(row)
    fork_free_set = {row[3] for row in fork_free_rows}
    fork_free_orbits = orbit_representatives(
        fork_free_set, actions
    )
    row_by_factor = {
        row[3]: row[:3] for row in fork_free_rows
    }
    edge_low, edge_high, completion_low, completion_high = (
        split_masks(fork_free_rows)
    )
    remaining_counts: list[dict[str, object]] = []
    total_seconds = 0
    total_thirds = 0
    for representative, orbit_size in fork_free_orbits:
        first_edges, first_bad, first_completion = row_by_factor[
            representative
        ]
        second_mask = vector_disjoint(
            first_edges | first_bad | first_completion,
            edge_low,
            edge_high,
        ) & vector_disjoint(
            first_edges, completion_low, completion_high
        )
        second_ids = np.flatnonzero(second_mask)
        thirds = 0
        for second_id in second_ids:
            second_edges, second_bad, _second_completion, second = (
                fork_free_rows[int(second_id)]
            )
            union_edges = first_edges | second_edges
            union_bad = first_bad | second_bad
            union_completion = completion_mask(
                tuple(set(representative) | set(second)),
                pair_completions,
            )
            third_mask = vector_disjoint(
                union_edges | union_bad | union_completion,
                edge_low,
                edge_high,
            ) & vector_disjoint(
                union_edges, completion_low, completion_high
            )
            thirds += int(np.count_nonzero(third_mask))
        total_seconds += len(second_ids)
        total_thirds += thirds
        remaining_counts.append(
            {
                "representative": [
                    list(item) for item in representative
                ],
                "orbit_size": orbit_size,
                "compatible_second_factors": len(second_ids),
                "compatible_ordered_third_factors": thirds,
            }
        )

    catalogue = {
        "n": N,
        "full_cycle_type": [3, 4, 7],
        "eligible_edges": [list(item) for item in ELIGIBLE_EDGES],
        "bad_two_edge_one_term_sets": [
            [list(first), list(second)]
            for first, second in bad_pairs
        ],
        "matching_fork_triples": [
            [list(item) for item in target] for target in forks
        ],
    }
    args.catalogue.parent.mkdir(parents=True, exist_ok=True)
    args.catalogue.write_text(
        json.dumps(catalogue, indent=2) + "\n", encoding="utf-8"
    )
    catalogue_sha = canonical_json_sha256(catalogue)

    payload = {
        "status": "all_c3_c4_c7_equality_supports_closed",
        "necessary_conditions_only": False,
        "n": N,
        "full_cycle_type": [3, 4, 7],
        "full_edges": len(FULL_EDGES),
        "eligible_singleton_edges": len(ELIGIBLE_EDGES),
        "eligible_singleton_perfect_matchings": len(
            eligible_factors
        ),
        "single_factor_safety_histogram": {
            f"triangle_to_square_{count}_safe_{str(safe).lower()}": value
            for (count, safe), value in sorted(
                safety_histogram.items()
            )
        },
        "individually_safe_factors": len(safe_factors),
        "exceptional_safe_factors": len(exceptional),
        "exceptional_orbits": exceptional_counts,
        "bad_two_edge_one_term_sets": len(bad_pairs),
        "exceptional_compatible_ordered_thirds": sum(
            int(row["compatible_safe_ordered_third_factors"])
            for row in exceptional_counts
        ),
        "triangle_to_seven_factors": len(all_triangle_to_seven),
        "matching_fork_triples": len(forks),
        "fork_free_triangle_to_seven_factors": len(
            fork_free_rows
        ),
        "fork_free_factor_orbits": remaining_counts,
        "compatible_second_factors_across_orbits": total_seconds,
        "compatible_ordered_third_factors_across_orbits": total_thirds,
        "catalogue": str(args.catalogue),
        "catalogue_canonical_sha256": catalogue_sha,
        "proof_dichotomy": [
            "an individually unsafe colour factor has a one-term amplitude",
            "an exceptional safe factor cannot be extended to three colours without a two-edge one-term set",
            "all remaining factors send the triangle to the seven-cycle",
            "every triple of those factors contains a two-edge one-term set or a matching-fork triple",
        ],
    }
    if sum(
        int(row["compatible_safe_ordered_third_factors"])
        for row in exceptional_counts
    ):
        raise AssertionError("exceptional factor survivor")
    if total_thirds:
        raise AssertionError("all-triangle-to-seven survivor")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
