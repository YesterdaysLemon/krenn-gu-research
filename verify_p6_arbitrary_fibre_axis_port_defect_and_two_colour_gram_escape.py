"""Exact checks for the P6 arbitrary-fibre axis port-defect theorem."""

from functools import cache
from itertools import combinations

import sympy as sp

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
PORT_INDICES = CROSS_INDICES + WINDOW_INDICES
FACE_COLUMNS = (
    (14, -24, 20, 15, -29, 9),
    (10, -33, 36, 30, -58, 18),
    (2, 38, -45, -30, 73, -23),
)


def edge(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def hafnian(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], sp.Expr]
) -> sp.Expr:
    @cache
    def rec(remaining: tuple[int, ...]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        first = remaining[0]
        total = sp.Integer(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += weights[edge(first, partner)] * rec(rest)
        return sp.expand(total)

    return rec(vertices)


def boundary_graph(
    face_column: tuple[int, ...],
) -> dict[tuple[int, int], sp.Expr]:
    weights: dict[tuple[int, int], sp.Expr] = {}
    for pair in combinations(CORE, 2):
        weights[pair] = sp.Integer(1)
    for core_vertex in CORE:
        for port in WINDOW:
            weights[(core_vertex, port)] = sp.Integer(0)
    for pair, value in zip(WINDOW_PAIRS, face_column, strict=True):
        weights[pair] = sp.Rational(value, 3)
    return weights


def axis_matrix(
    majority_first: dict[tuple[int, int], sp.Expr],
    majority_second: dict[tuple[int, int], sp.Expr],
) -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for face in FACES:
        for singleton in face:
            row = [sp.Integer(0)] * len(DIRECTED_EDGES)
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
            row = [sp.Integer(0)] * len(DIRECTED_EDGES)
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
    return sp.Matrix(rows)


def fibre_and_axis_checks() -> tuple[
    dict[tuple[int, int], sp.Expr], ...
]:
    graphs = tuple(boundary_graph(column) for column in FACE_COLUMNS)
    for graph, column in zip(graphs, FACE_COLUMNS, strict=True):
        assert hafnian(CORE, graph) == 3
        for face, target in zip(FACES, column, strict=True):
            assert hafnian(face, graph) == target

    assert len(CORE_INDICES) == 12
    assert len(CROSS_INDICES) == 32
    assert len(WINDOW_INDICES) == 12
    assert len(PORT_INDICES) == 44

    row_indices = tuple(range(72))
    for first, second in combinations(range(3), 2):
        matrix = axis_matrix(graphs[first], graphs[second])
        core_matrix = matrix.extract(row_indices, CORE_INDICES)
        cross_matrix = matrix.extract(row_indices, CROSS_INDICES)
        window_matrix = matrix.extract(row_indices, WINDOW_INDICES)
        assert matrix.shape == (72, 56)
        assert core_matrix.rank() == 7
        assert cross_matrix == sp.zeros(72, 32)
        assert window_matrix.rank() == 12
        assert matrix.rank() == 19
        defect = 44 - matrix.rank() + core_matrix.rank()
        assert defect == 32
        assert 56 - matrix.rank() == 37
    print(
        "boundary scalar fibre has axis ranks (19,7), "
        "nullity 37, and port defect 32: PASS"
    )
    return graphs


def four_deck_checks() -> None:
    symbols = sp.symbols("b45 b46 b47 b56 b57 b67")
    graph: dict[tuple[int, int], sp.Expr] = {}
    for pair in combinations(CORE, 2):
        graph[pair] = sp.Integer(1)
    for core_vertex in CORE:
        for port in WINDOW:
            graph[(core_vertex, port)] = sp.Integer(0)
    for pair, symbol in zip(WINDOW_PAIRS, symbols, strict=True):
        graph[pair] = symbol

    assert hafnian(CORE, graph) == 3
    assert hafnian((0, 1, 2, 4), graph) == 0
    assert hafnian((0, 1, 4, 5), graph) == symbols[0]
    assert hafnian((0, 4, 5, 6), graph) == 0
    expected_window = (
        symbols[0] * symbols[5]
        + symbols[1] * symbols[4]
        + symbols[2] * symbols[3]
    )
    assert hafnian(WINDOW, graph) == expected_window
    print("symbolic five-type H4 deck formula: PASS")


def coloured_matching(
    colours: dict[int, int],
    x_matrix: sp.Matrix,
    y_matrix: sp.Matrix,
    beta_c: sp.Expr,
    beta_d: sp.Expr,
) -> sp.Expr:
    face = (0, 1, 2, 3, 4, 5)
    port_index = {4: 0, 5: 1}

    def block_value(left: int, right: int) -> sp.Expr:
        if left > right:
            left, right = right, left
        left_colour = colours[left]
        right_colour = colours[right]
        if left in CORE and right in CORE:
            return (
                sp.Integer(1)
                if left_colour == right_colour
                else sp.Integer(0)
            )
        if left in WINDOW and right in WINDOW:
            if left_colour != right_colour:
                return sp.Integer(0)
            return beta_c if left_colour == 0 else beta_d

        core_vertex = left
        port = right
        core_colour = left_colour
        port_colour = right_colour
        if core_colour == port_colour:
            return sp.Integer(0)
        if core_colour == 0 and port_colour == 1:
            return x_matrix[core_vertex, port_index[port]]
        return y_matrix[core_vertex, port_index[port]]

    @cache
    def rec(remaining: tuple[int, ...]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        first = remaining[0]
        total = sp.Integer(0)
        for position in range(1, len(remaining)):
            partner = remaining[position]
            rest = remaining[1:position] + remaining[position + 1 :]
            total += block_value(first, partner) * rec(rest)
        return sp.expand(total)

    return rec(face)


def symbolic_coefficient_checks() -> None:
    d_matrix = sp.ones(4) - sp.eye(4)
    x_symbols = sp.symbols("x0:8")
    y_symbols = sp.symbols("z0:8")
    x_matrix = sp.Matrix(4, 2, x_symbols)
    y_matrix = sp.Matrix(4, 2, y_symbols)
    target = sp.symbols("t", nonzero=True)

    window_pair_colours = {
        vertex: (0 if vertex in CORE else 1)
        for vertex in (0, 1, 2, 3, 4, 5)
    }
    coefficient = coloured_matching(
        window_pair_colours,
        x_matrix,
        y_matrix,
        sp.symbols("bc"),
        target / 3,
    )
    expected = target + (x_matrix.T * d_matrix * x_matrix)[0, 1]
    assert sp.expand(coefficient - expected) == 0

    singleton_window = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    singleton_window[4] = 1
    assert (
        coloured_matching(
            singleton_window,
            x_matrix,
            y_matrix,
            sp.symbols("bc"),
            sp.symbols("bd"),
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
            sp.symbols("bc"),
            sp.symbols("bd"),
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
        sp.symbols("bc"),
        sp.symbols("bd"),
    )
    expected = y_matrix[0, 1] * (d_matrix * x_matrix)[0, 0]
    assert sp.expand(coefficient - expected) == 0
    print("symbolic 5+1, window-pair 4+2, and mixed-location residuals: PASS")


def gram_and_product_checks() -> None:
    d_matrix = sp.ones(4) - sp.eye(4)
    expected_determinants = (-78300, -349884, 2409300)
    expected_products = (
        (126, 696, 300),
        (180, 1914, 1080),
        (-46, 2774, 1350),
    )
    assert d_matrix.det() == -3

    for column, expected_det, product_target in zip(
        FACE_COLUMNS,
        expected_determinants,
        expected_products,
        strict=True,
    ):
        q_matrix = sp.zeros(4)
        for (left, right), value in zip(WINDOW_PAIRS, column, strict=True):
            q_matrix[left - 4, right - 4] = -value
            q_matrix[right - 4, left - 4] = -value
        assert q_matrix.det() == expected_det
        products = (
            column[0] * column[5],
            column[1] * column[4],
            column[2] * column[3],
        )
        assert products == product_target
        assert len(set(products)) > 1

    monomial_scalars = sp.symbols("m0:4", nonzero=True)
    monomial = sp.diag(*monomial_scalars)
    gram = monomial.T * d_matrix * monomial
    complement_products = (
        gram[0, 1] * gram[2, 3],
        gram[0, 2] * gram[1, 3],
        gram[0, 3] * gram[1, 2],
    )
    common_product = sp.prod(monomial_scalars)
    assert all(
        sp.expand(product - common_product) == 0
        for product in complement_products
    )
    print("nondegenerate Gram data and complementary-product boundary: PASS")


def main() -> None:
    fibre_and_axis_checks()
    four_deck_checks()
    symbolic_coefficient_checks()
    gram_and_product_checks()
    print("P6 arbitrary-fibre axis/Gram escape primary verification: PASS")


if __name__ == "__main__":
    main()
