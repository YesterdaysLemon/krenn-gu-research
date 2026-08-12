"""Primary exact checks for Cramer pair-pole differential flatness."""

from __future__ import annotations

from itertools import combinations_with_replacement

import sympy as sp


def first_stress(beta: sp.Expr, numerator: sp.Expr, variable: sp.Symbol) -> sp.Expr:
    """Return beta^2 times the first derivative of numerator / beta."""
    return sp.expand(
        beta * sp.diff(numerator, variable) - numerator * sp.diff(beta, variable)
    )


def second_stress(
    beta: sp.Expr,
    numerator: sp.Expr,
    left: sp.Symbol,
    right: sp.Symbol,
) -> sp.Expr:
    """Return beta^3 times one second derivative of numerator / beta."""
    beta_left = sp.diff(beta, left)
    beta_right = sp.diff(beta, right)
    numerator_left = sp.diff(numerator, left)
    numerator_right = sp.diff(numerator, right)
    return sp.expand(
        beta**2 * sp.diff(numerator, left, right)
        - beta
        * (
            numerator_left * beta_right
            + numerator_right * beta_left
            + numerator * sp.diff(beta, left, right)
        )
        + 2 * numerator * beta_left * beta_right
    )


def assert_universal_clearing_formulas() -> dict[str, int]:
    """Derive the beta^2 and beta^3 quotient-clearing powers exactly."""
    x, y = sp.symbols("x y")
    beta = sp.Function("beta")(x, y)
    numerator = sp.Function("v")(x, y)
    quotient = numerator / beta

    first = first_stress(beta, numerator, x)
    assert sp.simplify(beta**2 * sp.diff(quotient, x) - first) == 0

    second = second_stress(beta, numerator, x, y)
    assert sp.simplify(beta**3 * sp.diff(quotient, x, y) - second) == 0
    return {"first_denominator_power": 2, "second_denominator_power": 3}


def bilinear_form(
    left: tuple[sp.Symbol, ...],
    right: tuple[sp.Symbol, ...],
    matrix: tuple[tuple[int, ...], ...],
) -> sp.Expr:
    """Build a labelled constant bilinear form."""
    return sp.expand(
        sum(
            matrix[row][column] * left[row] * right[column]
            for row in range(len(left))
            for column in range(len(right))
        )
    )


def assert_physical_pair_family() -> dict[str, int]:
    """Check every ternary stress and reconstruct one nontrivial block."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    s = sp.symbols("s0:3")
    matrix = (
        (2, -1, 3),
        (0, 4, -2),
        (5, 1, 1),
    )
    block = bilinear_form(x, y, matrix)
    # A common multigroup monomial keeps the exact quotient-rule coverage
    # while avoiding irrelevant expansion of hundreds of common-factor terms.
    beta = x[0] * y[0] * r[0] * s[0]
    numerator = sp.expand(beta * block)

    transverse_count = 0
    for variable in (*r, *s):
        assert first_stress(beta, numerator, variable) == 0
        transverse_count += 1

    endpoint_hessian_count = 0
    for endpoint in (x, y):
        for left_index, right_index in combinations_with_replacement(range(3), 2):
            assert (
                second_stress(
                    beta,
                    numerator,
                    endpoint[left_index],
                    endpoint[right_index],
                )
                == 0
            )
            endpoint_hessian_count += 1

    reconstructed_count = 0
    for left_index in range(3):
        for right_index in range(3):
            cleared_mixed = second_stress(
                beta,
                numerator,
                x[left_index],
                y[right_index],
            )
            expected = sp.expand(beta**3 * matrix[left_index][right_index])
            assert sp.expand(cleared_mixed - expected) == 0
            reconstructed_count += 1

    assert transverse_count == 3 * (4 - 2)
    assert endpoint_hessian_count == 12
    assert reconstructed_count == 9
    return {
        "transverse_stresses": transverse_count,
        "endpoint_hessians": endpoint_hessian_count,
        "reconstructed_entries": reconstructed_count,
        "total_pair_gate": transverse_count + endpoint_hessian_count,
    }


def assert_chart_rescaling() -> dict[str, sp.Expr]:
    """Check that common Cramer rescaling preserves every vanishing test."""
    x0, x1, y0, y1, r0, r1 = sp.symbols("x0 x1 y0 y1 r0 r1")
    beta = (x0 + 2 * x1) * (r0 - r1)
    numerator = sp.expand(beta * (3 * x0 * y0 - 2 * x1 * y1))
    scale = y0 + y1 + r0
    scaled_beta = sp.expand(scale * beta)
    scaled_numerator = sp.expand(scale * numerator)

    first = first_stress(beta, numerator, r0)
    scaled_first = first_stress(scaled_beta, scaled_numerator, r0)
    assert sp.expand(scaled_first - scale**2 * first) == 0

    hessian = second_stress(beta, numerator, x0, x1)
    scaled_hessian = second_stress(scaled_beta, scaled_numerator, x0, x1)
    assert sp.expand(scaled_hessian - scale**3 * hessian) == 0
    assert first == 0
    assert hessian == 0
    return {"first_scale": scale**2, "hessian_scale": scale**3}


def homogeneous_group_degree(
    expression: sp.Expr,
    group: tuple[sp.Symbol, ...],
) -> int:
    """Return the common total degree in one variable group."""
    degrees = {
        sum(monomial) for monomial, _coefficient in sp.Poly(expression, *group).terms()
    }
    assert len(degrees) == 1
    return degrees.pop()


def assert_sharp_omissions() -> dict[str, object]:
    """Check ambient exact poles defeating either jet layer alone."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")

    transverse_beta = r[1]
    transverse_numerator = r[0] * x[0] * y[0]
    outside = first_stress(transverse_beta, transverse_numerator, r[0])
    assert outside == r[1] * x[0] * y[0]

    transverse_endpoint_hessians = 0
    for endpoint_variables in (x, y):
        for left_index, right_index in combinations_with_replacement(range(3), 2):
            assert (
                second_stress(
                    transverse_beta,
                    transverse_numerator,
                    endpoint_variables[left_index],
                    endpoint_variables[right_index],
                )
                == 0
            )
            transverse_endpoint_hessians += 1
    assert transverse_endpoint_hessians == 12
    transverse_quotient = sp.cancel(transverse_numerator / transverse_beta)
    assert sp.denom(transverse_quotient) == r[1]
    transverse_multidegree = tuple(
        homogeneous_group_degree(transverse_numerator, group)
        - homogeneous_group_degree(transverse_beta, group)
        for group in (x, y, r)
    )
    assert transverse_multidegree == (1, 1, 0)

    endpoint_beta = x[1]
    endpoint_numerator = x[0] ** 2 * y[0]
    endpoint_transverse_stresses = 0
    for variable in r:
        assert first_stress(endpoint_beta, endpoint_numerator, variable) == 0
        endpoint_transverse_stresses += 1
    assert endpoint_transverse_stresses == 3
    endpoint = second_stress(endpoint_beta, endpoint_numerator, x[0], x[0])
    assert endpoint == 2 * x[1] ** 2 * y[0]
    endpoint_quotient = sp.cancel(endpoint_numerator / endpoint_beta)
    assert sp.denom(endpoint_quotient) == x[1]
    endpoint_multidegree = tuple(
        homogeneous_group_degree(endpoint_numerator, group)
        - homogeneous_group_degree(endpoint_beta, group)
        for group in (x, y, r)
    )
    assert endpoint_multidegree == (1, 1, 0)

    return {
        "outside_stress": outside,
        "transverse_endpoint_hessians": transverse_endpoint_hessians,
        "transverse_multidegree": transverse_multidegree,
        "endpoint_transverse_stresses": endpoint_transverse_stresses,
        "endpoint_hessian": endpoint,
        "endpoint_multidegree": endpoint_multidegree,
    }


def assert_condition_count() -> dict[int, int]:
    """Check the ternary 3m+6 count on representative orders."""
    counts = {m: 3 * (m - 2) + 2 * (3 * 4 // 2) for m in range(2, 10)}
    assert counts == {m: 3 * m + 6 for m in range(2, 10)}
    return counts


def main() -> None:
    clearing = assert_universal_clearing_formulas()
    physical = assert_physical_pair_family()
    scaling = assert_chart_rescaling()
    sharpness = assert_sharp_omissions()
    counts = assert_condition_count()
    print("balanced Cramer pair-pole differential-flatness checks: PASS")
    print(f"  quotient clearing: {clearing}")
    print(f"  physical pair family: {physical}")
    print(f"  chart rescaling: {scaling}")
    print(f"  sharp omissions: {sharpness}")
    print(f"  ternary pair-gate counts: {counts}")


if __name__ == "__main__":
    main()
