"""Independently replay a direct full-only/one-extra cycle core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

N = 14
EQUATIONS = 3**N
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
SparseRelation = tuple[tuple[int, int], ...]
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_ID = {item: position for position, item in enumerate(ALL_EDGES)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> Edge:
    return (first, second) if first < second else (second, first)


def cycle_edges(cycle: Sequence[int]) -> tuple[Edge, ...]:
    return tuple(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def contiguous_cycles(
    lengths: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise AssertionError("cycle lengths do not cover order 14")
    return tuple(output)


def perfect_matchings(allowed: Iterable[Edge]) -> list[Factor]:
    allowed_set = set(allowed)
    adjacency = [0] * N
    for first, second in allowed_set:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output: list[Factor] = []

    def visit(remaining: int, chosen: Factor) -> None:
        if not remaining:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << N) - 1, ())
    return sorted(output)


def indexed_colouring(index: int) -> tuple[int, ...]:
    if index < 0 or index >= EQUATIONS:
        raise AssertionError("equation index is outside the cube")
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


def active_matching_ids(
    equation: int,
    matchings: Sequence[Factor],
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    colouring = indexed_colouring(equation)
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item not in labels
            or colouring[item[0]]
            == colouring[item[1]]
            == labels[item]
            for item in matching
        )
    )


def monomial_variables(
    matching: Factor,
    colouring: Sequence[int],
    labels: dict[Edge, int],
    full_edges: frozenset[Edge],
) -> tuple[int, ...]:
    output = []
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        output.append(
            9 * EDGE_ID[item]
            + 3 * first_colour
            + second_colour
        )
    return tuple(sorted(output))


def relation(
    first: Sequence[int], second: Sequence[int]
) -> SparseRelation:
    counter: Counter[int] = Counter(first)
    counter.subtract(second)
    direct = tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in counter.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient)
        for variable, coefficient in direct
    )
    return min(direct, negative)


def cycle_relation(
    cycle: Sequence[int],
    colouring: Sequence[int],
    labels: dict[Edge, int],
    full_edges: frozenset[Edge],
) -> SparseRelation:
    edges = cycle_edges(cycle)
    return relation(
        monomial_variables(
            edges[0::2], colouring, labels, full_edges
        ),
        monomial_variables(
            edges[1::2], colouring, labels, full_edges
        ),
    )


def parse_relation(
    raw: Sequence[Sequence[int]],
) -> SparseRelation:
    return tuple(tuple(map(int, item)) for item in raw)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    proof = json.loads(args.certificate.read_text(encoding="utf-8"))
    if proof.get("status") != "one_extra_cycle_core":
        raise AssertionError("producer did not report a direct core")

    lengths = tuple(map(int, proof["full_cycle_type"]))
    cycles = contiguous_cycles(lengths)
    if len(cycles) < 2 or any(len(cycle) % 2 for cycle in cycles):
        raise AssertionError("support is not all-even")
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    factors = tuple(
        tuple(
            sorted(
                edge(*map(int, item))
                for item in proof["singleton_matchings"][key]
            )
        )
        for key in ("first", "second", "third")
    )
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    if (
        any(len(factor) != 7 for factor in factors)
        or len(labels) != 21
        or set(labels) & set(full_edges)
    ):
        raise AssertionError("singleton support changed")
    matchings = perfect_matchings(set(full_edges) | set(labels))
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    if (
        len(matchings) != int(proof["skeleton_perfect_matchings"])
        or len(full_only) != 1 << len(cycles)
        or len(full_only) != int(proof["full_only_matching_count"])
    ):
        raise AssertionError("support matching census changed")

    certificate = proof["certificate"]
    if (
        certificate.get("certificate_mode")
        != "full_only_clause_blocked_by_one_extra_units"
    ):
        raise AssertionError("certificate mode changed")
    base_equation = int(
        certificate["full_only_equation_index"]
    )
    base_colouring = indexed_colouring(base_equation)
    if (
        list(base_colouring)
        != list(map(int, certificate["full_only_colouring"]))
        or len(set(base_colouring)) == 1
        or frozenset(
            active_matching_ids(base_equation, matchings, labels)
        )
        != full_only
    ):
        raise AssertionError("full-only forbidden equation changed")

    base_signatures = []
    unit_signatures = set()
    for row in certificate["cycle_rows"]:
        base_cycle_id = int(row["base_cycle_id"])
        unit_cycle_id = int(row["one_extra_cycle_id"])
        if (
            base_cycle_id < 0
            or base_cycle_id >= len(cycles)
            or unit_cycle_id < 0
            or unit_cycle_id >= len(cycles)
        ):
            raise AssertionError("cycle ID changed")
        signature = parse_relation(row["relation_signature"])
        if signature != cycle_relation(
            cycles[base_cycle_id],
            base_colouring,
            labels,
            full_edges,
        ):
            raise AssertionError("base cycle relation changed")
        base_signatures.append(signature)

        unit_equation = int(row["one_extra_equation_index"])
        unit_colouring = indexed_colouring(unit_equation)
        active = active_matching_ids(
            unit_equation, matchings, labels
        )
        extras = tuple(
            matching_id
            for matching_id in active
            if matching_id not in full_only
        )
        if (
            list(unit_colouring)
            != list(map(int, row["one_extra_colouring"]))
            or len(set(unit_colouring)) == 1
            or not full_only.issubset(active)
            or len(active) != len(full_only) + 1
            or extras
            != (int(row["one_extra_matching_id"]),)
            or signature
            != cycle_relation(
                cycles[unit_cycle_id],
                unit_colouring,
                labels,
                full_edges,
            )
        ):
            raise AssertionError("one-extra unit equation changed")
        unit_signatures.add(signature)

    if (
        len(base_signatures) != len(cycles)
        or set(base_signatures) != unit_signatures
        or len(set(base_signatures))
        != int(certificate["distinct_cycle_relations"])
    ):
        raise AssertionError("direct Boolean contradiction changed")

    output = {
        "verified": True,
        "status": "one_extra_cycle_core_verified",
        "scope": (
            "one fixed all-even order-14 support; not the complete "
            "cycle family or the global conjecture"
        ),
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "recorded_exploration": str(proof["exploration"]),
        "recorded_exploration_sha256": proof[
            "exploration_sha256"
        ],
        "full_cycle_type": list(lengths),
        "survivor_index": int(proof["survivor_index"]),
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": len(full_only),
        "full_only_equation_replayed": base_equation,
        "one_extra_equations_replayed": len(
            certificate["cycle_rows"]
        ),
        "distinct_cycle_relations": len(set(base_signatures)),
        "independent_direct_boolean_contradiction": True,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
