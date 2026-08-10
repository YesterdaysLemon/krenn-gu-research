"""Explore an order-14 equality factor via exact one-term/fork catalogues."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import argparse
import functools
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

from krenn_gu.explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)

N = 14
LOW_64 = (1 << 64) - 1


def canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def contiguous_cycles(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    return tuple(output)


def edge_mask(items: Iterable[Edge], edge_id: dict[Edge, int]) -> int:
    return sum(1 << edge_id[item] for item in items)


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


def completion_tables(
    cycles: Sequence[Sequence[int]],
) -> list[dict[frozenset[int], int]]:
    output = []
    for cycle in cycles:
        table = {}
        for mask in range(1 << len(cycle)):
            deleted = frozenset(
                cycle[index]
                for index in range(len(cycle))
                if mask & (1 << index)
            )
            remaining = frozenset(set(cycle) - set(deleted))
            allowed = {
                item
                for item in cycle_edges(cycle)
                if item[0] in remaining and item[1] in remaining
            }
            table[deleted] = count_matchings(remaining, allowed)
        output.append(table)
    return output


def factor_safe(
    factor: Sequence[Edge],
    cycles: Sequence[Sequence[int]],
    vertex_component: dict[int, int],
    tables: Sequence[dict[frozenset[int], int]],
) -> bool:
    exact = [0] * (1 << (N // 2))
    for mask in range(1 << (N // 2)):
        deleted = [set() for _cycle in cycles]
        for position, item in enumerate(factor):
            if mask & (1 << position):
                for vertex in item:
                    deleted[vertex_component[vertex]].add(vertex)
        value = 1
        for component, table in enumerate(tables):
            value *= table[frozenset(deleted[component])]
        exact[mask] = value
    totals = exact[:]
    for bit in range(N // 2):
        for mask in range(1 << (N // 2)):
            if mask & (1 << bit):
                totals[mask] += totals[mask ^ (1 << bit)]
    return not any(
        totals[mask] == 1
        for mask in range(1, (1 << (N // 2)) - 1)
    )


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("perfect matching misses vertex")


def full_automorphisms(
    cycles: Sequence[Sequence[int]],
) -> list[dict[int, int]]:
    groups: dict[int, list[int]] = defaultdict(list)
    for component, cycle in enumerate(cycles):
        groups[len(cycle)].append(component)
    component_permutations: list[dict[int, int]] = [{}]
    for indices in groups.values():
        next_rows = []
        for permutation in itertools.permutations(indices):
            mapping = dict(zip(indices, permutation))
            for row in component_permutations:
                next_rows.append({**row, **mapping})
        component_permutations = next_rows
    local_choices = list(
        itertools.product(
            *[
                [
                    (direction, rotation)
                    for direction in (1, -1)
                    for rotation in range(len(cycle))
                ]
                for cycle in cycles
            ]
        )
    )
    actions = []
    for component_map in component_permutations:
        for choices in local_choices:
            action = {}
            for source, cycle in enumerate(cycles):
                target = cycles[component_map[source]]
                direction, rotation = choices[source]
                for position, vertex in enumerate(cycle):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            actions.append(action)
    return actions


def transform(
    factor: Sequence[Edge], action: dict[int, int]
) -> tuple[Edge, ...]:
    return tuple(
        sorted(
            tuple(sorted((action[first], action[second])))
            for first, second in factor
        )
    )


def orbits(
    factors: Iterable[tuple[Edge, ...]],
    actions: Sequence[dict[int, int]],
) -> list[tuple[tuple[Edge, ...], int]]:
    factor_set = set(factors)
    unseen = set(factor_set)
    output = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform(representative, action)
            for action in actions
        } & factor_set
        output.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    return output


def vector_disjoint(mask: int, low: np.ndarray, high: np.ndarray):
    return (
        (low & np.uint64(mask & LOW_64)) == 0
    ) & ((high & np.uint64(mask >> 64)) == 0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", default="3+5+6")
    parser.add_argument(
        "--larger-fork-size",
        type=int,
        default=0,
        help=(
            "also filter final survivors by matching forks of every "
            "size from 4 through this size"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_factor_family_exploratory.json"
        ),
    )
    parser.add_argument(
        "--survivor-limit",
        type=int,
        default=3,
        help=(
            "maximum saved survivor supports; use 0 to save every "
            "survivor"
        ),
    )
    parser.add_argument(
        "--catalogue",
        type=Path,
        help=(
            "optional exact compact catalogue of one-term pairs and "
            "matching-fork edge masks"
        ),
    )
    parser.add_argument(
        "--one-term-catalogue",
        type=Path,
        help=(
            "optional catalogue of larger one-term matching masks to "
            "apply alongside the matching-fork obstructions"
        ),
    )
    parser.add_argument(
        "--stop-after-factor-orbits",
        action="store_true",
        help=(
            "write the exact single-factor and factor-orbit census "
            "without enumerating compatible triples"
        ),
    )
    args = parser.parse_args()
    lengths = tuple(map(int, args.partition.split("+")))
    if sum(lengths) != N or any(length < 3 for length in lengths):
        raise ValueError("partition must consist of cycles summing to 14")
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    edge_id = {
        item: index for index, item in enumerate(eligible_edges)
    }
    extra_one_terms_by_size: dict[int, set[int]] = {}
    one_term_catalogue_sha256 = None
    if args.one_term_catalogue is not None:
        one_term_payload = json.loads(
            args.one_term_catalogue.read_text(encoding="utf-8")
        )
        if tuple(map(int, one_term_payload["partition"])) != lengths:
            raise ValueError("one-term catalogue partition mismatch")
        if tuple(
            tuple(map(int, item))
            for item in one_term_payload["eligible_edges"]
        ) != eligible_edges:
            raise ValueError("one-term catalogue edge-order mismatch")
        extra_one_terms_by_size = {
            int(size): set(map(int, masks))
            for size, masks in one_term_payload[
                "one_term_masks_by_size"
            ].items()
        }
        one_term_catalogue_sha256 = canonical_json_sha256(
            one_term_payload
        )
    vertex_component = {
        vertex: component
        for component, cycle in enumerate(cycles)
        for vertex in cycle
    }
    factors = perfect_matchings(N, set(eligible_edges))
    tables = completion_tables(cycles)
    safe_factors = [
        factor
        for factor in factors
        if factor_safe(
            factor, cycles, vertex_component, tables
        )
    ]

    def support_matchings(items: Iterable[Edge]):
        return perfect_matchings(
            N, set(full_edges) | set(items)
        )

    bad_masks = [0] * len(eligible_edges)
    bad_pairs = []
    for first_id, first in enumerate(eligible_edges):
        for second_id in range(first_id + 1, len(eligible_edges)):
            second = eligible_edges[second_id]
            if set(first).intersection(second):
                continue
            if len(support_matchings((first, second))) == 1:
                bad_masks[first_id] |= 1 << second_id
                bad_masks[second_id] |= 1 << first_id
                bad_pairs.append((first, second))

    completion_by_deleted_mask = []
    for deleted_mask in range(1 << N):
        value = 1
        for component, cycle in enumerate(cycles):
            deleted = frozenset(
                vertex
                for vertex in cycle
                if deleted_mask & (1 << vertex)
            )
            value *= tables[component][deleted]
        completion_by_deleted_mask.append(value)
    eligible_vertex_masks = tuple(
        (1 << first) | (1 << second)
        for first, second in eligible_edges
    )

    @functools.lru_cache(maxsize=None)
    def support_count(edge_ids: tuple[int, ...]) -> int:
        """Count PMs in F plus a matching of eligible edges exactly."""
        deleted_masks = [0] * (1 << len(edge_ids))
        for position, item_id in enumerate(edge_ids):
            bit = 1 << position
            for subset in range(bit, 1 << len(edge_ids)):
                if subset & bit:
                    deleted_masks[subset] = (
                        deleted_masks[subset ^ bit]
                        | eligible_vertex_masks[item_id]
                    )
        return sum(
            completion_by_deleted_mask[deleted]
            for deleted in deleted_masks
        )

    def count_with_full_edge(
        edge_ids: tuple[int, ...], full_edge: Edge
    ) -> int:
        """Count support PMs containing one specified full-factor edge."""
        base = (1 << full_edge[0]) | (1 << full_edge[1])
        total = 0
        for subset in range(1 << len(edge_ids)):
            deleted = base
            valid = True
            for position, item_id in enumerate(edge_ids):
                if not subset & (1 << position):
                    continue
                item_mask = eligible_vertex_masks[item_id]
                if item_mask & base:
                    valid = False
                    break
                deleted |= item_mask
            if valid:
                total += completion_by_deleted_mask[deleted]
        return total

    full_neighbours = {
        vertex: tuple(
            other
            for item in full_edges
            if vertex in item
            for other in item
            if other != vertex
        )
        for vertex in range(N)
    }

    def matching_edge_id_sets(size: int):
        """Yield all eligible matchings of the requested size."""
        chosen: list[int] = []

        def visit(start: int, used_vertices: int):
            if len(chosen) == size:
                yield tuple(chosen)
                return
            for item_id in range(start, len(eligible_edges)):
                item_mask = eligible_vertex_masks[item_id]
                if item_mask & used_vertices:
                    continue
                chosen.append(item_id)
                yield from visit(
                    item_id + 1, used_vertices | item_mask
                )
                chosen.pop()

        yield from visit(0, 0)

    def build_forks(size: int) -> set[int]:
        """Return exact matching-fork edge masks of a fixed size."""
        output: set[int] = set()
        for target_ids in matching_edge_id_sets(size):
            rich = support_count(target_ids)
            for removed_position, removed_id in enumerate(target_ids):
                sparse_ids = (
                    target_ids[:removed_position]
                    + target_ids[removed_position + 1 :]
                )
                sparse = support_count(sparse_ids)
                if not sparse or rich != sparse + 1:
                    continue
                removed = eligible_edges[removed_id]
                found = False
                for changed in removed:
                    for partner in full_neighbours[changed]:
                        if count_with_full_edge(
                            sparse_ids,
                            tuple(sorted((changed, partner))),
                        ) == sparse:
                            found = True
                            break
                    if found:
                        break
                if found:
                    output.add(
                        sum(1 << item_id for item_id in target_ids)
                    )
                    break
        return output

    forks = build_forks(3)
    larger_forks_by_size = {
        size: build_forks(size)
        for size in range(4, args.larger_fork_size + 1)
    }
    size_three_obstructions = (
        forks | extra_one_terms_by_size.get(3, set())
    )
    larger_obstructions_by_size = {
        size: (
            larger_forks_by_size.get(size, set())
            | extra_one_terms_by_size.get(size, set())
        )
        for size in (
            set(larger_forks_by_size)
            | {
                size
                for size in extra_one_terms_by_size
                if size >= 4
            }
        )
    }
    pair_completions: dict[tuple[int, int], int] = {}
    for target_mask in size_three_obstructions:
        target_ids = tuple(
            item_id
            for item_id in range(len(eligible_edges))
            if target_mask & (1 << item_id)
        )
        for pair in itertools.combinations(target_ids, 2):
            third = next(
                item_id for item_id in target_ids if item_id not in pair
            )
            key = tuple(sorted(pair))
            pair_completions[key] = (
                pair_completions.get(key, 0)
                | (1 << third)
            )

    def bad_mask(factor: Sequence[Edge]) -> int:
        output = 0
        for item in factor:
            output |= bad_masks[edge_id[item]]
        return output

    def completion_mask(items: Sequence[Edge]) -> int:
        ids = sorted(edge_id[item] for item in items)
        output = 0
        for first, second in itertools.combinations(ids, 2):
            output |= pair_completions.get((first, second), 0)
        return output

    rows = []
    for factor in safe_factors:
        edges = edge_mask(factor, edge_id)
        completion = completion_mask(factor)
        if edges & completion:
            continue
        rows.append((edges, bad_mask(factor), completion, factor))
    actions = full_automorphisms(cycles)
    factor_orbits = orbits((row[3] for row in rows), actions)
    if args.stop_after_factor_orbits:
        payload = {
            "status": "factor_orbit_census_complete",
            "necessary_conditions_only": True,
            "partition": list(lengths),
            "full_automorphisms": len(actions),
            "eligible_singleton_factors": len(factors),
            "individually_one_term_free_factors": len(safe_factors),
            "bad_two_edge_one_term_sets": len(bad_pairs),
            "matching_fork_triples": len(forks),
            "fork_free_safe_factors": len(rows),
            "fork_free_safe_factor_orbits": len(factor_orbits),
            "factor_orbits": [
                {
                    "representative": [
                        list(item) for item in representative
                    ],
                    "orbit_size": orbit_size,
                }
                for representative, orbit_size in factor_orbits
            ],
            "exploratory_until_independently_replayed": True,
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
                    if key != "factor_orbits"
                },
                indent=2,
            )
        )
        return
    lookup = {row[3]: row[:3] for row in rows}
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
    orbit_rows = []
    total_seconds = 0
    total_thirds = 0
    survivors = []
    for representative, orbit_size in factor_orbits:
        first_edges, first_bad, first_completion = lookup[
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
            second_edges, second_bad, _second_completion, second = rows[
                int(second_id)
            ]
            union_edges = first_edges | second_edges
            union_bad = first_bad | second_bad
            union_completion = completion_mask(
                tuple(set(representative) | set(second))
            )
            third_mask = vector_disjoint(
                union_edges | union_bad | union_completion,
                edge_low,
                edge_high,
            ) & vector_disjoint(
                union_edges, completion_low, completion_high
            )
            third_ids = np.flatnonzero(third_mask)
            if larger_obstructions_by_size:
                accepted_ids = []
                selected = set(representative) | set(second)
                selected_obstructed = any(
                    any(
                        edge_mask(target, edge_id) in catalogue
                        for target in itertools.combinations(
                            sorted(selected), size
                        )
                    )
                    for size, catalogue
                    in larger_obstructions_by_size.items()
                )
                for third_id in (
                    () if selected_obstructed else third_ids
                ):
                    union = selected | set(rows[int(third_id)][3])
                    obstructed = any(
                        any(
                            edge_mask(target, edge_id) in catalogue
                            for target in itertools.combinations(
                                sorted(union), size
                            )
                        )
                        for size, catalogue
                        in larger_obstructions_by_size.items()
                    )
                    if obstructed:
                        continue
                    accepted_ids.append(int(third_id))
                third_ids = np.array(
                    accepted_ids, dtype=np.int64
                )
            count = len(third_ids)
            thirds += count
            if count and (
                args.survivor_limit == 0
                or len(survivors) < args.survivor_limit
            ):
                for third_id in third_ids:
                    survivors.append(
                        {
                            "first": [list(item) for item in representative],
                            "second": [list(item) for item in second],
                            "third": [
                                list(item)
                                for item in rows[int(third_id)][3]
                            ],
                        }
                    )
                    if (
                        args.survivor_limit
                        and len(survivors)
                        == args.survivor_limit
                    ):
                        break
        total_seconds += len(second_ids)
        total_thirds += thirds
        orbit_rows.append(
            {
                "representative": [
                    list(item) for item in representative
                ],
                "orbit_size": orbit_size,
                "compatible_seconds": len(second_ids),
                "compatible_ordered_thirds": thirds,
            }
        )
        print(
            f"orbit={len(orbit_rows)}/{len(factor_orbits)} "
            f"seconds={len(second_ids)} thirds={thirds}",
            flush=True,
        )

    catalogue_sha256 = None
    if args.catalogue is not None:
        catalogue = {
            "n": N,
            "partition": list(lengths),
            "eligible_edges": [
                list(item) for item in eligible_edges
            ],
            "bad_two_edge_one_term_masks": sorted(
                (1 << edge_id[first]) | (1 << edge_id[second])
                for first, second in bad_pairs
            ),
            "matching_fork_masks_by_size": {
                "3": sorted(forks),
                **{
                    str(size): sorted(catalogue)
                    for size, catalogue
                    in larger_forks_by_size.items()
                },
            },
        }
        args.catalogue.parent.mkdir(parents=True, exist_ok=True)
        args.catalogue.write_text(
            json.dumps(catalogue, indent=2) + "\n",
            encoding="utf-8",
        )
        catalogue_sha256 = canonical_json_sha256(catalogue)

    payload = {
        "status": (
            (
                "zero_supports_after_uncoloured_one_term_filter"
                if extra_one_terms_by_size
                else "zero_survivors"
            )
            if total_thirds == 0
            else "survivors_require_stronger_obstruction"
        ),
        "necessary_conditions_only": (
            total_thirds != 0 or bool(extra_one_terms_by_size)
        ),
        "partition": list(lengths),
        "full_automorphisms": len(actions),
        "eligible_singleton_factors": len(factors),
        "individually_one_term_free_factors": len(safe_factors),
        "bad_two_edge_one_term_sets": len(bad_pairs),
        "matching_fork_triples": len(forks),
        "larger_one_term_sets_by_size": {
            str(size): len(catalogue)
            for size, catalogue in extra_one_terms_by_size.items()
        },
        "larger_matching_fork_size": args.larger_fork_size,
        "larger_matching_forks": len(
            larger_forks_by_size.get(
                args.larger_fork_size, set()
            )
        ),
        "larger_matching_forks_by_size": {
            str(size): len(catalogue)
            for size, catalogue in larger_forks_by_size.items()
        },
        "fork_free_safe_factors": len(rows),
        "fork_free_safe_factor_orbits": len(factor_orbits),
        "compatible_seconds_across_orbits": total_seconds,
        "compatible_ordered_thirds_across_orbits": total_thirds,
        "survivor_save_limit": args.survivor_limit,
        "survivors": survivors,
        "orbit_rows": orbit_rows,
        "obstruction_catalogue": (
            str(args.catalogue) if args.catalogue is not None else None
        ),
        "obstruction_catalogue_canonical_sha256": catalogue_sha256,
        "one_term_catalogue": (
            str(args.one_term_catalogue)
            if args.one_term_catalogue is not None
            else None
        ),
        "one_term_catalogue_canonical_sha256": (
            one_term_catalogue_sha256
        ),
        "exploratory_until_independently_replayed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in payload.items() if key != "orbit_rows"}, indent=2))


if __name__ == "__main__":
    main()
