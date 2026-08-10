"""Close partial-circuit relations under exact two-coset amplitudes."""

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
import time
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
from krenn_gu.integer_signed_lattice import IntegerSignedLattice


def canonical_row(row: Sequence[int]) -> tuple[int, ...]:
    direct = tuple(map(int, row))
    negative = tuple(-value for value in direct)
    return min(direct, negative)


def compact_lattice(
    rows: Sequence[Sequence[int]], sign_bits: Sequence[int]
) -> tuple[IntegerSignedLattice, tuple[int, ...], set[int]]:
    positions = tuple(
        position
        for position in range(len(rows[0]))
        if any(row[position] for row in rows)
    )
    lattice = IntegerSignedLattice(
        [[row[position] for position in positions] for row in rows],
        sign_bits,
    )
    return lattice, positions, set(positions)


def transport(
    difference: Sequence[int],
    lattice: IntegerSignedLattice,
    positions: Sequence[int],
    position_set: set[int],
    cache: dict[
        tuple[int, ...], tuple[int, tuple[int, ...]] | None
    ] | None = None,
) -> tuple[int, list[int]] | None:
    cache_key = tuple(map(int, difference))
    if cache is not None and cache_key in cache:
        cached = cache[cache_key]
        if cached is None:
            return None
        sign, coordinates = cached
        return sign, list(coordinates)
    if any(
        value
        for position, value in enumerate(difference)
        if position not in position_set
    ):
        if cache is not None:
            cache[cache_key] = None
        return None
    compact = [difference[position] for position in positions]
    coordinates = lattice.coordinates(compact)
    if coordinates is None:
        if cache is not None:
            cache[cache_key] = None
        return None
    if lattice.has_inconsistent_kernel:
        raise ValueError(
            "transported sign is ambiguous because the signed "
            "relation system has an inconsistent kernel dependency"
        )
    parity = sum(
        coefficient * bit
        for coefficient, bit in zip(
            coordinates, lattice.sign_bits, strict=True
        )
    )
    sign = -1 if parity % 2 else 1
    if cache is not None:
        cache[cache_key] = (sign, tuple(coordinates))
    return sign, coordinates


def reduce_amplitude(
    activity: Sequence[int],
    colouring: Sequence[int],
    matchings: Sequence[Sequence[tuple[int, int]]],
    labels: dict[tuple[int, int], int],
    variable_positions: dict[int, int],
    lattice: IntegerSignedLattice,
    positions: Sequence[int],
    position_set: set[int],
    transport_cache: dict[
        tuple[int, ...], tuple[int, tuple[int, ...]] | None
    ],
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
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
                    vector, group["representative"], strict=True
                )
            ]
            result = transport(
                difference,
                lattice,
                positions,
                position_set,
                transport_cache,
            )
            if result is None:
                continue
            sign, coordinates = result
            group["coefficient"] = int(group["coefficient"]) + sign
            group["members"].append(
                {
                    "matching_id": int(matching_id),
                    "sign": sign,
                    "coordinates": coordinates,
                }
            )
            placed = True
            break
        if not placed:
            groups.append(
                {
                    "representative": list(vector),
                    "coefficient": 1,
                    "members": [
                        {
                            "matching_id": int(matching_id),
                            "sign": 1,
                            "coordinates": [0] * lattice.generators,
                        }
                    ],
                }
            )
    return [
        group for group in groups if int(group["coefficient"]) != 0
    ]


def sparse(row: Sequence[int]) -> list[list[int]]:
    return [
        [position, int(coefficient)]
        for position, coefficient in enumerate(row)
        if coefficient
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial_analysis", type=Path)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--max-rounds", type=int, default=20)
    parser.add_argument("--max-derived-per-round", type=int, default=500)
    parser.add_argument("--select-all-relations", action="store_true")
    parser.add_argument(
        "--select-mandatory-unit-core",
        action="store_true",
        help=(
            "use only relations forced by unit clauses; a contradiction "
            "in this mode closes the support without a branch selector"
        ),
    )
    parser.add_argument(
        "--selected-relation-ids",
        help="comma-separated relation-selection branch",
    )
    parser.add_argument(
        "--candidate-colourings-file",
        type=Path,
        help=(
            "optional sound subset of the full Hamming census; every "
            "listed colouring is checked against the full census"
        ),
    )
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
    if sum(
        (
            bool(args.select_all_relations),
            bool(args.select_mandatory_unit_core),
            bool(args.selected_relation_ids),
        )
    ) > 1:
        raise ValueError("choose one relation-selection mode")
    if (
        any(len(clause) != 1 for clause in clauses)
        and not args.select_all_relations
        and not args.select_mandatory_unit_core
        and not args.selected_relation_ids
    ):
        raise ValueError(
            "nonunit relation clauses require --select-all-relations; "
            "that analyzes one relation-selection branch only"
        )
    if args.select_all_relations:
        selected_ids = list(range(len(symbolic_relations)))
    elif args.select_mandatory_unit_core:
        selected_ids = sorted(
            {clause[0] for clause in clauses if len(clause) == 1}
        )
        if not selected_ids:
            raise ValueError("relation system has no mandatory unit core")
    elif args.selected_relation_ids:
        selected_ids = sorted(
            set(map(int, args.selected_relation_ids.split(",")))
        )
        if any(
            not set(clause) & set(selected_ids) for clause in clauses
        ):
            raise ValueError(
                "selected relations do not satisfy every relation clause"
            )
    else:
        selected_ids = sorted({clause[0] for clause in clauses})
    unit_relation_ids = {
        clause[0] for clause in clauses if len(clause) == 1
    }
    all_selected_relations_are_mandatory = (
        set(selected_ids) <= unit_relation_ids
    )
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
    rows = []
    for relation in symbolic_relations:
        row = [0] * len(support_variables)
        for raw_variable, raw_coefficient in relation:
            variable = parse_relation_variable(raw_variable)
            row[variable_positions[variable]] = int(raw_coefficient)
        rows.append(canonical_row(row))
    sign_bits = [1] * len(rows)
    relation_sources: list[dict[str, object]] = [
        {
            "mode": "mandatory_partial_cycle_relation",
            "original_relation_id": int(relation_id),
        }
        for relation_id in selected_ids
    ]
    relation_index = {
        row: index for index, row in enumerate(rows)
    }
    centres = [
        origin["target_colouring"]
        for relation_origins in origins
        for origin in relation_origins
    ]
    monochromatic = {
        tuple([colour] * engine.N) for colour in range(3)
    }
    full_candidates = sorted(
        set(hamming_ball(centres, args.radius)) | monochromatic
    )
    if args.candidate_colourings_file is None:
        candidates = full_candidates
    else:
        raw_candidates = json.loads(
            args.candidate_colourings_file.read_text(encoding="utf-8")
        )
        if isinstance(raw_candidates, dict):
            raw_candidates = raw_candidates["colourings"]
        requested = {
            tuple(map(int, colouring)) for colouring in raw_candidates
        }
        if any(
            len(colouring) != engine.N
            or any(value not in range(3) for value in colouring)
            for colouring in requested
        ):
            raise ValueError("candidate colouring has the wrong domain")
        full_candidate_set = set(full_candidates)
        if not requested <= full_candidate_set:
            raise ValueError(
                "candidate-colouring subset left the full Hamming census"
            )
        candidates = sorted(requested | monochromatic)
    candidate_activities = [
        (
            colouring,
            active_ids(matchings, colouring, labels),
            colouring in monochromatic,
        )
        for colouring in candidates
    ]

    rounds = []
    status = "round_limit"
    contradiction = None
    for round_id in range(1, args.max_rounds + 1):
        lattice, positions, position_set = compact_lattice(
            rows, sign_bits
        )
        transport_cache: dict[
            tuple[int, ...], tuple[int, tuple[int, ...]] | None
        ] = {}
        if lattice.has_inconsistent_kernel:
            kernel = next(
                vector
                for vector in lattice.kernel_basis
                if sum(
                    coefficient * bit
                    for coefficient, bit in zip(
                        vector, lattice.sign_bits, strict=True
                    )
                )
                % 2
            )
            contradiction = {
                "mode": "inconsistent_signed_kernel",
                "dependency_coefficients": list(kernel),
                "relation_ids": [
                    index
                    for index, coefficient in enumerate(kernel)
                    if coefficient
                ],
            }
            status = "contradiction"
            break

        derived: list[
            tuple[tuple[int, ...], int, dict[str, object]]
        ] = []
        amplitudes_tested = 0
        maximum_activity = 0
        one_class_forbidden = 0
        two_class_amplitudes = 0
        two_class_equal_magnitude = 0
        required_anchors = 0
        for colouring, activity, required in candidate_activities:
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
                transport_cache,
            )
            if not required and len(groups) == 1:
                one_class_forbidden += 1
                contradiction = {
                    "mode": "isolated_nonzero_lattice_class",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "surviving_group": groups[0],
                }
                status = "contradiction"
                break
            candidate_row = None
            candidate_bit = None
            source = None
            if not required and len(groups) == 2:
                two_class_amplitudes += 1
            if (
                not required
                and len(groups) == 2
                and abs(int(groups[0]["coefficient"]))
                == abs(int(groups[1]["coefficient"]))
            ):
                two_class_equal_magnitude += 1
                candidate_row = [
                    left - right
                    for left, right in zip(
                        groups[0]["representative"],
                        groups[1]["representative"],
                        strict=True,
                    )
                ]
                ratio = (
                    -int(groups[1]["coefficient"])
                    // int(groups[0]["coefficient"])
                )
                if ratio not in (-1, 1):
                    raise AssertionError("equal magnitude ratio changed")
                candidate_bit = int(ratio == -1)
                source = {
                    "mode": "derived_forbidden_binomial_amplitude",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "group_coefficients": [
                        int(group["coefficient"]) for group in groups
                    ],
                }
            elif required and len(groups) == 0:
                contradiction = {
                    "mode": "annihilated_required_amplitude",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                }
                status = "contradiction"
                break
            elif (
                required
                and len(groups) == 1
                and abs(int(groups[0]["coefficient"])) == 1
            ):
                required_anchors += 1
                candidate_row = list(groups[0]["representative"])
                candidate_bit = int(
                    int(groups[0]["coefficient"]) == -1
                )
                source = {
                    "mode": "derived_required_unit_amplitude",
                    "round": round_id,
                    "target_colouring": list(colouring),
                    "target_matching_ids": list(activity),
                    "group_coefficient": int(
                        groups[0]["coefficient"]
                    ),
                }
            if candidate_row is None:
                continue
            canonical = canonical_row(candidate_row)
            result = transport(
                canonical,
                lattice,
                positions,
                position_set,
                transport_cache,
            )
            if result is not None:
                implied_sign, coordinates = result
                implied_bit = int(implied_sign == -1)
                if implied_bit != candidate_bit:
                    contradiction = {
                        "mode": "inconsistent_derived_binomial",
                        "round": round_id,
                        "target_colouring": list(colouring),
                        "derived_relation": sparse(canonical),
                        "derived_sign_bit": candidate_bit,
                        "implied_sign_bit": implied_bit,
                        "implied_coordinates": coordinates,
                        "source": source,
                    }
                    status = "contradiction"
                    break
                continue
            if canonical in relation_index:
                existing = relation_index[canonical]
                if sign_bits[existing] != candidate_bit:
                    contradiction = {
                        "mode": "duplicate_relation_sign_conflict",
                        "round": round_id,
                        "existing_relation_id": existing,
                        "derived_relation": sparse(canonical),
                        "derived_sign_bit": candidate_bit,
                        "existing_sign_bit": sign_bits[existing],
                        "source": source,
                    }
                    status = "contradiction"
                    break
                continue
            derived.append((canonical, candidate_bit, source))
            if len(derived) >= args.max_derived_per_round:
                break
        round_record = {
            "round": round_id,
            "relation_count_before": len(rows),
            "integer_lattice_rank": lattice.rank,
            "integer_lattice_invariant_factors": list(
                lattice.invariant_factors
            ),
            "candidate_colourings": len(candidates),
            "amplitudes_tested": amplitudes_tested,
            "maximum_activity": maximum_activity,
            "one_class_forbidden_amplitudes": one_class_forbidden,
            "two_class_amplitudes": two_class_amplitudes,
            "two_class_equal_magnitude_amplitudes": (
                two_class_equal_magnitude
            ),
            "required_unit_anchors": required_anchors,
            "new_relations": 0,
        }
        if contradiction is not None:
            rounds.append(round_record)
            break
        unique_derived = []
        batch: dict[
            tuple[int, ...], tuple[int, dict[str, object]]
        ] = {}
        for row, bit, source in derived:
            if row in batch:
                existing_bit, existing_source = batch[row]
                if existing_bit != bit:
                    contradiction = {
                        "mode": "same_round_derived_sign_conflict",
                        "round": round_id,
                        "derived_relation": sparse(row),
                        "first_sign_bit": existing_bit,
                        "second_sign_bit": bit,
                        "first_source": existing_source,
                        "second_source": source,
                    }
                    status = "contradiction"
                    break
                continue
            batch[row] = (bit, source)
            unique_derived.append((row, bit, source))
        if contradiction is not None:
            rounds.append(round_record)
            break
        for row, bit, source in unique_derived:
            if row in relation_index:
                continue
            relation_index[row] = len(rows)
            rows.append(row)
            sign_bits.append(bit)
            relation_sources.append(source)
        round_record["new_relations"] = len(unique_derived)
        round_record["relation_count_after"] = len(rows)
        rounds.append(round_record)
        if not unique_derived:
            status = "binomial_closure_survivor"
            break

    branch_closed = status == "contradiction"
    support_closed = (
        branch_closed and all_selected_relations_are_mandatory
    )
    if branch_closed and not support_closed:
        status = "relation_selection_branch_contradiction"
    payload = {
        "status": status,
        "necessary_conditions_only": not support_closed,
        "scope": (
            "mandatory partial-cycle relations plus iterative exact "
            "equal-magnitude two-coset forbidden amplitudes and exact "
            "unit monochromatic anchors"
        ),
        "partial_analysis": str(args.partial_analysis),
        "partition": list(partition),
        "orbit": int(partial["orbit"]),
        "singleton_factors": partial["singleton_factors"],
        "initial_relations": len(symbolic_relations),
        "selected_initial_relation_ids": selected_ids,
        "selected_all_relation_branch": bool(
            args.select_all_relations
        ),
        "selected_mandatory_unit_core": bool(
            args.select_mandatory_unit_core
        ),
        "final_relations": len(rows),
        "final_sign_bits": sign_bits,
        "relation_vectors": [sparse(row) for row in rows],
        "relation_sources": relation_sources,
        "hamming_radius": args.radius,
        "candidate_colourings": len(candidates),
        "full_candidate_colourings": len(full_candidates),
        "candidate_colourings_file": (
            str(args.candidate_colourings_file)
            if args.candidate_colourings_file is not None
            else None
        ),
        "skeleton_perfect_matchings": len(matchings),
        "rounds": rounds,
        "contradiction": contradiction,
        "relation_selection_branch_closed": branch_closed,
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
                    "final_sign_bits",
                    "relation_vectors",
                    "relation_sources",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
