#!/usr/bin/env python3
"""Independent F_5 audit of the five-row projective incidence lemma."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 5
COORDINATES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rank_mod(rows: object) -> int:
    matrix = [
        [int(value) % PRIME for value in row]
        for row in rows
        if any(int(value) % PRIME for value in row)
    ]
    pivot_row = 0
    for column in range(3):
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
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, PRIME)
        matrix[pivot_row] = [
            value * inverse % PRIME for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    first = next(value for value in vector if value)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in vector)


def pair_contains_coordinate(
    left: tuple[int, ...], right: tuple[int, ...]
) -> bool:
    pair_rank = rank_mod((left, right))
    return any(
        rank_mod((left, right, coordinate)) == pair_rank
        for coordinate in COORDINATES
    )


def main() -> None:
    projective_points = tuple(
        sorted(
            {
                canonical(vector)
                for vector in itertools.product(range(PRIME), repeat=3)
                if any(vector)
            }
        )
    )
    points = ((0, 0, 0),) + projective_points
    assert len(projective_points) == 31

    pair_condition = tuple(
        tuple(pair_contains_coordinate(left, right) for right in points)
        for left in points
    )
    configurations_checked = 0
    spanning_pair_incidence_configurations = 0
    coordinate_point_counts: Counter[int] = Counter()
    zero_row_counts: Counter[int] = Counter()
    counterexamples = []
    for indices in itertools.combinations_with_replacement(
        range(len(points)), 5
    ):
        configurations_checked += 1
        if any(
            not pair_condition[indices[first]][indices[second]]
            for first, second in itertools.combinations(range(5), 2)
        ):
            continue
        rows = tuple(points[index] for index in indices)
        if rank_mod(rows) != 3:
            continue
        spanning_pair_incidence_configurations += 1
        coordinate_count = sum(row in COORDINATES for row in rows)
        zero_count = sum(not any(row) for row in rows)
        coordinate_point_counts[coordinate_count] += 1
        zero_row_counts[zero_count] += 1
        if coordinate_count == 0:
            counterexamples.append(rows)

    assert configurations_checked == math.comb(36, 5)
    assert spanning_pair_incidence_configurations == 2556
    assert not counterexamples
    assert min(coordinate_point_counts) == 1

    primary = ROOT / "tmp" / "five_row_projective_incidence_verified.json"
    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "projective_points": len(projective_points),
        "zero_row_adjoined": True,
        "five_point_multisets_checked": configurations_checked,
        "spanning_pair_incidence_configurations": (
            spanning_pair_incidence_configurations
        ),
        "coordinate_point_count_distribution": dict(
            sorted(coordinate_point_counts.items())
        ),
        "zero_row_count_distribution": dict(sorted(zero_row_counts.items())),
        "counterexamples_without_coordinate_point": len(counterexamples),
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "five_row_projective_incidence_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
