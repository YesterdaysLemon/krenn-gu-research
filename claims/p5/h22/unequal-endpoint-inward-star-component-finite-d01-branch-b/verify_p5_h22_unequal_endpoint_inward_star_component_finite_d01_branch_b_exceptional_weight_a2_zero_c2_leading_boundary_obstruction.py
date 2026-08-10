#!/usr/bin/env python3
"""Verify the leading-coefficient boundary of component 25's C2=0 piece."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
base, dummy = sp.polys.fields.field("dummy", sp.QQ)
relation_linear = base.from_expr(sp.Rational(-1, 3))
relation_constant = base.from_expr(sp.Rational(1, 3))
l_zero = (base.zero, base.zero)
l_one = (base.one, base.zero)
b_element = (base.zero, base.one)


def l_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def l_neg(value):
    return (-value[0], -value[1])


def l_sub(left, right):
    return (left[0] - right[0], left[1] - right[1])


def l_mul(left, right):
    # a^2=relation_linear*a+relation_constant on C2=0.
    return (
        left[0] * right[0] + relation_constant * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0] + relation_linear * left[1] * right[1],
    )


def l_inv(value):
    norm = (
        value[0] ** 2
        + relation_linear * value[0] * value[1]
        - relation_constant * value[1] ** 2
    )
    return (
        (value[0] + relation_linear * value[1]) / norm,
        -value[1] / norm,
    )


def l_div(left, right):
    return l_mul(left, l_inv(right))


def l_scalar(value):
    if hasattr(value, "field"):
        return (value, base.zero)
    return (base.from_expr(sp.sympify(value)), base.zero)


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


def l_norm(value):
    return (
        value[0] ** 2
        + relation_linear * value[0] * value[1]
        - relation_constant * value[1] ** 2
    )


def field_norm(value):
    return l_norm(
        l_sub(
            l_mul(value[0], value[0]),
            l_mul(k2, l_mul(value[1], value[1])),
        )
    )


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


j = b_element
e = l_div(
    l_mul(j, j),
    l_mul(l_add(j, l_one), l_add(j, l_one)),
)
q = l_add(e, j)
r = l_add(l_one, l_mul(e, j))
p = l_div(l_mul(q, q), r)
k2 = l_sub(p, l_mul(e, j))
zero = (l_zero, l_zero)
one = (l_one, l_zero)
k = (l_zero, l_one)
assert l_mul(p, r) == l_mul(q, q)


# N=A1*lambda+A0 on C2=0.
def l_power(value, exponent):
    result = l_one
    for _ in range(exponent):
        result = l_mul(result, value)
    return result


e_squared = l_power(e, 2)
e_cubed = l_power(e, 3)
j_squared = l_power(j, 2)
j_cubed = l_power(j, 3)
j_fourth = l_power(j, 4)
a1_core = l_sum(
    l_mul(l_scalar(3), l_mul(e_cubed, j_cubed)),
    l_mul(l_scalar(-2), l_mul(e_cubed, j)),
    l_neg(l_mul(e_squared, j_fourth)),
    l_mul(e_squared, j_squared),
    l_neg(e_squared),
    l_neg(l_mul(e, j)),
    j_fourth,
)
a1 = l_mul(l_scalar(-2), a1_core)
a0_core = l_sum(
    l_mul(l_scalar(3), l_mul(e_squared, j_squared)),
    l_neg(l_mul(e_squared, j)),
    l_neg(e_squared),
    l_neg(l_mul(e, j_cubed)),
    l_mul(l_scalar(2), l_mul(e, j_squared)),
    l_neg(l_mul(e, j)),
    l_neg(j_cubed),
)
a0 = l_mul(l_mul(l_sub(e, l_one), l_add(j, l_one)), a0_core)
slope = l_div(l_neg(a0), a1)

cap_a = tuple(map(scalar, (1, 1, 0, 0)))
cap_b = tuple(map(scalar, (0, 0, 1, 1)))
cap_c = tuple(map(scalar, (1, -1, 0, 0)))
cap_d = tuple(map(scalar, (0, 0, 1, -1)))
alpha = (
    row_sum(row_scale(q, cap_a), row_scale(l_neg(p), cap_b)),
    row_sum(
        row_scale(q, row_sum(cap_a, row_multiply(k, cap_d))),
        row_scale(l_neg(p), row_sum(cap_b, cap_c)),
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
        row_scale(l_neg(j), cap_c),
        row_scale(j, cap_b),
    ),
)

branch_denominator = l_sub(
    l_mul(l_sub(slope, l_one), p),
    l_mul(l_add(slope, l_one), q),
)
z3 = l_div(l_one, l_mul(l_scalar(2), l_mul(p, branch_denominator)))


def extension(w, z6):
    inverse_k = (l_zero, l_inv(k2))
    z5 = add(z6, e_scale(l_neg(z3), k))
    z1 = add(
        add(
            e_scale(q, z6),
            e_scale(l_neg(l_mul(p, l_sub(slope, l_one))), w),
        ),
        e_scale(l_mul(l_neg(j), l_mul(l_sub(k2, l_mul(e, e)), z3)), inverse_k),
    )
    z7 = e_scale(
        l_inv(l_sub(k2, l_mul(e, e))),
        add(
            add(
                e_scale(p, z6),
                e_scale(l_neg(l_mul(l_mul(k2, q), l_sub(slope, l_one))), w),
            ),
            e_scale(l_neg(e), z1),
        ),
    )
    z0 = mul(
        add(
            l_value(
                l_sub(
                    l_mul(l_mul(p, p), z3),
                    l_div(l_scalar(sp.Rational(1, 2)), l_sub(slope, l_one)),
                )
            ),
            e_scale(l_neg(l_mul(l_mul(q, q), l_add(slope, l_one))), mul(k, w)),
        ),
        e_scale(l_inv(q), inverse_k),
    )
    return (
        z0,
        z1,
        e_scale(l_sub(slope, l_one), w),
        l_value(z3),
        e_scale(l_neg(l_add(slope, l_one)), w),
        z5,
        z6,
        z7,
    )


def project(row, extra, direction):
    if direction == "D01":
        return (add(e_scale(slope, row[0]), row[1]), row[2], row[3], extra)
    return (row[0], row[1], add(e_scale(slope, row[2]), row[3]), extra)


def projected(w, z6, direction):
    ext = extension(w, z6)
    return (
        tuple(project(alpha[index], ext[index], direction) for index in range(4)),
        tuple(project(beta[index], ext[index + 4], direction) for index in range(4)),
    )


def permanent(rows):
    total = zero
    for permutation in itertools.permutations(range(4)):
        term = one
        for index in range(4):
            term = mul(term, rows[index][permutation[index]])
        total = add(total, term)
    return total


def residuals(w, z6):
    alpha_rows, beta_rows = projected(w, z6, "D01")

    def coefficient(word):
        return permanent(
            tuple(
                beta_rows[index] if bit else alpha_rows[index]
                for index, bit in enumerate(word)
            )
        )

    c0_local = coefficient((0, 0, 0, 0))
    c1 = coefficient((0, 1, 0, 0))
    c2 = coefficient((0, 0, 1, 0))
    c3 = coefficient((0, 0, 0, 1))
    return (
        sub(mul(coefficient((0, 1, 0, 1)), c0_local), mul(c1, c3)),
        sub(mul(coefficient((0, 0, 1, 1)), c0_local), mul(c2, c3)),
        sub(
            mul(coefficient((0, 1, 1, 1)), mul(c0_local, c0_local)),
            mul(mul(c1, c2), c3),
        ),
    )


origin = residuals(zero, zero)
unit_w = residuals(one, zero)
unit_z6 = residuals(zero, one)
a11 = sub(unit_w[0], origin[0])
a12 = sub(unit_z6[0], origin[0])
a21 = sub(unit_w[1], origin[1])
a22 = sub(unit_z6[1], origin[1])
determinant_system = sub(mul(a11, a22), mul(a12, a21))
rhs1 = neg(origin[0])
rhs2 = neg(origin[1])
w = div(sub(mul(rhs1, a22), mul(a12, rhs2)), determinant_system)
z6 = div(sub(mul(a11, rhs2), mul(rhs1, a21)), determinant_system)
assert residuals(w, z6) == (zero, zero, zero)

alpha_01, beta_01 = projected(w, z6, "D01")
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
opposite_diagonal_norm = field_norm(coefficients[(1, 1, 1, 1)])
assert opposite_diagonal_norm != base.zero

alpha_23, beta_23 = projected(w, z6, "D23")
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
    total = zero
    for permutation in itertools.permutations(range(4)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(4)
            for right in range(left + 1, 4)
        )
        term = one
        for index in range(4):
            term = mul(term, matrix[index][permutation[index]])
        total = add(total, neg(term) if inversions % 2 else term)
    return total


minor_norms = tuple(
    field_norm(determinant(one_marked_matrix(mode))) for mode in range(4)
)
assert all(norm != base.zero for norm in minor_norms)
gcd_numerator = minor_norms[0].numer
for norm in minor_norms[1:]:
    gcd_numerator = gcd_numerator.gcd(norm.numer)
assert slope == (base.from_expr(-3), base.from_expr(-6))
assert w == (
    l_zero,
    (
        base.from_expr(sp.Rational(-400273, 222720)),
        base.from_expr(sp.Rational(-173929, 74240)),
    ),
)
assert z6 == (
    l_zero,
    (
        base.from_expr(sp.Rational(-135151, 27840)),
        base.from_expr(sp.Rational(-46931, 7424)),
    ),
)
assert opposite_diagonal_norm == base.from_expr(sp.Rational(-7952112, 18125))
expected_minor_norms = (
    sp.Rational(30155630569279962260615452611, 409179521024000000000000),
    sp.Rational(-2996261580477497324383849919733, 881852416000000000000),
    sp.Rational(-3507185203823023069968, 5954345703125),
    sp.Rational(545235920497542050554260717, 5954345703125),
)
assert tuple(norm.as_expr() for norm in minor_norms) == expected_minor_norms

print(
    json.dumps(
        {
            "status": "PASS",
            "boundary": "3b^2+b-1=0",
            "field": "Q(b)[k]/(3b^2+b-1,k^2-P+ab)",
            "a": "b^2/(b+1)^2",
            "lambda_basis_1_b": ["-3", "-6"],
            "binary_section_solved_over_full_field": True,
            "coefficient_splitting_used": False,
            "opposite_diagonal_norm": str(opposite_diagonal_norm.as_expr()),
            "D23_minor_norms": [str(norm.as_expr()) for norm in minor_norms],
            "all_four_D23_modes_rank_four": True,
            "weighted_H22_lift": False,
            "counterexample": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
