"""Verify the uniform generic/exceptional elimination for prism core orbits."""

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
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from krenn_gu.enumerate_cubic_rankone import graph_edges, nested_pattern
from krenn_gu.prism_laurent_reduction import primitive_binomial_reduction
from prism_orbit_batch import (
    complement_edge_blocks,
    stabilizer_block_representatives,
)
from krenn_gu.prism_orbit_screen import (
    core_rank_one_audit_from_equations,
    minimal_monomial_zero_covers,
    orbit_equations,
    prism_orbit_representatives,
)
from krenn_gu.prism_rankone_parameterization import parameterize_polynomial
from prism_support_sat import (
    free_variable_indices,
    lambda_nonzero_variables,
)
from krenn_gu.rankone_support_sat import support_cnf
from krenn_gu.search_killer_patterns import active_mask_for_pattern
from krenn_gu.search_prism_stratum import PRISM_MATCHINGS
from krenn_gu.search_witness import EquationSystem


def verify_orbit(
    item: tuple[int, tuple[int, ...]]
) -> dict[str, object]:
    from pysat.solvers import Minisat22

    orbit_index, pattern = item
    system = EquationSystem(6, 3)
    names, equations = orbit_equations(system, pattern)
    audit = core_rank_one_audit_from_equations(names, equations)
    if not audit["passes"]:
        return {
            "orbit": orbit_index,
            "core": False,
            "linear_variables": audit.get("linear_variables"),
        }

    nested = nested_pattern(pattern)
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
    generic_cnf = support_cnf(
        system,
        nested,
        set(graph_edges(PRISM_MATCHINGS)),
        rectangular_support_edges=set(complement_edge_blocks()[0]),
    )
    free_entry_variables = []
    for edge in complement_edge_blocks()[0]:
        edge_index = system.edge_index[edge]
        for row in range(3):
            for column in range(3):
                flat_index = edge_index * 9 + 3 * row + column
                free_entry_variables.append(
                    cnf_variable_by_flat_index[flat_index]
                )
    # The extra clause asserts that at least one free entry is zero.
    generic_cnf.add(*(-variable for variable in free_entry_variables))
    with Minisat22(bootstrap_with=generic_cnf.clauses) as solver:
        admits_zero_entry = solver.solve()

    base_cnf = support_cnf(
        system,
        nested,
        set(graph_edges(PRISM_MATCHINGS)),
    )
    free_indices = free_variable_indices(system, pattern)
    lambdas = audit["lambdas"]
    matrices = audit["remainder_matrices"]
    assert isinstance(lambdas, list)
    assert isinstance(matrices, list)
    exceptional_branches = 0
    exceptional_sat_branches = 0
    with Minisat22(bootstrap_with=base_cnf.clauses) as solver:
        for block_index in stabilizer_block_representatives(pattern):
            lambda_variables = [
                cnf_variable_by_flat_index[free_indices[name]]
                for name in lambda_nonzero_variables(
                    lambdas[block_index]
                )
            ]
            for cover in minimal_monomial_zero_covers(
                matrices[block_index]
            ):
                assumptions = [
                    *lambda_variables,
                    *(
                        -cnf_variable_by_flat_index[free_indices[name]]
                        for name in cover
                    ),
                ]
                exceptional_branches += 1
                if solver.solve(assumptions=assumptions):
                    exceptional_sat_branches += 1

    parameterized = [
        parameterize_polynomial(equation) for equation in equations
    ]
    _, reduced, metadata = primitive_binomial_reduction(parameterized)
    unit_equations = sum(
        1 for equation in reduced if len(equation) == 1 and () in equation
    )
    return {
        "orbit": orbit_index,
        "core": True,
        "full_support_forced": not admits_zero_entry,
        "exceptional_branches": exceptional_branches,
        "exceptional_unsat_branches": (
            exceptional_branches - exceptional_sat_branches
        ),
        "unit_laurent_equations": unit_equations,
        "binomial_equations": metadata["binomial_equations"],
        "binomial_rank": metadata["binomial_rank"],
        "unimodular_determinant": metadata["unimodular_determinant"],
        "basis_equation_indices": metadata["basis_equation_indices"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    representatives = prism_orbit_representatives()
    items = list(enumerate(representatives))
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(verify_orbit, items))
    else:
        rows = [verify_orbit(item) for item in items]
    core_rows = [row for row in rows if row["core"]]
    failures = [
        row
        for row in core_rows
        if not row["full_support_forced"]
        or row["exceptional_unsat_branches"] != row["exceptional_branches"]
        or not row["unit_laurent_equations"]
        or row["binomial_rank"] != 13
        or abs(int(row["unimodular_determinant"])) != 1
    ]
    payload = {
        "prism_orbits": len(rows),
        "six_block_core_orbits": len(core_rows),
        "deficient_core_orbits": len(rows) - len(core_rows),
        "generic_full_support_forced": sum(
            bool(row["full_support_forced"]) for row in core_rows
        ),
        "generic_laurent_unit_certificates": sum(
            bool(row["unit_laurent_equations"]) for row in core_rows
        ),
        "exceptional_support_branches": sum(
            int(row["exceptional_branches"]) for row in core_rows
        ),
        "exceptional_support_unsat": sum(
            int(row["exceptional_unsat_branches"]) for row in core_rows
        ),
        "minimum_unit_equations": min(
            int(row["unit_laurent_equations"]) for row in core_rows
        ),
        "maximum_unit_equations": max(
            int(row["unit_laurent_equations"]) for row in core_rows
        ),
        "failures": failures,
        "rows": rows,
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: core={len(core_rows)} "
            f"failures={len(failures)}"
        )
    else:
        print(text)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
