#!/usr/bin/env python3
"""Exact replay of the full-support 2+2 triangle obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            left[i] * right[j] + left[j] * right[i]
            for i, j in PAIRS
        ]
    )


def multiplication_map(left_basis, right_basis) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(product(left, right) for left in left_basis for right in right_basis)
    )


def catalecticant(quadratic: sp.Matrix) -> sp.Matrix:
    coefficients = dict(zip(PAIRS, quadratic))
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


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    source_basis = sp.Matrix.hstack(a, a_bar, b, b_bar)
    assert source_basis.det() == 4
    assert product(a, a_bar) == sp.zeros(6, 1)
    assert product(b, b_bar) == sp.zeros(6, 1)
    assert product(a, a) != sp.zeros(6, 1)
    assert product(b, b) != sp.zeros(6, 1)

    cut = product(a, b)
    cut_catalecticant = catalecticant(cut)
    assert cut_catalecticant.rank() == 2
    assert cut_catalecticant * a_bar == sp.zeros(4, 1)
    assert cut_catalecticant * b_bar == sp.zeros(4, 1)

    # The exterior identity behind the anchor lemma.
    u0, u1, u2, u3, v0, v1, v2, v3 = sp.symbols(
        "u0 u1 u2 u3 v0 v1 v2 v3"
    )
    u_a = sp.Matrix((u0, u1))
    u_b = sp.Matrix((u2, u3))
    v_a = sp.Matrix((v0, v1))
    v_b = sp.Matrix((v2, v3))
    cross = u_a * v_b.T + v_a * u_b.T
    wedge_a = sp.Matrix.hstack(u_a, v_a).det()
    wedge_b = sp.Matrix.hstack(u_b, v_b).det()
    assert sp.factor(cross.det()) == sp.factor(-wedge_a * wedge_b)

    alpha, beta, tau = sp.symbols("alpha beta tau", nonzero=True)
    v = alpha * a + tau * b_bar
    w = -tau * a_bar + beta * b
    relation = sp.expand(product(a_bar, v) + product(b_bar, w))
    assert relation == sp.zeros(6, 1)

    partner_map = multiplication_map((a_bar, b_bar), (v, w))
    assert partner_map.rank() == 3
    selected_rows = (0, 2, 5)  # X01, X03, X23
    selected_columns = (0, 1, 2)
    rank_minor = sp.factor(
        partner_map.extract(selected_rows, selected_columns).det()
    )
    assert rank_minor == -4 * tau**3

    assert sp.Matrix.hstack(v, w, a).rank() == 3
    assert sp.Matrix.hstack(v, w, b).rank() == 3

    s, t = sp.symbols("s t")
    anchor_factorizations = (
        product(b, a + t * b_bar),
        product(a + t * b_bar, b),
        product(a, b + s * a_bar),
        product(b + s * a_bar, a),
    )
    assert all(candidate == cut for candidate in anchor_factorizations)

    result = {
        "cut": {
            "type": "full-support 2+2",
            "catalecticant_rank": cut_catalecticant.rank(),
            "annihilator": "span(a_bar,b_bar)",
        },
        "anchor_lemma": {
            "exterior_identity": "det(cross)=-wedge_A*wedge_B",
            "factorization_sheets_replayed": len(anchor_factorizations),
        },
        "crossed_graph_partner": {
            "normal_form": (
                "span(alpha*a+tau*b_bar,-tau*a_bar+beta*b)"
            ),
            "rank_three_minor": str(rank_minor),
            "avoids_anchor_a": True,
            "avoids_anchor_b": True,
        },
        "conclusion": (
            "no full-support 2+2 bridge in a nonresonant "
            "rank-two-relation triangle"
        ),
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
