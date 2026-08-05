#!/usr/bin/env python3
"""Verify the complete unequal-endpoint two-inward star-(2,1,1) ledger."""

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


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def support_signatures():
    supports = tuple(
        frozenset(subset)
        for size in (1, 2)
        for subset in itertools.combinations(range(4), size)
    )
    observed = {
        (len(left), len(right), len(left & right))
        for left in supports
        for right in supports
        if left != right or len(left) == 2
        if not (len(left) == len(right) == len(left & right) == 1)
    }
    expected = {
        (1, 1, 0),
        (1, 2, 0),
        (1, 2, 1),
        (2, 1, 0),
        (2, 1, 1),
        (2, 2, 0),
        (2, 2, 1),
        (2, 2, 2),
    }
    assert observed == expected
    return sorted(observed)


def coordinate_plane_cases():
    e0, e1 = sp.eye(4).col(0), sp.eye(4).col(1)
    representatives = (
        (e0, e0, e1, e1),
        (e0, e0, e0 + e1, e0 - e1),
        (e0 + e1, e0 - e1, e0, e0),
        (e0 + e1, e0 - e1, e0 + 2 * e1, e0 - 2 * e1),
    )
    k, s = sp.symbols("k s")
    for u, up, v, vp in representatives:
        center = sp.Matrix.vstack(u.T, v.T)
        synchronizer = sp.Matrix.vstack((u + k * vp).T, (v + s * up).T)
        assert pair_matrix(center, synchronizer).rank() <= 2
    return 4


def overlap_case():
    k, s = sp.symbols("k s")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    u = sp.Matrix((1, 1, 0, 0))
    up = sp.Matrix((1, -1, 0, 0))
    v = sp.Matrix((0, 1, 1, 0))
    vp = sp.Matrix((0, 1, -1, 0))
    planes = (
        sp.Matrix.vstack(u.T, v.T),
        sp.Matrix.vstack((u + k * vp).T, (v + s * up).T),
        sp.Matrix.vstack(up.T, sp.Matrix(a).T),
        sp.Matrix.vstack(vp.T, sp.Matrix(g).T),
    )
    values = coefficients(planes)
    assert values[(0, 0, 1, 0)] == -2 * a[3] * (k + 1)
    assert values[(1, 1, 0, 1)] == -2 * g[3] * (s - 1)
    center_pair = pair_matrix(planes[0], planes[1])
    assert center_pair.subs(k, -1).rank() <= 2
    assert center_pair.subs(s, 1).rank() <= 2
    forced = {a[3]: 0, g[3]: 0}
    assert all(sp.factor(value.subs(forced)) == 0 for value in values.values())
    return True


def binary_singleton_cases():
    k, s = sp.symbols("k s")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    binary = sp.Matrix((1, 1, 0, 0))
    polar = sp.Matrix((1, -1, 0, 0))
    singleton = sp.Matrix((0, 0, 1, 0))

    forward = (
        sp.Matrix.vstack(binary.T, singleton.T),
        sp.Matrix.vstack((binary + k * singleton).T, (singleton + s * polar).T),
        sp.Matrix.vstack(polar.T, sp.Matrix(a).T),
        sp.Matrix.vstack(singleton.T, sp.Matrix(g).T),
    )
    values = coefficients(forward)
    assert values[(0, 0, 1, 0)] == 2 * a[3]
    assert values[(1, 1, 0, 1)] == -2 * g[3] * s
    specialized = {a[3]: 0, s: 0}
    b00 = sp.factor(values[(0, 0, 1, 1)].subs(specialized))
    cross = sp.factor(values[(0, 1, 1, 1)].subs(specialized))
    b11 = sp.factor(values[(1, 1, 1, 1)].subs(specialized))
    assert b11 == 0
    assert sp.factor(b00 * b11 - cross**2) == -cross**2

    reverse = (
        sp.Matrix.vstack(singleton.T, binary.T),
        sp.Matrix.vstack((singleton + k * polar).T, (binary + s * singleton).T),
        sp.Matrix.vstack(singleton.T, sp.Matrix(a).T),
        sp.Matrix.vstack(polar.T, sp.Matrix(g).T),
    )
    values = coefficients(reverse)
    assert values[(0, 0, 1, 0)] == -2 * a[3] * k
    assert values[(1, 1, 0, 1)] == 2 * g[3]
    specialized = {g[3]: 0, k: 0}
    b00 = sp.factor(values[(0, 0, 1, 1)].subs(specialized))
    cross = sp.factor(values[(0, 1, 1, 1)].subs(specialized))
    b11 = sp.factor(values[(1, 1, 1, 1)].subs(specialized))
    assert b00 == 0
    assert sp.factor(b00 * b11 - cross**2) == -cross**2
    return True


def disjoint_binary_case():
    a, c, e, f, g, h, j, k, n, s = sp.symbols("a c e f g h j k n s")
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack(C.T, (a * A + c * C + e * B + f * D).T),
        sp.Matrix.vstack(D.T, (g * A + h * C + j * B + n * D).T),
    )
    values = coefficients(planes)
    assert sp.factor(values[(0, 0, 1, 0)] + 4 * (a * k + f)) == 0
    assert sp.factor(values[(1, 1, 0, 1)] + 4 * (h + j * s)) == 0
    inward = {f: -a * k, h: -j * s}
    b00 = sp.factor(values[(0, 0, 1, 1)].subs(inward))
    cross = sp.factor(values[(0, 1, 1, 1)].subs(inward))
    b11 = sp.factor(values[(1, 1, 1, 1)].subs(inward))
    assert sp.factor(b00 - 4 * (e * j + a * g * k**2)) == 0
    assert sp.factor(cross - 4 * (a * j + e * g)) == 0
    assert sp.factor(b11 - 4 * (a * g + e * j * s**2)) == 0
    hypersurface = sp.expand(
        (e * j + a * g * k**2) * (a * g + e * j * s**2)
        - (a * j + e * g) ** 2
    )
    assert sp.factor(b00 * b11 - cross**2 - 16 * hypersurface) == 0
    assert sp.factor(hypersurface) == hypersurface
    assert hypersurface.subs({a: 0}) != 0
    assert hypersurface.subs({g: 0}) != 0
    dehomogenized = sp.factor(hypersurface.subs({a: 1, g: 1}))
    expected = sp.expand((e * j + k**2) * (1 + e * j * s**2) - (e + j) ** 2)
    assert sp.factor(dehomogenized - expected) == 0
    return str(hypersurface)


def main():
    signatures = support_signatures()
    lower_pair_signatures = coordinate_plane_cases()
    overlap_case()
    binary_singleton_cases()
    hypersurface = disjoint_binary_case()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "ordered_support_signatures": signatures,
                "lower_pair_coordinate_plane_signatures": lower_pair_signatures,
                "overlap": "zero tensor or lower pair",
                "binary_singleton": "not genuinely two-inward",
                "sole_genuine_two_inward_route": "component 25",
                "projective_disjoint_binary_hypersurface": hypersurface,
                "star_211_cell_complete": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
