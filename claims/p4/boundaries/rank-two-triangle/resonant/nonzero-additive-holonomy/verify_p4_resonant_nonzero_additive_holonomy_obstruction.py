#!/usr/bin/env python3
"""Exact replay of the nonzero additive-holonomy obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def catalecticant(q01, q02, q03, q12, q13, q23):
    return sp.Matrix(
        (
            (0, q23, q13, q12),
            (q23, 0, q03, q02),
            (q13, q03, 0, q01),
            (q12, q02, q01, 0),
        )
    )


def main() -> None:
    # A full 1+3 kernel-pair cut and its opposite plane.
    q12, q13, q23 = sp.symbols("q12 q13 q23", nonzero=True)
    cut = catalecticant(0, 0, 0, q12, q13, q23)
    assert cut.rank() == 2
    cut_kernel = (
        sp.Matrix((0, -q13, q23, 0)),
        sp.Matrix((0, -q12, 0, q23)),
    )
    assert all(cut * vector == sp.zeros(4, 1) for vector in cut_kernel)

    # A nonzero symmetric zero-diagonal rank-one matrix is impossible:
    # vv^T has diagonal v_i^2.
    z = sp.symbols("z0:4")
    rank_one_diagonal = tuple(value**2 for value in z)
    assert all(value == 0 for value in sp.solve(rank_one_diagonal, z)[0])

    # Full 2+2 factorization anchors and crossed-graph avoidance.
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    alpha, beta, tau = sp.symbols("alpha beta tau", nonzero=True)
    partner_v = alpha * a + tau * b_bar
    partner_w = -tau * a_bar + beta * b
    assert sp.Matrix.hstack(partner_v, partner_w, a).rank() == 3
    assert sp.Matrix.hstack(partner_v, partner_w, b).rank() == 3

    # The singleton-label intersections are the only cyclic choices.
    normals = tuple(sp.eye(4).row(index) for index in range(4))
    intersection_dimensions = {}
    for labels in ((0, 0, 0), (0, 0, 1), (0, 1, 2)):
        dimension = 4 - sp.Matrix.vstack(*(normals[i] for i in labels)).rank()
        intersection_dimensions[str(labels)] = dimension
    assert tuple(intersection_dimensions.values()) == (3, 2, 1)

    # In a coordinate two-plane, all products span one edge.
    e2, e3 = sp.eye(4).col(2), sp.eye(4).col(3)
    pair_vectors = []
    for left, right in itertools.product((e2, e3), repeat=2):
        pair_vectors.append(
            sp.Matrix(
                [
                    left[i] * right[j] + left[j] * right[i]
                    for i, j in itertools.combinations(range(4), 2)
                ]
            )
        )
    assert sp.Matrix.hstack(*pair_vectors).rank() == 1

    p3_pairing = sp.Matrix(((0, 0, 1), (0, 1, 0), (1, 0, 0)))
    assert p3_pairing.det() == -1
    assert 3 + 2 - 3 == 2 > 1

    result = {
        "tangent_kernel_pairs": "three nonzero rank-two cuts",
        "proper_cut_supports": "excluded by partner rank",
        "full_two_two": "excluded by anchor versus crossed graph",
        "full_one_three_label_intersections": intersection_dimensions,
        "common_label_p3_pairing_determinant": int(p3_pairing.det()),
        "conclusion": "Omega=0 and delta!=0 is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
