#!/usr/bin/env python3
"""Verify the exact local zero-cofactor syzygy."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md"


def common_rows() -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.Matrix(rows)
        for rows in (
            ((-1, -2, -1), (0, -1, 1), (-1, -1, -2), (-1, -1, -2)),
            ((0, 0, 0), (0, 0, 0), (0, -1, -2), (1, 2, 2)),
            ((2, -2, 0), (0, 0, 1), (-2, 2, 1), (2, -2, 1)),
            ((-2, 0, 1), (2, -2, 0), (0, 0, -2), (-2, 0, 2)),
            ((2, -2, 0), (0, -1, 0), (1, 0, -1), (2, 1, -2)),
            ((1, 0, 1), (0, 2, 0), (0, 2, 1), (-1, 2, 0)),
        )
    )


def blocker_blocks() -> dict[tuple[int, int], sp.Matrix]:
    entries = {
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
    return {edge: sp.Matrix(matrix) for edge, matrix in entries.items()}


def permanent(matrix: list[list[int | sp.Expr]]) -> sp.Expr:
    size = len(matrix)
    return sp.expand(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def cofactor(common: tuple[sp.Matrix, ...], word, left: int, right: int) -> sp.Expr:
    modes = [mode for mode in range(6) if mode not in (left, right)]
    matrix = [[common[mode][root, word[mode]] for mode in modes] for root in range(4)]
    return permanent(matrix)


def cofactor_coefficient(common, blocks, word) -> sp.Expr:
    return sp.expand(
        sum(
            block[word[left], word[right]] * cofactor(common, word, left, right)
            for (left, right), block in blocks.items()
        )
    )


def exact_off_diagonal_rank(common, edges) -> int:
    variables = tuple(
        (left, right, row, column)
        for left, right in edges
        for row in range(3)
        for column in range(3)
    )
    indices = {variable: index for index, variable in enumerate(variables)}
    rows = []
    for word in itertools.product(range(3), repeat=6):
        if len(set(word)) == 1:
            continue
        data: dict[int, Fraction] = {}
        for left, right in edges:
            value = int(cofactor(common, word, left, right))
            if value:
                data[indices[left, right, word[left], word[right]]] = Fraction(value)
        rows.append(data)

    # Exact sparse rational echelon reduction.  A modular rank is not used.
    basis: dict[int, dict[int, Fraction]] = {}
    for source in rows:
        row = dict(source)
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = Fraction(1, 1) / row[pivot]
                row = {
                    column: value * inverse for column, value in row.items() if value
                }
                basis[pivot] = row
                break
            factor = row[pivot]
            for column, value in basis[pivot].items():
                updated = row.get(column, Fraction(0)) - factor * value
                if updated:
                    row[column] = updated
                elif column in row:
                    del row[column]
    assert len(rows) == 726
    assert len(variables) == 135
    return len(basis)


def profile(rows: sp.Matrix) -> int:
    rank = rows.rank()
    mask = 0
    for colour in range(3):
        if rows.col_join(sp.eye(3).row(colour)).rank() == rank:
            mask |= 1 << colour
    return mask


def local_realization(common: tuple[sp.Matrix, ...]) -> None:
    x = sp.Matrix([1, 1, 1])
    z_a = sp.Matrix([1, 2, 3])
    z_b = sp.Matrix([1, 3, 2])
    e0 = sp.Matrix([1, 0, 0])
    h_a = sp.Matrix([1, -2, 1])
    h_b = sp.Matrix([-1, -1, 2])
    alpha_a = sp.Matrix([2, -1, 0])
    zeta_a = sp.Matrix([-1, 1, 0])
    alpha_b = sp.Matrix([sp.Rational(3, 2), sp.Rational(-1, 2), 0])
    zeta_b = sp.Matrix([sp.Rational(-1, 2), sp.Rational(1, 2), 0])
    cross = alpha_a * alpha_b.T
    assert (x.T * cross * x)[0] == 1
    assert (x.T * cross * z_b)[0] == 0
    assert (z_a.T * cross * x)[0] == 0

    nonblocker_a = sp.Matrix.vstack(h_a.T, alpha_a.T)
    nonblocker_b = sp.Matrix.vstack(h_b.T, alpha_b.T)
    assert nonblocker_a.rank() == nonblocker_b.rank() == 2
    assert nonblocker_a * z_a == sp.zeros(2, 1)
    assert nonblocker_b * z_b == sp.zeros(2, 1)
    assert profile(nonblocker_a) == profile(nonblocker_b) == 0

    root_pair = sp.diag(1, -1, 0)
    common_to_a = e0 * h_a.T
    common_to_b = e0 * h_b.T
    for block in (root_pair, common_to_a, common_to_b, cross):
        assert block != sp.zeros(3)
    assert (x.T * root_pair * x)[0] == 0
    assert (x.T * common_to_a * x)[0] == 0
    assert (x.T * common_to_b * x)[0] == 0

    null_section = sp.Matrix([1, -1, 0])
    for matrix in common:
        for root in range(4):
            desired = matrix.row(root)
            block = e0 * desired if desired != sp.zeros(1, 3) else null_section * e0.T
            assert block != sp.zeros(3)
            assert x.T * block == desired

    root_a = sp.Matrix([[1, 0, 0]])
    root_b = sp.Matrix([[0, 1, 0]])
    port_a = sp.Matrix([[0, 1, 1]])
    port_b = sp.Matrix([[1, 0, 1]])
    for matrix in common:
        left_roots = sp.Matrix.vstack(matrix, root_a)
        right_roots = sp.Matrix.vstack(matrix, root_b)
        left_map = sp.Matrix.vstack(left_roots, port_b)
        right_map = sp.Matrix.vstack(right_roots, port_a)
        assert left_roots.rank() == right_roots.rank() == 3
        assert left_map.rank() == right_map.rank() == 3
        assert profile(left_roots) == profile(right_roots) == 7

        block_a = alpha_a * root_a + zeta_a * port_a
        block_b = alpha_b * root_b + zeta_b * port_b
        assert block_a != sp.zeros(3) and block_b != sp.zeros(3)
        assert x.T * block_a == root_a
        assert z_a.T * block_a == port_a
        assert x.T * block_b == root_b
        assert z_b.T * block_b == port_b

    # The cofactor condition alone does not make the endpoint permanent
    # diagonal: word 000001 has coefficient 44 at (x_a,z_b).
    word = (0, 0, 0, 0, 0, 1)
    endpoint = [
        [
            sp.Matrix.vstack(common[mode], root_a, port_b)[row, word[mode]]
            for mode in range(6)
        ]
        for row in range(6)
    ]
    assert permanent(endpoint) == 44


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero local realization theorem",
        "rank_Q(A)=134",
        "C_I=0 with all fifteen blocker blocks nonzero",
        "not a global Krenn--Gu witness",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "SIX_BLOCKER_ORDER12_QUOTIENT_RANK_FRAME_CLASSIFICATION.md",
        "SIX_BLOCKER_ORDER12_ISOTROPIC_P6_CURVE.md",
    ):
        assert (ROOT / dependency).exists()

    common = common_rows()
    blocks = blocker_blocks()
    assert tuple(matrix.rank() for matrix in common) == (2, 2, 2, 3, 3, 3)
    assert len(blocks) == 15
    assert all(block != sp.zeros(3) for block in blocks.values())
    coefficients = tuple(
        cofactor_coefficient(common, blocks, word)
        for word in itertools.product(range(3), repeat=6)
    )
    assert coefficients == (sp.S.Zero,) * (3**6)
    rank = exact_off_diagonal_rank(common, tuple(blocks))
    assert rank == 134
    assert sum(entry != 0 for block in blocks.values() for entry in block) == 94
    local_realization(common)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "common_row_ranks": [2, 2, 2, 3, 3, 3],
                "blocker_blocks_nonzero": 15,
                "nonzero_block_entries": 94,
                "cofactor_coefficients_checked": 3**6,
                "cofactor_nonzero_coefficients": 0,
                "off_diagonal_system_shape": [726, 135],
                "off_diagonal_system_rank_Q": rank,
                "off_diagonal_kernel_dimension_Q": 1,
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
