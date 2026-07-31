#!/usr/bin/env python3
"""Independent subset-product audit of the projective-partner theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def squarefree_product(rows: tuple[sp.Matrix, ...], degree: int) -> sp.Matrix:
    output = []
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
        output.append(sp.expand(states[(1 << degree) - 1]))
    # Degree three in the repository is indexed by the omitted coordinate.
    return sp.Matrix(list(reversed(output))) if degree == 3 else sp.Matrix(output)


def all_minors(matrix: sp.Matrix, size: int) -> list[sp.Expr]:
    return [
        sp.factor(matrix.extract(rows, columns).det())
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    ]


def build_C(rows: tuple[sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix, sp.Matrix]) -> sp.Matrix:
    y, x, y2, x2, y3, x3 = rows
    return sp.Matrix.hstack(
        squarefree_product((y, y2, y3), 3),
        squarefree_product((x, y2, y3), 3),
        squarefree_product((y, x2, x3), 3),
        squarefree_product((x, x2, x3), 3),
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *[
            squarefree_product((left.row(i).T, right.row(j).T), 2)
            for i in range(2)
            for j in range(2)
        ]
    )


def main() -> None:
    P, Q, U = sp.symbols("P Q U")
    y = sp.ones(4, 1)
    x = sp.Matrix((0, 1, P, Q))
    sy = sp.Matrix((0, P + Q - 1, P * (1 - P + Q), Q * (1 + P - Q)))
    sx = P * Q * sp.Matrix((-1, 1, 1, 1))
    fy, fx = y + U * sy, x + U * sx
    C = build_C((y, x, sy, sx, fy, fx))

    H = P**2 - 2 * P * Q - 2 * P + Q**2 - 2 * Q + 1
    G = P * Q * H * U**2 - 6 * P * Q * U - P - Q - 1
    triples = tuple(itertools.combinations(range(4), 3))
    compression = [sp.factor(C.extract(rows, (0, 1, 2)).det()) for rows in triples]
    assert compression[3] == 0
    assert all(
        sp.div(sp.Poly(value, P, Q, U), sp.Poly(G, P, Q, U))[1].is_zero
        for value in compression[:3]
    )

    repeated_sums = {
        "0+Q=1+P": {Q: P + 1, U: -1 / (2 * P)},
        "0+P=1+Q": {P: Q + 1, U: -1 / (2 * Q)},
        "0+1=P+Q": {P: 1 - Q, U: 1 / (2 * Q * (Q - 1))},
    }
    pair = pair_matrix(sp.Matrix.vstack(sy.T, sx.T), sp.Matrix.vstack(fy.T, fx.T))
    audited = {}
    for equation, substitution in repeated_sums.items():
        specialized_C = sp.simplify(C.subs(substitution))
        specialized_pair = sp.simplify(pair.subs(substitution))
        assert all(value == 0 for value in all_minors(specialized_C[:, :3], 2))
        assert any(value != 0 for value in all_minors(specialized_C, 2))
        assert all(value == 0 for value in all_minors(specialized_pair, 3))
        assert any(value != 0 for value in all_minors(specialized_pair, 2))
        audited[equation] = {"pure_rank_pattern": [1, 2], "exceptional_pair_rank": 2}

    C_double = build_C((y, x, sy, sx, sy, sx))
    assert all(
        sp.div(sp.Poly(value, P, Q), sp.Poly(H, P, Q))[1].is_zero
        for value in all_minors(C_double, 3)
    )
    first_two = all_minors(C_double[:, :3], 2)
    assert 4 * P**2 * Q**3 * (P - 1) * (P - Q + 1) ** 2 in first_two
    assert 4 * P**3 * Q**2 * (Q - 1) * (P - Q - 1) ** 2 in first_two

    result = {
        "independent_product": "subset dynamic programming",
        "one_infinity_curves": audited,
        "double_infinity": "H forces full rank at most two, but compression cannot be a line",
        "scope": "Borel-generic center with projective synchronized partners",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
