#!/usr/bin/env python3
"""Verify the A0 quadratic companion fibre on component 25's B branch."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
Q = sp.Rational

# L=Q(s)/(4s^2-2s-3), so s^2=s/2+3/4.
l_zero = (Q(0), Q(0))
l_one = (Q(1), Q(0))
s_element = (Q(0), Q(1))
relation_linear = Q(1, 2)
relation_constant = Q(3, 4)


def l_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def l_neg(value):
    return (-value[0], -value[1])


def l_sub(left, right):
    return l_add(left, l_neg(right))


def l_mul(left, right):
    return (
        left[0] * right[0] + relation_constant * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0] + relation_linear * left[1] * right[1],
    )


def l_norm(value):
    return (
        value[0] ** 2
        + relation_linear * value[0] * value[1]
        - relation_constant * value[1] ** 2
    )


def l_inv(value):
    norm = l_norm(value)
    return (
        (value[0] + relation_linear * value[1]) / norm,
        -value[1] / norm,
    )


def l_div(left, right):
    return l_mul(left, l_inv(right))


def l_scalar(value):
    return (Q(value), Q(0))


def l_scale(coefficient, value):
    return (Q(coefficient) * value[0], Q(coefficient) * value[1])


# E=L(k)/(k^2-(2-4s/3)).  Its relative norm followed by the L/Q norm is
# the exact four-dimensional field norm used below.
k2 = l_sub(l_scalar(2), l_scale(Q(4, 3), s_element))
zero = (l_zero, l_zero)
one = (l_one, l_zero)
k = (l_zero, l_one)


def add(left, right):
    return (l_add(left[0], right[0]), l_add(left[1], right[1]))


def neg(value):
    return (l_neg(value[0]), l_neg(value[1]))


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    return (
        l_add(l_mul(left[0], right[0]), l_mul(k2, l_mul(left[1], right[1]))),
        l_add(l_mul(left[0], right[1]), l_mul(left[1], right[0])),
    )


def inv(value):
    relative_norm = l_sub(
        l_mul(value[0], value[0]), l_mul(k2, l_mul(value[1], value[1]))
    )
    inverse_norm = l_inv(relative_norm)
    return (l_mul(value[0], inverse_norm), l_neg(l_mul(value[1], inverse_norm)))


def div(left, right):
    return mul(left, inv(right))


def field_norm(value):
    return l_norm(
        l_sub(l_mul(value[0], value[0]), l_mul(k2, l_mul(value[1], value[1])))
    )


def scalar(value):
    return (l_scalar(value), l_zero)


def l_value(value):
    return (value, l_zero)


def e_scale(coefficient, value):
    return (l_mul(coefficient, value[0]), l_mul(coefficient, value[1]))


def sum_entries(entries):
    total = zero
    for entry in entries:
        total = add(total, entry)
    return total


def row_sum(*rows):
    return tuple(sum_entries(tuple(row[column] for row in rows)) for column in range(4))


def row_scale(coefficient, row):
    return tuple(e_scale(coefficient, value) for value in row)


def row_multiply(value, row):
    return tuple(mul(value, entry) for entry in row)


e = l_one
j = l_scalar(2)
s = s_element
q = l_scalar(3)
r = l_add(l_one, l_mul(j, l_mul(s, s)))
p = l_div(l_mul(q, q), r)
assert p == l_sub(l_scalar(4), l_scale(Q(4, 3), s))
assert k2 == l_sub(p, l_mul(e, j))
assert l_norm(k2) == Q(4, 3)
assert sp.sqrt(l_norm(k2)).is_Rational is False

# On A0=0, the nonzero companion of lambda=0 is lambda=5.
slope = l_scalar(5)
a2 = l_mul(
    l_mul(l_add(s, l_one), l_sub(l_mul(l_scalar(2), s), l_one)),
    l_sub(l_add(l_mul(l_scalar(4), l_mul(s, s)), l_mul(l_scalar(2), s)), l_scalar(3)),
)
a1 = l_neg(
    l_mul(
        l_scalar(2),
        l_sub(
            l_add(
                l_mul(l_scalar(8), l_mul(l_mul(s, s), l_mul(s, s))),
                l_mul(l_scalar(16), l_mul(s, s)),
            ),
            l_scalar(3),
        ),
    )
)
assert l_add(l_mul(a2, slope), a1) == l_zero

cap_a = tuple(map(scalar, (1, 1, 0, 0)))
cap_b = tuple(map(scalar, (0, 0, 1, 1)))
cap_c = tuple(map(scalar, (1, -1, 0, 0)))
cap_d = tuple(map(scalar, (0, 0, 1, -1)))
alpha = (
    row_sum(row_scale(q, cap_a), row_scale(l_neg(p), cap_b)),
    row_sum(
        row_scale(q, row_sum(cap_a, row_multiply(k, cap_d))),
        row_scale(l_neg(p), row_sum(cap_b, row_scale(s, cap_c))),
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
    row_sum(cap_a, row_scale(l_neg(l_mul(s, j)), cap_c), row_scale(j, cap_b)),
)

branch_denominator = l_sub(
    l_mul(l_mul(l_sub(slope, l_one), s), p),
    l_mul(l_add(slope, l_one), q),
)
h = l_sub(
    l_mul(l_add(slope, l_one), r),
    l_mul(l_mul(l_sub(slope, l_one), s), q),
)
t = l_sub(l_mul(l_sub(l_mul(j, s), l_one), slope), l_add(l_mul(j, s), l_one))
assert h == l_sub(l_scalar(15), l_mul(l_scalar(6), s))
assert t == l_sub(l_mul(l_scalar(8), s), l_scalar(6))
assert branch_denominator == l_sub(l_mul(l_scalar(Q(40, 3)), s), l_scalar(22))
z3 = l_div(s, l_mul(l_scalar(2), l_mul(p, branch_denominator)))


def extension(w, z6):
    inverse_k = (l_zero, l_inv(k2))
    z5 = add(z6, e_scale(l_neg(z3), k))
    z1 = add(
        add(
            e_scale(q, z6),
            e_scale(l_neg(l_mul(l_mul(p, s), l_sub(slope, l_one))), w),
        ),
        e_scale(l_mul(l_neg(j), l_mul(l_sub(k2, l_mul(e, e)), z3)), inverse_k),
    )
    z7 = e_scale(
        l_inv(l_sub(k2, l_mul(e, e))),
        add(
            add(
                e_scale(p, z6),
                e_scale(
                    l_neg(l_mul(l_mul(l_mul(k2, q), s), l_sub(slope, l_one))),
                    w,
                ),
            ),
            e_scale(l_neg(e), z1),
        ),
    )
    z0 = mul(
        add(
            l_value(
                l_sub(
                    l_mul(l_mul(p, p), z3),
                    l_div(l_scalar(Q(1, 2)), l_sub(slope, l_one)),
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
assert all(value != 0 for value in minor_norms)

print(
    json.dumps(
        {
            "status": "PASS",
            "base": "Q(s)/(4s^2-2s-3)",
            "weight": "lambda=5",
            "field": "Q(s)[k]/(4s^2-2s-3,k^2-2+4s/3)",
            "field_degree": 4,
            "binary_section_solved_over_full_field": True,
            "coefficient_splitting_used": False,
            "opposite_diagonal_norm": str(opposite_diagonal_norm),
            "D23_minor_norms": list(map(str, minor_norms)),
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
