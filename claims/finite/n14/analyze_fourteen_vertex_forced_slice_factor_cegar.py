"""Exact factor-choice CEGAR on a forced all-even cycle slice.

For a skeleton whose full factor has three even cycles, the eight
full-only perfect matchings form a product of three binomials.  A previous
certificate may force one of those cycle binomials to vanish on a set of
local colour codes.  On that slice:

* a 10-term equation containing all eight full-only matchings forces the
  two remaining monomials to cancel, hence gives a signed Laurent
  relation;
* a 12-term equation containing all eight full-only matchings reduces to
  four monomials.  When their exponent vectors form a parallelogram, the
  reduced amplitude factors into two binomials and at least one of the two
  corresponding signed Laurent relations must hold.

The unit relations and two-way factor choices are sent to a SAT solver.
Each Boolean model is checked by exact integer signed-lattice reduction.
An inconsistent sign, or a higher odd-extra amplitude with one surviving
Laurent class, yields a blocking clause.  UNSAT after learned clauses is a
finite exact certificate for this support-local branch analysis.

This program is intentionally independent of the earlier exploratory
signed-lattice scout.  In particular it explicitly verifies that every
equation used for full-factor cancellation contains all eight full-only
matchings.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from pysat.solvers import Solver

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_even_cycle_double_pair_fork import (
    activity_arrays,
)
from analyze_fourteen_vertex_even_cycle_factor_fork import local_codes
from explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles
from signed_binomial_lattice import _basis_data, _coordinates


SparseRelation = tuple[tuple[int, int], ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sparse(counter: Counter[int]) -> SparseRelation:
    direct = tuple(
        sorted(
            (int(variable), int(coefficient))
            for variable, coefficient in counter.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient)
        for variable, coefficient in direct
    )
    return min(direct, negative)


def difference(
    first: Sequence[int], second: Sequence[int]
) -> SparseRelation:
    vector: Counter[int] = Counter(first)
    vector.subtract(second)
    return canonical_sparse(vector)


def dense_relation(
    relation: SparseRelation,
    positions: dict[int, int],
) -> list[int]:
    vector = [0] * len(positions)
    for variable, coefficient in relation:
        vector[positions[variable]] = coefficient
    return vector


def full_containing_indices(
    counts: np.ndarray,
    slots: Sequence[np.ndarray],
    full_only: frozenset[int],
    activity_size: int,
) -> np.ndarray:
    """Return activity-size equations containing every full-only matching."""
    indices = np.flatnonzero(counts == activity_size)
    if not len(indices):
        return indices
    bit_by_matching = np.zeros(
        max(
            max(full_only, default=0),
            max(
                (
                    int(slot.max())
                    for slot in slots[:activity_size]
                    if len(slot)
                ),
                default=0,
            ),
        )
        + 1,
        dtype=np.uint16,
    )
    for position, matching_id in enumerate(sorted(full_only)):
        bit_by_matching[matching_id] = 1 << position
    masks = np.zeros(len(indices), dtype=np.uint16)
    for slot in slots[:activity_size]:
        values = slot[indices]
        if np.any(values < 0):
            raise AssertionError("activity slot unexpectedly empty")
        masks |= bit_by_matching[values]
    expected = (1 << len(full_only)) - 1
    return indices[masks == expected]


def monomial_variables(
    matching: Sequence[tuple[int, int]],
    colouring: Sequence[int],
    labels: dict[tuple[int, int], int],
    full_edges: frozenset[tuple[int, int]],
) -> tuple[int, ...]:
    output = []
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        output.append(
            9 * engine.EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
        )
    return tuple(sorted(output))


def extras_at(
    equation: int,
    activity_size: int,
    slots: Sequence[np.ndarray],
    full_only: frozenset[int],
) -> tuple[int, ...]:
    activity = tuple(
        int(slots[position][equation])
        for position in range(activity_size)
    )
    extras = tuple(
        matching_id
        for matching_id in activity
        if matching_id not in full_only
    )
    expected = activity_size - len(full_only)
    if len(extras) != expected:
        raise AssertionError(
            "full-containing equation has the wrong extra count"
        )
    return extras


def parallelogram_directions(
    vectors: Sequence[tuple[int, ...]],
) -> tuple[SparseRelation, ...] | None:
    """Return nonzero factor directions for an exact four-point rectangle."""
    if len(vectors) != 4:
        raise ValueError("four monomial vectors are required")
    for first, second, opposite in (
        (1, 2, 3),
        (1, 3, 2),
        (2, 3, 1),
    ):
        if tuple(sorted(vectors[0] + vectors[opposite])) != tuple(
            sorted(vectors[first] + vectors[second])
        ):
            continue
        directions = tuple(
            relation
            for relation in (
                difference(vectors[0], vectors[first]),
                difference(vectors[0], vectors[second]),
            )
            if relation
        )
        return tuple(dict.fromkeys(directions))
    return None


def selected_lattice_conflict(
    selected_ids: Sequence[int],
    relations: Sequence[SparseRelation],
    relation_rows: Sequence[list[int]],
    variable_positions: dict[int, int],
    target_rows: Sequence[
        tuple[int, tuple[int, ...], tuple[tuple[int, ...], ...]]
    ],
) -> dict[str, object] | None:
    """Find one exact contradiction implied by selected signed relations."""
    rows = [relation_rows[index] for index in selected_ids]
    basis_data = _basis_data(rows)
    if basis_data is None:
        return None
    independent, pivots, basis, inverse = basis_data
    basis_ids = [
        int(selected_ids[position]) for position in independent
    ]

    for relation_id in selected_ids:
        coordinates = _coordinates(
            relation_rows[relation_id], pivots, basis, inverse
        )
        if coordinates is None or sum(coordinates) % 2:
            continue
        used_positions = [
            position
            for position, coefficient in enumerate(coordinates)
            if coefficient
        ]
        return {
            "certificate_mode": "inconsistent_factor_sign",
            "basis_relation_ids": [
                basis_ids[position] for position in used_positions
            ],
            "target_relation_id": int(relation_id),
            "target_coordinates": [
                int(coordinates[position]) for position in used_positions
            ],
        }

    for equation, matching_ids, raw_vectors in target_rows:
        groups: list[dict[str, object]] = []
        all_coordinates: list[list[int]] = []
        for matching_id, vector in zip(
            matching_ids, raw_vectors, strict=True
        ):
            placed = False
            for group in groups:
                signed: Counter[int] = Counter(vector)
                signed.subtract(group["representative_vector"])
                raw_difference = canonical_sparse(signed)
                difference_row = [0] * len(relation_rows[0])
                for variable, coefficient in raw_difference:
                    difference_row[
                        variable_positions[variable]
                    ] = coefficient
                coordinates = _coordinates(
                    difference_row, pivots, basis, inverse
                )
                if coordinates is None:
                    continue
                sign = -1 if sum(coordinates) % 2 else 1
                group["signed_coefficient"] = (
                    int(group["signed_coefficient"]) + sign
                )
                group["terms"].append(
                    {
                        "matching_id": int(matching_id),
                        "sign": sign,
                        "coordinates": list(map(int, coordinates)),
                    }
                )
                all_coordinates.append(
                    list(map(int, coordinates))
                )
                placed = True
                break
            if placed:
                continue
            groups.append(
                {
                    "representative_vector": vector,
                    "signed_coefficient": 1,
                    "terms": [
                        {
                            "matching_id": int(matching_id),
                            "sign": 1,
                            "coordinates": [0] * len(basis_ids),
                        }
                    ],
                }
            )
            all_coordinates.append([0] * len(basis_ids))

        nonzero = [
            group
            for group in groups
            if int(group["signed_coefficient"])
        ]
        if len(nonzero) != 1:
            continue
        used_basis_positions = {
            position
            for coordinates in all_coordinates
            for position, coefficient in enumerate(coordinates)
            if coefficient
        }
        used_basis_ids = [
            basis_ids[position]
            for position in sorted(used_basis_positions)
        ]
        return {
            "certificate_mode": "isolated_factor_lattice_class",
            "basis_relation_ids": used_basis_ids,
            "target_equation_index": int(equation),
            "target_matching_ids": list(map(int, matching_ids)),
            "signed_class_coefficients": [
                int(group["signed_coefficient"]) for group in groups
            ],
        }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("forced_cycle_analysis", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--forced-cycle-index", type=int, default=1)
    parser.add_argument("--maximum-activity", type=int, default=30)
    parser.add_argument(
        "--target-activities",
        default="13,15,21",
        help=(
            "comma-separated full-containing activity levels used for "
            "lattice survivor checks"
        ),
    )
    parser.add_argument("--max-models", type=int, default=0)
    parser.add_argument(
        "--solver",
        default="cadical195",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_forced_slice_factor_cegar.json"
        ),
    )
    args = parser.parse_args()

    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    forced_analysis = json.loads(
        args.forced_cycle_analysis.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    if len(cycles) != 3 or any(len(cycle) % 2 for cycle in cycles):
        raise ValueError("this analysis requires three even cycles")
    if not 0 <= args.forced_cycle_index < len(cycles):
        raise ValueError("invalid forced cycle index")
    forced_cycle = cycles[args.forced_cycle_index]
    forced_codes = set(
        map(
            int,
            forced_analysis["forced_local_codes_by_cycle"][
                args.forced_cycle_index
            ],
        )
    )
    if not forced_codes:
        raise ValueError("the selected cycle has no forced local codes")
    target_activities = tuple(
        sorted(
            {
                int(item)
                for item in args.target_activities.split(",")
                if item.strip()
            }
        )
    )
    if any(
        level <= 12 or level > args.maximum_activity
        for level in target_activities
    ):
        raise ValueError("target activities must lie in [13, maximum]")

    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = full_edges
    factors = [
        tuple(engine.edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    matchings = engine.perfect_matchings(set(full_edges) | set(labels))
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    baseline = 1 << len(cycles)
    if len(full_only) != baseline:
        raise AssertionError("full-only matching count changed")
    support_variables = sorted(
        {
            9 * engine.EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
            for item in full_edges
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

    started = time.perf_counter()
    counts, slots, total_extensions = activity_arrays(
        matchings, labels, args.maximum_activity
    )
    forced_array = np.array(sorted(forced_codes), dtype=np.int64)

    relation_index: dict[SparseRelation, int] = {}
    relations: list[SparseRelation] = []
    origins: list[dict[str, object]] = []
    clauses: set[tuple[int, ...]] = set()
    clause_origins: dict[tuple[int, ...], dict[str, object]] = {}

    def relation_id(
        relation: SparseRelation,
        origin: dict[str, object],
    ) -> int:
        if relation not in relation_index:
            relation_index[relation] = len(relations)
            relations.append(relation)
            origins.append(origin)
        return relation_index[relation]

    ten_indices = full_containing_indices(
        counts, slots, full_only, baseline + 2
    )
    ten_codes = local_codes(ten_indices, forced_cycle)
    ten_indices = ten_indices[np.isin(ten_codes, forced_array)]
    for equation_value in ten_indices:
        equation = int(equation_value)
        extras = extras_at(
            equation, baseline + 2, slots, full_only
        )
        colouring = engine.indexed_colouring(equation)
        vectors = tuple(
            monomial_variables(
                matchings[matching_id],
                colouring,
                labels,
                full_edges,
            )
            for matching_id in extras
        )
        relation = difference(vectors[0], vectors[1])
        if not relation:
            raise AssertionError(
                "a forced two-extra amplitude has identical monomials"
            )
        item_id = relation_id(
            relation,
            {
                "certificate_mode": "forced_two_extra_relation",
                "equation_index": equation,
                "matching_ids": list(extras),
            },
        )
        clause = (item_id + 1,)
        clauses.add(clause)
        clause_origins.setdefault(
            clause,
            {
                "certificate_mode": "forced_two_extra_relation",
                "equation_index": equation,
                "matching_ids": list(extras),
            },
        )

    twelve_indices = full_containing_indices(
        counts, slots, full_only, baseline + 4
    )
    twelve_codes = local_codes(twelve_indices, forced_cycle)
    twelve_indices = twelve_indices[
        np.isin(twelve_codes, forced_array)
    ]
    factor_equations = 0
    nonfactor_equations = 0
    literal_impossibility = None
    for equation_value in twelve_indices:
        equation = int(equation_value)
        extras = extras_at(
            equation, baseline + 4, slots, full_only
        )
        colouring = engine.indexed_colouring(equation)
        vectors = tuple(
            monomial_variables(
                matchings[matching_id],
                colouring,
                labels,
                full_edges,
            )
            for matching_id in extras
        )
        directions = parallelogram_directions(vectors)
        if directions is None:
            nonfactor_equations += 1
            continue
        factor_equations += 1
        if not directions:
            literal_impossibility = {
                "certificate_mode": (
                    "four_identical_nonzero_monomials"
                ),
                "equation_index": equation,
                "matching_ids": list(extras),
            }
            break
        ids = tuple(
            sorted(
                relation_id(
                    relation,
                    {
                        "certificate_mode": (
                            "four_extra_parallelogram_factor"
                        ),
                        "equation_index": equation,
                        "matching_ids": list(extras),
                    },
                )
                + 1
                for relation in directions
            )
        )
        clauses.add(ids)
        clause_origins.setdefault(
            ids,
            {
                "certificate_mode": (
                    "four_extra_parallelogram_factor"
                ),
                "equation_index": equation,
                "matching_ids": list(extras),
            },
        )

    relation_rows = [
        dense_relation(relation, variable_positions)
        for relation in relations
    ]

    target_rows = []
    target_level_counts: dict[int, int] = {}
    for level in target_activities:
        indices = full_containing_indices(
            counts, slots, full_only, level
        )
        codes = local_codes(indices, forced_cycle)
        indices = indices[np.isin(codes, forced_array)]
        target_level_counts[level] = len(indices)
        for equation_value in indices:
            equation = int(equation_value)
            extras = extras_at(
                equation, level, slots, full_only
            )
            colouring = engine.indexed_colouring(equation)
            vectors = tuple(
                monomial_variables(
                    matchings[matching_id],
                    colouring,
                    labels,
                    full_edges,
                )
                for matching_id in extras
            )
            target_rows.append((equation, extras, vectors))

    # Pin one full-only forcing equation for every local code used by the
    # forced-cycle premise.  These rows are redundant for the CEGAR solve
    # but make the whole certificate transferable and independently
    # replayable without rediscovering witnesses.
    base_indices = full_containing_indices(
        counts, slots, full_only, baseline
    )
    base_code_arrays = [
        local_codes(base_indices, cycle) for cycle in cycles
    ]
    forcing_mask = np.ones(len(base_indices), dtype=bool)
    conditional_code_rows = forced_analysis[
        "conditional_fork_local_codes_by_cycle"
    ]
    for cycle_id in range(len(cycles)):
        if cycle_id == args.forced_cycle_index:
            continue
        forcing_mask &= np.isin(
            base_code_arrays[cycle_id],
            np.array(
                sorted(map(int, conditional_code_rows[cycle_id])),
                dtype=np.int64,
            ),
        )
    forcing_base_equations: dict[int, int] = {}
    for position_value in np.flatnonzero(forcing_mask):
        position = int(position_value)
        code = int(
            base_code_arrays[args.forced_cycle_index][position]
        )
        if code in forced_codes:
            forcing_base_equations.setdefault(
                code, int(base_indices[position])
            )
    if set(forcing_base_equations) != forced_codes:
        raise AssertionError(
            "could not pin every forced local-code equation"
        )

    sorted_clauses = sorted(clauses, key=lambda row: (len(row), row))
    learned: list[list[int]] = []
    branches: list[dict[str, object]] = []
    terminal_status = "literal_contradiction"
    if literal_impossibility is None:
        terminal_status = "running"
        with Solver(
            name=args.solver, bootstrap_with=sorted_clauses
        ) as solver:
            solver.set_phases(
                [-(index + 1) for index in range(len(relations))]
            )
            while solver.solve():
                model = set(solver.get_model())
                selected_ids = [
                    index
                    for index in range(len(relations))
                    if index + 1 in model
                ]
                certificate = selected_lattice_conflict(
                    selected_ids,
                    relations,
                    relation_rows,
                    variable_positions,
                    target_rows,
                )
                if certificate is None:
                    terminal_status = "survivor"
                    branches.append(
                        {
                            "selected_relation_ids": selected_ids,
                            "certificate": None,
                        }
                    )
                    break
                blocking_ids = set(
                    map(int, certificate["basis_relation_ids"])
                )
                if certificate["certificate_mode"] == (
                    "inconsistent_factor_sign"
                ):
                    blocking_ids.add(
                        int(certificate["target_relation_id"])
                    )
                clause = [
                    -(index + 1) for index in sorted(blocking_ids)
                ]
                if not clause:
                    raise AssertionError(
                        "empty exact-lattice blocking clause"
                    )
                solver.add_clause(clause)
                learned.append(clause)
                branches.append(
                    {
                        "selected_relation_count": len(selected_ids),
                        "blocking_clause": clause,
                        "certificate": certificate,
                    }
                )
                print(
                    f"branch={len(branches)} "
                    f"selected={len(selected_ids)} "
                    f"rank={len(certificate['basis_relation_ids'])} "
                    f"mode={certificate['certificate_mode']}",
                    flush=True,
                )
                if args.max_models and len(branches) >= args.max_models:
                    terminal_status = "limit"
                    break
            else:
                terminal_status = "UNSAT"

    payload = {
        "status": terminal_status,
        "necessary_conditions_only": terminal_status
        not in {"UNSAT", "literal_contradiction"},
        "scope": (
            "fixed C4+C4+C6 support sample, forced middle-cycle "
            "local-code slice, exact 10/12-term factor choices"
        ),
        "exploration": str(args.exploration),
        "exploration_sha256": sha256(args.exploration),
        "forced_cycle_analysis": str(args.forced_cycle_analysis),
        "forced_cycle_analysis_sha256": sha256(
            args.forced_cycle_analysis
        ),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "forced_cycle": list(forced_cycle),
        "forced_local_codes": sorted(forced_codes),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": len(full_only),
        "matching_extensions_accumulated": total_extensions,
        "full_containing_forced_ten_term_equations": len(
            ten_indices
        ),
        "full_containing_forced_twelve_term_equations": len(
            twelve_indices
        ),
        "factorable_twelve_term_equations": factor_equations,
        "nonfactorable_twelve_term_equations": nonfactor_equations,
        "factor_relation_count": len(relations),
        "factor_clause_count": len(sorted_clauses),
        "unit_clause_count": sum(
            len(clause) == 1 for clause in sorted_clauses
        ),
        "binary_clause_count": sum(
            len(clause) == 2 for clause in sorted_clauses
        ),
        "target_activity_counts": target_level_counts,
        "target_rows": len(target_rows),
        "forcing_base_equations_by_local_code": {
            str(code): equation
            for code, equation in sorted(
                forcing_base_equations.items()
            )
        },
        "factor_relations": [
            {
                "relation_id": index,
                "signature": [list(item) for item in relation],
                "origin": origins[index],
            }
            for index, relation in enumerate(relations)
        ],
        "factor_clauses": [
            list(map(int, clause)) for clause in sorted_clauses
        ],
        "factor_clause_origins": [
            clause_origins[clause] for clause in sorted_clauses
        ],
        "learned_clauses": learned,
        "branches": branches,
        "literal_certificate": literal_impossibility,
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
                    "factor_relations",
                    "factor_clauses",
                    "factor_clause_origins",
                    "learned_clauses",
                    "branches",
                }
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
