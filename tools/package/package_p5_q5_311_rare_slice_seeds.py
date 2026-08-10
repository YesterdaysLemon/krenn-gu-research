#!/usr/bin/env python3
"""Bind q5_311 chart records to exact rare-slice certificates."""

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

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "tools/explore")

from krenn_gu import atomic_json as MINIMIZE
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_q5_311_program as RARE


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--probe", type=Path, required=True)
    parser.add_argument(
        "--allow-inconclusive",
        action="store_true",
        help="package only certified records when the probe has timeouts",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    raw_state = args.state.read_bytes()
    raw_probe = args.probe.read_bytes()
    state = json.loads(raw_state)
    probe = json.loads(raw_probe)
    source_records = state.get("records", [])
    results = probe.get("results", [])
    if (
        state.get("branch") != "q5_311"
        or probe.get("state_sha256")
        != hashlib.sha256(raw_state).hexdigest()
        or probe.get("records_tested") != len(results)
        or len(
            {
                int(result.get("record_index", -1))
                for result in results
            }
        )
        != len(results)
        or any(
            not 0 <= int(result.get("record_index", -1))
            < len(source_records)
            for result in results
        )
    ):
        raise AssertionError("state/probe binding changed")
    if (
        not args.allow_inconclusive
        and any(not result.get("verified") for result in results)
    ):
        raise ValueError("probe contains inconclusive records")

    allowed = SEMANTICS.finite_field_local_signatures()
    _cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(_cnf, pool, allowed, "q5_311")
    HIGH.add_stabilizer_lex_leaders(_cnf, pool, "q5_311")

    records = []
    skipped = []
    empty_forest_override = bool(
        probe.get("empty_forest_override", False)
    )
    for result in results:
        index = int(result["record_index"])
        if not result.get("verified"):
            skipped.append(index)
            continue
        source = source_records[index]
        if empty_forest_override:
            source = {**source, "gauge_tree": ()}
        program, split_program, metadata = RARE.build_program(
            source,
            include_majority_pure=True,
            basis_algorithm=result["metadata"].get(
                "basis_algorithm",
                "slimgb",
            ),
            inverse_first=result["metadata"].get(
                "split_inverse_variables_first",
                False,
            ),
        )
        method = result.get("method")
        stored_metadata = result["metadata"]
        normalized_metadata = json.loads(json.dumps(metadata))
        if (
            method not in ("direct", "split")
            or result.get("cas", {}).get("status") != "UNIT_IDEAL"
            or result.get("source_sha256")
            != HIGH.sha256_text(program)
            or result.get("split_source_sha256")
            != HIGH.sha256_text(split_program)
            or stored_metadata
            != {
                key: normalized_metadata[key]
                for key in stored_metadata
            }
        ):
            raise AssertionError(
                f"rare certificate {index} changed"
            )
        closure = tuple(
            tuple(map(int, row))
            for row in source["closure_supports"]
        )
        tree = tuple(
            tuple(map(int, edge))
            for edge in source["gauge_tree"]
        )
        clause = HIGH.chart_clause(
            pool,
            closure,
            tree,
            "q5_311",
        )
        if (
            not empty_forest_override
            and tuple(map(int, source["clause"])) != clause
        ):
            raise AssertionError(f"chart clause {index} changed")
        records.append(
            {
                "source_record_index": index,
                "clause": clause,
                "supports": source["supports"],
                "closure_supports": closure,
                "signature_indices": source["signature_indices"],
                "gauge_tree": tree,
                "certificate": {
                    "status": "UNIT_IDEAL",
                    "method": method,
                    "source_sha256": result["source_sha256"],
                    "split_source_sha256": result[
                        "split_source_sha256"
                    ],
                    "metadata": normalized_metadata,
                    "cas": result["cas"],
                },
            }
        )

    payload = {
        "status": "EXACT_FINITE_RARE_SLICE_SEED_SET",
        "branch": "q5_311",
        "metadata": {
            "scope": (
                "exact rare mixed slices plus all three pure "
                "nonvanishing conditions; not a complete branch cover"
            ),
            "source_state": args.state.as_posix(),
            "source_state_sha256": hashlib.sha256(raw_state).hexdigest(),
            "probe": args.probe.as_posix(),
            "probe_sha256": hashlib.sha256(raw_probe).hexdigest(),
            "source_records": len(source_records),
            "probed_records": len(results),
            "certified_records": len(records),
            "skipped_inconclusive_records": skipped,
            "empty_forest_override": empty_forest_override,
            "majority_mixed_equations": 0,
            "global_conjecture_resolved": False,
        },
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    MINIMIZE.atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "records": len(records),
                "skipped": skipped,
                "output": args.output.as_posix(),
                "output_sha256": hashlib.sha256(
                    args.output.read_bytes()
                ).hexdigest(),
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
