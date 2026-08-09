"""Independent audit of the balanced three-colour bridge classification.

This auditor intentionally does not import the generating verifier.  It
rebuilds the endpoint types from three binary choices, constructs the
forced-zero masks directly from restrictions of matrix units to the
coordinate planes, and checks the complete recorded table.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Any


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for piece in iter(lambda: handle.read(1 << 20), b""):
            digest.update(piece)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "analysis",
        type=Path,
        nargs="?",
        default=Path(
            "tmp",
            "three_colour_balanced_bridge_intersection_verified.json",
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "three_colour_balanced_bridge_intersection_audited.json",
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    source = read_json(args.analysis)
    if source.get("verified") is not True:
        raise ValueError("source classification is not marked verified")

    choices = ((1, 2), (0, 2), (0, 1))
    endpoint_types = list(itertools.product(*choices))
    if len(endpoint_types) != 8:
        raise AssertionError("wrong endpoint-type count")

    source_types = [
        tuple(map(int, item["normals"]))
        for item in source["normal_types"]
    ]
    if source_types != endpoint_types:
        raise AssertionError("endpoint-type enumeration mismatch")

    expected_records = []
    entry_counts: dict[int, int] = {}
    rank_counts: dict[int, int] = {}
    zero_pairs = []
    rank_three_pairs = []

    for left_id, left in enumerate(endpoint_types):
        for right_id, right in enumerate(endpoint_types):
            forced_zero = [[False] * 3 for _ in range(3)]
            for colour in range(3):
                left_basis = [
                    row for row in range(3) if row != left[colour]
                ]
                right_basis = [
                    column
                    for column in range(3)
                    if column != right[colour]
                ]
                for row in left_basis:
                    for column in right_basis:
                        if (row, column) != (colour, colour):
                            forced_zero[row][column] = True

            allowed = [
                [row, column]
                for row in range(3)
                for column in range(3)
                if not forced_zero[row][column]
            ]
            allowed_set = {tuple(item) for item in allowed}
            determinant_terms = [
                list(permutation)
                for permutation in itertools.permutations(range(3))
                if all(
                    (row, permutation[row]) in allowed_set
                    for row in range(3)
                )
            ]
            if determinant_terms:
                rank = 3
            else:
                two_minor = any(
                    (rows[0], columns[order[0]]) in allowed_set
                    and (rows[1], columns[order[1]]) in allowed_set
                    for rows in itertools.combinations(range(3), 2)
                    for columns in itertools.combinations(range(3), 2)
                    for order in ((0, 1), (1, 0))
                )
                rank = 2 if two_minor else (1 if allowed else 0)

            complement = all(
                left[colour] != right[colour]
                for colour in range(3)
            )
            if (rank == 3) != complement:
                raise AssertionError(
                    "rank-three/complement classification failed"
                )
            if rank == 3:
                rank_three_pairs.append([left_id, right_id])
            if not allowed:
                zero_pairs.append([left_id, right_id])
            entry_counts[len(allowed)] = (
                entry_counts.get(len(allowed), 0) + 1
            )
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
            expected_records.append(
                {
                    "left_type": left_id,
                    "right_type": right_id,
                    "left_normals": list(left),
                    "right_normals": list(right),
                    "complementary_types": complement,
                    "allowed_entries": allowed,
                    "allowed_entry_count": len(allowed),
                    "structural_rank": rank,
                }
            )

    if source["records"] != expected_records:
        raise AssertionError("64-record classification table mismatch")
    if entry_counts != {3: 44, 2: 12, 4: 6, 0: 2}:
        raise AssertionError("allowed-entry distribution mismatch")
    if rank_counts != {2: 42, 1: 12, 3: 8, 0: 2}:
        raise AssertionError("structural-rank distribution mismatch")
    if zero_pairs != [[2, 2], [5, 5]]:
        raise AssertionError("zero-pair classification mismatch")

    reciprocal_singletons = 0
    records_by_pair = {
        (record["left_type"], record["right_type"]): record
        for record in expected_records
    }
    for left_id, left in enumerate(endpoint_types):
        for killed_colour in range(3):
            row_colour = left[killed_colour]
            singleton = (row_colour, killed_colour)
            for right_id, right in enumerate(endpoint_types):
                allowed = {
                    tuple(item)
                    for item in records_by_pair[
                        (left_id, right_id)
                    ]["allowed_entries"]
                }
                if singleton not in allowed:
                    continue
                reciprocal_singletons += 1
                if right[row_colour] != killed_colour:
                    raise AssertionError(
                        "allowed singleton is not reciprocal"
                    )
    if reciprocal_singletons != 72:
        raise AssertionError("reciprocal-singleton count mismatch")
    if (
        source.get("allowed_primary_singletons_are_reciprocal")
        is not True
    ):
        raise AssertionError("source omits reciprocal-singleton result")
    if len(source.get("reciprocal_singleton_incidences", [])) != 72:
        raise AssertionError("source reciprocal-singleton table mismatch")

    payload = {
        "verified": True,
        "status": "balanced_bridge_intersection_independently_audited",
        "scope": (
            "fresh coordinate-plane matrix-unit restrictions and "
            "determinant-transversal audit for all 64 type pairs"
        ),
        "analysis": str(args.analysis),
        "analysis_sha256": file_hash(args.analysis),
        "endpoint_types": len(endpoint_types),
        "ordered_type_pairs": len(expected_records),
        "allowed_entry_count_distribution": {
            str(key): entry_counts[key] for key in sorted(entry_counts)
        },
        "structural_rank_distribution": {
            str(key): rank_counts[key] for key in sorted(rank_counts)
        },
        "zero_type_pairs": zero_pairs,
        "rank_three_type_pairs": rank_three_pairs,
        "full_rank_exactly_complementary": True,
        "allowed_primary_singletons_are_reciprocal": True,
        "reciprocal_singleton_incidences": reciprocal_singletons,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
