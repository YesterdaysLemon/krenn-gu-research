#!/usr/bin/env python3
"""Independent crossed-coordinate audit of the (2,2,1)-star classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))
PERMUTATION = (1, 0, 3, 2)


def permanent_dp(rows: list[sp.Matrix]) -> sp.Expr:
    layer: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        next_layer: dict[int, sp.Expr] = {}
        for mask, value in layer.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_layer[new_mask] = next_layer.get(new_mask, 0) + value * row[column]
        layer = next_layer
    return sp.expand(layer[15])


def tensor(planes: list[tuple[sp.Matrix, sp.Matrix]]) -> dict[tuple[int, ...], sp.Expr]:
    crossed = [
        (plane[0][list(PERMUTATION), :], plane[1][list(PERMUTATION), :])
        for plane in planes
    ]
    return {
        bits: sp.factor(
            permanent_dp([crossed[mode][bits[mode]] for mode in range(4)])
        )
        for bits in BITS
    }


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    r1, r2, s, t = sp.symbols("R1 R2 S T")
    A, B, C, D = sp.symbols("P Q U V")

    def leaf(r: sp.Expr, slope: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
        return a + b - r * b_bar - slope * a_bar, b - slope * a_bar

    full = tensor(
        [
            (a + b, b),
            leaf(r1, s),
            leaf(r2, t),
            (b_bar, sp.Matrix((A, B, C, D))),
        ]
    )
    assert sp.factor(full[(0, 0, 0, 0)] - 4 * (r1 + r2)) == 0

    r = sp.symbols("R")
    full = {bits: sp.factor(value.subs({r1: r, r2: -r})) for bits, value in full.items()}
    e0 = sp.factor(-full[(0, 0, 0, 1)] / 2)
    e2 = sp.factor(-full[(0, 0, 1, 1)] / 2)
    e3 = sp.factor(-full[(0, 1, 1, 1)] / 2)
    e4 = sp.factor(-full[(1, 1, 1, 1)] / 2)
    h, q = A + B, C + D
    assert sp.factor(e2 - e3 + h + q) == 0
    assert sp.factor(e4 - e3 - h) == 0
    assert sp.factor((e0 - e3).subs(D, -h - C) - h * (1 - r**2)) == 0

    total = s + t
    active = sp.Matrix((total - 1 - s * t, total + 1 + s * t, -total, -total))
    normal = tensor([(a + b, b), leaf(1, s), leaf(-1, t), (b_bar, active)])
    assert sum(value != 0 for value in normal.values()) == 1
    assert sp.factor(normal[(1, 1, 1, 1)] + 4 * total) == 0

    alpha1, alpha2, beta1, beta2 = sp.symbols("X1 X2 Y1 Y2")
    center = (a, b)
    leaf1 = (a + beta1 * b_bar, b + alpha1 * a_bar)
    leaf2 = (a + beta2 * b_bar, b + alpha2 * a_bar)
    vector = sp.Matrix((A, B, C, D))

    kk = tensor([center, leaf1, leaf2, (a_bar, vector)])
    assert sp.factor(
        kk[(1, 1, 1, 1)].subs({alpha2: -alpha1, B: -A, D: -C})
    ) == 0

    ka = tensor([center, leaf1, leaf2, (vector, a_bar)])
    ka_obstruction = sp.factor(-ka[(1, 1, 1, 0)] / 2)
    assert sp.factor(
        ka_obstruction.subs({B: -A, D: -C}) - 2 * A * (alpha1 + alpha2)
    ) == 0

    ak = tensor([center, leaf1, leaf2, (b_bar, vector)])
    assert sp.factor(
        ak[(1, 1, 1, 1)].subs({beta2: -beta1, B: -A, D: -C})
        + 4 * A * (alpha1 + alpha2)
    ) == 0

    result = {
        "audit_source_order": [1, 0, 3, 2],
        "full_support_purity_recovered": True,
        "independent_permanent": "subset dynamic programming",
        "normalized_nonzero_coefficient": "-4*(S+T)",
        "support_two_orientations_checked": 3,
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
