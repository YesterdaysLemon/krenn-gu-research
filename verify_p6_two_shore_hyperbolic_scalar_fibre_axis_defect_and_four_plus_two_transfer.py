"""Exact checks for the P6 two-shore scalar-fibre theorem."""

from fractions import Fraction
from functools import cache
from itertools import combinations

import sympy as sp

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


def scalar_graph(
    factor: tuple[tuple[Fraction, ...], tuple[Fraction, ...]],
) -> dict[tuple[int, int], sp.Expr]:
    r_row, s_row = factor
    weights: dict[tuple[int, int], sp.Expr] = {}
    for pair in combinations(CORE, 2):
        weights[pair] = sp.Integer(
            3 if pair == (0, 1) else 1 if pair == (2, 3) else 0
        )
    for position, port in enumerate(WINDOW):
        weights[(0, port)] = sp.Rational(r_row[position])
        weights[(1, port)] = sp.Rational(s_row[position])
        weights[(2, port)] = sp.Integer(0)
        weights[(3, port)] = sp.Integer(0)
    for pair in WINDOW_PAIRS:
        weights[pair] = sp.Integer(0)
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


def factor_and_fibre_checks() -> tuple[
    tuple[tuple[tuple[Fraction, ...], tuple[Fraction, ...]], ...],
    tuple[dict[tuple[int, int], sp.Expr], ...],
]:
    expected_factors = (
        (
            (
                Fraction(1),
                Fraction(-29, 32),
                Fraction(-27, 56),
                Fraction(-87, 112),
            ),
            (Fraction(0), Fraction(14), Fraction(-24), Fraction(20)),
        ),
        (
            (
                Fraction(1),
                Fraction(-469, 396),
                Fraction(-109, 120),
                Fraction(-169, 110),
            ),
            (Fraction(0), Fraction(10), Fraction(-33), Fraction(36)),
        ),
        (
            (
                Fraction(1),
                Fraction(-139, 114),
                Fraction(49, 6),
                Fraction(689, 76),
            ),
            (Fraction(0), Fraction(2), Fraction(38), Fraction(-45)),
        ),
    )
    factors = tuple(hyperbolic_factor(column) for column in FACE_COLUMNS)
    assert factors == expected_factors

    graphs = tuple(scalar_graph(factor) for factor in factors)
    for column, factor, graph in zip(
        FACE_COLUMNS, factors, graphs, strict=True
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
        assert all(graph[pair] == 0 for pair in WINDOW_PAIRS)
        assert len(set(column)) > 1
    print("rational hyperbolic factors and exact non-tau scalar fibre: PASS")
    return factors, graphs


def cofactor_and_axis_checks(
    factors: tuple[
        tuple[tuple[Fraction, ...], tuple[Fraction, ...]], ...
    ],
    graphs: tuple[dict[tuple[int, int], sp.Expr], ...],
) -> None:
    for factor, graph, column in zip(
        factors, graphs, FACE_COLUMNS, strict=True
    ):
        r_row, s_row = factor
        face = FACES[0]
        assert hafnian(tuple(v for v in face if v not in (2, 3)), graph) == column[0]
        assert hafnian(tuple(v for v in face if v not in (0, 1)), graph) == 0
        assert hafnian(tuple(v for v in face if v not in (0, 4)), graph) == s_row[1]
        assert hafnian(tuple(v for v in face if v not in (1, 4)), graph) == r_row[1]
        assert hafnian(tuple(v for v in face if v not in (2, 4)), graph) == 0
        assert hafnian(tuple(v for v in face if v not in (4, 5)), graph) == 3

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

    row_indices = tuple(range(72))
    for first, second in combinations(range(3), 2):
        matrix = axis_matrix(graphs[first], graphs[second])
        free_matrix = matrix.extract(row_indices, free_indices)
        constrained_matrix = matrix.extract(row_indices, constrained_indices)
        core_matrix = matrix.extract(row_indices, core_indices)
        assert matrix.shape == (72, 56)
        assert free_matrix == sp.zeros(72, 26)
        assert constrained_matrix.rank() == 30
        assert matrix.rank() == 30
        assert core_matrix.rank() == 2
        assert 56 - matrix.rank() == 26
        assert 44 - matrix.rank() + core_matrix.rank() == 16
    print("coordinate axis kernel, ranks (30,2), and port defect 16: PASS")


def symbolic_two_colour_matching(
    colours: dict[int, int],
    r_rows: tuple[tuple[sp.Expr, sp.Expr], tuple[sp.Expr, sp.Expr]],
    s_rows: tuple[tuple[sp.Expr, sp.Expr], tuple[sp.Expr, sp.Expr]],
) -> sp.Expr:
    face = (0, 1, 2, 3, 4, 5)
    port_index = {4: 0, 5: 1}

    def block_value(left: int, right: int) -> sp.Expr:
        if left > right:
            left, right = right, left
        left_colour = colours[left]
        right_colour = colours[right]
        same_colour = left_colour == right_colour
        if left in CORE and right in CORE:
            if same_colour:
                if (left, right) == (0, 1):
                    return sp.Integer(3)
                if (left, right) == (2, 3):
                    return sp.Integer(1)
                return sp.Integer(0)
            return sp.Integer(-1) if (left, right) == (0, 3) else sp.Integer(0)

        if left in WINDOW and right in WINDOW:
            return sp.Integer(0)

        core_vertex = left
        port = right
        port_position = port_index[port]
        if same_colour:
            if core_vertex == 0:
                return r_rows[left_colour][port_position]
            if core_vertex == 1:
                return s_rows[left_colour][port_position]
            return sp.Integer(0)
        if core_vertex == 2:
            return r_rows[right_colour][port_position]
        return sp.Integer(0)

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


def four_plus_two_transfer_checks() -> None:
    rc = sp.symbols("rc0:2")
    sc = sp.symbols("sc0:2")
    rd = sp.symbols("rd0:2")
    sd = sp.symbols("sd0:2")
    r_rows = (rc, rd)
    s_rows = (sc, sd)

    window_minority = {vertex: (1 if vertex in CORE else 0) for vertex in (0, 1, 2, 3, 4, 5)}
    assert symbolic_two_colour_matching(window_minority, r_rows, s_rows) == 0

    inactive_pair = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    inactive_pair[2] = 1
    inactive_pair[3] = 1
    assert symbolic_two_colour_matching(inactive_pair, r_rows, s_rows) == 0

    first_active_mixed = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    first_active_mixed[0] = 1
    first_active_mixed[4] = 1
    assert symbolic_two_colour_matching(first_active_mixed, r_rows, s_rows) == 0

    second_active_mixed = {vertex: 0 for vertex in (0, 1, 2, 3, 4, 5)}
    second_active_mixed[1] = 1
    second_active_mixed[4] = 1
    residual = symbolic_two_colour_matching(second_active_mixed, r_rows, s_rows)
    assert sp.expand(residual - sd[0] * rc[1]) == 0
    print("three cancelled 4+2 families and exact active-row residual: PASS")


def main() -> None:
    factors, graphs = factor_and_fibre_checks()
    cofactor_and_axis_checks(factors, graphs)
    four_plus_two_transfer_checks()
    print("P6 two-shore scalar-fibre primary verification: PASS")


if __name__ == "__main__":
    main()
