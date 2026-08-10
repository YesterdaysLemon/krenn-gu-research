#!/usr/bin/env python3
"""No-import audit of component 21 extension normals on p=0,q!=0."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_ROWS = tuple(range(1, 15)) + tuple(range(17, 31))
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
    alpha_rows = tuple(project(row, direction, slope) for row in alpha)
    beta_rows = tuple(project(row, direction, slope) for row in beta)
    output = []
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index]
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
    return sp.factor(
        sp.polys.matrices.DomainMatrix.from_Matrix(
            matrix.extract(rows, columns)
        )
        .det()
        .as_expr()
    )


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero(vector):
    return all(sp.expand(value) == 0 for value in vector)


def unit(length, index):
    return sp.eye(length).col(index)


def diagonal_images(normal, vectors):
    return tuple(
        tuple(
            sp.factor(value)
            for value in normal.extract(DIAGONAL_ROWS, range(normal.cols)) * vector
        )
        for vector in vectors
    )


p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
X, Y = sp.symbols("X Y")
parameters = (p, q, kappa, ell, slope)
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = stacked_matrix(alpha, beta, slope)
divisor = matrix.subs(p, 0)


def frozen(leading, substitution):
    return tuple(
        (sp.diff(matrix, parameter) * leading).subs(substitution)
        for parameter in parameters
    )


factor_a = (ell + 1) * slope - ell + 1
factor_b = (ell + 1) * slope + ell - 1
rank_checks = (
    (
        (11, 14, 15, 16, 18, 19, 20, 24),
        256
        * ell
        * q**3
        * (slope - 1) ** 5
        * (slope + 1) ** 2
        * (ell**2 - 1)
        * factor_a,
    ),
    (
        (10, 11, 16, 18, 19, 20, 23, 24),
        -256
        * ell
        * q**2
        * (slope - 1) ** 5
        * (slope + 1) ** 2
        * (ell**2 - 1)
        * factor_b,
    ),
    (
        (10, 11, 15, 16, 18, 20, 22, 24),
        256
        * kappa
        * q**3
        * (slope - 1) ** 6
        * factor_a
        * factor_b,
    ),
)
for rows, expected in rank_checks:
    assert_equal(determinant(divisor, rows, tuple(range(8))), expected)

ell_zero = divisor.subs(ell, 0)
assert_equal(
    determinant(
        ell_zero, (10, 11, 15, 16, 19, 20, 22, 24), tuple(range(8))
    ),
    256 * q**3 * (slope - 1) ** 6 * (slope + 1) ** 2,
)
assert_equal(
    determinant(
        ell_zero, (10, 11, 16, 18, 20, 22, 24, 26), tuple(range(8))
    ),
    -256 * kappa**2 * q**2 * (slope - 1) ** 8,
)

leading_plus = sp.Matrix((0, 0, 0, 0, -q, 0, 1, 0))
plus_sub = {p: 0, slope: 1}
plus_matrix = matrix.subs(plus_sub)
plus_columns = frozen(leading_plus, plus_sub)
plus_normal = plus_matrix.row_join(plus_columns[4])
assert is_zero(plus_matrix * leading_plus)
assert_equal(
    determinant(
        plus_matrix,
        (10, 11, 15, 23, 25, 29, 31),
        (0, 1, 2, 3, 4, 5, 7),
    ),
    -16384 * ell * q**5 * (ell**2 - 1),
)
assert_equal(
    determinant(
        plus_normal,
        (10, 11, 18, 23, 25, 29),
        (0, 1, 2, 3, 7, 8),
    ),
    2048 * ell**2 * q**4 * (ell**2 - 1),
)
plus_vectors = (
    unit(9, 4),
    -unit(9, 0) + ell * unit(9, 2) + unit(9, 5),
    unit(9, 6),
)
assert all(
    is_zero(plus_normal.extract(MIXED_ROWS, range(9)) * vector)
    for vector in plus_vectors
)
assert all(
    row[0] == 0 and row[2] == 0
    for row in diagonal_images(plus_normal, plus_vectors)
)

assert_equal(
    determinant(
        plus_matrix.subs(ell, 0),
        (11, 14, 15, 23, 25, 29, 31),
        (0, 1, 2, 3, 4, 5, 7),
    ),
    -16384 * q**5,
)
assert_equal(
    determinant(
        plus_normal.subs(ell, 0),
        (11, 14, 22, 23, 25, 29),
        (0, 1, 2, 3, 7, 8),
    ),
    2048 * q**4,
)

endpoint_summary = {}
for epsilon in (1, -1):
    endpoint = divisor.subs(ell, epsilon)
    assert_equal(
        determinant(
            endpoint, (14, 15, 16, 18, 19, 20, 23, 24), tuple(range(8))
        ),
        -256 * q**2 * (slope - 1) ** 5 * (slope + 1) ** 3,
    )
    second = determinant(
        endpoint, (10, 11, 15, 16, 18, 20, 22, 24), tuple(range(8))
    )
    expected = (
        1024 * slope**2 * kappa * q**3 * (slope - 1) ** 6
        if epsilon == 1
        else -1024 * kappa * q**3 * (slope - 1) ** 6
    )
    assert_equal(second, expected)

    plus_endpoint_sub = {p: 0, ell: epsilon, slope: 1}
    endpoint_matrix = matrix.subs(plus_endpoint_sub)
    endpoint_vector = sp.Matrix(
        (0, -epsilon, -epsilon, 0, -epsilon, -1, 0, 1)
    )
    assert is_zero(endpoint_matrix * leading_plus)
    assert is_zero(endpoint_matrix * endpoint_vector)
    assert_equal(
        determinant(
            endpoint_matrix,
            (10, 11, 15, 23, 29, 31),
            (0, 1, 2, 3, 4, 5),
        ),
        -4096 * epsilon * q**4,
    )
    leading = X * leading_plus + Y * endpoint_vector
    normal = endpoint_matrix
    for column in frozen(leading, plus_endpoint_sub):
        normal = normal.row_join(column)
    assert_equal(
        determinant(
            normal,
            (10, 11, 20, 23, 25, 29),
            (0, 1, 2, 3, 11, 12),
        ),
        -4096 * epsilon * Y**2 * q**4,
    )
    vectors = (
        unit(13, 4),
        -unit(13, 0) + epsilon * unit(13, 2) + unit(13, 5),
        unit(13, 6),
        -unit(13, 0) - epsilon * unit(13, 1) + unit(13, 7),
        -X * unit(13, 0) + unit(13, 8),
        unit(13, 9),
        unit(13, 10),
    )
    assert all(
        is_zero(normal.extract(MIXED_ROWS, range(13)) * vector)
        for vector in vectors
    )
    assert all(
        row[0] == 0 and row[2] == 0
        for row in diagonal_images(normal, vectors)
    )
    pure = normal.subs({X: 1, Y: 0})
    assert_equal(
        determinant(
            pure, (10, 11, 18, 23, 29), (0, 1, 2, 3, 12)
        ),
        512 * q**3,
    )
    pure_vectors = tuple(vector.subs({X: 1, Y: 0}) for vector in vectors) + (
        unit(13, 11),
    )
    assert all(
        is_zero(pure.extract(MIXED_ROWS, range(13)) * vector)
        for vector in pure_vectors
    )
    assert all(
        row[0] == 0 and row[2] == 0
        for row in diagonal_images(pure, pure_vectors)
    )
    endpoint_summary[str(epsilon)] = "kernel-plane normals closed"

leading_minus = sp.Matrix((0, -1 / ell, 0, 0, 1 / ell, 0, 0, 1))
minus_sub = {p: 0, kappa: 0, slope: -1}
minus_matrix = matrix.subs(minus_sub)
assert is_zero(minus_matrix * leading_minus)
assert_equal(
    determinant(
        minus_matrix,
        (10, 11, 15, 16, 18, 20, 24),
        (0, 1, 2, 3, 4, 5, 6),
    ),
    16384 * ell**3 * q**3,
)
minus_columns = frozen(leading_minus, minus_sub)
minus_normal = minus_matrix.row_join(minus_columns[2]).row_join(minus_columns[4])
assert_equal(
    determinant(
        minus_normal,
        (10, 11, 18, 19, 20, 22, 24, 28),
        (1, 2, 3, 4, 5, 6, 8, 9),
    ),
    32768 * q**2 * (ell**2 - 1) / ell,
)
minus_vectors = (unit(10, 0), leading_minus.col_join(sp.zeros(2, 1)))
assert all(
    is_zero(minus_normal.extract(MIXED_ROWS, range(10)) * vector)
    for vector in minus_vectors
)
assert diagonal_images(minus_normal, minus_vectors) == (
    (0, 0, 4, 0),
    (0, 0, 0, 0),
)

zero_minus_vector = sp.Matrix((0, -1, 0, 0, 1, 0, 0, 0))
zero_minus_sub = {p: 0, ell: 0, kappa: 0, slope: -1}
zero_minus_matrix = matrix.subs(zero_minus_sub)
zero_minus_columns = frozen(zero_minus_vector, zero_minus_sub)
zero_minus_normal = zero_minus_matrix.row_join(zero_minus_columns[2]).row_join(
    zero_minus_columns[4]
)
assert_equal(
    determinant(
        zero_minus_matrix,
        (10, 11, 16, 20, 22, 24, 28),
        (0, 1, 2, 3, 5, 6, 7),
    ),
    -16384 * q**2,
)
assert_equal(
    determinant(
        zero_minus_normal,
        (10, 11, 18, 19, 20, 22, 24, 28),
        (1, 2, 3, 5, 6, 7, 8, 9),
    ),
    32768 * q**2,
)

for epsilon in (1, -1):
    vector = sp.Matrix((0, -epsilon, 0, 0, epsilon, 0, 0, 1))
    substitution = {p: 0, ell: epsilon, kappa: 0, slope: -1}
    endpoint_matrix = matrix.subs(substitution)
    columns = frozen(vector, substitution)
    normal = endpoint_matrix.row_join(columns[2]).row_join(columns[4])
    assert_equal(
        determinant(
            endpoint_matrix,
            (10, 11, 15, 16, 18, 20, 24),
            (0, 1, 2, 3, 4, 5, 6),
        ),
        16384 * epsilon * q**3,
    )
    assert_equal(
        determinant(
            normal,
            (10, 11, 18, 20, 22, 23, 24, 28),
            (1, 2, 3, 4, 5, 6, 8, 9),
        ),
        32768 * q**2,
    )

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; direct six-term permanents",
            "field": "exact characteristic zero",
            "component": 21,
            "divisor": "p=0, q!=0",
            "rank_drop_locus": ["lambda=1", "kappa=0, lambda=-1"],
            "unit_endpoint_kernel_planes": endpoint_summary,
            "zero_base_closed": False,
            "higher_normals_closed": False,
            "arbitrary_order_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
