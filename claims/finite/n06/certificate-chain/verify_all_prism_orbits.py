"""Exact support/Laurent verification of all 718 mutual prism label orbits."""

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
from prism_orbit_batch import complement_edge_blocks
from krenn_gu.prism_orbit_screen import orbit_equations, prism_orbit_representatives
from prism_partial_core import partial_core_audit
from prism_partial_parameterization import (
    partial_parameter_names,
    partially_parameterize_polynomial,
)
from prism_support_sat import free_variable_indices, lambda_nonzero_variables
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
    audit = partial_core_audit(names, equations)
    if not audit["passes"]:
        return {
            "orbit": orbit_index,
            "partial_core": False,
            "reason": audit["reason"],
        }
    blocks = audit["blocks"]
    rank_one_blocks = audit["rank_one_blocks"]
    assert isinstance(blocks, list)
    assert isinstance(rank_one_blocks, set)

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
    free_indices = free_variable_indices(system, pattern)
    free_edges = complement_edge_blocks()[0]
    free_entry_variables = [
        cnf_variable_by_flat_index[
            system.edge_index[edge] * 9 + 3 * row + column
        ]
        for edge in free_edges
        for row in range(3)
        for column in range(3)
    ]

    generic_cnf = support_cnf(
        system,
        nested,
        set(graph_edges(PRISM_MATCHINGS)),
        rectangular_support_edges={
            free_edges[block] for block in rank_one_blocks
        },
    )
    generic_cnf.add(*(-variable for variable in free_entry_variables))
    with Minisat22(bootstrap_with=generic_cnf.clauses) as solver:
        generic_admits_zero_entry = solver.solve()

    base_cnf = support_cnf(
        system,
        nested,
        set(graph_edges(PRISM_MATCHINGS)),
    )
    branch_data: list[tuple[int, list[int]]] = []
    for block_index, block in enumerate(blocks):
        selector = base_cnf.variable()
        remainders = block["remainders"]
        assert isinstance(remainders, dict)
        for remainder in remainders.values():
            monomials = [
                monomial
                for monomial, coefficient in remainder.items()
                if coefficient
            ]
            if len(monomials) != 1:
                raise ValueError("partial-core remainder is not monomial")
            base_cnf.add(
                -selector,
                *(
                    -cnf_variable_by_flat_index[free_indices[name]]
                    for name in monomials[0]
                ),
            )
        lambda_polynomial = block["lambda"]
        assumptions = [
            selector,
            *(
                cnf_variable_by_flat_index[free_indices[name]]
                for name in lambda_nonzero_variables(
                    lambda_polynomial
                )
            ),
        ]
        branch_data.append((block_index, assumptions))
    exceptional_sat_blocks: list[int] = []
    with Minisat22(bootstrap_with=base_cnf.clauses) as solver:
        for block_index, assumptions in branch_data:
            if solver.solve(assumptions=assumptions):
                exceptional_sat_blocks.append(block_index)

    parameterized = [
        partially_parameterize_polynomial(
            equation, rank_one_blocks
        )
        for equation in equations
    ]
    parameter_names = partial_parameter_names(rank_one_blocks)
    _, reduced, metadata = primitive_binomial_reduction(
        parameterized, parameter_names
    )
    unit_equations = sum(
        1 for equation in reduced if len(equation) == 1 and () in equation
    )
    defect_count = 6 - len(rank_one_blocks)
    return {
        "orbit": orbit_index,
        "partial_core": True,
        "linear_variables": audit["linear_variables"],
        "rank_one_blocks": len(rank_one_blocks),
        "generic_full_support_forced": not generic_admits_zero_entry,
        "exceptional_lambda_blocks": 6,
        "exceptional_support_unsat": 6 - len(exceptional_sat_blocks),
        "exceptional_sat_blocks": exceptional_sat_blocks,
        "parameter_variables": len(parameter_names),
        "binomial_equations": metadata["binomial_equations"],
        "binomial_rank": metadata["binomial_rank"],
        "expected_binomial_rank": 13 + 4 * defect_count,
        "unimodular_determinant": metadata["unimodular_determinant"],
        "unit_laurent_equations": unit_equations,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    items = list(enumerate(prism_orbit_representatives()))
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(verify_orbit, items))
    else:
        rows = [verify_orbit(item) for item in items]
    failures = [
        row
        for row in rows
        if not row["partial_core"]
        or not row["generic_full_support_forced"]
        or row["exceptional_support_unsat"]
        != row["exceptional_lambda_blocks"]
        or row["binomial_rank"] != row["expected_binomial_rank"]
        or abs(int(row["unimodular_determinant"])) != 1
        or not row["unit_laurent_equations"]
    ]
    payload = {
        "prism_orbits": len(rows),
        "partial_core_orbits": sum(
            bool(row["partial_core"]) for row in rows
        ),
        "generic_full_support_forced": sum(
            bool(row["generic_full_support_forced"]) for row in rows
        ),
        "generic_laurent_unit_certificates": sum(
            bool(row["unit_laurent_equations"]) for row in rows
        ),
        "exceptional_lambda_branches": sum(
            int(row["exceptional_lambda_blocks"]) for row in rows
        ),
        "exceptional_support_unsat": sum(
            int(row["exceptional_support_unsat"]) for row in rows
        ),
        "minimum_unit_equations": min(
            int(row["unit_laurent_equations"]) for row in rows
        ),
        "maximum_unit_equations": max(
            int(row["unit_laurent_equations"]) for row in rows
        ),
        "failures": failures,
        "rows": rows,
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: orbits={len(rows)} "
            f"failures={len(failures)}"
        )
    else:
        print(text)
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
