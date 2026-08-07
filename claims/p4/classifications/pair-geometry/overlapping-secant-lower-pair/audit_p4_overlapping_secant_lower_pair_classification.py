#!/usr/bin/env python3
"""Independent dual-number audit of the overlapping-secant sixfold chart."""

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
        return other if isinstance(other, Dual) else Dual(other, (0,) * len(self.gradient))

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
            tuple(self.value * right + other.value * left for left, right in zip(self.gradient, other.gradient)),
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
    result = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(result, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        value = work[result][column]
        work[result] = [entry / value for entry in work[result]]
        for row in range(len(work)):
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


def rref(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [left - factor * right for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return work


def main() -> None:
    # Family chart derivatives at the common point.
    p = [Dual.variable(value, index, 6) for index, value in enumerate((1, 1, -2, 7, -1, 3))]
    s, t, lam, u, n, v = p
    denominator = -2 * n + v + 1
    coordinates = [
        t, 0, -t / s, 0,
        -t, 0, -t / s, 0,
        t * (u - 1) / (u + 1), lam / (u + 1), t / s, 0,
        t * (v - 1) / denominator,
        lam * (n - 1) / denominator,
        t * (v + 1) / (s * denominator),
        lam * n / (s * denominator),
    ]
    family_jacobian = [
        list(value.gradient) if isinstance(value, Dual) else [Fraction(0)] * 6
        for value in coordinates
    ]
    family_rows = [0, 2, 8, 9, 12, 14]
    family_minor = determinant([family_jacobian[row] for row in family_rows])
    assert family_minor == Fraction(-1, 13824)
    assert rank(family_jacobian) == 6

    sample = [
        1, 0, -1, 0,
        -1, 0, -1, 0,
        Fraction(3, 4), Fraction(-1, 4), 1, 0,
        Fraction(1, 3), Fraction(2, 3), Fraction(2, 3), Fraction(1, 3),
        -1, 0, 0, Fraction(4, 5),
    ]
    variables = [Dual.variable(value, index, 20) for index, value in enumerate(sample)]
    x = variables[:16]
    target = variables[16:]
    planes = []
    for mode in range(4):
        x0, x1, x2, x3 = x[4 * mode : 4 * mode + 4]
        planes.append(((Dual(1, (0,) * 20), Dual(0, (0,) * 20), x0, x1),
                       (Dual(0, (0,) * 20), Dual(1, (0,) * 20), x2, x3)))
    coefficients = {
        bits: permanent_dp(tuple(planes[mode][bits[mode]] for mode in range(4)))
        for bits in BITS
    }
    anchor = (0, 1, 0, 0)
    equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        monomial = Dual(1, (0,) * 20)
        for mode in range(4):
            if bits[mode] != anchor[mode]:
                monomial = monomial * target[mode]
        equation = coefficients[bits] - coefficients[anchor] * monomial
        assert equation.value == 0
        equations.append(list(equation.gradient))
    assert rank(equations) == 14
    columns = list(range(12)) + [17, 18]
    incidence_minor = determinant([[equations[row][column] for column in columns] for row in range(14)])
    assert incidence_minor == Fraction(280, 729)

    # Independently replay the common row spaces.
    old = [
        [[1, 0, 0, -1], [0, 0, 1, 1]],
        [[1, 1, 0, 2], [0, 2, 1, 3]],
        [[1, 0, -1, 0], [0, 1, -3, -4]],
        [[1, 0, 0, 1], [0, 0, 1, -1]],
    ]
    transformed = []
    for index in (0, 3, 2, 1):
        transformed.append([[row[3], -row[0], row[2], row[1]] for row in old[index]])
    current = [
        [[1, 1, 0, 0], [1, 0, 1, 0]],
        [[1, -1, 0, 0], [1, 0, -1, 0]],
        [[0, 1, 1, 0], [8, -6, 0, -2]],
        [[-1, 2, 1, 0], [4, -2, 0, 2]],
    ]
    assert all(rref(left) == rref(right) for left, right in zip(transformed, current))

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "dual-number subset-DP plus common-point row spaces",
                "family_rank": 6,
                "family_minor": str(family_minor),
                "incidence_rank": 14,
                "incidence_minor": str(incidence_minor),
                "common_point_identified": True,
                "new_component": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
