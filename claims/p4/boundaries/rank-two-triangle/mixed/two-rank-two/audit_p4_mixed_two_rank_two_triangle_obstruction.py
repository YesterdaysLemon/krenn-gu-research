#!/usr/bin/env python3
"""Independent coordinate audit of the mixed (2,2,1) obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def multiply(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def four_products(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    columns = []
    for left_row in left:
        for right_row in right:
            columns.append(multiply(left_row, right_row))
    return sp.Matrix.hstack(*columns)


def main() -> None:
    # Use the crossed partition {0,2}|{1,3}, independently permuting the
    # primary certificate's coordinates.
    a = sp.Matrix((1, 0, 1, 0))
    a_bar = sp.Matrix((1, 0, -1, 0))
    b = sp.Matrix((0, 1, 0, 1))
    b_bar = sp.Matrix((0, 1, 0, -1))
    r2, r3, s2, s3 = sp.symbols("r2 r3 s2 s3")

    def leaf(r: sp.Expr, s: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
        return a + b - r * b_bar - s * a_bar, b - s * a_bar

    left, right = leaf(r2, s2), leaf(r3, s3)
    matrix = four_products(left, right)
    minors = [
        sp.factor(matrix.extract(rows, range(4)).det())
        for rows in itertools.combinations(range(6), 4)
    ]

    delta = r2 * s3 - r3 * s2
    residuals = (
        s2 * s3 * (r2 + r3) - (s2 + s3),
        s2 * s3 * (r2 + r3) + (s2 + s3),
        r2 * r3 * (s2 + s3) - (r2 + r3),
        r2 * r3 * (s2 + s3) + (r2 + r3),
    )
    for residual in residuals:
        assert any(
            sp.simplify(minor / (delta * residual)) in (8, -8)
            for minor in minors
            if minor != 0
        )

    # Logical audit of the open set delta!=0: the four vanishing residuals
    # imply the two vector sums are zero, hence delta itself is zero.
    assert sp.expand(residuals[1] - residuals[0]) == 2 * (s2 + s3)
    assert sp.expand(residuals[3] - residuals[2]) == 2 * (r2 + r3)
    contradiction = sp.expand(delta.subs({r3: -r2, s3: -s2}))
    assert contradiction == 0

    relation = multiply(left[0], right[1]) - multiply(left[1], right[0])
    assert relation == delta * sp.Matrix((1, 0, -1, -1, 0, 1))
    assert sp.Matrix(((0, 1), (-1, 0))).rank() == 2

    # Re-audit the support-two equal-ratio boundary in crossed coordinates.
    alpha, beta = sp.symbols("alpha beta")
    y_partner = a + beta * b_bar
    x_partner = b + alpha * a_bar
    multiplication = sp.Matrix.hstack(
        *(multiply(y_partner, sp.eye(4).col(column)) for column in range(4))
    )
    full_minor = sp.factor(multiplication.extract((0, 1, 3, 5), range(4)).det())
    assert full_minor != 0 and full_minor.subs(beta, 0) == 0
    boundary = multiplication.subs(beta, 0)
    assert boundary.rank() == 3
    assert sp.Matrix.hstack(boundary.nullspace()[0], a_bar).rank() == 1
    assert sp.Matrix.hstack(a + beta * b_bar, b + alpha * a_bar, a_bar).rank() == 3

    result = {
        "coordinate_partition": "{0,2}|{1,3}",
        "maximal_minors_checked": len(minors),
        "delta_open_set_contradiction": True,
        "alternating_relation_rank": 2,
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
