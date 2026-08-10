"""Test whether unary cycle relations close all 23 hard equality orbits.

A selected Laurent factor relation spans a rank-one signed lattice.  This
script reduces every amplitude modulo that one relation directly.  If a
forbidden amplitude has exactly one nonzero signed class, or a required
amplitude has none, that relation is individually impossible and receives
a negative unit clause.

The resulting factor-choice CNFs are written for independent SAT/proof
replay.  This producer is exploratory until a separate semantic verifier
and raw proof replay are attached.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Sequence

from pysat.solvers import Solver

from analyze_full_cycle_factor_conflicts import hard_models
from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from eight_vertex_sparse_exact import positive_model_literals
from factor_lattice_cegar import (
    active_matching_data,
    factor_relations,
    sha256,
    write_dimacs,
)
from search_witness import EquationSystem


def unary_conflict(
    system: EquationSystem,
    relation: Sequence[int],
    activities: Sequence[Sequence[int]],
    monomials: Sequence[Sequence[tuple[int, ...]]],
) -> dict[str, object] | None:
    pivot = next(
        (
            index
            for index, coefficient in enumerate(relation)
            if coefficient
        ),
        None,
    )
    if pivot is None or abs(int(relation[pivot])) != 1:
        raise AssertionError("factor relation has no unit pivot")
    pivot_sign = int(relation[pivot])

    for equation, vectors in enumerate(monomials):
        if not vectors:
            continue
        target = bool(system.target[equation])
        # A rank-one relation cannot leave exactly one nonzero class from
        # an even number of unit-coefficient monomials, nor annihilate an
        # odd required amplitude.  This parity filter avoids most work.
        if (not target and len(vectors) % 2 == 0) or (
            target and len(vectors) % 2 == 1
        ):
            continue
        classes: dict[
            tuple[int, ...],
            list[tuple[int, int, int]],
        ] = {}
        for matching, vector in zip(
            activities[equation],
            vectors,
            strict=True,
        ):
            coordinate = int(vector[pivot]) * pivot_sign
            residual = tuple(
                int(value - coordinate * direction)
                for value, direction in zip(
                    vector,
                    relation,
                    strict=True,
                )
            )
            sign = -1 if coordinate % 2 else 1
            classes.setdefault(residual, []).append(
                (int(matching), sign, coordinate)
            )
        signed_classes = [
            {
                "signed_coefficient": sum(
                    sign for _matching, sign, _coordinate in members
                ),
                "members": [
                    {
                        "matching_index": matching,
                        "sign": sign,
                        "coordinate": coordinate,
                    }
                    for matching, sign, coordinate in members
                ],
            }
            for _residual, members in sorted(classes.items())
        ]
        nonzero = [
            row
            for row in signed_classes
            if int(row["signed_coefficient"]) != 0
        ]
        if not target and len(nonzero) == 1:
            return {
                "certificate_mode": "unary_isolated_lattice_class",
                "pivot": pivot,
                "target_equation_index": equation,
                "target_matching_indices": list(
                    map(int, activities[equation])
                ),
                "signed_classes": signed_classes,
            }
        if target and not nonzero:
            return {
                "certificate_mode": "unary_annihilated_required_amplitude",
                "pivot": pivot,
                "target_equation_index": equation,
                "target_matching_indices": list(
                    map(int, activities[equation])
                ),
                "signed_classes": signed_classes,
            }
    return None


def analyze(
    system: EquationSystem,
    model: Path,
    cnf: Path,
) -> dict[str, object]:
    selected = local_positive_to_flat(
        system,
        sorted(positive_model_literals(model)),
        center_degree=1,
    )
    activities, monomials = active_matching_data(system, selected)
    clauses, relations, origins = factor_relations(
        system,
        activities,
        monomials,
    )
    certificates: list[dict[str, object]] = []
    forbidden: list[int] = []
    for relation_id, relation in enumerate(relations):
        certificate = unary_conflict(
            system,
            relation,
            activities,
            monomials,
        )
        if certificate is None:
            continue
        forbidden.append(relation_id)
        certificates.append(
            {
                "relation_id": relation_id,
                "relation_origin": origins[relation_id],
                "certificate": certificate,
            }
        )
    unit_clauses = [(-(relation_id + 1),) for relation_id in forbidden]
    final_clauses = [*clauses, *unit_clauses]
    with Solver(name="cadical195", bootstrap_with=final_clauses) as solver:
        status = "SAT" if solver.solve() else "UNSAT"
    write_dimacs(cnf, len(relations), final_clauses)
    return {
        "status": status,
        "model": str(model),
        "model_sha256": sha256(model),
        "selected_entries": len(selected),
        "factor_relations": len(relations),
        "factor_clauses": len(clauses),
        "unary_forbidden_relations": len(forbidden),
        "unary_certificates": certificates,
        "final_cnf": str(cnf),
        "final_cnf_sha256": sha256(cnf),
        "final_cnf_variables": len(relations),
        "final_cnf_clauses": len(final_clauses),
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
        "--cnf-dir",
        type=Path,
        default=Path("tmp/eight_vertex_unary_cycle_relation_cnf"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    family = json.loads(args.family.read_text(encoding="utf-8"))
    args.cnf_dir.mkdir(parents=True, exist_ok=True)
    system = EquationSystem(8, 3)
    rows: list[dict[str, object]] = []
    for index, model in enumerate(hard_models(family)):
        row = analyze(
            system,
            model,
            args.cnf_dir / f"orbit_{index:02d}.cnf",
        )
        rows.append(row)
        print(
            f"orbit={index + 1}/23 status={row['status']} "
            f"unary={row['unary_forbidden_relations']}/"
            f"{row['factor_relations']}",
            flush=True,
        )
    payload = {
        "status": (
            "UNSAT" if all(row["status"] == "UNSAT" for row in rows)
            else "INCOMPLETE"
        ),
        "scope": (
            "unary signed-cycle relation reduction of all 23 "
            "binomial-free n=8 equality-support orbits"
        ),
        "necessary_conditions_only": True,
        "family": str(args.family),
        "family_sha256": sha256(args.family),
        "orbits": len(rows),
        "unary_forbidden_relations": sum(
            int(row["unary_forbidden_relations"]) for row in rows
        ),
        "factor_relations": sum(
            int(row["factor_relations"]) for row in rows
        ),
        "factor_clauses": sum(
            int(row["factor_clauses"]) for row in rows
        ),
        "rows": rows,
        "solve_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "rows"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
