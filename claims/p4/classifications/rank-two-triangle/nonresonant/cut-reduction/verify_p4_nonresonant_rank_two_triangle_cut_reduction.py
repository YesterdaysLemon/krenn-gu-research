#!/usr/bin/env python3
"""Exact replay for the nonresonant triangle-to-cuts reduction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def catalecticant(q01, q02, q03, q12, q13, q23) -> sp.Matrix:
    return sp.Matrix(
        (
            (0, q23, q13, q12),
            (q23, 0, q03, q02),
            (q13, q03, 0, q01),
            (q12, q02, q01, 0),
        )
    )


def derive_catalecticant(coefficients) -> sp.Matrix:
    rows = tuple(
        frozenset(set(range(4)) - {missing}) for missing in range(4)
    )
    return sp.Matrix(
        4,
        4,
        lambda row, column: (
            coefficients[tuple(sorted(rows[row] - {column}))]
            if column in rows[row]
            else 0
        ),
    )


def three_by_three_minors(matrix: sp.Matrix):
    for rows in itertools.combinations(range(4), 3):
        for columns in itertools.combinations(range(4), 3):
            yield matrix.extract(rows, columns).det()


def main() -> None:
    b12, c12, b13, c13, b23, c23 = sp.symbols(
        "b12 c12 b13 c13 b23 c23"
    )
    omega = c12 * b13 * c23 + b12 * c13 * b23

    one_active = sp.Matrix(
        (
            (c12, b12, 0),
            (c13, 0, b13),
            (0, c23, b23),
        )
    )
    two_active = sp.Matrix(
        (
            (b12, c12, 0),
            (b13, 0, c13),
            (0, b23, c23),
        )
    )
    assert sp.factor(one_active.det()) == -omega
    assert sp.factor(two_active.det()) == -omega

    q01, q02, q03, q12, q13, q23 = sp.symbols(
        "q01 q02 q03 q12 q13 q23"
    )
    general = catalecticant(q01, q02, q03, q12, q13, q23)
    derived = derive_catalecticant(
        {
            (0, 1): q01,
            (0, 2): q02,
            (0, 3): q03,
            (1, 2): q12,
            (1, 3): q13,
            (2, 3): q23,
        }
    )
    assert derived == general
    assert general == general.T
    assert tuple(general.diagonal()) == (0, 0, 0, 0)

    triangle = catalecticant(0, 0, 0, q12, q13, q23)
    assert all(
        sp.expand(minor) == 0 for minor in three_by_three_minors(triangle)
    )
    triangle_sample = triangle.subs({q12: 2, q13: 3, q23: 5})
    assert triangle_sample.rank() == 2
    assert triangle_sample.nullspace() == [
        sp.Matrix((0, -sp.Rational(3, 5), 1, 0)),
        sp.Matrix((0, -sp.Rational(2, 5), 0, 1)),
    ]

    alpha0, alpha1, beta2, beta3 = sp.symbols(
        "alpha0 alpha1 beta2 beta3"
    )
    cut_values = {
        q01: 0,
        q02: alpha0 * beta2,
        q03: alpha0 * beta3,
        q12: alpha1 * beta2,
        q13: alpha1 * beta3,
        q23: 0,
    }
    two_two = general.subs(cut_values)
    assert sp.factor(
        cut_values[q02] * cut_values[q13]
        - cut_values[q03] * cut_values[q12]
    ) == 0
    assert all(
        sp.expand(minor) == 0 for minor in three_by_three_minors(two_two)
    )
    two_two_sample = two_two.subs(
        {alpha0: 2, alpha1: 3, beta2: 5, beta3: 7}
    )
    assert two_two_sample.rank() == 2

    result = {
        "holonomy_determinants": {
            "one_active": str(sp.factor(one_active.det())),
            "two_active": str(sp.factor(two_active.det())),
        },
        "catalecticant": {
            "symmetric": True,
            "zero_diagonal": True,
        },
        "cut_normal_forms": {
            "1+3_sample_rank": triangle_sample.rank(),
            "2+2_sample_rank": two_two_sample.rank(),
            "2+2_tetrad": "q02*q13-q03*q12=0",
        },
        "method": "symbolic determinants and rank-two cut normal forms",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
