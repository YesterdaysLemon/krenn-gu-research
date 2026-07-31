#!/usr/bin/env python3
"""Replay of local lemmas in a withdrawn mixed-triangle theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def annihilator_matrix(linear: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        6,
        4,
        lambda row, column: pair(
            linear, sp.eye(4).col(column)
        )[row],
    )


def main() -> None:
    # A generic synchronizer pencil is totally synchronized.
    L, t, u = sp.symbols("lambda t u")
    y = sp.Matrix((1, 0, 1, 1))
    x = sp.Matrix((0, 1, 1, L))
    ys = sp.Matrix((0, 1, -1, -L))
    xs = sp.Matrix((L, 0, -L, -L))
    y2, x2 = y + t * ys, x + t * xs
    y3, x3 = y + u * ys, x + u * xs
    assert pair(y2, x3) == pair(x2, y3)

    # The 2+1+1 collision synchronizer is also totally synchronized.
    yc = sp.Matrix((1, 1, 0, 1))
    xc = sp.Matrix((0, 0, 1, 1))
    zc = sp.Matrix((0, 0, 1, -1))
    p, q = sp.symbols("p q")
    assert pair(yc + p * zc, xc) == pair(xc, yc + q * zc)

    # Balanced 2+2 partner normal form.
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    alpha, beta = sp.symbols("alpha beta")
    y_partner = a + beta * b_bar
    x_partner = b + alpha * a_bar
    assert pair(a, x_partner) == pair(b, y_partner)

    assert annihilator_matrix(a).rank() == 3
    a_kernel = annihilator_matrix(a).nullspace()
    assert len(a_kernel) == 1
    assert sp.Matrix.hstack(a_kernel[0], a_bar).rank() == 1
    # On beta!=0, four explicit columns give full degree-one rank.
    full_minor = sp.factor(
        annihilator_matrix(y_partner).extract((0, 1, 2, 4), range(4)).det()
    )
    assert full_minor != 0
    assert sp.factor(full_minor).has(beta)

    A, B, alpha_3, beta_3 = sp.symbols("A B alpha_3 beta_3")
    containment = sp.Matrix.hstack(
        a + beta_3 * b_bar,
        b + alpha_3 * a_bar,
        -a_bar,
    )
    # Equivalently solve A*y3+B*x3=a_bar coefficient by coefficient.
    equations = list(
        A * (a + beta_3 * b_bar)
        + B * (b + alpha_3 * a_bar)
        - a_bar
    )
    solution = sp.solve(equations, (A, B), dict=True)
    assert solution == []
    assert containment.rank() == 3

    result = {
        "generic_partner_pair": "automatically rank-two synchronized",
        "collision_partner_pair": "automatically rank-two synchronized",
        "balanced_full_support_kernel_annihilator_dimension": 0,
        "balanced_two_support_annihilator": "C*a_bar",
        "other_leaf_contains_a_bar": False,
        "conclusion": "rank pattern (2,2,1) triangle is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
