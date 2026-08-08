#!/usr/bin/env python3
"""Independent support/module audit of component 18's H22 obstruction."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from typing import TypeAlias

PERMUTATIONS = tuple(itertools.permutations(range(4)))
WORDS = tuple(itertools.product((0, 1), repeat=4))
Monomial: TypeAlias = tuple[str, ...]
Polynomial: TypeAlias = dict[Monomial, int]


def direct_permanent(rows):
    return sum(
        scalar_product(rows[row][permutation[row]] for row in range(4))
        for permutation in PERMUTATIONS
    )


def scalar_product(entries):
    result = 1
    for entry in entries:
        result *= entry
    return result


def variable(name: str) -> Polynomial:
    return {(name,): 1}


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    if not left or not right:
        return {}
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, 0)
                + left_coefficient * right_coefficient
            )
    return {monomial: value for monomial, value in result.items() if value}


def polynomial_product(entries) -> Polynomial:
    result: Polynomial = {(): 1}
    for entry in entries:
        result = polynomial_multiply(result, entry)
    return result


def subset_permanent(
    rows: tuple[tuple[Polynomial, ...], ...],
) -> Polynomial:
    """Compute the permanent in a tiny exact sparse polynomial ring."""

    table: dict[int, Polynomial] = {0: {(): 1}}
    for row in rows:
        nxt: dict[int, Polynomial] = {}
        for mask, coefficient in table.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) == 0:
                    target = mask | (1 << column)
                    nxt[target] = polynomial_add(
                        nxt.get(target, {}),
                        polynomial_multiply(coefficient, entry),
                    )
        table = nxt
    return table.get(15, {})


def sample_marking_audit() -> None:
    e = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    ell = (Fraction(0), Fraction(1), Fraction(-3), Fraction(-2))
    v1 = (Fraction(0), Fraction(1), Fraction(-1), Fraction(-1))
    v2 = (Fraction(0), Fraction(1), Fraction(-1), Fraction(2))
    v3 = (Fraction(0), Fraction(1), Fraction(3), Fraction(-1))
    alpha = (ell, e, e, e)
    beta = (e, v1, v2, v3)
    tensor = {
        word: direct_permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert {word: value for word, value in tensor.items() if value} == {
        (1, 1, 1, 1): Fraction(4)
    }


def hall_audit(
    label: str,
    common_entries: tuple[Polynomial, ...],
) -> dict[str, object]:
    a0, a1, a2, a3 = tuple(
        variable(f"{label}_a{index}") for index in range(4)
    )
    x1, x2, x3 = tuple(
        variable(f"{label}_x{index}") for index in range(1, 4)
    )
    zero: Polynomial = {}
    rows = (
        (a0, a1, a2, a3),
        (common_entries[0], zero, zero, x1),
        (common_entries[1], zero, zero, x2),
        (common_entries[2], zero, zero, x3),
    )

    row_neighbourhoods = tuple(
        frozenset(index for index, entry in enumerate(row) if entry)
        for row in rows[1:]
    )
    union = frozenset().union(*row_neighbourhoods)
    assert row_neighbourhoods == (
        frozenset((0, 3)),
        frozenset((0, 3)),
        frozenset((0, 3)),
    )
    assert len(union) == 2
    assert len(union) < len(row_neighbourhoods)

    zero_summands = 0
    for permutation in PERMUTATIONS:
        summand = polynomial_product(
            rows[row][permutation[row]] for row in range(4)
        )
        assert not summand
        zero_summands += 1
    assert not subset_permanent(rows)
    return {
        "direction": label,
        "hall_rows": [1, 2, 3],
        "hall_neighborhood": sorted(union),
        "hall_defect": 1,
        "zero_permanent_summands": zero_summands,
        "subset_dp_permanent": "0",
    }


def main() -> None:
    sample_marking_audit()

    s0 = variable("s0")
    lam = variable("lambda")
    row_scales = tuple(variable(f"c{index}") for index in range(1, 4))
    d01_entries = tuple(
        polynomial_product((row_scale, lam, s0))
        for row_scale in row_scales
    )
    d23_entries = tuple(
        polynomial_product((row_scale, s0))
        for row_scale in row_scales
    )
    certificates = (
        hall_audit("D01", d01_entries),
        hall_audit("D23", d23_entries),
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": (
                    "independent rational sample plus abstract Hall-support "
                    "and dependency-free sparse-polynomial subset-DP identity"
                ),
                "sample_only_nonzero_pure_coefficient": "T_1111=4",
                "independent_kernel_row_rescalings": True,
                "arbitrary_mode_zero_row": True,
                "certificates": certificates,
                "both_weighted_all_kernel_diagonals_zero": True,
                "generic_weighted_H22_fibre_empty": True,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
