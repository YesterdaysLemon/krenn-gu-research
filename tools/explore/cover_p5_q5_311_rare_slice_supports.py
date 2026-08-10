#!/usr/bin/env python3
"""Cover hard q5_311 closures by exact rare-slice support charts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from pysat.solvers import Solver

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu import atomic_json as MINIMIZE
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_q5_311_program as RARE
from krenn_gu.p5_q5_311_support import (
    BRANCH,
    condition_closure,
    general_chart_clause,
    rare_mixed_colourings,
)


def certify(
    record: dict,
    timeout: float,
) -> dict:
    program, split_program, metadata = RARE.build_program(
        record,
        include_majority_pure=True,
    )
    cas = HIGH.run_singular(split_program, timeout)
    return {
        "status": (
            "UNIT_IDEAL"
            if cas["status"] == "UNIT_IDEAL"
            else "INCONCLUSIVE"
        ),
        "method": "split",
        "source_sha256": HIGH.sha256_text(program),
        "split_source_sha256": HIGH.sha256_text(split_program),
        "metadata": metadata,
        "cas": cas,
    }


def solver_result(
    name: str,
    base_clauses: list[list[int]],
    condition: list[list[int]],
    learned: list[tuple[int, ...]],
) -> str:
    with Solver(
        name=name,
        bootstrap_with=[*base_clauses, *condition, *learned],
    ) as solver:
        return "SAT" if solver.solve() else "UNSAT"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument(
        "--record-index",
        type=int,
        action="append",
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--max-charts", type=int, default=10_000)
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.timeout <= 0
        or args.max_charts <= 0
        or not 15 <= args.min_available_percent < 100
        or any(index < 0 for index in args.record_index)
        or len(set(args.record_index)) != len(args.record_index)
    ):
        raise ValueError("invalid support-cover arguments")

    raw_state = args.state.read_bytes()
    state = json.loads(raw_state)
    if state.get("branch") != BRANCH:
        raise ValueError("support cover requires q5_311")
    source_records = state.get("records", [])
    if any(index >= len(source_records) for index in args.record_index):
        raise IndexError("record index is outside the source ledger")

    allowed = SEMANTICS.finite_field_local_signatures()
    retained_mixed = rare_mixed_colourings()
    cnf, pool = SEMANTICS.build_pair_support_cnf(
        allowed,
        mixed_colourings=retained_mixed,
    )
    branch_metadata = HIGH.add_branch_restriction(
        cnf,
        pool,
        allowed,
        BRANCH,
    )
    # Deliberately no lex leaders: each closure is covered before any
    # global symmetry breaking.
    base_clauses = list(cnf.clauses)
    cover_records = []
    targets = []
    started = time.monotonic()

    for source_index in args.record_index:
        target_closure = tuple(
            tuple(map(int, row))
            for row in source_records[source_index]["closure_supports"]
        )
        condition = condition_closure(pool, target_closure)
        learned: list[tuple[int, ...]] = []
        target_record_indices = []
        with Solver(
            name="cadical195",
            bootstrap_with=[*base_clauses, *condition],
        ) as solver:
            while solver.solve():
                if len(cover_records) >= args.max_charts:
                    raise RuntimeError("support cover reached chart limit")
                available = HIGH.available_memory_percent()
                if available < args.min_available_percent:
                    raise MemoryError(
                        "available host memory fell below requested floor"
                    )
                model = solver.get_model()
                supports = SEMANTICS.supports_from_model(pool, model)
                signatures = HIGH.selected_signature_indices(
                    pool,
                    model,
                    allowed,
                )
                trials = []
                for strategy, closure in (
                    (
                        "singleton-relaxation",
                        HIGH.closure_supports(supports),
                    ),
                    ("exact-support", supports),
                ):
                    tree = HIGH.gauge_tree(supports, closure)
                    candidate = {
                        "supports": supports,
                        "closure_supports": closure,
                        "gauge_tree": tree,
                    }
                    certificate = certify(candidate, args.timeout)
                    trials.append(
                        {
                            "strategy": strategy,
                            "certificate_status": certificate["status"],
                            "elapsed_seconds": certificate["cas"][
                                "elapsed_seconds"
                            ],
                        }
                    )
                    if certificate["status"] != "UNIT_IDEAL":
                        continue
                    clause = general_chart_clause(pool, closure, tree)
                    solver.add_clause(clause)
                    learned.append(clause)
                    cover_index = len(cover_records)
                    target_record_indices.append(cover_index)
                    cover_records.append(
                        {
                            "target_record_index": source_index,
                            "clause": clause,
                            "supports": supports,
                            "closure_supports": closure,
                            "signature_indices": signatures,
                            "gauge_tree": tree,
                            "strategy": strategy,
                            "trials": trials,
                            "certificate": certificate,
                        }
                    )
                    print(
                        json.dumps(
                            {
                                "target_record_index": source_index,
                                "cover_charts": len(learned),
                                "closure_entries": certificate[
                                    "metadata"
                                ]["closure_entries"],
                                "rare_mixed_equations": certificate[
                                    "metadata"
                                ]["rare_mixed_equations"],
                            }
                        ),
                        flush=True,
                    )
                    break
                else:
                    raise RuntimeError(
                        f"rare support chart inconclusive for target "
                        f"{source_index}: {trials}"
                    )

        results = {
            name: solver_result(
                name,
                base_clauses,
                condition,
                learned,
            )
            for name in ("cadical195", "glucose4")
        }
        if set(results.values()) != {"UNSAT"}:
            raise AssertionError("support cover did not replay UNSAT")
        targets.append(
            {
                "source_record_index": source_index,
                "target_closure_supports": target_closure,
                "condition_units": len(condition),
                "cover_record_indices": target_record_indices,
                "solver_results": results,
            }
        )

    payload = {
        "status": "EXACT_FINITE_SUPPORT_COVER",
        "branch": BRANCH,
        "metadata": {
            "scope": (
                "selected q5_311 zero-forest closures; not a complete "
                "branch cover"
            ),
            "source_state": args.state.as_posix(),
            "source_state_sha256": hashlib.sha256(raw_state).hexdigest(),
            "source_state_status": state.get("status"),
            "local_signature_patterns": len(allowed),
            "rare_mixed_colourings": len(retained_mixed),
            "majority_mixed_colourings": 0,
            "pure_colour_nonvanishing": [0, 1, 2],
            "lex_leaders": 0,
            "branch_restriction": branch_metadata,
            "base_variables": pool.top,
            "base_clauses": len(base_clauses),
            "cover_charts": len(cover_records),
            "targets": targets,
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "global_conjecture_resolved": False,
        },
        "records": cover_records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    MINIMIZE.atomic_write(args.output, payload)
    print(
        json.dumps(
            {
                "verified": True,
                "targets": len(targets),
                "cover_charts": len(cover_records),
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
