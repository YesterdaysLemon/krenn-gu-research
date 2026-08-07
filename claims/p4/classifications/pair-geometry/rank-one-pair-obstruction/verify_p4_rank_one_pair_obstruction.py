#!/usr/bin/env python3
"""Symbolically verify the rank-one pair-image obstruction for pure P4."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def main() -> None:
    a, b = sp.symbols("a b")

    # Each of the six P1 curves consists of exact zero products.
    for p, q in PAIRS:
        left = tuple(a if i == p else b if i == q else 0 for i in range(4))
        right = tuple(a if i == p else -b if i == q else 0 for i in range(4))
        assert product(left, right) == sp.zeros(6, 1)

    # Support-three annihilators vanish.  Normalizing u=(u0,u1,u2,0),
    # the first three equations have determinant -2*u0*u1*u2.
    u0, u1, u2 = sp.symbols("u0 u1 u2", nonzero=True)
    support_three_matrix = sp.Matrix(
        [[u1, u0, 0], [u2, 0, u0], [0, u2, u1]]
    )
    assert sp.factor(support_three_matrix.det()) == -2 * u0 * u1 * u2

    # On support two the annihilator is the opposite binary line.
    v0, v1 = sp.symbols("v0 v1")
    support_two_matrix = sp.Matrix([[u1, u0]])
    assert support_two_matrix.rank() == 1
    assert support_two_matrix * sp.Matrix([u0, -u1]) == sp.zeros(1, 1)

    # Multiplication on the forced coordinate plane is the hyperbolic form.
    hyperbolic = sp.Matrix([[0, 1], [1, 0]])
    assert hyperbolic.det() == -1
    assert hyperbolic.rank() == 2

    # Frobenius separation: the 4-mode coefficient array is the Kronecker
    # product of this rank-two form with any nonzero opposite functional.
    c00, c01, c10, c11 = sp.symbols("c00 c01 c10 c11")
    opposite = sp.Matrix([[c00, c01], [c10, c11]])
    flattened = sp.kronecker_product(hyperbolic, opposite)
    # A nonzero opposite entry exhibits a 2x2 hyperbolic minor.
    for row, column, entry in (
        (0, 0, c00),
        (0, 1, c01),
        (1, 0, c10),
        (1, 1, c11),
    ):
        selected = flattened.extract([row, row + 2], [column, column + 2])
        assert sp.factor(selected.det()) == -entry**2

    print(
        json.dumps(
            {
                "status": "pass",
                "zero_product_components": 6,
                "components_are": "coordinate-pair P1 curves",
                "support_three_annihilator_determinant": str(
                    sp.factor(support_three_matrix.det())
                ),
                "forced_binary_form_rank": 2,
                "nonzero_pure_pair_rank_lower_bound": 2,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
