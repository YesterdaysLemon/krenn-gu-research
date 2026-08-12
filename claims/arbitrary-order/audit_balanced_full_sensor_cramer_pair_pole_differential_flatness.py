"""Independent no-import audit of Cramer pair differential flatness."""

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
        cleaned = tuple(
            sorted(
                (exponent, Fraction(coefficient))
                for exponent, coefficient in terms.items()
                if coefficient
            )
        )
        return cls(variable_count, cleaned)

    @classmethod
    def constant(cls, variable_count: int, coefficient: Fraction | int) -> Polynomial:
        return cls.make(
            variable_count,
            {(0,) * variable_count: Fraction(coefficient)},
        )

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

    def _assert_compatible(self, other: Polynomial) -> None:
        assert self.variable_count == other.variable_count

    def __add__(self, other: Polynomial) -> Polynomial:
        self._assert_compatible(other)
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
        self._assert_compatible(other)
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

    def evaluate(self, point: tuple[Fraction, ...]) -> Fraction:
        assert len(point) == self.variable_count
        total = Fraction(0)
        for exponent, coefficient in self.terms:
            term = coefficient
            for value, degree in zip(point, exponent, strict=True):
                term *= value**degree
            total += term
        return total

    def divisible_by_variable(self, variable: int) -> bool:
        return bool(self.terms) and all(
            exponent[variable] > 0 for exponent, _ in self.terms
        )


def first_stress(beta: Polynomial, numerator: Polynomial, variable: int) -> Polynomial:
    """Build the displayed first-order cleared polynomial."""
    return beta * numerator.derivative(variable) - (
        numerator * beta.derivative(variable)
    )


def second_stress(
    beta: Polynomial,
    numerator: Polynomial,
    left: int,
    right: int,
) -> Polynomial:
    """Build the displayed symmetric second-order cleared polynomial."""
    beta_left = beta.derivative(left)
    beta_right = beta.derivative(right)
    numerator_left = numerator.derivative(left)
    numerator_right = numerator.derivative(right)
    middle = (
        numerator_left * beta_right
        + numerator_right * beta_left
        + numerator * beta_left.derivative(right)
    )
    return (
        beta.power(2) * numerator.derivative(left).derivative(right)
        - beta * middle
        + (numerator * beta_left * beta_right).scale(2)
    )


@dataclass(frozen=True)
class Jet:
    """An exact value/gradient/Hessian jet at one rational point."""

    value: Fraction
    gradient: tuple[Fraction, ...]
    hessian: tuple[tuple[Fraction, ...], ...]

    def __mul__(self, other: Jet) -> Jet:
        size = len(self.gradient)
        assert len(other.gradient) == size
        gradient = tuple(
            self.gradient[index] * other.value + self.value * other.gradient[index]
            for index in range(size)
        )
        hessian = tuple(
            tuple(
                self.hessian[row][column] * other.value
                + self.gradient[row] * other.gradient[column]
                + self.gradient[column] * other.gradient[row]
                + self.value * other.hessian[row][column]
                for column in range(size)
            )
            for row in range(size)
        )
        return Jet(self.value * other.value, gradient, hessian)

    def inverse(self) -> Jet:
        assert self.value != 0
        size = len(self.gradient)
        inverse_value = 1 / self.value
        gradient = tuple(-entry / self.value**2 for entry in self.gradient)
        hessian = tuple(
            tuple(
                2 * self.gradient[row] * self.gradient[column] / self.value**3
                - self.hessian[row][column] / self.value**2
                for column in range(size)
            )
            for row in range(size)
        )
        return Jet(inverse_value, gradient, hessian)


def polynomial_jet(polynomial: Polynomial, point: tuple[Fraction, ...]) -> Jet:
    """Evaluate a polynomial and its complete two-jet independently."""
    size = polynomial.variable_count
    gradient = tuple(
        polynomial.derivative(index).evaluate(point) for index in range(size)
    )
    hessian = tuple(
        tuple(
            polynomial.derivative(row).derivative(column).evaluate(point)
            for column in range(size)
        )
        for row in range(size)
    )
    return Jet(polynomial.evaluate(point), gradient, hessian)


def audit_denominator_clearing_by_jets() -> dict[str, Fraction]:
    """Compare cleared polynomials with independently inverted local jets."""
    size = 3
    x, y, z = (Polynomial.variable(size, index) for index in range(size))
    one = Polynomial.constant(size, 1)
    beta = one + x + y.scale(2) + x * z
    numerator = x.power(2) + y * z + (x * y).scale(3) + one.scale(5)
    point = (Fraction(2), Fraction(-1), Fraction(3))
    beta_value = beta.evaluate(point)
    assert beta_value != 0
    quotient_jet = (
        polynomial_jet(numerator, point) * polynomial_jet(beta, point).inverse()
    )

    first = first_stress(beta, numerator, 0).evaluate(point)
    second = second_stress(beta, numerator, 0, 2).evaluate(point)
    assert first == beta_value**2 * quotient_jet.gradient[0]
    assert second == beta_value**3 * quotient_jet.hessian[0][2]
    return {"beta": beta_value, "first": first, "mixed_second": second}


def audit_physical_pair_and_reconstruction() -> dict[str, int]:
    """Rebuild a physical pair in an independent sparse representation."""
    size = 9
    variables = tuple(Polynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    matrix = ((2, -1, 3), (0, 4, -2), (5, 1, 1))
    block = Polynomial.zero(size)
    for row in range(3):
        for column in range(3):
            block += (x[row] * y[column]).scale(matrix[row][column])
    beta = (
        (x[0] * x[1] + x[2].power(2))
        * (y[0] + y[1].scale(-2) + y[2])
        * (r[0] + r[1] + r[2].scale(-3))
    )
    numerator = beta * block

    transverse = 0
    for variable in range(6, 9):
        assert first_stress(beta, numerator, variable).terms == ()
        transverse += 1

    endpoint_hessians = 0
    for endpoint in (range(3), range(3, 6)):
        for left, right in combinations_with_replacement(endpoint, 2):
            assert second_stress(beta, numerator, left, right).terms == ()
            endpoint_hessians += 1

    reconstructed = 0
    for row in range(3):
        for column in range(3):
            cleared = second_stress(beta, numerator, row, 3 + column)
            expected = beta.power(3).scale(matrix[row][column])
            assert cleared == expected
            reconstructed += 1
    return {
        "transverse": transverse,
        "endpoint_hessians": endpoint_hessians,
        "reconstructed": reconstructed,
    }


def audit_common_rescaling() -> dict[str, int]:
    """Independently verify common chart-factor covariance."""
    size = 4
    x, y, r, s = (Polynomial.variable(size, index) for index in range(size))
    one = Polynomial.constant(size, 1)
    beta = one + x + r
    numerator = beta * (x * y + y * s)
    scale = one + x * r + s
    scaled_beta = scale * beta
    scaled_numerator = scale * numerator

    for variable in range(size):
        assert first_stress(scaled_beta, scaled_numerator, variable) == scale.power(
            2
        ) * first_stress(beta, numerator, variable)
    for left in range(size):
        for right in range(size):
            assert second_stress(
                scaled_beta, scaled_numerator, left, right
            ) == scale.power(3) * second_stress(beta, numerator, left, right)
    return {"first_covariance": 2, "second_covariance": 3}


def homogeneous_group_degree(polynomial: Polynomial, group: range) -> int:
    """Return the common total degree in one coordinate group."""
    degrees = {
        sum(exponent[index] for index in group) for exponent, _ in polynomial.terms
    }
    assert len(degrees) == 1
    return degrees.pop()


def audit_sharp_omissions() -> dict[str, object]:
    """Retain the two ambient exact pole controls without imports."""
    size = 9
    variables = tuple(Polynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    groups = (range(3), range(3, 6), range(6, 9))

    transverse_beta = r[1]
    transverse_numerator = r[0] * x[0] * y[0]
    outside = first_stress(transverse_beta, transverse_numerator, 6)
    assert outside == r[1] * x[0] * y[0]

    transverse_endpoint_hessians = 0
    for endpoint_variables in (range(3), range(3, 6)):
        for left, right in combinations_with_replacement(endpoint_variables, 2):
            assert (
                second_stress(
                    transverse_beta,
                    transverse_numerator,
                    left,
                    right,
                ).terms
                == ()
            )
            transverse_endpoint_hessians += 1
    assert transverse_endpoint_hessians == 12
    assert not transverse_numerator.divisible_by_variable(7)
    transverse_multidegree = tuple(
        homogeneous_group_degree(transverse_numerator, group)
        - homogeneous_group_degree(transverse_beta, group)
        for group in groups
    )
    assert transverse_multidegree == (1, 1, 0)

    endpoint_beta = x[1]
    endpoint_numerator = x[0].power(2) * y[0]
    endpoint_transverse_stresses = 0
    for variable in range(6, 9):
        assert first_stress(endpoint_beta, endpoint_numerator, variable).terms == ()
        endpoint_transverse_stresses += 1
    assert endpoint_transverse_stresses == 3
    endpoint = second_stress(endpoint_beta, endpoint_numerator, 0, 0)
    assert endpoint == x[1].power(2) * y[0].scale(2)
    assert not endpoint_numerator.divisible_by_variable(1)
    endpoint_multidegree = tuple(
        homogeneous_group_degree(endpoint_numerator, group)
        - homogeneous_group_degree(endpoint_beta, group)
        for group in groups
    )
    assert endpoint_multidegree == (1, 1, 0)
    return {
        "outside_terms": len(outside.terms),
        "transverse_endpoint_hessians": transverse_endpoint_hessians,
        "transverse_multidegree": transverse_multidegree,
        "endpoint_transverse_stresses": endpoint_transverse_stresses,
        "endpoint_terms": len(endpoint.terms),
        "endpoint_multidegree": endpoint_multidegree,
    }


def audit_ternary_counts() -> dict[int, int]:
    """Audit the finite 3m+6 identity count through twelve nonroots."""
    counts = {
        m: 3 * (m - 2) + 2 * sum(1 for _ in combinations_with_replacement(range(3), 2))
        for m in range(2, 13)
    }
    assert all(count == 3 * m + 6 for m, count in counts.items())
    return counts


def main() -> None:
    clearing = audit_denominator_clearing_by_jets()
    physical = audit_physical_pair_and_reconstruction()
    rescaling = audit_common_rescaling()
    sharpness = audit_sharp_omissions()
    counts = audit_ternary_counts()
    print("balanced Cramer pair-pole no-import audit: PASS")
    print(f"  independent quotient jets: {clearing}")
    print(f"  sparse physical reconstruction: {physical}")
    print(f"  chart covariance: {rescaling}")
    print(f"  sharp omission controls: {sharpness}")
    print(f"  ternary counts: {counts}")


if __name__ == "__main__":
    main()
