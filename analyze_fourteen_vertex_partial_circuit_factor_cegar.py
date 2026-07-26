"""CEGAR over all disjunctive relations forced by partial minimal circuits."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Sequence

from pysat.solvers import Solver

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_full_only_cycle_cover_cegar import (
    odd_kernel_conflict,
)
from analyze_fourteen_vertex_partial_circuit_amplitude_lattice import (
    active_ids,
    hamming_ball,
    monomial_vector,
    parse_relation_variable,
)
from analyze_fourteen_vertex_partial_minimal_circuit_lattice import (
    full_cycle_relation,
    is_port_exception,
    minimal_feasible_subsets,
)
from analyze_fourteen_vertex_portal_determinant_lattice import (
    Factor,
    contiguous_cycles,
    cycle_edges,
    edge,
    proper_colourings,
)
from integer_signed_lattice import IntegerSignedLattice


SymbolicVector = tuple[tuple[str, int], ...]
SparseVector = tuple[tuple[int, int], ...]


def partial_relation_clauses(
    factors: Sequence[Factor],
    cycles: Sequence[Sequence[int]],
) -> tuple[
    list[tuple[int, ...]],
    list[SymbolicVector],
    list[list[dict[str, object]]],
]:
    relation_index: dict[SymbolicVector, int] = {}
    relations: list[SymbolicVector] = []
    origins: list[list[dict[str, object]]] = []
    clauses: set[tuple[int, ...]] = set()
    for colour in range(3):
        other = [item for item in range(3) if item != colour]
        bases = proper_colourings(
            factors[other[0]],
            factors[other[1]],
            other[0],
            other[1],
        )
        for chosen in minimal_feasible_subsets(
            factors[colour], cycles
        ):
            endpoints = {vertex for item in chosen for vertex in item}
            touched = tuple(
                cycle_id
                for cycle_id, cycle in enumerate(cycles)
                if set(cycle) & endpoints
            )
            untouched = tuple(
                cycle_id
                for cycle_id in range(len(cycles))
                if cycle_id not in touched
            )
            if not untouched or is_port_exception(
                chosen, cycles, touched
            ):
                continue
            for base_id, base in enumerate(bases):
                target = list(base)
                for vertex in endpoints:
                    target[vertex] = colour
                relation_ids = []
                for forced_cycle in untouched:
                    vector = full_cycle_relation(
                        cycles[forced_cycle], target
                    )
                    origin = {
                        "colour": colour,
                        "minimal_subset": [
                            list(item) for item in chosen
                        ],
                        "touched_cycles": list(touched),
                        "untouched_cycles": list(untouched),
                        "candidate_forced_cycle": forced_cycle,
                        "base_colouring_id": base_id,
                        "base_colouring": list(base),
                        "target_colouring": target,
                    }
                    if vector not in relation_index:
                        relation_index[vector] = len(relations)
                        relations.append(vector)
                        origins.append([])
                    relation_id = relation_index[vector]
                    origins[relation_id].append(origin)
                    relation_ids.append(relation_id)
                clauses.add(tuple(sorted(set(relation_ids))))
    if any(not clause for clause in clauses):
        raise AssertionError("empty partial relation clause")
    return sorted(clauses), relations, origins


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial_analysis", type=Path)
    parser.add_argument("--max-rounds", type=int, default=10000)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    partial = json.loads(
        args.partial_analysis.read_text(encoding="utf-8")
    )
    partition = tuple(map(int, partial["partition"]))
    cycles = contiguous_cycles(partition)
    factors = tuple(
        tuple(tuple(map(int, item)) for item in factor)
        for factor in partial["singleton_factors"]
    )
    clauses, symbolic_relations, origins = partial_relation_clauses(
        factors, cycles
    )
    variables = sorted(
        {
            variable
            for relation in symbolic_relations
            for variable, _coefficient in relation
        }
    )
    positions = {
        variable: index for index, variable in enumerate(variables)
    }
    relations: list[SparseVector] = [
        tuple(
            (positions[variable], coefficient)
            for variable, coefficient in relation
        )
        for relation in symbolic_relations
    ]
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    matchings = engine.perfect_matchings(
        set(engine.FULL_EDGES) | set(labels)
    )
    support_variables = sorted(
        {
            9 * engine.EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
            for item in engine.FULL_EDGES
            for first_colour in range(3)
            for second_colour in range(3)
        }
        | {
            9 * engine.EDGE_INDEX[item] + 4 * colour
            for item, colour in labels.items()
        }
    )
    variable_positions = {
        variable: position
        for position, variable in enumerate(support_variables)
    }
    relation_rows = []
    for relation in symbolic_relations:
        row = [0] * len(support_variables)
        for raw_variable, coefficient in relation:
            variable = parse_relation_variable(raw_variable)
            row[variable_positions[variable]] = int(coefficient)
        relation_rows.append(row)
    dimacs = [
        tuple(relation_id + 1 for relation_id in clause)
        for clause in clauses
    ]
    learned = []
    status = "round_limit"
    surviving_selection = None
    last_integer_lattice_rank = None
    last_integer_lattice_invariant_factors = None
    last_candidate_colourings = 0
    last_amplitudes_tested = 0
    last_maximum_activity = 0
    with Solver(name="cadical195", bootstrap_with=dimacs) as solver:
        for _round in range(args.max_rounds):
            if not solver.solve():
                status = "partial_relation_factor_cnf_unsat"
                break
            model = solver.get_model() or []
            selected = sorted(
                literal - 1
                for literal in model
                if 1 <= literal <= len(relations)
            )
            conflict = odd_kernel_conflict(
                selected, relations, len(variables)
            )
            if conflict is not None:
                support = sorted(
                    set(
                        map(
                            int,
                            conflict["conflict_relation_ids"],
                        )
                    )
                )
                block = tuple(
                    -(relation_id + 1) for relation_id in support
                )
                solver.add_clause(block)
                learned.append(
                    {
                        "mode": "odd_signed_dependency",
                        "selected_relation_ids": selected,
                        "conflict_relation_ids": support,
                        "dependency_coefficients": conflict[
                            "dependency_coefficients"
                        ],
                        "coefficient_sum": conflict["coefficient_sum"],
                        "blocking_clause": list(block),
                    }
                )
                continue

            selected_rows = [
                relation_rows[index] for index in selected
            ]
            relation_positions = [
                position
                for position in range(len(support_variables))
                if any(row[position] for row in selected_rows)
            ]
            relation_position_set = set(relation_positions)
            lattice = IntegerSignedLattice(
                [
                    [row[position] for position in relation_positions]
                    for row in selected_rows
                ]
            )
            if lattice.has_odd_kernel:
                raise AssertionError(
                    "Smith lattice found an odd kernel missed by the "
                    "explicit dependency check"
                )
            basis_ids = selected
            last_integer_lattice_rank = lattice.rank
            last_integer_lattice_invariant_factors = list(
                lattice.invariant_factors
            )
            centres = [
                origin["target_colouring"]
                for relation_id in selected
                for origin in origins[relation_id]
            ]
            candidates = hamming_ball(centres, args.radius)
            last_candidate_colourings = len(candidates)
            last_amplitudes_tested = 0
            last_maximum_activity = 0
            monochromatic = {
                tuple([colour] * engine.N) for colour in range(3)
            }
            amplitude_conflict = None
            for colouring in candidates:
                activity = active_ids(matchings, colouring, labels)
                required = colouring in monochromatic
                if not activity and not required:
                    continue
                last_amplitudes_tested += 1
                last_maximum_activity = max(
                    last_maximum_activity, len(activity)
                )
                groups: list[dict[str, object]] = []
                all_coordinates: list[list[int]] = []
                for matching_id in activity:
                    vector = monomial_vector(
                        matchings[matching_id],
                        colouring,
                        labels,
                        variable_positions,
                    )
                    placed = False
                    for group in groups:
                        difference = [
                            left - right
                            for left, right in zip(
                                vector,
                                group["representative"],
                                strict=True,
                            )
                        ]
                        if any(
                            value
                            for position, value in enumerate(difference)
                            if position not in relation_position_set
                        ):
                            coordinates = None
                        else:
                            coordinates = lattice.coordinates(
                                [
                                    difference[position]
                                    for position in relation_positions
                                ]
                            )
                        if coordinates is None:
                            continue
                        sign = (
                            -1 if sum(coordinates) % 2 else 1
                        )
                        group["coefficient"] = (
                            int(group["coefficient"]) + sign
                        )
                        group["members"].append(
                            {
                                "matching_id": matching_id,
                                "sign": sign,
                                "coordinates": coordinates,
                            }
                        )
                        all_coordinates.append(coordinates)
                        placed = True
                        break
                    if placed:
                        continue
                    zero = [0] * len(basis_ids)
                    groups.append(
                        {
                            "representative": vector,
                            "coefficient": 1,
                            "members": [
                                {
                                    "matching_id": matching_id,
                                    "sign": 1,
                                    "coordinates": zero,
                                }
                            ],
                        }
                    )
                    all_coordinates.append(zero)
                nonzero = [
                    group
                    for group in groups
                    if int(group["coefficient"])
                ]
                contradiction = (
                    required and not nonzero
                ) or (
                    not required and len(nonzero) == 1
                )
                if not contradiction:
                    continue
                used_positions = sorted(
                    {
                        position
                        for coordinates in all_coordinates
                        for position, coefficient in enumerate(
                            coordinates
                        )
                        if coefficient
                    }
                )
                used_ids = [
                    basis_ids[position] for position in used_positions
                ]
                amplitude_conflict = {
                    "mode": (
                        "annihilated_required_amplitude"
                        if required
                        else "isolated_partial_relation_class"
                    ),
                    "selected_relation_ids": selected,
                    "basis_relation_ids": basis_ids,
                    "used_relation_ids": used_ids,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "signed_classes": [
                        {
                            "coefficient": int(
                                group["coefficient"]
                            ),
                            "members": group["members"],
                        }
                        for group in groups
                    ],
                }
                break
            if amplitude_conflict is None:
                status = "integer_lattice_amplitude_survivor"
                surviving_selection = selected
                break
            used = amplitude_conflict["used_relation_ids"]
            if not used:
                solver.add_clause([])
                block = ()
            else:
                block = tuple(
                    -(relation_id + 1) for relation_id in used
                )
                solver.add_clause(block)
            amplitude_conflict["blocking_clause"] = list(block)
            learned.append(amplitude_conflict)
    payload = {
        "status": status,
        "necessary_conditions_only": (
            status != "partial_relation_factor_cnf_unsat"
        ),
        "scope": (
            "all partial positive-minimal singleton circuits of one "
            "support, all proper base colourings, exact untouched-cycle "
            "relation clauses, and exact odd signed dependencies"
        ),
        "partial_analysis": str(args.partial_analysis),
        "partition": list(partition),
        "orbit": int(partial["orbit"]),
        "singleton_factors": partial["singleton_factors"],
        "minimal_relation_clauses": len(clauses),
        "unit_clauses": sum(len(clause) == 1 for clause in clauses),
        "binary_clauses": sum(len(clause) == 2 for clause in clauses),
        "larger_clauses": sum(len(clause) > 2 for clause in clauses),
        "distinct_relations": len(relations),
        "relation_variables": len(variables),
        "relation_vectors": [
            [[variable, coefficient] for variable, coefficient in relation]
            for relation in symbolic_relations
        ],
        "relation_origins": origins,
        "clauses": [list(clause) for clause in clauses],
        "odd_dependency_blocks": len(learned),
        "signed_dependency_blocks": sum(
            row["mode"] == "odd_signed_dependency"
            for row in learned
        ),
        "amplitude_lattice_blocks": sum(
            row["mode"] != "odd_signed_dependency"
            for row in learned
        ),
        "hamming_radius": args.radius,
        "skeleton_perfect_matchings": len(matchings),
        "last_integer_lattice_rank": last_integer_lattice_rank,
        "last_integer_lattice_invariant_factors": (
            last_integer_lattice_invariant_factors
        ),
        "last_candidate_colourings": last_candidate_colourings,
        "last_amplitudes_tested": last_amplitudes_tested,
        "last_maximum_activity": last_maximum_activity,
        "learned_conflicts": learned,
        "surviving_relation_selection": surviving_selection,
        "support_closed": status == "partial_relation_factor_cnf_unsat",
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: value
                for key, value in payload.items()
                if key
                not in {
                    "singleton_factors",
                    "relation_vectors",
                    "relation_origins",
                    "clauses",
                    "learned_conflicts",
                    "surviving_relation_selection",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
