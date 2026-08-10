#!/usr/bin/env python3
"""Verify component 21 finite-H22 extension normals at ell=0,+/-1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_FINITE_H22_EXTENSION_ELL_ZERO_UNIT_ENDPOINT_NORMAL_CLOSURE.md"
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
    extension = sp.symbols("z0:8")
    parameters = (p, q, kappa, ell, slope)
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )

    # ell=0 rank-drop cover.
    ell_zero = matrix.subs(ell, 0)
    assert_equal(
        determinant(
            ell_zero,
            (2, 3, 7, 16, 17, 20, 22, 24),
            tuple(range(8)),
        ),
        256 * p**4 * (slope - 1) ** 5 * (slope + 1) ** 3,
    )
    assert_equal(
        determinant(
            ell_zero,
            (2, 3, 16, 18, 20, 22, 24, 26),
            tuple(range(8)),
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
    zero_plus_columns = frozen_columns(
        matrix, leading_plus, parameters, zero_plus_sub
    )
    assert zero_plus_columns[0] == zero_plus_matrix.col(0)
    assert zero_plus_columns[1] == zero_plus_matrix.col(4)
    assert is_zero(zero_plus_columns[2])
    assert is_zero(zero_plus_columns[3])
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
    zero_plus_mixed = zero_plus_normal.extract(MIXED_ROWS, range(9))
    assert all(is_zero(zero_plus_mixed * vector) for vector in zero_plus_vectors)
    zero_plus_diagonals = diagonal_images(zero_plus_normal, zero_plus_vectors)
    assert zero_plus_diagonals == ((0, 0, 0, 4), (0, 0, 0, 4 * q))

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
    zero_minus_columns = frozen_columns(
        matrix, leading_zero_minus, parameters, zero_minus_sub
    )
    assert is_zero(zero_minus_columns[0])
    assert is_zero(zero_minus_columns[1])
    assert zero_minus_columns[3] == -zero_minus_matrix.col(7)
    zero_minus_normal = (
        zero_minus_matrix.row_join(zero_minus_columns[2]).row_join(
            zero_minus_columns[4]
        )
    )
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
    zero_minus_mixed = zero_minus_normal.extract(MIXED_ROWS, range(10))
    assert all(
        is_zero(zero_minus_mixed * vector) for vector in zero_minus_vectors
    )
    zero_minus_diagonals = diagonal_images(
        zero_minus_normal, zero_minus_vectors
    )
    assert zero_minus_diagonals == ((0, 0, 4, 0), (0, 0, 0, 0))

    endpoint_data = {}
    direction_x, direction_y = sp.symbols("X Y")
    for epsilon in (1, -1):
        endpoint = matrix.subs(ell, epsilon)
        first_cover = determinant(
            endpoint,
            (6, 7, 16, 17, 18, 20, 21, 24),
            tuple(range(8)),
        )
        assert_equal(
            first_cover,
            -256
            * epsilon
            * p**4
            * (slope - 1) ** 4
            * (slope + 1) ** 4,
        )
        second_cover = determinant(
            endpoint,
            (2, 3, 7, 16, 18, 20, 22, 24),
            tuple(range(8)),
        )
        expected_second = (
            1024 * slope**2 * kappa * p**3 * (slope - 1) ** 6
            if epsilon == 1
            else -1024 * kappa * p**3 * (slope - 1) ** 6
        )
        assert_equal(second_cover, expected_second)

        endpoint_plus_sub = {ell: epsilon, slope: 1}
        endpoint_plus_matrix = matrix.subs(endpoint_plus_sub)
        endpoint_vector = sp.Matrix(
            (0, -epsilon, -epsilon, 0, -epsilon, -1, 0, 1)
        )
        assert is_zero(endpoint_plus_matrix * leading_plus)
        assert is_zero(endpoint_plus_matrix * endpoint_vector)
        assert_equal(
            determinant(
                endpoint_plus_matrix,
                (2, 3, 7, 21, 23, 31),
                (0, 1, 2, 3, 4, 5),
            ),
            4096 * epsilon * p**4,
        )

        leading = direction_x * leading_plus + direction_y * endpoint_vector
        columns = frozen_columns(matrix, leading, parameters, endpoint_plus_sub)
        normal = endpoint_plus_matrix
        for column in columns:
            normal = normal.row_join(column)
        assert_equal(
            determinant(
                normal,
                (2, 3, 7, 17, 20, 21, 23),
                (0, 1, 2, 3, 5, 11, 12),
            ),
            16384 * epsilon * direction_y**2 * p**5,
        )
        generic_vectors = (
            unit(13, 4),
            -p * unit(13, 0) + unit(13, 6),
            -epsilon * unit(13, 1)
            - epsilon * unit(13, 2)
            - unit(13, 5)
            + unit(13, 7),
            -direction_x * unit(13, 0) + unit(13, 8),
            unit(13, 9),
            unit(13, 10),
        )
        mixed = normal.extract(MIXED_ROWS, range(13))
        assert all(is_zero(mixed * vector) for vector in generic_vectors)
        generic_diagonals = diagonal_images(normal, generic_vectors)
        assert generic_diagonals == (
            (0, 0, 0, 4),
            (0, 0, 0, 4 * q),
            (0, 0, 0, 4 * epsilon),
            (0, 0, 0, 0),
            (0, 0, 0, 4 * direction_x),
            (0, 0, 0, 0),
        )

        pure = normal.subs({direction_x: 1, direction_y: 0})
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
            vector.subs({direction_x: 1, direction_y: 0})
            for vector in generic_vectors
        ) + (unit(13, 11),)
        pure_mixed = pure.extract(MIXED_ROWS, range(13))
        assert all(is_zero(pure_mixed * vector) for vector in pure_vectors)
        pure_diagonals = diagonal_images(pure, pure_vectors)
        assert all(row[:3] == (0, 0, 0) for row in pure_diagonals)

        endpoint_minus_sub = {ell: epsilon, kappa: 0, slope: -1}
        endpoint_minus_matrix = matrix.subs(endpoint_minus_sub)
        minus_vector = sp.Matrix(
            (0, -epsilon, 0, 0, epsilon, 0, 0, 1)
        )
        assert is_zero(endpoint_minus_matrix * minus_vector)
        assert_equal(
            determinant(
                endpoint_minus_matrix,
                (2, 3, 7, 16, 18, 20, 24),
                (0, 1, 2, 3, 4, 5, 6),
            ),
            16384 * epsilon * p**3,
        )
        minus_columns = frozen_columns(
            matrix, minus_vector, parameters, endpoint_minus_sub
        )
        assert is_zero(minus_columns[0])
        assert is_zero(minus_columns[1])
        assert minus_columns[3] == (
            -endpoint_minus_matrix.col(1) + endpoint_minus_matrix.col(4)
        )
        minus_normal = endpoint_minus_matrix.row_join(
            minus_columns[2]
        ).row_join(minus_columns[4])
        assert_equal(
            determinant(
                minus_normal,
                (2, 3, 7, 18, 20, 22, 23, 24),
                (1, 2, 3, 4, 5, 6, 8, 9),
            ),
            32768 * epsilon * p**3,
        )
        minus_vectors = (
            unit(10, 0),
            minus_vector.col_join(sp.zeros(2, 1)),
        )
        minus_mixed = minus_normal.extract(MIXED_ROWS, range(10))
        assert all(is_zero(minus_mixed * vector) for vector in minus_vectors)
        minus_diagonals = diagonal_images(minus_normal, minus_vectors)
        assert minus_diagonals == ((0, 0, 4, 0), (0, 0, 0, 0))

        endpoint_data[str(epsilon)] = {
            "lambda_1_extension_rank": 6,
            "lambda_1_kernel_dimension": 2,
            "lambda_1_projective_directions_closed": True,
            "kappa_0_lambda_minus_1_extension_rank": 7,
            "kappa_0_lambda_minus_1_normal_closed": True,
        }

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero divisor theorem",
        "rank drop exactly",
        "higher normals after a zero first normal",
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
                "divisors": ["ell=0", "ell=1", "ell=-1"],
                "open_condition": "p != 0",
                "finite_weight_extension_rank_drop_locus": [
                    "lambda=1",
                    "kappa=0, lambda=-1",
                ],
                "ell_zero": {
                    "lambda_1_rank": 7,
                    "lambda_minus_1_kappa_0_rank": 7,
                    "plus_diagonal_image": [
                        [str(value) for value in row]
                        for row in zero_plus_diagonals
                    ],
                    "minus_diagonal_image": [
                        [str(value) for value in row]
                        for row in zero_minus_diagonals
                    ],
                },
                "unit_endpoints": endpoint_data,
                "finite_markings": "triangular rank invariance",
                "p_zero_closed": False,
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
