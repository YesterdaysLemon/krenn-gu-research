"""Search equality supports through their feasible singleton-set poset.

For a skeleton perfect matching M, let T be its singleton-edge subset.
The exact-activation lemma gives a colouring whose active graph is F union T.
If T is inclusion-minimal among feasible singleton sets and meets every
cycle of F, M is the unique active perfect matching.  This exploratory
script tests that criterion without enumerating all 3^n colourings.
"""

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
import json
import random
import time
from pathlib import Path
from typing import Sequence

from krenn_gu.explore_random_even_cycle_forks import (
    Edge,
    cycle_edges,
    perfect_matchings,
    random_singletons,
)


def contiguous_cycles(lengths: Sequence[int]) -> list[tuple[int, ...]]:
    cycles: list[tuple[int, ...]] = []
    start = 0
    for length in lengths:
        cycles.append(tuple(range(start, start + length)))
        start += length
    return cycles


def analyze_support(
    n: int,
    cycles: Sequence[Sequence[int]],
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
) -> dict[str, object]:
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    if len(labels) != 3 * n // 2:
        raise AssertionError("singleton matchings overlap")
    skeleton = set(full_edges) | set(labels)
    matchings = perfect_matchings(n, skeleton)
    singleton_ids = {
        item: index for index, item in enumerate(sorted(labels))
    }
    feasible: set[frozenset[int]] = {
        frozenset(
            singleton_ids[item]
            for item in matching
            if item in labels
        )
        for matching in matchings
    }
    minimal: list[frozenset[int]] = []
    for candidate in sorted(feasible, key=lambda item: (len(item), sorted(item))):
        if not any(previous < candidate for previous in minimal):
            minimal.append(candidate)
    cycle_vertex_sets = [set(cycle) for cycle in cycles]
    id_edges = {index: item for item, index in singleton_ids.items()}

    def touched(target: frozenset[int]) -> list[bool]:
        vertices = {
            vertex
            for item_id in target
            for vertex in id_edges[item_id]
        }
        return [
            bool(vertices & cycle_vertices)
            for cycle_vertices in cycle_vertex_sets
        ]

    certificates = [
        target for target in minimal if all(touched(target))
    ]
    minimum_size = min(map(len, feasible))
    return {
        "skeleton_perfect_matchings": len(matchings),
        "distinct_feasible_singleton_sets": len(feasible),
        "inclusion_minimal_singleton_sets": len(minimal),
        "minimum_singleton_edges": minimum_size,
        "minimum_sets_touching_all_cycles": sum(
            len(target) == minimum_size and all(touched(target))
            for target in minimal
        ),
        "one_term_minimal_sets": len(certificates),
        "certificate_singleton_set": (
            sorted(certificates[0]) if certificates else None
        ),
        "minimal_set_sizes": sorted(
            {len(target) for target in minimal}
        ),
        "minimal_set_touch_patterns": sorted(
            {
                tuple(touched(target))
                for target in minimal
            }
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--partitions",
        nargs="+",
        default=[
            "3+3+6",
            "3+4+5",
            "3+3+8",
            "3+4+7",
            "3+5+6",
            "4+5+5",
            "3+3+4+4",
        ],
    )
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/random_minimal_singleton_sets.json"),
    )
    args = parser.parse_args()
    rng = random.Random(args.seed)
    rows: list[dict[str, object]] = []
    started = time.perf_counter()
    for text in args.partitions:
        lengths = tuple(map(int, text.split("+")))
        n = sum(lengths)
        if n % 2 or all(length % 2 == 0 for length in lengths):
            raise ValueError(f"not an even order with odd components: {text}")
        cycles = contiguous_cycles(lengths)
        full_edges = frozenset(
            item for cycle in cycles for item in cycle_edges(cycle)
        )
        for sample in range(args.samples):
            singletons = random_singletons(n, full_edges, rng)
            result = analyze_support(n, cycles, full_edges, singletons)
            row = {
                "full_cycle_type": list(lengths),
                "sample": sample,
                "singleton_matchings": [
                    [list(item) for item in matching]
                    for matching in singletons
                ],
                **result,
            }
            rows.append(row)
            print(
                f"type={text} sample={sample + 1}/{args.samples} "
                f"minimal={result['inclusion_minimal_singleton_sets']} "
                f"one_term={result['one_term_minimal_sets']}",
                flush=True,
            )
            if result["one_term_minimal_sets"] == 0:
                print("COUNTEREXAMPLE CANDIDATE", flush=True)
                break
    failures = [
        row for row in rows if row["one_term_minimal_sets"] == 0
    ]
    payload = {
        "status": "exploratory",
        "necessary_conditions_only": True,
        "samples": len(rows),
        "failures": len(failures),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
