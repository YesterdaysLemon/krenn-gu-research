#!/usr/bin/env python3
"""Verify the fixed-core obstruction to a nonzero diagonal P6 pullback."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_CORE_NO_CONCISE_P6.md"


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


def kernel_generator() -> dict[tuple[int, int], sp.Matrix]:
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
    states: dict[int, sp.Expr] = {0: sp.S.One}
    for column in range(len(matrix)):
        next_states: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for row in range(len(matrix)):
                if mask & (1 << row):
                    continue
                new_mask = mask | (1 << row)
                next_states[new_mask] = next_states.get(new_mask, sp.S.Zero) + (
                    value * matrix[row][column]
                )
        states = next_states
    return sp.expand(states[(1 << len(matrix)) - 1])


def four_cofactor(common, word, left: int, right: int) -> sp.Expr:
    modes = [mode for mode in range(6) if mode not in (left, right)]
    matrix = [[common[mode][root, word[mode]] for mode in modes] for root in range(4)]
    return permanent(matrix)


def coefficient(common, blocks, word) -> sp.Expr:
    return sp.expand(
        sum(
            block[word[left], word[right]] * four_cofactor(common, word, left, right)
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
    basis: dict[int, dict[int, Fraction]] = {}
    row_count = 0
    for word in itertools.product(range(3), repeat=6):
        if len(set(word)) == 1:
            continue
        row_count += 1
        row: dict[int, Fraction] = {}
        for left, right in edges:
            value = int(four_cofactor(common, word, left, right))
            if value:
                row[indices[left, right, word[left], word[right]]] = Fraction(value)
        while row:
            pivot = min(row)
            if pivot not in basis:
                inverse = Fraction(1, 1) / row[pivot]
                basis[pivot] = {
                    column: value * inverse for column, value in row.items() if value
                }
                break
            factor = row[pivot]
            for column, value in basis[pivot].items():
                updated = row.get(column, Fraction(0)) - factor * value
                if updated:
                    row[column] = updated
                elif column in row:
                    del row[column]
    assert row_count == 726
    assert len(variables) == 135
    return len(basis)


def laplace_check(common) -> int:
    # Dense, deterministic appended rows make this an indexing-sensitive check
    # of the general two-row Laplace formula.  The proof itself is symbolic.
    a = tuple(sp.Matrix([[mode + 1, 2 * mode - 1, 3 - mode]]) for mode in range(6))
    b = tuple(sp.Matrix([[2 - mode, mode + 2, 2 * mode + 1]]) for mode in range(6))
    effective = {
        (left, right): a[left].T * b[right] + b[left].T * a[right]
        for left in range(6)
        for right in range(left + 1, 6)
    }
    checked = 0
    for word in itertools.product(range(3), repeat=6):
        direct_matrix = [
            [
                sp.Matrix.vstack(common[mode], a[mode], b[mode])[row, word[mode]]
                for mode in range(6)
            ]
            for row in range(6)
        ]
        assert permanent(direct_matrix) == coefficient(common, effective, word)
        checked += 1
    return checked


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "Exact characteristic-zero fixed-core obstruction",
        "rank_Q(Lambda_H^off)=134",
        "Pi_H(a,b)=kappa Lambda_H(W_*)=0",
        "all quotient-zero common-row cores: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem
    for dependency in (
        "SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md",
        "SIX_BLOCKER_ORDER12_QUOTIENT_RANK_FRAME_CLASSIFICATION.md",
    ):
        assert (ROOT / dependency).exists()

    common = common_rows()
    generator = kernel_generator()
    assert tuple(matrix.rank() for matrix in common) == (2, 2, 2, 3, 3, 3)
    assert len(generator) == 15
    assert any(entry != 0 for block in generator.values() for entry in block)

    rank = exact_off_diagonal_rank(common, tuple(generator))
    assert rank == 134
    coefficients = tuple(
        coefficient(common, generator, word)
        for word in itertools.product(range(3), repeat=6)
    )
    assert coefficients == (sp.S.Zero,) * (3**6)
    laplace_coefficients = laplace_check(common)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "common_row_ranks": [2, 2, 2, 3, 3, 3],
                "off_diagonal_map_shape": [726, 135],
                "off_diagonal_rank_Q": rank,
                "off_diagonal_kernel_dimension_Q": 1,
                "kernel_full_tensor_nonzero_coefficients": sum(
                    value != 0 for value in coefficients
                ),
                "laplace_rational_indexing_check_coefficients": laplace_coefficients,
                "nonzero_diagonal_p6_for_fixed_core": False,
                "other_common_row_cores_excluded": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
