#!/usr/bin/env python3
"""No-import audit of the component-21 ordinary-weight second normal."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))


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


p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
extension = sp.symbols("z0:8")
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = stacked_matrix(alpha, beta, slope)
zero_matrix = matrix.subs({p: 0, q: 0})
kernel = sp.Matrix((0, 0, 0, 1 - slope, 0, 0, slope + 1, 0))
assert is_zero(zero_matrix * kernel)

normal = zero_matrix
for parameter in (p, q, kappa, ell, slope):
    normal = normal.row_join(
        (sp.diff(matrix, parameter) * kernel).subs({p: 0, q: 0})
    )

first_kernel = (
    kernel.col_join(sp.zeros(5, 1)),
    unit(13, 10),
    unit(13, 11),
    -2 * unit(13, 3) + (slope + 1) * unit(13, 12),
)
assert all(is_zero(normal * vector) for vector in first_kernel)
assert sp.Matrix.hstack(*first_kernel).rank() == 4

columns = (0, 1, 2, 3, 4, 5, 7, 8, 9)
assert_equal(
    determinant(
        normal,
        (6, 14, 18, 19, 20, 23, 24, 27, 28),
        columns,
    ),
    512
    * ell
    * (slope - 1) ** 5
    * (slope + 1) ** 6
    * (ell**2 - 1),
)
factor_b = slope * ell + slope + ell - 1
assert_equal(
    determinant(
        normal,
        (2, 10, 19, 20, 22, 23, 24, 27, 28),
        columns,
    ),
    512
    * (slope - 1) ** 5
    * (slope + 1) ** 4
    * (ell**2 - 1)
    * factor_b**2,
)
assert_equal(
    determinant(
        normal,
        (6, 14, 18, 19, 20, 22, 23, 24, 28),
        columns,
    ),
    512 * ell * kappa * (slope - 1) ** 6 * (slope + 1) ** 5,
)
assert_equal(
    determinant(
        normal.subs({kappa: 0, ell: 1}),
        (6, 14, 16, 18, 19, 20, 23, 24, 28),
        columns,
    ),
    -512 * (slope - 1) ** 6 * (slope + 1) ** 5,
)
assert_equal(
    determinant(
        normal.subs({kappa: 0, ell: -1}),
        (2, 10, 16, 18, 19, 20, 23, 24, 28),
        columns,
    ),
    2048 * (slope - 1) ** 6 * (slope + 1) ** 3,
)

dp_column = (sp.diff(matrix, p) * kernel).subs({p: 0, q: 0})
dq_column = (sp.diff(matrix, q) * kernel).subs({p: 0, q: 0})
second = zero_matrix.row_join(dp_column).row_join(dq_column)
assert second.row(0) == sp.zeros(1, 10)
assert second.row(15) == sp.zeros(1, 10)
assert is_zero(second * kernel.col_join(sp.zeros(2, 1)))

dkappa_column = (sp.diff(matrix, kappa) * kernel).subs({p: 0, q: 0})
dell_column = (sp.diff(matrix, ell) * kernel).subs({p: 0, q: 0})
dslope_column = (sp.diff(matrix, slope) * kernel).subs({p: 0, q: 0})
assert is_zero(dkappa_column)
assert is_zero(dell_column)
assert is_zero((slope + 1) * dslope_column - 2 * zero_matrix.col(3))

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; direct six-term permanents",
            "field": "exact characteristic zero",
            "component": 21,
            "stratum": "p=q=0, finite lambda not equal to +/-1",
            "exact_zero_family": True,
            "complete_first_normal_rank": 9,
            "complete_first_normal_kernel_dimension": 4,
            "complete_second_normal_rank": 9,
            "complete_second_normal_kernel_dimension": 1,
            "D01_diagonal_rows_identically_zero": True,
            "second_normal_H22_incidence_empty": True,
            "higher_zero_normals_closed": False,
            "arbitrary_order_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
