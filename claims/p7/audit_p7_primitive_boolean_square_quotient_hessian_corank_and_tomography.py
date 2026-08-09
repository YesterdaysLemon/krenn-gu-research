"""Independent stdlib audit of primitive P7 quotient-Hessian tomography."""

from fractions import Fraction
from itertools import combinations, product
from math import gcd

VERTICES = tuple(range(8))
EDGES = tuple(combinations(VERTICES, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FOUR_SETS = tuple(combinations(VERTICES, 4))
FOUR_INDEX = {subset: index for index, subset in enumerate(FOUR_SETS)}


def exact_rank(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            tail = [
                pivot_value * work[row][inner]
                - factor * work[pivot_row][inner]
                for inner in range(column, len(work[0]))
            ]
            divisor = 0
            for value in tail:
                divisor = gcd(divisor, abs(value))
            if divisor > 1:
                tail = [value // divisor for value in tail]
            work[row][column:] = tail
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for inner in range(column + 1, size):
                numerator = (
                    work[row][inner] * pivot_value
                    - work[row][column] * work[column][inner]
                )
                assert numerator % previous == 0
                work[row][inner] = numerator // previous
            work[row][column] = 0
        previous = pivot_value
    return sign * work[-1][-1]


def standard_tableaux() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    tableaux = []
    for top in combinations(VERTICES, 4):
        bottom = tuple(vertex for vertex in VERTICES if vertex not in top)
        if all(left < right for left, right in zip(top, bottom, strict=True)):
            tableaux.append((top, bottom))
    return tableaux


def polytabloid(top: tuple[int, ...], bottom: tuple[int, ...]) -> list[int]:
    vector = [0] * len(FOUR_SETS)
    for choices in product((0, 1), repeat=4):
        subset = tuple(
            sorted(
                bottom[index] if choice else top[index]
                for index, choice in enumerate(choices)
            )
        )
        vector[FOUR_INDEX[subset]] += (-1) ** sum(choices)
    return vector


def catalecticant(four_vector: list[int]) -> list[list[int]]:
    matrix = [[0] * len(EDGES) for _ in EDGES]
    for row, edge in enumerate(EDGES):
        for column, other in enumerate(EDGES):
            if set(edge).isdisjoint(other):
                subset = tuple(sorted((*edge, *other)))
                matrix[row][column] = four_vector[FOUR_INDEX[subset]]
    return matrix


def incidence() -> list[list[int]]:
    return [[int(vertex in edge) for vertex in VERTICES] for edge in EDGES]


def multiply(
    left: list[list[int | Fraction]],
    right: list[list[int | Fraction]],
) -> list[list[int | Fraction]]:
    return [
        [
            sum(left[row][middle] * right[middle][column] for middle in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def transpose(matrix: list[list[int | Fraction]]) -> list[list[int | Fraction]]:
    return [list(row) for row in zip(*matrix, strict=True)]


def mat_vec(
    matrix: list[list[int | Fraction]], vector: list[int | Fraction]
) -> list[int | Fraction]:
    return [
        sum(entry * value for entry, value in zip(row, vector, strict=True))
        for row in matrix
    ]


def zero_row_basis() -> list[list[int]]:
    """Integral basis of ker R^T using K7 edges with one sum constraint."""
    special = (5, 6)
    free_edges = [edge for edge in combinations(range(7), 2) if edge != special]
    columns = []
    for free in free_edges:
        vector = [0] * len(EDGES)
        vector[EDGE_INDEX[free]] = 1
        vector[EDGE_INDEX[special]] = -1
        for vertex in range(7):
            row_sum = sum(
                vector[EDGE_INDEX[tuple(sorted((vertex, other)))]]
                for other in range(7)
                if other != vertex
            )
            vector[EDGE_INDEX[(vertex, 7)]] = -row_sum
        columns.append(vector)
    return transpose(columns)


def main() -> None:
    tableaux = standard_tableaux()
    assert len(tableaux) == 14
    primitive = [polytabloid(top, bottom) for top, bottom in tableaux]
    assert exact_rank(primitive) == 14
    control = [sum(vector[index] for vector in primitive) for index in range(70)]

    for triple in combinations(VERTICES, 3):
        assert (
            sum(
                control[FOUR_INDEX[tuple(sorted((*triple, vertex)))]]
                for vertex in VERTICES
                if vertex not in triple
            )
            == 0
        )
    for subset in FOUR_SETS:
        complement = tuple(vertex for vertex in VERTICES if vertex not in subset)
        assert control[FOUR_INDEX[subset]] == control[FOUR_INDEX[complement]]

    vertex_edge = incidence()
    hessian = catalecticant(control)
    assert multiply(hessian, vertex_edge) == [[0] * 8 for _ in range(28)]
    assert exact_rank(vertex_edge) == 8
    assert exact_rank(hessian) == 20

    named_edges = (
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (0, 6),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 4),
        (3, 5),
        (3, 6),
        (4, 5),
        (4, 6),
    )
    indices = [EDGE_INDEX[edge] for edge in named_edges]
    minor = [[hessian[row][column] for column in indices] for row in indices]
    determinant = bareiss_determinant(minor)
    assert determinant == 1_551_182_856_192

    quotient = zero_row_basis()
    assert len(quotient) == 28 and len(quotient[0]) == 20
    assert exact_rank(transpose(quotient)) == 20
    assert multiply(transpose(vertex_edge), quotient) == [[0] * 20 for _ in range(8)]
    quotient_hessian = multiply(multiply(transpose(quotient), hessian), quotient)
    assert bareiss_determinant(quotient_hessian) != 0

    coordinates = [index - 9 for index in range(20)]
    gauge = [2, -1, 3, 0, 4, -2, 1, 5]
    primitive_edge = mat_vec(quotient, coordinates)
    additive_edge = mat_vec(vertex_edge, gauge)
    full_edge = [left + right for left, right in zip(primitive_edge, additive_edge, strict=True)]
    cofactor = [Fraction(value, 3) for value in mat_vec(hessian, full_edge)]
    assert mat_vec(transpose(vertex_edge), cofactor) == [0] * 8
    assert mat_vec(hessian, primitive_edge) == mat_vec(hessian, full_edge)

    compressed = mat_vec(transpose(quotient), cofactor)
    assert mat_vec(quotient_hessian, coordinates) == [3 * value for value in compressed]
    top_scalar = sum(
        value * dual for value, dual in zip(full_edge, cofactor, strict=True)
    ) / 4
    assert 4 * top_scalar == sum(
        value * dual for value, dual in zip(primitive_edge, cofactor, strict=True)
    )
    assert 4 * top_scalar == sum(
        value * dual for value, dual in zip(coordinates, compressed, strict=True)
    )

    print("AUDIT PASS: independent primitive/complement polytabloid rebuild")
    print("AUDIT PASS: eight incidence kernels and exact rank twenty")
    print("AUDIT PASS: Bareiss minor = 2^18*3^6*8117")
    print("AUDIT PASS: independent zero-row quotient and additive gauge")
    print("AUDIT PASS: quotient recovery equation and scalar stress")
    print("imports_from_primary=0 imports_from_project=0 searches=0")
    print("SCOPE: ambient rank-20 control is not asserted physical")
    print("SCOPE: primitive-square quotient-open incidence remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
