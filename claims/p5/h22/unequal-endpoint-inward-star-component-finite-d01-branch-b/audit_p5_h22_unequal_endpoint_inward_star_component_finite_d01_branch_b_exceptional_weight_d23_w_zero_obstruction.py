#!/usr/bin/env python3
"""Independent audit of component 25's paired-D23 w=0 obstruction."""

from __future__ import annotations

import json
import time

import sympy as sp

started = time.perf_counter()
a, b, k, slope = sp.symbols("a b k lambda")
p_symbol, z3_symbol, v0_symbol = sp.symbols("P z3 v0")
z6_symbol, z7_symbol = sp.symbols("z6 z7")
plus = slope + 1
minus = slope - 1

pairs = (
    ((1, 1, 0, 0), (0, 0, -p_symbol * plus, v0_symbol)),
    ((1, -1, 0, 0), (1, 1, a * plus - k * minus, z6_symbol)),
    ((0, 0, minus, z3_symbol), (1 - b, 1 + b, b * plus, z7_symbol)),
)


def permanent_subset_dp(rows, columns):
    width = len(columns)
    values = {0: sp.Integer(1)}
    for row in rows:
        following = {}
        for mask, subtotal in values.items():
            for local_index, column in enumerate(columns):
                bit = 1 << local_index
                if not mask & bit:
                    following[mask | bit] = following.get(mask | bit, 0) + (
                        subtotal * row[column]
                    )
        values = following
    return sp.expand(values[(1 << width) - 1])


def cofactor_row(word):
    rows = tuple(pairs[index][bit] for index, bit in enumerate(word))
    return tuple(
        permanent_subset_dp(
            rows, tuple(index for index in range(4) if index != omitted)
        )
        for omitted in range(4)
    )


def determinant_recursive(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    total = 0
    for column, entry in enumerate(matrix[0]):
        submatrix = tuple(
            tuple(row[index] for index in range(len(row)) if index != column)
            for row in matrix[1:]
        )
        term = entry * determinant_recursive(submatrix)
        total += -term if column % 2 else term
    return sp.expand(total)


# A different rank-equivalent row set from the primary certificate.
audit_words = ((0, 1, 0), (1, 0, 0), (1, 0, 1), (1, 1, 0))
audit_matrix = tuple(cofactor_row(word) for word in audit_words)
audit_minor = sp.factor(determinant_recursive(audit_matrix))
x_minus_universal = p_symbol * plus * z3_symbol - minus * v0_symbol
x_plus_universal = p_symbol * plus * z3_symbol + minus * v0_symbol
assert sp.expand(
    audit_minor + 8 * b * x_minus_universal**2 * x_plus_universal
) == 0

# Recompute the nonzero norm by clearing denominators before factorization.
q = a + b
r = 1 + a * b
p = q**2 / r
k2 = p - a * b
d0 = a**2 * b**2 - a**2 - a * b - b**2
chart_factor = plus * r - minus * q
branch_denominator = minus * p - plus * q
z3 = 1 / (2 * p * branch_denominator)
y0 = (p**2 * z3 - sp.Rational(1, 2) / minus) / (q * k2)
x_minus = sp.cancel(p * plus * z3 - minus * k * y0)

norm_expression = sp.cancel(
    sp.expand(x_minus * x_minus.subs(k, -k)).subs(k**2, k2)
)
norm_numerator, norm_denominator = sp.together(norm_expression).as_numer_denom()
expected_numerator = (
    (a - 1)
    * (a + 1)
    * (b - 1)
    * (b + 1)
    * plus**2
    * r**2
)
expected_denominator = 4 * q**2 * d0 * chart_factor**2
assert sp.factor(norm_numerator * expected_denominator - expected_numerator * norm_denominator) == 0

# The audit minor has one additional factor b, already a standing unit.
print(
    json.dumps(
        {
            "status": "PASS",
            "method": "subset-DP permanents and recursive cofactor determinant",
            "marked_mode": 1,
            "independent_sparse_row_words": [
                "".join(map(str, word)) for word in audit_words
            ],
            "independent_minor": "-8*b*X_minus^2*X_plus",
            "norm_numerator": str(sp.factor(expected_numerator)),
            "norm_denominator": str(sp.factor(expected_denominator)),
            "rank_four": True,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
