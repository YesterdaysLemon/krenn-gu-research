"""Independent Fraction audit of the aligned-rank-two exclusion."""

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
    return [sum(entries) for entries in zip(*vectors, strict=True)]


def scale(value: Fraction, vector: Vector) -> Vector:
    return [value * entry for entry in vector]


def dot(left: Vector, right: Vector) -> Fraction:
    return sum(a * b for a, b in zip(left, right, strict=True))


def outer(left: Vector, right: Vector) -> Matrix:
    return [[a * b for b in right] for a in left]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return [dot(row, vector) for row in matrix]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    columns = transpose(right)
    return [[dot(row, column) for column in columns] for row in left]


def subtract(left: Matrix, right: Matrix) -> Matrix:
    return [
        [a - b for a, b in zip(row_left, row_right, strict=True)]
        for row_left, row_right in zip(left, right, strict=True)
    ]


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


def select_columns(matrix: Matrix, columns: list[Vector]) -> Matrix:
    return matmul(matrix, transpose(columns))


def block_derivative(b23: Matrix, b13: Matrix) -> Matrix:
    rows: Matrix = []
    for a, b, c in product(range(3), repeat=3):
        row = [q(0)] * 9
        row[a] = b23[b][c]
        row[3 + b] = b13[a][c]
        rows.append(row)
    return rows


def audit_graph_identity() -> None:
    transform = [[q(0), q(0), q(0)], [q(2), q(3), q(0)], [q(5), q(0), q(7)]]
    t = matvec(transform, unit(3, 0))
    kernel = [q(1), q(-2, 3), q(-5, 7)]
    assert rank(transform) == 2
    assert matvec(transform, kernel) == [q(0)] * 3

    kappa, lam = q(11), q(13)
    b23 = outer(scale(kappa, unit(3, 0)), unit(3, 0))
    w = [q(17), q(19), q(23)]
    b13 = [
        [
            lam * int(i == 0 and j == 0) + kernel[i] * w[j]
            for j in range(3)
        ]
        for i in range(3)
    ]
    assert rank(block_derivative(b23, b13)) == 6
    expected_tc = outer(scale(lam, t), unit(3, 0))
    assert matmul(transform, b13) == expected_tc

    coefficient = [q(0)] * 27
    for a, b, c in product(range(3), repeat=3):
        index = 9 * a + 3 * b + c
        target = q(int(a == b == c == 0))
        graph = unit(3, 0)[a] * b23[b][c] + b13[a][c] * t[b]
        coefficient[index] = target - graph / kappa
        assert coefficient[index] == -b13[a][c] * t[b] / kappa
    assert all(coefficient[9 * a + c] == 0 for a, c in product(range(3), repeat=2))

    for colour in (1, 2):
        matrix = outer(unit(3, colour), unit(3, colour))
        pulled = matmul(transform, matrix)
        assert pulled == transpose(pulled)
    for colour in range(3):
        column = [b13[row][colour] for row in range(3)]
        matrix = outer(scale(q(-1, 11), column), t)
        pulled = matmul(transform, matrix)
        assert pulled == transpose(pulled)
    print("independent graph audit: PASS (rank six / target / symmetry)")


def tensor_flatten_rank(tensor: Vector, mode: int) -> int:
    matrix = [[q(0)] * 9 for _ in range(3)]
    for i, j, k in product(range(3), repeat=3):
        indices = (i, j, k)
        others = [indices[index] for index in range(3) if index != mode]
        matrix[indices[mode]][3 * others[0] + others[1]] = tensor[9 * i + 3 * j + k]
    return rank(matrix)


def audit_tangent_rank() -> None:
    diagonal = [q(0)] * 27
    for colour, value in enumerate((q(2), q(3), q(5))):
        diagonal[9 * colour + 3 * colour + colour] = value
    assert [tensor_flatten_rank(diagonal, mode) for mode in range(3)] == [3, 3, 3]

    ux, uy, uz = [q(1), q(2), q(3)], [q(2), q(3), q(5)], [q(3), q(5), q(7)]
    qx, qy, qz = [q(5), q(7), q(11)], [q(7), q(11), q(13)], [q(11), q(13), q(17)]
    tangent = [q(0)] * 27
    for i, j, k in product(range(3), repeat=3):
        tangent[9 * i + 3 * j + k] = 2 * (
            ux[i] * uy[j] * qz[k]
            + ux[i] * qy[j] * uz[k]
            + qx[i] * uy[j] * uz[k]
        )
    assert all(tensor_flatten_rank(tangent, mode) <= 2 for mode in range(3))
    print("independent tangent audit: PASS (mode-rank mismatch)")


def audit_kernel_cases() -> None:
    basis = [unit(9, i) for i in range(9)]
    x0, x1 = basis[0], basis[1]
    y0, y1 = basis[3], basis[4]
    z0, z1, z2 = basis[6], basis[7], basis[8]

    zero_u, zero_v = add(x0, y0), add(x0, scale(q(-1), y0))
    assert rank(derivative(zero_u, zero_v)) == 0
    assert derivative(zero_v, zero_v) == [
        scale(q(-1), row) for row in derivative(zero_u, zero_u)
    ]

    one_u = add(x0, y0, z0)
    one_v = add(scale(q(-1), x0), scale(q(-1), y0), z0)
    xy = basis[:6]
    assert rank(select_columns(derivative(one_u, one_v), xy)) == 0
    assert select_columns(derivative(one_v, one_v), xy) == [
        scale(q(-1), row) for row in select_columns(derivative(one_u, one_u), xy)
    ]

    regular_u = add(x0, y0, z0)
    regular_v = add(x0, scale(q(-1), y0), z1)
    regular_cross = derivative(regular_u, regular_v)
    assert rank(regular_cross) == 6
    assert rank(select_columns(regular_cross, [z0, z1, z2])) == 0
    assert rank(select_columns(derivative(regular_u, regular_u), [z0, z1, z2])) == 3

    special_u = add(x0, y0, z0)
    special_v = add(x0, scale(q(-1), y0), scale(q(2), z0))
    kernel = [z0, z1, z2, add(scale(q(-3), x0), y0)]
    special_cross = derivative(special_u, special_v)
    assert rank(select_columns(special_cross, kernel)) == 0
    assert rank(select_columns(derivative(special_u, special_u), kernel)) == 3

    three_u = add(x0, y0, z0)
    three_v = add(x1, y1, z1)
    assert all(rank(block) > 0 for block in pair_blocks(three_u, three_v))
    assert 9 - rank(derivative(three_u, three_v)) <= 2
    print("independent kernel atlas: PASS (zero / one / two / three)")


def audit_binary_reduction() -> None:
    transform = [[q(0), q(0), q(0)], [q(2), q(3), q(0)], [q(5), q(0), q(7)]]
    kernel = [q(1), q(-2, 3), q(-5, 7)]
    alpha1 = [q(2, 3), q(1), q(0)]
    alpha2 = [q(5, 7), q(0), q(1)]
    beta1 = [q(0), q(1, 3), q(0)]
    beta2 = [q(0), q(0), q(1, 7)]
    assert dot(alpha1, kernel) == dot(alpha2, kernel) == 0
    assert matvec(transpose(transform), beta1) == alpha1
    assert matvec(transpose(transform), beta2) == alpha2
    print("independent binary reduction: PASS (same-row squares / cross zero)")


def main() -> None:
    audit_graph_identity()
    audit_tangent_rank()
    audit_kernel_cases()
    audit_binary_reduction()
    print("independent transverse-rank-six aligned-rank-two exclusion audit: PASS")


if __name__ == "__main__":
    main()
