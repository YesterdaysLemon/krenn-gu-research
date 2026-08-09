"""Independent no-import audit of border-GHZ and single-flip transversality."""

from fractions import Fraction
from itertools import product

WORDS = tuple(product(range(3), repeat=5))


def word_index(word):
    index = 0
    for digit in word:
        index = 3 * index + digit
    return index


def unit_column(word):
    index = word_index(word)
    return [1 if row == index else 0 for row in range(243)]


def rows_from_columns(columns):
    return [[column[row] for column in columns] for row in range(243)]


def rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    for column in range(column_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if work[row][column]:
                pivot = row
                break
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row != pivot_row and work[row][column]:
                multiplier = work[row][column]
                work[row] = [
                    value - multiplier * pivot_entry
                    for value, pivot_entry in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def flip_words(active_colours):
    result = []
    for colour in active_colours:
        for position in range(5):
            for replacement in range(3):
                if replacement == colour:
                    continue
                word = [colour] * 5
                word[position] = replacement
                result.append(tuple(word))
    return tuple(result)


def mat_vec(matrix, vector):
    return [sum(row[column] * vector[column] for column in range(3)) for row in matrix]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant_three(matrix):
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def inverse_three(matrix):
    determinant = determinant_three(matrix)
    cofactors = []
    for row in range(3):
        cofactor_row = []
        for column in range(3):
            minor_rows = [index for index in range(3) if index != row]
            minor_columns = [index for index in range(3) if index != column]
            minor = (
                matrix[minor_rows[0]][minor_columns[0]]
                * matrix[minor_rows[1]][minor_columns[1]]
                - matrix[minor_rows[0]][minor_columns[1]]
                * matrix[minor_rows[1]][minor_columns[0]]
            )
            cofactor_row.append(Fraction(((-1) ** (row + column)) * minor, determinant))
        cofactors.append(cofactor_row)
    return transpose(cofactors)


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def main():
    pure_words = tuple((colour,) * 5 for colour in range(3))
    flips = flip_words((0, 1, 2))
    assert len(flips) == len(set(flips)) == 30
    assert set(flips).isdisjoint(pure_words)
    assert rank(rows_from_columns([unit_column(word) for word in pure_words + flips])) == 33

    segre_dimension = sum(3 - 1 for _ in range(5))
    secant_dimension = 3 * segre_dimension + 2
    forced_dimension = 218 + secant_dimension - 242
    assert (segre_dimension, secant_dimension, forced_dimension) == (10, 32, 8)

    omitted = set(flips[-22:])
    nonpure = [word for word in WORDS if word not in pure_words]
    included = [word for word in nonpure if word not in omitted]
    tau = [sum(unit_column(word)[row] for word in pure_words) for row in range(243)]
    sensor_columns = [tau] + [unit_column(word) for word in included]
    delta_columns = [unit_column(word) for word in pure_words]
    flip_columns = [unit_column(word) for word in flips]
    assert len(sensor_columns) == 219
    assert rank(rows_from_columns(sensor_columns)) == 219
    assert rank(rows_from_columns(sensor_columns + delta_columns)) == 221
    assert rank(rows_from_columns(sensor_columns + delta_columns + flip_columns)) == 243

    flip_intersection = 30 + 221 - 243
    assert flip_intersection == 8
    assert 30 - flip_intersection == 22
    assert len(flip_words((0,))) == 10
    assert len(flip_words((0, 1))) == 20

    # Independent exact contraction audit with explicit inverse-transpose.
    g = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    assert determinant_three(g) == 2
    inverse_transpose = transpose(inverse_three(g))
    x = [1, 1, 1]
    h = [2, -1, 3]
    transformed_h = mat_vec(g, h)
    transformed_x = mat_vec(inverse_transpose, x)
    assert dot(transformed_h, transformed_x) == dot(h, x)

    print("AUDIT PASS: 33 independent pure/single-flip tangent words")
    print("AUDIT PASS: forced border-rank-three intersection dimension is 8")
    print("AUDIT PASS: independent coordinate model has normal rank 22")
    print("AUDIT PASS: one/two-term flip capacities are 10 and 20")
    print("AUDIT PASS: contragredient contraction covariance")
    print("searches=0")
    print("SCOPE: torus-concise point in the legal sensor image remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
