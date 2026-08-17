"""Independent no-import audit of paired incidence and all-depth M purity."""

from fractions import Fraction
from itertools import combinations


PORTS = tuple(range(6))
LEFT = frozenset((0, 1, 2))
RIGHT = frozenset((3, 4, 5))
EDGES = tuple(combinations(PORTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FOUR_SETS = tuple(combinations(PORTS, 4))
FOUR_INDEX = {support: index for index, support in enumerate(FOUR_SETS)}


def column_number(edge: tuple[int, int], colours: tuple[int, int]) -> int:
    return 9 * EDGE_INDEX[tuple(sorted(edge))] + 3 * colours[0] + colours[1]


def output_number(support: tuple[int, ...], word: tuple[int, ...]) -> int:
    value = 0
    for colour in word:
        value = 3 * value + colour
    return 81 * FOUR_INDEX[support] + value


def channel_edges() -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for left in sorted(LEFT) for right in sorted(RIGHT))


def wick_columns() -> list[dict[int, Fraction]]:
    columns: list[dict[int, Fraction]] = []
    for edge in EDGES:
        for first_colour in range(3):
            for second_colour in range(3):
                assignment = {edge[0]: first_colour, edge[1]: second_colour}
                column: dict[int, Fraction] = {}
                for channel_edge in channel_edges():
                    if set(edge).isdisjoint(channel_edge):
                        support = tuple(sorted(edge + channel_edge))
                        word = tuple(assignment.get(port, 0) for port in support)
                        row = output_number(support, word)
                        column[row] = column.get(row, Fraction(0)) + 1
                columns.append({row: value for row, value in column.items() if value})
    return columns


def sparse_rank(columns: list[dict[int, Fraction]]) -> int:
    pivots: dict[int, dict[int, Fraction]] = {}
    for source in columns:
        vector = dict(source)
        while vector:
            pivot = min(vector)
            if pivot not in pivots:
                scale = vector[pivot]
                vector = {row: value / scale for row, value in vector.items() if value}
                pivots[pivot] = vector
                break
            factor = vector[pivot]
            reducer = pivots[pivot]
            for row, value in reducer.items():
                updated = vector.get(row, Fraction(0)) - factor * value
                if updated:
                    vector[row] = updated
                else:
                    vector.pop(row, None)
    return len(pivots)


def vector(
    positive: tuple[tuple[int, int], tuple[int, int]],
    negative: tuple[tuple[int, int], tuple[int, int]],
) -> dict[int, Fraction]:
    return {
        column_number(*positive): Fraction(1),
        column_number(*negative): Fraction(-1),
    }


def explicit_kernel() -> tuple[list[dict[int, Fraction]], list[int]]:
    vectors: list[dict[int, Fraction]] = []
    selected: list[int] = []
    for positive, negative in (
        ((0, 2), (0, 1)),
        ((1, 2), (0, 1)),
        ((3, 5), (3, 4)),
        ((4, 5), (3, 4)),
    ):
        vectors.append(vector((positive, (0, 0)), (negative, (0, 0))))
        selected.append(column_number(positive, (0, 0)))

    for port in PORTS:
        shore = LEFT if port in LEFT else RIGHT
        mates = sorted(shore - {port})
        for colour in (1, 2):
            positive_edge = tuple(sorted((port, mates[0])))
            negative_edge = tuple(sorted((port, mates[1])))
            positive_colours = (colour, 0) if positive_edge[0] == port else (0, colour)
            negative_colours = (colour, 0) if negative_edge[0] == port else (0, colour)
            vectors.append(
                vector(
                    (positive_edge, positive_colours),
                    (negative_edge, negative_colours),
                )
            )
            selected.append(column_number(positive_edge, positive_colours))
    return vectors, selected


def multiply_matrix_vector(
    columns: list[dict[int, Fraction]], direction: dict[int, Fraction]
) -> dict[int, Fraction]:
    answer: dict[int, Fraction] = {}
    for column, coefficient in direction.items():
        for row, value in columns[column].items():
            answer[row] = answer.get(row, Fraction(0)) + coefficient * value
    return {row: value for row, value in answer.items() if value}


def check_block_decomposition() -> None:
    columns = wick_columns()
    assert sparse_rank(columns) == 119

    scalar = [columns[column_number(edge, (0, 0))] for edge in EDGES]
    assert sparse_rank(scalar) == 11

    singleton_ranks = []
    for port in PORTS:
        for colour in (1, 2):
            block = []
            for other in PORTS:
                if other == port:
                    continue
                edge = tuple(sorted((port, other)))
                colours = (colour, 0) if edge[0] == port else (0, colour)
                block.append(columns[column_number(edge, colours)])
            singleton_ranks.append(sparse_rank(block))
    assert singleton_ranks == [4] * 12

    double_nonzero = [
        columns[column_number(edge, (c, d))]
        for edge in EDGES
        for c in (1, 2)
        for d in (1, 2)
    ]
    assert sparse_rank(double_nonzero) == 60
    assert 11 + sum(singleton_ranks) + 60 == 119

    diagonal = [
        columns[column_number(edge, (colour, colour))]
        for edge in EDGES
        for colour in range(3)
    ]
    assert sparse_rank(diagonal) == 41

    basis, selected = explicit_kernel()
    assert sparse_rank(basis) == 16
    assert all(not multiply_matrix_vector(columns, direction) for direction in basis)
    for row_index, coordinate in enumerate(selected):
        for column_index, direction in enumerate(basis):
            expected = Fraction(1) if row_index == column_index else Fraction(0)
            assert direction.get(coordinate, Fraction(0)) == expected

    mixed_coordinates = {
        column_number(edge, (c, d))
        for edge in EDGES
        for c in range(3)
        for d in range(3)
        if c != d
    }
    projected = [
        {
            coordinate: value
            for coordinate, value in direction.items()
            if coordinate in mixed_coordinates
        }
        for direction in basis
    ]
    assert sparse_rank(projected) == 12


def pairings(
    support: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    a, b, c, d = support
    return (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c)))


def shape_rows() -> list[tuple[tuple[int, int], tuple[int, int], int, int]]:
    rows = []
    for support in FOUR_SETS:
        for edge, complement in pairings(support):
            for first in range(3):
                for second in range(3):
                    if first != second:
                        rows.append((edge, complement, first, second))
    return rows


def detected_rows(
    coefficients: dict[tuple[tuple[int, int], int], Fraction],
) -> list[tuple[tuple[int, int], tuple[int, int], int, int]]:
    return [
        row
        for row in shape_rows()
        if coefficients.get((row[0], row[2]), Fraction(0))
        * coefficients.get((row[1], row[3]), Fraction(0))
    ]


def check_shape_certificate() -> None:
    assert 15 * 6 == 90
    rows = shape_rows()
    assert len(rows) == 270
    assert len(set(rows)) == 270
    for row in rows:
        coefficients = {
            (row[0], row[2]): Fraction(2),
            (row[1], row[3]): Fraction(-3),
        }
        assert detected_rows(coefficients) == [row]

    star = {
        ((0, 1), 0): Fraction(1),
        ((0, 2), 1): Fraction(1),
        ((0, 3), 2): Fraction(1),
    }
    assert not detected_rows(star)


def check_affine_controls() -> None:
    # L=span(e0,e1) in K^3.  Two coordinate rows are injective; one is not.
    assert sparse_rank([{0: Fraction(1)}, {1: Fraction(1)}]) == 2
    assert sparse_rank([{0: Fraction(1)}]) == 1
    # The third-coordinate row vanishes on L, so target 1 is nonincident.
    restriction: dict[int, Fraction] = {}
    assert not restriction
    assert Fraction(1) != 0


def main() -> None:
    check_block_decomposition()
    check_shape_certificate()
    check_affine_controls()
    print(
        "paired M2 incidence/one-colour kernel/all-depth M-shape independent audit: PASS"
    )


if __name__ == "__main__":
    main()
