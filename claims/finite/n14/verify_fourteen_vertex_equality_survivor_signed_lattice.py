"""Independent replay of a generic order-14 signed-lattice certificate."""

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
import hashlib
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


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((first, second)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cycle_edges(cycle: Sequence[int]) -> set[Edge]:
    return {
        edge(cycle[position], cycle[(position + 1) % len(cycle)])
        for position in range(len(cycle))
    }


def contiguous_cycles(lengths: Sequence[int]) -> list[tuple[int, ...]]:
    cycles = []
    start = 0
    for length in lengths:
        cycles.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise AssertionError("cycle partition does not cover 14 vertices")
    return cycles


def perfect_matchings(allowed: set[Edge]) -> list[tuple[Edge, ...]]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in allowed:
        adjacency[first].add(second)
        adjacency[second].add(first)

    @lru_cache(maxsize=None)
    def recurse(remaining: int) -> tuple[tuple[Edge, ...], ...]:
        if not remaining:
            return ((),)
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = remaining ^ first_bit
        output: list[tuple[Edge, ...]] = []
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            item = (first, second)
            if item not in allowed:
                continue
            for suffix in recurse(remaining ^ first_bit ^ second_bit):
                output.append((item,) + suffix)
        return tuple(output)

    return sorted(recurse((1 << N) - 1))


def decode_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def active_ids(
    matchings: Sequence[Sequence[Edge]],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> list[int]:
    return [
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item in full_edges
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        )
    ]


def monomial(
    matching: Sequence[Edge],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> Counter[int]:
    output: Counter[int] = Counter()
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        output[
            9 * EDGE_INDEX[item] + 3 * first_colour + second_colour
        ] += 1
    return output


def canonical_relation(
    first: Sequence[Edge],
    second: Sequence[Edge],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> tuple[tuple[int, int], ...]:
    vector = monomial(first, colouring, full_edges, labels)
    vector.subtract(monomial(second, colouring, full_edges, labels))
    direct = tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in vector.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient)
        for variable, coefficient in direct
    )
    return min(direct, negative)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("analysis", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_survivor_"
            "signed_lattice_verified.json"
        ),
    )
    args = parser.parse_args()
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    analysis = json.loads(args.analysis.read_text(encoding="utf-8"))
    if analysis.get("status") != "contradiction":
        raise AssertionError("analysis does not claim a contradiction")
    if Path(analysis["exploration"]) != args.exploration:
        raise AssertionError("analysis is bound to another exploration")
    survivor_index = int(analysis["survivor_index"])
    survivor = exploration["survivors"][survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    if list(lengths) != list(map(int, analysis["full_cycle_type"])):
        raise AssertionError("full cycle type mismatch")
    cycles = contiguous_cycles(lengths)
    full_edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    singleton_matchings = [
        tuple(edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    singleton_edges: set[Edge] = set()
    for matching in singleton_matchings:
        if len(matching) != N // 2:
            raise AssertionError("singleton factor has wrong cardinality")
        if {
            vertex for item in matching for vertex in item
        } != set(range(N)):
            raise AssertionError("singleton factor is not perfect")
        if singleton_edges.intersection(matching):
            raise AssertionError("singleton factors overlap")
        singleton_edges.update(matching)
    if singleton_edges & full_edges:
        raise AssertionError("full and singleton blocks overlap")
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = perfect_matchings(full_edges | singleton_edges)
    if len(matchings) != int(analysis["skeleton_perfect_matchings"]):
        raise AssertionError("skeleton perfect-matching count mismatch")

    basis_vectors: list[Counter[int]] = []
    for record in analysis["basis_relations"]:
        equation = int(record["origin_equation_index"])
        colouring = decode_colouring(equation)
        if len(set(colouring)) == 1:
            raise AssertionError("basis equation is monochromatic")
        activity = active_ids(
            matchings, colouring, full_edges, labels
        )
        if len(activity) != 2:
            raise AssertionError("basis equation is not binomial")
        signature = canonical_relation(
            matchings[activity[0]],
            matchings[activity[1]],
            colouring,
            full_edges,
            labels,
        )
        reported = tuple(
            (int(variable), int(coefficient))
            for variable, coefficient in record["signature"]
        )
        if signature != reported:
            raise AssertionError("basis relation signature mismatch")
        basis_vectors.append(Counter(dict(signature)))
    if len(basis_vectors) != int(analysis["signed_lattice_rank"]):
        raise AssertionError("signed-lattice rank record mismatch")

    certificate = analysis["certificate"]
    if certificate["certificate_mode"] != (
        "signed_lattice_trinomial_survivor"
    ):
        raise AssertionError("unsupported certificate mode")
    target_equation = int(certificate["target_equation_index"])
    target_colouring = decode_colouring(target_equation)
    if list(target_colouring) != certificate["target_colouring"]:
        raise AssertionError("target colouring/index mismatch")
    if len(set(target_colouring)) == 1:
        raise AssertionError("target equation is monochromatic")
    target_activity = active_ids(
        matchings, target_colouring, full_edges, labels
    )
    if target_activity != list(map(int, certificate["target_activity"])):
        raise AssertionError("target activity mismatch")
    if len(target_activity) != 3:
        raise AssertionError("target equation is not trinomial")
    paired = list(map(int, certificate["target_paired_matchings"]))
    survivor_id = int(certificate["target_surviving_matching"])
    if set(target_activity) != {*paired, survivor_id}:
        raise AssertionError("target pair/survivor partition mismatch")
    target_signature = canonical_relation(
        matchings[paired[0]],
        matchings[paired[1]],
        target_colouring,
        full_edges,
        labels,
    )
    reported_target = tuple(
        (int(variable), int(coefficient))
        for variable, coefficient
        in certificate["target_relation_signature"]
    )
    if target_signature != reported_target:
        raise AssertionError("target relation signature mismatch")

    coordinate = [0] * len(basis_vectors)
    for position, coefficient in certificate["basis_coordinates"]:
        position = int(position)
        if not 0 <= position < len(coordinate):
            raise AssertionError("basis coordinate index out of range")
        coordinate[position] = int(coefficient)
    reconstructed: Counter[int] = Counter()
    for coefficient, vector in zip(
        coordinate, basis_vectors, strict=True
    ):
        for variable, value in vector.items():
            reconstructed[variable] += coefficient * value
    reconstructed = Counter(
        {
            variable: value
            for variable, value in reconstructed.items()
            if value
        }
    )
    if reconstructed != Counter(dict(target_signature)):
        raise AssertionError("basis coordinates do not reconstruct target")
    if sum(coordinate) % 2 == 0:
        raise AssertionError("basis combination does not force sign -1")
    if not matchings[survivor_id]:
        raise AssertionError("surviving perfect matching is empty")

    cycle_type = "+".join(f"C{length}" for length in lengths)
    payload = {
        "verified": True,
        "scope": (
            f"one n=14,d=3 {cycle_type} equality support is impossible "
            "by a three-relation signed-lattice contradiction"
        ),
        "claim_scope": (
            f"this survivor only; not yet the full {cycle_type} family "
            "or the global conjecture"
        ),
        "exploration": str(args.exploration),
        "exploration_sha256": sha256(args.exploration),
        "analysis": str(args.analysis),
        "analysis_sha256": sha256(args.analysis),
        "survivor_index": survivor_index,
        "full_cycle_type": list(lengths),
        "skeleton_perfect_matchings": len(matchings),
        "verified_basis_relations": len(basis_vectors),
        "used_basis_relations": sum(
            coefficient != 0 for coefficient in coordinate
        ),
        "coordinate_parity": sum(coordinate) % 2,
        "target_equation_index": target_equation,
        "target_activity": target_activity,
        "target_paired_matchings": paired,
        "target_surviving_matching": survivor_id,
        "logical_check": (
            "the odd signed product of independently replayed "
            "binomial relations forces the target pair to cancel; "
            "the third active supported monomial is nonzero"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
