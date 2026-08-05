#!/usr/bin/env python3
"""Independent finite-field audit of the nonzero diagonal cofactor core."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_NONZERO_DIAGONAL_COFACTOR_NO_TORUS_P6.md"


def data():
    common = []
    for mode in range(4):
        matrix = [[0] * 3 for _ in range(4)]
        matrix[mode][0] = 1
        matrix[(mode + 1) % 4][1] = 1
        common.append(matrix)
    common.extend(
        (
            ((0, -4, 4), (2, -3, 2), (2, 5, -6), (2, 1, -2)),
            ((-1, 0, -4), (-2, -4, 0), (0, -2, 4), (0, 1, -2)),
        )
    )
    blocks = {
        (0, 1): ((1478, 128, 0), (1007, 980, 0), (0, 0, 0)),
        (0, 2): ((-128, 384, 0), (-980, -120, 0), (0, 0, 0)),
        (0, 3): ((-384, 356, 0), (120, 1478, 0), (0, 0, 0)),
        (0, 4): ((640, 784, -784), (234, 1225, -1374), (0, 0, 0)),
        (0, 5): ((100, -384, 1296), (1672, 3772, -1240), (0, 0, 0)),
        (1, 2): ((980, 120, 0), (298, -512, 0), (0, 0, 0)),
        (1, 3): ((-120, -1478, 0), (512, -128, 0), (0, 0, 0)),
        (1, 4): ((-2248, 1796, -640), (-340, -2130, 2428), (0, 0, 0)),
        (1, 5): ((342, 256, 1240), (256, 980, -680), (0, 0, 0)),
        (2, 3): ((-512, 128, 0), (384, -384, 0), (0, 0, 0)),
        (2, 4): ((-256, 640, -640), (-512, 0, 1152), (0, 0, 0)),
        (2, 5): ((-256, -384, -512), (384, -128, 384), (0, 0, 0)),
        (3, 4): ((-256, -384, -384), (-640, 640, -640), (0, 0, 0)),
        (3, 5): ((-384, -256, 384), (256, 384, 128), (0, 0, 0)),
        (4, 5): ((576, 1536, 2304), (-256, 512, -512), (-416, -512, -640)),
    }
    return tuple(tuple(tuple(row) for row in matrix) for matrix in common), blocks


PERMUTATIONS = tuple(itertools.permutations(range(4)))


def permanent_four(matrix):
    return sum(
        matrix[0][permutation[0]]
        * matrix[1][permutation[1]]
        * matrix[2][permutation[2]]
        * matrix[3][permutation[3]]
        for permutation in PERMUTATIONS
    )


def cofactor(common, word, left, right):
    modes = [mode for mode in range(6) if mode not in (left, right)]
    return permanent_four(
        [[common[mode][root][word[mode]] for mode in modes] for root in range(4)]
    )


def coefficient(common, blocks, word):
    return sum(
        block[word[left]][word[right]] * cofactor(common, word, left, right)
        for (left, right), block in blocks.items()
    )


def matrix_rows(common, edges):
    variables = tuple(
        (left, right, row, column)
        for left, right in edges
        for row in range(3)
        for column in range(3)
    )
    indices = {variable: index for index, variable in enumerate(variables)}
    off = []
    diagonal = []
    for word in itertools.product(range(3), repeat=6):
        row = {}
        for left, right in edges:
            value = cofactor(common, word, left, right)
            if value:
                row[indices[left, right, word[left], word[right]]] = value
        (diagonal if len(set(word)) == 1 else off).append(row)
    return off, diagonal


def rank_mod(rows, prime):
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


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert "finite fields only" in theorem
    assert "No finite-field output is used" in theorem
    common, blocks = data()

    coefficients = [
        coefficient(common, blocks, word)
        for word in itertools.product(range(3), repeat=6)
    ]
    nonzero = [(index, value) for index, value in enumerate(coefficients) if value]
    assert nonzero == [(0, -1536), ((3**6 - 1) // 2, 1536)]

    off, diagonal = matrix_rows(common, tuple(blocks))
    ranks = {}
    for prime in (101, 1009):
        ranks[prime] = {
            "off": rank_mod(off, prime),
            "full": rank_mod([*off, *diagonal], prime),
        }
    assert ranks == {
        101: {"off": 108, "full": 109},
        1009: {"off": 108, "full": 109},
    }

    payload = repr((common, tuple(sorted(blocks.items())))).encode()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "finite-field ranks only; integer tensor checked directly",
                "data_sha256": hashlib.sha256(payload).hexdigest(),
                "cofactor_nonzero_coefficients": nonzero,
                "ranks_mod_prime": ranks,
                "finite_field_used_for_characteristic_zero_proof": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
