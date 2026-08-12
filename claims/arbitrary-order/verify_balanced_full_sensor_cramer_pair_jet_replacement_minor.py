"""Primary exact checks for Cramer pair-jet replacement minors."""

from __future__ import annotations

from itertools import combinations_with_replacement

import sympy as sp


def expanded(matrix: sp.MatrixBase) -> sp.Matrix:
    """Expand every entry of a matrix or column vector."""
    return sp.Matrix(matrix).applyfunc(sp.expand)


def assert_zero(matrix: sp.MatrixBase) -> None:
    """Assert exact entrywise polynomial vanishing."""
    assert all(sp.expand(entry) == 0 for entry in matrix)


def first_stress(
    beta: sp.Expr,
    numerator: sp.MatrixBase,
    variable: sp.Symbol,
) -> sp.Matrix:
    """Return beta^2 times one derivative of numerator / beta."""
    return expanded(
        beta * numerator.diff(variable) - numerator * sp.diff(beta, variable)
    )


def second_stress(
    beta: sp.Expr,
    numerator: sp.MatrixBase,
    left: sp.Symbol,
    right: sp.Symbol,
) -> sp.Matrix:
    """Return beta^3 times one mixed derivative of numerator / beta."""
    beta_left = sp.diff(beta, left)
    beta_right = sp.diff(beta, right)
    return expanded(
        beta**2 * numerator.diff(left, right)
        - beta
        * (
            numerator.diff(left) * beta_right
            + numerator.diff(right) * beta_left
            + numerator * sp.diff(beta, left, right)
        )
        + 2 * numerator * beta_left * beta_right
    )


def first_raw_residual(
    matrix: sp.MatrixBase,
    target: sp.MatrixBase,
    beta: sp.Expr,
    numerator: sp.MatrixBase,
    variable: sp.Symbol,
) -> sp.Matrix:
    """Build beta D(target) - D(matrix) numerator."""
    return expanded(beta * target.diff(variable) - matrix.diff(variable) * numerator)


def second_raw_residual(
    matrix: sp.MatrixBase,
    target: sp.MatrixBase,
    beta: sp.Expr,
    numerator: sp.MatrixBase,
    first_left: sp.MatrixBase,
    first_right: sp.MatrixBase,
    left: sp.Symbol,
    right: sp.Symbol,
) -> sp.Matrix:
    """Build the raw second target residual from first cleared jets."""
    return expanded(
        beta**2 * target.diff(left, right)
        - beta * matrix.diff(left, right) * numerator
        - matrix.diff(left) * first_right
        - matrix.diff(right) * first_left
    )


def replacement_determinant(
    matrix: sp.MatrixBase,
    column: int,
    replacement: sp.MatrixBase,
) -> sp.Expr:
    """Return the determinant after replacing one column."""
    replaced = sp.Matrix(matrix)
    replaced[:, column] = replacement
    return sp.expand(replaced.det())


def assert_selected_transport() -> dict[str, int]:
    """Check all first and second directions on a nonconstant 3x3 system."""
    x, y = sp.symbols("x y")
    matrix = sp.Matrix(
        (
            (1 + x, y, x * y),
            (x**2 + y, 2 - y, x),
            (y**2, x + y, 1 + x * y),
        )
    )
    target = sp.Matrix((1 + x * y, x**2 - y, y**2 + x))
    beta = sp.expand(matrix.det())
    assert beta != 0
    adjugate = matrix.adjugate().applyfunc(sp.expand)
    numerator = expanded(adjugate * target)
    assert_zero(matrix * numerator - beta * target)

    first_jets: dict[sp.Symbol, sp.Matrix] = {}
    first_residuals: dict[sp.Symbol, sp.Matrix] = {}
    replacement_count = 0
    for variable in (x, y):
        stress = first_stress(beta, numerator, variable)
        residual = first_raw_residual(matrix, target, beta, numerator, variable)
        assert_zero(stress - adjugate * residual)
        assert_zero(matrix * stress - beta * residual)
        for column in range(3):
            assert (
                sp.expand(
                    stress[column] - replacement_determinant(matrix, column, residual)
                )
                == 0
            )
            replacement_count += 1
        first_jets[variable] = stress
        first_residuals[variable] = residual

    second_count = 0
    for left, right in combinations_with_replacement((x, y), 2):
        hessian = second_stress(beta, numerator, left, right)
        residual = second_raw_residual(
            matrix,
            target,
            beta,
            numerator,
            first_jets[left],
            first_jets[right],
            left,
            right,
        )
        assert_zero(hessian - adjugate * residual)
        assert_zero(matrix * hessian - beta * residual)
        for column in range(3):
            assert (
                sp.expand(
                    hessian[column] - replacement_determinant(matrix, column, residual)
                )
                == 0
            )
            second_count += 1

    recursive_count = 0
    for left, right in combinations_with_replacement((x, y), 2):
        recursive = expanded(
            beta**2 * target.diff(left, right)
            - beta * matrix.diff(left, right) * numerator
            - matrix.diff(left) * adjugate * first_residuals[right]
            - matrix.diff(right) * adjugate * first_residuals[left]
        )
        direct = second_raw_residual(
            matrix,
            target,
            beta,
            numerator,
            first_jets[left],
            first_jets[right],
            left,
            right,
        )
        assert_zero(recursive - direct)
        recursive_count += 1

    return {
        "first_replacement_minors": replacement_count,
        "second_replacement_minors": second_count,
        "recursive_second_residuals": recursive_count,
    }


def assert_full_row_residual_covariance() -> dict[str, int]:
    """Check consistent and inconsistent full-row transport identities."""
    x, y = sp.symbols("x y")
    matrix = sp.Matrix(
        (
            (1 + x, y, x * y),
            (x**2 + y, 2 - y, x),
            (y**2, x + y, 1 + x * y),
        )
    )
    target = sp.Matrix((1 + x * y, x**2 - y, y**2 + x))
    beta = sp.expand(matrix.det())
    numerator = expanded(matrix.adjugate() * target)
    multiplier = sp.Matrix(
        (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (x, 1 + y, -1),
            (y**2, x, 2 + x),
        )
    )
    sensor = expanded(multiplier * matrix)
    full_target = expanded(multiplier * target)
    target_residual = expanded(sensor * numerator - beta * full_target)
    assert_zero(target_residual)

    first_jets = {
        variable: first_stress(beta, numerator, variable) for variable in (x, y)
    }
    consistent_first = 0
    consistent_second = 0
    for variable in (x, y):
        raw = first_raw_residual(sensor, full_target, beta, numerator, variable)
        selected_raw = first_raw_residual(matrix, target, beta, numerator, variable)
        assert_zero(raw[:3, :] - selected_raw)
        assert_zero(sensor * first_jets[variable] - beta * raw)
        for column in range(3):
            assert (
                sp.expand(
                    first_jets[variable][column]
                    - replacement_determinant(matrix, column, raw[:3, :])
                )
                == 0
            )
        consistent_first += 1

    for left, right in combinations_with_replacement((x, y), 2):
        hessian = second_stress(beta, numerator, left, right)
        raw = second_raw_residual(
            sensor,
            full_target,
            beta,
            numerator,
            first_jets[left],
            first_jets[right],
            left,
            right,
        )
        selected_raw = second_raw_residual(
            matrix,
            target,
            beta,
            numerator,
            first_jets[left],
            first_jets[right],
            left,
            right,
        )
        assert_zero(raw[:3, :] - selected_raw)
        assert_zero(sensor * hessian - beta * raw)
        for column in range(3):
            assert (
                sp.expand(
                    hessian[column]
                    - replacement_determinant(matrix, column, raw[:3, :])
                )
                == 0
            )
        consistent_second += 1

    perturbation = sp.Matrix((x * y, 0, y, 1 + x, y**2 - x))
    bad_target = expanded(full_target + perturbation)
    bad_residual = expanded(sensor * numerator - beta * bad_target)
    inconsistent_first = 0
    inconsistent_second = 0
    for variable in (x, y):
        raw = first_raw_residual(sensor, bad_target, beta, numerator, variable)
        left_side = expanded(sensor * first_jets[variable] - beta * raw)
        right_side = first_stress(beta, bad_residual, variable)
        assert_zero(left_side - right_side)
        inconsistent_first += 1

    for left, right in combinations_with_replacement((x, y), 2):
        hessian = second_stress(beta, numerator, left, right)
        raw = second_raw_residual(
            sensor,
            bad_target,
            beta,
            numerator,
            first_jets[left],
            first_jets[right],
            left,
            right,
        )
        left_side = expanded(sensor * hessian - beta * raw)
        right_side = second_stress(beta, bad_residual, left, right)
        assert_zero(left_side - right_side)
        inconsistent_second += 1

    return {
        "consistent_first_rows": consistent_first,
        "consistent_second_rows": consistent_second,
        "inconsistent_first_covariance": inconsistent_first,
        "inconsistent_second_covariance": inconsistent_second,
    }


def assert_column_span_controls() -> dict[str, int]:
    """Compose tall full-row spans with selected replacement determinants."""
    x, y = sp.symbols("x y")
    matrix = sp.Matrix(
        (
            (1 + x, y, x * y),
            (x**2 + y, 2 - y, x),
            (y**2, x + y, 1 + x * y),
        )
    )
    beta = sp.expand(matrix.det())
    multiplier = sp.Matrix(
        (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (x, 1 + y, -1),
            (y**2, x, 2 + x),
        )
    )
    sensor = expanded(multiplier * matrix)
    coefficients = sp.Matrix((1 + x, y - 2, 1 + x * y))
    pass_count = 0
    fail_count = 0
    for column in range(3):
        pass_coefficients = coefficients.copy()
        pass_coefficients[column] = 0
        full_pass = expanded(sensor * pass_coefficients)
        selected_pass = full_pass[:3, :]
        assert_zero(selected_pass - matrix * pass_coefficients)
        in_other_span = sp.zeros(sensor.rows, 1)
        for other in range(3):
            if other != column:
                in_other_span += sensor[:, other] * pass_coefficients[other]
        assert_zero(full_pass - in_other_span)
        assert replacement_determinant(matrix, column, selected_pass) == 0
        pass_count += 1

        fail_coefficients = pass_coefficients.copy()
        fail_coefficients[column] = 1
        full_fail = expanded(sensor * fail_coefficients)
        selected_fail = full_fail[:3, :]
        assert_zero(selected_fail - matrix * fail_coefficients)
        assert (
            sp.expand(replacement_determinant(matrix, column, selected_fail) - beta)
            == 0
        )
        fail_count += 1
    return {"tall_span_passes": pass_count, "tall_span_failures": fail_count}


def assert_nondivisible_target_residual() -> dict[str, sp.Expr]:
    """Check both correction formulas when one target residual equals one."""
    x = sp.symbols("x")
    matrix = sp.diag(x, 1)
    target = sp.Matrix((1, 0))
    beta = sp.expand(matrix.det())
    numerator = expanded(matrix.adjugate() * target)
    sensor = sp.Matrix(((x, 0), (0, 1), (1, 0)))
    full_target = sp.Matrix((1, 0, 0))
    target_residual = expanded(sensor * numerator - beta * full_target)
    assert target_residual == sp.Matrix((0, 0, 1))

    first = first_stress(beta, numerator, x)
    first_raw = first_raw_residual(sensor, full_target, beta, numerator, x)
    assert_zero(
        sensor * first - beta * first_raw - first_stress(beta, target_residual, x)
    )

    hessian = second_stress(beta, numerator, x, x)
    second_raw = second_raw_residual(
        sensor,
        full_target,
        beta,
        numerator,
        first,
        first,
        x,
        x,
    )
    assert_zero(
        sensor * hessian
        - beta * second_raw
        - second_stress(beta, target_residual, x, x)
    )
    return {
        "beta": beta,
        "nondivisible_residual": target_residual[2],
    }


def assert_abstract_cramer_boundaries() -> dict[str, sp.Expr]:
    """Retain the transverse and endpoint abstract Cramer controls."""
    x0, x1, y0, r0, r1 = sp.symbols("x0 x1 y0 r0 r1")

    transverse_matrix = sp.diag(r1, 1)
    transverse_target = sp.Matrix((r0 * x0 * y0, 0))
    transverse_beta = sp.expand(transverse_matrix.det())
    transverse_numerator = expanded(transverse_matrix.adjugate() * transverse_target)
    transverse_first = first_stress(transverse_beta, transverse_numerator, r0)
    transverse_raw = first_raw_residual(
        transverse_matrix,
        transverse_target,
        transverse_beta,
        transverse_numerator,
        r0,
    )
    transverse_minor = replacement_determinant(transverse_matrix, 0, transverse_raw)
    assert transverse_minor == r1 * x0 * y0
    assert transverse_first[0] == transverse_minor
    for endpoint in (x0, y0):
        assert (
            second_stress(transverse_beta, transverse_numerator, endpoint, endpoint)[0]
            == 0
        )

    endpoint_matrix = sp.diag(x1, 1)
    endpoint_target = sp.Matrix((x0**2 * y0, 0))
    endpoint_beta = sp.expand(endpoint_matrix.det())
    endpoint_numerator = expanded(endpoint_matrix.adjugate() * endpoint_target)
    endpoint_hessian = second_stress(endpoint_beta, endpoint_numerator, x0, x0)
    endpoint_transverse = first_stress(endpoint_beta, endpoint_numerator, r0)
    assert_zero(endpoint_transverse)
    endpoint_x_first = first_stress(endpoint_beta, endpoint_numerator, x0)
    endpoint_raw = second_raw_residual(
        endpoint_matrix,
        endpoint_target,
        endpoint_beta,
        endpoint_numerator,
        endpoint_x_first,
        endpoint_x_first,
        x0,
        x0,
    )
    endpoint_minor = replacement_determinant(endpoint_matrix, 0, endpoint_raw)
    assert endpoint_minor == 2 * x1**2 * y0
    assert endpoint_hessian[0] == endpoint_minor

    return {
        "transverse_minor": transverse_minor,
        "endpoint_minor": endpoint_minor,
    }


def main() -> None:
    selected = assert_selected_transport()
    full_rows = assert_full_row_residual_covariance()
    spans = assert_column_span_controls()
    nondivisible = assert_nondivisible_target_residual()
    boundaries = assert_abstract_cramer_boundaries()
    print("balanced Cramer pair-jet replacement-minor checks: PASS")
    print(f"  selected transport: {selected}")
    print(f"  full-row covariance: {full_rows}")
    print(f"  column-span controls: {spans}")
    print(f"  nondivisible target residual: {nondivisible}")
    print(f"  abstract Cramer boundaries: {boundaries}")


if __name__ == "__main__":
    main()
