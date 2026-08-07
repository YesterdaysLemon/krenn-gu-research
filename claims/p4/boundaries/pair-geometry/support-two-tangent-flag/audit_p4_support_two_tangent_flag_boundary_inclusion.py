#!/usr/bin/env python3
"""Independent Laurent audit of the support-two polar-flag arc."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))


class Laurent:
    def __init__(self, terms=None):
        self.terms = {
            int(power): Fraction(value)
            for power, value in (terms or {}).items()
            if value
        }

    @classmethod
    def constant(cls, value):
        return cls({0: Fraction(value)})

    def __add__(self, other):
        other = other if isinstance(other, Laurent) else Laurent.constant(other)
        result = dict(self.terms)
        for power, value in other.terms.items():
            result[power] = result.get(power, Fraction(0)) + value
            if not result[power]:
                del result[power]
        return Laurent(result)

    __radd__ = __add__

    def __neg__(self):
        return Laurent({power: -value for power, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return Laurent.constant(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Laurent) else Laurent.constant(other)
        result = {}
        for left_power, left_value in self.terms.items():
            for right_power, right_value in other.terms.items():
                power = left_power + right_power
                result[power] = result.get(power, Fraction(0)) + left_value * right_value
        return Laurent(result)

    __rmul__ = __mul__

    def valuation(self):
        return min(self.terms) if self.terms else None

    def coefficient(self, power):
        return self.terms.get(power, Fraction(0))


def wedge(rows):
    def lift(value):
        return value if isinstance(value, Laurent) else Laurent.constant(value)

    return tuple(
        lift(rows[0][i]) * lift(rows[1][j])
        - lift(rows[0][j]) * lift(rows[1][i])
        for i, j in PAIRS
    )


def leading_vector(values):
    valuation = min(value.valuation() for value in values if value.terms)
    return valuation, tuple(value.coefficient(valuation) for value in values)


def numeric_wedge(rows):
    return tuple(
        rows[0][i] * rows[1][j] - rows[0][j] * rows[1][i]
        for i, j in PAIRS
    )


def proportional(left, right):
    pivot = next(index for index, value in enumerate(right) if value)
    scale = left[pivot] / right[pivot]
    return all(l == scale * r for l, r in zip(left, right))


def main() -> None:
    eps = Laurent({1: 1})
    inv = Laurent({-1: 1})
    b = Fraction(1, 2) * eps - Fraction(1, 2) * eps * eps
    e1 = Fraction(1, 2) * eps
    h = 2 * inv + 3
    total_s = 2 * inv + 6

    v0 = ((eps, 0, 0, -1), (0, 0, eps, 1))
    v3 = ((eps, 0, 0, 1), (0, 0, eps, -1))
    v1 = (
        (eps, b, 0, 1 - b * h),
        (0, e1, eps, 1 - e1 * h),
    )
    v2 = (
        (eps, 0, -eps, 0),
        (0, 1, -total_s * eps, -3),
    )

    limits = [leading_vector(wedge(plane)) for plane in (v0, v3, v1, v2)]
    assert [valuation for valuation, _ in limits] == [1, 1, 2, 1]

    tangent = numeric_wedge(((0, 0, 0, 1), (1, 0, 1, 0)))
    target_a = numeric_wedge(((1, 0, -1, 1), (3, 1, -1, 0)))
    target_b = numeric_wedge(((1, 0, -1, 0), (1, -1, 1, 3)))
    targets = (tangent, tangent, target_a, target_b)
    assert all(
        proportional(limit, target)
        for (_, limit), target in zip(limits, targets)
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "exact rational Laurent wedges",
                "pluecker_valuations": [valuation for valuation, _ in limits],
                "tangent_planes_coalesce": True,
                "polar_flag_planes_recovered": True,
                "limit_component": "known six-dimensional lower-pair component",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
