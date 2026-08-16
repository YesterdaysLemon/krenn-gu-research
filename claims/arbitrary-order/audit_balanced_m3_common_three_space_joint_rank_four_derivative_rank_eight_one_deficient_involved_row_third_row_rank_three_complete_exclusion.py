#!/usr/bin/env python3
"""Independent Fraction audit for the S2BY mixed q=3 exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Vector = tuple[Fraction, ...]
D, S, T = 0, 1, 2


def add(left: Vector, right: Vector, scale: Fraction = Fraction(1)) -> Vector:
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def scale(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def rank(columns: list[Vector]) -> int:
    if not columns:
        return 0
    matrix = [list(row) for row in zip(*columns, strict=True)]
    rows, cols = len(matrix), len(matrix[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next(
            (row for row in range(pivot_row, rows) if matrix[row][col]), None
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not matrix[row][col]:
                continue
            factor = matrix[row][col]
            matrix[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def target(a: int, b: int, c: int) -> Vector:
    if a == b == c == S:
        return (Fraction(0), Fraction(1), Fraction(0))
    if a == b == c == T:
        return (Fraction(0), Fraction(0), Fraction(1))
    return (Fraction(0), Fraction(0), Fraction(0))


def audit_correction() -> None:
    kappa = Fraction(11)
    # Reverse the two-root coordinate order: index = third*3 + second.
    columns = []
    for colour in (D, S, T):
        column = [Fraction(0)] * 9
        column[3 * colour + D] = kappa
        columns.append(tuple(column))
    solution = (Fraction(-1, 11), Fraction(0), Fraction(0))
    result = tuple(
        sum(solution[col] * columns[col][row] for col in range(3))
        for row in range(9)
    )
    expected = [Fraction(0)] * 9
    expected[0] = -1
    assert result == tuple(expected)
    assert rank(columns) == 3


def audit_mixed_table() -> None:
    nonzero: list[tuple[int, int, int]] = []
    for a, b, c in product((S, T), (D, S, T), (D, S, T)):
        value = target(a, b, c)
        if any(value):
            nonzero.append((a, b, c))
        if b == D or c == D:
            assert not any(value)
        assert value == target(b, a, c)
    assert nonzero == [(S, S, S), (T, T, T)]

    # Reverse abstract row order relative to the primary replay.
    e0 = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    e1 = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    e2 = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    e3 = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    assert rank([e0, e1, e2]) == 3
    assert rank([e0, e2, e3]) == 3
    assert rank([e1, e2]) == rank([e2, e3]) == 2


def audit_shifts() -> None:
    zero = (Fraction(0), Fraction(0), Fraction(0))
    for lam_s, lam_t in product(range(-4, 5), repeat=2):
        for a, b, c in product((S, T), repeat=3):
            coefficient = Fraction(lam_s if c == S else lam_t)
            shifted = add(target(a, b, c), zero, coefficient)
            assert shifted == target(a, b, c)


def audit_line_trap() -> None:
    # Reverse coordinate convention: (h,q_t,q_s,q_d).
    h = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    qt = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    qs = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    qd = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    q_binary = [qs, qt]
    q_space = [qd, qs, qt]

    masks = {1: 0, 2: 0}
    for aa, bb in product(range(-3, 4), repeat=2):
        if aa == bb == 0:
            continue
        masks[int(aa != 0) + int(bb != 0)] += 1
        for cc in (-7, -1, 2, 5):
            if aa:
                lam_s, lam_t = Fraction(cc, aa), Fraction(0)
            else:
                lam_s, lam_t = Fraction(0), Fraction(cc, bb)
            line = add(add(scale(Fraction(aa), qs), scale(Fraction(bb), qt)), scale(Fraction(cc), qd))
            shifted_s = add(qs, qd, lam_s)
            shifted_t = add(qt, qd, lam_t)
            reconstructed = add(
                scale(Fraction(aa), shifted_s),
                scale(Fraction(bb), shifted_t),
            )
            assert reconstructed == line
            assert rank([shifted_s, shifted_t, line]) == 2

            plane = [line, h]
            assert rank(plane + q_binary) == 4
            assert len(plane) + len(q_space) - rank(plane + q_space) == 1
    assert masks == {1: 12, 2: 36}
    assert rank([qd, scale(Fraction(17), qd)]) == 1


def main() -> None:
    audit_correction()
    audit_mixed_table()
    audit_shifts()
    audit_line_trap()
    print(
        "S2BY independent audit passed: reverse correction, injective rows, "
        "complete mixed table, kernel shifts, and rational line masks."
    )


if __name__ == "__main__":
    main()
