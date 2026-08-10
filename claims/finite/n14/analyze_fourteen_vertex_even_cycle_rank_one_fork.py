"""Search an all-even factor fork by exact rank-one Laurent classes."""

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
import json
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

from analyze_fourteen_vertex_full_direct_motifs import (
    EQUATIONS,
    extension_offsets,
)
from analyze_fourteen_vertex_two_even_cycle_lattice_fork import (
    indexed_colouring,
    local_code,
    local_codes_array,
    rank_one_conflict,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges, perfect_matchings
from explore_random_minimal_singleton_sets import contiguous_cycles

N = 14


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--survivor-key", default="survivors")
    parser.add_argument("--maximum-activity", type=int, default=64)
    parser.add_argument(
        "--candidates-per-level-code",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_even_cycle_rank_one_fork.json"
        ),
    )
    args = parser.parse_args()
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration[args.survivor_key][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    if any(length % 2 for length in lengths):
        raise ValueError("every full-factor cycle must be even")
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
    baseline = 1 << len(cycles)
    if len(full_only) != baseline:
        raise AssertionError("full-only matching count changed")

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
    base_indices = np.array(
        [
            int(index)
            for index in np.flatnonzero(counts == baseline)
            if int(index) not in monochromatic
        ],
        dtype=np.int64,
    )
    target_indices = np.array(
        [
            int(index)
            for index in np.flatnonzero(
                (counts > baseline)
                & (counts <= args.maximum_activity)
            )
            if int(index) not in monochromatic
        ],
        dtype=np.int64,
    )

    killers_by_cycle: list[dict[int, dict[str, object]]] = []
    tested_by_cycle = []
    candidate_counts_by_cycle = []
    for cycle in cycles:
        candidates: dict[int, list[int]] = defaultdict(list)
        for activity_size in range(
            baseline + 1, args.maximum_activity + 1
        ):
            level = target_indices[
                counts[target_indices] == activity_size
            ]
            if not len(level):
                continue
            codes = local_codes_array(level, cycle)
            for code in np.unique(codes):
                positions = np.flatnonzero(codes == code)
                for position in positions[
                    : args.candidates_per_level_code
                ]:
                    candidates[int(code)].append(
                        int(level[int(position)])
                    )
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
        candidate_counts_by_cycle.append(
            sum(map(len, candidates.values()))
        )

    certificate = None
    for base_value in base_indices:
        base = int(base_value)
        alternatives = []
        for cycle, killers in zip(
            cycles, killers_by_cycle, strict=True
        ):
            conflict = killers.get(local_code(base, cycle))
            if conflict is None:
                break
            alternatives.append({"cycle": list(cycle), **conflict})
        if len(alternatives) == len(cycles):
            certificate = {
                "certificate_mode": (
                    "even_cycle_rank_one_laurent_factor_fork"
                ),
                "base_equation_index": base,
                "base_colouring": list(indexed_colouring(base)),
                "base_activity": sorted(full_only),
                "alternatives": alternatives,
            }
            break

    unique, frequencies = np.unique(counts, return_counts=True)
    payload = {
        "status": (
            "even_cycle_rank_one_laurent_fork"
            if certificate is not None
            else "rank_one_laurent_fork_absent_in_search_window"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "matching_extensions_accumulated": total_extensions,
        "activity_histogram": {
            str(int(value)): int(frequency)
            for value, frequency in zip(unique, frequencies, strict=True)
        },
        "maximum_activity_searched": args.maximum_activity,
        "candidates_per_level_code": (
            args.candidates_per_level_code
        ),
        "candidate_targets": len(target_indices),
        "candidate_equations_by_cycle": candidate_counts_by_cycle,
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
