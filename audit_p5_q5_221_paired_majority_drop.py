#!/usr/bin/env python3
"""Independent finite-field audit of the paired-majority rank gates."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
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


def rref_subspaces(
    prime: int,
    ambient: int,
    dimension: int,
):
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
            rows = [
                [0] * ambient for _ in range(dimension)
            ]
            for row, pivot in enumerate(pivots):
                rows[row][pivot] = 1
            for (row, column), value in zip(
                free_positions,
                values,
                strict=True,
            ):
                rows[row][column] = value
            yield tuple(tuple(row) for row in rows)


def contains(
    rows: tuple[tuple[int, ...], ...],
    vector: tuple[int, ...],
    prime: int,
) -> bool:
    return rank_mod(rows + (vector,), prime) == len(rows)


def restriction_rank(
    rows: tuple[tuple[int, ...], ...],
    basis: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
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
    x_plus = (1, 1, 0, 0, 0)
    x_minus = (1, -1, 0, 0, 0)
    y_plus = (0, 0, 1, 1, 0)
    y_minus = (0, 0, 1, -1, 0)
    z = (0, 0, 0, 0, 1)
    common = (x_minus, y_minus, z)
    j01 = (x_plus, y_minus, z)
    j10 = (x_minus, y_plus, z)

    spaces = tuple(rref_subspaces(prime, 5, 3))
    non_h0 = tuple(
        rows for rows in spaces if not contains(rows, x_minus, prime)
    )
    non_h1 = tuple(
        rows for rows in spaces if not contains(rows, y_minus, prime)
    )
    assert all(
        restriction_rank(rows, j01, prime) >= 2
        for rows in non_h0
    )
    assert all(
        restriction_rank(rows, j10, prime) >= 2
        for rows in non_h1
    )

    annihilates_both = tuple(
        rows
        for rows in spaces
        if all(
            sum(
                left * right
                for left, right in zip(row, vector, strict=True)
            )
            % prime
            == 0
            for row in rows
            for vector in (x_plus, y_plus)
        )
    )
    assert len(annihilates_both) == 1
    assert all(
        contains(annihilates_both[0], row, prime)
        for row in common
    )

    exceptional_u1 = (x_minus, y_minus, y_plus)
    exceptional_u0 = (x_minus, y_minus, x_plus)
    assert restriction_rank(exceptional_u1, j01, prime) == 1
    assert restriction_rank(exceptional_u1, j10, prime) == 2
    assert restriction_rank(exceptional_u0, j01, prime) == 2
    assert restriction_rank(exceptional_u0, j10, prime) == 1

    support_two_or_three = tuple(
        frozenset(support)
        for size in (2, 3)
        for support in itertools.combinations(range(3), size)
    )
    paired_supports = (
        frozenset((0, 2)),
        frozenset((1, 2)),
    )
    singleton_containing_plane_supports = tuple(
        support for support in support_two_or_three if 2 not in support
    )
    assert all(
        support not in singleton_containing_plane_supports
        for support in paired_supports
    )

    return {
        "prime": prime,
        "rank_three_row_spaces": len(spaces),
        "spaces_avoiding_h0": len(non_h0),
        "spaces_avoiding_h1": len(non_h1),
        "common_kernel_annihilators": len(annihilates_both),
        "rank_one_exceptions_checked": 2,
        "normal_support_conflicts_checked": 2,
    }


def main() -> None:
    audits = [audit_prime(prime) for prime in (3, 5)]
    output = {
        "audited": True,
        "finite_fields": audits,
        "paired_majority_exact_pair_excluded": True,
        "common_kernel_unique": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "independent finite-field linear-algebra audit",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q5_221_paired_majority_drop_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
