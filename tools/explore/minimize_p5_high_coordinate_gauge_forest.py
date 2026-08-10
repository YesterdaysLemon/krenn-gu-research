#!/usr/bin/env python3
"""Greedily strengthen one high-coordinate chart by deleting gauge pivots."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from pathlib import Path

import p5_high_coordinate_tree_chart_cegar as HIGH
import p5_pair_support_semantics as SEMANTICS


def atomic_write(path: Path, payload: dict) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    for attempt in range(50):
        try:
            os.replace(temporary, path)
            return
        except PermissionError:
            if os.name != "nt" or attempt == 49:
                raise
            time.sleep(0.1)


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
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument(
        "--prefer-split",
        action="store_true",
        help="try the equivalent split-saturation system first",
    )
    parser.add_argument(
        "--direct-empty-forest",
        action="store_true",
        help=(
            "test the zero-pivot closure directly instead of greedy "
            "one-edge deletion"
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
        or args.timeout <= 0
        or not 15 <= args.min_available_percent < 100
    ):
        raise ValueError("invalid minimization arguments")

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

    closure = tuple(
        tuple(map(int, row)) for row in source["closure_supports"]
    )
    supports = tuple(
        tuple(map(int, row)) for row in source["supports"]
    )
    indices = tuple(map(int, source["signature_indices"]))
    original_forest = tuple(
        tuple(map(int, edge)) for edge in source["gauge_tree"]
    )
    forest = list(original_forest)
    trials = []
    final_certificate = source_certificate
    removal_groups = (
        (original_forest,)
        if args.direct_empty_forest
        else tuple((edge,) for edge in original_forest)
    )
    for removal_group in removal_groups:
        available = HIGH.available_memory_percent()
        if available < args.min_available_percent:
            raise MemoryError(
                "available host memory fell below the requested floor"
            )
        removed = set(removal_group)
        candidate = tuple(item for item in forest if item not in removed)
        certificate = HIGH.certify_chart(
            closure,
            indices,
            candidate,
            args.timeout,
            prefer_split=args.prefer_split,
        )
        accepted = certificate["status"] == "UNIT_IDEAL"
        trials.append(
            {
                "removed_edges": removal_group,
                "accepted": accepted,
                "remaining_edges": (
                    len(candidate) if accepted else len(forest)
                ),
                "method": certificate.get("method"),
                "certificate_status": certificate["status"],
            }
        )
        if accepted:
            forest = list(candidate)
            final_certificate = certificate
        print(json.dumps(trials[-1]), flush=True)
    if args.direct_empty_forest and forest:
        raise RuntimeError("zero-pivot closure was not certified")

    allowed = SEMANTICS.finite_field_local_signatures()
    _cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(_cnf, pool, allowed, args.branch)
    HIGH.add_stabilizer_lex_leaders(_cnf, pool, args.branch)
    minimized_forest = tuple(forest)
    clause = HIGH.chart_clause(
        pool, closure, minimized_forest, args.branch
    )
    connectors = tuple(
        edge
        for edge in minimized_forest
        if closure[edge[0]][edge[1]] not in (1, 2, 4)
    )
    record = {
        "clause": clause,
        "supports": supports,
        "initial_closure_supports": source.get(
            "initial_closure_supports", source["closure_supports"]
        ),
        "closure_supports": closure,
        "signature_indices": indices,
        "coordinate_profile": source["coordinate_profile"],
        "gauge_tree": minimized_forest,
        "connector_entries": connectors,
        "relaxation": source.get("relaxation", {}),
        "forest_minimization": {
            "strategy": (
                "direct-empty-forest-v1"
                if args.direct_empty_forest
                else "greedy-deletion-v1"
            ),
            "original_edges": len(original_forest),
            "remaining_edges": len(minimized_forest),
            "timeout_seconds": args.timeout,
            "prefer_split": args.prefer_split,
            "trials": trials,
        },
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
                "no entries outside closure plus present gauge pivots; "
                "normalized branch-fixed singleton conditions omitted"
            ),
            "forest_minimization": (
                "direct-empty-forest-v1"
                if args.direct_empty_forest
                else "greedy-deletion-v1"
            ),
        },
        "records": [record],
    }
    atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "branch": args.branch,
                "source_record_index": args.record_index,
                "original_forest_edges": len(original_forest),
                "minimized_forest_edges": len(minimized_forest),
                "clause_literals": len(clause),
                "output": args.output.as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
