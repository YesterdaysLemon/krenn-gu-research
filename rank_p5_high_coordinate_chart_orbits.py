#!/usr/bin/env python3
"""Rank exact P5 chart orbits by retrospective ledger coverage.

For every representative chart in a state ledger, reconstruct its complete
branch-symmetry orbit and count which recorded SAT models violate at least one
transported clause.  Clause evaluation uses integer bitsets, so the quadratic
coverage calculation remains cheap compared with the algebra certificates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import p5_high_coordinate_tree_chart_cegar as HIGH
import p5_pair_support_semantics as SEMANTICS
import verify_p5_high_coordinate_chart_ledgers as LEDGER


def model_truth_bits(pool, records: list[dict]) -> dict[int, int]:
    """Return the ledger-model truth bitset for every support variable."""
    supports = [
        LEDGER.normalized_supports(record["supports"])
        for record in records
    ]
    truth: dict[int, int] = {}
    keys = [
        (label, mode, source, colour)
        for label in ("x", "singleton")
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        for colour in SEMANTICS.COLOURS
    ]
    for key in keys:
        variable = pool.id(key)
        bits = 0
        for index, support in enumerate(supports):
            if key[0] == "x":
                _label, mode, source, colour = key
                value = bool(
                    support[mode][source] & (1 << colour)
                )
            else:
                _label, mode, source, colour = key
                value = (
                    support[mode][source] == 1 << colour
                )
            if value:
                bits |= 1 << index
        truth[variable] = bits
    return truth


def clause_violation_bits(
    clause: tuple[int, ...],
    truth: dict[int, int],
    universe: int,
) -> int:
    """Return models on which every literal in ``clause`` is false."""
    violated = universe
    for literal in clause:
        variable_truth = truth[abs(literal)]
        literal_false = (
            universe ^ variable_truth
            if literal > 0
            else variable_truth
        )
        violated &= literal_false
        if not violated:
            break
    return violated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.top <= 0:
        raise ValueError("--top must be positive")

    raw = args.state.read_bytes()
    state = json.loads(raw)
    branch = state.get("branch")
    if branch not in HIGH.BRANCH_BACKBONES:
        raise ValueError("state has an unsupported branch")
    records = state.get("records", [])
    if not records:
        raise ValueError("state contains no records")

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    HIGH.add_branch_restriction(cnf, pool, allowed, branch)
    HIGH.add_stabilizer_lex_leaders(cnf, pool, branch)
    truth = model_truth_bits(pool, records)
    universe = (1 << len(records)) - 1

    rows = []
    coverage_bits = []
    for index, record in enumerate(records):
        closure = LEDGER.normalized_supports(
            record["closure_supports"]
        )
        tree = LEDGER.normalized_tree(record["gauge_tree"])
        clauses = HIGH.chart_symmetry_orbit_clauses(
            closure,
            tree,
            branch,
            pool,
        )
        hit_bits = 0
        for clause in clauses:
            hit_bits |= clause_violation_bits(
                clause,
                truth,
                universe,
            )
        if not hit_bits & (1 << index):
            raise AssertionError(
                f"record {index} orbit misses its source model"
            )
        coverage_bits.append(hit_bits)
        rows.append(
            {
                "record_index": index,
                "hits": hit_bits.bit_count(),
                "orbit_clauses": len(clauses),
                "clause_literals": len(
                    HIGH.chart_clause(
                        pool,
                        closure,
                        tree,
                        branch,
                    )
                ),
                "coordinate_profile": record[
                    "coordinate_profile"
                ],
                "gauge_tree_edges": len(tree),
                "covered_record_indices": [
                    target
                    for target in range(len(records))
                    if hit_bits & (1 << target)
                ],
            }
        )

    ranked = sorted(
        rows,
        key=lambda row: (
            -row["hits"],
            row["clause_literals"],
            row["record_index"],
        ),
    )

    # Also compute a deterministic greedy set cover.  This highlights
    # representatives with genuinely new coverage rather than many hits that
    # are already explained by a stronger family.
    uncovered = universe
    greedy = []
    while uncovered:
        best_index = max(
            range(len(records)),
            key=lambda index: (
                (coverage_bits[index] & uncovered).bit_count(),
                -rows[index]["clause_literals"],
                -index,
            ),
        )
        new_bits = coverage_bits[best_index] & uncovered
        if not new_bits:
            raise AssertionError("chart orbits do not cover the ledger")
        greedy.append(
            {
                "record_index": best_index,
                "new_hits": new_bits.bit_count(),
                "total_hits": coverage_bits[
                    best_index
                ].bit_count(),
                "remaining_after": (
                    uncovered ^ new_bits
                ).bit_count(),
            }
        )
        uncovered ^= new_bits

    payload = {
        "verified": True,
        "scope": (
            "retrospective coverage of recorded source models only; "
            "not a branch proof"
        ),
        "branch": branch,
        "state": args.state.as_posix(),
        "state_sha256": hashlib.sha256(raw).hexdigest(),
        "state_status": state.get("status"),
        "records": len(records),
        "ranked": ranked[: args.top],
        "greedy_cover": greedy,
    }
    text = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(
            json.dumps(
                {
                    "verified": True,
                    "records": len(records),
                    "highest_coverage_record": ranked[0][
                        "record_index"
                    ],
                    "highest_coverage_hits": ranked[0]["hits"],
                    "greedy_cover_records": len(greedy),
                    "output": args.output.as_posix(),
                },
                indent=2,
            )
        )
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
