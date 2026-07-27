#!/usr/bin/env python3
"""Independent F_5 census of the five-row projective normal forms."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIME = 5
ZERO = (0, 0, 0)
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
    return pivot_row


def canonical(vector: tuple[int, ...]) -> tuple[int, ...]:
    if not any(value % PRIME for value in vector):
        return ZERO
    first = next(value % PRIME for value in vector if value % PRIME)
    inverse = pow(first, -1, PRIME)
    return tuple(value * inverse % PRIME for value in vector)


def cross(
    left: tuple[int, int, int], right: tuple[int, int, int]
) -> tuple[int, int, int]:
    return canonical(
        (
            left[1] * right[2] - left[2] * right[1],
            left[2] * right[0] - left[0] * right[2],
            left[0] * right[1] - left[1] * right[0],
        )
    )


def pair_contains_coordinate(
    left: tuple[int, ...], right: tuple[int, ...]
) -> bool:
    pair_rank = rank_mod((left, right))
    return any(
        rank_mod((left, right, coordinate)) == pair_rank
        for coordinate in COORDINATES
    )


def classify_noncoordinates(
    points: tuple[tuple[int, ...], ...]
) -> str:
    count = len(points)
    if count <= 1:
        return f"noncoordinate_{count}"
    if count == 2:
        assert pair_contains_coordinate(points[0], points[1])
        return "noncoordinate_2_secant"
    if rank_mod(points) <= 2:
        assert pair_contains_coordinate(points[0], points[1])
        return f"noncoordinate_{count}_line"
    if count == 3:
        side_coordinates = []
        for left, right in itertools.combinations(range(3), 2):
            on_side = tuple(
                coordinate
                for coordinate in COORDINATES
                if rank_mod((points[left], points[right], coordinate)) == 2
            )
            assert len(on_side) == 1
            side_coordinates.extend(on_side)
        assert set(side_coordinates) == set(COORDINATES)
        return "noncoordinate_3_triangle"
    assert count == 4
    assert all(
        rank_mod(points[index] for index in triple) == 3
        for triple in itertools.combinations(range(4), 3)
    )
    opposite_pairs = (
        (((0, 1)), ((2, 3))),
        (((0, 2)), ((1, 3))),
        (((0, 3)), ((1, 2))),
    )
    diagonal_points = []
    for first, second in opposite_pairs:
        first_line = cross(points[first[0]], points[first[1]])
        second_line = cross(points[second[0]], points[second[1]])
        diagonal_points.append(cross(first_line, second_line))
    assert set(diagonal_points) == set(COORDINATES)
    return "noncoordinate_4_quadrangle"


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
    points = (ZERO,) + projective_points
    assert len(projective_points) == 31
    pair_condition = tuple(
        tuple(pair_contains_coordinate(left, right) for right in points)
        for left in points
    )

    checked = 0
    retained = 0
    strata: Counter[str] = Counter()
    noncoordinate_counts: Counter[int] = Counter()
    failures = []
    for indices in itertools.combinations_with_replacement(
        range(len(points)), 5
    ):
        checked += 1
        if any(
            not pair_condition[indices[first]][indices[second]]
            for first, second in itertools.combinations(range(5), 2)
        ):
            continue
        rows = tuple(points[index] for index in indices)
        if rank_mod(rows) != 3:
            continue
        retained += 1
        noncoordinates = tuple(
            row
            for row in rows
            if row != ZERO and row not in COORDINATES
        )
        noncoordinate_counts[len(noncoordinates)] += 1
        try:
            if ZERO in rows:
                assert all(
                    row == ZERO or row in COORDINATES for row in rows
                )
                stratum = "zero_and_coordinates"
            else:
                assert len(set(noncoordinates)) == len(noncoordinates)
                stratum = classify_noncoordinates(noncoordinates)
            strata[stratum] += 1
        except AssertionError:
            failures.append(rows)

    assert checked == math.comb(36, 5)
    assert retained == 2556
    assert not failures
    assert max(noncoordinate_counts) == 4

    primary = (
        ROOT / "tmp" / "five_row_projective_normal_forms_verified.json"
    )
    output = {
        "verified": True,
        "finite_field": f"F_{PRIME}",
        "projective_points": len(projective_points),
        "zero_row_adjoined": True,
        "five_point_multisets_checked": checked,
        "spanning_pair_incidence_configurations": retained,
        "noncoordinate_count_distribution": dict(
            sorted(noncoordinate_counts.items())
        ),
        "normal_form_distribution": dict(sorted(strata.items())),
        "classification_failures": len(failures),
        "primary_artifact": primary.relative_to(ROOT).as_posix(),
        "primary_artifact_sha256": sha256(primary),
        "source": str(Path(__file__).resolve()),
        "source_sha256": sha256(Path(__file__).resolve()),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "five_row_projective_normal_forms_audited.json"
    )
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
