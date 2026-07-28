#!/usr/bin/env python3
"""Certify zero-pivot support closures for selected high-coordinate records."""

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
    parser.add_argument(
        "--record-index",
        type=int,
        action="append",
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--prefer-split", action="store_true")
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.timeout <= 0
        or not 15 <= args.min_available_percent < 100
        or any(index < 0 for index in args.record_index)
        or len(set(args.record_index)) != len(args.record_index)
    ):
        raise ValueError("invalid batch arguments")

    raw_state = args.state.read_bytes()
    state = json.loads(raw_state)
    if state.get("branch") != args.branch:
        raise ValueError("source state branch changed")
    source_records = state.get("records", [])
    if any(index >= len(source_records) for index in args.record_index):
        raise IndexError("record index is outside the source ledger")

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(cnf, pool, allowed, args.branch)
    HIGH.add_stabilizer_lex_leaders(cnf, pool, args.branch)

    output_records = []
    results = []
    for index in args.record_index:
        if (
            HIGH.available_memory_percent()
            < args.min_available_percent
        ):
            raise MemoryError(
                "available host memory fell below the requested floor"
            )
        source = source_records[index]
        source_certificate = source.get("certificate", {})
        if (
            source_certificate.get("status") != "UNIT_IDEAL"
            or source_certificate.get("metadata", {}).get(
                "saturated_parameters"
            )
            != 0
        ):
            raise ValueError(
                f"record {index} is not a pure-only unit-ideal chart"
            )
        closure = tuple(
            tuple(map(int, row))
            for row in source["closure_supports"]
        )
        supports = tuple(
            tuple(map(int, row)) for row in source["supports"]
        )
        signature_indices = tuple(
            map(int, source["signature_indices"])
        )
        original_forest = tuple(
            tuple(map(int, edge)) for edge in source["gauge_tree"]
        )
        certificate = HIGH.certify_chart(
            closure,
            signature_indices,
            (),
            args.timeout,
            prefer_split=args.prefer_split,
        )
        certified = certificate["status"] == "UNIT_IDEAL"
        result = {
            "source_record_index": index,
            "certified": certified,
            "method": certificate.get("method"),
            "original_forest_edges": len(original_forest),
        }
        results.append(result)
        print(json.dumps(result), flush=True)
        if not certified:
            continue

        clause = HIGH.chart_clause(pool, closure, (), args.branch)
        output_records.append(
            {
                "clause": clause,
                "supports": supports,
                "initial_closure_supports": source.get(
                    "initial_closure_supports",
                    source["closure_supports"],
                ),
                "closure_supports": closure,
                "signature_indices": signature_indices,
                "coordinate_profile": source[
                    "coordinate_profile"
                ],
                "gauge_tree": (),
                "connector_entries": (),
                "relaxation": source.get("relaxation", {}),
                "forest_minimization": {
                    "strategy": "direct-empty-forest-v1",
                    "original_edges": len(original_forest),
                    "remaining_edges": 0,
                    "timeout_seconds": args.timeout,
                    "prefer_split": args.prefer_split,
                    "trials": [
                        {
                            "removed_edges": original_forest,
                            "accepted": True,
                            "remaining_edges": 0,
                            "method": certificate.get("method"),
                            "certificate_status": certificate[
                                "status"
                            ],
                        }
                    ],
                },
                "certificate": certificate,
            }
        )

    payload = {
        "status": "SEED",
        "branch": args.branch,
        "metadata": {
            "source_state": args.state.as_posix(),
            "source_state_sha256": hashlib.sha256(
                raw_state
            ).hexdigest(),
            "source_state_status": state.get("status"),
            "source_record_indices": args.record_index,
            "chart_clause_schema": (
                "no entries outside closure plus present gauge pivots; "
                "normalized branch-fixed singleton conditions omitted"
            ),
            "forest_minimization": "direct-empty-forest-v1",
            "attempts": len(results),
            "certified": len(output_records),
        },
        "records": output_records,
    }
    MINIMIZE.atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "branch": args.branch,
                "attempts": len(results),
                "certified_zero_forests": len(output_records),
                "output": args.output.as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
