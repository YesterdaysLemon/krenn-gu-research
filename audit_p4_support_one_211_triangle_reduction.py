#!/usr/bin/env python3
"""Independent exact audit of the support-one triangle reduction."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction


PAIRS = tuple(itertools.combinations(range(4), 2))


def product(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(
        left[i] * right[j] + left[j] * right[i] for i, j in PAIRS
    )


def rank(columns: list[tuple[Fraction, ...]]) -> int:
    matrix = [[columns[column][row] for column in range(len(columns))] for row in range(6)]
    result = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(result, 6) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[result], matrix[pivot] = matrix[pivot], matrix[result]
        pivot_value = matrix[result][column]
        matrix[result] = [entry / pivot_value for entry in matrix[result]]
        for row in range(6):
            if row == result or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right for left, right in zip(matrix[row], matrix[result])
            ]
        result += 1
    return result


def pair_rank(left, right) -> int:
    return rank([product(u, v) for u in left for v in right])


def permute(row: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    order = (2, 0, 3, 1)
    return tuple(row[index] for index in order)


def main() -> None:
    e0 = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    e1 = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    P = (Fraction(2), Fraction(3), Fraction(0), Fraction(0))
    s = (Fraction(0), Fraction(0), Fraction(5), Fraction(0))
    lam = Fraction(1, 12)
    p = tuple(P[index] + s[index] for index in range(4))
    q = tuple(lam * (P[index] - s[index]) for index in range(4))
    assert product(p, q) == product(e0, e1)

    triangle = ((p, e0), (e1, q), (e0, e1))
    permuted = tuple(tuple(permute(row) for row in plane) for plane in triangle)
    pair_ranks = [
        pair_rank(permuted[i], permuted[j])
        for i, j in itertools.combinations(range(3), 2)
    ]
    assert pair_ranks == [3, 3, 3]

    mixed_p = tuple(map(Fraction, (1, 1, 2, 0)))
    mixed_q = (
        Fraction(1, 4),
        Fraction(3, 4),
        Fraction(-3, 2),
        Fraction(0),
    )
    mixed_y2 = tuple(map(Fraction, (0, 1, -1, 0)))
    mixed_x3 = tuple(map(Fraction, (0, 1, 1, 0)))
    assert product(mixed_p, mixed_q) == product(e0, mixed_y2)
    mixed_triangle = ((mixed_p, e0), (mixed_y2, mixed_q), (e0, mixed_x3))
    mixed_pair_ranks = [
        pair_rank(mixed_triangle[i], mixed_triangle[j])
        for i, j in itertools.combinations(range(3), 2)
    ]
    assert mixed_pair_ranks == [3, 3, 3]

    common_yy = ((e0, (Fraction(1), Fraction(2), Fraction(3), Fraction(4))),
                 (e0, (Fraction(3), Fraction(2), Fraction(3), Fraction(4))))
    assert pair_rank(*common_yy) <= 2

    used_coordinates = {
        index
        for plane in triangle
        for row in plane
        for index, value in enumerate(row)
        if value
    }
    assert used_coordinates == {0, 1, 2}

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "source-permuted exact rational reflection branch",
                "reflected_pair_ranks": pair_ranks,
                "mixed_two_edge_star_pair_ranks": mixed_pair_ranks,
                "common_factor_pair_rank_at_most": 2,
                "triangle_coordinate_support": sorted(used_coordinates),
                "embedded_P3": True,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
