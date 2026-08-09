"""Independent final audit for all n=10 C4+C6 equality supports."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path
from typing import Sequence

N = 10
Edge = tuple[int, int]
Entry = tuple[str, int, int, int, int]
CYCLES = (tuple(range(4)), tuple(range(4, 10)))
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


FULL_EDGES = frozenset(
    item for cycle in CYCLES for item in cycle_edges(cycle)
)


def perfect_matchings(
    allowed: set[Edge] | None = None,
) -> list[tuple[Edge, ...]]:
    adjacency = {
        vertex: {
            other
            for other in range(N)
            if other != vertex
            and (
                allowed is None
                or edge(vertex, other) in allowed
            )
        }
        for vertex in range(N)
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

    visit(frozenset(range(N)), ())
    return result


def matching_mask(matching: Sequence[Edge]) -> int:
    return sum(1 << EDGE_INDEX[item] for item in matching)


def dihedral(cycle: Sequence[int]) -> list[dict[int, int]]:
    size = len(cycle)
    maps: list[dict[int, int]] = []
    for shift in range(size):
        maps.append(
            {
                int(cycle[index]): int(cycle[(index + shift) % size])
                for index in range(size)
            }
        )
        maps.append(
            {
                int(cycle[index]): int(cycle[(shift - index) % size])
                for index in range(size)
            }
        )
    return maps


def factor_automorphisms() -> list[tuple[int, ...]]:
    result = []
    for first in dihedral(CYCLES[0]):
        for second in dihedral(CYCLES[1]):
            mapping = {**first, **second}
            result.append(tuple(mapping[vertex] for vertex in range(N)))
    result = sorted(set(result))
    if len(result) != 96:
        raise AssertionError("factor automorphism count changed")
    return result


def transform(mask: int, permutation: Sequence[int]) -> int:
    result = 0
    for index, (first, second) in enumerate(ALL_EDGES):
        if mask & (1 << index):
            image = edge(permutation[first], permutation[second])
            result |= 1 << EDGE_INDEX[image]
    return result


def active_matchings(
    matchings: Sequence[Sequence[Edge]],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    result: list[int] = []
    for matching_id, matching in enumerate(matchings):
        if all(
            item in FULL_EDGES
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        ):
            result.append(matching_id)
    return tuple(result)


def monomial(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> Counter[Entry]:
    result: Counter[Entry] = Counter()
    for item in matching:
        if item in FULL_EDGES:
            result[
                (
                    "F",
                    item[0],
                    item[1],
                    int(colouring[item[0]]),
                    int(colouring[item[1]]),
                )
            ] += 1
        else:
            colour = labels[item]
            result[("S", item[0], item[1], colour, colour)] += 1
    return result


def subtract(
    first: Counter[Entry], second: Counter[Entry]
) -> Counter[Entry]:
    result = first.copy()
    result.subtract(second)
    return Counter(
        {entry: value for entry, value in result.items() if value}
    )


def negate(vector: Counter[Entry]) -> Counter[Entry]:
    return Counter({entry: -value for entry, value in vector.items()})


def relation(
    cycle: Sequence[int], colouring: Sequence[int]
) -> Counter[Entry]:
    result: Counter[Entry] = Counter()
    for index, first in enumerate(cycle):
        item = edge(first, cycle[(index + 1) % len(cycle)])
        entry = (
            "F",
            item[0],
            item[1],
            int(colouring[item[0]]),
            int(colouring[item[1]]),
        )
        result[entry] += 1 if index % 2 == 0 else -1
    return result


def same_up_to_sign(
    first: Counter[Entry], second: Counter[Entry]
) -> bool:
    return first == second or first == negate(second)


def verify_fork(
    singleton_matchings: Sequence[Sequence[Edge]],
    certificate: dict[str, object],
) -> dict[str, object]:
    labels = {
        tuple(map(int, item)): colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    if len(labels) != 15:
        raise AssertionError("singleton matchings are not edge-disjoint")
    skeleton = set(FULL_EDGES) | set(labels)
    if any(
        sum(vertex in item for item in skeleton) != 5
        for vertex in range(N)
    ):
        raise AssertionError("support skeleton is not 5-regular")
    matchings = perfect_matchings(skeleton)
    full_only = tuple(
        index
        for index, matching in enumerate(matchings)
        if set(matching) <= set(FULL_EDGES)
    )
    if len(full_only) != 4:
        raise AssertionError("C4+C6 has the wrong full-only activity")

    fork = certificate["fork"]
    base = tuple(map(int, fork["base_colouring"]))
    if base != indexed_colouring(int(fork["base_colouring_index"])):
        raise AssertionError("base colouring index changed")
    if len(base) != N or len(set(base)) == 1:
        raise AssertionError("base colouring is not forbidden")
    if active_matchings(matchings, base, labels) != full_only:
        raise AssertionError("base amplitude is not exactly full-only")
    for cycle_index, (cycle, alternative) in enumerate(
        zip(CYCLES, fork["alternatives"], strict=True)
    ):
        if list(cycle) != list(map(int, alternative["cycle"])):
            raise AssertionError("fork cycle order changed")
        target = tuple(map(int, alternative["target_colouring"]))
        if target != indexed_colouring(
            int(alternative["target_colouring_index"])
        ):
            raise AssertionError("target colouring index changed")
        if len(target) != N or len(set(target)) == 1:
            raise AssertionError("target colouring is not forbidden")
        if any(target[vertex] != base[vertex] for vertex in cycle):
            raise AssertionError("target changed the forced cycle relation")
        activity = active_matchings(matchings, target, labels)
        if len(activity) != 5 or not set(full_only) < set(activity):
            raise AssertionError("target is not four full terms plus one")
        extra = next(index for index in activity if index not in full_only)
        if set(matchings[extra]) <= set(FULL_EDGES):
            raise AssertionError("extra matching has no singleton entry")

        direction = relation(cycle, base)
        cycle_set = cycle_edges(cycle)
        paired: set[int] = set()
        for matching_id in full_only:
            if matching_id in paired:
                continue
            matching_set = set(matchings[matching_id])
            flipped_set = matching_set ^ set(cycle_set)
            partner = next(
                (
                    other
                    for other in full_only
                    if set(matchings[other]) == flipped_set
                ),
                None,
            )
            if partner is None:
                raise AssertionError("full matching has no cycle flip")
            raw_difference = subtract(
                monomial(matchings[matching_id], target, labels),
                monomial(matchings[partner], target, labels),
            )
            if not same_up_to_sign(raw_difference, direction):
                raise AssertionError("cycle relation does not pair terms")
            paired.update((matching_id, partner))
        if paired != set(full_only):
            raise AssertionError("cycle relation does not pair all full terms")
    return {
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matchings": len(full_only),
        "base_equation_terms": len(full_only),
        "alternative_target_terms": [5, 5],
        "verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbits",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_support_orbits.json"
        ),
    )
    parser.add_argument(
        "--forks",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_support_forks.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_family_verified.json"
        ),
    )
    args = parser.parse_args()
    catalogue = json.loads(args.orbits.read_text(encoding="utf-8"))
    forks = json.loads(args.forks.read_text(encoding="utf-8"))
    if forks.get("status") != "all_forked":
        raise AssertionError("fork producer is incomplete")
    if len(catalogue["rows"]) != len(forks["rows"]):
        raise AssertionError("catalogue/fork row count mismatch")

    complete = perfect_matchings()
    candidates = [
        matching
        for matching in complete
        if not (set(matching) & set(FULL_EDGES))
    ]
    masks = [matching_mask(matching) for matching in candidates]
    candidate_masks = set(masks)
    raw_count = sum(
        1
        for first_index, first in enumerate(masks)
        for second_index in range(first_index + 1, len(masks))
        for second in (masks[second_index],)
        if not first & second
        for third in masks[second_index + 1 :]
        if not first & third and not second & third
    )
    if raw_count != 446_592:
        raise AssertionError("independent raw triple count changed")
    permutations = factor_automorphisms()
    representatives: set[tuple[int, int, int]] = set()
    orbit_total = 0
    checks: list[dict[str, object]] = []
    for index, (catalogue_row, fork_row) in enumerate(
        zip(catalogue["rows"], forks["rows"], strict=True)
    ):
        representative = tuple(
            map(int, catalogue_row["singleton_matching_masks"])
        )
        if representative != tuple(sorted(representative)):
            raise AssertionError("representative matching order changed")
        images = {
            tuple(
                sorted(transform(mask, permutation) for mask in representative)
            )
            for permutation in permutations
        }
        if representative != min(images):
            raise AssertionError("orbit representative is not canonical")
        if len(images) != int(catalogue_row["orbit_size_uncoloured"]):
            raise AssertionError("orbit size changed")
        if representative in representatives:
            raise AssertionError("duplicate orbit representative")
        representatives.add(representative)
        orbit_total += len(images)
        if fork_row["singleton_matchings"] != catalogue_row[
            "singleton_matchings"
        ]:
            raise AssertionError("fork support changed")
        singleton_matchings = [
            [edge(*map(int, item)) for item in matching]
            for matching in catalogue_row["singleton_matchings"]
        ]
        reconstructed_masks = tuple(
            sorted(matching_mask(matching) for matching in singleton_matchings)
        )
        if reconstructed_masks != representative:
            raise AssertionError("matching masks do not encode the support")
        if any(mask not in candidate_masks for mask in reconstructed_masks):
            raise AssertionError(
                "singleton colour class is not a perfect matching "
                "disjoint from the full factor"
            )
        direct = verify_fork(singleton_matchings, fork_row)
        checks.append(
            {
                "orbit_index": index,
                "orbit_size_uncoloured": len(images),
                **direct,
            }
        )
        if (index + 1) % 100 == 0 or index + 1 == len(
            catalogue["rows"]
        ):
            print(
                f"orbit={index + 1}/{len(catalogue['rows'])} verified",
                flush=True,
            )
    if orbit_total != raw_count:
        raise AssertionError("canonical orbit union does not cover raw triples")
    if len(representatives) != 4_903:
        raise AssertionError("support orbit count changed")
    labelled_factors = (
        math.comb(N, 4)
        * math.factorial(4 - 1)
        // 2
        * math.factorial(6 - 1)
        // 2
    )
    if labelled_factors != 37_800:
        raise AssertionError("labelled C4+C6 factor count changed")
    labelled_coloured_supports = (
        labelled_factors * raw_count * math.factorial(3)
    )

    payload = {
        "verified": True,
        "scope": (
            "all n=10,d=3 equality supports with a full-block C4+C6 "
            "2-factor"
        ),
        "claim_scope": (
            "excludes this complete equality architecture only; does not "
            "cover C10 or odd-cycle full factors, arbitrary supports, or "
            "the global Krenn-Gu conjecture"
        ),
        "orbit_catalogue": str(args.orbits),
        "orbit_catalogue_sha256": sha256(args.orbits),
        "fork_manifest": str(args.forks),
        "fork_manifest_sha256": sha256(args.forks),
        "factor_automorphisms": len(permutations),
        "candidate_singleton_matchings": len(candidates),
        "raw_uncoloured_factorizations": raw_count,
        "support_orbits": len(representatives),
        "labelled_full_factors": labelled_factors,
        "labelled_coloured_supports": labelled_coloured_supports,
        "verified_forks": len(checks),
        "checks": checks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "checks"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
