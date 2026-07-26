"""Extract one exact SAT support from a compiled all-even rule CNF.

This is deliberately a sampler, not a verifier.  It decodes the three
singleton perfect matchings from a CaDiCaL model and writes the same compact
support format consumed by the support-local obstruction analyzers.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from analyze_fourteen_vertex_two_even_cycle_rule_sat import (
    edge_variable,
    parse_factor,
)
from explore_fourteen_vertex_equality_factor_family import (
    N,
    contiguous_cycles,
)
from explore_random_even_cycle_forks import cycle_edges


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--orbit", type=int)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    census = json.loads(args.census.read_text(encoding="utf-8"))
    lengths = tuple(map(int, census["partition"]))
    if (
        sum(lengths) != N
        or len(lengths) < 2
        or any(length % 2 for length in lengths)
    ):
        raise AssertionError("census is not an all-even order-14 partition")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    representatives = tuple(
        parse_factor(row["representative"])
        for row in census["factor_orbits"]
    )
    if args.orbit is not None and not (
        0 <= args.orbit < len(representatives)
    ):
        raise ValueError("orbit is outside the census")
    selectors = tuple(
        3 * len(eligible_edges) + 1 + index
        for index in range(len(representatives))
    )

    cnf = CNF(from_file=str(args.cnf))
    assumptions = (
        [selectors[args.orbit]] if args.orbit is not None else []
    )
    with Solver(
        name="cadical195", bootstrap_with=cnf.clauses
    ) as solver:
        sat = solver.solve(assumptions=assumptions)
        model = solver.get_model() if sat else None

    survivors = []
    selected_orbit = None
    if model is not None:
        positive = {literal for literal in model if literal > 0}
        selected = [
            index
            for index, selector in enumerate(selectors)
            if selector in positive
        ]
        if len(selected) != 1:
            raise AssertionError("SAT model has no unique orbit selector")
        selected_orbit = selected[0]
        if args.orbit is not None and selected_orbit != args.orbit:
            raise AssertionError("conditioned selector changed")
        factors = tuple(
            tuple(
                item
                for edge_id, item in enumerate(eligible_edges)
                if edge_variable(
                    role, edge_id, len(eligible_edges)
                )
                in positive
            )
            for role in range(3)
        )
        if any(len(factor) != N // 2 for factor in factors):
            raise AssertionError("decoded role is not a perfect matching")
        if factors[0] != representatives[selected_orbit]:
            raise AssertionError("first factor is not the selected representative")
        survivors.append(
            {
                "orbit_id": selected_orbit,
                "first": [list(item) for item in factors[0]],
                "second": [list(item) for item in factors[1]],
                "third": [list(item) for item in factors[2]],
            }
        )

    payload = {
        "status": (
            "SAT_rule_residual_samples"
            if sat
            else "UNSAT_conditioned_rule_cnf"
        ),
        "partition": list(lengths),
        "source_census": str(args.census),
        "source_census_sha256": sha256(args.census),
        "source_cnf": str(args.cnf),
        "source_cnf_sha256": sha256(args.cnf),
        "conditioned_orbit": args.orbit,
        "selected_orbit": selected_orbit,
        "survivors": survivors,
        "cnf_variables": cnf.nv,
        "cnf_clauses": len(cnf.clauses),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_only": sat,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
