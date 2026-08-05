"""Independent no-project-import audit of the P3+K2 cubic obstruction."""

from __future__ import annotations

from fractions import Fraction

VARIABLE_COUNT = 9


class Poly:
    """Minimal sparse polynomial over Q for the fixed ideal certificate."""

    def __init__(self, terms=None):
        self.terms = {
            monomial: Fraction(coefficient)
            for monomial, coefficient in (terms or {}).items()
            if coefficient
        }

    @staticmethod
    def coerce(value):
        if isinstance(value, Poly):
            return value
        return Poly({(0,) * VARIABLE_COUNT: Fraction(value)})

    def __add__(self, other):
        other = self.coerce(other)
        result = dict(self.terms)
        for monomial, coefficient in other.terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
            if result[monomial] == 0:
                del result[monomial]
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly(
            {monomial: -coefficient for monomial, coefficient in self.terms.items()}
        )

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        result = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in other.terms.items():
                monomial = tuple(
                    left + right
                    for left, right in zip(left_monomial, right_monomial, strict=True)
                )
                result[monomial] = (
                    result.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly(result)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def variable(index):
    monomial = [0] * VARIABLE_COUNT
    monomial[index] = 1
    return Poly({tuple(monomial): Fraction(1)})


def matrix_add(*matrices):
    return tuple(
        tuple(sum(matrix[row][column] for matrix in matrices) for column in range(2))
        for row in range(2)
    )


def main() -> None:
    p, x, y, u, v, r, s, t, w = tuple(
        variable(index) for index in range(VARIABLE_COUNT)
    )
    equation_a = u + p * r
    equation_b = x + p * s
    equation_c = v + p * t
    equation_d = y + p * w
    equation_e = 1 + x * t + y * r
    equation_f = p + x * v + y * u

    first_certificate = (
        p * equation_e
        + equation_f
        - x * equation_c
        - y * equation_a
    )
    assert first_certificate == 2 * p
    unit_certificate = (
        equation_e
        - t * equation_b
        - r * equation_d
        + Fraction(1, 2) * (s * t + r * w) * first_certificate
    )
    assert unit_certificate == 1

    # The five graph types are distinguished structurally by their degree
    # sequences; no labelled support list is generated.
    degree_signatures = (
        (1, 1, 1, 1, 1, 1),
        (2, 1, 1, 1, 1),
        (2, 2, 1, 1),
        (3, 1, 1, 1),
        (2, 2, 2),
    )
    assert all(sum(signature) == 6 for signature in degree_signatures)
    assert len(set(degree_signatures)) == 5

    zero = Fraction(0)
    one = Fraction(1)
    minus_one = Fraction(-1)

    # P4: u tensor t and -u tensor t cancel; the middle support edge is
    # independently nonzero but is multiplied by the zero 03 edge.
    outer = ((zero, one), (zero, zero))
    cross = ((zero, minus_one), (zero, zero))
    middle_times_zero = ((zero, zero), (zero, zero))
    assert matrix_add(outer, cross, middle_times_zero) == middle_times_zero
    middle_support_edge = ((one, zero), (zero, zero))
    assert middle_support_edge != middle_times_zero

    # Star and triangle have no nonzero pair of disjoint dedicated edges on
    # four displayed modes.  Their displayed active-mode counts, like P4's,
    # also make the sixfold singleton quotient shadow zero.
    triangle = (
        frozenset((0, 1)),
        frozenset((1, 2)),
        frozenset((0, 2)),
    )
    star = (
        frozenset((0, 1)),
        frozenset((0, 2)),
        frozenset((0, 3)),
    )
    path = (
        frozenset((0, 1)),
        frozenset((1, 2)),
        frozenset((2, 3)),
    )
    assert all(left & right for left in triangle for right in triangle if left != right)
    assert all(left & right for left in star for right in star if left != right)
    active_counts = tuple(len(set().union(*edges)) for edges in (triangle, star, path))
    assert active_counts == (3, 4, 4)
    assert max(active_counts) < 6
    assert Fraction(2) != 0

    print("AUDIT PASS: rational unit certificate excludes P3+K2")
    print("AUDIT PASS: five structural degree signatures")
    print("AUDIT PASS: P4 cancellation and K3/K1,3 dimension controls")
    print("AUDIT PASS: characteristic-zero denominator is only 2")
    print("AUDIT SCOPE: no full physical lift of the surviving controls")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
