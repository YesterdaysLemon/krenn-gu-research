"""Independent stdlib audit of compressed P5 four-hafnian tomography.

This file imports neither the primary replay nor a computer-algebra package.
"""

from itertools import combinations, product

ROOTS = range(3)
ENDPOINTS = range(7)
POWERS = (1, 2, 4)
WORDS = list(product(range(3), repeat=3))
DELETIONS = list(combinations(ENDPOINTS, 3))
EDGES = list(combinations(ENDPOINTS, 2))
PURE_ROWS = (0, 13, 26)


def entry(root: int, endpoint: int, coordinate: int) -> int:
    t = endpoint + 1
    a = t ** POWERS[root]
    values = (1, a, a * a) if endpoint < 5 else (1, a, -1 - a)
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


def build_sensor() -> list[list[int]]:
    rows: list[list[int]] = []
    for word in WORDS:
        current: list[int] = []
        for deleted in DELETIONS:
            matrix = [
                [entry(root, endpoint, word[root]) for endpoint in deleted]
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


def multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in zip(*right)]
        for row in left
    ]


def main() -> None:
    for root in ROOTS:
        assert all(sum(entry(root, endpoint, c) for c in range(3)) for endpoint in range(5))
        assert all(
            sum(entry(root, endpoint, c) for c in range(3)) == 0
            for endpoint in range(5, 7)
        )

    gamma = build_sensor()
    sensor_minor = [row[:27] for row in gamma]
    sensor_residue = determinant_mod(sensor_minor, 1_000_033)
    assert sensor_residue == 356_742

    deck_jacobian = []
    for deleted in DELETIONS:
        complement = set(ENDPOINTS) - set(deleted)
        deck_jacobian.append(
            [int(set(edge).issubset(complement)) for edge in EDGES]
        )
    composite = multiply(gamma, deck_jacobian)
    jacobian_residue = determinant_mod(composite[:21], 1_000_033)
    assert jacobian_residue == 541_617

    augmented = [
        row + [int(index == pure_row) for pure_row in PURE_ROWS]
        for index, row in enumerate(composite)
    ]
    target_residue = determinant_mod(
        [augmented[index] for index in [*range(23), 26]], 1_000_033
    )
    assert target_residue == 559_439

    all_one_tensor = [3 * sum(row) for row in gamma]
    assert all_one_tensor[1] == 420_840

    print("AUDIT PASS: independent Ryser construction of the 27x35 sensor")
    print("AUDIT PASS: named sensor determinant mod 1000033 = 356742")
    print("AUDIT PASS: composite Jacobian determinant mod 1000033 = 541617")
    print("AUDIT PASS: tangent-target determinant mod 1000033 = 559439")
    print("AUDIT PASS: legal blocker and residual contractions")
    print("searches=0 project_imports=0 computer_algebra=0")
    print("AUDIT SCOPE: physical target incidence and global Krenn-Gu remain UNKNOWN")


if __name__ == "__main__":
    main()
