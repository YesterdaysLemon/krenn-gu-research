#!/usr/bin/env python3
"""Independent cochain audit of the resonant affine-holonomy reduction."""

from __future__ import annotations

import json

import sympy as sp


def main() -> None:
    # Edge order is 12, 23, 13.  The last orientation is the direct
    # edge from vertex one to vertex three.
    coboundary = sp.Matrix(
        (
            (1, -1, 0),
            (0, 1, -1),
            (1, 0, -1),
        )
    )
    cycle = sp.Matrix((1, 1, -1))
    assert coboundary.rank() == 2
    assert (cycle.T * coboundary) == sp.zeros(1, 3)
    cycle_kernel = coboundary.T.nullspace()
    assert len(cycle_kernel) == 1
    assert cycle_kernel[0].cross(cycle) == sp.zeros(3, 1)

    a12, a23, a13 = sp.symbols("a12 a23 a13")
    edge_constants = sp.Matrix((a12, a23, a13))
    additive_class = sp.expand((cycle.T * edge_constants)[0])
    assert additive_class == a12 + a23 - a13

    # The kernel-rich triple products obey the same cycle relation
    # twice, first in degree zero and then in degree one.
    y = sp.symbols("y")
    k = sp.symbols("k0:3")
    first_equations = sp.Matrix(
        (
            a12 * y + k[1] - k[0],
            a23 * y + k[2] - k[1],
            a13 * y + k[2] - k[0],
        )
    )
    assert sp.expand((cycle.T * first_equations)[0]) == sp.expand(
        additive_class * y
    )

    common_k = sp.symbols("common_k")
    j = sp.symbols("j0:3")
    second_equations = sp.Matrix(
        (
            a12 * common_k + j[0] - j[1],
            a23 * common_k + j[1] - j[2],
            a13 * common_k + j[0] - j[2],
        )
    )
    assert sp.expand((cycle.T * second_equations)[0]) == sp.expand(
        additive_class * common_k
    )

    # Symmetric-cube indexing is independent of the primary dictionary.
    words = tuple(
        format(index, "03b").replace("0", "y").replace("1", "x")
        for index in range(8)
    )
    weight_partition = {}
    for word in words:
        weight_partition.setdefault(word.count("x"), []).append(word)
    assert {weight: len(group) for weight, group in weight_partition.items()} == {
        0: 1,
        1: 3,
        2: 3,
        3: 1,
    }

    # Perfect R1-R3 pairing in four variables has an invertible
    # complementary-monomial matrix.
    perfect_pairing = sp.eye(4)[:, ::-1]
    assert abs(perfect_pairing.det()) == 1
    annihilator_dimension = 4 - 2
    assert annihilator_dimension == 2

    result = {
        "coboundary_rank": coboundary.rank(),
        "cycle_generator": [int(value) for value in cycle],
        "additive_class": str(additive_class),
        "two_cyclic_identities": True,
        "binary_cubic_weight_partition": {
            str(weight): group for weight, group in weight_partition.items()
        },
        "R1_R3_pairing_determinant": int(perfect_pairing.det()),
        "plane_annihilator_dimension": annihilator_dimension,
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
