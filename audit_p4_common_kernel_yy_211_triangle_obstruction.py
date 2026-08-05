#!/usr/bin/env python3
"""Independent exact audit of the common-kernel YY triangle obstruction."""

from __future__ import annotations

import json
from fractions import Fraction


MASKS3 = (7, 11, 13, 14)


def multiply(left: dict[int, Fraction], right: dict[int, Fraction]) -> dict[int, Fraction]:
    result: dict[int, Fraction] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, Fraction(0)) + left_value * right_value
    return result


def covector(*rows: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    value = {0: Fraction(1)}
    for row in rows:
        value = multiply(
            value,
            {1 << index: entry for index, entry in enumerate(row) if entry},
        )
    return tuple(value.get(mask, Fraction(0)) for mask in MASKS3)


def add(*rows: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(row[index] for row in rows) for index in range(4))


def scale(value: Fraction, row: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(value * entry for entry in row)


def rank(columns: list[tuple[Fraction, ...]]) -> int:
    matrix = [[columns[column][row] for column in range(len(columns))] for row in range(4)]
    result = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(result, 4) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[result], matrix[pivot] = matrix[pivot], matrix[result]
        pivot_value = matrix[result][column]
        matrix[result] = [entry / pivot_value for entry in matrix[result]]
        for row in range(4):
            if row == result or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                left - factor * right for left, right in zip(matrix[row], matrix[result])
            ]
        result += 1
    return result


def audit_point(beta: int, r: int, u: int, v: int, p: int, delta: int) -> dict[str, object]:
    # Source order (3,1,0,2) is unrelated to the primary verifier's order.
    order = (3, 1, 0, 2)
    a0 = (Fraction(1), Fraction(1), Fraction(0), Fraction(0))
    c0 = (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))
    s0 = (Fraction(0), Fraction(0), Fraction(u), Fraction(v))
    q = Fraction(-v * p, u)
    t0 = (Fraction(0), Fraction(0), Fraction(p), q)
    m0 = add(scale(Fraction(beta), c0), s0)
    mr0 = add(m0, scale(Fraction(r), c0))
    d0 = add(scale(Fraction(delta), c0), t0)

    def permute(row: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(row[index] for index in order)

    a, c, m, mr, d = map(permute, (a0, c0, m0, mr0, d0))
    C0 = covector(a, a, d)
    C1 = covector(a, m, d)
    C2 = covector(m, mr, c)
    active = covector(m, mr, d)
    expected = tuple(
        Fraction(delta) * C2[index]
        - Fraction(beta * (beta + r)) * C0[index]
        for index in range(4)
    )
    assert C1 == (0, 0, 0, 0)
    assert active == expected
    assert rank([C0, C2]) == 2
    assert rank([C0, C2, active]) == 2
    return {
        "parameters": [beta, r, u, v, p, delta],
        "forced_q": str(q),
        "kernel_rich_rank": 2,
        "rank_after_active": 2,
    }


def main() -> None:
    results = [
        audit_point(1, 2, 2, 3, 5, 7),
        audit_point(2, -1, 3, 4, 2, -3),
    ]
    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent permuted squarefree subset product",
                "points": results,
                "active_cubic_in_kernel_rich_span": True,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
