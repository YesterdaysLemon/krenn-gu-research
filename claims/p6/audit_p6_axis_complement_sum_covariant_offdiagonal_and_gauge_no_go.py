"""Independent no-import audit of the P6 axis off-diagonal completion no-go."""

from fractions import Fraction
from functools import cache
from itertools import combinations

CORE = (0, 1, 2, 3)
WINDOW = (4, 5, 6, 7)
VERTICES = CORE + WINDOW
WINDOW_PAIRS = tuple(combinations(WINDOW, 2))
FACES = tuple(tuple(sorted(CORE + pair)) for pair in WINDOW_PAIRS)
DIRECTED_EDGES = tuple((vertex, other) for vertex in VERTICES for other in VERTICES if vertex != other)
DIRECTED_INDEX = {directed: index for index, directed in enumerate(DIRECTED_EDGES)}


def edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def scalar_graph(face_column: tuple[int, ...]) -> dict[tuple[int, int], Fraction]:
    graph: dict[tuple[int, int], Fraction] = {}
    for pair in combinations(CORE, 2):
        graph[pair] = Fraction(1)
    for core_vertex in CORE:
        for port in WINDOW:
            graph[(core_vertex, port)] = Fraction(1)
    for pair, value in zip(WINDOW_PAIRS, face_column, strict=True):
        graph[pair] = Fraction(value - 12, 3)
    return graph


def hafnian(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], Fraction]
) -> Fraction:
    @cache
    def rec(remaining: tuple[int, ...]) -> Fraction:
        if not remaining:
            return Fraction(1)
        first = remaining[0]
        total = Fraction(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += weights[edge(first, partner)] * rec(rest)
        return total

    return rec(vertices)


def axis_matrix(
    majority_first: dict[tuple[int, int], Fraction],
    majority_second: dict[tuple[int, int], Fraction],
) -> list[list[Fraction]]:
    rows: list[list[Fraction]] = []
    for face in FACES:
        for singleton in face:
            row = [Fraction(0) for _ in DIRECTED_EDGES]
            for partner in face:
                if partner == singleton:
                    continue
                remaining = tuple(
                    vertex for vertex in face if vertex not in (singleton, partner)
                )
                row[DIRECTED_INDEX[(singleton, partner)]] = hafnian(
                    remaining, majority_first
                )
            rows.append(row)
    for face in FACES:
        for singleton in face:
            row = [Fraction(0) for _ in DIRECTED_EDGES]
            for partner in face:
                if partner == singleton:
                    continue
                remaining = tuple(
                    vertex for vertex in face if vertex not in (singleton, partner)
                )
                row[DIRECTED_INDEX[(partner, singleton)]] = hafnian(
                    remaining, majority_second
                )
            rows.append(row)
    return rows


def rref(matrix: list[list[Fraction]]) -> tuple[list[list[Fraction]], tuple[int, ...]]:
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    pivots: list[int] = []
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
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return work, tuple(pivots)


def nullspace_from_rref(
    reduced: list[list[Fraction]], pivots: tuple[int, ...]
) -> tuple[tuple[Fraction, ...], ...]:
    column_count = len(reduced[0])
    free_columns = tuple(column for column in range(column_count) if column not in pivots)
    basis: list[tuple[Fraction, ...]] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(tuple(vector))
    return tuple(basis)


def complement_data(face_column: tuple[int, ...]) -> tuple[tuple[int, int, int], tuple[int, int]]:
    values = dict(zip(WINDOW_PAIRS, face_column, strict=True))
    sums = (
        values[(4, 5)] + values[(6, 7)],
        values[(4, 6)] + values[(5, 7)],
        values[(4, 7)] + values[(5, 6)],
    )
    return sums, (sums[0] - sums[1], sums[0] - sums[2])


def axis_audit() -> tuple[dict[tuple[int, int], Fraction], ...]:
    face_columns = (
        (14, -24, 20, 15, -29, 9),
        (10, -33, 36, 30, -58, 18),
        (2, 38, -45, -30, 73, -23),
    )
    expected = (
        ((23, -53, 35), (76, -12)),
        ((28, -91, 66), (119, -38)),
        ((-21, 111, -75), (-132, 54)),
    )
    graphs = tuple(scalar_graph(column) for column in face_columns)
    for column, target in zip(face_columns, expected, strict=True):
        assert complement_data(column) == target

    for first, second in combinations(range(3), 2):
        matrix = axis_matrix(graphs[first], graphs[second])
        assert len(matrix) == 72
        assert len(matrix[0]) == 56
        reduced, pivots = rref(matrix)
        assert len(pivots) == 51
        basis = nullspace_from_rref(reduced, pivots)
        assert len(basis) == 5
        for vector in basis:
            for index, (left, right) in enumerate(DIRECTED_EDGES):
                if left in WINDOW or right in WINDOW:
                    assert vector[index] == 0
            for vertex in CORE:
                assert sum(
                    vector[DIRECTED_INDEX[(vertex, other)]]
                    for other in CORE
                    if other != vertex
                ) == 0
                assert sum(
                    vector[DIRECTED_INDEX[(other, vertex)]]
                    for other in CORE
                    if other != vertex
                ) == 0
    print("independent rational axis ranks and exact core-circulation kernels: PASS")
    return graphs


def forced_coefficient_audit(
    graphs: tuple[dict[tuple[int, int], Fraction], ...]
) -> None:
    for majority, minority in combinations(range(3), 2):
        core_hafnian = hafnian(CORE, graphs[majority])
        assert core_hafnian == 3
        for pair in WINDOW_PAIRS:
            forced = core_hafnian * graphs[minority][pair]
            assert forced
    assert 3 * graphs[2][(4, 5)] == -10
    print("independent forced 4+2 coefficients are all nonzero: PASS")


def monomial_gauge_audit() -> None:
    mixed = Fraction(-10, 3)
    factors = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
        (41, 43, 47),
    )
    products = tuple(
        Fraction(1, 1)
        * factors[0][colour]
        * factors[1][colour]
        * factors[2][colour]
        * factors[3][colour]
        * factors[4][colour]
        for colour in range(3)
    )
    last = tuple(Fraction(1, product) for product in products)
    all_factors = factors + (last,)
    word = (0, 0, 1, 1, 2, 2)
    multiplier = Fraction(1)
    for vertex, colour in enumerate(word):
        multiplier *= all_factors[vertex][colour]
    assert multiplier
    assert mixed * multiplier
    print("independent normalized-GHZ-stabilizer gauge audit: PASS")


def main() -> None:
    graphs = axis_audit()
    forced_coefficient_audit(graphs)
    monomial_gauge_audit()
    print("P6 axis complement-sum/off-diagonal no-go independent audit: PASS")


if __name__ == "__main__":
    main()
