#!/usr/bin/env python3
"""Greedily enlarge one exact zero-forest high-coordinate P5 closure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu import atomic_json as MINIMIZE
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS


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
        raise ValueError("invalid closure-maximization arguments")

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
        source.get("gauge_tree") not in ([], ())
        or source_certificate.get("status") != "UNIT_IDEAL"
        or source_certificate.get("metadata", {}).get(
            "saturated_parameters"
        )
        != 0
    ):
        raise ValueError(
            "source is not a zero-forest pure-only unit ideal"
        )

    supports = tuple(
        tuple(map(int, row)) for row in source["supports"]
    )
    initial_closure = tuple(
        tuple(map(int, row))
        for row in source["closure_supports"]
    )
    current = [list(row) for row in initial_closure]
    indices = tuple(map(int, source["signature_indices"]))
    trials = []
    accepted_cells = []
    final_certificate = source_certificate

    def attempt(cells: tuple[tuple[int, int], ...]) -> None:
        nonlocal current, final_certificate
        active = tuple(
            (mode, source)
            for mode, source in cells
            if current[mode][source] in (1, 2, 4)
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
            (),
            args.timeout,
            prefer_split=True,
            split_only=True,
        )
        accepted = certificate["status"] == "UNIT_IDEAL"
        result = {
            "cells": active,
            "accepted": accepted,
            "status": certificate["status"],
            "seconds": (
                certificate.get("cas")
                or certificate.get("split_cas")
                or {}
            ).get("elapsed_seconds"),
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

    # Mode zero is fixed by the normalized branch restriction.
    for mode in SEMANTICS.MODES[1:]:
        attempt(
            tuple(
                (mode, source)
                for source in SEMANTICS.SOURCES
                if current[mode][source] in (1, 2, 4)
            )
        )

    closure = tuple(tuple(row) for row in current)
    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(cnf, pool, allowed, args.branch)
    HIGH.add_stabilizer_lex_leaders(cnf, pool, args.branch)
    clause = HIGH.chart_clause(pool, closure, (), args.branch)
    record = {
        "clause": clause,
        "supports": supports,
        "initial_closure_supports": initial_closure,
        "closure_supports": closure,
        "signature_indices": indices,
        "coordinate_profile": source["coordinate_profile"],
        "gauge_tree": (),
        "connector_entries": (),
        "relaxation": {
            "strategy": "zero-forest-recursive-row-greedy-v1",
            "trial_timeout_seconds": args.timeout,
            "trials": trials,
            "accepted_cells": accepted_cells,
            "paused_for_memory": False,
        },
        "forest_minimization": source.get(
            "forest_minimization", {}
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
                "no entries outside closure; no gauge-pivot "
                "presence assumptions; normalized branch-fixed "
                "singleton conditions omitted"
            ),
            "closure_relaxation": (
                "zero-forest-recursive-row-greedy-v1"
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
                "initial_clause_literals": len(
                    source["clause"]
                ),
                "relaxed_clause_literals": len(clause),
                "output": args.output.as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
