#!/usr/bin/env python3
"""Run the P5 high-coordinate tree-chart CEGAR operator."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu import p5_pair_support_semantics as SEMANTICS  # noqa: E402
from krenn_gu import p5_support_system as GENERATOR  # noqa: E402
from krenn_gu.p5_high_coordinate import (  # noqa: E402
    BRANCH_BACKBONES,
    add_branch_restriction,
    add_stabilizer_lex_leaders,
    available_memory_percent,
    certify_chart,
    chart_clause,
    chart_symmetry_orbit_clauses,
    closure_supports,
    gauge_tree,
    gauge_tree_variants,
    selected_signature_indices,
    source_colour_stabilizer,
    transform_support_array,
)

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

def certify_gauge_tree_portfolio(
    supports: tuple[tuple[int, ...], ...],
    closure: tuple[tuple[int, ...], ...],
    indices: tuple[int, ...],
    alternatives: int,
    timeout: float,
) -> tuple[
    tuple[tuple[int, int, int], ...],
    dict | None,
    dict,
]:
    """Try short exact direct certificates across gauge forests."""
    variants = gauge_tree_variants(
        supports,
        closure,
        alternatives,
    )
    original = variants[0]
    scored = []
    for tree in variants:
        _program, metadata = GENERATOR.generate(
            closure,
            indices,
            expected_partial_cells=0,
            pure_saturation_only=True,
            gauge_tree_edges=tree,
            allow_arbitrary_support=True,
        )
        scored.append(
            (
                metadata["mixed_equations"],
                tree != original,
                tree,
            )
        )
    # Prefer fewer distinct equations, retaining the historical tree
    # first on a tie.
    ordered = tuple(tree for _count, _alternate, tree in sorted(scored))
    trials = []
    for tree in ordered:
        certificate = certify_chart(
            closure,
            indices,
            tree,
            timeout,
            try_split=False,
        )
        cas = (
            certificate.get("cas")
            or certificate.get("direct_cas")
            or {}
        )
        trials.append(
            {
                "tree": tree,
                "mixed_equations": certificate["metadata"][
                    "mixed_equations"
                ],
                "status": certificate["status"],
                "seconds": cas.get("elapsed_seconds"),
            }
        )
        if certificate["status"] == "UNIT_IDEAL":
            return tree, certificate, {
                "strategy": "deterministic-min-equations-v1",
                "alternative_count": alternatives,
                "trial_timeout_seconds": timeout,
                "trials": trials,
                "selected_tree": tree,
            }
    return original, None, {
        "strategy": "deterministic-min-equations-v1",
        "alternative_count": alternatives,
        "trial_timeout_seconds": timeout,
        "trials": trials,
        "selected_tree": None,
    }

def relax_chart_closure(
    supports: tuple[tuple[int, ...], ...],
    indices: tuple[int, ...],
    initial_closure: tuple[tuple[int, ...], ...],
    timeout: int,
    min_available_percent: float,
    recursive: bool = True,
    prefer_split: bool = False,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, int, int], ...],
    dict,
]:
    """Greedily enlarge a chart by recursive row-wise group trials."""
    current = [list(row) for row in initial_closure]
    trials = []
    accepted = []
    paused_for_memory = False

    def attempt(cells: tuple[tuple[int, int], ...]) -> None:
        nonlocal current, paused_for_memory
        if not cells or paused_for_memory:
            return
        available = available_memory_percent()
        if available < min_available_percent:
            paused_for_memory = True
            return
        proposed = [row[:] for row in current]
        for mode, source in cells:
            proposed[mode][source] = 7
        proposed_closure = tuple(tuple(row) for row in proposed)
        proposed_tree = gauge_tree(supports, proposed_closure)
        certificate = certify_chart(
            proposed_closure,
            indices,
            proposed_tree,
            timeout,
            try_split=prefer_split,
            prefer_split=prefer_split,
        )
        trial = {
            "cells": cells,
            "status": certificate["status"],
            "direct_cas": (
                certificate.get("cas")
                or certificate.get("direct_cas")
            ),
        }
        trials.append(trial)
        if certificate["status"] == "UNIT_IDEAL":
            current = proposed
            accepted.extend(cells)
            return
        if len(cells) == 1 or not recursive:
            return
        midpoint = len(cells) // 2
        attempt(cells[:midpoint])
        attempt(cells[midpoint:])

    # Mode zero is fixed by branch normalization.  Enlarging it adds
    # algebraic difficulty without increasing coverage inside the branch.
    for mode in SEMANTICS.MODES[1:]:
        attempt(
            tuple(
                (mode, source)
                for source in SEMANTICS.SOURCES
                if current[mode][source] in (1, 2, 4)
            )
        )

    closure = tuple(tuple(row) for row in current)
    tree = gauge_tree(supports, closure)
    return closure, tree, {
        "strategy": (
            "recursive-row-greedy-v1"
            if recursive
            else "whole-row-greedy-v1"
        ),
        "trial_timeout_seconds": timeout,
        "trials": trials,
        "accepted_cells": tuple(accepted),
        "paused_for_memory": paused_for_memory,
    }

def checkpoint(
    path: Path | None,
    branch: str,
    metadata: dict,
    records: list[dict],
    status: str,
) -> None:
    if path is None:
        return
    payload = {
        "status": status,
        "branch": branch,
        "metadata": metadata,
        "records": records,
    }
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # OneDrive and virus scanners can momentarily open the destination
    # without delete sharing on Windows.  Preserve the atomic replace
    # contract, but tolerate that transient lock instead of losing the
    # completed checkpoint batch.
    for attempt in range(50):
        try:
            os.replace(temporary, path)
            break
        except PermissionError:
            if os.name != "nt" or attempt == 49:
                raise
            time.sleep(0.1)

def transformed_seed_clauses(
    paths: list[Path],
    branch: str,
    pool,
) -> tuple[tuple[tuple[int, ...], ...], list[dict]]:
    """Upgrade prior pure-only chart records to exact applicability."""
    clauses = []
    sources = []
    for path in paths:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != branch:
            raise ValueError(f"seed branch mismatch: {path}")
        records = state.get("records", [])
        for index, record in enumerate(records):
            certificate = record.get("certificate", {})
            certificate_metadata = certificate.get("metadata", {})
            if (
                certificate.get("status") != "UNIT_IDEAL"
                or certificate_metadata.get(
                    "saturated_parameters"
                )
                != 0
            ):
                raise ValueError(
                    "seed chart is not a pure-only unit ideal: "
                    f"{path} record {index}"
                )
            closure = tuple(
                tuple(row) for row in record["closure_supports"]
            )
            tree = tuple(
                tuple(edge) for edge in record["gauge_tree"]
            )
            clauses.append(
                chart_clause(pool, closure, tree, branch)
            )
        sources.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "records": len(records),
            }
        )
    return tuple(sorted(set(clauses))), sources

def chart_orbit_seed_clauses(
    paths: list[Path],
    branch: str,
    pool,
) -> tuple[tuple[tuple[int, ...], ...], list[dict]]:
    """Transport every exact pure-only chart in prior ledgers."""
    clauses = set()
    sources_metadata = []
    for path in paths:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != branch:
            raise ValueError(f"chart-orbit seed branch mismatch: {path}")
        records = state.get("records", [])
        source_clauses = set()
        for index, record in enumerate(records):
            certificate = record.get("certificate", {})
            if (
                certificate.get("status") != "UNIT_IDEAL"
                or certificate.get("metadata", {}).get(
                    "saturated_parameters"
                )
                != 0
            ):
                raise ValueError(
                    "chart-orbit seed is not a pure-only unit ideal: "
                    f"{path} record {index}"
                )
            closure = tuple(
                tuple(map(int, row))
                for row in record["closure_supports"]
            )
            tree = tuple(
                tuple(map(int, edge))
                for edge in record["gauge_tree"]
            )
            source_clauses.update(
                chart_symmetry_orbit_clauses(
                    closure,
                    tree,
                    branch,
                    pool,
                )
            )
        clauses.update(source_clauses)
        sources_metadata.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "representative_records": len(records),
                "transported_clauses": len(source_clauses),
            }
        )
    return tuple(sorted(clauses)), sources_metadata

def zero_forest_orbit_clauses(
    paths: list[Path],
    branch: str,
    pool,
) -> tuple[tuple[tuple[int, ...], ...], list[dict]]:
    """Transport exact zero-forest closures through branch symmetries."""
    clauses = []
    sources_metadata = []
    source_colour_actions = source_colour_stabilizer(branch)
    for path in paths:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != branch:
            raise ValueError(f"orbit seed branch mismatch: {path}")
        records = state.get("records", [])
        source_clauses = set()
        source_closures = set()
        for index, record in enumerate(records):
            certificate = record.get("certificate", {})
            if (
                record.get("gauge_tree") not in ([], ())
                or certificate.get("status") != "UNIT_IDEAL"
                or certificate.get("metadata", {}).get(
                    "saturated_parameters"
                )
                != 0
            ):
                raise ValueError(
                    "orbit seed is not a zero-forest pure-only "
                    f"unit ideal: {path} record {index}"
                )
            closure = tuple(
                tuple(map(int, row))
                for row in record["closure_supports"]
            )
            for modes in (
                (0,) + permutation
                for permutation in itertools.permutations((1, 2, 3, 4))
            ):
                for sources, colours in source_colour_actions:
                    transformed = transform_support_array(
                        closure,
                        modes,
                        sources,
                        colours,
                    )
                    source_closures.add(transformed)
                    source_clauses.add(
                        chart_clause(
                            pool,
                            transformed,
                            (),
                            branch,
                        )
                    )
        clauses.extend(source_clauses)
        sources_metadata.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "representative_records": len(records),
                "transported_closures": len(source_closures),
                "transported_clauses": len(source_clauses),
                "mode_actions": 24,
                "source_colour_actions": len(
                    source_colour_actions
                ),
            }
        )
    return tuple(sorted(set(clauses))), sources_metadata

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--branch",
        choices=tuple(BRANCH_BACKBONES),
        required=True,
    )
    parser.add_argument("--models", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--relax-timeout",
        type=int,
        default=2,
        help="direct Singular timeout for each closure-enlargement trial",
    )
    parser.add_argument(
        "--skip-relax",
        action="store_true",
        help="learn the initial closure without enlargement trials",
    )
    parser.add_argument(
        "--relax-rows-only",
        action="store_true",
        help="try at most one whole-cell-group relaxation per row",
    )
    parser.add_argument(
        "--prefer-split",
        action="store_true",
        help="try the equivalent split-saturation system first",
    )
    parser.add_argument(
        "--gauge-tree-alternatives",
        type=int,
        default=0,
        help=(
            "try this many deterministic alternative maximal gauge "
            "forests before the long historical-tree calculation"
        ),
    )
    parser.add_argument(
        "--gauge-tree-portfolio-timeout",
        type=float,
        default=6.0,
        help="exact direct-Singular deadline per gauge-tree candidate",
    )
    parser.add_argument(
        "--try-empty-forest-first",
        action="store_true",
        help=(
            "probe a zero-pivot support-closure certificate before "
            "falling back to the maximal gauge forest"
        ),
    )
    parser.add_argument(
        "--empty-forest-timeout",
        type=float,
        default=0.75,
        help="split-Singular timeout for the zero-pivot probe",
    )
    parser.add_argument(
        "--transformed-seed-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "reuse pure-only unit-ideal records after upgrading their "
            "clauses to exact chart applicability"
        ),
    )
    parser.add_argument(
        "--zero-forest-orbit-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "transport exact zero-forest representative closures "
            "through branch-preserving mode/source/colour symmetries"
        ),
    )
    parser.add_argument(
        "--chart-orbit-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "transport all exact pure-only charts in a prior ledger "
            "through branch-preserving symmetries"
        ),
    )
    parser.add_argument(
        "--learn-chart-orbits",
        action="store_true",
        help=(
            "add the full branch-symmetry orbit of every newly "
            "certified chart"
        ),
    )
    parser.add_argument("--state", type=Path)
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=1,
        help="persist the full ledger after this many learned charts",
    )
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.models <= 0
        or args.timeout <= 0
        or args.relax_timeout <= 0
        or args.empty_forest_timeout <= 0
        or args.gauge_tree_alternatives < 0
        or args.gauge_tree_portfolio_timeout <= 0
        or args.checkpoint_every <= 0
    ):
        raise ValueError(
            "models and both CAS timeouts must be positive"
        )
    if args.skip_relax and args.relax_rows_only:
        raise ValueError(
            "skip-relax and relax-rows-only are mutually exclusive"
        )
    if args.try_empty_forest_first and not args.skip_relax:
        raise ValueError(
            "the empty-forest probe currently requires --skip-relax"
        )
    if not 15 <= args.min_available_percent < 100:
        raise ValueError(
            "memory floor must be at least 15 and below 100"
        )

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    branch_restriction = add_branch_restriction(
        cnf,
        pool,
        allowed,
        args.branch,
    )
    lex_leaders = add_stabilizer_lex_leaders(
        cnf,
        pool,
        args.branch,
    )
    base_clauses = len(cnf.clauses)
    transformed_clauses, seed_sources = transformed_seed_clauses(
        args.transformed_seed_state,
        args.branch,
        pool,
    )
    zero_orbit_clauses, zero_orbit_sources = (
        zero_forest_orbit_clauses(
            args.zero_forest_orbit_state,
            args.branch,
            pool,
        )
    )
    chart_orbit_clauses, chart_orbit_sources = (
        chart_orbit_seed_clauses(
            args.chart_orbit_state,
            args.branch,
            pool,
        )
    )
    seed_clause_set = (
        set(transformed_clauses)
        | set(zero_orbit_clauses)
        | set(chart_orbit_clauses)
    )
    seed_clauses = tuple(sorted(seed_clause_set))
    cnf.extend([list(clause) for clause in seed_clauses])
    metadata = {
        "catalogue_signatures": len(allowed),
        "chart_clause_schema": (
            "no entries outside closure plus present gauge pivots; "
            "normalized branch-fixed singleton conditions omitted"
        ),
        "gauge_schema": (
            "maximal acyclic actual-support forest prioritizing "
            "remaining closure-singleton pivots"
        ),
        "gauge_tree_portfolio": {
            "alternative_count": args.gauge_tree_alternatives,
            "trial_timeout_seconds": (
                args.gauge_tree_portfolio_timeout
            ),
            "ordering": "deterministic-min-equations-v1",
        },
        "closure_relaxation": {
            "strategy": "recursive-row-greedy-v1",
            "trial_timeout_seconds": args.relax_timeout,
            "modes": [1, 2, 3, 4],
        },
        "empty_forest_probe": {
            "enabled": args.try_empty_forest_first,
            "strategy": "split-only-v1",
            "timeout_seconds": args.empty_forest_timeout,
        },
        "branch_restriction": branch_restriction,
        "stabilizer_size": len(
            source_colour_stabilizer(args.branch)
        ),
        "lex_leaders": lex_leaders,
        "variables": pool.top,
        "base_clauses": base_clauses,
        "transformed_seed_sources": seed_sources,
        "transformed_seed_clauses": len(transformed_clauses),
        "zero_forest_orbit_sources": zero_orbit_sources,
        "zero_forest_orbit_clauses": len(zero_orbit_clauses),
        "chart_orbit_sources": chart_orbit_sources,
        "chart_orbit_clauses": len(chart_orbit_clauses),
        "combined_seed_clauses": len(seed_clauses),
        "learn_chart_orbits": args.learn_chart_orbits,
    }
    # Checkpoints round-trip through JSON; normalize tuples now so resume
    # comparisons are stable across processes.
    metadata = json.loads(json.dumps(metadata))
    records = []
    if args.state is not None and args.state.exists():
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if (
            state.get("branch") != args.branch
            or state.get("metadata") != metadata
        ):
            raise ValueError("state metadata does not match this branch")
        records = list(state.get("records", []))
        for record in records:
            if args.learn_chart_orbits:
                resumed_clauses = chart_symmetry_orbit_clauses(
                    tuple(
                        tuple(map(int, row))
                        for row in record["closure_supports"]
                    ),
                    tuple(
                        tuple(map(int, edge))
                        for edge in record["gauge_tree"]
                    ),
                    args.branch,
                    pool,
                )
            else:
                resumed_clauses = (tuple(record["clause"]),)
            for resumed_clause in resumed_clauses:
                if resumed_clause not in seed_clause_set:
                    cnf.append(list(resumed_clause))
                    seed_clause_set.add(resumed_clause)

    with Solver(
        name="cadical195",
        bootstrap_with=cnf.clauses,
    ) as solver:
        for _model_index in range(args.models):
            available = available_memory_percent()
            if available < args.min_available_percent:
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "PAUSED_MEMORY_FLOOR",
                )
                print(
                    json.dumps(
                        {
                            "status": "PAUSED_MEMORY_FLOOR",
                            "branch": args.branch,
                            "charts": len(records),
                            "available_percent": round(available, 3),
                            "min_available_percent": (
                                args.min_available_percent
                            ),
                        }
                    ),
                    flush=True,
                )
                return
            if not solver.solve():
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "UNSAT",
                )
                print(
                    json.dumps(
                        {
                            "status": "UNSAT",
                            "branch": args.branch,
                            "charts": len(records),
                            "seed_charts": len(seed_clauses),
                            "metadata": metadata,
                        }
                    ),
                    flush=True,
                )
                return
            model = solver.get_model()
            supports = SEMANTICS.supports_from_model(pool, model)
            indices = selected_signature_indices(
                pool,
                model,
                allowed,
            )
            initial_closure = closure_supports(supports)
            maximal_tree = gauge_tree(supports, initial_closure)
            initial_tree = maximal_tree
            gauge_portfolio = {
                "strategy": "disabled",
                "alternative_count": 0,
                "trial_timeout_seconds": (
                    args.gauge_tree_portfolio_timeout
                ),
                "trials": [],
                "selected_tree": initial_tree,
            }
            profile = tuple(
                sum(mask in (1, 2, 4) for mask in row)
                for row in supports
            )
            empty_forest_trial = None
            if args.try_empty_forest_first:
                empty_certificate = certify_chart(
                    initial_closure,
                    indices,
                    (),
                    args.empty_forest_timeout,
                    prefer_split=True,
                    split_only=True,
                )
                empty_forest_trial = {
                    "status": empty_certificate["status"],
                    "method": empty_certificate.get("method"),
                    "seconds": (
                        empty_certificate.get("cas")
                        or empty_certificate.get("split_cas")
                        or {}
                    ).get("elapsed_seconds"),
                }
                if empty_certificate["status"] == "UNIT_IDEAL":
                    initial_tree = ()
                    certificate = empty_certificate
                    gauge_portfolio = {
                        "strategy": "zero-forest-selected",
                        "alternative_count": 0,
                        "trial_timeout_seconds": (
                            args.empty_forest_timeout
                        ),
                        "trials": [],
                        "selected_tree": (),
                    }
                else:
                    if args.gauge_tree_alternatives:
                        (
                            portfolio_tree,
                            portfolio_certificate,
                            gauge_portfolio,
                        ) = certify_gauge_tree_portfolio(
                            supports,
                            initial_closure,
                            indices,
                            args.gauge_tree_alternatives,
                            args.gauge_tree_portfolio_timeout,
                        )
                        if portfolio_certificate is not None:
                            initial_tree = portfolio_tree
                            certificate = portfolio_certificate
                        else:
                            certificate = certify_chart(
                                initial_closure,
                                indices,
                                initial_tree,
                                args.timeout,
                                prefer_split=args.prefer_split,
                            )
                    else:
                        certificate = certify_chart(
                            initial_closure,
                            indices,
                            initial_tree,
                            args.timeout,
                            prefer_split=args.prefer_split,
                        )
            else:
                certificate = certify_chart(
                    initial_closure,
                    indices,
                    initial_tree,
                    args.timeout,
                    prefer_split=args.prefer_split,
                )
            if certificate["status"] != "UNIT_IDEAL":
                print(
                    json.dumps(
                        {
                            "status": "CAS_INCONCLUSIVE",
                            "branch": args.branch,
                            "coordinate_profile": profile,
                            "supports": supports,
                            "signature_indices": indices,
                            "gauge_tree": initial_tree,
                            "certificate": certificate,
                        }
                    ),
                    flush=True,
                )
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "CAS_INCONCLUSIVE",
                )
                return
            if args.skip_relax:
                closure = initial_closure
                tree = initial_tree
                relaxation = {
                    "strategy": "skipped",
                    "trial_timeout_seconds": args.relax_timeout,
                    "trials": [],
                    "accepted_cells": (),
                    "paused_for_memory": False,
                }
            else:
                closure, tree, relaxation = relax_chart_closure(
                    supports,
                    indices,
                    initial_closure,
                    args.relax_timeout,
                    args.min_available_percent,
                    recursive=not args.relax_rows_only,
                    prefer_split=args.prefer_split,
                )
            if closure != initial_closure:
                certificate = certify_chart(
                    closure,
                    indices,
                    tree,
                    args.timeout,
                    prefer_split=args.prefer_split,
                )
                if certificate["status"] != "UNIT_IDEAL":
                    raise AssertionError(
                        "accepted relaxed closure did not recertify"
                    )
            clause = chart_clause(
                pool,
                closure,
                tree,
                args.branch,
            )
            positive = {literal for literal in model if literal > 0}
            if any(
                (
                    abs(literal) in positive
                    if literal > 0
                    else abs(literal) not in positive
                )
                for literal in clause
            ):
                raise AssertionError(
                    "learned chart clause is not false on its model"
                )
            if args.learn_chart_orbits:
                learned_clauses = chart_symmetry_orbit_clauses(
                    closure,
                    tree,
                    args.branch,
                    pool,
                )
                if clause not in learned_clauses:
                    raise AssertionError(
                        "chart symmetry orbit lost its representative"
                    )
            else:
                learned_clauses = (clause,)
            new_learned_clauses = tuple(
                candidate
                for candidate in learned_clauses
                if candidate not in seed_clause_set
            )
            for learned_clause in new_learned_clauses:
                solver.add_clause(list(learned_clause))
                seed_clause_set.add(learned_clause)
            connectors = tuple(
                edge
                for edge in tree
                if closure[edge[0]][edge[1]] not in (1, 2, 4)
            )
            records.append(
                {
                    "clause": clause,
                    "supports": supports,
                    "initial_closure_supports": initial_closure,
                    "closure_supports": closure,
                    "signature_indices": indices,
                    "coordinate_profile": profile,
                    "gauge_tree": tree,
                    "connector_entries": connectors,
                    "relaxation": relaxation,
                    "empty_forest_trial": empty_forest_trial,
                    "gauge_tree_portfolio": gauge_portfolio,
                    "certificate": certificate,
                    "transported_orbit_clauses": len(
                        learned_clauses
                    ),
                    "new_transported_orbit_clauses": len(
                        new_learned_clauses
                    ),
                }
            )
            if len(records) % args.checkpoint_every == 0:
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "IN_PROGRESS",
                )
            print(
                json.dumps(
                    {
                        "status": "LEARNED",
                        "branch": args.branch,
                        "charts": len(records),
                        "seed_charts": len(seed_clauses),
                        "coordinate_profile": profile,
                        "support_components": 20 - len(maximal_tree),
                        "gauge_forest_edges": len(tree),
                        "relaxed_cells": len(
                            relaxation["accepted_cells"]
                        ),
                        "relaxation_trials": len(
                            relaxation["trials"]
                        ),
                        "connectors": len(connectors),
                        "clause_literals": len(clause),
                        "transported_orbit_clauses": len(
                            learned_clauses
                        ),
                        "new_transported_orbit_clauses": len(
                            new_learned_clauses
                        ),
                        "cas_method": certificate["method"],
                        "cas_seconds": certificate["cas"][
                            "elapsed_seconds"
                        ],
                    }
                ),
                flush=True,
            )

    checkpoint(
        args.state,
        args.branch,
        metadata,
        records,
        "IN_PROGRESS",
    )

if __name__ == "__main__":
    main()
