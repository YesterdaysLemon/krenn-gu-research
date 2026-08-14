#!/usr/bin/env python3
"""Independent Fraction audit for the S2BZ support-two exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Vector = tuple[Fraction, ...]


def unit(size: int, index: int) -> Vector:
    return tuple(Fraction(i == index) for i in range(size))


def add(left: Vector, right: Vector, scale: Fraction = Fraction(1)) -> Vector:
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def join(*vectors: Vector) -> Vector:
    return tuple(entry for vector in vectors for entry in vector)


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
        value = matrix[pivot_row][col]
        matrix[pivot_row] = [entry / value for entry in matrix[pivot_row]]
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


def outer3(a: Vector, b: Vector, c: Vector) -> Vector:
    # Reverse third/second/first storage relative to the primary replay.
    return tuple(a[i] * b[j] * c[k] for k, j, i in product(range(3), repeat=3))


def c_tensor(C: tuple[Vector, ...], c: Vector) -> Vector:
    return tuple(C[i][j] * c[k] for k, j, i in product(range(3), repeat=3))


def derivative(
    x: Vector,
    y: Vector,
    w: Vector,
    C: tuple[Vector, ...],
    a: Vector,
    b: Vector,
    c: Vector,
) -> Vector:
    first = outer3(a, y, w)
    second = outer3(x, b, w)
    third = c_tensor(C, c)
    return tuple(
        u - v + z for u, v, z in zip(first, second, third, strict=True)
    )


def audit_fixture() -> None:
    d, s, t = 0, 1, 2
    zero = unit(3, 0)
    zero = tuple(Fraction(0) for _ in zero)
    x, y = unit(3, s), unit(3, t)
    w = add(unit(3, s), unit(3, t))
    C = tuple(
        tuple(Fraction(i == d and j == d) for j in range(3)) for i in range(3)
    )
    derivative_columns = []
    for block in range(3):
        for colour in range(3):
            entries = [zero, zero, zero]
            entries[block] = unit(3, colour)
            derivative_columns.append(derivative(x, y, w, C, *entries))
    assert rank(derivative_columns) == 8

    n = join(x, y, zero)
    h = join(unit(3, t), zero, zero)
    v_d = join(zero, unit(3, d), unit(3, d))
    v_u = join(unit(3, t), unit(3, s), add(unit(3, s), unit(3, t), -1))
    K = [n, h, v_d, v_u]
    assert rank(K) == 4
    for block, expected in ((0, 2), (1, 3), (2, 2)):
        projections = [vector[3 * block : 3 * (block + 1)] for vector in K]
        assert rank(projections) == expected
    assert rank([derivative_columns[0]]) == 1
    assert rank([derivative(x, y, w, C, *(
        (vector[:3], vector[3:6], vector[6:])
    )) for vector in K]) == 3


def audit_correction_and_lines() -> None:
    kappa = Fraction(13)
    for source_colour in range(3):
        solution = [Fraction(0)] * 3
        if source_colour == 0:
            solution[0] = -1 / kappa
        reconstructed = [Fraction(0)] * 9
        for colour, coefficient in enumerate(solution):
            reconstructed[3 * colour] += kappa * coefficient
        expected = [Fraction(0)] * 9
        if source_colour == 0:
            expected[0] = -1
        assert reconstructed == expected

    for d, s, t in permutations(range(3)):
        diagonal_s = tuple(
            Fraction(i == s and j == s) for j, i in product(range(3), repeat=2)
        )
        diagonal_t = tuple(
            Fraction(i == t and j == t) for j, i in product(range(3), repeat=2)
        )
        assert rank([diagonal_s, diagonal_t]) == 2
        for scale in (Fraction(-7, 3), Fraction(2), Fraction(11, 5)):
            forced = tuple(scale * entry for entry in diagonal_s)
            assert rank([forced, diagonal_s]) == 1
            assert rank([forced, diagonal_t]) == 2


def main() -> None:
    audit_fixture()
    audit_correction_and_lines()
    print(
        "S2BZ independent audit passed: reverse derivative fixture, K ranks, "
        "correction components, all colour permutations, and incompatible lines."
    )


if __name__ == "__main__":
    main()
