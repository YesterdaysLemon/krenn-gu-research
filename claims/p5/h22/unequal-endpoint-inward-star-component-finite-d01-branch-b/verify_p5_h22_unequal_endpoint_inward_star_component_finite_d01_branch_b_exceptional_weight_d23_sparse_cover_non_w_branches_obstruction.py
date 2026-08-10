#!/usr/bin/env python3
"""Verify obstruction of component 25's sparse-cover non-w branches."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
a_symbol, b_symbol, lambda_symbol, k_symbol = sp.symbols("a b lambda k")
component_polynomial = (
    (a_symbol * b_symbol + k_symbol**2) * (1 + a_symbol * b_symbol)
    - (a_symbol + b_symbol) ** 2
)
assert sp.factor(component_polynomial.subs(k_symbol, 1)) == (
    (a_symbol - 1)
    * (a_symbol + 1)
    * (b_symbol - 1)
    * (b_symbol + 1)
)

a2_symbolic = (a_symbol + 1) * (b_symbol - 1) * (
    3 * a_symbol**2 * b_symbol**2
    + a_symbol**2 * b_symbol
    - a_symbol**2
    - a_symbol * b_symbol**3
    - 2 * a_symbol * b_symbol**2
    - a_symbol * b_symbol
    + b_symbol**3
)
a1_symbolic = -2 * (
    3 * a_symbol**3 * b_symbol**3
    - 2 * a_symbol**3 * b_symbol
    - a_symbol**2 * b_symbol**4
    + a_symbol**2 * b_symbol**2
    - a_symbol**2
    - a_symbol * b_symbol
    + b_symbol**4
)
a0_symbolic = (a_symbol - 1) * (b_symbol + 1) * (
    3 * a_symbol**2 * b_symbol**2
    - a_symbol**2 * b_symbol
    - a_symbol**2
    - a_symbol * b_symbol**3
    + 2 * a_symbol * b_symbol**2
    - a_symbol * b_symbol
    - b_symbol**3
)
n_symbolic = (
    a2_symbolic * lambda_symbol**2
    + a1_symbolic * lambda_symbol
    + a0_symbolic
)
lambda_joint = (1 + b_symbol) / (1 - b_symbol)
k_joint = a_symbol / b_symbol
component_joint = (
    a_symbol**3 * b_symbol
    + a_symbol**2 * b_symbol**4
    - a_symbol**2 * b_symbol**2
    + a_symbol**2
    - a_symbol * b_symbol**3
    - b_symbol**4
)
exceptional_joint = (
    3 * a_symbol**3 * b_symbol**3
    - a_symbol**3 * b_symbol
    - a_symbol**2 * b_symbol**4
    + a_symbol**2 * b_symbol**2
    - a_symbol**2
    - a_symbol * b_symbol**3
    - a_symbol * b_symbol
    + b_symbol**4
)
assert sp.factor(
    sp.together(component_polynomial.subs(k_symbol, k_joint))
    - component_joint / b_symbol**2
) == 0
assert sp.factor(
    sp.together(n_symbolic.subs(lambda_symbol, lambda_joint))
    - 4 * (b_symbol + 1) * exceptional_joint / (b_symbol - 1)
) == 0

w_polynomial = 3 * b_symbol**6 - 3 * b_symbol**4 - 6 * b_symbol**2 - 2
assert sp.factor_list(w_polynomial) == (1, [(w_polynomial, 1)])
subresultants = sp.subresultants(component_joint, exceptional_joint, a_symbol)
linear_subresultant_core = (
    3 * a_symbol * b_symbol**8
    + 12 * a_symbol * b_symbol**6
    - 3 * a_symbol * b_symbol**4
    - 2 * a_symbol * b_symbol**2
    + 2 * a_symbol
    + 9 * b_symbol**7
    + 3 * b_symbol**5
)
assert sp.factor(subresultants[-2]) == (
    b_symbol**4
    * (b_symbol - 1)
    * (b_symbol + 1)
    * linear_subresultant_core
)
assert sp.factor(subresultants[-1]) == (
    b_symbol**9
    * (b_symbol - 1) ** 3
    * (b_symbol + 1) ** 3
    * w_polynomial
)
linear_coefficient = sp.diff(linear_subresultant_core, a_symbol)
assert sp.gcd(linear_coefficient, w_polynomial) == 1
a_parameterization = b_symbol * (3 * b_symbol**4 - 5 * b_symbol**2 - 4) / 2
assert sp.rem(
    sp.together(linear_subresultant_core.subs(a_symbol, a_parameterization)),
    w_polynomial,
    domain=sp.QQ,
) == 0

base = sp.QQ.alg_field_from_poly(sp.Poly(w_polynomial, b_symbol), "b")
b = base.unit
one = base.one
zero = base.zero
a = b * (3 * b**4 - 5 * b**2 - 4) / 2
slope = (1 + b) / (1 - b)
k = a / b
s = one
e = a
j = b
q = e + j
r = 1 + e * j
p = q**2 / r
k2 = p - e * j
assert k**2 == k2
assert (1 - b) * slope - (1 + b) == zero
assert a * (slope + 1) - k * (slope - 1) == zero

a2 = (a + 1) * (b - 1) * (
    3 * a**2 * b**2
    + a**2 * b
    - a**2
    - a * b**3
    - 2 * a * b**2
    - a * b
    + b**3
)
a1 = -2 * (
    3 * a**3 * b**3
    - 2 * a**3 * b
    - a**2 * b**4
    + a**2 * b**2
    - a**2
    - a * b
    + b**4
)
a0 = (a - 1) * (b + 1) * (
    3 * a**2 * b**2
    - a**2 * b
    - a**2
    - a * b**3
    + 2 * a * b**2
    - a * b
    - b**3
)
assert a2 * slope**2 + a1 * slope + a0 == zero

standing = {
    "a": a,
    "b": b,
    "a-b": a - b,
    "a+b": a + b,
    "a-1": a - 1,
    "a+1": a + 1,
    "b-1": b - 1,
    "b+1": b + 1,
    "R": r,
    "P": p,
    "k": k,
    "a2-k2": a**2 - k2,
    "lambda": slope,
    "lambda-1": slope - 1,
    "lambda+1": slope + 1,
    "A0": a0,
    "A2": a2,
}
assert all(value != zero for value in standing.values())


def row_add(*rows):
    return tuple(sum((row[column] for row in rows), zero) for column in range(4))


def row_scale(coefficient, row):
    return tuple(coefficient * value for value in row)


cap_a = tuple(map(base.convert, (1, 1, 0, 0)))
cap_b = tuple(map(base.convert, (0, 0, 1, 1)))
cap_c = tuple(map(base.convert, (1, -1, 0, 0)))
cap_d = tuple(map(base.convert, (0, 0, 1, -1)))
alpha = (
    row_add(row_scale(q, cap_a), row_scale(-p, cap_b)),
    row_add(
        row_scale(q, row_add(cap_a, row_scale(k, cap_d))),
        row_scale(-p, row_add(cap_b, cap_c)),
    ),
    cap_c,
    cap_d,
)
beta = (
    cap_a,
    row_add(cap_a, row_scale(k, cap_d)),
    row_add(cap_a, row_scale(e, cap_b), row_scale(-k, cap_d)),
    row_add(cap_a, row_scale(-j, cap_c), row_scale(j, cap_b)),
)

branch_denominator = (slope - 1) * p - (slope + 1) * q
z3 = one / (2 * p * branch_denominator)
half = base.convert(sp.Rational(1, 2))


def extensions(w, z6):
    z5 = z6 - z3 * k
    z1 = q * z6 - p * (slope - 1) * w - j * (k2 - e**2) * z3 / k
    z7 = (p * z6 - k2 * q * (slope - 1) * w - e * z1) / (k2 - e**2)
    z0 = (p**2 * z3 - half / (slope - 1) - q**2 * (slope + 1) * k * w) / (q * k)
    return (
        z0,
        z1,
        (slope - 1) * w,
        z3,
        -(slope + 1) * w,
        z5,
        z6,
        z7,
    )


def projected(w, z6, direction):
    ext = extensions(w, z6)

    def project(row, extra):
        if direction == "D01":
            return (slope * row[0] + row[1], row[2], row[3], extra)
        return (row[0], row[1], slope * row[2] + row[3], extra)

    return (
        tuple(project(alpha[index], ext[index]) for index in range(4)),
        tuple(project(beta[index], ext[index + 4]) for index in range(4)),
    )


def permanent(rows):
    total = zero
    for permutation in itertools.permutations(range(4)):
        term = one
        for index in range(4):
            term *= rows[index][permutation[index]]
        total += term
    return total


def residuals(w, z6):
    alpha_rows, beta_rows = projected(w, z6, "D01")

    def coefficient(word):
        return permanent(
            tuple(
                beta_rows[index] if word[index] else alpha_rows[index]
                for index in range(4)
            )
        )

    c0 = coefficient((0, 0, 0, 0))
    c1 = coefficient((0, 1, 0, 0))
    c2 = coefficient((0, 0, 1, 0))
    c3 = coefficient((0, 0, 0, 1))
    c13 = coefficient((0, 1, 0, 1))
    c23 = coefficient((0, 0, 1, 1))
    c123 = coefficient((0, 1, 1, 1))
    return (
        c13 * c0 - c1 * c3,
        c23 * c0 - c2 * c3,
        c123 * c0**2 - c1 * c2 * c3,
    )


origin = residuals(zero, zero)
unit_w = residuals(one, zero)
unit_z6 = residuals(zero, one)
m11 = unit_w[0] - origin[0]
m12 = unit_z6[0] - origin[0]
m21 = unit_w[1] - origin[1]
m22 = unit_z6[1] - origin[1]
determinant = m11 * m22 - m12 * m21
assert determinant != zero
w = (-origin[0] * m22 + m12 * origin[1]) / determinant
z6 = (-m11 * origin[1] + origin[0] * m21) / determinant
assert residuals(w, z6) == (zero, zero, zero)

alpha_01, beta_01 = projected(w, z6, "D01")
c0_binary = permanent(alpha_01)
assert c0_binary != zero
marking = tuple(
    -permanent(
        tuple(beta_01[index] if index == mode else alpha_01[index] for index in range(4))
    )
    / c0_binary
    for mode in range(4)
)
marked_01 = tuple(
    tuple(beta_01[index][column] + marking[index] * alpha_01[index][column] for column in range(4))
    for index in range(4)
)
binary_coefficients = {
    word: permanent(
        tuple(marked_01[index] if bit else alpha_01[index] for index, bit in enumerate(word))
    )
    / c0_binary
    for word in itertools.product((0, 1), repeat=4)
}
assert binary_coefficients[(0, 0, 0, 0)] == one
assert all(
    value == zero
    for word, value in binary_coefficients.items()
    if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
opposite_diagonal = binary_coefficients[(1, 1, 1, 1)]
assert opposite_diagonal != zero

alpha_23, beta_23 = projected(w, z6, "D23")
marked_23 = tuple(
    tuple(beta_23[index][column] + marking[index] * alpha_23[index][column] for column in range(4))
    for index in range(4)
)
words = tuple(itertools.product((0, 1), repeat=3))


def one_marked_matrix(mode):
    matrix = []
    for word in words:
        selected = []
        cursor = 0
        for index in range(4):
            if index == mode:
                selected.append(None)
            else:
                selected.append(marked_23[index] if word[cursor] else alpha_23[index])
                cursor += 1
        matrix.append(
            [
                permanent(
                    tuple(
                        tuple(base.convert(int(basis_index == column)) for basis_index in range(4))
                        if index == mode
                        else selected[index]
                        for index in range(4)
                    )
                )
                for column in range(4)
            ]
        )
    return matrix


def determinant4(matrix):
    total = zero
    for permutation in itertools.permutations(range(4)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(4)
            for right in range(left + 1, 4)
        )
        term = one
        for row in range(4):
            term *= matrix[row][permutation[row]]
        total += -term if inversions % 2 else term
    return total


rank_witness = None
for mode in range(4):
    matrix = one_marked_matrix(mode)
    for row_indices in itertools.combinations(range(8), 4):
        minor = determinant4([[matrix[row][column] for column in range(4)] for row in row_indices])
        if minor != zero:
            rank_witness = (mode, row_indices, minor)
            break
    if rank_witness is not None:
        break
assert rank_witness is not None
mode, row_indices, minor = rank_witness
def element_expression(value):
    coefficients = value.to_list()
    return sp.factor(
        sum(
            sp.Rational(str(coefficient))
            * b_symbol ** (len(coefficients) - index - 1)
            for index, coefficient in enumerate(coefficients)
        )
    )


w_expression = element_expression(w)
z6_expression = element_expression(z6)
minor_expression = element_expression(minor)
minor_numerator = sp.together(minor_expression).as_numer_denom()[0]
minor_norm = sp.factor(sp.resultant(w_polynomial, minor_numerator, b_symbol))
assert minor_norm != 0

print(
    json.dumps(
        {
            "status": "PASS",
            "k_equals_one_component_factorization": "(a-1)(a+1)(b-1)(b+1)",
            "branch": ["Tbar=0", "A=0", "N=0", "component equation"],
            "primitive_joint_resultant": str(sp.factor(subresultants[-1])),
            "base_field": "Q[b]/(3*b^6-3*b^4-6*b^2-2)",
            "a": "b*(3*b^4-5*b^2-4)/2",
            "lambda": "(1+b)/(1-b)",
            "k": "a/b",
            "w": str(w_expression),
            "z6": str(z6_expression),
            "opposite_diagonal_nonzero": True,
            "D23_rank_witness_mode": mode,
            "D23_rank_witness_rows": ["".join(map(str, words[index])) for index in row_indices],
            "D23_minor": str(minor_expression),
            "D23_minor_norm": str(minor_norm),
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
