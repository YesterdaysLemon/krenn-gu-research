#!/usr/bin/env python3
"""Verify the marked double-plus-disjoint q5_221 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md"
)
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(rows) -> int:
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
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
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [
            value / pivot_value for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right
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


def pair_vector(first, second):
    return tuple(
        first[left] * second[right]
        + first[right] * second[left]
        for left, right in PAIRS
    )


def row_basis(rows):
    accepted = []
    for row in rows:
        if rank(tuple(accepted) + (row,)) > len(accepted):
            accepted.append(row)
    return tuple(accepted)


def pair_image(first_rows, second_rows):
    return row_basis(
        tuple(
            pair_vector(first, second)
            for first in first_rows
            for second in second_rows
        )
    )


def complement_pairing(first, second):
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    matrix = []
    for left in first:
        row = []
        for right in second:
            value = 0
            for index, pair in enumerate(PAIRS):
                complement = tuple(
                    coordinate
                    for coordinate in range(4)
                    if coordinate not in pair
                )
                value += left[index] * right[
                    pair_index[complement]
                ]
            row.append(value)
        matrix.append(tuple(row))
    return tuple(matrix)


def main() -> None:
    h0 = (1, -1, 0, 0)
    u0 = (1, 1, 0, 0)
    h1 = (0, 0, 1, -1)
    u1 = (0, 0, 1, 1)
    common_hyperplane = (h0, u0, h1)
    common_pair_image = pair_image(
        common_hyperplane,
        common_hyperplane,
    )
    assert len(common_pair_image) == 4

    k0 = (h0, u0)
    k1 = (h0, u1)
    for parameter in (-2, -1, 0, 1, 2):
        ub = (
            h0,
            tuple(
                u1[index] + parameter * u0[index]
                for index in range(4)
            ),
        )
        pairing = complement_pairing(
            pair_image(k0, ub),
            common_pair_image,
        )
        assert rank(pairing) == 1

        for second_parameter in (-2, -1, 0, 1, 2):
            ua = (
                h0,
                tuple(
                    u1[index] + second_parameter * u0[index]
                    for index in range(4)
                ),
            )
            nonexception_pairing = complement_pairing(
                pair_image(ua, ub),
                common_pair_image,
            )
            assert rank(nonexception_pairing) >= 2

    p2_k0_rank = rank(
        tuple(
            tuple(
                row[coordinate] for coordinate in (0, 1)
            )
            for row in k0
        )
    )
    p2_k1_rank = rank(
        tuple(
            tuple(
                row[coordinate] for coordinate in (0, 1)
            )
            for row in k1
        )
    )
    assert p2_k0_rank == 2
    assert p2_k1_rank == 1

    residual_three_space = (0, 1, 4)
    full_k0 = (
        (1, -1, 0, 0, 0),
        (0, 0, 0, 0, 1),
        (1, 1, 0, 0, 0),
    )
    k0_residual_rank = rank(
        tuple(
            tuple(row[index] for index in residual_three_space)
            for row in full_k0
        )
    )
    assert k0_residual_rank == 3

    output = {
        "verified": True,
        "field": "C",
        "common_hyperplane_pair_image_dimension": len(
            common_pair_image
        ),
        "mixed_K0_Ub_flattening_rank": 1,
        "two_nonexception_flattening_minimum_rank": 2,
        "K0_P2_rank": p2_k0_rank,
        "K1_P2_rank": p2_k1_rank,
        "final_K0_residual_rank": k0_residual_rank,
        "conclusion": (
            "exact singleton-doubled disjoint pattern excluded"
        ),
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_marked_double_disjoint_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
