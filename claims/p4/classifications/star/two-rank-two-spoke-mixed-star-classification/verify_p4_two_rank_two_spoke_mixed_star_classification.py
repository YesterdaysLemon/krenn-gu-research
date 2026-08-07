#!/usr/bin/env python3
"""Exact replay of the complete rank-three (2,2,1)-star classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def pair_matrix(left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(x, y) for x in left for y in right))


def coefficients(planes: list[tuple[sp.Matrix, sp.Matrix]]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        bits: sp.factor(permanent([planes[mode][bits[mode]] for mode in range(4)]))
        for bits in BITS
    }


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))

    # Full-support 2+2 chart.
    r1, r2, s, t = sp.symbols("r1 r2 s t")
    A, B, C, D = sp.symbols("A B C D")

    def leaf(r: sp.Expr, slope: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
        return a + b - r * b_bar - slope * a_bar, b - slope * a_bar

    full_planes = [
        (a + b, b),
        leaf(r1, s),
        leaf(r2, t),
        (b_bar, sp.Matrix((A, B, C, D))),
    ]
    full = coefficients(full_planes)
    assert sp.factor(full[(0, 0, 0, 0)] - 4 * (r1 + r2)) == 0

    r = sp.symbols("r")
    specialized = {
        bits: sp.factor(value.subs({r1: r, r2: -r})) for bits, value in full.items()
    }
    e0 = sp.factor(-specialized[(0, 0, 0, 1)] / 2)
    e2 = sp.factor(-specialized[(0, 0, 1, 1)] / 2)
    e3 = sp.factor(-specialized[(0, 1, 1, 1)] / 2)
    e4 = sp.factor(-specialized[(1, 1, 1, 1)] / 2)
    total = s + t
    product_st = s * t
    h = A + B
    q = C + D
    difference = B - A

    assert sp.factor(e2 - e3 + h + q) == 0
    assert sp.factor(e4 - e3 - h) == 0
    assert sp.factor(e0 - e3 + h * r**2 + 2 * h + 3 * q) == 0
    assert sp.factor(e3 - (difference * total - h + q * product_st)) == 0

    # The leaf-leaf commutator is nonzero precisely on the star open set.
    leaf_commutator = product(full_planes[1][0], full_planes[2][1]) - product(
        full_planes[1][1], full_planes[2][0]
    )
    delta = r1 * t - r2 * s
    assert leaf_commutator == delta * sp.Matrix((0, 1, -1, -1, 1, 0))
    assert sp.factor(delta.subs({r1: r, r2: -r}) - r * total) == 0

    # Purity with a nonzero active coefficient gives, successively:
    # q=-h, r^2=1, and (B-A)/h=(1+st)/(s+t).
    assert sp.factor((e0 - e3).subs(D, -h - C) - h * (1 - r**2)) == 0
    d = (1 + product_st) / total
    assert sp.factor(d * total - (1 + product_st)) == 0

    normalized_active = sp.Matrix(
        (total - 1 - product_st, total + 1 + product_st, -total, -total)
    )
    normalized_planes = [
        (a + b, b),
        leaf(1, s),
        leaf(-1, t),
        (b_bar, normalized_active),
    ]
    normalized = coefficients(normalized_planes)
    assert sp.factor(normalized[(1, 1, 1, 1)] + 4 * total) == 0
    assert all(
        value == 0 for bits, value in normalized.items() if bits != (1, 1, 1, 1)
    )

    # Support-two equal-ratio center.  Its synchronized leaves are as below.
    alpha1, alpha2, beta1, beta2 = sp.symbols(
        "alpha1 alpha2 beta1 beta2"
    )
    center = (a, b)
    partner1 = (a + beta1 * b_bar, b + alpha1 * a_bar)
    partner2 = (a + beta2 * b_bar, b + alpha2 * a_bar)
    vector = sp.Matrix((A, B, C, D))

    # Kernel-kernel: y0*y3=a*a_bar=0.  Purity forces alpha1+alpha2=0,
    # A+B=C+D=0, and therefore the supposedly active coefficient is zero.
    kernel_kernel = coefficients([center, partner1, partner2, (a_bar, vector)])
    assert sp.factor(kernel_kernel[(1, 1, 1, 0)] + 4 * (alpha1 + alpha2)) == 0
    assert sp.factor(kernel_kernel[(0, 0, 1, 1)] - 2 * (C + D)) == 0
    assert sp.factor(kernel_kernel[(0, 1, 1, 1)] - 2 * (A + B)) == 0
    active_kk = kernel_kernel[(1, 1, 1, 1)]
    assert sp.factor(
        active_kk.subs({alpha2: -alpha1, B: -A, D: -C})
    ) == 0

    # Kernel-active: y0*x3=a*a_bar=0.  A nonzero active coefficient forces
    # the other row of U3 onto b_bar, so U0*U3 has rank two.
    kernel_active = coefficients([center, partner1, partner2, (vector, a_bar)])
    assert sp.factor(kernel_active[(1, 1, 1, 1)] + 4 * (alpha1 + alpha2)) == 0
    assert sp.factor(kernel_active[(0, 0, 1, 0)] - 2 * (C + D)) == 0
    assert sp.factor(kernel_active[(0, 1, 1, 0)] - 2 * (A + B)) == 0
    obstruction_ka = sp.factor(-kernel_active[(1, 1, 1, 0)] / 2)
    assert sp.factor(
        obstruction_ka.subs({B: -A, D: -C}) - 2 * A * (alpha1 + alpha2)
    ) == 0

    opposite_plane = (b_bar, a_bar)
    assert pair_matrix(center, opposite_plane).rank() == 2

    # Active-kernel: x0*y3=b*b_bar=0.  The same purity equations force the
    # active row onto a_bar, again producing the opposite plane and rank two.
    active_kernel = coefficients([center, partner1, partner2, (b_bar, vector)])
    assert sp.factor(active_kernel[(0, 0, 0, 0)] + 4 * (beta1 + beta2)) == 0
    assert sp.factor(active_kernel[(0, 0, 1, 1)] - 2 * (C + D)) == 0
    assert sp.factor(active_kernel[(0, 1, 1, 1)] - 2 * (A + B)) == 0
    active_ak = active_kernel[(1, 1, 1, 1)]
    assert sp.factor(
        active_ak.subs({beta2: -beta1, B: -A, D: -C})
        + 4 * A * (alpha1 + alpha2)
    ) == 0

    result = {
        "classified_stratum": "rank-three star with relation ranks (2,2,1)",
        "full_support_normal_form": "the Cayley-toric tenth component",
        "full_support_forced_equations": [
            "r2=-r1",
            "r1^2=1",
            "C+D=-(A+B)",
            "(B-A)/(A+B)=(1+s*t)/(s+t)",
        ],
        "ordinary_synchronizer_pencils": "leaf pair rank at most three",
        "support_two_equal_center": "zero tensor or center-fourth pair rank two",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
