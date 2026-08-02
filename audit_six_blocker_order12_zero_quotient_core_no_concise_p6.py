#!/usr/bin/env python3
"""Independent finite-field audit of the fixed common-row obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_CORE_NO_CONCISE_P6.md"

COMMON = (
    ((-1, -2, -1), (0, -1, 1), (-1, -1, -2), (-1, -1, -2)),
    ((0, 0, 0), (0, 0, 0), (0, -1, -2), (1, 2, 2)),
    ((2, -2, 0), (0, 0, 1), (-2, 2, 1), (2, -2, 1)),
    ((-2, 0, 1), (2, -2, 0), (0, 0, -2), (-2, 0, 2)),
    ((2, -2, 0), (0, -1, 0), (1, 0, -1), (2, 1, -2)),
    ((1, 0, 1), (0, 2, 0), (0, 2, 1), (-1, 2, 0)),
)

BLOCKS = {
    (0, 1): ((-1, -1, 0), (-1, -1, 0), (-2, -2, 0)),
    (0, 2): ((0, 0, 2), (0, 0, 2), (0, 0, 4)),
    (0, 3): ((-2, 0, 0), (-2, 0, 0), (-4, 0, 0)),
    (0, 4): ((3, 1, -3), (3, 1, -3), (6, 2, -6)),
    (0, 5): ((-1, 4, 1), (-1, 4, 1), (-2, 8, 2)),
    (1, 2): ((-2, 2, 1), (-6, 6, 1), (-8, 8, 0)),
    (1, 3): ((0, 0, -2), (2, 0, -6), (4, 0, -8)),
    (1, 4): ((1, 0, -1), (0, -1, 0), (-2, -2, 2)),
    (1, 5): ((0, 2, 1), (1, 2, 2), (2, 0, 2)),
    (2, 3): ((-4, 0, 8), (4, 0, -8), (2, 0, 0)),
    (2, 4): ((2, 2, -2), (-2, -2, 2), (-3, -1, 3)),
    (2, 5): ((-2, 0, -2), (2, 0, 2), (1, -4, -1)),
    (3, 4): ((2, 0, -2), (0, 0, 0), (2, 2, -2)),
    (3, 5): ((0, 4, 2), (0, 0, 0), (-2, 0, -2)),
    (4, 5): ((1, -6, -2), (0, -2, -1), (-1, 6, 2)),
}


def permanent_four(matrix) -> int:
    return sum(
        matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
        * matrix[3][permutation[3]]
        for permutation in itertools.permutations(range(4))
    )


def cofactor(word, left: int, right: int) -> int:
    modes = [mode for mode in range(6) if mode not in (left, right)]
    return permanent_four(
        [[COMMON[mode][root][word[mode]] for mode in modes] for root in range(4)]
    )


def coefficient(word) -> int:
    return sum(
        block[word[left]][word[right]] * cofactor(word, left, right)
        for (left, right), block in BLOCKS.items()
    )


def rank_mod_prime(rows, prime: int) -> int:
    basis = {}
    for source in rows:
        row = {
            column: value % prime for column, value in source.items() if value % prime
        }
        while row:
            pivot = min(row)
            value = row[pivot]
            if pivot not in basis:
                inverse = pow(value, prime - 2, prime)
                basis[pivot] = {
                    column: entry * inverse % prime
                    for column, entry in row.items()
                    if entry % prime
                }
                break
            for column, entry in basis[pivot].items():
                updated = (row.get(column, 0) - value * entry) % prime
                if updated:
                    row[column] = updated
                elif column in row:
                    del row[column]
    return len(basis)


def off_diagonal_rows():
    variables = tuple(
        (left, right, row, column)
        for left, right in BLOCKS
        for row in range(3)
        for column in range(3)
    )
    indices = {variable: index for index, variable in enumerate(variables)}
    rows = []
    for word in itertools.product(range(3), repeat=6):
        if len(set(word)) == 1:
            continue
        row = {}
        for left, right in BLOCKS:
            value = cofactor(word, left, right)
            if value:
                row[indices[left, right, word[left], word[right]]] = value
        rows.append(row)
    return rows


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "finite-field audit" in theorem
    assert "characteristic-zero proof" in theorem

    payload = repr((COMMON, tuple(sorted(BLOCKS.items())))).encode()
    digest = hashlib.sha256(payload).hexdigest()
    coefficients = [coefficient(word) for word in itertools.product(range(3), repeat=6)]
    assert coefficients == [0] * (3**6)

    rows = off_diagonal_rows()
    ranks = {prime: rank_mod_prime(rows, prime) for prime in (101, 1009)}
    assert ranks == {101: 134, 1009: 134}

    # A nonzero 134-minor modulo either prime audits rank_Q >= 134.  The
    # displayed nonzero rational kernel generator audits rank_Q <= 134.
    assert any(entry for block in BLOCKS.values() for row in block for entry in row)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "finite-field only; characteristic-zero proof is primary",
                "data_sha256": digest,
                "coefficients_checked": len(coefficients),
                "kernel_full_tensor_nonzero_coefficients": sum(
                    value != 0 for value in coefficients
                ),
                "off_diagonal_ranks_mod_prime": ranks,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
