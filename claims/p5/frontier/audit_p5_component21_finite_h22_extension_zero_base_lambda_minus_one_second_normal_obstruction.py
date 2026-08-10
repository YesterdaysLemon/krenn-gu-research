#!/usr/bin/env python3
"""No-import audit of component 21's lambda=-1 second normals."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
DIAGONAL_ROWS = (0, 15, 16, 31)


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


def permanent3(rows):
    return sum(
        sp.prod(rows[row][column] for row, column in enumerate(permutation))
        for permutation in itertools.permutations(range(3))
    )


def project(row, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3])
    return (row[0], row[1], slope * row[2] + row[3])


def contraction_matrix(alpha, beta, direction, slope):
    projected_alpha = tuple(project(row, direction, slope) for row in alpha)
    projected_beta = tuple(project(row, direction, slope) for row in beta)
    output = []
    for word in WORDS:
        selected = tuple(
            projected_beta[index] if word[index] else projected_alpha[index]
            for index in range(4)
        )
        matrix_row = [sp.S.Zero] * 8
        for mode in range(4):
            cofactor = permanent3(
                tuple(selected[index] for index in range(4) if index != mode)
            )
            matrix_row[(4 if word[mode] else 0) + mode] = cofactor
        output.append(matrix_row)
    return sp.Matrix(output)


def stacked_matrix(alpha, beta, slope):
    return contraction_matrix(alpha, beta, "D01", slope).col_join(
        contraction_matrix(alpha, beta, "D23", slope)
    )


def determinant(matrix, rows, columns):
    return sp.factor(matrix.extract(rows, columns).det())


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero(vector):
    return all(sp.expand(value) == 0 for value in vector)


def unit(length, index):
    return sp.eye(length).col(index)


def independent(vectors):
    return sp.Matrix.hstack(*vectors).rank() == len(vectors)


p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
X, Y, Z = sp.symbols("X Y Z")
tangent = sp.symbols("t")
P, Q, A, B, C, E = sp.symbols("P Q A B C E")
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = stacked_matrix(alpha, beta, slope)
identity = sp.eye(8)
u = identity.col(3)
w = identity.col(7)
v = -identity.col(1) + identity.col(4)


def normal(leading, substitution):
    output = matrix.subs(substitution)
    for parameter in (p, q, kappa, ell, slope):
        output = output.row_join(
            (sp.diff(matrix, parameter) * leading).subs(substitution)
        )
    return output


# kappa!=0 P1, its open locus, and its intersection with the ordinary line.
h_plane = X * u + Y * w
n_plane = normal(h_plane, {p: 0, q: 0, slope: -1})
plane_kernel = (
    u.col_join(sp.zeros(5, 1)),
    w.col_join(sp.zeros(5, 1)),
    unit(13, 10),
    unit(13, 11),
)
assert independent(plane_kernel)
assert all(is_zero(n_plane * vector) for vector in plane_kernel)
assert n_plane.row(0) == sp.zeros(1, 13)
assert n_plane.row(15) == sp.zeros(1, 13)
assert_equal(
    determinant(
        n_plane,
        (3, 11, 18, 20, 22, 23, 24, 26, 28),
        (0, 1, 2, 4, 5, 6, 8, 9, 12),
    ),
    -131072 * Y**3 * kappa**2,
)
n_u_nonzero = n_plane.subs({X: 1, Y: 0})
weight_lift = sp.Rational(1, 2) * unit(13, 6) + unit(13, 12)
assert is_zero(n_u_nonzero * weight_lift)
assert_equal(
    determinant(
        n_u_nonzero,
        (2, 10, 18, 20, 22, 24, 26, 28),
        (0, 1, 2, 4, 5, 6, 8, 9),
    ),
    65536 * kappa**2,
)
force_lambda_w = (sp.diff(matrix, slope) * w).subs(
    {p: 0, q: 0, slope: -1}
)
assert all(force_lambda_w[row] == 0 for row in DIAGONAL_ROWS)
augmented_u = n_u_nonzero.row_join(force_lambda_w)
augmented_columns = (0, 1, 2, 4, 5, 6, 8, 9, 13)
assert_equal(
    determinant(
        augmented_u,
        (2, 10, 16, 18, 20, 22, 23, 24, 26),
        augmented_columns,
    ),
    -131072 * kappa**2 * (ell**2 - 1),
)
assert_equal(
    determinant(
        augmented_u,
        (2, 10, 16, 18, 19, 20, 22, 24, 28),
        augmented_columns,
    ),
    -131072 * ell * kappa,
)

# kappa=0 P2 and exact rank-nine cover away from its exceptional line.
p2_substitution = {p: 0, q: 0, kappa: 0, slope: -1}
h_p2 = X * u + Y * v + Z * w
n_p2 = normal(h_p2, p2_substitution)
p2_kernel = (
    u.col_join(sp.zeros(5, 1)),
    v.col_join(sp.zeros(5, 1)),
    w.col_join(sp.zeros(5, 1)),
    unit(13, 11),
)
assert independent(p2_kernel)
assert all(is_zero(n_p2 * vector) for vector in p2_kernel)
p2_columns = (0, 1, 2, 5, 6, 8, 9, 10, 12)
for value, expected in zip(
    (
        determinant(
            n_p2,
            (2, 10, 16, 18, 19, 20, 22, 24, 28),
            p2_columns,
        ),
        determinant(
            n_p2,
            (2, 10, 16, 18, 20, 22, 23, 24, 28),
            p2_columns,
        ),
        determinant(
            n_p2,
            (3, 11, 16, 18, 19, 20, 22, 24, 28),
            p2_columns,
        ),
        determinant(
            n_p2,
            (3, 11, 16, 18, 20, 22, 23, 24, 28),
            p2_columns,
        ),
    ),
    (
        -131072 * X**2 * Y * (-Y + Z * ell),
        -131072 * X**2 * Y * Z,
        -131072 * Y * (-Y + Z * ell) * (Y * ell - Z) ** 2,
        -131072 * Y * Z * (Y * ell - Z) ** 2,
    ),
    strict=True,
):
    assert_equal(value, expected)

# Exceptional line and its direct quadratic p,q forcing.
h_special = v + ell * w
n_special = normal(h_special, p2_substitution)
special_kernel = (
    u.col_join(sp.zeros(5, 1)),
    v.col_join(sp.zeros(5, 1)),
    w.col_join(sp.zeros(5, 1)),
    unit(13, 8),
    unit(13, 9),
    unit(13, 11),
)
assert independent(special_kernel)
assert all(is_zero(n_special * vector) for vector in special_kernel)
assert n_special.extract(range(16), range(13)) == sp.zeros(16, 13)
special_columns = (0, 1, 2, 5, 6, 10, 12)
assert_equal(
    determinant(
        n_special,
        (16, 18, 19, 20, 22, 24, 28),
        special_columns,
    ),
    -8192 * (ell**2 - 1),
)
assert_equal(
    determinant(
        n_special,
        (16, 18, 20, 22, 23, 24, 28),
        special_columns,
    ),
    -8192 * ell,
)
first_extension = A * u + B * v + C * w
expansion = matrix.subs(
    {
        p: tangent * P,
        q: tangent * Q,
        kappa: 0,
        ell: ell + tangent * E,
        slope: -1,
    }
) * (h_special + tangent * first_extension)
assert is_zero(
    sp.Matrix([sp.expand(value).coeff(tangent, 1) for value in expansion])
)
second_force = sp.Matrix(
    [sp.factor(sp.expand(value).coeff(tangent, 2)) for value in expansion]
)
expected_force = sp.zeros(32, 1)
expected_force[2] = -4 * A * P
expected_force[3] = 4 * P * (B * ell - C + E)
expected_force[10] = -4 * A * Q
expected_force[11] = 4 * Q * (B * ell - C + E)
assert is_zero(second_force - expected_force)

# Y=0,Z!=0 kappa crossing.
h_crossing = X * u + Z * w
n_crossing = normal(h_crossing, p2_substitution)
crossing_kernel = (
    u.col_join(sp.zeros(5, 1)),
    v.col_join(sp.zeros(5, 1)),
    w.col_join(sp.zeros(5, 1)),
    unit(13, 10),
    unit(13, 11),
)
assert independent(crossing_kernel)
assert all(is_zero(n_crossing * vector) for vector in crossing_kernel)
crossing_columns = (0, 1, 2, 5, 6, 8, 9, 12)
assert_equal(
    determinant(
        n_crossing,
        (3, 11, 16, 20, 22, 23, 24, 28),
        crossing_columns,
    ),
    -32768 * Z**3,
)
force_kappa_v = (sp.diff(matrix, kappa) * v).subs(p2_substitution)
assert all(force_kappa_v[row] == 0 for row in DIAGONAL_ROWS)
assert_equal(
    determinant(
        n_crossing.row_join(force_kappa_v),
        (3, 11, 16, 18, 20, 22, 23, 24, 28),
        crossing_columns + (13,),
    ),
    131072 * Z**3,
)

# Triple crossing H=u.
n_triple = n_crossing.subs({X: 1, Z: 0})
assert is_zero(n_triple * weight_lift)
assert_equal(
    determinant(
        n_triple,
        (2, 10, 16, 20, 22, 24, 28),
        (0, 1, 2, 5, 6, 8, 9),
    ),
    -16384,
)
force_lambda_v = (sp.diff(matrix, slope) * v).subs(p2_substitution)
force_lambda_w_zero = force_lambda_w.subs(kappa, 0)
for force in (force_kappa_v, force_lambda_v, force_lambda_w_zero):
    assert force[0] == 0 and force[15] == 0
augmented_triple = (
    n_triple.row_join(force_kappa_v)
    .row_join(force_lambda_v)
    .row_join(force_lambda_w_zero)
)
assert_equal(
    determinant(
        augmented_triple,
        (2, 10, 16, 18, 19, 20, 22, 23, 24, 28),
        (0, 1, 2, 5, 6, 8, 9, 13, 14, 15),
    ),
    262144,
)

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; direct six-term permanents",
            "field": "exact characteristic zero",
            "component": 21,
            "stratum": "p=q=0, lambda=-1",
            "kappa_nonzero_second_normal_H22_empty": True,
            "kappa_zero_second_normal_H22_empty": True,
            "exceptional_projective_line": "H=v+ell*w",
            "triple_crossing_force_rank_increment": 3,
            "higher_zero_normals_closed": False,
            "lambda_plus_one_closed": False,
            "arbitrary_order_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
