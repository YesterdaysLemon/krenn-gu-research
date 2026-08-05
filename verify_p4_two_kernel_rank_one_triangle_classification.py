#!/usr/bin/env python3
"""Verify the exactly-two-kernel rank-one triangle classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp

PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pair_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_rank(left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]) -> int:
    return sp.Matrix.hstack(
        *(pair_product(u, v) for u in left for v in right)
    ).rank()


def plucker(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[i] * right[j] - left[j] * right[i] for i, j in PAIRS])


def main() -> None:
    alpha, beta = sp.symbols("alpha beta")
    b2, b3, d2, d3 = sp.symbols("b2 b3 d2 d3")
    gamma = sp.symbols("gamma", nonzero=True)
    z0, z1, z2, z3 = sp.symbols("z0 z1 z2 z3")

    X0 = sp.Matrix((1, 0, 0, 0))
    X1 = sp.Matrix((0, 1, 0, 0))
    X2 = sp.Matrix((0, 0, 1, 0))
    X3 = sp.Matrix((0, 0, 0, 1))
    p = X0 + X1
    q = X0 - X1
    r1 = b2 * X2 + b3 * X3
    r2 = d2 * X2 + d3 * X3
    v1 = alpha * q + r1
    v2 = beta * p + r2
    z = sp.Matrix((z0, z1, z2, z3))

    triangle = ((p, v1), (q, v2), (q, p))
    covectors = {}
    for bits in itertools.product((0, 1), repeat=3):
        covectors[bits] = sp.factor(
            permanent([z] + [triangle[i][bits[i]] for i in range(3)])
        )

    S = b2 * d3 + b3 * d2
    Delta = b2 * d3 - b3 * d2
    expected = {
        (0, 0, 0): 0,
        (0, 0, 1): 0,
        (0, 1, 0): 0,
        (0, 1, 1): 2 * (d2 * z3 + d3 * z2),
        (1, 0, 0): -2 * (b2 * z3 + b3 * z2),
        (1, 0, 1): 0,
        (1, 1, 0): -2 * alpha * (d2 * z3 + d3 * z2) - S * (z0 - z1),
        (1, 1, 1): 2 * beta * (b2 * z3 + b3 * z2) + S * (z0 + z1),
    }
    assert all(sp.expand(covectors[key] - value) == 0 for key, value in expected.items())

    forbidden = sp.Matrix(
        (
            (0, 0, 2 * d3, 2 * d2),
            (0, 0, -2 * b3, -2 * b2),
            (-S, S, -2 * alpha * d3, -2 * alpha * d2),
        )
    )
    minors = [sp.factor(forbidden[:, columns].det()) for columns in itertools.combinations(range(4), 3)]
    expected_minors = [0, 0, 4 * Delta * S, -4 * Delta * S]
    assert all(sp.expand(left - right) == 0 for left, right in zip(minors, expected_minors))

    active = sp.Matrix(((S, S, 2 * beta * b3, 2 * beta * b2),))
    assert sp.expand(forbidden.col_join(active).det() - 8 * Delta * S**2) == 0

    # On the dependent branch r2=lambda*r1, the only nonzero case has
    # genuine binary support and the normal form below.
    b = X2 + X3
    b_bar = X2 - X3
    U = (
        (b_bar, p),
        (p, b + alpha * q),
        (q, b + gamma * p),
        (q, p),
    )
    coefficients = {}
    for bits in itertools.product((0, 1), repeat=4):
        coefficients[bits] = sp.factor(
            permanent([U[mode][bits[mode]] for mode in range(4)])
        )
    assert coefficients[(1, 1, 1, 1)] == 4
    assert all(
        value == 0 for bits, value in coefficients.items() if bits != (1, 1, 1, 1)
    )

    dense_profile = tuple(
        pair_rank(
            tuple(row.subs(alpha, 2) for row in U[i]),
            tuple(row.subs(alpha, 2) for row in U[j]),
        )
        for i, j in PAIRS
    )
    endpoint_profile = tuple(
        pair_rank(
            tuple(row.subs(alpha, 0) for row in U[i]),
            tuple(row.subs(alpha, 0) for row in U[j]),
        )
        for i, j in PAIRS
    )
    assert dense_profile == (4, 3, 3, 3, 3, 3)
    assert endpoint_profile == (3, 3, 3, 3, 3, 3)

    # The selected triangle has exactly the two requested kernel-kernel
    # relations; the third unique relation is q*p=0.
    assert pair_product(p, q) == sp.zeros(6, 1)
    assert pair_product(q, q) != sp.zeros(6, 1)
    assert [pair_rank(U[i], U[j]) for i, j in ((1, 2), (1, 3), (2, 3))] == [3, 3, 3]

    # Exact mode-permuted identification with the transitive survivor.
    tau = sp.symbols("tau", nonzero=True)
    V0 = (p, q + tau * b)
    V1 = (q, gamma * p + b)
    V2 = (q, p)
    V3 = (b_bar, p)
    target_nonzero_alpha = tuple(
        tuple(row.subs(alpha, 1 / tau) for row in plane) for plane in U
    )
    transitive_order = (V3, V0, V1, V2)
    for target_plane, transitive_plane in zip(target_nonzero_alpha, transitive_order):
        left = plucker(*target_plane)
        right = plucker(*transitive_plane)
        nonzero_index = next(i for i, value in enumerate(right) if value != 0)
        multiplier = sp.cancel(left[nonzero_index] / right[nonzero_index])
        assert all(sp.simplify(left[i] - multiplier * right[i]) == 0 for i in range(6))

    epsilon = sp.symbols("epsilon")
    endpoint_arc = plucker(p, b + epsilon * q)
    assert endpoint_arc.subs(epsilon, 0) == plucker(p, b)

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "characteristic zero",
                "cell": "triangle-(1,1,1)",
                "stratum": "exactly two kernel-kernel relations",
                "independent_transverse_branch": "empty or zero",
                "dependent_transverse_branch": "component-11 closure",
                "dense_pair_profile": list(dense_profile),
                "projective_endpoint_profile": list(endpoint_profile),
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
