"""Probe mandatory binomial lattices in one n=10 C10 equality orbit."""

from __future__ import annotations

import argparse
import itertools
import json
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

from explore_random_even_cycle_forks import colouring_table, perfect_matchings
from signed_binomial_lattice import _basis_data

Edge = tuple[int, int]
Entry = tuple[Edge, int, int]


def canonical(values: tuple[int, ...]) -> tuple[int, ...]:
    negative = tuple(-value for value in values)
    return min(values, negative)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbits",
        type=Path,
        default=Path("tmp/ten_vertex_c10_equality_support_orbits.json"),
    )
    parser.add_argument("--orbit", type=int, default=0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/ten_vertex_c10_lattice_probe.json"),
    )
    args = parser.parse_args()
    source = json.loads(args.orbits.read_text(encoding="utf-8"))
    orbit = source["rows"][args.orbit]
    full_edges = {
        tuple(map(int, item)) for item in source["full_edges"]
    }
    singleton_matchings = [
        [tuple(map(int, item)) for item in matching]
        for matching in orbit["singleton_matchings"]
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    skeleton = full_edges | set(labels)
    matchings = perfect_matchings(10, skeleton)
    entries: list[Entry] = [
        (item, labels[item], labels[item]) for item in sorted(labels)
    ]
    entries.extend(
        (item, first_colour, second_colour)
        for item in sorted(full_edges)
        for first_colour in range(3)
        for second_colour in range(3)
    )
    positions = {entry: index for index, entry in enumerate(entries)}
    colourings = colouring_table(10)
    activities: list[list[int]] = []
    sparse_monomials: list[list[tuple[int, ...]]] = []
    relation_index: dict[tuple[int, ...], int] = {}
    relations: list[tuple[int, ...]] = []
    origins: list[dict[str, object]] = []
    started = time.perf_counter()
    for equation, colouring in enumerate(colourings):
        activity: list[int] = []
        monomials: list[tuple[int, ...]] = []
        for matching_id, matching in enumerate(matchings):
            if not all(
                item in full_edges
                or (
                    colouring[item[0]]
                    == colouring[item[1]]
                    == labels[item]
                )
                for item in matching
            ):
                continue
            variables: list[int] = []
            for item in matching:
                if item in full_edges:
                    entry = (
                        item,
                        int(colouring[item[0]]),
                        int(colouring[item[1]]),
                    )
                else:
                    entry = (item, labels[item], labels[item])
                variables.append(positions[entry])
            activity.append(matching_id)
            monomials.append(tuple(sorted(variables)))
        activities.append(activity)
        sparse_monomials.append(monomials)
        if (
            len(set(map(int, colouring))) != 1
            and len(activity) == 2
        ):
            dense = [0] * len(entries)
            for variable in monomials[0]:
                dense[variable] += 1
            for variable in monomials[1]:
                dense[variable] -= 1
            relation = canonical(tuple(dense))
            if relation not in relation_index:
                relation_index[relation] = len(relations)
                relations.append(relation)
                origins.append(
                    {
                        "equation_index": equation,
                        "colouring": list(map(int, colouring)),
                        "matching_indices": activity,
                    }
                )
    for equation, monomials in enumerate(sparse_monomials):
        if (
            len(set(map(int, colourings[equation]))) == 1
            or len(monomials) != 3
        ):
            continue
        for first, second in itertools.combinations(range(3), 2):
            dense = [0] * len(entries)
            for variable in monomials[first]:
                dense[variable] += 1
            for variable in monomials[second]:
                dense[variable] -= 1
            relation = canonical(tuple(dense))
            if relation not in relation_index:
                continue
            relation_id = relation_index[relation]
            survivor = next(
                index for index in range(3) if index not in {first, second}
            )
            conflict = {
                "certificate_mode": (
                    "mandatory_binomial_pairs_two_terms_of_trinomial"
                ),
                "relation_id": relation_id,
                "relation_origin": origins[relation_id],
                "target_equation_index": equation,
                "target_colouring": list(
                    map(int, colourings[equation])
                ),
                "target_activity": activities[equation],
                "paired_matching_indices": [
                    activities[equation][first],
                    activities[equation][second],
                ],
                "surviving_matching_index": activities[equation][survivor],
            }
            payload = {
                "status": "conflict",
                "scope": (
                    "one n=10 C10 equality-support direct "
                    "binomial/trinomial contradiction"
                ),
                "necessary_conditions_only": False,
                "orbit": args.orbit,
                "singleton_matchings": orbit["singleton_matchings"],
                "skeleton_perfect_matchings": len(matchings),
                "selected_entries": len(entries),
                "colourings": len(colourings),
                "distinct_binomial_relations": len(relations),
                "relation_lattice_rank": None,
                "conflict": conflict,
                "elapsed_seconds": time.perf_counter() - started,
            }
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(payload, indent=2) + "\n",
                encoding="utf-8",
            )
            print(
                json.dumps(
                    {
                        key: value
                        for key, value in payload.items()
                        if key not in {"conflict", "singleton_matchings"}
                    },
                    indent=2,
                )
            )
            print(json.dumps(conflict, indent=2))
            return
    basis_data = _basis_data([list(relation) for relation in relations])
    if basis_data is None:
        raise AssertionError("mandatory relation lattice is not unimodular")
    independent, pivots, raw_basis, raw_inverse = basis_data
    basis_ids = [int(index) for index in independent]
    basis = np.asarray(raw_basis.tolist(), dtype=np.int64)
    inverse = np.asarray(raw_inverse.tolist(), dtype=np.int64)
    pivot_array = np.asarray(pivots, dtype=np.int64)

    def reduce_sparse(
        sparse: tuple[int, ...],
    ) -> tuple[tuple[int, ...], tuple[int, ...]]:
        vector = np.zeros(len(entries), dtype=np.int64)
        for variable in sparse:
            vector[variable] += 1
        coordinate = vector[pivot_array] @ inverse
        residual = vector - coordinate @ basis
        return (
            tuple(map(int, coordinate)),
            tuple(map(int, residual)),
        )

    conflict: dict[str, object] | None = None
    for relation_id, relation in enumerate(relations):
        vector = np.asarray(relation, dtype=np.int64)
        coordinate = vector[pivot_array] @ inverse
        residual = vector - coordinate @ basis
        if not np.any(residual) and int(coordinate.sum()) % 2 == 0:
            conflict = {
                "certificate_mode": "inconsistent_binomial_sign",
                "target_relation_id": relation_id,
                "target_origin": origins[relation_id],
                "basis_relation_ids": basis_ids,
                "target_coordinates": list(map(int, coordinate)),
            }
            break
    if conflict is None:
        for equation, monomials in enumerate(sparse_monomials):
            if not monomials:
                continue
            classes: dict[
                tuple[int, ...], list[tuple[int, int, tuple[int, ...]]]
            ] = defaultdict(list)
            for matching, sparse in zip(
                activities[equation], monomials, strict=True
            ):
                coordinates, residual = reduce_sparse(sparse)
                sign = -1 if sum(coordinates) % 2 else 1
                classes[residual].append(
                    (int(matching), sign, coordinates)
                )
            coefficients = [
                sum(member[1] for member in members)
                for members in classes.values()
            ]
            nonzero = [coefficient for coefficient in coefficients if coefficient]
            target = len(set(map(int, colourings[equation]))) == 1
            if not target and len(nonzero) == 1:
                conflict = {
                    "certificate_mode": "isolated_binomial_lattice_class",
                    "basis_relation_ids": basis_ids,
                    "target_equation_index": equation,
                    "target_colouring": list(
                        map(int, colourings[equation])
                    ),
                    "target_activity": activities[equation],
                    "signed_class_coefficients": coefficients,
                    "nonzero_signed_coefficients": nonzero,
                }
                break
            if target and not nonzero:
                conflict = {
                    "certificate_mode": "annihilated_required_amplitude",
                    "basis_relation_ids": basis_ids,
                    "target_equation_index": equation,
                    "target_colouring": list(
                        map(int, colourings[equation])
                    ),
                    "target_activity": activities[equation],
                    "signed_class_coefficients": coefficients,
                    "nonzero_signed_coefficients": [],
                }
                break
    if (
        conflict is not None
        and conflict["certificate_mode"]
        in {
            "isolated_binomial_lattice_class",
            "annihilated_required_amplitude",
        }
    ):
        target_equation = int(conflict["target_equation_index"])

        def target_conflict(
            relation_ids: list[int],
        ) -> dict[str, object] | None:
            raw = _basis_data(
                [list(relations[index]) for index in relation_ids]
            )
            if raw is None:
                return None
            independent2, pivots2, basis2_raw, inverse2_raw = raw
            basis2_ids = [
                relation_ids[position] for position in independent2
            ]
            basis2 = np.asarray(
                basis2_raw.tolist(), dtype=np.int64
            )
            inverse2 = np.asarray(
                inverse2_raw.tolist(), dtype=np.int64
            )
            pivots2_array = np.asarray(pivots2, dtype=np.int64)
            classes2: dict[tuple[int, ...], int] = defaultdict(int)
            for sparse in sparse_monomials[target_equation]:
                vector2 = np.zeros(len(entries), dtype=np.int64)
                for variable in sparse:
                    vector2[variable] += 1
                coordinates2 = vector2[pivots2_array] @ inverse2
                residual2 = vector2 - coordinates2 @ basis2
                sign2 = -1 if int(coordinates2.sum()) % 2 else 1
                classes2[tuple(map(int, residual2))] += sign2
            coefficients2 = list(classes2.values())
            nonzero2 = [
                coefficient
                for coefficient in coefficients2
                if coefficient
            ]
            target2 = (
                len(set(map(int, colourings[target_equation]))) == 1
            )
            if (not target2 and len(nonzero2) == 1) or (
                target2 and not nonzero2
            ):
                return {
                    "basis_relation_ids": basis2_ids,
                    "signed_class_coefficients": coefficients2,
                    "nonzero_signed_coefficients": nonzero2,
                }
            return None

        core = list(map(int, conflict["basis_relation_ids"]))
        changed = True
        minimized: dict[str, object] | None = None
        while changed:
            changed = False
            for relation_id in list(core):
                trial = [
                    other for other in core if other != relation_id
                ]
                replay = target_conflict(trial)
                if replay is not None:
                    core = trial
                    minimized = replay
                    changed = True
        final_replay = target_conflict(core)
        if final_replay is None:
            raise AssertionError("C10 minimized core lost contradiction")
        conflict["original_basis_size"] = len(
            conflict["basis_relation_ids"]
        )
        conflict["basis_relation_ids"] = core
        conflict["minimized_basis_size"] = len(core)
        conflict["basis_relation_origins"] = [
            origins[index] for index in core
        ]
        conflict.update(final_replay)
    payload = {
        "status": "conflict" if conflict is not None else "survivor",
        "scope": "one n=10 C10 equality-support mandatory-binomial lattice",
        "necessary_conditions_only": conflict is None,
        "orbit": args.orbit,
        "singleton_matchings": orbit["singleton_matchings"],
        "skeleton_perfect_matchings": len(matchings),
        "selected_entries": len(entries),
        "colourings": len(colourings),
        "distinct_binomial_relations": len(relations),
        "relation_lattice_rank": len(basis_ids),
        "conflict": conflict,
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
                if key not in {"conflict", "singleton_matchings"}
            },
            indent=2,
        )
    )
    if conflict is not None:
        print(
            json.dumps(
                {
                    "mode": conflict["certificate_mode"],
                    "target_equation": conflict.get(
                        "target_equation_index"
                    ),
                    "target_activity": conflict.get("target_activity"),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()
