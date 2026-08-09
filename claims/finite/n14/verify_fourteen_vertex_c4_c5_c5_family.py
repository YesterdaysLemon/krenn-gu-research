"""Independent replay of the complete C4+C5+C5 equality-family proof."""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence

N = 14
CYCLES = (
    tuple(range(0, 4)),
    tuple(range(4, 9)),
    tuple(range(9, 14)),
)
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
ALL_VERTICES = (1 << N) - 1


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> set[Edge]:
    return {
        edge(cycle[position], cycle[(position + 1) % len(cycle)])
        for position in range(len(cycle))
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
    item: position for position, item in enumerate(ELIGIBLE_EDGES)
}
EDGE_VERTEX_MASK = tuple(
    (1 << first) | (1 << second)
    for first, second in ELIGIBLE_EDGES
)
FULL_ADJACENCY = [0] * N
for _first, _second in FULL_EDGES:
    FULL_ADJACENCY[_first] |= 1 << _second
    FULL_ADJACENCY[_second] |= 1 << _first


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_sha256(payload: object) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@functools.lru_cache(maxsize=None)
def full_completion(remaining: int) -> int:
    if remaining == 0:
        return 1
    first_bit = remaining & -remaining
    first = first_bit.bit_length() - 1
    candidates = FULL_ADJACENCY[first] & remaining
    total = 0
    while candidates:
        second_bit = candidates & -candidates
        candidates ^= second_bit
        total += full_completion(remaining ^ first_bit ^ second_bit)
    return total


COMPLETION_BY_DELETED = tuple(
    full_completion(ALL_VERTICES ^ deleted)
    for deleted in range(1 << N)
)


def enumerate_factors(allowed: Iterable[Edge]) -> list[Factor]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first

    @functools.lru_cache(maxsize=None)
    def visit(remaining: int) -> tuple[Factor, ...]:
        if remaining == 0:
            return ((),)
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        output = []
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            for suffix in visit(remaining ^ first_bit ^ second_bit):
                output.append(((first, second),) + suffix)
        return tuple(output)

    return sorted(visit(ALL_VERTICES))


@functools.lru_cache(maxsize=None)
def support_count(item_ids: tuple[int, ...]) -> int:
    total = 0
    for subset in range(1 << len(item_ids)):
        deleted = 0
        for position, item_id in enumerate(item_ids):
            if subset & (1 << position):
                deleted |= EDGE_VERTEX_MASK[item_id]
        total += COMPLETION_BY_DELETED[deleted]
    return total


def count_containing_full_edge(
    item_ids: Sequence[int], full_edge: Edge
) -> int:
    fixed = (1 << full_edge[0]) | (1 << full_edge[1])
    total = 0
    for subset in range(1 << len(item_ids)):
        deleted = fixed
        valid = True
        for position, item_id in enumerate(item_ids):
            if not subset & (1 << position):
                continue
            item_mask = EDGE_VERTEX_MASK[item_id]
            if item_mask & fixed:
                valid = False
                break
            deleted |= item_mask
        if valid:
            total += COMPLETION_BY_DELETED[deleted]
    return total


def factor_safe(factor: Factor) -> bool:
    item_ids = tuple(EDGE_ID[item] for item in factor)
    exact = [0] * (1 << len(item_ids))
    for subset in range(1 << len(item_ids)):
        deleted = 0
        for position, item_id in enumerate(item_ids):
            if subset & (1 << position):
                deleted |= EDGE_VERTEX_MASK[item_id]
        exact[subset] = COMPLETION_BY_DELETED[deleted]
    totals = exact[:]
    for bit in range(len(item_ids)):
        for subset in range(1 << len(item_ids)):
            if subset & (1 << bit):
                totals[subset] += totals[subset ^ (1 << bit)]
    return not any(
        totals[subset] == 1
        for subset in range(1, (1 << len(item_ids)) - 1)
    )


FULL_NEIGHBOURS = {
    vertex: tuple(
        other
        for item in FULL_EDGES
        if vertex in item
        for other in item
        if other != vertex
    )
    for vertex in range(N)
}


def decode_mask(mask: int) -> tuple[int, ...]:
    return tuple(
        item_id
        for item_id in range(len(ELIGIBLE_EDGES))
        if mask & (1 << item_id)
    )


def validate_bad_pairs(catalogue: set[int]) -> None:
    for mask in catalogue:
        item_ids = decode_mask(mask)
        if len(item_ids) != 2:
            raise AssertionError("bad-pair mask has the wrong size")
        if (
            EDGE_VERTEX_MASK[item_ids[0]]
            & EDGE_VERTEX_MASK[item_ids[1]]
        ):
            raise AssertionError("bad-pair mask is not a matching")
        if support_count(item_ids) != 1:
            raise AssertionError("catalogued bad pair is not one-term")


def validate_forks(size: int, catalogue: set[int]) -> None:
    for mask in catalogue:
        item_ids = decode_mask(mask)
        if len(item_ids) != size:
            raise AssertionError(f"size-{size} fork has wrong size")
        used = 0
        for item_id in item_ids:
            if used & EDGE_VERTEX_MASK[item_id]:
                raise AssertionError(f"size-{size} fork is not a matching")
            used |= EDGE_VERTEX_MASK[item_id]
        rich = support_count(item_ids)
        valid = False
        for position, removed_id in enumerate(item_ids):
            sparse_ids = item_ids[:position] + item_ids[position + 1 :]
            sparse = support_count(sparse_ids)
            if not sparse or rich != sparse + 1:
                continue
            removed = ELIGIBLE_EDGES[removed_id]
            if any(
                count_containing_full_edge(
                    sparse_ids, edge(changed, partner)
                )
                == sparse
                for changed in removed
                for partner in FULL_NEIGHBOURS[changed]
            ):
                valid = True
                break
        if not valid:
            raise AssertionError(
                f"catalogued size-{size} fork failed semantic replay"
            )


def factor_mask(factor: Sequence[Edge]) -> int:
    return sum(1 << EDGE_ID[item] for item in factor)


def bad_neighbour_masks(bad_pairs: set[int]) -> list[int]:
    output = [0] * len(ELIGIBLE_EDGES)
    for target in bad_pairs:
        first, second = decode_mask(target)
        output[first] |= 1 << second
        output[second] |= 1 << first
    return output


def factor_bad_mask(
    factor: Sequence[Edge], bad_masks: Sequence[int]
) -> int:
    output = 0
    for item in factor:
        output |= bad_masks[EDGE_ID[item]]
    return output


def pair_completion_masks(forks: set[int]) -> dict[tuple[int, int], int]:
    output: dict[tuple[int, int], int] = {}
    for target in forks:
        item_ids = decode_mask(target)
        for first, second in itertools.combinations(item_ids, 2):
            third = next(
                item_id
                for item_id in item_ids
                if item_id not in {first, second}
            )
            output[(first, second)] = (
                output.get((first, second), 0) | (1 << third)
            )
    return output


def completion_mask(
    items: Iterable[Edge],
    pair_completions: dict[tuple[int, int], int],
) -> int:
    item_ids = sorted(EDGE_ID[item] for item in items)
    output = 0
    for first, second in itertools.combinations(item_ids, 2):
        output |= pair_completions.get((first, second), 0)
    return output


def contains_catalogued_fork(
    selected: int, size: int, catalogue: set[int]
) -> bool:
    item_ids = decode_mask(selected)
    return any(
        sum(1 << item_id for item_id in target) in catalogue
        for target in itertools.combinations(item_ids, size)
    )


def full_automorphisms() -> list[dict[int, int]]:
    groups: dict[int, list[int]] = {}
    for component, cycle in enumerate(CYCLES):
        groups.setdefault(len(cycle), []).append(component)
    component_maps: list[dict[int, int]] = [{}]
    for indices in groups.values():
        expanded = []
        for permutation in itertools.permutations(indices):
            current = dict(zip(indices, permutation))
            for previous in component_maps:
                expanded.append({**previous, **current})
        component_maps = expanded
    local_choices = itertools.product(
        *[
            [
                (direction, rotation)
                for direction in (1, -1)
                for rotation in range(len(cycle))
            ]
            for cycle in CYCLES
        ]
    )
    choices = list(local_choices)
    actions = []
    for component_map in component_maps:
        for local in choices:
            action = {}
            for source, cycle in enumerate(CYCLES):
                target = CYCLES[component_map[source]]
                direction, rotation = local[source]
                for position, vertex in enumerate(cycle):
                    action[vertex] = target[
                        (rotation + direction * position) % len(target)
                    ]
            actions.append(action)
    return actions


def transform(
    factor: Sequence[Edge], action: dict[int, int]
) -> Factor:
    return tuple(
        sorted(
            edge(action[first], action[second])
            for first, second in factor
        )
    )


def factor_orbits(
    factors: Iterable[Factor], actions: Sequence[dict[int, int]]
) -> list[tuple[Factor, int]]:
    unseen = set(factors)
    output = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform(representative, action) for action in actions
        } & unseen
        output.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    return output


def parse_factor(raw: Sequence[Sequence[int]]) -> Factor:
    return tuple(sorted(edge(*map(int, item)) for item in raw))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--enumeration",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_5_5_fork5_survivors.json"
        ),
    )
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_5_5_fork5_catalogue.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c5_c5_family_verified.json"
        ),
    )
    args = parser.parse_args()
    enumeration = json.loads(
        args.enumeration.read_text(encoding="utf-8")
    )
    catalogue = json.loads(
        args.catalogue.read_text(encoding="utf-8")
    )
    if catalogue.get("partition") != [4, 5, 5]:
        raise AssertionError("catalogue cycle type mismatch")
    if tuple(
        edge(*map(int, item)) for item in catalogue["eligible_edges"]
    ) != ELIGIBLE_EDGES:
        raise AssertionError("eligible-edge catalogue mismatch")
    if enumeration.get("status") != "zero_survivors":
        raise AssertionError("producer did not claim a final closure")
    if enumeration.get("necessary_conditions_only"):
        raise AssertionError("producer left the result exploratory")

    bad_pairs_list = list(
        map(int, catalogue["bad_two_edge_one_term_masks"])
    )
    if len(bad_pairs_list) != len(set(bad_pairs_list)):
        raise AssertionError("duplicate bad-pair masks")
    bad_pairs = set(bad_pairs_list)
    fork_sets = {}
    for size in (3, 4, 5):
        raw = list(
            map(
                int,
                catalogue["matching_fork_masks_by_size"][str(size)],
            )
        )
        if len(raw) != len(set(raw)):
            raise AssertionError(f"duplicate size-{size} fork masks")
        fork_sets[size] = set(raw)

    validate_bad_pairs(bad_pairs)
    for size in (3, 4, 5):
        validate_forks(size, fork_sets[size])

    canonical_catalogue_sha = canonical_json_sha256(catalogue)
    if canonical_catalogue_sha != enumeration[
        "obstruction_catalogue_canonical_sha256"
    ]:
        raise AssertionError("catalogue hash binding mismatch")

    factors = enumerate_factors(ELIGIBLE_EDGES)
    safe_factors = [factor for factor in factors if factor_safe(factor)]
    bad_masks = bad_neighbour_masks(bad_pairs)
    pair_completions = pair_completion_masks(fork_sets[3])
    rows = []
    for factor in safe_factors:
        selected = factor_mask(factor)
        completion = completion_mask(factor, pair_completions)
        if selected & completion:
            continue
        rows.append(
            (
                selected,
                factor_bad_mask(factor, bad_masks),
                completion,
                factor,
            )
        )

    actions = full_automorphisms()
    orbits = factor_orbits((row[3] for row in rows), actions)
    reported_rows = enumeration["orbit_rows"]
    reported = [
        (
            parse_factor(row["representative"]),
            int(row["orbit_size"]),
        )
        for row in reported_rows
    ]
    if reported != orbits:
        raise AssertionError("factor-orbit manifest mismatch")

    total_seconds = 0
    total_thirds = 0
    replay_rows = []
    for orbit_id, (representative, orbit_size) in enumerate(orbits):
        first_row = next(row for row in rows if row[3] == representative)
        first_edges, first_bad, first_completion, _first = first_row
        seconds = []
        for row in rows:
            second_edges, _second_bad, second_completion, _second = row
            if second_edges & (
                first_edges | first_bad | first_completion
            ):
                continue
            if second_completion & first_edges:
                continue
            seconds.append(row)

        thirds = 0
        for second_edges, second_bad, _second_completion, second in seconds:
            selected_edges = first_edges | second_edges
            selected_bad = first_bad | second_bad
            selected_completion = completion_mask(
                set(representative) | set(second),
                pair_completions,
            )
            if any(
                contains_catalogued_fork(
                    selected_edges, size, fork_sets[size]
                )
                for size in (4, 5)
            ):
                continue
            for (
                third_edges,
                _third_bad,
                third_completion,
                _third,
            ) in rows:
                if third_edges & (
                    selected_edges
                    | selected_bad
                    | selected_completion
                ):
                    continue
                if third_completion & selected_edges:
                    continue
                union = selected_edges | third_edges
                if any(
                    contains_catalogued_fork(
                        union, size, fork_sets[size]
                    )
                    for size in (4, 5)
                ):
                    continue
                thirds += 1

        expected = reported_rows[orbit_id]
        if len(seconds) != int(expected["compatible_seconds"]):
            raise AssertionError("compatible-second count mismatch")
        if thirds != int(expected["compatible_ordered_thirds"]):
            raise AssertionError("compatible-third count mismatch")
        total_seconds += len(seconds)
        total_thirds += thirds
        replay_rows.append(
            {
                "representative": [
                    list(item) for item in representative
                ],
                "orbit_size": orbit_size,
                "compatible_seconds": len(seconds),
                "compatible_ordered_thirds": thirds,
            }
        )

    expected_counts = {
        "eligible_singleton_factors": len(factors),
        "individually_one_term_free_factors": len(safe_factors),
        "bad_two_edge_one_term_sets": len(bad_pairs),
        "matching_fork_triples": len(fork_sets[3]),
        "fork_free_safe_factors": len(rows),
        "fork_free_safe_factor_orbits": len(orbits),
        "compatible_seconds_across_orbits": total_seconds,
        "compatible_ordered_thirds_across_orbits": total_thirds,
    }
    for key, value in expected_counts.items():
        if int(enumeration[key]) != value:
            raise AssertionError(f"enumeration count mismatch: {key}")
    if total_thirds:
        raise AssertionError("C4+C5+C5 survivor remained")

    payload = {
        "verified": True,
        "status": "all_c4_c5_c5_equality_supports_closed",
        "claim_scope": (
            "all order-14,d=3 equality supports with full factor "
            "C4+C5+C5; not the other order-14 factors or global conjecture"
        ),
        "full_cycle_type": [4, 5, 5],
        **expected_counts,
        "matching_forks_by_size": {
            str(size): len(fork_sets[size]) for size in (3, 4, 5)
        },
        "full_automorphisms": len(actions),
        "enumeration": str(args.enumeration),
        "enumeration_sha256": file_sha256(args.enumeration),
        "catalogue": str(args.catalogue),
        "catalogue_sha256": file_sha256(args.catalogue),
        "catalogue_canonical_sha256": canonical_catalogue_sha,
        "orbit_rows": replay_rows,
        "logical_check": (
            "every catalogued obstruction was replayed semantically; "
            "the independently regenerated factor orbits have no "
            "obstruction-free ordered third factor"
        ),
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
