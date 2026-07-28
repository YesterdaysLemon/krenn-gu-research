#!/usr/bin/env python3
"""Independent finite-field audit of the marked-adjacent obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    if not rows:
        return 0
    matrix = [[value % prime for value in row] for row in rows]
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


def rref_subspaces(prime: int):
    for pivots in itertools.combinations(range(5), 3):
        free_positions = tuple(
            (row, column)
            for column in range(5)
            if column not in pivots
            for row, pivot in enumerate(pivots)
            if pivot < column
        )
        for values in itertools.product(
            range(prime),
            repeat=len(free_positions),
        ):
            rows = [[0] * 5 for _ in range(3)]
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
    return rank_mod(rows + (vector,), prime) == 3


def restriction_rank(rows, basis, prime: int) -> int:
    restricted = tuple(
        tuple(
            sum(
                left * right
                for left, right in zip(row, vector, strict=True)
            )
            % prime
            for vector in basis
        )
        for row in rows
    )
    return rank_mod(restricted, prime)


def audit_prime(prime: int) -> dict:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    x_plus = (1, 1, 0, 0, 0)
    x_minus = (1, -1, 0, 0, 0)
    y_plus = (0, 0, 1, 1, 0)
    y_minus = (0, 0, 1, -1, 0)
    z = e[4]
    j20 = (x_minus, e[2], e[3])
    j12 = (e[0], e[1], y_plus)
    j21 = (e[0], e[1], y_minus)

    spaces = tuple(rref_subspaces(prime))
    exact_b = tuple(
        rows
        for rows in spaces
        if contains(rows, x_minus, prime)
        and contains(rows, z, prime)
        and not contains(rows, y_minus, prime)
    )
    exact_c = tuple(
        rows
        for rows in spaces
        if contains(rows, y_minus, prime)
        and not contains(rows, x_minus, prime)
        and not contains(rows, z, prime)
    )
    assert exact_b and exact_c

    exceptional_b = tuple(
        rows
        for rows in exact_b
        if contains(rows, x_plus, prime)
    )
    assert all(
        restriction_rank(rows, j12, prime) == 2
        and restriction_rank(rows, j21, prime) == 2
        for rows in exceptional_b
    )

    assert all(
        restriction_rank(rows, j20, prime) >= 2
        for rows in exact_c
    )
    assert all(
        restriction_rank(rows, j12, prime) >= 2
        and restriction_rank(rows, j21, prime) >= 2
        for rows in exact_c
    )

    no_u1_no_h2 = tuple(
        rows
        for rows in exact_c
        if all(
            sum(
                left * right
                for left, right in zip(row, y_plus, strict=True)
            )
            % prime
            == 0
            for row in rows
        )
    )
    assert all(
        restriction_rank(rows, j21, prime) == 3
        for rows in no_u1_no_h2
    )

    return {
        "prime": prime,
        "rank_three_row_spaces": len(spaces),
        "exact_B_spaces": len(exact_b),
        "exact_C_spaces": len(exact_c),
        "exceptional_B_spaces": len(exceptional_b),
        "C_spaces_killing_y_plus": len(no_u1_no_h2),
    }


def main() -> None:
    output = {
        "audited": True,
        "finite_fields": [
            audit_prime(prime) for prime in (3, 5)
        ],
        "rank_gates_checked": ["J20", "J12", "J21"],
        "marked_double_adjacent_exact_pattern_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "independent finite-field linear-algebra audit",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_marked_double_adjacent_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
