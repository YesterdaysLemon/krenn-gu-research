"""Solve a materialized DIMACS instance with a selected PySAT backend."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument(
        "--solver",
        choices=(
            "cadical195",
            "glucose42",
            "lingeling",
            "maplechrono",
            "mergesat3",
            "minisat22",
        ),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    from pysat.formula import CNF
    from pysat.solvers import Solver

    formula = CNF(from_file=str(args.cnf))
    started = time.perf_counter()
    with Solver(
        name=args.solver,
        bootstrap_with=formula.clauses,
    ) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        try:
            statistics = solver.accum_stats()
        except NotImplementedError:
            statistics = None
    result = {
        "cnf": str(args.cnf),
        "solver": args.solver,
        "status": "SAT" if sat else "UNSAT",
        "variables": formula.nv,
        "clauses": len(formula.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "statistics": statistics,
        "model": model,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: status={result['status']} "
        f"elapsed={result['elapsed_seconds']:.3f}s"
    )


if __name__ == "__main__":
    main()
