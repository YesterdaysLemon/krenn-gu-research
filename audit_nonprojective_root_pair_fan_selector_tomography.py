"""Independent no-import audit of nonprojective fan tomography."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

PAIRS = tuple(combinations(range(4), 2))


def fan_matrix(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    rows = [[0 for _ in PAIRS] for _ in range(4)]
    for column, (first, second) in enumerate(PAIRS):
        rows[0][column] = (
            left[0][first] * right[0][second]
            + left[0][second] * right[0][first]
        )
        rows[1][column] = (
            left[0][first] * right[1][second]
            + left[0][second] * right[1][first]
        )
        rows[2][column] = (
            left[1][first] * right[0][second]
            + left[1][second] * right[0][first]
        )
        rows[3][column] = (
            left[1][first] * right[1][second]
            + left[1][second] * right[1][first]
        )
    return rows


def rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(value * coordinate for value, coordinate in zip(row, vector, strict=True))
        for row in matrix
    ]


def hollow(vector: list[int]) -> list[list[int]]:
    result = [[0 for _ in range(4)] for _ in range(4)]
    for value, (first, second) in zip(vector, PAIRS, strict=True):
        result[first][second] = result[second][first] = value
    return result


def sandwich(
    left: list[list[int]], matrix: list[list[int]], right: list[list[int]]
) -> list[int]:
    result = []
    for left_row in range(2):
        for right_row in range(2):
            result.append(
                sum(
                    left[left_row][first]
                    * matrix[first][second]
                    * right[right_row][second]
                    for first in range(4)
                    for second in range(4)
                )
            )
    return result


def complement(vector: list[int]) -> list[int]:
    universe = frozenset(range(4))
    result = [0 for _ in PAIRS]
    for port_index, pair in enumerate(PAIRS):
        face = tuple(sorted(universe.difference(pair)))
        result[port_index] = vector[PAIRS.index(face)]
    return result


def add(left: list[int], right: list[int]) -> list[int]:
    return [a + b for a, b in zip(left, right, strict=True)]


def main() -> None:
    left_one = [[1, 0, 1, 0], [0, 1, 0, 1]]
    right_one = [[1, 0, 0, 1], [0, 1, 1, 0]]
    fan_one = fan_matrix(left_one, right_one)
    expected_one = [
        [0, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 1, 1],
    ]
    assert fan_one == expected_one
    assert rank(fan_one) == 4

    null_vectors = ([0, 1, -1, -1, 1, 0], [1, 0, -1, -1, 0, 1])
    for vector in null_vectors:
        assert matvec(fan_one, list(vector)) == [0, 0, 0, 0]
    assert rank([list(vector) for vector in null_vectors]) == 2

    face = [2, -1, 3, 4, 0, -2]
    assert matvec(fan_one, face) == sandwich(
        left_one, hollow(face), right_one
    )

    left_two = [[1, 0, 1, 1], [0, 1, 1, 2]]
    right_two = [[1, 0, 1, 2], [0, 1, 2, 1]]
    fan_two = fan_matrix(left_two, right_two)
    expected_two = [
        [0, 2, 3, 0, 0, 3],
        [1, 2, 1, 1, 1, 3],
        [1, 1, 2, 1, 2, 4],
        [0, 0, 0, 3, 3, 5],
    ]
    assert fan_two == expected_two
    assert rank(fan_two) == 4
    assert rank(fan_one + fan_two) == 6

    observed = matvec(fan_one, complement(face))
    for invisible in null_vectors:
        deformed = add(face, complement(list(invisible)))
        assert matvec(fan_one, complement(deformed)) == observed
        assert matvec(fan_two, complement(deformed)) != matvec(
            fan_two, complement(face)
        )

    assert fan_matrix([[0] * 4, [0] * 4], right_one) == [[0] * 6 for _ in range(4)]

    print("AUDIT PASS: direct hollow sandwich and exact fan matrix")
    print("AUDIT PASS: one fan has rank four with two invisible directions")
    print("AUDIT PASS: two integer fans have transverse defect and rank six")
    print("AUDIT PASS: complement-face ambiguity is separated by the second fan")
    print("AUDIT SCOPE: no legal P7 co-occurrence theorem is asserted")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
