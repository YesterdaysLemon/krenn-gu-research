#!/usr/bin/env python3
"""Exact replay for the corrected mixed (2,2,1) triangle obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Squarefree degree-two product in the ordered basis e_ij, i<j."""
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def pair_matrix(left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(left_row, right_row) for left_row in left for right_row in right)
    )


def multiplication_matrix(linear: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(linear, sp.eye(4).col(column)) for column in range(4))
    )


def maximal_minors(matrix: sp.Matrix) -> set[sp.Expr]:
    return {
        sp.factor(matrix.extract(rows, range(matrix.cols)).det())
        for rows in itertools.combinations(range(matrix.rows), matrix.cols)
    }


def main() -> None:
    # All ordinary two-dimensional synchronizer pencils are totally isotropic.
    lam, t, u = sp.symbols("lambda t u")
    y = sp.Matrix((1, 0, 1, 1))
    x = sp.Matrix((0, 1, 1, lam))
    y_sharp = sp.Matrix((0, 1, -1, -lam))
    x_sharp = sp.Matrix((lam, 0, -lam, -lam))
    assert product(y + t * y_sharp, x + u * x_sharp) == product(
        x + t * x_sharp, y + u * y_sharp
    )

    # The support-two equal-ratio chart: a two-supported factor has one
    # degree-one annihilator, and no other synchronized leaf contains it.
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    alpha, beta = sp.symbols("alpha beta")
    y_partner = a + beta * b_bar
    x_partner = b + alpha * a_bar
    assert product(a, x_partner) == product(b, y_partner)

    ann_a = multiplication_matrix(a)
    assert ann_a.rank() == 3
    assert len(ann_a.nullspace()) == 1
    assert sp.Matrix.hstack(ann_a.nullspace()[0], a_bar).rank() == 1

    full_support_minor = sp.factor(
        multiplication_matrix(y_partner).extract((0, 1, 2, 4), range(4)).det()
    )
    assert full_support_minor != 0
    assert sp.factor(full_support_minor).has(beta)

    alpha_3, beta_3 = sp.symbols("alpha_3 beta_3")
    other_leaf_and_annihilator = sp.Matrix.hstack(
        a + beta_3 * b_bar,
        b + alpha_3 * a_bar,
        a_bar,
    )
    assert other_leaf_and_annihilator.rank() == 3

    # The Borel-legal full-support 2+2 chart.  The center is (a+b,b), and
    # every rank-three synchronized leaf can be normalized to leaf(r,s).
    r2, r3, s2, s3 = sp.symbols("r2 r3 s2 s3")

    def leaf(r: sp.Expr, s: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
        return a + b - r * b_bar - s * a_bar, b - s * a_bar

    leaf2 = leaf(r2, s2)
    leaf3 = leaf(r3, s3)
    matrix23 = pair_matrix(leaf2, leaf3)
    minors4 = maximal_minors(matrix23)

    delta = r2 * s3 - r3 * s2
    a_minus = s2 * s3 * (r2 + r3) - (s2 + s3)
    a_plus = s2 * s3 * (r2 + r3) + (s2 + s3)
    d_minus = r2 * r3 * (s2 + s3) - (r2 + r3)
    d_plus = r2 * r3 * (s2 + s3) + (r2 + r3)

    # These four maximal minors suffice.  On rank<=3 and delta!=0, their
    # residual factors vanish.  Paired subtraction then gives both sums zero,
    # which makes delta zero after all.
    targets = {
        sp.factor(-8 * delta * a_minus),
        sp.factor(8 * delta * a_plus),
        sp.factor(8 * delta * d_minus),
        sp.factor(8 * delta * d_plus),
    }
    assert targets <= minors4
    assert sp.expand(a_plus - a_minus) == 2 * (s2 + s3)
    assert sp.expand(d_plus - d_minus) == 2 * (r2 + r3)
    assert sp.expand(delta.subs({r3: -r2, s3: -s2})) == 0

    # Hence a rank-three leaf pair has the alternating synchronization as its
    # unique relation.  Its 2x2 coefficient matrix is nonsingular, so the
    # relation has coefficient rank two, never one.
    commutator = product(leaf2[0], leaf3[1]) - product(leaf2[1], leaf3[0])
    radical_vector = sp.Matrix((0, 1, -1, -1, 1, 0))
    assert commutator == delta * radical_vector
    coefficient_matrix = sp.Matrix(((0, 1), (-1, 0)))
    assert coefficient_matrix.det() == 1

    result = {
        "full_2_plus_2_rank_drop_implies": "delta=r2*s3-r3*s2=0",
        "leaf_commutator": "delta*(0,1,-1,-1,1,0)",
        "forced_relation_coefficient_rank": 2,
        "support_two_equal_annihilator": "C*(1,-1,0,0)",
        "conclusion": "rank pattern (2,2,1) triangle is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
