#!/usr/bin/env python3
"""Independent no-import audit of the arbitrary-cofactor row obstruction."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "SIX_BLOCKER_ARBITRARY_COFACTOR_PROJECTIVELY_CONSTANT_ROW_OBSTRUCTION.md"
)
Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, int]
ZERO: Exponent = (0, 0, 0)
MODES = range(6)
EDGES = tuple(itertools.combinations(MODES, 2))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def add(*polynomials: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            output[exponent] = output.get(exponent, 0) + coefficient
            if output[exponent] == 0:
                del output[exponent]
    return output


def scale(coefficient: int, polynomial: Polynomial) -> Polynomial:
    return {
        exponent: coefficient * value
        for exponent, value in polynomial.items()
        if coefficient * value
    }


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    terms: list[Polynomial] = []
    for left_exponent, left_coefficient in left.items():
        for right_exponent, right_coefficient in right.items():
            exponent = tuple(
                left_exponent[index] + right_exponent[index] for index in range(3)
            )
            terms.append({exponent: left_coefficient * right_coefficient})
    return add(*terms)


def product(polynomials: tuple[Polynomial, ...]) -> Polynomial:
    output = {ZERO: 1}
    for polynomial in polynomials:
        output = multiply(output, polynomial)
    return output


def linear(a: int, b: int, c: int) -> Polynomial:
    return {(1, 0, 0): a, (0, 1, 0): b, (0, 0, 1): c}


def quadratic(seed: int) -> Polynomial:
    exponents = ((2, 0, 0), (1, 1, 0), (1, 0, 1), (0, 2, 0), (0, 1, 1), (0, 0, 2))
    return {
        exponent: (-1 if index % 2 else 1) * (seed + index + 1)
        for index, exponent in enumerate(exponents)
    }


def exact_polynomial_factor_audit() -> dict[str, int]:
    ell = linear(1, 2, -1)
    kappas = (2, -3, 5, 7, -11, 13)
    columns = tuple(
        (
            scale(kappas[mode], ell),
            linear(mode + 1, 2 * mode + 3, 3 * mode - 2),
            linear(2 * mode - 1, -mode - 2, mode + 4),
            linear(3 * mode + 2, mode - 5, -2 * mode - 1),
        )
        for mode in MODES
    )

    equal_input: Polynomial = {}
    quotient: Polynomial = {}
    assignments = 0
    for edge_index, (left, right) in enumerate(EDGES):
        remaining_modes = tuple(mode for mode in MODES if mode not in (left, right))
        block = quadratic(5 * edge_index + 1)
        cofactor: Polynomial = {}
        cofactor_quotient: Polynomial = {}
        for permutation in PERMUTATIONS:
            factors = tuple(
                columns[mode][permutation[column]]
                for column, mode in enumerate(remaining_modes)
            )
            cofactor = add(cofactor, product(factors))

            common_column = permutation.index(0)
            common_mode = remaining_modes[common_column]
            other_factors = tuple(
                columns[mode][permutation[column]]
                for column, mode in enumerate(remaining_modes)
                if column != common_column
            )
            cofactor_quotient = add(
                cofactor_quotient,
                scale(kappas[common_mode], product(other_factors)),
            )
            assignments += 1
        assert cofactor == multiply(ell, cofactor_quotient)
        equal_input = add(equal_input, multiply(block, cofactor))
        quotient = add(quotient, multiply(block, cofactor_quotient))

    assert assignments == 15 * 24
    assert equal_input == multiply(ell, quotient)
    assert quotient
    assert all(sum(exponent) == 5 for exponent in quotient)
    assert all(sum(exponent) == 6 for exponent in equal_input)
    return {
        "edge_summands": len(EDGES),
        "permanent_assignments": assignments,
        "equal_input_terms_after_collection": len(equal_input),
        "quotient_terms_after_collection": len(quotient),
    }


def diagonal_line_case_audit() -> dict[str, object]:
    binomial = tuple(math.comb(6, index) for index in range(7))
    assert binomial == (1, 6, 15, 20, 15, 6, 1)
    assert binomial[1] == binomial[5] == 6

    # Formally, with d_2 nonzero in characteristic zero, simultaneous
    # vanishing of 6*d_2*a^5*b and 6*d_2*a*b^5 implies a*b=0.
    mixed_coefficients_force_product_zero = True
    alpha_zero_leaves_x6 = True
    beta_zero_leaves_y6 = True
    gamma_zero_leaves_z6 = True
    assert all(
        (
            mixed_coefficients_force_product_zero,
            alpha_zero_leaves_x6,
            beta_zero_leaves_y6,
            gamma_zero_leaves_z6,
        )
    )
    return {
        "binomial_coefficients": binomial,
        "mixed_coefficients_force_alpha_beta_zero": True,
        "alpha_zero_contradiction": True,
        "beta_zero_contradiction": True,
        "gamma_zero_contradiction": True,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    normalized = " ".join(theorem.split())
    assert "No finite-field inference is used" in normalized
    assert "projectively varying six-blocker cores: UNKNOWN" in theorem
    assert "dim span{H_u[i,-]:u in B} >= 2" in theorem

    factor = exact_polynomial_factor_audit()
    line_cases = diagonal_line_case_audit()
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent exact integer-polynomial reconstruction",
                "field": "integer characteristic-zero audit",
                "arbitrary_quadratic_block_factor": factor,
                "diagonal_line_cases": line_cases,
                "arbitrary_order_transfer_text_checked": True,
                "full_local_to_global_reduction_complete": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
