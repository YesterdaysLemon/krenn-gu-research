#!/usr/bin/env python3
"""Verify that the all-rank-two-relation triangle is in component eleven."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pluecker(rows: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [rows[0, i] * rows[1, j] - rows[0, j] * rows[1, i] for i, j in PAIRS]
    )


def main() -> None:
    alpha_1, alpha_2, alpha_3 = sp.symbols(
        "alpha_1 alpha_2 alpha_3", nonzero=True
    )
    a = sp.Matrix([1, 1, 0, 0])
    a_bar = sp.Matrix([1, -1, 0, 0])
    b = sp.Matrix([0, 0, 1, 1])
    b_bar = sp.Matrix([0, 0, 1, -1])

    target = [
        sp.Matrix.vstack(b_bar.T, a_bar.T),
        sp.Matrix.vstack(a.T, (b + alpha_1 * a_bar).T),
        sp.Matrix.vstack(a.T, (b + alpha_2 * a_bar).T),
        sp.Matrix.vstack(a.T, (b + alpha_3 * a_bar).T),
    ]
    source_scaling = sp.diag(1, 1, alpha_1, alpha_1)
    transformed = [matrix * source_scaling for matrix in target]

    r = alpha_2 / alpha_1
    q = alpha_1 / alpha_3
    component_eleven = [
        sp.Matrix.vstack(a.T, (a_bar + q * b).T),
        sp.Matrix.vstack(a.T, (a_bar + b).T),
        sp.Matrix.vstack(a.T, (r * a_bar + b).T),
        sp.Matrix.vstack(b_bar.T, a_bar.T),
    ]
    reordered = [
        component_eleven[3],
        component_eleven[1],
        component_eleven[2],
        component_eleven[0],
    ]
    for left, right in zip(transformed, reordered):
        left_pluecker = pluecker(left)
        right_pluecker = pluecker(right)
        nonzero = next(index for index, value in enumerate(right_pluecker) if value != 0)
        scale = sp.simplify(left_pluecker[nonzero] / right_pluecker[nonzero])
        assert sp.simplify(left_pluecker - scale * right_pluecker) == sp.zeros(6, 1)

    factor_identity = sp.factor(
        1 + q * (r + 1)
        - (alpha_1 + alpha_2 + alpha_3) / alpha_3
    )
    assert factor_identity == 0

    target_planes = tuple(
        tuple(tuple(row) for row in matrix.tolist()) for matrix in target
    )
    coefficients = {
        bits: sp.factor(
            permanent(tuple(target_planes[mode][bits[mode]] for mode in range(4)))
        )
        for bits in BITS
    }
    expected = {(1, 1, 1, 1): -4 * (alpha_1 + alpha_2 + alpha_3)}
    for bits, value in coefficients.items():
        assert sp.factor(value - expected.get(bits, 0)) == 0

    sample = {alpha_1: 1, alpha_2: 2, alpha_3: 4}
    sampled = tuple(
        tuple(
            tuple(sp.sympify(entry).subs(sample) for entry in row)
            for row in plane
        )
        for plane in target_planes
    )
    profile = []
    relation_ranks = []
    for i, j in itertools.combinations(range(4), 2):
        matrix = pair_matrix(sampled[i], sampled[j])
        profile.append(matrix.rank())
        kernel = matrix.nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, kernel[0]).rank())
    assert profile == [3, 3, 3, 3, 3, 3]
    assert relation_ranks == [1, 1, 1, 2, 2, 2]

    print(
        json.dumps(
            {
                "status": "pass",
                "dense_parameter_map": {
                    "p": 0,
                    "r": "alpha_2/alpha_1",
                    "q": "alpha_1/alpha_3",
                },
                "mode_order": [3, 1, 2, 0],
                "nonzero_factor_identity": "(alpha_1+alpha_2+alpha_3)/alpha_3",
                "pair_profile": [int(value) for value in profile],
                "relation_ranks": [int(value) for value in relation_ranks],
                "containing_component": 11,
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
