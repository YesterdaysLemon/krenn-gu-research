"""Independent Fraction audit of the P6 two-shore scalar fibre."""

from fractions import Fraction
from functools import cache
from itertools import combinations, permutations

CORE = (0, 1, 2, 3)
WINDOW = (4, 5, 6, 7)
VERTICES = CORE + WINDOW
WINDOW_PAIRS = tuple(combinations(WINDOW, 2))
FACES = tuple(tuple(sorted(CORE + pair)) for pair in WINDOW_PAIRS)
DIRECTED_EDGES = tuple(
    (left, right)
    for left in VERTICES
    for right in VERTICES
    if left != right
)
DIRECTED_INDEX = {
    directed: index for index, directed in enumerate(DIRECTED_EDGES)
}
FACE_COLUMNS = (
    (14, -24, 20, 15, -29, 9),
    (10, -33, 36, 30, -58, 18),
    (2, 38, -45, -30, 73, -23),
)


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def hyperbolic_factor(
    column: tuple[int, ...],
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    q45, q46, q47, q56, q57, q67 = column
    r5 = Fraction(
        q56 * q47 + q46 * q57 - q45 * q67,
        2 * q46 * q47,
    )
    r6 = Fraction(q56 - r5 * q46, q45)
    r7 = Fraction(q57 - r5 * q47, q45)
    return (
        (Fraction(1), r5, r6, r7),
        (Fraction(0), Fraction(q45), Fraction(q46), Fraction(q47)),
    )


def scalar_graph(
    factor: tuple[tuple[Fraction, ...], tuple[Fraction, ...]],
) -> dict[tuple[int, int], Fraction]:
    r_row, s_row = factor
    graph: dict[tuple[int, int], Fraction] = {}
    for pair in combinations(CORE, 2):
        graph[pair] = Fraction(
            3 if pair == (0, 1) else 1 if pair == (2, 3) else 0
        )
    for position, port in enumerate(WINDOW):
        graph[(0, port)] = r_row[position]
        graph[(1, port)] = s_row[position]
        graph[(2, port)] = Fraction(0)
        graph[(3, port)] = Fraction(0)
    for pair in WINDOW_PAIRS:
        graph[pair] = Fraction(0)
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


def fibre_and_axis_audit() -> tuple[
    tuple[tuple[tuple[Fraction, ...], tuple[Fraction, ...]], ...],
    tuple[dict[tuple[int, int], Fraction], ...],
]:
    factors = tuple(hyperbolic_factor(column) for column in FACE_COLUMNS)
    graphs = tuple(scalar_graph(factor) for factor in factors)
    for factor, graph, column in zip(
        factors, graphs, FACE_COLUMNS, strict=True
    ):
        r_row, s_row = factor
        reconstructed = tuple(
            r_row[left] * s_row[right] + s_row[left] * r_row[right]
            for left, right in combinations(range(4), 2)
        )
        assert reconstructed == tuple(Fraction(value) for value in column)
        assert all(r_row)
        assert sum(bool(value) for value in s_row) == 3
        assert hafnian(CORE, graph) == 3
        for face, target in zip(FACES, column, strict=True):
            assert hafnian(face, graph) == target

    free_directed = tuple(
        directed
        for directed in DIRECTED_EDGES
        if (
            directed[0] in CORE
            and directed[1] in CORE
            and directed not in ((2, 3), (3, 2))
        )
        or (
            (directed[0] in (2, 3) and directed[1] in WINDOW)
            or (directed[0] in WINDOW and directed[1] in (2, 3))
        )
    )
    free_indices = tuple(DIRECTED_INDEX[item] for item in free_directed)
    constrained_indices = tuple(
        index
        for index in range(len(DIRECTED_EDGES))
        if index not in free_indices
    )
    core_indices = tuple(
        index
        for index, (left, right) in enumerate(DIRECTED_EDGES)
        if left in CORE and right in CORE
    )
    assert len(free_indices) == 26

    for first, second in combinations(range(3), 2):
        matrix = axis_matrix(graphs[first], graphs[second])
        free_matrix = select_columns(matrix, free_indices)
        constrained_matrix = select_columns(matrix, constrained_indices)
        core_matrix = select_columns(matrix, core_indices)
        assert not any(value for row in free_matrix for value in row)
        assert rank(constrained_matrix) == 30
        assert rank(matrix) == 30
        assert rank(core_matrix) == 2
        assert 44 - rank(matrix) + rank(core_matrix) == 16
    print("independent exact fibre, coordinate kernel, and defect 16: PASS")
    return factors, graphs


def two_colour_matching(
    colours: dict[int, int],
    factors: tuple[
        tuple[tuple[Fraction, ...], tuple[Fraction, ...]],
        tuple[tuple[Fraction, ...], tuple[Fraction, ...]],
    ],
) -> Fraction:
    face = (0, 1, 2, 3, 4, 5)
    port_index = {4: 0, 5: 1}

    def block_value(left: int, right: int) -> Fraction:
        if left > right:
            left, right = right, left
        left_colour = colours[left]
        right_colour = colours[right]
        same_colour = left_colour == right_colour
        if left in CORE and right in CORE:
            if same_colour:
                if (left, right) == (0, 1):
                    return Fraction(3)
                if (left, right) == (2, 3):
                    return Fraction(1)
                return Fraction(0)
            return Fraction(-1) if (left, right) == (0, 3) else Fraction(0)

        if left in WINDOW and right in WINDOW:
            return Fraction(0)

        core_vertex = left
        port_position = port_index[right]
        if same_colour:
            r_row, s_row = factors[left_colour]
            if core_vertex == 0:
                return r_row[port_position]
            if core_vertex == 1:
                return s_row[port_position]
            return Fraction(0)
        if core_vertex == 2:
            r_row, _ = factors[right_colour]
            return r_row[port_position]
        return Fraction(0)

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


def four_plus_two_audit(
    all_factors: tuple[
        tuple[tuple[Fraction, ...], tuple[Fraction, ...]], ...
    ],
) -> None:
    face_vertices = (0, 1, 2, 3, 4, 5)
    for majority, minority in permutations(range(3), 2):
        factors = (all_factors[majority], all_factors[minority])

        window_minority = {
            vertex: (1 if vertex in CORE else 0)
            for vertex in face_vertices
        }
        assert two_colour_matching(window_minority, factors) == 0

        inactive_pair = {vertex: 0 for vertex in face_vertices}
        inactive_pair[2] = 1
        inactive_pair[3] = 1
        assert two_colour_matching(inactive_pair, factors) == 0

        first_active = {vertex: 0 for vertex in face_vertices}
        first_active[0] = 1
        first_active[5] = 1
        assert two_colour_matching(first_active, factors) == 0

        second_active = {vertex: 0 for vertex in face_vertices}
        second_active[1] = 1
        second_active[5] = 1
        coefficient = two_colour_matching(second_active, factors)
        expected = all_factors[minority][1][1] * all_factors[majority][0][0]
        assert coefficient == expected
        assert expected == FACE_COLUMNS[minority][0]
        assert expected
    print("independent 4+2 transfer and nonzero residual: PASS")


def main() -> None:
    factors, _graphs = fibre_and_axis_audit()
    four_plus_two_audit(factors)
    print("computer_algebra=0")
    print("P6 two-shore scalar-fibre independent audit: PASS")


if __name__ == "__main__":
    main()
