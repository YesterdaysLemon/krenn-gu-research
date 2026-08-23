"""Focused exact checks for the GLS42 hafnian first-variation boundary."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

Edge = tuple[str, str]


def edge_key(left: str, right: str) -> Edge:
    return tuple(sorted((left, right)))


def hafnian(
    vertices: tuple[str, ...], edge_values: dict[Edge, sp.Expr]
) -> sp.Expr:
    """Return the exact principal hafnian by the pivot recurrence."""

    @cache
    def recurse(active: tuple[str, ...]) -> sp.Expr:
        if not active:
            return sp.Integer(1)
        if len(active) % 2:
            return sp.Integer(0)
        first = active[0]
        total = sp.Integer(0)
        for index, partner in enumerate(active[1:], start=1):
            remainder = active[1:index] + active[index + 1 :]
            total += edge_values.get(edge_key(first, partner), sp.Integer(0)) * recurse(
                remainder
            )
        return sp.expand(total)

    return recurse(tuple(sorted(vertices)))


def first_variation(
    vertices: tuple[str, ...],
    edge_values: dict[Edge, sp.Expr],
    theta_values: dict[Edge, sp.Expr],
) -> sp.Expr:
    total = sp.Integer(0)
    for left, right in combinations(vertices, 2):
        remainder = tuple(vertex for vertex in vertices if vertex not in (left, right))
        total += theta_values.get(edge_key(left, right), sp.Integer(0)) * hafnian(
            remainder, edge_values
        )
    return sp.expand(total)


def verify_formal_identities() -> None:
    vertices = tuple(f"v{index}" for index in range(6))
    edges = list(combinations(vertices, 2))
    weights = {
        edge_key(*edge): sp.Symbol(f"w_{edge[0]}_{edge[1]}") for edge in edges
    }
    theta = {
        edge_key(*edge): sp.Symbol(f"d_{edge[0]}_{edge[1]}") for edge in edges
    }
    parameter = sp.Symbol("t")
    varied = {
        edge: weights[edge] + parameter * theta[edge] for edge in weights
    }

    coefficient = sp.expand(hafnian(vertices, varied)).coeff(parameter, 1)
    direct = first_variation(vertices, weights, theta)
    assert sp.expand(coefficient - direct) == 0

    pivot = vertices[0]
    recurrence = sp.Integer(0)
    for partner in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices if vertex not in (pivot, partner)
        )
        edge = edge_key(pivot, partner)
        recurrence += theta[edge] * hafnian(remainder, weights)
        recurrence += weights[edge] * first_variation(remainder, weights, theta)
    assert sp.expand(direct - recurrence) == 0

    gauges = {vertex: sp.Symbol(f"a_{vertex}") for vertex in vertices}
    gauge_theta = {
        edge_key(left, right): (gauges[left] + gauges[right])
        * weights[edge_key(left, right)]
        for left, right in edges
    }
    gauge_variation = first_variation(vertices, weights, gauge_theta)
    expected = sum(gauges.values()) * hafnian(vertices, weights)
    assert sp.expand(gauge_variation - expected) == 0


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[row, column] for row in range(3) for column in range(3)])


def pair_incidence(left: sp.Matrix, right: sp.Matrix, i: int, j: int) -> sp.Matrix:
    left_vector = left[:, i]
    right_vector = right[:, j]
    return left_vector * right_vector.T + right_vector * left_vector.T


def projected_pair_tensor(
    left: sp.Matrix, right: sp.Matrix, root_row: int, root_column: int
) -> sp.Matrix:
    result = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            result[i, j] = pair_incidence(left, right, i, j)[
                root_row, root_column
            ]
    return result


def verify_physical_control() -> None:
    labels = ("q0", "u0", "q1", "u1", "u2", "u3")
    q_pair = edge_key("q0", "q1")
    projectors = [sp.diag(1, 0, 0), sp.diag(0, 1, 0), sp.diag(0, 0, 1)]
    maps = {
        "q0": projectors[0],
        "u0": projectors[0] - projectors[1],
        "q1": projectors[1],
        "u1": projectors[1],
        "u2": projectors[2],
        "u3": projectors[2],
    }

    incidence_columns: list[sp.Matrix] = []
    for left, right in combinations(labels, 2):
        if edge_key(left, right) == q_pair:
            continue
        for i in range(3):
            for j in range(3):
                incidence_columns.append(
                    vectorize(pair_incidence(maps[left], maps[right], i, j))
                )
    sigma = sp.Matrix.hstack(*incidence_columns)
    assert sigma.rank() == 6

    ones = sp.ones(3, 1)
    q_left = maps["q0"] * ones
    q_right = maps["q1"] * ones
    q_matrix = q_left * q_right.T + q_right * q_left.T
    delta_columns = [vectorize(projector) for projector in projectors]
    source_space = sp.Matrix.hstack(*delta_columns, vectorize(q_matrix))
    assert source_space.rank() == 4
    assert sp.Matrix.hstack(sigma, source_space).rank() == 6
    assert q_matrix == sp.Matrix(((0, 1, 0), (1, 0, 0), (0, 0, 0)))

    colours = {"q0": 0, "u0": 0, "q1": 1, "u1": 1, "u2": 2, "u3": 2}
    scalar_weights = {
        edge_key("q0", "u2"): sp.Rational(1),
        edge_key("q0", "u3"): sp.Rational(-1, 3),
        edge_key("u0", "u2"): sp.Rational(1, 3),
        edge_key("u0", "u3"): sp.Rational(-1),
        edge_key("q1", "u1"): sp.Rational(1),
        edge_key("u0", "u1"): sp.Rational(1),
        edge_key("u2", "u3"): sp.Rational(1),
        edge_key("q0", "q1"): sp.Rational(1),
    }
    vertex_gauge = dict(zip(labels, (-1, 1, 1, -1, 2, -2), strict=True))

    tensor_weights: dict[Edge, sp.Matrix] = {}
    theta_02: dict[Edge, sp.Matrix] = {}
    theta_01: dict[Edge, sp.Matrix] = {}
    for left, right in combinations(labels, 2):
        edge = edge_key(left, right)
        weight_tensor = sp.zeros(3, 3)
        if edge in scalar_weights:
            weight_tensor[colours[left], colours[right]] = scalar_weights[edge]
        tensor_weights[edge] = weight_tensor
        theta_02[edge] = projected_pair_tensor(maps[left], maps[right], 0, 2)
        theta_01[edge] = projected_pair_tensor(maps[left], maps[right], 0, 1)
        assert theta_02[edge] == (
            vertex_gauge[left] + vertex_gauge[right]
        ) * weight_tensor

    assert sum(vertex_gauge.values()) == 0
    active_02 = {edge for edge, tensor in theta_02.items() if tensor != sp.zeros(3)}
    assert active_02 == {
        edge_key("q0", "u2"),
        edge_key("q0", "u3"),
        edge_key("u0", "u2"),
        edge_key("u0", "u3"),
    }

    assert hafnian(("q0", "q1"), scalar_weights) == 1
    assert hafnian(("u0", "u1", "u2", "u3"), scalar_weights) == 1
    assert hafnian(labels, scalar_weights) == sp.Rational(-1, 9)

    deletion_values = {
        edge_key("u0", "u3"): sp.Rational(1),
        edge_key("u0", "u2"): sp.Rational(-1, 3),
        edge_key("q0", "u3"): sp.Rational(1, 3),
        edge_key("q0", "u2"): sp.Rational(-1),
    }
    for deleted_edge, expected in deletion_values.items():
        remainder = tuple(vertex for vertex in labels if vertex not in deleted_edge)
        assert hafnian(remainder, scalar_weights) == expected
        assert expected != 0

    scalar_theta_02 = {
        edge: tensor[colours[edge[0]], colours[edge[1]]]
        for edge, tensor in theta_02.items()
    }
    assert first_variation(labels, scalar_weights, scalar_theta_02) == 0

    variables = {
        (label, coordinate): sp.Symbol(f"x_{label}_{coordinate}")
        for label in labels
        for coordinate in range(3)
    }
    polynomial_weights: dict[Edge, sp.Expr] = {}
    polynomial_theta_01: dict[Edge, sp.Expr] = {}
    for left, right in combinations(labels, 2):
        edge = edge_key(left, right)
        polynomial_weights[edge] = scalar_weights.get(edge, 0) * variables[
            left, colours[left]
        ] * variables[right, colours[right]]
        polynomial_theta_01[edge] = sum(
            theta_01[edge][i, j] * variables[left, i] * variables[right, j]
            for i in range(3)
            for j in range(3)
        )
    failed_01 = first_variation(labels, polynomial_weights, polynomial_theta_01)
    full_word = sp.prod(variables[label, colours[label]] for label in labels)
    correction_word = (
        variables["q0", 0]
        * variables["u0", 1]
        * variables["q1", 1]
        * variables["u1", 1]
        * variables["u2", 2]
        * variables["u3", 2]
    )
    assert sp.expand(failed_01 - 2 * full_word + correction_word) == 0

    epsilon_q = sum(q_matrix)
    assert epsilon_q == 2
    assert (ones.T * maps["u0"] * ones)[0] == 0

    source_ports = ("u1", "u2", "u3")
    pi_q = sp.Integer(0)
    for left, right in combinations(source_ports, 2):
        remaining = next(port for port in source_ports if port not in (left, right))
        root_coefficient = 2 * variables[left, colours[left]] * variables[
            right, colours[right]
        ]
        old_root_edge = scalar_weights[edge_key("u0", remaining)] * variables[
            remaining, colours[remaining]
        ]
        pi_q += root_coefficient * old_root_edge
    expected_pi = (
        sp.Rational(2, 3)
        * variables["u1", 1]
        * variables["u2", 2]
        * variables["u3", 2]
    )
    assert sp.expand(pi_q - expected_pi) == 0


def main() -> None:
    verify_formal_identities()
    verify_physical_control()
    print("GLS42 excess hafnian first-variation primary checks: PASS")


if __name__ == "__main__":
    main()
