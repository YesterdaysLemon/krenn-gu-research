"""Independently verify the 23 unary cycle-relation certificates.

The producer in ``analyze_unary_cycle_relation_family.py`` is intentionally
not imported.  This verifier reconstructs the selected supports, active
perfect matchings, Laurent exponent vectors, four-term factor clauses,
rank-one signed quotients, unit exclusions, and exact DIMACS bytes.

SAT proof replay is a separate layer.  This script checks the semantic
translation and confirms UNSAT with an independently instantiated solver.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Sequence

from pysat.solvers import Solver

from search_witness import EquationSystem


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def positive_literals(path: Path) -> set[int]:
    result: set[int] = set()
    for line in path.read_text(encoding="ascii").splitlines():
        for token in line.split():
            if token in {"s", "v", "SAT", "SATISFIABLE"}:
                continue
            try:
                literal = int(token)
            except ValueError:
                continue
            if literal > 0:
                result.add(literal)
    return result


def hard_model_rows(family: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for skeleton_type in family["types"]:
        for factor_type in skeleton_type["factor_types"]:
            if list(map(int, factor_type["full_factor_cycle_type"])) != [4, 4]:
                continue
            for orbit in factor_type["orbits"]:
                if orbit["binomial_free"] is not True:
                    raise AssertionError("C4+C4 orbit is not binomial-free")
                rows.append(orbit)
    rows.sort(key=lambda row: int(row["global_orbit_index"]))
    if len(rows) != 23:
        raise AssertionError(f"expected 23 hard orbits, got {len(rows)}")
    return rows


def selected_flat_indices(path: Path, variable_count: int) -> set[int]:
    """Decode the n=8 local SAT variables without producer helpers.

    In the center-degree-one catalogue all 28 edges are allowed and both the
    local and global edge order are lexicographic combinations.  Therefore
    SAT literal ``k`` directly denotes flat entry ``k - 1`` for 1..252.
    """

    return {
        literal - 1
        for literal in positive_literals(path)
        if 1 <= literal <= variable_count
    }


def entry_index(
    system: EquationSystem,
    first: int,
    second: int,
    first_colour: int,
    second_colour: int,
) -> int:
    if first < second:
        edge = (first, second)
        row, column = first_colour, second_colour
    else:
        edge = (second, first)
        row, column = second_colour, first_colour
    return (
        system.d**2 * system.edge_index[edge]
        + system.d * row
        + column
    )


def reconstruct_activities(
    system: EquationSystem,
    selected: set[int],
) -> tuple[list[list[int]], list[list[tuple[int, ...]]]]:
    ordered_variables = sorted(selected)
    position = {
        variable: index for index, variable in enumerate(ordered_variables)
    }
    activities: list[list[int]] = []
    monomials: list[list[tuple[int, ...]]] = []
    for colouring in system.colourings:
        raw_colouring = list(map(int, colouring))
        active: list[int] = []
        vectors: list[tuple[int, ...]] = []
        for matching_id, matching in enumerate(system.matchings):
            entries = [
                entry_index(
                    system,
                    int(first),
                    int(second),
                    raw_colouring[int(first)],
                    raw_colouring[int(second)],
                )
                for first, second in matching
            ]
            if not all(entry in selected for entry in entries):
                continue
            vector = [0] * len(ordered_variables)
            for entry in entries:
                vector[position[entry]] += 1
            active.append(matching_id)
            vectors.append(tuple(vector))
        activities.append(active)
        monomials.append(vectors)
    return activities, monomials


def canonical_direction(values: Sequence[int]) -> tuple[int, ...]:
    direct = tuple(map(int, values))
    negative = tuple(-value for value in direct)
    return min(direct, negative)


def reconstruct_factors(
    system: EquationSystem,
    activities: Sequence[Sequence[int]],
    monomials: Sequence[Sequence[tuple[int, ...]]],
) -> tuple[list[tuple[int, int]], list[tuple[int, ...]], list[dict[str, object]]]:
    relation_index: dict[tuple[int, ...], int] = {}
    relations: list[tuple[int, ...]] = []
    origins: list[dict[str, object]] = []
    clauses: list[tuple[int, int]] = []
    for equation, vectors in enumerate(monomials):
        if bool(system.target[equation]) or len(vectors) != 4:
            continue
        pair: tuple[tuple[int, ...], tuple[int, ...]] | None = None
        for first, second, opposite in ((1, 2, 3), (1, 3, 2), (2, 3, 1)):
            if all(
                vectors[0][coordinate] + vectors[opposite][coordinate]
                == vectors[first][coordinate] + vectors[second][coordinate]
                for coordinate in range(len(vectors[0]))
            ):
                pair = (
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
                break
        if pair is None:
            continue
        ids: list[int] = []
        for direction in pair:
            if direction not in relation_index:
                relation_index[direction] = len(relations)
                relations.append(direction)
                origins.append(
                    {
                        "equation_index": equation,
                        "matching_indices": list(map(int, activities[equation])),
                    }
                )
            ids.append(relation_index[direction])
        if ids[0] == ids[1]:
            raise AssertionError("factor clause collapsed")
        clauses.append((ids[0] + 1, ids[1] + 1))
    return clauses, relations, origins


def unary_contradiction(
    system: EquationSystem,
    relation: tuple[int, ...],
    activities: Sequence[Sequence[int]],
    monomials: Sequence[Sequence[tuple[int, ...]]],
) -> dict[str, object] | None:
    pivots = [
        index for index, coefficient in enumerate(relation)
        if abs(coefficient) == 1
    ]
    if not pivots:
        raise AssertionError("relation has no unit coordinate")
    pivot = pivots[0]
    pivot_sign = relation[pivot]
    for equation, vectors in enumerate(monomials):
        if not vectors:
            continue
        classes: dict[tuple[int, ...], list[tuple[int, int, int]]] = {}
        for matching, vector in zip(
            activities[equation], vectors, strict=True
        ):
            coordinate = vector[pivot] * pivot_sign
            residual = tuple(
                value - coordinate * direction
                for value, direction in zip(vector, relation, strict=True)
            )
            sign = -1 if coordinate % 2 else 1
            classes.setdefault(residual, []).append(
                (int(matching), sign, coordinate)
            )
        signed_classes = [
            {
                "signed_coefficient": sum(member[1] for member in members),
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
        if not bool(system.target[equation]) and len(nonzero) == 1:
            return {
                "certificate_mode": "unary_isolated_lattice_class",
                "pivot": pivot,
                "target_equation_index": equation,
                "target_matching_indices": list(
                    map(int, activities[equation])
                ),
                "signed_classes": signed_classes,
            }
        if bool(system.target[equation]) and not nonzero:
            return {
                "certificate_mode": (
                    "unary_annihilated_required_amplitude"
                ),
                "pivot": pivot,
                "target_equation_index": equation,
                "target_matching_indices": list(
                    map(int, activities[equation])
                ),
                "signed_classes": signed_classes,
            }
    return None


def dimacs_bytes(
    variables: int,
    clauses: Sequence[Sequence[int]],
) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}"]
    lines.extend(
        " ".join(map(str, clause)) + " 0" for clause in clauses
    )
    return ("\n".join(lines) + "\n").encode("ascii")


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
        "--producer",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/eight_vertex_unary_cycle_relation_family_verified.json"
        ),
    )
    args = parser.parse_args()
    started = time.perf_counter()
    family = json.loads(args.family.read_text(encoding="utf-8"))
    producer = json.loads(args.producer.read_text(encoding="utf-8"))
    models = hard_model_rows(family)
    if len(producer["rows"]) != len(models):
        raise AssertionError("producer row count mismatch")

    system = EquationSystem(8, 3)
    checks: list[dict[str, object]] = []
    total_relations = 0
    total_clauses = 0
    total_forbidden = 0
    for orbit_index, (orbit, stored) in enumerate(
        zip(models, producer["rows"], strict=True)
    ):
        model = Path(orbit["model"])
        if Path(stored["model"]) != model:
            raise AssertionError("producer model order mismatch")
        if sha256(model) != orbit["model_sha256"]:
            raise AssertionError("family model hash mismatch")
        if sha256(model) != stored["model_sha256"]:
            raise AssertionError("producer model hash mismatch")

        selected = selected_flat_indices(model, system.variable_count)
        if selected != set(map(int, orbit["selected_flat_indices"])):
            raise AssertionError("family selected support mismatch")
        if len(selected) != 84 or stored["selected_entries"] != 84:
            raise AssertionError("unexpected support size")
        activities, monomials = reconstruct_activities(system, selected)
        clauses, relations, origins = reconstruct_factors(
            system, activities, monomials
        )
        forbidden: list[int] = []
        certificates: list[dict[str, object]] = []
        for relation_id, relation in enumerate(relations):
            certificate = unary_contradiction(
                system, relation, activities, monomials
            )
            if certificate is not None:
                forbidden.append(relation_id)
                certificates.append(
                    {
                        "relation_id": relation_id,
                        "relation_origin": origins[relation_id],
                        "certificate": certificate,
                    }
                )
        final_clauses: list[Sequence[int]] = [
            *clauses,
            *((-(relation_id + 1),) for relation_id in forbidden),
        ]
        if len(relations) != stored["factor_relations"]:
            raise AssertionError("factor relation count mismatch")
        if len(clauses) != stored["factor_clauses"]:
            raise AssertionError("factor clause count mismatch")
        if len(forbidden) != stored["unary_forbidden_relations"]:
            raise AssertionError("unary exclusion count mismatch")
        if certificates != stored["unary_certificates"]:
            raise AssertionError("unary certificate content mismatch")

        cnf_path = Path(stored["final_cnf"])
        expected_bytes = dimacs_bytes(len(relations), final_clauses)
        if cnf_path.read_bytes() != expected_bytes:
            raise AssertionError("DIMACS bytes differ from reconstruction")
        if sha256(cnf_path) != stored["final_cnf_sha256"]:
            raise AssertionError("DIMACS hash mismatch")
        with Solver(
            name="cadical195", bootstrap_with=final_clauses
        ) as solver:
            if solver.solve():
                raise AssertionError("reconstructed unary CNF is SAT")

        total_relations += len(relations)
        total_clauses += len(clauses)
        total_forbidden += len(forbidden)
        checks.append(
            {
                "orbit_index": orbit_index,
                "global_orbit_index": int(orbit["global_orbit_index"]),
                "model": str(model),
                "model_sha256": sha256(model),
                "factor_relations": len(relations),
                "factor_clauses": len(clauses),
                "unary_forbidden_relations": len(forbidden),
                "final_cnf": str(cnf_path),
                "final_cnf_sha256": sha256(cnf_path),
                "semantic_reconstruction": True,
                "independent_solver_unsat": True,
            }
        )
        print(
            f"orbit={orbit_index + 1}/23 verified "
            f"unary={len(forbidden)}/{len(relations)}",
            flush=True,
        )

    expected_totals = (
        int(producer["factor_relations"]),
        int(producer["factor_clauses"]),
        int(producer["unary_forbidden_relations"]),
    )
    actual_totals = (total_relations, total_clauses, total_forbidden)
    if actual_totals != expected_totals:
        raise AssertionError(
            f"aggregate mismatch: {actual_totals} != {expected_totals}"
        )
    payload = {
        "verified": True,
        "scope": (
            "independent semantic reconstruction of all 23 unary "
            "cycle-relation factor CNFs"
        ),
        "family": str(args.family),
        "family_sha256": sha256(args.family),
        "producer": str(args.producer),
        "producer_sha256": sha256(args.producer),
        "orbits": len(checks),
        "factor_relations": total_relations,
        "factor_clauses": total_clauses,
        "unary_forbidden_relations": total_forbidden,
        "checks": checks,
        "verify_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {key: value for key, value in payload.items() if key != "checks"},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
