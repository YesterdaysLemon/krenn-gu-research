"""Hybrid torus parameterization for deficient prism core orbits."""

from __future__ import annotations

from collections import Counter

from prism_orbit_screen import Polynomial, clean_polynomial


def partial_parameter_names(rank_one_blocks: set[int]) -> list[str]:
    names: list[str] = []
    for block in range(6):
        if block in rank_one_blocks:
            names.extend(f"u{3 * block + row}" for row in range(3))
            names.extend(f"v{3 * block + column}" for column in range(3))
        else:
            names.extend(f"x{9 * block + entry}" for entry in range(9))
    return names


def partially_parameterize_polynomial(
    polynomial: Polynomial, rank_one_blocks: set[int]
) -> Polynomial:
    result: Polynomial = Counter()
    for monomial, coefficient in polynomial.items():
        factors: list[str] = []
        for variable in monomial:
            entry_index = int(variable[1:])
            block = entry_index // 9
            within_block = entry_index % 9
            if block not in rank_one_blocks:
                factors.append(variable)
                continue
            row = within_block // 3
            column = within_block % 3
            factors.extend((f"u{3 * block + row}", f"v{3 * block + column}"))
        result[tuple(sorted(factors))] += coefficient
    return clean_polynomial(result)
