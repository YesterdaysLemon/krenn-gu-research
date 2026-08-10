"""Find a direct amplitude fork in every n=10 C4+C6 equality orbit."""

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
import time
from pathlib import Path

from krenn_gu.explore_random_even_cycle_forks import (
    analyze_support,
    colouring_table,
    cycle_edges,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbits",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_support_orbits.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_support_forks.json"
        ),
    )
    args = parser.parse_args()
    source = json.loads(args.orbits.read_text(encoding="utf-8"))
    if source.get("verified") is not True:
        raise AssertionError("orbit catalogue is not verified")
    cycles = [
        list(map(int, cycle)) for cycle in source["full_cycles"]
    ]
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    colourings = colouring_table(10)
    rows: list[dict[str, object]] = []
    started = time.perf_counter()
    for index, orbit in enumerate(source["rows"]):
        singletons = tuple(
            tuple(tuple(map(int, item)) for item in matching)
            for matching in orbit["singleton_matchings"]
        )
        result = analyze_support(
            10, cycles, full_edges, singletons, colourings
        )
        if not result["fork_found"]:
            raise AssertionError(
                f"orbit {index} has no direct even-cycle fork"
            )
        rows.append(
            {
                "orbit_index": index,
                "orbit_size_uncoloured": int(
                    orbit["orbit_size_uncoloured"]
                ),
                "singleton_matchings": orbit["singleton_matchings"],
                **result,
            }
        )
        if (index + 1) % 25 == 0 or index + 1 == len(source["rows"]):
            print(
                f"orbit={index + 1}/{len(source['rows'])} "
                f"forks={result['fork_colouring_count']}",
                flush=True,
            )
    payload = {
        "status": "all_forked",
        "scope": (
            "all n=10,d=3 equality supports whose full-block "
            "2-factor has type C4+C6, modulo vertex and global-colour "
            "symmetry"
        ),
        "necessary_conditions_only": False,
        "orbit_catalogue": str(args.orbits),
        "factor_automorphisms": int(
            source["factor_automorphisms"]
        ),
        "raw_uncoloured_factorizations": int(
            source["raw_uncoloured_factorizations"]
        ),
        "support_orbits": len(rows),
        "forked_orbits": sum(bool(row["fork_found"]) for row in rows),
        "minimum_fork_colourings": min(
            int(row["fork_colouring_count"]) for row in rows
        ),
        "maximum_fork_colourings": max(
            int(row["fork_colouring_count"]) for row in rows
        ),
        "rows": rows,
        "solve_seconds": time.perf_counter() - started,
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
