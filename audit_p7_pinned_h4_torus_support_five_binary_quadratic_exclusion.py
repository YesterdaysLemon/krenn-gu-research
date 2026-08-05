"""Independent stdlib audit of the P7 support-five torus exclusion."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def rational_rank(rows: list[list[Fraction | int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def determinant(rows: list[list[Fraction | int]]) -> Fraction:
    matrix = [[Fraction(value) for value in row] for row in rows]
    result = Fraction(1)
    for column in range(len(matrix)):
        pivot = next(row for row in range(column, len(matrix)) if matrix[row][column])
        if pivot != column:
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            result = -result
        pivot_value = matrix[column][column]
        result *= pivot_value
        for row in range(column + 1, len(matrix)):
            multiplier = matrix[row][column] / pivot_value
            for later in range(column, len(matrix)):
                matrix[row][later] -= multiplier * matrix[column][later]
    return result


def audit_binary_pair_product() -> None:
    beta = [
        [0, 1, 0],
        [-2, -1, 0],
        [0, -1, -2],
    ]
    assert determinant(beta) == -4
    q_zero = [-1, 1, -1]
    product = [sum(row[index] * q_zero[index] for index in range(3)) for row in beta]
    assert product == [1, 1, 1]
    assert determinant([[-1, Fraction(1, 2)], [Fraction(1, 2), -1]]) == Fraction(3, 4)


def pair_product(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return (
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[2] * right[0],
        left[1] * right[2] + left[2] * right[1],
    )


def audit_representative_hafnian_identity() -> None:
    v_a = (Fraction(2), Fraction(3), Fraction(-5))
    v_b = (Fraction(5), Fraction(-7), Fraction(2))
    v_c = (Fraction(-11), Fraction(13), Fraction(-2))
    assert sum(v_a) == sum(v_b) == sum(v_c) == 0
    d_ab, d_ac, d_bc = Fraction(17), Fraction(-19), Fraction(23)
    internal = d_ab + d_ac + d_bc

    expanded = []
    for i, j in combinations(range(3), 2):
        h_ab = d_ab + v_a[i] * v_b[j] + v_a[j] * v_b[i]
        h_ac = d_ac + v_a[i] * v_c[j] + v_a[j] * v_c[i]
        h_bc = d_bc + v_b[i] * v_c[j] + v_b[j] * v_c[i]
        expanded.append(h_ab + h_ac + h_bc)

    pair_ab = pair_product(v_a, v_b)
    pair_ac = pair_product(v_a, v_c)
    pair_bc = pair_product(v_b, v_c)
    expected = [
        internal + pair_ab[index] + pair_ac[index] + pair_bc[index]
        for index in range(3)
    ]
    assert expanded == expected


def audit_triple_incidence() -> None:
    triples = list(combinations(range(5), 3))
    incidence = [[int(vertex in triple) for vertex in range(5)] for triple in triples]
    assert rational_rank(incidence) == 5
    selected = [incidence[index] for index in (0, 1, 2, 3, 6)]
    assert determinant(selected) == -3

    # If two scalar entries were nonzero, every entry would be nonzero and
    # their reciprocals would lie in this zero kernel, which is impossible.
    assert rational_rank(incidence) == len(incidence[0])


def main() -> None:
    audit_binary_pair_product()
    print("AUDIT PASS: independent Beta determinant and Q0 nondegeneracy")
    audit_representative_hafnian_identity()
    print("AUDIT PASS: independent exact three-support hafnian expansion")
    audit_triple_incidence()
    print("AUDIT PASS: independent five-point triple-incidence rank and minor")
    print("AUDIT SCOPE: stdlib only; imports_primary=0; searches=0; finite_fields=0")
    print("AUDIT BOUNDARY: this replay leaves sizes six through eight")
    print("CURRENT: later packages exclude sizes six and seven; only eight remains")


if __name__ == "__main__":
    main()
