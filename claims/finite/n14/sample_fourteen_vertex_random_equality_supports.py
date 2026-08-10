"""Generate reproducible random equality supports, one or more per factor orbit."""

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
import random
from pathlib import Path

from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges, perfect_matchings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("census", type=Path)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--samples-per-orbit", type=int, default=1)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_random_equality_supports.json"
        ),
    )
    args = parser.parse_args()
    if args.samples_per_orbit < 1:
        raise ValueError("--samples-per-orbit must be positive")
    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = {
        (first, second)
        for first in range(N)
        for second in range(first + 1, N)
        if (first, second) not in full_edges
    }
    factors = perfect_matchings(N, eligible_edges)
    rng = random.Random(args.seed)
    survivors = []
    for orbit_id, row in enumerate(census["factor_orbits"]):
        first = tuple(
            tuple(map(int, item)) for item in row["representative"]
        )
        compatible_seconds = [
            factor
            for factor in factors
            if not set(first).intersection(factor)
        ]
        produced = 0
        attempts = 0
        seen: set[
            tuple[
                tuple[tuple[int, int], ...],
                tuple[tuple[int, int], ...],
            ]
        ] = set()
        while produced < args.samples_per_orbit:
            attempts += 1
            if attempts > 10_000:
                raise AssertionError(
                    f"could not sample orbit {orbit_id}"
                )
            second = rng.choice(compatible_seconds)
            selected = set(first) | set(second)
            compatible_thirds = [
                factor
                for factor in factors
                if not selected.intersection(factor)
            ]
            if not compatible_thirds:
                continue
            third = rng.choice(compatible_thirds)
            key = (second, third)
            if key in seen:
                continue
            seen.add(key)
            survivors.append(
                {
                    "orbit_id": orbit_id,
                    "sample_in_orbit": produced,
                    "first": [list(item) for item in first],
                    "second": [list(item) for item in second],
                    "third": [list(item) for item in third],
                }
            )
            produced += 1
    payload = {
        "status": "reproducible_random_support_samples",
        "partition": list(lengths),
        "source_census": str(args.census),
        "seed": args.seed,
        "samples_per_orbit": args.samples_per_orbit,
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
                "seed": args.seed,
                "samples": len(survivors),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
