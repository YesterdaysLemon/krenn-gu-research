"""Independent final audit for one odd-cycle n=10 equality factor type."""

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


def cycle_edges(cycle: Sequence[int]) -> set[Edge]:
    return {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
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


def component_images(
    cycles: Sequence[Sequence[int]],
) -> list[tuple[int, ...]]:
    length_groups: dict[int, list[int]] = {}
    for index, cycle in enumerate(cycles):
        length_groups.setdefault(len(cycle), []).append(index)
    group_rows = sorted(length_groups.items())
    results: list[tuple[int, ...]] = []
    for choices in itertools.product(
        *[
            list(itertools.permutations(indices))
            for _length, indices in group_rows
        ]
    ):
        image = list(range(len(cycles)))
        for (_length, sources), targets in zip(
            group_rows, choices, strict=True
        ):
            for source, target in zip(sources, targets, strict=True):
                image[source] = target
        results.append(tuple(image))
    return results


def factor_automorphisms(
    cycles: Sequence[Sequence[int]],
) -> list[tuple[int, ...]]:
    results: set[tuple[int, ...]] = set()
    for images in component_images(cycles):
        local_options = [
            list(itertools.product(range(len(cycle)), (1, -1)))
            for cycle in cycles
        ]
        for choices in itertools.product(*local_options):
            permutation = [0] * N
            for source_id, source in enumerate(cycles):
                target = cycles[images[source_id]]
                shift, orientation = choices[source_id]
                for position, vertex in enumerate(source):
                    permutation[vertex] = target[
                        (shift + orientation * position) % len(source)
                    ]
            results.add(tuple(permutation))
    return sorted(results)


def transform(mask: int, permutation: Sequence[int]) -> int:
    result = 0
    for index, (first, second) in enumerate(ALL_EDGES):
        if mask & (1 << index):
            image = edge(permutation[first], permutation[second])
            result |= 1 << EDGE_INDEX[image]
    return result


def active(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> bool:
    return all(
        item in full_edges
        or (
            colouring[item[0]]
            == colouring[item[1]]
            == labels[item]
        )
        for item in matching
    )


def labelled_factor_count(lengths: Sequence[int]) -> int:
    multiplicities = Counter(lengths)
    denominator = math.prod(2 * length for length in lengths)
    denominator *= math.prod(
        math.factorial(count) for count in multiplicities.values()
    )
    return math.factorial(N) // denominator


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--certificates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    catalogue = json.loads(args.orbits.read_text(encoding="utf-8"))
    certificates = json.loads(
        args.certificates.read_text(encoding="utf-8")
    )
    if catalogue.get("status") != "complete":
        raise AssertionError("orbit catalogue is incomplete")
    if certificates.get("status") != "all_one_term":
        raise AssertionError("one-term certificate run is incomplete")
    cycles = [
        tuple(map(int, cycle)) for cycle in catalogue["full_cycles"]
    ]
    lengths = tuple(map(len, cycles))
    if all(length % 2 == 0 for length in lengths):
        raise AssertionError("factor has no odd cycle")
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    complete = perfect_matchings()
    candidates = [
        matching
        for matching in complete
        if not (set(matching) & full_edges)
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
    permutations = factor_automorphisms(cycles)
    if len(permutations) != int(catalogue["factor_automorphisms"]):
        raise AssertionError("factor automorphism count changed")
    if len(catalogue["rows"]) != len(certificates["rows"]):
        raise AssertionError("catalogue/certificate row count mismatch")
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
        skeleton = full_edges | set(labels)
        matchings = perfect_matchings(skeleton)
        colouring = tuple(map(int, certificate["colouring"]))
        if colouring != indexed_colouring(
            int(certificate["equation_index"])
        ):
            raise AssertionError("certificate equation index changed")
        if len(colouring) != N or len(set(colouring)) == 1:
            raise AssertionError("certificate colouring is not forbidden")
        activity = tuple(
            matching_id
            for matching_id, matching in enumerate(matchings)
            if active(matching, colouring, full_edges, labels)
        )
        if len(activity) != 1:
            raise AssertionError("certificate is not a one-term amplitude")
        matching_id = activity[0]
        if matching_id != int(certificate["unique_matching_index"]):
            raise AssertionError("unique matching index changed")
        if [list(item) for item in matchings[matching_id]] != certificate[
            "unique_matching"
        ]:
            raise AssertionError("unique matching edges changed")
        # Every edge of the unique matching selects a supported nonzero
        # matrix entry, so its product is nonzero and cannot equal the
        # required zero forbidden amplitude.
        checks.append(
            {
                "orbit_index": index,
                "orbit_size_uncoloured": len(images),
                "skeleton_perfect_matchings": len(matchings),
                "equation_index": int(certificate["equation_index"]),
                "unique_matching_index": matching_id,
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
        raise AssertionError("orbit union does not cover raw triples")
    if raw_count != int(catalogue["raw_uncoloured_factorizations"]):
        raise AssertionError("raw factorization count changed")
    labelled_factors = labelled_factor_count(lengths)
    labelled_supports = labelled_factors * raw_count * math.factorial(3)
    payload = {
        "verified": True,
        "scope": (
            "all n=10,d=3 equality supports with full-factor type "
            f"{list(lengths)}"
        ),
        "claim_scope": (
            "this full-factor equality family only; not other factor "
            "types, supports below equality, or the global conjecture"
        ),
        "orbit_catalogue": str(args.orbits),
        "orbit_catalogue_sha256": sha256(args.orbits),
        "certificate_manifest": str(args.certificates),
        "certificate_manifest_sha256": sha256(args.certificates),
        "full_cycle_type": list(lengths),
        "factor_automorphisms": len(permutations),
        "candidate_singleton_matchings": len(candidates),
        "raw_uncoloured_factorizations": raw_count,
        "support_orbits": len(representatives),
        "labelled_full_factors": labelled_factors,
        "labelled_coloured_supports": labelled_supports,
        "verified_one_term_certificates": len(checks),
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
