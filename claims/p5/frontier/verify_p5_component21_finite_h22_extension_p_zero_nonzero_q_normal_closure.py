#!/usr/bin/env python3
"""Verify component 21 finite-H22 extension normals on p=0,q!=0."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_FINITE_H22_EXTENSION_P_ZERO_NONZERO_Q_NORMAL_CLOSURE.md"
MIXED_ROWS = tuple(range(1, 15)) + tuple(range(17, 31))
DIAGONAL_ROWS = (0, 15, 16, 31)


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


def frozen_columns(matrix, leading, parameters, substitution):
    return tuple(
        (sp.diff(matrix, parameter) * leading).subs(substitution)
        for parameter in parameters
    )


def diagonal_images(normal, vectors):
    return tuple(
        tuple(
            sp.factor(value)
            for value in normal.extract(DIAGONAL_ROWS, range(normal.cols)) * vector
        )
        for vector in vectors
    )


def main() -> None:
    p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
    x, y = sp.symbols("X Y")
    extension = sp.symbols("z0:8")
    parameters = (p, q, kappa, ell, slope)
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )
    divisor = matrix.subs(p, 0)

    factor_a = (ell + 1) * slope - ell + 1
    factor_b = (ell + 1) * slope + ell - 1
    generic_rank_minors = (
        determinant(
            divisor,
            (11, 14, 15, 16, 18, 19, 20, 24),
            tuple(range(8)),
        ),
        determinant(
            divisor,
            (10, 11, 16, 18, 19, 20, 23, 24),
            tuple(range(8)),
        ),
        determinant(
            divisor,
            (10, 11, 15, 16, 18, 20, 22, 24),
            tuple(range(8)),
        ),
    )
    expected_generic_rank_minors = (
        256
        * ell
        * q**3
        * (slope - 1) ** 5
        * (slope + 1) ** 2
        * (ell**2 - 1)
        * factor_a,
        -256
        * ell
        * q**2
        * (slope - 1) ** 5
        * (slope + 1) ** 2
        * (ell**2 - 1)
        * factor_b,
        256
        * kappa
        * q**3
        * (slope - 1) ** 6
        * factor_a
        * factor_b,
    )
    for actual, expected in zip(
        generic_rank_minors, expected_generic_rank_minors, strict=True
    ):
        assert_equal(actual, expected)

    ell_zero = divisor.subs(ell, 0)
    assert_equal(
        determinant(
            ell_zero,
            (10, 11, 15, 16, 19, 20, 22, 24),
            tuple(range(8)),
        ),
        256 * q**3 * (slope - 1) ** 6 * (slope + 1) ** 2,
    )
    assert_equal(
        determinant(
            ell_zero,
            (10, 11, 16, 18, 20, 22, 24, 26),
            tuple(range(8)),
        ),
        -256 * kappa**2 * q**2 * (slope - 1) ** 8,
    )

    for epsilon in (1, -1):
        endpoint = divisor.subs(ell, epsilon)
        assert_equal(
            determinant(
                endpoint,
                (14, 15, 16, 18, 19, 20, 23, 24),
                tuple(range(8)),
            ),
            -256 * q**2 * (slope - 1) ** 5 * (slope + 1) ** 3,
        )
        second = determinant(
            endpoint,
            (10, 11, 15, 16, 18, 20, 22, 24),
            tuple(range(8)),
        )
        expected = (
            1024 * slope**2 * kappa * q**3 * (slope - 1) ** 6
            if epsilon == 1
            else -1024 * kappa * q**3 * (slope - 1) ** 6
        )
        assert_equal(second, expected)

    leading_plus = sp.Matrix((0, 0, 0, 0, -q, 0, 1, 0))
    plus_sub = {p: 0, slope: 1}
    plus_matrix = matrix.subs(plus_sub)
    assert is_zero(plus_matrix * leading_plus)
    plus_columns = frozen_columns(matrix, leading_plus, parameters, plus_sub)
    assert plus_columns[0] == plus_matrix.col(0)
    assert plus_columns[1] == plus_matrix.col(4)
    assert is_zero(plus_columns[2])
    assert is_zero(plus_columns[3])
    plus_normal = plus_matrix.row_join(plus_columns[4])
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
    plus_mixed = plus_normal.extract(MIXED_ROWS, range(9))
    assert all(is_zero(plus_mixed * vector) for vector in plus_vectors)
    plus_diagonals = diagonal_images(plus_normal, plus_vectors)
    expected_plus_diagonals = (
        (0, 0, 0, 4),
        (0, 4 * q, 0, 4 * (kappa * q - ell)),
        (0, 0, 0, 4 * q),
    )
    for actual_row, expected_row in zip(
        plus_diagonals, expected_plus_diagonals, strict=True
    ):
        for actual, expected in zip(actual_row, expected_row, strict=True):
            assert_equal(actual, expected)

    zero_plus_matrix = plus_matrix.subs(ell, 0)
    zero_plus_normal = plus_normal.subs(ell, 0)
    assert_equal(
        determinant(
            zero_plus_matrix,
            (11, 14, 15, 23, 25, 29, 31),
            (0, 1, 2, 3, 4, 5, 7),
        ),
        -16384 * q**5,
    )
    assert_equal(
        determinant(
            zero_plus_normal,
            (11, 14, 22, 23, 25, 29),
            (0, 1, 2, 3, 7, 8),
        ),
        2048 * q**4,
    )

    endpoint_summary = {}
    for epsilon in (1, -1):
        endpoint_sub = {p: 0, ell: epsilon, slope: 1}
        endpoint_matrix = matrix.subs(endpoint_sub)
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
        leading = x * leading_plus + y * endpoint_vector
        normal = endpoint_matrix
        for column in frozen_columns(matrix, leading, parameters, endpoint_sub):
            normal = normal.row_join(column)
        assert_equal(
            determinant(
                normal,
                (10, 11, 20, 23, 25, 29),
                (0, 1, 2, 3, 11, 12),
            ),
            -4096 * epsilon * y**2 * q**4,
        )
        generic_vectors = (
            unit(13, 4),
            -unit(13, 0) + epsilon * unit(13, 2) + unit(13, 5),
            unit(13, 6),
            -unit(13, 0) - epsilon * unit(13, 1) + unit(13, 7),
            -x * unit(13, 0) + unit(13, 8),
            unit(13, 9),
            unit(13, 10),
        )
        mixed = normal.extract(MIXED_ROWS, range(13))
        assert all(is_zero(mixed * vector) for vector in generic_vectors)
        generic_diagonals = diagonal_images(normal, generic_vectors)
        assert all(row[0] == 0 and row[2] == 0 for row in generic_diagonals)

        pure = normal.subs({x: 1, y: 0})
        assert_equal(
            determinant(
                pure,
                (10, 11, 18, 23, 29),
                (0, 1, 2, 3, 12),
            ),
            512 * q**3,
        )
        pure_vectors = tuple(
            vector.subs({x: 1, y: 0}) for vector in generic_vectors
        ) + (unit(13, 11),)
        pure_mixed = pure.extract(MIXED_ROWS, range(13))
        assert all(is_zero(pure_mixed * vector) for vector in pure_vectors)
        pure_diagonals = diagonal_images(pure, pure_vectors)
        assert all(row[0] == 0 and row[2] == 0 for row in pure_diagonals)
        endpoint_summary[str(epsilon)] = {
            "extension_rank": 6,
            "kernel_dimension": 2,
            "all_projective_first_normals_closed": True,
        }

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
    minus_columns = frozen_columns(matrix, leading_minus, parameters, minus_sub)
    assert is_zero(minus_columns[0])
    assert is_zero(minus_columns[1])
    assert minus_columns[3] == (
        -minus_matrix.col(1) + minus_matrix.col(4)
    ) / ell**2
    minus_normal = minus_matrix.row_join(minus_columns[2]).row_join(
        minus_columns[4]
    )
    assert_equal(
        determinant(
            minus_normal,
            (10, 11, 18, 19, 20, 22, 24, 28),
            (1, 2, 3, 4, 5, 6, 8, 9),
        ),
        32768 * q**2 * (ell**2 - 1) / ell,
    )
    minus_vectors = (unit(10, 0), leading_minus.col_join(sp.zeros(2, 1)))
    minus_mixed = minus_normal.extract(MIXED_ROWS, range(10))
    assert all(is_zero(minus_mixed * vector) for vector in minus_vectors)
    minus_diagonals = diagonal_images(minus_normal, minus_vectors)
    assert minus_diagonals == ((0, 0, 4, 0), (0, 0, 0, 0))

    zero_minus_vector = sp.Matrix((0, -1, 0, 0, 1, 0, 0, 0))
    zero_minus_sub = {p: 0, ell: 0, kappa: 0, slope: -1}
    zero_minus_matrix = matrix.subs(zero_minus_sub)
    assert is_zero(zero_minus_matrix * zero_minus_vector)
    assert_equal(
        determinant(
            zero_minus_matrix,
            (10, 11, 16, 20, 22, 24, 28),
            (0, 1, 2, 3, 5, 6, 7),
        ),
        -16384 * q**2,
    )
    zero_minus_columns = frozen_columns(
        matrix, zero_minus_vector, parameters, zero_minus_sub
    )
    zero_minus_normal = zero_minus_matrix.row_join(
        zero_minus_columns[2]
    ).row_join(zero_minus_columns[4])
    assert_equal(
        determinant(
            zero_minus_normal,
            (10, 11, 18, 19, 20, 22, 24, 28),
            (1, 2, 3, 5, 6, 7, 8, 9),
        ),
        32768 * q**2,
    )

    endpoint_minus_summary = {}
    for epsilon in (1, -1):
        endpoint_minus_vector = sp.Matrix(
            (0, -epsilon, 0, 0, epsilon, 0, 0, 1)
        )
        endpoint_minus_sub = {p: 0, ell: epsilon, kappa: 0, slope: -1}
        endpoint_minus_matrix = matrix.subs(endpoint_minus_sub)
        assert is_zero(endpoint_minus_matrix * endpoint_minus_vector)
        assert_equal(
            determinant(
                endpoint_minus_matrix,
                (10, 11, 15, 16, 18, 20, 24),
                (0, 1, 2, 3, 4, 5, 6),
            ),
            16384 * epsilon * q**3,
        )
        endpoint_minus_columns = frozen_columns(
            matrix, endpoint_minus_vector, parameters, endpoint_minus_sub
        )
        endpoint_minus_normal = endpoint_minus_matrix.row_join(
            endpoint_minus_columns[2]
        ).row_join(endpoint_minus_columns[4])
        assert_equal(
            determinant(
                endpoint_minus_normal,
                (10, 11, 18, 20, 22, 23, 24, 28),
                (1, 2, 3, 4, 5, 6, 8, 9),
            ),
            32768 * q**2,
        )
        endpoint_minus_summary[str(epsilon)] = True

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero divisor theorem",
        "rank drop exactly",
        "present theorem is nonredundant",
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
                "divisor": "p=0, q!=0",
                "finite_weight_extension_rank_drop_locus": [
                    "lambda=1",
                    "kappa=0, lambda=-1",
                ],
                "lambda_1_generic_diagonal_image": [
                    [str(value) for value in row] for row in plus_diagonals
                ],
                "unit_endpoint_kernel_planes": endpoint_summary,
                "unit_endpoint_minus_normals": endpoint_minus_summary,
                "finite_markings": "triangular rank invariance",
                "zero_base_closed": False,
                "higher_normals_closed": False,
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
