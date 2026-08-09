#!/usr/bin/env python3
"""Independent brute-force audit of the permanent block selector.

This audit imports nothing from the primary verifier.  It evaluates explicit
complementary permanents over the integers for d=2 and over the exact
Eisenstein field Q(omega) for d=3.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass


def integer_permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    size = len(matrix)
    return sum(
        math.prod(matrix[row][sigma[row]] for row in range(size))
        for sigma in itertools.permutations(range(size))
    )


@dataclass(frozen=True)
class Eisenstein:
    """The exact number a + b*omega with omega^2 + omega + 1 = 0."""

    a: int
    b: int = 0

    def __add__(self, other: Eisenstein) -> Eisenstein:
        return Eisenstein(self.a + other.a, self.b + other.b)

    def __mul__(self, other: Eisenstein) -> Eisenstein:
        return Eisenstein(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    def scale(self, scalar: int) -> Eisenstein:
        return Eisenstein(scalar * self.a, scalar * self.b)


ZERO = Eisenstein(0)
ONE = Eisenstein(1)
OMEGA = Eisenstein(0, 1)


def eisenstein_permanent(
    matrix: tuple[tuple[Eisenstein, ...], ...],
) -> Eisenstein:
    size = len(matrix)
    total = ZERO
    for sigma in itertools.permutations(range(size)):
        term = ONE
        for row in range(size):
            term = term * matrix[row][sigma[row]]
        total = total + term
    return total


def d2_columns(blocks: int) -> tuple[tuple[int, ...], ...]:
    """Explicit U columns for t=d=2 and zeta=-1."""

    rows = 2 * blocks
    columns = []
    for h in range(1, blocks):
        for root in (1, -1):
            column = []
            for row in range(rows):
                block = row // 2
                if block < h:
                    column.append(1)
                elif block == h:
                    column.append(2 * root)
                else:
                    column.append(0)
            columns.append(tuple(column))
    return tuple(columns)


def audit_d2_three_blocks() -> dict[str, object]:
    blocks = 3
    rows = 6
    columns = d2_columns(blocks)
    theta = -4
    lambdas = (theta**2, theta, 1 + theta)
    expected_nonzero = {
        tuple(range(2 * block, 2 * block + 2)): 4 * lambdas[block]
        for block in range(blocks)
    }

    observed_nonzero = {}
    for omitted in itertools.combinations(range(rows), 2):
        retained = tuple(row for row in range(rows) if row not in omitted)
        matrix = tuple(
            tuple(columns[column][row] for column in range(len(columns)))
            for row in retained
        )
        value = integer_permanent(matrix)
        if value:
            observed_nonzero[omitted] = value

    assert observed_nonzero == expected_nonzero
    return {
        "field": "Q",
        "blocks": blocks,
        "nonzero_complements": {
            str(key): value for key, value in observed_nonzero.items()
        },
    }


def audit_d3_two_blocks() -> dict[str, object]:
    roots = (ONE, OMEGA, OMEGA * OMEGA)
    columns = []
    for root in roots:
        columns.append(
            tuple([ONE] * 3 + [root.scale(2)] * 3)
        )

    observed_nonzero = {}
    for omitted in itertools.combinations(range(6), 3):
        retained = tuple(row for row in range(6) if row not in omitted)
        matrix = tuple(
            tuple(columns[column][row] for column in range(3))
            for row in retained
        )
        value = eisenstein_permanent(matrix)
        if value != ZERO:
            observed_nonzero[omitted] = value

    assert observed_nonzero == {
        (0, 1, 2): Eisenstein(48),
        (3, 4, 5): Eisenstein(6),
    }
    return {
        "field": "Q(omega)",
        "relation": "omega^2+omega+1=0",
        "nonzero_complements": {
            str(key): [value.a, value.b]
            for key, value in observed_nonzero.items()
        },
    }


def audit_micro_selector_numerically() -> int:
    variable_rows = (
        (3, 5),
        (7, 11),
        (13, 17),
        (19, 23),
    )
    matrix = tuple(
        variable_rows[row] + ((1, 1) if row < 2 else (2, -2))
        for row in range(4)
    )
    observed = integer_permanent(matrix)
    expected = -8 * (3 * 11 + 5 * 7) + 2 * (13 * 23 + 17 * 19)
    assert observed == expected
    return observed


def main() -> None:
    print(
        json.dumps(
            {
                "status": "verified",
                "method": "independent complementary-permanent enumeration",
                "micro_selector_value": audit_micro_selector_numerically(),
                "audits": [audit_d2_three_blocks(), audit_d3_two_blocks()],
                "mixed_complements_nonzero": False,
                "global_krenn_gu_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
