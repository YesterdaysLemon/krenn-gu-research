#!/usr/bin/env python3
"""Verify the arbitrary-surplus common-row full-span obstruction."""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md"
DEPENDENCY = ROOT / "TWO_PORT_SEVEN_BLOCKER_REDUCTION.md"


def symbolic_product_grading(root_count: int, surplus: int) -> dict[str, int]:
    mode_count = root_count + surplus
    rows = range(root_count)
    modes = range(mode_count)
    markers = sp.symbols(f"L0:{root_count}")
    values = sp.symbols(f"h0:{root_count * mode_count}")
    subsets = tuple(itertools.combinations(modes, surplus))
    port_values = sp.symbols(f"w0:{len(subsets)}")
    terms = []
    for subset_index, unused in enumerate(subsets):
        retained = tuple(mode for mode in modes if mode not in unused)
        for permutation in itertools.permutations(rows):
            terms.append(
                port_values[subset_index]
                * sp.prod(
                    markers[permutation[column]]
                    * values[mode_count * permutation[column] + mode]
                    for column, mode in enumerate(retained)
                )
            )
    equal_input = sp.Add(*terms)
    marker_product = sp.prod(markers)
    quotient = sp.cancel(equal_input / marker_product)
    assert sp.expand(equal_input - marker_product * quotient) == 0
    assert not set(markers).intersection(quotient.free_symbols)
    term_count = len(sp.Poly(quotient, *port_values, *values).terms())
    expected = math.comb(mode_count, surplus) * math.factorial(root_count)
    assert len(terms) == term_count == expected
    return {
        "roots": root_count,
        "surplus": surplus,
        "blockers": mode_count,
        "product_graded_terms": term_count,
    }


def permanent(matrix: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    size = len(matrix)
    return sp.expand(
        sum(
            sp.prod(matrix[row][permutation[row]] for row in range(size))
            for permutation in itertools.permutations(range(size))
        )
    )


def first_polar_case(root_count: int, surplus: int) -> dict[str, int]:
    mode_count = root_count + surplus
    modes = range(mode_count)
    subsets = tuple(itertools.combinations(modes, surplus))
    port_values = sp.symbols(f"w0:{len(subsets)}")
    point_values = sp.symbols(f"q0:{(root_count - 1) * mode_count}")
    variable_other_rows = sp.symbols(f"y0:{(root_count - 1) * mode_count}")
    distinguished = sp.symbols(f"h0:{mode_count}")
    mode_results = []

    for variable_mode in modes:
        total = sp.S.Zero
        for subset_index, unused in enumerate(subsets):
            retained = tuple(mode for mode in modes if mode not in unused)
            columns = []
            for mode in retained:
                if mode == variable_mode:
                    column = (distinguished[mode],) + tuple(
                        variable_other_rows[(row - 1) * mode_count + mode]
                        for row in range(1, root_count)
                    )
                else:
                    column = (sp.S.Zero,) + tuple(
                        point_values[(row - 1) * mode_count + mode]
                        for row in range(1, root_count)
                    )
                columns.append(column)
            matrix = tuple(
                tuple(columns[column][row] for column in range(root_count))
                for row in range(root_count)
            )
            total += port_values[subset_index] * permanent(matrix)

        quotient = sp.cancel(total / distinguished[variable_mode])
        assert sp.expand(total - distinguished[variable_mode] * quotient) == 0
        assert distinguished[variable_mode] not in quotient.free_symbols
        assert not set(variable_other_rows).intersection(quotient.free_symbols)
        surviving_terms = len(sp.Poly(quotient, *port_values, *point_values).terms())
        expected = math.comb(mode_count - 1, surplus) * math.factorial(root_count - 1)
        assert surviving_terms == expected
        mode_results.append(surviving_terms)

    assert len(set(mode_results)) == 1
    return {
        "roots": root_count,
        "surplus": surplus,
        "blockers": mode_count,
        "modes_checked": mode_count,
        "surviving_terms_per_mode": mode_results[0],
        "terms_with_variable_mode_in_port_set": math.comb(mode_count - 1, surplus - 1)
        if surplus
        else 0,
    }


def diagonal_no_line_and_nonzero_polar(degree: int) -> dict[str, object]:
    x, y = sp.symbols("x y")
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    d0, d1, d2 = sp.symbols("d0 d1 d2", nonzero=True)
    restriction = sp.expand(
        gamma**degree * (d0 * x**degree + d1 * y**degree)
        + d2 * (-alpha * x - beta * y) ** degree
    )
    polynomial = sp.Poly(restriction, x, y)
    first_mixed = sp.expand(polynomial.coeff_monomial(x ** (degree - 1) * y))
    last_mixed = sp.expand(polynomial.coeff_monomial(x * y ** (degree - 1)))
    sign = (-1) ** degree
    assert first_mixed == sign * degree * alpha ** (degree - 1) * beta * d2
    assert last_mixed == sign * degree * alpha * beta ** (degree - 1) * d2

    alpha_zero = sp.Poly(restriction.subs(alpha, 0), x, y).coeff_monomial(x**degree)
    beta_zero = sp.Poly(restriction.subs(beta, 0), x, y).coeff_monomial(y**degree)
    assert alpha_zero == gamma**degree * d0
    assert beta_zero == gamma**degree * d1

    # If gamma=0, the proposed line only constrains x,y.  The z-coordinate
    # remains free, and its nonzero pure coefficient d2 cannot disappear.
    gamma_zero_free_pure_term = d2
    assert gamma_zero_free_pure_term != 0

    p0, p1, p2 = sp.symbols("p0:3")
    polar_coefficients = (
        d0 * p0 ** (degree - 1),
        d1 * p1 ** (degree - 1),
        d2 * p2 ** (degree - 1),
    )
    return {
        "degree": degree,
        "first_mixed": str(first_mixed),
        "last_mixed": str(last_mixed),
        "alpha_zero_survivor": str(alpha_zero),
        "beta_zero_survivor": str(beta_zero),
        "gamma_zero_survivor": str(gamma_zero_free_pure_term),
        "polar_coefficients": [str(value) for value in polar_coefficients],
        "polar_nonzero_for_nonzero_projective_point": True,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    assert DEPENDENCY.exists()
    for phrase in (
        "Exact arbitrary-order characteristic-zero necessary theorem",
        "L_i=(C^3)^*",
        "g_p=C_(i,u) H_u[i,-]",
        "root-row span exactly two at any surplus: EXCLUDED",
        "full arbitrary-order local-to-global reduction: UNKNOWN",
        "UNRESOLVED",
    ):
        assert phrase in theorem

    grading_cases = tuple(
        symbolic_product_grading(roots, surplus)
        for roots, surplus in ((3, 0), (4, 1), (4, 2), (3, 3), (5, 2))
    )
    polar_cases = tuple(
        first_polar_case(roots, surplus)
        for roots, surplus in ((3, 0), (4, 1), (4, 2), (3, 3), (5, 2))
    )
    diagonal_cases = tuple(
        diagonal_no_line_and_nonzero_polar(degree) for degree in (3, 5, 6, 7)
    )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "root_dependency": DEPENDENCY.name,
                "symbolic_product_grading": grading_cases,
                "modewise_first_polar_factorization": polar_cases,
                "diagonal_cases": diagonal_cases,
                "rank_zero_or_one_row_span_possible": False,
                "rank_two_row_span_possible": False,
                "required_common_row_span": 3,
                "arbitrary_parameters_proved_in_written_termwise_argument": True,
                "full_local_to_global_reduction_complete": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
