#!/usr/bin/env python3
"""Independent finite-field census of zero P3 plane restrictions."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rref(
    rows: list[list[int]],
    columns: int,
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    matrix = [
        [value % prime for value in row]
        for row in rows
        if any(value % prime for value in row)
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
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime for value in matrix[pivot_row]
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
    return tuple(tuple(row) for row in matrix[:pivot_row])


def planes(prime: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    result = []
    for pivots in itertools.combinations(range(3), 2):
        free_positions = [
            (row, column)
            for row, pivot in enumerate(pivots)
            for column in range(pivot + 1, 3)
            if column not in pivots
        ]
        for values in itertools.product(
            range(prime),
            repeat=len(free_positions),
        ):
            basis = [[0] * 3 for _ in range(2)]
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


def permanent_three(
    first: tuple[int, ...],
    second: tuple[int, ...],
    third: tuple[int, ...],
    prime: int,
) -> int:
    return sum(
        first[permutation[0]]
        * second[permutation[1]]
        * third[permutation[2]]
        for permutation in itertools.permutations(range(3))
    ) % prime


def restriction_is_zero(
    first: tuple[tuple[int, ...], ...],
    second: tuple[tuple[int, ...], ...],
    third: tuple[tuple[int, ...], ...],
    prime: int,
) -> bool:
    return all(
        permanent_three(u, v, w, prime) == 0
        for u in first
        for v in second
        for w in third
    )


def audit_prime(prime: int) -> dict[str, int]:
    all_planes = planes(prime)
    expected_count = (prime**3 - 1) // (prime - 1)
    assert len(all_planes) == expected_count
    all_subspaces = all_planes + (
        ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
    )

    coordinate_planes = {
        rref(
            [
                [1 if row == column else 0 for column in range(3)]
                for row in range(3)
                if row != missing
            ],
            3,
            prime,
        )
        for missing in range(3)
    }

    zero_triples = []
    for first_index, first in enumerate(all_subspaces):
        for second_index, second in enumerate(all_subspaces):
            for third_index, third in enumerate(all_subspaces):
                if restriction_is_zero(first, second, third, prime):
                    zero_triples.append(
                        (first_index, second_index, third_index)
                    )

    expected_triples = {
        (index, index, index)
        for index, plane in enumerate(all_planes)
        if plane in coordinate_planes
    }
    assert set(zero_triples) == expected_triples
    assert len(zero_triples) == 3
    return {
        "planes": len(all_planes),
        "full_spaces": 1,
        "rank_at_least_two_subspaces": len(all_subspaces),
        "ordered_subspace_triples": len(all_subspaces) ** 3,
        "zero_restrictions": len(zero_triples),
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (3, 5)}
    output = {
        "audited": True,
        "finite_fields": ["F_3", "F_5"],
        "audits": audits,
        "zero_restrictions_in_each_field": 3,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "finite-field audit; written theorem is over C",
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p3_zero_hyperplane_product_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
