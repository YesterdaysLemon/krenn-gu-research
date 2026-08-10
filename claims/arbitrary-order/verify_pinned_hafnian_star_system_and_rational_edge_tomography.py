"""Primary exact checks for pinned hafnian rational edge tomography.

Only fixed symbolic identities and fixed exact inclusion matrices are checked.
No graph support, word, parameter-grid, or finite-field search is performed.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from itertools import combinations

import sympy as sp

Edge = tuple[int, int]
Hafnian = Callable[[tuple[int, ...]], sp.Expr]

PINNED_PIVOTS = {
    (7, 3): (0, 1, 2, 3, 4, 5),
    (8, 3): (0, 1, 2, 3, 6, 10, 15),
    (9, 3): (0, 1, 2, 3, 4, 10, 20, 35),
    (11, 5): tuple(range(10)),
}


def edge_list(n: int) -> list[Edge]:
    return list(combinations(range(n), 2))


def cached_hafnian(weights: dict[Edge, sp.Expr]) -> Hafnian:
    @cache
    def evaluate(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        total = sp.Integer(0)
        for partner in vertices[1:]:
            remainder = tuple(
                vertex for vertex in vertices[1:] if vertex != partner
            )
            edge = tuple(sorted((first, partner)))
            total += weights.get(edge, sp.Integer(0)) * evaluate(remainder)
        return sp.expand(total)

    return evaluate


def symbolic_weights(n: int) -> dict[Edge, sp.Expr]:
    edges = edge_list(n)
    variables = sp.symbols(" ".join(f"a{i}{j}" for i, j in edges))
    return dict(zip(edges, variables, strict=True))


def verify_symbolic_partner_and_euler_identities(k: int) -> None:
    n = 2 * k
    vertices = tuple(range(n))
    weights = symbolic_weights(n)
    hafnian = cached_hafnian(weights)

    pin = 0
    others = tuple(range(1, n))
    partner_sum = sum(
        weights[(pin, partner)]
        * hafnian(tuple(vertex for vertex in others if vertex != partner))
        for partner in others
    )
    assert sp.expand(partner_sum - hafnian(vertices)) == 0

    euler_sum = sum(
        weight
        * hafnian(tuple(vertex for vertex in vertices if vertex not in edge))
        for edge, weight in weights.items()
    )
    assert sp.expand(euler_sum - k * hafnian(vertices)) == 0


def one_inclusion_matrix(vertex_count: int, subset_size: int) -> sp.Matrix:
    vertices = tuple(range(vertex_count))
    return sp.Matrix(
        [
            [int(vertex in subset) for vertex in vertices]
            for subset in combinations(vertices, subset_size)
        ]
    )


def two_inclusion_matrix(vertex_count: int, subset_size: int) -> sp.Matrix:
    vertices = tuple(range(vertex_count))
    edges = edge_list(vertex_count)
    return sp.Matrix(
        [
            [int(edge[0] in subset and edge[1] in subset) for edge in edges]
            for subset in combinations(vertices, subset_size)
        ]
    )


def verify_pinned_inclusion_certificates() -> None:
    cases = (
        (6, 5, (0, 1, 2, 3, 4, 5), 5),
        (7, 5, (0, 1, 2, 3, 6, 10, 15), 5),
        (8, 5, (0, 1, 2, 3, 4, 10, 20, 35), 5),
        (10, 9, tuple(range(10)), 9),
    )
    for vertex_count, subset_size, pivots, expected_determinant in cases:
        matrix = one_inclusion_matrix(vertex_count, subset_size)
        assert matrix.rank() == vertex_count
        selected = matrix[list(pivots), :]
        assert selected.det() == expected_determinant

    assert 5 * 3**6 != 0
    assert 5 * 3**7 != 0
    assert 5 * 3**8 != 0
    assert 9 * 105**10 != 0


def verify_first_deck_hierarchy() -> None:
    full_rank_cases = ((7, 4, 21), (10, 8, 45), (11, 8, 55))
    for n, order, expected_rank in full_rank_cases:
        matrix = two_inclusion_matrix(n, order)
        assert matrix.rank() == expected_rank
        assert expected_rank == sp.binomial(n, 2)

    deficient_cases = ((9, 8, 27, 105), (13, 12, 65, 10395))
    for n, order, fibre_dimension, all_one_value in deficient_cases:
        matrix = two_inclusion_matrix(n, order)
        edges = edge_list(n)
        assert matrix.shape == (n, len(edges))
        assert matrix.rank() == n
        assert len(edges) - n == fibre_dimension
        assert sp.factorial2(n - 2) == all_one_value

        for prescribed in edges:
            u, v = prescribed
            other_vertices = [
                vertex for vertex in range(n) if vertex not in prescribed
            ]
            a, b = other_vertices[:2]
            tangent = dict.fromkeys(edges, sp.Integer(0))
            tangent[tuple(sorted((u, v)))] = 1
            tangent[tuple(sorted((v, a)))] = -1
            tangent[tuple(sorted((a, b)))] = 1
            tangent[tuple(sorted((b, u)))] = -1
            vector = sp.Matrix([tangent[edge] for edge in edges])
            assert vector[edges.index(prescribed)] == 1
            assert matrix * vector == sp.zeros(n, 1)


def fixed_nonconstant_weights(n: int) -> dict[Edge, sp.Expr]:
    weights = dict.fromkeys(edge_list(n), sp.Integer(1))
    weights[(0, 1)] = sp.Integer(2)
    return weights


def pinned_system(
    n: int, k: int, pin: int, hafnian: Hafnian
) -> tuple[tuple[int, ...], sp.Matrix, sp.Matrix]:
    other_vertices = tuple(vertex for vertex in range(n) if vertex != pin)
    row_subsets = list(combinations(other_vertices, 2 * k - 1))
    matrix = sp.Matrix(
        [
            [
                hafnian(tuple(vertex for vertex in subset if vertex != partner))
                if partner in subset
                else 0
                for partner in other_vertices
            ]
            for subset in row_subsets
        ]
    )
    right_hand_side = sp.Matrix(
        [hafnian(tuple(sorted((pin, *subset)))) for subset in row_subsets]
    )
    return other_vertices, matrix, right_hand_side


def verify_all_star_reconstruction(n: int, k: int) -> None:
    weights = fixed_nonconstant_weights(n)
    hafnian = cached_hafnian(weights)
    pivots = PINNED_PIVOTS[(n, k)]
    for pin in range(n):
        other_vertices, matrix, right_hand_side = pinned_system(
            n, k, pin, hafnian
        )
        selected_matrix = matrix[list(pivots), :]
        selected_rhs = right_hand_side[list(pivots), :]
        assert selected_matrix.det() != 0
        recovered = selected_matrix.inv() * selected_rhs
        expected = sp.Matrix(
            [weights[tuple(sorted((pin, partner)))] for partner in other_vertices]
        )
        assert recovered == expected
        assert matrix * expected == right_hand_side


def all_deck_values(
    n: int, order: int, hafnian: Hafnian
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        subset: hafnian(subset) for subset in combinations(range(n), order)
    }


def verify_sparse_matching_tori() -> None:
    for q in (2, 4):
        n = 2 * q + 2
        edges = edge_list(n)
        parameters = sp.symbols(f"t0:{q - 1}", nonzero=True)
        weights = dict.fromkeys(edges, sp.Integer(0))
        matching_edges = [(2 * index, 2 * index + 1) for index in range(q)]
        for edge, parameter in zip(
            matching_edges[:-1], parameters, strict=True
        ):
            weights[edge] = parameter
        weights[matching_edges[-1]] = 1 / sp.prod(parameters)
        hafnian = cached_hafnian(weights)
        lower_deck = all_deck_values(n, 2 * q, hafnian)
        supported_vertices = tuple(range(2 * q))
        assert sp.simplify(lower_deck[supported_vertices]) == 1
        assert all(
            value == 0
            for subset, value in lower_deck.items()
            if subset != supported_vertices
        )
        assert all(
            value == 0
            for value in all_deck_values(n, 2 * q + 2, hafnian).values()
        )


def verify_label_capacities() -> None:
    cases = (
        (42, 3, False),
        (98, 4, False),
        (210, 5, True),
        (99, 4, False),
        (219, 5, True),
        (176, 3, False),
        (45, 2, False),
        (9, 1, False),
        (46, 2, False),
        (13, 1, False),
    )
    for deck_size, roots, expected_to_fit in cases:
        assert (deck_size <= 3**roots) is expected_to_fit


def main() -> None:
    verify_symbolic_partner_and_euler_identities(2)
    verify_symbolic_partner_and_euler_identities(3)
    print("PASS: symbolic pinned-partner and Euler identities at k=2,3")
    verify_pinned_inclusion_certificates()
    print("PASS: exact pinned W_(1,t) ranks and named maximal minors")
    verify_first_deck_hierarchy()
    print("PASS: exact r>=2 ranks and r=1 dimension-27/65 tangent kernels")
    for n, k in PINNED_PIVOTS:
        verify_all_star_reconstruction(n, k)
    print("PASS: every star reconstructed in fixed q2 and q4 P5/P6/P7 charts")
    verify_sparse_matching_tori()
    print("PASS: exact nonzero sparse matching tori at q=2,4")
    verify_label_capacities()
    print("PASS: exact direct-label capacity boundaries")
    print("SCOPE: legal deck exposure and determinant forcing remain UNKNOWN")
    print("searches=0 project_imports=0 finite_fields=0")


if __name__ == "__main__":
    main()
