"""Independently audit every first-factor selector in a rule SAT CNF.

The C4+C4+C6 rule compiler uses one selector for each of the 93 orbits of
the first singleton perfect matching.  Solving the combined CNF once can
hide which parts of the symmetry-broken search remain open.  This audit
loads an already materialized DIMACS file and performs one assumption
solve per selector, recording a hash of the exact input and the complete
SAT/UNSAT orbit partition.

This checks only the stated CNF.  It does not certify that the clauses
faithfully encode the graph-theoretic certificate semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def consecutive_ranges(values: list[int]) -> list[list[int]]:
    if not values:
        return []
    output: list[list[int]] = []
    start = previous = values[0]
    for value in values[1:]:
        if value == previous + 1:
            previous = value
            continue
        output.append([start, previous])
        start = previous = value
    output.append([start, previous])
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument(
        "--first-selector",
        type=int,
        help="DIMACS selector variable for the first audited orbit",
    )
    parser.add_argument(
        "--selector-zero",
        type=int,
        help=(
            "DIMACS selector variable for orbit zero; the audited start "
            "is derived by adding --orbit-offset"
        ),
    )
    parser.add_argument(
        "--orbit-offset",
        type=int,
        default=0,
        help="label assigned to --first-selector in the output",
    )
    parser.add_argument("--orbits", type=int, default=93)
    parser.add_argument(
        "--orbit",
        type=int,
        action="append",
        default=[],
        help=(
            "audit this exact orbit label; may be repeated and uses "
            "--selector-zero (default 232) instead of a contiguous range"
        ),
    )
    parser.add_argument(
        "--solver",
        default="cadical195",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if (
        args.first_selector is not None
        and args.selector_zero is not None
    ):
        raise ValueError(
            "use only one of --first-selector and --selector-zero"
        )
    if args.orbit and args.first_selector is not None:
        raise ValueError(
            "--orbit cannot be combined with --first-selector"
        )
    selected_orbits = (
        sorted(set(map(int, args.orbit)))
        if args.orbit
        else list(
            range(
                args.orbit_offset,
                args.orbit_offset + args.orbits,
            )
        )
    )
    if selected_orbits and selected_orbits[0] < 0:
        raise ValueError("orbit labels must be nonnegative")
    selector_zero = (
        args.selector_zero
        if args.selector_zero is not None
        else 232
    )
    first_selector = (
        selector_zero + selected_orbits[0]
        if args.orbit
        else (
            args.first_selector
            if args.first_selector is not None
            else selector_zero + args.orbit_offset
        )
    )
    if first_selector < 1:
        raise ValueError("--first-selector must be positive")
    if args.orbits < 1:
        raise ValueError("--orbits must be positive")

    started = time.perf_counter()
    cnf_hash = sha256(args.cnf)
    cnf = CNF(from_file=str(args.cnf))
    rows: list[dict[str, object]] = []
    with Solver(
        name=args.solver, bootstrap_with=cnf.clauses
    ) as solver:
        for local_orbit, orbit in enumerate(selected_orbits):
            orbit_started = time.perf_counter()
            sat = solver.solve(
                assumptions=[
                    (
                        selector_zero + orbit
                        if args.orbit
                        else first_selector + local_orbit
                    )
                ]
            )
            rows.append(
                {
                    "orbit": orbit,
                    "sat": bool(sat),
                    "elapsed_seconds": (
                        time.perf_counter() - orbit_started
                    ),
                }
            )

    sat_orbits = [
        int(row["orbit"]) for row in rows if row["sat"]
    ]
    unsat_orbits = [
        int(row["orbit"]) for row in rows if not row["sat"]
    ]
    payload = {
        "status": (
            "UNSAT_every_first_factor_orbit"
            if not sat_orbits
            else "per_orbit_rule_sat_frontier"
        ),
        "cnf": str(args.cnf),
        "cnf_sha256": cnf_hash,
        "cnf_variables": cnf.nv,
        "cnf_clauses": len(cnf.clauses),
        "solver": args.solver,
        "first_selector": first_selector,
        "selector_zero": selector_zero,
        "orbit_offset": (
            selected_orbits[0] if args.orbit else args.orbit_offset
        ),
        "selected_orbits": selected_orbits,
        "first_factor_orbits": len(selected_orbits),
        "assumption_solves": len(selected_orbits),
        "sat_orbits": sat_orbits,
        "sat_orbit_ranges": consecutive_ranges(sat_orbits),
        "unsat_orbits": unsat_orbits,
        "unsat_orbit_ranges": consecutive_ranges(unsat_orbits),
        "orbit_results": rows,
        "elapsed_seconds": time.perf_counter() - started,
        "semantic_encoding_independently_verified": False,
        "exploratory_only": bool(sat_orbits),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
