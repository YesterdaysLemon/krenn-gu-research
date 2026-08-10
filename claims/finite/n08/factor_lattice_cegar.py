"""Explore Laurent-cube factor branches with exact signed-lattice reduction.

This is an algebraic follow-up to ``eight_vertex_no_binomial_cegar.py``.
For a fixed nonzero support, a forbidden amplitude with four active
monomials often has a Laurent factorization

    x^a + x^b + x^c + x^d
      = x^g (1 + x^r) (1 + x^s).

Since every selected entry is nonzero, the amplitude can vanish only if
``x^r = -1`` or ``x^s = -1``.  We encode those alternatives as Boolean
clauses.  A SAT assignment selects signed binomial relations; exact integer
lattice reduction then looks for an inconsistent sign or an amplitude that
reduces to one nonzero signed monomial class.

The same mechanism applies to an eight-term affine exponent cube, producing
a three-way signed-relation clause.  The procedure is deliberately
support-local.  A surviving Boolean branch is not a complex witness, while
UNSAT needs an independently replayed SAT proof before it can be promoted
to a finite theorem.
"""

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
import hashlib
import itertools
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np
from pysat.solvers import Solver

from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from krenn_gu.eight_vertex_sparse_exact import positive_model_literals
from krenn_gu.search_witness import EquationSystem
from krenn_gu.signed_binomial_lattice import _basis_data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_dimacs(
    path: Path,
    variables: int,
    clauses: Sequence[Sequence[int]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def canonical_vector(vector: Sequence[int]) -> tuple[int, ...]:
    direct = tuple(map(int, vector))
    negative = tuple(-value for value in direct)
    return min(direct, negative)


def monomial_vector(
    system: EquationSystem,
    variables: Sequence[int],
    equation: int,
    matching: int,
) -> tuple[int, ...]:
    positions = {
        int(variable): position
        for position, variable in enumerate(variables)
    }
    vector = [0] * len(variables)
    for raw_entry in system.variable_ids[matching, equation, :]:
        vector[positions[int(raw_entry)]] += 1
    return tuple(vector)


def active_matching_data(
    system: EquationSystem,
    selected: set[int],
) -> tuple[list[list[int]], list[list[tuple[int, ...]]]]:
    mask = np.zeros(system.variable_count, dtype=bool)
    mask[list(selected)] = True
    active_matrix = np.all(mask[system.variable_ids], axis=2)
    variables = sorted(selected)
    activities: list[list[int]] = []
    vectors: list[list[tuple[int, ...]]] = []
    for equation in range(len(system.colourings)):
        activity = list(
            map(int, np.flatnonzero(active_matrix[:, equation]))
        )
        activities.append(activity)
        vectors.append(
            [
                monomial_vector(
                    system,
                    variables,
                    equation,
                    matching,
                )
                for matching in activity
            ]
        )
    return activities, vectors


def eight_term_cube_factors(
    vectors: Sequence[tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None:
    """Return Laurent directions when eight exponents form an affine cube."""
    if len(vectors) != 8 or len(set(vectors)) != 8:
        return None
    base = vectors[0]
    point_set = set(vectors)
    differences = [
        tuple(
            int(right - left)
            for left, right in zip(base, point, strict=True)
        )
        for point in vectors[1:]
    ]
    for raw_directions in itertools.combinations(differences, 3):
        expected: set[tuple[int, ...]] = set()
        for mask in range(8):
            expected.add(
                tuple(
                    int(
                        base[position]
                        + sum(
                            raw_directions[axis][position]
                            for axis in range(3)
                            if mask & (1 << axis)
                        )
                    )
                    for position in range(len(base))
                )
            )
        if expected != point_set:
            continue
        directions = tuple(
            canonical_vector(direction)
            for direction in raw_directions
        )
        if len(set(directions)) != 3:
            raise AssertionError("eight-term factor directions collapsed")
        return directions
    return None


def factor_relations(
    system: EquationSystem,
    activities: Sequence[Sequence[int]],
    monomials: Sequence[Sequence[tuple[int, ...]]],
    include_direct_binomials: bool = False,
    include_eight_term_cubes: bool = False,
) -> tuple[
    list[tuple[int, ...]],
    list[tuple[int, ...]],
    list[dict[str, object]],
]:
    """Return Boolean factor clauses and their exact exponent relations."""
    relation_index: dict[tuple[int, ...], int] = {}
    relations: list[tuple[int, ...]] = []
    origins: list[dict[str, object]] = []
    clauses: list[tuple[int, ...]] = []

    for equation, activity in enumerate(activities):
        if bool(system.target[equation]):
            continue
        vectors = monomials[equation]
        if include_direct_binomials and len(activity) == 2:
            vector = canonical_vector(
                left - right
                for left, right in zip(
                    vectors[0],
                    vectors[1],
                    strict=True,
                )
            )
            if vector not in relation_index:
                relation_index[vector] = len(relations)
                relations.append(vector)
                origins.append(
                    {
                        "certificate_mode": (
                            "direct_two_term_forbidden_amplitude"
                        ),
                        "equation_index": equation,
                        "matching_indices": list(map(int, activity)),
                    }
                )
            clauses.append((relation_index[vector] + 1,))
            continue
        if include_eight_term_cubes and len(activity) == 8:
            factor_vectors = eight_term_cube_factors(vectors)
            if factor_vectors is None:
                continue
            ids: list[int] = []
            for vector in factor_vectors:
                if vector not in relation_index:
                    relation_index[vector] = len(relations)
                    relations.append(vector)
                    origins.append(
                        {
                            "certificate_mode": (
                                "eight_term_laurent_cube"
                            ),
                            "equation_index": equation,
                            "matching_indices": list(
                                map(int, activity)
                            ),
                        }
                    )
                ids.append(relation_index[vector])
            clauses.append(tuple(index + 1 for index in ids))
            continue
        if len(activity) != 4:
            continue
        factor_pair: tuple[tuple[int, ...], tuple[int, ...]] | None = None
        # With vector 0 fixed, the three choices below enumerate the three
        # possible opposite-corner pairings of a four-point parallelogram.
        for first, second, opposite in (
            (1, 2, 3),
            (1, 3, 2),
            (2, 3, 1),
        ):
            if all(
                vectors[0][position] + vectors[opposite][position]
                == vectors[first][position] + vectors[second][position]
                for position in range(len(vectors[0]))
            ):
                factor_pair = (
                    canonical_vector(
                        left - right
                        for left, right in zip(
                            vectors[0],
                            vectors[first],
                            strict=True,
                        )
                    ),
                    canonical_vector(
                        left - right
                        for left, right in zip(
                            vectors[0],
                            vectors[second],
                            strict=True,
                        )
                    ),
                )
                break
        if factor_pair is None:
            continue
        ids: list[int] = []
        for vector in factor_pair:
            if vector not in relation_index:
                relation_index[vector] = len(relations)
                relations.append(vector)
                origins.append(
                    {
                        "equation_index": equation,
                        "matching_indices": list(map(int, activity)),
                    }
                )
            ids.append(relation_index[vector])
        if ids[0] == ids[1]:
            raise AssertionError("factor clause collapsed to one relation")
        clauses.append((ids[0] + 1, ids[1] + 1))
    return clauses, relations, origins


def exact_lattice_conflict(
    system: EquationSystem,
    selected_relation_ids: Sequence[int],
    relations: Sequence[tuple[int, ...]],
    activities: Sequence[Sequence[int]],
    monomials: Sequence[Sequence[tuple[int, ...]]],
) -> dict[str, object] | None:
    """Find one exact contradiction implied by selected factor relations."""
    rows = [list(relations[index]) for index in selected_relation_ids]
    basis_data = _basis_data(rows)
    if basis_data is None:
        return None
    independent, pivots, raw_basis, raw_inverse = basis_data
    basis_ids = [
        int(selected_relation_ids[position])
        for position in independent
    ]
    basis = np.asarray(raw_basis.tolist(), dtype=np.int64)
    inverse = np.asarray(raw_inverse.tolist(), dtype=np.int64)
    pivot_array = np.asarray(pivots, dtype=np.int64)

    def coordinates(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        coordinate = vector[pivot_array] @ inverse
        residual = vector - coordinate @ basis
        return coordinate, residual

    # A selected dependent relation must also receive sign -1.  If the
    # independent basis predicts +1, the branch is already inconsistent.
    for relation_id in selected_relation_ids:
        vector = np.asarray(relations[relation_id], dtype=np.int64)
        coordinate, residual = coordinates(vector)
        if np.any(residual):
            continue
        if int(coordinate.sum()) % 2 == 0:
            return {
                "certificate_mode": "inconsistent_factor_sign",
                "basis_relation_ids": basis_ids,
                "target_relation_id": int(relation_id),
                "target_coordinates": list(map(int, coordinate)),
            }

    # Reduce each amplitude into signed classes modulo the selected lattice.
    for equation, raw_vectors in enumerate(monomials):
        if not raw_vectors:
            continue
        classes: dict[
            tuple[int, ...],
            list[tuple[int, int, list[int]]],
        ] = defaultdict(list)
        for matching, raw_vector in zip(
            activities[equation],
            raw_vectors,
            strict=True,
        ):
            vector = np.asarray(raw_vector, dtype=np.int64)
            coordinate, residual = coordinates(vector)
            sign = -1 if int(coordinate.sum()) % 2 else 1
            classes[tuple(map(int, residual))].append(
                (
                    int(matching),
                    sign,
                    list(map(int, coordinate)),
                )
            )
        signed_classes = [
            {
                "signed_coefficient": sum(item[1] for item in members),
                "members": [
                    {
                        "matching_index": item[0],
                        "sign": item[1],
                        "coordinates": item[2],
                    }
                    for item in members
                ],
            }
            for _residual, members in sorted(classes.items())
        ]
        nonzero_classes = [
            item
            for item in signed_classes
            if int(item["signed_coefficient"]) != 0
        ]
        if (
            not bool(system.target[equation])
            and len(nonzero_classes) == 1
        ):
            return {
                "certificate_mode": "isolated_factor_lattice_class",
                "basis_relation_ids": basis_ids,
                "target_equation_index": equation,
                "target_matching_indices": list(
                    map(int, activities[equation])
                ),
                "signed_classes": signed_classes,
            }
        if bool(system.target[equation]) and not nonzero_classes:
            return {
                "certificate_mode": "annihilated_required_amplitude",
                "basis_relation_ids": basis_ids,
                "target_equation_index": equation,
                "target_matching_indices": list(
                    map(int, activities[equation])
                ),
                "signed_classes": signed_classes,
            }
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--center-degree", type=int, default=1)
    parser.add_argument("--max-models", type=int, default=0)
    parser.add_argument(
        "--solver",
        default="cadical195",
        choices=("cadical195", "glucose4", "maplechrono"),
    )
    parser.add_argument(
        "--include-direct-binomials",
        action="store_true",
        help=(
            "add every literal two-term forbidden amplitude as a mandatory "
            "signed relation alongside the four-term factor choices"
        ),
    )
    parser.add_argument(
        "--include-eight-term-cubes",
        action="store_true",
        help=(
            "also factor exact eight-term affine exponent cubes into "
            "three-way signed-relation clauses"
        ),
    )
    args = parser.parse_args()

    started = time.perf_counter()
    system = EquationSystem(8, 3)
    selected = local_positive_to_flat(
        system,
        sorted(positive_model_literals(args.model)),
        center_degree=args.center_degree,
    )
    activities, monomials = active_matching_data(system, selected)
    clauses, relations, origins = factor_relations(
        system,
        activities,
        monomials,
        include_direct_binomials=args.include_direct_binomials,
        include_eight_term_cubes=args.include_eight_term_cubes,
    )
    learned: list[list[int]] = []
    rows: list[dict[str, object]] = []
    terminal_status = "running"

    with Solver(name=args.solver, bootstrap_with=clauses) as solver:
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
            certificate = exact_lattice_conflict(
                system,
                selected_ids,
                relations,
                activities,
                monomials,
            )
            if certificate is None:
                terminal_status = "survivor"
                rows.append(
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
                blocking_ids.add(int(certificate["target_relation_id"]))
            clause = [-(index + 1) for index in sorted(blocking_ids)]
            if not clause:
                raise AssertionError("empty factor-lattice blocking clause")
            solver.add_clause(clause)
            learned.append(clause)
            rows.append(
                {
                    "selected_relations": len(selected_ids),
                    "blocking_clause": clause,
                    "certificate": certificate,
                }
            )
            print(
                f"model={len(rows)} selected={len(selected_ids)} "
                f"rank={len(certificate['basis_relation_ids'])} "
                f"mode={certificate['certificate_mode']}",
                flush=True,
            )
            if args.max_models and len(rows) >= args.max_models:
                terminal_status = "limit"
                break
        else:
            terminal_status = "UNSAT"

    payload = {
        "status": terminal_status,
        "scope": (
            "fixed-support four-term factor branches with exact "
            "signed-lattice reduction"
        ),
        "necessary_conditions_only": terminal_status == "survivor",
        "model": str(args.model),
        "model_sha256": sha256(args.model),
        "selected_entries": len(selected),
        "selected_flat_indices": sorted(map(int, selected)),
        "factor_relations": [
            {
                "relation_id": index,
                "vector": list(map(int, vector)),
                "origin": origins[index],
            }
            for index, vector in enumerate(relations)
        ],
        "factor_clauses": [list(map(int, clause)) for clause in clauses],
        "factor_clause_count": len(clauses),
        "factor_relation_count": len(relations),
        "include_direct_binomials": args.include_direct_binomials,
        "include_eight_term_cubes": args.include_eight_term_cubes,
        "learned_clauses": learned,
        "branches": rows,
        "solve_seconds": time.perf_counter() - started,
    }
    if args.cnf is not None:
        write_dimacs(
            args.cnf,
            len(relations),
            [*clauses, *learned],
        )
        payload["final_cnf"] = str(args.cnf)
        payload["final_cnf_sha256"] = sha256(args.cnf)
        payload["final_cnf_clauses"] = len(clauses) + len(learned)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": terminal_status,
                "selected_entries": len(selected),
                "factor_clauses": len(clauses),
                "factor_relations": len(relations),
                "branches": len(rows),
                "solve_seconds": payload["solve_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
