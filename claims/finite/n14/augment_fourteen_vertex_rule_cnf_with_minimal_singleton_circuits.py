"""Add factor no-goods from the minimal singleton-circuit theorem."""

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
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

from certify_fourteen_vertex_minimal_singleton_circuit_factors import (
    contiguous_cycles,
    cycle_edges,
    perfect_matchings,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--compiled-result", type=Path, required=True)
    parser.add_argument("--factor-census", type=Path, required=True)
    parser.add_argument("--factor-audit", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    compiled = json.loads(
        args.compiled_result.read_text(encoding="utf-8")
    )
    census = json.loads(args.factor_census.read_text(encoding="utf-8"))
    audit = json.loads(args.factor_audit.read_text(encoding="utf-8"))
    partition = tuple(map(int, census["partition"]))
    if tuple(map(int, compiled["partition"])) != partition:
        raise ValueError("compiled result and factor census disagree")
    if not audit.get("verified"):
        raise ValueError("factor census audit is not verified")
    if audit.get("census_sha256") != sha256(args.factor_census):
        raise ValueError("factor census audit hash changed")

    cycles = contiguous_cycles(partition)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    eligible_edges = tuple(
        sorted(set(itertools.combinations(range(14), 2)) - full_edges)
    )
    if len(eligible_edges) != int(compiled["eligible_edges"]):
        raise AssertionError("eligible edge count changed")
    edge_index = {
        item: index for index, item in enumerate(eligible_edges)
    }
    factors = [
        factor
        for factor in perfect_matchings(14)
        if not (set(factor) & set(full_edges))
    ]
    if len(factors) != int(census["eligible_singleton_factors"]):
        raise AssertionError("eligible factor count changed")

    base = CNF(from_file=str(args.base_cnf))
    existing = {tuple(map(int, clause)) for clause in base.clauses}
    candidate_clauses = []
    new_clauses = []
    for record in census["obstructed_factor_records"]:
        factor = factors[int(record["factor_index"])]
        for role in range(3):
            clause = tuple(
                -(
                    role * len(eligible_edges)
                    + edge_index[item]
                    + 1
                )
                for item in factor
            )
            candidate_clauses.append(clause)
            if clause not in existing:
                existing.add(clause)
                new_clauses.append(clause)
    base.extend(new_clauses)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    base.to_file(str(args.output_cnf))

    selector_start = 3 * len(eligible_edges) + 1
    selector_count = int(compiled["first_factor_orbits"])
    unsat_orbits = []
    with Solver(
        name="cadical195", bootstrap_with=base.clauses
    ) as solver:
        sat = solver.solve()
        for orbit in range(selector_count):
            if not solver.solve(
                assumptions=[selector_start + orbit]
            ):
                unsat_orbits.append(orbit)

    payload = {
        "status": (
            "minimal_singleton_circuit_factor_no_goods_augmented"
        ),
        "partition": list(partition),
        "compiled_result": str(args.compiled_result),
        "compiled_result_sha256": sha256(args.compiled_result),
        "factor_census": str(args.factor_census),
        "factor_census_sha256": sha256(args.factor_census),
        "factor_audit": str(args.factor_audit),
        "factor_audit_sha256": sha256(args.factor_audit),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_variables": CNF(from_file=str(args.base_cnf)).nv,
        "base_clauses": len(CNF(from_file=str(args.base_cnf)).clauses),
        "eligible_singleton_factors": len(factors),
        "rectangle_obstructed_factors": int(
            census["rectangle_obstructed_factors"]
        ),
        "candidate_factor_no_goods": len(candidate_clauses),
        "new_factor_no_goods": len(new_clauses),
        "factor_no_good_widths": sorted(
            {len(clause) for clause in new_clauses}
        ),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_variables": base.nv,
        "output_clauses": len(base.clauses),
        "independent_solver": "cadical195",
        "sat": sat,
        "selector_orbits": selector_count,
        "unsat_selector_orbits": unsat_orbits,
        "unsat_selector_count": len(unsat_orbits),
        "elapsed_seconds": time.perf_counter() - started,
        "exploratory_until_independently_reconstructed": True,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
