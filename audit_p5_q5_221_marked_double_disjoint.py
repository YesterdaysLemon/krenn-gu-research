#!/usr/bin/env python3
"""Independent finite-field pair-image audit for the disjoint type."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md"
)
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(rows, prime: int) -> int:
    if not rows:
        return 0
    matrix = [
        [value % prime for value in row]
        for row in rows
    ]
    pivot_row = 0
    for column in range(len(matrix[0])):
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
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime
            for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(
                    matrix[row],
                    matrix[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def rref_subspaces(prime: int, ambient: int, dimension: int):
    for pivots in itertools.combinations(range(ambient), dimension):
        free_positions = tuple(
            (row, column)
            for column in range(ambient)
            if column not in pivots
            for row, pivot in enumerate(pivots)
            if pivot < column
        )
        for values in itertools.product(
            range(prime),
            repeat=len(free_positions),
        ):
            rows = [[0] * ambient for _ in range(dimension)]
            for row, pivot in enumerate(pivots):
                rows[row][pivot] = 1
            for (row, column), value in zip(
                free_positions,
                values,
                strict=True,
            ):
                rows[row][column] = value
            yield tuple(tuple(row) for row in rows)


def contains(rows, vector, prime: int) -> bool:
    return rank_mod(rows + (vector,), prime) == len(rows)


def basis_mod(rows, prime: int):
    accepted = []
    for row in rows:
        if rank_mod(tuple(accepted) + (row,), prime) > len(accepted):
            accepted.append(row)
    return tuple(accepted)


def pair_vector(first, second, prime: int):
    return tuple(
        (
            first[left] * second[right]
            + first[right] * second[left]
        )
        % prime
        for left, right in PAIRS
    )


def pair_image(first_rows, second_rows, prime: int):
    return basis_mod(
        tuple(
            pair_vector(first, second, prime)
            for first in first_rows
            for second in second_rows
        ),
        prime,
    )


def pairing_rank(first, second, prime: int):
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    matrix = tuple(
        tuple(
            sum(
                left[index]
                * right[
                    pair_index[
                        tuple(
                            coordinate
                            for coordinate in range(4)
                            if coordinate not in pair
                        )
                    ]
                ]
                for index, pair in enumerate(PAIRS)
            )
            % prime
            for right in second
        )
        for left in first
    )
    return rank_mod(matrix, prime)


def audit_prime(prime: int) -> dict:
    h0 = (1, -1, 0, 0)
    u0 = (1, 1, 0, 0)
    h1 = (0, 0, 1, -1)
    u1 = (0, 0, 1, 1)
    hyperplane = (h0, u0, h1)
    hyperplane_pairs = pair_image(
        hyperplane,
        hyperplane,
        prime,
    )
    assert len(hyperplane_pairs) == 4

    planes = tuple(
        plane
        for plane in rref_subspaces(prime, 4, 2)
        if contains(plane, h0, prime)
    )
    k0 = next(
        plane
        for plane in planes
        if contains(plane, u0, prime)
    )
    nonexception_families = []
    for parameter in range(prime):
        vector = tuple(
            (
                u1[index] + parameter * u0[index]
            )
            % prime
            for index in range(4)
        )
        nonexception_families.append(
            next(
                plane
                for plane in planes
                if contains(plane, vector, prime)
            )
        )

    allowed_first_planes = set()
    for second in nonexception_families:
        for first in planes:
            rank_value = pairing_rank(
                pair_image(first, second, prime),
                hyperplane_pairs,
                prime,
            )
            if rank_value <= 1:
                allowed_first_planes.add(first)
                assert first == k0

    assert allowed_first_planes == {k0}
    return {
        "prime": prime,
        "planes_containing_h0": len(planes),
        "nonexception_family_planes": len(
            set(nonexception_families)
        ),
        "rank_one_compatible_first_planes": len(
            allowed_first_planes
        ),
    }


def main() -> None:
    output = {
        "audited": True,
        "finite_fields": [
            audit_prime(prime) for prime in (3, 5)
        ],
        "pair_image_boundary_checked": True,
        "marked_double_disjoint_exact_pattern_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "independent finite-field pair-image audit",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_marked_double_disjoint_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
