#!/usr/bin/env python3
"""Verify raw zero-base component-21 finite-H22 extension normals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_FINITE_H22_EXTENSION_ZERO_BASE_RAW_KERNEL_NORMAL_OBSTRUCTION.md"
MIXED_ROWS = tuple(range(1, 15)) + tuple(range(17, 31))
DIAGONAL_ROWS = (0, 15, 16, 31)


def determinant(matrix, rows, columns):
    return sp.factor(matrix.extract(rows, columns).det())


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero(vector):
    return all(sp.expand(value) == 0 for value in vector)


def unit(length, index):
    return sp.eye(length).col(index)


def frozen_normal(matrix, leading, parameters, substitution):
    normal = matrix.subs(substitution)
    for parameter in parameters:
        normal = normal.row_join(
            (sp.diff(matrix, parameter) * leading).subs(substitution)
        )
    return normal


def main() -> None:
    p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
    x, y, zeta, tau = sp.symbols("X Y Z T")
    extension = sp.symbols("z0:8")
    parameters = (p, q, kappa, ell, slope)
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )
    zero_matrix = matrix.subs({p: 0, q: 0})

    # Ordinary weights: exact rank seven and kernel line.
    ordinary_kernel = sp.Matrix(
        (0, 0, 0, 1 - slope, 0, 0, slope + 1, 0)
    )
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

    ordinary_normal = frozen_normal(
        matrix, ordinary_kernel, parameters, {p: 0, q: 0}
    )
    assert ordinary_normal.row(0) == sp.zeros(1, 13)
    assert ordinary_normal.row(15) == sp.zeros(1, 13)

    # Mixed rank nine away from kappa=0,ell=+/-1.
    rank9_nonzero_nonendpoint = determinant(
        ordinary_normal,
        (6, 14, 18, 19, 20, 23, 24, 27, 28),
        (0, 1, 2, 3, 4, 5, 7, 8, 9),
    )
    assert_equal(
        rank9_nonzero_nonendpoint,
        512
        * ell
        * (slope - 1) ** 5
        * (slope + 1) ** 6
        * (ell**2 - 1),
    )
    rank9_ell_zero = determinant(
        ordinary_normal,
        (2, 10, 19, 20, 22, 23, 24, 27, 28),
        (0, 1, 2, 3, 4, 5, 7, 8, 9),
    )
    factor_b = slope * ell + slope + ell - 1
    assert_equal(
        rank9_ell_zero,
        512
        * (slope - 1) ** 5
        * (slope + 1) ** 4
        * (ell**2 - 1)
        * factor_b**2,
    )
    rank9_endpoint_kappa = determinant(
        ordinary_normal,
        (6, 14, 18, 19, 20, 22, 23, 24, 28),
        (0, 1, 2, 3, 4, 5, 7, 8, 9),
    )
    assert_equal(
        rank9_endpoint_kappa,
        512 * ell * kappa * (slope - 1) ** 6 * (slope + 1) ** 5,
    )

    ordinary_mixed = ordinary_normal.extract(MIXED_ROWS, range(13))
    ordinary_vectors = (
        ordinary_kernel.col_join(sp.zeros(5, 1)),
        unit(13, 10),
        unit(13, 11),
        -2 * unit(13, 3) + (slope + 1) * unit(13, 12),
    )
    assert all(is_zero(ordinary_mixed * vector) for vector in ordinary_vectors)

    exceptional_ordinary = {}
    for epsilon in (1, -1):
        specialized = ordinary_normal.subs({kappa: 0, ell: epsilon})
        assert_equal(
            determinant(
                specialized,
                (6, 14, 18, 19, 20, 23, 24, 28),
                (0, 1, 2, 3, 4, 5, 8, 9),
            ),
            -256
            * epsilon
            * (slope - 1) ** 5
            * (slope + 1) ** 5,
        )
        extra = (
            -unit(13, 0)
            - epsilon * unit(13, 1)
            + epsilon * unit(13, 4)
            + unit(13, 7)
        )
        assert is_zero(
            specialized.extract(MIXED_ROWS, range(13)) * extra
        )
        diagonal = specialized.extract(DIAGONAL_ROWS, range(13)) * extra
        expected = sp.Matrix(
            (0, 0, 2 * (slope - 1), 2 * epsilon * (slope + 1))
        )
        assert is_zero(diagonal - expected)
        exceptional_ordinary[str(epsilon)] = {
            "mixed_rank": 8,
            "extra_diagonal_image": [str(value) for value in expected],
        }

    # lambda=-1, kappa nonzero: rank six, kernel plane and normal directions.
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
    minus_leading = x * unit(8, 3) + y * unit(8, 7)
    minus_normal = frozen_normal(
        matrix,
        minus_leading,
        parameters,
        {p: 0, q: 0, slope: -1},
    )
    assert minus_normal.row(0) == sp.zeros(1, 13)
    assert minus_normal.row(15) == sp.zeros(1, 13)
    assert_equal(
        determinant(
            minus_normal,
            (3, 11, 18, 20, 22, 23, 24, 26, 28),
            (0, 1, 2, 4, 5, 6, 8, 9, 12),
        ),
        -131072 * y**3 * kappa**2,
    )
    pure_minus = minus_normal.subs({x: 1, y: 0})
    assert_equal(
        determinant(
            pure_minus,
            (2, 10, 18, 20, 22, 24, 26, 28),
            (0, 1, 2, 4, 5, 6, 8, 9),
        ),
        65536 * kappa**2,
    )

    # lambda=-1, kappa=0: rank five and complete kernel P2.
    minus_zero_kappa = minus_matrix.subs(kappa, 0)
    middle_minus = -unit(8, 1) + unit(8, 4)
    assert is_zero(minus_zero_kappa * middle_minus)
    assert_equal(
        determinant(
            minus_zero_kappa,
            (16, 20, 22, 24, 28),
            (0, 1, 2, 5, 6),
        ),
        -1024,
    )
    minus_zero_leading = (
        x * unit(8, 3) + y * middle_minus + zeta * unit(8, 7)
    )
    minus_zero_normal = frozen_normal(
        matrix,
        minus_zero_leading,
        parameters,
        {p: 0, q: 0, kappa: 0, slope: -1},
    )
    assert minus_zero_normal.row(0) == sp.zeros(1, 13)
    assert minus_zero_normal.row(15) == sp.zeros(1, 13)

    # lambda=1, ell nonendpoint: rank five and complete kernel P2.
    plus_matrix = zero_matrix.subs(slope, 1)
    plus_vectors = (
        unit(8, 2),
        -unit(8, 0) + ell * unit(8, 4) + unit(8, 5),
        unit(8, 6),
    )
    assert all(is_zero(plus_matrix * vector) for vector in plus_vectors)
    assert_equal(
        determinant(
            plus_matrix,
            (19, 22, 23, 27, 31),
            (0, 1, 3, 4, 7),
        ),
        -1024 * (ell**2 - 1),
    )
    plus_leading = (
        x * plus_vectors[0] + y * plus_vectors[1] + zeta * plus_vectors[2]
    )
    plus_normal = frozen_normal(
        matrix,
        plus_leading,
        parameters,
        {p: 0, q: 0, slope: 1},
    )
    expected_row16 = sp.zeros(1, 13)
    expected_row16[0, 12] = 2 * (ell * x + y)
    expected_row20 = sp.zeros(1, 13)
    expected_row20[0, 12] = 2 * x
    expected_row28 = sp.zeros(1, 13)
    expected_row28[0, 12] = -2 * y
    assert plus_normal.row(16) == expected_row16
    assert plus_normal.row(20) == expected_row20
    assert plus_normal.row(28) == expected_row28

    # lambda=1, ell endpoints: rank four, complete kernel P3, same row forcing.
    endpoint_plus = {}
    for epsilon in (1, -1):
        endpoint_matrix = plus_matrix.subs(ell, epsilon)
        endpoint_vector = (
            -unit(8, 0) - epsilon * unit(8, 1) + unit(8, 7)
        )
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
            x * plus_vectors[0].subs(ell, epsilon)
            + y * plus_vectors[1].subs(ell, epsilon)
            + zeta * plus_vectors[2]
            + tau * endpoint_vector
        )
        endpoint_normal = frozen_normal(
            matrix,
            endpoint_leading,
            parameters,
            {p: 0, q: 0, ell: epsilon, slope: 1},
        )
        row16 = sp.zeros(1, 13)
        row16[0, 12] = 2 * (tau + epsilon * x + y)
        row20 = sp.zeros(1, 13)
        row20[0, 12] = 2 * x
        row28 = sp.zeros(1, 13)
        row28[0, 12] = -2 * y
        row24 = sp.zeros(1, 13)
        row24[0, 12] = 2 * epsilon * (tau - epsilon * x - y)
        assert endpoint_normal.row(16) == row16
        assert endpoint_normal.row(20) == row20
        assert endpoint_normal.row(28) == row28
        assert endpoint_normal.row(24) == row24
        endpoint_plus[str(epsilon)] = {
            "extension_rank": 4,
            "kernel_projective_dimension": 3,
            "D23_0000_forced_zero_on_mixed_kernel": True,
        }

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero raw-chart theorem",
        "distinct from the existing first projectivized `(p,q)`-normal",
        "Higher normals after a zero first normal",
        "remain **UNKNOWN**",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
        "No finite-field",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "PASS",
                "field": "exact characteristic zero",
                "component": 21,
                "base": "p=q=0 raw displayed chart",
                "ordinary_weight": {
                    "extension_rank": 7,
                    "kernel_projective_dimension": 0,
                    "generic_normal_mixed_rank": 9,
                    "exceptional_normal_strata": exceptional_ordinary,
                    "D01_diagonal_rows_identically_zero": True,
                },
                "lambda_minus_1": {
                    "kappa_nonzero_extension_rank": 6,
                    "kappa_nonzero_kernel_projective_dimension": 1,
                    "kappa_zero_extension_rank": 5,
                    "kappa_zero_kernel_projective_dimension": 2,
                    "D01_diagonal_rows_identically_zero": True,
                },
                "lambda_plus_1": {
                    "ell_nonendpoint_extension_rank": 5,
                    "ell_nonendpoint_kernel_projective_dimension": 2,
                    "endpoints": endpoint_plus,
                    "D23_0000_forced_zero_on_mixed_kernel": True,
                },
                "existing_pq_blowup_reproved": False,
                "higher_zero_normals_closed": False,
                "arbitrary_order_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
