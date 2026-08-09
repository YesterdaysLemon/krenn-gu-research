"""Independent stdlib audit of five-root shared-root fan transversality."""

from __future__ import annotations

from fractions import Fraction

PAIRS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(column) for column in zip(*matrix, strict=True)]


def matmul(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    right_transpose = transpose(right)
    return [
        [
            sum(a * b for a, b in zip(row, column, strict=True))
            for column in right_transpose
        ]
        for row in left
    ]


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(value * entry for value, entry in zip(row, vector, strict=True))
        for row in matrix
    ]


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


def determinant(matrix: list[list[int]]) -> int:
    if len(matrix) == 1:
        return matrix[0][0]
    total = 0
    sign = 1
    for column, value in enumerate(matrix[0]):
        minor = [
            row[:column] + row[column + 1 :]
            for row in matrix[1:]
        ]
        total += sign * value * determinant(minor)
        sign = -sign
    return total


def permanent(matrix: list[list[int]]) -> int:
    """Exact row-by-row subset recurrence, independent of SymPy."""
    size = len(matrix)
    states = {0: 1}
    for row in range(size):
        updated: dict[int, int] = {}
        for mask, coefficient in states.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                updated[new_mask] = updated.get(new_mask, 0) + (
                    coefficient * matrix[row][column]
                )
        states = updated
    return states[(1 << size) - 1]


def fan_matrix(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    result = [[0 for _ in PAIRS] for _ in range(4)]
    for column, (first, second) in enumerate(PAIRS):
        for left_row in range(2):
            for right_row in range(2):
                row = 2 * left_row + right_row
                result[row][column] = (
                    left[left_row][first] * right[right_row][second]
                    + left[left_row][second] * right[right_row][first]
                )
    return result


def hollow(face: list[int]) -> list[list[int]]:
    result = [[0 for _ in range(4)] for _ in range(4)]
    for value, (first, second) in zip(face, PAIRS, strict=True):
        result[first][second] = result[second][first] = value
    return result


def flatten(matrix: list[list[int]]) -> list[int]:
    return [entry for row in matrix for entry in row]


def veronese(kernel_basis: list[list[int]]) -> list[list[int]]:
    return [
        [first * first, 2 * first * second, second * second]
        for first, second in kernel_basis
    ]


def kronecker(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    result = []
    for left_row in range(2):
        for right_row in range(2):
            result.append(
                [
                    left[left_row][left_column]
                    * right[right_row][right_column]
                    for left_column in range(2)
                    for right_column in range(2)
                ]
            )
    return result


def outer(left: list[int], right: list[int]) -> list[list[int]]:
    return [[first * second for second in right] for first in left]


def bilinear(left: list[int], block: list[list[int]], right: list[int]) -> int:
    return sum(
        left[row] * block[row][column] * right[column]
        for row in range(3)
        for column in range(3)
    )


def audit_physical_incidence(incidence: list[list[int]]) -> None:
    frozen = [1, 1, 1]
    tangent = ([0, 1, 0], [0, 0, 1])
    beta = [1, 0, 0]
    for port in range(4):
        first = incidence[0][port]
        second = incidence[1][port]
        block = outer([-(first + second), first, second], beta)
        assert bilinear(frozen, block, frozen) == 0
        assert bilinear(tangent[0], block, frozen) == first
        assert bilinear(tangent[1], block, frozen) == second


def main() -> None:
    common = [[-1, -1, 1, 0], [-1, -2, 0, 1]]
    other_one = [[1, 0, 0, 0], [0, 1, 0, 0]]
    other_two = [[0, 0, 1, 0], [0, 0, 0, 1]]
    kernel_basis = [[1, 0], [0, 1], [1, 1], [1, 2]]
    combined_other = other_one + other_two

    assert determinant(combined_other) == 1
    assert matmul(common, kernel_basis) == [[0, 0], [0, 0]]
    assert rank(veronese(kernel_basis)) == 3

    face = [2, -1, 3, 4, 0, -2]
    common_hollow = hollow(face)
    fan_one = fan_matrix(common, other_one)
    fan_two = fan_matrix(common, other_two)
    assert matvec(fan_one, face) == flatten(
        matmul(matmul(common, common_hollow), transpose(other_one))
    )
    assert matvec(fan_two, face) == flatten(
        matmul(matmul(common, common_hollow), transpose(other_two))
    )
    assert rank(fan_one) == rank(fan_two) == 4
    assert rank(fan_one + fan_two) == 6

    boundary_common = [[1, -1, 0, 0], [0, 0, 1, -1]]
    boundary_kernel = [[1, 0], [1, 0], [0, 1], [0, 1]]
    boundary_one = [[1, 0, 1, 1], [0, 1, 1, 2]]
    boundary_two = [[1, 0, 1, 2], [0, 1, 2, 1]]
    boundary_fan_one = fan_matrix(boundary_common, boundary_one)
    boundary_fan_two = fan_matrix(boundary_common, boundary_two)
    boundary_stack = boundary_fan_one + boundary_fan_two
    common_face = [0, 1, 1, 1, 1, 0]

    assert matmul(boundary_common, boundary_kernel) == [[0, 0], [0, 0]]
    assert determinant(boundary_one + boundary_two) == -1
    assert rank(veronese(boundary_kernel)) == 2
    assert rank(boundary_fan_one) == rank(boundary_fan_two) == 4
    assert rank(boundary_stack) == 5
    assert matvec(boundary_stack, common_face) == [0] * 8

    disjoint_left_one = [[1, 0, 1, 0], [0, 1, 0, 1]]
    disjoint_right_one = [[1, 0, 0, 1], [0, 1, 1, 0]]
    disjoint_fan_one = fan_matrix(disjoint_left_one, disjoint_right_one)
    disjoint_fan_two = fan_matrix(boundary_one, boundary_two)
    assert rank(disjoint_fan_one) == rank(disjoint_fan_two) == 4
    assert rank(disjoint_fan_one + disjoint_fan_two) == 6

    change_left = [[1, 1], [0, 1]]
    change_right = [[2, 0], [1, 1]]
    changed_left = matmul(change_left, disjoint_left_one)
    changed_right = matmul(change_right, disjoint_right_one)
    assert fan_matrix(changed_left, changed_right) == matmul(
        kronecker(change_left, change_right), disjoint_fan_one
    )

    roots = {0, 1, 2, 3, 4}
    first_pair = {0, 1}
    shared_pair = {0, 2}
    disjoint_pair = {2, 3}
    assert len((roots - first_pair) & (roots - first_pair)) == 3
    assert len((roots - first_pair) & (roots - shared_pair)) == 2
    assert len((roots - first_pair) & (roots - disjoint_pair)) == 1
    assert first_pair <= roots - disjoint_pair
    assert disjoint_pair <= roots - first_pair

    assert permanent([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 6

    frozen = [1, 1, 1]
    tangent_one = [0, 1, 0]
    tangent_two = [0, 0, 1]
    blocker = outer([1, 0, 0], [1, 0, 0])
    assert bilinear(frozen, blocker, frozen) == 1
    assert bilinear(tangent_one, blocker, frozen) == 0
    assert bilinear(tangent_two, blocker, frozen) == 0

    for incidence in (
        common,
        other_one,
        other_two,
        disjoint_left_one,
        disjoint_right_one,
        boundary_one,
        boundary_two,
    ):
        audit_physical_incidence(incidence)

    print("AUDIT PASS: equal/shared/disjoint five-root shore geometry")
    print("AUDIT PASS: independent shared-root Veronese rank dichotomy")
    print("AUDIT PASS: transverse and sharp defective shared-root controls")
    print("AUDIT PASS: disjoint transverse control and shore permanent six")
    print("AUDIT PASS: physical frozen/tangent edge-block evaluations")
    print("AUDIT SCOPE: full target GHZ compatibility remains UNKNOWN")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
