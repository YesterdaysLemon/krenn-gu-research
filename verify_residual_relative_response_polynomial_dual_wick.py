"""Verify the residual-relative response polynomial and dual-Wick theorem."""

from __future__ import annotations

from collections.abc import Mapping

import sympy as sp

Polynomial = dict[int, sp.Expr]


def multiply(left: Mapping[int, sp.Expr], right: Mapping[int, sp.Expr]) -> Polynomial:
    product: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            product[mask] = product.get(mask, 0) + left_value * right_value
    return {mask: sp.expand(value) for mask, value in product.items()}


def wick_exponential(edges: Mapping[tuple[int, int], sp.Expr]) -> Polynomial:
    result: Polynomial = {0: sp.Integer(1)}
    for (first, second), weight in edges.items():
        assert first < second
        edge_mask = (1 << first) | (1 << second)
        result = multiply(result, {0: sp.Integer(1), edge_mask: weight})
    return result


def response_with_residuals(
    moments: Mapping[int, sp.Expr], port_count: int, residual_count: int
) -> Polynomial:
    residual_mask = ((1 << residual_count) - 1) << port_count
    return {
        port_mask: moments.get(port_mask | residual_mask, sp.Integer(0))
        for port_mask in range(1 << port_count)
    }


def permanent_subset_dp(matrix: sp.Matrix) -> sp.Expr:
    assert matrix.rows == matrix.cols
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in range(matrix.rows):
        next_states: dict[int, sp.Expr] = {}
        for mask, coefficient in states.items():
            for column in range(matrix.cols):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                next_states[new_mask] = (
                    next_states.get(new_mask, 0)
                    + coefficient * matrix[row, column]
                )
        states = next_states
    return sp.expand(states[(1 << matrix.rows) - 1])


def check_two_residual_symbolic_factorization() -> None:
    port_count = 4
    h = sp.symbols("h")
    a = sp.symbols("a0:4")
    b = sp.symbols("b0:4")
    port_edges = {
        (first, second): sp.symbols(f"B{first}{second}")
        for first in range(port_count)
        for second in range(first + 1, port_count)
    }
    full_edges = dict(port_edges)
    residual_first = port_count
    residual_second = port_count + 1
    full_edges[(residual_first, residual_second)] = h
    for port in range(port_count):
        full_edges[(port, residual_first)] = a[port]
        full_edges[(port, residual_second)] = b[port]

    base = wick_exponential(port_edges)
    full = wick_exponential(full_edges)
    response = response_with_residuals(full, port_count, 2)
    relative: Polynomial = {0: h}
    pair_values: dict[tuple[int, int], sp.Expr] = {}
    for first in range(port_count):
        for second in range(first + 1, port_count):
            value = a[first] * b[second] + b[first] * a[second]
            pair_values[(first, second)] = value
            relative[(1 << first) | (1 << second)] = value

    expected = multiply(base, relative)
    for mask in range(1 << port_count):
        assert sp.expand(response[mask] - expected.get(mask, 0)) == 0

    corrected = {
        mask: sp.expand(response[mask] - h * base.get(mask, 0))
        for mask in range(1 << port_count)
    }
    top_mask = (1 << port_count) - 1
    four_point = sp.Integer(0)
    for first in range(port_count):
        for second in range(first + 1, port_count):
            pair_mask = (1 << first) | (1 << second)
            complement = top_mask ^ pair_mask
            four_point += pair_values[(first, second)] * base.get(complement, 0)
    assert sp.expand(corrected[top_mask] - four_point) == 0

    completed_channel = sp.Matrix(a) * sp.Matrix(b).T + sp.Matrix(b) * sp.Matrix(a).T
    assert completed_channel.rank() <= 2


def check_four_residual_symbolic_tower() -> None:
    port_count = 4
    residual_count = 4
    residual_edges = {
        (first, second): sp.symbols(f"A{first}{second}")
        for first in range(residual_count)
        for second in range(first + 1, residual_count)
    }
    incidence = sp.symbols("r0:4")
    full_edges: dict[tuple[int, int], sp.Expr] = {
        (port_count + first, port_count + second): value
        for (first, second), value in residual_edges.items()
    }
    for index, value in enumerate(incidence):
        full_edges[(index, port_count + index)] = value

    response = response_with_residuals(
        wick_exponential(full_edges), port_count, residual_count
    )
    a01 = residual_edges[(0, 1)]
    a02 = residual_edges[(0, 2)]
    a03 = residual_edges[(0, 3)]
    a12 = residual_edges[(1, 2)]
    a13 = residual_edges[(1, 3)]
    a23 = residual_edges[(2, 3)]
    residual_hafnian = a01 * a23 + a02 * a13 + a03 * a12
    assert sp.expand(response[0] - residual_hafnian) == 0

    for first in range(port_count):
        for second in range(first + 1, port_count):
            remaining = [
                index
                for index in range(residual_count)
                if index not in (first, second)
            ]
            cofactor = residual_edges[tuple(remaining)]
            mask = (1 << first) | (1 << second)
            expected = incidence[first] * incidence[second] * cofactor
            assert sp.expand(response[mask] - expected) == 0

    top_mask = (1 << port_count) - 1
    assert sp.expand(response[top_mask] - sp.prod(incidence)) == 0


def check_cross_depth_disjoint_flattening() -> None:
    residual_count = 4
    left = sp.Matrix(residual_count, 2, sp.symbols("l0:8"))
    right = sp.Matrix(residual_count, 3, sp.symbols("v0:12"))
    residual_edges = {
        (first, second): sp.symbols(f"c{first}{second}")
        for first in range(residual_count)
        for second in range(first + 1, residual_count)
    }
    cofactor = sp.zeros(residual_count)
    for first in range(residual_count):
        for second in range(first + 1, residual_count):
            remaining = [
                index
                for index in range(residual_count)
                if index not in (first, second)
            ]
            value = residual_edges[tuple(remaining)]
            cofactor[first, second] = value
            cofactor[second, first] = value

    degree_two = left.T * cofactor * right
    degree_four_middle = sp.Matrix(
        [
            permanent_subset_dp(right.extract(
                [row for row in range(residual_count) if row != omitted],
                range(right.cols),
            ))
            for omitted in range(residual_count)
        ]
    )
    degree_four = left.T * degree_four_middle
    for left_port in range(left.cols):
        direct = permanent_subset_dp(
            sp.Matrix.hstack(left[:, left_port], right)
        )
        assert sp.expand(degree_four[left_port, 0] - direct) == 0

    combined = degree_two.row_join(degree_four)
    common_middle = (cofactor * right).row_join(degree_four_middle)
    difference = combined - left.T * common_middle
    assert all(sp.expand(entry) == 0 for entry in difference)


def main() -> None:
    check_two_residual_symbolic_factorization()
    check_four_residual_symbolic_tower()
    check_cross_depth_disjoint_flattening()
    print("residual-relative response polynomial and dual-Wick theorem: PASS")
    print("symbolic q=2 tangent, q=4 tower, and cross-depth factorization")


if __name__ == "__main__":
    main()
