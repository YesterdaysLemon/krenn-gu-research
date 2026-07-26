"""CEGAR support/Laurent certificates for a fixed killer-union orbit."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np

from enumerate_killer_union_orbits import parse_edges, union_from_missing
from killer_union_stratum import union_orbit_equations
from prism_laurent_reduction import primitive_binomial_reduction
from prism_orbit_screen import clean_polynomial
from rankone_support_sat import support_cnf
from search_killer_patterns import active_mask_for_pattern
from search_witness import EquationSystem


def restrict_equations(
    equations,
    nonzero_names: set[str],
) -> tuple[list[Counter], list[int]]:
    restricted = []
    sources = []
    for equation_index, equation in enumerate(equations):
        surviving = Counter(
            {
                monomial: coefficient
                for monomial, coefficient in equation.items()
                if all(variable in nonzero_names for variable in monomial)
            }
        )
        surviving = clean_polynomial(surviving)
        if surviving:
            restricted.append(surviving)
            sources.append(equation_index)
    return restricted, sources


def certify_orbit(
    pattern: list[list[int]],
    union_edges: set[tuple[int, int]],
    max_certificates: int = 10_000,
    solver_name: str = "minisat22",
    normalize_mutual: bool = True,
) -> dict[str, object]:
    from pysat.solvers import Solver

    system = EquationSystem(6, 3)
    names, equations, variable_names = union_orbit_equations(
        system,
        pattern,
        normalize_mutual=normalize_mutual,
    )
    structural_indices = [
        int(index)
        for index in np.flatnonzero(
            active_mask_for_pattern(system, pattern)
        )
    ]
    cnf_variable_by_flat_index = {
        flat_index: variable
        for variable, flat_index in enumerate(structural_indices, start=1)
    }
    cnf_variable_by_name = {
        name: cnf_variable_by_flat_index[flat_index]
        for flat_index, name in variable_names.items()
    }
    cnf = support_cnf(system, pattern, union_edges)
    certificates: list[dict[str, object]] = []
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        while solver.solve():
            if len(certificates) >= max_certificates:
                return {
                    "status": "limit",
                    "variables": len(names),
                    "certificates": certificates,
                }
            model = set(solver.get_model() or ())
            nonzero_names = {
                name
                for name, variable in cnf_variable_by_name.items()
                if variable in model
            }
            restricted, sources = restrict_equations(
                equations, nonzero_names
            )
            active_names = [
                name for name in names if name in nonzero_names
            ]
            _, _, metadata = primitive_binomial_reduction(
                restricted, active_names
            )
            unit_restricted_indices = metadata[
                "unit_equation_indices"
            ]
            if not unit_restricted_indices:
                return {
                    "status": "algebraic_survivor",
                    "variables": len(names),
                    "support_nonzero": sorted(nonzero_names),
                    "metadata": metadata,
                    "certificates": certificates,
                }
            basis_restricted_indices = metadata[
                "basis_equation_indices"
            ]
            used_original_indices = {
                sources[index]
                for index in [
                    *basis_restricted_indices,
                    unit_restricted_indices[0],
                ]
            }
            positive_names: set[str] = set()
            negative_names: set[str] = set()
            for equation_index in used_original_indices:
                for monomial, coefficient in equations[
                    equation_index
                ].items():
                    if not coefficient:
                        continue
                    zero_factors = [
                        variable
                        for variable in monomial
                        if variable not in nonzero_names
                    ]
                    if zero_factors:
                        negative_names.add(zero_factors[0])
                    else:
                        positive_names.update(monomial)
            if positive_names & negative_names:
                raise AssertionError("support cube is inconsistent")
            blocking_clause = [
                *(
                    -cnf_variable_by_name[name]
                    for name in sorted(positive_names)
                ),
                *(
                    cnf_variable_by_name[name]
                    for name in sorted(negative_names)
                ),
            ]
            if not blocking_clause:
                return {
                    "status": "unconditional_laurent_contradiction",
                    "variables": len(names),
                    "certificates": certificates,
                }
            solver.add_clause(blocking_clause)
            certificates.append(
                {
                    "nonzero_support_size": len(nonzero_names),
                    "binomial_rank": metadata["binomial_rank"],
                    "unimodular_determinant": metadata[
                        "unimodular_determinant"
                    ],
                    "basis_equations": sorted(
                        sources[index]
                        for index in basis_restricted_indices
                    ),
                    "unit_equation": sources[
                        unit_restricted_indices[0]
                    ],
                    "positive_cube": sorted(positive_names),
                    "negative_cube": sorted(negative_names),
                }
            )
    return {
        "status": "certified",
        "variables": len(names),
        "certificates": certificates,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbits", type=Path, required=True)
    parser.add_argument("--index", type=int, required=True)
    parser.add_argument(
        "--missing-edges",
        required=True,
    )
    parser.add_argument("--max-certificates", type=int, default=10_000)
    parser.add_argument(
        "--solver",
        choices=("cadical195", "glucose42", "minisat22"),
        default="minisat22",
    )
    parser.add_argument("--unnormalized", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.orbits.read_text(encoding="utf-8"))
    pattern = payload["representatives"][args.index]
    union_edges = set(
        union_from_missing(parse_edges(args.missing_edges))
    )
    result = certify_orbit(
        pattern,
        union_edges,
        args.max_certificates,
        args.solver,
        not args.unnormalized,
    )
    result["orbit"] = args.index
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
        print(
            f"wrote {args.output}: status={result['status']} "
            f"certificates={len(result['certificates'])}"
        )
    else:
        print(text)
    if result["status"] not in {
        "certified",
        "unconditional_laurent_contradiction",
    }:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
