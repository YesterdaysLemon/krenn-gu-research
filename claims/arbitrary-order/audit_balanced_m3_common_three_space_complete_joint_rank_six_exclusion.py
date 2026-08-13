"""Independent Fraction audit of the complete joint-rank-six exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Vector = list[Fraction]
Matrix = list[list[Fraction]]


def q(value: int, denominator: int = 1) -> Fraction:
    return Fraction(value, denominator)


def unit(size: int, index: int) -> Vector:
    return [q(int(i == index)) for i in range(size)]


def add(*vectors: Vector) -> Vector:
    return [sum(values) for values in zip(*vectors, strict=True)]


def scale(value: Fraction, vector: Vector) -> Vector:
    return [value * entry for entry in vector]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum(a * b for a, b in zip(left, right, strict=True))


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    columns = transpose(right)
    return [[dot(row, column) for column in columns] for row in left]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [dot(row, vector) for row in matrix]


def rank(matrix: Matrix) -> int:
    work = [row[:] for row in matrix]
    pivot_row = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [entry / divisor for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def pair_blocks(left: Vector, right: Vector) -> tuple[Matrix, Matrix, Matrix]:
    a = [
        [left[3 + i] * right[6 + j] + right[3 + i] * left[6 + j] for j in range(3)]
        for i in range(3)
    ]
    b = [
        [left[i] * right[6 + j] + right[i] * left[6 + j] for j in range(3)]
        for i in range(3)
    ]
    c = [
        [left[i] * right[3 + j] + right[i] * left[3 + j] for j in range(3)]
        for i in range(3)
    ]
    return a, b, c


def derivative(left: Vector, right: Vector) -> Matrix:
    a, b, c = pair_blocks(left, right)
    rows: Matrix = []
    for x, y, z in product(range(3), repeat=3):
        row = [q(0)] * 9
        row[x] = a[y][z]
        row[3 + y] = b[x][z]
        row[6 + z] = c[x][y]
        rows.append(row)
    return rows


def root_derivative(b23: Matrix, b13: Matrix) -> Matrix:
    rows: Matrix = []
    for a, b, c in product(range(3), repeat=3):
        row = [q(0)] * 9
        row[a] = b23[b][c]
        row[3 + b] = b13[a][c]
        rows.append(row)
    return rows


def columns(matrix: Matrix, vectors: list[Vector]) -> Matrix:
    return matmul(matrix, transpose(vectors))


def mixed_variable_map(u: Vector, q_vectors: list[Vector]) -> Matrix:
    # Each column is the concatenated output for one coordinate basis vector
    # in the first mixed argument.  This orientation differs from the primary.
    output_columns: list[Vector] = []
    for coordinate in range(9):
        current: Vector = []
        operator = derivative(unit(9, coordinate), u)
        for q_vector in q_vectors:
            current.extend(matvec(operator, q_vector))
        output_columns.append(current)
    return transpose(output_columns)


def audit_profiles_and_target() -> None:
    same = [[q(0), q(0), q(0)], [q(0), q(2), q(0)], [q(0), q(0), q(3)]]
    different = [[q(0), q(2), q(0)], [q(0), q(0), q(0)], [q(0), q(5), q(7)]]
    assert rank(same) == rank(different) == 2
    assert matvec(same, unit(3, 0)) == matvec(different, unit(3, 0)) == [q(0)] * 3
    assert different[1] == [q(0)] * 3

    b23 = [[q(2), q(1), q(3)], [q(0), q(11), q(0)], [q(5), q(7), q(13)]]
    b13 = [[q(17), q(19), q(23)], [q(29), q(31), q(37)], [q(41), q(43), q(47)]]
    assert rank(root_derivative(b23, b13)) == 6
    assert b23[1] == [q(0), q(11), q(0)]

    a = unit(3, 1)
    ta = matvec(different, a)
    graph_vector = a + ta + [q(0)] * 3
    correction = matvec(root_derivative(b23, b13), graph_vector)
    for first, second, third in product(range(3), repeat=3):
        expected = a[first] * b23[second][third] + b13[first][third] * ta[second]
        assert correction[9 * first + 3 * second + third] == expected
    print("independent coordinate-profile audit: PASS")


def audit_five_product_cases() -> None:
    basis = [unit(9, index) for index in range(9)]
    x0, x1, x2 = basis[0], basis[1], basis[2]
    y0, y1 = basis[3], basis[4]
    z0 = basis[6]

    full_u = add(x0, y0, z0)
    full_kernel = [add(x0, scale(q(-1), y0)), add(x0, scale(q(-1), z0))]
    assert rank(derivative(full_u, full_u)) == 7
    assert rank(columns(derivative(full_u, full_u), full_kernel)) == 0
    # The mixed-argument constraint has rank eight, hence only the line u.
    full_mixed = mixed_variable_map(full_u, full_kernel)
    assert rank(full_mixed) == 8
    assert all(value == 0 for value in matvec(full_mixed, full_u))

    two_u = add(x0, y0)
    xy = basis[:6]
    assert rank(columns(derivative(two_u, two_u), xy)) == 0
    two_v = add(x1, y1, z0)
    assert rank(columns(derivative(two_u, two_v), xy)) == 5

    pure_u = x0
    pure_v = add(y0, z0)
    h = add(y0, scale(q(-1), z0))
    q_plane = [x1, h]
    assert rank(columns(derivative(pure_u, pure_v), q_plane)) == 0
    square = columns(derivative(pure_v, pure_v), q_plane)
    assert rank(square) == 1
    r = add(x2, scale(q(3), y0), scale(q(-3), z0))
    assert rank(columns(derivative(r, pure_v), q_plane)) == 0
    other = columns(derivative(r, pure_u), q_plane)
    assert rank(other) == 1
    assert square[9 * 1 + 0][0] != 0
    assert other[0][1] != 0
    print("independent five-product audit: PASS")


def audit_square_pencil() -> None:
    basis = [unit(9, index) for index in range(9)]
    x0, x1 = basis[0], basis[1]
    y0 = basis[3]
    z0 = basis[6]

    two_u = add(x0, y0)
    two_q = [x0, y0, z0]
    square = columns(derivative(two_u, two_u), two_q)
    assert rank(square) == 1
    mixed_map = mixed_variable_map(two_u, two_q)
    assert rank(mixed_map) == 8  # one-dimensional zero-divisor space
    assert all(value == 0 for value in matvec(mixed_map, add(x0, scale(q(-1), y0))))

    # Restricting every output to the disjoint X1 Y1 Z1 line adds no allowed
    # value: the kept-row functionals already lie in the row span of the
    # equations killing every other tensor coordinate.
    kept = 9 * 1 + 3 * 1 + 1
    excluded_rows = [
        27 * column + row
        for column in range(3)
        for row in range(27)
        if row != kept
    ]
    kept_rows = [27 * column + kept for column in range(3)]
    outside = [mixed_map[row] for row in excluded_rows]
    with_kept = outside + [mixed_map[row] for row in kept_rows]
    assert rank(outside) == rank(with_kept)

    full_u = add(x0, y0, z0)
    full_q = [add(x0, scale(q(-1), y0)), add(x0, scale(q(-1), z0)), x1]
    full_square = columns(derivative(full_u, full_u), full_q)
    assert rank(full_square) == 1
    full_map = mixed_variable_map(full_u, full_q)
    assert rank(full_map) == 9  # zero-divisor space is zero

    full_outside = [full_map[row] for row in excluded_rows]
    full_with_kept = full_outside + [full_map[row] for row in kept_rows]
    assert rank(full_outside) == rank(full_with_kept)
    print("independent square-pencil audit: PASS")


def audit_two_rank_two_form() -> None:
    tau = q(5)
    k_columns = [
        unit(3, 0) + [q(0)] * 3,
        [q(0)] * 3 + unit(3, 1),
        unit(3, 2) + scale(tau, unit(3, 2)),
    ]
    l_columns = [
        unit(3, 1) + [q(0)] * 3,
        [q(0)] * 3 + unit(3, 0),
        scale(-tau, unit(3, 2)) + unit(3, 2),
    ]
    k_matrix = transpose(k_columns)
    l_matrix = transpose(l_columns)
    assert rank(k_matrix) == rank(l_matrix) == 3
    assert matmul(transpose(k_matrix), l_matrix) == [[q(0)] * 3 for _ in range(3)]

    # Coordinate image plus the required row (7,0,0) fixes the whole block.
    coordinate_block = [[q(7), q(0), q(0)], [q(0)] * 3, [q(0)] * 3]
    assert coordinate_block[0] == [q(7), q(0), q(0)]
    assert rank(coordinate_block) == 1
    print("independent two-rank-two audit: PASS")


def main() -> None:
    audit_profiles_and_target()
    audit_five_product_cases()
    audit_square_pencil()
    audit_two_rank_two_form()
    print("independent complete common-three-space joint-rank-six exclusion audit: PASS")


if __name__ == "__main__":
    main()
