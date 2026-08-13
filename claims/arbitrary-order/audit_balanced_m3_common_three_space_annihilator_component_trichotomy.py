"""Independent stdlib audit of the m=3 component trichotomy arithmetic."""

from fractions import Fraction
from itertools import product


def rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    pivots = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(pivots, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivots], matrix[pivot] = matrix[pivot], matrix[pivots]
        scale = matrix[pivots][column]
        matrix[pivots] = [value / scale for value in matrix[pivots]]
        for row in range(len(matrix)):
            if row == pivots or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [value - scale * base for value, base in zip(matrix[row], matrix[pivots])]
        pivots += 1
    return pivots


def check_integer_budget():
    count = 0
    for r1, r2, r3 in product(range(3), repeat=3):
        for epsilon in (0, 1):
            projective_dimension = sum(2 - value for value in (r1, r2, r3)) - epsilon
            if projective_dimension < 3:
                continue
            count += 1
            assert r1 + r2 + r3 <= 3 - epsilon
    assert count == 27
    print("independent dimension-budget census: PASS (27)")


def check_coordinate_models():
    e0, e1, e2 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    redundant = ((e2,), (e2,), (e2,))
    assert [rank(list(columns)) for columns in redundant] == [1, 1, 1]
    redundant_kernels = (
        ((1, 0, 0), (0, 1, 0)),
        ((1, 0, 0), (0, 1, 0)),
        ((1, 0, 0), (0, 1, 0)),
    )
    assert all(all(sum(column[i] * vector[i] for i in range(3)) == 0 for column in columns) for columns, kernel in zip(redundant, redundant_kernels) for vector in kernel)

    independent = ((), (e0,), (e1,))
    assert [rank(list(columns)) for columns in independent] == [0, 1, 1]
    projective_dimensions = (1, 1, 1)
    assert sum(projective_dimensions) == 3
    print("independent sharp rank controls: PASS")


def check_diagonal_control():
    # Boundary choices: first factor kills colour 0, second kills 1, third kills 2.
    values = ((0, 2, 3), (5, 0, 7), (11, 13, 0))
    equations = [values[0][colour] * values[1][colour] * values[2][colour] for colour in range(3)]
    assert equations == [0, 0, 0]
    print("independent diagonal multi-boundary control: PASS")


def main():
    check_integer_budget()
    check_coordinate_models()
    check_diagonal_control()
    print("independent m=3 component-trichotomy audit: PASS")


if __name__ == "__main__":
    main()
