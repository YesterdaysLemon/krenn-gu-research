"""Independent final audit for all n=10 C10 equality supports."""

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
CYCLE = tuple(range(N))
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


FULL_EDGES = {
    edge(CYCLE[index], CYCLE[(index + 1) % N])
    for index in range(N)
}


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


def matching_mask(matching: Sequence[Edge]) -> int:
    return sum(1 << EDGE_INDEX[item] for item in matching)


def automorphisms() -> list[tuple[int, ...]]:
    return sorted(
        {
            tuple(
                (shift + orientation * vertex) % N
                for vertex in range(N)
            )
            for shift in range(N)
            for orientation in (1, -1)
        }
    )


def transform(mask: int, permutation: Sequence[int]) -> int:
    result = 0
    for index, (first, second) in enumerate(ALL_EDGES):
        if mask & (1 << index):
            result |= 1 << EDGE_INDEX[
                edge(permutation[first], permutation[second])
            ]
    return result


def active_matchings(
    matchings: Sequence[Sequence[Edge]],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item in FULL_EDGES
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        )
    )


def relation(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> Counter[int]:
    def variables(matching: Sequence[Edge]) -> list[int]:
        output = []
        for item in matching:
            if item in FULL_EDGES:
                first_colour = int(colouring[item[0]])
                second_colour = int(colouring[item[1]])
            else:
                first_colour = second_colour = labels[item]
            output.append(
                9 * EDGE_INDEX[item]
                + 3 * first_colour
                + second_colour
            )
        return output

    result = Counter(variables(first))
    result.subtract(variables(second))
    return Counter(
        {entry: value for entry, value in result.items() if value}
    )


def linear_combination(
    vectors: Sequence[Counter[int]],
    coefficients: Sequence[int],
) -> Counter[int]:
    result: Counter[int] = Counter()
    for vector, coefficient in zip(
        vectors, coefficients, strict=True
    ):
        for entry, value in vector.items():
            result[entry] += coefficient * value
    return Counter(
        {entry: value for entry, value in result.items() if value}
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbits",
        type=Path,
        default=Path("tmp/ten_vertex_c10_equality_support_orbits.json"),
    )
    parser.add_argument(
        "--certificates",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c10_equality_support_transport.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c10_equality_family_verified.json"
        ),
    )
    args = parser.parse_args()
    catalogue = json.loads(args.orbits.read_text(encoding="utf-8"))
    certificates = json.loads(
        args.certificates.read_text(encoding="utf-8")
    )
    if catalogue.get("status") != "complete":
        raise AssertionError("orbit catalogue is incomplete")
    if certificates.get("status") != "all_direct":
        raise AssertionError("transport certificate run is incomplete")
    if catalogue["full_cycle_type"] != [10]:
        raise AssertionError("catalogue is not C10")
    if len(catalogue["rows"]) != len(certificates["rows"]):
        raise AssertionError("catalogue/certificate row count mismatch")

    complete = perfect_matchings()
    candidates = [
        matching
        for matching in complete
        if not (set(matching) & FULL_EDGES)
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
    permutations = automorphisms()
    if len(permutations) != 20:
        raise AssertionError("C10 automorphism count changed")
    representatives: set[tuple[int, int, int]] = set()
    orbit_total = 0
    checks: list[dict[str, object]] = []
    for index, (orbit, certificate) in enumerate(
        zip(catalogue["rows"], certificates["rows"], strict=True)
    ):
        representative = tuple(
            map(int, orbit["singleton_matching_masks"])
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
        if len(images) != int(orbit["orbit_size_uncoloured"]):
            raise AssertionError("orbit size changed")
        if representative in representatives:
            raise AssertionError("duplicate orbit representative")
        representatives.add(representative)
        orbit_total += len(images)
        if certificate["singleton_matchings"] != orbit[
            "singleton_matchings"
        ]:
            raise AssertionError("certificate support changed")

        singleton_matchings = [
            [edge(*map(int, item)) for item in matching]
            for matching in orbit["singleton_matchings"]
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
        labels = {
            item: colour
            for colour, matching in enumerate(singleton_matchings)
            for item in matching
        }
        if len(labels) != 15:
            raise AssertionError("singleton matchings overlap")
        skeleton = FULL_EDGES | set(labels)
        matchings = perfect_matchings(skeleton)
        origin_indices = list(
            map(int, certificate["transport_binomial_equation_indices"])
        )
        origin_colourings = [
            tuple(map(int, colouring))
            for colouring in certificate[
                "transport_binomial_colourings"
            ]
        ]
        signs = list(map(int, certificate["transport_relation_signs"]))
        if signs != [1, -1, 1]:
            raise AssertionError("transport signs changed")
        origin_activities = []
        origin_relations = []
        for origin_index, colouring in zip(
            origin_indices, origin_colourings, strict=True
        ):
            if colouring != indexed_colouring(origin_index):
                raise AssertionError("origin equation index changed")
            if len(set(colouring)) == 1:
                raise AssertionError("origin amplitude is not forbidden")
            activity = active_matchings(matchings, colouring, labels)
            if len(activity) != 2:
                raise AssertionError("transport origin is not binomial")
            origin_activities.append(list(activity))
            origin_relations.append(
                relation(
                    matchings[activity[0]],
                    matchings[activity[1]],
                    colouring,
                    labels,
                )
            )
        if origin_activities != certificate[
            "transport_binomial_activities"
        ]:
            raise AssertionError("transport origin activities changed")
        if len({tuple(activity) for activity in origin_activities}) != 1:
            raise AssertionError("transport origins use different pairs")

        target_colouring = tuple(
            map(int, certificate["target_colouring"])
        )
        if target_colouring != indexed_colouring(
            int(certificate["target_equation_index"])
        ):
            raise AssertionError("target equation index changed")
        if len(set(target_colouring)) == 1:
            raise AssertionError("target amplitude is not forbidden")
        target_activity = active_matchings(
            matchings, target_colouring, labels
        )
        if list(target_activity) != certificate["target_activity"]:
            raise AssertionError("target activity changed")
        if len(target_activity) != 3:
            raise AssertionError("target is not trinomial")
        pair = tuple(map(int, certificate["paired_matching_indices"]))
        if set(pair) != set(origin_activities[0]):
            raise AssertionError("transport pair changed")
        survivor = int(certificate["surviving_matching_index"])
        if set(target_activity) != {*pair, survivor}:
            raise AssertionError("target pair/survivor partition changed")
        target_relation = relation(
            matchings[pair[0]],
            matchings[pair[1]],
            target_colouring,
            labels,
        )
        if linear_combination(origin_relations, signs) != target_relation:
            raise AssertionError("transport relation identity changed")
        checks.append(
            {
                "orbit_index": index,
                "orbit_size_uncoloured": len(images),
                "skeleton_perfect_matchings": len(matchings),
                "origin_equation_indices": origin_indices,
                "target_equation_index": int(
                    certificate["target_equation_index"]
                ),
                "verified": True,
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
        raise AssertionError("orbit union does not cover raw factorizations")
    if raw_count != int(catalogue["raw_uncoloured_factorizations"]):
        raise AssertionError("raw factorization count changed")
    labelled_factors = math.factorial(N) // (2 * N)
    labelled_supports = labelled_factors * raw_count * math.factorial(3)
    payload = {
        "verified": True,
        "scope": "all n=10,d=3 equality supports with full-factor C10",
        "claim_scope": (
            "this equality family only; not supports below equality or "
            "the global conjecture"
        ),
        "orbit_catalogue": str(args.orbits),
        "orbit_catalogue_sha256": sha256(args.orbits),
        "certificate_manifest": str(args.certificates),
        "certificate_manifest_sha256": sha256(args.certificates),
        "full_cycle_type": [10],
        "factor_automorphisms": len(permutations),
        "candidate_singleton_matchings": len(candidates),
        "raw_uncoloured_factorizations": raw_count,
        "support_orbits": len(representatives),
        "labelled_full_factors": labelled_factors,
        "labelled_coloured_supports": labelled_supports,
        "verified_transport_certificates": len(checks),
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
