"""Verify the fifth-compound fibre dichotomy's exact singular escape.

The script checks one fixed relabelled pure-chart incidence and one exact edge
vector.  It performs no word, support, graph-family, parameter, or fibre
search.
"""

from functools import cache
from itertools import combinations

import sympy as sp

import verify_p7_221_common_terminal_block_scalar_hafnian_realizability as scalar

INDICES = tuple(range(7))
CORE_PAIRS = tuple(combinations(INDICES, 2))
TERMINAL_FACES = tuple(combinations(INDICES, 5))


def permanent_evaluator(matrix: sp.Matrix):
    @cache
    def permanent(rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Expr:
        if not rows:
            return sp.Integer(1)
        first = rows[0]
        return sp.expand(
            sum(
                matrix[first, column]
                * permanent(
                    rows[1:], columns[:position] + columns[position + 1 :]
                )
                for position, column in enumerate(columns)
            )
        )

    return permanent


def fifth_compound(matrix: sp.Matrix) -> sp.Matrix:
    permanent = permanent_evaluator(matrix)
    return sp.Matrix(
        [
            [
                permanent(
                    tuple(index for index in INDICES if index not in deleted_pair),
                    face,
                )
                for deleted_pair in CORE_PAIRS
            ]
            for face in TERMINAL_FACES
        ]
    )


def check_pure_rectangle() -> None:
    ledger, _ = scalar.formal_ledger()
    terminal_block = scalar.common_terminal_block()
    all_terminals = frozenset(scalar.P)

    @cache
    def negative_hafnian(vertices: tuple[str, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        return sp.simplify(
            sum(
                -terminal_block.get(frozenset((first, second)), 0)
                * negative_hafnian(
                    vertices[1:position] + vertices[position + 1 :]
                )
                for position, second in enumerate(vertices[1:], start=1)
            )
        )

    def response(face: str, color: int) -> sp.Expr:
        total = sp.Integer(0)
        for size in (0, 2, 4):
            for matched in combinations(tuple(face), size):
                surviving = tuple(value for value in face if value not in matched)
                deletion = all_terminals - frozenset(surviving)
                total += negative_hafnian(tuple(matched)) * ledger[color][deletion]
        return sp.simplify(total)

    rho = scalar.RHO
    expected = {
        "125ab": (rho - 2, 0, (1 + rho) / 7),
        "145ab": (0, 0, (1 + rho) / 7),
        "235ab": (0, 0, (1 + rho) / 7),
        "345ab": (0, rho - 2, (1 + rho) / 7),
    }
    responses = {
        face: tuple(response(face, color) for color in range(3))
        for face in expected
    }
    assert responses == expected
    rectangle = tuple(
        sp.simplify(
            responses["125ab"][color]
            - responses["145ab"][color]
            - responses["235ab"][color]
            + responses["345ab"][color]
        )
        for color in range(3)
    )
    assert rectangle == (rho - 2, rho - 2, 0)


def main() -> None:
    rho = sp.sqrt(21)
    incidence = sp.Matrix(
        [
            [1, 0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, sp.Rational(1, 7), 0, 0],
            [0, 0, 1, 0, 0, 0, -rho],
            [0, 0, 0, 1, 0, 0, -5 - 2 * rho / 21],
            [0, 0, 0, 0, 1, 0, 230 + 104 * rho / 7],
            [0, 0, 0, 0, 0, 1, 1 + 16 * rho / 21],
        ]
    )

    # Derive the displayed rows from the already verified pure charts, rather
    # than treating the mixed incidence as an unrelated hard-coded matrix.
    colour_zero_graph, _ = scalar.build_colour_zero()
    colour_two_graph, _ = scalar.build_colour_two()
    relabelled_cores = (
        (colour_two_graph, "z_1"),
        (colour_two_graph, "z_5"),
        (colour_two_graph, "z_*"),
        (colour_zero_graph, "h3"),
        (colour_zero_graph, "h4"),
        (colour_zero_graph, "h5"),
        (colour_zero_graph, "ha"),
    )
    incidence_from_pure_charts = sp.Matrix(
        [
            [graph.get(frozenset((core, terminal)), 0) for terminal in scalar.P]
            for graph, core in relabelled_cores
        ]
    )
    assert incidence == incidence_from_pure_charts
    compound = fifth_compound(incidence)

    # Five independent relations from the two equal incidence rows.
    for other in range(2, 7):
        left = CORE_PAIRS.index((0, other))
        right = CORE_PAIRS.index((1, other))
        assert compound[:, left] == compound[:, right]
    assert compound.rank() == 6

    edge_values = {pair: sp.Integer(0) for pair in CORE_PAIRS}
    edge_values.update(
        {
            (3, 5): rho,
            (4, 5): -6 - 1 / rho,
            (4, 6): 1 / rho,
            (5, 6): 1 + 22 / rho,
            (0, 3): (-16905 + 1092 * rho) / 84463,
            (0, 4): (5747 - 4778 * rho) / 84463,
            (0, 5): -2 * rho,
            (0, 6): (16618 - 339 * rho) / 84463,
        }
    )
    for left, right in CORE_PAIRS:
        left_graph, left_core = relabelled_cores[left]
        right_graph, right_core = relabelled_cores[right]
        if left_graph is right_graph:
            assert sp.simplify(
                edge_values[left, right]
                - left_graph.get(frozenset((left_core, right_core)), 0)
            ) == 0
    edge_vector = sp.Matrix([edge_values[pair] for pair in CORE_PAIRS])
    response = compound * edge_vector
    assert response.applyfunc(sp.simplify) == sp.zeros(21, 1)

    # Product-one vertex gauge: C columns and edge entries acquire reciprocal
    # factors whose product is one, so the full response is unchanged.
    scales = (
        sp.Rational(2),
        sp.Rational(3),
        sp.Rational(5),
        sp.Rational(7),
        sp.Rational(11),
        sp.Rational(13),
        sp.Rational(1, 30030),
    )
    assert sp.prod(scales) == 1
    scaled_incidence = sp.diag(*scales) * incidence
    scaled_compound = fifth_compound(scaled_incidence)
    scaled_edges = sp.Matrix(
        [
            scales[left] * scales[right] * edge_values[left, right]
            for left, right in CORE_PAIRS
        ]
    )
    scaled_response = scaled_compound * scaled_edges
    assert (scaled_response - response).applyfunc(sp.simplify) == sp.zeros(21, 1)

    check_pure_rectangle()

    print("PASS: proportional-row fifth compound is singular of rank 6")
    print("PASS: exact cross-edge vector kills all 21 degree-five faces")
    print("PASS: product-one gauge preserves the pure response")
    print("PASS: pure rectangle is (rho-2)*(D0+D1)")
    print("SCOPE: degree-five fibre escape only; full tensor ledger unresolved")


if __name__ == "__main__":
    main()
