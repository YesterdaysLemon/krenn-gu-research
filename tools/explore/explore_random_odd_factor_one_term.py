"""Sample odd-component equality supports for one-term obstructions.

This is exploratory, not a theorem certificate.  An equality support is the
union of a full-block 2-factor and three colour-labelled singleton perfect
matchings.  For every sampled support whose full factor has an odd
component, enumerate all vertex colourings and ask whether a forbidden
amplitude has exactly one active perfect matching.
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

import numpy as np

from krenn_gu.explore_random_even_cycle_forks import (
    Edge,
    colouring_table,
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
    full_edges: frozenset[Edge],
    singletons: Sequence[Sequence[Edge]],
    colourings: np.ndarray,
) -> dict[str, object]:
    labels = {
        item: colour
        for colour, matching in enumerate(singletons)
        for item in matching
    }
    if len(labels) != 3 * n // 2:
        raise AssertionError("singleton matchings overlap")
    skeleton = set(full_edges) | set(labels)
    if any(
        sum(vertex in item for item in skeleton) != 5
        for vertex in range(n)
    ):
        raise AssertionError("sampled skeleton is not 5-regular")
    matchings = perfect_matchings(n, skeleton)
    active_count = np.zeros(len(colourings), dtype=np.int16)
    singleton_counts: list[int] = []
    requirements_by_matching: list[dict[int, int]] = []
    for matching in matchings:
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        requirements_by_matching.append(requirements)
        singleton_counts.append(len(requirements) // 2)
        mask = np.ones(len(colourings), dtype=bool)
        for vertex, colour in requirements.items():
            mask &= colourings[:, vertex] == colour
        active_count += mask
    monochromatic = np.all(
        colourings == colourings[:, :1], axis=1
    )
    one_term = np.flatnonzero((active_count == 1) & ~monochromatic)
    if not len(one_term):
        return {
            "skeleton_perfect_matchings": len(matchings),
            "one_term_colourings": 0,
            "certificate": None,
        }
    equation_index = int(one_term[0])
    colouring = colourings[equation_index]
    active_matching = next(
        index
        for index, requirements in enumerate(requirements_by_matching)
        if all(
            int(colouring[vertex]) == colour
            for vertex, colour in requirements.items()
        )
    )
    minimum_singletons = min(
        singleton_counts[
            next(
                index
                for index, requirements in enumerate(
                    requirements_by_matching
                )
                if all(
                    int(colourings[equation, vertex]) == colour
                    for vertex, colour in requirements.items()
                )
            )
        ]
        for equation in one_term
    )
    return {
        "skeleton_perfect_matchings": len(matchings),
        "one_term_colourings": int(len(one_term)),
        "minimum_singleton_edges_in_unique_matching": int(
            minimum_singletons
        ),
        "certificate": {
            "equation_index": equation_index,
            "colouring": list(map(int, colouring)),
            "active_matching_index": active_matching,
            "active_matching": [
                list(item) for item in matchings[active_matching]
            ],
            "singleton_edges_in_active_matching": singleton_counts[
                active_matching
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--partitions",
        nargs="+",
        default=["3+9", "5+7", "3+3+6", "3+4+5", "3+3+3+3"],
    )
    parser.add_argument("--samples", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260724)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/random_odd_factor_one_term.json"),
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
        colourings = colouring_table(n)
        for sample in range(args.samples):
            singletons = random_singletons(n, full_edges, rng)
            result = analyze_support(
                n, full_edges, singletons, colourings
            )
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
                f"one_term={result['one_term_colourings']}",
                flush=True,
            )
    failures = sum(
        row["certificate"] is None for row in rows
    )
    payload = {
        "status": "exploratory",
        "necessary_conditions_only": True,
        "samples": len(rows),
        "failures": failures,
        "minimum_one_term_colourings": min(
            int(row["one_term_colourings"]) for row in rows
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in payload.items() if key != "rows"}, indent=2))


if __name__ == "__main__":
    main()
