#!/usr/bin/env python3
"""Independent audit of the mixed-endpoint star singleton boundary."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
QUADRATIC_WORDS = tuple(itertools.combinations(range(4), 2))


def subset_permanent(vectors: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    states = {0: Fraction(1)}
    for vector in vectors:
        next_states: dict[int, Fraction] = {}
        for mask, value in states.items():
            for coordinate, entry in enumerate(vector):
                if mask & (1 << coordinate):
                    continue
                new_mask = mask | (1 << coordinate)
                next_states[new_mask] = (
                    next_states.get(new_mask, Fraction(0)) + value * entry
                )
        states = next_states
    return states.get(15, Fraction(0))


def transform(row: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    # Unequal diagonal scales followed by source permutation (0,1,2,3)->(2,0,3,1).
    scaled = tuple(
        entry * scale for entry, scale in zip(row, (2, 3, 5, 7), strict=True)
    )
    return (scaled[2], scaled[0], scaled[3], scaled[1])


def family(a, b, c, d, f, g, h, j):
    A = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    C = (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))
    E2 = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    E3 = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))

    def combine(*terms):
        return tuple(
            sum(scale * row[index] for scale, row in terms) for index in range(4)
        )

    planes = (
        (E2, combine((a, A), (b, C), (Fraction(1), E3))),
        (combine((c, C), (f, E2), (g, E3)), A),
        (combine((d, C), (h, E2), (j, E3)), A),
        (C, E2),
    )
    return tuple(tuple(transform(row) for row in plane) for plane in planes)


def tensor(planes):
    return {
        word: subset_permanent(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS
    }


def product_matrix(left, right):
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            u = left[left_row]
            v = right[right_row]
            columns.append([u[i] * v[j] + u[j] * v[i] for i, j in QUADRATIC_WORDS])
    return sp.Matrix(6, 4, lambda row, column: columns[column][row])


def profile(planes):
    return tuple(product_matrix(planes[i], planes[j]).rank() for i, j in PAIRS)


def pure_anchor(planes):
    values = tensor(planes)
    assert values[(1, 1, 1, 1)] != 0
    assert all(value == 0 for word, value in values.items() if word != (1, 1, 1, 1))
    return values[(1, 1, 1, 1)]


def main() -> None:
    loop = family(0, 0, 0, 0, 1, 2, 3, 4)
    polar = family(0, 2, 0, 0, 1, 2, Fraction(-3, 2), 3)
    asymmetric = family(0, 2, 0, -6, 1, 0, 5, 3)
    nonzero_a = family(1, 2, 0, 0, 1, 0, 1, 0)

    assert pure_anchor(loop) != 0
    assert pure_anchor(polar) != 0
    assert pure_anchor(asymmetric) != 0
    assert pure_anchor(nonzero_a) != 0
    assert profile(loop) == (3, 3, 3, 4, 3, 3)
    assert profile(polar) == (4, 4, 3, 3, 3, 3)
    assert profile(asymmetric)[4] == 2
    assert profile(nonzero_a)[4] == 2

    # The polar branch has three rank-one triangle relations.
    relation_ranks = []
    for left, right in ((1, 2), (1, 3), (2, 3)):
        matrix = product_matrix(polar[left], polar[right])
        assert matrix.rank() == 3
        relation_ranks.append(sp.Matrix(2, 2, tuple(matrix.nullspace()[0])).rank())
    assert relation_ranks == [1, 1, 1]

    # Common singleton and equal binary supports kill the active cubic directly.
    common_singleton = (
        transform((Fraction(1), 0, 0, 0)),
        transform((Fraction(1), 0, 0, 0)),
        transform((0, 1, 0, 0)),
        transform((0, 0, 1, 0)),
    )
    equal_binary = (
        transform((1, 1, 0, 0)),
        transform((1, 1, 0, 0)),
        transform((1, -1, 0, 0)),
        transform((0, 0, 1, 0)),
    )
    assert subset_permanent(common_singleton) == 0
    assert subset_permanent(equal_binary) == 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent subset-DP permanent and rational rank audit",
                "source_permutation": [2, 0, 3, 1],
                "source_scales": [2, 3, 5, 7],
                "loop_profile": profile(loop),
                "polar_profile": profile(polar),
                "lower_pair_rank": 2,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
