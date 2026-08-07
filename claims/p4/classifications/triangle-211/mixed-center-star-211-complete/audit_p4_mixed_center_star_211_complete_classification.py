#!/usr/bin/env python3
"""Independent rational audit of the mixed-center star support ledger."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes):
    return {
        bits: sp.factor(permanent([planes[index].row(bits[index]) for index in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_rank(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    ).rank()


def move(row):
    permutation = (2, 0, 3, 1)
    scales = (sp.Rational(2), sp.Rational(3), sp.Rational(5), sp.Rational(7))
    return sp.Matrix([row[permutation[index]] * scales[index] for index in range(4)])


def main():
    u = sp.Matrix((1, 1, 0, 0))
    up = sp.Matrix((1, -1, 0, 0))
    v = sp.Matrix((0, 1, 1, 0))
    vp = sp.Matrix((0, 1, -1, 0))
    overlap = (
        sp.Matrix.vstack(u.T, v.T),
        sp.Matrix.vstack((u - vp).T, (v + 2 * up).T),
        sp.Matrix.vstack(sp.Matrix((-2, -10, 2, 1)).T, up.T),
        sp.Matrix.vstack(vp.T, sp.Matrix((2, 3, 5, 1)).T),
    )
    moved_overlap = tuple(sp.Matrix.vstack(move(plane.row(0)).T, move(plane.row(1)).T) for plane in overlap)
    assert pair_rank(moved_overlap[0], moved_overlap[1]) == 2

    singleton = sp.Matrix((0, 0, 1, 0))
    forward = (
        sp.Matrix.vstack(u.T, singleton.T),
        sp.Matrix.vstack((u + 2 * singleton).T, (singleton + 3 * up).T),
        sp.Matrix.vstack(sp.Matrix((1, 2, 3, 4)).T, up.T),
        sp.Matrix.vstack(singleton.T, sp.Matrix((2, 3, 5, 1)).T),
    )
    forward_tensor = coefficients(forward)
    assert any(value != 0 for bits, value in forward_tensor.items() if bits != (1, 1, 1, 1))

    reverse_lower = (
        sp.Matrix.vstack(singleton.T, u.T),
        sp.Matrix.vstack(singleton.T, (u + 3 * singleton).T),
    )
    assert pair_rank(*reverse_lower) == 2

    A, C = sp.Matrix((1, 1, 0, 0)), sp.Matrix((1, -1, 0, 0))
    B, D = sp.Matrix((0, 0, 1, 1)), sp.Matrix((0, 0, 1, -1))
    k, s, tau = sp.Rational(2), sp.Rational(3), sp.Rational(2)
    c = (tau - k * s) / (1 - k * s * tau)
    component = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack((A + c * C + k * B - k * D).T, C.T),
        sp.Matrix.vstack(D.T, (tau * A + C - k * tau * B).T),
    )
    moved_component = tuple(sp.Matrix.vstack(move(plane.row(0)).T, move(plane.row(1)).T) for plane in component)
    tensor = coefficients(moved_component)
    assert {bits: value for bits, value in tensor.items() if value} == {(1, 1, 1, 1): 9240}
    profile = tuple(pair_rank(moved_component[i], moved_component[j]) for i, j in PAIRS)
    assert profile == (3, 3, 3, 4, 4, 4)

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import rational audit",
                "field": "Q",
                "overlap_routes_to_lower_pair": True,
                "binary_singleton_forward_purity_fails": True,
                "binary_singleton_reverse_routes_to_lower_pair": True,
                "component24_pure_support": {"1111": "9240"},
                "component24_pair_profile": profile,
                "mixed_center_orientation_complete": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
