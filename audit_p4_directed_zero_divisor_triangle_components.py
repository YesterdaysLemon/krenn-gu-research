#!/usr/bin/env python3
"""Independent exact audit of the two directed-triangle components."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PRIME = 101
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = {
    "star": ((0, 1), (1, 2), (0, 1), (0, 2)),
    "path": ((0, 1), (0, 2), (0, 1), (0, 2)),
}


class Dual:
    def __init__(self, value, gradient):
        self.value = int(value) % PRIME
        self.gradient = tuple(int(entry) % PRIME for entry in gradient)

    @classmethod
    def constant(cls, value, size):
        return cls(value, (0,) * size)

    def __add__(self, other):
        if not isinstance(other, Dual):
            other = Dual.constant(other, len(self.gradient))
        return Dual(
            self.value + other.value,
            tuple(a + b for a, b in zip(self.gradient, other.gradient, strict=True)),
        )

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, tuple(-entry for entry in self.gradient))

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __mul__(self, other):
        if not isinstance(other, Dual):
            other = Dual.constant(other, len(self.gradient))
        return Dual(
            self.value * other.value,
            tuple(
                self.value * right + other.value * left
                for left, right in zip(self.gradient, other.gradient, strict=True)
            ),
        )

    __rmul__ = __mul__

    def inverse(self):
        inverse_value = pow(self.value, -1, PRIME)
        return Dual(
            inverse_value,
            tuple(-entry * inverse_value * inverse_value for entry in self.gradient),
        )

    def __truediv__(self, other):
        if not isinstance(other, Dual):
            other = Dual.constant(other, len(self.gradient))
        return self * other.inverse()


def seed(value, index, size):
    gradient = [0] * size
    gradient[index] = 1
    return Dual(value, gradient)


def permanent_dp(rows):
    sample = rows[0][0]
    if isinstance(sample, Dual):
        one = Dual.constant(1, len(sample.gradient))
        zero = Dual.constant(0, len(sample.gradient))
    else:
        one = Fraction(1)
        zero = Fraction(0)
    state = {0: one}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, zero) + value * entry
        state = following
    return state[15]


def rank_fraction(matrix):
    work = [[Fraction(entry) for entry in row] for row in matrix]
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
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[result], strict=True)
            ]
        result += 1
    return result


def rank_mod(matrix):
    work = [[int(entry) % PRIME for entry in row] for row in matrix]
    result = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(result, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        inverse = pow(work[result][column], -1, PRIME)
        work[result] = [entry * inverse % PRIME for entry in work[result]]
        for row in range(len(work)):
            if row == result or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % PRIME
                for left, right in zip(work[row], work[result], strict=True)
            ]
        result += 1
    return result


def raw_family(kind, u, v):
    if kind == "star":
        return (
            ((1 - u, 1, 0, u), (1 - v, 0, 1, v)),
            ((0, 1, 1, 0), (0, 0, 1, 1)),
            ((1, 0, -1, 0), (0, 1, -1, 0)),
            ((0, 0, 1, -1), (1, 0, 1, 0)),
        )
    if kind == "path":
        return (
            ((-1 - u, 1, 0, u), (1 - v, 0, 1, v)),
            ((1, 1, 0, 0), (0, 0, 1, 1)),
            ((1, 0, -1, 0), (1, -1, 0, 0)),
            ((0, 0, 1, -1), (1, 0, 1, 0)),
        )
    raise ValueError(kind)


def pair_rank(left, right):
    columns = []
    for first in left:
        for second in right:
            columns.append(
                tuple(
                    first[i] * second[j] + first[j] * second[i]
                    for i, j in PAIRS
                )
            )
    return rank_fraction([list(row) for row in zip(*columns, strict=True)])


def reduce_plane(plane, pivot):
    a = plane[0][pivot[0]]
    b = plane[0][pivot[1]]
    c = plane[1][pivot[0]]
    d = plane[1][pivot[1]]
    determinant = a * d - b * c
    inverse = ((d / determinant, -b / determinant), (-c / determinant, a / determinant))
    return tuple(
        tuple(inverse[row][0] * plane[0][column] + inverse[row][1] * plane[1][column] for column in range(4))
        for row in range(2)
    )


def family_tangent(kind):
    size = 5
    u, v, t_0, t_1, t_2 = (
        seed(2, 0, size),
        seed(3, 1, size),
        seed(1, 2, size),
        seed(1, 3, size),
        seed(1, 4, size),
    )
    scales = (t_0, t_1, t_2, Dual.constant(1, size))
    planes = raw_family(kind, u, v)
    scaled = tuple(
        tuple(
            tuple(entry * scales[column] for column, entry in enumerate(row))
            for row in plane
        )
        for plane in planes
    )
    coordinates = []
    values = []
    for plane, pivot in zip(scaled, PIVOTS[kind], strict=True):
        reduced = reduce_plane(plane, pivot)
        nonpivots = tuple(index for index in range(4) if index not in pivot)
        for row in range(2):
            for column in nonpivots:
                coordinates.append(reduced[row][column].gradient)
                values.append(reduced[row][column].value)
    assert rank_mod(coordinates) == 5
    return values


def chart_planes(variables, pivots):
    result = []
    for mode, pivot in enumerate(pivots):
        plane = [[None] * 4 for _ in range(2)]
        zero = Dual.constant(0, len(variables[0].gradient))
        one = Dual.constant(1, len(variables[0].gradient))
        for row in range(2):
            for column in range(4):
                plane[row][column] = zero
        plane[0][pivot[0]] = one
        plane[1][pivot[1]] = one
        nonpivots = tuple(index for index in range(4) if index not in pivot)
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row][column] = entries[2 * row + offset]
        result.append(tuple(tuple(row) for row in plane))
    return tuple(result)


def incidence_rank(kind, coordinate_values):
    size = 20
    variables = tuple(seed(value, index, size) for index, value in enumerate(coordinate_values))
    expected_ratios = {
        "star": (1, -1, 0, 0),
        "path": (5, 0, 0, 0),
    }[kind]
    z = tuple(seed(value, 16 + index, size) for index, value in enumerate(expected_ratios))
    planes = chart_planes(variables, PIVOTS[kind])
    tensor = {
        word: permanent_dp(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS
    }
    anchor = {"star": (0, 0, 1, 0), "path": (0, 1, 1, 0)}[kind]
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        target = Dual.constant(1, size)
        for mode in range(4):
            if word[mode] != anchor[mode]:
                target = target * z[mode]
        equation = tensor[word] - tensor[anchor] * target
        assert equation.value == 0
        equations.append(equation.gradient)
    return rank_mod(equations)


def rational_sample(kind):
    planes = tuple(
        tuple(tuple(Fraction(entry) for entry in row) for row in plane)
        for plane in raw_family(kind, Fraction(2), Fraction(3))
    )
    tensor = {
        word: permanent_dp(tuple(planes[mode][word[mode]] for mode in range(4)))
        for word in WORDS
    }
    expected = {
        "star": {(1, 1, 1, 1): Fraction(2)},
        "path": {(0, 1, 1, 1): Fraction(2), (1, 1, 1, 1): Fraction(-2)},
    }[kind]
    assert {word: value for word, value in tensor.items() if value} == expected
    profile = tuple(pair_rank(planes[left], planes[right]) for left, right in PAIRS)
    assert profile == (4, 4, 4, 3, 3, 3)
    return profile


def main():
    results = {}
    for kind in ("star", "path"):
        profile = rational_sample(kind)
        coordinate_values = family_tangent(kind)
        universal_rank = incidence_rank(kind, coordinate_values)
        assert universal_rank == 15
        results[kind] = {
            "pair_profile": profile,
            "family_tangent_rank_mod_101": 5,
            "incidence_rank_mod_101": universal_rank,
        }

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent rational permanent and finite-field dual Jacobians",
                "components": results,
                "support_degree_sequences": {
                    "star": (3, 1, 1, 1),
                    "path": (2, 2, 1, 1),
                },
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
