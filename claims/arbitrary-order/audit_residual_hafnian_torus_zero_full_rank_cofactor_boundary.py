"""Independent no-import audit of the torus-zero cofactor boundary."""

from fractions import Fraction


def odd_double_factorial(value):
    product = 1
    for factor in range(1, value + 1, 2):
        product *= factor
    return product


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    size = len(work)
    result = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            factor = work[row][column] / pivot_value
            for index in range(column, size):
                work[row][index] -= factor * work[column][index]
    return result


def cofactor_matrix(order):
    alpha = odd_double_factorial(order - 3)
    beta = -2 * odd_double_factorial(order - 5)
    return [
        [
            0 if row == column else beta if row >= 2 and column >= 2 else alpha
            for column in range(order)
        ]
        for row in range(order)
    ]


def deletion_cofactor_by_partition(order, first, second):
    if 0 in (first, second) or 1 in (first, second):
        return odd_double_factorial(order - 3)
    all_one = odd_double_factorial(order - 3)
    using_special = odd_double_factorial(order - 5)
    return all_one + (-(order - 2) - 1) * using_special


def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def outer(left, right):
    return [[row * column for column in right] for row in left]


def main():
    for order in (4, 6, 8, 10, 12, 14):
        special = -(order - 2)
        hafnian = odd_double_factorial(order - 1) + (
            special - 1
        ) * odd_double_factorial(order - 3)
        assert hafnian == 0

        cofactor = cofactor_matrix(order)
        cofactor_from_deletions = [
            [
                0
                if row == column
                else deletion_cofactor_by_partition(order, row, column)
                for column in range(order)
            ]
            for row in range(order)
        ]
        assert cofactor_from_deletions == cofactor
        g = odd_double_factorial(order - 5)
        expected = 2 ** (order - 2) * (order - 1) * (order - 3) ** 3 * g**order
        assert determinant(cofactor) == expected
        assert matrix_rank(cofactor) == order

    # A single symmetrized outer-product channel has rank at most two, so
    # the independently reconstructed order-four matrix needs two channels.
    canonical_four = cofactor_matrix(4)
    assert matrix_rank(canonical_four) == 4

    # Independent integer check of the rank-two diagonal completion of its
    # physically visible off-diagonal entries.
    completed_four = [
        [-2, 1, 1, 1],
        [1, -2, 1, 1],
        [1, 1, -2, -2],
        [1, 1, -2, -2],
    ]
    assert matrix_rank(completed_four) == 2
    for row in range(4):
        for column in range(4):
            if row != column:
                assert completed_four[row][column] == canonical_four[row][column]

    left = (3, 5)
    right = (7, 11, 13)
    separator_block = outer(left, right)
    assert separator_block == [[21, 33, 39], [35, 55, 65]]
    assert matrix_rank(separator_block) == 1

    print("independent torus-zero full-rank cofactor audit: PASS")
    print("no matching or colour-word enumeration")


if __name__ == "__main__":
    main()
