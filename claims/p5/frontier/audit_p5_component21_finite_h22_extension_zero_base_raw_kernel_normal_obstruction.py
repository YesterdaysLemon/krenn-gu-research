#!/usr/bin/env python3
"""No-import audit of raw zero-base component-21 extension normals."""

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
    return sp.factor(matrix.extract(rows, columns).det())


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero(vector):
    return all(sp.expand(value) == 0 for value in vector)


def unit(length, index):
    return sp.eye(length).col(index)


p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
X, Y, Z, T = sp.symbols("X Y Z T")
parameters = (p, q, kappa, ell, slope)
alpha, beta = finite_bases(p, q, kappa, ell)
matrix = stacked_matrix(alpha, beta, slope)
zero_matrix = matrix.subs({p: 0, q: 0})


def normal(leading, substitution):
    output = matrix.subs(substitution)
    for parameter in parameters:
        output = output.row_join(
            (sp.diff(matrix, parameter) * leading).subs(substitution)
        )
    return output


# Ordinary-weight kernel and rank cover.
ordinary_kernel = sp.Matrix((0, 0, 0, 1 - slope, 0, 0, slope + 1, 0))
assert is_zero(zero_matrix * ordinary_kernel)
assert_equal(
    determinant(
        zero_matrix,
        (16, 19, 20, 22, 23, 24, 27),
        (0, 1, 2, 3, 4, 5, 7),
    ),
    -128 * (slope - 1) ** 3 * (slope + 1) ** 4 * (ell**2 - 1),
)
assert_equal(
    determinant(
        zero_matrix,
        (16, 18, 19, 20, 23, 24, 28),
        (0, 1, 2, 3, 4, 5, 7),
    ),
    -128 * ell * (slope - 1) ** 4 * (slope + 1) ** 3,
)
ordinary_normal = normal(ordinary_kernel, {p: 0, q: 0})
assert ordinary_normal.row(0) == sp.zeros(1, 13)
assert ordinary_normal.row(15) == sp.zeros(1, 13)
assert_equal(
    determinant(
        ordinary_normal,
        (6, 14, 18, 19, 20, 23, 24, 27, 28),
        (0, 1, 2, 3, 4, 5, 7, 8, 9),
    ),
    512
    * ell
    * (slope - 1) ** 5
    * (slope + 1) ** 6
    * (ell**2 - 1),
)
for epsilon in (1, -1):
    specialized = ordinary_normal.subs({kappa: 0, ell: epsilon})
    assert_equal(
        determinant(
            specialized,
            (6, 14, 18, 19, 20, 23, 24, 28),
            (0, 1, 2, 3, 4, 5, 8, 9),
        ),
        -256 * epsilon * (slope - 1) ** 5 * (slope + 1) ** 5,
    )

# lambda=-1 exact kernel strata and identically absent D01 diagonals.
minus_matrix = zero_matrix.subs(slope, -1)
assert is_zero(minus_matrix * unit(8, 3))
assert is_zero(minus_matrix * unit(8, 7))
assert_equal(
    determinant(
        minus_matrix,
        (16, 18, 20, 22, 24, 28),
        (0, 1, 2, 4, 5, 6),
    ),
    -4096 * kappa,
)
minus_leading = X * unit(8, 3) + Y * unit(8, 7)
minus_normal = normal(minus_leading, {p: 0, q: 0, slope: -1})
assert minus_normal.row(0) == sp.zeros(1, 13)
assert minus_normal.row(15) == sp.zeros(1, 13)
assert_equal(
    determinant(
        minus_normal,
        (3, 11, 18, 20, 22, 23, 24, 26, 28),
        (0, 1, 2, 4, 5, 6, 8, 9, 12),
    ),
    -131072 * Y**3 * kappa**2,
)
assert_equal(
    determinant(
        minus_normal.subs({X: 1, Y: 0}),
        (2, 10, 18, 20, 22, 24, 26, 28),
        (0, 1, 2, 4, 5, 6, 8, 9),
    ),
    65536 * kappa**2,
)

middle_minus = -unit(8, 1) + unit(8, 4)
minus_zero = minus_matrix.subs(kappa, 0)
assert is_zero(minus_zero * middle_minus)
assert_equal(
    determinant(
        minus_zero,
        (16, 20, 22, 24, 28),
        (0, 1, 2, 5, 6),
    ),
    -1024,
)
minus_zero_leading = X * unit(8, 3) + Y * middle_minus + Z * unit(8, 7)
minus_zero_normal = normal(
    minus_zero_leading, {p: 0, q: 0, kappa: 0, slope: -1}
)
assert minus_zero_normal.row(0) == sp.zeros(1, 13)
assert minus_zero_normal.row(15) == sp.zeros(1, 13)

# lambda=1 kernel P2/P3 and exact mixed-row forcing of D23(0000).
plus_matrix = zero_matrix.subs(slope, 1)
plus_basis = (
    unit(8, 2),
    -unit(8, 0) + ell * unit(8, 4) + unit(8, 5),
    unit(8, 6),
)
assert all(is_zero(plus_matrix * vector) for vector in plus_basis)
assert_equal(
    determinant(
        plus_matrix,
        (19, 22, 23, 27, 31),
        (0, 1, 3, 4, 7),
    ),
    -1024 * (ell**2 - 1),
)
plus_leading = X * plus_basis[0] + Y * plus_basis[1] + Z * plus_basis[2]
plus_normal = normal(plus_leading, {p: 0, q: 0, slope: 1})
for row, coefficient in (
    (16, 2 * (ell * X + Y)),
    (20, 2 * X),
    (28, -2 * Y),
):
    expected = sp.zeros(1, 13)
    expected[0, 12] = coefficient
    assert plus_normal.row(row) == expected

endpoint_summary = {}
for epsilon in (1, -1):
    endpoint_matrix = plus_matrix.subs(ell, epsilon)
    endpoint_vector = -unit(8, 0) - epsilon * unit(8, 1) + unit(8, 7)
    assert is_zero(endpoint_matrix * endpoint_vector)
    assert_equal(
        determinant(
            endpoint_matrix,
            (18, 19, 23, 31),
            (0, 1, 3, 4),
        ),
        -256 * epsilon,
    )
    endpoint_leading = (
        X * plus_basis[0].subs(ell, epsilon)
        + Y * plus_basis[1].subs(ell, epsilon)
        + Z * plus_basis[2]
        + T * endpoint_vector
    )
    endpoint_normal = normal(
        endpoint_leading, {p: 0, q: 0, ell: epsilon, slope: 1}
    )
    for row, coefficient in (
        (16, 2 * (T + epsilon * X + Y)),
        (20, 2 * X),
        (28, -2 * Y),
        (24, 2 * epsilon * (T - epsilon * X - Y)),
    ):
        expected = sp.zeros(1, 13)
        expected[0, 12] = coefficient
        assert endpoint_normal.row(row) == expected
    endpoint_summary[str(epsilon)] = "P3 directions forced D23(0000)=0"

print(
    json.dumps(
        {
            "status": "PASS",
            "method": "no repository imports; direct six-term permanents",
            "field": "exact characteristic zero",
            "component": 21,
            "base": "p=q=0 raw displayed chart",
            "ordinary_extension_rank": 7,
            "lambda_minus_1_ranks": {"kappa_nonzero": 6, "kappa_zero": 5},
            "lambda_plus_1_ranks": {"ell_nonendpoint": 5, "endpoints": 4},
            "lambda_plus_1_endpoint_normals": endpoint_summary,
            "existing_pq_blowup_reproved": False,
            "higher_zero_normals_closed": False,
            "arbitrary_order_closed": False,
            "finite_field_proof_used": False,
            "global_conjecture_resolved": False,
        },
        indent=2,
    )
)
