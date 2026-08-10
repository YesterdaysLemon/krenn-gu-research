#!/usr/bin/env python3
"""Verify component 25's global C0=0 companion-weight divisor."""

from __future__ import annotations

import itertools
import json
import time

import sympy as sp

started = time.perf_counter()

A, B, Lambda = sp.symbols("A B Lambda")
c0_global = (3 * B**2 - B - 1) * A**2 - B * (B - 1) ** 2 * A - B**3
a1_global = -2 * (
    3 * A**3 * B**3 - 2 * A**3 * B - A**2 * B**4 + A**2 * B**2 - A**2 - A * B + B**4
)
a2_global = (
    (A + 1)
    * (B - 1)
    * (3 * A**2 * B**2 + A**2 * B - A**2 - A * B**3 - 2 * A * B**2 - A * B + B**3)
)
a0_global = (A - 1) * (B + 1) * c0_global
n_global = a2_global * Lambda**2 + a1_global * Lambda + a0_global
assert sp.factor(n_global.subs(B, -1)) == (
    -2 * Lambda * (Lambda - 1) * (A - 1) * (A + 1) ** 2
)

r_global = 1 + A * B
q_global = A + B
k2_numerator = q_global**2 - A * B * r_global
e2_minus_k2_numerator = A**2 * r_global - k2_numerator
assert sp.expand(e2_minus_k2_numerator.subs(A, 1)) == 0
h_numerator = (a2_global - a1_global) * r_global + (a1_global + a2_global) * q_global
t_numerator = -(B - 1) * a1_global - (B + 1) * a2_global
assert (
    sp.factor(
        sp.discriminant(c0_global, A) - B**2 * (B**4 + 8 * B**3 + 2 * B**2 - 8 * B + 1)
    )
    == 0
)
resultant_identities = {
    "Q": (q_global, 4 * B**3 * (B - 1)),
    "R": (
        r_global,
        -((B - 1) ** 2) * (B**3 + B**2 + 3 * B + 1),
    ),
    "k": (
        k2_numerator,
        -(B**4) * (B - 1) ** 2 * (B**3 - 3 * B**2 + B - 1),
    ),
    "e-j": (A - B, 2 * B**2 * (B - 1) * (B + 1)),
    "e^2-k^2": (
        e2_minus_k2_numerator,
        -4 * B**5 * (B - 1) ** 3 * (B + 1) * (2 * B**2 - 3 * B - 1),
    ),
    "A2": (a2_global, 16 * B**6 * (B - 1) ** 5 * (B + 1) ** 3),
    "A1": (
        a1_global,
        -16 * B**6 * (B - 1) ** 3 * (B + 1) * (B**4 + 8 * B**3 - 4 * B - 1),
    ),
    "H": (
        h_numerator,
        64 * B**10 * (B - 1) ** 6 * (B + 1) * (B**2 + 8 * B + 3),
    ),
    "T": (t_numerator, -128 * B**10 * (B - 1) ** 4 * (B + 1)),
}
for polynomial, expected in resultant_identities.values():
    assert sp.factor(sp.resultant(c0_global, polynomial, A) - expected) == 0

base, b = sp.polys.fields.field("b", sp.QQ)
relation_denominator = 3 * b**2 - b - 1
relation_linear = b * (b - 1) ** 2 / relation_denominator
relation_constant = b**3 / relation_denominator
l_zero = (base.zero, base.zero)
l_one = (base.one, base.zero)
a = (base.zero, base.one)


def l_add(left, right):
    return (left[0] + right[0], left[1] + right[1])


def l_neg(value):
    return (-value[0], -value[1])


def l_sub(left, right):
    return (left[0] - right[0], left[1] - right[1])


def l_mul(left, right):
    # a^2=relation_linear*a+relation_constant on C0=0.
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


e = a
j = l_scalar(b)
q = l_add(e, j)
r = l_add(l_one, l_mul(e, j))
p = l_div(l_mul(q, q), r)
k2 = l_sub(p, l_mul(e, j))
zero = (l_zero, l_zero)
one = (l_one, l_zero)
k = (l_zero, l_one)
assert l_mul(p, r) == l_mul(q, q)

# On C0=0, the nonzero companion of lambda=0 is lambda=-A1/A2.
a_squared = l_mul(a, a)
a_cubed = l_mul(a_squared, a)
a1_core = l_sum(
    l_mul(l_scalar(3 * b**3), a_cubed),
    l_mul(l_scalar(-2 * b), a_cubed),
    l_mul(l_scalar(-(b**4)), a_squared),
    l_mul(l_scalar(b**2), a_squared),
    l_neg(a_squared),
    l_mul(l_scalar(-b), a),
    l_scalar(b**4),
)
a1 = l_mul(l_scalar(-2), a1_core)
a2_core = l_sum(
    l_mul(l_scalar(3 * b**2), a_squared),
    l_mul(l_scalar(b), a_squared),
    l_neg(a_squared),
    l_mul(l_scalar(-(b**3)), a),
    l_mul(l_scalar(-2 * b**2), a),
    l_mul(l_scalar(-b), a),
    l_scalar(b**3),
)
a2 = l_mul(l_mul(l_add(a, l_one), l_scalar(b - 1)), a2_core)
slope = l_div(l_neg(a1), a2)

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


minor_determinants = tuple(determinant(one_marked_matrix(mode)) for mode in range(4))
minor_norms = tuple(field_norm(value) for value in minor_determinants)
assert all(norm != base.zero for norm in minor_norms)
gcd_numerator = minor_norms[0].numer
for norm in minor_norms[1:]:
    gcd_numerator = gcd_numerator.gcd(norm.numer)
assert gcd_numerator.as_expr() == 1

b_symbol = sp.Symbol("b")
denominator_irreducibles = set()


def collect_denominators(value):
    if isinstance(value, dict):
        for entry in value.values():
            collect_denominators(entry)
        return
    if isinstance(value, (tuple, list, set)):
        for entry in value:
            collect_denominators(entry)
        return
    if hasattr(value, "denom"):
        denominator_irreducibles.update(
            sp.Poly(factor, b_symbol).monic().as_expr()
            for factor, _multiplicity in sp.factor_list(value.denom.as_expr())[1]
        )


collect_denominators(
    (
        p,
        k2,
        a2,
        a1,
        slope,
        branch_denominator,
        z3,
        alpha,
        beta,
        extension(w, z6),
        marking,
        coefficients,
        marked_23,
        minor_determinants,
        opposite_diagonal_norm,
        minor_norms,
    )
)
expected_denominator_irreducibles = {
    sp.Poly(factor, b_symbol).monic().as_expr()
    for factor in (
        b_symbol,
        b_symbol - 1,
        b_symbol + 1,
        3 * b_symbol**2 - b_symbol - 1,
        b_symbol**2 + 8 * b_symbol + 3,
        b_symbol**3 + b_symbol**2 + 3 * b_symbol + 1,
        b_symbol**3 - 3 * b_symbol**2 + b_symbol - 1,
        b_symbol**4 + 8 * b_symbol**3 - 4 * b_symbol - 1,
    )
}
assert denominator_irreducibles == expected_denominator_irreducibles


def norm_signature(value):
    numerator = value.numer.as_expr()
    denominator = value.denom.as_expr()
    return (
        sp.degree(numerator, b_symbol),
        sp.degree(denominator, b_symbol),
        numerator.subs(b_symbol, 0),
        sp.LC(sp.Poly(numerator, b_symbol)),
    )


opposite_signature = norm_signature(opposite_diagonal_norm)
minor_signatures = tuple(norm_signature(norm) for norm in minor_norms)
assert opposite_signature == (15, 23, -4, 48)
assert minor_signatures == (
    (86, 80, 1, 9072),
    (81, 75, 540, 27),
    (51, 51, 256, 2160),
    (58, 54, -1764, 48),
)
print(
    json.dumps(
        {
            "status": "PASS",
            "divisor": "C0=0 companion lambda=-A1/A2",
            "field": "Q(b)[a,k]/(C0,k^2-P+ab)",
            "binary_section_solved_over_full_field": True,
            "coefficient_splitting_used": False,
            "opposite_diagonal_norm_signature": list(map(str, opposite_signature)),
            "D23_minor_norm_signatures": [
                list(map(str, signature)) for signature in minor_signatures
            ],
            "D23_minor_norm_numerator_gcd": "1",
            "denominator_irreducibles": sorted(map(str, denominator_irreducibles)),
            "weighted_H22_lift": False,
            "counterexample": False,
            "finite_field_evidence_used": False,
            "global_conjecture_resolved": False,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        },
        indent=2,
    )
)
