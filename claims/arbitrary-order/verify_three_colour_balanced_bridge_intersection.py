"""Verify the simultaneous balanced-bridge zero-pattern classification.

For each colour c and vertex i, the balanced boundary supplies a coordinate
normal f_i(c) different from c.  The failure plane is

    H_i^c = {x : x[f_i(c)] = 0}.

If an edge block restricts on H_i^c x H_j^c to a scalar multiple of
x[c]y[c] for all three colours, this script independently enumerates the
eight possible normal types at each endpoint and reconstructs every
potentially nonzero matrix entry.

The result is a finite structural lemma.  It is not a Krenn--Gu proof.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Sequence


COLOURS = tuple(range(3))
Entry = tuple[int, int]
NormalType = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normal_types() -> list[NormalType]:
    return [
        tuple(values)
        for values in itertools.product(COLOURS, repeat=3)
        if all(values[colour] != colour for colour in COLOURS)
    ]


def allowed_entries(
    left: NormalType,
    right: NormalType,
) -> tuple[Entry, ...]:
    output = []
    for row in COLOURS:
        for column in COLOURS:
            allowed = True
            for colour in COLOURS:
                in_left_plane = row != left[colour]
                in_right_plane = column != right[colour]
                is_bridge_entry = (row, column) == (colour, colour)
                if in_left_plane and in_right_plane and not is_bridge_entry:
                    allowed = False
                    break
            if allowed:
                output.append((row, column))
    return tuple(output)


def structural_rank(entries: Sequence[Entry]) -> int:
    support = set(entries)
    best = 0
    for size in range(1, 4):
        for rows in itertools.combinations(COLOURS, size):
            for columns in itertools.combinations(COLOURS, size):
                for permuted in itertools.permutations(columns):
                    if all(
                        (row, column) in support
                        for row, column in zip(
                            rows, permuted, strict=True
                        )
                    ):
                        best = size
    return best


def complement_type(item: NormalType) -> NormalType:
    return tuple(
        next(
            colour
            for colour in COLOURS
            if colour not in (index, item[index])
        )
        for index in COLOURS
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "three_colour_balanced_bridge_intersection_verified.json",
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    types = normal_types()
    assert len(types) == 8
    type_id = {item: index for index, item in enumerate(types)}

    size_distribution = {size: 0 for size in range(5)}
    rank_distribution = {rank: 0 for rank in range(4)}
    joint_distribution: dict[str, int] = {}
    records = []

    for left_id, left in enumerate(types):
        for right_id, right in enumerate(types):
            entries = allowed_entries(left, right)
            transposed = tuple(
                sorted((column, row) for row, column in entries)
            )
            assert transposed == allowed_entries(right, left)

            rank = structural_rank(entries)
            size_distribution[len(entries)] += 1
            rank_distribution[rank] += 1
            joint_key = f"entries_{len(entries)}_rank_{rank}"
            joint_distribution[joint_key] = (
                joint_distribution.get(joint_key, 0) + 1
            )

            complementary = right == complement_type(left)
            assert (rank == 3) == complementary
            if complementary:
                diagonal = {(colour, colour) for colour in COLOURS}
                assert diagonal.issubset(entries)
                assert len(entries) in (3, 4)
            else:
                assert rank <= 2

            records.append(
                {
                    "left_type": left_id,
                    "right_type": right_id,
                    "left_normals": list(left),
                    "right_normals": list(right),
                    "complementary_types": complementary,
                    "allowed_entries": [list(item) for item in entries],
                    "allowed_entry_count": len(entries),
                    "structural_rank": rank,
                }
            )

    assert size_distribution == {0: 2, 1: 0, 2: 12, 3: 44, 4: 6}
    assert rank_distribution == {0: 2, 1: 12, 2: 42, 3: 8}
    assert joint_distribution == {
        "entries_0_rank_0": 2,
        "entries_2_rank_1": 12,
        "entries_3_rank_2": 42,
        "entries_3_rank_3": 2,
        "entries_4_rank_3": 6,
    }

    zero_pairs = [
        [record["left_type"], record["right_type"]]
        for record in records
        if record["allowed_entry_count"] == 0
    ]
    assert zero_pairs == [[2, 2], [5, 5]]

    complementary_pairs = [
        [index, type_id[complement_type(item)]]
        for index, item in enumerate(types)
    ]
    assert complementary_pairs == [
        [0, 7],
        [1, 6],
        [2, 5],
        [3, 4],
        [4, 3],
        [5, 2],
        [6, 1],
        [7, 0],
    ]

    reciprocal_singleton_incidences = []
    for left_id, left in enumerate(types):
        for colour in COLOURS:
            row = left[colour]
            for right_id, right in enumerate(types):
                entries = set(allowed_entries(left, right))
                if (row, colour) not in entries:
                    continue
                assert right[row] == colour
                reciprocal_singleton_incidences.append(
                    {
                        "left_type": left_id,
                        "right_type": right_id,
                        "left_killer_colour": colour,
                        "left_row_colour": row,
                        "right_killer_colour": row,
                        "right_row_colour": colour,
                    }
                )
    assert len(reciprocal_singleton_incidences) == 72

    payload = {
        "verified": True,
        "status": "balanced_bridge_intersection_verified",
        "scope": (
            "all 64 ordered endpoint-type pairs for three simultaneous "
            "coordinate balanced-bridge restrictions"
        ),
        "normal_types": [
            {"type": index, "normals": list(item)}
            for index, item in enumerate(types)
        ],
        "ordered_type_pairs": len(records),
        "maximum_allowed_entries_per_block": max(
            record["allowed_entry_count"] for record in records
        ),
        "size_distribution": {
            str(key): value for key, value in size_distribution.items()
        },
        "structural_rank_distribution": {
            str(key): value for key, value in rank_distribution.items()
        },
        "joint_distribution": joint_distribution,
        "zero_type_pairs": zero_pairs,
        "full_rank_exactly_complementary": True,
        "complementary_type_pairs": complementary_pairs,
        "allowed_primary_singletons_are_reciprocal": True,
        "reciprocal_singleton_incidences": (
            reciprocal_singleton_incidences
        ),
        "records": records,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    payload["output"] = str(args.output)
    payload["output_sha256"] = sha256(args.output)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
