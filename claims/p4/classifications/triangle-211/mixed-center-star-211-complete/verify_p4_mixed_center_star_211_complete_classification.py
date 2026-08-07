#!/usr/bin/env python3
"""Verify the complete mixed-center support ledger for star-(2,1,1)."""

from __future__ import annotations

import itertools
from pathlib import Path
import json

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap,
    expose_claim_package,
)

REPO_ROOT, HERE = bootstrap(__file__)
# Expose the split-center package (moved in the same Stage 5 batch)
# so the bare-name import below resolves.
expose_claim_package(
    REPO_ROOT,
    "claims/p4/classifications/triangle-211/split-center-mixed-star-211")
from verify_p4_split_center_mixed_star_211_component import (  # noqa: E402
    reverse_purity_ledger,
)

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
    signatures = {
        (len(left), len(right), len(left & right))
        for left in supports
        for right in supports
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
    assert signatures == expected
    return sorted(signatures)


def syzygy_check(u, up, v, vp):
    basis = sp.eye(4)
    matrix = sp.Matrix.hstack(
        *(product(u, basis.col(index)) for index in range(4)),
        *(-product(v, basis.col(index)) for index in range(4)),
    )
    expected = (
        sp.Matrix.vstack(v, u),
        sp.Matrix.vstack(up, sp.zeros(4, 1)),
        sp.Matrix.vstack(sp.zeros(4, 1), vp),
    )
    assert matrix.rank() == 5
    assert all(matrix * vector == sp.zeros(6, 1) for vector in expected)
    assert sp.Matrix.hstack(*expected).rank() == 3


def overlap_case():
    k, s = sp.symbols("k s")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    u = sp.Matrix((1, 1, 0, 0))
    up = sp.Matrix((1, -1, 0, 0))
    v = sp.Matrix((0, 1, 1, 0))
    vp = sp.Matrix((0, 1, -1, 0))
    syzygy_check(u, up, v, vp)
    planes = (
        sp.Matrix.vstack(u.T, v.T),
        sp.Matrix.vstack((u + k * vp).T, (v + s * up).T),
        sp.Matrix.vstack(sp.Matrix(a).T, up.T),
        sp.Matrix.vstack(vp.T, sp.Matrix(g).T),
    )
    observed = coefficients(planes)
    expected = {
        (0, 0, 0, 0): -2 * a[3] * (k + 1),
        (0, 0, 0, 1): -a[0] * g[3] * k - a[1] * g[3] * k + a[2] * g[3] * k + 2 * a[2] * g[3] - a[3] * g[0] * k - a[3] * g[1] * k + a[3] * g[2] * k + 2 * a[3] * g[2],
        (0, 1, 0, 1): g[3] * (a[0] + a[1] + a[2]) + a[3] * (g[0] + g[1] + g[2]),
        (1, 0, 0, 1): g[3] * (a[0] + a[1] + a[2]) + a[3] * (g[0] + g[1] + g[2]),
        (1, 1, 0, 1): (2 - s) * (a[0] * g[3] + a[3] * g[0]) + s * (a[1] * g[3] + a[2] * g[3] + a[3] * g[1] + a[3] * g[2]),
        (1, 1, 1, 1): -2 * g[3] * (s - 1),
    }
    assert all(sp.factor(observed[bits] - expected.get(bits, 0)) == 0 for bits in BITS)
    coefficient_matrix = sp.Matrix(((-k, -k, k + 2), (1, 1, 1), (2 - s, s, s)))
    assert sp.factor(coefficient_matrix.det() - 4 * (k + 1) * (s - 1)) == 0
    rank_drop = pair_matrix(planes[0], planes[1]).subs(k, -1)
    assert rank_drop.rank() == 2
    assert len(rank_drop.nullspace()) == 2


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
        sp.Matrix.vstack(sp.Matrix(a).T, polar.T),
        sp.Matrix.vstack(singleton.T, sp.Matrix(g).T),
    )
    values = coefficients(forward)
    assert values[(0, 0, 0, 0)] == 2 * a[3]
    assert values[(1, 1, 1, 1)] == -2 * g[3] * s
    forced = {a[3]: 0, a[1]: -a[0]}
    assert sp.factor(values[(1, 1, 0, 1)].subs(forced) + 2 * s * a[0] * g[3]) == 0
    final_equation = values[(0, 0, 0, 1)].subs(forced).subs(a[0], 0)
    assert sp.factor(final_equation - 2 * a[2] * g[3]) == 0

    reverse = (
        sp.Matrix.vstack(singleton.T, binary.T),
        sp.Matrix.vstack((singleton + k * polar).T, (binary + s * singleton).T),
        sp.Matrix.vstack(sp.Matrix(a).T, singleton.T),
        sp.Matrix.vstack(polar.T, sp.Matrix(g).T),
    )
    values = coefficients(reverse)
    assert values[(0, 0, 0, 0)] == -2 * a[3] * k
    assert values[(1, 1, 1, 1)] == 2 * g[3]
    rank_drop = pair_matrix(reverse[0], reverse[1]).subs(k, 0)
    assert rank_drop.rank() == 2


def coordinate_plane_cases():
    e0, e1 = sp.eye(4).col(0), sp.eye(4).col(1)
    plane = sp.Matrix.vstack(e0.T, e1.T)
    assert pair_matrix(plane, plane).rank() == 1
    binary = sp.Matrix.vstack((e0 + e1).T, e0.T)
    assert pair_matrix(binary, binary).rank() == 1


def all_syzygy_representatives():
    e0, e1, e2 = sp.eye(4).col(0), sp.eye(4).col(1), sp.eye(4).col(2)
    a01 = e0 + e1
    c01 = e0 - e1
    b12 = e1 + e2
    d12 = e1 - e2
    b23 = e2 + sp.eye(4).col(3)
    d23 = e2 - sp.eye(4).col(3)
    representatives = (
        (e0, e0, e1, e1),
        (e0, e0, a01, c01),
        (e2, e2, a01, c01),
        (a01, c01, e0, e0),
        (a01, c01, e2, e2),
        (a01, c01, e0 + 2 * e1, e0 - 2 * e1),
        (a01, c01, b12, d12),
        (a01, c01, b23, d23),
    )
    for representative in representatives:
        syzygy_check(*representative)
    return len(representatives)


def main():
    signatures = support_signatures()
    overlap_case()
    binary_singleton_cases()
    coordinate_plane_cases()
    syzygy_representatives = all_syzygy_representatives()
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    reverse_purity_ledger(A, C, B, D)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "ordered_support_signatures": signatures,
                "signature_count": 8,
                "syzygy_representatives": syzygy_representatives,
                "sole_all_pair_route": "component 24 on disjoint binary supports",
                "mixed_center_orientation_complete": True,
                "remaining_after_this_theorem": [
                    "two inward spokes, equal center endpoint",
                    "two inward spokes, unequal center endpoints",
                ],
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
