"""Signed-lattice closure after a cycle relation is forced on a code slice."""

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
import itertools
import json
import math
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_even_cycle_double_pair_fork import (
    activity_arrays,
)
from analyze_fourteen_vertex_even_cycle_factor_fork import local_codes
from krenn_gu.explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles
def dense_signature(
    signature: tuple[tuple[int, int], ...],
    variable_positions: dict[int, int],
) -> list[int]:
    vector = [0] * len(variable_positions)
    for variable, coefficient in signature:
        vector[variable_positions[int(variable)]] = int(coefficient)
    return vector


def greedy_unimodular_basis_data(
    rows: list[list[int]],
):
    """Select original relations with a unit triangular pivot minor."""
    from sympy import Matrix

    independent: list[int] = []
    pivots: list[int] = []
    echelon: list[list[int]] = []
    for row_id, raw in enumerate(rows):
        vector = list(map(int, raw))
        for pivot, basis_row in zip(pivots, echelon, strict=True):
            coefficient = vector[pivot]
            if coefficient:
                vector = [
                    value - coefficient * basis_value
                    for value, basis_value in zip(
                        vector, basis_row, strict=True
                    )
                ]
        pivot = next(
            (
                position
                for position, value in enumerate(vector)
                if abs(value) == 1 and position not in pivots
            ),
            None,
        )
        if pivot is None:
            continue
        if vector[pivot] == -1:
            vector = [-value for value in vector]
        independent.append(row_id)
        pivots.append(pivot)
        echelon.append(vector)
    if not independent:
        return None
    basis = Matrix([rows[index] for index in independent])
    pivot_matrix = basis[:, pivots]
    determinant = int(pivot_matrix.det())
    if abs(determinant) != 1:
        raise AssertionError(
            f"greedy pivot minor is not unimodular: {determinant}"
        )
    inverse = pivot_matrix.inv()
    if any(value.q != 1 for value in inverse):
        raise AssertionError("unimodular inverse has denominators")
    return independent, pivots, basis, inverse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("forced_cycle_analysis", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--forced-cycle-index", type=int, default=1)
    parser.add_argument("--maximum-activity", type=int, default=30)
    parser.add_argument(
        "--candidates-per-level-code", type=int, default=10
    )
    parser.add_argument(
        "--maximum-relations",
        type=int,
        default=5_000,
        help=(
            "maximum distinct forced pair relations used to build the "
            "certificate lattice"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_forced_cycle_signed_lattice.json"
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
    if not 0 <= args.forced_cycle_index < len(cycles):
        raise ValueError("invalid forced cycle index")
    forced_cycle = cycles[args.forced_cycle_index]
    forced_code_rows = forced_analysis[
        "forced_local_codes_by_cycle"
    ]
    forced_codes = set(
        map(int, forced_code_rows[args.forced_cycle_index])
    )
    if not forced_codes:
        raise ValueError("forced analysis has an empty code slice")
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
    monochromatic = {
        sum(colour * (3**vertex) for vertex in range(engine.N))
        for colour in range(3)
    }

    def activity(equation: int, size: int) -> tuple[int, ...]:
        return tuple(
            int(slots[position][equation]) for position in range(size)
        )

    pair_indices = np.flatnonzero(counts == baseline + 2)
    pair_codes = local_codes(pair_indices, forced_cycle)
    pair_selector = np.isin(
        pair_codes,
        np.array(sorted(forced_codes), dtype=np.int64),
    )
    pair_indices = pair_indices[pair_selector]
    pair_codes = pair_codes[pair_selector]
    extra_first = np.full(engine.EQUATIONS, -1, dtype=np.int16)
    extra_second = np.full(engine.EQUATIONS, -1, dtype=np.int16)
    full_array = np.array(sorted(full_only), dtype=np.int16)
    for slot in slots[: baseline + 2]:
        values = slot[pair_indices]
        selected = ~np.isin(values, full_array)
        indices = pair_indices[selected]
        selected_values = values[selected]
        first_empty = extra_first[indices] == -1
        extra_first[indices[first_empty]] = selected_values[first_empty]
        extra_second[indices[~first_empty]] = selected_values[~first_empty]
    if np.any(extra_first[pair_indices] < 0) or np.any(
        extra_second[pair_indices] < 0
    ):
        raise AssertionError("could not extract every extra pair")
    all_relation_origins = engine.unique_relation_origins(
        pair_indices,
        extra_first,
        extra_second,
        matchings,
        labels,
    )
    relation_origins: dict[
        tuple[tuple[int, int], ...], int
    ] = {}
    quota = math.ceil(args.maximum_relations / len(forced_codes))
    relation_counts_by_code: dict[int, int] = defaultdict(int)
    for signature, equation in all_relation_origins.items():
        code = int(
            local_codes(
                np.array([equation], dtype=np.int64), forced_cycle
            )[0]
        )
        if relation_counts_by_code[code] >= quota:
            continue
        relation_origins[signature] = equation
        relation_counts_by_code[code] += 1
        if len(relation_origins) >= args.maximum_relations:
            break
    pair_origin_equations_scanned = len(pair_indices)

    signatures = tuple(relation_origins)
    print(
        "forced_pair_relations="
        f"{len(signatures)} scanned={pair_origin_equations_scanned}",
        flush=True,
    )
    rows = [
        dense_signature(signature, variable_positions)
        for signature in signatures
    ]
    data = greedy_unimodular_basis_data(rows)
    print(
        "unimodular_basis_rank="
        f"{0 if data is None else len(data[0])}",
        flush=True,
    )
    basis_records: list[dict[str, object]] = []
    certificate = None
    targets_tested = 0
    candidate_targets = 0
    lattice_status = "unimodular_basis_absent"
    if data is not None:
        independent, pivots, raw_basis, raw_inverse = data
        basis = np.asarray(raw_basis.tolist(), dtype=object)
        inverse = np.asarray(raw_inverse.tolist(), dtype=object)
        pivot_array = np.asarray(pivots, dtype=np.int64)
        basis_records = [
            {
                "signature": [
                    list(item) for item in signatures[index]
                ],
                "origin_equation_index": int(
                    relation_origins[signatures[index]]
                ),
            }
            for index in independent
        ]

        def reduce_vector(
            vector: list[int],
        ) -> tuple[tuple[int, ...], tuple[int, ...]]:
            dense = np.asarray(vector, dtype=object)
            coordinate = dense[pivot_array] @ inverse
            residual = dense - coordinate @ basis
            return (
                tuple(map(int, coordinate)),
                tuple(map(int, residual)),
            )

        # A dependent pair relation demanding -1 with even basis parity
        # is already inconsistent.
        for relation_id, row in enumerate(rows):
            coordinate, residual = reduce_vector(row)
            if any(residual) or sum(coordinate) % 2:
                continue
            certificate = {
                "certificate_mode": (
                    "forced_slice_inconsistent_pair_sign"
                ),
                "target_relation_id": relation_id,
                "target_equation_index": int(
                    relation_origins[signatures[relation_id]]
                ),
                "target_relation_signature": [
                    list(item) for item in signatures[relation_id]
                ],
                "basis_coordinates": [
                    [position, coefficient]
                    for position, coefficient in enumerate(coordinate)
                    if coefficient
                ],
            }
            break

        if certificate is None:
            candidates: dict[
                tuple[int, int], list[int]
            ] = defaultdict(list)
            all_indices = np.arange(engine.EQUATIONS, dtype=np.int64)
            all_codes = local_codes(all_indices, forced_cycle)
            for activity_size in range(
                baseline + 1, args.maximum_activity + 1
            ):
                level = np.flatnonzero(counts == activity_size)
                if not len(level):
                    continue
                level = level[
                    np.isin(
                        all_codes[level],
                        np.array(
                            sorted(forced_codes), dtype=np.int64
                        ),
                    )
                ]
                for code in np.unique(all_codes[level]):
                    positions = np.flatnonzero(
                        all_codes[level] == code
                    )
                    for position in positions[
                        : args.candidates_per_level_code
                    ]:
                        equation = int(level[int(position)])
                        if equation not in monochromatic:
                            candidates[
                                (activity_size, int(code))
                            ].append(equation)
            candidate_targets = sum(map(len, candidates.values()))
            for equations in candidates.values():
                for equation in equations:
                    targets_tested += 1
                    size = int(counts[equation])
                    ids = activity(equation, size)
                    extras = tuple(
                        matching_id
                        for matching_id in ids
                        if matching_id not in full_only
                    )
                    if not extras:
                        continue
                    colouring = engine.indexed_colouring(equation)
                    classes: dict[
                        tuple[int, ...], int
                    ] = defaultdict(int)
                    class_members: dict[
                        tuple[int, ...], list[tuple[int, int, list[int]]]
                    ] = defaultdict(list)
                    for matching_id in extras:
                        monomial = [0] * len(variable_positions)
                        for item in matchings[matching_id]:
                            if item in full_edges:
                                first_colour = colouring[item[0]]
                                second_colour = colouring[item[1]]
                            else:
                                first_colour = second_colour = labels[item]
                            variable = (
                                9 * engine.EDGE_INDEX[item]
                                + 3 * first_colour
                                + second_colour
                            )
                            monomial[variable_positions[variable]] += 1
                        coordinate, residual = reduce_vector(monomial)
                        sign = -1 if sum(coordinate) % 2 else 1
                        classes[residual] += sign
                        class_members[residual].append(
                            (
                                matching_id,
                                sign,
                                [
                                    value
                                    for pair in enumerate(coordinate)
                                    if pair[1]
                                    for value in pair
                                ],
                            )
                        )
                    nonzero = [
                        (residual, coefficient)
                        for residual, coefficient in classes.items()
                        if coefficient
                    ]
                    if len(nonzero) != 1:
                        continue
                    residual, coefficient = nonzero[0]
                    certificate = {
                        "certificate_mode": (
                            "forced_slice_signed_lattice_survivor"
                        ),
                        "target_equation_index": equation,
                        "target_colouring": list(colouring),
                        "target_activity": list(ids),
                        "target_extra_matchings": list(extras),
                        "nonzero_class_coefficient": coefficient,
                        "nonzero_class_members": [
                            {
                                "matching_id": matching_id,
                                "sign": sign,
                                "basis_coordinates_flat": coordinates,
                            }
                            for matching_id, sign, coordinates
                            in class_members[residual]
                        ],
                    }
                    break
                if certificate is not None:
                    break
        lattice_status = (
            "contradiction"
            if certificate is not None
            else "no_forced_slice_signed_lattice_contradiction"
        )

    payload = {
        "status": lattice_status,
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "forced_cycle_analysis": str(args.forced_cycle_analysis),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "forced_cycle": list(forced_cycle),
        "forced_local_codes": sorted(forced_codes),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "matching_extensions_accumulated": total_extensions,
        "pair_origin_equations": len(pair_indices),
        "pair_origin_equations_scanned": (
            pair_origin_equations_scanned
        ),
        "maximum_relations": args.maximum_relations,
        "distinct_forced_pair_relations": len(signatures),
        "lattice_variable_dimension": len(variable_positions),
        "signed_lattice_rank": len(basis_records),
        "basis_relations": basis_records,
        "maximum_activity_searched": args.maximum_activity,
        "candidates_per_level_code": (
            args.candidates_per_level_code
        ),
        "candidate_targets": candidate_targets,
        "targets_tested": targets_tested,
        "certificate": certificate,
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
                if key != "basis_relations"
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
