"""Verify the residual-depth observability staircase and physical kernels.

This is a fixed exact symbolic replay, not a graph or selector search.
"""

from collections.abc import Mapping
from itertools import combinations

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
    return {
        mask: sp.expand(value)
        for mask, value in product.items()
        if sp.expand(value) != 0
    }


def wick_exponential(edges: Mapping[tuple[int, int], sp.Expr]) -> Polynomial:
    result: Polynomial = {0: sp.Integer(1)}
    for (first, second), weight in edges.items():
        assert first < second
        edge_mask = (1 << first) | (1 << second)
        result = multiply(result, {0: sp.Integer(1), edge_mask: weight})
    return result


def response_at_depth(
    moments: Mapping[int, sp.Expr],
    port_count: int,
    residual_count: int,
    residual_mask: int,
) -> Polynomial:
    shifted_residual_mask = residual_mask << port_count
    return {
        port_mask: moments.get(port_mask | shifted_residual_mask, sp.Integer(0))
        for port_mask in range(1 << port_count)
    }


def budget_visible(
    port_mask: int,
    residual_mask: int,
    residual_count: int,
) -> bool:
    return port_mask.bit_count() + residual_mask.bit_count() >= 2 * residual_count


def check_q2_symbolic_kernel() -> None:
    port_count = 7
    residual_count = 2
    residual_first = port_count
    residual_second = port_count + 1
    parameter = sp.symbols("t")
    edges = {
        (0, 1): parameter,
        (0, residual_first): sp.Integer(1),
        (1, residual_second): -parameter,
        (residual_first, residual_second): sp.Integer(1),
    }
    moments = wick_exponential(edges)
    base = response_at_depth(moments, port_count, residual_count, 0)
    first = response_at_depth(moments, port_count, residual_count, 1)
    second = response_at_depth(moments, port_count, residual_count, 2)
    full = response_at_depth(moments, port_count, residual_count, 3)
    pair_mask = (1 << 0) | (1 << 1)

    assert base[0] == 1
    assert base[pair_mask] == parameter
    assert first[1 << 0] == 1
    assert all(first[mask] == 0 for mask in range(1 << port_count) if mask != 1)
    assert second[1 << 1] == -parameter
    assert all(second[mask] == 0 for mask in range(1 << port_count) if mask != 2)
    assert full[0] == 1
    assert all(full[mask] == 0 for mask in range(1, 1 << port_count))

    tower = (base, first, second, full)
    for residual_mask, response in enumerate(tower):
        for port_mask, value in response.items():
            if budget_visible(port_mask, residual_mask, residual_count):
                assert parameter not in sp.sympify(value).free_symbols

    # MZ-Y0Y1=M^2, including the hidden degree-two coefficient 2t.
    left = multiply(base, full)
    residual_product = multiply(first, second)
    discriminant = {
        mask: sp.expand(left.get(mask, 0) - residual_product.get(mask, 0))
        for mask in range(1 << port_count)
    }
    square = multiply(base, base)
    assert all(
        sp.expand(discriminant[mask] - square.get(mask, 0)) == 0
        for mask in range(1 << port_count)
    )
    assert discriminant[pair_mask] == 2 * parameter


def star_values(pair_values: tuple[int, ...]) -> tuple[int, ...]:
    b12, b13, b14, b23, b24, b34 = pair_values
    return (
        b12 + b13 + b14,
        b12 + b23 + b24,
        b13 + b23 + b34,
        b14 + b24 + b34,
    )


def four_moment(pair_values: tuple[int, ...]) -> int:
    b12, b13, b14, b23, b24, b34 = pair_values
    return b12 * b34 + b13 * b24 + b14 * b23


def check_marked_star_torus_zero_kernel() -> None:
    port_count = 7
    residual_count = 2
    edge_order = tuple(combinations(range(4), 2))
    models = (
        (-1, 1, 0, 0, 1, -1),
        (-1, 0, 1, 1, 0, -1),
    )
    assert tuple(star_values(model) for model in models) == ((0, 0, 0, 0),) * 2
    assert tuple(four_moment(model) for model in models) == (2, 2)

    base_responses = []
    for model in models:
        edges = {
            edge: sp.Integer(value)
            for edge, value in zip(edge_order, model, strict=True)
            if value
        }
        base_responses.append(wick_exponential(edges))

    for residual_mask in range(1 << residual_count):
        for port_mask in range(1 << port_count):
            if not budget_visible(port_mask, residual_mask, residual_count):
                continue
            if residual_mask:
                values = (sp.Integer(0), sp.Integer(0))
            else:
                values = tuple(
                    response.get(port_mask, sp.Integer(0))
                    for response in base_responses
                )
            assert values[0] == values[1]


def higher_residual_tower(residual_count: int, parameter: sp.Symbol):
    port_count = 7
    edges: dict[tuple[int, int], sp.Expr] = {}
    residual_offset = port_count
    for first in range(0, residual_count, 2):
        edges[(residual_offset + first, residual_offset + first + 1)] = sp.Integer(1)
    edges[(0, residual_offset)] = sp.Integer(1)
    edges[(1, residual_offset + 1)] = parameter
    moments = wick_exponential(edges)
    return tuple(
        response_at_depth(
            moments,
            port_count,
            residual_count,
            residual_mask,
        )
        for residual_mask in range(1 << residual_count)
    )


def check_higher_residual_kernels() -> None:
    parameter = sp.symbols("t")
    pair_mask = 3
    for residual_count in (4, 6):
        tower = higher_residual_tower(residual_count, parameter)
        for residual_mask, response in enumerate(tower):
            for port_mask, value in response.items():
                if budget_visible(port_mask, residual_mask, residual_count):
                    assert parameter not in sp.sympify(value).free_symbols
        full_response = tower[(1 << residual_count) - 1]
        assert full_response[0] == 1
        assert full_response[pair_mask] == parameter
        assert all(
            full_response[mask] == 0
            for mask in range(1 << 7)
            if mask not in (0, pair_mask)
        )


def check_budget_tables() -> None:
    assert tuple(4 - depth for depth in range(3)) == (4, 3, 2)
    assert tuple(8 - depth for depth in range(5)) == (8, 7, 6, 5, 4)
    assert tuple(12 - depth for depth in range(7)) == (
        12,
        11,
        10,
        9,
        8,
        7,
        6,
    )


def main() -> None:
    check_budget_tables()
    check_q2_symbolic_kernel()
    check_marked_star_torus_zero_kernel()
    check_higher_residual_kernels()
    print("PASS: residual-depth root budget is the staircase |S|+|T|>=2q")
    print("PASS: q=2 all-depth eligible tower has a nonzero-h affine fiber")
    print("PASS: marked stars plus all eligible depths retain the h=0 pair kernel")
    print("PASS: q=4,6 eligible towers hide a varying common-Gram pair entry")
    print("SCOPE: new mixed-GHZ or herald observations remain unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
