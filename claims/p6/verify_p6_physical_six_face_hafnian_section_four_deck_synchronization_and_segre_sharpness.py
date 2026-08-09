"""Primary exact checks for the physical P6 six-face hafnian section."""

from functools import cache
from itertools import combinations

import sympy as sp

CORE = (0, 1, 2, 3)
WINDOW = (4, 5, 6, 7)
VERTICES = CORE + WINDOW
WINDOW_PAIRS = tuple(combinations(WINDOW, 2))


def edge(i: int, j: int) -> tuple[int, int]:
    return (i, j) if i < j else (j, i)


def hafnian(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], sp.Expr]
) -> sp.Expr:
    """Return the exact loopless hafnian by first-vertex recurrence."""

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


def section_weights(
    faces: dict[tuple[int, int], sp.Expr], tau: sp.Expr
) -> dict[tuple[int, int], sp.Expr]:
    weights: dict[tuple[int, int], sp.Expr] = {}
    for i, j in combinations(CORE, 2):
        weights[(i, j)] = sp.Integer(1)
    for i in CORE:
        for p in WINDOW:
            weights[(i, p)] = tau
    for pair in WINDOW_PAIRS:
        weights[pair] = sp.expand((faces[pair] - 12 * tau**2) / 3)
    return weights


def symbolic_section_and_complete_deck_check() -> None:
    tau = sp.Symbol("tau")
    face_symbols = sp.symbols("y45 y46 y47 y56 y57 y67")
    faces = dict(zip(WINDOW_PAIRS, face_symbols, strict=True))
    weights = section_weights(faces, tau)

    assert hafnian(CORE, weights) == 3
    for pair in WINDOW_PAIRS:
        remaining = tuple(sorted(CORE + pair))
        assert sp.expand(hafnian(remaining, weights) - faces[pair]) == 0

    deck: dict[tuple[int, ...], sp.Expr] = {}
    for remaining in combinations(VERTICES, 4):
        actual = hafnian(remaining, weights)
        ports = tuple(vertex for vertex in remaining if vertex in WINDOW)
        port_count = len(ports)
        if port_count == 0:
            expected = sp.Integer(3)
        elif port_count == 1:
            expected = 3 * tau
        elif port_count == 2:
            expected = (faces[edge(*ports)] - 6 * tau**2) / 3
        elif port_count == 3:
            pair_sum = sum(faces[pair] for pair in combinations(ports, 2))
            expected = tau * (pair_sum - 36 * tau**2) / 3
        else:
            b = {
                pair: (faces[pair] - 12 * tau**2) / 3
                for pair in WINDOW_PAIRS
            }
            expected = b[(4, 5)] * b[(6, 7)]
            expected += b[(4, 6)] * b[(5, 7)]
            expected += b[(4, 7)] * b[(5, 6)]
        assert sp.expand(actual - expected) == 0
        deck[remaining] = actual
    assert len(deck) == 70

    stress_count = 0
    for pair in WINDOW_PAIRS:
        remaining = tuple(sorted(CORE + pair))
        for pivot in remaining:
            partner_sum = sp.Integer(0)
            for partner in remaining:
                if partner == pivot:
                    continue
                four_set = tuple(
                    vertex for vertex in remaining if vertex not in (pivot, partner)
                )
                partner_sum += weights[edge(pivot, partner)] * hafnian(
                    four_set, weights
                )
            assert sp.expand(partner_sum - faces[pair]) == 0
            stress_count += 1
    assert stress_count == 36
    print("symbolic six-face section, 70-label H4 deck, and 36 stresses: PASS")


def fan_matrix() -> sp.Matrix:
    parameters = (1, 2, 3, 4)
    a = sp.Matrix([[1, 1, 1, 1], list(parameters)])
    b = sp.Matrix(
        [[1, 1, 1, 1], [value**2 for value in parameters], [value**3 for value in parameters]]
    )
    return sp.Matrix.hstack(
        *[
            sp.kronecker_product(a[:, i], b[:, j])
            + sp.kronecker_product(a[:, j], b[:, i])
            for i, j in combinations(range(4), 2)
        ]
    )


def three_colour_block_certificate_check() -> None:
    face_columns = (
        (14, -24, 20, 15, -29, 9),
        (10, -33, 36, 30, -58, 18),
        (2, 38, -45, -30, 73, -23),
    )
    left_factors = ((1, 1), (1, 1), (1, 2))
    right_factors = ((1, 1, 1), (1, 2, 3), (1, 4, 9))
    scales = (10, 6, 30)
    fan = fan_matrix()
    assert fan.det() == -2880

    scalar_graphs: list[dict[tuple[int, int], sp.Expr]] = []
    for column, left, right, scale in zip(
        face_columns, left_factors, right_factors, scales, strict=True
    ):
        face_map = {
            pair: sp.Integer(value)
            for pair, value in zip(WINDOW_PAIRS, column, strict=True)
        }
        weights = section_weights(face_map, sp.Integer(1))
        scalar_graphs.append(weights)
        assert all(value != 0 for value in weights.values())
        for pair in WINDOW_PAIRS:
            assert hafnian(tuple(sorted(CORE + pair)), weights) == face_map[pair]

        observed = fan * sp.Matrix(column)
        target = scale * sp.kronecker_product(sp.Matrix(left), sp.Matrix(right))
        assert observed == target
        assert sp.Matrix(2, 3, list(observed)).rank() == 1

    expected_window_rows = (
        (sp.Rational(2, 3), sp.Rational(-2, 3), sp.Rational(-10, 3)),
        (-12, -15, sp.Rational(26, 3)),
        (sp.Rational(8, 3), 8, -19),
        (1, 6, -14),
        (sp.Rational(-41, 3), sp.Rational(-70, 3), sp.Rational(61, 3)),
        (-1, 2, sp.Rational(-35, 3)),
    )
    for pair, expected in zip(WINDOW_PAIRS, expected_window_rows, strict=True):
        diagonal = tuple(graph[pair] for graph in scalar_graphs)
        assert diagonal == expected
        assert sp.prod(diagonal) != 0

    mixed_word = (
        scalar_graphs[0][(0, 1)]
        * scalar_graphs[1][(2, 3)]
        * scalar_graphs[2][(4, 5)]
    )
    assert mixed_word == sp.Rational(-10, 3)
    print("three pure-colour physical sections and nonzero mixed word -10/3: PASS")


def general_bordered_formula_check() -> None:
    core_edges = {
        pair: sp.Symbol(f"a{pair[0]}{pair[1]}")
        for pair in combinations(CORE, 2)
    }
    x = {vertex: sp.Symbol(f"x{vertex}") for vertex in CORE}
    z = {vertex: sp.Symbol(f"z{vertex}") for vertex in CORE}
    direct = sp.Symbol("d")
    weights = dict(core_edges)
    for vertex in CORE:
        weights[(vertex, 4)] = x[vertex]
        weights[(vertex, 5)] = z[vertex]
    weights[(4, 5)] = direct

    core_hafnian = hafnian(CORE, weights)
    correction = sp.Integer(0)
    for u, v in combinations(CORE, 2):
        complement = tuple(vertex for vertex in CORE if vertex not in (u, v))
        cofactor = hafnian(complement, weights)
        correction += (x[u] * z[v] + x[v] * z[u]) * cofactor
    expected = direct * core_hafnian + correction
    assert sp.expand(hafnian(CORE + (4, 5), weights) - expected) == 0
    print("arbitrary symbolic bordered-hafnian two-port formula: PASS")


def main() -> None:
    general_bordered_formula_check()
    symbolic_section_and_complete_deck_check()
    three_colour_block_certificate_check()
    print("P6 physical six-face/four-deck section primary verification: PASS")


if __name__ == "__main__":
    main()
