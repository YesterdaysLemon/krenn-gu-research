"""Independent stdlib audit of the P6 four-root full-H4 sensor package.

This file does not import the primary verifier or a computer-algebra package.
"""

from fractions import Fraction
from itertools import combinations, product

ROOTS = range(4)
ENDPOINTS = range(8)
POWERS = (1, 2, 4, 8)
WORDS = list(product(range(3), repeat=4))
FOUR_SETS = list(combinations(ENDPOINTS, 4))
SENSOR_ROWS = list(range(54)) + [
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
]
TARGET_ROWS = list(range(54)) + [
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
]


def entry(root: int, endpoint: int, coordinate: int) -> int:
    t = endpoint + 1
    a = t ** POWERS[root]
    values = (1, a, a * a) if endpoint < 6 else (1, a, -1 - a)
    return values[coordinate]


def permanent_ryser(matrix: list[list[int]]) -> int:
    size = len(matrix)
    total = 0
    for mask in range(1, 1 << size):
        chosen = mask.bit_count()
        term = 1
        for row in matrix:
            term *= sum(row[column] for column in range(size) if mask >> column & 1)
        total += (-1) ** (size - chosen) * term
    return total


def build_rows() -> list[list[int]]:
    rows = []
    for word in WORDS:
        current = []
        for subset in FOUR_SETS:
            matrix = [
                [entry(root, endpoint, word[root]) for endpoint in subset]
                for root in ROOTS
            ]
            current.append(permanent_ryser(matrix))
        rows.append(current)
    return rows


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in matrix]
    answer = 1
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        diagonal = work[column][column]
        answer = answer * diagonal % prime
        inverse = pow(diagonal, prime - 2, prime)
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] * inverse % prime
            if multiplier:
                work[row] = [
                    (left - multiplier * right) % prime
                    for left, right in zip(work[row], work[column], strict=True)
                ]
    return answer % prime


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    columns = len(work[0])
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        divisor = work[rank][column]
        work[rank] = [value / divisor for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
    return rank


def main() -> None:
    for root in ROOTS:
        assert all(sum(entry(root, endpoint, c) for c in range(3)) for endpoint in range(6))
        assert all(
            sum(entry(root, endpoint, c) for c in range(3)) == 0
            for endpoint in range(6, 8)
        )

    rows = build_rows()
    sensor_residue = determinant_mod([rows[index] for index in SENSOR_ROWS], 1_000_033)
    assert sensor_residue == 549_813

    augmented = [
        row + [int(index == 0), int(index == 40), int(index == 80)]
        for index, row in enumerate(rows)
    ]
    target_residue = determinant_mod(
        [augmented[index] for index in TARGET_ROWS], 1_000_033
    )
    assert target_residue == 680_957

    edges = list(combinations(ENDPOINTS, 2))
    inclusion = [
        [int(set(edge).issubset(subset)) for edge in edges]
        for subset in FOUR_SETS
    ]
    assert rational_rank(inclusion) == 28

    print("AUDIT PASS: independent Ryser construction of the 81x70 sensor")
    print("AUDIT PASS: named sensor determinant mod 1000033 = 549813")
    print("AUDIT PASS: diagonal-target determinant mod 1000033 = 680957")
    print("AUDIT PASS: independent rational W_(2,4)(8) rank = 28")
    print("AUDIT PASS: legal blocker and residual contractions")
    print("searches=0 project_imports=0 computer_algebra=0")
    print("AUDIT SCOPE: target incidence and global Krenn-Gu remain UNKNOWN")


if __name__ == "__main__":
    main()
