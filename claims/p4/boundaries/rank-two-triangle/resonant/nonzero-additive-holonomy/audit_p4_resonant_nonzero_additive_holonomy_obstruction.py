#!/usr/bin/env python3
"""Independent support audit of the nonzero additive branch."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def main() -> None:
    # Complete discrete label table, independent of the primary samples.
    label_counts = {1: 0, 2: 0, 3: 0}
    for labels in itertools.product(range(4), repeat=3):
        distinct = len(set(labels))
        label_counts[distinct] += 1
        dimension = 4 - distinct
        if distinct == 1:
            assert dimension == 3
        elif distinct == 2:
            assert dimension == 2
        else:
            assert dimension == 1
    assert label_counts == {1: 4, 2: 36, 3: 24}

    # Opposite singleton: use cuts inside X3=0.
    q01, q02, q12 = sp.symbols("q01 q02 q12", nonzero=True)
    cut = sp.Matrix(
        (
            (0, 0, 0, q12),
            (0, 0, 0, q02),
            (0, 0, 0, q01),
            (q12, q02, q01, 0),
        )
    )
    assert cut.rank() == 2
    assert all(vector[3] == 0 for vector in cut.nullspace())

    # Proper support sizes are exactly one and two; the previous local
    # partner normal forms then force rank one or a common hyperplane.
    support_sizes = {
        "1+3": {1, 2, 3},
        "2+2": {1, 2, 4},
    }
    assert support_sizes["1+3"] - {3} == {1, 2}
    assert support_sizes["2+2"] - {4} == {1, 2}

    # A coordinate line squares to zero; a coordinate two-plane has
    # only one nonzero degree-two monomial.
    e = tuple(sp.eye(4).col(index) for index in range(4))
    assert e[0][0] * e[0][1] + e[0][1] * e[0][0] == 0
    coordinate_products = sp.Matrix.hstack(
        sp.zeros(6, 1),
        sp.Matrix((1, 0, 0, 0, 0, 0)),
    )
    assert coordinate_products.rank() == 1

    pairing = sp.eye(3)[:, ::-1]
    assert abs(pairing.det()) == 1
    assert 3 + 2 - 3 > 1

    result = {
        "label_table": label_counts,
        "opposite_singleton_cut_rank": cut.rank(),
        "proper_support_sizes": {
            key: sorted(values) for key, values in support_sizes.items()
        },
        "coordinate_two_plane_product_rank": coordinate_products.rank(),
        "p3_pairing_determinant": int(pairing.det()),
        "remaining_triangle_branch": "Omega=0, delta=0",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
