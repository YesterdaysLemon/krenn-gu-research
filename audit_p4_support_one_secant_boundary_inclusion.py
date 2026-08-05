#!/usr/bin/env python3
"""Independent rational-Laurent audit of the support-one secant arc."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))
BITS = tuple(itertools.product((0, 1), repeat=4))


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

    def _lift(self, other):
        return other if isinstance(other, Laurent) else Laurent.constant(other)

    def __add__(self, other):
        other = self._lift(other)
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
        return self + (-self._lift(other))

    def __rsub__(self, other):
        return self._lift(other) - self

    def __mul__(self, other):
        other = self._lift(other)
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

    def is_zero(self):
        return not self.terms


def lift(value):
    return value if isinstance(value, Laurent) else Laurent.constant(value)


def wedge(rows):
    return tuple(
        lift(rows[0][i]) * lift(rows[1][j])
        - lift(rows[0][j]) * lift(rows[1][i])
        for i, j in PAIRS
    )


def leading_vector(values):
    valuation = min(value.valuation() for value in values if not value.is_zero())
    return valuation, tuple(value.coefficient(valuation) for value in values)


def numeric_wedge(rows):
    return tuple(
        Fraction(rows[0][i]) * Fraction(rows[1][j])
        - Fraction(rows[0][j]) * Fraction(rows[1][i])
        for i, j in PAIRS
    )


def proportional(left, right):
    pivot = next(index for index, value in enumerate(right) if value)
    scale = left[pivot] / right[pivot]
    return all(l == scale * r for l, r in zip(left, right))


def permanent_dp(rows):
    state = {0: Laurent.constant(1)}
    for row in rows:
        following = {}
        for mask, value in state.items():
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                following[next_mask] = following.get(next_mask, Laurent()) + value * entry
        state = following
    return state[(1 << 4) - 1]


def product(left, right):
    return tuple(
        Fraction(left[i]) * Fraction(right[j])
        + Fraction(left[j]) * Fraction(right[i])
        for i, j in PAIRS
    )


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
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


def pair_rank(left, right):
    columns = [product(u, v) for u in left for v in right]
    return rank([list(row) for row in zip(*columns)])


def main() -> None:
    # Independent sample: (t,lambda,u,n,v)=(1,2,3,4,5).
    eps = Laurent({1: 1})
    e = (1, 0, 0, 0)
    a = (0, 1, 1, 0)
    a_bar = (0, 1, -1, 0)
    z = (0, 0, 0, 1)

    g_plus = tuple(lift(e[i]) + eps * z[i] for i in range(4))
    g_minus = tuple(lift(e[i]) - eps * z[i] for i in range(4))
    capital_l = eps
    capital_m = -3 * eps
    capital_n = Fraction(1, 4)
    rho = -1 + Fraction(5, 4) * eps

    add = lambda left, right: tuple(left[i] + right[i] for i in range(4))
    scale = lambda scalar, vector: tuple(scalar * vector[i] for i in range(4))
    arc = (
        (g_plus, a),
        (g_minus, a_bar),
        (add(g_minus, scale(capital_m, a)), add(g_plus, scale(capital_l, a_bar))),
        (
            add(a, scale(capital_n, g_minus)),
            add(add(g_plus, scale(-1 * capital_l, a_bar)), scale(rho, g_minus)),
        ),
    )

    arc_coefficients = {
        bits: permanent_dp(tuple(arc[mode][bits[mode]] for mode in range(4)))
        for bits in BITS
    }
    support = [bits for bits, value in arc_coefficients.items() if not value.is_zero()]
    assert support == [(1, 0, 0, 0), (1, 0, 0, 1)]

    limits = [leading_vector(wedge(plane)) for plane in arc]
    assert [valuation for valuation, _ in limits] == [0, 0, 1, 1]

    target = (
        (e, a),
        (e, a_bar),
        (e, (0, 4, 2, 2)),
        ((1, 4, 4, 0), (0, 6, 4, -2)),
    )
    target_wedges = [numeric_wedge(plane) for plane in target]
    assert all(
        proportional(leading, expected)
        for (_, leading), expected in zip(limits, target_wedges)
    )

    profile = [
        pair_rank(target[i], target[j])
        for i, j in itertools.combinations(range(4), 2)
    ]
    assert profile == [2, 3, 4, 3, 4, 4]

    singleton = ((e, (0, 1, 0, 0)), (e, (0, 1, 0, 0)))
    overlap = ((e, (1, 1, 0, 0)), (e, (1, -1, 0, 0)))
    assert pair_rank(*singleton) == 1
    assert pair_rank(*overlap) == 1

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "rational Laurent wedges plus subset-DP permanent",
                "arc_support": ["".join(map(str, bits)) for bits in support],
                "pluecker_valuations": [valuation for valuation, _ in limits],
                "target_planes_recovered": True,
                "pair_profile": profile,
                "support_overlap_rank_drop": True,
                "limit_component": 15,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
