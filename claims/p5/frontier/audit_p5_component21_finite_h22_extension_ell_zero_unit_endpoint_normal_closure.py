#!/usr/bin/env python3
"""No-import audit of component 21 extension normals at ell=0,+/-1."""

from __future__ import annotations

import itertools
import json

import sympy as sp
import sys
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


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
parameters = (p, q, kappa, ell, slope)
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = stacked_matrix(alpha, beta, slope)


def frozen(leading, substitution):
    return tuple(
        (sp.diff(matrix, parameter) * leading).subs(substitution)
        for parameter in parameters
    )


# ell=0 exact cover and both normals.
ell_zero = matrix.subs(ell, 0)
assert_equal(
    determinant(
        ell_zero, (2, 3, 7, 16, 17, 20, 22, 24), tuple(range(8))
    ),
    256 * p**4 * (slope - 1) ** 5 * (slope + 1) ** 3,
)
assert_equal(
    determinant(
        ell_zero, (2, 3, 16, 18, 20, 22, 24, 26), tuple(range(8))
    ),
    -256 * kappa**2 * p**2 * (slope - 1) ** 8,
)
leading_plus = sp.Matrix((-p, 0, 0, 0, -q, 0, 1, 0))
zero_plus_sub = {ell: 0, slope: 1}
zero_plus_matrix = matrix.subs(zero_plus_sub)
assert is_zero(zero_plus_matrix * leading_plus)
assert_equal(
    determinant(
        zero_plus_matrix,
        (3, 6, 7, 17, 21, 23, 31),
        (0, 1, 2, 3, 4, 5, 7),
    ),
    -16384 * p**5,
)
zero_plus_columns = frozen(leading_plus, zero_plus_sub)
zero_plus_normal = zero_plus_matrix.row_join(zero_plus_columns[4])
assert_equal(
    determinant(
        zero_plus_normal,
        (3, 6, 7, 17, 21, 23, 26),
        (0, 1, 2, 3, 5, 7, 8),
    ),
    8192 * p**5,
)
zero_plus_vectors = (unit(9, 4), -p * unit(9, 0) + unit(9, 6))
assert all(
    is_zero(zero_plus_normal.extract(MIXED_ROWS, range(9)) * vector)
    for vector in zero_plus_vectors
)
assert diagonal_images(zero_plus_normal, zero_plus_vectors) == (
    (0, 0, 0, 4),
    (0, 0, 0, 4 * q),
)

leading_zero_minus = sp.Matrix((0, -1, 0, 0, 1, 0, 0, 0))
zero_minus_sub = {ell: 0, kappa: 0, slope: -1}
zero_minus_matrix = matrix.subs(zero_minus_sub)
assert is_zero(zero_minus_matrix * leading_zero_minus)
assert_equal(
    determinant(
        zero_minus_matrix,
        (2, 3, 16, 20, 22, 24, 28),
        (0, 1, 2, 3, 5, 6, 7),
    ),
    -16384 * p**2,
)
zero_minus_columns = frozen(leading_zero_minus, zero_minus_sub)
zero_minus_normal = zero_minus_matrix.row_join(
    zero_minus_columns[2]
).row_join(zero_minus_columns[4])
assert_equal(
    determinant(
        zero_minus_normal,
        (2, 3, 18, 19, 20, 22, 24, 28),
        (1, 2, 3, 5, 6, 7, 8, 9),
    ),
    32768 * p**2,
)
zero_minus_vectors = (
    unit(10, 0),
    leading_zero_minus.col_join(sp.zeros(2, 1)),
)
assert all(
    is_zero(zero_minus_normal.extract(MIXED_ROWS, range(10)) * vector)
    for vector in zero_minus_vectors
)
assert diagonal_images(zero_minus_normal, zero_minus_vectors) == (
    (0, 0, 4, 0),
    (0, 0, 0, 0),
)

X, Y = sp.symbols("X Y")
endpoint_summary = {}
for epsilon in (1, -1):
    endpoint = matrix.subs(ell, epsilon)
    assert_equal(
        determinant(
            endpoint, (6, 7, 16, 17, 18, 20, 21, 24), tuple(range(8))
        ),
        -256
        * epsilon
        * p**4
        * (slope - 1) ** 4
        * (slope + 1) ** 4,
    )
    second = determinant(
        endpoint, (2, 3, 7, 16, 18, 20, 22, 24), tuple(range(8))
    )
    expected_second = (
        1024 * slope**2 * kappa * p**3 * (slope - 1) ** 6
        if epsilon == 1
        else -1024 * kappa * p**3 * (slope - 1) ** 6
    )
    assert_equal(second, expected_second)

    plus_sub = {ell: epsilon, slope: 1}
    plus_matrix = matrix.subs(plus_sub)
    endpoint_vector = sp.Matrix(
        (0, -epsilon, -epsilon, 0, -epsilon, -1, 0, 1)
    )
    assert is_zero(plus_matrix * leading_plus)
    assert is_zero(plus_matrix * endpoint_vector)
    assert_equal(
        determinant(
            plus_matrix,
            (2, 3, 7, 21, 23, 31),
            (0, 1, 2, 3, 4, 5),
        ),
        4096 * epsilon * p**4,
    )
    leading = X * leading_plus + Y * endpoint_vector
    normal = plus_matrix
    for column in frozen(leading, plus_sub):
        normal = normal.row_join(column)
    assert_equal(
        determinant(
            normal,
            (2, 3, 7, 17, 20, 21, 23),
            (0, 1, 2, 3, 5, 11, 12),
        ),
        16384 * epsilon * Y**2 * p**5,
    )
    generic_vectors = (
        unit(13, 4),
        -p * unit(13, 0) + unit(13, 6),
        -epsilon * unit(13, 1)
        - epsilon * unit(13, 2)
        - unit(13, 5)
        + unit(13, 7),
        -X * unit(13, 0) + unit(13, 8),
        unit(13, 9),
        unit(13, 10),
    )
    mixed = normal.extract(MIXED_ROWS, range(13))
    assert all(is_zero(mixed * vector) for vector in generic_vectors)
    assert all(
        row[:3] == (0, 0, 0)
        for row in diagonal_images(normal, generic_vectors)
    )

    pure = normal.subs({X: 1, Y: 0})
    assert_equal(
        determinant(
            pure,
            (2, 3, 7, 21, 23, 24),
            (0, 1, 2, 3, 5, 12),
        ),
        -2048 * epsilon * p**4 * q,
    )
    assert_equal(
        determinant(
            pure,
            (2, 3, 7, 21, 23, 26),
            (0, 1, 2, 3, 5, 12),
        ),
        2048 * p**4 * (kappa * q + epsilon),
    )
    pure_vectors = tuple(
        vector.subs({X: 1, Y: 0}) for vector in generic_vectors
    ) + (unit(13, 11),)
    assert all(
        is_zero(pure.extract(MIXED_ROWS, range(13)) * vector)
        for vector in pure_vectors
    )
    assert all(
        row[:3] == (0, 0, 0)
        for row in diagonal_images(pure, pure_vectors)
    )

    minus_sub = {ell: epsilon, kappa: 0, slope: -1}
    minus_matrix = matrix.subs(minus_sub)
    minus_vector = sp.Matrix(
        (0, -epsilon, 0, 0, epsilon, 0, 0, 1)
    )
    assert is_zero(minus_matrix * minus_vector)
    assert_equal(
        determinant(
            minus_matrix,
            (2, 3, 7, 16, 18, 20, 24),
            (0, 1, 2, 3, 4, 5, 6),
        ),
        16384 * epsilon * p**3,
    )
    minus_columns = frozen(minus_vector, minus_sub)
    minus_normal = minus_matrix.row_join(minus_columns[2]).row_join(
        minus_columns[4]
    )
    assert_equal(
        determinant(
            minus_normal,
            (2, 3, 7, 18, 20, 22, 23, 24),
            (1, 2, 3, 4, 5, 6, 8, 9),
        ),
        32768 * epsilon * p**3,
    )
    minus_vectors = (unit(10, 0), minus_vector.col_join(sp.zeros(2, 1)))
    assert all(
        is_zero(minus_normal.extract(MIXED_ROWS, range(10)) * vector)
        for vector in minus_vectors
    )
    assert diagonal_images(minus_normal, minus_vectors) == (
        (0, 0, 4, 0),
        (0, 0, 0, 0),
    )
    endpoint_summary[str(epsilon)] = "all projective kernel normals closed"

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; direct six-term permanents",
            "field": "exact characteristic zero",
            "component": 21,
            "divisors": ["ell=0", "ell=1", "ell=-1"],
            "open_condition": "p != 0",
            "rank_drop_locus": ["lambda=1", "kappa=0, lambda=-1"],
            "unit_endpoint_kernel_normals": endpoint_summary,
            "p_zero_closed": False,
            "higher_normals_closed": False,
            "arbitrary_order_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
