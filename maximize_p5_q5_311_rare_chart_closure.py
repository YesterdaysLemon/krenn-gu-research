#!/usr/bin/env python3
"""Greedily enlarge one exact q5_311 rare-slice chart."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import minimize_p5_high_coordinate_gauge_forest as MINIMIZE
import p5_high_coordinate_tree_chart_cegar as HIGH
import p5_pair_support_semantics as SEMANTICS
import p5_q5_311_rare_slice_cegar as CEGAR


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--record-index", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--direct-timeout", type=float, default=1)
    parser.add_argument("--split-timeout", type=float, default=3)
    parser.add_argument(
        "--retry-split-timeout",
        type=float,
        default=0,
        help=(
            "after the greedy pass, retry each remaining singleton cell "
            "with this longer split deadline; zero disables retries"
        ),
    )
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.record_index < 0
        or args.direct_timeout <= 0
        or args.split_timeout <= 0
        or args.retry_split_timeout < 0
        or (
            args.retry_split_timeout
            and args.retry_split_timeout <= args.split_timeout
        )
        or not 15 <= args.min_available_percent < 100
    ):
        raise ValueError("invalid rare maximization arguments")

    raw_state = args.state.read_bytes()
    state = json.loads(raw_state)
    if state.get("branch") != CEGAR.BRANCH:
        raise ValueError("rare maximizer requires q5_311")
    records = state.get("records", [])
    if args.record_index >= len(records):
        raise IndexError("record index is outside source ledger")
    source = records[args.record_index]
    if (
        source.get("certificate", {}).get("status")
        != "UNIT_IDEAL"
    ):
        raise ValueError("source is not an exact rare chart")

    supports = tuple(
        tuple(map(int, row)) for row in source["supports"]
    )
    initial_closure = tuple(
        tuple(map(int, row))
        for row in source["closure_supports"]
    )
    tree = tuple(
        tuple(map(int, edge))
        for edge in source["gauge_tree"]
    )
    signatures = tuple(map(int, source["signature_indices"]))
    current = [list(row) for row in initial_closure]
    tree_cells = {
        (mode, source_index)
        for mode, source_index, _colour in tree
    }
    accepted_cells = []
    trials = []
    final_certificate = source["certificate"]

    def attempt(
        cells: tuple[tuple[int, int], ...],
        *,
        split_timeout: float | None = None,
        recursive: bool = True,
        retry: bool = False,
    ) -> None:
        nonlocal current, final_certificate
        active = tuple(
            (mode, source_index)
            for mode, source_index in cells
            if current[mode][source_index] in (0, 1, 2, 4)
        )
        if not active:
            return
        if (
            HIGH.available_memory_percent()
            < args.min_available_percent
        ):
            raise MemoryError(
                "available host memory fell below requested floor"
            )
        proposed = [row[:] for row in current]
        for mode, source_index in active:
            proposed[mode][source_index] = 7
        closure = tuple(tuple(row) for row in proposed)
        candidate = {
            "supports": supports,
            "closure_supports": closure,
            "gauge_tree": tree,
        }
        effective_split_timeout = (
            args.split_timeout
            if split_timeout is None
            else split_timeout
        )
        certificate = (
            CEGAR.split_certificate(
                candidate,
                effective_split_timeout,
            )
            if not tree
            else CEGAR.certificate(
                candidate,
                args.direct_timeout,
                effective_split_timeout,
            )
        )
        cas = (
            certificate.get("cas")
            or certificate.get("split_cas")
            or {}
        )
        accepted = certificate["status"] == "UNIT_IDEAL"
        trial = {
            "cells": active,
            "accepted": accepted,
            "status": certificate["status"],
            "method": certificate.get("method"),
            "seconds": cas.get("elapsed_seconds"),
            "split_timeout_seconds": effective_split_timeout,
            "retry": retry,
        }
        trials.append(trial)
        print(json.dumps(trial), flush=True)
        if accepted:
            current = proposed
            accepted_cells.extend(active)
            final_certificate = certificate
            return
        if len(active) == 1 or not recursive:
            return
        midpoint = len(active) // 2
        attempt(active[:midpoint], split_timeout=split_timeout)
        attempt(active[midpoint:], split_timeout=split_timeout)

    for mode in SEMANTICS.MODES[1:]:
        cells = [
            (mode, source_index)
            for source_index in SEMANTICS.SOURCES
            if current[mode][source_index] in (0, 1, 2, 4)
        ]
        cells.sort(
            key=lambda cell: (
                cell in tree_cells,
                cell[1],
            )
        )
        attempt(tuple(cells))

    if args.retry_split_timeout:
        for mode in SEMANTICS.MODES[1:]:
            for source_index in SEMANTICS.SOURCES:
                if current[mode][source_index] not in (0, 1, 2, 4):
                    continue
                attempt(
                    ((mode, source_index),),
                    split_timeout=args.retry_split_timeout,
                    recursive=False,
                    retry=True,
                )

    closure = tuple(tuple(row) for row in current)
    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(
        cnf,
        pool,
        allowed,
        CEGAR.BRANCH,
    )
    HIGH.add_stabilizer_lex_leaders(
        cnf,
        pool,
        CEGAR.BRANCH,
    )
    clause = HIGH.chart_clause(
        pool,
        closure,
        tree,
        CEGAR.BRANCH,
    )
    profile = source.get(
        "coordinate_profile",
        tuple(
            sum(mask in (1, 2, 4) for mask in row)
            for row in supports
        ),
    )
    record = {
        "source_record_index": args.record_index,
        "clause": clause,
        "supports": supports,
        "initial_closure_supports": initial_closure,
        "closure_supports": closure,
        "signature_indices": signatures,
        "coordinate_profile": profile,
        "gauge_tree": tree,
        "relaxation": {
            "strategy": "rare-fixed-gauge-recursive-row-greedy-v1",
            "direct_timeout_seconds": args.direct_timeout,
            "split_timeout_seconds": args.split_timeout,
            "retry_split_timeout_seconds": (
                args.retry_split_timeout or None
            ),
            "trials": trials,
            "accepted_cells": accepted_cells,
        },
        "certificate": final_certificate,
    }
    payload = {
        "status": "EXACT_FINITE_RARE_SLICE_SEED_SET",
        "branch": CEGAR.BRANCH,
        "metadata": {
            "scope": (
                "one enlarged exact rare-slice chart; not a complete "
                "branch cover"
            ),
            "source_state": args.state.as_posix(),
            "source_state_sha256": hashlib.sha256(
                raw_state
            ).hexdigest(),
            "source_state_status": state.get("status"),
            "source_record_index": args.record_index,
            "accepted_cells": len(accepted_cells),
            "majority_mixed_equations": 0,
            "global_conjecture_resolved": False,
        },
        "records": [record],
    }
    MINIMIZE.atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "source_record_index": args.record_index,
                "accepted_cells": len(accepted_cells),
                "initial_clause_literals": len(source["clause"]),
                "relaxed_clause_literals": len(clause),
                "output": args.output.as_posix(),
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
