#!/usr/bin/env python3
"""Independent audit of component 25's sparse-cover non-w branches."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
a_symbol, b_symbol, k_symbol = sp.symbols("a b k")
component = (
    (a_symbol * b_symbol + k_symbol**2) * (1 + a_symbol * b_symbol)
    - (a_symbol + b_symbol) ** 2
)
assert sp.factor(component.subs(k_symbol, 1)) == (
    (a_symbol - 1)
    * (a_symbol + 1)
    * (b_symbol - 1)
    * (b_symbol + 1)
)

phi_f = (
    a_symbol**3 * b_symbol
    + a_symbol**2 * b_symbol**4
    - a_symbol**2 * b_symbol**2
    + a_symbol**2
    - a_symbol * b_symbol**3
    - b_symbol**4
)
phi_n = (
    3 * a_symbol**3 * b_symbol**3
    - a_symbol**3 * b_symbol
    - a_symbol**2 * b_symbol**4
    + a_symbol**2 * b_symbol**2
    - a_symbol**2
    - a_symbol * b_symbol**3
    - a_symbol * b_symbol
    + b_symbol**4
)
f_coefficients = tuple(sp.Poly(phi_f, a_symbol).all_coeffs())
n_coefficients = tuple(sp.Poly(phi_n, a_symbol).all_coeffs())
sylvester_rows = []
for shift in range(3):
    sylvester_rows.append(
        [sp.S.Zero] * shift + list(f_coefficients) + [sp.S.Zero] * (2 - shift)
    )
for shift in range(3):
    sylvester_rows.append(
        [sp.S.Zero] * shift + list(n_coefficients) + [sp.S.Zero] * (2 - shift)
    )
sextic = 3 * b_symbol**6 - 3 * b_symbol**4 - 6 * b_symbol**2 - 2
sylvester_determinant = sp.factor(
    sp.Matrix(sylvester_rows).det(method="domain-ge")
)
assert sylvester_determinant == (
    b_symbol**9
    * (b_symbol - 1) ** 3
    * (b_symbol + 1) ** 3
    * sextic
)
assert sp.factor_list(sextic) == (1, [(sextic, 1)])

base = sp.QQ.alg_field_from_poly(sp.Poly(sextic, b_symbol), "b")
b = base.unit
zero = base.zero
one = base.one
half = base.convert(sp.Rational(1, 2))
a = b * (3 * b**4 - 5 * b**2 - 4) / 2
slope = (1 + b) / (1 - b)
k = a / b
q = a + b
r = 1 + a * b
p = q**2 / r
k2 = p - a * b
assert k**2 == k2
assert a**3 * b + a**2 * b**4 - a**2 * b**2 + a**2 - a * b**3 - b**4 == zero
assert (
    3 * a**3 * b**3
    - a**3 * b
    - a**2 * b**4
    + a**2 * b**2
    - a**2
    - a * b**3
    - a * b
    + b**4
) == zero

w = 3 * (33 * b**5 + 123 * b**4 - 56 * b**3 - 200 * b**2 - 26 * b - 126) / 128
z6 = -(969 * b**5 + 591 * b**4 - 1560 * b**3 - 936 * b**2 - 1002 * b - 646) / 128
branch_denominator = (slope - 1) * p - (slope + 1) * q
z3 = one / (2 * p * branch_denominator)
z5 = z6 - z3 * k
z1 = q * z6 - p * (slope - 1) * w - b * (k2 - a**2) * z3 / k
z7 = (p * z6 - k2 * q * (slope - 1) * w - a * z1) / (k2 - a**2)
z0 = (
    p**2 * z3
    - half / (slope - 1)
    - q**2 * (slope + 1) * k * w
) / (q * k)
extension = (
    z0,
    z1,
    (slope - 1) * w,
    z3,
    -(slope + 1) * w,
    z5,
    z6,
    z7,
)


def row_sum(*rows):
    return tuple(sum((row[column] for row in rows), zero) for column in range(4))


def row_scale(coefficient, row):
    return tuple(coefficient * value for value in row)


def permanent_dp(matrix):
    states = {0: one}
    for row in matrix:
        new_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                new_states[new_mask] = (
                    new_states.get(new_mask, zero) + coefficient * entry
                )
        states = new_states
    return states[(1 << len(matrix)) - 1]


cap_a = tuple(map(base.convert, (1, 1, 0, 0)))
cap_b = tuple(map(base.convert, (0, 0, 1, 1)))
cap_c = tuple(map(base.convert, (1, -1, 0, 0)))
cap_d = tuple(map(base.convert, (0, 0, 1, -1)))
alpha = (
    row_sum(row_scale(q, cap_a), row_scale(-p, cap_b)),
    row_sum(
        row_scale(q, row_sum(cap_a, row_scale(k, cap_d))),
        row_scale(-p, row_sum(cap_b, cap_c)),
    ),
    cap_c,
    cap_d,
)
beta = (
    cap_a,
    row_sum(cap_a, row_scale(k, cap_d)),
    row_sum(cap_a, row_scale(a, cap_b), row_scale(-k, cap_d)),
    row_sum(cap_a, row_scale(-b, cap_c), row_scale(b, cap_b)),
)


def project(row, extra, direction):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extra)
    return (row[0], row[1], slope * row[2] + row[3], extra)


alpha_01 = tuple(project(alpha[index], extension[index], "D01") for index in range(4))
beta_01 = tuple(project(beta[index], extension[index + 4], "D01") for index in range(4))


def coefficient_01(word):
    return permanent_dp(
        tuple(beta_01[index] if word[index] else alpha_01[index] for index in range(4))
    )


c0 = coefficient_01((0, 0, 0, 0))
c1 = coefficient_01((0, 1, 0, 0))
c2 = coefficient_01((0, 0, 1, 0))
c3 = coefficient_01((0, 0, 0, 1))
assert c0 != zero
assert coefficient_01((0, 1, 0, 1)) * c0 - c1 * c3 == zero
assert coefficient_01((0, 0, 1, 1)) * c0 - c2 * c3 == zero
assert coefficient_01((0, 1, 1, 1)) * c0**2 - c1 * c2 * c3 == zero

marking = tuple(
    -permanent_dp(
        tuple(beta_01[index] if index == mode else alpha_01[index] for index in range(4))
    )
    / c0
    for mode in range(4)
)
marked_01 = tuple(
    tuple(beta_01[index][column] + marking[index] * alpha_01[index][column] for column in range(4))
    for index in range(4)
)
binary = {
    word: permanent_dp(
        tuple(marked_01[index] if bit else alpha_01[index] for index, bit in enumerate(word))
    )
    / c0
    for word in itertools.product((0, 1), repeat=4)
}
assert binary[(0, 0, 0, 0)] == one
assert binary[(1, 1, 1, 1)] != zero
assert all(
    value == zero
    for word, value in binary.items()
    if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)

alpha_23 = tuple(project(alpha[index], extension[index], "D23") for index in range(4))
beta_23 = tuple(project(beta[index], extension[index + 4], "D23") for index in range(4))
sparse_pairs = (
    (beta_23[0], tuple(alpha_23[0][column] - q * beta_23[0][column] for column in range(4))),
    (beta_23[1], tuple(alpha_23[1][column] - q * beta_23[1][column] for column in range(4))),
    (alpha_23[2], beta_23[2]),
    (alpha_23[3], beta_23[3]),
)
expected_sparse_pairs = (
    ((one, one, zero, -(slope + 1) * w), (zero, zero, -p * (slope + 1), z0 - q * (-(slope + 1) * w))),
    ((one, one, k * (slope - 1), z5), (-p, p, -p * (slope + 1), z1 - q * z5)),
    ((one, -one, zero, (slope - 1) * w), (one, one, zero, z6)),
    ((zero, zero, slope - 1, z3), (1 - b, 1 + b, b * (slope + 1), z7)),
)
assert sparse_pairs == expected_sparse_pairs


def cofactor_row(rows):
    return tuple(
        permanent_dp(
            tuple(tuple(row[index] for index in range(4) if index != column) for row in rows)
        )
        for column in range(4)
    )


cube_rows = []
for word in ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1)):
    cube_rows.append(
        cofactor_row(
            tuple(sparse_pairs[mode][word[mode - 1]] for mode in (1, 2, 3))
        )
    )


def determinant_recursive(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    total = zero
    for column, entry in enumerate(matrix[0]):
        submatrix = tuple(
            tuple(row[index] for index in range(len(matrix)) if index != column)
            for row in matrix[1:]
        )
        term = entry * determinant_recursive(submatrix)
        total += -term if column % 2 else term
    return total


minor = determinant_recursive(tuple(cube_rows))
assert minor != zero
minor_coefficients = minor.to_list()
minor_polynomial = sum(
    sp.Rational(str(coefficient))
    * b_symbol ** (len(minor_coefficients) - index - 1)
    for index, coefficient in enumerate(minor_coefficients)
)
minor_norm = sp.factor(sp.resultant(sextic, minor_polynomial, b_symbol))
assert minor_norm != 0

print(
    json.dumps(
        {
            "status": "PASS",
            "k_equals_one_boundary_closed": True,
            "joint_branch_field": "Q[b]/(3*b^6-3*b^4-6*b^2-2)",
            "independent_permanent_algorithm": "subset dynamic programming",
            "independent_determinant_algorithm": "recursive cofactor expansion",
            "binary_mixed_coefficients_zero": 14,
            "opposite_diagonal_nonzero": True,
            "D23_rank_witness_mode": 0,
            "D23_rank_witness_rows": ["000", "001", "010", "011"],
            "D23_minor": str(sp.factor(minor_polynomial)),
            "D23_minor_norm": str(minor_norm),
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
