"""Solve fixed odd-group-size cases in the Tutte-Berge obstruction."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from candidate_matching_obstruction_sat import (
    matching_obstruction_cnf,
    odd_group_size_patterns,
)


def solve_pattern(
    item: tuple[int, int, tuple[int, ...], str],
) -> dict[str, object]:
    from pysat.solvers import Solver

    index, separator_size, group_sizes, solver_name = item
    cnf, metadata = matching_obstruction_cnf(
        separator_size,
        group_sizes,
    )
    started = time.perf_counter()
    with Solver(
        name=solver_name,
        bootstrap_with=cnf.clauses,
    ) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        try:
            statistics = solver.accum_stats()
        except NotImplementedError:
            statistics = None
    return {
        "case": index,
        "separator_size": separator_size,
        "group_sizes": list(group_sizes),
        "status": "SAT" if sat else "UNSAT",
        "solver": solver_name,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "statistics": statistics,
        "model": model,
        "encoding": metadata.get("simplification"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--separator-size", type=int, required=True)
    parser.add_argument(
        "--solver",
        choices=(
            "cadical195",
            "glucose42",
            "maplechrono",
            "mergesat3",
            "minisat22",
        ),
        default="cadical195",
    )
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    patterns = odd_group_size_patterns(args.separator_size)
    items = [
        (
            index,
            args.separator_size,
            group_sizes,
            args.solver,
        )
        for index, group_sizes in enumerate(patterns)
    ]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(solve_pattern, items))
    else:
        rows = [solve_pattern(item) for item in items]
    counts = Counter(str(row["status"]) for row in rows)
    result = {
        "separator_size": args.separator_size,
        "patterns": len(rows),
        "status_counts": dict(counts),
        "certified": counts == Counter({"UNSAT": len(rows)}),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: patterns={len(rows)} "
        f"counts={dict(counts)}"
    )
    if not result["certified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
