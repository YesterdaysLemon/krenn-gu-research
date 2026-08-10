"""Search a two-cycle factor fork using exact rank-one Laurent classes."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import itertools
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np

from analyze_fourteen_vertex_full_direct_motifs import (
    EQUATIONS,
    extension_offsets,
)
from krenn_gu.explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
)
from explore_random_minimal_singleton_sets import contiguous_cycles

N = 14
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def local_code(index: int, cycle: Sequence[int]) -> int:
    return sum(
        ((index // (3**vertex)) % 3) * (3**position)
        for position, vertex in enumerate(cycle)
    )


def local_codes_array(
    indices: np.ndarray, cycle: Sequence[int]
) -> np.ndarray:
    output = np.zeros(len(indices), dtype=np.int64)
    for position, vertex in enumerate(cycle):
        output += (
            (indices // (3**vertex)) % 3
        ) * (3**position)
    return output


def cycle_relation(
    cycle: Sequence[int], colouring: Sequence[int]
) -> Counter[int]:
    output: Counter[int] = Counter()
    for position, first in enumerate(cycle):
        second = cycle[(position + 1) % len(cycle)]
        item = tuple(sorted((first, second)))
        variable = (
            9 * EDGE_INDEX[item]
            + 3 * int(colouring[item[0]])
            + int(colouring[item[1]])
        )
        output[variable] += 1 if position % 2 == 0 else -1
    return output


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


def rank_one_conflict(
    cycle: Sequence[int],
    equation: int,
    matchings: Sequence[Sequence[Edge]],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> dict[str, object] | None:
    colouring = indexed_colouring(equation)
    relation = cycle_relation(cycle, colouring)
    pivot, pivot_value = next(
        (variable, coefficient)
        for variable, coefficient in sorted(relation.items())
        if coefficient
    )
    if abs(pivot_value) != 1:
        raise AssertionError("cycle relation is not primitive at pivot")
    activity = active_ids(matchings, colouring, full_edges, labels)
    classes: dict[tuple[tuple[int, int], ...], int] = defaultdict(int)
    class_members: dict[
        tuple[tuple[int, int], ...], list[tuple[int, int]]
    ] = defaultdict(list)
    for matching_id in activity:
        vector = monomial(
            matchings[matching_id], colouring, full_edges, labels
        )
        coordinate = vector[pivot] * pivot_value
        for variable, coefficient in relation.items():
            vector[variable] -= coordinate * coefficient
            if not vector[variable]:
                del vector[variable]
        residual = tuple(sorted(vector.items()))
        sign = -1 if coordinate % 2 else 1
        classes[residual] += sign
        class_members[residual].append((matching_id, sign))
    nonzero = [
        (residual, coefficient)
        for residual, coefficient in classes.items()
        if coefficient
    ]
    if len(nonzero) != 1:
        return None
    residual, coefficient = nonzero[0]
    return {
        "target_equation_index": equation,
        "target_colouring": list(colouring),
        "target_activity": activity,
        "target_activity_size": len(activity),
        "cycle_relation": [
            [variable, value]
            for variable, value in sorted(relation.items())
            if value
        ],
        "nonzero_class_coefficient": coefficient,
        "nonzero_class_members": [
            [matching_id, sign]
            for matching_id, sign in class_members[residual]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--maximum-activity", type=int, default=8)
    parser.add_argument("--candidates-per-code", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_two_even_cycle_lattice_fork.json"
        ),
    )
    args = parser.parse_args()
    if args.candidates_per_code != 1:
        raise ValueError(
            "the current vectorized search supports one candidate per code"
        )
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    if len(lengths) != 2 or any(length % 2 for length in lengths):
        raise ValueError("full factor must consist of two even cycles")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    singleton_matchings = [
        tuple(tuple(map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = perfect_matchings(N, full_edges | set(labels))
    full_only = {
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    }
    if len(full_only) != 4:
        raise AssertionError("two even cycles need four full matchings")
    started = time.perf_counter()
    counts = np.zeros(EQUATIONS, dtype=np.int16)
    offset_cache: dict[tuple[int, ...], np.ndarray] = {}
    total_extensions = 0
    for matching in matchings:
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        base = sum(
            colour * (3**vertex)
            for vertex, colour in requirements.items()
        )
        free = tuple(
            vertex for vertex in range(N) if vertex not in requirements
        )
        indices = base + extension_offsets(free, offset_cache)
        counts[indices] += 1
        total_extensions += len(indices)
    monochromatic = {
        sum(colour * (3**vertex) for vertex in range(N))
        for colour in range(3)
    }
    base_indices = np.flatnonzero(counts == 4)
    base_indices = np.array(
        [
            int(index)
            for index in base_indices
            if int(index) not in monochromatic
        ],
        dtype=np.int64,
    )
    target_indices = np.flatnonzero(
        (counts >= 5) & (counts <= args.maximum_activity)
    )
    target_indices = np.array(
        [
            int(index)
            for index in target_indices
            if int(index) not in monochromatic
        ],
        dtype=np.int64,
    )
    killers_by_cycle: list[dict[int, dict[str, object]]] = []
    tested_by_cycle = []
    for cycle in cycles:
        candidates: dict[int, list[int]] = defaultdict(list)
        for activity_size in range(5, args.maximum_activity + 1):
            level = target_indices[
                counts[target_indices] == activity_size
            ]
            if not len(level):
                continue
            codes = local_codes_array(level, cycle)
            unique_codes, first_positions = np.unique(
                codes, return_index=True
            )
            for code, position in zip(
                unique_codes, first_positions, strict=True
            ):
                code = int(code)
                if candidates[code]:
                    continue
                candidates[code].append(int(level[int(position)]))
        killers: dict[int, dict[str, object]] = {}
        tested = 0
        for code, equations in candidates.items():
            for equation in equations:
                tested += 1
                conflict = rank_one_conflict(
                    cycle,
                    equation,
                    matchings,
                    full_edges,
                    labels,
                )
                if conflict is not None:
                    killers[code] = conflict
                    break
        killers_by_cycle.append(killers)
        tested_by_cycle.append(tested)
    certificate = None
    for base in map(int, base_indices):
        alternatives = []
        for cycle, killers in zip(
            cycles, killers_by_cycle, strict=True
        ):
            conflict = killers.get(local_code(base, cycle))
            if conflict is None:
                break
            alternatives.append(
                {"cycle": list(cycle), **conflict}
            )
        if len(alternatives) == 2:
            certificate = {
                "base_equation_index": base,
                "base_colouring": list(indexed_colouring(base)),
                "base_activity": sorted(full_only),
                "alternatives": alternatives,
            }
            break
    unique, frequencies = np.unique(counts, return_counts=True)
    payload = {
        "status": (
            "two_even_cycle_lattice_fork"
            if certificate is not None
            else "lattice_fork_absent_in_search_window"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "skeleton_perfect_matchings": len(matchings),
        "matching_extensions_accumulated": total_extensions,
        "activity_histogram": {
            str(int(value)): int(frequency)
            for value, frequency in zip(unique, frequencies, strict=True)
        },
        "maximum_activity_searched": args.maximum_activity,
        "candidates_per_cycle_code": args.candidates_per_code,
        "candidate_targets": len(target_indices),
        "targets_tested_by_cycle": tested_by_cycle,
        "killed_cycle_codes": [
            len(killers) for killers in killers_by_cycle
        ],
        "certificate": certificate,
        "elapsed_seconds": time.perf_counter() - started,
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
                if key not in {"activity_histogram", "certificate"}
            },
            indent=2,
        )
    )
    if certificate is not None:
        print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
