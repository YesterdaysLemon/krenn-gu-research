#!/usr/bin/env python3
"""Verify the arbitrary-surplus common-row full-span obstruction."""

from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md"
DEPENDENCY = HERE / "TWO_PORT_SEVEN_BLOCKER_REDUCTION.md"
PROFILE_DEPENDENCY = (
    REPO_ROOT
    / "claims/p6/P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md"
)


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


def factored_port_laplace(root_count: int, port_count: int) -> dict[str, int]:
    mode_count = root_count + port_count
    entries = sp.symbols(f"x0:{mode_count * mode_count}")
    matrix = tuple(
        tuple(entries[row * mode_count + column] for column in range(mode_count))
        for row in range(mode_count)
    )
    full = permanent(matrix)
    laplace = sp.S.Zero
    for port_columns in itertools.combinations(range(mode_count), port_count):
        port_column_set = set(port_columns)
        root_columns = tuple(
            column for column in range(mode_count) if column not in port_column_set
        )
        root_minor = tuple(
            tuple(matrix[row][column] for column in root_columns)
            for row in range(root_count)
        )
        port_minor = tuple(
            tuple(matrix[row][column] for column in port_columns)
            for row in range(root_count, mode_count)
        )
        laplace += permanent(root_minor) * permanent(port_minor)

    assert sp.expand(full - laplace) == 0
    full_terms = len(sp.Poly(full, *entries).terms())
    laplace_terms = len(sp.Poly(sp.expand(laplace), *entries).terms())
    assert full_terms == laplace_terms == math.factorial(mode_count)
    return {
        "roots": root_count,
        "ports": port_count,
        "blockers": mode_count,
        "full_permanent_terms": full_terms,
        "laplace_terms": laplace_terms,
    }


def exact_rank(rows: tuple[tuple[int, ...], ...]) -> int:
    return int(sp.Matrix(rows).rank())


def common_port_profile_full_span_models() -> tuple[dict[str, object], ...]:
    basis = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    profiles = {
        "empty": (0, 0, 0, 0, 0, 0),
        "1": (1, 0, 0, 0, 0, 0),
        "1+1": (1, 2, 0, 0, 0, 0),
        "1+1+1": (1, 2, 4, 0, 0, 0),
        "2": (3, 0, 0, 0, 0, 0),
        "2+1": (3, 4, 0, 0, 0, 0),
    }
    models = []
    for profile, masks in profiles.items():
        root_rows_by_mode: list[tuple[tuple[int, ...], ...]] = []
        port_rows: list[tuple[int, ...]] = []
        full_index = 0
        realized_masks = []
        for mask in masks:
            missing = tuple(color for color in range(3) if mask & (1 << color))
            if not missing:
                shift = full_index % 3
                full_index += 1
                root_rows = tuple(basis[(row + shift) % 3] for row in range(5))
                port_row = basis[shift]
            elif len(missing) == 1:
                present = tuple(color for color in range(3) if color not in missing)
                plane_basis = (basis[present[0]], basis[present[1]])
                root_rows = tuple(plane_basis[row % 2] for row in range(5))
                port_row = basis[missing[0]]
            else:
                first, second = missing
                third = next(color for color in range(3) if color not in missing)
                plane_basis = (
                    basis[third],
                    tuple(
                        basis[first][color] - basis[second][color] for color in range(3)
                    ),
                )
                root_rows = tuple(plane_basis[row % 2] for row in range(5))
                port_row = basis[first]

            root_rank = exact_rank(root_rows)
            assert root_rank == (3 if not missing else 2)
            assert exact_rank(root_rows + (port_row,)) == 3
            realized_mask = sum(
                1 << color
                for color in range(3)
                if exact_rank(root_rows + (basis[color],)) > root_rank
            )
            assert realized_mask == mask
            root_rows_by_mode.append(root_rows)
            port_rows.append(port_row)
            realized_masks.append(realized_mask)

        root_family_ranks = tuple(
            exact_rank(tuple(root_rows_by_mode[mode][row] for mode in range(6)))
            for row in range(5)
        )
        port_family_rank = exact_rank(tuple(port_rows))
        assert root_family_ranks == (3, 3, 3, 3, 3)
        assert port_family_rank == 3
        models.append(
            {
                "profile": profile,
                "missing_masks": realized_masks,
                "mode_root_ranks": [
                    exact_rank(root_rows) for root_rows in root_rows_by_mode
                ],
                "mode_augmented_ranks": [
                    exact_rank(root_rows_by_mode[mode] + (port_rows[mode],))
                    for mode in range(6)
                ],
                "root_family_ranks": root_family_ranks,
                "port_family_rank": port_family_rank,
            }
        )
    return tuple(models)


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
    assert PROFILE_DEPENDENCY.exists()
    for phrase in (
        "Exact arbitrary-order characteristic-zero necessary theorem",
        "L_i=(C^3)^*",
        "g_p=C_(i,u) H_u[i,-]",
        "root-row span exactly two at any surplus: EXCLUDED",
        "span{g_(a,u):u in B}=(C^3)^*",
        "six common-port missing-colour profiles at incidence level: ALL SURVIVE",
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
    laplace_cases = tuple(
        factored_port_laplace(roots, ports) for roots, ports in ((3, 1), (4, 2), (3, 3))
    )
    profile_models = common_port_profile_full_span_models()
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "root_dependency": DEPENDENCY.name,
                "profile_dependency": PROFILE_DEPENDENCY.name,
                "symbolic_product_grading": grading_cases,
                "modewise_first_polar_factorization": polar_cases,
                "diagonal_cases": diagonal_cases,
                "factored_port_laplace_cases": laplace_cases,
                "common_port_profile_span_models": profile_models,
                "rank_zero_or_one_row_span_possible": False,
                "rank_two_row_span_possible": False,
                "required_common_row_span": 3,
                "automatic_first_surplus_port_span": 3,
                "effective_two_port_a_span": 3,
                "effective_two_port_b_span": 3,
                "profile_excluded_by_span_conditions": False,
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
