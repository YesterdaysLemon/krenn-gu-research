"""Verify arbitrary-order hafnian Euler--Hessian channel unmixing."""

from __future__ import annotations

from functools import cache
from itertools import combinations

import sympy as sp

Edge = tuple[int, int]


def edge_list(q: int) -> tuple[Edge, ...]:
    return tuple(combinations(range(q), 2))


def hafnian(vertices: tuple[int, ...], weights: dict[Edge, sp.Expr]) -> sp.Expr:
    @cache
    def visit(active: tuple[int, ...]) -> sp.Expr:
        if not active:
            return sp.Integer(1)
        first = active[0]
        total = sp.Integer(0)
        for offset, partner in enumerate(active[1:], start=1):
            remainder = active[1:offset] + active[offset + 1 :]
            total += weights[tuple(sorted((first, partner)))] * visit(remainder)
        return sp.expand(total)

    return visit(tuple(sorted(vertices)))


def symbolic_hafnian_jet(
    q: int,
) -> tuple[
    tuple[Edge, ...],
    tuple[sp.Symbol, ...],
    sp.Expr,
    sp.Matrix,
    sp.Matrix,
    tuple[sp.Matrix, ...],
]:
    edges = edge_list(q)
    variables = sp.symbols(f"a0:{len(edges)}")
    weights = dict(zip(edges, variables, strict=True))
    h_value = hafnian(tuple(range(q)), weights)
    c_vector = sp.Matrix([sp.diff(h_value, variable) for variable in variables])
    d_matrix = c_vector.jacobian(variables)
    j_slices = tuple(d_matrix.diff(variable) for variable in variables)
    return edges, variables, h_value, c_vector, d_matrix, j_slices


def response_polynomials(
    h_value: sp.Expr,
    c_vector: sp.Matrix,
    variables: tuple[sp.Symbol, ...],
    direct: sp.Matrix,
    channels: sp.Matrix,
) -> tuple[sp.Matrix, sp.Matrix, tuple[sp.Matrix, ...]]:
    width = direct.rows
    response = sp.Matrix(
        [
            sp.expand(
                h_value * direct[column]
                + sum(
                    c_vector[edge] * channels[edge, column]
                    for edge in range(len(variables))
                )
            )
            for column in range(width)
        ]
    )
    gradient = sp.Matrix(
        [
            [sp.diff(response[column], variable) for column in range(width)]
            for variable in variables
        ]
    )
    response_hessians = tuple(
        sp.hessian(response[column], variables) for column in range(width)
    )
    return response, gradient, response_hessians


def contract_third(
    third_slices: tuple[sp.Matrix, ...], vector: sp.Matrix
) -> sp.Matrix:
    answer = sp.zeros(third_slices[0].rows)
    for index, third_slice in enumerate(third_slices):
        answer += third_slice * vector[index]
    return answer


def substitute_matrix(matrix: sp.Matrix, values: dict[sp.Symbol, sp.Expr]) -> sp.Matrix:
    return matrix.applyfunc(lambda entry: sp.expand(entry.subs(values)))


def check_six_vertex_open_unmixing() -> None:
    q = 6
    m = q // 2
    edges, variables, h_poly, c_poly, d_poly, j_poly = symbolic_hafnian_jet(q)
    direct = sp.Matrix([2, -3])
    channels = sp.Matrix(
        [
            [index + 1, (-1) ** index * (index + 2)]
            for index in range(len(edges))
        ]
    )
    response, gradient, response_hessians = response_polynomials(
        h_poly, c_poly, variables, direct, channels
    )

    weights = {
        variable: sp.Integer(2 + (edge[0] + 1) * (edge[1] + 1))
        for edge, variable in zip(edges, variables, strict=True)
    }
    edge_vector = sp.Matrix([weights[variable] for variable in variables])
    h_value = sp.expand(h_poly.subs(weights))
    c_vector = substitute_matrix(c_poly, weights)
    d_matrix = substitute_matrix(d_poly, weights)
    j_slices = tuple(substitute_matrix(third, weights) for third in j_poly)
    l_value = substitute_matrix(response, weights)
    g_matrix = substitute_matrix(gradient, weights)
    g_hessians = tuple(
        substitute_matrix(response_hessian, weights)
        for response_hessian in response_hessians
    )

    delta = d_matrix.det()
    assert delta != 0
    assert h_value != 0
    assert d_matrix * edge_vector == (m - 1) * c_vector

    expected_gradient = c_vector * direct.T + d_matrix * channels
    assert g_matrix == expected_gradient
    for column in range(direct.rows):
        expected_hessian = direct[column] * d_matrix + contract_third(
            j_slices, channels[:, column]
        )
        assert g_hessians[column] == expected_hessian

    d_inverse = d_matrix.inv()
    adjugate = delta * d_inverse
    that = adjugate * g_matrix
    expected_that = delta * (
        channels + edge_vector * direct.T / (m - 1)
    )
    assert that == expected_that

    first_scalar = c_vector.dot(that[:, 0]) - delta * l_value[0]
    second_scalar = c_vector.dot(that[:, 1]) - delta * l_value[1]
    assert (m - 1) * first_scalar == delta * h_value * direct[0]
    assert (m - 1) * second_scalar == delta * h_value * direct[1]

    recovered_direct_second: list[sp.Expr] = []
    recovered_channels = sp.zeros(len(edges), direct.rows)
    for column in range(direct.rows):
        t_tilde = d_inverse * g_matrix[:, column]
        s_matrix = g_hessians[column] - contract_third(j_slices, t_tilde)
        d_inverse_s = d_inverse * s_matrix
        recovered_u = sp.expand((m - 1) * sp.trace(d_inverse_s) / len(edges))
        assert d_inverse_s == sp.eye(len(edges)) * recovered_u / (m - 1)
        recovered_direct_second.append(recovered_u)
        recovered_channels[:, column] = t_tilde - edge_vector * recovered_u / (
            m - 1
        )

        shat = delta * g_hessians[column] - contract_third(
            j_slices, that[:, column]
        )
        assert (m - 1) * shat == delta * d_matrix * direct[column]

    assert sp.Matrix(recovered_direct_second) == direct
    assert recovered_channels == channels

    recovered_direct_first = sp.Matrix(
        [
            sp.expand(
                (m - 1)
                * (c_vector.dot(d_inverse * g_matrix[:, column]) - l_value[column])
                / h_value
            )
            for column in range(direct.rows)
        ]
    )
    assert recovered_direct_first == direct

    bad_hessian = g_hessians[0].copy()
    bad_hessian[0, 1] += 1
    bad_hessian[1, 0] += 1
    bad_s = bad_hessian - contract_third(j_slices, d_inverse * g_matrix[:, 0])
    normalized_bad = d_inverse * bad_s
    scalar_part = sp.trace(normalized_bad) / len(edges)
    assert normalized_bad != sp.eye(len(edges)) * scalar_part


def check_four_vertex_zero_hafnian_gauge() -> None:
    q = 4
    m = q // 2
    edges, variables, h_poly, c_poly, d_poly, j_poly = symbolic_hafnian_jet(q)
    direct = sp.Matrix([3, -4])
    channels = sp.Matrix(
        [[index + 2, 2 * index - 3] for index in range(len(edges))]
    )
    response, gradient, response_hessians = response_polynomials(
        h_poly, c_poly, variables, direct, channels
    )
    assigned = [1, 1, 1, -2, 1, 1]
    weights = dict(zip(variables, map(sp.Integer, assigned), strict=True))
    edge_vector = sp.Matrix(assigned)
    h_value = sp.expand(h_poly.subs(weights))
    c_vector = substitute_matrix(c_poly, weights)
    d_matrix = substitute_matrix(d_poly, weights)
    j_slices = tuple(substitute_matrix(third, weights) for third in j_poly)
    l_value = substitute_matrix(response, weights)
    g_matrix = substitute_matrix(gradient, weights)
    g_hessians = tuple(
        substitute_matrix(response_hessian, weights)
        for response_hessian in response_hessians
    )

    assert h_value == 0
    assert all(weight != 0 for weight in assigned)
    assert d_matrix.det() != 0
    assert all(third == sp.zeros(len(edges)) for third in j_slices)
    d_inverse = d_matrix.inv()

    for column in range(direct.rows):
        assert l_value[column] == c_vector.dot(d_inverse * g_matrix[:, column])

    gauge = sp.Matrix([5, -7])
    shifted_direct = direct - (m - 1) * gauge
    shifted_channels = channels + edge_vector * gauge.T
    shifted_value = h_value * shifted_direct + shifted_channels.T * c_vector
    shifted_gradient = c_vector * shifted_direct.T + d_matrix * shifted_channels
    assert shifted_value == l_value
    assert shifted_gradient == g_matrix
    assert shifted_direct != direct
    assert shifted_channels != channels

    recovered_direct: list[sp.Expr] = []
    recovered_channels = sp.zeros(len(edges), direct.rows)
    for column in range(direct.rows):
        t_tilde = d_inverse * g_matrix[:, column]
        s_matrix = g_hessians[column] - contract_third(j_slices, t_tilde)
        recovered_u = sp.expand(
            (m - 1) * sp.trace(d_inverse * s_matrix) / len(edges)
        )
        recovered_direct.append(recovered_u)
        recovered_channels[:, column] = t_tilde - edge_vector * recovered_u / (
            m - 1
        )
    assert sp.Matrix(recovered_direct) == direct
    assert recovered_channels == channels


def check_six_vertex_singular_discriminant() -> None:
    q = 6
    edges, variables, h_poly, c_poly, d_poly, _ = symbolic_hafnian_jet(q)
    left = {0, 1, 2}
    parameter = sp.symbols("t")
    family: dict[sp.Symbol, sp.Expr] = {}
    for edge, variable in zip(edges, variables, strict=True):
        if edge[0] in left and edge[1] in left:
            family[variable] = sp.Integer(1)
        elif edge[0] not in left and edge[1] not in left:
            family[variable] = sp.Integer(2)
        else:
            family[variable] = parameter

    family_hessian = substitute_matrix(d_poly, family)
    assert sp.factor(family_hessian.det()) == -46656 * parameter**5 * (
        parameter - 1
    ) * (parameter + 1)

    singular_values = {parameter: sp.Integer(1)}
    d_matrix = substitute_matrix(family_hessian, singular_values)
    c_vector = substitute_matrix(substitute_matrix(c_poly, family), singular_values)
    h_value = sp.expand(h_poly.subs(family).subs(singular_values))
    assert h_value == 24
    assert d_matrix.rank() == len(edges) - 1
    adjugate = d_matrix.adjugate()
    assert adjugate != sp.zeros(len(edges))

    direct = sp.Matrix([2, -3])
    channels = sp.Matrix(
        [
            [index + 1, (-1) ** index * (index + 2)]
            for index in range(len(edges))
        ]
    )
    gradient = c_vector * direct.T + d_matrix * channels
    assert adjugate * gradient == sp.zeros(len(edges), direct.rows)

    kernel = d_matrix.nullspace()[0]
    assert (kernel.T * gradient) == sp.zeros(1, direct.rows)
    bad_gradient = gradient.copy()
    bad_gradient[:, 0] += kernel
    assert adjugate * bad_gradient[:, 0] != sp.zeros(len(edges), 1)


def check_conditional_support_arithmetic() -> None:
    for roots, expected in ((3, 18), (4, 21), (5, 24)):
        order = roots + 2
        assert 3 * order + 3 == 3 * roots + 9 == expected


def main() -> None:
    check_six_vertex_open_unmixing()
    check_four_vertex_zero_hafnian_gauge()
    check_six_vertex_singular_discriminant()
    check_conditional_support_arithmetic()
    print("hafnian Euler-Hessian channel unmixing verification: PASS")
    print("fixed symbolic q=6 open response and both recovery formulas: exact")
    print("fixed full-torus q=4 h=0 gauge and second-jet separation: exact")
    print("q=6 two-block determinant and corank-one adjugate test: exact")
    print("conditional P5/P6/P7 support arithmetic 18/21/24: exact")
    print("legal exposure of response edge jets: UNKNOWN")
    print("global Krenn-Gu: UNRESOLVED")


if __name__ == "__main__":
    main()
