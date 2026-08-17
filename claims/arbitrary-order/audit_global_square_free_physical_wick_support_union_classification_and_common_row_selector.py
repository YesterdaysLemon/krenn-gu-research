"""Independent no-import audit of the global square-free Wick theorem."""

from fractions import Fraction
from itertools import combinations


def choose(n: int, size: int):
    return tuple(combinations(range(n), size))


def wick_rows(a, b):
    n = len(a)
    pairs = choose(n, 2)
    result = []
    for four_set in choose(n, 4):
        support = set(four_set)
        row = []
        for pair in pairs:
            if set(pair) <= support:
                i, j = tuple(support - set(pair))
                row.append(Fraction(a[i] * b[j] + b[i] * a[j]))
            else:
                row.append(Fraction(0))
        result.append(row)
    return result


def up_rows(c, degree: int):
    n = len(c)
    columns = choose(n, degree)
    rows = []
    for upper in choose(n, degree + 1):
        upper_set = set(upper)
        row = []
        for lower in columns:
            difference = upper_set - set(lower)
            row.append(
                Fraction(c[next(iter(difference))])
                if len(difference) == 1
                else Fraction(0)
            )
        rows.append(row)
    return rows


def rational_rank(rows) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    pivot_row = 0
    for column in range(n):
        pivot = next((i for i in range(pivot_row, m) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        diagonal = matrix[pivot_row][column]
        for j in range(column, n):
            matrix[pivot_row][j] /= diagonal
        for i in range(pivot_row + 1, m):
            scale = matrix[i][column]
            if not scale:
                continue
            for j in range(column, n):
                matrix[i][j] -= scale * matrix[pivot_row][j]
        pivot_row += 1
        if pivot_row == m:
            break
    return pivot_row


def bareiss_determinant(rows) -> int:
    matrix = [[int(value) for value in row] for row in rows]
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError("Bareiss requires a square matrix")
    sign = 1
    previous = 1
    for column in range(n - 1):
        pivot = next((i for i in range(column, n) if matrix[i][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            sign *= -1
        diagonal = matrix[column][column]
        for i in range(column + 1, n):
            for j in range(column + 1, n):
                numerator = (
                    matrix[i][j] * diagonal - matrix[i][column] * matrix[column][j]
                )
                assert numerator % previous == 0
                matrix[i][j] = numerator // previous
        previous = diagonal
    return sign * matrix[-1][-1]


def multiply(rows, vector):
    return [
        sum(value * entry for value, entry in zip(row, vector, strict=True))
        for row in rows
    ]


def pair_vector(n: int, terms):
    normalized = {tuple(sorted(pair)): Fraction(value) for pair, value in terms.items()}
    return [normalized.get(pair, Fraction(0)) for pair in choose(n, 2)]


def linear_product(left, right):
    return [
        Fraction(left[i] * right[j] + left[j] * right[i])
        for i, j in choose(len(left), 2)
    ]


def audit_one_step_kernels() -> None:
    n = 7
    expected = (21, 6, 6, 2, 2, 0, 0, 0)
    for support, nullity in enumerate(expected):
        coefficients = [i + 2 if i < support else 0 for i in range(n)]
        rows = up_rows(coefficients, 2)
        assert len(choose(n, 2)) - rational_rank(rows) == nullity

    b2 = [2, 3, 0, 0, 0, 0, 0]
    rows2 = up_rows(b2, 2)
    candidates = [pair_vector(n, {(0, 1): 6})]
    candidates.extend(pair_vector(n, {(0, z): 2, (1, z): -3}) for z in range(2, n))
    assert len(candidates) == n - 1
    assert all(not any(multiply(rows2, vector)) for vector in candidates)
    assert (
        rational_rank([list(column) for column in zip(*candidates, strict=True)])
        == n - 1
    )


def audit_common_row_control() -> None:
    a = [1] * 7
    b = [1] * 5 + [0, 0]
    rows = wick_rows(a, b)
    assert rational_rank(rows) == 21

    selected = {5, 6}
    windows = [window for window in choose(7, 6) if selected <= set(window)]
    assert len(windows) == 5
    for window in windows:
        local = wick_rows([a[i] for i in window], [b[i] for i in window])
        assert rational_rank(local) < 15

    coincident = wick_rows([1] * 5 + [0, 0], [2] * 5 + [0, 0])
    assert 21 - rational_rank(coincident) == 5


def audit_six_union_walls() -> None:
    generic_t = [2, 3, 5, 7]
    a = [1, 1, 1, 1, 1, 0]
    b = generic_t + [0, 1]
    rows = wick_rows(a, b)
    four_sets = choose(6, 4)
    row_by_set = {
        frozenset(four_set): row for four_set, row in zip(four_sets, rows, strict=True)
    }
    # The published Delta_6 orders each row by its complementary pair.
    complemented_rows = [
        row_by_set[frozenset(set(range(6)) - set(pair))] for pair in choose(6, 2)
    ]
    e2 = sum(generic_t[i] * generic_t[j] for i, j in combinations(range(4), 2))
    expected = -9216
    for value in generic_t:
        expected *= value**2
    expected *= e2
    assert bareiss_determinant(complemented_rows) == expected

    singular_t = [1, 1, 1, -1]
    singular_b = singular_t + [0, 1]
    singular_rows = wick_rows(a, singular_b)
    assert rational_rank(singular_rows) == 14
    first = [-value for value in singular_t] + [0, 1]
    second = [-1, -1, -1, -1, 1, 0]
    kernel = linear_product(first, second)
    assert any(kernel)
    assert not any(multiply(singular_rows, kernel))

    nested_a = [1] * 6
    nested_b = [3, 3, 3, -5, 6, 0]
    nested_rows = wick_rows(nested_a, nested_b)
    assert rational_rank(nested_rows) == 14
    nested_kernel = pair_vector(
        6,
        {
            (0, 1): 6,
            (0, 2): 6,
            (1, 2): 6,
            (0, 3): 2,
            (1, 3): 2,
            (2, 3): 2,
            (0, 4): -9,
            (1, 4): -9,
            (2, 4): -9,
            (0, 5): -3,
            (1, 5): -3,
            (2, 5): -3,
            (3, 4): -13,
            (3, 5): 1,
            (4, 5): 12,
        },
    )
    assert not any(multiply(nested_rows, nested_kernel))


def main() -> None:
    audit_one_step_kernels()
    audit_common_row_control()
    audit_six_union_walls()
    print("global square-free physical Wick independent audit: PASS")
    print("Fraction elimination, Bareiss determinant, and direct kernels: PASS")


if __name__ == "__main__":
    main()
