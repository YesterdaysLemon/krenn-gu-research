#!/usr/bin/env python3
"""Independently reconstruct high-coordinate P5 chart ledgers."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pysat.solvers import Solver

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu import p5_support_system as GENERATOR
from krenn_gu.p5_split_saturation import convert_text
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu.p5_high_coordinate import (
    normalized_supports,
    normalized_tree,
    validate_forest,
)
from krenn_gu import p5_pair_support_semantics as SEMANTICS


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clause_is_false(
    pool,
    clause: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
) -> bool:
    for literal in clause:
        key = pool.obj(abs(literal))
        if key[0] == "x":
            _label, mode, source, colour = key
            value = bool(supports[mode][source] & (1 << colour))
        elif key[0] == "singleton":
            _label, mode, source, colour = key
            value = supports[mode][source] == 1 << colour
        else:
            raise AssertionError(
                f"chart clause used a non-support variable: {key}"
            )
        if value == (literal > 0):
            return False
    return True


def validate_record(
    branch: str,
    pool,
    record: dict,
) -> tuple[tuple[int, ...], dict]:
    supports = normalized_supports(record["supports"])
    closure = normalized_supports(record["closure_supports"])
    tree = normalized_tree(record["gauge_tree"])
    actual_components, forest_components = validate_forest(
        supports, closure, tree
    )
    indices = tuple(map(int, record["signature_indices"]))
    program, metadata = GENERATOR.generate(
        closure,
        indices,
        expected_partial_cells=0,
        pure_saturation_only=True,
        gauge_tree_edges=tree,
        allow_arbitrary_support=True,
    )
    certificate = record["certificate"]
    if (
        certificate.get("status") != "UNIT_IDEAL"
        or certificate.get("metadata") != metadata
        or certificate.get("source_sha256") != sha256_text(program)
        or certificate.get("cas", {}).get("status") != "UNIT_IDEAL"
    ):
        raise AssertionError("recorded direct source or certificate changed")
    method = certificate.get("method")
    split_program = None
    if method == "split":
        split_program = convert_text(program)
        if certificate.get("split_source_sha256") != sha256_text(
            split_program
        ):
            raise AssertionError("recorded split source changed")
    elif method != "direct":
        raise AssertionError(f"unsupported certificate method: {method}")

    clause = HIGH.chart_clause(pool, closure, tree, branch)
    if not clause_is_false(pool, clause, supports):
        raise AssertionError("upgraded chart clause misses its source model")
    stored_clause = tuple(record.get("clause", ()))
    if (
        "initial_closure_supports" in record
        and stored_clause != clause
    ):
        raise AssertionError("stored upgraded chart clause changed")
    return clause, {
        "method": method,
        "actual_components": actual_components,
        "forest_components": forest_components,
        "forest_edges": len(tree),
        "program": program,
        "split_program": split_program,
    }


def rerun(task: dict, timeout: int) -> dict:
    program = (
        task["split_program"]
        if task["method"] == "split"
        else task["program"]
    )
    result = HIGH.run_singular(program, timeout)
    return {
        "verified": result["status"] == "UNIT_IDEAL",
        "method": task["method"],
        "seconds": result["elapsed_seconds"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branch",
        choices=tuple(HIGH.BRANCH_BACKBONES),
        required=True,
    )
    parser.add_argument(
        "--state",
        action="append",
        type=Path,
        required=True,
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--require-unsat", action="store_true")
    parser.add_argument("--rerun-singular", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--singular-timeout", type=int, default=240)
    args = parser.parse_args()
    if (
        args.jobs <= 0
        or args.singular_timeout <= 0
        or (args.limit is not None and args.limit <= 0)
    ):
        raise ValueError("invalid replay arguments")

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    branch_metadata = HIGH.add_branch_restriction(
        cnf, pool, allowed, args.branch
    )
    lex_leaders = HIGH.add_stabilizer_lex_leaders(
        cnf, pool, args.branch
    )
    records = []
    state_statuses = []
    for path in args.state:
        state = json.loads(path.read_text(encoding="utf-8"))
        if state.get("branch") != args.branch:
            raise AssertionError(f"state branch mismatch: {path}")
        state_statuses.append(state.get("status"))
        records.extend(state.get("records", []))
    selected = records if args.limit is None else records[: args.limit]

    clauses = []
    tasks = []
    method_counts = Counter()
    component_counts = Counter()
    forest_component_counts = Counter()
    forest_edge_counts = Counter()
    for record in selected:
        clause, task = validate_record(args.branch, pool, record)
        clauses.append(clause)
        tasks.append(task)
        method_counts[task["method"]] += 1
        component_counts[task["actual_components"]] += 1
        forest_component_counts[task["forest_components"]] += 1
        forest_edge_counts[task["forest_edges"]] += 1

    unique_clauses = tuple(sorted(set(clauses)))
    if len(unique_clauses) != len(clauses):
        raise AssertionError("ledger contains repeated upgraded clauses")
    cnf.extend([list(clause) for clause in unique_clauses])
    solver_results = {}
    for solver_name in ("cadical195", "glucose4"):
        with Solver(
            name=solver_name,
            bootstrap_with=cnf.clauses,
        ) as solver:
            solver_results[solver_name] = (
                "UNSAT" if not solver.solve() else "SAT"
            )
    if args.require_unsat and any(
        result != "UNSAT" for result in solver_results.values()
    ):
        raise AssertionError("required branch cover remains satisfiable")

    singular_results = []
    if args.rerun_singular:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            singular_results = list(
                executor.map(
                    lambda task: rerun(
                        task, args.singular_timeout
                    ),
                    tasks,
                )
            )
        if not all(item["verified"] for item in singular_results):
            raise AssertionError("fresh Singular replay failed")

    print(
        json.dumps(
            {
                "verified": True,
                "branch": args.branch,
                "state_statuses": state_statuses,
                "catalogue_signatures": len(allowed),
                "branch_restriction": branch_metadata,
                "lex_leaders": lex_leaders,
                "records_checked": len(selected),
                "unique_upgraded_clauses": len(unique_clauses),
                "certificate_methods": dict(method_counts),
                "actual_support_components": dict(component_counts),
                "gauge_forest_components": dict(
                    forest_component_counts
                ),
                "gauge_forest_edges": dict(forest_edge_counts),
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "solver_results": solver_results,
                "fresh_singular_replays": len(singular_results),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
