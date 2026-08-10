"""Audit the analytic two-vertex rectangle theorem for the C14 family."""

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
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Sequence

N = 14
Edge = tuple[int, int]
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}
CYCLE = tuple(range(N))


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


FULL_EDGES = {
    edge(CYCLE[position], CYCLE[(position + 1) % N])
    for position in range(N)
}
ELIGIBLE_EDGES = set(ALL_EDGES) - FULL_EDGES


def perfect_matchings(allowed: set[Edge]) -> list[tuple[Edge, ...]]:
    adjacency = [0] * N
    for first, second in allowed:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first

    @lru_cache(maxsize=None)
    def visit(remaining: int) -> tuple[tuple[Edge, ...], ...]:
        if not remaining:
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

    return sorted(visit((1 << N) - 1))


def proper_two_colouring(edges: set[Edge]) -> tuple[int, ...]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    colours = [-1] * N
    for start in range(N):
        if colours[start] >= 0:
            continue
        colours[start] = 1
        stack = [start]
        while stack:
            current = stack.pop()
            for other in adjacency[current]:
                expected = 3 - colours[current]
                if colours[other] < 0:
                    colours[other] = expected
                    stack.append(other)
                elif colours[other] != expected:
                    raise AssertionError(
                        "union of two factors is not bipartite"
                    )
    return tuple(colours)


def active_singletons(
    colouring: Sequence[int], labels: dict[Edge, int]
) -> set[Edge]:
    return {
        item
        for item, colour in labels.items()
        if (
            colouring[item[0]]
            == colouring[item[1]]
            == colour
        )
    }


def active_matching_ids(
    matchings: Sequence[Sequence[Edge]],
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> list[int]:
    return [
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
    ]


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

    output = monomial(first)
    output.subtract(monomial(second))
    return Counter(
        {
            variable: coefficient
            for variable, coefficient in output.items()
            if coefficient
        }
    )


def decode_support(item: dict[str, object]):
    return [
        tuple(
            edge(*map(int, raw))
            for raw in item[key]  # type: ignore[index]
        )
        for key in ("first", "second", "third")
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=Path,
        default=Path("tmp/fourteen_vertex_c14_support_samples.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c14_rectangle_theorem_verified.json"
        ),
    )
    args = parser.parse_args()
    source = json.loads(args.samples.read_text(encoding="utf-8"))
    if source["partition"] != [14]:
        raise AssertionError("sample source is not C14")

    eligible_factors = perfect_matchings(ELIGIBLE_EDGES)
    cross_histogram: Counter[int] = Counter(
        sum((first % 2) != (second % 2) for first, second in factor)
        for factor in eligible_factors
    )
    if not eligible_factors or min(cross_histogram) < 1:
        raise AssertionError(
            "an eligible factor without a bipartition-crossing chord exists"
        )

    sample_checks = []
    for sample_id, raw_support in enumerate(source["survivors"]):
        singleton_matchings = decode_support(raw_support)
        labels = {
            item: colour
            for colour, matching in enumerate(singleton_matchings)
            for item in matching
        }
        if len(labels) != 3 * N // 2:
            raise AssertionError("singleton factors overlap")
        if set(labels) & FULL_EDGES:
            raise AssertionError("singleton/full factors overlap")
        chord = next(
            item
            for item in singleton_matchings[0]
            if (item[0] % 2) != (item[1] % 2)
        )
        x, z = chord
        if chord in FULL_EDGES:
            raise AssertionError("chosen chord is a cycle edge")
        base = proper_two_colouring(
            set(singleton_matchings[1])
            | set(singleton_matchings[2])
        )
        corner_x = list(base)
        corner_x[x] = 0
        corner_z = list(base)
        corner_z[z] = 0
        target = list(base)
        target[x] = 0
        target[z] = 0
        colourings = (
            base,
            tuple(corner_x),
            tuple(corner_z),
            tuple(target),
        )
        expected_singletons = (set(), set(), set(), {chord})
        for colouring, expected in zip(
            colourings, expected_singletons, strict=True
        ):
            if active_singletons(colouring, labels) != expected:
                raise AssertionError(
                    "rectangle singleton activation mismatch"
                )
            if len(set(colouring)) == 1:
                raise AssertionError(
                    "rectangle colouring is monochromatic"
                )
        matchings = perfect_matchings(FULL_EDGES | set(labels))
        full_only = [
            matching_id
            for matching_id, matching in enumerate(matchings)
            if all(item in FULL_EDGES for item in matching)
        ]
        if len(full_only) != 2:
            raise AssertionError("C14 does not have two alternatings")
        activities = [
            active_matching_ids(matchings, colouring, labels)
            for colouring in colourings
        ]
        if any(activity != full_only for activity in activities[:3]):
            raise AssertionError("a rectangle corner is not full-only")
        if (
            len(activities[3]) != 3
            or not set(full_only).issubset(activities[3])
        ):
            raise AssertionError("target is not alternating pair plus one")
        survivor = next(
            item for item in activities[3] if item not in full_only
        )
        relations = [
            relation(
                matchings[full_only[0]],
                matchings[full_only[1]],
                colouring,
                labels,
            )
            for colouring in colourings
        ]
        reconstructed = relations[1].copy()
        reconstructed.update(relations[2])
        reconstructed.subtract(relations[0])
        reconstructed = Counter(
            {
                variable: coefficient
                for variable, coefficient in reconstructed.items()
                if coefficient
            }
        )
        if reconstructed != relations[3]:
            raise AssertionError(
                "two-vertex exponent rectangle identity failed"
            )
        sample_checks.append(
            {
                "sample": sample_id,
                "skeleton_perfect_matchings": len(matchings),
                "crossing_chord": list(chord),
                "corner_equation_indices": [
                    sum(
                        colour * (3**vertex)
                        for vertex, colour in enumerate(colouring)
                    )
                    for colouring in colourings[:3]
                ],
                "target_equation_index": sum(
                    colour * (3**vertex)
                    for vertex, colour in enumerate(colourings[3])
                ),
                "target_activity": activities[3],
                "surviving_matching": survivor,
                "relation_identity_signs": [-1, 1, 1],
            }
        )

    payload = {
        "verified": True,
        "status": "c14_rectangle_theorem_audited",
        "analytic_scope": (
            "every equality support with a single full cycle C_n "
            "for n congruent to 2 mod 4; in particular C14"
        ),
        "finite_scope": "all 44,189 eligible first factors at n=14",
        "eligible_c14_singleton_factors": len(eligible_factors),
        "crossing_chord_histogram": {
            str(count): multiplicity
            for count, multiplicity in sorted(cross_histogram.items())
        },
        "minimum_crossing_chords": min(cross_histogram),
        "sample_rectangle_replays": sample_checks,
        "logical_check": (
            "odd bipartition classes force a crossing chord f=xz; "
            "the other two singleton factors admit a proper 2-colouring; "
            "the three full-only rectangle corners force the alternating "
            "pair to cancel at the target, leaving the unique f-matching"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
