#!/usr/bin/env python3
"""Independent no-import audit of the local zero-cofactor syzygy."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction


def permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    states = {0: 1}
    size = len(matrix)
    for column in range(size):
        next_states = {}
        for mask, value in states.items():
            for row in range(size):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, 0) + (
                    value * matrix[row][column]
                )
        states = next_states
    return states[(1 << size) - 1]


def data():
    common = (
        ((-1, -2, -1), (0, -1, 1), (-1, -1, -2), (-1, -1, -2)),
        ((0, 0, 0), (0, 0, 0), (0, -1, -2), (1, 2, 2)),
        ((2, -2, 0), (0, 0, 1), (-2, 2, 1), (2, -2, 1)),
        ((-2, 0, 1), (2, -2, 0), (0, 0, -2), (-2, 0, 2)),
        ((2, -2, 0), (0, -1, 0), (1, 0, -1), (2, 1, -2)),
        ((1, 0, 1), (0, 2, 0), (0, 2, 1), (-1, 2, 0)),
    )
    matrices = (
        ((0, 1), ((-1, -1, 0), (-1, -1, 0), (-2, -2, 0))),
        ((0, 2), ((0, 0, 2), (0, 0, 2), (0, 0, 4))),
        ((0, 3), ((-2, 0, 0), (-2, 0, 0), (-4, 0, 0))),
        ((0, 4), ((3, 1, -3), (3, 1, -3), (6, 2, -6))),
        ((0, 5), ((-1, 4, 1), (-1, 4, 1), (-2, 8, 2))),
        ((1, 2), ((-2, 2, 1), (-6, 6, 1), (-8, 8, 0))),
        ((1, 3), ((0, 0, -2), (2, 0, -6), (4, 0, -8))),
        ((1, 4), ((1, 0, -1), (0, -1, 0), (-2, -2, 2))),
        ((1, 5), ((0, 2, 1), (1, 2, 2), (2, 0, 2))),
        ((2, 3), ((-4, 0, 8), (4, 0, -8), (2, 0, 0))),
        ((2, 4), ((2, 2, -2), (-2, -2, 2), (-3, -1, 3))),
        ((2, 5), ((-2, 0, -2), (2, 0, 2), (1, -4, -1))),
        ((3, 4), ((2, 0, -2), (0, 0, 0), (2, 2, -2))),
        ((3, 5), ((0, 4, 2), (0, 0, 0), (-2, 0, -2))),
        ((4, 5), ((1, -6, -2), (0, -2, -1), (-1, 6, 2))),
    )
    return common, dict(matrices)


def cofactor(common, word, left, right):
    modes = tuple(mode for mode in range(6) if mode not in (left, right))
    matrix = tuple(
        tuple(common[mode][root][word[mode]] for mode in modes) for root in range(4)
    )
    return permanent(matrix)


def rank(matrix) -> int:
    rows = [[Fraction(entry) for entry in row] for row in matrix]
    result = 0
    for column in range(3):
        pivot = next(
            (index for index in range(result, len(rows)) if rows[index][column]),
            None,
        )
        if pivot is None:
            continue
        rows[result], rows[pivot] = rows[pivot], rows[result]
        value = rows[result][column]
        rows[result] = [entry / value for entry in rows[result]]
        for index in range(len(rows)):
            if index == result:
                continue
            factor = rows[index][column]
            rows[index] = [
                left - factor * right for left, right in zip(rows[index], rows[result])
            ]
        result += 1
    return result


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def evaluate(vector, matrix):
    return tuple(
        sum(vector[row] * matrix[row][column] for row in range(3))
        for column in range(3)
    )


def main() -> None:
    common, blocks = data()
    assert tuple(rank(matrix) for matrix in common) == (2, 2, 2, 3, 3, 3)
    assert len(blocks) == 15
    assert all(
        any(entry for row in matrix for entry in row) for matrix in blocks.values()
    )

    coefficients = []
    for word in itertools.product(range(3), repeat=6):
        value = sum(
            matrix[word[left]][word[right]] * cofactor(common, word, left, right)
            for (left, right), matrix in blocks.items()
        )
        assert value == 0
        coefficients.append(value)
    assert len(coefficients) == 729

    encoded = ";".join(
        ",".join(str(entry) for row in blocks[edge] for entry in row)
        for edge in sorted(blocks)
    ).encode()
    digest = hashlib.sha256(encoded).hexdigest()

    # Independent contraction checks for zero desired common rows and for
    # the exchanged root/port block sections.
    x, z_a, z_b = (1, 1, 1), (1, 2, 3), (1, 3, 2)
    null_block = ((1, 0, 0), (-1, 0, 0), (0, 0, 0))
    assert evaluate(x, null_block) == (0, 0, 0)
    assert any(entry for row in null_block for entry in row)

    alpha_a, zeta_a = (2, -1, 0), (-1, 1, 0)
    alpha_b = (Fraction(3, 2), Fraction(-1, 2), Fraction(0))
    zeta_b = (Fraction(-1, 2), Fraction(1, 2), Fraction(0))
    root_a, root_b = (1, 0, 0), (0, 1, 0)
    port_a, port_b = (0, 1, 1), (1, 0, 1)

    def outer(left, right):
        return tuple(tuple(a * b for b in right) for a in left)

    def add(left, right):
        return tuple(
            tuple(left[row][column] + right[row][column] for column in range(3))
            for row in range(3)
        )

    block_a = add(outer(alpha_a, root_a), outer(zeta_a, port_a))
    block_b = add(outer(alpha_b, root_b), outer(zeta_b, port_b))
    assert evaluate(x, block_a) == root_a
    assert evaluate(z_a, block_a) == port_a
    assert evaluate(x, block_b) == root_b
    assert evaluate(z_b, block_b) == port_b

    # Separate subset-permanent evaluation of the failing mixed endpoint.
    word = (0, 0, 0, 0, 0, 1)
    endpoint = tuple(
        tuple((*common[mode], root_a, port_b)[row][word[mode]] for mode in range(6))
        for row in range(6)
    )
    assert permanent(endpoint) == 44

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "no-import coefficient and local-block reconstruction",
                "field": "rational characteristic zero",
                "cofactor_coefficients_checked": len(coefficients),
                "blocker_blocks_nonzero": len(blocks),
                "block_data_sha256": digest,
                "endpoint_off_diagonal_coefficient": 44,
                "global_matching_identity_realized": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
