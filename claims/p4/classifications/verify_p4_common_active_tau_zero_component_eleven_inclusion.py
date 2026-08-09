#!/usr/bin/env python3
"""Verify the component-eleven arc for the dependent common-active tau=0 sheet."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))
PLUCKER_PAIRS = PAIRS


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def coefficients(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(tuple(planes[mode].row(word[mode]) for mode in range(4)))
        )
        for word in WORDS
    }


def squarefree_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            squarefree_product(left.row(i), right.row(j))
            for i in range(2)
            for j in range(2)
        )
    )


def plucker(plane: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(
                plane[0, left] * plane[1, right] - plane[0, right] * plane[1, left]
            )
            for left, right in PLUCKER_PAIRS
        ]
    )


def main() -> None:
    alpha, beta, s, t, epsilon = sp.symbols("alpha beta s t epsilon", nonzero=True)
    e = sp.Matrix([[1, 0, 0, 0]])
    h = sp.Matrix([[0, 1, -1, 0]])
    w = sp.Matrix([[0, 1, 1, 0]])
    c = sp.Matrix([[0, 0, 0, 1]])

    target = (
        sp.Matrix.vstack(h + alpha * e, c + beta * e),
        sp.Matrix.vstack(e, t * h + c),
        sp.Matrix.vstack(e, s * h + c),
        sp.Matrix.vstack(w, e),
    )
    tensor = coefficients(target)
    expected_tensor = {
        (0, 1, 1, 1): -2 * (s + t),
        (1, 1, 1, 1): -2 * s * t,
    }
    for word, value in tensor.items():
        assert sp.factor(value - expected_tensor.get(word, 0)) == 0

    sample = {alpha: 1, beta: 2, s: 3, t: 4}
    profile = tuple(
        pair_matrix(target[left], target[right]).subs(sample).rank()
        for left, right in PAIRS
    )
    assert profile == (4, 4, 4, 3, 3, 3)
    expected_relations = {
        (1, 2): sp.Matrix([1, 0, 0, 0]),
        (1, 3): sp.Matrix([0, 1, 0, 0]),
        (2, 3): sp.Matrix([0, 1, 0, 0]),
    }
    for edge, relation in expected_relations.items():
        matrix = pair_matrix(target[edge[0]], target[edge[1]])
        assert matrix * relation == sp.zeros(6, 1)
        assert sp.Matrix(2, 2, tuple(relation)).rank() == 1
        assert matrix.subs(sample).rank() == 3

    a = e + c
    a_bar = e - c
    b = h
    b_bar = w
    assert squarefree_product(a, a_bar) == sp.zeros(6, 1)
    assert squarefree_product(b, b_bar) == sp.zeros(6, 1)

    p_epsilon = -1 / (2 * t * alpha * epsilon)
    q_epsilon = p_epsilon - beta / (t * alpha)
    r = t / s
    component_eleven = (
        sp.Matrix.vstack(a + p_epsilon * b, a_bar + q_epsilon * b),
        sp.Matrix.vstack(a, a_bar + b),
        sp.Matrix.vstack(a, r * a_bar + b),
        sp.Matrix.vstack(b_bar, a_bar),
    )
    source_scale = sp.diag(1, -2 * t * epsilon, -2 * t * epsilon, epsilon)
    moving = tuple(plane * source_scale for plane in component_eleven)

    moving_tensor = coefficients(moving)
    nonzero_words = tuple(word for word, value in moving_tensor.items() if value != 0)
    assert nonzero_words == ((0, 1, 1, 1), (1, 1, 1, 1))

    scales = (
        -2 * epsilon / alpha,
        -2 * epsilon,
        -2 * epsilon * t / s,
        -2 * epsilon * t,
    )
    normalized_expected = (
        sp.Matrix([-beta, beta, alpha, 0, 1 + epsilon * beta, -1 - epsilon * beta]),
        sp.Matrix([t, -t, 1, 0, -epsilon * t, epsilon * t]),
        sp.Matrix([s, -s, 1, 0, -epsilon * s, epsilon * s]),
        sp.Matrix([-1, -1, 0, 0, -epsilon, -epsilon]),
    )
    for plane, scale, expected, limit_plane in zip(
        moving, scales, normalized_expected, target, strict=True
    ):
        normalized = sp.simplify(plucker(plane) / scale)
        assert normalized == expected
        assert normalized.subs(epsilon, 0) == plucker(limit_plane)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C",
                "target_nonzero_coefficients": {
                    "0111": "-2*(s+t)",
                    "1111": "-2*s*t",
                },
                "generic_pair_profile": profile,
                "component": 11,
                "arc_parameter": "epsilon",
                "symbolic_plucker_limits": 4,
                "dense_open": "alpha*s*t != 0",
                "search_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
