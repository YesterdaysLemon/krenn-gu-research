#!/usr/bin/env python3
"""Exact replay of the crossed (2,1,1) triangle support classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in PAIRS
        ]
    )


def pair_matrix(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def triple(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    entries: list[sp.Expr] = []
    for missing in range(4):
        columns = [column for column in range(4) if column != missing]
        entries.append(
            sp.expand(
                sum(
                    left[columns[permutation[0]]]
                    * middle[columns[permutation[1]]]
                    * right[columns[permutation[2]]]
                    for permutation in itertools.permutations(range(3))
                )
            )
        )
    return sp.Matrix(entries)


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def main() -> None:
    zero = sp.zeros(6, 1)

    # Disjoint supports: the four anchor-lemma outcomes all factor ab.
    t = sp.symbols("t")
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    q_disjoint = product(a, b)
    disjoint_factorizations = (
        (a + t * b_bar, b),
        (b, a + t * b_bar),
        (a, b + t * a_bar),
        (b + t * a_bar, a),
    )
    assert all(product(left, right) == q_disjoint for left, right in disjoint_factorizations)
    assert product(a, a_bar) == zero and product(b, b_bar) == zero

    # The exterior determinant behind the K_(2,2) anchor lemma.
    u0, u1, up0, up1, v0, v1, vp0, vp1 = sp.symbols(
        "u0 u1 up0 up1 v0 v1 vp0 vp1"
    )
    left_block = sp.Matrix(((u0, up0), (u1, up1)))
    right_block = sp.Matrix(((vp0, v0), (vp1, v1)))
    cross = left_block * right_block.T
    assert sp.factor(cross.det() - left_block.det() * right_block.det()) == 0

    # Equal supports: a nonzero outside coordinate forces the other outside
    # coordinate to vanish.  This is the complete b_2 != 0 chart.
    a0, a1, a2, b2 = sp.symbols("a0 a1 a2 b2", nonzero=True)
    equal_left = sp.Matrix((a0, a1, a2, 0))
    equal_right = sp.Matrix((-a0 * b2 / a2, -a1 * b2 / a2, b2, 0))
    equal_product = product(equal_left, equal_right)
    assert all(equal_product[index] == 0 for index in (1, 2, 3, 4, 5))
    assert sp.factor(equal_product[0] + 2 * a0 * a1 * b2 / a2) == 0

    # Adjacent supports: the unique dense factorization orbit.
    r = sp.symbols("r", nonzero=True)
    y1 = sp.Matrix((1, r, 1, 1))
    x1 = sp.Matrix((0, 0, 1, 1))
    y2 = sp.Matrix((1, 0, 1, 0))
    x2 = sp.Matrix((1, -r, 1, 1))
    y3 = sp.Matrix((0, 0, 1, -1))
    x3 = sp.Matrix((1, 0, -1, 0))
    planes = ((y1, x1), (y2, x2), (y3, x3))

    assert product(x1, y3) == zero
    assert product(y2, x3) == zero
    assert product(y1, x2) == 2 * product(x1, y2)

    matrices = {
        (1, 2): pair_matrix(planes[0], planes[1]),
        (1, 3): pair_matrix(planes[0], planes[2]),
        (2, 3): pair_matrix(planes[1], planes[2]),
    }
    relation12 = sp.Matrix((0, -sp.Rational(1, 2), 1, 0))
    relation13 = sp.Matrix((0, 0, 1, 0))
    relation23 = sp.Matrix((0, 1, 0, 0))
    assert matrices[(1, 2)] * relation12 == zero
    assert matrices[(1, 3)] * relation13 == zero
    assert matrices[(2, 3)] * relation23 == zero
    assert [sp.Matrix(2, 2, list(v)).rank() for v in (relation12, relation13, relation23)] == [2, 1, 1]

    rank_minors = (
        sp.factor(matrices[(1, 2)].extract((0, 1, 3), (0, 1, 3)).det()),
        sp.factor(matrices[(1, 3)].extract((0, 1, 2), (0, 1, 3)).det()),
        sp.factor(matrices[(2, 3)].extract((0, 1, 3), (0, 2, 3)).det()),
    )
    assert rank_minors == (-2 * r**2, -2 * r, r**2)

    mixed_triples = {
        bits: triple(planes[0][bits[0]], planes[1][bits[1]], planes[2][bits[2]])
        for bits in itertools.product(range(2), repeat=3)
        if bits not in ((0, 0, 0), (1, 1, 1))
    }
    assert all(value == sp.zeros(4, 1) for value in mixed_triples.values())
    kernel_triple = triple(y1, y2, y3)
    active_triple = triple(x1, x2, x3)
    assert kernel_triple == sp.Matrix((-r, -1, -r, r))
    assert active_triple == sp.Matrix((r, 1, -r, -r))

    # At r=1, replay the apolar opposite plane and the pure restriction.
    p, q = sp.symbols("p q")
    specialize = {r: 1}
    triangle = tuple(
        tuple(row.subs(specialize) for row in plane) for plane in planes
    )
    u0 = sp.Matrix((1, 0, p, 1 + p))
    x0 = sp.Matrix((0, 1, q, 1 + q))
    all_planes = ((u0, x0),) + triangle
    coefficients = {
        bits: sp.factor(permanent([all_planes[i][bits[i]] for i in range(4)]))
        for bits in itertools.product(range(2), repeat=4)
    }
    assert coefficients[(0, 1, 1, 1)] == -2 * p
    assert coefficients[(1, 1, 1, 1)] == -2 * q
    assert all(
        value == 0
        for bits, value in coefficients.items()
        if bits not in ((0, 1, 1, 1), (1, 1, 1, 1))
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "theorem": "crossed (2,1,1) support classification",
                "support_orbits": ["equal -> coordinate hyperplane", "disjoint -> rank drop", "overlap -> first component"],
                "generic_rank_minors": [str(value) for value in rank_minors],
                "relation_ranks": [2, 1, 1],
                "method": "exact symbolic identities; no search",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
