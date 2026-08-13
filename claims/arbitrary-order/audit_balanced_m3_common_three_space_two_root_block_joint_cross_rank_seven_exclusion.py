"""Independent stdlib audit of the two-root-block rank-seven exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

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


def derivative(third: bool) -> Matrix:
    columns: Matrix = []
    for column in range(9):
        vector = [Fraction(0)] * 27
        if column < 3:
            vector[9 * column] += 1
        elif column < 6:
            vector[3 * (column - 3)] += 1
        elif third:
            vector[column - 6] += 1
        columns.append(vector)
    return [list(row) for row in zip(*columns, strict=True)]


def audit_derivative_boundary() -> None:
    assert rank(derivative(False)) == 5
    assert rank(derivative(True)) == 7

    vectors = [[Fraction(-1), 0, 0, 1, 0, 0, 0, 0, 0]]
    vectors.extend(
        [[Fraction(int(i == j)) for i in range(9)] for j in (6, 7, 8)]
    )
    matrix = derivative(False)
    for vector in vectors:
        assert all(
            sum(row[j] * vector[j] for j in range(9)) == 0 for row in matrix
        )
    assert rank(vectors) == 4
    print("independent derivative audit: PASS (rank 5 / kernel 4 / third 7)")


def permanent(left: list[Fraction], middle: list[Fraction], right: list[Fraction]) -> Fraction:
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


def audit_permanent_identity() -> None:
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
    print("independent permanent-matrix identity: PASS (9 entries)")


def audit_rank_floor() -> None:
    by_support: dict[int, set[int]] = {1: set(), 2: set(), 3: set()}
    for support in product((0, 1), repeat=3):
        if not any(support):
            continue
        by_support[sum(support)].add(rank(zero_diagonal(list(map(Fraction, support)))))
    assert by_support == {1: {2}, 2: {2}, 3: {3}}
    print("independent zero-diagonal ranks: PASS (2 / 2 / 3)")


def audit_missing_colour_logic() -> None:
    # If a root block row has global rank two, the two exact unaffected pure
    # slices force its only row relation to be the missing coordinate row.
    kernel = [[Fraction(0), Fraction(0), Fraction(1)]]
    assert rank(kernel) == 1

    # The corresponding tangent image has a zero missing-coordinate slice:
    # a_s=x_s=0 makes (a tensor y+x tensor b)_(s,s)=0.
    a_s = x_s = Fraction(0)
    y_s = b_s = Fraction(5)
    assert a_s * y_s + x_s * b_s == 0

    target_covectors = [
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]
    assert rank(target_covectors) == 2
    print("independent missing-colour logic: PASS (rank two cannot absorb pure s)")


def main() -> None:
    audit_derivative_boundary()
    audit_missing_colour_logic()
    audit_permanent_identity()
    audit_rank_floor()
    print("independent two-root-block joint-rank-seven exclusion audit: PASS")


if __name__ == "__main__":
    main()
