"""Independent replay of the explicit n=14 two-amplitude contradiction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

N = 14
Edge = tuple[int, int]
CYCLES = (
    (0, 1, 2),
    (3, 4, 5, 6),
    (7, 8, 9, 10, 11, 12, 13),
)
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


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


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def perfect_matchings(
    allowed: set[Edge],
) -> list[tuple[Edge, ...]]:
    adjacency = {
        vertex: {
            other
            for other in range(N)
            if other != vertex and edge(vertex, other) in allowed
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
    def monomial(matching: Sequence[Edge]) -> Counter[int]:
        output: Counter[int] = Counter()
        for item in matching:
            if item in FULL_EDGES:
                first_colour = int(colouring[item[0]])
                second_colour = int(colouring[item[1]])
            else:
                first_colour = second_colour = labels[item]
            output[
                9 * EDGE_INDEX[item]
                + 3 * first_colour
                + second_colour
            ] += 1
        return output

    result = monomial(first)
    result.subtract(monomial(second))
    return Counter(
        {entry: value for entry, value in result.items() if value}
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path(
            "tmp/minimal_singleton_counterexample_search_small.json"
        ),
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_binomial_trinomial_certificate.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_binomial_trinomial_verified.json"
        ),
    )
    args = parser.parse_args()
    candidate = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    certificate = json.loads(
        args.certificate.read_text(encoding="utf-8")
    )
    if certificate.get("status") != "direct_contradiction":
        raise AssertionError("producer certificate is incomplete")
    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in matching)
        for matching in candidate["best_singleton_matchings"]
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    if len(labels) != 3 * N // 2:
        raise AssertionError("singleton colour classes overlap")
    if set(labels) & set(FULL_EDGES):
        raise AssertionError("singleton/full support overlap")
    skeleton = set(FULL_EDGES) | set(labels)
    matchings = perfect_matchings(skeleton)
    if len(matchings) != int(
        certificate["skeleton_perfect_matchings"]
    ):
        raise AssertionError("skeleton matching count changed")

    origin_index = int(certificate["origin_equation_index"])
    target_index = int(certificate["target_equation_index"])
    origin_colouring = indexed_colouring(origin_index)
    target_colouring = indexed_colouring(target_index)
    if list(origin_colouring) != certificate["origin_colouring"]:
        raise AssertionError("origin equation index changed")
    if list(target_colouring) != certificate["target_colouring"]:
        raise AssertionError("target equation index changed")
    if len(set(origin_colouring)) == 1 or len(set(target_colouring)) == 1:
        raise AssertionError("certificate amplitude is monochromatic")
    origin_activity = active_matchings(
        matchings, origin_colouring, labels
    )
    target_activity = active_matchings(
        matchings, target_colouring, labels
    )
    if list(origin_activity) != certificate["origin_activity"]:
        raise AssertionError("origin activity changed")
    if list(target_activity) != certificate["target_activity"]:
        raise AssertionError("target activity changed")
    if len(origin_activity) != 2 or len(target_activity) != 3:
        raise AssertionError("certificate is not binomial/trinomial")
    pair = tuple(map(int, certificate["target_paired_matchings"]))
    survivor = int(certificate["target_surviving_matching"])
    if set(target_activity) != {*pair, survivor}:
        raise AssertionError("target pair/survivor partition changed")

    origin_relation = relation(
        matchings[origin_activity[0]],
        matchings[origin_activity[1]],
        origin_colouring,
        labels,
    )
    target_relation = relation(
        matchings[pair[0]],
        matchings[pair[1]],
        target_colouring,
        labels,
    )
    if not (
        origin_relation == target_relation
        or origin_relation
        == Counter(
            {
                entry: -value
                for entry, value in target_relation.items()
            }
        )
    ):
        raise AssertionError("Laurent relation transport changed")

    payload = {
        "verified": True,
        "scope": (
            "one explicit n=14,d=3 C3+C4+C7 equality support is "
            "impossible by a binomial-to-trinomial relation"
        ),
        "claim_scope": (
            "this support only; not the full C3+C4+C7 family or the "
            "global conjecture"
        ),
        "candidate": str(args.candidate),
        "candidate_sha256": sha256(args.candidate),
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "skeleton_perfect_matchings": len(matchings),
        "origin_equation_index": origin_index,
        "origin_activity": list(origin_activity),
        "target_equation_index": target_index,
        "target_activity": list(target_activity),
        "target_paired_matchings": list(pair),
        "target_surviving_matching": survivor,
        "verified_relation_entries": len(origin_relation),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
