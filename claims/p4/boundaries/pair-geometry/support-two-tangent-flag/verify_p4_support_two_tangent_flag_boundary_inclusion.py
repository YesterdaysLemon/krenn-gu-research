#!/usr/bin/env python3
"""Verify the polar-flag degeneration into the known P4 sixfold."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def pluecker(rows: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [rows[0, i] * rows[1, j] - rows[0, j] * rows[1, i] for i, j in PAIRS]
    )


def main() -> None:
    epsilon = sp.symbols("epsilon")
    alpha, beta, tau, sigma = sp.symbols("alpha beta tau sigma", nonzero=True)
    big_b, big_c, h0, d0 = sp.symbols("B C h0 D")
    s0 = h0 + d0
    total_s = sigma / epsilon + s0
    h = sigma / epsilon + h0
    little_b = epsilon / sigma + big_b * epsilon**2
    little_e = epsilon / sigma + big_c * epsilon**2

    v0 = sp.Matrix(
        [[alpha * epsilon, 0, 0, -1], [0, 0, beta * epsilon, 1]]
    )
    v3 = sp.Matrix(
        [[alpha * epsilon, 0, 0, 1], [0, 0, beta * epsilon, -1]]
    )
    v1 = sp.Matrix(
        [
            [alpha * epsilon, little_b * tau, 0, 1 - little_b * h],
            [0, little_e * tau, beta * epsilon, 1 - little_e * h],
        ]
    )
    v2 = sp.Matrix(
        [
            [alpha * epsilon, 0, -beta * epsilon, 0],
            [0, tau, -total_s * beta * epsilon, -d0],
        ]
    )

    tangent = sp.Matrix([0, 0, alpha, 0, 0, beta])
    assert sp.simplify(pluecker(v0) / epsilon).subs(epsilon, 0) == tangent
    assert sp.simplify(pluecker(v3) / epsilon).subs(epsilon, 0) == -tangent

    limit_v1 = sp.simplify(pluecker(v1) / epsilon**2).subs(epsilon, 0)
    expected_v1 = sp.Matrix(
        [
            alpha * tau / sigma,
            alpha * beta,
            -alpha * (big_c * sigma**2 + h0) / sigma,
            beta * tau / sigma,
            tau * (big_b - big_c),
            beta * (big_b * sigma**2 + h0) / sigma,
        ]
    )
    assert sp.simplify(limit_v1 - expected_v1) == sp.zeros(6, 1)

    lam = 2 / sigma
    p = -1 / (sigma * (big_b - big_c))
    q = 2 * p * (big_c * sigma**2 + h0) / sigma - 1
    e = sp.Matrix([0, 0, 0, 1])
    capital_h = sp.Matrix([alpha, 0, beta, 0])
    capital_s = sp.Matrix([alpha, 0, -beta, 0])
    capital_z = sp.Matrix([0, tau, 0, 0])
    target_a = sp.Matrix.hstack(
        e + p * capital_s,
        capital_h + lam * capital_z + q * capital_s,
    ).T
    assert sp.simplify(limit_v1 - pluecker(target_a) / (2 * p)) == sp.zeros(6, 1)

    limit_v2 = sp.simplify(pluecker(v2) / epsilon).subs(epsilon, 0)
    expected_v2 = sp.Matrix(
        [alpha * tau, -alpha * beta * sigma, -alpha * d0, beta * tau, 0, beta * d0]
    )
    assert sp.simplify(limit_v2 - expected_v2) == sp.zeros(6, 1)
    r = 2 * d0 / sigma
    target_b = sp.Matrix.hstack(
        capital_s,
        capital_h - lam * capital_z + r * e,
    ).T
    assert sp.simplify(limit_v2 + sigma * pluecker(target_b) / 2) == sp.zeros(6, 1)

    # Rational arc for (p,q,lambda,r)=(1,2,1,3).
    rational = {
        alpha: 1,
        beta: 1,
        tau: 1,
        sigma: 2,
        d0: 3,
        big_b: sp.Rational(-1, 2),
        big_c: 0,
        h0: 3,
    }
    assert sp.simplify(p.subs(rational)) == 1
    assert sp.simplify(q.subs(rational)) == 2
    assert sp.simplify(lam.subs(rational)) == 1
    assert sp.simplify(r.subs(rational)) == 3

    print(
        json.dumps(
            {
                "status": "pass",
                "tangent_edge_valuation": 1,
                "flag_plane_valuations": [2, 1],
                "dense_target_parameters": ["p", "q", "lambda", "r"],
                "rational_target": [1, 2, 1, 3],
                "containing_component_dimension": 6,
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
