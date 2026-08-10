"""Support-level certificates for generic and exceptional prism branches.

The generic core forces each of the six complement blocks to rank at most
one, hence its nonzero support is rectangular.  On an exceptional branch,
``lambda = 0`` forces the variables in lambda's nonconstant monomial to be
nonzero, while one minimal cover of the rank-one remainder is zero.
Both are exact necessary conditions and can be tested by SAT before invoking
polynomial elimination.
"""

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
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from krenn_gu.enumerate_cubic_rankone import graph_edges, nested_pattern
from prism_orbit_batch import (
    complement_edge_blocks,
    stabilizer_block_representatives,
)
from krenn_gu.prism_orbit_screen import (
    Polynomial,
    core_rank_one_audit,
    minimal_monomial_zero_covers,
    normalized_pattern_stratum,
    prism_orbit_representatives,
)
from krenn_gu.rankone_support_sat import CNF, solve_with_minisat, support_cnf
from krenn_gu.search_killer_patterns import active_mask_for_pattern
from krenn_gu.search_prism_stratum import PRISM_MATCHINGS
from krenn_gu.search_witness import EquationSystem


def free_variable_indices(
    system: EquationSystem, pattern: tuple[int, ...]
) -> dict[str, int]:
    _, active = normalized_pattern_stratum(system, pattern)
    return {
        f"x{variable_index}": int(flat_index)
        for variable_index, flat_index in enumerate(np.flatnonzero(active))
    }


def lambda_nonzero_variables(lambda_polynomial: Polynomial) -> set[str]:
    """Variables forced nonzero by a binomial ``1 + monomial = 0``."""
    constant = lambda_polynomial.get((), 0)
    nonconstant = [
        monomial
        for monomial, coefficient in lambda_polynomial.items()
        if monomial and coefficient
    ]
    if constant == 0 or len(nonconstant) != 1:
        raise ValueError(
            "exceptional support extraction requires constant plus one monomial"
        )
    return set(nonconstant[0])


def orbit_support_jobs(
    system: EquationSystem,
    orbit_index: int,
    pattern: tuple[int, ...],
) -> list[tuple[str, object]]:
    audit = core_rank_one_audit(system, pattern)
    if not audit["passes"]:
        return []
    lambdas = audit["lambdas"]
    matrices = audit["remainder_matrices"]
    assert isinstance(lambdas, list)
    assert isinstance(matrices, list)
    nested = nested_pattern(pattern)
    fixed_edges = set(graph_edges(PRISM_MATCHINGS))
    generic = support_cnf(
        system,
        nested,
        fixed_edges,
        rectangular_support_edges=set(complement_edge_blocks()[0]),
    )
    base = support_cnf(system, nested, fixed_edges)
    active_indices = [
        int(flat_index)
        for flat_index in np.flatnonzero(
            active_mask_for_pattern(system, nested)
        )
    ]
    cnf_variable_by_flat_index = {
        flat_index: variable
        for variable, flat_index in enumerate(active_indices, start=1)
    }
    free_indices = free_variable_indices(system, pattern)
    jobs: list[tuple[str, object]] = [
        ("generic", generic)
    ]
    for block_index in stabilizer_block_representatives(pattern):
        covers = minimal_monomial_zero_covers(matrices[block_index])
        forced_nonzero = {
            cnf_variable_by_flat_index[free_indices[name]]
            for name in lambda_nonzero_variables(lambdas[block_index])
        }
        for cover_index, cover in enumerate(covers):
            label = f"b{block_index}_cover{cover_index}"
            cnf = CNF(base.variable_count, list(base.clauses))
            for variable in sorted(forced_nonzero):
                cnf.add(variable)
            for name in cover:
                cnf.add(
                    -cnf_variable_by_flat_index[free_indices[name]]
                )
            jobs.append((label, cnf))
    return jobs


def solve_with_pysat(cnf: CNF) -> str:
    """Solve in-process when python-sat is available on PYTHONPATH."""
    from pysat.solvers import Minisat22

    with Minisat22(bootstrap_with=cnf.clauses) as solver:
        return "SAT" if solver.solve() else "UNSAT"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--indices", type=int, nargs="*")
    parser.add_argument(
        "--all-reduced",
        action="store_true",
        help="check all prism orbits that pass the six-block core audit",
    )
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--tmp", type=Path, default=Path("tmp/prism_support"))
    parser.add_argument(
        "--solver",
        choices=("minisat", "pysat"),
        default="minisat",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--generic-only",
        action="store_true",
        help="skip exceptional lambda-zero cover branches",
    )
    args = parser.parse_args()
    representatives = prism_orbit_representatives()
    system = EquationSystem(6, 3)
    if args.all_reduced:
        indices = [
            index
            for index, pattern in enumerate(representatives)
            if core_rank_one_audit(system, pattern)["passes"]
        ]
    elif args.indices:
        indices = args.indices
    else:
        parser.error("provide --indices or --all-reduced")

    args.tmp.mkdir(parents=True, exist_ok=True)
    def analyze_orbit(orbit_index: int) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        pattern = representatives[orbit_index]
        for label, cnf in orbit_support_jobs(system, orbit_index, pattern):
            if args.generic_only and label != "generic":
                continue
            if args.solver == "pysat":
                status = solve_with_pysat(cnf)
            else:
                status = solve_with_minisat(
                    cnf,
                    args.tmp / f"orbit_{orbit_index}_{label}.cnf",
                )
            rows.append(
                {
                    "orbit": orbit_index,
                    "branch": label,
                    "status": status,
                    "variables": cnf.variable_count,
                    "clauses": len(cnf.clauses),
                }
            )
        return rows

    if args.jobs > 1:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            grouped_results = list(executor.map(analyze_orbit, indices))
    else:
        grouped_results = [analyze_orbit(index) for index in indices]
    results = [row for group in grouped_results for row in group]
    counts = Counter(str(row["status"]) for row in results)
    closed = sorted(
        {
            orbit_index
            for orbit_index in indices
            if all(
                row["status"] == "UNSAT"
                for row in results
                if row["orbit"] == orbit_index
            )
        }
    )
    payload = json.dumps(
        {
            "orbits": len(indices),
            "jobs": len(results),
            "status_counts": dict(counts),
            "fully_support_closed_orbits": closed,
            "results": results,
        },
        indent=2,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: orbits={len(indices)} jobs={len(results)} "
            f"counts={dict(counts)}"
        )
    else:
        print(payload)


if __name__ == "__main__":
    main()
