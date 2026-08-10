"""Test a generic order-14 equality survivor by exact signed lattices."""

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
import time
from pathlib import Path

import numpy as np

import analyze_fourteen_vertex_full_direct_motifs as engine
from krenn_gu.explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles
from krenn_gu.signed_binomial_lattice import _basis_data


def dense_signature(
    signature: tuple[tuple[int, int], ...],
    variable_positions: dict[int, int],
) -> list[int]:
    vector = [0] * len(variable_positions)
    for variable, coefficient in signature:
        vector[variable_positions[int(variable)]] = int(coefficient)
    return vector


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_survivor_"
            "signed_lattice.json"
        ),
    )
    args = parser.parse_args()
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = full_edges
    singleton_matchings = [
        tuple(engine.edge(*map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    support_variables = sorted(
        {
            9 * engine.EDGE_INDEX[item] + 3 * first_colour + second_colour
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
    matchings = engine.perfect_matchings(set(full_edges) | set(labels))
    started = time.perf_counter()
    counts, first, second, third, total_extensions = (
        engine.activity_arrays(matchings, labels)
    )
    monochromatic = np.array(
        [
            sum(
                colour * (3**vertex)
                for vertex in range(engine.N)
            )
            for colour in range(3)
        ],
        dtype=np.int64,
    )
    counts[monochromatic] = -1
    binomial = np.flatnonzero(counts == 2)
    trinomial = np.flatnonzero(counts == 3)
    relation_origins = engine.unique_relation_origins(
        binomial, first, second, matchings, labels
    )
    signatures = tuple(relation_origins)
    rows = [
        dense_signature(signature, variable_positions)
        for signature in signatures
    ]
    data = _basis_data(rows)
    certificate: dict[str, object] | None = None
    basis_records: list[dict[str, object]] = []
    lattice_status = "unimodular_basis_absent"
    target_signatures_scanned = 0
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

        def coordinates(
            signature: tuple[tuple[int, int], ...],
        ) -> tuple[int, ...] | None:
            vector = np.asarray(
                dense_signature(signature, variable_positions), dtype=object
            )
            coordinate = vector[pivot_array] @ inverse
            residual = vector - coordinate @ basis
            if any(int(value) for value in residual):
                return None
            return tuple(map(int, coordinate))

        # A dependent binomial relation with even coordinate parity asks
        # for ratio -1 while the chosen basis forces ratio +1.
        for relation_id, signature in enumerate(signatures):
            coordinate = coordinates(signature)
            if coordinate is None or sum(coordinate) % 2:
                continue
            certificate = {
                "certificate_mode": "inconsistent_binomial_sign",
                "target_relation_id": relation_id,
                "target_equation_index": int(
                    relation_origins[signature]
                ),
                "target_relation_signature": [
                    list(item) for item in signature
                ],
                "basis_coordinates": [
                    [position, coefficient]
                    for position, coefficient in enumerate(coordinate)
                    if coefficient
                ],
            }
            break

        # Otherwise look for a pair in a forbidden trinomial whose ratio
        # is -1 modulo a combination of basis binomials.  Those two terms
        # cancel and the third supported monomial survives.
        if certificate is None:
            id_arrays = (first, second, third)
            target_origins: dict[
                tuple[tuple[int, int], ...],
                tuple[int, int, int],
            ] = {}
            for left_position, right_position in itertools.combinations(
                range(3), 2
            ):
                found = engine.unique_relation_origins(
                    trinomial,
                    id_arrays[left_position],
                    id_arrays[right_position],
                    matchings,
                    labels,
                )
                for signature, equation in found.items():
                    target_origins.setdefault(
                        signature,
                        (
                            int(equation),
                            left_position,
                            right_position,
                        ),
                    )
            for signature, (
                equation,
                left_position,
                right_position,
            ) in target_origins.items():
                target_signatures_scanned += 1
                coordinate = coordinates(signature)
                if coordinate is None or sum(coordinate) % 2 == 0:
                    continue
                activity = [
                    int(first[equation]),
                    int(second[equation]),
                    int(third[equation]),
                ]
                paired = [
                    activity[left_position],
                    activity[right_position],
                ]
                survivor_id = next(
                    item for item in activity if item not in paired
                )
                certificate = {
                    "certificate_mode": (
                        "signed_lattice_trinomial_survivor"
                    ),
                    "target_equation_index": equation,
                    "target_colouring": list(
                        engine.indexed_colouring(equation)
                    ),
                    "target_activity": activity,
                    "target_paired_matchings": paired,
                    "target_surviving_matching": survivor_id,
                    "target_relation_signature": [
                        list(item) for item in signature
                    ],
                    "basis_coordinates": [
                        [position, coefficient]
                        for position, coefficient in enumerate(coordinate)
                        if coefficient
                    ],
                }
                break
        lattice_status = (
            "contradiction"
            if certificate is not None
            else "no_signed_lattice_trinomial_contradiction"
        )

    payload = {
        "status": lattice_status,
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": engine.EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "binomial_forbidden_colourings": len(binomial),
        "trinomial_forbidden_colourings": len(trinomial),
        "distinct_binomial_relations": len(signatures),
        "lattice_variable_dimension": len(variable_positions),
        "signed_lattice_rank": len(basis_records),
        "basis_relations": basis_records,
        "target_pair_signatures_scanned": target_signatures_scanned,
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
