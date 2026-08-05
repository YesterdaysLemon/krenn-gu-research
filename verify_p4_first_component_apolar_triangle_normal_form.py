#!/usr/bin/env python3
"""Exact replay of the apolar-triangle normal form for the first component."""

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


def triple(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    entries = []
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


def plucker(plane: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.factor(plane[:, (i, j)].det()) for i, j in itertools.combinations(range(4), 2)]
    )


def main() -> None:
    p, q = sp.symbols("p q")
    y1 = sp.Matrix((1, 1, 1, 1))
    x1 = sp.Matrix((0, 0, 1, 1))
    y2 = sp.Matrix((1, 0, 1, 0))
    x2 = sp.Matrix((1, -1, 1, 1))
    y3 = sp.Matrix((0, 0, 1, -1))
    x3 = sp.Matrix((1, 0, -1, 0))
    u0 = sp.Matrix((1, 0, p, 1 + p))
    x0 = sp.Matrix((0, 1, q, 1 + q))
    planes = [(u0, x0), (y1, x1), (y2, x2), (y3, x3)]

    coefficients = {
        bits: sp.factor(permanent([planes[mode][bits[mode]] for mode in range(4)]))
        for bits in BITS
    }
    assert coefficients[(0, 1, 1, 1)] == -2 * p
    assert coefficients[(1, 1, 1, 1)] == -2 * q
    assert all(
        value == 0
        for bits, value in coefficients.items()
        if bits not in ((0, 1, 1, 1), (1, 1, 1, 1))
    )

    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]])
        for edge in itertools.combinations(range(4), 2)
    }
    relation12 = sp.Matrix((0, -sp.Rational(1, 2), 1, 0))
    relation13 = sp.Matrix((0, 0, 1, 0))
    relation23 = sp.Matrix((0, 1, 0, 0))
    assert pair_matrices[(1, 2)] * relation12 == sp.zeros(6, 1)
    assert pair_matrices[(1, 3)] * relation13 == sp.zeros(6, 1)
    assert pair_matrices[(2, 3)] * relation23 == sp.zeros(6, 1)
    assert [sp.Matrix(2, 2, list(v)).rank() for v in (relation12, relation13, relation23)] == [2, 1, 1]

    exceptional_minors = [
        sp.factor(pair_matrices[(1, 2)].extract((0, 1, 3), (0, 1, 3)).det()),
        sp.factor(pair_matrices[(1, 3)].extract((0, 1, 2), (0, 1, 3)).det()),
        sp.factor(pair_matrices[(2, 3)].extract((0, 1, 3), (0, 2, 3)).det()),
    ]
    assert all(value != 0 for value in exceptional_minors)

    exterior_minors = {
        (0, 1): sp.factor(
            pair_matrices[(0, 1)].extract((0, 1, 3, 5), range(4)).det()
        ),
        (0, 2): sp.factor(
            pair_matrices[(0, 2)].extract((0, 1, 2, 3), range(4)).det()
        ),
        (0, 3): sp.factor(
            pair_matrices[(0, 3)].extract((0, 1, 2, 3), range(4)).det()
        ),
    }
    assert sp.factor(exterior_minors[(0, 1)] + 2 * (p - q) * (p + q + 1)) == 0
    assert sp.factor(exterior_minors[(0, 2)] + 2 * q * (p + 1)) == 0
    assert sp.factor(exterior_minors[(0, 3)] + 2 * p) == 0

    # Factorization lemma behind the synchronized rank-two edge.
    a0, a1, a2, a3, scale = sp.symbols("a0 a1 a2 a3 lambda")
    left = sp.Matrix((a0, a1, a2, a3))
    right = scale * sp.Matrix((-a0, a1, -a2, -a3))
    factorized = product(left, right)
    assert factorized[0] == 0 and factorized[3] == 0 and factorized[4] == 0
    assert sp.factor(factorized[1] + 2 * scale * a0 * a2) == 0
    assert sp.factor(factorized[2] + 2 * scale * a0 * a3) == 0
    assert sp.factor(factorized[5] + 2 * scale * a2 * a3) == 0
    # Equal nonzero target coefficients force a0=a2=a3; source scaling of
    # coordinate one then sets the remaining ratio to one.

    kernel_triple = triple(y1, y2, y3)
    active_triple = triple(x1, x2, x3)
    assert kernel_triple == sp.Matrix((-1, -1, -1, 1))
    assert active_triple == sp.Matrix((1, 1, -1, -1))
    assert all(
        triple(planes[1][bits[0]], planes[2][bits[1]], planes[3][bits[2]])
        == sp.zeros(4, 1)
        for bits in itertools.product(range(2), repeat=3)
        if bits not in ((0, 0, 0), (1, 1, 1))
    )
    assert (kernel_triple.T * u0)[0] == 0
    assert (kernel_triple.T * x0)[0] == 0
    assert (active_triple.T * u0)[0] == -2 * p
    assert (active_triple.T * x0)[0] == -2 * q

    # Exact equivalence with the repository's original component family.
    # Set e=i=l=1, c=-1-q, j=-p/q, then apply diag(-1,-1,1,1).
    c_old = -1 - q
    j_old = -p / q
    original = [
        sp.Matrix.vstack(
            sp.Matrix((0, 1, c_old + 1, c_old)).T,
            sp.Matrix((1, j_old, 0, -(1 + j_old))).T,
        ),
        sp.Matrix.vstack(
            sp.Matrix((0, 0, 1, 1)).T,
            sp.Matrix((1, 1, -1, -1)).T,
        ),
        sp.Matrix.vstack(
            sp.Matrix((0, 1, 0, 1)).T,
            sp.Matrix((-1, 0, 1, 0)).T,
        ),
        sp.Matrix.vstack(
            sp.Matrix((1, 0, 1, 0)).T,
            sp.Matrix((0, 0, -1, 1)).T,
        ),
    ]
    source = sp.diag(-1, -1, 1, 1)
    target = [sp.Matrix.vstack(u0.T, x0.T)] + [
        sp.Matrix.vstack(plane[0].T, plane[1].T) for plane in planes[1:]
    ]
    for old_plane, new_plane in zip(original, target):
        assert sp.Matrix.hstack(plucker(old_plane * source), plucker(new_plane)).rank() == 1

    result = {
        "component": "the original five-dimensional pure-P4 component",
        "exceptional_graph": "triangle on modes 1,2,3",
        "relation_ranks": [2, 1, 1],
        "normal_form": "fixed triangle plus U0 in one apolar hyperplane",
        "pair_profile_open_condition": "p*q*(p+1)*(p-q)*(p+q+1)!=0",
        "restricted_tensor": "-2*(p*e0+q*e1) tensor e1 tensor e1 tensor e1",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
