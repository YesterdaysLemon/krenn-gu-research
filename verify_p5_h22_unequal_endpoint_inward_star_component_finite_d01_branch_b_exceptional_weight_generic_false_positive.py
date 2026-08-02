#!/usr/bin/env python3
"""Verify the generic false-positive classification on branch B's N=0 divisor."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()
base, s = sp.polys.fields.field("s", sp.QQ)
e = base.one
j = 2 * base.one
q = e + j
r = 1 + e * j * s**2
p = q**2 / r
k2 = p - e * j

a2 = (
    (e * s + 1)
    * (j * s - 1)
    * (
        3 * e**2 * j**2 * s**2
        + e**2 * j * s
        - e**2
        - e * j**3 * s**2
        - 2 * e * j**2 * s
        - e * j
        + j**3 * s
    )
)
a1 = -2 * (
    3 * e**3 * j**3 * s**4
    - 2 * e**3 * j * s**2
    - e**2 * j**4 * s**4
    + e**2 * j**2 * s**2
    - e**2
    - e * j
    + j**4 * s**2
)
a0 = (
    (e * s - 1)
    * (j * s + 1)
    * (
        3 * e**2 * j**2 * s**2
        - e**2 * j * s
        - e**2
        - e * j**3 * s**2
        + 2 * e * j**2 * s
        - e * j
        - j**3 * s
    )
)

# lambda^2 = lambda_linear*lambda + lambda_constant modulo N.
lambda_linear = -a1 / a2
lambda_constant = -a0 / a2
l_zero = (base.zero, base.zero)
l_one = (base.one, base.zero)
lam = (base.zero, base.one)

# The exact slice is genuinely one-dimensional.  Its discriminant is a
# nonzero square times a squarefree, nonconstant polynomial, hence N remains
# irreducible over Q(s); no algebraic weight is specialized to a point.
s_symbol = sp.Symbol("s")
slice_discriminant = sp.factor((a1**2 - 4 * a2 * a0).as_expr())
squarefree_core = 448 * s_symbol**4 + 16 * s_symbol**2 - 23
assert slice_discriminant == 4 * s_symbol**2 * squarefree_core
assert (
    sp.gcd(
        sp.Poly(squarefree_core, s_symbol), sp.Poly(squarefree_core, s_symbol).diff()
    )
    == 1
)
k_numerator = 7 - 4 * s_symbol**2
k_denominator = 1 + 2 * s_symbol**2
assert sp.gcd(sp.Poly(k_numerator, s_symbol), sp.Poly(k_denominator, s_symbol)) == 1
assert sp.gcd(sp.Poly(squarefree_core, s_symbol), sp.Poly(k_numerator, s_symbol)) == 1
assert sp.gcd(sp.Poly(squarefree_core, s_symbol), sp.Poly(k_denominator, s_symbol)) == 1


def l_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def l_neg(left):
    return (-left[0], -left[1])


def l_sub(left, right):
    return (left[0] - right[0], left[1] - right[1])


def l_mul(left, right):
    return (
        left[0] * right[0] + lambda_constant * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0] + lambda_linear * left[1] * right[1],
    )


def l_inv(value):
    norm = l_norm(value)
    return (
        (value[0] + lambda_linear * value[1]) / norm,
        -value[1] / norm,
    )


def l_norm(value):
    return (
        value[0] ** 2
        + lambda_linear * value[0] * value[1]
        - lambda_constant * value[1] ** 2
    )


def l_div(left, right):
    return l_mul(left, l_inv(right))


def l_scalar(value):
    if hasattr(value, "field"):
        return (value, base.zero)
    return (base.from_expr(sp.sympify(value)), base.zero)


zero = (l_zero, l_zero)
one = (l_one, l_zero)
k = (l_zero, l_one)


def add(left, right):
    return (l_add(left[0], right[0]), l_add(left[1], right[1]))


def neg(left):
    return (l_neg(left[0]), l_neg(left[1]))


def sub(left, right):
    return (l_sub(left[0], right[0]), l_sub(left[1], right[1]))


def mul(left, right):
    return (
        l_add(l_mul(left[0], right[0]), l_mul(l_scalar(k2), l_mul(left[1], right[1]))),
        l_add(l_mul(left[0], right[1]), l_mul(left[1], right[0])),
    )


def inv(value):
    norm = l_sub(
        l_mul(value[0], value[0]), l_mul(l_scalar(k2), l_mul(value[1], value[1]))
    )
    inverse_norm = l_inv(norm)
    return (l_mul(value[0], inverse_norm), l_neg(l_mul(value[1], inverse_norm)))


def field_norm(value):
    return l_norm(
        l_sub(
            l_mul(value[0], value[0]),
            l_mul(l_scalar(k2), l_mul(value[1], value[1])),
        )
    )


def div(left, right):
    return mul(left, inv(right))


def scalar(value):
    return (l_scalar(value), l_zero)


def lambda_value(value):
    return (value, l_zero)


def e_scale(coefficient, value):
    return (l_mul(coefficient, value[0]), l_mul(coefficient, value[1]))


def row_sum(*rows):
    return tuple(sum_entries(tuple(row[column] for row in rows)) for column in range(4))


def sum_entries(entries):
    value = zero
    for entry in entries:
        value = add(value, entry)
    return value


def row_scale(coefficient, row):
    return tuple(e_scale(coefficient, value) for value in row)


def row_multiply(value, row):
    return tuple(mul(value, entry) for entry in row)


cap_a = tuple(map(scalar, (1, 1, 0, 0)))
cap_b = tuple(map(scalar, (0, 0, 1, 1)))
cap_c = tuple(map(scalar, (1, -1, 0, 0)))
cap_d = tuple(map(scalar, (0, 0, 1, -1)))
alpha = (
    row_sum(row_scale(l_scalar(q), cap_a), row_scale(l_scalar(-p), cap_b)),
    row_sum(
        row_scale(l_scalar(q), row_sum(cap_a, row_multiply(k, cap_d))),
        row_scale(l_scalar(-p), row_sum(cap_b, row_scale(l_scalar(s), cap_c))),
    ),
    cap_c,
    cap_d,
)
beta = (
    cap_a,
    row_sum(cap_a, row_multiply(k, cap_d)),
    row_sum(
        cap_a,
        row_scale(l_scalar(e), cap_b),
        row_scale(l_scalar(-1), row_multiply(k, cap_d)),
    ),
    row_sum(cap_a, row_scale(l_scalar(-s * j), cap_c), row_scale(l_scalar(j), cap_b)),
)

slope_minus_one = l_sub(lam, l_one)
slope_plus_one = l_add(lam, l_one)
branch_denominator = l_sub(
    l_mul(slope_minus_one, l_scalar(s * p)),
    l_mul(slope_plus_one, l_scalar(q)),
)
z3 = l_div(l_scalar(s), l_mul(l_scalar(2 * p), branch_denominator))

chart_factor = l_sub(
    l_mul(slope_plus_one, l_scalar(r)),
    l_mul(slope_minus_one, l_scalar(s * q)),
)
weight_factor = l_sub(l_mul(l_scalar(j * s - 1), lam), l_scalar(j * s + 1))
retained_base_factors = (
    p,
    r,
    k2,
    q,
    e - j,
    e**2 - k2,
    e,
    j,
    s,
    a2,
)
assert all(value != base.zero for value in retained_base_factors)
retained_weight_factors = (
    lam,
    slope_minus_one,
    slope_plus_one,
    l_sub(l_mul(lam, lam), l_one),
    chart_factor,
    weight_factor,
    branch_denominator,
)
assert all(l_norm(value) != base.zero for value in retained_weight_factors)


def extension(w, z6):
    inverse_k = mul(k, scalar(1 / k2))
    z5 = add(z6, e_scale(l_neg(z3), k))
    z1 = add(
        add(
            e_scale(l_scalar(q), z6),
            e_scale(l_mul(l_scalar(-p * s), slope_minus_one), w),
        ),
        e_scale(l_mul(l_scalar(-j * (k2 - e**2)), z3), inverse_k),
    )
    z7 = e_scale(
        l_scalar(1 / (k2 - e**2)),
        add(
            add(
                e_scale(l_scalar(p), z6),
                e_scale(l_mul(l_scalar(-k2 * q * s), slope_minus_one), w),
            ),
            e_scale(l_scalar(-e), z1),
        ),
    )
    z0 = mul(
        add(
            lambda_value(
                l_sub(
                    l_mul(l_scalar(p**2), z3),
                    l_div(l_scalar(sp.Rational(1, 2)), slope_minus_one),
                )
            ),
            e_scale(l_neg(l_mul(l_scalar(q**2), slope_plus_one)), mul(k, w)),
        ),
        mul(k, scalar(1 / (k2 * q))),
    )
    return (
        z0,
        z1,
        e_scale(slope_minus_one, w),
        lambda_value(z3),
        e_scale(l_neg(slope_plus_one), w),
        z5,
        z6,
        z7,
    )


def project(row, extra, direction):
    if direction == "D01":
        return (add(e_scale(lam, row[0]), row[1]), row[2], row[3], extra)
    return (row[0], row[1], add(e_scale(lam, row[2]), row[3]), extra)


def projected(w, z6, direction):
    ext = extension(w, z6)
    return (
        tuple(project(alpha[i], ext[i], direction) for i in range(4)),
        tuple(project(beta[i], ext[i + 4], direction) for i in range(4)),
    )


def permanent_dp(rows):
    states = {0: one}
    for row in rows:
        new_states = {}
        for mask, coefficient in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                new_states[new_mask] = add(
                    new_states.get(new_mask, zero), mul(coefficient, entry)
                )
        states = new_states
    return states[15]


def residuals(w, z6):
    alpha_rows, beta_rows = projected(w, z6, "D01")

    def coefficient(word):
        return permanent_dp(
            tuple(beta_rows[i] if bit else alpha_rows[i] for i, bit in enumerate(word))
        )

    c0 = coefficient((0, 0, 0, 0))
    c1 = coefficient((0, 1, 0, 0))
    c2 = coefficient((0, 0, 1, 0))
    c3 = coefficient((0, 0, 0, 1))
    return (
        sub(mul(coefficient((0, 1, 0, 1)), c0), mul(c1, c3)),
        sub(mul(coefficient((0, 0, 1, 1)), c0), mul(c2, c3)),
        sub(mul(coefficient((0, 1, 1, 1)), mul(c0, c0)), mul(mul(c1, c2), c3)),
    )


origin = residuals(zero, zero)
unit_w = residuals(one, zero)
unit_z6 = residuals(zero, one)
a11 = sub(unit_w[0], origin[0])
a12 = sub(unit_z6[0], origin[0])
a21 = sub(unit_w[1], origin[1])
a22 = sub(unit_z6[1], origin[1])
det = sub(mul(a11, a22), mul(a12, a21))
rhs1 = neg(origin[0])
rhs2 = neg(origin[1])
w = div(sub(mul(rhs1, a22), mul(a12, rhs2)), det)
z6 = div(sub(mul(a11, rhs2), mul(rhs1, a21)), det)
assert residuals(w, z6) == (zero, zero, zero)

alpha_01, beta_01 = projected(w, z6, "D01")
c0 = permanent_dp(alpha_01)
marking = tuple(
    div(
        neg(
            permanent_dp(
                tuple(beta_01[i] if i == mode else alpha_01[i] for i in range(4))
            )
        ),
        c0,
    )
    for mode in range(4)
)

marked_01 = tuple(
    tuple(
        add(
            beta_01[index][coordinate], mul(marking[index], alpha_01[index][coordinate])
        )
        for coordinate in range(4)
    )
    for index in range(4)
)
binary_coefficients = {}
for word in itertools.product((0, 1), repeat=4):
    binary_coefficients[word] = permanent_dp(
        tuple(
            marked_01[index] if bit else alpha_01[index]
            for index, bit in enumerate(word)
        )
    )
assert binary_coefficients[(0, 0, 0, 0)] == one
for word, value in binary_coefficients.items():
    if word not in ((0, 0, 0, 0), (1, 1, 1, 1)):
        assert value == zero
opposite_diagonal = binary_coefficients[(1, 1, 1, 1)]
opposite_diagonal_norm = field_norm(opposite_diagonal)
assert opposite_diagonal_norm != base.zero
opposite_diagonal_signature = (
    sp.degree(opposite_diagonal_norm.numer.as_expr(), s_symbol),
    sp.degree(opposite_diagonal_norm.denom.as_expr(), s_symbol),
    opposite_diagonal_norm.numer.as_expr().subs(s_symbol, 0),
    sp.LC(sp.Poly(opposite_diagonal_norm.numer.as_expr(), s_symbol)),
)
assert opposite_diagonal_signature == (24, 28, 0, 12845056)

alpha_23, beta_23 = projected(w, z6, "D23")
marked_23 = tuple(
    tuple(
        add(beta_23[i][column], mul(marking[i], alpha_23[i][column]))
        for column in range(4)
    )
    for i in range(4)
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
                permanent_dp(
                    tuple(
                        basis if index == mode else selected[index]
                        for index in range(4)
                    )
                )
            )
        matrix.append(row)
    return matrix


def determinant4(matrix):
    total = zero
    for permutation in itertools.permutations(range(4)):
        sign = (
            -1
            if sum(
                permutation[a] > permutation[b]
                for a in range(4)
                for b in range(a + 1, 4)
            )
            % 2
            else 1
        )
        term = scalar(sign)
        for i in range(4):
            term = mul(term, matrix[i][permutation[i]])
        total = add(total, term)
    return total


norm_signatures = []
for mode in range(4):
    minor = determinant4(one_marked_matrix(mode))
    norm = field_norm(minor)
    assert norm != base.zero
    norm_signatures.append(
        (
            sp.degree(norm.numer.as_expr(), sp.Symbol("s")),
            sp.degree(norm.denom.as_expr(), sp.Symbol("s")),
            norm.numer.as_expr().subs(sp.Symbol("s"), 0),
            sp.LC(sp.Poly(norm.numer.as_expr(), sp.Symbol("s"))),
        )
    )

expected_norm_signatures = (
    (92, 56, 2559780258021441, 1152921504606846976),
    (102, 66, -70413806736, 295147905179352825856),
    (80, 60, 0, 166020696663385964544),
    (84, 64, 0, 2594073385365405696),
)
assert tuple(norm_signatures) == expected_norm_signatures

print(
    json.dumps(
        {
            "status": "PASS",
            "global_exceptional_divisor": "N=A2*lambda^2+A1*lambda+A0",
            "exact_nonpoint_slice": {"e": 1, "j": 2, "parameter": "s"},
            "slice_field": "Q(s)[lambda,k]/(N,k^2-(7-4s^2)/(1+2s^2))",
            "coefficient_splitting_used": False,
            "binary_residuals_zero_on_N": True,
            "opposite_diagonal_norm_signature": list(
                map(str, opposite_diagonal_signature)
            ),
            "D23_rank_four_modes": [0, 1, 2, 3],
            "iterated_norm_signatures": [
                list(map(str, signature)) for signature in norm_signatures
            ],
            "generic_exceptional_section_is_false_positive": True,
            "known_point_used_for_generic_inference": False,
            "counterexample": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
