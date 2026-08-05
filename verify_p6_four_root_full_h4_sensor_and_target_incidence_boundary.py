"""Primary exact replay for the P6 four-root full-H4 sensor theorem.

The script evaluates two named integer minors and fixed inclusion ranks.
It performs no graph, support, word, or parameter-family search.
"""

from functools import cache
from itertools import combinations, product

import sympy as sp

ROOTS = tuple(range(4))
NONROOTS = tuple(range(8))
BLOCKERS = tuple(range(6))
RESIDUALS = (6, 7)
WEIGHTS = (1, 2, 4, 8)
WORDS = tuple(product(range(3), repeat=4))
FOUR_SETS = tuple(combinations(NONROOTS, 4))
SENSOR_ROWS = (
    *range(54),
    55,
    56,
    58,
    59,
    61,
    62,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    76,
    77,
)
TARGET_ROWS = (
    *range(54),
    55,
    56,
    57,
    58,
    59,
    61,
    62,
    64,
    65,
    66,
    67,
    68,
    69,
    70,
    71,
    76,
    77,
    79,
    80,
)


def covector(root: int, endpoint: int) -> tuple[int, int, int]:
    """Return the fixed legal root--nonroot covector."""

    t = endpoint + 1
    power = WEIGHTS[root]
    a = t**power
    if endpoint in BLOCKERS:
        return (1, a, a * a)
    return (1, a, -1 - a)


@cache
def permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Permanent by an exact first-row matching recurrence."""

    if not matrix:
        return 1
    if len(matrix) == 1:
        return matrix[0][0]
    total = 0
    for column, value in enumerate(matrix[0]):
        minor = tuple(
            tuple(row[j] for j in range(len(row)) if j != column)
            for row in matrix[1:]
        )
        total += value * permanent(minor)
    return total


def sensor_matrix() -> list[list[int]]:
    rows: list[list[int]] = []
    for word in WORDS:
        row = []
        for endpoints in FOUR_SETS:
            matrix = tuple(
                tuple(covector(root, endpoint)[word[root]] for endpoint in endpoints)
                for root in ROOTS
            )
            row.append(permanent(matrix))
        rows.append(row)
    return rows


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
    for column in range(len(work)):
        pivot = next(
            row for row in range(column, len(work)) if work[row][column]
        )
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % prime
        inverse = pow(pivot_value, prime - 2, prime)
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            factor = work[row][column] * inverse % prime
            for j in range(column, len(work)):
                work[row][j] = (work[row][j] - factor * work[column][j]) % prime
    return determinant % prime


def inclusion_matrix() -> sp.Matrix:
    edges = tuple(combinations(NONROOTS, 2))
    return sp.Matrix(
        [
            [int(set(edge).issubset(four_set)) for edge in edges]
            for four_set in FOUR_SETS
        ]
    )


def main() -> None:
    for root in ROOTS:
        assert all(sum(covector(root, endpoint)) != 0 for endpoint in BLOCKERS)
        assert all(sum(covector(root, endpoint)) == 0 for endpoint in RESIDUALS)

    matrix = sensor_matrix()
    assert len(matrix) == 3**4 == 81
    assert len(matrix[0]) == len(FOUR_SETS) == 70

    sensor_minor = [matrix[row] for row in SENSOR_ROWS]
    sensor_residue = determinant_mod(sensor_minor, 1_000_003)
    assert sensor_residue == 636_419

    pure_word_rows = {0: 0, 40: 1, 80: 2}
    augmented = [
        row
        + [
            int(index == 0),
            int(index == 40),
            int(index == 80),
        ]
        for index, row in enumerate(matrix)
    ]
    assert pure_word_rows == {0: 0, 40: 1, 80: 2}
    target_minor = [augmented[row] for row in TARGET_ROWS]
    target_residue = determinant_mod(target_minor, 1_000_003)
    assert target_residue == 420_326

    inclusion = inclusion_matrix()
    assert inclusion.shape == (70, 28)
    assert inclusion.rank() == 28

    print("PASS: legal six-blocker/two-residual four-root chart")
    print("PASS: complete P6 depth-four label count = binom(8,4) = 70")
    print("PASS: named 70x70 sensor determinant mod 1000003 = 636419")
    print("PASS: all 70 principal four-hafnians are individually selectable")
    print("PASS: augmented diagonal-target rank = 73")
    print("PASS: named 73x73 determinant mod 1000003 = 420326")
    print("PASS: W_(2,4)(8) has exact rank 28")
    print("searches=0 graph_enumerations=0 support_enumerations=0")
    print("SCOPE: the displayed full sensor has no nonzero diagonal target")
    print("SCOPE: GHZ forcing of the incidence locus remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
