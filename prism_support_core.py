"""Extract small colouring-level UNSAT cores for exceptional prism branches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from enumerate_cubic_rankone import graph_edges, nested_pattern
from prism_orbit_batch import stabilizer_block_representatives
from prism_orbit_screen import (
    core_rank_one_audit,
    minimal_monomial_zero_covers,
    normalized_pattern_stratum,
    prism_orbit_representatives,
)
from prism_support_sat import (
    free_variable_indices,
    lambda_nonzero_variables,
)
from rankone_support_sat import support_cnf
from search_killer_patterns import active_mask_for_pattern
from search_prism_stratum import PRISM_MATCHINGS
from search_witness import EquationSystem


def minimize_assumption_core(solver, assumptions: list[int]) -> list[int]:
    """Deletion-minimize an UNSAT assumption core."""
    if solver.solve(assumptions=assumptions):
        raise ValueError("branch is SAT under all colouring assumptions")
    core = list(solver.get_core() or assumptions)
    position = 0
    while position < len(core):
        trial = core[:position] + core[position + 1 :]
        if not solver.solve(assumptions=trial):
            core = list(solver.get_core() or trial)
            position = 0
        else:
            position += 1
    return sorted(core)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, default=0)
    parser.add_argument("--block", type=int)
    parser.add_argument("--cover", type=int, default=0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    from pysat.solvers import Minisat22

    system = EquationSystem(6, 3)
    representatives = prism_orbit_representatives()
    pattern = representatives[args.orbit]
    audit = core_rank_one_audit(system, pattern)
    if not audit["passes"]:
        raise ValueError("orbit does not have the six-block core")
    lambdas = audit["lambdas"]
    matrices = audit["remainder_matrices"]
    assert isinstance(lambdas, list)
    assert isinstance(matrices, list)
    blocks = stabilizer_block_representatives(pattern)
    block = blocks[0] if args.block is None else args.block
    covers = minimal_monomial_zero_covers(matrices[block])
    cover = covers[args.cover]

    nested = nested_pattern(pattern)
    selectors: dict[int, int] = {}
    cnf = support_cnf(
        system,
        nested,
        set(graph_edges(PRISM_MATCHINGS)),
        colouring_selectors=selectors,
    )
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
    lambda_variables = sorted(
        lambda_nonzero_variables(lambdas[block])
    )
    for name in lambda_variables:
        cnf.add(cnf_variable_by_flat_index[free_indices[name]])
    for name in cover:
        cnf.add(-cnf_variable_by_flat_index[free_indices[name]])

    with Minisat22(bootstrap_with=cnf.clauses) as solver:
        core_variables = minimize_assumption_core(
            solver, list(selectors.values())
        )
    colouring_by_selector = {
        selector: index for index, selector in selectors.items()
    }
    core_indices = [
        colouring_by_selector[selector] for selector in core_variables
    ]
    payload = {
        "orbit": args.orbit,
        "pattern": nested,
        "block": block,
        "cover_index": args.cover,
        "lambda_nonzero_variables": lambda_variables,
        "cover_zero_variables": list(cover),
        "core_size": len(core_indices),
        "colourings": [
            [int(value) for value in system.colourings[index]]
            for index in core_indices
        ],
    }
    text = json.dumps(payload, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.output}: core_size={len(core_indices)}")
    else:
        print(text)


if __name__ == "__main__":
    main()
