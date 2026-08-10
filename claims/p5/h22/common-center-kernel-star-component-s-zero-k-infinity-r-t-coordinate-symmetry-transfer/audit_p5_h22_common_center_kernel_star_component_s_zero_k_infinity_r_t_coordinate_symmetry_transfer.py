#!/usr/bin/env python3
"""No-import audit of component 23's corner r/t symmetry transfer."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
TERNARY_WORDS = tuple(itertools.product((0, 1, 2), repeat=4))
PULLBACK = (0, 1, 3, 2)

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def rows(r, t):
    return (A, D, add(B, D, r), add(B, D, t)), (B, B, C, C)


def marked(alpha, beta, h):
    return tuple(add(beta[i], alpha[i], h[i]) for i in range(4))


def permanent_dp(matrix):
    states = {0: sp.Integer(1)}
    for row in matrix:
        following = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if not mask & (1 << column):
                    target = mask | (1 << column)
                    following[target] = following.get(target, 0) + value * entry
        states = following
    return sp.expand(states[(1 << len(matrix)) - 1])


def contraction(direction, mu, nu):
    if direction == "D01":
        return (nu, mu, 0, 0, 0)
    if direction == "D23":
        return (0, 0, nu, mu, 0)
    raise ValueError(direction)


def equal(left, right):
    return sp.cancel(sp.together(left - right)) == 0


def main():
    r, t, mu, nu = sp.symbols("r t mu nu")
    h = sp.symbols("h0:4")
    x = sp.symbols("x0:8")
    old_alpha, old_beta = rows(r, t)
    new_alpha, new_beta = rows(t, r)
    old_marked = marked(old_alpha, old_beta, h)
    new_h = (h[0], h[1], h[3], h[2])
    new_marked = marked(new_alpha, new_beta, new_h)
    new_x = (x[0], x[1], x[3], x[2], x[4], x[5], x[7], x[6])

    for i, old_i in enumerate(PULLBACK):
        assert new_alpha[i] == old_alpha[old_i]
        assert new_beta[i] == old_beta[old_i]
        assert new_marked[i] == old_marked[old_i]
        assert new_x[i] == x[old_i]
        assert new_x[4 + i] == x[4 + old_i]

    # No marked plane degenerates.  For each parameter-dependent plane the
    # two displayed minors cannot vanish together in characteristic zero.
    for parameter, index in ((t, 2), (r, 3)):
        matrix = sp.Matrix((new_alpha[index], new_marked[index]))
        first = sp.factor(matrix.extract((0, 1), (0, 2)).det())
        second = sp.factor(matrix.extract((0, 1), (0, 3)).det())
        assert (first, second) == (-parameter - 1, parameter - 1)
        assert sp.gcd(first, second) == 1
    assert sp.Matrix((new_alpha[0], new_marked[0])).rank() == 2
    assert sp.Matrix((new_alpha[1], new_marked[1])).rank() == 2

    old_alpha5 = tuple((*old_alpha[i], x[i]) for i in range(4))
    old_marked5 = tuple((*old_marked[i], x[4 + i]) for i in range(4))
    new_alpha5 = tuple((*new_alpha[i], new_x[i]) for i in range(4))
    new_marked5 = tuple((*new_marked[i], new_x[4 + i]) for i in range(4))

    binary_counts = {}
    for direction in ("D01", "D23"):
        q = contraction(direction, mu, nu)
        count = 0
        for word in WORDS:
            pulled_word = (word[0], word[1], word[3], word[2])
            new_selected = tuple(
                new_marked5[i] if word[i] else new_alpha5[i] for i in range(4)
            )
            old_selected = tuple(
                old_marked5[i] if pulled_word[i] else old_alpha5[i] for i in range(4)
            )
            assert equal(
                permanent_dp(new_selected + (q,)),
                permanent_dp(old_selected + (q,)),
            )
            count += 1
        binary_counts[direction] = count

    gamma_symbols = sp.symbols("g0:20")
    old_gamma = tuple(
        tuple(gamma_symbols[5 * i + column] for column in range(5)) for i in range(4)
    )
    new_gamma = tuple(old_gamma[PULLBACK[i]] for i in range(4))
    old_colours = (old_alpha5, old_marked5, old_gamma)
    new_colours = (new_alpha5, new_marked5, new_gamma)

    ternary_counts = {}
    for direction in ("D01", "D23"):
        q = contraction(direction, mu, nu)
        count = 0
        for word in TERNARY_WORDS:
            pulled_word = (word[0], word[1], word[3], word[2])
            new_selected = tuple(new_colours[word[i]][i] for i in range(4))
            old_selected = tuple(old_colours[pulled_word[i]][i] for i in range(4))
            assert equal(
                permanent_dp(new_selected + (q,)),
                permanent_dp(old_selected + (q,)),
            )
            count += 1
        ternary_counts[direction] = count

    # The transfer and every auxiliary coordinate action are involutions.
    assert (t, r)[::-1] == (r, t)
    assert (new_h[0], new_h[1], new_h[3], new_h[2]) == h
    assert (
        new_x[0],
        new_x[1],
        new_x[3],
        new_x[2],
        new_x[4],
        new_x[5],
        new_x[7],
        new_x[6],
    ) == x
    assert contraction("D01", 0, 1) == (1, 0, 0, 0, 0)
    assert contraction("D01", 1, 0) == (0, 1, 0, 0, 0)
    assert contraction("D23", 0, 1) == (0, 0, 1, 0, 0)
    assert contraction("D23", 1, 0) == (0, 0, 0, 1, 0)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import subset-DP permanent rebuild",
                "field": "Q",
                "component": 23,
                "corner": "s=0,k=infinity",
                "ambient_map": "identity",
                "mode_map": "(2 3)",
                "parameter_map": "(r,t) -> (t,r)",
                "marking_map": tuple(map(str, new_h)),
                "extension_map": tuple(map(str, new_x)),
                "homogeneous_weight_map": "identity",
                "binary_words_checked_per_direction": binary_counts,
                "ternary_words_checked_per_direction": ternary_counts,
                "finite_zero_weight_fixed": True,
                "projective_weight_fixed_but_source_unproved": True,
                "transferred_finite_target_divisor": "t=0,r finite",
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
