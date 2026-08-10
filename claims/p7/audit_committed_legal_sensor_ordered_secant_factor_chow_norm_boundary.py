"""Independent stdlib audit of the ordered secant--factor criterion."""

from __future__ import annotations

from fractions import Fraction

Matrix = list[list[Fraction]]


def matrix(rows: list[list[int]]) -> Matrix:
    return [[Fraction(entry) for entry in row] for row in rows]


def identity(size: int) -> Matrix:
    return [
        [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]


def add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][column] + right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def subtract(left: Matrix, right: Matrix) -> Matrix:
    return [
        [left[row][column] - right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return [
        [
            sum(
                (left[row][pivot] * right[pivot][column] for pivot in range(len(right))),
                Fraction(0),
            )
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def scalar_multiply(scalar: Fraction, value: Matrix) -> Matrix:
    return [[scalar * entry for entry in row] for row in value]


def transpose(value: Matrix) -> Matrix:
    return [list(column) for column in zip(*value, strict=True)]


def determinant_3(value: Matrix) -> Fraction:
    a, b, c = value
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def minor_2(value: Matrix, deleted_row: int, deleted_column: int) -> Fraction:
    entries = [
        value[row][column]
        for row in range(3)
        for column in range(3)
        if row != deleted_row and column != deleted_column
    ]
    return entries[0] * entries[3] - entries[1] * entries[2]


def adjugate_3(value: Matrix) -> Matrix:
    cofactor = [
        [
            Fraction((-1) ** (row + column)) * minor_2(value, row, column)
            for column in range(3)
        ]
        for row in range(3)
    ]
    return transpose(cofactor)


def rank(value: Matrix) -> int:
    work = [row[:] for row in value]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    entry - factor * pivot_entry
                    for entry, pivot_entry in zip(
                        work[row], work[pivot_row], strict=True
                    )
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def determinant(value: Matrix) -> Fraction:
    work = [row[:] for row in value]
    size = len(work)
    result = Fraction(1)
    sign = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for target_column in range(column, size):
                work[row][target_column] -= factor * work[column][target_column]
    return Fraction(sign) * result


def power(value: Matrix, exponent: int) -> Matrix:
    result = identity(len(value))
    factor = value
    while exponent:
        if exponent & 1:
            result = multiply(result, factor)
        factor = multiply(factor, factor)
        exponent //= 2
    return result


def verify_membership() -> None:
    b = matrix([[1, 2, 0], [0, 1, 1], [2, 0, 1]])
    c = matrix([[1, -1, 2], [3, 1, 0]])
    q = matrix([[2], [-1], [3]])
    beta = determinant_3(b)
    assert beta == 5
    z_pivot = multiply(b, q)
    z_tail = multiply(c, q)
    numerator = multiply(adjugate_3(b), z_pivot)
    assert numerator == scalar_multiply(beta, q)
    assert subtract(scalar_multiply(beta, z_tail), multiply(c, numerator)) == matrix(
        [[0], [0]]
    )

    perturbed_tail = add(z_tail, matrix([[0], [1]]))
    residual = subtract(
        scalar_multiply(beta, perturbed_tail), multiply(c, numerator)
    )
    assert residual == matrix([[0], [5]])


def verify_incidence_rank() -> None:
    vectors = [
        [Fraction(int(row == column)) for column in range(7)] for row in range(7)
    ]
    # Rows are ambient coordinates and columns are basis vectors.
    w = transpose(vectors[:3])
    simple = transpose([vectors[2], vectors[3], vectors[4]])
    deeper = transpose([vectors[1], vectors[2], vectors[3]])
    assert rank([left + right for left, right in zip(w, simple, strict=True)]) == 5
    assert rank([left + right for left, right in zip(w, deeper, strict=True)]) == 4


def wedge_coordinates(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return [
        left[row] * right[column] - left[column] * right[row]
        for row in range(len(left))
        for column in range(row + 1, len(left))
    ]


def verify_universal_separator() -> None:
    # A contraction by algebraically independent selectors is zero exactly
    # when every coefficient in these lists is zero.
    simple_wedge = wedge_coordinates(
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0)],
    )
    deeper_wedge = wedge_coordinates(
        [Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(2), Fraction(0), Fraction(0)],
    )
    pair_vector = [Fraction(2), Fraction(-1), Fraction(0)]
    zero_pair_vector = [Fraction(0), Fraction(0), Fraction(0)]
    assert any(simple_wedge)
    assert not any(deeper_wedge)
    assert any(pair_vector)
    assert not any(zero_pair_vector)


def verify_artinian_operators() -> None:
    # In A=Q[x]/(x^3-x^2), these are multiplication matrices in [1,x,x^2].
    m_x = matrix([[0, 0, 0], [1, 0, 0], [0, 1, 1]])
    zero = matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    m_trapped = subtract(multiply(m_x, m_x), m_x)  # x(x-1)
    m_unit = add(identity(3), m_x)  # x+1

    assert m_trapped != zero
    assert power(m_trapped, 2) == zero
    assert determinant(m_x) == 0
    assert power(m_x, 3) != zero
    assert determinant(m_unit) == 2


def verify_arithmetic() -> None:
    assert 3 * (5 * 2) + 2 == 32
    assert 32 - (243 - 219) - 8 == 0
    assert 3 + 3 + 3 >= 2 * 3 + 2
    assert 6 * 259 == 1554


def main() -> None:
    verify_membership()
    verify_incidence_rank()
    verify_universal_separator()
    verify_artinian_operators()
    verify_arithmetic()
    print("PASS: independent ordered secant-factor Chow/norm audit")
    print("no enumeration, sampling, finite fields, or numerical inference")


if __name__ == "__main__":
    main()
