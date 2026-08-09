"""Verify a three-amplitude fork in each hard n=8 equality-support orbit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from verify_unary_cycle_relation_family import (
    canonical_direction,
    hard_model_rows,
    reconstruct_activities,
    reconstruct_factors,
    selected_flat_indices,
    sha256,
)
from search_witness import EquationSystem


def equation_factor_pair(
    vectors: Sequence[tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...]] | None:
    if len(vectors) != 4:
        return None
    for first, second, opposite in ((1, 2, 3), (1, 3, 2), (2, 3, 1)):
        if all(
            vectors[0][coordinate] + vectors[opposite][coordinate]
            == vectors[first][coordinate] + vectors[second][coordinate]
            for coordinate in range(len(vectors[0]))
        ):
            return (
                canonical_direction(
                    left - right
                    for left, right in zip(
                        vectors[0], vectors[first], strict=True
                    )
                ),
                canonical_direction(
                    left - right
                    for left, right in zip(
                        vectors[0], vectors[second], strict=True
                    )
                ),
            )
    return None


def clause_records(
    system: EquationSystem,
    monomials: Sequence[Sequence[tuple[int, ...]]],
    relations: Sequence[tuple[int, ...]],
) -> list[dict[str, object]]:
    relation_ids = {
        relation: index for index, relation in enumerate(relations)
    }
    records: list[dict[str, object]] = []
    for equation, vectors in enumerate(monomials):
        if bool(system.target[equation]):
            continue
        pair = equation_factor_pair(vectors)
        if pair is None:
            continue
        ids = [relation_ids[direction] for direction in pair]
        records.append(
            {
                "equation_index": equation,
                "relation_ids": ids,
                "clause": [index + 1 for index in ids],
            }
        )
    return records


def unary_pair_partition(
    relation: Sequence[int],
    activity: Sequence[int],
    vectors: Sequence[tuple[int, ...]],
) -> dict[str, object]:
    pivot = next(
        index
        for index, coefficient in enumerate(relation)
        if abs(coefficient) == 1
    )
    pivot_sign = int(relation[pivot])
    classes: dict[tuple[int, ...], list[tuple[int, int]]] = {}
    for matching, vector in zip(activity, vectors, strict=True):
        coordinate = int(vector[pivot]) * pivot_sign
        residual = tuple(
            int(value - coordinate * direction)
            for value, direction in zip(vector, relation, strict=True)
        )
        sign = -1 if coordinate % 2 else 1
        classes.setdefault(residual, []).append((int(matching), sign))
    cancelling_pairs: list[list[int]] = []
    survivors: list[tuple[int, int]] = []
    for members in classes.values():
        coefficient = sum(sign for _matching, sign in members)
        if coefficient:
            survivors.extend(members)
        else:
            if len(members) != 2 or {sign for _matching, sign in members} != {
                -1,
                1,
            }:
                raise AssertionError("zero class is not one cancelling pair")
            cancelling_pairs.append(
                [members[0][0], members[1][0]]
            )
    if len(activity) != 5:
        raise AssertionError("unary target is not a five-term amplitude")
    if len(cancelling_pairs) != 2 or len(survivors) != 1:
        raise AssertionError("unary contradiction is not 2 pairs + survivor")
    return {
        "pivot": pivot,
        "cancelling_pairs": cancelling_pairs,
        "surviving_matching_index": survivors[0][0],
        "surviving_coefficient": survivors[0][1],
    }


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
        "--family-audit",
        type=Path,
        default=Path(
            "tmp/eight_vertex_five_regular_full_singleton_"
            "family_verified.json"
        ),
    )
    parser.add_argument(
        "--unary",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family.json"
        ),
    )
    parser.add_argument(
        "--semantic",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_three_amplitude_forks_verified.json"
        ),
    )
    args = parser.parse_args()
    family = json.loads(args.family.read_text(encoding="utf-8"))
    family_audit = json.loads(
        args.family_audit.read_text(encoding="utf-8")
    )
    unary = json.loads(args.unary.read_text(encoding="utf-8"))
    semantic = json.loads(args.semantic.read_text(encoding="utf-8"))
    if family_audit.get("verified") is not True:
        raise AssertionError("family orbit audit is not verified")
    if family_audit["family_manifest_sha256"] != sha256(args.family):
        raise AssertionError("family audit binds a different manifest")
    if semantic.get("verified") is not True:
        raise AssertionError("unary semantic replay is not verified")
    if semantic["producer_sha256"] != sha256(args.unary):
        raise AssertionError("semantic replay binds another unary producer")

    system = EquationSystem(8, 3)
    models = hard_model_rows(family)
    rows: list[dict[str, object]] = []
    for orbit_index, (orbit, source) in enumerate(
        zip(models, unary["rows"], strict=True)
    ):
        model = Path(orbit["model"])
        selected = selected_flat_indices(model, system.variable_count)
        activities, monomials = reconstruct_activities(system, selected)
        clauses, relations, _origins = reconstruct_factors(
            system, activities, monomials
        )
        records = clause_records(system, monomials, relations)
        if [record["clause"] for record in records] != [
            list(map(int, clause)) for clause in clauses
        ]:
            raise AssertionError("factor clause record reconstruction changed")
        certificates = {
            int(row["relation_id"]): row["certificate"]
            for row in source["unary_certificates"]
        }
        record = next(
            (
                item
                for item in records
                if all(
                    relation_id in certificates
                    for relation_id in item["relation_ids"]
                )
            ),
            None,
        )
        if record is None:
            raise AssertionError("orbit has no double-unary factor fork")
        base_equation = int(record["equation_index"])
        if len(activities[base_equation]) != 4:
            raise AssertionError("fork base is not four-term")
        alternatives: list[dict[str, object]] = []
        for relation_id in record["relation_ids"]:
            certificate = certificates[int(relation_id)]
            target = int(certificate["target_equation_index"])
            partition = unary_pair_partition(
                relations[int(relation_id)],
                activities[target],
                monomials[target],
            )
            if list(map(int, activities[target])) != list(
                map(int, certificate["target_matching_indices"])
            ):
                raise AssertionError("unary target activity changed")
            if bool(system.target[target]):
                raise AssertionError("unary target is not forbidden")
            alternatives.append(
                {
                    "relation_id": int(relation_id),
                    "target_equation_index": target,
                    "target_colouring": list(
                        map(int, system.colourings[target])
                    ),
                    "target_activity": list(
                        map(int, activities[target])
                    ),
                    **partition,
                }
            )
        rows.append(
            {
                "orbit_index": orbit_index,
                "global_orbit_index": int(orbit["global_orbit_index"]),
                "model": str(model),
                "model_sha256": sha256(model),
                "base_equation_index": base_equation,
                "base_colouring": list(
                    map(int, system.colourings[base_equation])
                ),
                "base_activity": list(
                    map(int, activities[base_equation])
                ),
                "factor_relation_ids": list(
                    map(int, record["relation_ids"])
                ),
                "alternatives": alternatives,
                "verified": True,
            }
        )
        print(
            f"orbit={orbit_index + 1}/23 "
            f"fork={record['relation_ids']} verified",
            flush=True,
        )

    payload = {
        "verified": True,
        "scope": (
            "direct three-amplitude factor forks in all 23 "
            "binomial-free C4+C4 n=8 equality-support orbits"
        ),
        "claim_scope": (
            "covers the 1086 labelled binomial-free supports through the "
            "independently audited orbit catalogue; not the global "
            "Krenn-Gu conjecture"
        ),
        "family": str(args.family),
        "family_sha256": sha256(args.family),
        "family_audit": str(args.family_audit),
        "family_audit_sha256": sha256(args.family_audit),
        "unary": str(args.unary),
        "unary_sha256": sha256(args.unary),
        "semantic": str(args.semantic),
        "semantic_sha256": sha256(args.semantic),
        "support_orbits": len(rows),
        "covered_labelled_supports": int(
            family_audit["binomial_free_labelled_supports"]
        ),
        "amplitudes_per_orbit": 3,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
