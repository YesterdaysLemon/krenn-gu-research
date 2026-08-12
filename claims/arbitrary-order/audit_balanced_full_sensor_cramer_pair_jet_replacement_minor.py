"""Independent no-import audit of Cramer pair-jet replacement minors."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement

Exponent = tuple[int, ...]


@dataclass(frozen=True)
class Polynomial:
    """A tiny sparse multivariate polynomial over Q."""

    variable_count: int
    terms: tuple[tuple[Exponent, Fraction], ...]

    @classmethod
    def make(
        cls,
        variable_count: int,
        terms: dict[Exponent, Fraction | int],
    ) -> Polynomial:
        return cls(
            variable_count,
            tuple(
                sorted(
                    (exponent, Fraction(coefficient))
                    for exponent, coefficient in terms.items()
                    if coefficient
                )
            ),
        )

    @classmethod
    def constant(cls, variable_count: int, coefficient: Fraction | int) -> Polynomial:
        return cls.make(variable_count, {(0,) * variable_count: coefficient})

    @classmethod
    def variable(cls, variable_count: int, index: int) -> Polynomial:
        exponent = [0] * variable_count
        exponent[index] = 1
        return cls.make(variable_count, {tuple(exponent): 1})

    @classmethod
    def zero(cls, variable_count: int) -> Polynomial:
        return cls.make(variable_count, {})

    def as_dict(self) -> dict[Exponent, Fraction]:
        return dict(self.terms)

    def _compatible(self, other: Polynomial) -> None:
        assert self.variable_count == other.variable_count

    def __add__(self, other: Polynomial) -> Polynomial:
        self._compatible(other)
        result = self.as_dict()
        for exponent, coefficient in other.terms:
            result[exponent] = result.get(exponent, Fraction(0)) + coefficient
        return Polynomial.make(self.variable_count, result)

    def __neg__(self) -> Polynomial:
        return Polynomial.make(
            self.variable_count,
            {exponent: -coefficient for exponent, coefficient in self.terms},
        )

    def __sub__(self, other: Polynomial) -> Polynomial:
        return self + (-other)

    def __mul__(self, other: Polynomial) -> Polynomial:
        self._compatible(other)
        result: dict[Exponent, Fraction] = {}
        for left_exponent, left_coefficient in self.terms:
            for right_exponent, right_coefficient in other.terms:
                exponent = tuple(
                    left + right
                    for left, right in zip(left_exponent, right_exponent, strict=True)
                )
                result[exponent] = result.get(exponent, Fraction(0)) + (
                    left_coefficient * right_coefficient
                )
        return Polynomial.make(self.variable_count, result)

    def scale(self, scalar: Fraction | int) -> Polynomial:
        return Polynomial.make(
            self.variable_count,
            {
                exponent: coefficient * Fraction(scalar)
                for exponent, coefficient in self.terms
            },
        )

    def power(self, exponent: int) -> Polynomial:
        assert exponent >= 0
        result = Polynomial.constant(self.variable_count, 1)
        for _ in range(exponent):
            result = result * self
        return result

    def derivative(self, variable: int) -> Polynomial:
        result: dict[Exponent, Fraction] = {}
        for exponent, coefficient in self.terms:
            degree = exponent[variable]
            if degree == 0:
                continue
            derived = list(exponent)
            derived[variable] -= 1
            result[tuple(derived)] = coefficient * degree
        return Polynomial.make(self.variable_count, result)


Vector = list[Polynomial]
Matrix = list[list[Polynomial]]


def zero_like(polynomial: Polynomial) -> Polynomial:
    return Polynomial.zero(polynomial.variable_count)


def vector_add(left: Vector, right: Vector) -> Vector:
    assert len(left) == len(right)
    return [a + b for a, b in zip(left, right, strict=True)]


def vector_subtract(left: Vector, right: Vector) -> Vector:
    assert len(left) == len(right)
    return [a - b for a, b in zip(left, right, strict=True)]


def vector_scale(scalar: Polynomial, vector: Vector) -> Vector:
    return [scalar * entry for entry in vector]


def vector_derivative(vector: Vector, variable: int) -> Vector:
    return [entry.derivative(variable) for entry in vector]


def matrix_derivative(matrix: Matrix, variable: int) -> Matrix:
    return [[entry.derivative(variable) for entry in row] for row in matrix]


def matrix_vector(matrix: Matrix, vector: Vector) -> Vector:
    assert matrix and len(matrix[0]) == len(vector)
    result = []
    for row in matrix:
        total = zero_like(vector[0])
        for entry, value in zip(row, vector, strict=True):
            total += entry * value
        result.append(total)
    return result


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    assert left and right and len(left[0]) == len(right)
    columns = len(right[0])
    result: Matrix = []
    for left_row in left:
        row: list[Polynomial] = []
        for column in range(columns):
            total = zero_like(left_row[0])
            for index, entry in enumerate(left_row):
                total += entry * right[index][column]
            row.append(total)
        result.append(row)
    return result


def matrix_minor(matrix: Matrix, deleted_row: int, deleted_column: int) -> Matrix:
    return [
        [entry for column, entry in enumerate(row) if column != deleted_column]
        for row_index, row in enumerate(matrix)
        if row_index != deleted_row
    ]


def determinant(matrix: Matrix) -> Polynomial:
    size = len(matrix)
    assert size > 0 and all(len(row) == size for row in matrix)
    if size == 1:
        return matrix[0][0]
    total = zero_like(matrix[0][0])
    for column, entry in enumerate(matrix[0]):
        term = entry * determinant(matrix_minor(matrix, 0, column))
        total += term if column % 2 == 0 else -term
    return total


def adjugate(matrix: Matrix) -> Matrix:
    size = len(matrix)
    assert size >= 2
    result: Matrix = []
    for row in range(size):
        result_row: list[Polynomial] = []
        for column in range(size):
            cofactor = determinant(matrix_minor(matrix, column, row))
            result_row.append(cofactor if (row + column) % 2 == 0 else -cofactor)
        result.append(result_row)
    return result


def replacement_determinant(
    matrix: Matrix, column: int, replacement: Vector
) -> Polynomial:
    replaced = [row.copy() for row in matrix]
    for row, value in enumerate(replacement):
        replaced[row][column] = value
    return determinant(replaced)


def first_stress(beta: Polynomial, numerator: Vector, variable: int) -> Vector:
    return vector_subtract(
        vector_scale(beta, vector_derivative(numerator, variable)),
        vector_scale(beta.derivative(variable), numerator),
    )


def second_stress(
    beta: Polynomial,
    numerator: Vector,
    left: int,
    right: int,
) -> Vector:
    beta_left = beta.derivative(left)
    beta_right = beta.derivative(right)
    middle = vector_add(
        vector_add(
            vector_scale(beta_right, vector_derivative(numerator, left)),
            vector_scale(beta_left, vector_derivative(numerator, right)),
        ),
        vector_scale(beta.derivative(left).derivative(right), numerator),
    )
    return vector_add(
        vector_subtract(
            vector_scale(
                beta.power(2),
                vector_derivative(vector_derivative(numerator, left), right),
            ),
            vector_scale(beta, middle),
        ),
        vector_scale((beta_left * beta_right).scale(2), numerator),
    )


def first_raw_residual(
    matrix: Matrix,
    target: Vector,
    beta: Polynomial,
    numerator: Vector,
    variable: int,
) -> Vector:
    return vector_subtract(
        vector_scale(beta, vector_derivative(target, variable)),
        matrix_vector(matrix_derivative(matrix, variable), numerator),
    )


def second_raw_residual(
    matrix: Matrix,
    target: Vector,
    beta: Polynomial,
    numerator: Vector,
    first_left: Vector,
    first_right: Vector,
    left: int,
    right: int,
) -> Vector:
    result = vector_subtract(
        vector_scale(
            beta.power(2),
            vector_derivative(vector_derivative(target, left), right),
        ),
        vector_scale(
            beta,
            matrix_vector(
                matrix_derivative(matrix_derivative(matrix, left), right),
                numerator,
            ),
        ),
    )
    result = vector_subtract(
        result,
        matrix_vector(matrix_derivative(matrix, left), first_right),
    )
    return vector_subtract(
        result,
        matrix_vector(matrix_derivative(matrix, right), first_left),
    )


def assert_zero(vector: Vector) -> None:
    assert all(entry.terms == () for entry in vector)


def audit_selected_transport() -> dict[str, int]:
    """Audit transport and replacements in a separate sparse ring."""
    size = 2
    x, y = (Polynomial.variable(size, index) for index in range(size))
    one = Polynomial.constant(size, 1)
    matrix = [
        [one + x, y, one.scale(2) + x * y],
        [x.power(2), one - y, x + y],
        [x + y.power(2), one.scale(2) + x, one + x * y],
    ]
    target = [one + x * y, x.power(2) + y, y.power(2) - x]
    beta = determinant(matrix)
    assert beta.terms
    matrix_adjugate = adjugate(matrix)
    numerator = matrix_vector(matrix_adjugate, target)
    assert_zero(
        vector_subtract(matrix_vector(matrix, numerator), vector_scale(beta, target))
    )

    first_jets: dict[int, Vector] = {}
    first_residuals: dict[int, Vector] = {}
    first_replacements = 0
    for variable in range(2):
        stress = first_stress(beta, numerator, variable)
        residual = first_raw_residual(matrix, target, beta, numerator, variable)
        assert_zero(vector_subtract(stress, matrix_vector(matrix_adjugate, residual)))
        assert_zero(
            vector_subtract(matrix_vector(matrix, stress), vector_scale(beta, residual))
        )
        for column in range(3):
            assert stress[column] == replacement_determinant(matrix, column, residual)
            first_replacements += 1
        first_jets[variable] = stress
        first_residuals[variable] = residual

    second_replacements = 0
    recursive_residuals = 0
    for left, right in combinations_with_replacement(range(2), 2):
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
        assert_zero(vector_subtract(hessian, matrix_vector(matrix_adjugate, residual)))
        for column in range(3):
            assert hessian[column] == replacement_determinant(matrix, column, residual)
            second_replacements += 1

        recursive = vector_subtract(
            vector_subtract(
                vector_scale(
                    beta.power(2),
                    vector_derivative(vector_derivative(target, left), right),
                ),
                vector_scale(
                    beta,
                    matrix_vector(
                        matrix_derivative(matrix_derivative(matrix, left), right),
                        numerator,
                    ),
                ),
            ),
            matrix_vector(
                matrix_derivative(matrix, left),
                matrix_vector(matrix_adjugate, first_residuals[right]),
            ),
        )
        recursive = vector_subtract(
            recursive,
            matrix_vector(
                matrix_derivative(matrix, right),
                matrix_vector(matrix_adjugate, first_residuals[left]),
            ),
        )
        assert recursive == residual
        recursive_residuals += 1

    return {
        "first_replacements": first_replacements,
        "second_replacements": second_replacements,
        "recursive_residuals": recursive_residuals,
    }


def audit_full_row_covariance() -> dict[str, int]:
    """Audit consistent and inconsistent extra rows independently."""
    size = 2
    x, y = (Polynomial.variable(size, index) for index in range(size))
    one = Polynomial.constant(size, 1)
    zero = Polynomial.zero(size)
    matrix = [
        [one + x, y, one.scale(2) + x * y],
        [x.power(2), one - y, x + y],
        [x + y.power(2), one.scale(2) + x, one + x * y],
    ]
    target = [one + x * y, x.power(2) + y, y.power(2) - x]
    beta = determinant(matrix)
    numerator = matrix_vector(adjugate(matrix), target)
    multiplier = [
        [one, zero, zero],
        [zero, one, zero],
        [zero, zero, one],
        [x, one + y, -one],
        [y.power(2), x, one.scale(2) + x],
    ]
    sensor = matrix_multiply(multiplier, matrix)
    full_target = matrix_vector(multiplier, target)
    residual = vector_subtract(
        matrix_vector(sensor, numerator), vector_scale(beta, full_target)
    )
    assert_zero(residual)

    first_jets = {
        variable: first_stress(beta, numerator, variable) for variable in range(2)
    }
    consistent = 0
    for variable in range(2):
        raw = first_raw_residual(sensor, full_target, beta, numerator, variable)
        selected_raw = first_raw_residual(matrix, target, beta, numerator, variable)
        assert raw[:3] == selected_raw
        assert_zero(
            vector_subtract(
                matrix_vector(sensor, first_jets[variable]), vector_scale(beta, raw)
            )
        )
        for column in range(3):
            assert first_jets[variable][column] == replacement_determinant(
                matrix, column, raw[:3]
            )
        consistent += 1

    for left, right in combinations_with_replacement(range(2), 2):
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
        assert raw[:3] == selected_raw
        assert_zero(
            vector_subtract(matrix_vector(sensor, hessian), vector_scale(beta, raw))
        )
        for column in range(3):
            assert hessian[column] == replacement_determinant(matrix, column, raw[:3])
        consistent += 1

    perturbation = [x * y, zero, y, one + x, y.power(2) - x]
    bad_target = vector_add(full_target, perturbation)
    bad_residual = vector_subtract(
        matrix_vector(sensor, numerator), vector_scale(beta, bad_target)
    )
    covariance = 0
    for variable in range(2):
        raw = first_raw_residual(sensor, bad_target, beta, numerator, variable)
        left_side = vector_subtract(
            matrix_vector(sensor, first_jets[variable]),
            vector_scale(beta, raw),
        )
        assert left_side == first_stress(beta, bad_residual, variable)
        covariance += 1

    for left, right in combinations_with_replacement(range(2), 2):
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
        left_side = vector_subtract(
            matrix_vector(sensor, hessian), vector_scale(beta, raw)
        )
        assert left_side == second_stress(beta, bad_residual, left, right)
        covariance += 1
    return {"consistent_identities": consistent, "residual_covariance": covariance}


def audit_span_and_boundaries() -> dict[str, int]:
    """Compose tall spans with selected determinants and audit boundaries."""
    size = 2
    x, y = (Polynomial.variable(size, index) for index in range(size))
    one = Polynomial.constant(size, 1)
    matrix = [
        [one + x, y, one.scale(2) + x * y],
        [x.power(2), one - y, x + y],
        [x + y.power(2), one.scale(2) + x, one + x * y],
    ]
    beta = determinant(matrix)
    zero = Polynomial.zero(size)
    multiplier = [
        [one, zero, zero],
        [zero, one, zero],
        [zero, zero, one],
        [x, one + y, -one],
        [y.power(2), x, one.scale(2) + x],
    ]
    sensor = matrix_multiply(multiplier, matrix)
    coefficients = [one + x, y - one.scale(2), one + x * y]
    span_passes = 0
    span_failures = 0
    for column in range(3):
        pass_coefficients = coefficients.copy()
        pass_coefficients[column] = zero
        full_pass = matrix_vector(sensor, pass_coefficients)
        selected_pass = full_pass[:3]
        assert selected_pass == matrix_vector(matrix, pass_coefficients)
        other_span = [Polynomial.zero(size) for _ in range(len(sensor))]
        for other in range(3):
            if other == column:
                continue
            other_span = vector_add(
                other_span,
                vector_scale(pass_coefficients[other], [row[other] for row in sensor]),
            )
        assert full_pass == other_span
        assert replacement_determinant(matrix, column, selected_pass).terms == ()
        span_passes += 1

        fail_coefficients = pass_coefficients.copy()
        fail_coefficients[column] = one
        full_fail = matrix_vector(sensor, fail_coefficients)
        selected_fail = full_fail[:3]
        assert selected_fail == matrix_vector(matrix, fail_coefficients)
        assert replacement_determinant(matrix, column, selected_fail) == beta
        span_failures += 1

    boundary_size = 5
    x0, x1, y0, r0, r1 = (
        Polynomial.variable(boundary_size, index) for index in range(boundary_size)
    )
    boundary_one = Polynomial.constant(boundary_size, 1)
    boundary_zero = Polynomial.zero(boundary_size)

    transverse_matrix = [[r1, boundary_zero], [boundary_zero, boundary_one]]
    transverse_target = [r0 * x0 * y0, boundary_zero]
    transverse_beta = determinant(transverse_matrix)
    transverse_numerator = matrix_vector(adjugate(transverse_matrix), transverse_target)
    transverse_raw = first_raw_residual(
        transverse_matrix,
        transverse_target,
        transverse_beta,
        transverse_numerator,
        3,
    )
    assert replacement_determinant(transverse_matrix, 0, transverse_raw) == r1 * x0 * y0
    for endpoint in (0, 2):
        assert (
            second_stress(
                transverse_beta,
                transverse_numerator,
                endpoint,
                endpoint,
            )[0].terms
            == ()
        )

    endpoint_matrix = [[x1, boundary_zero], [boundary_zero, boundary_one]]
    endpoint_target = [x0.power(2) * y0, boundary_zero]
    endpoint_beta = determinant(endpoint_matrix)
    endpoint_numerator = matrix_vector(adjugate(endpoint_matrix), endpoint_target)
    endpoint_transverse = first_stress(endpoint_beta, endpoint_numerator, 3)
    assert_zero(endpoint_transverse)
    endpoint_x_first = first_stress(endpoint_beta, endpoint_numerator, 0)
    endpoint_raw = second_raw_residual(
        endpoint_matrix,
        endpoint_target,
        endpoint_beta,
        endpoint_numerator,
        endpoint_x_first,
        endpoint_x_first,
        0,
        0,
    )
    assert replacement_determinant(endpoint_matrix, 0, endpoint_raw) == x1.power(
        2
    ) * y0.scale(2)
    return {
        "tall_span_passes": span_passes,
        "tall_span_failures": span_failures,
        "boundary_minors": 2,
    }


def audit_nondivisible_residual() -> dict[str, int]:
    """Audit both corrections when an inconsistent target residual is one."""
    size = 1
    x = Polynomial.variable(size, 0)
    one = Polynomial.constant(size, 1)
    zero = Polynomial.zero(size)
    matrix = [[x, zero], [zero, one]]
    target = [one, zero]
    beta = determinant(matrix)
    numerator = matrix_vector(adjugate(matrix), target)
    sensor = [[x, zero], [zero, one], [one, zero]]
    full_target = [one, zero, zero]
    target_residual = vector_subtract(
        matrix_vector(sensor, numerator), vector_scale(beta, full_target)
    )
    assert target_residual == [zero, zero, one]

    first = first_stress(beta, numerator, 0)
    first_raw = first_raw_residual(sensor, full_target, beta, numerator, 0)
    first_left = vector_subtract(
        matrix_vector(sensor, first), vector_scale(beta, first_raw)
    )
    assert first_left == first_stress(beta, target_residual, 0)

    hessian = second_stress(beta, numerator, 0, 0)
    second_raw = second_raw_residual(
        sensor,
        full_target,
        beta,
        numerator,
        first,
        first,
        0,
        0,
    )
    second_left = vector_subtract(
        matrix_vector(sensor, hessian), vector_scale(beta, second_raw)
    )
    assert second_left == second_stress(beta, target_residual, 0, 0)
    return {"nondivisible_residual_terms": len(target_residual[2].terms)}


def main() -> None:
    selected = audit_selected_transport()
    full_rows = audit_full_row_covariance()
    controls = audit_span_and_boundaries()
    nondivisible = audit_nondivisible_residual()
    print("balanced Cramer pair-jet no-import audit: PASS")
    print(f"  selected transport: {selected}")
    print(f"  full-row covariance: {full_rows}")
    print(f"  span and boundary controls: {controls}")
    print(f"  nondivisible target residual: {nondivisible}")


if __name__ == "__main__":
    main()
