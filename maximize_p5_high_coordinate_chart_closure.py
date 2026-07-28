#!/usr/bin/env python3
"""Greedily enlarge one exact P5 chart while retaining its gauge tree."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import minimize_p5_high_coordinate_gauge_forest as MINIMIZE
import p5_high_coordinate_tree_chart_cegar as HIGH
import p5_pair_support_semantics as SEMANTICS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branch",
        choices=tuple(HIGH.BRANCH_BACKBONES),
        required=True,
    )
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--record-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=2)
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.record_index < 0
        or args.timeout <= 0
        or not 15 <= args.min_available_percent < 100
    ):
        raise ValueError("invalid fixed-gauge maximization arguments")

    raw_state = args.state.read_bytes()
    state = json.loads(raw_state)
    if state.get("branch") != args.branch:
        raise ValueError("source state branch changed")
    records = state.get("records", [])
    if args.record_index >= len(records):
        raise IndexError("record index is outside the source ledger")
    source = records[args.record_index]
    source_certificate = source.get("certificate", {})
    if (
        source_certificate.get("status") != "UNIT_IDEAL"
        or source_certificate.get("metadata", {}).get(
            "saturated_parameters"
        )
        != 0
    ):
        raise ValueError("source is not a pure-only unit-ideal chart")

    supports = tuple(
        tuple(map(int, row)) for row in source["supports"]
    )
    initial_closure = tuple(
        tuple(map(int, row))
        for row in source["closure_supports"]
    )
    tree = tuple(
        tuple(map(int, edge)) for edge in source["gauge_tree"]
    )
    current = [list(row) for row in initial_closure]
    indices = tuple(map(int, source["signature_indices"]))
    tree_cells = {
        (mode, source)
        for mode, source, _colour in tree
    }
    trials = []
    accepted_cells = []
    final_certificate = source_certificate

    def attempt(cells: tuple[tuple[int, int], ...]) -> None:
        nonlocal current, final_certificate
        active = tuple(
            (mode, source)
            for mode, source in cells
            if current[mode][source] in (0, 1, 2, 4)
        )
        if not active:
            return
        if (
            HIGH.available_memory_percent()
            < args.min_available_percent
        ):
            raise MemoryError(
                "available host memory fell below the requested floor"
            )
        proposed = [row[:] for row in current]
        for mode, source in active:
            proposed[mode][source] = 7
        proposed_closure = tuple(tuple(row) for row in proposed)
        certificate = HIGH.certify_chart(
            proposed_closure,
            indices,
            tree,
            args.timeout,
            try_split=False,
        )
        cas = (
            certificate.get("cas")
            or certificate.get("direct_cas")
            or {}
        )
        accepted = certificate["status"] == "UNIT_IDEAL"
        result = {
            "cells": active,
            "accepted": accepted,
            "status": certificate["status"],
            "seconds": cas.get("elapsed_seconds"),
        }
        trials.append(result)
        print(json.dumps(result), flush=True)
        if accepted:
            current = proposed
            accepted_cells.extend(active)
            final_certificate = certificate
            return
        if len(active) == 1:
            return
        midpoint = len(active) // 2
        attempt(active[:midpoint])
        attempt(active[midpoint:])

    # Mode zero is fixed by the normalized branch restriction.  Within
    # each other mode, try non-pivot cells before pivot cells because
    # freeing a non-pivot singleton deletes two clause conditions.
    for mode in SEMANTICS.MODES[1:]:
        cells = [
            (mode, source)
            for source in SEMANTICS.SOURCES
            if current[mode][source] in (0, 1, 2, 4)
        ]
        cells.sort(
            key=lambda cell: (
                cell in tree_cells,
                cell[1],
            )
        )
        attempt(tuple(cells))

    closure = tuple(tuple(row) for row in current)
    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(cnf, pool, allowed, args.branch)
    HIGH.add_stabilizer_lex_leaders(cnf, pool, args.branch)
    clause = HIGH.chart_clause(pool, closure, tree, args.branch)
    record = {
        "clause": clause,
        "supports": supports,
        "initial_closure_supports": initial_closure,
        "closure_supports": closure,
        "signature_indices": indices,
        "coordinate_profile": source["coordinate_profile"],
        "gauge_tree": tree,
        "connector_entries": tuple(
            edge
            for edge in tree
            if closure[edge[0]][edge[1]] not in (1, 2, 4)
        ),
        "relaxation": {
            "strategy": "fixed-gauge-recursive-row-greedy-v1",
            "trial_timeout_seconds": args.timeout,
            "trials": trials,
            "accepted_cells": accepted_cells,
            "paused_for_memory": False,
        },
        "empty_forest_trial": source.get("empty_forest_trial"),
        "gauge_tree_portfolio": source.get(
            "gauge_tree_portfolio", {}
        ),
        "certificate": final_certificate,
    }
    payload = {
        "status": "SEED",
        "branch": args.branch,
        "metadata": {
            "source_state": args.state.as_posix(),
            "source_state_sha256": hashlib.sha256(
                raw_state
            ).hexdigest(),
            "source_state_status": state.get("status"),
            "source_record_index": args.record_index,
            "chart_clause_schema": (
                "no entries outside closure plus retained gauge "
                "pivots; normalized branch-fixed singleton "
                "conditions omitted"
            ),
            "closure_relaxation": (
                "fixed-gauge-recursive-row-greedy-v1"
            ),
        },
        "records": [record],
    }
    MINIMIZE.atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "branch": args.branch,
                "source_record_index": args.record_index,
                "accepted_cells": len(accepted_cells),
                "initial_clause_literals": len(source["clause"]),
                "relaxed_clause_literals": len(clause),
                "output": args.output.as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
