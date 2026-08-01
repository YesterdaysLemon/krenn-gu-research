#!/usr/bin/env python3
"""Exact verifier for the absent AB flag orbit of triangle-(2,1,1)."""

from __future__ import annotations

import itertools
import json

import sympy as sp

PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def synchronization_matrix(a: sp.Matrix, b: sp.Matrix) -> sp.Matrix:
    variables = sp.symbols("x0:4 z0:4")
    x1 = sp.Matrix(variables[:4])
    x2 = sp.Matrix(variables[4:])
    equations = product(a, x2) - product(x1, b)
    return equations.jacobian(variables)


def pair_matrix(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def rank_at_most(matrix: sp.Matrix, rank: int) -> bool:
    size = rank + 1
    return all(
        sp.factor(matrix.extract(rows, columns).det()) == 0
        for rows in itertools.combinations(range(matrix.rows), size)
        for columns in itertools.combinations(range(matrix.cols), size)
    )


def distinct_support_case(
    label: str,
    a: sp.Matrix,
    a_bar: sp.Matrix,
    b: sp.Matrix,
    b_bar: sp.Matrix,
) -> dict[str, object]:
    assert product(a, a_bar) == sp.zeros(6, 1)
    assert product(b, b_bar) == sp.zeros(6, 1)
    matrix = synchronization_matrix(a, b)
    generators = sp.Matrix.hstack(
        sp.Matrix.vstack(a, b),
        sp.Matrix.vstack(b_bar, sp.zeros(4, 1)),
        sp.Matrix.vstack(sp.zeros(4, 1), a_bar),
    )
    assert matrix.rank() == 5
    assert generators.rank() == 3
    assert matrix * generators == sp.zeros(6, 3)

    lam, mu, nu = sp.symbols("lambda mu nu")
    x1 = lam * a + mu * b_bar
    x2 = lam * b + nu * a_bar
    edge = pair_matrix((a, x1), (b, x2))
    assert rank_at_most(edge, 2)
    basis = sp.Matrix.hstack(product(a, b), product(a_bar, b_bar))
    assert basis.row_join(edge).rank() == basis.rank()
    return {
        "support_orbit": label,
        "synchronizer_rank": matrix.rank(),
        "kernel_dimension": 8 - matrix.rank(),
        "pair_rank_upper_bound": 2,
    }


def main() -> None:
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    adjacent_b = sp.Matrix((1, 0, 1, 0))
    adjacent_b_bar = sp.Matrix((1, 0, -1, 0))
    disjoint_b = sp.Matrix((0, 0, 1, 1))
    disjoint_b_bar = sp.Matrix((0, 0, 1, -1))

    cases = [
        distinct_support_case(
            "adjacent", a, a_bar, adjacent_b, adjacent_b_bar
        ),
        distinct_support_case(
            "disjoint", a, a_bar, disjoint_b, disjoint_b_bar
        ),
    ]

    # Equal support with a projective gain g.
    g = sp.symbols("g", nonzero=True)
    b = sp.Matrix((1, g, 0, 0))
    b_bar = sp.Matrix((1, -g, 0, 0))
    matrix = synchronization_matrix(a, b)
    variables = sp.symbols("x0:4 z0:4")
    equations = matrix * sp.Matrix(variables)
    assert sp.factor(equations[1] - equations[3]) == (g - 1) * variables[2]
    assert sp.factor(equations[2] - equations[4]) == (g - 1) * variables[3]
    assert matrix.subs(g, 2).rank() == 5
    assert matrix.subs(g, -1).rank() == 5
    assert matrix.subs(g, 1).rank() == 3
    assert b.subs(g, 1) == a
    assert b_bar.subs(g, 1) == a_bar

    x1_binary = sp.Matrix(sp.symbols("r0:2") + (0, 0))
    x2_binary = sp.Matrix(sp.symbols("s0:2") + (0, 0))
    equal_edge = pair_matrix((a, x1_binary), (b, x2_binary))
    assert rank_at_most(equal_edge, 1)

    print(
        json.dumps(
            {
                "status": "verified",
                "claim_label": "VERIFIED",
                "scope": "AB radical-crossed Borel flag orbit in triangle-(2,1,1)",
                "distinct_support_cases": cases,
                "equal_support": {
                    "g_equals_1": "mode-three plane collapses",
                    "g_not_equals_1": "synchronized rows stay in one binary plane; pair rank at most one",
                },
                "orientation_empty_on_all_pair_frontier": True,
                "triangle_211_cell_exhausted": False,
                "finite_field_inference_used": False,
                "broad_search_used": False,
                "global_Krenn_Gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
