"""Independent no-import audit of the projective-minimal pair-jet gate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations_with_replacement

Exponent = tuple[int, ...]


@dataclass(frozen=True)
class SparsePolynomial:
    """Small exact multivariate polynomial used only by this audit."""

    variable_count: int
    terms: tuple[tuple[Exponent, Fraction], ...]

    @classmethod
    def from_dict(
        cls,
        variable_count: int,
        raw: dict[Exponent, int | Fraction],
    ) -> SparsePolynomial:
        terms = tuple(
            sorted(
                (exponent, Fraction(coefficient))
                for exponent, coefficient in raw.items()
                if coefficient
            )
        )
        return cls(variable_count, terms)

    @classmethod
    def zero(cls, variable_count: int) -> SparsePolynomial:
        return cls.from_dict(variable_count, {})

    @classmethod
    def one(cls, variable_count: int) -> SparsePolynomial:
        return cls.from_dict(variable_count, {(0,) * variable_count: 1})

    @classmethod
    def variable(cls, variable_count: int, index: int) -> SparsePolynomial:
        exponent = [0] * variable_count
        exponent[index] = 1
        return cls.from_dict(variable_count, {tuple(exponent): 1})

    def dictionary(self) -> dict[Exponent, Fraction]:
        return dict(self.terms)

    def __add__(self, other: SparsePolynomial) -> SparsePolynomial:
        assert self.variable_count == other.variable_count
        result = self.dictionary()
        for exponent, coefficient in other.terms:
            result[exponent] = result.get(exponent, Fraction(0)) + coefficient
        return SparsePolynomial.from_dict(self.variable_count, result)

    def __neg__(self) -> SparsePolynomial:
        return SparsePolynomial.from_dict(
            self.variable_count,
            {exponent: -coefficient for exponent, coefficient in self.terms},
        )

    def __sub__(self, other: SparsePolynomial) -> SparsePolynomial:
        return self + (-other)

    def __mul__(self, other: SparsePolynomial) -> SparsePolynomial:
        assert self.variable_count == other.variable_count
        result: dict[Exponent, Fraction] = {}
        for left_exponent, left_coefficient in self.terms:
            for right_exponent, right_coefficient in other.terms:
                exponent = tuple(
                    left + right
                    for left, right in zip(
                        left_exponent,
                        right_exponent,
                        strict=True,
                    )
                )
                result[exponent] = result.get(exponent, Fraction(0)) + (
                    left_coefficient * right_coefficient
                )
        return SparsePolynomial.from_dict(self.variable_count, result)

    def scaled(self, scalar: int | Fraction) -> SparsePolynomial:
        return SparsePolynomial.from_dict(
            self.variable_count,
            {
                exponent: coefficient * Fraction(scalar)
                for exponent, coefficient in self.terms
            },
        )

    def power(self, exponent: int) -> SparsePolynomial:
        assert exponent >= 0
        result = SparsePolynomial.one(self.variable_count)
        for _ in range(exponent):
            result = result * self
        return result

    def derivative(self, variable: int) -> SparsePolynomial:
        result: dict[Exponent, Fraction] = {}
        for exponent, coefficient in self.terms:
            degree = exponent[variable]
            if not degree:
                continue
            derived = list(exponent)
            derived[variable] -= 1
            result[tuple(derived)] = coefficient * degree
        return SparsePolynomial.from_dict(self.variable_count, result)


def first_stress(
    beta: SparsePolynomial,
    numerator: SparsePolynomial,
    variable: int,
) -> SparsePolynomial:
    """Build one quotient-cleared first derivative from scratch."""
    return beta * numerator.derivative(variable) - (
        numerator * beta.derivative(variable)
    )


def second_stress(
    beta: SparsePolynomial,
    numerator: SparsePolynomial,
    left: int,
    right: int,
) -> SparsePolynomial:
    """Build one quotient-cleared Hessian entry from scratch."""
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
        + (numerator * beta_left * beta_right).scaled(2)
    )


def linear_combination(
    coefficients: tuple[SparsePolynomial, ...],
    entries: tuple[SparsePolynomial, ...],
) -> SparsePolynomial:
    """Form a same-length polynomial linear combination."""
    assert len(coefficients) == len(entries)
    total = SparsePolynomial.zero(coefficients[0].variable_count)
    for coefficient, entry in zip(coefficients, entries, strict=True):
        total += coefficient * entry
    return total


def group_degree(polynomial: SparsePolynomial, group: range) -> int:
    """Return the common degree of a homogeneous variable group."""
    degrees = {
        sum(exponent[index] for index in group) for exponent, _ in polynomial.terms
    }
    assert len(degrees) == 1
    return degrees.pop()


def audit_euler_syzygies() -> dict[str, int]:
    """Reconstruct both radial syzygies on different sparse data."""
    size = 9
    variables = tuple(SparsePolynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    beta = (
        (x[0] + x[1].scaled(-2) + x[2])
        * (y[0] + y[1] + y[2].scaled(2))
        * (r[0] + r[1])
    )
    numerator = (
        (x[0] * x[2] + x[1].power(2) + x[2].power(2).scaled(3))
        * (y[0].power(2) + y[0] * y[2] + y[1] * y[2])
        * r[2]
    )
    groups = (range(3), range(3, 6), range(6, 9))
    multidegree = tuple(
        group_degree(numerator, group) - group_degree(beta, group)
        for group in groups
    )
    assert multidegree == (1, 1, 0)

    outside = tuple(first_stress(beta, numerator, variable) for variable in range(6, 9))
    assert any(stress.terms for stress in outside)
    assert linear_combination(r, outside).terms == ()

    endpoint_relations = 0
    for endpoint in (range(3), range(3, 6)):
        endpoint_variables = tuple(variables[index] for index in endpoint)
        hessian = tuple(
            tuple(second_stress(beta, numerator, row, column) for column in endpoint)
            for row in endpoint
        )
        assert any(entry.terms for row in hessian for entry in row)
        for offset in range(3):
            column = tuple(row[offset] for row in hessian)
            assert linear_combination(endpoint_variables, column).terms == ()
            endpoint_relations += 1

    return {"outside": 1, "endpoint": endpoint_relations}


def audit_physical_reduction() -> dict[str, int]:
    """Check the reduced list and every recovered radial entry independently."""
    size = 12
    variables = tuple(SparsePolynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    s = variables[9:12]
    block = (
        (x[0] * y[0]).scaled(2)
        + (x[0] * y[2]).scaled(-1)
        + (x[1] * y[0]).scaled(3)
        + (x[1] * y[1]).scaled(5)
        + x[2] * y[1]
        + (x[2] * y[2]).scaled(-4)
    )
    beta = (
        (x[0] + x[2])
        * (y[0] + y[1].scaled(-1))
        * (r[0] + r[2])
        * (s[0] + s[1] + s[2])
    )
    numerator = beta * block
    retained = 0
    radial = 0

    for outside in (range(6, 9), range(9, 12)):
        stresses = tuple(first_stress(beta, numerator, index) for index in outside)
        assert all(not stresses[offset].terms for offset in (1, 2))
        retained += 2
        assert not stresses[0].terms
        radial += 1

    for endpoint in (range(3), range(3, 6)):
        pivot = endpoint.start
        for left, right in combinations_with_replacement(tuple(endpoint)[1:], 2):
            assert not second_stress(beta, numerator, left, right).terms
            retained += 1
        for index in endpoint:
            assert not second_stress(beta, numerator, pivot, index).terms
            radial += 1

    assert retained == 10
    assert radial == 8
    return {"retained": retained, "radial": radial}


def audit_diagonal_replacement_form() -> dict[str, int]:
    """Check retained diagonal-Cramer replacement entries without matrices."""
    size = 9
    variables = tuple(SparsePolynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    beta = (r[0] + r[2]) * (x[0] + x[2])
    numerator = r[1] * (x[1].power(2) + x[1] * x[2]) * y[0]

    first_count = 0
    first_replacements: list[SparsePolynomial] = []
    for variable in range(6, 9):
        raw_replacement = beta * numerator.derivative(variable) - (
            beta.derivative(variable) * numerator
        )
        assert raw_replacement == first_stress(beta, numerator, variable)
        first_replacements.append(raw_replacement)
        if variable > 6:
            first_count += 1
    assert not linear_combination(r, tuple(first_replacements)).terms

    second_count = 0
    for endpoint in (range(3), range(3, 6)):
        endpoint_indices = tuple(endpoint)
        endpoint_variables = tuple(variables[index] for index in endpoint_indices)
        replacements: list[list[SparsePolynomial]] = []
        for left_offset, left in enumerate(endpoint_indices):
            row: list[SparsePolynomial] = []
            for right_offset, right in enumerate(endpoint_indices):
                first_left = first_stress(beta, numerator, left)
                first_right = first_stress(beta, numerator, right)
                raw_replacement = (
                    beta.power(2) * numerator.derivative(left).derivative(right)
                    - beta * beta.derivative(left).derivative(right) * numerator
                    - beta.derivative(left) * first_right
                    - beta.derivative(right) * first_left
                )
                assert raw_replacement == second_stress(
                    beta,
                    numerator,
                    left,
                    right,
                )
                row.append(raw_replacement)
                if 0 < left_offset <= right_offset:
                    second_count += 1
            replacements.append(row)
        for column in range(3):
            assert not linear_combination(
                endpoint_variables,
                tuple(replacements[row][column] for row in range(3)),
            ).terms
    assert (first_count, second_count) == (2, 6)
    return {"first": first_count, "second": second_count, "syzygies": 7}


def audit_chart_covariance() -> dict[str, int]:
    """Verify common-factor powers for every retained ternary direction."""
    size = 9
    variables = tuple(SparsePolynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    beta = (x[0] + x[1]) * (r[0] + r[2])
    numerator = r[1] * (x[1].power(2) + x[2].power(2)) * y[0]
    scale = y[0] + y[2] + r[1]
    scaled_beta = scale * beta
    scaled_numerator = scale * numerator

    first_count = 0
    for variable in range(7, 9):
        assert first_stress(scaled_beta, scaled_numerator, variable) == (
            scale.power(2) * first_stress(beta, numerator, variable)
        )
        first_count += 1
    second_count = 0
    for endpoint in (range(3), range(3, 6)):
        nonpivot = tuple(endpoint)[1:]
        for left, right in combinations_with_replacement(nonpivot, 2):
            assert second_stress(
                scaled_beta,
                scaled_numerator,
                left,
                right,
            ) == scale.power(3) * second_stress(beta, numerator, left, right)
            second_count += 1
    return {"first": first_count, "second": second_count}


def audit_coordinatewise_controls() -> dict[str, int]:
    """Falsify omission of each retained affine-projective coordinate."""
    size = 9
    variables = tuple(SparsePolynomial.variable(size, index) for index in range(size))
    x = variables[0:3]
    y = variables[3:6]
    r = variables[6:9]
    groups = (range(3), range(3, 6), range(6, 9))

    outside_controls = 0
    for exceptional in (1, 2):
        beta = r[0]
        numerator = r[exceptional] * x[0] * y[0]
        assert tuple(
            group_degree(numerator, group) - group_degree(beta, group)
            for group in groups
        ) == (1, 1, 0)
        for index in (1, 2):
            expected = r[0] * x[0] * y[0] if index == exceptional else SparsePolynomial.zero(size)
            assert first_stress(beta, numerator, 6 + index) == expected
        for endpoint in (range(3), range(3, 6)):
            for left, right in combinations_with_replacement(tuple(endpoint)[1:], 2):
                assert not second_stress(beta, numerator, left, right).terms
        outside_controls += 1

    endpoint_controls = 0
    retained_pairs = tuple(combinations_with_replacement((1, 2), 2))
    for endpoint, other in ((range(3), range(3, 6)), (range(3, 6), range(3))):
        endpoint_indices = tuple(endpoint)
        other_indices = tuple(other)
        for exceptional in retained_pairs:
            left, right = exceptional
            beta = variables[endpoint_indices[0]]
            factor = (
                variables[endpoint_indices[left]].power(2)
                if left == right
                else variables[endpoint_indices[left]] * variables[endpoint_indices[right]]
            )
            numerator = factor * variables[other_indices[0]]
            assert tuple(
                group_degree(numerator, group) - group_degree(beta, group)
                for group in groups
            ) == (1, 1, 0)
            for candidate in retained_pairs:
                candidate_left = endpoint_indices[candidate[0]]
                candidate_right = endpoint_indices[candidate[1]]
                coefficient = 2 if left == right else 1
                expected = (
                    variables[endpoint_indices[0]].power(2)
                    * variables[other_indices[0]]
                ).scaled(coefficient)
                if candidate != exceptional:
                    expected = SparsePolynomial.zero(size)
                assert second_stress(
                    beta,
                    numerator,
                    candidate_left,
                    candidate_right,
                ) == expected
            for candidate in retained_pairs:
                assert not second_stress(
                    beta,
                    numerator,
                    other_indices[candidate[0]],
                    other_indices[candidate[1]],
                ).terms
            for variable in range(7, 9):
                assert not first_stress(beta, numerator, variable).terms
            endpoint_controls += 1

    assert outside_controls == 2
    assert endpoint_controls == 6
    return {"outside": outside_controls, "endpoint": endpoint_controls}


def audit_counts() -> dict[int, int]:
    """Recompute the uniform-d formula and the ternary saving."""
    ternary: dict[int, int] = {}
    for order in range(2, 15):
        reduced = (3 - 1) * (order - 2) + 2 * sum(
            1 for _ in combinations_with_replacement(range(1, 3), 2)
        )
        full = 3 * (order - 2) + 2 * sum(
            1 for _ in combinations_with_replacement(range(3), 2)
        )
        assert reduced == 2 * order + 2
        assert full == 3 * order + 6
        assert full - reduced == order + 4
        ternary[order] = reduced

    for dimension in range(2, 9):
        for order in range(2, 10):
            direct = (dimension - 1) * (order - 2) + 2 * sum(
                1
                for _ in combinations_with_replacement(range(1, dimension), 2)
            )
            assert direct == (dimension - 1) * (order + dimension - 2)
    return ternary


def main() -> None:
    euler = audit_euler_syzygies()
    physical = audit_physical_reduction()
    replacements = audit_diagonal_replacement_form()
    covariance = audit_chart_covariance()
    controls = audit_coordinatewise_controls()
    counts = audit_counts()
    print("projective-minimal pair-jet no-import audit: PASS")
    print(f"  sparse Euler syzygies: {euler}")
    print(f"  physical reduced/full family: {physical}")
    print(f"  diagonal replacement entries: {replacements}")
    print(f"  chart covariance: {covariance}")
    print(f"  coordinatewise controls: {controls}")
    print(f"  ternary counts: {counts}")


if __name__ == "__main__":
    main()
