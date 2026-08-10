"""Exhaust support charts for canonical killer patterns seen by global CEGAR."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from certify_union_orbit_supports import (
    restrict_equations,
)
from enumerate_cubic_rankone import canonical_pattern, nested_pattern
from global_candidate_laurent_cegar import exact_torus_unit
from killer_union_stratum import union_orbit_equations
from prism_laurent_reduction import primitive_binomial_reduction
from prism_orbit_screen import clean_polynomial
from rankone_support_sat import support_cnf
from search_killer_patterns import active_mask_for_pattern
from search_witness import EquationSystem


def pattern_union(
    pattern: list[list[int]],
) -> set[tuple[int, int]]:
    return {
        tuple(sorted((vertex, neighbour)))
        for vertex, row in enumerate(pattern)
        for neighbour in row
    }


def certify_pattern_with_fallback(
    index: int,
    pattern: list[list[int]],
    max_certificates: int,
    fallback_directory: Path,
    support_solver: str,
    normalize_mutual: bool = False,
) -> dict[str, object]:
    """Exhaust every support chart, continuing after exact torus fallbacks."""
    from pysat.solvers import Solver

    system = EquationSystem(6, 3)
    names, equations, variable_names = union_orbit_equations(
        system,
        pattern,
        normalize_mutual=normalize_mutual,
    )
    structural_indices = [
        int(flat_index)
        for flat_index in np.flatnonzero(
            active_mask_for_pattern(system, pattern)
        )
    ]
    variable_by_flat = {
        flat_index: variable
        for variable, flat_index in enumerate(structural_indices, start=1)
    }
    variable_by_name = {
        name: variable_by_flat[flat_index]
        for flat_index, name in variable_names.items()
    }
    cnf = support_cnf(system, pattern, pattern_union(pattern))
    certificates: list[dict[str, object]] = []
    exact_certificates: list[dict[str, object]] = []
    with Solver(name=support_solver, bootstrap_with=cnf.clauses) as solver:
        while solver.solve():
            if (
                len(certificates) + len(exact_certificates)
                >= max_certificates
            ):
                return {
                    "status": "limit",
                    "variables": len(names),
                    "certificates": certificates,
                    "exact_certificates": exact_certificates,
                }
            model = set(solver.get_model() or ())
            nonzero_names = {
                name
                for name, variable in variable_by_name.items()
                if variable in model
            }
            restricted, sources = restrict_equations(
                equations,
                nonzero_names,
            )
            active_names = [
                name for name in names if name in nonzero_names
            ]
            reduced_names, reduced, metadata = (
                primitive_binomial_reduction(
                    restricted,
                    active_names,
                )
            )
            unit_indices = list(metadata["unit_equation_indices"])
            linear_units = list(
                metadata["linear_monomial_unit_relations"]
            )
            if not unit_indices and not linear_units:
                fallback_id = f"{index}_{len(exact_certificates)}"
                if not exact_torus_unit(
                    reduced_names,
                    reduced,
                    fallback_directory,
                    fallback_id,
                ):
                    return {
                        "status": "algebraic_survivor",
                        "variables": len(names),
                        "support_nonzero": sorted(nonzero_names),
                        "metadata": metadata,
                        "certificates": certificates,
                        "exact_certificates": exact_certificates,
                    }
                zero_names = set(variable_by_name) - nonzero_names
                blocking_clause = [
                    *(
                        -variable_by_name[name]
                        for name in sorted(nonzero_names)
                    ),
                    *(
                        variable_by_name[name]
                        for name in sorted(zero_names)
                    ),
                ]
                solver.add_clause(blocking_clause)
                exact_certificates.append(
                    {
                        "fallback_id": fallback_id,
                        "nonzero_support": sorted(nonzero_names),
                        "metadata": metadata,
                    }
                )
                continue

            basis_indices = metadata["basis_equation_indices"]
            if unit_indices:
                unit_reduced_index: int | None = int(unit_indices[0])
                linear_unit: dict[str, object] | None = None
                linear_reduced_indices: list[int] = []
            else:
                unit_reduced_index = None
                linear_unit = dict(linear_units[0])
                output_sources = list(
                    metadata["output_equation_sources"]
                )
                linear_reduced_indices = [
                    int(output_sources[int(index)])
                    for index in linear_unit[
                        "output_equation_indices"
                    ]
                ]
            used_original = {
                sources[reduced_index]
                for reduced_index in [
                    *basis_indices,
                    *(
                        []
                        if unit_reduced_index is None
                        else [unit_reduced_index]
                    ),
                    *linear_reduced_indices,
                ]
            }
            positive_names: set[str] = set()
            negative_names: set[str] = set()
            for equation_index in used_original:
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
                    -variable_by_name[name]
                    for name in sorted(positive_names)
                ),
                *(
                    variable_by_name[name]
                    for name in sorted(negative_names)
                ),
            ]
            if not blocking_clause:
                return {
                    "status": "unconditional_laurent_contradiction",
                    "variables": len(names),
                    "certificates": certificates,
                    "exact_certificates": exact_certificates,
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
                        sources[reduced_index]
                        for reduced_index in basis_indices
                    ),
                    "unit_equation": (
                        None
                        if unit_reduced_index is None
                        else sources[unit_reduced_index]
                    ),
                    "linear_equations": sorted(
                        sources[index]
                        for index in linear_reduced_indices
                    ),
                    "linear_monomial_unit_relation": linear_unit,
                    "positive_cube": sorted(positive_names),
                    "negative_cube": sorted(negative_names),
                }
            )
    return {
        "status": (
            "certified_with_exact_fallback"
            if exact_certificates
            else "certified"
        ),
        "variables": len(names),
        "certificates": certificates,
        "exact_certificates": exact_certificates,
    }


def certify_item(
    item: tuple[int, tuple[int, ...], int, str, str],
) -> dict[str, object]:
    (
        index,
        flat_pattern,
        max_certificates,
        fallback_directory_text,
        support_solver,
    ) = item
    pattern = nested_pattern(flat_pattern)
    result = certify_pattern_with_fallback(
        index,
        pattern,
        max_certificates,
        Path(fallback_directory_text),
        support_solver,
    )
    used_exact_fallback = bool(result["exact_certificates"])
    return {
        "orbit": index,
        "pattern": pattern,
        "union_size": len(pattern_union(pattern)),
        "status": result["status"],
        "variables": result["variables"],
        "certificate_count": len(result["certificates"]),
        "used_exact_fallback": used_exact_fallback,
        "support_nonzero": result.get("support_nonzero"),
        "metadata": result.get("metadata"),
        "certificates": result["certificates"],
        "exact_certificates": result["exact_certificates"],
        "support_solver": support_solver,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--max-certificates", type=int, default=10_000)
    parser.add_argument(
        "--support-solver",
        choices=("cadical195", "glucose42", "minisat22"),
        default="minisat22",
    )
    parser.add_argument(
        "--fallback-directory",
        type=Path,
        default=Path("tmp/global_pattern_orbit_fallback"),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    vertex_permutations = list(itertools.permutations(range(6)))
    representatives = sorted(
        {
            canonical_pattern(
                tuple(
                    neighbour
                    for row in row_payload["pattern"]
                    for neighbour in row
                ),
                vertex_permutations,
            )
            for row_payload in manifest["rows"]
        }
    )
    items = [
        (
            index,
            pattern,
            args.max_certificates,
            str(args.fallback_directory),
            args.support_solver,
        )
        for index, pattern in enumerate(representatives)
    ]
    if args.jobs > 1:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            rows = list(executor.map(certify_item, items))
    else:
        rows = [certify_item(item) for item in items]
    counts = Counter(str(row["status"]) for row in rows)
    result = {
        "source_manifest": str(args.manifest),
        "pattern_orbits": len(rows),
        "status_counts": dict(counts),
        "fully_certified": all(
            row["status"]
            in {
                "certified",
                "certified_with_exact_fallback",
                "unconditional_laurent_contradiction",
            }
            for row in rows
        ),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: pattern_orbits={len(rows)} "
        f"counts={dict(counts)}"
    )
    if not result["fully_certified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
