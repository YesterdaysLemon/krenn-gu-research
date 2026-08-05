#!/usr/bin/env python3
"""Exact replay of the corrected rank-two-relation star obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def pair_matrix(
    first: tuple[sp.Matrix, sp.Matrix], second: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[pair(left, right) for left in first for right in second]
    )


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def synchronization_matrix(y: sp.Matrix, x: sp.Matrix) -> sp.Matrix:
    variables = sp.symbols("a0:4 b0:4")
    candidate_y = sp.Matrix(variables[:4])
    candidate_x = sp.Matrix(variables[4:])
    matrix, _ = sp.linear_eq_to_matrix(
        list(pair(y, candidate_x) - pair(x, candidate_y)), variables
    )
    return matrix


def main() -> None:
    L, z = sp.symbols("L z")

    # The invariant four-distinct-column pencil lemma.  These three
    # quadratics encode the three pair-rank-drop edges.  Their root sets are
    # pairwise disjoint off L=0,1 and have no repeated point there.
    matching_polynomials = (
        z**2 - 2 * z + 1 / L,
        z**2 - 2 * z / L + 1 / L,
        z**2 - 1 / L,
    )
    resultants = [
        sp.factor(sp.resultant(left, right, z))
        for left, right in itertools.combinations(matching_polynomials, 2)
    ]
    resultant_numerators = [sp.together(value).as_numer_denom()[0] for value in resultants]
    assert all(sp.factor(value).subs(L, 1) == 0 for value in resultant_numerators)
    assert all(value != 0 for value in resultants)
    discriminants = [sp.factor(sp.discriminant(poly, z)) for poly in matching_polynomials]
    assert all(value != 0 for value in discriminants)

    # The projective pencil point has no rank-drop partner off L=0,1.
    v = sp.symbols("v")
    leading = (L * v, L * v - 1, L * (v - 1))
    leading_solutions = [
        sp.solve((left, right), (v, L), dict=True)
        for left, right in itertools.combinations(leading, 2)
    ]
    assert leading_solutions == [[], [{L: 0}], [{L: 1, v: 1}]]

    a = sp.Matrix((1, 1, 0, 0))
    abar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    bbar = sp.Matrix((0, 0, 1, -1))

    # Kernel support two, distinct finite ratios.  Every leaf has the
    # annihilator-line form.  Two kernel rows and two active rows give a
    # parameter-free forbidden coefficient.
    alpha2, alpha3 = sp.symbols("alpha2 alpha3")
    distinct_forbidden = permanent(
        (a, a, b + alpha2 * abar, b + alpha3 * abar)
    )
    assert distinct_forbidden == 4

    # Kernel support two, coincident finite ratios.  The full synchronizer
    # plane has leaves (a+beta*bbar, b+alpha*abar), and the same coefficient
    # survives.
    beta1 = sp.symbols("beta1")
    equal_forbidden = permanent(
        (a, a + beta1 * bbar, b + alpha2 * abar, b + alpha3 * abar)
    )
    assert equal_forbidden == 4

    # Full-kernel-support 2+2 collision.  This is the Borel chart missed by
    # the withdrawn proof.  Center-leaf rank three forces c!=0.
    center = (a + b, b)
    c, r, s = sp.symbols("c r s")
    leaf = (c * (a + b) - r * bbar - s * abar, c * b - s * abar)
    sync_basis = sp.Matrix.hstack(
        sp.Matrix.vstack(*center),
        sp.Matrix.vstack(-bbar, sp.zeros(4, 1)),
        sp.Matrix.vstack(-abar, -abar),
    )
    sync = synchronization_matrix(*center)
    assert sync.rank() == 5
    assert sync * sync_basis == sp.zeros(6, 3)
    root_pair = pair_matrix(center, leaf)
    assert 4 * c**3 in minors(root_pair, 3)

    # Normalize all three nonzero c_i to one.  Two forbidden marked words
    # demand E=0 and E=1 simultaneously.
    r1, r2, r3, s1, s2, s3 = sp.symbols("r1 r2 r3 s1 s2 s3")
    leaves = tuple(
        (a + b - rr * bbar - ss * abar, b - ss * abar)
        for rr, ss in ((r1, s1), (r2, s2), (r3, s3))
    )
    E = s1 * s2 + s1 * s3 + s2 * s3
    word_0111 = sp.factor(permanent((center[0], leaves[0][1], leaves[1][1], leaves[2][1])))
    word_0011 = sp.factor(permanent((center[0], leaves[0][0], leaves[1][1], leaves[2][1])))
    assert sp.expand(word_0111 + 4 * E) == 0
    assert sp.expand(word_0011 + 4 * (E - 1)) == 0
    assert sp.expand(word_0011 - word_0111 - 4) == 0

    # Collision pencils with a common active row of support <=2 cannot have
    # a nonzero all-active coefficient.
    support_two_active = sp.Matrix((0, 0, 1, L))
    support_one_active = sp.Matrix((0, 0, 0, 1))
    assert permanent(tuple(support_two_active for _ in range(4))) == 0
    assert permanent(tuple(support_one_active for _ in range(4))) == 0

    # Kernel support one yields one underlying plane whose square has rank 2.
    support_one_plane = (
        sp.Matrix((1, 0, 0, 0)),
        sp.Matrix((0, 1, 1, 1)),
    )
    assert pair_matrix(support_one_plane, support_one_plane).rank() == 2

    result = {
        "tree_gauge": "three center-leaf relations synchronize",
        "four_distinct_rank_drop_graph": "three disjoint edges",
        "triangle_input": "corrected support-two annihilator-line classification",
        "support_two_forbidden_coefficients": [int(distinct_forbidden), int(equal_forbidden)],
        "full_support_2+2_contradiction": "word_0111 requires E=0; word_0011 requires E=1",
        "collision_active_cubes": "zero",
        "conclusion": "the rank-two-relation star is empty",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
