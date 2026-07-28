#!/usr/bin/env python3
"""Verify the paired-majority q5_221 drop obstruction scaffold."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_rank(rows: tuple[tuple[int, ...], ...]) -> int:
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


def restriction(
    rows: tuple[tuple[int, ...], ...],
    basis: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(
                first * second
                for first, second in zip(row, vector, strict=True)
            )
            for vector in basis
        )
        for row in rows
    )


def main() -> None:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    x_plus = (1, 1, 0, 0, 0)
    x_minus = (1, -1, 0, 0, 0)
    y_plus = (0, 0, 1, 1, 0)
    y_minus = (0, 0, 1, -1, 0)
    z = e[4]
    common_rows = (x_minus, y_minus, z)
    j01 = (x_plus, y_minus, z)
    j10 = (x_minus, y_plus, z)
    j01_annihilator = (x_minus, y_plus)
    j10_annihilator = (x_plus, y_minus)

    assert matrix_rank(common_rows) == 3
    assert matrix_rank(j01) == matrix_rank(j10) == 3
    for basis, annihilator in (
        (j01, j01_annihilator),
        (j10, j10_annihilator),
    ):
        assert matrix_rank(annihilator) == 2
        assert all(
            sum(
                left * right
                for left, right in zip(row, vector, strict=True)
            )
            == 0
            for row in annihilator
            for vector in basis
        )

    common_on_j01 = restriction(common_rows, j01)
    common_on_j10 = restriction(common_rows, j10)
    assert matrix_rank(common_on_j01) == 2
    assert matrix_rank(common_on_j10) == 2
    assert all(row[0] == 0 for row in common_on_j01)
    assert all(row[1] == 0 for row in common_on_j10)

    common_kernel = (x_plus, y_plus)
    assert matrix_rank(common_kernel) == 2
    assert all(
        sum(
            left * right
            for left, right in zip(row, vector, strict=True)
        )
        == 0
        for row in common_rows
        for vector in common_kernel
    )

    exceptional_u1_rows = (x_minus, y_minus, y_plus)
    exceptional_u0_rows = (x_minus, y_minus, x_plus)
    exceptional_u1_on_j10 = restriction(
        exceptional_u1_rows,
        j10,
    )
    exceptional_u0_on_j01 = restriction(
        exceptional_u0_rows,
        j01,
    )
    assert matrix_rank(exceptional_u1_on_j10) == 2
    assert matrix_rank(exceptional_u0_on_j01) == 2
    assert all(row[2] == 0 for row in exceptional_u1_on_j10)
    assert all(row[2] == 0 for row in exceptional_u0_on_j01)

    # In the complementary branch, a nonzero Q_01 normal at the
    # paired-majority mode must use {x_+,z}, while a plane containing
    # h_2 has a normal with zero z-coordinate.  Q_10 is symmetric.
    paired_q01_normal_support = frozenset((0, 2))
    paired_q10_normal_support = frozenset((1, 2))
    singleton_plane_normal_supports = {
        frozenset(support)
        for size in (2, 3)
        for support in itertools.combinations(range(3), size)
        if 2 not in support
    }
    assert paired_q01_normal_support not in (
        singleton_plane_normal_supports
    )
    assert paired_q10_normal_support not in (
        singleton_plane_normal_supports
    )

    output = {
        "verified": True,
        "field": "C",
        "j01_rank": matrix_rank(j01),
        "j10_rank": matrix_rank(j10),
        "common_row_space_rank": matrix_rank(common_rows),
        "common_restriction_ranks": [
            matrix_rank(common_on_j01),
            matrix_rank(common_on_j10),
        ],
        "support_one_coordinates_killed": ["x_plus", "y_plus"],
        "forced_kernel_rank": matrix_rank(common_kernel),
        "rank_one_exceptions_checked": ["u0", "u1"],
        "complementary_support_conflicts_checked": 2,
        "conclusion": "exact majority drop pairs cannot coincide",
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_paired_majority_drop_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
