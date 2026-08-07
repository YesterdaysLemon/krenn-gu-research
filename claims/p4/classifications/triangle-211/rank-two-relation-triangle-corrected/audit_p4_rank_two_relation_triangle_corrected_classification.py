#!/usr/bin/env python3
"""Independent subset-product audit of the corrected triangle theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def squarefree_product(rows: tuple[sp.Matrix, ...]) -> sp.Matrix | sp.Expr:
    degree = len(rows)
    if degree == 4:
        return sp.expand(
            sum(
                sp.prod(rows[index][permutation[index]] for index in range(4))
                for permutation in itertools.permutations(range(4))
            )
        )
    values = []
    for support in itertools.combinations(range(4), degree):
        states = {0: sp.Integer(1)}
        for row in rows:
            next_states = {}
            for mask, coefficient in states.items():
                for local, source in enumerate(support):
                    if not mask & (1 << local):
                        target = mask | (1 << local)
                        next_states[target] = next_states.get(target, 0) + coefficient * row[source]
            states = next_states
        values.append(sp.expand(states[(1 << degree) - 1]))
    return sp.Matrix(list(reversed(values))) if degree == 3 else sp.Matrix(values)


def pair_matrix(left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[squarefree_product((a, b)) for a in left for b in right]
    )


def cubic_matrix(planes: tuple[tuple[sp.Matrix, sp.Matrix], ...]) -> sp.Matrix:
    (y0, x0), (y1, x1), (y2, x2) = planes
    return sp.Matrix.hstack(
        squarefree_product((y0, y1, y2)),
        squarefree_product((x0, y1, y2)),
        squarefree_product((y0, x1, x2)),
        squarefree_product((x0, x1, x2)),
    )


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    abar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    bbar = sp.Matrix((0, 0, 1, -1))
    A0, A1, A2 = sp.symbols("A0 A1 A2")
    leaves = tuple((a, b + value * abar) for value in (A0, A1, A2))
    C = cubic_matrix(leaves)

    assert C[:, :3].rank() == 2
    assert C.rank() == 3
    pair_ranks = [pair_matrix(left, right).rank() for left, right in itertools.combinations(leaves, 2)]
    assert pair_ranks == [3, 3, 3]

    planes = ((bbar, abar),) + leaves
    nonzero = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows = tuple(planes[index][bits[index]] for index in range(4))
        value = sp.factor(squarefree_product(rows))
        if value != 0:
            nonzero["".join(map(str, bits))] = str(value)
    assert nonzero == {"1111": "-4*(A0 + A1 + A2)"}

    # Replay the two support-two charts by direct subset multiplication.
    T, U = sp.symbols("T U")
    distinct = (
        (a, sp.Matrix((0, 1, 1, 1))),
        (a, sp.Matrix((-T, T + 1, 1, 1))),
        (a, sp.Matrix((-U, U + 1, 1, 1))),
    )
    distinct_C = cubic_matrix(distinct)
    assert distinct_C[:, :3].rank() == 2
    assert distinct_C.rank() == 3

    R, S = sp.symbols("R S")
    dy, dx = R * bbar, S * abar
    equal = ((a, b), (a + T * dy, b + T * dx), (a + U * dy, b + U * dx))
    equal_C = cubic_matrix(equal)
    compression = [
        sp.factor(equal_C.extract(rows, (0, 1, 2)).det())
        for rows in itertools.combinations(range(4), 3)
    ]
    expected_compression = [0, 0, -16 * R * (T + U), -16 * R * (T + U)]
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(compression, expected_compression)
    )

    # Kernel support three collisions have zero active cube; kernel support
    # one has pair-image rank two.
    for active in (sp.Matrix((0, 1, 0, 1)), sp.Matrix((0, 1, 0, 0))):
        assert squarefree_product((active, active, active)) == sp.zeros(4, 1)
    support_one = (sp.Matrix((1, 0, 0, 0)), sp.Matrix((0, 1, 1, 1)))
    assert pair_matrix(support_one, support_one).rank() == 2

    result = {
        "independent_product": "subset dynamic programming",
        "survivor_pair_ranks": pair_ranks,
        "survivor_nonzero_coefficients": nonzero,
        "support_two_charts": "distinct and coincident finite ratios replayed",
        "smaller_support_exclusions": "zero active cube or pair-rank two",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
