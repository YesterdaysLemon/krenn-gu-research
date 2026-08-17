"""Primary exact replay for paired M2 incidence and all-depth M purity."""

from itertools import combinations

import sympy as sp


PORTS = tuple(range(6))
LEFT = frozenset((0, 1, 2))
RIGHT = frozenset((3, 4, 5))
EDGES = tuple(combinations(PORTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FOUR_SETS = tuple(combinations(PORTS, 4))
FOUR_INDEX = {support: index for index, support in enumerate(FOUR_SETS)}


def column_index(edge: tuple[int, int], colours: tuple[int, int]) -> int:
    return 9 * EDGE_INDEX[tuple(sorted(edge))] + 3 * colours[0] + colours[1]


def row_index(support: tuple[int, ...], word: tuple[int, ...]) -> int:
    word_index = 0
    for colour in word:
        word_index = 3 * word_index + colour
    return 81 * FOUR_INDEX[support] + word_index


def cross_edges() -> tuple[tuple[int, int], ...]:
    return tuple((u, v) for u in sorted(LEFT) for v in sorted(RIGHT))


def wick_matrix() -> sp.SparseMatrix:
    entries: dict[tuple[int, int], int] = {}
    for edge in EDGES:
        for colours in ((c, d) for c in range(3) for d in range(3)):
            column = column_index(edge, colours)
            edge_colours = dict(zip(edge, colours, strict=True))
            for channel_edge in cross_edges():
                if set(edge).isdisjoint(channel_edge):
                    support = tuple(sorted(edge + channel_edge))
                    word = tuple(edge_colours.get(port, 0) for port in support)
                    entries[(row_index(support, word), column)] = 1
    return sp.SparseMatrix(1215, 135, entries)


def direction(
    positive: tuple[tuple[int, int], tuple[int, int]],
    negative: tuple[tuple[int, int], tuple[int, int]],
) -> sp.SparseMatrix:
    vector = sp.MutableSparseMatrix(135, 1, {})
    vector[column_index(*positive)] = 1
    vector[column_index(*negative)] = -1
    return sp.SparseMatrix(vector)


def kernel_basis() -> tuple[sp.SparseMatrix, list[int]]:
    vectors: list[sp.SparseMatrix] = []
    selected: list[int] = []
    pure_pairs = (
        ((0, 2), (0, 1)),
        ((1, 2), (0, 1)),
        ((3, 5), (3, 4)),
        ((4, 5), (3, 4)),
    )
    for positive, negative in pure_pairs:
        vectors.append(direction((positive, (0, 0)), (negative, (0, 0))))
        selected.append(column_index(positive, (0, 0)))

    for port in PORTS:
        shore = LEFT if port in LEFT else RIGHT
        mates = sorted(shore - {port})
        for colour in (1, 2):
            positive_edge = tuple(sorted((port, mates[0])))
            negative_edge = tuple(sorted((port, mates[1])))
            positive_colours = (colour, 0) if positive_edge[0] == port else (0, colour)
            negative_colours = (colour, 0) if negative_edge[0] == port else (0, colour)
            vectors.append(
                direction(
                    (positive_edge, positive_colours),
                    (negative_edge, negative_colours),
                )
            )
            selected.append(column_index(positive_edge, positive_colours))

    return sp.SparseMatrix.hstack(*vectors), selected


def check_tensor_kernel() -> None:
    matrix = wick_matrix()
    assert matrix.rank() == 119
    assert 135 - matrix.rank() == 16

    diagonal_columns = [
        column_index(edge, (colour, colour)) for edge in EDGES for colour in range(3)
    ]
    assert matrix[:, diagonal_columns].rank() == 41
    assert len(diagonal_columns) - matrix[:, diagonal_columns].rank() == 4

    basis, selected = kernel_basis()
    assert basis.rank() == 16
    assert matrix * basis == sp.zeros(1215, 16)
    restriction = basis[selected, :]
    assert restriction == sp.eye(16)
    assert restriction.det() == 1

    mixed_coordinates = [
        column_index(edge, (c, d))
        for edge in EDGES
        for c in range(3)
        for d in range(3)
        if c != d
    ]
    assert basis[mixed_coordinates, :].rank() == 12


def check_affine_trichotomy() -> None:
    kernel_space = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    base = sp.Matrix([3, 5, 7])

    injective_rows = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    target = injective_rows * base + sp.Matrix([2, -4])
    restricted = injective_rows * kernel_space
    assert restricted.rank() == 2
    lift = restricted.inv() * (target - injective_rows * base)
    assert base + kernel_space * lift == sp.Matrix([5, 1, 7])

    one_row = sp.Matrix([[1, 0, 0]])
    assert (one_row * kernel_space).rank() == 1
    assert len((one_row * kernel_space).nullspace()) == 1

    nonincident_row = sp.Matrix([[0, 0, 1]])
    assert nonincident_row * kernel_space == sp.zeros(1, 2)
    assert sp.Matrix([8]) - nonincident_row * base not in sp.zeros(1, 2).columnspace()


def perfect_matchings(
    four_set: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    a, b, c, d = four_set
    return (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )


def mixed_four_rows() -> set[
    tuple[tuple[int, ...], tuple[int, int], tuple[int, int], int, int]
]:
    rows = set()
    for support in FOUR_SETS:
        for edge, complement in perfect_matchings(support):
            for colour in range(3):
                for other_colour in range(3):
                    if colour != other_colour:
                        rows.add((support, edge, complement, colour, other_colour))
    return rows


def active_mixed_rows(
    coefficients: dict[tuple[tuple[int, int], int], int],
) -> set[tuple[tuple[int, ...], tuple[int, int], tuple[int, int], int, int]]:
    return {
        row
        for row in mixed_four_rows()
        if coefficients.get((row[1], row[3]), 0) * coefficients.get((row[2], row[4]), 0)
        != 0
    }


def check_mixed_shape_ledger() -> None:
    pair_rows = {
        (edge, c, d) for edge in EDGES for c in range(3) for d in range(3) if c != d
    }
    four_rows = mixed_four_rows()
    assert len(pair_rows) == 90
    assert len(four_rows) == 270

    for row in four_rows:
        coefficients = {(row[1], row[3]): 1, (row[2], row[4]): 1}
        assert active_mixed_rows(coefficients) == {row}

    two_colour_star = {
        ((0, 1), 0): 2,
        ((0, 2), 0): -3,
        ((0, 3), 1): 5,
        ((0, 4), 1): 7,
    }
    three_colour_star = {
        ((0, 1), 0): 1,
        ((0, 2), 1): 1,
        ((0, 3), 2): 1,
    }
    assert not active_mixed_rows(two_colour_star)
    assert not active_mixed_rows(three_colour_star)

    detector = {((0, 1), 0): 2, ((2, 3), 1): -3}
    active = active_mixed_rows(detector)
    assert len(active) == 1
    assert next(iter(active))[3:] == (0, 1)


def main() -> None:
    check_tensor_kernel()
    check_affine_trichotomy()
    check_mixed_shape_ledger()
    print("paired M2 incidence/one-colour kernel/all-depth M-shape primary: PASS")


if __name__ == "__main__":
    main()
