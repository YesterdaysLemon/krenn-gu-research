#!/usr/bin/env python3
"""Certify that no q=23 record reaches the complementary-ruling event.

The certificate consumes the pinned exact q<=23 near-frontier ledger and
records, for every q=23 record, the first failed condition in the extremal
gain-three chain.  It is intentionally independent of the finite-field event
sampler: nonautomatic collinearity is decided exactly by a support-matching
calculation.

This exact finite certificate discharges only the q=23 extremal filter used by
the fixed-pencil rank-degeneracy theorem.  It makes no claim about B_all or
seventy-pencil compatibility by itself.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path


EXPECTED_INPUT_SHA256 = "F72C0C678B14AC480265A5D6CAB3F0ED3F09B798AA15C7B4A27B12D9A8505B80"
EXPECTED_Q23_RECORDS_SHA256 = (
    "608A32C7F8386D193FC2B438576318D9366D59E05C11F22171500B63B9CAB926"
)
EXPECTED_HISTOGRAM = {"20": 2, "21": 39, "22": 506, "23": 8882}
EXPECTED_FIRST_FAILURE_COUNTS = {
    "two_complementary_211_partitions": 8832,
    "two_synchronized_passive_partitions": 32,
    "nonautomatic_line_incidence_at_both_active_vertices": 18,
}
EXPECTED_FAILURE_LEDGER_SHA256 = (
    "41C3C107FF93D247B1D8AE2575395BBAFF43B274CF7EE94C7CB707D034E30B3D"
)
PAIR_ORDER = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
CONDITIONS = (
    "two_complementary_211_partitions",
    "two_synchronized_passive_partitions",
    "nonautomatic_line_incidence_at_both_active_vertices",
    "five_generic_rank_one_losses",
    "total_codimension_two",
)


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def partition_shape(partition: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(Counter(partition).values()))


def repeated_pair(partition: tuple[int, ...]) -> tuple[int, int] | None:
    if partition_shape(partition) != (1, 1, 2):
        return None
    for label in sorted(set(partition)):
        charts = tuple(index for index, value in enumerate(partition) if value == label)
        if len(charts) == 2:
            return charts
    raise AssertionError("2+1+1 partition has no repeated pair")


def complementary(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return set(left).isdisjoint(right) and set(left) | set(right) == set(range(4))


def structural_rank(masks: tuple[int, ...]) -> int:
    """Maximum possible vector rank for coordinate-support masks, exactly."""

    best = 0
    for size in range(1, min(3, len(masks)) + 1):
        for blocks in combinations(range(len(masks)), size):
            for coordinates in combinations(range(3), size):
                if any(
                    all(
                        masks[blocks[row]] & (1 << coordinates[column])
                        for row, column in enumerate(permutation)
                    )
                    for permutation in permutations(range(size))
                ):
                    best = size
                    break
    return best


def expected_generic_ranks(
    active: tuple[int, int], passive: tuple[int, int]
) -> tuple[int, ...]:
    result = []
    for left, right in PAIR_ORDER:
        if left in active and right in active:
            result.append(4)
        elif left in passive and right in passive:
            result.append(1)
        else:
            result.append(3)
    return tuple(result)


def first_failure(record: dict[str, object]) -> tuple[str, dict[str, object]]:
    partitions = tuple(tuple(value) for value in record["partitions"])
    repeated = tuple(repeated_pair(partition) for partition in partitions)
    complementary_active_pairs = tuple(
        (left, right)
        for left, right in combinations(range(4), 2)
        if repeated[left] is not None
        and repeated[right] is not None
        and complementary(repeated[left], repeated[right])
    )
    context: dict[str, object] = {
        "complementary_active_pairs": [list(pair) for pair in complementary_active_pairs]
    }
    if not complementary_active_pairs:
        return CONDITIONS[0], context

    synchronized_pairs = tuple(
        active
        for active in complementary_active_pairs
        if all(
            partition_shape(partitions[vertex]) == (4,)
            for vertex in range(4)
            if vertex not in active
        )
    )
    context["synchronized_active_pairs"] = [list(pair) for pair in synchronized_pairs]
    if not synchronized_pairs:
        return CONDITIONS[1], context

    masks_by_vertex = tuple(
        tuple(value) for value in record["support_masks_by_vertex_block"]
    )
    structural_ranks_by_pair = tuple(
        (
            active,
            tuple(structural_rank(masks_by_vertex[vertex]) for vertex in active),
        )
        for active in synchronized_pairs
    )
    context["active_structural_ranks_by_pair"] = [
        {"active_vertices": list(active), "structural_ranks": list(ranks)}
        for active, ranks in structural_ranks_by_pair
    ]
    nonautomatic_pairs = tuple(
        active for active, ranks in structural_ranks_by_pair if ranks == (3, 3)
    )
    if not nonautomatic_pairs:
        # For three distinct blocks the line determinant is nonzero precisely
        # when structural rank is three.  Rank <=2 means the line condition is
        # already forced by coordinate supports and has event codimension zero.
        return CONDITIONS[2], context

    generic_ranks = tuple(record["ranks_01_02_03_12_13_23"])
    loss_pairs = []
    for active in nonautomatic_pairs:
        passive = tuple(vertex for vertex in range(4) if vertex not in active)
        expected = expected_generic_ranks(active, passive)
        if generic_ranks == expected:
            loss_pairs.append(active)
    context["five_loss_active_pairs"] = [list(pair) for pair in loss_pairs]
    if not loss_pairs:
        return CONDITIONS[3], context

    # The pinned ledger is expected to be empty before this point.  Refuse to
    # certify a newly appearing record without adding an exact event-rank
    # checker instead of silently assuming the five losses or codimension.
    raise AssertionError(
        "record reached the event-rank stage; extend the certificate before accepting it"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    input_bytes = args.input.read_bytes()
    input_sha256 = sha256_bytes(input_bytes)
    assert input_sha256 == EXPECTED_INPUT_SHA256
    data = json.loads(input_bytes)
    assert data["status"] == "exact_s3ccd_near_frontier_extract"
    assert data["global_conjecture"] == "UNRESOLVED"
    assert data["threshold"] == 23
    assert data["near_frontier_histogram"] == EXPECTED_HISTOGRAM
    q23_records = [record for record in data["records"] if int(record["q"]) == 23]
    q23_records_sha256 = sha256_bytes(canonical_json(q23_records))
    assert q23_records_sha256 == EXPECTED_Q23_RECORDS_SHA256

    ledger = []
    stage_counts: Counter[str] = Counter()
    near_extremal = []
    q23_ordinal = 0
    for record_index, record in enumerate(data["records"]):
        if int(record["q"]) != 23:
            continue
        stage, context = first_failure(record)
        entry = {
            "record_index": record_index,
            "q23_ordinal": q23_ordinal,
            "record_sha256": sha256_bytes(canonical_json(record)),
            "first_failed_condition": stage,
        }
        ledger.append(entry)
        stage_counts[stage] += 1
        if stage in CONDITIONS[1:]:
            near_extremal.append(
                {
                    **entry,
                    **context,
                    "selector_ids": record["selector_ids"],
                    "selectors": record["selectors"],
                    "partitions": record["partitions"],
                    "support_masks_by_vertex_block": record[
                        "support_masks_by_vertex_block"
                    ],
                    "delta_by_vertex": record["delta_by_vertex"],
                    "generic_ranks_01_02_03_12_13_23": record[
                        "ranks_01_02_03_12_13_23"
                    ],
                }
            )
        q23_ordinal += 1

    assert q23_ordinal == 8882
    assert sum(stage_counts.values()) == 8882
    assert dict(stage_counts) == EXPECTED_FIRST_FAILURE_COUNTS
    assert not any(stage_counts[stage] for stage in CONDITIONS[3:])
    assert stage_counts[CONDITIONS[2]] > 0
    ledger_sha256 = sha256_bytes(canonical_json(ledger))
    assert ledger_sha256 == EXPECTED_FAILURE_LEDGER_SHA256
    summary = {
        "status": "exact_q23_complementary_ruling_zero_certificate",
        "global_conjecture": "UNRESOLVED",
        "input_sha256": input_sha256,
        "q23_records_sha256": q23_records_sha256,
        "condition_order": list(CONDITIONS),
        "q23_record_count": q23_ordinal,
        "first_failure_counts": dict(stage_counts),
        "failure_ledger_sha256": ledger_sha256,
        "failure_ledger": ledger,
        "near_extremal_records": near_extremal,
        "records_reaching_five_loss_check": stage_counts[CONDITIONS[3]],
        "records_reaching_total_codimension_check": stage_counts[CONDITIONS[4]],
        "candidate_equality_records": 0,
        "scope_limit": (
            "certifies only that the pinned q=23 generic ledger has no "
            "complementary-ruling codimension-two equality source; B_all, "
            "seventy-pencil compatibility, and the global conjecture remain open"
        ),
    }
    args.output.write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: summary[key]
                for key in (
                    "status",
                    "q23_record_count",
                    "first_failure_counts",
                    "candidate_equality_records",
                    "failure_ledger_sha256",
                    "global_conjecture",
                )
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
