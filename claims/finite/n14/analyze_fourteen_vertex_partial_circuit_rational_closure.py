"""Close mandatory partial-circuit relations under rational binomials."""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Sequence

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_partial_circuit_amplitude_lattice import (
    active_ids,
    hamming_ball,
    monomial_vector,
    parse_relation_variable,
)
from analyze_fourteen_vertex_partial_circuit_factor_cegar import (
    partial_relation_clauses,
)
from analyze_fourteen_vertex_portal_determinant_lattice import (
    contiguous_cycles,
    cycle_edges,
    edge,
)
from integer_constant_lattice import IntegerConstantLattice


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def canonical_relation(
    row: Sequence[int], constant: Fraction
) -> tuple[tuple[int, ...], Fraction]:
    direct = tuple(map(int, row))
    negative = tuple(-value for value in direct)
    if negative < direct:
        return negative, 1 / constant
    return direct, constant


def compact_lattice(
    rows: Sequence[Sequence[int]], constants: Sequence[Fraction]
) -> tuple[IntegerConstantLattice, tuple[int, ...], set[int]]:
    positions = tuple(
        position
        for position in range(len(rows[0]))
        if any(row[position] for row in rows)
    )
    return (
        IntegerConstantLattice(
            [[row[position] for position in positions] for row in rows],
            constants,
        ),
        positions,
        set(positions),
    )


def transported(
    difference: Sequence[int],
    lattice: IntegerConstantLattice,
    positions: Sequence[int],
    position_set: set[int],
) -> tuple[Fraction, list[int]] | None:
    if any(
        value
        for position, value in enumerate(difference)
        if position not in position_set
    ):
        return None
    compact = [difference[position] for position in positions]
    coordinates = lattice.coordinates(compact)
    if coordinates is None:
        return None
    constant = lattice.transported_constant(compact)
    if constant is None:
        raise AssertionError("lattice member lost its constant")
    return constant, coordinates


def reduce_amplitude(
    activity: Sequence[int],
    colouring: Sequence[int],
    matchings: Sequence[Sequence[tuple[int, int]]],
    labels: dict[tuple[int, int], int],
    variable_positions: dict[int, int],
    lattice: IntegerConstantLattice,
    positions: Sequence[int],
    position_set: set[int],
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    for matching_id in activity:
        vector = monomial_vector(
            matchings[matching_id],
            colouring,
            labels,
            variable_positions,
        )
        for group in groups:
            difference = [
                left - right
                for left, right in zip(
                    vector, group["representative"], strict=True
                )
            ]
            result = transported(
                difference, lattice, positions, position_set
            )
            if result is None:
                continue
            constant, coordinates = result
            group["coefficient"] += constant
            group["members"].append(
                {
                    "matching_id": int(matching_id),
                    "multiplier": fraction_text(constant),
                    "coordinates": coordinates,
                }
            )
            break
        else:
            groups.append(
                {
                    "representative": list(vector),
                    "coefficient": Fraction(1),
                    "members": [
                        {
                            "matching_id": int(matching_id),
                            "multiplier": "1",
                            "coordinates": [0] * lattice.generators,
                        }
                    ],
                }
            )
    return [group for group in groups if group["coefficient"]]


def sparse(row: Sequence[int]) -> list[list[int]]:
    return [
        [position, int(coefficient)]
        for position, coefficient in enumerate(row)
        if coefficient
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial_analysis", type=Path)
    parser.add_argument("--radius", type=int, default=3)
    parser.add_argument("--max-rounds", type=int, default=20)
    parser.add_argument("--max-derived-per-round", type=int, default=500)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    partial = json.loads(
        args.partial_analysis.read_text(encoding="utf-8")
    )
    partition = tuple(map(int, partial["partition"]))
    cycles = contiguous_cycles(partition)
    factors = tuple(
        tuple(edge(*map(int, item)) for item in factor)
        for factor in partial["singleton_factors"]
    )
    clauses, symbolic_relations, origins = partial_relation_clauses(
        factors, cycles
    )
    if any(len(clause) != 1 for clause in clauses):
        raise ValueError(
            "rational closure currently requires mandatory unit relations"
        )
    selected_ids = sorted({clause[0] for clause in clauses})
    symbolic_relations = [
        symbolic_relations[index] for index in selected_ids
    ]
    origins = [origins[index] for index in selected_ids]

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
            9 * engine.EDGE_INDEX[item] + 3 * left + right
            for item in engine.FULL_EDGES
            for left in range(3)
            for right in range(3)
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
    rows = []
    for relation in symbolic_relations:
        row = [0] * len(support_variables)
        for raw_variable, raw_coefficient in relation:
            variable = parse_relation_variable(raw_variable)
            row[variable_positions[variable]] = int(raw_coefficient)
        canonical, _constant = canonical_relation(
            row, Fraction(-1)
        )
        rows.append(canonical)
    constants = [Fraction(-1)] * len(rows)
    sources: list[dict[str, object]] = [
        {
            "mode": "mandatory_partial_cycle_relation",
            "original_relation_id": int(relation_id),
        }
        for relation_id in selected_ids
    ]
    relation_index = {row: index for index, row in enumerate(rows)}
    centres = [
        origin["target_colouring"]
        for relation_origins in origins
        for origin in relation_origins
    ]
    monochromatic = {
        tuple([colour] * engine.N) for colour in range(3)
    }
    candidates = sorted(
        set(hamming_ball(centres, args.radius)) | monochromatic
    )

    rounds = []
    status = "round_limit"
    contradiction = None
    for round_id in range(1, args.max_rounds + 1):
        lattice, positions, position_set = compact_lattice(
            rows, constants
        )
        if lattice.has_inconsistent_kernel:
            contradiction = {
                "mode": "inconsistent_rational_kernel",
                "round": round_id,
                "dependency_coefficients": list(
                    lattice.inconsistent_kernel_vector
                ),
            }
            status = "contradiction"
            break
        derived = []
        amplitudes_tested = 0
        maximum_activity = 0
        two_class_amplitudes = 0
        required_anchors = 0
        for colouring in candidates:
            activity = active_ids(matchings, colouring, labels)
            required = colouring in monochromatic
            if not activity and not required:
                continue
            amplitudes_tested += 1
            maximum_activity = max(maximum_activity, len(activity))
            groups = reduce_amplitude(
                activity,
                colouring,
                matchings,
                labels,
                variable_positions,
                lattice,
                positions,
                position_set,
            )
            if not required and len(groups) == 1:
                contradiction = {
                    "mode": "isolated_nonzero_rational_class",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "surviving_group": {
                        **groups[0],
                        "coefficient": fraction_text(
                            groups[0]["coefficient"]
                        ),
                    },
                }
                status = "contradiction"
                break
            candidate_row = None
            candidate_constant = None
            source = None
            if not required and len(groups) == 2:
                two_class_amplitudes += 1
                candidate_row = [
                    left - right
                    for left, right in zip(
                        groups[0]["representative"],
                        groups[1]["representative"],
                        strict=True,
                    )
                ]
                candidate_constant = (
                    -groups[1]["coefficient"]
                    / groups[0]["coefficient"]
                )
                source = {
                    "mode": "derived_forbidden_rational_binomial",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "group_coefficients": [
                        fraction_text(group["coefficient"])
                        for group in groups
                    ],
                }
            elif required and not groups:
                contradiction = {
                    "mode": "annihilated_required_amplitude",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                }
                status = "contradiction"
                break
            elif required and len(groups) == 1:
                required_anchors += 1
                candidate_row = list(groups[0]["representative"])
                candidate_constant = 1 / groups[0]["coefficient"]
                source = {
                    "mode": "derived_required_rational_anchor",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "group_coefficient": fraction_text(
                        groups[0]["coefficient"]
                    ),
                }
            if candidate_row is None:
                continue
            canonical, candidate_constant = canonical_relation(
                candidate_row, candidate_constant
            )
            if not any(canonical):
                if candidate_constant != 1:
                    contradiction = {
                        "mode": "derived_constant_conflict",
                        "round": round_id,
                        "constant": fraction_text(candidate_constant),
                        "source": source,
                    }
                    status = "contradiction"
                    break
                continue
            result = transported(
                canonical, lattice, positions, position_set
            )
            if result is not None:
                implied, coordinates = result
                if implied != candidate_constant:
                    contradiction = {
                        "mode": "inconsistent_derived_rational_binomial",
                        "round": round_id,
                        "derived_relation": sparse(canonical),
                        "derived_constant": fraction_text(
                            candidate_constant
                        ),
                        "implied_constant": fraction_text(implied),
                        "implied_coordinates": coordinates,
                        "source": source,
                    }
                    status = "contradiction"
                    break
                continue
            if canonical in relation_index:
                existing = relation_index[canonical]
                if constants[existing] != candidate_constant:
                    contradiction = {
                        "mode": "duplicate_rational_relation_conflict",
                        "round": round_id,
                        "existing_relation_id": existing,
                        "derived_constant": fraction_text(
                            candidate_constant
                        ),
                        "existing_constant": fraction_text(
                            constants[existing]
                        ),
                        "source": source,
                    }
                    status = "contradiction"
                    break
                continue
            derived.append((canonical, candidate_constant, source))
            if len(derived) >= args.max_derived_per_round:
                break
        round_record = {
            "round": round_id,
            "relation_count_before": len(rows),
            "integer_lattice_rank": lattice.rank,
            "candidate_colourings": len(candidates),
            "amplitudes_tested": amplitudes_tested,
            "maximum_activity": maximum_activity,
            "two_class_amplitudes": two_class_amplitudes,
            "required_rational_anchors": required_anchors,
            "new_relations": 0,
        }
        if contradiction is not None:
            rounds.append(round_record)
            break
        batch = {}
        unique = []
        for row, constant, source in derived:
            if row in batch:
                prior_constant, prior_source = batch[row]
                if prior_constant != constant:
                    contradiction = {
                        "mode": "same_round_rational_sign_conflict",
                        "round": round_id,
                        "derived_relation": sparse(row),
                        "first_constant": fraction_text(prior_constant),
                        "second_constant": fraction_text(constant),
                        "first_source": prior_source,
                        "second_source": source,
                    }
                    status = "contradiction"
                    break
                continue
            batch[row] = (constant, source)
            unique.append((row, constant, source))
        if contradiction is not None:
            rounds.append(round_record)
            break
        for row, constant, source in unique:
            if row in relation_index:
                continue
            relation_index[row] = len(rows)
            rows.append(row)
            constants.append(constant)
            sources.append(source)
        round_record["new_relations"] = len(unique)
        round_record["relation_count_after"] = len(rows)
        rounds.append(round_record)
        if not unique:
            status = "rational_binomial_closure_survivor"
            break

    support_closed = status == "contradiction"
    payload = {
        "status": status,
        "necessary_conditions_only": not support_closed,
        "scope": (
            "mandatory partial-cycle relations plus iterative exact "
            "rational two-coset forbidden amplitudes and exact rational "
            "monochromatic anchors"
        ),
        "partial_analysis": str(args.partial_analysis),
        "partition": list(partition),
        "orbit": int(partial["orbit"]),
        "singleton_factors": partial["singleton_factors"],
        "initial_relations": len(symbolic_relations),
        "final_relations": len(rows),
        "relation_vectors": [sparse(row) for row in rows],
        "relation_constants": [
            fraction_text(constant) for constant in constants
        ],
        "relation_sources": sources,
        "hamming_radius": args.radius,
        "candidate_colourings": len(candidates),
        "skeleton_perfect_matchings": len(matchings),
        "rounds": rounds,
        "contradiction": contradiction,
        "support_closed": support_closed,
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
                    "relation_constants",
                    "relation_sources",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
