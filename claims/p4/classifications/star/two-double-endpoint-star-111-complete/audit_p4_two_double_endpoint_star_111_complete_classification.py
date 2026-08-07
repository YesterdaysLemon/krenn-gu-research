#!/usr/bin/env python3
"""Independent no-import audit of the two-double-endpoint star theorem."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
SOURCE_PAIRS = tuple(itertools.combinations(range(4), 2))
MODE_PAIRS = tuple(itertools.combinations(range(4), 2))


def subset_permanent(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        next_states = {}
        for mask, value in states.items():
            for coordinate, entry in enumerate(row):
                if mask & (1 << coordinate):
                    continue
                new_mask = mask | (1 << coordinate)
                next_states[new_mask] = sp.expand(
                    next_states.get(new_mask, 0) + value * entry
                )
        states = next_states
    return sp.expand(states.get(15, 0))


def tensor(planes):
    return {
        bits: subset_permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in WORDS
    }


def product(left, right):
    return [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in SOURCE_PAIRS]


def pair_matrix(left, right):
    columns = [
        product(left[i], right[j]) for i, j in itertools.product(range(2), repeat=2)
    ]
    return sp.Matrix(6, 4, lambda row, column: columns[column][row])


def profile(planes):
    return tuple(pair_matrix(planes[i], planes[j]).rank() for i, j in MODE_PAIRS)


def transform(row):
    scaled = tuple(
        sp.Rational(scale) * entry
        for scale, entry in zip((2, 3, 5, 7), row, strict=True)
    )
    # Source permutation (0,1,2,3) -> (2,0,3,1).
    return (scaled[2], scaled[0], scaled[3], scaled[1])


def transformed(planes):
    return tuple(tuple(transform(row) for row in plane) for plane in planes)


def pure_anchor(planes):
    values = tensor(planes)
    assert values[(1, 1, 1, 1)] != 0
    assert all(value == 0 for bits, value in values.items() if bits != (1, 1, 1, 1))
    return values[(1, 1, 1, 1)]


def relation_rank(planes, left, right):
    matrix = pair_matrix(planes[left], planes[right])
    assert matrix.rank() == 3
    return sp.Matrix(2, 2, tuple(matrix.nullspace()[0])).rank()


def add(*rows):
    return tuple(sum(row[index] for row in rows) for index in range(4))


def scale(coefficient, row):
    return tuple(coefficient * entry for entry in row)


def main():
    Z = Fraction(0)
    O = Fraction(1)
    e0 = (O, Z, Z, Z)
    e1 = (Z, O, Z, Z)
    e2 = (Z, Z, O, Z)
    e3 = (Z, Z, Z, O)
    A = add(e0, e1)
    C = add(e0, scale(-1, e1))
    B = add(e2, e3)
    D = add(e2, scale(-1, e3))

    # Center-kernel binary support: a component-21 endpoint chart.
    center21 = (
        (A, C),
        (C, add(B, A)),
        (C, add(B, scale(2, A))),
        (D, C),
    )
    center21 = transformed(center21)
    anchor21 = pure_anchor(center21)
    profile21 = profile(center21)
    assert min(profile21) >= 3

    # Center-kernel singleton support: the integral component-18 sample,
    # reordered so that the fourth active row is the common singleton.
    ell = (Z, O, Fraction(-3), Fraction(-2))
    v1 = (Z, O, Fraction(-1), Fraction(-1))
    v2 = (Z, O, Fraction(-1), Fraction(2))
    v3 = (Z, O, Fraction(3), Fraction(-1))
    center18 = transformed(((e0, v1), (e0, v2), (e0, v3), (ell, e0)))
    anchor18 = pure_anchor(center18)
    profile18 = profile(center18)
    assert min(profile18) >= 3

    # Reverse disjoint binary support: transverse mixed-chain/component 8.
    reverse8 = transformed(
        (
            (A, B),
            (C, add(A, scale(2, B), D)),
            (C, add(A, scale(Fraction(-1, 2), B), scale(-1, D))),
            (D, A),
        )
    )
    anchor8 = pure_anchor(reverse8)
    profile8 = profile(reverse8)
    assert profile8 == (3, 3, 3, 4, 3, 3)
    assert all(
        relation_rank(reverse8, *edge) == 1
        for edge in ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3))
    )

    # Singleton double support, disjoint binary reverse pair, gamma != 0:
    # the fully kernel-kernel triangle branch in component 16.
    E12 = add(e1, e2)
    F12 = add(e1, scale(-1, e2))
    component16 = transformed(
        (
            (e0, E12),
            (e0, add(e2, scale(-1, e3))),
            (e0, add(e1, scale(-1, e3))),
            (F12, add(e0, E12, scale(2, e3))),
        )
    )
    anchor16 = pure_anchor(component16)
    profile16 = profile(component16)
    assert profile16 == (3, 3, 3, 3, 4, 4)
    assert all(
        relation_rank(component16, *edge) == 1 for edge in ((0, 1), (0, 2), (1, 2))
    )

    # The gamma=0 subbranch has all four planes through the singleton and is
    # component 18.  This sample also checks the projective row placement.
    singleton18 = transformed(
        (
            (e0, E12),
            (e0, add(e1, e3)),
            (e0, add(e2, e3)),
            (F12, e0),
        )
    )
    anchor_singleton18 = pure_anchor(singleton18)
    profile_singleton18 = profile(singleton18)
    assert min(profile_singleton18) == 2

    # Independent symbolic subset-DP checks of representative empty-orbit
    # syzygies.  These do not import or call the primary verifier.
    a1, b1, d1, a2, b2, d2, a3, b3, d3 = sp.symbols("a1 b1 d1 a2 b2 d2 a3 b3 d3")
    same = tensor(
        (
            (tuple(A), tuple(C)),
            (tuple(C), tuple(add(scale(a1, A), scale(b1, B), scale(d1, D)))),
            (tuple(C), tuple(add(scale(a2, A), scale(b2, B), scale(d2, D)))),
            (tuple(A), tuple(add(scale(a3, C), scale(b3, B), scale(d3, D)))),
        )
    )
    assert sp.factor(same[(1, 1, 1, 1)] + a3 * same[(0, 1, 1, 0)]) == 0

    u1, v1s, w1, u2, v2s, w2, c0, c1s, c3 = sp.symbols("u1 v1s w1 u2 v2s w2 c0 c1s c3")
    outside = tensor(
        (
            (tuple(A), tuple(e2)),
            (tuple(C), tuple(add(scale(u1, A), scale(v1s, B), scale(w1, D)))),
            (tuple(C), tuple(add(scale(u2, A), scale(v2s, B), scale(w2, D)))),
            (tuple(e2), (c0, c1s, 0, c3)),
        )
    )
    X = u1 * (v2s - w2) + u2 * (v1s - w1)
    assert sp.factor(outside[(1, 0, 0, 1)] + 2 * c3) == 0
    assert sp.factor(outside[(0, 1, 1, 0)] - 2 * X) == 0
    assert sp.factor(outside[(1, 1, 1, 1)].subs(c3, 0) - (c0 + c1s) * X) == 0

    q0, q2, q3 = sp.symbols("q0 q2 q3")
    reverse_singleton = tensor(
        (
            (tuple(e0), tuple(e1)),
            (tuple(e0), (0, a1, b1, d1)),
            (tuple(e0), (0, a2, b2, d2)),
            (tuple(e1), (q0, 0, q2, q3)),
        )
    )
    assert (
        sp.factor(
            reverse_singleton[(1, 1, 1, 1)] - q0 * reverse_singleton[(0, 1, 1, 0)]
        )
        == 0
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP permanent and rational pair-rank audit",
                "source_scales": [2, 3, 5, 7],
                "source_permutation": [2, 0, 3, 1],
                "anchors": {
                    "component21": str(anchor21),
                    "component18_center": str(anchor18),
                    "component8": str(anchor8),
                    "component16": str(anchor16),
                    "component18_singleton_reverse": str(anchor_singleton18),
                },
                "profiles": {
                    "component21": profile21,
                    "component18_center": profile18,
                    "component8": profile8,
                    "component16": profile16,
                    "component18_singleton_reverse_lower_pair": profile_singleton18,
                },
                "symbolic_empty_orbit_syzygies": 3,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
