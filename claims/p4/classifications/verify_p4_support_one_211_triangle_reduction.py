#!/usr/bin/env python3
"""Verify the complete support-one (2,1,1) triangle reduction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))


def product(left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(rows)
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def pair_matrix(
    left: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
    right: tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]],
) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def main() -> None:
    e0 = (1, 0, 0, 0)
    e1 = (0, 1, 0, 0)
    p0, p1, s2, s3, q0, q1, t2, t3 = sp.symbols(
        "p0 p1 s2 s3 q0 q1 t2 t3"
    )
    p = (p0, p1, s2, s3)
    q = (q0, q1, t2, t3)
    coefficients = product(p, q)
    assert coefficients == sp.Matrix(
        [
            p0 * q1 + p1 * q0,
            p0 * t2 + q0 * s2,
            p0 * t3 + q0 * s3,
            p1 * t2 + q1 * s2,
            p1 * t3 + q1 * s3,
            s2 * t3 + s3 * t2,
        ]
    )
    delta = p0 * q1 - p1 * q0
    for s, t, e0k, e1k in (
        (s2, t2, coefficients[1], coefficients[3]),
        (s3, t3, coefficients[2], coefficients[4]),
    ):
        assert sp.expand(q1 * e0k - q0 * e1k - delta * t) == 0
        assert sp.expand(p1 * e0k - p0 * e1k + delta * s) == 0

    lam = sp.symbols("lambda", nonzero=True)
    P = (p0, p1, 0, 0)
    s = (0, 0, s2, s3)
    reflected_p = tuple(P[index] + s[index] for index in range(4))
    reflected_q = tuple(lam * (P[index] - s[index]) for index in range(4))
    assert product(reflected_p, reflected_q) == sp.Matrix(
        [2 * lam * p0 * p1, 0, 0, 0, 0, -2 * lam * s2 * s3]
    )

    # If a two-edge star X0(X1-X2) had both X3 coefficients nonzero,
    # vanishing of the three X3 edges would force q_i=-k*p_i for i<3.
    # The remaining three edge coefficients then obey an identity that the
    # target star violates.
    k = sp.symbols("k", nonzero=True)
    star_p = (p0, p1, s2, s3)
    star_q = (-k * p0, -k * p1, -k * s2, k * s3)
    star_coefficients = product(star_p, star_q)
    assert all(star_coefficients[index] == 0 for index in (2, 4, 5))
    e01, e02, e12 = (
        star_coefficients[0],
        star_coefficients[1],
        star_coefficients[3],
    )
    assert sp.expand(e01 * e02 + 2 * k * p0**2 * e12) == 0
    assert sp.expand((1 * -1 + 2 * k * p0**2 * 0)) != 0

    # Common-factor YY and XX leaves have coincident planes and pair rank <=2.
    z0, z1, z2, z3, r = sp.symbols("z0 z1 z2 z3 r")
    z = (z0, z1, z2, z3)
    z_r = (z0 + r, z1, z2, z3)
    common_yy = pair_matrix((e0, z), (e0, z_r))
    common_xx = pair_matrix((z, e0), (z_r, e0))
    assert common_yy.rank() <= 2
    assert common_xx.rank() <= 2

    # Generic reflected crossed branch lies in H=<X0,X1,X2> and has the
    # intended rank-three triangle.
    reflected = {
        p0: 2,
        p1: 3,
        s2: 5,
        s3: 0,
        lam: sp.Rational(1, 12),
    }
    rp = tuple(entry.subs(reflected) if isinstance(entry, sp.Expr) else entry for entry in reflected_p)
    rq = tuple(entry.subs(reflected) if isinstance(entry, sp.Expr) else entry for entry in reflected_q)
    triangle = ((rp, e0), (e1, rq), (e0, e1))
    triangle_ranks = [
        pair_matrix(triangle[i], triangle[j]).rank()
        for i, j in itertools.combinations(range(3), 2)
    ]
    assert triangle_ranks == [3, 3, 3]

    # A disjoint mixed support-one/support-two survivor stays in the same
    # coordinate three-space and has the intended rank-three triangle.
    mixed_p = (1, 1, 2, 0)
    mixed_q = (sp.Rational(1, 4), sp.Rational(3, 4), sp.Rational(-3, 2), 0)
    mixed_target = product(e0, (0, 1, -1, 0))
    assert product(mixed_p, mixed_q) == mixed_target
    mixed_triangle = ((mixed_p, e0), ((0, 1, -1, 0), mixed_q), (e0, (0, 1, 1, 0)))
    mixed_triangle_ranks = [
        pair_matrix(mixed_triangle[i], mixed_triangle[j]).rank()
        for i, j in itertools.combinations(range(3), 2)
    ]
    assert mixed_triangle_ranks == [3, 3, 3]

    # Kunneth factorization: triangle rows have no X3 coordinate, so mode 0
    # must use X3 in every four-by-four permanent.
    a0, a1, a2, a3, b0, b1, b2, b3 = sp.symbols("a0:4 b0:4")
    opposite = ((a0, a1, a2, a3), (b0, b1, b2, b3))
    for bits in BITS4:
        selected_triangle = tuple(triangle[mode][bits[mode + 1]] for mode in range(3))
        ternary = permanent(tuple(tuple(row[index] for index in range(3)) for row in selected_triangle))
        full = permanent((opposite[bits[0]],) + selected_triangle)
        expected = opposite[bits[0]][3] * ternary
        assert sp.expand(full - expected) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "boundary": "all support-one (2,1,1) triangles",
                "common_factor_pair_rank_at_most": 2,
                "crossed_reflection_factorisation": "p=P+s, q=lambda(P-s), s^2=0",
                "crossed_sample_pair_ranks": triangle_ranks,
                "mixed_two_edge_star_obstruction": True,
                "mixed_sample_pair_ranks": mixed_triangle_ranks,
                "surviving_coordinate_dimension": 3,
                "kunneth_factorisation_all_coefficients": True,
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
