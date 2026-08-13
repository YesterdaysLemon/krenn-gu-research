"""Independent stdlib audit of the rank-six shared-factor exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

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
        if pivot_row == len(work):
            break
    return pivot_row


def e(index: int) -> Vector:
    return [Fraction(int(i == index)) for i in range(9)]


def add(left: Vector, right: Vector, sign: int = 1) -> Vector:
    return [a + sign * b for a, b in zip(left, right, strict=True)]


def pair_product(p: Vector, q: Vector) -> Vector:
    out: Vector = []
    for left, right in ((3, 6), (0, 6), (0, 3)):
        out.extend(
            p[left + i] * q[right + j] + q[left + i] * p[right + j]
            for i, j in product(range(3), repeat=2)
        )
    return out


def derivative(p: Vector, q: Vector) -> Matrix:
    pair = pair_product(p, q)
    columns: Matrix = []
    for column in range(9):
        r = e(column)
        vector = [Fraction(0)] * 27
        for x, y, z in product(range(3), repeat=3):
            vector[9 * x + 3 * y + z] = (
                r[x] * pair[3 * y + z]
                + r[3 + y] * pair[9 + 3 * x + z]
                + r[6 + z] * pair[18 + 3 * x + y]
            )
        columns.append(vector)
    return [list(row) for row in zip(*columns, strict=True)]


def audit_shared_derivative() -> None:
    columns: Matrix = []
    for column in range(9):
        vector = [Fraction(0)] * 27
        if column < 3:
            vector[9 * column] = 1
        elif column < 6:
            vector[3 * (column - 3)] = 1
        columns.append(vector)
    matrix = [list(row) for row in zip(*columns, strict=True)]
    assert rank(matrix) == 5
    print("independent shared derivative: PASS (rank 5 / nullity 4)")


def permanent(left: Vector, middle: Vector, right: Vector) -> Fraction:
    return sum(
        left[sigma[0]] * middle[sigma[1]] * right[sigma[2]]
        for sigma in permutations(range(3))
    )


def zero_diagonal(q: list[Fraction]) -> Matrix:
    return [[0, q[2], q[1]], [q[2], 0, q[0]], [q[1], q[0], 0]]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def audit_pointwise_slice() -> None:
    values = [Fraction(((19 * i + 7) % 13) - 6) for i in range(21)]
    r_matrix = [values[3 * i : 3 * i + 3] for i in range(3)]
    p_matrix = [values[9 + 3 * i : 12 + 3 * i] for i in range(3)]
    q = values[18:21]
    direct = [
        [permanent(r_matrix[i], p_matrix[j], q) for j in range(3)]
        for i in range(3)
    ]
    factored = multiply(multiply(r_matrix, zero_diagonal(q)), transpose(p_matrix))
    assert direct == factored

    support_ranks = [
        rank(zero_diagonal(list(map(Fraction, support))))
        for support in product((0, 1), repeat=3)
        if any(support)
    ]
    assert set(support_ranks) == {2, 3}
    assert all(value >= 2 for value in support_ranks)
    print("independent pointwise slice: PASS (identity / rank floor 2)")


def audit_crossed_pairs() -> None:
    x0, x1, x2 = e(0), e(1), e(2)
    y0, y1, z0 = e(3), e(4), e(6)
    controls = [
        (x0, y0, x1, y1),
        (x0, add(x2, y0), x1, add(x2, y0, -1)),
        (x0, add(y0, z0, -1), x1, add(y0, z0)),
        (add(x0, y0), add(x1, y1), add(x0, y0, -1), add(x1, y1, -1)),
        (add(x0, y0), add(x1, z0), add(x0, y0, -1), add(x1, z0, -1)),
        (add(x0, y0), add(x0, z0), add(x0, y0, -1), add(x0, z0, -1)),
    ]
    zero = [Fraction(0)] * 27
    for a_t, a_u, q_u, q_t in controls:
        assert pair_product(a_t, q_u) == zero
        assert pair_product(a_u, q_t) == zero
        assert pair_product(a_t, q_t) != zero
        assert pair_product(a_u, q_u) != zero

    same = controls[3]
    same_left = pair_product(same[0], same[3])
    same_right = pair_product(same[1], same[2])
    assert same_left == [-entry for entry in same_right]

    transverse = controls[4]
    assert rank(
        [
            *derivative(transverse[0], transverse[3]),
            *derivative(transverse[1], transverse[2]),
        ]
    ) == 9
    tangent = controls[5]
    tangent_columns = [
        *zip(*derivative(tangent[0], tangent[3]), strict=True),
        *zip(*derivative(tangent[1], tangent[2]), strict=True),
    ]
    assert rank([list(row) for row in tangent_columns]) == 7
    print("independent crossed-pair atlas: PASS (6 families / ranks 9 and 7)")


def main() -> None:
    audit_shared_derivative()
    audit_pointwise_slice()
    audit_crossed_pairs()
    print("independent rank-six shared-factor exclusion audit: PASS")


if __name__ == "__main__":
    main()
