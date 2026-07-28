#!/usr/bin/env python3
"""Combine self-contained zero-pivot high-coordinate seed records."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import minimize_p5_high_coordinate_gauge_forest as MINIMIZE
import p5_high_coordinate_tree_chart_cegar as HIGH


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
    parser.add_argument(
        "--deduplicate-identical-closures",
        action="store_true",
        help=(
            "retain one deterministic representative when the closure, "
            "clause, split source, and algebra metadata are identical"
        ),
    )
    parser.add_argument(
        "--select-zero-forest-only",
        action="store_true",
        help=(
            "skip records with nonempty gauge forests while retaining the "
            "same exact validation for selected zero-forest records"
        ),
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records = []
    provenance = []
    for path in args.state:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != args.branch:
            raise ValueError(f"branch mismatch in {path}")
        state_records = state.get("records", [])
        selected_records = 0
        for index, record in enumerate(state_records):
            if (
                args.select_zero_forest_only
                and record.get("gauge_tree") not in ([], ())
            ):
                continue
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
                    f"{path} record {index} is not a zero-pivot "
                    "pure-only certificate"
                )
            records.append(record)
            selected_records += 1
        provenance.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "source_records": len(state_records),
                "selected_records": selected_records,
                "skipped_records": len(state_records) - selected_records,
            }
        )

    input_records = len(records)
    duplicate_records_removed = 0
    if args.deduplicate_identical_closures:
        by_closure = {}
        for record in records:
            closure = tuple(
                tuple(map(int, row))
                for row in record["closure_supports"]
            )
            previous = by_closure.get(closure)
            if previous is None:
                by_closure[closure] = record
                continue
            left_certificate = previous["certificate"]
            right_certificate = record["certificate"]
            if (
                tuple(map(int, previous["clause"]))
                != tuple(map(int, record["clause"]))
                or left_certificate.get("method") != "split"
                or right_certificate.get("method") != "split"
                or left_certificate.get("split_source_sha256")
                != right_certificate.get("split_source_sha256")
                or left_certificate.get("metadata")
                != right_certificate.get("metadata")
            ):
                raise AssertionError(
                    "duplicate closure has nonidentical algebra data"
                )

            def representative_key(candidate: dict) -> tuple:
                certificate = candidate["certificate"]
                return (
                    certificate.get("cas", {}).get(
                        "elapsed_seconds", float("inf")
                    ),
                    certificate["source_sha256"],
                    tuple(map(int, candidate["signature_indices"])),
                )

            if representative_key(record) < representative_key(
                previous
            ):
                by_closure[closure] = record
            duplicate_records_removed += 1
        records = list(by_closure.values())

    clauses = {
        tuple(map(int, record["clause"])) for record in records
    }
    closures = {
        tuple(
            tuple(map(int, row))
            for row in record["closure_supports"]
        )
        for record in records
    }
    source_hashes = {
        record["certificate"]["source_sha256"]
        for record in records
    }
    if not (
        len(clauses)
        == len(closures)
        == len(source_hashes)
        == len(records)
    ):
        raise AssertionError("packaged zero-pivot records are not unique")

    payload = {
        "status": "EXACT_FINITE_SEED_SET",
        "branch": args.branch,
        "metadata": {
            "scope": (
                "self-contained exact zero-pivot support-closure "
                "certificates; not a complete branch cover"
            ),
            "chart_clause_schema": (
                "no entries outside closure; no gauge-pivot presence "
                "assumptions; normalized branch-fixed singleton "
                "conditions omitted"
            ),
            "records": len(records),
            "input_records": input_records,
            "duplicate_records_removed": duplicate_records_removed,
            "unique_clauses": len(clauses),
            "unique_closures": len(closures),
            "unique_source_hashes": len(source_hashes),
            "provenance": provenance,
        },
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    MINIMIZE.atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "branch": args.branch,
                "records": len(records),
                "output": args.output.as_posix(),
                "output_sha256": hashlib.sha256(
                    args.output.read_bytes()
                ).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
