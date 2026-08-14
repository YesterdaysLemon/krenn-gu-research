#!/usr/bin/env python3
"""Independent no-import audit for the joint-rank-three q=2 controls."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

DIM = 3
TOTAL = 9
D, C, J = 0, 1, 2

Vector = tuple[Fraction, ...]
SparseTensor = dict[tuple[int, int, int], Fraction]
Laurent = dict[tuple[int, ...], Fraction]


def unit(index: int, size: int = TOTAL) -> Vector:
    return tuple(Fraction(int(position == index)) for position in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def matrix_rank(rows: list[list[Fraction]]) -> int:
    data = [row[:] for row in rows if any(row)]
    if not data:
        return 0
    pivot_row = 0
    for column in range(len(data[0])):
        pivot = next(
            (candidate for candidate in range(pivot_row, len(data)) if data[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        data[pivot_row], data[pivot] = data[pivot], data[pivot_row]
        divisor = data[pivot_row][column]
        data[pivot_row] = [entry / divisor for entry in data[pivot_row]]
        for candidate in range(len(data)):
            if candidate == pivot_row or not data[candidate][column]:
                continue
            multiplier = data[candidate][column]
            data[candidate] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    data[candidate], data[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(data):
            break
    return pivot_row


def split(row: Vector) -> tuple[Vector, Vector, Vector]:
    return row[:DIM], row[DIM : 2 * DIM], row[2 * DIM :]


def permanent(left: Vector, middle: Vector, right: Vector) -> SparseTensor:
    rows = split(left), split(middle), split(right)
    result: SparseTensor = {}
    for assignment in reversed(tuple(permutations(range(3)))):
        for x_index, y_index, z_index in product(range(DIM), repeat=3):
            coefficient = (
                rows[assignment[0]][0][x_index]
                * rows[assignment[1]][1][y_index]
                * rows[assignment[2]][2][z_index]
            )
            if coefficient:
                key = x_index, y_index, z_index
                result[key] = result.get(key, Fraction(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def alternating(first: Vector, second: Vector, third: Vector) -> SparseTensor:
    rows = split(first), split(second), split(third)
    result: SparseTensor = {}
    for assignment in reversed(tuple(permutations(range(3)))):
        inversions = sum(
            assignment[left] > assignment[right]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        sign = Fraction(-1 if inversions % 2 else 1)
        for x_index, y_index, z_index in product(range(DIM), repeat=3):
            coefficient = sign * (
                rows[assignment[0]][0][x_index]
                * rows[assignment[1]][1][y_index]
                * rows[assignment[2]][2][z_index]
            )
            if coefficient:
                key = x_index, y_index, z_index
                result[key] = result.get(key, Fraction(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def control_rows(support: int) -> tuple[list[Vector], list[Vector], list[Vector]]:
    x = unit(J)
    y = unit(DIM + J)
    z = unit(2 * DIM + J)
    a = add(scale(Fraction(-2), y), z)
    b = add(scale(Fraction(2), x), scale(Fraction(-1), z))
    v = add(x, y)
    w = add(x, scale(Fraction(-1), y))
    q = scale(Fraction(1, 2), add(x, y, z))
    zero = tuple(Fraction(0) for _ in range(TOTAL))
    first = [a, zero, v]
    second = [zero, b, v]
    if support == 1:
        third = [zero, w, q]
    else:
        third = [w, scale(Fraction(2), w), q]
    return first, second, third


def singleton_slice(first_coefficients: Vector, second_coefficients: Vector) -> SparseTensor:
    result: SparseTensor = {}
    for index, coefficient in enumerate(first_coefficients):
        if coefficient:
            key = index, D, D
            result[key] = result.get(key, Fraction(0)) + coefficient
    for index, coefficient in enumerate(second_coefficients):
        if coefficient:
            key = C, index, C
            result[key] = result.get(key, Fraction(0)) + coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def column_from_rows(
    root_rows: tuple[list[Vector], list[Vector], list[Vector]], source_index: int
) -> SparseTensor:
    first, second, _third = root_rows
    first_coefficients = tuple(first[colour][source_index] for colour in range(DIM))
    second_coefficients = tuple(second[colour][source_index] for colour in range(DIM))
    return singleton_slice(first_coefficients, second_coefficients)


def audit_control(support: int) -> None:
    root_rows = control_rows(support)
    flattened = [list(row) for block in root_rows for row in block]
    assert matrix_rank(flattened) == 3

    first, second, third = root_rows
    assert matrix_rank([list(row) for row in third]) == 2
    if support == 1:
        assert not any(third[D])
    else:
        assert third[C] == scale(Fraction(2), third[D])

    empty: dict[tuple[int, int, int, int, int, int], Fraction] = {}
    for left, middle, right in product(range(DIM), repeat=3):
        for nonroot, coefficient in permanent(
            first[left], second[middle], third[right]
        ).items():
            empty[(left, middle, right, *nonroot)] = coefficient
    assert empty == {(J, J, J, J, J, J): Fraction(1)}

    x_index, y_index, z_index = J, DIM + J, 2 * DIM + J
    singleton_columns = [
        column_from_rows(root_rows, source_index)
        for source_index in (x_index, y_index, z_index)
    ]
    support_keys = sorted(set().union(*(column.keys() for column in singleton_columns)))
    matrix = [
        [column.get(key, Fraction(0)) for column in singleton_columns]
        for key in support_keys
    ]
    assert matrix_rank(matrix) == 3
    assert support_keys == [(D, D, D), (C, C, C), (C, J, C), (J, D, D)]

    target_j = {(J, J, J): Fraction(1)}
    a, b = first[D], second[C]
    v, w, q = first[J], third[C], third[J]
    assert permanent(v, v, q) == target_j
    for left, middle in ((a, v), (v, b), (a, b)):
        assert not permanent(left, middle, w)
        assert not permanent(left, middle, q)
    assert alternating(a, b, v) == {(J, J, J): Fraction(4)}
    print(f"independent support-{support} control: PASS")


def laurent_add(*polynomials: Laurent) -> Laurent:
    result: Laurent = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, Fraction(0)) + coefficient
    return {exponent: coefficient for exponent, coefficient in result.items() if coefficient}


def laurent_shift(value: Fraction, shift: tuple[int, ...], polynomial: Laurent) -> Laurent:
    result: Laurent = {}
    for exponent, coefficient in polynomial.items():
        shifted = tuple(
            left + right for left, right in zip(exponent, shift, strict=True)
        )
        scaled = value * coefficient
        if scaled:
            result[shifted] = scaled
    return result


def monomial(*indices: int) -> Laurent:
    exponent = [0] * TOTAL
    for index in indices:
        exponent[index] += 1
    return {tuple(exponent): Fraction(1)}


def unit_shift(index: int, amount: int = 1) -> tuple[int, ...]:
    exponent = [0] * TOTAL
    exponent[index] = amount
    return tuple(exponent)


def rational_pair_audit() -> None:
    target_d = monomial(D, DIM + D, 2 * DIM + D)
    target_c = monomial(C, DIM + C, 2 * DIM + C)
    target_sum = laurent_add(target_d, target_c)
    target_difference = laurent_add(target_d, laurent_shift(Fraction(-1), (0,) * TOTAL, target_c))
    x_index, y_index, z_index = J, DIM + J, 2 * DIM + J

    c_x = laurent_shift(Fraction(1, 4), unit_shift(x_index, -1), target_sum)
    c_y = laurent_shift(Fraction(-1, 4), unit_shift(y_index, -1), target_sum)
    c_z = laurent_shift(Fraction(1, 2), unit_shift(z_index, -1), target_difference)

    coordinate_d = laurent_add(
        laurent_shift(Fraction(-2), unit_shift(y_index), c_y),
        laurent_shift(Fraction(1), unit_shift(z_index), c_z),
    )
    coordinate_c = laurent_add(
        laurent_shift(Fraction(2), unit_shift(x_index), c_x),
        laurent_shift(Fraction(-1), unit_shift(z_index), c_z),
    )
    coordinate_j = laurent_add(
        laurent_shift(Fraction(1), unit_shift(x_index), c_x),
        laurent_shift(Fraction(1), unit_shift(y_index), c_y),
    )
    assert coordinate_d == target_d
    assert coordinate_c == target_c
    assert not coordinate_j
    assert min(exponent[x_index] for exponent in c_x) == -1
    assert min(exponent[y_index] for exponent in c_y) == -1
    assert min(exponent[z_index] for exponent in c_z) == -1
    print("independent rational pair lift: PASS (three exposed poles)")


def main() -> None:
    audit_control(1)
    audit_control(2)
    rational_pair_audit()
    print("independent joint-rank-three q=2 control audit: PASS")


if __name__ == "__main__":
    main()
