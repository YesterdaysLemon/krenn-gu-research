"""Independent no-import audit of the P6 axis port-defect theorem."""

from fractions import Fraction
from functools import cache
from itertools import combinations

CORE = (0, 1, 2, 3)
WINDOW = (4, 5, 6, 7)
VERTICES = CORE + WINDOW
WINDOW_PAIRS = tuple(combinations(WINDOW, 2))
FACES = tuple(tuple(sorted(CORE + pair)) for pair in WINDOW_PAIRS)
DIRECTED_EDGES = tuple(
    (vertex, other)
    for vertex in VERTICES
    for other in VERTICES
    if vertex != other
)
DIRECTED_INDEX = {
    directed: index for index, directed in enumerate(DIRECTED_EDGES)
}
CORE_INDICES = tuple(
    index
    for index, (left, right) in enumerate(DIRECTED_EDGES)
    if left in CORE and right in CORE
)
CROSS_INDICES = tuple(
    index
    for index, (left, right) in enumerate(DIRECTED_EDGES)
    if (left in CORE) != (right in CORE)
)
WINDOW_INDICES = tuple(
    index
    for index, (left, right) in enumerate(DIRECTED_EDGES)
    if left in WINDOW and right in WINDOW
)
FACE_COLUMNS = (
    (14, -24, 20, 15, -29, 9),
    (10, -33, 36, 30, -58, 18),
    (2, 38, -45, -30, 73, -23),
)


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def boundary_graph(
    face_column: tuple[int, ...],
) -> dict[tuple[int, int], Fraction]:
    graph: dict[tuple[int, int], Fraction] = {}
    for pair in combinations(CORE, 2):
        graph[pair] = Fraction(1)
    for core_vertex in CORE:
        for port in WINDOW:
            graph[(core_vertex, port)] = Fraction(0)
    for pair, value in zip(WINDOW_PAIRS, face_column, strict=True):
        graph[pair] = Fraction(value, 3)
    return graph


def hafnian(
    vertices: tuple[int, ...],
    weights: dict[tuple[int, int], Fraction],
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
                    vertex
                    for vertex in face
                    if vertex not in (singleton, partner)
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
                    vertex
                    for vertex in face
                    if vertex not in (singleton, partner)
                )
                row[DIRECTED_INDEX[(partner, singleton)]] = hafnian(
                    remaining, majority_second
                )
            rows.append(row)
    return rows


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(pivot_row + 1, row_count):
            if not work[row][column]:
                continue
            factor = work[row][column] / pivot_value
            for index in range(column, column_count):
                work[row][index] -= factor * work[pivot_row][index]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def select_columns(
    matrix: list[list[Fraction]], indices: tuple[int, ...]
) -> list[list[Fraction]]:
    return [[row[index] for index in indices] for row in matrix]


def fibre_axis_audit() -> tuple[
    dict[tuple[int, int], Fraction], ...
]:
    graphs = tuple(boundary_graph(column) for column in FACE_COLUMNS)
    for graph, column in zip(graphs, FACE_COLUMNS, strict=True):
        assert hafnian(CORE, graph) == 3
        for face, target in zip(FACES, column, strict=True):
            assert hafnian(face, graph) == target

    assert len(CORE_INDICES) == 12
    assert len(CROSS_INDICES) == 32
    assert len(WINDOW_INDICES) == 12
    for first, second in combinations(range(3), 2):
        matrix = axis_matrix(graphs[first], graphs[second])
        core_matrix = select_columns(matrix, CORE_INDICES)
        cross_matrix = select_columns(matrix, CROSS_INDICES)
        window_matrix = select_columns(matrix, WINDOW_INDICES)
        assert len(matrix) == 72
        assert len(matrix[0]) == 56
        assert rank(core_matrix) == 7
        assert not any(value for row in cross_matrix for value in row)
        assert rank(window_matrix) == 12
        assert rank(matrix) == 19
        defect = 44 - rank(matrix) + rank(core_matrix)
        assert defect == 32
    print("independent Fraction axis ranks and port defect: PASS")
    return graphs


def determinant(matrix: tuple[tuple[int, ...], ...]) -> Fraction:
    work = [[Fraction(value) for value in row] for row in matrix]
    size = len(work)
    result = Fraction(1)
    sign = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        result *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for index in range(column, size):
                work[row][index] -= factor * work[column][index]
    return sign * result


def q_matrix(column: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    rows = [[0 for _ in range(4)] for _ in range(4)]
    for (left, right), value in zip(WINDOW_PAIRS, column, strict=True):
        rows[left - 4][right - 4] = -value
        rows[right - 4][left - 4] = -value
    return tuple(tuple(row) for row in rows)


def gram_audit() -> None:
    d_matrix = (
        (0, 1, 1, 1),
        (1, 0, 1, 1),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
    )
    assert determinant(d_matrix) == -3
    expected_determinants = (-78300, -349884, 2409300)
    expected_products = (
        (126, 696, 300),
        (180, 1914, 1080),
        (-46, 2774, 1350),
    )
    for column, expected_det, target_products in zip(
        FACE_COLUMNS,
        expected_determinants,
        expected_products,
        strict=True,
    ):
        assert determinant(q_matrix(column)) == expected_det
        products = (
            column[0] * column[5],
            column[1] * column[4],
            column[2] * column[3],
        )
        assert products == target_products
        assert len(set(products)) > 1
    print("independent Gram determinants and product boundary: PASS")


def coloured_matching(
    colours: dict[int, int],
    x_matrix: tuple[tuple[Fraction, Fraction], ...],
    y_matrix: tuple[tuple[Fraction, Fraction], ...],
    beta_c: Fraction,
    beta_d: Fraction,
) -> Fraction:
    face = (0, 1, 2, 3, 4, 5)
    port_index = {4: 0, 5: 1}

    def block_value(left: int, right: int) -> Fraction:
        if left > right:
            left, right = right, left
        left_colour = colours[left]
        right_colour = colours[right]
        if left in CORE and right in CORE:
            return Fraction(int(left_colour == right_colour))
        if left in WINDOW and right in WINDOW:
            if left_colour != right_colour:
                return Fraction(0)
            return beta_c if left_colour == 0 else beta_d

        core_vertex = left
        port = right
        core_colour = left_colour
        port_colour = right_colour
        if core_colour == port_colour:
            return Fraction(0)
        if core_colour == 0 and port_colour == 1:
            return x_matrix[core_vertex][port_index[port]]
        return y_matrix[core_vertex][port_index[port]]

    @cache
    def rec(remaining: tuple[int, ...]) -> Fraction:
        if not remaining:
            return Fraction(1)
        first = remaining[0]
        total = Fraction(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += block_value(first, partner) * rec(rest)
        return total

    return rec(face)


def matrix_entry_dx(
    x_matrix: tuple[tuple[Fraction, Fraction], ...],
    row: int,
    column: int,
) -> Fraction:
    return sum(
        x_matrix[other][column] for other in range(4) if other != row
    )


def fixed_matching_audit() -> None:
    x_matrix = (
        (Fraction(2), Fraction(3)),
        (Fraction(5), Fraction(7)),
        (Fraction(11), Fraction(13)),
        (Fraction(17), Fraction(19)),
    )
    y_matrix = (
        (Fraction(23), Fraction(29)),
        (Fraction(31), Fraction(37)),
        (Fraction(41), Fraction(43)),
        (Fraction(47), Fraction(53)),
    )

    window_pair = {
        vertex: (0 if vertex in CORE else 1)
        for vertex in (0, 1, 2, 3, 4, 5)
    }
    gram_offdiag = sum(
        x_matrix[left][0] * x_matrix[right][1]
        for left in range(4)
        for right in range(4)
        if left != right
    )
    coefficient = coloured_matching(
        window_pair,
        x_matrix,
        y_matrix,
        Fraction(5),
        Fraction(14, 3),
    )
    assert coefficient == 14 + gram_offdiag

    singleton_window = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    singleton_window[4] = 1
    assert (
        coloured_matching(
            singleton_window,
            x_matrix,
            y_matrix,
            Fraction(5),
            Fraction(7),
        )
        == 0
    )

    singleton_core = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    singleton_core[0] = 1
    assert (
        coloured_matching(
            singleton_core,
            x_matrix,
            y_matrix,
            Fraction(5),
            Fraction(7),
        )
        == 0
    )

    mixed_location = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    mixed_location[0] = 1
    mixed_location[4] = 1
    coefficient = coloured_matching(
        mixed_location,
        x_matrix,
        y_matrix,
        Fraction(5),
        Fraction(7),
    )
    expected = y_matrix[0][1] * matrix_entry_dx(x_matrix, 0, 0)
    assert coefficient == expected
    print("independent fixed matching identities: PASS")


def four_deck_audit(
    graphs: tuple[dict[tuple[int, int], Fraction], ...],
) -> None:
    graph = graphs[0]
    assert hafnian(CORE, graph) == 3
    assert hafnian((0, 1, 2, 4), graph) == 0
    assert hafnian((0, 1, 4, 5), graph) == Fraction(14, 3)
    assert hafnian((0, 4, 5, 6), graph) == 0
    expected = (
        Fraction(14, 3) * Fraction(9, 3)
        + Fraction(-24, 3) * Fraction(-29, 3)
        + Fraction(20, 3) * Fraction(15, 3)
    )
    assert hafnian(WINDOW, graph) == expected
    print("independent representative H4 deck audit: PASS")


def main() -> None:
    graphs = fibre_axis_audit()
    four_deck_audit(graphs)
    gram_audit()
    fixed_matching_audit()
    print("computer_algebra=0")
    print("P6 arbitrary-fibre axis/Gram escape independent audit: PASS")


if __name__ == "__main__":
    main()
