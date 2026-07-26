"""Independent replay of the complete C3+C4+C7 family certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

N = 14
CYCLES = (
    tuple(range(0, 3)),
    tuple(range(3, 7)),
    tuple(range(7, 14)),
)
Edge = tuple[int, int]


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> set[Edge]:
    return {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    }


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


def canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def enumerate_matchings(
    allowed: Iterable[Edge],
) -> list[tuple[Edge, ...]]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first

    @lru_cache(maxsize=None)
    def visit(remaining: int) -> tuple[tuple[Edge, ...], ...]:
        if remaining == 0:
            return ((),)
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining & ~(
            (1 << (first + 1)) - 1
        )
        output: list[tuple[Edge, ...]] = []
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            for suffix in visit(
                remaining ^ first_bit ^ second_bit
            ):
                output.append(((first, second),) + suffix)
        return tuple(output)

    return sorted(visit((1 << N) - 1))


def active_count_table(factor: Sequence[Edge]) -> list[int]:
    edge_positions = {
        item: index for index, item in enumerate(factor)
    }
    exact = [0] * (1 << (N // 2))
    for matching in enumerate_matchings(
        set(FULL_EDGES) | set(factor)
    ):
        mask = 0
        for item in matching:
            if item in edge_positions:
                mask |= 1 << edge_positions[item]
        exact[mask] += 1
    totals = exact[:]
    for bit in range(N // 2):
        for mask in range(1 << (N // 2)):
            if mask & (1 << bit):
                totals[mask] += totals[mask ^ (1 << bit)]
    return totals


def factor_safe(factor: Sequence[Edge]) -> bool:
    totals = active_count_table(factor)
    full_mask = (1 << (N // 2)) - 1
    return not any(
        totals[mask] == 1 for mask in range(1, full_mask)
    )


def partner_at(matching: Sequence[Edge], vertex: int) -> int:
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise AssertionError("matching misses vertex")


def reconstruct_bad_pairs() -> set[frozenset[Edge]]:
    output: set[frozenset[Edge]] = set()
    for first, second in itertools.combinations(
        ELIGIBLE_EDGES, 2
    ):
        if set(first).intersection(second):
            continue
        if len(
            enumerate_matchings(
                set(FULL_EDGES) | {first, second}
            )
        ) == 1:
            output.add(frozenset((first, second)))
    return output


def reconstruct_forks() -> set[frozenset[Edge]]:
    output: set[frozenset[Edge]] = set()
    for target in itertools.combinations(ELIGIBLE_EDGES, 3):
        if len({vertex for item in target for vertex in item}) != 6:
            continue
        rich = enumerate_matchings(
            set(FULL_EDGES) | set(target)
        )
        for removed in target:
            sparse_edges = set(target) - {removed}
            sparse = enumerate_matchings(
                set(FULL_EDGES) | sparse_edges
            )
            if (
                not sparse
                or len(rich) != len(sparse) + 1
                or len(set(rich) - set(sparse)) != 1
            ):
                continue
            for changed in removed:
                partners = {
                    partner_at(matching, changed)
                    for matching in sparse
                }
                if (
                    len(partners) == 1
                    and edge(changed, next(iter(partners)))
                    in FULL_EDGES
                ):
                    output.add(frozenset(target))
                    break
            if frozenset(target) in output:
                break
    return output


def dihedral_actions(cycle: Sequence[int]) -> list[dict[int, int]]:
    return [
        {
            cycle[index]: cycle[
                (rotation + direction * index) % len(cycle)
            ]
            for index in range(len(cycle))
        }
        for direction in (1, -1)
        for rotation in range(len(cycle))
    ]


def automorphisms() -> list[dict[int, int]]:
    return [
        {**first, **second, **third}
        for first, second, third in itertools.product(
            *(dihedral_actions(cycle) for cycle in CYCLES)
        )
    ]


def transform(
    factor: Sequence[Edge], action: dict[int, int]
) -> tuple[Edge, ...]:
    return tuple(
        sorted(
            edge(action[first], action[second])
            for first, second in factor
        )
    )


def parse_factor(raw: Sequence[Sequence[int]]) -> tuple[Edge, ...]:
    return tuple(sorted(edge(*map(int, item)) for item in raw))


def expand_orbits(
    rows: Sequence[dict[str, object]],
    actions: Sequence[dict[int, int]],
) -> set[tuple[Edge, ...]]:
    expanded: set[tuple[Edge, ...]] = set()
    for row in rows:
        representative = parse_factor(row["representative"])
        orbit = {transform(representative, action) for action in actions}
        if len(orbit) != int(row["orbit_size"]):
            raise AssertionError("reported orbit size mismatch")
        if expanded.intersection(orbit):
            raise AssertionError("reported orbits overlap")
        expanded.update(orbit)
    return expanded


def edge_mask(items: Iterable[Edge]) -> int:
    return sum(1 << EDGE_ID[item] for item in items)


def bad_neighbour_masks(
    bad_pairs: set[frozenset[Edge]],
) -> list[int]:
    output = [0] * len(ELIGIBLE_EDGES)
    for target in bad_pairs:
        first, second = tuple(target)
        first_id = EDGE_ID[first]
        second_id = EDGE_ID[second]
        output[first_id] |= 1 << second_id
        output[second_id] |= 1 << first_id
    return output


def factor_bad_mask(
    factor: Sequence[Edge], masks: Sequence[int]
) -> int:
    output = 0
    for item in factor:
        output |= masks[EDGE_ID[item]]
    return output


def has_fork(
    items: set[Edge], forks: set[frozenset[Edge]]
) -> bool:
    return any(
        frozenset(target) in forks
        for target in itertools.combinations(sorted(items), 3)
    )


def obstruction_free_union(
    factors: Sequence[Sequence[Edge]],
    bad_pairs: set[frozenset[Edge]],
    forks: set[frozenset[Edge]],
) -> bool:
    item_list = [
        item for factor in factors for item in factor
    ]
    if len(set(item_list)) != len(item_list):
        return False
    item_set = set(item_list)
    if any(
        frozenset(pair) in bad_pairs
        for pair in itertools.combinations(sorted(item_set), 2)
    ):
        return False
    return not has_fork(item_set, forks)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c4_c7_family_certificate.json"
        ),
    )
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
            "tmp/fourteen_vertex_c3_c4_c7_family_verified.json"
        ),
    )
    args = parser.parse_args()
    certificate = json.loads(
        args.certificate.read_text(encoding="utf-8")
    )
    catalogue = json.loads(
        args.catalogue.read_text(encoding="utf-8")
    )
    if (
        certificate["status"]
        != "all_c3_c4_c7_equality_supports_closed"
        or certificate["necessary_conditions_only"]
    ):
        raise AssertionError("producer did not claim a final closure")
    if Path(certificate["catalogue"]) != args.catalogue:
        raise AssertionError("certificate/catalogue path mismatch")
    catalogue_sha = canonical_json_sha256(catalogue)
    if catalogue_sha != certificate["catalogue_canonical_sha256"]:
        raise AssertionError("catalogue hash mismatch")
    if list(map(int, catalogue["full_cycle_type"])) != [3, 4, 7]:
        raise AssertionError("wrong full factor")
    if [
        edge(*map(int, item)) for item in catalogue["eligible_edges"]
    ] != list(ELIGIBLE_EDGES):
        raise AssertionError("eligible-edge catalogue mismatch")

    eligible_factors = enumerate_matchings(ELIGIBLE_EDGES)
    safety_histogram: Counter[tuple[int, bool]] = Counter()
    safe_factors: list[tuple[Edge, ...]] = []
    exceptional: list[tuple[Edge, ...]] = []
    all_triangle_to_seven: list[tuple[Edge, ...]] = []
    for factor in eligible_factors:
        triangle_to_square = sum(
            first < 3 and 3 <= second < 7
            for first, second in factor
        )
        safe = factor_safe(factor)
        safety_histogram[(triangle_to_square, safe)] += 1
        if safe:
            safe_factors.append(factor)
        if safe and triangle_to_square == 2:
            exceptional.append(factor)
        if triangle_to_square == 0:
            all_triangle_to_seven.append(factor)
    expected_histogram = {
        f"triangle_to_square_{count}_safe_{str(safe).lower()}": value
        for (count, safe), value in sorted(safety_histogram.items())
    }
    if expected_histogram != certificate[
        "single_factor_safety_histogram"
    ]:
        raise AssertionError("single-factor safety histogram mismatch")

    bad_pairs = reconstruct_bad_pairs()
    catalogued_bad = {
        frozenset(
            edge(*map(int, item)) for item in target
        )
        for target in catalogue["bad_two_edge_one_term_sets"]
    }
    if bad_pairs != catalogued_bad:
        raise AssertionError("two-edge catalogue mismatch")
    forks = reconstruct_forks()
    catalogued_forks = {
        frozenset(
            edge(*map(int, item)) for item in target
        )
        for target in catalogue["matching_fork_triples"]
    }
    if forks != catalogued_forks:
        raise AssertionError("matching-fork catalogue mismatch")

    actions = automorphisms()
    expanded_exceptional = expand_orbits(
        certificate["exceptional_orbits"], actions
    )
    if expanded_exceptional != set(exceptional):
        raise AssertionError("exceptional orbit coverage mismatch")
    bad_masks = bad_neighbour_masks(bad_pairs)
    safe_rows = [
        (
            edge_mask(factor),
            factor_bad_mask(factor, bad_masks),
            factor,
        )
        for factor in safe_factors
    ]
    exceptional_counts = []
    for row in certificate["exceptional_orbits"]:
        representative = parse_factor(row["representative"])
        first_edges = edge_mask(representative)
        first_bad = factor_bad_mask(representative, bad_masks)
        seconds = [
            candidate
            for candidate_edges, _candidate_bad, candidate in safe_rows
            if candidate_edges & (first_edges | first_bad) == 0
        ]
        thirds = 0
        for second in seconds:
            union_edges = first_edges | edge_mask(second)
            union_bad = first_bad | factor_bad_mask(
                second, bad_masks
            )
            thirds += sum(
                candidate_edges & (union_edges | union_bad) == 0
                for candidate_edges, _candidate_bad, _candidate in safe_rows
            )
        observed = (len(seconds), thirds)
        expected = (
            int(row["compatible_safe_second_factors"]),
            int(row["compatible_safe_ordered_third_factors"]),
        )
        if observed != expected:
            raise AssertionError("exceptional extension count mismatch")
        exceptional_counts.append(observed)
    if any(thirds for _seconds, thirds in exceptional_counts):
        raise AssertionError("exceptional survivor")

    fork_free_factors = [
        factor
        for factor in all_triangle_to_seven
        if not has_fork(set(factor), forks)
    ]
    expanded_fork_free = expand_orbits(
        certificate["fork_free_factor_orbits"], actions
    )
    if expanded_fork_free != set(fork_free_factors):
        raise AssertionError("fork-free orbit coverage mismatch")

    total_seconds = 0
    total_thirds = 0
    for row in certificate["fork_free_factor_orbits"]:
        representative = parse_factor(row["representative"])
        seconds = [
            candidate
            for candidate in fork_free_factors
            if obstruction_free_union(
                (representative, candidate),
                bad_pairs,
                forks,
            )
        ]
        thirds = 0
        for second in seconds:
            thirds += sum(
                obstruction_free_union(
                    (representative, second, candidate),
                    bad_pairs,
                    forks,
                )
                for candidate in fork_free_factors
            )
        observed = (len(seconds), thirds)
        expected = (
            int(row["compatible_second_factors"]),
            int(row["compatible_ordered_third_factors"]),
        )
        if observed != expected:
            raise AssertionError("final extension count mismatch")
        total_seconds += len(seconds)
        total_thirds += thirds
    if total_thirds:
        raise AssertionError("final family survivor")
    if total_seconds != int(
        certificate["compatible_second_factors_across_orbits"]
    ):
        raise AssertionError("aggregate second-factor count mismatch")

    payload = {
        "verified": True,
        "certificate": str(args.certificate),
        "catalogue": str(args.catalogue),
        "catalogue_canonical_sha256": catalogue_sha,
        "eligible_singleton_perfect_matchings": len(
            eligible_factors
        ),
        "individually_safe_factors": len(safe_factors),
        "exceptional_safe_factors": len(exceptional),
        "bad_two_edge_one_term_sets": len(bad_pairs),
        "matching_fork_triples": len(forks),
        "fork_free_triangle_to_seven_factors": len(
            fork_free_factors
        ),
        "exceptional_orbits": len(exceptional_counts),
        "fork_free_factor_orbits": len(
            certificate["fork_free_factor_orbits"]
        ),
        "compatible_second_factors_across_orbits": total_seconds,
        "compatible_ordered_third_factors_across_orbits": total_thirds,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
