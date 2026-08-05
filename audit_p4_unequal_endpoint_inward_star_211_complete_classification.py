#!/usr/bin/env python3
"""Independent no-import audit of the unequal inward support ledger."""

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


def transform(row):
    permutation = (2, 0, 3, 1)
    scales = tuple(map(sp.Rational, (2, 3, 5, 7)))
    return sp.Matrix([row[permutation[index]] * scales[index] for index in range(4)])


def moved(planes):
    return tuple(
        sp.Matrix.vstack(transform(plane.row(0)).T, transform(plane.row(1)).T)
        for plane in planes
    )


def flattening(tensor, mode):
    other = tuple(index for index in range(4) if index != mode)
    matrix = sp.zeros(2, 8)
    for row in (0, 1):
        for column, tail in enumerate(itertools.product((0, 1), repeat=3)):
            bits = [0, 0, 0, 0]
            bits[mode] = row
            for index, bit in zip(other, tail):
                bits[index] = bit
            matrix[row, column] = tensor[tuple(bits)]
    return matrix


def main():
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))

    # Independent projective boundary point g=0 on the component-25
    # hypersurface.  It remains pure and all-pair after the source move.
    a, e, g, j, k, s = map(sp.Rational, (1, 1, 0, 1, 2, 1))
    hypersurface = (
        (e * j + a * g * k**2) * (a * g + e * j * s**2)
        - (a * j + e * g) ** 2
    )
    assert hypersurface == 0
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack(C.T, (a * A + e * B - a * k * D).T),
        sp.Matrix.vstack(D.T, (g * A - j * s * C + j * B).T),
    )
    planes = moved(planes)
    tensor = coefficients(planes)
    assert [flattening(tensor, mode).rank() for mode in range(4)] == [1, 1, 1, 1]
    profile = tuple(
        pair_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )
    assert profile == (3, 3, 3, 4, 4, 4)

    # Overlapping binary support: the only ways to retain a forbidden leaf
    # coefficient make the center pair rank at most two.
    u = sp.Matrix((1, 1, 0, 0))
    up = sp.Matrix((1, -1, 0, 0))
    v = sp.Matrix((0, 1, 1, 0))
    vp = sp.Matrix((0, 1, -1, 0))
    for kk, ss in ((-1, 2), (2, 1)):
        center = moved(
            (
                sp.Matrix.vstack(u.T, v.T),
                sp.Matrix.vstack((u + kk * vp).T, (v + ss * up).T),
            )
        )
        assert pair_matrix(center[0], center[1]).rank() <= 2

    print(
        json.dumps(
            {
                "status": "pass",
                "role": "independent no-import exact audit",
                "field": "Q",
                "source_permutation": [2, 0, 3, 1],
                "source_scales": [2, 3, 5, 7],
                "component25_projective_g_zero_boundary": True,
                "boundary_pair_profile": profile,
                "overlap_rank_drop_branches": ["k=-1", "s=1"],
                "unequal_inward_support_ledger_complete": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
