#!/usr/bin/env python3
"""No-import audit of one finite-weight component-21 kernel normal."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_ROWS = tuple(range(1, 15)) + tuple(range(17, 31))


def add(*rows):
    return tuple(sum(row[index] for row in rows) for index in range(4))


def scale(value, row):
    return tuple(value * entry for entry in row)


def finite_bases(p, q, kappa, ell):
    cap_a = (1, 1, 0, 0)
    cap_c = (1, -1, 0, 0)
    cap_b = (0, 0, 1, 1)
    cap_d = (0, 0, 1, -1)
    return (
        add(cap_a, scale(p, cap_b)),
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    ), (
        add(cap_c, scale(q, cap_b)),
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )


def permanent_dp(rows):
    states = {0: sp.S.One}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                next_states[new_mask] = next_states.get(new_mask, 0) + coefficient * entry
        states = next_states
    return states[(1 << len(rows)) - 1]


def project(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    return (row[0], row[1], slope * row[2] + row[3], extension)


def contraction_matrix(alpha, beta, extension, direction, slope):
    alpha_rows = tuple(
        project(alpha[index], extension[index], direction, slope)
        for index in range(4)
    )
    beta_rows = tuple(
        project(beta[index], extension[4 + index], direction, slope)
        for index in range(4)
    )
    output = []
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index]
            for index in range(4)
        )
        output.append(
            tuple(
                permanent_dp(
                    tuple(selected[index][:3] for index in range(4) if index != mode)
                )
                for mode in range(4)
            )
        )
    # The first four entries multiply alpha extensions and the second four
    # multiply beta extensions according to the selected binary word.
    rows = []
    for word, cofactors in zip(WORDS, output, strict=True):
        row = [sp.S.Zero] * 8
        for mode in range(4):
            row[(4 if word[mode] else 0) + mode] = cofactors[mode]
        rows.append(row)
    return sp.Matrix(rows)


def rank_rational(matrix):
    rows = [[sp.Rational(entry) for entry in matrix.row(index)] for index in range(matrix.rows)]
    rank = 0
    column = 0
    while rank < len(rows) and column < matrix.cols:
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column]), None)
        if pivot is None:
            column += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            factor = rows[index][column]
            rows[index] = [
                rows[index][other] - factor * rows[rank][other]
                for other in range(matrix.cols)
            ]
        rank += 1
        column += 1
    return rank


p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
extension = sp.symbols("z0:8")
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = contraction_matrix(alpha, beta, extension, "D01", slope).col_join(
    contraction_matrix(alpha, beta, extension, "D23", slope)
)
leading = sp.Matrix((-2, 0, 0, 0, -3, 0, 1, 0))
parameters = (p, q, kappa, ell, slope)
centre = {p: 2, q: 3, kappa: 5, ell: 7, slope: 1}
specialized = matrix.subs(centre)
assert specialized * leading == sp.zeros(32, 1)
parameter_columns = sp.Matrix.hstack(
    *(sp.diff(matrix * leading, parameter).subs(centre) for parameter in parameters)
)
normal = specialized.row_join(parameter_columns)
mixed = normal.extract(MIXED_ROWS, range(13))
assert rank_rational(specialized) == 7
assert rank_rational(mixed) == 7
for diagonal in (0, 15, 16):
    assert rank_rational(mixed.col_join(normal.extract((diagonal,), range(13)))) == 7
assert rank_rational(mixed.col_join(normal.extract((31,), range(13)))) == 8

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; subset-DP permanents; rational Gaussian rank",
            "component": 21,
            "point": [2, 3, 5, 7, 1],
            "leading_extension_kernel": [-2, 0, 0, 0, -3, 0, 1, 0],
            "mixed_rank": 7,
            "diagonal_rows_in_mixed_span": [0, 15, 16],
            "independent_diagonal_row": 31,
            "finite_weight_locus_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
