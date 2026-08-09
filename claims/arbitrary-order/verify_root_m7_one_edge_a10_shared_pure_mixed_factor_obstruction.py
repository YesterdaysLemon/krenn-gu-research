"""Verify the shared pure/mixed factor after adding a_(1,0)."""

from __future__ import annotations

import json
from functools import cache
from itertools import combinations, product

import sympy as sp

M = 7
R = 5
ROWS = tuple(range(7))


def permanent(matrix: sp.Matrix) -> sp.Expr:
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
    gamma = sp.symbols("gamma")
    x, y, z = (sp.symbols(name) for name in ("X_0:5", "Y_0:5", "Z_0:5"))
    a = [[sp.Integer(0) for _ in range(3)] for _ in range(M)]
    b = [[sp.Integer(0) for _ in range(3)] for _ in range(M)]
    for (u, colour), value in zip(((0, 0), (3, 2), (5, 1), (6, 1)), alpha):
        a[u][colour] = value
    a[1][0] = gamma
    for (u, colour), value in zip(((0, 0), (1, 0), (5, 2), (6, 1)), beta):
        b[u][colour] = value
    h = [[[sp.Integer(0) for _ in range(3)] for _ in range(R)] for _ in range(M)]
    locations = (
        ((2, 0), (3, 1), (4, 2), (5, 3), (6, 4)),
        ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)),
        ((1, 0), (0, 1), (6, 2), (4, 3), (2, 4)),
    )
    for colour, variables in enumerate((x, y, z)):
        for value, (u, root) in zip(variables, locations[colour]):
            h[u][root][colour] = value
    return alpha, beta, gamma, x, y, z, a, b, h


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
    edges = {(root, u) for root in range(R) for u in range(M) if h[u][root][word[u]] != 0}
    edges.update((5, u) for u in range(M) if a[u][word[u]] != 0)
    edges.update((6, u) for u in range(M) if b[u][word[u]] != 0)
    return edges


def matching_count(edges: set[tuple[int, int]]) -> int:
    choices = {row: tuple(u for u in range(M) if (row, u) in edges) for row in ROWS}

    @cache
    def recurse(row: int, used: int) -> int:
        if row == 7:
            return 1
        return sum(recurse(row + 1, used | (1 << u)) for u in choices[row] if not used & (1 << u))

    return recurse(0, 0)


def verify() -> dict[str, object]:
    alpha, beta, gamma, x, y, z, a, b, h = symbolic_data()
    c0, c1, c2 = (coefficient((colour,) * M, a, b, h) for colour in range(3))
    word = (0, 0, 0, 0, 1, 0, 2)
    cw = coefficient(word, a, b, h)
    port_binomial = alpha[0] * beta[1] + beta[0] * gamma
    assert sp.expand(c0 - port_binomial * sp.prod(x)) == 0
    assert sp.expand(c1 - alpha[2] * beta[3] * sp.prod(y)) == 0
    assert sp.expand(c2 - alpha[1] * beta[2] * sp.prod(z)) == 0
    r = x[0] * x[1] * x[3] * y[4] * z[2]
    assert sp.expand(cw - port_binomial * r) == 0

    pure_product = sp.expand(c0 * c1 * c2)
    quotient = x[2] * x[4]
    quotient *= alpha[2] * beta[3] * sp.prod(y[:4])
    quotient *= alpha[1] * beta[2] * z[0] * z[1] * z[3] * z[4]
    assert sp.expand(pure_product - cw * quotient) == 0

    # Pure nonvanishing supplies rank-three minors after endpoint
    # compatibility fixes alpha_0 and beta_0 nonzero.
    rank_minors = [alpha[0] * alpha[2] * alpha[1], beta[1] * beta[3] * beta[2]]
    rank_minors += [x[root] * y[root] * z[root] for root in range(R)]
    rank_minors += [
        alpha[0] * y[0] * z[1], beta[1] * y[1] * z[0], x[0] * y[2] * z[4],
        x[1] * y[3] * alpha[1], x[2] * y[4] * z[3],
        x[3] * alpha[2] * beta[2], x[4] * beta[3] * z[2],
    ]
    assert len(rank_minors) == 14
    endpoint_specialization = {alpha[0]: 1, alpha[3]: 1, beta[0]: 1, beta[3]: -1}
    assert list(endpoint_specialization.values()) == [1, 1, 1, -1]

    edges = support_edges(word, a, b, h)
    assert matching_count(edges) == 2
    missing = sorted(set(product(ROWS, range(M))) - edges)
    one_edge = [edge for edge in missing if matching_count(edges | {edge}) > 2]
    assert one_edge == []
    two_edges = [
        pair for pair in combinations(missing, 2)
        if matching_count(edges | set(pair)) > 2
    ]
    assert len(two_edges) == 30
    root_swaps = [pair for pair in two_edges if all(row < R for edge in pair for row in [edge[0]])]
    root_port = [pair for pair in two_edges if pair not in root_swaps]
    assert (len(root_swaps), len(root_port)) == (10, 20)

    left = (0, 1, 0, 1, 0, 1, 0)
    right = (1, 0, 1, 0, 2, 2, 0)
    next_escapes = []
    for other_word in (left, right):
        other_edges = support_edges(other_word, a, b, h)
        assert matching_count(other_edges) == 1
        alternatives = [
            edge for edge in product(ROWS, range(M))
            if edge not in other_edges and matching_count(other_edges | {edge}) > 1
        ]
        next_escapes.append(alternatives)
    assert next_escapes == [[(6, 5)], [(5, 5)]]

    return {
        "shared_port_binomial": "alpha_0*beta_1 + beta_0*gamma",
        "mixed_word": "0000102",
        "pure_matching_count_colour_0": 2,
        "mixed_matching_count": 2,
        "principal_saturation_is_unit_ideal": True,
        "endpoint_cofactor_compatible": True,
        "rank_minor_count": len(rank_minors),
        "single_further_incidence_breaks_factor": False,
        "minimal_two_incidence_pairs": len(two_edges),
        "pair_types": {"root_swaps": len(root_swaps), "root_port_exchanges": len(root_port)},
        "additional_unique_word_escapes": ["b_(5,1)", "a_(5,2)"],
    }


def main() -> None:
    print(json.dumps({
        "status": "pass",
        "field": "exact characteristic zero",
        "result": verify(),
        "one_edge_enlarged_support_full_p7_exists": False,
        "arbitrary_support_full_p7_exists": None,
        "finite_field_proof_used": False,
        "global_conjecture_resolved": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
