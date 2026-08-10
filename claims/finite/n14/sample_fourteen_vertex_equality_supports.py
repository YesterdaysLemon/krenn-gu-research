"""Construct deterministic support samples from a factor-orbit census."""

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
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges, perfect_matchings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_support_samples.json"
        ),
    )
    args = parser.parse_args()
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = {
        tuple(item)
        for first in range(N)
        for second in range(first + 1, N)
        for item in [(first, second)]
        if item not in full_edges
    }
    factors = perfect_matchings(N, eligible_edges)
    survivors = []
    for row in census["factor_orbits"]:
        first = tuple(tuple(map(int, item)) for item in row["representative"])
        first_set = set(first)
        seconds = [
            factor for factor in factors if not first_set.intersection(factor)
        ]
        found = None
        for second in seconds:
            selected = first_set | set(second)
            third = next(
                (
                    factor
                    for factor in factors
                    if not selected.intersection(factor)
                ),
                None,
            )
            if third is not None:
                found = (second, third)
                break
        if found is None:
            continue
        second, third = found
        survivors.append(
            {
                "first": [list(item) for item in first],
                "second": [list(item) for item in second],
                "third": [list(item) for item in third],
            }
        )
        if len(survivors) == args.count:
            break
    if len(survivors) != args.count:
        raise AssertionError("could not construct requested support samples")
    payload = {
        "status": "deterministic_support_samples",
        "partition": list(lengths),
        "source_census": str(args.census),
        "survivors": survivors,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "partition": list(lengths),
                "samples": len(survivors),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
