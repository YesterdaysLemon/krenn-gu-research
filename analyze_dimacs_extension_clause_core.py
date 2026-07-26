"""Extract a deletion-irredundant assumption core from a DIMACS extension.

This is an exploratory theorem-discovery aid.  It checks that ``extended``
starts with the exact clauses of ``base``, guards every appended clause by
its own fresh selector, and minimizes the appended selectors needed for
UNSAT under one caller-supplied literal.
"""

from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--extended-cnf", type=Path, required=True)
    parser.add_argument("--assumption", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    base = CNF(from_file=str(args.base_cnf))
    extended = CNF(from_file=str(args.extended_cnf))
    if extended.clauses[: len(base.clauses)] != base.clauses:
        raise AssertionError("extended CNF does not have the exact base prefix")
    added = extended.clauses[len(base.clauses) :]
    if not added:
        raise AssertionError("CNF extension has no appended clauses")

    with Solver(name="cadical195", bootstrap_with=base.clauses) as solver:
        if not solver.solve(assumptions=[args.assumption]):
            raise AssertionError("base CNF is already UNSAT under assumption")

    first_guard = max(base.nv, extended.nv) + 1
    guards = [first_guard + index for index in range(len(added))]
    guarded = [
        [*clause, -guard] for clause, guard in zip(added, guards, strict=True)
    ]
    with Solver(
        name="cadical195",
        bootstrap_with=[*base.clauses, *guarded],
    ) as solver:
        assumptions = [args.assumption, *guards]
        if solver.solve(assumptions=assumptions):
            raise AssertionError("guarded extension is SAT under all guards")
        raw = set(solver.get_core() or [])

    core = [guard for guard in guards if guard in raw]
    if not core:
        raise AssertionError("solver returned no appended-clause core")

    with Solver(
        name="cadical195",
        bootstrap_with=[*base.clauses, *guarded],
    ) as solver:
        index = 0
        while index < len(core):
            trial = core[:index] + core[index + 1 :]
            if solver.solve(assumptions=[args.assumption, *trial]):
                index += 1
            else:
                core = trial

        if solver.solve(assumptions=[args.assumption, *core]):
            raise AssertionError("minimized core unexpectedly became SAT")
        for index in range(len(core)):
            trial = core[:index] + core[index + 1 :]
            if not solver.solve(assumptions=[args.assumption, *trial]):
                raise AssertionError("core is not deletion-irredundant")

    guard_to_index = {guard: index for index, guard in enumerate(guards)}
    indices = [guard_to_index[guard] for guard in core]
    clauses = [added[index] for index in indices]
    payload = {
        "status": "UNSAT_deletion_irredundant_extension_clause_core",
        "base_cnf": str(args.base_cnf),
        "extended_cnf": str(args.extended_cnf),
        "assumption": args.assumption,
        "added_clauses": len(added),
        "raw_core_clauses": len([guard for guard in guards if guard in raw]),
        "irredundant_core_clauses": len(core),
        "clause_indices": indices,
        "clause_widths": dict(sorted(Counter(map(len, clauses)).items())),
        "clauses": clauses,
        "solver": "cadical195",
        "deletion_irredundant": True,
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
