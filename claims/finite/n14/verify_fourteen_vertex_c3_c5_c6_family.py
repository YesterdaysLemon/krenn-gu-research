"""Independent replay of the complete C3+C5+C6 equality-family proof."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

N = 14
CYCLES = (
    tuple(range(0, 3)),
    tuple(range(3, 8)),
    tuple(range(8, 14)),
)
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
Support = tuple[Factor, Factor, Factor]


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
    item: index for index, item in enumerate(ELIGIBLE_EDGES)
}
EDGE_VERTEX_MASK = tuple(
    (1 << first) | (1 << second)
    for first, second in ELIGIBLE_EDGES
)
ALL_VERTICES = (1 << N) - 1


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


def factor_mask(factor: Sequence[Edge]) -> int:
    return sum(1 << EDGE_ID[item] for item in factor)


FULL_ADJACENCY = [0] * N
for _first, _second in FULL_EDGES:
    FULL_ADJACENCY[_first] |= 1 << _second
    FULL_ADJACENCY[_second] |= 1 << _first


@lru_cache(maxsize=None)
def full_completion(remaining: int) -> int:
    """Count perfect matchings of the induced fixed full factor."""
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


def enumerate_perfect_factors(allowed: set[Edge]) -> list[Factor]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first

    @lru_cache(maxsize=None)
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


@lru_cache(maxsize=None)
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


@lru_cache(maxsize=None)
def pairings(vertices: tuple[int, ...]) -> tuple[Factor, ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remaining = vertices[1:position] + vertices[position + 1 :]
        for suffix in pairings(remaining):
            output.append((edge(first, second),) + suffix)
    return tuple(output)


def matching_id_sets(size: int):
    """Enumerate by chosen vertices, independently of edge recursion."""
    for vertices in itertools.combinations(range(N), 2 * size):
        for matching in pairings(vertices):
            if all(item in EDGE_ID for item in matching):
                yield tuple(sorted(EDGE_ID[item] for item in matching))


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


def fork_catalogue(size: int) -> set[int]:
    output = set()
    for target in matching_id_sets(size):
        rich = support_count(target)
        for position, removed_id in enumerate(target):
            sparse_ids = target[:position] + target[position + 1 :]
            sparse = support_count(sparse_ids)
            if not sparse or rich != sparse + 1:
                continue
            removed = ELIGIBLE_EDGES[removed_id]
            forced = any(
                count_containing_full_edge(
                    sparse_ids, edge(changed, partner)
                )
                == sparse
                for changed in removed
                for partner in FULL_NEIGHBOURS[changed]
            )
            if forced:
                output.add(sum(1 << item_id for item_id in target))
                break
    return output


def bad_pair_catalogue() -> set[int]:
    output = set()
    for first_id, second_id in itertools.combinations(
        range(len(ELIGIBLE_EDGES)), 2
    ):
        if EDGE_VERTEX_MASK[first_id] & EDGE_VERTEX_MASK[second_id]:
            continue
        if support_count((first_id, second_id)) == 1:
            output.add((1 << first_id) | (1 << second_id))
    return output


def pair_completion_masks(forks: Iterable[int]) -> dict[tuple[int, int], int]:
    output: dict[tuple[int, int], int] = {}
    for target in forks:
        ids = tuple(
            item_id
            for item_id in range(len(ELIGIBLE_EDGES))
            if target & (1 << item_id)
        )
        for first, second in itertools.combinations(ids, 2):
            third = next(
                item_id
                for item_id in ids
                if item_id not in {first, second}
            )
            output[(first, second)] = (
                output.get((first, second), 0) | (1 << third)
            )
    return output


def completion_mask(
    items: Iterable[Edge], pair_completions: dict[tuple[int, int], int]
) -> int:
    ids = sorted(EDGE_ID[item] for item in items)
    output = 0
    for first, second in itertools.combinations(ids, 2):
        output |= pair_completions.get((first, second), 0)
    return output


def bad_neighbour_mask(
    factor: Factor, bad_pairs: set[int]
) -> int:
    selected = factor_mask(factor)
    output = 0
    for target in bad_pairs:
        overlap = target & selected
        if overlap and overlap != target:
            output |= target ^ overlap
    return output


def dihedral_actions(cycle: Sequence[int]) -> list[dict[int, int]]:
    return [
        {
            cycle[position]: cycle[
                (rotation + direction * position) % len(cycle)
            ]
            for position in range(len(cycle))
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


def transform_factor(
    factor: Factor, action: dict[int, int]
) -> Factor:
    return tuple(
        sorted(edge(action[first], action[second]) for first, second in factor)
    )


def factor_orbits(
    factors: Iterable[Factor], actions: Sequence[dict[int, int]]
) -> list[tuple[Factor, int]]:
    unseen = set(factors)
    output = []
    while unseen:
        representative = min(unseen)
        orbit = {
            transform_factor(representative, action)
            for action in actions
        } & unseen
        output.append((representative, len(orbit)))
        unseen.difference_update(orbit)
    return output


def mask_contains_catalogue(
    selected: int, size: int, catalogue: set[int]
) -> bool:
    ids = [
        item_id
        for item_id in range(len(ELIGIBLE_EDGES))
        if selected & (1 << item_id)
    ]
    return any(
        sum(1 << item_id for item_id in target) in catalogue
        for target in itertools.combinations(ids, size)
    )


def support_canonical(
    support: Support, actions: Sequence[dict[int, int]]
) -> Support:
    return min(
        tuple(
            sorted(
                transform_factor(factor, action)
                for factor in support
            )
        )
        for action in actions
    )  # type: ignore[return-value]


def decode_support(item: dict[str, object]) -> Support:
    return tuple(
        tuple(
            sorted(
                edge(*map(int, raw))
                for raw in item[key]  # type: ignore[index]
            )
        )
        for key in ("first", "second", "third")
    )  # type: ignore[return-value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--enumeration",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c5_c6_family_enumeration.json"
        ),
    )
    parser.add_argument(
        "--catalogue",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c5_c6_obstruction_catalogue.json"
        ),
    )
    parser.add_argument(
        "--orbit-manifest",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c5_c6_fork5_survivor_orbits.json"
        ),
    )
    parser.add_argument(
        "--analysis-pattern",
        default=(
            "tmp/fourteen_vertex_c3_c5_c6_fork5_"
            "orbit{orbit}_signed_lattice.json"
        ),
    )
    parser.add_argument(
        "--verified-pattern",
        default=(
            "tmp/fourteen_vertex_c3_c5_c6_fork5_"
            "orbit{orbit}_signed_lattice_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c3_c5_c6_family_verified.json"
        ),
    )
    args = parser.parse_args()
    enumeration = json.loads(
        args.enumeration.read_text(encoding="utf-8")
    )
    catalogue = json.loads(
        args.catalogue.read_text(encoding="utf-8")
    )
    orbit_manifest = json.loads(
        args.orbit_manifest.read_text(encoding="utf-8")
    )
    if catalogue["partition"] != [3, 5, 6]:
        raise AssertionError("catalogue cycle type mismatch")
    if tuple(
        tuple(map(int, item)) for item in catalogue["eligible_edges"]
    ) != ELIGIBLE_EDGES:
        raise AssertionError("eligible-edge catalogue mismatch")

    bad_pairs = bad_pair_catalogue()
    fork_sets = {
        size: fork_catalogue(size) for size in (3, 4, 5)
    }
    if bad_pairs != set(
        map(int, catalogue["bad_two_edge_one_term_masks"])
    ):
        raise AssertionError("bad-pair catalogue mismatch")
    for size in (3, 4, 5):
        reported = set(
            map(
                int,
                catalogue["matching_fork_masks_by_size"][str(size)],
            )
        )
        if fork_sets[size] != reported:
            raise AssertionError(f"size-{size} fork catalogue mismatch")
    canonical_catalogue_sha = canonical_json_sha256(catalogue)
    if canonical_catalogue_sha != enumeration[
        "obstruction_catalogue_canonical_sha256"
    ]:
        raise AssertionError("catalogue hash binding mismatch")

    factors = enumerate_perfect_factors(set(ELIGIBLE_EDGES))
    safe_factors = [factor for factor in factors if factor_safe(factor)]
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
                bad_neighbour_mask(factor, bad_pairs),
                completion,
                factor,
            )
        )
    actions = automorphisms()
    orbits = factor_orbits((row[3] for row in rows), actions)
    row_by_factor = {row[3]: row[:3] for row in rows}
    ordered_candidates: list[Support] = []
    orbit_rows = []
    total_seconds = 0
    total_before_larger = 0
    for representative, orbit_size in orbits:
        first_edges, first_bad, first_completion = row_by_factor[
            representative
        ]
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
        surviving = 0
        before_larger = 0
        for second_edges, second_bad, _second_completion, second in seconds:
            selected_edges = first_edges | second_edges
            selected_bad = first_bad | second_bad
            selected_completion = completion_mask(
                set(representative) | set(second),
                pair_completions,
            )
            selected_has_larger = any(
                mask_contains_catalogue(
                    selected_edges, size, fork_sets[size]
                )
                for size in (4, 5)
            )
            for (
                third_edges,
                _third_bad,
                third_completion,
                third,
            ) in rows:
                if third_edges & (
                    selected_edges
                    | selected_bad
                    | selected_completion
                ):
                    continue
                if third_completion & selected_edges:
                    continue
                before_larger += 1
                if selected_has_larger:
                    continue
                union = selected_edges | third_edges
                if any(
                    mask_contains_catalogue(
                        union, size, fork_sets[size]
                    )
                    for size in (4, 5)
                ):
                    continue
                surviving += 1
                ordered_candidates.append(
                    (representative, second, third)
                )
        total_seconds += len(seconds)
        total_before_larger += before_larger
        orbit_rows.append(
            {
                "representative": [
                    list(item) for item in representative
                ],
                "orbit_size": orbit_size,
                "compatible_seconds": len(seconds),
                "before_larger_forks": before_larger,
                "surviving_ordered_thirds": surviving,
            }
        )

    canonical_supports: dict[Support, list[Support]] = defaultdict(list)
    for support in ordered_candidates:
        canonical_supports[support_canonical(support, actions)].append(
            support
        )
    reported_representatives = [
        decode_support(item) for item in orbit_manifest["survivors"]
    ]
    reported_canonical = {
        support_canonical(support, actions)
        for support in reported_representatives
    }
    if reported_canonical != set(canonical_supports):
        raise AssertionError("residual support orbit coverage mismatch")

    expected_counts = {
        "eligible_singleton_factors": len(factors),
        "individually_one_term_free_factors": len(safe_factors),
        "bad_two_edge_one_term_sets": len(bad_pairs),
        "matching_fork_triples": len(fork_sets[3]),
        "fork_free_safe_factors": len(rows),
        "fork_free_safe_factor_orbits": len(orbits),
        "compatible_seconds_across_orbits": total_seconds,
        "compatible_ordered_thirds_across_orbits": len(
            ordered_candidates
        ),
    }
    for key, value in expected_counts.items():
        if int(enumeration[key]) != value:
            raise AssertionError(f"enumeration count mismatch: {key}")
    if total_before_larger != 47936:
        raise AssertionError("unexpected pre-size-4/5 survivor count")
    if len(ordered_candidates) != 156:
        raise AssertionError("unexpected residual ordered support count")
    if len(canonical_supports) != 9:
        raise AssertionError("unexpected residual support orbit count")

    orbit_audits = []
    orbit_manifest_sha = file_sha256(args.orbit_manifest)
    for orbit in range(9):
        analysis_path = Path(
            args.analysis_pattern.format(orbit=orbit)
        )
        verified_path = Path(
            args.verified_pattern.format(orbit=orbit)
        )
        analysis = json.loads(
            analysis_path.read_text(encoding="utf-8")
        )
        verified = json.loads(
            verified_path.read_text(encoding="utf-8")
        )
        if analysis.get("status") != "contradiction":
            raise AssertionError("orbit analysis is not a contradiction")
        if int(analysis["survivor_index"]) != orbit:
            raise AssertionError("orbit analysis index mismatch")
        if not verified.get("verified"):
            raise AssertionError("orbit algebra was not independently replayed")
        if int(verified["survivor_index"]) != orbit:
            raise AssertionError("verified orbit index mismatch")
        if verified["exploration_sha256"] != orbit_manifest_sha:
            raise AssertionError("verified orbit manifest hash mismatch")
        if verified["analysis_sha256"] != file_sha256(analysis_path):
            raise AssertionError("verified analysis hash mismatch")
        orbit_audits.append(
            {
                "orbit": orbit,
                "analysis": str(analysis_path),
                "analysis_sha256": file_sha256(analysis_path),
                "verified": str(verified_path),
                "verified_sha256": file_sha256(verified_path),
                "signed_lattice_rank": int(
                    analysis["signed_lattice_rank"]
                ),
                "used_basis_relations": int(
                    verified["used_basis_relations"]
                ),
                "target_equation_index": int(
                    verified["target_equation_index"]
                ),
            }
        )

    payload = {
        "verified": True,
        "status": "all_c3_c5_c6_equality_supports_closed",
        "claim_scope": (
            "all order-14,d=3 equality supports with full factor "
            "C3+C5+C6; not the other order-14 factors or global conjecture"
        ),
        "full_cycle_type": [3, 5, 6],
        **expected_counts,
        "matching_forks_by_size": {
            str(size): len(fork_sets[size]) for size in (3, 4, 5)
        },
        "pre_larger_fork_ordered_thirds": total_before_larger,
        "residual_ordered_supports": len(ordered_candidates),
        "residual_support_orbits": len(canonical_supports),
        "full_automorphisms": len(actions),
        "enumeration": str(args.enumeration),
        "enumeration_sha256": file_sha256(args.enumeration),
        "catalogue": str(args.catalogue),
        "catalogue_sha256": file_sha256(args.catalogue),
        "catalogue_canonical_sha256": canonical_catalogue_sha,
        "orbit_manifest": str(args.orbit_manifest),
        "orbit_manifest_sha256": orbit_manifest_sha,
        "orbit_rows": orbit_rows,
        "algebraic_orbit_audits": orbit_audits,
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
                if key not in {"orbit_rows", "algebraic_orbit_audits"}
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
