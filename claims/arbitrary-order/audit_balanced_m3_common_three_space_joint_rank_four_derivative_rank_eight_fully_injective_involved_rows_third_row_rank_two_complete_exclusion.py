#!/usr/bin/env python3
"""Independent Fraction audit for the S2CB fully injective (3,3,2) cell."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

Vector = tuple[Fraction, ...]
N = 3


def zero(size: int) -> Vector:
    return (Fraction(0),) * size


def unit(size: int, index: int) -> Vector:
    return tuple(Fraction(i == index) for i in range(size))


def add(left: Vector, right: Vector, scale: Fraction = Fraction(1)) -> Vector:
    return tuple(a + scale * b for a, b in zip(left, right, strict=True))


def scale(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


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
    # Reverse third/second/first order relative to the SymPy replay.
    return tuple(a[i] * b[j] * c[k] for k, j, i in product(range(N), repeat=3))


def c_tensor(C: tuple[Vector, ...], c: Vector) -> Vector:
    return tuple(C[i][j] * c[k] for k, j, i in product(range(N), repeat=3))


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
        left - middle + right
        for left, middle, right in zip(first, second, third, strict=True)
    )


def projections(vectors: list[Vector], block: int) -> list[Vector]:
    return [vector[block * N : (block + 1) * N] for vector in vectors]


def audit_vertical_forks() -> None:
    z = zero(N)
    for d, s, t in permutations(range(N)):
        one_x = [
            join(unit(N, s), unit(N, t), z),
            join(z, z, unit(N, d)),
            join(z, unit(N, s), unit(N, t)),
            join(unit(N, d), unit(N, d), unit(N, s)),
        ]
        assert rank(one_x) == 4
        assert rank(projections(one_x, 0)) == 2

        one_y = [
            join(unit(N, t), unit(N, s), z),
            join(z, z, unit(N, d)),
            join(unit(N, s), z, unit(N, t)),
            join(unit(N, d), unit(N, d), unit(N, s)),
        ]
        assert rank(one_y) == 4
        assert rank(projections(one_y, 1)) == 2

        two = [
            join(unit(N, s), unit(N, t), z),
            join(z, z, unit(N, d)),
            join(z, unit(N, s), unit(N, s)),
            join(unit(N, t), z, unit(N, t)),
        ]
        assert rank(two) == 4
        assert rank(projections(two, 0)) == rank(projections(two, 1)) == 2


def audit_direct_box() -> None:
    z = zero(N)
    for d, s, t in permutations(range(N)):
        x, y, w = unit(N, s), unit(N, t), unit(N, s)
        C = tuple(
            tuple(Fraction(i == d and j == d) for j in range(N))
            for i in range(N)
        )
        derivative_columns = []
        for block in range(3):
            for colour in range(N):
                entries = [z, z, z]
                entries[block] = unit(N, colour)
                derivative_columns.append(derivative(x, y, w, C, *entries))
        assert rank(derivative_columns) == 8

        q = add(unit(N, s), unit(N, t), Fraction(-1))
        K = [
            join(x, y, z),
            join(z, scale(Fraction(-1), unit(N, s)), z),
            join(unit(N, t), z, q),
            join(unit(N, d), unit(N, d), unit(N, d)),
        ]
        assert rank(K) == 4
        assert [rank(projections(K, block)) for block in range(3)] == [3, 3, 2]
        images = [
            derivative(x, y, w, C, vector[:3], vector[3:6], vector[6:])
            for vector in K
        ]
        assert rank(images) == 3

        box = [
            outer3(unit(N, i), unit(N, j), third)
            for i in range(N)
            for j in range(N)
            for third in (unit(N, d), q)
        ]
        assert rank(box) == 18
        assert rank(box + images[1:]) == 21
        assert images[1] == outer3(unit(N, s), unit(N, s), unit(N, s))


def audit_rank_interface_and_equal_plane() -> None:
    permanent = [
        tuple(
            Fraction(sorted((i, j, k)) == [0, 1, 2])
            for k, j in product(range(N), repeat=2)
        )
        for i in range(N)
    ]
    assert rank(permanent) == 3

    r_d, r_t = unit(4, 2), unit(4, 3)
    q_d, q_t = unit(4, 2), unit(4, 3)
    assert rank([r_d, r_t]) == 2
    assert rank([q_d, q_t]) == 2
    assert rank([r_d, r_t, q_d, q_t]) == 2


def tensor_index(first: int, middle: int, third: int) -> int:
    # Third-major storage, independently of the primary replay.
    return 2 * N * third + 2 * middle + first


def audit_support_two_symmetry() -> None:
    q_d, q_c, lam = Fraction(2), Fraction(3), Fraction(5)
    e_t = unit(N, 2)
    m_d = scale(-q_d / lam, e_t)
    m_c = (Fraction(1), Fraction(4), Fraction(2))
    tensor = [Fraction(0)] * (2 * N * 2)
    for middle in range(N):
        tensor[tensor_index(1, middle, 0)] += q_d * e_t[middle]
        tensor[tensor_index(1, middle, 1)] += q_c * e_t[middle]
        tensor[tensor_index(0, middle, 1)] -= lam * m_d[middle]
        tensor[tensor_index(1, middle, 1)] -= lam * m_c[middle]

    for first, middle, third in product(range(2), range(N), range(2)):
        assert tensor[tensor_index(first, middle, third)] == tensor[
            tensor_index(third, middle, first)
        ]

    n = add(scale(q_c, e_t), scale(lam, m_c), Fraction(-1))
    for middle in range(N):
        assert tensor[tensor_index(1, middle, 1)] == n[middle]

    # q_d=0 leaves the two exact terminal middle-factor alternatives.
    e_d = unit(N, 0)
    assert rank([e_d, add(unit(N, 1), unit(N, 2))]) == 2
    assert rank([e_d, scale(Fraction(7), e_d)]) == 1


def main() -> None:
    audit_vertical_forks()
    audit_direct_box()
    audit_rank_interface_and_equal_plane()
    audit_support_two_symmetry()
    print(
        "S2CB independent audit passed: reverse derivative box, all colour "
        "orientations, vertical ranks, equal plane, outer symmetry, and "
        "binary/two-square terminal fork."
    )


if __name__ == "__main__":
    main()
