"""Solve every fixed separator orbit for the s=5 Tutte obstruction."""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from candidate_matching_obstruction_sat import (
    fixed_separator_cnf,
    separator_orbit_representatives,
)


def solve_orbit(
    item: tuple[int, tuple[int, ...], str, str | None],
) -> dict[str, object]:
    from pysat.solvers import Solver

    index, row_masks, solver_name, cnf_directory_text = item
    cnf, metadata = fixed_separator_cnf(row_masks)
    if cnf_directory_text is not None:
        cnf_directory = Path(cnf_directory_text)
        cnf_directory.mkdir(parents=True, exist_ok=True)
        cnf.write_dimacs(cnf_directory / f"separator_orbit_{index}.cnf")
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
        "orbit": index,
        **metadata,
        "status": "SAT" if sat else "UNSAT",
        "solver": solver_name,
        "variables": cnf.variable_count,
        "clauses": len(cnf.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "statistics": statistics,
        "model": model,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--cnf-directory", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    representatives = separator_orbit_representatives(5)
    items = [
        (
            index,
            row_masks,
            args.solver,
            str(args.cnf_directory) if args.cnf_directory else None,
        )
        for index, row_masks in enumerate(representatives)
    ]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(solve_orbit, items))
    else:
        rows = [solve_orbit(item) for item in items]
    counts = Counter(str(row["status"]) for row in rows)
    result = {
        "separator_size": 5,
        "orbits": len(rows),
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
        f"wrote {args.output}: orbits={len(rows)} "
        f"counts={dict(counts)}"
    )
    if not result["certified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
