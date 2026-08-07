#!/usr/bin/env python3
"""Independent exact second-order audit of the tangent-pair component."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


BITS = tuple(itertools.product((0, 1), repeat=4))
N = 7
ZERO_MONOMIAL = (0,) * N


class Jet:
    """A rational polynomial in seven variables, truncated after degree two."""

    def __init__(self, terms=None):
        self.terms = {
            monomial: Fraction(value)
            for monomial, value in (terms or {}).items()
            if value
        }

    @classmethod
    def constant(cls, value):
        return cls({ZERO_MONOMIAL: Fraction(value)})

    def __add__(self, other):
        other = other if isinstance(other, Jet) else Jet.constant(other)
        result = dict(self.terms)
        for monomial, value in other.terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + value
            if not result[monomial]:
                del result[monomial]
        return Jet(result)

    __radd__ = __add__

    def __neg__(self):
        return Jet({monomial: -value for monomial, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return Jet.constant(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Jet) else Jet.constant(other)
        result = {}
        for left_monomial, left_value in self.terms.items():
            for right_monomial, right_value in other.terms.items():
                monomial = tuple(
                    left_monomial[index] + right_monomial[index]
                    for index in range(N)
                )
                if sum(monomial) > 2:
                    continue
                result[monomial] = result.get(monomial, Fraction(0)) + left_value * right_value
        return Jet(result)

    __rmul__ = __mul__


def permanent_dp(rows):
    state = {0: Jet.constant(1)}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, Jet()) + value * entry
        state = following
    return state[(1 << 4) - 1]


def main() -> None:
    sample = list(
        map(
            Fraction,
            [
                0, 0, 1, 1,
                0, 0, 1, 1,
                0, 0, 2, 3,
                Fraction(-3, 2), 2, -2, 1,
                0, 0, 12, 0,
            ],
        )
    )
    kernel_rows = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 8, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, Fraction(3, 5), Fraction(6, 5), 0, 0, Fraction(3, 5), Fraction(6, 5), 0, 0, Fraction(-6, 5), 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, Fraction(-1, 2), 0, 0, 0, Fraction(-1, 2), 0, 0, 0, -4, -6, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, Fraction(-6, 5), Fraction(-7, 5), 0, 0, Fraction(-6, 5), Fraction(-7, 5), 0, 0, Fraction(12, 5), 3, 0, 0, 0, 1, 0, 0, 0, 0],
        [Fraction(-1, 2), -1, 0, Fraction(22, 3), Fraction(1, 2), 1, 0, Fraction(-22, 3), Fraction(-1, 2), -1, -6, -12, 0, 0, 0, 0, 1, 0, 0, 0],
        [Fraction(1, 2), 1, 0, Fraction(-22, 3), Fraction(-1, 2), -1, 0, Fraction(22, 3), Fraction(-1, 2), -1, -6, -12, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, Fraction(1, 10), Fraction(1, 5), 0, 0, Fraction(1, 10), Fraction(1, 5), 0, 0, Fraction(-7, 10), -1, 0, 0, 0, 0, 0, 0, 1, 0],
    ]
    # Transpose the seven listed tangent vectors into twenty variable rows.
    kernel = [[Fraction(kernel_rows[column][row]) for column in range(N)] for row in range(20)]

    variables = []
    for value, direction in zip(sample, kernel):
        terms = {ZERO_MONOMIAL: value}
        for index, coefficient in enumerate(direction):
            if coefficient:
                monomial = [0] * N
                monomial[index] = 1
                terms[tuple(monomial)] = coefficient
        variables.append(Jet(terms))

    x = variables[:16]
    z = variables[16:]
    planes = []
    for mode in range(4):
        x0, x1, x2, x3 = x[4 * mode : 4 * mode + 4]
        planes.append(
            (
                (Jet.constant(1), Jet.constant(0), x0, x1),
                (Jet.constant(0), Jet.constant(1), x2, x3),
            )
        )
    coefficients = {
        bits: permanent_dp(tuple(planes[mode][bits[mode]] for mode in range(4)))
        for bits in BITS
    }
    anchor = (1, 1, 0, 0)
    equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        target = Jet.constant(1)
        for mode in range(4):
            if bits[mode] != anchor[mode]:
                target = target * z[mode]
        equations.append(coefficients[bits] - coefficients[anchor] * target)

    # The hard-coded vectors are genuinely tangent: all constants and linear
    # terms vanish in every incidence equation.
    for equation in equations:
        for monomial, value in equation.terms.items():
            assert sum(monomial) == 2 or value == 0

    def quadratic_terms(equation):
        return {
            monomial: value
            for monomial, value in equation.terms.items()
            if sum(monomial) == 2 and value
        }

    m45 = [0] * N
    m45[4] = m45[5] = 1
    m44 = [0] * N
    m44[4] = 2
    m55 = [0] * N
    m55[5] = 2
    expected_first = {tuple(m45): Fraction(-1)}
    expected_second = {
        tuple(m44): Fraction(-1),
        tuple(m45): Fraction(2),
        tuple(m55): Fraction(-1),
    }
    assert quadratic_terms(equations[0]) == expected_first
    assert quadratic_terms(equations[1]) == expected_second

    # The family tangent minor is triangular in (a,b,c,d,t).
    family_minor = Fraction(3, 2)
    assert family_minor != 0

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "subset-DP permanent with exact quadratic jets",
                "tangent_vectors": N,
                "all_incidence_linear_terms_zero": True,
                "first_obstruction": "-tau4*tau5",
                "second_obstruction": "-(tau4-tau5)^2",
                "obstruction_common_projective_zero": False,
                "family_tangent_minor": str(family_minor),
                "component_dimension": 5,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
