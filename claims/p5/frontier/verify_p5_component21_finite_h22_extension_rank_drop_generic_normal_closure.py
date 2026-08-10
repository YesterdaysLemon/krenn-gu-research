#!/usr/bin/env python3
"""Verify the generic component-21 finite-H22 extension rank-drop normals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_FINITE_H22_EXTENSION_RANK_DROP_GENERIC_NORMAL_CLOSURE.md"
MIXED_ROWS = tuple(range(1, 15)) + tuple(range(17, 31))
DIAGONAL_ROWS = (0, 15, 16, 31)

MAP_MINOR_ROWS = (
    (2, 3, 16, 17, 18, 20, 21, 24),
    (3, 6, 7, 16, 17, 18, 20, 24),
    (2, 3, 7, 16, 18, 20, 22, 24),
)
PLUS_RANK_ROWS = (2, 3, 7, 17, 21, 23, 31)
PLUS_RANK_COLUMNS = (0, 1, 2, 3, 4, 5, 7)
PLUS_NORMAL_ROWS = (
    (2, 3, 7, 17, 21, 23, 24),
    (2, 3, 7, 17, 21, 23, 26),
)
PLUS_NORMAL_COLUMNS = (0, 1, 2, 3, 5, 7, 8)
MINUS_RANK_ROWS = (2, 3, 7, 16, 18, 20, 24)
MINUS_RANK_COLUMNS = (0, 1, 2, 3, 4, 5, 6)
MINUS_NORMAL_ROWS = (2, 3, 7, 18, 19, 20, 22, 24)
MINUS_NORMAL_COLUMNS = (1, 2, 3, 4, 5, 6, 8, 9)


def determinant(
    matrix: sp.Matrix, rows: tuple[int, ...], columns: tuple[int, ...]
) -> sp.Expr:
    selected = matrix.extract(rows, columns)
    return sp.factor(
        sp.polys.matrices.DomainMatrix.from_Matrix(selected).det().as_expr()
    )


def unit_vector(length: int, index: int) -> sp.Matrix:
    return sp.eye(length).col(index)


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.expand(left - right) == 0


def main() -> None:
    p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
    extension = sp.symbols("z0:8")
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )

    factor_a = (ell + 1) * slope - ell + 1
    factor_b = (ell + 1) * slope + ell - 1
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
    map_minors = tuple(
        determinant(matrix, rows, tuple(range(8))) for rows in MAP_MINOR_ROWS
    )
    for actual, expected in zip(map_minors, expected_map_minors, strict=True):
        assert_equal(actual, expected)
    assert sp.expand(factor_b - factor_a) == 2 * (ell - 1)
    assert (factor_a.subs(slope, -1), factor_b.subs(slope, -1)) == (
        -2 * ell,
        -2,
    )

    plus_kernel = sp.Matrix((-p, 0, 0, 0, -q, 0, 1, 0))
    plus_matrix = matrix.subs(slope, 1)
    assert plus_matrix * plus_kernel == sp.zeros(32, 1)
    plus_rank_minor = determinant(
        plus_matrix, PLUS_RANK_ROWS, PLUS_RANK_COLUMNS
    )
    assert_equal(plus_rank_minor, -16384 * ell * p**5 * (ell**2 - 1))

    plus_parameter_columns = tuple(
        (sp.diff(matrix, parameter) * plus_kernel).subs(slope, 1)
        for parameter in (p, q, kappa, ell, slope)
    )
    assert plus_parameter_columns[0] == plus_matrix.col(0)
    assert plus_parameter_columns[1] == plus_matrix.col(4)
    assert plus_parameter_columns[2] == sp.zeros(32, 1)
    assert plus_parameter_columns[3] == sp.zeros(32, 1)
    plus_transverse = plus_parameter_columns[4]
    plus_normal = plus_matrix.row_join(plus_transverse)
    plus_mixed = plus_normal.extract(MIXED_ROWS, tuple(range(9)))

    plus_normal_minors = tuple(
        determinant(plus_normal, rows, PLUS_NORMAL_COLUMNS)
        for rows in PLUS_NORMAL_ROWS
    )
    expected_plus_normal_minors = (
        -8192 * ell * p**5 * q * (ell**2 - 1),
        8192 * ell * p**5 * (ell**2 - 1) * (ell * kappa * q + 1),
    )
    for actual, expected in zip(
        plus_normal_minors, expected_plus_normal_minors, strict=True
    ):
        assert_equal(actual, expected)
    plus_mixed_kernels = (
        unit_vector(9, 4),
        -p * unit_vector(9, 0) + unit_vector(9, 6),
    )
    assert all(
        plus_mixed * vector == sp.zeros(28, 1)
        for vector in plus_mixed_kernels
    )
    plus_diagonals = tuple(
        tuple(
            sp.factor(value)
            for value in plus_normal.extract(
                DIAGONAL_ROWS, tuple(range(9))
            )
            * vector
        )
        for vector in plus_mixed_kernels
    )
    assert plus_diagonals == ((0, 0, 0, 4), (0, 0, 0, 4 * q))

    minus_kernel = sp.Matrix((0, -1 / ell, 0, 0, 1 / ell, 0, 0, 1))
    minus_centre = {kappa: 0, slope: -1}
    minus_matrix = matrix.subs(minus_centre)
    assert minus_matrix * minus_kernel == sp.zeros(32, 1)
    minus_rank_minor = determinant(
        minus_matrix, MINUS_RANK_ROWS, MINUS_RANK_COLUMNS
    )
    assert_equal(minus_rank_minor, 16384 * ell**3 * p**3)

    minus_parameter_columns = tuple(
        (sp.diff(matrix, parameter) * minus_kernel).subs(minus_centre)
        for parameter in (p, q, kappa, ell, slope)
    )
    assert minus_parameter_columns[0] == sp.zeros(32, 1)
    assert minus_parameter_columns[1] == sp.zeros(32, 1)
    assert minus_parameter_columns[3] == (
        -minus_matrix.col(1) + minus_matrix.col(4)
    ) / ell**2
    minus_normal = (
        minus_matrix.row_join(minus_parameter_columns[2]).row_join(
            minus_parameter_columns[4]
        )
    )
    minus_mixed = minus_normal.extract(MIXED_ROWS, tuple(range(10)))
    minus_normal_minor = determinant(
        minus_normal, MINUS_NORMAL_ROWS, MINUS_NORMAL_COLUMNS
    )
    assert_equal(minus_normal_minor, 32768 * p**3 * (ell**2 - 1))
    minus_mixed_kernels = (
        unit_vector(10, 0),
        minus_kernel.col_join(sp.zeros(2, 1)),
    )
    assert all(
        minus_mixed * vector == sp.zeros(28, 1)
        for vector in minus_mixed_kernels
    )
    minus_diagonals = tuple(
        tuple(
            sp.factor(value)
            for value in minus_normal.extract(
                DIAGONAL_ROWS, tuple(range(10))
            )
            * vector
        )
        for vector in minus_mixed_kernels
    )
    assert minus_diagonals == ((0, 0, 4, 0), (0, 0, 0, 0))

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero open-chart theorem",
        "complete rank-drop locus",
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
                "open_chart": "p*ell*(ell^2-1) != 0",
                "finite_weight_extension_rank_drop_locus": [
                    "lambda=1",
                    "kappa=0, lambda=-1",
                ],
                "rank_on_each_divisor": 7,
                "plus_kernel": [str(value) for value in plus_kernel],
                "minus_kernel": [str(value) for value in minus_kernel],
                "plus_mixed_rank": 7,
                "minus_mixed_rank": 8,
                "plus_diagonal_image": [
                    [str(value) for value in row] for row in plus_diagonals
                ],
                "minus_diagonal_image": [
                    [str(value) for value in row] for row in minus_diagonals
                ],
                "finite_markings": "triangular rank invariance",
                "omitted_divisors_closed": False,
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
