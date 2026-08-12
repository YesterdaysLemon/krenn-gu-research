"""Primary exact checks for the projective-minimal Cramer pair-jet gate."""

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


def homogeneous_group_degree(
    expression: sp.Expr,
    group: tuple[sp.Symbol, ...],
) -> int:
    """Return the common degree in one variable group."""
    degrees = {
        sum(monomial) for monomial, _coefficient in sp.Poly(expression, *group).terms()
    }
    assert len(degrees) == 1
    return degrees.pop()


def assert_euler_syzygies() -> dict[str, int]:
    """Check the outside and differentiated endpoint Euler identities."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    beta = sp.expand(
        (x[0] + 2 * x[1] - x[2])
        * (y[0] - y[1] + 3 * y[2])
        * (r[0] + r[2])
    )
    numerator = sp.expand(
        (x[0] ** 2 + x[1] * x[2] + x[2] ** 2)
        * (y[0] * y[1] + y[1] ** 2 + y[2] ** 2)
        * r[1]
    )
    multidegree = tuple(
        homogeneous_group_degree(numerator, group)
        - homogeneous_group_degree(beta, group)
        for group in (x, y, r)
    )
    assert multidegree == (1, 1, 0)

    outside = tuple(first_stress(beta, numerator, variable) for variable in r)
    assert any(stress != 0 for stress in outside)
    assert sp.expand(sum(variable * stress for variable, stress in zip(r, outside))) == 0

    endpoint_equations = 0
    for endpoint in (x, y):
        hessian = tuple(
            tuple(
                second_stress(beta, numerator, left, right)
                for right in endpoint
            )
            for left in endpoint
        )
        assert any(entry != 0 for row in hessian for entry in row)
        assert all(hessian[a][b] == hessian[b][a] for a in range(3) for b in range(3))
        for column in range(3):
            radial = sum(
                endpoint[row] * hessian[row][column] for row in range(3)
            )
            assert sp.expand(radial) == 0
            endpoint_equations += 1

    return {
        "outside_euler_syzygies": 1,
        "endpoint_euler_syzygies": endpoint_equations,
        "nonzero_outside_stresses": sum(stress != 0 for stress in outside),
    }


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


def assert_reduced_gate_on_physical_family() -> dict[str, int]:
    """Check all reduced and recovered full stresses on a physical family."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    s = sp.symbols("s0:3")
    matrix = ((2, -1, 3), (4, 0, -2), (5, 1, 1))
    block = bilinear_form(x, y, matrix)
    beta = sp.expand(
        (x[0] + x[1] + x[2])
        * (y[0] - 2 * y[1] + y[2])
        * (r[0] + r[1])
        * (s[0] - s[2])
    )
    numerator = sp.expand(beta * block)

    retained = 0
    recovered = 0
    for outside in (r, s):
        stresses = tuple(
            first_stress(beta, numerator, variable) for variable in outside
        )
        for index in (1, 2):
            assert stresses[index] == 0
            retained += 1
        assert sp.expand(sum(outside[index] * stresses[index] for index in range(3))) == 0
        assert stresses[0] == 0
        recovered += 1

    for endpoint in (x, y):
        hessian = tuple(
            tuple(
                second_stress(beta, numerator, endpoint[row], endpoint[column])
                for column in range(3)
            )
            for row in range(3)
        )
        for row, column in combinations_with_replacement((1, 2), 2):
            assert hessian[row][column] == 0
            retained += 1
        for column in (1, 2):
            assert sp.expand(
                sum(endpoint[row] * hessian[row][column] for row in range(3))
            ) == 0
            assert hessian[0][column] == 0
            recovered += 1
        assert sp.expand(
            sum(endpoint[row] * hessian[row][0] for row in range(3))
        ) == 0
        assert hessian[0][0] == 0
        recovered += 1

    assert retained == 2 * (4 - 2) + 2 * 3
    assert recovered == 2 + 2 * 3
    return {"retained": retained, "recovered_radial": recovered}


def replacement_minor(
    matrix: sp.Matrix,
    column: int,
    replacement: sp.Matrix,
) -> sp.Expr:
    """Return one selected-column replacement determinant."""
    replaced = matrix.copy()
    replaced[:, column] = replacement
    return sp.expand(replaced.det())


def assert_reduced_replacement_minors() -> dict[str, int]:
    """Compose every retained ternary stress with the raw Cramer formula."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    beta = sp.expand(r[0] * (x[0] + x[2]))
    numerator = sp.expand(r[1] * (x[1] ** 2 + x[2] ** 2) * y[0])
    matrix = sp.diag(beta, 1)
    target = sp.Matrix([numerator, 0])
    cramer_numerator = matrix.adjugate() * target
    assert cramer_numerator == sp.Matrix([numerator, 0])
    assert sp.expand(matrix.det() - beta) == 0

    first_count = 0
    first_determinants: list[sp.Expr] = []
    for variable in r:
        residual = sp.expand(beta) * target.diff(variable) - matrix.diff(
            variable
        ) * cramer_numerator
        expected_vector = sp.Matrix(
            [
                first_stress(beta, cramer_numerator[row], variable)
                for row in range(2)
            ]
        )
        assert sp.simplify(
            matrix.adjugate() * residual - expected_vector
        ) == sp.zeros(2, 1)
        determinant = replacement_minor(matrix, 0, residual)
        assert sp.expand(
            determinant - first_stress(beta, numerator, variable)
        ) == 0
        first_determinants.append(determinant)
        if variable in r[1:]:
            first_count += 1
    assert sp.expand(
        sum(variable * determinant for variable, determinant in zip(r, first_determinants))
    ) == 0

    second_count = 0
    for endpoint in (x, y):
        determinant_hessian: list[list[sp.Expr]] = []
        for left_index, left in enumerate(endpoint):
            determinant_row: list[sp.Expr] = []
            for right_index, right in enumerate(endpoint):
                second_residual = (
                    beta**2 * target.diff(left, right)
                    - beta * matrix.diff(left, right) * cramer_numerator
                    - matrix.diff(left) * sp.Matrix(
                        [
                            first_stress(beta, cramer_numerator[row], right)
                            for row in range(2)
                        ]
                    )
                    - matrix.diff(right) * sp.Matrix(
                        [
                            first_stress(beta, cramer_numerator[row], left)
                            for row in range(2)
                        ]
                    )
                )
                expected_vector = sp.Matrix(
                    [
                        second_stress(beta, cramer_numerator[row], left, right)
                        for row in range(2)
                    ]
                )
                assert sp.simplify(
                    matrix.adjugate() * second_residual - expected_vector
                ) == sp.zeros(2, 1)
                determinant = replacement_minor(matrix, 0, second_residual)
                assert sp.expand(
                    determinant - second_stress(beta, numerator, left, right)
                ) == 0
                determinant_row.append(determinant)
                if 0 < left_index <= right_index:
                    second_count += 1
            determinant_hessian.append(determinant_row)
        for column in range(3):
            assert sp.expand(
                sum(
                    endpoint[row] * determinant_hessian[row][column]
                    for row in range(3)
                )
            ) == 0

    assert first_count == 2
    assert second_count == 6
    return {
        "retained_first_minors": first_count,
        "retained_endpoint_minors": second_count,
        "replacement_euler_syzygies": 7,
    }


def assert_chart_rescaling() -> dict[str, int]:
    """Check covariance on all retained directions."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    beta = sp.expand((x[0] + x[1]) * (r[0] - r[2]))
    numerator = sp.expand(r[1] * (x[1] ** 2 + x[2] ** 2) * y[0])
    scale = y[0] + y[1] + r[2]
    scaled_beta = sp.expand(scale * beta)
    scaled_numerator = sp.expand(scale * numerator)

    first_count = 0
    for variable in r[1:]:
        original = first_stress(beta, numerator, variable)
        scaled = first_stress(scaled_beta, scaled_numerator, variable)
        assert sp.expand(scaled - scale**2 * original) == 0
        first_count += 1

    second_count = 0
    for endpoint in (x, y):
        for left, right in combinations_with_replacement(endpoint[1:], 2):
            original = second_stress(beta, numerator, left, right)
            scaled = second_stress(scaled_beta, scaled_numerator, left, right)
            assert sp.expand(scaled - scale**3 * original) == 0
            second_count += 1
    return {"first": first_count, "second": second_count}


def assert_coordinatewise_sharpness() -> dict[str, int]:
    """Enumerate an ambient control for every retained ternary coordinate."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    groups = (x, y, r)

    outside_controls = 0
    for exceptional in (1, 2):
        beta = r[0]
        numerator = r[exceptional] * x[0] * y[0]
        multidegree = tuple(
            homogeneous_group_degree(numerator, group)
            - homogeneous_group_degree(beta, group)
            for group in groups
        )
        assert multidegree == (1, 1, 0)
        for index in (1, 2):
            stress = first_stress(beta, numerator, r[index])
            expected = r[0] * x[0] * y[0] if index == exceptional else 0
            assert sp.expand(stress - expected) == 0
        for endpoint in (x, y):
            for left, right in combinations_with_replacement(endpoint[1:], 2):
                assert second_stress(beta, numerator, left, right) == 0
        matrix = sp.diag(beta, 1)
        target = sp.Matrix([numerator, 0])
        residual = beta * target.diff(r[exceptional]) - matrix.diff(
            r[exceptional]
        ) * (matrix.adjugate() * target)
        assert replacement_minor(matrix, 0, residual) == r[0] * x[0] * y[0]
        outside_controls += 1

    endpoint_controls = 0
    retained_pairs = tuple(combinations_with_replacement((1, 2), 2))
    for endpoint_name, endpoint, other in (("x", x, y), ("y", y, x)):
        del endpoint_name
        for exceptional in retained_pairs:
            left, right = exceptional
            beta = endpoint[0]
            endpoint_factor = (
                endpoint[left] ** 2
                if left == right
                else endpoint[left] * endpoint[right]
            )
            numerator = endpoint_factor * other[0]
            ordered_groups = (x, y, r)
            multidegree = tuple(
                homogeneous_group_degree(numerator, group)
                - homogeneous_group_degree(beta, group)
                for group in ordered_groups
            )
            assert multidegree == (1, 1, 0)
            for candidate in retained_pairs:
                stress = second_stress(
                    beta,
                    numerator,
                    endpoint[candidate[0]],
                    endpoint[candidate[1]],
                )
                coefficient = 2 if left == right else 1
                expected = (
                    coefficient * endpoint[0] ** 2 * other[0]
                    if candidate == exceptional
                    else 0
                )
                assert sp.expand(stress - expected) == 0
            for candidate in retained_pairs:
                assert (
                    second_stress(
                        beta,
                        numerator,
                        other[candidate[0]],
                        other[candidate[1]],
                    )
                    == 0
                )
            for variable in r[1:]:
                assert first_stress(beta, numerator, variable) == 0
            endpoint_controls += 1

    # Each nonphysical control fails the reduced family in every pivot chart.
    outside_beta = r[0]
    outside_numerator = r[1] * x[0] * y[0]
    for pivot in range(3):
        retained = [index for index in range(3) if index != pivot]
        assert any(
            first_stress(outside_beta, outside_numerator, r[index]) != 0
            for index in retained
        )
    endpoint_beta = x[0]
    endpoint_numerator = x[1] ** 2 * y[0]
    for pivot in range(3):
        retained = [index for index in range(3) if index != pivot]
        assert any(
            second_stress(
                endpoint_beta,
                endpoint_numerator,
                x[left],
                x[right],
            )
            != 0
            for left, right in combinations_with_replacement(retained, 2)
        )

    assert outside_controls == 2
    assert endpoint_controls == 6
    return {
        "outside_coordinate_controls": outside_controls,
        "endpoint_hessian_controls": endpoint_controls,
        "pivot_charts_checked": 3,
    }


def assert_column_multidegrees(
    matrix: sp.Matrix,
    groups: tuple[tuple[sp.Symbol, ...], ...],
    expected: tuple[tuple[int, ...], ...],
) -> None:
    """Check one homogeneous multidegree for every nonzero column entry."""
    assert matrix.cols == len(expected)
    for column in range(matrix.cols):
        degrees = {
            tuple(homogeneous_group_degree(entry, group) for group in groups)
            for entry in matrix[:, column]
            if entry != 0
        }
        assert degrees == {expected[column]}


def assert_cramer_solution(
    matrix: sp.Matrix,
    target: sp.Matrix,
    solution: sp.Matrix,
) -> tuple[sp.Expr, sp.Matrix]:
    """Check an exact rational solution and return polynomial Cramer data."""
    assert sp.simplify(matrix * solution - target) == sp.zeros(matrix.rows, 1)
    beta = sp.expand(matrix.det())
    assert beta != 0
    numerator_entries: list[sp.Expr] = []
    for entry in solution:
        cleared = sp.cancel(beta * entry)
        assert sp.denom(cleared) == 1
        numerator_entries.append(sp.expand(cleared))
    numerator = sp.Matrix(numerator_entries)
    assert sp.simplify(matrix * numerator - beta * target) == sp.zeros(
        matrix.rows,
        1,
    )
    return beta, numerator


def selected_first_minor(
    matrix: sp.Matrix,
    target: sp.Matrix,
    beta: sp.Expr,
    numerator: sp.Matrix,
    variable: sp.Symbol,
) -> sp.Expr:
    """Build one raw selected first replacement determinant."""
    residual = beta * target.diff(variable) - matrix.diff(variable) * numerator
    return replacement_minor(matrix, 0, residual)


def selected_second_minor(
    matrix: sp.Matrix,
    target: sp.Matrix,
    beta: sp.Expr,
    numerator: sp.Matrix,
    left: sp.Symbol,
    right: sp.Symbol,
) -> sp.Expr:
    """Build one raw selected second replacement determinant."""
    first_left = sp.Matrix(
        [first_stress(beta, numerator[row], left) for row in range(matrix.cols)]
    )
    first_right = sp.Matrix(
        [first_stress(beta, numerator[row], right) for row in range(matrix.cols)]
    )
    residual = (
        beta**2 * target.diff(left, right)
        - beta * matrix.diff(left, right) * numerator
        - matrix.diff(left) * first_right
        - matrix.diff(right) * first_left
    )
    return replacement_minor(matrix, 0, residual)


def assert_structured_selected_systems() -> dict[str, int]:
    """Embed every sharp coordinate in deck-degree/GHZ-compatible 4x4 data."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    groups = (x, y, r)
    retained_pairs = tuple(combinations_with_replacement((1, 2), 2))

    outside_systems = 0
    for exceptional in (1, 2):
        matrix = sp.Matrix(
            [
                [r[0], y[0], 0, 0],
                [0, y[1], 0, 0],
                [0, 0, x[0], 0],
                [0, 0, 0, x[0] * y[0] * r[0]],
            ]
        )
        target = sp.Matrix([x[exceptional] * y[exceptional] * r[exceptional], 0, 0, 0])
        solution = sp.Matrix(
            [
                r[exceptional] * x[exceptional] * y[exceptional] / r[0],
                0,
                0,
                0,
            ]
        )
        assert_column_multidegrees(
            matrix,
            groups,
            ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)),
        )
        beta, numerator = assert_cramer_solution(matrix, target, solution)
        pair = sp.cancel(numerator[0] / beta)
        for index in (1, 2):
            stress = first_stress(beta, numerator[0], r[index])
            determinant = selected_first_minor(
                matrix,
                target,
                beta,
                numerator,
                r[index],
            )
            assert sp.expand(determinant - stress) == 0
            assert (stress != 0) == (index == exceptional)
        for endpoint in (x, y):
            for left, right in combinations_with_replacement(endpoint[1:], 2):
                assert sp.diff(pair, left, right) == 0
        outside_systems += 1

    endpoint_systems = 0
    for endpoint_name in ("x", "y"):
        for exceptional in retained_pairs:
            left_index, right_index = exceptional
            colour = left_index
            if endpoint_name == "x":
                matrix = sp.Matrix(
                    [
                        [r[colour], -x[right_index] * y[colour] * r[colour], 0, 0],
                        [0, x[0] * y[colour] * r[colour], 0, 0],
                        [0, 0, y[0], 0],
                        [0, 0, 0, x[0]],
                    ]
                )
                target = sp.Matrix([0, x[colour] * y[colour] * r[colour], 0, 0])
                solution = sp.Matrix(
                    [
                        x[left_index] * x[right_index] * y[colour] / x[0],
                        x[left_index] / x[0],
                        0,
                        0,
                    ]
                )
                endpoint = x
                other = y
            else:
                matrix = sp.Matrix(
                    [
                        [r[colour], -x[colour] * y[right_index] * r[colour], 0, 0],
                        [0, x[colour] * y[0] * r[colour], 0, 0],
                        [0, 0, y[0], 0],
                        [0, 0, 0, x[0]],
                    ]
                )
                target = sp.Matrix([0, x[colour] * y[colour] * r[colour], 0, 0])
                solution = sp.Matrix(
                    [
                        x[colour] * y[left_index] * y[right_index] / y[0],
                        y[left_index] / y[0],
                        0,
                        0,
                    ]
                )
                endpoint = y
                other = x
            assert_column_multidegrees(
                matrix,
                groups,
                ((0, 0, 1), (1, 1, 1), (0, 1, 0), (1, 0, 0)),
            )
            beta, numerator = assert_cramer_solution(matrix, target, solution)
            for candidate in retained_pairs:
                left = endpoint[candidate[0]]
                right = endpoint[candidate[1]]
                stress = second_stress(beta, numerator[0], left, right)
                determinant = selected_second_minor(
                    matrix,
                    target,
                    beta,
                    numerator,
                    left,
                    right,
                )
                assert sp.expand(determinant - stress) == 0
                assert (stress != 0) == (candidate == exceptional)
            for left, right in combinations_with_replacement(other[1:], 2):
                assert second_stress(beta, numerator[0], left, right) == 0
            for variable in r[1:]:
                assert first_stress(beta, numerator[0], variable) == 0
            endpoint_systems += 1

    assert (outside_systems, endpoint_systems) == (2, 6)
    return {"outside": outside_systems, "endpoint": endpoint_systems}


def assert_condition_counts() -> dict[str, dict[int, int]]:
    """Check general and ternary counts without hiding reconstruction terms."""
    general: dict[int, int] = {}
    for dimension in range(2, 8):
        order = 9
        reduced = (dimension - 1) * (order - 2) + 2 * (
            dimension * (dimension - 1) // 2
        )
        assert reduced == (dimension - 1) * (order + dimension - 2)
        general[dimension] = reduced

    ternary = {
        order: 2 * (order - 2) + 2 * 3 for order in range(2, 13)
    }
    old = {order: 3 * (order - 2) + 2 * 6 for order in range(2, 13)}
    assert all(ternary[order] == 2 * order + 2 for order in ternary)
    assert all(old[order] == 3 * order + 6 for order in old)
    assert all(old[order] - ternary[order] == order + 4 for order in old)
    return {"general_at_m9": general, "ternary": ternary}


def main() -> None:
    euler = assert_euler_syzygies()
    physical = assert_reduced_gate_on_physical_family()
    minors = assert_reduced_replacement_minors()
    scaling = assert_chart_rescaling()
    sharpness = assert_coordinatewise_sharpness()
    structured = assert_structured_selected_systems()
    counts = assert_condition_counts()
    print("balanced Cramer pair projective-minimal jet checks: PASS")
    print(f"  Euler syzygies: {euler}")
    print(f"  physical reduced/full gate: {physical}")
    print(f"  retained replacement minors: {minors}")
    print(f"  chart covariance: {scaling}")
    print(f"  ambient coordinate controls: {sharpness}")
    print(f"  structured selected systems: {structured}")
    print(f"  condition counts: {counts}")


if __name__ == "__main__":
    main()
