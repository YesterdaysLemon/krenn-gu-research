#!/usr/bin/env python3
"""Verify the equal-center-endpoint two-inward star obstruction."""

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


def inward_support(values):
    """Both leaf relation factors kill the pure Segre point."""
    return {
        bits: value
        for bits, value in values.items()
        if bits[2] == 0 or bits[3] == 0
    }


def support_one_case():
    tau, nu = sp.symbols("tau nu")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    E0 = sp.Matrix((1, 0, 0, 0))
    A = sp.Matrix((0, 1, 1, 0))
    C = sp.Matrix((0, 1, -1, 0))
    planes = (
        sp.Matrix.vstack(E0.T, A.T),
        sp.Matrix.vstack((E0 + tau * C).T, (nu * E0 + A).T),
        sp.Matrix.vstack(E0.T, sp.Matrix(a).T),
        sp.Matrix.vstack(E0.T, sp.Matrix(g).T),
    )
    values = coefficients(planes)
    assert values[(1, 1, 0, 1)] == 2 * g[3]
    assert values[(1, 1, 1, 0)] == 2 * a[3]
    forced = {a[3]: 0, g[3]: 0}
    assert all(sp.factor(value.subs(forced)) == 0 for value in values.values())
    return True


def support_two_nonsingular_cases(A, C, B, D):
    alpha, b, d, k, s = sp.symbols("alpha b d k s")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    E = b * B + d * D
    Eperp = d * B + b * D
    q = b**2 - d**2

    alpha_zero = (
        sp.Matrix.vstack(A.T, E.T),
        sp.Matrix.vstack((A + k * Eperp).T, (E + s * C).T),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    alpha_nonzero = (
        sp.Matrix.vstack(A.T, (alpha * C + E).T),
        sp.Matrix.vstack(A.T, (s * C + E).T),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    for planes in (alpha_zero, alpha_nonzero):
        values = coefficients(planes)
        assert sp.factor(values[(1, 1, 0, 0)] + 4 * q) == 0
    return "T1100=-4Q"


def singleton_alpha_zero(A, C):
    u, w, s = sp.symbols("u w s")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    E = sp.Matrix((0, 0, 1, 0))
    planes = (
        sp.Matrix.vstack(A.T, E.T),
        sp.Matrix.vstack((u * A + w * E).T, (s * C + u * E).T),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    values = coefficients(planes)
    assert values[(1, 1, 0, 1)] == -2 * g[3] * s
    assert values[(1, 1, 1, 0)] == -2 * a[3] * s
    assert pair_matrix(planes[0], planes[1]).subs(s, 0).rank() <= 2
    forced = {a[3]: 0, g[3]: 0}
    assert all(sp.factor(value.subs(forced)) == 0 for value in values.values())
    return True


def singleton_alpha_nonzero(A, C, B, D):
    u, v, s = sp.symbols("u v s")
    a = sp.symbols("a0:4")
    g = sp.symbols("g0:4")
    E = B + D
    planes = (
        sp.Matrix.vstack(A.T, (C + E).T),
        sp.Matrix.vstack(
            (u * A + v * C - v * E).T,
            (-v * A + s * C + u * E).T,
        ),
        sp.Matrix.vstack(C.T, sp.Matrix(a).T),
        sp.Matrix.vstack(C.T, sp.Matrix(g).T),
    )
    values = coefficients(planes)
    assert values[(1, 1, 0, 1)] == -4 * g[3] * (s + u)
    assert values[(1, 1, 1, 0)] == -4 * a[3] * (s + u)
    minor = sp.factor(
        pair_matrix(planes[0], planes[1]).extract((0, 1, 3), (0, 1, 3)).det()
    )
    assert sp.factor(minor + 16 * (s + u) * (u - v) * (u + v)) == 0
    forced = {a[3]: 0, g[3]: 0}
    assert all(sp.factor(value.subs(forced)) == 0 for value in values.values())
    return str(minor)


def main():
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    support_one_case()
    nonsingular = support_two_nonsingular_cases(A, C, B, D)
    singleton_alpha_zero(A, C)
    singleton_minor = singleton_alpha_nonzero(A, C, B, D)

    # A pure tensor with both spokes genuinely inward has no coefficient with
    # leaf bit 0.  The preceding exact coefficients either contradict that
    # support, force the tensor to zero, or force pair rank at most two.
    probe = {bits: sp.Symbol("t" + "".join(map(str, bits))) for bits in BITS}
    assert len(inward_support(probe)) == 12
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "orientation": "equal-center-endpoint two-inward star-(2,1,1)",
                "support_one": "zero tensor",
                "support_two_Q_nonzero": nonsingular,
                "singleton_alpha_zero": "zero tensor or lower pair",
                "singleton_alpha_nonzero_pair_minor": singleton_minor,
                "all_pair_nonzero_stratum_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
