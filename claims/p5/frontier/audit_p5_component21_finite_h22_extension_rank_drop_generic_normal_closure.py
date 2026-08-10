#!/usr/bin/env python3
"""No-import audit of the generic component-21 finite-H22 rank-drop normals."""

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


def unit_vector(length, index):
    return sp.eye(length).col(index)


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero_vector(vector):
    return all(sp.expand(value) == 0 for value in vector)


p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = stacked_matrix(alpha, beta, slope)
factor_a = (ell + 1) * slope - ell + 1
factor_b = (ell + 1) * slope + ell - 1

map_rows = (
    (2, 3, 16, 17, 18, 20, 21, 24),
    (3, 6, 7, 16, 17, 18, 20, 24),
    (2, 3, 7, 16, 18, 20, 22, 24),
)
map_minors = tuple(
    determinant(matrix, rows, tuple(range(8))) for rows in map_rows
)
expected_map_minors = (
    -256
    * ell**2
    * p**4
    * (slope - 1) ** 4
    * (slope + 1) ** 3
    * (ell**2 - 1)
    * factor_b,
    -256
    * ell
    * p**4
    * (slope - 1) ** 4
    * (slope + 1) ** 3
    * (ell**2 - 1)
    * factor_a,
    256
    * kappa
    * p**3
    * (slope - 1) ** 6
    * factor_a
    * factor_b,
)
for actual, expected in zip(map_minors, expected_map_minors, strict=True):
    assert_equal(actual, expected)
assert sp.expand(factor_b - factor_a) == 2 * (ell - 1)

plus_kernel = sp.Matrix((-p, 0, 0, 0, -q, 0, 1, 0))
plus_matrix = matrix.subs(slope, 1)
assert is_zero_vector(plus_matrix * plus_kernel)
assert_equal(determinant(
    plus_matrix,
    (2, 3, 7, 17, 21, 23, 31),
    (0, 1, 2, 3, 4, 5, 7),
), -16384 * ell * p**5 * (ell**2 - 1))
plus_transverse = sp.diff(matrix * plus_kernel, slope).subs(slope, 1)
plus_normal = plus_matrix.row_join(plus_transverse)
plus_mixed = plus_normal.extract(MIXED_ROWS, tuple(range(9)))
assert_equal(determinant(
    plus_normal,
    (2, 3, 7, 17, 21, 23, 24),
    (0, 1, 2, 3, 5, 7, 8),
), -8192 * ell * p**5 * q * (ell**2 - 1))
assert_equal(determinant(
    plus_normal,
    (2, 3, 7, 17, 21, 23, 26),
    (0, 1, 2, 3, 5, 7, 8),
), 8192 * ell * p**5 * (ell**2 - 1) * (ell * kappa * q + 1))
plus_vectors = (
    unit_vector(9, 4),
    -p * unit_vector(9, 0) + unit_vector(9, 6),
)
assert all(is_zero_vector(plus_mixed * vector) for vector in plus_vectors)
assert tuple(
    tuple(
        sp.factor(value)
        for value in plus_normal.extract(DIAGONAL_ROWS, tuple(range(9))) * vector
    )
    for vector in plus_vectors
) == ((0, 0, 0, 4), (0, 0, 0, 4 * q))

minus_kernel = sp.Matrix((0, -1 / ell, 0, 0, 1 / ell, 0, 0, 1))
minus_centre = {kappa: 0, slope: -1}
minus_matrix = matrix.subs(minus_centre)
assert is_zero_vector(minus_matrix * minus_kernel)
assert_equal(determinant(
    minus_matrix,
    (2, 3, 7, 16, 18, 20, 24),
    (0, 1, 2, 3, 4, 5, 6),
), 16384 * ell**3 * p**3)
minus_normal = (
    minus_matrix.row_join(
        sp.diff(matrix * minus_kernel, kappa).subs(minus_centre)
    ).row_join(sp.diff(matrix * minus_kernel, slope).subs(minus_centre))
)
minus_mixed = minus_normal.extract(MIXED_ROWS, tuple(range(10)))
assert_equal(determinant(
    minus_normal,
    (2, 3, 7, 18, 19, 20, 22, 24),
    (1, 2, 3, 4, 5, 6, 8, 9),
), 32768 * p**3 * (ell**2 - 1))
minus_vectors = (unit_vector(10, 0), minus_kernel.col_join(sp.zeros(2, 1)))
assert all(is_zero_vector(minus_mixed * vector) for vector in minus_vectors)
assert tuple(
    tuple(
        sp.factor(value)
        for value in minus_normal.extract(DIAGONAL_ROWS, tuple(range(10))) * vector
    )
    for vector in minus_vectors
) == ((0, 0, 4, 0), (0, 0, 0, 0))

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; direct six-term three-row permanents",
            "field": "exact characteristic zero",
            "component": 21,
            "open_chart": "p*ell*(ell^2-1) != 0",
            "rank_drop_locus": ["lambda=1", "kappa=0, lambda=-1"],
            "plus_kernel": [str(value) for value in plus_kernel],
            "minus_kernel": [str(value) for value in minus_kernel],
            "plus_diagonal_image": [[0, 0, 0, 4], [0, 0, 0, "4*q"]],
            "minus_diagonal_image": [[0, 0, 4, 0], [0, 0, 0, 0]],
            "omitted_divisors_closed": False,
            "arbitrary_order_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
