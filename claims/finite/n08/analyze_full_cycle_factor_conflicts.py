"""Probe a common cycle-factor obstruction in all hard equality orbits.

For each binomial-free full-``C4+C4`` support, retain only forbidden
amplitudes whose four active matchings use full blocks exclusively.  Solve
their two-way factor clauses once, then test that selected relation branch
against all amplitudes.  The output records the first exact lattice
contradiction and the cycle-colour structure of its target amplitude.

This is an exploratory pattern census, not a theorem verifier.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from pysat.solvers import Solver

from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from eight_vertex_sparse_exact import positive_model_literals
from factor_lattice_cegar import (
    active_matching_data,
    exact_lattice_conflict,
    factor_relations,
    sha256,
)
from search_witness import EquationSystem


def components(
    edges: set[tuple[int, int]],
    n: int,
) -> list[list[int]]:
    unseen = set(range(n))
    output: list[list[int]] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component: set[int] = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(
                other
                for edge in edges
                if vertex in edge
                for other in edge
                if other != vertex and other not in component
            )
        unseen -= component
        output.append(sorted(component))
    return sorted(output)


def hard_models(family: dict[str, object]) -> list[Path]:
    rows: list[tuple[int, Path]] = []
    for skeleton_type in family["types"]:
        for factor_type in skeleton_type["factor_types"]:
            if factor_type["full_factor_cycle_type"] != [4, 4]:
                continue
            for orbit in factor_type["orbits"]:
                if not bool(orbit["binomial_free"]):
                    raise AssertionError(
                        "a full-C4+C4 orbit is not binomial-free"
                    )
                rows.append(
                    (
                        int(orbit["global_orbit_index"]),
                        Path(orbit["model"]),
                    )
                )
    rows.sort()
    if len(rows) != 23:
        raise AssertionError(f"expected 23 hard orbits, got {len(rows)}")
    return [path for _index, path in rows]


def analyze_model(
    system: EquationSystem,
    model: Path,
) -> dict[str, object]:
    selected = local_positive_to_flat(
        system,
        sorted(positive_model_literals(model)),
        center_degree=1,
    )
    full_edges = {
        edge
        for edge in system.edges
        if sum(
            (
                system.d**2 * system.edge_index[edge] + offset
            )
            in selected
            for offset in range(system.d**2)
        )
        == system.d**2
    }
    full_components = components(full_edges, system.n)
    if sorted(map(len, full_components)) != [4, 4]:
        raise AssertionError("model full blocks are not C4+C4")

    activities, monomials = active_matching_data(system, selected)
    qualified = {
        equation
        for equation, activity in enumerate(activities)
        if len(activity) == 4
        and all(
            all(edge in full_edges for edge in system.matchings[matching])
            for matching in activity
        )
    }
    restricted_activities = [
        activity if equation in qualified else []
        for equation, activity in enumerate(activities)
    ]
    restricted_monomials = [
        vectors if equation in qualified else []
        for equation, vectors in enumerate(monomials)
    ]
    clauses, relations, _origins = factor_relations(
        system,
        restricted_activities,
        restricted_monomials,
    )

    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        solver.set_phases(
            [-(index + 1) for index in range(len(relations))]
        )
        if not solver.solve():
            raise AssertionError("full-only factor clauses are UNSAT")
        raw_model = set(solver.get_model())
    selected_ids = [
        index
        for index in range(len(relations))
        if index + 1 in raw_model
    ]
    if exact_lattice_conflict(
        system,
        selected_ids,
        relations,
        restricted_activities,
        restricted_monomials,
    ) is not None:
        raise AssertionError("restricted factor branch is inconsistent")

    conflict = exact_lattice_conflict(
        system,
        selected_ids,
        relations,
        activities,
        monomials,
    )
    result: dict[str, object] = {
        "model": str(model),
        "model_sha256": sha256(model),
        "selected_entries": len(selected),
        "full_edges": [list(edge) for edge in sorted(full_edges)],
        "full_components": full_components,
        "full_only_factor_equations": len(qualified),
        "factor_clauses": len(clauses),
        "factor_relations": len(relations),
        "selected_relations": len(selected_ids),
        "restricted_branch_consistent": True,
    }
    if conflict is None:
        result["full_system_conflict"] = None
        return result

    equation = int(conflict["target_equation_index"])
    colouring = list(map(int, system.colourings[equation]))
    target_matchings = list(
        map(int, conflict["target_matching_indices"])
    )
    full_counts = [
        sum(edge in full_edges for edge in system.matchings[matching])
        for matching in target_matchings
    ]
    result["full_system_conflict"] = {
        "certificate_mode": conflict["certificate_mode"],
        "basis_relation_count": len(
            conflict["basis_relation_ids"]
        ),
        "target_equation_index": equation,
        "target_colouring": colouring,
        "component_colour_sets": [
            sorted({colouring[vertex] for vertex in component})
            for component in full_components
        ],
        "target_activity": len(target_matchings),
        "matching_full_edge_histogram": dict(
            sorted(Counter(full_counts).items())
        ),
        "nonzero_signed_class_coefficients": [
            int(row["signed_coefficient"])
            for row in conflict["signed_classes"]
            if int(row["signed_coefficient"]) != 0
        ],
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family",
        type=Path,
        default=Path(
            "tmp/eight_vertex_five_regular_full_singleton_family.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_full_cycle_factor_conflict_census.json"
        ),
    )
    args = parser.parse_args()
    family = json.loads(args.family.read_text(encoding="utf-8"))
    system = EquationSystem(8, 3)
    rows: list[dict[str, object]] = []
    for index, model in enumerate(hard_models(family)):
        row = analyze_model(system, model)
        rows.append(row)
        conflict = row["full_system_conflict"]
        print(
            f"orbit={index + 1}/23 "
            f"mode={None if conflict is None else conflict['certificate_mode']} "
            f"activity={None if conflict is None else conflict['target_activity']}",
            flush=True,
        )
    modes = Counter(
        (
            None
            if row["full_system_conflict"] is None
            else row["full_system_conflict"]["certificate_mode"]
        )
        for row in rows
    )
    payload = {
        "scope": (
            "exploratory first-branch full-cycle factor conflict census"
        ),
        "necessary_conditions_only": True,
        "family": str(args.family),
        "family_sha256": sha256(args.family),
        "orbits": len(rows),
        "conflict_modes": dict(modes),
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({key: payload[key] for key in payload if key != "rows"}))


if __name__ == "__main__":
    main()
