#!/usr/bin/env python3
"""Verify the transitive all-rank-one P4 triangle classification."""

from __future__ import annotations

import itertools
import json

import sympy as sp


PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))
WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def contraction_covectors(planes):
    identity = sp.eye(4)
    result = {}
    for bits in itertools.product((0, 1), repeat=3):
        result[bits] = sp.Matrix(
            [[
                permanent(
                    (
                        identity.row(coordinate),
                        planes[0].row(bits[0]),
                        planes[1].row(bits[1]),
                        planes[2].row(bits[2]),
                    )
                )
                for coordinate in range(4)
            ]]
        )
    return result


def pluecker(plane):
    return sp.Matrix([plane[:, pair].det() for pair in PAIRS])


def main() -> None:
    alpha, delta, b_2, b_3, d_2, d_3 = sp.symbols(
        "alpha delta b2 b3 d2 d3"
    )
    a = sp.Matrix([[1, 1, 0, 0]])
    c = sp.Matrix([[1, -1, 0, 0]])
    b = sp.Matrix([[0, 0, b_2, b_3]])
    d = sp.Matrix([[0, 0, d_2, d_3]])
    leaves = (
        sp.Matrix.vstack(c, alpha * a + b),
        sp.Matrix.vstack(c, a),
        sp.Matrix.vstack(delta * c + d, a),
    )
    covectors = contraction_covectors(leaves)
    expected_nonzero = {
        (0, 0, 0): sp.Matrix([[0, 0, -2 * d_3, -2 * d_2]]),
        (1, 0, 0): sp.Matrix(
            [[
                -b_2 * d_3 - b_3 * d_2,
                b_2 * d_3 + b_3 * d_2,
                -2 * b_3 * delta,
                -2 * b_2 * delta,
            ]]
        ),
        (1, 1, 0): sp.Matrix(
            [[
                b_2 * d_3 + b_3 * d_2,
                b_2 * d_3 + b_3 * d_2,
                2 * alpha * d_3,
                2 * alpha * d_2,
            ]]
        ),
        (1, 1, 1): sp.Matrix([[0, 0, 2 * b_3, 2 * b_2]]),
    }
    for bits, covector in covectors.items():
        assert sp.simplify(covector - expected_nonzero.get(bits, sp.zeros(1, 4))) == sp.zeros(1, 4)

    forbidden = sp.Matrix.vstack(
        covectors[(0, 0, 0)], covectors[(1, 0, 0)], covectors[(1, 1, 0)]
    )
    maximal_minors = tuple(
        sp.factor(forbidden[:, columns].det())
        for columns in itertools.combinations(range(4), 3)
    )
    cross_sum = b_2 * d_3 + b_3 * d_2
    cross_difference = b_2 * d_3 - b_3 * d_2
    assert maximal_minors == (
        4 * d_3 * cross_sum**2,
        4 * d_2 * cross_sum**2,
        4 * delta * cross_difference * cross_sum,
        4 * delta * cross_difference * cross_sum,
    )

    # On the nondegenerate support-two branch, rank <=2 forces b*d=0.
    normalized = {b_2: 1, b_3: 1, d_2: 1, d_3: -1}
    normalized_forbidden = forbidden.subs(normalized)
    escape = covectors[(1, 1, 1)].subs(normalized)
    assert normalized_forbidden.subs(delta, 0).rank() == 1
    assert sp.Matrix.vstack(normalized_forbidden.subs(delta, 0), escape).rank() == 2
    assert normalized_forbidden.subs(delta, 1).rank() == 2
    assert sp.Matrix.vstack(normalized_forbidden.subs(delta, 1), escape).rank() == 2

    # If the complementary factors have support one, b*d=0 forces them
    # onto the same coordinate.  The active covector is then already the
    # all-kernel forbidden covector, so the restriction is zero rather than
    # a further all-pair-rank-three family.
    singleton = {b_2: 1, b_3: 0, d_2: 1, d_3: 0}
    singleton_forbidden = forbidden.subs(singleton)
    singleton_escape = covectors[(1, 1, 1)].subs(singleton)
    assert singleton_escape == -singleton_forbidden.row(0)
    singleton_leaves = tuple(plane.subs(singleton) for plane in leaves)
    assert tuple(
        pair_matrix(singleton_leaves[left], singleton_leaves[right]).rank()
        for left, right in ((0, 1), (0, 2), (1, 2))
    ) == (3, 3, 3)

    # The surviving delta=0 family is pure and is an explicit boundary of
    # the equal-support component eleven.
    p, q = sp.symbols("p q")
    b_plus = sp.Matrix([[0, 0, 1, 1]])
    b_minus = sp.Matrix([[0, 0, 1, -1]])
    family = (
        sp.Matrix.vstack(a + p * b_plus, c + q * b_plus),
        sp.Matrix.vstack(c, alpha * a + b_plus),
        sp.Matrix.vstack(c, a),
        sp.Matrix.vstack(b_minus, a),
    )
    tensor = {
        word: sp.factor(
            permanent(tuple(family[mode].row(word[mode]) for mode in range(4)))
        )
        for word in WORDS
    }
    assert {word: value for word, value in tensor.items() if value != 0} == {
        (0, 1, 1, 1): 4 * p,
        (1, 1, 1, 1): 4 * q,
    }

    sample = tuple(plane.subs({p: 2, q: 3, alpha: 2}) for plane in family)
    pair_profile = tuple(
        pair_matrix(sample[left], sample[right]).rank() for left, right in PAIRS
    )
    assert pair_profile == (4, 3, 4, 3, 3, 3)

    # Source sign X1 -> -X1 exchanges a and c.  After that symmetry, the
    # following epsilon arc is exactly component eleven with parameter
    # r=alpha/epsilon and a block source scale diag(alpha,alpha,1,1).
    epsilon = sp.symbols("epsilon")
    target_after_swap = (
        sp.Matrix.vstack(a + q * b_plus, c + p * b_plus),
        sp.Matrix.vstack(a, alpha * c + b_plus),
        sp.Matrix.vstack(a, c),
        sp.Matrix.vstack(b_minus, c),
    )
    arc = (
        target_after_swap[0],
        target_after_swap[1],
        sp.Matrix.vstack(a, alpha * c + epsilon * b_plus),
        target_after_swap[3],
    )
    for mode in (0, 1, 3):
        assert pluecker(arc[mode]) == pluecker(target_after_swap[mode])
    assert pluecker(arc[2].subs(epsilon, 0)) == alpha * pluecker(target_after_swap[2])

    # Reconstruct the component-eleven rows before the harmless row scaling
    # on its second moving plane.
    component_eleven = (
        target_after_swap[0],
        sp.Matrix.vstack(a, alpha * c + b_plus),
        sp.Matrix.vstack(a, (alpha / epsilon) * c + b_plus),
        sp.Matrix.vstack(b_minus, c),
    )
    assert all(
        sp.simplify(
            pluecker(component_eleven[mode])
            - (pluecker(arc[mode]) / epsilon if mode == 2 else pluecker(arc[mode]))
        ) == sp.zeros(6, 1)
        for mode in range(4)
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "determinantal_factor": str(cross_sum),
                "escape_condition": "delta=0",
                "support_one_boundary": "zero because escape is forbidden",
                "surviving_pair_profile": pair_profile,
                "containing_component": 11,
                "projective_parameter": "r=alpha/epsilon",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
