#!/usr/bin/env python3
"""No-import audit of component 25's exceptional linear-solve divisors."""

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

# Reconstruct N and its retained e,j,s,lambda intersections over Q.
E, J, S, slope = sp.symbols("E J S lambda")
a2_global = (
    (E * S + 1)
    * (J * S - 1)
    * (
        3 * E**2 * J**2 * S**2
        + E**2 * J * S
        - E**2
        - E * J**3 * S**2
        - 2 * E * J**2 * S
        - E * J
        + J**3 * S
    )
)
a1_global = -2 * (
    3 * E**3 * J**3 * S**4
    - 2 * E**3 * J * S**2
    - E**2 * J**4 * S**4
    + E**2 * J**2 * S**2
    - E**2
    - E * J
    + J**4 * S**2
)
c0_global = (
    3 * E**2 * J**2 * S**2
    - E**2 * J * S
    - E**2
    - E * J**3 * S**2
    + 2 * E * J**2 * S
    - E * J
    - J**3 * S
)
a0_global = (E * S - 1) * (J * S + 1) * c0_global
n_global = a2_global * slope**2 + a1_global * slope + a0_global
q_global = E + J
r_global = 1 + E * J * S**2
h_global = (slope + 1) * r_global - (slope - 1) * S * q_global
t_global = (J * S - 1) * slope - (J * S + 1)

assert sp.expand(n_global.subs(slope, 0) - a0_global) == 0
assert (
    sp.expand(n_global.subs(E, 0) - J**3 * S * (slope - 1) * t_global.subs(E, 0)) == 0
)
assert (
    sp.expand(
        n_global.subs(J, 0) - E**2 * (slope + 1) * ((E * S + 1) * slope + (1 - E * S))
    )
    == 0
)
assert sp.expand(n_global.subs(S, 0) - E * (E + J) * (slope + 1) ** 2) == 0

# At lambda=0, the already-certified S13/S23 consistency condition is
# (ES-1)(S(E-J)+2)=0 after units are removed.  On the C0 factor, its second
# branch gives the exact quadratic u-family.
consistency_factor = (E * S - 1) * (S * (E - J) + 2)
assert consistency_factor != 0
c0_on_second_branch = sp.factor(c0_global.subs(J, E + 2 / S))
assert c0_on_second_branch == 2 * (E * S + 1) ** 2 * (E**2 * S**2 + E * S - 4) / S**2

# The other consistency branch ES=1 is exactly e^2-k^2=0 on the component.
k2_component = q_global**2 / r_global - E * J
assert sp.factor((E**2 - k2_component).subs(E, 1 / S)) == 0
assert sp.factor((E**2 - k2_component).subs(J, 0)) == 0

base, s, t0, t1 = sp.polys.fields.field("s,t0,t1", sp.QQ)
l_zero = (base.zero, base.zero)
l_one = (base.one, base.zero)
u = (base.zero, base.one)


def l_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def l_neg(value):
    return (-value[0], -value[1])


def l_sub(left, right):
    return (left[0] - right[0], left[1] - right[1])


def l_mul(left, right):
    # u^2=4-u.
    return (
        left[0] * right[0] + 4 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0] - left[1] * right[1],
    )


def l_inv(value):
    norm = value[0] ** 2 - value[0] * value[1] - 4 * value[1] ** 2
    return ((value[0] - value[1]) / norm, -value[1] / norm)


def l_div(left, right):
    return l_mul(left, l_inv(right))


def l_scalar(value):
    if hasattr(value, "field"):
        return (value, base.zero)
    return (base.from_expr(sp.sympify(value)), base.zero)


k2 = l_mul(l_scalar(-(1 / s**2)), u)
zero = (l_zero, l_zero)
one = (l_one, l_zero)
k = (l_zero, l_one)


def add(left, right):
    return (l_add(left[0], right[0]), l_add(left[1], right[1]))


def neg(value):
    return (l_neg(value[0]), l_neg(value[1]))


def sub(left, right):
    return (l_sub(left[0], right[0]), l_sub(left[1], right[1]))


def mul(left, right):
    return (
        l_add(l_mul(left[0], right[0]), l_mul(k2, l_mul(left[1], right[1]))),
        l_add(l_mul(left[0], right[1]), l_mul(left[1], right[0])),
    )


def inv(value):
    norm = l_sub(l_mul(value[0], value[0]), l_mul(k2, l_mul(value[1], value[1])))
    inverse_norm = l_inv(norm)
    return (l_mul(value[0], inverse_norm), l_neg(l_mul(value[1], inverse_norm)))


def div(left, right):
    return mul(left, inv(right))


def scalar(value):
    return (l_scalar(value), l_zero)


def l_value(value):
    return (value, l_zero)


def e_scale(coefficient, value):
    return (l_mul(coefficient, value[0]), l_mul(coefficient, value[1]))


def l_sum(*values):
    total = l_zero
    for value in values:
        total = l_add(total, value)
    return total


def row_sum(*rows):
    return tuple(
        sum_entries(tuple(row[coordinate] for row in rows)) for coordinate in range(4)
    )


def sum_entries(entries):
    total = zero
    for entry in entries:
        total = add(total, entry)
    return total


def row_scale(coefficient, row):
    return tuple(e_scale(coefficient, value) for value in row)


def row_multiply(value, row):
    return tuple(mul(value, entry) for entry in row)


e = l_mul(l_scalar(1 / s), u)
j = l_mul(l_scalar(1 / s), l_add(u, l_scalar(2)))
q = l_mul(l_scalar(2 / s), l_add(u, l_one))
r = l_add(l_scalar(5), u)
p = l_scalar(4 / s**2)
assert l_mul(p, r) == l_mul(q, q)
assert l_sub(k2, l_mul(e, e)) == l_scalar(-4 / s**2)

cap_a = tuple(map(scalar, (1, 1, 0, 0)))
cap_b = tuple(map(scalar, (0, 0, 1, 1)))
cap_c = tuple(map(scalar, (1, -1, 0, 0)))
cap_d = tuple(map(scalar, (0, 0, 1, -1)))
alpha = (
    row_sum(row_scale(q, cap_a), row_scale(l_neg(p), cap_b)),
    row_sum(
        row_scale(q, row_sum(cap_a, row_multiply(k, cap_d))),
        row_scale(l_neg(p), row_sum(cap_b, row_scale(l_scalar(s), cap_c))),
    ),
    cap_c,
    cap_d,
)
beta = (
    cap_a,
    row_sum(cap_a, row_multiply(k, cap_d)),
    row_sum(
        cap_a,
        row_scale(e, cap_b),
        row_scale(l_scalar(-1), row_multiply(k, cap_d)),
    ),
    row_sum(
        cap_a,
        row_scale(l_neg(l_mul(l_scalar(s), j)), cap_c),
        row_scale(j, cap_b),
    ),
)

branch_denominator = l_neg(l_add(l_mul(l_scalar(s), p), q))
z3 = l_div(l_scalar(s), l_mul(l_scalar(2), l_mul(p, branch_denominator)))
sum_solution = (
    l_zero,
    (
        base.from_expr(sp.Rational(1, 32)) * s**4,
        base.from_expr(sp.Rational(-1, 32)) * s**4,
    ),
)
w = ((t0, base.zero), (t1, base.zero))
z6 = sub(sum_solution, w)


def extension():
    inverse_k = (l_zero, l_inv(k2))
    z5 = add(z6, e_scale(l_neg(z3), k))
    z1 = add(
        add(e_scale(q, z6), e_scale(l_mul(p, l_scalar(s)), w)),
        e_scale(l_mul(l_neg(j), l_mul(l_sub(k2, l_mul(e, e)), z3)), inverse_k),
    )
    z7 = e_scale(
        l_inv(l_sub(k2, l_mul(e, e))),
        add(
            add(
                e_scale(p, z6),
                e_scale(l_mul(l_mul(k2, q), l_scalar(s)), w),
            ),
            e_scale(l_neg(e), z1),
        ),
    )
    z0 = mul(
        add(
            l_value(l_add(l_mul(l_mul(p, p), z3), l_scalar(sp.Rational(1, 2)))),
            e_scale(l_neg(l_mul(q, q)), mul(k, w)),
        ),
        e_scale(l_inv(q), inverse_k),
    )
    return (z0, z1, neg(w), l_value(z3), neg(w), z5, z6, z7)


def project(row, extra, direction):
    if direction == "D01":
        return (row[1], row[2], row[3], extra)
    return (row[0], row[1], row[3], extra)


def projected(direction):
    ext = extension()
    return (
        tuple(project(alpha[index], ext[index], direction) for index in range(4)),
        tuple(project(beta[index], ext[index + 4], direction) for index in range(4)),
    )


def permanent(rows):
    states = {0: one}
    for row in rows:
        next_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                term = mul(coefficient, entry)
                next_states[new_mask] = add(next_states.get(new_mask, zero), term)
        states = next_states
    return states[15]


alpha_01, beta_01 = projected("D01")
c0 = permanent(alpha_01)
marking = tuple(
    div(
        neg(
            permanent(
                tuple(
                    beta_01[index] if index == mode else alpha_01[index]
                    for index in range(4)
                )
            )
        ),
        c0,
    )
    for mode in range(4)
)
marked_01 = tuple(
    tuple(
        add(beta_01[index][column], mul(marking[index], alpha_01[index][column]))
        for column in range(4)
    )
    for index in range(4)
)
coefficients = {
    word: permanent(
        tuple(
            marked_01[index] if bit else alpha_01[index]
            for index, bit in enumerate(word)
        )
    )
    for word in itertools.product((0, 1), repeat=4)
}
assert all(
    value == zero
    for word, value in coefficients.items()
    if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
assert coefficients[(0, 0, 0, 0)] == one
expected_opposite_diagonal = (
    (-(16 * t0) / s**2, base.zero),
    ((s**4 - 64 * t1) / (4 * s**2), -(s**2) / 4),
)
assert coefficients[(1, 1, 1, 1)] == expected_opposite_diagonal

alpha_23, beta_23 = projected("D23")
marked_23 = tuple(
    tuple(
        add(beta_23[index][column], mul(marking[index], alpha_23[index][column]))
        for column in range(4)
    )
    for index in range(4)
)
bits = tuple(itertools.product((0, 1), repeat=3))


def one_marked_matrix(mode):
    matrix = []
    for row_index in range(4):
        selected = []
        cursor = 0
        for index in range(4):
            if index == mode:
                selected.append(None)
            else:
                selected.append(
                    marked_23[index] if bits[row_index][cursor] else alpha_23[index]
                )
                cursor += 1
        row = []
        for coordinate in range(4):
            basis = tuple(scalar(int(index == coordinate)) for index in range(4))
            row.append(
                permanent(
                    tuple(
                        basis if index == mode else selected[index]
                        for index in range(4)
                    )
                )
            )
        matrix.append(row)
    return matrix


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    total = zero
    for column, entry in enumerate(matrix[0]):
        submatrix = tuple(
            tuple(row[index] for index in range(len(row)) if index != column)
            for row in matrix[1:]
        )
        term = mul(entry, determinant(submatrix))
        total = add(total, neg(term) if column % 2 else term)
    return total


minor = determinant(one_marked_matrix(0))
x, y = sp.symbols("x y")
quadrics = (
    320 * x**2 - 7424 * x * y + 196 * x + 7936 * y**2 - 312 * y + 3,
    1984 * x**2 - 3840 * x * y + 140 * x + 2304 * y**2 - 232 * y + 3,
    1984 * x**2 - 1280 * x * y + 308 * x + 7424 * y**2 - 392 * y + 5,
    1856 * x**2 - 7936 * x * y + 156 * x + 3840 * y**2 - 280 * y + 3,
)
scaled_x = t0 / s**3
scaled_y = t1 / s**4


def evaluate_scaled(poly):
    total = base.zero
    for (x_degree, y_degree), coefficient in sp.Poly(poly, x, y).terms():
        total += base.from_expr(coefficient) * scaled_x**x_degree * scaled_y**y_degree
    return total


scaled_quadrics = tuple(evaluate_scaled(poly) for poly in quadrics)
expected_minor = (
    (
        s**4 * scaled_quadrics[0] / 2,
        -(s**4) * scaled_quadrics[1] / 2,
    ),
    (
        -(s**5) * scaled_quadrics[2] / 4,
        s**5 * scaled_quadrics[3] / 4,
    ),
)
assert minor == expected_minor
resultants = tuple(
    sp.Poly(sp.resultant(quadrics[0], quadrics[index], x), y, domain=sp.QQ)
    for index in (1, 2, 3)
)
resultant_gcd = sp.gcd(sp.gcd(resultants[0], resultants[1]), resultants[2])
assert resultant_gcd.degree() == 0


def verify_e_zero_s_zero_split_sheet(sign):
    j_symbol, lambda_symbol, free_w = sp.symbols("j lambda w")
    k_symbol = sign * j_symbol
    z6_value = (
        -sign / (2 * j_symbol**3 * (lambda_symbol - 1)) - (lambda_symbol + 1) * free_w
    )
    cap_a_local = (1, 1, 0, 0)
    cap_b_local = (0, 0, 1, 1)
    cap_c_local = (1, -1, 0, 0)
    cap_d_local = (0, 0, 1, -1)

    def row_add_local(*rows):
        return tuple(sum(row[column] for row in rows) for column in range(4))

    def row_scale_local(coefficient, row):
        return tuple(coefficient * value for value in row)

    alpha_local = (
        row_add_local(
            row_scale_local(j_symbol, cap_a_local),
            row_scale_local(-(j_symbol**2), cap_b_local),
        ),
        row_add_local(
            row_scale_local(
                j_symbol,
                row_add_local(cap_a_local, row_scale_local(k_symbol, cap_d_local)),
            ),
            row_scale_local(-(j_symbol**2), cap_b_local),
        ),
        cap_c_local,
        cap_d_local,
    )
    beta_local = (
        cap_a_local,
        row_add_local(cap_a_local, row_scale_local(k_symbol, cap_d_local)),
        row_add_local(cap_a_local, row_scale_local(-k_symbol, cap_d_local)),
        row_add_local(cap_a_local, row_scale_local(j_symbol, cap_b_local)),
    )
    extension_local = (
        -1 / (2 * (lambda_symbol - 1) * j_symbol * k_symbol)
        - j_symbol * (lambda_symbol + 1) * free_w,
        j_symbol * z6_value,
        (lambda_symbol - 1) * free_w,
        0,
        -(lambda_symbol + 1) * free_w,
        z6_value,
        z6_value,
        z6_value,
    )

    def project_local(row, extra, direction):
        if direction == "D01":
            return (
                lambda_symbol * row[0] + row[1],
                row[2],
                row[3],
                extra,
            )
        return (
            row[0],
            row[1],
            lambda_symbol * row[2] + row[3],
            extra,
        )

    def permanent_local(rows):
        states = {0: sp.Integer(1)}
        for row in rows:
            next_states = {}
            for mask, coefficient in states.items():
                for column, entry in enumerate(row):
                    bit = 1 << column
                    if mask & bit:
                        continue
                    new_mask = mask | bit
                    next_states[new_mask] = (
                        next_states.get(new_mask, 0) + coefficient * entry
                    )
            states = next_states
        return sp.factor(states[15])

    alpha_01_local = tuple(
        project_local(alpha_local[index], extension_local[index], "D01")
        for index in range(4)
    )
    beta_01_local = tuple(
        project_local(beta_local[index], extension_local[index + 4], "D01")
        for index in range(4)
    )
    marking_local = tuple(
        sp.factor(
            -permanent_local(
                tuple(
                    beta_01_local[index] if index == mode else alpha_01_local[index]
                    for index in range(4)
                )
            )
        )
        for mode in range(4)
    )
    marked_01_local = tuple(
        tuple(
            sp.factor(
                beta_01_local[index][column]
                + marking_local[index] * alpha_01_local[index][column]
            )
            for column in range(4)
        )
        for index in range(4)
    )
    binary_local = {
        word: permanent_local(
            tuple(
                marked_01_local[index] if bit else alpha_01_local[index]
                for index, bit in enumerate(word)
            )
        )
        for word in itertools.product((0, 1), repeat=4)
    }
    assert binary_local[(0, 0, 0, 0)] == 1
    assert all(
        value == 0
        for word, value in binary_local.items()
        if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )

    alpha_23_local = tuple(
        project_local(alpha_local[index], extension_local[index], "D23")
        for index in range(4)
    )
    beta_23_local = tuple(
        project_local(beta_local[index], extension_local[index + 4], "D23")
        for index in range(4)
    )
    marked_23_local = tuple(
        tuple(
            sp.factor(
                beta_23_local[index][column]
                + marking_local[index] * alpha_23_local[index][column]
            )
            for column in range(4)
        )
        for index in range(4)
    )
    ternary_words = tuple(itertools.product((0, 1), repeat=3))
    mode = 1
    matrix = []
    for word in ternary_words:
        selected = []
        cursor = 0
        for index in range(4):
            if index == mode:
                selected.append(None)
            else:
                selected.append(
                    marked_23_local[index] if word[cursor] else alpha_23_local[index]
                )
                cursor += 1
        row = []
        for column in range(4):
            basis = tuple(int(index == column) for index in range(4))
            row.append(
                permanent_local(
                    tuple(
                        basis if index == mode else selected[index]
                        for index in range(4)
                    )
                )
            )
        matrix.append(row)
    matrix = sp.Matrix(matrix)
    first_minor = sp.factor(matrix.extract((0, 1, 2, 4), range(4)).det())
    second_minor = sp.factor(matrix.extract((0, 2, 3, 6), range(4)).det())
    expected_first = sign * 4 * free_w**2 * (lambda_symbol - 1) ** 4
    expected_second = (
        sign
        * 3
        * (2 * j_symbol**3 * (lambda_symbol**2 - 1) * free_w + sign) ** 2
        / j_symbol**6
    )
    assert sp.factor(first_minor - expected_first) == 0
    assert sp.factor(second_minor - expected_second) == 0
    assert binary_local[(1, 1, 1, 1)] != 0
    return tuple(map(str, marking_local))


split_sheet_markings = {
    sign: verify_e_zero_s_zero_split_sheet(sign) for sign in (1, -1)
}

print(
    json.dumps(
        {
            "status": "PASS",
            "audit_independence": "no project imports; subset-DP permanents; recursive determinant; resultant gcd",
            "closed_intersections": ["e=0", "j=0", "s=0", "lambda=0"],
            "lambda_zero_standing_family": "es=u, js=u+2, u^2+u-4=0",
            "lambda_zero_binary_free_parameters": ["t0", "t1"],
            "lambda_zero_mode_zero_minor_coefficient_ideal": "unit",
            "e_zero_s_zero_component_sheets": ["k=j", "k=-j"],
            "e_zero_s_zero_markings": split_sheet_markings,
            "e_zero_s_zero_mode_one_complementary_minors_nonzero": True,
            "weighted_H22_lift": False,
            "counterexample": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
