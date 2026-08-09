"""Primary exact checks for the four-residual even Wick tower theorem."""

from __future__ import annotations

from itertools import combinations
from math import factorial

import sympy as sp

Polynomial = dict[int, sp.Expr]
RESIDUAL_EDGES = tuple(combinations(range(4), 2))


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for mask, coefficient in polynomial.items():
            result[mask] = result.get(mask, 0) + coefficient
    return {
        mask: sp.expand(coefficient)
        for mask, coefficient in result.items()
        if sp.expand(coefficient) != 0
    }


def scale(polynomial: Polynomial, scalar: sp.Expr) -> Polynomial:
    return add(
        {
            mask: sp.expand(scalar * coefficient)
            for mask, coefficient in polynomial.items()
        }
    )


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = (
                result.get(mask, 0) + left_coefficient * right_coefficient
            )
    return add(result)


def constant(value: sp.Expr) -> Polynomial:
    return {} if value == 0 else {0: value}


def linear(values: tuple[sp.Expr, ...]) -> Polynomial:
    return {1 << index: value for index, value in enumerate(values) if value != 0}


def exponential(quadratic: Polynomial, port_count: int) -> Polynomial:
    result = constant(sp.Integer(1))
    power = constant(sp.Integer(1))
    for degree in range(1, port_count // 2 + 1):
        power = multiply(power, quadratic)
        result = add(result, scale(power, sp.Rational(1, factorial(degree))))
    return result


def complement(pair: tuple[int, int]) -> tuple[int, int]:
    return tuple(vertex for vertex in range(4) if vertex not in pair)  # type: ignore[return-value]


def equal(left: Polynomial, right: Polynomial) -> bool:
    return not add(left, scale(right, -1))


def generic_even_tower_check() -> None:
    port_count = 6
    a_symbols = sp.symbols("a01 a02 a03 a12 a13 a23")
    residual_edges = dict(zip(RESIDUAL_EDGES, a_symbols, strict=True))
    incidence_symbols = sp.symbols(f"r0:{4 * port_count}")
    loops = tuple(
        linear(
            tuple(
                incidence_symbols[vertex * port_count + port]
                for port in range(port_count)
            )
        )
        for vertex in range(4)
    )

    port_quadratic: Polynomial = {}
    for value, (left, right) in enumerate(combinations(range(port_count), 2), 1):
        port_quadratic[(1 << left) | (1 << right)] = sp.Integer(value)
    moment = exponential(port_quadratic, port_count)
    inverse_moment = exponential(scale(port_quadratic, -1), port_count)
    assert equal(multiply(moment, inverse_moment), constant(sp.Integer(1)))

    pair_products = {
        pair: multiply(loops[pair[0]], loops[pair[1]])
        for pair in RESIDUAL_EDGES
    }
    normalized_pairs = {
        pair: add(constant(residual_edges[pair]), pair_products[pair])
        for pair in RESIDUAL_EDGES
    }

    residual_hafnian = (
        residual_edges[(0, 1)] * residual_edges[(2, 3)]
        + residual_edges[(0, 2)] * residual_edges[(1, 3)]
        + residual_edges[(0, 3)] * residual_edges[(1, 2)]
    )
    mixed_terms = add(
        *(
            scale(pair_products[complement(pair)], residual_edges[pair])
            for pair in RESIDUAL_EDGES
        )
    )
    four_linear = multiply(pair_products[(0, 1)], pair_products[(2, 3)])
    normalized_top = add(constant(residual_hafnian), mixed_terms, four_linear)

    pair_decks = {
        pair: multiply(moment, normalized_pairs[pair]) for pair in RESIDUAL_EDGES
    }
    top_deck = multiply(moment, normalized_top)
    corrected = {
        pair: add(pair_decks[pair], scale(moment, -residual_edges[pair]))
        for pair in RESIDUAL_EDGES
    }

    for pair in RESIDUAL_EDGES:
        recovered = multiply(inverse_moment, pair_decks[pair])
        assert equal(recovered, normalized_pairs[pair])
        assert equal(multiply(inverse_moment, corrected[pair]), pair_products[pair])

    complementary_products = (
        multiply(pair_products[(0, 1)], pair_products[(2, 3)]),
        multiply(pair_products[(0, 2)], pair_products[(1, 3)]),
        multiply(pair_products[(0, 3)], pair_products[(1, 2)]),
    )
    assert equal(complementary_products[0], complementary_products[1])
    assert equal(complementary_products[0], complementary_products[2])

    division_free_right = add(
        scale(multiply(moment, moment), residual_hafnian),
        multiply(
            moment,
            add(
                *(
                    scale(corrected[complement(pair)], residual_edges[pair])
                    for pair in RESIDUAL_EDGES
                )
            ),
        ),
        multiply(corrected[(0, 1)], corrected[(2, 3)]),
    )
    assert equal(multiply(moment, top_deck), division_free_right)

    pairing_sum = add(
        multiply(normalized_pairs[(0, 1)], normalized_pairs[(2, 3)]),
        multiply(normalized_pairs[(0, 2)], normalized_pairs[(1, 3)]),
        multiply(normalized_pairs[(0, 3)], normalized_pairs[(1, 2)]),
    )
    assert equal(add(pairing_sum, scale(normalized_top, -1)), scale(four_linear, 2))
    print("generic four-residual even Wick tower and division-free top law: PASS")


def pentad(values: dict[tuple[int, int], int]) -> int:
    def k(left: int, right: int) -> int:
        return values[tuple(sorted((left, right)))]

    return (
        k(0, 1) * k(0, 2) * k(1, 3) * k(2, 4) * k(3, 4)
        - k(0, 1) * k(0, 2) * k(1, 4) * k(2, 3) * k(3, 4)
        - k(0, 1) * k(0, 3) * k(1, 2) * k(2, 4) * k(3, 4)
        + k(0, 1) * k(0, 3) * k(1, 4) * k(2, 3) * k(2, 4)
        + k(0, 1) * k(0, 4) * k(1, 2) * k(2, 3) * k(3, 4)
        - k(0, 1) * k(0, 4) * k(1, 3) * k(2, 3) * k(2, 4)
        + k(0, 2) * k(0, 3) * k(1, 2) * k(1, 4) * k(3, 4)
        - k(0, 2) * k(0, 3) * k(1, 3) * k(1, 4) * k(2, 4)
        - k(0, 2) * k(0, 4) * k(1, 2) * k(1, 3) * k(3, 4)
        + k(0, 2) * k(0, 4) * k(1, 3) * k(1, 4) * k(2, 3)
        - k(0, 3) * k(0, 4) * k(1, 2) * k(1, 4) * k(2, 3)
        + k(0, 3) * k(0, 4) * k(1, 2) * k(1, 3) * k(2, 4)
    )


def sharpness_control_check() -> None:
    cycle = {(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)}
    values = {
        pair: int(pair in cycle) for pair in combinations(range(5), 2)
    }
    assert pentad(values) == 1
    print("complementary-product/top laws alone miss a five-port pentad defect: PASS")


def main() -> None:
    generic_even_tower_check()
    sharpness_control_check()
    print("four-residual even Wick tower primary verification: PASS")


if __name__ == "__main__":
    main()
