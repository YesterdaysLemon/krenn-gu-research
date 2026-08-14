#!/usr/bin/env python3
"""Independent no-import audit for the lower-rank transverse controls."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

DIM = 3
TOTAL = 9
S, T, U = 0, 1, 2


def unit(index: int, size: int = TOTAL) -> tuple[Fraction, ...]:
    return tuple(Fraction(int(position == index)) for position in range(size))


def add(*vectors: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale(value: Fraction, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(value * entry for entry in vector)


def matrix_rank(rows: list[list[Fraction]]) -> int:
    data = [row[:] for row in rows if any(row)]
    if not data:
        return 0
    pivot_row = 0
    for column in range(len(data[0])):
        pivot = next((row for row in range(pivot_row, len(data)) if data[row][column]), None)
        if pivot is None:
            continue
        data[pivot_row], data[pivot] = data[pivot], data[pivot_row]
        factor = data[pivot_row][column]
        data[pivot_row] = [entry / factor for entry in data[pivot_row]]
        for row in range(len(data)):
            if row == pivot_row or not data[row][column]:
                continue
            factor = data[row][column]
            data[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(data[row], data[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(data):
            break
    return pivot_row


def split(row: tuple[Fraction, ...]) -> tuple[tuple[Fraction, ...], ...]:
    return row[:3], row[3:6], row[6:9]


def permanent(
    left: tuple[Fraction, ...],
    middle: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
) -> dict[tuple[int, int, int], Fraction]:
    rows = split(left), split(middle), split(right)
    result: dict[tuple[int, int, int], Fraction] = {}
    for assignment in permutations(range(3)):
        for i, j, k in product(range(3), repeat=3):
            coefficient = (
                rows[assignment[0]][0][i]
                * rows[assignment[1]][1][j]
                * rows[assignment[2]][2][k]
            )
            if coefficient:
                key = (i, j, k)
                result[key] = result.get(key, Fraction(0)) + coefficient
    return {key: value for key, value in result.items() if value}


def rows(rank_h: int) -> tuple[list[tuple[Fraction, ...]], ...]:
    x = unit(0)
    extra = x if rank_h == 3 else unit(1)
    y = unit(3)
    z = unit(6)
    v = add(x, z)
    a = add(scale(Fraction(-1), x), z)
    b = add(scale(Fraction(-1), extra), y)
    q = scale(Fraction(1, 2), add(extra, y))
    zero = tuple(Fraction(0) for _ in range(TOTAL))
    return [v, a, zero], [v, zero, b], [q, zero, zero]


def singleton_slice(
    h_one: tuple[Fraction, ...], h_two: tuple[Fraction, ...]
) -> dict[tuple[int, int, int], Fraction]:
    result: dict[tuple[int, int, int], Fraction] = {}
    for index, coefficient in enumerate(h_one):
        if coefficient:
            key = (index, T, T)
            result[key] = result.get(key, Fraction(0)) + coefficient
    for index, coefficient in enumerate(h_two):
        if coefficient:
            key = (U, index, U)
            result[key] = result.get(key, Fraction(0)) + coefficient
    return {key: value for key, value in result.items() if value}


def column_from_rows(
    root_rows: tuple[list[tuple[Fraction, ...]], ...], source_index: int
) -> dict[tuple[int, int, int], Fraction]:
    first, second, _third = root_rows
    h_one = tuple(first[colour][source_index] for colour in range(3))
    h_two = tuple(second[colour][source_index] for colour in range(3))
    return singleton_slice(h_one, h_two)


def laurent_add(
    *polynomials: dict[tuple[int, ...], Fraction],
) -> dict[tuple[int, ...], Fraction]:
    result: dict[tuple[int, ...], Fraction] = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def laurent_scale(
    coefficient: Fraction,
    shift: tuple[int, ...],
    polynomial: dict[tuple[int, ...], Fraction],
) -> dict[tuple[int, ...], Fraction]:
    return {
        tuple(a + b for a, b in zip(monomial, shift, strict=True)): coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def monomial(*indices: int) -> dict[tuple[int, ...], Fraction]:
    exponent = [0] * 9
    for index in indices:
        exponent[index] += 1
    return {tuple(exponent): Fraction(1)}


def rational_identity(rank_h: int) -> None:
    tt = monomial(1, 4, 7)
    tu = monomial(2, 5, 8)
    extra_index = 0 if rank_h == 3 else 1

    c_x = laurent_scale(Fraction(-1, 2), (-1, 0, 0, 0, 0, 0, 0, 0, 0), tt)
    c_z = laurent_scale(Fraction(1, 2), (0, 0, 0, 0, 0, 0, -1, 0, 0), tt)
    c_y = laurent_add(
        laurent_scale(Fraction(1), (0, 0, 0, -1, 0, 0, 0, 0, 0), tu),
        laurent_scale(
            Fraction(-1, 2),
            tuple(
                int(index == extra_index) - int(index == 0) - int(index == 3)
                for index in range(9)
            ),
            tt,
        ),
    )

    # U-coordinate singleton columns are (-xs,-extra,xs), (0,ys,0),
    # and (zs,0,zs).  Replay their Cramer combination as Laurent polynomials.
    coordinate_one = laurent_add(
        laurent_scale(Fraction(-1), unit_shift(0), c_x),
        laurent_scale(Fraction(1), unit_shift(6), c_z),
    )
    coordinate_two = laurent_add(
        laurent_scale(Fraction(-1), unit_shift(extra_index), c_x),
        laurent_scale(Fraction(1), unit_shift(3), c_y),
    )
    coordinate_three = laurent_add(
        laurent_scale(Fraction(1), unit_shift(0), c_x),
        laurent_scale(Fraction(1), unit_shift(6), c_z),
    )
    assert coordinate_one == tt
    assert coordinate_two == tu
    assert not coordinate_three


def unit_shift(index: int) -> tuple[int, ...]:
    exponent = [0] * 9
    exponent[index] = 1
    return tuple(exponent)


def audit_control(rank_h: int) -> None:
    root_rows = rows(rank_h)
    flattened = [list(row) for block in root_rows for row in block]
    assert matrix_rank(flattened) == rank_h

    first, second, third = root_rows
    empty: dict[tuple[int, int, int, int, int, int], Fraction] = {}
    for a, b, c in product(range(3), repeat=3):
        for nonroot, coefficient in permanent(first[a], second[b], third[c]).items():
            empty[(a, b, c, *nonroot)] = coefficient
    assert empty == {(S, S, S, S, S, S): Fraction(1)}

    selected_columns = [
        column_from_rows(root_rows, 0),
        column_from_rows(root_rows, 3),
        column_from_rows(root_rows, 6),
    ]
    support = sorted(set().union(*(column.keys() for column in selected_columns)))
    matrix = [[column.get(key, Fraction(0)) for column in selected_columns] for key in support]
    assert matrix_rank(matrix) == 3

    v, a = first[S], first[T]
    b, q = second[U], third[S]
    assert permanent(v, v, q) == {(S, S, S): Fraction(1)}
    assert not permanent(a, v, q)
    assert not permanent(v, b, q)
    assert not permanent(a, b, q)

    rational_identity(rank_h)
    print(f"independent joint-rank-{rank_h} audit: PASS")


def main() -> None:
    for rank_h in (3, 4):
        audit_control(rank_h)
    print("independent lower-joint-rank transverse audit: PASS")


if __name__ == "__main__":
    main()
