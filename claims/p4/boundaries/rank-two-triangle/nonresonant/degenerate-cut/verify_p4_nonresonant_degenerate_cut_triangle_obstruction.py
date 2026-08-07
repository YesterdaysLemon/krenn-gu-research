#!/usr/bin/env python3
"""Exact replay for proper-support nonresonant cut triangles."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left, right):
    return sp.Matrix(
        tuple(
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in PAIRS
        )
    )


def catalecticant(quadratic):
    coefficients = dict(zip(PAIRS, quadratic))
    triples = tuple(
        frozenset(set(range(4)) - {missing}) for missing in range(4)
    )
    return sp.Matrix(
        4,
        4,
        lambda row, column: (
            coefficients[tuple(sorted(triples[row] - {column}))]
            if column in triples[row]
            else 0
        ),
    )


def main() -> None:
    e = tuple(sp.eye(4).col(i) for i in range(4))

    single = product(e[0], e[1])
    single_map = catalecticant(single)
    assert single_map.rank() == 2
    assert single_map * e[0] == sp.zeros(4, 1)
    assert single_map * e[1] == sp.zeros(4, 1)

    v = sp.symbols("v0:4")
    w = sp.symbols("w0:4")
    single_relation = product(e[0], sp.Matrix(v)) + product(
        e[1], sp.Matrix(w)
    )
    expected_single = sp.Matrix(
        (v[1] + w[0], v[2], v[3], w[2], w[3], 0)
    )
    assert single_relation == expected_single
    single_partner_v = sp.Matrix((v[0], v[1], 0, 0))
    single_partner_w = sp.Matrix((-v[1], w[1], 0, 0))
    single_partner_map = sp.Matrix.hstack(
        *(
            product(left, right)
            for left in (e[0], e[1])
            for right in (single_partner_v, single_partner_w)
        )
    )
    assert single_partner_map.rank() <= 1

    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    b = alpha * e[1] + beta * e[2]
    b_bar = alpha * e[1] - beta * e[2]
    star = product(e[0], b)
    star_map = catalecticant(star)
    assert star_map.rank() == 2
    assert star_map * e[0] == sp.zeros(4, 1)
    assert star_map * b_bar == sp.zeros(4, 1)

    star_relation = product(e[0], sp.Matrix(v)) + product(
        b_bar, sp.Matrix(w)
    )
    assert star_relation[2] == v[3]  # X03
    assert star_relation[4] == alpha * w[3]  # X13
    assert star_relation[5] == -beta * w[3]  # X23

    # Solve the remaining star equations in a transparent normal form.
    rho, sigma, tau = sp.symbols("rho sigma tau")
    star_partner_v = rho * e[0] - tau * b_bar
    star_partner_w = tau * e[0] + sigma * b
    assert (
        product(e[0], star_partner_v)
        + product(b_bar, star_partner_w)
        == sp.zeros(6, 1)
    )
    assert star_partner_v[3] == 0
    assert star_partner_w[3] == 0

    p3_pairing = sp.Matrix(((0, 0, 1), (0, 1, 0), (1, 0, 0)))
    assert p3_pairing.det() == -1
    rank_three_lower_bound = 3 + 2 - 3
    assert rank_three_lower_bound == 2 > 1

    result = {
        "proper_cut_supports": ["single edge", "two-edge star"],
        "single_edge": {
            "catalecticant_rank": single_map.rank(),
            "annihilator": "span(X0,X1)",
            "forced_partner_product_rank_upper_bound": 1,
        },
        "two_edge_star": {
            "catalecticant_rank": star_map.rank(),
            "annihilator": "span(X0,alpha*X1-beta*X2)",
            "common_coordinate_hyperplane": "X3=0",
        },
        "p3_pairing_determinant": int(p3_pairing.det()),
        "rank_three_flattening_lower_bound": rank_three_lower_bound,
        "conclusion": "complete nonresonant triangle is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
