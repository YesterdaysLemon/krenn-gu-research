"""Find a binomial-to-trinomial contradiction in the explicit n=14 support."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Sequence

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.verify_fourteen_vertex_no_one_term_support import (
    CYCLES,
    FULL_EDGES,
    N,
    Edge,
    edge,
    perfect_matchings,
)

ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


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


def relation_signature(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
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

    vector: Counter[int] = Counter(variables(first))
    vector.subtract(variables(second))
    direct = tuple(
        sorted(
            (entry, coefficient)
            for entry, coefficient in vector.items()
            if coefficient
        )
    )
    negative = tuple(
        (entry, -coefficient) for entry, coefficient in direct
    )
    return min(direct, negative)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path(
            "tmp/minimal_singleton_counterexample_search_small.json"
        ),
    )
    parser.add_argument("--prefix", type=int, default=400)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_binomial_trinomial_certificate.json"
        ),
    )
    args = parser.parse_args()
    candidate = json.loads(
        args.candidate.read_text(encoding="utf-8")
    )
    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in matching)
        for matching in candidate["best_singleton_matchings"]
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    skeleton = set(FULL_EDGES) | set(labels)
    matchings = perfect_matchings(skeleton)
    activities = [
        active_matchings(
            matchings, indexed_colouring(index), labels
        )
        for index in range(args.prefix)
    ]
    relations: dict[tuple[tuple[int, int], ...], int] = {}
    for index, activity in enumerate(activities):
        if len(activity) != 2:
            continue
        signature = relation_signature(
            matchings[activity[0]],
            matchings[activity[1]],
            indexed_colouring(index),
            labels,
        )
        relations.setdefault(signature, index)
    found: dict[str, object] | None = None
    for target_index, activity in enumerate(activities):
        if len(activity) != 3:
            continue
        for first, second in itertools.combinations(activity, 2):
            signature = relation_signature(
                matchings[first],
                matchings[second],
                indexed_colouring(target_index),
                labels,
            )
            if signature not in relations:
                continue
            origin_index = relations[signature]
            origin_activity = activities[origin_index]
            survivor = next(
                item for item in activity if item not in {first, second}
            )
            found = {
                "origin_equation_index": origin_index,
                "origin_colouring": list(
                    indexed_colouring(origin_index)
                ),
                "origin_activity": list(origin_activity),
                "target_equation_index": target_index,
                "target_colouring": list(
                    indexed_colouring(target_index)
                ),
                "target_activity": list(activity),
                "target_paired_matchings": [first, second],
                "target_surviving_matching": survivor,
                "relation_signature": [
                    list(item) for item in signature
                ],
            }
            break
        if found is not None:
            break
    if found is None:
        raise RuntimeError("no binomial-to-trinomial certificate found")
    payload = {
        "status": "direct_contradiction",
        "scope": (
            "one explicit n=14,d=3 C3+C4+C7 equality support"
        ),
        "necessary_conditions_only": False,
        "candidate": str(args.candidate),
        "full_cycle_type": [len(cycle) for cycle in CYCLES],
        "skeleton_perfect_matchings": len(matchings),
        "search_prefix": args.prefix,
        "binomial_colourings_in_prefix": sum(
            len(activity) == 2 for activity in activities
        ),
        "trinomial_colourings_in_prefix": sum(
            len(activity) == 3 for activity in activities
        ),
        **found,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
