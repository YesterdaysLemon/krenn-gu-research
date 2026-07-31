#!/usr/bin/env python3
"""Verify that support-one secants lie in the disjoint-secant component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pluecker(rows: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [rows[0, i] * rows[1, j] - rows[0, j] * rows[1, i] for i, j in PAIRS]
    )


def main() -> None:
    t, lam, u, n, v, epsilon = sp.symbols(
        "t lambda u n v epsilon", nonzero=True
    )
    e = sp.Matrix([1, 0, 0, 0])
    a = sp.Matrix([0, 1, t, 0])
    a_bar = sp.Matrix([0, 1, -t, 0])
    z = sp.Matrix([0, 0, 0, 1])

    # Two singleton kernel points, or an overlapping singleton/binary pair,
    # have pair-image rank one rather than two.
    e1 = sp.Matrix([0, 1, 0, 0])
    singleton_planes = ((e, e1), (e, e1))
    assert pair_matrix(*singleton_planes).rank() == 1
    overlap_a = sp.Matrix([1, 1, 0, 0])
    overlap_a_bar = sp.Matrix([1, -1, 0, 0])
    overlap_planes = ((e, overlap_a), (e, overlap_a_bar))
    assert pair_matrix(*overlap_planes).rank() == 1

    target_matrices = [
        sp.Matrix.vstack(e.T, a.T),
        sp.Matrix.vstack(e.T, a_bar.T),
        sp.Matrix.vstack(e.T, (a_bar + lam * z + u * a).T),
        sp.Matrix.vstack((e + n * a).T, (a_bar - lam * z + v * a).T),
    ]
    target_planes = tuple(
        tuple(tuple(row) for row in matrix.tolist()) for matrix in target_matrices
    )
    assert pair_matrix(target_planes[0], target_planes[1]).rank() == 2

    coefficients = {
        bits: permanent(tuple(target_planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }
    expected = {
        (1, 0, 1, 0): 2 * lam * n * t,
        (1, 0, 1, 1): -2 * lam * t * (u - v),
    }
    for bits, value in coefficients.items():
        assert sp.factor(value - expected.get(bits, 0)) == 0

    m = sp.symbols("m")
    star_matrix = sp.Matrix([[0, -m * lam], [n * lam, lam * (v - u)]])
    assert sp.factor(star_matrix.det()) == m * n * lam**2

    # The punctured arc is the maximal disjoint-secant flag chart.
    g_plus = e + epsilon * z
    g_minus = e - epsilon * z
    capital_l = 2 * epsilon / lam
    capital_m = -2 * u * epsilon / lam
    capital_n = 1 / n
    rho = -1 + 2 * v * epsilon / (lam * n)
    assert product(g_plus, g_minus) == sp.zeros(6, 1)
    assert product(a, a_bar) == sp.zeros(6, 1)

    arc_matrices = [
        sp.Matrix.vstack(g_plus.T, a.T),
        sp.Matrix.vstack(g_minus.T, a_bar.T),
        sp.Matrix.vstack(
            (g_minus + capital_m * a).T,
            (g_plus + capital_l * a_bar).T,
        ),
        sp.Matrix.vstack(
            (a + capital_n * g_minus).T,
            (g_plus - capital_l * a_bar + rho * g_minus).T,
        ),
    ]
    arc_planes = tuple(
        tuple(tuple(row) for row in matrix.tolist()) for matrix in arc_matrices
    )
    arc_coefficients = {
        bits: sp.factor(
            permanent(tuple(arc_planes[i][bits[i]] for i in range(4)))
        )
        for bits in BITS
    }
    nonzero_arc_support = [bits for bits, value in arc_coefficients.items() if value != 0]
    assert nonzero_arc_support == [(1, 0, 0, 0), (1, 0, 0, 1)]

    assert sp.simplify(pluecker(arc_matrices[0]).subs(epsilon, 0) - pluecker(target_matrices[0])) == sp.zeros(6, 1)
    assert sp.simplify(pluecker(arc_matrices[1]).subs(epsilon, 0) - pluecker(target_matrices[1])) == sp.zeros(6, 1)
    limit_a = sp.simplify(pluecker(arc_matrices[2]) / epsilon).subs(epsilon, 0)
    limit_b = sp.simplify(pluecker(arc_matrices[3]) / epsilon).subs(epsilon, 0)
    assert sp.simplify(limit_a - 2 * pluecker(target_matrices[2]) / lam) == sp.zeros(6, 1)
    assert sp.simplify(limit_b + 2 * pluecker(target_matrices[3]) / (lam * n)) == sp.zeros(6, 1)

    sample = {t: 1, lam: 2, u: 3, n: 4, v: 5}
    sampled_planes = tuple(
        tuple(
            tuple(sp.sympify(entry).subs(sample) for entry in row)
            for row in plane
        )
        for plane in target_planes
    )
    profile = [
        pair_matrix(sampled_planes[i], sampled_planes[j]).rank()
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert profile == [2, 3, 4, 3, 4, 4]

    print(
        json.dumps(
            {
                "status": "pass",
                "singleton_singleton_pair_rank": 1,
                "overlapping_singleton_binary_pair_rank": 1,
                "disjoint_singleton_binary_pair_rank": 2,
                "star_determinant": str(sp.factor(star_matrix.det())),
                "target_support": ["1010", "1011"],
                "arc_support": ["".join(map(str, bits)) for bits in nonzero_arc_support],
                "pluecker_valuations": [0, 0, 1, 1],
                "pair_profile": [int(value) for value in profile],
                "containing_component": 15,
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
