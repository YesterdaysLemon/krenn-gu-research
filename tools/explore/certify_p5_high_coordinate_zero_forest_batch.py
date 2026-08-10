#!/usr/bin/env python3
"""Certify zero-pivot support closures for selected high-coordinate records."""

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
    selectors = parser.add_mutually_exclusive_group(required=True)
    selectors.add_argument(
        "--record-index",
        type=int,
        action="append",
    )
    selectors.add_argument(
        "--all-nonzero-forest",
        action="store_true",
        help="test every source record that still has a gauge pivot",
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--prefer-split", action="store_true")
    parser.add_argument("--checkpoint-every", type=int, default=20)
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.timeout <= 0
        or args.checkpoint_every <= 0
        or not 15 <= args.min_available_percent < 100
        or any(index < 0 for index in (args.record_index or ()))
        or len(set(args.record_index or ()))
        != len(args.record_index or ())
    ):
        raise ValueError("invalid batch arguments")

    raw_state = args.state.read_bytes()
    state = json.loads(raw_state)
    if state.get("branch") != args.branch:
        raise ValueError("source state branch changed")
    source_records = state.get("records", [])
    selected_indices = (
        [
            index
            for index, record in enumerate(source_records)
            if record.get("gauge_tree")
        ]
        if args.all_nonzero_forest
        else list(args.record_index or ())
    )
    if any(index >= len(source_records) for index in selected_indices):
        raise IndexError("record index is outside the source ledger")

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(cnf, pool, allowed, args.branch)
    HIGH.add_stabilizer_lex_leaders(cnf, pool, args.branch)

    output_records = []
    results = []

    def write_payload(status: str) -> None:
        payload = {
            "status": status,
            "branch": args.branch,
            "metadata": {
                "source_state": args.state.as_posix(),
                "source_state_sha256": hashlib.sha256(
                    raw_state
                ).hexdigest(),
                "source_state_status": state.get("status"),
                "source_record_indices": selected_indices,
                "chart_clause_schema": (
                    "no entries outside closure plus present gauge "
                    "pivots; normalized branch-fixed singleton "
                    "conditions omitted"
                ),
                "forest_minimization": "direct-empty-forest-v1",
                "attempts_planned": len(selected_indices),
                "attempts_completed": len(results),
                "certified": len(output_records),
            },
            "records": output_records,
        }
        MINIMIZE.atomic_write(args.output, payload)

    for position, index in enumerate(selected_indices, start=1):
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
        if certified:
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
        if position % args.checkpoint_every == 0:
            write_payload("IN_PROGRESS_ZERO_FOREST_BATCH")

    write_payload("SEED")
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
