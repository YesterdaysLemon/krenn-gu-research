#!/usr/bin/env python3
"""Independent exact audit of the common-kernel YX obstruction."""

from __future__ import annotations

import json
from fractions import Fraction


MASKS2 = (12, 10, 6, 9, 5, 3)


def product(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    values: list[Fraction] = []
    for mask in MASKS2:
        indices = [index for index in range(4) if mask & (1 << index)]
        i, j = indices
        values.append(left[i] * right[j] + left[j] * right[i])
    return tuple(values)


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
                left - factor * right
                for left, right in zip(matrix[row], matrix[result])
            ]
        result += 1
    return result


def permute(row: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    order = (2, 0, 3, 1)
    return tuple(row[index] for index in order)


def audit_branch(
    b: tuple[Fraction, ...], d: tuple[Fraction, ...]
) -> dict[str, object]:
    a = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    assert product(b, d) == product(a, a)
    pa, pb, pd = map(permute, (a, b, d))
    columns = [
        product(pa, pd),
        product(pa, pa),
        product(pb, pd),
        product(pb, pa),
    ]
    image_rank = rank(columns)
    assert image_rank <= 2
    return {
        "b": [str(value) for value in b],
        "d": [str(value) for value in d],
        "pair_image_rank": image_rank,
        "relation_dimension_at_least": 4 - image_rank,
    }


def main() -> None:
    results = [
        # Delta != 0: rigid binary branch.
        audit_branch(
            (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(2), Fraction(0), Fraction(0)),
        ),
        # Delta = 0: the two reflected coordinate-ray branches.
        audit_branch(
            (Fraction(2), Fraction(1), Fraction(3), Fraction(0)),
            (Fraction(1), Fraction(1, 2), Fraction(-3, 2), Fraction(0)),
        ),
        audit_branch(
            (Fraction(3), Fraction(2), Fraction(0), Fraction(5)),
            (Fraction(1, 2), Fraction(1, 3), Fraction(0), Fraction(-5, 6)),
        ),
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "permuted exact rational branch representatives",
                "branches": results,
                "rank_three_pair": False,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
