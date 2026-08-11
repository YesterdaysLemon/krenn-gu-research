"""Independent no-import audit of the balanced Cramer--Euler pair-pole gate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

Vertices = tuple[int, ...]
Edge = tuple[int, int]


def edge(left: int, right: int) -> Edge:
    """Canonicalize one unordered edge."""
    return (left, right) if left < right else (right, left)


def recursive_hafnian(
    vertices: Vertices, weights: dict[Edge, Fraction]
) -> Fraction:
    """Compute a hafnian through a separately written first-vertex recursion."""
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    total = Fraction(0)
    for index, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        total += weights[edge(first, partner)] * recursive_hafnian(
            remainder, weights
        )
    return total


def audit_matching_count() -> dict[int, int]:
    """Audit every even labelled subset through eight vertices."""
    vertices = tuple(range(8))
    weights = {
        pair: Fraction((pair[0] + 2) * (pair[1] + 3) - 11)
        for pair in combinations(vertices, 2)
    }
    counts: dict[int, int] = {}
    for size in (2, 4, 6, 8):
        checked = 0
        for subset in combinations(vertices, size):
            moment = recursive_hafnian(subset, weights)
            right = Fraction(0)
            for pair in combinations(subset, 2):
                remainder = tuple(vertex for vertex in subset if vertex not in pair)
                right += weights[edge(*pair)] * recursive_hafnian(
                    remainder, weights
                )
            assert Fraction(size, 2) * moment == right
            checked += 1
        counts[size] = checked
    assert counts == {2: 28, 4: 70, 6: 28, 8: 1}
    return counts


def determinant_2(matrix: tuple[tuple[Fraction, Fraction], ...]) -> Fraction:
    """Return the determinant of a two-by-two matrix."""
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def cramer_numerator(
    matrix: tuple[tuple[Fraction, Fraction], ...],
    target: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    """Return adj(A)j without importing a linear-algebra package."""
    (a, b), (c, d) = matrix
    left, right = target
    return (d * left - b * right, -c * left + a * right)


def audit_cramer_overlap_and_residual() -> dict[str, Fraction]:
    """Audit two Cramer charts and one unused-row consistency residual."""
    gamma = (
        (Fraction(2), Fraction(-1)),
        (Fraction(3), Fraction(4)),
        (Fraction(-2), Fraction(5)),
    )
    solution = (Fraction(7, 3), Fraction(-5, 2))
    target = tuple(
        row[0] * solution[0] + row[1] * solution[1] for row in gamma
    )

    first_matrix = gamma[:2]
    first_target = target[:2]
    beta = determinant_2(first_matrix)
    numerator = cramer_numerator(first_matrix, first_target)
    assert numerator == tuple(beta * value for value in solution)

    other_matrix = (gamma[0], gamma[2])
    other_target = (target[0], target[2])
    other_beta = determinant_2(other_matrix)
    other_numerator = cramer_numerator(other_matrix, other_target)
    assert tuple(other_beta * value for value in numerator) == tuple(
        beta * value for value in other_numerator
    )

    inconsistent = (target[0], target[1], target[2] + 1)
    bad_numerator = cramer_numerator(first_matrix, inconsistent[:2])
    residual = (
        gamma[2][0] * bad_numerator[0]
        + gamma[2][1] * bad_numerator[1]
        - beta * inconsistent[2]
    )
    assert residual == -beta
    return {"beta": beta, "other_beta": other_beta, "bad_residual": residual}


@dataclass(frozen=True)
class Laurent:
    """A tiny exact Laurent polynomial over Q."""

    terms: tuple[tuple[int, Fraction], ...]

    @classmethod
    def make(cls, terms: dict[int, Fraction | int]) -> Laurent:
        cleaned = tuple(
            sorted(
                (power, Fraction(coefficient))
                for power, coefficient in terms.items()
                if coefficient
            )
        )
        return cls(cleaned)

    @classmethod
    def monomial(cls, power: int, coefficient: Fraction | int = 1) -> Laurent:
        return cls.make({power: coefficient})

    @classmethod
    def zero(cls) -> Laurent:
        return cls(())

    def as_dict(self) -> dict[int, Fraction]:
        return dict(self.terms)

    def __add__(self, other: Laurent) -> Laurent:
        result = self.as_dict()
        for power, coefficient in other.terms:
            result[power] = result.get(power, Fraction(0)) + coefficient
        return Laurent.make(result)

    def __neg__(self) -> Laurent:
        return Laurent.make(
            {power: -coefficient for power, coefficient in self.terms}
        )

    def __sub__(self, other: Laurent) -> Laurent:
        return self + (-other)

    def __mul__(self, other: Laurent) -> Laurent:
        result: dict[int, Fraction] = {}
        for left_power, left_coefficient in self.terms:
            for right_power, right_coefficient in other.terms:
                power = left_power + right_power
                result[power] = result.get(power, Fraction(0)) + (
                    left_coefficient * right_coefficient
                )
        return Laurent.make(result)

    def scale(self, scalar: Fraction | int) -> Laurent:
        return Laurent.make(
            {
                power: Fraction(scalar) * coefficient
                for power, coefficient in self.terms
            }
        )

    def shift(self, power: int) -> Laurent:
        return Laurent.make(
            {old_power + power: coefficient for old_power, coefficient in self.terms}
        )

    def valuation(self) -> int:
        if not self.terms:
            raise ValueError("the zero Laurent polynomial has infinite valuation")
        return self.terms[0][0]


def laurent_hafnian(
    vertices: Vertices, weights: dict[Edge, Laurent]
) -> Laurent:
    """Independent hafnian recursion over the tiny Laurent ring."""
    if not vertices:
        return Laurent.monomial(0)
    first = vertices[0]
    total = Laurent.zero()
    for index, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        total += weights[edge(first, partner)] * laurent_hafnian(
            remainder, weights
        )
    return total


def audit_pair_regular_propagation() -> dict[int, int]:
    """Audit that a common beta factor on pairs propagates to every deck term."""
    vertices = tuple(range(6))
    beta = Laurent.monomial(2)
    weights = {
        pair: Laurent.make(
            {
                0: (pair[0] + 1) * (pair[1] + 2),
                1: pair[1] - pair[0],
            }
        )
        for pair in combinations(vertices, 2)
    }
    numerators: dict[Vertices, Laurent] = {(): beta}
    for size in (2, 4, 6):
        for subset in combinations(vertices, size):
            numerators[subset] = beta * laurent_hafnian(subset, weights)

    counts: dict[int, int] = {}
    for size in (4, 6):
        checked = 0
        for subset in combinations(vertices, size):
            right = Laurent.zero()
            for pair in combinations(subset, 2):
                remainder = tuple(vertex for vertex in subset if vertex not in pair)
                right += numerators[tuple(pair)] * numerators[remainder]
            left = (beta * numerators[subset]).scale(Fraction(size, 2))
            assert left == right
            assert numerators[subset].valuation() >= beta.valuation()
            checked += 1
        counts[size] = checked
    return counts


def audit_pole_counterexample() -> dict[str, int]:
    """Audit the normalized four-label Wick deck whose first pair has a pole."""
    beta = Laurent.monomial(1)
    v12 = Laurent.monomial(0)
    v34 = Laurent.monomial(2)
    v1234 = Laurent.monomial(1)
    left = (beta * v1234).scale(2)
    right = (v12 * v34).scale(2)
    assert left == right

    c12 = v12.shift(-1)
    c34 = v34.shift(-1)
    c1234 = v1234.shift(-1)
    assert c12.valuation() == -1
    assert c34.valuation() == 1
    assert c1234 == c12 * c34 == Laurent.monomial(0)
    return {
        "beta": beta.valuation(),
        "C12": c12.valuation(),
        "C34": c34.valuation(),
        "C1234": c1234.valuation(),
    }


def main() -> None:
    counts = audit_matching_count()
    cramer = audit_cramer_overlap_and_residual()
    propagation = audit_pair_regular_propagation()
    pole = audit_pole_counterexample()
    print("balanced Cramer--Euler pair-pole independent audit: PASS")
    print(f"  exact recurrence subsets: {counts}")
    print(f"  independent Cramer charts: {cramer}")
    print(f"  Laurent pair propagation: {propagation}")
    print(f"  retained pole valuations: {pole}")


if __name__ == "__main__":
    main()
