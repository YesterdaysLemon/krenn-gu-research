#!/usr/bin/env python3
"""Independent exact audit of the full-support 2+2 bridge obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def multiply(left, right):
    return sp.Matrix(
        tuple(
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in PAIRS
        )
    )


def map_matrix(left_rows, right_rows):
    return sp.Matrix.hstack(
        *(multiply(left, right) for right in right_rows for left in left_rows)
    )


def main() -> None:
    # Unequal weights and the reversed block order keep this independent
    # of the primary normal-form replay.
    p = sp.Matrix((0, 0, 2, 3))
    p_orthogonal = sp.Matrix((0, 0, 2, -3))
    q = sp.Matrix((5, 7, 0, 0))
    q_orthogonal = sp.Matrix((5, -7, 0, 0))
    assert multiply(p, p_orthogonal) == sp.zeros(6, 1)
    assert multiply(q, q_orthogonal) == sp.zeros(6, 1)
    bridge = multiply(p, q)
    assert all(bridge[index] != 0 for index in (1, 2, 3, 4))
    assert bridge[0] == 0
    assert bridge[5] == 0

    alpha, beta, coupling = sp.symbols(
        "alpha beta coupling", nonzero=True
    )
    first = alpha * p + coupling * q_orthogonal
    second = -coupling * p_orthogonal + beta * q
    assert (
        multiply(p_orthogonal, first)
        + multiply(q_orthogonal, second)
        == sp.zeros(6, 1)
    )

    paired_map = map_matrix(
        (p_orthogonal, q_orthogonal), (first, second)
    )
    assert paired_map.rank() == 3
    nonzero_minors = tuple(
        sp.factor(paired_map.extract(rows, columns).det())
        for rows in itertools.combinations(range(6), 3)
        for columns in itertools.combinations(range(4), 3)
    )
    coupling_minors = tuple(
        minor for minor in nonzero_minors if minor != 0
    )
    assert coupling_minors
    assert any(minor.subs(coupling, 0) == 0 for minor in coupling_minors)

    basis = sp.Matrix.hstack(p, p_orthogonal, q, q_orthogonal)
    assert basis.det() != 0
    first_coordinates = basis.inv() * first
    second_coordinates = basis.inv() * second
    assert first_coordinates == sp.Matrix((alpha, 0, 0, coupling))
    assert second_coordinates == sp.Matrix((0, -coupling, beta, 0))
    assert sp.Matrix.hstack(first, second, p).rank() == 3
    assert sp.Matrix.hstack(first, second, q).rank() == 3

    r = sp.symbols("r")
    factorization_checks = (
        multiply(p, q + r * p_orthogonal),
        multiply(q, p + r * q_orthogonal),
    )
    assert all(candidate == bridge for candidate in factorization_checks)

    # Directly replay the two-by-two exterior identity with new symbols.
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    left_block = sp.Matrix((x[0], x[1]))
    right_block = sp.Matrix((x[2], x[3]))
    left_prime = sp.Matrix((y[0], y[1]))
    right_prime = sp.Matrix((y[2], y[3]))
    cross = (
        left_block * right_prime.T + left_prime * right_block.T
    )
    exterior = (
        sp.Matrix.hstack(left_block, left_prime).det()
        * sp.Matrix.hstack(right_block, right_prime).det()
    )
    assert sp.factor(cross.det() + exterior) == 0

    result = {
        "weighted_cut": "verified",
        "crossed_graph_relation": "verified",
        "partner_rank": paired_map.rank(),
        "nonzero_rank_minors": len(coupling_minors),
        "anchor_lines_avoided": 2,
        "anchor_factorizations_replayed": len(factorization_checks),
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
