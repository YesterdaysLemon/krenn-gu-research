"""Verify the residual-hafnian Hessian Kneser and open-jet theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations
from math import comb

import sympy as sp

Edge = tuple[int, int]


def edge_list(q: int) -> tuple[Edge, ...]:
    return tuple(combinations(range(q), 2))


def double_factorial_odd(n: int) -> int:
    if n == -1:
        return 1
    value = 1
    for factor in range(1, n + 1, 2):
        value *= factor
    return value


def hafnian(vertices: tuple[int, ...], weights: dict[Edge, sp.Expr]) -> sp.Expr:
    @cache
    def recurse(active: tuple[int, ...]) -> sp.Expr:
        if not active:
            return sp.Integer(1)
        if len(active) % 2:
            return sp.Integer(0)
        first = active[0]
        total = sp.Integer(0)
        for position, partner in enumerate(active[1:], start=1):
            remainder = active[1:position] + active[position + 1 :]
            total += weights[tuple(sorted((first, partner)))] * recurse(remainder)
        return sp.expand(total)

    return recurse(tuple(sorted(vertices)))


def jet(
    q: int, weights: dict[Edge, sp.Expr]
) -> tuple[sp.Expr, sp.Matrix, sp.Matrix]:
    vertices = tuple(range(q))
    edges = edge_list(q)
    h_value = hafnian(vertices, weights)
    cofactors = sp.Matrix(
        [hafnian(tuple(v for v in vertices if v not in edge), weights) for edge in edges]
    )
    hessian = sp.zeros(len(edges))
    for row, edge in enumerate(edges):
        for column, other in enumerate(edges):
            if set(edge).isdisjoint(other):
                deleted = set(edge + other)
                hessian[row, column] = hafnian(
                    tuple(v for v in vertices if v not in deleted), weights
                )
    return h_value, cofactors, hessian


def kneser_matrix(q: int) -> sp.Matrix:
    edges = edge_list(q)
    return sp.Matrix(
        [
            [int(set(edge).isdisjoint(other)) for other in edges]
            for edge in edges
        ]
    )


def expected_kneser_hessian_det(q: int) -> int:
    number_edges = comb(q, 2)
    scale = double_factorial_odd(q - 5)
    return (
        scale**number_edges
        * comb(q - 2, 2)
        * (-(q - 3)) ** (q - 1)
    )


def check_generic_six_vertex_derivatives() -> None:
    q = 6
    vertices = tuple(range(q))
    edges = edge_list(q)
    variables = sp.symbols(f"x0:{len(edges)}")
    weights = dict(zip(edges, variables, strict=True))
    h_value, cofactors, hessian = jet(q, weights)

    for index, variable in enumerate(variables):
        assert sp.expand(sp.diff(h_value, variable) - cofactors[index]) == 0
    for row, variable in enumerate(variables):
        for column, other_variable in enumerate(variables):
            assert (
                sp.expand(
                    sp.diff(h_value, variable, other_variable)
                    - hessian[row, column]
                )
                == 0
            )

    edge_vector = sp.Matrix(variables)
    assert all(
        sp.expand(value) == 0
        for value in hessian * edge_vector - 2 * cofactors
    )
    assert sp.expand(edge_vector.dot(cofactors) - 3 * h_value) == 0

    for four_set in combinations(vertices, 4):
        i, j, k, ell = four_set
        edge_index = {edge: position for position, edge in enumerate(edges)}
        entries = (
            hessian[edge_index[(i, j)], edge_index[(k, ell)]],
            hessian[edge_index[(i, k)], edge_index[(j, ell)]],
            hessian[edge_index[(i, ell)], edge_index[(j, k)]],
        )
        assert entries[0] == entries[1] == entries[2]


def check_all_one_kneser_determinants() -> None:
    for q in (4, 6, 8):
        scale = double_factorial_odd(q - 5)
        hessian = scale * kneser_matrix(q)
        assert hessian.det() == expected_kneser_hessian_det(q)

        edges = edge_list(q)
        constant = sp.ones(len(edges), 1)
        assert hessian * constant == (
            scale * comb(q - 2, 2) * constant
        )

        vertex_values = [1, -1, *([0] * (q - 2))]
        vertex_mode = sp.Matrix(
            [vertex_values[i] + vertex_values[j] for i, j in edges]
        )
        assert hessian * vertex_mode == -scale * (q - 3) * vertex_mode

        cycle_values = {
            (0, 1): 1,
            (2, 3): 1,
            (0, 2): -1,
            (1, 3): -1,
        }
        cycle_mode = sp.Matrix([cycle_values.get(edge, 0) for edge in edges])
        assert hessian * cycle_mode == scale * cycle_mode


def check_nonconstant_open_jet() -> None:
    q = 6
    m = q // 2
    vertices = tuple(range(q))
    edges = edge_list(q)
    weights = {
        edge: sp.Integer(2 + (edge[0] + 1) * (edge[1] + 1)) for edge in edges
    }
    h_value, cofactors, hessian = jet(q, weights)
    delta = hessian.det()
    assert delta != 0

    edge_vector = sp.Matrix([weights[edge] for edge in edges])
    reconstructed = (m - 1) * hessian.inv() * cofactors
    assert reconstructed == edge_vector

    adjugate_times_c = delta * hessian.inv() * cofactors
    b_vector = (m - 1) * adjugate_times_c
    assert b_vector == delta * edge_vector
    b_weights = dict(zip(edges, b_vector, strict=True))

    for row, edge in enumerate(edges):
        for column, other in enumerate(edges):
            if not set(edge).isdisjoint(other):
                assert hessian[row, column] == 0
                continue
            deleted = set(edge + other)
            right = hafnian(
                tuple(v for v in vertices if v not in deleted), b_weights
            )
            assert delta ** (m - 2) * hessian[row, column] == right

    scalar_right = (m - 1) * cofactors.dot(adjugate_times_c)
    assert m * delta * h_value == scalar_right


def check_linear_shell_false_control() -> None:
    q = 4
    scaled = 2 * kneser_matrix(q)
    assert scaled.det() != 0
    edges = edge_list(q)
    for row, edge in enumerate(edges):
        for column, other in enumerate(edges):
            if set(edge).isdisjoint(other):
                # At q=4, the determinant-cleared right side is haf(empty)=1.
                assert scaled[row, column] == 2
                assert scaled[row, column] != 1
    assert comb(8, 4) > comb(8, 2)


def main() -> None:
    check_generic_six_vertex_derivatives()
    check_all_one_kneser_determinants()
    check_nonconstant_open_jet()
    check_linear_shell_false_control()
    print("residual hafnian Hessian Kneser/open-jet verification: PASS")
    print("q=4,6,8 all-one determinants: exact")
    print("generic q=6 derivative and Euler identities: exact")
    print("nonconstant q=6 determinant-cleared iff equations: exact")
    print("q=4 scaled-Kneser linear-shell false control: rejected")
    print("global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
