"""Independent standard-library audit of lower-jet deletion-label tomography."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from math import prod


def odd_double_factorial(n: int) -> int:
    if n == -1:
        return 1
    return prod(range(1, n + 1, 2))


def hafnian(weights: tuple[tuple[int, ...], ...]) -> int:
    size = len(weights)

    @cache
    def recurrence(mask: int) -> int:
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        total = 0
        partners = rest
        while partners:
            partner_bit = partners & -partners
            partner = partner_bit.bit_length() - 1
            total += weights[first][partner] * recurrence(rest ^ partner_bit)
            partners ^= partner_bit
        return total

    return recurrence((1 << size) - 1)


def coefficient_from_legal_blocks(q: int, tangent_mask: int, endpoint_mask: int) -> int:
    endpoints = [i for i in range(q) if endpoint_mask & (1 << i)]
    size = q + len(endpoints)
    weights = [[0 for _ in range(size)] for _ in range(size)]

    # alpha_i alpha_j root--root blocks are active exactly on two zero bits.
    for i in range(q):
        for j in range(i + 1, q):
            if not (tangent_mask & (1 << i)) and not (tangent_mask & (1 << j)):
                weights[i][j] = weights[j][i] = 1

    # beta_i private-port blocks are active exactly on bit one.
    for local_endpoint, endpoint in enumerate(endpoints):
        vertex = q + local_endpoint
        if tangent_mask & (1 << endpoint):
            weights[endpoint][vertex] = weights[vertex][endpoint] = 1

    return hafnian(tuple(tuple(row) for row in weights))


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    cols = len(work[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][col]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                work[row][entry] - factor * work[pivot_row][entry] for entry in range(cols)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def audit_chart(q: int, expected_determinant: int) -> None:
    masks = [mask for mask in range(1 << q) if mask.bit_count() % 2 == 0]
    matrix = [
        [coefficient_from_legal_blocks(q, tangent, endpoint) for endpoint in masks]
        for tangent in masks
    ]
    determinant = 1
    for row, tangent in enumerate(masks):
        for col, endpoint in enumerate(masks):
            expected = (
                odd_double_factorial(q - endpoint.bit_count() - 1)
                if tangent == endpoint
                else 0
            )
            assert matrix[row][col] == expected
        determinant *= matrix[row][row]
    assert determinant == expected_determinant
    assert rational_rank(matrix) == 1 << (q - 1)


def audit_kernel_translation() -> None:
    gamma = [[1, 0, 1], [0, 1, 1]]
    kernel = [-1, -1, 1]
    assert [sum(row[i] * kernel[i] for i in range(3)) for row in gamma] == [0, 0]
    cofactors = [[2, 7], [3, 11], [5, 13]]
    invisible = [17, 19]
    shifted = [
        [cofactors[i][j] + kernel[i] * invisible[j] for j in range(2)] for i in range(3)
    ]
    for row in gamma:
        before = [sum(row[i] * cofactors[i][j] for i in range(3)) for j in range(2)]
        after = [sum(row[i] * shifted[i][j] for i in range(3)) for j in range(2)]
        assert before == after
    assert shifted[0] != cofactors[0]


def zeon_multiply(left: int, right: int) -> int | None:
    return None if left & right else left | right


def audit_squarefree_gauge() -> None:
    permutation = (1, 3, 0, 2)
    scales = (Fraction(2), Fraction(5), Fraction(7), Fraction(1, 70))
    assert prod(scales) == 1

    def transform(mask: int) -> tuple[int, Fraction]:
        target = 0
        scale = Fraction(1)
        for i in range(4):
            if mask & (1 << i):
                target |= 1 << permutation[i]
                scale *= scales[i]
        return target, scale

    for left in range(16):
        for right in range(16):
            source_product = zeon_multiply(left, right)
            image_left, left_scale = transform(left)
            image_right, right_scale = transform(right)
            image_product = zeon_multiply(image_left, image_right)
            if source_product is None:
                assert image_product is None
            else:
                target, target_scale = transform(source_product)
                assert image_product == target
                assert left_scale * right_scale == target_scale
    assert transform(15) == (15, Fraction(1))


def main() -> None:
    audit_chart(4, 3)
    print("AUDIT PASS: independent q=4 legal-block matching recurrence")
    audit_chart(6, 15 * 3**15)
    print("AUDIT PASS: independent q=6 legal-block matching recurrence")
    audit_kernel_translation()
    print("AUDIT PASS: independent invisible-kernel perturbation")
    audit_squarefree_gauge()
    print("AUDIT PASS: direct square-free multiplication and top normalization")
    print("AUDIT SCOPE: common-core synchronization is not supplied")
    print("searches=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
