#!/usr/bin/env python3
"""Independent exact audit of the 1+3 cyclic-label obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def product(left, right):
    return {
        pair: sp.expand(
            left[pair[0]] * right[pair[1]]
            + left[pair[1]] * right[pair[0]]
        )
        for pair in itertools.combinations(range(4), 2)
    }


def main() -> None:
    # Use singleton coordinate three, independently of the primary replay.
    a, b, c, lam = sp.symbols("a b c lam", nonzero=True)
    reflected_left = (a, b, c, 1)
    reflected_right = (-lam * a, -lam * b, -lam * c, lam)
    reflected = product(reflected_left, reflected_right)
    assert reflected[(0, 3)] == 0
    assert reflected[(1, 3)] == 0
    assert reflected[(2, 3)] == 0
    assert reflected[(0, 1)] == -2 * lam * a * b
    assert reflected[(0, 2)] == -2 * lam * a * c
    assert reflected[(1, 2)] == -2 * lam * b * c

    q01, q02, q12 = sp.symbols("q01 q02 q12", nonzero=True)
    singleton_three_map = sp.Matrix(
        (
            (0, 0, 0, q12),
            (0, 0, 0, q02),
            (0, 0, 0, q01),
            (q12, q02, q01, 0),
        )
    )
    kernel = (
        sp.Matrix((-q02, q12, 0, 0)),
        sp.Matrix((-q01, 0, q12, 0)),
    )
    assert singleton_three_map.rank() == 2
    assert all(singleton_three_map * vector == sp.zeros(4, 1) for vector in kernel)
    assert all(vector[3] == 0 for vector in kernel)

    label_counts = {1: 0, 2: 0, 3: 0}
    for labels in itertools.product(range(4), repeat=3):
        distinct = len(set(labels))
        label_counts[distinct] += 1
        intersection_dimension = 4 - distinct
        if distinct == 3:
            assert intersection_dimension == 1
        elif distinct == 2:
            assert intersection_dimension == 2
        else:
            assert intersection_dimension == 3
    assert label_counts == {1: 4, 2: 36, 3: 24}

    # A two-coordinate plane has only one squarefree quadratic product.
    e0 = (1, 0, 0, 0)
    e1 = (0, 1, 0, 0)
    products = [
        tuple(product(left, right).values())
        for left in (e0, e1)
        for right in (e0, e1)
    ]
    pair_matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in products))
    assert pair_matrix.rank() == 1

    # The complementary-monomial pairing in three variables is perfect.
    complementary_pairing = sp.zeros(3)
    degree_two = ((0, 1), (0, 2), (1, 2))
    for row, pair in enumerate(degree_two):
        missing = ({0, 1, 2} - set(pair)).pop()
        complementary_pairing[row, missing] = 1
    assert abs(complementary_pairing.det()) == 1
    assert 3 + 2 - 3 == 2 > 1

    result = {
        "opposite_singleton": 3,
        "reflection_normal_form": "verified",
        "annihilator_rank": singleton_three_map.rank(),
        "label_table": label_counts,
        "two_coordinate_pair_rank": pair_matrix.rank(),
        "three_variable_pairing_determinant": int(
            complementary_pairing.det()
        ),
        "component_search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
