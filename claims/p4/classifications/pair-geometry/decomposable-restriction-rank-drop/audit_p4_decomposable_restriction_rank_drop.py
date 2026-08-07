#!/usr/bin/env python3
"""Finite-field audit of the P4 decomposable rank-drop boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md"
PRIME = 3
PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = (5, 4, 3, 2, 1, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rref(rows: list[list[int]], columns: int) -> tuple[tuple[int, ...], ...]:
    matrix = [
        [value % PRIME for value in row]
        for row in rows
        if any(value % PRIME for value in row)
    ]
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, PRIME)
        matrix[pivot_row] = [
            value * inverse % PRIME for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(
                    matrix[row],
                    matrix[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def rank(rows: list[list[int]], columns: int) -> int:
    return len(rref(rows, columns))


def subspaces(dimension: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    result = []
    for pivots in itertools.combinations(range(4), dimension):
        free_positions = [
            (row, column)
            for row, pivot in enumerate(pivots)
            for column in range(pivot + 1, 4)
            if column not in pivots
        ]
        for values in itertools.product(
            range(PRIME),
            repeat=len(free_positions),
        ):
            basis = [[0] * 4 for _ in range(dimension)]
            for row, pivot in enumerate(pivots):
                basis[row][pivot] = 1
            for (row, column), value in zip(
                free_positions,
                values,
                strict=True,
            ):
                basis[row][column] = value
            result.append(tuple(tuple(row) for row in basis))
    return tuple(result)


def pair_vector(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> list[int]:
    return [
        (
            left[first] * right[second]
            + left[second] * right[first]
        )
        % PRIME
        for first, second in PAIRS
    ]


def pair_image(
    left: tuple[tuple[int, ...], ...],
    right: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return rref(
        [
            pair_vector(u, v)
            for u in left
            for v in right
        ],
        6,
    )


def main() -> None:
    planes = subspaces(2)
    hyperplanes = subspaces(3)
    assert len(planes) == 130
    assert len(hyperplanes) == 40

    all_subspaces = hyperplanes + planes
    image_ids = {}
    images = []
    pair_images = {}
    pair_image_dimension_counts: Counter[int] = Counter()
    hyperplane_plane_minimum = 6
    for left_index, left in enumerate(all_subspaces):
        for right_index, right in enumerate(all_subspaces):
            image = pair_image(left, right)
            identifier = image_ids.get(image)
            if identifier is None:
                identifier = len(images)
                image_ids[image] = identifier
                images.append(image)
            pair_images[(left_index, right_index)] = identifier
            pair_image_dimension_counts[len(image)] += 1
            if left_index < 40 <= right_index:
                hyperplane_plane_minimum = min(
                    hyperplane_plane_minimum,
                    len(image),
                )
    assert hyperplane_plane_minimum == 3

    pairing_rank_cache = {}

    def pairing_rank(left_id: int, right_id: int) -> int:
        key = (left_id, right_id)
        cached = pairing_rank_cache.get(key)
        if cached is not None:
            return cached
        left = images[left_id]
        right = images[right_id]
        value = rank(
            [
                [
                    sum(
                        x[index] * y[COMPLEMENT[index]]
                        for index in range(6)
                    )
                    % PRIME
                    for y in right
                ]
                for x in left
            ],
            len(right),
        )
        pairing_rank_cache[key] = value
        return value

    def count_rank_one_profiles(
        fourth_indices: range,
    ) -> tuple[int, int]:
        checked = 0
        hits = 0
        for first in range(40):
            for second in range(40):
                first_second = pair_images[(first, second)]
                for third in range(40):
                    first_third = pair_images[(first, third)]
                    second_third = pair_images[(second, third)]
                    for fourth in fourth_indices:
                        checked += 1
                        if pairing_rank(
                            first_second,
                            pair_images[(third, fourth)],
                        ) != 1:
                            continue
                        if pairing_rank(
                            first_third,
                            pair_images[(second, fourth)],
                        ) != 1:
                            continue
                        if pairing_rank(
                            pair_images[(first, fourth)],
                            second_third,
                        ) == 1:
                            hits += 1
        return checked, hits

    checked_3333, hits_3333 = count_rank_one_profiles(range(40))
    checked_3332, hits_3332 = count_rank_one_profiles(range(40, 170))
    assert checked_3333 == 40**4
    assert checked_3332 == 40**3 * 130
    assert hits_3333 == hits_3332 == 0

    output = {
        "audited": True,
        "field": "F_3",
        "planes": len(planes),
        "hyperplanes": len(hyperplanes),
        "ordered_pair_images": len(all_subspaces) ** 2,
        "distinct_pair_images": len(images),
        "pair_image_dimension_counts": dict(
            sorted(pair_image_dimension_counts.items())
        ),
        "hyperplane_plane_pair_image_minimum": (
            hyperplane_plane_minimum
        ),
        "rank_profile_3333_checked": checked_3333,
        "rank_profile_3333_decomposable_candidates": hits_3333,
        "rank_profile_3332_checked": checked_3332,
        "rank_profile_3332_decomposable_candidates": hits_3332,
        "rank_profiles_checked_total": checked_3333 + checked_3332,
        "maximum_rank_three_local_maps_verified": 2,
        "pairing_rank_cache_entries": len(pairing_rank_cache),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "finite formula audit; written theorem is over C",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p4_decomposable_restriction_rank_drop_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
