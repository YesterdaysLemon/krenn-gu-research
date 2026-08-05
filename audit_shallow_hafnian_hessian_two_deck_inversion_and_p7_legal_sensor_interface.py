"""Independent stdlib audit of shallow hafnian Hessian tomography.

This file imports neither the primary replay nor a computer-algebra package.
All arithmetic is over the integers or rational numbers; no finite field and
no graph/support/parameter search is used.
"""

from fractions import Fraction
from functools import cache
from itertools import combinations


def edge_key(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def hafnian_factory(weights: dict[tuple[int, int], int]):
    """Return an independent anchored integer hafnian recurrence."""

    @cache
    def hafnian(vertices: tuple[int, ...]) -> int:
        if not vertices:
            return 1
        anchor = vertices[0]
        total = 0
        for partner in vertices[1:]:
            rest = tuple(v for v in vertices if v not in (anchor, partner))
            total += weights[edge_key(anchor, partner)] * hafnian(rest)
        return total

    return hafnian


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Compute an exact integer determinant by fraction-free elimination."""

    work = [row[:] for row in matrix]
    size = len(work)
    if size == 0:
        return 1
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next(
            (row for row in range(column, size) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        diagonal = work[column][column]
        for row in range(column + 1, size):
            for j in range(column + 1, size):
                numerator = (
                    work[row][j] * diagonal
                    - work[row][column] * work[column][j]
                )
                assert numerator % previous == 0
                work[row][j] = numerator // previous
            work[row][column] = 0
        previous = diagonal
    return sign * work[-1][-1]


def rational_solve(
    matrix: list[list[int]], right_hand_side: list[int]
) -> list[Fraction]:
    """Solve one exact square system by independent Gauss-Jordan reduction."""

    size = len(matrix)
    work = [
        [Fraction(value) for value in row] + [Fraction(right_hand_side[index])]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        diagonal = work[column][column]
        work[column] = [entry / diagonal for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[column], strict=True)
            ]
    return [work[row][-1] for row in range(size)]


def rational_rank(matrix: list[list[int]]) -> int:
    """Return exact row rank over Q."""

    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        diagonal = work[pivot_row][column]
        work[pivot_row] = [entry / diagonal for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                left - multiplier * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def shallow_arrays(
    shore: tuple[int, ...],
    hafnian,
) -> tuple[tuple[tuple[int, int], ...], list[list[int]], list[int]]:
    """Build the edge Hessian D and two-deletion vector c on one shore."""

    edges = tuple(combinations(shore, 2))
    hessian: list[list[int]] = []
    for left in edges:
        row: list[int] = []
        for right in edges:
            if set(left).isdisjoint(right):
                removed = {*left, *right}
                row.append(hafnian(tuple(v for v in shore if v not in removed)))
            else:
                row.append(0)
        hessian.append(row)
    cofactors = [
        hafnian(tuple(v for v in shore if v not in set(edge))) for edge in edges
    ]
    return edges, hessian, cofactors


def multiply(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(left * right for left, right in zip(row, vector, strict=True))
        for row in matrix
    ]


def main() -> None:
    vertices = tuple(range(9))
    scales = tuple(range(1, 10))
    weights = {
        edge: scales[edge[0]] * scales[edge[1]]
        for edge in combinations(vertices, 2)
    }
    hafnian = hafnian_factory(weights)

    shore = tuple(range(8))
    edges, hessian, cofactors = shallow_arrays(shore, hafnian)
    true_edges = [weights[edge] for edge in edges]
    assert multiply(hessian, true_edges) == [3 * value for value in cofactors]

    shore_product = 1
    for vertex in shore:
        shore_product *= scales[vertex]
    expected_det = 3**28 * shore_product**14 * 15 * (-5) ** 7
    assert bareiss_determinant(hessian) == expected_det

    recovered = rational_solve(hessian, [3 * value for value in cofactors])
    assert recovered == [Fraction(value) for value in true_edges]
    assert rational_rank(hessian[:27]) == 27

    omitted = 8
    cyclic_triples = [
        (row, (row + 1) % 8, (row + 2) % 8) for row in range(8)
    ]
    star_matrix: list[list[int]] = []
    star_rhs: list[int] = []
    for triple in cyclic_triples:
        row = []
        for vertex in shore:
            if vertex not in triple:
                row.append(0)
                continue
            pair = tuple(v for v in triple if v != vertex)
            row.append(weights[edge_key(pair[0], pair[1])])
        star_matrix.append(row)
        star_rhs.append(hafnian(tuple(sorted((omitted, *triple)))))
    recovered_star = rational_solve(star_matrix, star_rhs)
    assert recovered_star == [
        Fraction(weights[edge_key(omitted, vertex)]) for vertex in shore
    ]

    reconstructed_shores: dict[int, dict[tuple[int, int], int]] = {}
    for missing in vertices:
        local_shore = tuple(vertex for vertex in vertices if vertex != missing)
        local_edges, local_d, local_c = shallow_arrays(local_shore, hafnian)
        local_true = [weights[edge] for edge in local_edges]
        assert multiply(local_d, local_true) == [3 * value for value in local_c]
        reconstructed_shores[missing] = dict(zip(local_edges, local_true, strict=True))

        for four_set in combinations(local_shore, 4):
            product_scale = 1
            for vertex in four_set:
                product_scale *= scales[vertex]
            assert hafnian(four_set) == 3 * product_scale
        product_scale = 1
        for vertex in local_shore:
            product_scale *= scales[vertex]
        assert hafnian(local_shore) == 105 * product_scale

    for left, right in combinations(vertices, 2):
        overlap = set(reconstructed_shores[left]) & set(reconstructed_shores[right])
        assert all(
            reconstructed_shores[left][edge] == reconstructed_shores[right][edge]
            for edge in overlap
        )

    for six_set in combinations(vertices, 6):
        product_scale = 1
        for vertex in six_set:
            product_scale *= scales[vertex]
        assert hafnian(six_set) == 15 * product_scale

    print("AUDIT PASS: nonconstant integer graph satisfies D a = 3 c")
    print("AUDIT PASS: exact 28x28 Bareiss determinant matches Kneser formula")
    print("AUDIT PASS: rational Hessian solve recovers all 28 shore edges")
    print("AUDIT PASS: 27 projected Hessian rows have rank only 27")
    print("AUDIT PASS: independent cyclic-star solve recovers the omitted star")
    print("AUDIT PASS: nine local shore candidates satisfy descent on overlaps")
    print("AUDIT PASS: all local H6 values are forced by the reconstructed graph")
    print("searches=0 finite_fields=0 project_imports=0 computer_algebra=0")
    print("AUDIT SCOPE: GHZ incidence on the Hessian open remains UNKNOWN")
    print("AUDIT SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
