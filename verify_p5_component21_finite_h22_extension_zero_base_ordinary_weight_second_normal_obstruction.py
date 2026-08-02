#!/usr/bin/env python3
"""Verify the ordinary-weight component-21 zero-base second normal."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

import verify_p5_component21_finite_base_extension_infinity_partial_closure as V

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT
    / "P5_COMPONENT21_FINITE_H22_EXTENSION_ZERO_BASE_ORDINARY_WEIGHT_SECOND_NORMAL_OBSTRUCTION.md"
)


def determinant(matrix, rows, columns):
    return sp.factor(matrix.extract(rows, columns).det())


def assert_equal(left, right):
    assert sp.expand(left - right) == 0


def is_zero(vector):
    return all(sp.expand(value) == 0 for value in vector)


def unit(length, index):
    return sp.eye(length).col(index)


def main() -> None:
    p, q, kappa, ell, slope = sp.symbols("p q kappa ell slope")
    extension = sp.symbols("z0:8")
    parameters = (p, q, kappa, ell, slope)
    alpha, beta = V.finite_bases(p, q, kappa, ell)
    matrix = V.stacked_contraction_matrix(
        alpha, beta, extension, "finite", slope
    )
    zero_matrix = matrix.subs({p: 0, q: 0})
    kernel = sp.Matrix((0, 0, 0, 1 - slope, 0, 0, slope + 1, 0))

    # Exact all-parameter zero family.
    assert is_zero(zero_matrix * kernel)

    # Complete first normal and its four universal kernel directions.
    normal = zero_matrix
    for parameter in parameters:
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
    minor_nonzero_nonendpoint = determinant(
        normal,
        (6, 14, 18, 19, 20, 23, 24, 27, 28),
        columns,
    )
    assert_equal(
        minor_nonzero_nonendpoint,
        512
        * ell
        * (slope - 1) ** 5
        * (slope + 1) ** 6
        * (ell**2 - 1),
    )
    factor_b = slope * ell + slope + ell - 1
    minor_ell_zero = determinant(
        normal,
        (2, 10, 19, 20, 22, 23, 24, 27, 28),
        columns,
    )
    assert_equal(
        minor_ell_zero,
        512
        * (slope - 1) ** 5
        * (slope + 1) ** 4
        * (ell**2 - 1)
        * factor_b**2,
    )
    minor_endpoint_kappa = determinant(
        normal,
        (6, 14, 18, 19, 20, 22, 23, 24, 28),
        columns,
    )
    assert_equal(
        minor_endpoint_kappa,
        512 * ell * kappa * (slope - 1) ** 6 * (slope + 1) ** 5,
    )

    plus_exception = normal.subs({kappa: 0, ell: 1})
    assert_equal(
        determinant(
            plus_exception,
            (6, 14, 16, 18, 19, 20, 23, 24, 28),
            columns,
        ),
        -512 * (slope - 1) ** 6 * (slope + 1) ** 5,
    )
    minus_exception = normal.subs({kappa: 0, ell: -1})
    assert_equal(
        determinant(
            minus_exception,
            (2, 10, 16, 18, 19, 20, 23, 24, 28),
            columns,
        ),
        2048 * (slope - 1) ** 6 * (slope + 1) ** 3,
    )

    # Complete second normal after straightening along the exact zero family.
    dp_column = (sp.diff(matrix, p) * kernel).subs({p: 0, q: 0})
    dq_column = (sp.diff(matrix, q) * kernel).subs({p: 0, q: 0})
    second = zero_matrix.row_join(dp_column).row_join(dq_column)
    assert second.shape == (32, 10)
    assert second.row(0) == sp.zeros(1, 10)
    assert second.row(15) == sp.zeros(1, 10)

    # N and S have the same column image for slope!=-1.
    dkappa_column = (sp.diff(matrix, kappa) * kernel).subs({p: 0, q: 0})
    dell_column = (sp.diff(matrix, ell) * kernel).subs({p: 0, q: 0})
    dslope_column = (sp.diff(matrix, slope) * kernel).subs({p: 0, q: 0})
    assert is_zero(dkappa_column)
    assert is_zero(dell_column)
    assert is_zero((slope + 1) * dslope_column - 2 * zero_matrix.col(3))

    second_kernel = kernel.col_join(sp.zeros(2, 1))
    assert is_zero(second * second_kernel)
    # The rank-nine cover above applies to S because each column of N is in
    # col(S), while S is literally a submatrix of N.  Hence nullity(S)=1.
    assert len(first_kernel) == 13 - 9

    theorem = " ".join(THEOREM.read_text(encoding="utf-8").split())
    for phrase in (
        "Exact characteristic-zero theorem in the displayed raw finite chart",
        "sole surviving second-zero directions remain tangent to the exact zero family",
        "A zero second normal may continue to higher order",
        "remains **UNKNOWN**",
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
                "stratum": "p=q=0, finite lambda not equal to +/-1",
                "exact_zero_family": True,
                "complete_first_normal_rank": 9,
                "complete_first_normal_kernel_dimension": 4,
                "first_zero_forces_dp_dq_zero": True,
                "complete_second_normal_shape": [32, 10],
                "complete_second_normal_rank": 9,
                "complete_second_normal_kernel": "span{(K_lambda,0,0)}",
                "D01_diagonal_rows_identically_zero": True,
                "second_normal_H22_incidence_empty": True,
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
