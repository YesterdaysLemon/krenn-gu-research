"""Independently reconstruct a singleton-circuit CNF augmentation."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from verify_fourteen_vertex_minimal_singleton_circuit_factors import (
    edge,
    enumerate_matchings,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("augmentation", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest = json.loads(
        args.augmentation.read_text(encoding="utf-8")
    )
    paths = {
        key: Path(manifest[key])
        for key in (
            "compiled_result",
            "factor_census",
            "factor_audit",
            "base_cnf",
            "output_cnf",
        )
    }
    for key, path in paths.items():
        if sha256(path) != manifest[f"{key}_sha256"]:
            raise AssertionError(f"{key} hash changed")
    compiled = json.loads(
        paths["compiled_result"].read_text(encoding="utf-8")
    )
    census = json.loads(
        paths["factor_census"].read_text(encoding="utf-8")
    )
    audit = json.loads(
        paths["factor_audit"].read_text(encoding="utf-8")
    )
    if (
        not audit.get("verified")
        or audit.get("census_sha256")
        != manifest["factor_census_sha256"]
    ):
        raise AssertionError("factor census audit changed")
    partition = tuple(map(int, census["partition"]))
    if partition != tuple(map(int, compiled["partition"])):
        raise AssertionError("partition changed")

    cycles = []
    start = 0
    for length in partition:
        cycles.append(tuple(range(start, start + length)))
        start += length
    full_edges = {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for cycle in cycles
        for index in range(len(cycle))
    }
    eligible_edges = tuple(
        sorted(set(itertools.combinations(range(14), 2)) - full_edges)
    )
    edge_index = {
        item: index for index, item in enumerate(eligible_edges)
    }
    factors = [
        factor
        for factor in enumerate_matchings(tuple(range(14)))
        if not (set(factor) & full_edges)
    ]
    if len(factors) != int(census["eligible_singleton_factors"]):
        raise AssertionError("factor enumeration changed")

    base = CNF(from_file=str(paths["base_cnf"]))
    if (
        base.nv != int(manifest["base_variables"])
        or len(base.clauses) != int(manifest["base_clauses"])
    ):
        raise AssertionError("base DIMACS dimensions changed")
    existing = {tuple(map(int, clause)) for clause in base.clauses}
    candidate_count = 0
    new_clauses = []
    for record in census["obstructed_factor_records"]:
        factor = factors[int(record["factor_index"])]
        for role in range(3):
            candidate_count += 1
            clause = tuple(
                -(
                    role * len(eligible_edges)
                    + edge_index[item]
                    + 1
                )
                for item in factor
            )
            if clause not in existing:
                existing.add(clause)
                new_clauses.append(clause)
    if candidate_count != int(manifest["candidate_factor_no_goods"]):
        raise AssertionError("candidate no-good count changed")
    if len(new_clauses) != int(manifest["new_factor_no_goods"]):
        raise AssertionError("new no-good count changed")
    base.extend(new_clauses)
    observed = CNF(from_file=str(paths["output_cnf"]))
    if (
        base.nv != observed.nv
        or base.clauses != observed.clauses
        or observed.nv != int(manifest["output_variables"])
        or len(observed.clauses) != int(manifest["output_clauses"])
    ):
        raise AssertionError("output CNF reconstruction changed")

    selector_start = 3 * len(eligible_edges) + 1
    selector_count = int(manifest["selector_orbits"])
    unsat_orbits = []
    with Solver(
        name="cadical195", bootstrap_with=observed.clauses
    ) as solver:
        sat = solver.solve()
        for orbit in range(selector_count):
            if not solver.solve(
                assumptions=[selector_start + orbit]
            ):
                unsat_orbits.append(orbit)
    if sat != bool(manifest["sat"]):
        raise AssertionError("global SAT status changed")
    if unsat_orbits != manifest["unsat_selector_orbits"]:
        raise AssertionError("selector audit changed")

    payload = {
        "verified": True,
        "status": (
            "minimal_singleton_circuit_factor_augmentation_"
            "reconstructed"
        ),
        "scope": (
            "all source hashes, independent factor enumeration, exact "
            "role no-goods, DIMACS reconstruction, and selector SAT audit"
        ),
        "augmentation": str(args.augmentation),
        "augmentation_sha256": sha256(args.augmentation),
        "partition": list(partition),
        "eligible_singleton_factors": len(factors),
        "rectangle_obstructed_factors": int(
            census["rectangle_obstructed_factors"]
        ),
        "new_factor_no_goods": len(new_clauses),
        "output_variables": observed.nv,
        "output_clauses": len(observed.clauses),
        "independent_solver": "cadical195",
        "sat": sat,
        "unsat_selector_count": len(unsat_orbits),
        "unsat_selector_orbits": unsat_orbits,
        "elapsed_seconds": time.perf_counter() - started,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
