#!/usr/bin/env python3
"""Independent dual-number audit of the disjoint-secant component."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


BITS = tuple(itertools.product((0, 1), repeat=4))


class Dual:
    def __init__(self, value=0, gradient=()):
        self.value = Fraction(value)
        self.gradient = tuple(Fraction(entry) for entry in gradient)

    @classmethod
    def variable(cls, value, index, size):
        gradient = [Fraction(0)] * size
        gradient[index] = Fraction(1)
        return cls(value, gradient)

    def _lift(self, other):
        if isinstance(other, Dual):
            return other
        return Dual(other, (Fraction(0),) * len(self.gradient))

    def __add__(self, other):
        other = self._lift(other)
        return Dual(self.value + other.value, tuple(a + b for a, b in zip(self.gradient, other.gradient)))

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other):
        return self + (-self._lift(other))

    def __rsub__(self, other):
        return self._lift(other) - self

    def __mul__(self, other):
        other = self._lift(other)
        return Dual(
            self.value * other.value,
            tuple(
                self.value * right + other.value * left
                for left, right in zip(self.gradient, other.gradient)
            ),
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._lift(other)
        return Dual(
            self.value / other.value,
            tuple(
                (left * other.value - self.value * right) / other.value**2
                for left, right in zip(self.gradient, other.gradient)
            ),
        )


def permanent_dp(rows):
    size = len(rows[0][0].gradient)
    state = {0: Dual(1, (0,) * size)}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, Dual(0, (0,) * size)) + value * entry
        state = following
    return state[(1 << 4) - 1]


def rank(matrix):
    work = [list(row) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    result = 0
    for column in range(columns):
        pivot = next((row for row in range(result, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        value = work[result][column]
        work[result] = [entry / value for entry in work[result]]
        for row in range(rows):
            if row == result or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right for left, right in zip(work[row], work[result])]
        result += 1
    return result


def determinant(matrix):
    work = [list(row) for row in matrix]
    result = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            factor = work[row][column] / value
            for inner in range(column, len(work)):
                work[row][inner] -= factor * work[column][inner]
    return sign * result


def main() -> None:
    # Family tangent from independently evaluated rational chart formulas.
    p = [Dual.variable(value, index, 6) for index, value in enumerate((1, 2, 3, 4, 5, 6))]
    s, t, lam, m, n, rho = p
    d2 = lam - m
    d3 = lam * n + rho + 1
    family_coordinates = [
        s, 0, 0, t,
        -s, 0, 0, -t,
        s * (-lam - m) / d2,
        2 * lam * m * t / d2,
        2 * s / d2,
        t * (-lam - m) / d2,
        s * (-lam * n - rho + 1) / d3,
        2 * lam * t / d3,
        -2 * n * s / d3,
        t * (-lam * n + rho + 1) / d3,
    ]
    family_jacobian = [
        list(value.gradient) if isinstance(value, Dual) else [Fraction(0)] * 6
        for value in family_coordinates
    ]
    assert rank(family_jacobian) == 6
    family_rows = [0, 3, 8, 9, 12, 14]
    family_minor = determinant([family_jacobian[row] for row in family_rows])
    assert family_minor == Fraction(48, 1331)

    # Universal pivot-02 incidence with 20 dual variables.
    sample = [
        1, 0, 0, 2,
        -1, 0, 0, -2,
        7, -48, -2, 14,
        Fraction(-10, 11), Fraction(6, 11),
        Fraction(-5, 11), Fraction(-8, 11),
        0, 0, Fraction(-1, 3), Fraction(9, 29),
    ]
    variables = [Dual.variable(value, index, 20) for index, value in enumerate(sample)]
    x = variables[:16]
    z = variables[16:]
    planes = []
    for mode in range(4):
        x0, x1, x2, x3 = x[4 * mode : 4 * mode + 4]
        planes.append(((Dual(1, (0,) * 20), x0, Dual(0, (0,) * 20), x1),
                       (Dual(0, (0,) * 20), x2, Dual(1, (0,) * 20), x3)))
    coefficients = {
        bits: permanent_dp(tuple(planes[mode][bits[mode]] for mode in range(4)))
        for bits in BITS
    }
    anchor = (1, 0, 0, 0)
    equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        target = Dual(1, (0,) * 20)
        for mode in range(4):
            if bits[mode] != anchor[mode]:
                target = target * z[mode]
        equation = coefficients[bits] - coefficients[anchor] * target
        assert equation.value == 0
        equations.append(list(equation.gradient))
    assert rank(equations) == 14
    incidence_rows = list(range(14))
    incidence_columns = list(range(12)) + [16, 17]
    incidence_minor = determinant(
        [[equations[row][column] for column in incidence_columns] for row in incidence_rows]
    )
    assert incidence_minor == Fraction(136141760102400, 19487171)

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "dual-number subset-DP incidence",
                "family_rank": 6,
                "family_minor": str(family_minor),
                "incidence_rank": 14,
                "incidence_minor": str(incidence_minor),
                "component_dimension": 6,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
