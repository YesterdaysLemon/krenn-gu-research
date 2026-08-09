"""Independent no-import audit of the P7 combined-deck double-star theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations


def rational_rank(rows: list[list[int | Fraction]]) -> int:
    """Exact row rank by independent Fraction elimination."""
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
                value - multiplier * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def hafnian(weights: dict[tuple[int, int], Fraction], vertices: tuple[int, ...]) -> Fraction:
    """Independent exact recursive hafnian."""
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    total = Fraction(0)
    for position in range(1, len(vertices)):
        partner = vertices[position]
        edge = tuple(sorted((first, partner)))
        remainder = vertices[1:position] + vertices[position + 1 :]
        total += weights.get(edge, Fraction(0)) * hafnian(weights, remainder)
    return total


def double_star_weights(center: Fraction, scale: Fraction) -> dict[tuple[int, int], Fraction]:
    """A rational member of the c-line times reciprocal-shore family."""
    weights = {(0, 1): center}
    for index, leaf in enumerate(range(2, 9), start=1):
        weights[(0, leaf)] = scale
        weights[(1, leaf)] = Fraction(index, 1) / scale
    return weights


def audit_hafnian_family() -> None:
    """Check fixed representative orders for two distinct fibre points."""
    first = double_star_weights(Fraction(2), Fraction(1))
    second = double_star_weights(Fraction(11), Fraction(3))
    four = (0, 1, 2, 3)
    six = (0, 1, 2, 3, 4, 5)
    eight = (0, 1, 2, 3, 4, 5, 6, 7)
    assert hafnian(first, four) == hafnian(second, four) == 3
    assert hafnian(first, six) == hafnian(second, six) == 0
    assert hafnian(first, eight) == hafnian(second, eight) == 0


def gram_rows(m: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for i, j in combinations(range(m), 2):
        row = [0] * (2 * m)
        row[2 * i] = j + 1
        row[2 * i + 1] = 1
        row[2 * j] = i + 1
        row[2 * j + 1] = 1
        rows.append(row)
    return rows


def audit_ranks() -> None:
    """Repeat all tangent and toric ranks without SymPy or primary imports."""
    m = 7
    gram = gram_rows(m)
    assert rational_rank(gram) == 13

    leaf_edges = list(combinations(range(m), 2))
    edge_index = {edge: index for index, edge in enumerate(leaf_edges)}
    width = len(leaf_edges) + 2 * m + 1
    ambient: list[list[int]] = []
    triangle_rows: list[list[int]] = []
    for triple in combinations(range(m), 3):
        triangle = [0] * len(leaf_edges)
        row = [0] * width
        for edge in combinations(triple, 2):
            triangle[edge_index[edge]] = 1
            row[edge_index[edge]] = 1
        triangle_rows.append(triangle)
        ambient.append(row)
    assert rational_rank(triangle_rows) == 21

    offset = len(leaf_edges)
    for (i, j), gram_row in zip(combinations(range(m), 2), gram, strict=True):
        row = [0] * width
        row[edge_index[(i, j)]] = 1
        row[offset : offset + 2 * m] = gram_row
        ambient.append(row)
    assert rational_rank(ambient) == 34

    incidence: list[list[int]] = []
    for i, j in combinations(range(m), 2):
        row = [1, 1] + [0] * m
        row[2 + i] = 1
        row[2 + j] = 1
        incidence.append(row)
    assert rational_rank(incidence) == 7


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Small exact determinant by elimination."""
    work = [row[:] for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next(row for row in range(column, len(work)) if work[row][column])
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, len(work)):
            multiplier = work[row][column] / pivot_value
            for later in range(column, len(work)):
                work[row][later] -= multiplier * work[column][later]
    return result


def audit_zero_deck_boundary() -> None:
    """Audit the invertibility of the four triple-sum equations."""
    matrix = [
        [Fraction(1), Fraction(1), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(1), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(1), Fraction(1)],
        [Fraction(0), Fraction(1), Fraction(1), Fraction(1)],
    ]
    assert determinant(matrix) == -3
    assert rational_rank(matrix) == 4


def main() -> None:
    audit_hafnian_family()
    print("AUDIT PASS: center edge and reciprocal shore scale leave H4/H6/H8 fixed")
    audit_ranks()
    print("AUDIT PASS: independent ranks 13, 21, 34, and toric exponent rank 7")
    audit_zero_deck_boundary()
    print("AUDIT PASS: four-ratio triple-sum determinant is -3")
    print("AUDIT SCOPE: stdlib only; imports_primary=0; searches=0; support_enumerations=0")
    print("AUDIT BOUNDARY: no claim that the double-star family is a GHZ witness")


if __name__ == "__main__":
    main()
