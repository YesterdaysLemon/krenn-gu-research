"""Reduce nearby amplitudes modulo mandatory partial-circuit relations."""

from __future__ import annotations

import argparse
import itertools
import json
import re
import time
from collections import Counter
from pathlib import Path
from typing import Sequence

from signed_binomial_lattice import _basis_data, _coordinates

import analyze_fourteen_vertex_full_direct_motifs as engine
from analyze_fourteen_vertex_portal_determinant_lattice import (
    contiguous_cycles,
    cycle_edges,
    edge,
)


VARIABLE = re.compile(
    r"^W:(?P<u>\d+)-(?P<v>\d+):a(?P<a>\d+):b(?P<b>\d+)$"
)


def parse_relation_variable(raw: str) -> int:
    match = VARIABLE.fullmatch(raw)
    if match is None:
        raise ValueError(f"unsupported relation variable {raw!r}")
    item = edge(int(match["u"]), int(match["v"]))
    return (
        9 * engine.EDGE_INDEX[item]
        + 3 * int(match["a"])
        + int(match["b"])
    )


def monomial_vector(
    matching: Sequence[tuple[int, int]],
    colouring: Sequence[int],
    labels: dict[tuple[int, int], int],
    variable_positions: dict[int, int],
) -> tuple[int, ...]:
    vector = [0] * len(variable_positions)
    for item in matching:
        if item in engine.FULL_EDGES:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        variable = (
            9 * engine.EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
        )
        vector[variable_positions[variable]] += 1
    return tuple(vector)


def active_ids(
    matchings: Sequence[Sequence[tuple[int, int]]],
    colouring: Sequence[int],
    labels: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item in engine.FULL_EDGES
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        )
    )


def hamming_ball(
    centres: Sequence[Sequence[int]], radius: int
) -> tuple[tuple[int, ...], ...]:
    output: set[tuple[int, ...]] = set()
    for raw in centres:
        centre = tuple(map(int, raw))
        output.add(centre)
        for distance in range(1, radius + 1):
            for vertices in itertools.combinations(
                range(engine.N), distance
            ):
                for replacements in itertools.product(
                    (0, 1), repeat=distance
                ):
                    candidate = list(centre)
                    changed = True
                    for vertex, bit in zip(
                        vertices, replacements, strict=True
                    ):
                        alternatives = [
                            colour
                            for colour in range(3)
                            if colour != centre[vertex]
                        ]
                        candidate[vertex] = alternatives[bit]
                        changed &= candidate[vertex] != centre[vertex]
                    if changed:
                        output.add(tuple(candidate))
    return tuple(sorted(output))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial_analysis", type=Path)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    analysis = json.loads(
        args.partial_analysis.read_text(encoding="utf-8")
    )
    if int(analysis["distinct_forced_relations"]) < 1:
        raise ValueError("partial analysis has no mandatory relations")
    partition = tuple(map(int, analysis["partition"]))
    cycles = contiguous_cycles(partition)
    engine.CYCLES = tuple(cycles)
    engine.FULL_EDGES = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    factors = [
        tuple(edge(*map(int, item)) for item in factor)
        for factor in analysis["singleton_factors"]
    ]
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
    for raw_relation in analysis["relation_vectors"]:
        row = [0] * len(support_variables)
        for raw_variable, raw_coefficient in raw_relation:
            variable = parse_relation_variable(str(raw_variable))
            row[variable_positions[variable]] = int(raw_coefficient)
        rows.append(row)
    basis_data = _basis_data(rows)
    if basis_data is None:
        raise AssertionError("mandatory relation lattice not unimodular")
    independent, pivots, basis, inverse = basis_data
    basis_relation_ids = list(map(int, independent))

    certificate = None
    for relation_id, row in enumerate(rows):
        coordinates = _coordinates(row, pivots, basis, inverse)
        if coordinates is None or sum(coordinates) % 2:
            continue
        certificate = {
            "certificate_mode": "inconsistent_mandatory_relation_sign",
            "target_relation_id": relation_id,
            "basis_relation_ids": basis_relation_ids,
            "target_coordinates": coordinates,
        }
        break

    centres = [
        origin["target_colouring"]
        for origin in analysis["relation_origins"]
    ]
    candidates = hamming_ball(centres, args.radius)
    monochromatic = {
        tuple([colour] * engine.N) for colour in range(3)
    }
    activity_histogram: Counter[int] = Counter()
    maximum_activity = 0
    amplitudes_tested = 0
    if certificate is None:
        for colouring in candidates:
            activity = active_ids(matchings, colouring, labels)
            size = len(activity)
            activity_histogram[size] += 1
            maximum_activity = max(maximum_activity, size)
            required = colouring in monochromatic
            if not required and size == 0:
                continue
            amplitudes_tested += 1
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
                    coordinates = _coordinates(
                        difference, pivots, basis, inverse
                    )
                    if coordinates is None:
                        continue
                    sign = -1 if sum(coordinates) % 2 else 1
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
                zero = [0] * len(basis_relation_ids)
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
                group for group in groups if int(group["coefficient"])
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
                    for position, coefficient in enumerate(coordinates)
                    if coefficient
                }
            )
            certificate = {
                "certificate_mode": (
                    "annihilated_required_amplitude"
                    if required
                    else "isolated_partial_circuit_lattice_class"
                ),
                "target_colouring": list(colouring),
                "target_matching_ids": list(activity),
                "basis_relation_ids": [
                    basis_relation_ids[position]
                    for position in used_positions
                ],
                "signed_classes": [
                    {
                        "coefficient": int(group["coefficient"]),
                        "members": group["members"],
                    }
                    for group in groups
                ],
            }
            break

    payload = {
        "status": (
            "contradiction"
            if certificate is not None
            else "no_nearby_partial_circuit_lattice_contradiction"
        ),
        "necessary_conditions_only": certificate is None,
        "partial_analysis": str(args.partial_analysis),
        "partition": list(partition),
        "orbit": int(analysis["orbit"]),
        "singleton_factors": analysis["singleton_factors"],
        "skeleton_perfect_matchings": len(matchings),
        "mandatory_relations": len(rows),
        "mandatory_lattice_rank": len(basis_relation_ids),
        "basis_relation_ids": basis_relation_ids,
        "hamming_radius": args.radius,
        "candidate_colourings": len(candidates),
        "amplitudes_tested": amplitudes_tested,
        "maximum_activity": maximum_activity,
        "activity_histogram": {
            str(key): value
            for key, value in sorted(activity_histogram.items())
        },
        "certificate": certificate,
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
                if key not in {"singleton_factors", "certificate"}
            },
            indent=2,
        )
    )
    if certificate is not None:
        print(json.dumps(certificate, indent=2))


if __name__ == "__main__":
    main()
