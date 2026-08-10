#!/usr/bin/env python3
"""Verify the marked double-plus-adjacent q5_221 obstruction."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank(rows: tuple[tuple[int, ...], ...]) -> int:
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
                (left - factor * right)
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


def restrict(
    rows: tuple[tuple[int, ...], ...],
    basis: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            sum(
                left * right
                for left, right in zip(row, vector, strict=True)
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
    common = (x_minus, y_minus, z)
    j20 = (x_minus, e[2], e[3])
    j12 = (e[0], e[1], y_plus)
    j21 = (e[0], e[1], y_minus)

    common_j20 = restrict(common, j20)
    assert rank(common_j20) == 2
    assert all(
        sum(
            left * right
            for left, right in zip(row, y_plus, strict=True)
        )
        == 0
        for row in common
    )

    exceptional = (x_minus, z, x_plus)
    exceptional_j12 = restrict(exceptional, j12)
    exceptional_j21 = restrict(exceptional, j21)
    assert rank(exceptional_j12) == 2
    assert rank(exceptional_j21) == 2
    assert all(row[2] == 0 for row in exceptional_j12)
    assert all(row[2] == 0 for row in exceptional_j21)

    # Use a=1 in h_1+a*u_0; nonzero a is the only invariant needed.
    plus_rows = (
        x_minus,
        z,
        tuple(
            y_minus[index] + x_plus[index]
            for index in range(5)
        ),
    )
    plus_j12 = restrict(plus_rows, j12)
    assert rank(plus_j12) == 2
    assert all(row[2] == 0 for row in plus_j12)

    minus_nonzero_rows = (
        x_minus,
        z,
        tuple(
            y_plus[index] + x_plus[index]
            for index in range(5)
        ),
    )
    minus_nonzero_j21 = restrict(minus_nonzero_rows, j21)
    assert rank(minus_nonzero_j21) == 2
    assert all(row[2] == 0 for row in minus_nonzero_j21)

    minus_boundary_rows = (x_minus, z, y_plus)
    minus_boundary_j12 = restrict(minus_boundary_rows, j12)
    assert rank(minus_boundary_j12) == 2
    # Its plane normal is proportional to x_+=e_0+e_1 and therefore
    # has support exactly {0,1}.
    assert all(
        sum(
            left * right
            for left, right in zip(row, x_plus[:3], strict=True)
        )
        == 0
        for row in minus_boundary_j12
    )

    output = {
        "verified": True,
        "field": "C",
        "residual_spaces_checked": ["J20", "J12", "J21"],
        "all_normal_j20_rank": rank(common_j20),
        "rank_one_boundary_support_one_planes_checked": 2,
        "plus_sign_support_one_plane_checked": True,
        "minus_nonzero_support_one_plane_checked": True,
        "minus_boundary_support": [0, 1],
        "conclusion": (
            "exact singleton-doubled adjacent pattern excluded"
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
        / "p5_q5_221_marked_double_adjacent_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
