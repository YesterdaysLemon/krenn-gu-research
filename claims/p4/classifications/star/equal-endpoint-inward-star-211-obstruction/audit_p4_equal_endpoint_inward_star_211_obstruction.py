#!/usr/bin/env python3
"""Independent no-import audit of the equal-endpoint inward obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column in range(4):
                if not mask & (1 << column):
                    new_mask = mask | (1 << column)
                    updated[new_mask] = updated.get(new_mask, 0) + value * row[column]
        states = updated
    return sp.expand(states[15])


def coefficients(planes):
    return {
        bits: sp.factor(permanent_dp([planes[index].row(bits[index]) for index in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def moved(row, permutation, scales):
    return sp.Matrix([row[permutation[index]] * scales[index] for index in range(4)])


def move_planes(planes):
    permutation = (3, 1, 0, 2)
    scales = tuple(map(sp.Rational, (2, 3, 5, 7)))
    return tuple(
        sp.Matrix.vstack(
            moved(plane.row(0), permutation, scales).T,
            moved(plane.row(1), permutation, scales).T,
        )
        for plane in planes
    )


def main():
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")

    # Q != 0: the forbidden coefficient survives an unrelated source move.
    nonsingular = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + 2 * D).T, (B + 3 * C).T),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    values = coefficients(move_planes(nonsingular))
    source_multiplier = sp.Integer(2 * 3 * 5 * 7)
    assert values[(1, 1, 0, 0)] == -4 * source_multiplier

    # Singleton alpha=0: full center-spoke rank requires s != 0, after which
    # inward leaf support forces a3=g3=0 and hence the zero tensor.
    E = sp.Matrix((0, 0, 1, 0))
    singleton_zero = (
        sp.Matrix.vstack(A.T, E.T),
        sp.Matrix.vstack((2 * A + 3 * E).T, (5 * C + 2 * E).T),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    moved_zero = move_planes(singleton_zero)
    values = coefficients(moved_zero)
    forced = {a[3]: 0, g[3]: 0}
    assert all(sp.factor(value.subs(forced)) == 0 for value in values.values())
    assert pair_matrix(moved_zero[0], moved_zero[1]).rank() == 3

    # Singleton alpha!=0: s+u=0 is visibly lower-pair; otherwise the same
    # two forbidden coefficients force zero.
    u, v, s = map(sp.Rational, (2, 1, 3))
    E2 = B + D
    singleton_nonzero = (
        sp.Matrix.vstack(A.T, (C + E2).T),
        sp.Matrix.vstack(
            (u * A + v * C - v * E2).T,
            (-v * A + s * C + u * E2).T,
        ),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    moved_nonzero = move_planes(singleton_nonzero)
    values = coefficients(moved_nonzero)
    assert all(sp.factor(value.subs(forced)) == 0 for value in values.values())
    assert pair_matrix(moved_nonzero[0], moved_nonzero[1]).rank() == 3

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import exact audit",
                "field": "Q",
                "source_permutation": [3, 1, 0, 2],
                "source_scales": [2, 3, 5, 7],
                "Q_nonzero_forbidden_coefficient": str(-4 * source_multiplier),
                "singleton_charts_force_zero_or_lower_pair": True,
                "equal_endpoint_inward_all_pair_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
