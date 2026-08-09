"""Primary exact checks for the P6 axis complement-sum tensor no-go."""

from functools import cache
from itertools import combinations

import sympy as sp

CORE = (0, 1, 2, 3)
WINDOW = (4, 5, 6, 7)
VERTICES = CORE + WINDOW
WINDOW_PAIRS = tuple(combinations(WINDOW, 2))
FACES = tuple(tuple(sorted(CORE + pair)) for pair in WINDOW_PAIRS)
DIRECTED_EDGES = tuple((vertex, other) for vertex in VERTICES for other in VERTICES if vertex != other)
DIRECTED_INDEX = {directed: index for index, directed in enumerate(DIRECTED_EDGES)}


def edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


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


def scalar_graph(face_column: tuple[int, ...]) -> dict[tuple[int, int], sp.Expr]:
    weights: dict[tuple[int, int], sp.Expr] = {}
    for pair in combinations(CORE, 2):
        weights[pair] = sp.Integer(1)
    for core_vertex in CORE:
        for port in WINDOW:
            weights[(core_vertex, port)] = sp.Integer(1)
    for pair, value in zip(WINDOW_PAIRS, face_column, strict=True):
        weights[pair] = sp.Rational(value - 12, 3)
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
                    vertex for vertex in face if vertex not in (singleton, partner)
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
                    vertex for vertex in face if vertex not in (singleton, partner)
                )
                row[DIRECTED_INDEX[(partner, singleton)]] = hafnian(
                    remaining, majority_second
                )
            rows.append(row)
    return sp.Matrix(rows)


def complement_covariant(face_column: tuple[int, ...]) -> tuple[int, int]:
    values = dict(zip(WINDOW_PAIRS, face_column, strict=True))
    first = values[(4, 5)] + values[(6, 7)]
    second = values[(4, 6)] + values[(5, 7)]
    third = values[(4, 7)] + values[(5, 6)]
    return first - second, first - third


def axis_kernel_checks() -> tuple[
    tuple[dict[tuple[int, int], sp.Expr], ...],
    tuple[tuple[sp.Matrix, ...], ...],
]:
    face_columns = (
        (14, -24, 20, 15, -29, 9),
        (10, -33, 36, 30, -58, 18),
        (2, 38, -45, -30, 73, -23),
    )
    expected_covariants = ((76, -12), (119, -38), (-132, 54))
    graphs = tuple(scalar_graph(column) for column in face_columns)
    for column, expected in zip(face_columns, expected_covariants, strict=True):
        assert complement_covariant(column) == expected

    all_bases: list[tuple[sp.Matrix, ...]] = []
    for first, second in combinations(range(3), 2):
        matrix = axis_matrix(graphs[first], graphs[second])
        assert matrix.shape == (72, 56)
        assert matrix.rank() == 51
        basis = tuple(matrix.nullspace())
        assert len(basis) == 5
        for vector in basis:
            for index, (left, right) in enumerate(DIRECTED_EDGES):
                if left in WINDOW or right in WINDOW:
                    assert vector[index] == 0
            for vertex in CORE:
                row_sum = sum(
                    vector[DIRECTED_INDEX[(vertex, other)]]
                    for other in CORE
                    if other != vertex
                )
                column_sum = sum(
                    vector[DIRECTED_INDEX[(other, vertex)]]
                    for other in CORE
                    if other != vertex
                )
                assert row_sum == 0
                assert column_sum == 0
        all_bases.append(basis)
    print("three exact axis operators have rank 51 and core-circulation kernels: PASS")
    return graphs, tuple(all_bases)


def two_colour_coefficient(
    face: tuple[int, ...],
    minority_ports: tuple[int, int],
    majority_colour: int,
    minority_colour: int,
    graphs: tuple[dict[tuple[int, int], sp.Expr], ...],
    directed_values: dict[tuple[int, int], sp.Expr],
) -> sp.Expr:
    colours = {
        vertex: minority_colour if vertex in minority_ports else majority_colour
        for vertex in face
    }

    def block_value(left: int, right: int) -> sp.Expr:
        left_colour = colours[left]
        right_colour = colours[right]
        if left_colour == right_colour:
            return graphs[left_colour][edge(left, right)]
        if left_colour == minority_colour:
            return directed_values[(left, right)]
        return directed_values[(right, left)]

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


def forced_four_plus_two_checks(
    graphs: tuple[dict[tuple[int, int], sp.Expr], ...],
    all_bases: tuple[tuple[sp.Matrix, ...], ...],
) -> None:
    parameters = sp.symbols("q0:5")
    for pair_index, (majority, minority) in enumerate(combinations(range(3), 2)):
        generic_kernel = sp.zeros(56, 1)
        for parameter, basis_vector in zip(parameters, all_bases[pair_index], strict=True):
            generic_kernel += parameter * basis_vector
        directed_values = {
            directed: generic_kernel[index]
            for index, directed in enumerate(DIRECTED_EDGES)
        }
        for port_pair, face in zip(WINDOW_PAIRS, FACES, strict=True):
            coefficient = two_colour_coefficient(
                face,
                port_pair,
                majority,
                minority,
                graphs,
                directed_values,
            )
            expected = 3 * graphs[minority][port_pair]
            assert sp.expand(coefficient - expected) == 0
            assert expected != 0
    print("generic axis-kernel deformation leaves every forced 4+2 coefficient nonzero: PASS")


def monomial_gauge_check() -> None:
    mixed_value = sp.Rational(-10, 3)
    scalings = (
        (2, 3, 5),
        (7, 11, 13),
        (17, 19, 23),
        (29, 31, 37),
        (41, 43, 47),
    )
    product_by_colour = [sp.prod(row[colour] for row in scalings) for colour in range(3)]
    final_scaling = tuple(sp.Rational(1, product) for product in product_by_colour)
    all_scalings = scalings + (final_scaling,)
    for colour in range(3):
        assert sp.prod(row[colour] for row in all_scalings) == 1

    word = (0, 0, 1, 1, 2, 2)
    gauge_factor = sp.prod(all_scalings[vertex][colour] for vertex, colour in enumerate(word))
    assert gauge_factor != 0
    assert sp.expand(mixed_value * gauge_factor) != 0
    print("fixed normalized-GHZ-stabilizer gauge keeps the obstruction nonzero: PASS")


def main() -> None:
    graphs, all_bases = axis_kernel_checks()
    forced_four_plus_two_checks(graphs, all_bases)
    monomial_gauge_check()
    print("P6 axis complement-sum/off-diagonal no-go primary verification: PASS")


if __name__ == "__main__":
    main()
