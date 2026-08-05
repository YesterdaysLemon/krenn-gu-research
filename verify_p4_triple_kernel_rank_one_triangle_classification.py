#!/usr/bin/env python3
"""Verify the fully kernel-kernel rank-one triangle classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp

COORDINATE_PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pair_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in COORDINATE_PAIRS]
    )


def pair_rank(left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]) -> int:
    products = [pair_product(u, v) for u in left for v in right]
    return sp.Matrix.hstack(*products).rank()


def main() -> None:
    eps = sp.symbols("epsilon", nonzero=True)
    alpha, beta, gamma = sp.symbols("alpha beta gamma", nonzero=True)
    p, q, r, s = sp.symbols("p q r s")
    z_a, z_b, z_e, z_c = sp.symbols("z_A z_B z_e z_C")

    A = sp.Matrix((1, 0, 0, 0))
    B = sp.Matrix((0, 1, 0, 0))
    e = sp.Matrix((0, 0, 1, 0))
    C = sp.Matrix((0, 0, 0, 1))

    # The support argument in the theorem forces this three-parameter form.
    u1 = alpha * B + beta * C
    u2 = gamma * A + beta * C
    u3 = gamma * A + alpha * B
    common_pair = pair_product(u1, u2)
    assert pair_product(u1, u3) == common_pair
    assert pair_product(u2, u3) == common_pair
    assert pair_product(u1, u2 - u3) == sp.zeros(6, 1)
    assert pair_product(u2, u1 - u3) == sp.zeros(6, 1)
    assert pair_product(u3, u1 - u2) == sp.zeros(6, 1)
    assert sp.factor(permanent([e, u1, u2, u3])) == 2 * alpha * beta * gamma

    # Signed representative adapted to the component-sixteen degeneration.
    v1 = B - C
    v2 = A - B
    v3 = A + C
    q12 = pair_product(v1, v2)
    assert pair_product(v1, v3) == q12
    assert pair_product(v2, v3) == -q12
    assert permanent([e, v1, v2, v3]) == 2
    assert sp.Matrix.hstack(v1, v2, v3)[[0, 1, 3], :].det() == -2

    triangle = ((e, v1), (e, v2), (e, v3))
    assert [pair_rank(triangle[i], triangle[j]) for i, j in ((0, 1), (0, 2), (1, 2))] == [3, 3, 3]

    # A symbolic opposite plane inside H_0 and transverse to W.
    w_a = A + B
    w_c = B + C
    y0 = p * w_a + q * w_c
    w0 = r * w_a + s * w_c
    x0 = e + w0
    assert sp.expand(y0[0] - y0[1] + y0[3]) == 0
    assert sp.expand(w0[0] - w0[1] + w0[3]) == 0
    assert sp.factor(sp.Matrix.hstack(y0, w0)[[0, 3], :].det()) == p * s - q * r

    target_planes = ((y0, x0),) + triangle
    coefficients = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows = [target_planes[mode][bits[mode]] for mode in range(4)]
        coefficients[bits] = sp.factor(permanent(rows))
    assert coefficients[(1, 1, 1, 1)] == 2
    assert all(
        value == 0 for bits, value in coefficients.items() if bits != (1, 1, 1, 1)
    )

    # Exact arc and its universal coefficient identities.
    k1 = e + eps * B
    k2 = e - eps * A
    k3 = e - eps * C
    kernels = (k1, k2, k3)
    actives = (v1, v2, v3)
    z = sp.Matrix((z_a, z_b, z_e, z_c))
    g = z_a - z_b + z_c - eps * z_e
    expected_factors = {
        (0, 0, 0): -eps**2,
        (0, 0, 1): eps,
        (0, 1, 0): eps,
        (0, 1, 1): -1,
        (1, 0, 0): -eps,
        (1, 0, 1): 1,
        (1, 1, 0): 1,
    }
    for bits, factor in expected_factors.items():
        rows = [z] + [actives[i] if bits[i] else kernels[i] for i in range(3)]
        assert sp.expand(permanent(rows) - factor * g) == 0
    assert permanent([z, v1, v2, v3]) == 2 * z_e

    # L_epsilon maps H_0 into H_epsilon and preserves the active coordinate.
    z_h0 = sp.Matrix((z_a, z_a + z_c, z_e, z_c))
    lifted = z_h0 + eps * z_e * A
    assert sp.expand(lifted[0] - lifted[1] + lifted[3] - eps * lifted[2]) == 0
    assert lifted[2] == z_e

    # Row identities with the source-scaled support-star component.
    d1_u1 = e + eps * B
    d2_u1 = e + eps * C
    assert k1 == d1_u1
    assert sp.expand((d1_u1 - d2_u1) / eps) == v1

    d1_u2 = eps * A - e
    d2_u2 = eps * B - e
    assert k2 == -d1_u2
    assert sp.expand((d1_u2 - d2_u2) / eps) == v2

    d1_u3 = e - eps * C
    d2_u3 = eps * A + e
    assert k3 == d1_u3
    assert sp.expand((d2_u3 - d1_u3) / eps) == v3

    # One exact sample confirms the all-pair-rank branch of the theorem.
    sample = {p: 1, q: 2, r: 3, s: 5}
    sample_planes = tuple(
        tuple(row.subs(sample) for row in plane) for plane in target_planes
    )
    sample_profile = tuple(
        pair_rank(sample_planes[i], sample_planes[j]) for i, j in COORDINATE_PAIRS
    )
    assert min(sample_profile) >= 3

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "characteristic zero",
                "cell": "triangle-(1,1,1)",
                "stratum": "three kernel-kernel unique relations",
                "common_singleton_branch": "component-18 closure",
                "rank_one_polar_branch": "component-16 closure",
                "symbolic_arc_coefficients": 8,
                "sample_pair_profile": list(sample_profile),
                "remaining_triangle_111_boundary": "exactly one kernel-kernel edge",
                "component_exhaustiveness": "unresolved",
                "global_conjecture": "unresolved",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
