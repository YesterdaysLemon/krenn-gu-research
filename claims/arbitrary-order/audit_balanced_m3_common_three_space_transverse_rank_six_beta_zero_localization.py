"""Independent stdlib audit of the transverse-rank-six localization."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Vector = list[Fraction]
Matrix = list[list[Fraction]]


def rank(rows: Matrix) -> int:
    work = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (i for i in range(pivot_row, len(work)) if work[i][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for i, row in enumerate(work):
            if i == pivot_row or not row[column]:
                continue
            multiple = row[column]
            work[i] = [
                left - multiple * right
                for left, right in zip(row, work[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [
        sum(entry * value for entry, value in zip(row, vector, strict=True))
        for row in matrix
    ]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum(a * b for a, b in zip(left, right, strict=True))


def outer(left: Vector, right: Vector) -> Matrix:
    return [[a * b for b in right] for a in left]


def add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [a + b for a, b in zip(row_l, row_r, strict=True)]
        for row_l, row_r in zip(left, right, strict=True)
    ]


def derivative_columns(b23: Matrix, b13: Matrix) -> Matrix:
    columns: Matrix = []
    for column in range(9):
        vector = [Fraction(0)] * 27
        for a, b, c in product(range(3), repeat=3):
            row = 9 * a + 3 * b + c
            if column < 3 and a == column:
                vector[row] = b23[b][c]
            if 3 <= column < 6 and b == column - 3:
                vector[row] += b13[a][c]
        columns.append(vector)
    return [list(row) for row in zip(*columns, strict=True)]


def unit(index: int) -> Vector:
    return [Fraction(int(i == index)) for i in range(3)]


def audit_transverse_and_atlas() -> None:
    b_type_i = outer(unit(1), unit(2))
    c_rank_two = add(outer(unit(0), unit(0)), outer(unit(2), unit(2)))
    assert rank(derivative_columns(b_type_i, c_rank_two)) == 6

    z = [Fraction(1), Fraction(1), Fraction(0)]
    w = [Fraction(1), Fraction(-1), Fraction(0)]
    b_type_ii = outer(unit(1), z)
    c_type_ii = add(outer(unit(0), w), outer(unit(2), z))
    assert rank(derivative_columns(b_type_ii, c_type_ii)) == 6

    gamma = [Fraction(2), Fraction(-2), Fraction(3)]
    assert dot(z, gamma) == 0
    assert dot(w, gamma) == 4
    assert matvec(c_type_ii, gamma) == [Fraction(4), 0, 0]

    z_wide = [Fraction(1), Fraction(1), Fraction(-1)]
    w_wide = [Fraction(0), Fraction(1), Fraction(-1)]
    boundary_base = [Fraction(0), Fraction(1), Fraction(1)]
    assert dot(z_wide, boundary_base) == 0
    assert dot(w_wide, boundary_base) == 0
    assert sum(value == 0 for value in boundary_base) == 1
    print("independent transverse/atlas audit: PASS (ranks and tangent boundary)")


def audit_relation_identity() -> None:
    b23 = [
        [Fraction(1), Fraction(2), Fraction(3)],
        [Fraction(4), Fraction(5), Fraction(6)],
        [Fraction(7), Fraction(8), Fraction(10)],
    ]
    b13 = [
        [Fraction(3), Fraction(1), Fraction(4)],
        [Fraction(1), Fraction(5), Fraction(9)],
        [Fraction(2), Fraction(6), Fraction(5)],
    ]
    u = [Fraction(2), Fraction(3), Fraction(5)]
    v = [Fraction(7), Fraction(11), Fraction(13)]
    gamma = [Fraction(17), Fraction(19), Fraction(23)]

    lam = dot(v, matvec(b23, gamma))
    mu = dot(u, matvec(b13, gamma))
    btv = [sum(b23[i][j] * v[i] for i in range(3)) for j in range(3)]
    ctu = [sum(b13[i][j] * u[i] for i in range(3)) for j in range(3)]
    assert dot([a - b for a, b in zip(btv, ctu, strict=True)], gamma) == lam - mu

    noncoordinate_form = [Fraction(2), Fraction(3), Fraction(0)]
    torus_point = [Fraction(3), Fraction(-2), Fraction(5)]
    assert dot(noncoordinate_form, torus_point) == 0
    assert all(torus_point)
    print("independent relation-annihilator audit: PASS")


def audit_support_and_kernel() -> None:
    accepted = []
    for support in product((0, 1), repeat=3):
        if not any(support):
            continue
        matrix = [
            [Fraction(int(i == j) * support[i]) for j in range(3)]
            for i in range(3)
        ]
        if rank(matrix) <= 1:
            accepted.append(support)
    assert accepted == [(0, 0, 1), (0, 1, 0), (1, 0, 0)]

    shared_b = outer([Fraction(2), Fraction(3), Fraction(5)], unit(1))
    shared_c = outer([Fraction(7), Fraction(11), Fraction(13)], unit(1))
    assert rank(derivative_columns(shared_b, shared_c)) == 5
    print("independent support/kernel audit: PASS (coordinate only / shared rank 5)")


def main() -> None:
    audit_transverse_and_atlas()
    audit_relation_identity()
    audit_support_and_kernel()
    print("independent transverse-rank-six beta-zero localization audit: PASS")


if __name__ == "__main__":
    main()
