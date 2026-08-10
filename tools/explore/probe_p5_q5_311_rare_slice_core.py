#!/usr/bin/env python3
"""Run the bounded q5_311 rare-slice Singular probe."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu import p5_high_coordinate as HIGH  # noqa: E402
from krenn_gu.p5_q5_311_program import build_program  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument(
        "--record-index",
        type=int,
        action="append",
        required=True,
    )
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--source-output", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--quiet-progress", action="store_true")
    parser.add_argument(
        "--split-only",
        action="store_true",
        help=(
            "skip the direct product saturation and run only the "
            "equivalent split-inverse formulation"
        ),
    )
    parser.add_argument(
        "--basis-algorithm",
        choices=("slimgb", "std"),
        default="slimgb",
    )
    parser.add_argument(
        "--inverse-first",
        action="store_true",
        help="place split inverse variables before chart variables",
    )
    parser.add_argument(
        "--empty-forest",
        action="store_true",
        help=(
            "discard each stored gauge forest and probe the same "
            "closure without pivot-nonvanishing assumptions"
        ),
    )
    parser.add_argument(
        "--include-majority-pure",
        action="store_true",
        help=(
            "also require the majority pure coefficient to be nonzero "
            "while retaining only rare-colour mixed equations"
        ),
    )
    args = parser.parse_args()
    if any(index < 0 for index in args.record_index) or args.timeout <= 0:
        raise ValueError("invalid rare-slice probe arguments")
    if args.source_output and len(args.record_index) != 1:
        raise ValueError(
            "--source-output requires exactly one record index"
        )

    raw = args.state.read_bytes()
    state = json.loads(raw)
    if state.get("branch") != "q5_311":
        raise ValueError("rare-slice probe requires q5_311")
    records = state.get("records", [])
    if any(index >= len(records) for index in args.record_index):
        raise IndexError("record index is outside the state ledger")

    results = []
    for index in args.record_index:
        record = records[index]
        if args.empty_forest:
            record = {**record, "gauge_tree": ()}
        program, split_program, metadata = build_program(
            record,
            args.include_majority_pure,
            args.basis_algorithm,
            args.inverse_first,
        )
        if args.source_output:
            args.source_output.write_text(program, encoding="utf-8")
        direct = (
            {
                "status": "SKIPPED",
                "elapsed_seconds": 0.0,
            }
            if args.split_only
            else HIGH.run_singular(program, args.timeout)
        )
        split = None
        method = "direct"
        result = direct
        if direct["status"] != "UNIT_IDEAL":
            split = HIGH.run_singular(split_program, args.timeout)
            result = split
            if split["status"] == "UNIT_IDEAL":
                method = "split"
            else:
                method = "inconclusive"
        results.append(
            {
                "record_index": index,
                "verified": result["status"] == "UNIT_IDEAL",
                "method": method,
                "source_sha256": HIGH.sha256_text(program),
                "split_source_sha256": HIGH.sha256_text(
                    split_program
                ),
                "metadata": metadata,
                "direct_cas": direct,
                "split_cas": split,
                "cas": result,
            }
        )
        if not args.quiet_progress:
            print(
                json.dumps(
                    {
                        "record_index": index,
                        "status": result["status"],
                        "seconds": result["elapsed_seconds"],
                        "rare_mixed_equations": metadata[
                            "rare_mixed_equations"
                        ],
                    }
                ),
                flush=True,
            )

    payload = {
        "verified": all(result["verified"] for result in results),
        "scope": (
            "selected exact q5_311 charts under only the simultaneous "
            "rare-colour P4 slice equations"
        ),
        "state": args.state.as_posix(),
        "state_sha256": hashlib.sha256(raw).hexdigest(),
        "records_tested": len(results),
        "empty_forest_override": args.empty_forest,
        "unit_ideals": sum(
            result["verified"] for result in results
        ),
        "inconclusive": sum(
            not result["verified"] for result in results
        ),
        "results": results,
        "global_conjecture_resolved": False,
    }
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(
            json.dumps(
                {
                    "verified": payload["verified"],
                    "records_tested": payload["records_tested"],
                    "unit_ideals": payload["unit_ideals"],
                    "inconclusive": payload["inconclusive"],
                    "output": args.output.as_posix(),
                },
                indent=2,
            )
        )
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
