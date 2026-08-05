#!/usr/bin/env python3
"""Verify the tangent rank-two pair purity classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


def product(left, right) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def permanent(rows) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pair_rank(left, right) -> int:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right)).rank()


def coefficients(planes) -> dict[tuple[int, ...], sp.Expr]:
    return {
        bits: permanent(tuple(planes[i][bits[i]] for i in range(4)))
        for bits in BITS
    }


def main() -> None:
    w1, w2, w3 = sp.symbols("w1 w2 w3", nonzero=True)
    q_matrix = sp.Matrix(
        [[0, w3, w2], [w3, 0, w1], [w2, w1, 0]]
    )
    assert sp.factor(q_matrix.det()) == 2 * w1 * w2 * w3

    # The w^2 catalecticant is a star between e0 and the ternary functional.
    ell = sp.Matrix([2 * w2 * w3, 2 * w1 * w3, 2 * w1 * w2])
    r_matrix = sp.zeros(4)
    for index in range(3):
        r_matrix[0, index + 1] = ell[index]
        r_matrix[index + 1, 0] = ell[index]
    assert r_matrix.rank() == 2

    # A graph B={phi(v)e+v} gives rows ell(v), ell(u)*phi(v).
    l1, l2, phi1, phi2, ell_u = sp.symbols("l1 l2 phi1 phi2 ell_u")
    graph_matrix = sp.Matrix([[l1, l2], [ell_u * phi1, ell_u * phi2]])
    assert sp.factor(graph_matrix.det()) == ell_u * (l1 * phi2 - l2 * phi1)

    # If both opposite planes contain e, the matrix is anti-diagonal.
    ell_v = sp.symbols("ell_v")
    double_radical = sp.Matrix([[0, ell_v], [ell_u, 0]])
    assert double_radical.det() == -ell_u * ell_v

    # In the support-two quotient, R_w pairs only e and Z.  For bases
    # (kA,a),(kB,b), the determinant is -eA*eB*zA*zB.
    e_a, e_b, z_a, z_b, a0, b0 = sp.symbols("eA eB zA zB a0 b0")
    polar_flag_matrix = sp.Matrix(
        [[0, e_a * z_b], [z_a * e_b, a0 * z_b + z_a * b0]]
    )
    assert sp.factor(polar_flag_matrix.det()) == -e_a * e_b * z_a * z_b

    e = (1, 0, 0, 0)

    # Full-support graph representative.
    full_planes = (
        (e, (0, 1, 1, 1)),
        (e, (0, 1, 1, 1)),
        (e, (0, 1, 2, 3)),
        ((-2, 4, -5, 0), (-4, 3, 0, -5)),
    )
    full_coefficients = coefficients(full_planes)
    full_nonzero = {bits: value for bits, value in full_coefficients.items() if value}
    assert full_nonzero == {
        (1, 1, 0, 0): -2,
        (1, 1, 0, 1): -4,
        (1, 1, 1, 0): -24,
        (1, 1, 1, 1): -48,
    }
    full_profile = [
        pair_rank(full_planes[i], full_planes[j])
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert full_profile == [2, 3, 4, 3, 4, 4]

    # Support-two non-embedded polar flag.
    support_planes = (
        (e, (0, 1, 1, 0)),
        (e, (0, 1, 1, 0)),
        ((1, 1, -1, 0), (0, 1, 1, 1)),
        ((0, 1, -1, 0), (1, 1, 1, -1)),
    )
    support_coefficients = coefficients(support_planes)
    support_nonzero = {bits: value for bits, value in support_coefficients.items() if value}
    assert support_nonzero == {(1, 1, 0, 1): -2, (1, 1, 1, 1): 2}
    support_profile = [
        pair_rank(support_planes[i], support_planes[j])
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert support_profile == [2, 4, 3, 4, 3, 4]

    print(
        json.dumps(
            {
                "status": "pass",
                "full_support_polar_determinant": str(sp.factor(q_matrix.det())),
                "full_support_graph_condition": str(sp.factor(graph_matrix.det())),
                "support_two_flag_determinant": str(
                    sp.factor(polar_flag_matrix.det())
                ),
                "full_support_pair_profile": full_profile,
                "support_two_pair_profile": support_profile,
                "nonembedded_survivors": True,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
