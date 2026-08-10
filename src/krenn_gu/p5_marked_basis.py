"""Shared exact marked-basis linear algebra for P5 claim verifiers.

This module is infrastructure only for the four widely reused algebraic
operations below.  It does not contain the marked-basis-open theorem, its
reporting logic, or an exhaustiveness claim.
"""

from __future__ import annotations

import itertools

import sympy as sp


BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Return the exact permanent of a four-by-four row tuple."""
    return sp.factor(sum(
        sp.prod(rows[row][permutation[row]] for row in range(4))
        for permutation in PERMUTATIONS
    ))


def extension_coefficients(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: sp.Matrix,
) -> dict[tuple[int, ...], sp.Expr]:
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[mode][coordinate] for coordinate in common)
        + (extension[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][coordinate] for coordinate in common)
        + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        bits: permanent(tuple(
            beta_p[mode] if bits[mode] else alpha_p[mode]
            for mode in range(4)
        ))
        for bits in BITS4
    }


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    rows = []
    for bits in BITS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(permanent(tuple(
                basis if other == mode else selected[other]
                for other in range(4)
            )))
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def marked_extension(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    mode: int,
) -> sp.Matrix:
    common = tuple(
        coordinate for coordinate in range(4)
        if coordinate != distinguished
    )
    alpha_p = tuple(
        tuple(alpha[row][coordinate] for coordinate in common)
        + (extension[row],)
        for row in range(4)
    )
    beta_p = tuple(
        tuple(beta[row][coordinate] for coordinate in common)
        + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_p, beta_p)


def mixed_matrix(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    variables = sp.symbols("x0:4") + sp.symbols("y0:4")
    coefficients = extension_coefficients(
        distinguished,
        alpha,
        beta,
        sp.Matrix(variables),
    )
    mixed = sp.Matrix([
        [sp.diff(coefficients[bits], variable) for variable in variables]
        for bits in BITS4
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ])
    diagonals = tuple(sp.Matrix([[
        sp.diff(coefficients[bits], variable) for variable in variables
    ]]) for bits in ((0, 0, 0, 0), (1, 1, 1, 1)))
    return mixed, *diagonals


__all__ = ["marked_extension", "mixed_matrix", "one_marked_map", "permanent"]
