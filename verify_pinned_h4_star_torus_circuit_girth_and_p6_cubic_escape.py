"""Primary exact checks for pinned-star torus circuit girth and P6 escape.

Only displayed symbolic identities and fixed exact matrices are evaluated.
There is no graph, support, finite-field, word, or parameter-grid search.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp


def cached_hafnian(
    weights: dict[tuple[int, int], sp.Expr],
):
    @cache
    def evaluate(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        total = sp.Integer(0)
        for partner in vertices[1:]:
            edge = tuple(sorted((first, partner)))
            remainder = tuple(vertex for vertex in vertices[1:] if vertex != partner)
            total += weights[edge] * evaluate(remainder)
        return sp.simplify(total)

    return evaluate


def verify_k4_cubic_determinant() -> None:
    a, b, c, d, e, f = sp.symbols("a b c d e f", nonzero=True)
    matrix = sp.Matrix(
        [
            [0, f, e, d],
            [f, 0, c, b],
            [e, c, 0, a],
            [d, b, a, 0],
        ]
    )
    u_value, v_value, w_value = a * f, b * e, c * d
    expected = (
        u_value**2
        + v_value**2
        + w_value**2
        - 2 * u_value * v_value
        - 2 * u_value * w_value
        - 2 * v_value * w_value
    )
    assert sp.expand(matrix.det() - expected) == 0
    on_zero_deck = sp.factor(matrix.det().subs(f, -(b * e + c * d) / a))
    assert sp.simplify(on_zero_deck - 4 * (b**2 * e**2 + b * c * d * e + c**2 * d**2)) == 0


def canonical_core_weights() -> tuple[sp.Expr, dict[tuple[int, int], sp.Expr]]:
    omega = (-1 + sp.sqrt(-3)) / 2
    weights = {
        (0, 1): sp.Integer(1),
        (0, 2): omega,
        (0, 3): sp.Integer(1),
        (1, 2): sp.Integer(1),
        (1, 3): sp.Integer(1),
        (2, 3): omega**2,
        (0, 4): omega,
        (1, 4): omega**2,
        (2, 4): omega**2,
        (3, 4): sp.Integer(1),
    }
    assert sp.simplify(omega**2 + omega + 1) == 0
    return omega, weights


def triangle_star_matrix(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], sp.Expr]
) -> sp.Matrix:
    return sp.Matrix(
        [
            [
                weights[tuple(sorted(vertex for vertex in triple if vertex != pin))]
                if pin in triple
                else 0
                for pin in vertices
            ]
            for triple in combinations(vertices, 3)
        ]
    )


def verify_cubic_core_and_auxiliary_ranks() -> None:
    omega, weights = canonical_core_weights()
    hafnian = cached_hafnian(weights)
    assert all(hafnian(subset) == 0 for subset in combinations(range(5), 4))

    k4_matrix = sp.Matrix(
        [
            [0, omega**2, 1, 1],
            [omega**2, 0, 1, omega],
            [1, 1, 0, 1],
            [1, omega, 1, 0],
        ]
    )
    kernel = sp.Matrix([omega, omega**2, omega**2, 1])
    assert k4_matrix.rank() == 3
    assert all(sp.simplify(value) == 0 for value in k4_matrix * kernel)

    core_star = triangle_star_matrix(tuple(range(5)), weights)
    assert core_star.rank() == 5

    vertices = tuple(range(5))
    edges = tuple(combinations(vertices, 2))
    inclusion = sp.Matrix(
        [
            [int(edge[0] in triple and edge[1] in triple) for edge in edges]
            for triple in combinations(vertices, 3)
        ]
    )
    assert inclusion.rank() == 10

    triple_sums = sp.Matrix(
        [
            [1, 1, 1, 0],
            [1, 1, 0, 1],
            [1, 0, 1, 1],
            [0, 1, 1, 1],
        ]
    )
    assert triple_sums.det() == -3

    core_edges = sp.Matrix(
        [weights[edge] for edge in combinations(range(4), 2)]
    )
    kernel_products = sp.Matrix(
        [kernel[i] * kernel[j] for i, j in combinations(range(4), 2)]
    )
    assert sp.Matrix.hstack(core_edges, kernel_products).rank() == 2


def p6_escape_weights() -> tuple[sp.Expr, dict[tuple[int, int], sp.Expr]]:
    omega, weights = canonical_core_weights()
    for core_vertex in range(5):
        weights[(core_vertex, 5)] = sp.Integer(1)
        weights[(core_vertex, 6)] = sp.Integer(-1)
    weights[(5, 6)] = sp.Integer(1)
    return omega, weights


def pinned_matrix(
    vertex_count: int,
    hafnian,
) -> tuple[list[tuple[int, ...]], sp.Matrix]:
    row_sets = list(combinations(range(vertex_count), 5))
    matrix = sp.Matrix(
        [
            [
                hafnian(tuple(vertex for vertex in row_set if vertex != column))
                if column in row_set
                else 0
                for column in range(vertex_count)
            ]
            for row_set in row_sets
        ]
    )
    return row_sets, matrix


def verify_p6_full_torus_escape() -> None:
    omega, weights = p6_escape_weights()
    assert len(weights) == 21
    assert all(sp.simplify(value) != 0 for value in weights.values())
    hafnian = cached_hafnian(weights)
    row_sets, matrix = pinned_matrix(7, hafnian)
    kernel = sp.Matrix([0, 0, 0, 0, 0, 1, 1])
    assert matrix * kernel == sp.zeros(len(row_sets), 1)

    row_indices = (1, 3, 5, 6, 8, 10)
    selected = matrix[list(row_indices), list(range(6))]
    assert sp.simplify(selected.det()) == 216
    assert matrix.rank() == 6
    assert len(matrix.nullspace()) == 1

    assert sp.simplify(hafnian((0, 1, 2, 5)) - (omega + 2)) == 0
    assert hafnian((0, 1, 2, 3, 5, 6)) == -6


def verify_zero_deck_ratio_factor() -> None:
    a12 = sp.symbols("a12", nonzero=True)
    u_i, u_j, u_k = sp.symbols("u_i u_j u_k", nonzero=True)
    r_i, r_j, r_k = sp.symbols("r_i r_j r_k")

    def inferred_edge(u_left, r_left, u_right, r_right):
        return -u_left * u_right * (r_left + r_right) / a12

    expression = (
        u_i * inferred_edge(u_j, r_j, u_k, r_k)
        + u_j * inferred_edge(u_i, r_i, u_k, r_k)
        + u_k * inferred_edge(u_i, r_i, u_j, r_j)
    )
    expected = -2 * u_i * u_j * u_k * (r_i + r_j + r_k) / a12
    assert sp.simplify(expression - expected) == 0


def main() -> None:
    verify_k4_cubic_determinant()
    print("PASS: symbolic K4 determinant reduces to the cubic-resonance factor")
    verify_cubic_core_and_auxiliary_ranks()
    print("PASS: exact K5 zero deck, triangle-star injectivity, and circuit matrices")
    verify_p6_full_torus_escape()
    print("PASS: all-edge-nonzero P6 pinned matrix has exact rank six and nonzero decks")
    verify_zero_deck_ratio_factor()
    print("PASS: zero-H4 edge-torus exclusion ratio identity")
    print("SCOPE: searches=0 support_enumerations=0 finite_fields=0 project_imports=0")
    print("BOUNDARY: P7 torus circuits of support five through eight remain UNKNOWN")


if __name__ == "__main__":
    main()
