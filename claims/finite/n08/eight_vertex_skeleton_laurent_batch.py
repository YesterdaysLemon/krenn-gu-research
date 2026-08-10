"""Incremental exact Laurent CEGAR over a fixed skeleton catalogue.

Each canonical skeleton is supplied through the 25 block indicators as SAT
assumptions.  Whenever its support relaxation is SAT, the selected nonzero
entry stratum is checked against all exact characteristic-zero amplitude
equations.  A Laurent-unit dependency becomes a sound support no-good; all
twelve canonical symmetry images are learned globally before the same
skeleton is solved again.

The run stops fail-closed if a SAT support has no Laurent unit.  Such a
stratum requires the full exact Gröbner fallback and is never silently
discarded.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from eight_vertex_degree4_cegar import (
    full_equations,
    laurent_conflict,
    symmetry_clauses,
    write_augmented_cnf,
)
from eight_vertex_skeleton_batch import (
    canonical_degree_three_role_skeletons,
    canonical_minimum_five_skeletons,
    canonical_normalized_killer_skeletons,
    canonical_role_skeletons,
    ordered_role_skeletons,
)
from eight_vertex_sparse_exact import (
    local_allowed_edges,
    selected_flat_indices,
)
from search_witness import EquationSystem


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def local_positive_to_flat(
    system: EquationSystem,
    model: list[int],
    center_degree: int = 4,
) -> set[int]:
    entry_variables = 9 * len(local_allowed_edges(center_degree))
    positive = {
        literal
        for literal in model
        if 0 < literal <= entry_variables
    }
    return set(
        selected_flat_indices(
            system, positive, center_degree=center_degree
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument(
        "--target-edges",
        type=int,
        help="omit to process every edge count in the catalogue",
    )
    parser.add_argument(
        "--center-degree",
        type=int,
        choices=(0, 1, 3, 4),
        default=4,
    )
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--learned-cnf", type=Path, required=True)
    parser.add_argument("--learned-manifest", type=Path, required=True)
    parser.add_argument(
        "--prefer-transport",
        action="store_true",
        help="try an elementary transport certificate before Laurent reduction",
    )
    parser.add_argument(
        "--role-index",
        type=int,
        action="append",
        help=(
            "process only this zero-based canonical role; repeat for a "
            "targeted globally-valid learning pass"
        ),
    )
    parser.add_argument(
        "--assumption",
        type=int,
        action="append",
        help=(
            "add a fixed DIMACS literal to every catalogue solve; "
            "repeat for a case split"
        ),
    )
    parser.add_argument(
        "--fallback-limit",
        type=int,
        default=1,
        help=(
            "enumerate up to this many exact fallback supports per role; "
            "temporary support blockers are not written to the learned CNF"
        ),
    )
    args = parser.parse_args()
    if args.fallback_limit < 1:
        raise ValueError("--fallback-limit must be positive")
    fixed_assumptions = tuple(sorted(set(args.assumption or [])))
    if any(
        -literal in fixed_assumptions
        for literal in fixed_assumptions
    ):
        raise ValueError("fixed assumptions contain a contradiction")

    from pysat.formula import CNF
    from pysat.solvers import Solver

    catalogue_started = time.perf_counter()
    catalogue_builder = {
        0: canonical_minimum_five_skeletons,
        1: canonical_normalized_killer_skeletons,
        3: canonical_degree_three_role_skeletons,
        4: canonical_role_skeletons,
    }[args.center_degree]
    roles, catalogue = catalogue_builder(
        args.graph6, target_edges=args.target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    indexed_roles = list(enumerate(ordered_roles))
    if args.role_index:
        selected_indices = sorted(set(args.role_index))
        if (
            selected_indices[0] < 0
            or selected_indices[-1] >= len(ordered_roles)
        ):
            raise ValueError("--role-index is outside the catalogue")
        indexed_roles = [
            (index, ordered_roles[index])
            for index in selected_indices
        ]
    else:
        selected_indices = list(range(len(ordered_roles)))
    catalogue_complete = len(indexed_roles) == len(ordered_roles)
    catalogue_seconds = time.perf_counter() - catalogue_started

    formula = CNF(from_file=str(args.cnf))
    allowed = local_allowed_edges(args.center_degree)
    system = EquationSystem(8, 3)
    allowed_flat = {
        9 * system.edge_index[edge] + 3 * row + column
        for edge in allowed
        for row in range(3)
        for column in range(3)
    }
    first_block_variable = 1 + 9 * len(allowed)
    equations, names, name_to_flat = full_equations(system)
    progress_interval = 10 if len(indexed_roles) < 250 else 250

    learned: set[tuple[int, ...]] = set()
    conflicts: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    fallback_count = 0
    temporary_fallback_blockers: set[tuple[int, ...]] = set()
    support_models = 0
    solve_started = time.perf_counter()
    print(
        f"catalogue roles={len(ordered_roles)} "
        f"selected={len(indexed_roles)} "
        f"first_edges={len(ordered_roles[0]) if ordered_roles else 0} "
        f"last_edges={len(ordered_roles[-1]) if ordered_roles else 0}",
        flush=True,
    )
    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        for processed_index, (role_index, skeleton) in enumerate(
            indexed_roles, start=1
        ):
            present = set(skeleton)
            assumptions = [
                (
                    first_block_variable + edge_index
                    if edge in present
                    else -(first_block_variable + edge_index)
                )
                for edge_index, edge in enumerate(allowed)
            ]
            assumptions.extend(fixed_assumptions)
            role_started = time.perf_counter()
            role_models = 0
            role_conflicts: list[int] = []
            status = "UNSAT"
            role_fallbacks: list[dict[str, object]] = []
            while solver.solve(assumptions=assumptions):
                model = solver.get_model() or []
                support_models += 1
                role_models += 1
                selected = local_positive_to_flat(
                    system, model, args.center_degree
                )
                try:
                    positive, negative, metadata = laurent_conflict(
                        system,
                        equations,
                        names,
                        name_to_flat,
                        selected,
                        center_degree=args.center_degree,
                        prefer_transport=args.prefer_transport,
                    )
                except (RuntimeError, ValueError) as error:
                    status = "EXACT_FALLBACK"
                    fallback_count += 1
                    positive_entry_variables = {
                        literal
                        for literal in model
                        if 0 < literal < first_block_variable
                    }
                    role_fallbacks.append(
                        {
                        "reason": str(error),
                        "selected_entries": len(selected),
                        "selected_flat_indices": sorted(selected),
                        "positive_entry_variables": sorted(
                            positive_entry_variables
                        ),
                        "temporary_symmetry_blockers": 0,
                        }
                    )
                    if len(role_fallbacks) >= args.fallback_limit:
                        break
                    # These full-support symmetry blockers are enumeration
                    # devices only.  They are deliberately absent from
                    # ``learned`` and therefore from the output CNF.  The
                    # exact Singular phase must certify the representative
                    # before the same images can be emitted permanently.
                    fallback_images = symmetry_clauses(
                        system,
                        selected,
                        allowed_flat - selected,
                        center_degree=args.center_degree,
                    )
                    new_temporary = [
                        clause
                        for clause in fallback_images
                        if clause not in temporary_fallback_blockers
                    ]
                    for clause in new_temporary:
                        solver.add_clause(list(clause))
                        temporary_fallback_blockers.add(clause)
                    role_fallbacks[-1]["temporary_symmetry_blockers"] = len(
                        new_temporary
                    )
                    continue

                images = symmetry_clauses(
                    system,
                    positive,
                    negative,
                    center_degree=args.center_degree,
                )
                new_clauses = [
                    clause for clause in images if clause not in learned
                ]
                if not new_clauses:
                    raise AssertionError(
                        "SAT model yielded no new Laurent conflict"
                    )
                conflict_index = len(conflicts)
                role_conflicts.append(conflict_index)
                conflicts.append(
                    {
                        "conflict_index": conflict_index,
                        "role_index": role_index,
                        **metadata,
                        "positive_entries": sorted(positive),
                        "negative_entries": sorted(negative),
                        "cube_size": len(positive) + len(negative),
                        "symmetry_images": len(images),
                        "new_clauses": len(new_clauses),
                    }
                )
                for clause in new_clauses:
                    solver.add_clause(list(clause))
                    learned.add(clause)

            row: dict[str, object] = {
                "role_index": role_index,
                "skeleton_edges": [list(edge) for edge in skeleton],
                "status": status,
                "support_models": role_models,
                "conflict_indices": role_conflicts,
                "solve_seconds": time.perf_counter() - role_started,
            }
            if len(role_fallbacks) == 1:
                row["fallback"] = role_fallbacks[0]
            elif role_fallbacks:
                row["fallbacks"] = role_fallbacks
            rows.append(row)
            if processed_index % progress_interval == 0:
                print(
                    f"{processed_index}/{len(indexed_roles)} "
                    f"models={support_models} "
                    f"conflicts={len(conflicts)} "
                    f"fallbacks={fallback_count}",
                    flush=True,
                )
                checkpoint(
                    args.output,
                    {
                        "status": "running",
                        **catalogue,
                        "target_edges": args.target_edges,
                        "center_degree": args.center_degree,
                        "prefer_transport": args.prefer_transport,
                        "catalogue_complete": catalogue_complete,
                        "selected_role_indices": selected_indices,
                        "fixed_assumptions": list(
                            fixed_assumptions
                        ),
                        "catalogue_seconds": catalogue_seconds,
                        "processed": len(rows),
                        "support_models": support_models,
                        "laurent_conflicts": len(conflicts),
                        "transport_conflicts": sum(
                            conflict.get("certificate_kind")
                            == "cancellation_transport"
                            for conflict in conflicts
                        ),
                        "learned_clauses": len(learned),
                        "fallback_count": fallback_count,
                        "temporary_fallback_blockers": len(
                            temporary_fallback_blockers
                        ),
                        "rows": rows,
                        "conflicts": conflicts,
                    },
                )

    ordered_learned = sorted(learned)
    write_augmented_cnf(
        args.cnf, args.learned_cnf, ordered_learned
    )
    learned_payload = {
        "scope": (
            "exact Laurent support no-goods learned over the "
            "n=8, "
            + (
                f"{args.target_edges}-edge"
                if args.target_edges is not None
                else "all-edge-count"
            )
            + " degree-"
            f"{args.center_degree} catalogue"
        ),
        "center_degree": args.center_degree,
        "prefer_transport": args.prefer_transport,
        "fixed_assumptions": list(fixed_assumptions),
        "base_cnf": str(args.cnf),
        "base_cnf_sha256": sha256(args.cnf),
        "learned_cnf": str(args.learned_cnf),
        "learned_cnf_sha256": sha256(args.learned_cnf),
        "support_models": support_models,
        "laurent_conflicts": len(conflicts),
        "transport_conflicts": sum(
            conflict.get("certificate_kind") == "cancellation_transport"
            for conflict in conflicts
        ),
        "learned_clauses": [
            list(clause) for clause in ordered_learned
        ],
        "conflicts": conflicts,
    }
    checkpoint(args.learned_manifest, learned_payload)

    payload = {
        "status": (
            (
                "complete"
                if catalogue_complete
                else "subset_complete"
            )
            if fallback_count == 0
            else "exact_fallback_required"
        ),
        **catalogue,
        "target_edges": args.target_edges,
        "center_degree": args.center_degree,
        "catalogue_complete": catalogue_complete,
        "selected_role_indices": selected_indices,
        "fixed_assumptions": list(fixed_assumptions),
        "catalogue_seconds": catalogue_seconds,
        "solver": "cadical195",
        "prefer_transport": args.prefer_transport,
        "cnf": str(args.cnf),
        "processed": len(rows),
        "support_models": support_models,
        "laurent_conflicts": len(conflicts),
        "transport_conflicts": sum(
            conflict.get("certificate_kind") == "cancellation_transport"
            for conflict in conflicts
        ),
        "learned_clauses": len(learned),
        "fallback_count": fallback_count,
        "temporary_fallback_blockers": len(temporary_fallback_blockers),
        "unsat_count": sum(
            row["status"] == "UNSAT" for row in rows
        ),
        "solve_seconds": time.perf_counter() - solve_started,
        "rows": rows,
        "conflicts": conflicts,
        "learned_cnf": str(args.learned_cnf),
        "learned_cnf_sha256": sha256(args.learned_cnf),
    }
    checkpoint(args.output, payload)
    print(
        f"{payload['status']} roles={len(rows)} "
        f"models={support_models} conflicts={len(conflicts)} "
        f"fallbacks={fallback_count}",
        flush=True,
    )


if __name__ == "__main__":
    main()
