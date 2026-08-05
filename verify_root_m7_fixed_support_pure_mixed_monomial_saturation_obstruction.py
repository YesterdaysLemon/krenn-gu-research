"""Verify the fixed-support pure--mixed monomial saturation obstruction."""

from __future__ import annotations

import json
from functools import cache
from itertools import product

import sympy as sp

M = 7
R = 5
ROWS = tuple(range(7))  # root rows 0,...,4, followed by a=5 and b=6


def permanent(matrix: sp.Matrix) -> sp.Expr:
    """Exact permanent by a sparse row/mask dynamic program."""
    totals: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in range(matrix.rows):
        updated: dict[int, sp.Expr] = {}
        for mask, coefficient in totals.items():
            for column in range(matrix.cols):
                value = matrix[row, column]
                bit = 1 << column
                if value != 0 and not mask & bit:
                    new_mask = mask | bit
                    updated[new_mask] = updated.get(new_mask, 0) + coefficient * value
        totals = updated
    return sp.expand(totals.get((1 << matrix.cols) - 1, 0))


def symbolic_data():
    alpha = sp.symbols("alpha_0 alpha_3 alpha_5 alpha_6")
    beta = sp.symbols("beta_0 beta_1 beta_5 beta_6")
    x = sp.symbols("X_0:5")
    y = sp.symbols("Y_0:5")
    z = sp.symbols("Z_0:5")

    a = [[sp.Integer(0) for _ in range(3)] for _ in range(M)]
    b = [[sp.Integer(0) for _ in range(3)] for _ in range(M)]
    for (u, colour), value in zip(((0, 0), (3, 2), (5, 1), (6, 1)), alpha):
        a[u][colour] = value
    for (u, colour), value in zip(((0, 0), (1, 0), (5, 2), (6, 1)), beta):
        b[u][colour] = value

    h = [[[sp.Integer(0) for _ in range(3)] for _ in range(R)] for _ in range(M)]
    colour_columns = (
        ((2, 0), (3, 1), (4, 2), (5, 3), (6, 4)),
        ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)),
        ((1, 0), (0, 1), (6, 2), (4, 3), (2, 4)),
    )
    for colour, (variables, locations) in enumerate(zip((x, y, z), colour_columns)):
        for value, (u, root) in zip(variables, locations):
            h[u][root][colour] = value
    return alpha, beta, x, y, z, a, b, h


def coefficient(word, a, b, h) -> sp.Expr:
    matrix = sp.zeros(7, 7)
    for root in range(R):
        for u in range(M):
            matrix[root, u] = h[u][root][word[u]]
    for u in range(M):
        matrix[5, u] = a[u][word[u]]
        matrix[6, u] = b[u][word[u]]
    return permanent(matrix)


def support_edges(word, a, b, h) -> set[tuple[int, int]]:
    edges = set()
    for root in range(R):
        for u in range(M):
            if h[u][root][word[u]] != 0:
                edges.add((root, u))
    for u in range(M):
        if a[u][word[u]] != 0:
            edges.add((5, u))
        if b[u][word[u]] != 0:
            edges.add((6, u))
    return edges


def matchings(edges: set[tuple[int, int]]) -> tuple[tuple[int, ...], ...]:
    by_row = {row: tuple(col for col in range(M) if (row, col) in edges) for row in ROWS}

    @cache
    def recurse(row: int, used: int):
        if row == 7:
            return ((),)
        answer = []
        for column in by_row[row]:
            bit = 1 << column
            if not used & bit:
                for tail in recurse(row + 1, used | bit):
                    answer.append((column,) + tail)
        return tuple(answer)

    return recurse(0, 0)


def verify() -> dict[str, object]:
    alpha, beta, x, y, z, a, b, h = symbolic_data()
    c0 = coefficient((0,) * M, a, b, h)
    c1 = coefficient((1,) * M, a, b, h)
    c2 = coefficient((2,) * M, a, b, h)
    word = (0, 0, 0, 0, 1, 0, 2)
    cw = coefficient(word, a, b, h)

    expected_c0 = alpha[0] * beta[1] * sp.prod(x)
    expected_c1 = alpha[2] * beta[3] * sp.prod(y)
    expected_c2 = alpha[1] * beta[2] * sp.prod(z)
    expected_cw = alpha[0] * beta[1] * x[0] * x[1] * x[3] * y[4] * z[2]
    assert (c0, c1, c2, cw) == (expected_c0, expected_c1, expected_c2, expected_cw)

    quotient = x[2] * x[4]
    quotient *= alpha[2] * beta[3] * sp.prod(y[:4])
    quotient *= alpha[1] * beta[2] * z[0] * z[1] * z[3] * z[4]
    pure_product = sp.expand(c0 * c1 * c2)
    assert sp.expand(pure_product - cw * quotient) == 0
    # This equality is the explicit certificate S in <C_w>, so 1 lies in
    # <C_w>:S and the saturation by S is the unit ideal.

    words = ((0,) * M, (1,) * M, (2,) * M, word)
    matching_counts = [len(matchings(support_edges(item, a, b, h))) for item in words]
    assert matching_counts == [1, 1, 1, 1]

    mixed_edges = support_edges(word, a, b, h)
    missing_edges = set(product(ROWS, range(M))) - mixed_edges
    one_edge_alternatives = []
    for edge in sorted(missing_edges):
        if len(matchings(mixed_edges | {edge})) > 1:
            one_edge_alternatives.append(edge)
    assert one_edge_alternatives == [(5, 1)]
    assert all(row >= R for row, _ in one_edge_alternatives)

    return {
        "pure_matching_counts": matching_counts[:3],
        "mixed_word": "".join(map(str, word)),
        "mixed_matching_count": matching_counts[3],
        "pure_mixed_identity": True,
        "saturation_is_unit_ideal": True,
        "one_edge_alternatives": [["a" if row == 5 else "b", column] for row, column in one_edge_alternatives],
        "single_root_edge_can_cancel": False,
    }


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "result": verify(),
                "fixed_support_full_p7_exists": False,
                "arbitrary_support_full_p7_exists": None,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
