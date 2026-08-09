#!/usr/bin/env python3
"""Exact replay of the root-of-unity block permanent selector.

The verifier checks three layers independently inside one characteristic-zero
calculation:

1. the published 4 x 4 two-block identity;
2. the cyclotomic product that removes mixed block choices; and
3. the square-zero coefficient formula for a range of block parameters.

No graph-support search or numerical root approximation is used.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import defaultdict

import sympy as sp


def permanent(matrix: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Expand a small permanent directly from its defining permutations."""

    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    return sp.expand(
        sum(
            math.prod(matrix[row][sigma[row]] for row in range(size))
            for sigma in itertools.permutations(range(size))
        )
    )


def multiply_square_zero(
    left: dict[int, int], right: dict[int, int]
) -> dict[int, int]:
    """Multiply polynomials in commuting variables z_i with z_i^2 = 0."""

    result: defaultdict[int, int] = defaultdict(int)
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            result[left_mask | right_mask] += left_coefficient * right_coefficient
    return {mask: coefficient for mask, coefficient in result.items() if coefficient}


def subset_power(indices: tuple[int, ...], exponent: int) -> dict[int, int]:
    """Return (sum_i z_i)^exponent in the square-zero algebra."""

    if exponent < 0 or exponent > len(indices):
        return {}
    coefficient = math.factorial(exponent)
    return {
        sum(1 << index for index in subset): coefficient
        for subset in itertools.combinations(indices, exponent)
    }


def add_polynomials(*terms: tuple[int, dict[int, int]]) -> dict[int, int]:
    result: defaultdict[int, int] = defaultdict(int)
    for scalar, polynomial in terms:
        for mask, coefficient in polynomial.items():
            result[mask] += scalar * coefficient
    return {mask: coefficient for mask, coefficient in result.items() if coefficient}


def block_selector_product(b: int, t: int, d: int) -> dict[int, int]:
    """Build the simplified root-filter product in the square-zero algebra."""

    assert b >= 1 and 1 <= d <= t
    blocks = tuple(tuple(range(h * t, (h + 1) * t)) for h in range(b))
    theta = (-1) ** (d + 1) * 2**d

    result = {0: 1}
    for block in blocks:
        result = multiply_square_zero(result, subset_power(block, t - d))

    for h in range(1, b):
        earlier = tuple(index for block in blocks[:h] for index in block)
        root_filter = add_polynomials(
            (1, subset_power(earlier, d)),
            (theta, subset_power(blocks[h], d)),
        )
        result = multiply_square_zero(result, root_filter)
    return result


def expected_lambda(block: int, b: int, d: int) -> int:
    """Coefficient of the term whose unsaturated block is ``block``."""

    theta = (-1) ** (d + 1) * 2**d
    if block == 0:
        return theta ** (b - 1)
    return theta ** (b - block - 1) * (1 + theta) ** (block - 1)


def check_square_zero_selector(b: int, t: int, d: int) -> dict[str, int]:
    product = block_selector_product(b, t, d)
    r = b * t
    blocks = tuple(set(range(h * t, (h + 1) * t)) for h in range(b))
    full_mask = (1 << r) - 1
    common_factor = math.factorial(t - d) * math.factorial(t) ** (b - 1)

    expected: dict[int, int] = {}
    for omitted in itertools.combinations(range(r), d):
        omitted_set = set(omitted)
        complement_mask = full_mask ^ sum(1 << index for index in omitted)
        containing_blocks = [
            block for block, indices in enumerate(blocks) if omitted_set <= indices
        ]
        coefficient = 0
        if containing_blocks:
            assert len(containing_blocks) == 1
            coefficient = expected_lambda(containing_blocks[0], b, d) * common_factor
        if coefficient:
            expected[complement_mask] = coefficient

    assert product == expected
    assert len(product) == b * math.comb(t, d)
    assert all(coefficient for coefficient in product.values())
    return {
        "blocks": b,
        "block_size": t,
        "selected_rows": d,
        "surviving_row_sets": len(product),
        "all_row_sets": math.comb(r, d),
    }


def check_cyclotomic_filters() -> list[int]:
    """Check the root-of-unity product modulo Phi_d for 1 <= d <= 7."""

    z, capital_y, y = sp.symbols("z Y y")
    checked = []
    coefficient_field = sp.QQ.frac_field(capital_y, y)
    for d in range(1, 8):
        theta = (-1) ** (d + 1) * 2**d
        product = sp.prod(capital_y + 2 * z**j * y for j in range(d))
        difference = sp.expand(product - (capital_y**d + theta * y**d))
        dividend = sp.Poly(difference, z, domain=coefficient_field)
        cyclotomic = sp.Poly(sp.cyclotomic_poly(d, z), z, domain=coefficient_field)
        assert dividend.rem(cyclotomic).is_zero
        checked.append(d)
    return checked


def check_micro_selector() -> int:
    u, v, w, z, p, q, r, s = sp.symbols("u v w z p q r s")
    matrix = (
        (u, v, sp.Integer(1), sp.Integer(1)),
        (w, z, sp.Integer(1), sp.Integer(1)),
        (p, q, sp.Integer(2), sp.Integer(-2)),
        (r, s, sp.Integer(2), sp.Integer(-2)),
    )
    selected = permanent(matrix)
    expected = -8 * (u * z + v * w) + 2 * (p * s + q * r)
    assert sp.expand(selected - expected) == 0

    polynomial = sp.Poly(selected, u, v, w, z, p, q, r, s)
    assert len(polynomial.terms()) == 4
    return len(polynomial.terms())


def main() -> None:
    micro_terms = check_micro_selector()
    cyclotomic_degrees = check_cyclotomic_filters()
    cases = [
        check_square_zero_selector(b, t, d)
        for b, t, d in (
            (1, 3, 1),
            (2, 2, 2),
            (2, 3, 2),
            (2, 3, 3),
            (3, 2, 2),
            (3, 4, 2),
            (3, 4, 3),
            (4, 3, 2),
        )
    ]

    print(
        json.dumps(
            {
                "status": "verified",
                "characteristic": 0,
                "micro_selector_terms": micro_terms,
                "cyclotomic_degrees": cyclotomic_degrees,
                "square_zero_cases": cases,
                "mixed_block_coefficients": 0,
                "theorem_scope": "bipartite permanent block selector",
                "global_krenn_gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
