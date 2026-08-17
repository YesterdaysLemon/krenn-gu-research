"""Primary exact replay for GLD18.

The full-nuisance operator inclusion and arbitrary-field support/rank proofs in
the theorem are load-bearing.  This script uses exact SymPy arithmetic to
replay the bounded chart minors, response-visibility branches, variable-slope
identity, eighteen displayed words, ratio system, decomposable-channel
formulas, and physical sharp controls.
"""

from itertools import combinations, product

import sympy as sp

PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def verify_visibility_and_chart_minors() -> None:
    p = sp.symbols("p")
    nuisance = sp.Matrix([[1], [0], [0]])
    desired_m = sp.Matrix([0, 1, 0])
    desired_z = sp.Matrix([2, p, 0])
    joint = nuisance.row_join(desired_m).row_join(desired_z)
    assert nuisance.rank() == 1
    assert joint.rank() == 2

    mu = sp.det(sp.Matrix([[1, 0], [0, 1]]))
    zeta = sp.det(sp.Matrix([[1, 2], [0, p]]))
    assert mu == 1 and zeta == p

    visible = sp.Matrix([[-p, 1]])
    operator = sp.Matrix([1, p])
    assert visible * operator == sp.zeros(1, 1)
    assert visible.rank() == 1

    invisible = sp.zeros(1, 2)
    assert invisible * operator == sp.zeros(1, 1)
    assert invisible.rank() == 0

    stacked = sp.Matrix([[-2, 1], [-3, 1]])
    assert stacked.rank() == 2
    assert sp.det(sp.Matrix([[1, 2], [1, 3]])) == 1

    pair_rows = 6
    four_rows = 78
    total_rows = 6 * pair_rows + four_rows
    assert total_rows == 114
    assert sp.binomial(total_rows, 2) == 6441
    assert (
        sp.binomial(total_rows, 2)
        - 6 * sp.binomial(pair_rows, 2)
        - sp.binomial(four_rows, 2)
        == 3348
    )


def compound_scalars(blocks):
    return sum(blocks[e] * blocks[f] for e, f in MATCHINGS)


def cross_scalars(left, right):
    return sum(left[e] * right[f] + right[e] * left[f] for e, f in MATCHINGS)


def verify_variable_slope_identity() -> None:
    t = sp.symbols("t")
    direct = {edge: sp.symbols(f"B{edge[0]}{edge[1]}") for edge in EDGES}
    channel = {edge: sp.symbols(f"K{edge[0]}{edge[1]}") for edge in EDGES}
    slopes = {edge: sp.symbols(f"p{edge[0]}{edge[1]}") for edge in EDGES}
    selected = {edge: direct[edge] + slopes[edge] * channel[edge] for edge in EDGES}
    response = compound_scalars(direct) + t * cross_scalars(direct, channel)
    claimed = 0
    for edge, complement in MATCHINGS:
        gamma = slopes[edge] * slopes[complement] - t * (
            slopes[edge] + slopes[complement]
        )
        claimed += (
            selected[edge] * selected[complement]
            + (t - slopes[complement]) * selected[edge] * channel[complement]
            + (t - slopes[edge]) * channel[edge] * selected[complement]
            + gamma * channel[edge] * channel[complement]
        )
    assert sp.expand(response - claimed) == 0

    ae, be, af, bf, au, bu = sp.symbols("ae be af bf au bu", nonzero=True)
    gamma_affine = be * bf / (ae * af) - bu / au * (be / ae + bf / af)
    gamma_projective = au * be * bf - bu * (be * af + ae * bf)
    assert sp.factor(gamma_affine - gamma_projective / (au * ae * af)) == 0

    a, b = sp.symbols("a b")
    common = sp.expand(au * b**2 - bu * (b * a + a * b))
    assert sp.expand(common - b * (au * b - 2 * a * bu)) == 0


def symbolic_diagonal_blocks(prefix: str):
    return {
        edge: sp.ImmutableMatrix.diag(
            *(sp.symbols(f"{prefix}{edge[0]}{edge[1]}_{color}") for color in COLORS)
        )
        for edge in EDGES
    }


def symbolic_full_blocks(prefix: str):
    return {
        edge: sp.ImmutableMatrix(
            3,
            3,
            lambda row, column: sp.symbols(f"{prefix}{edge[0]}{edge[1]}_{row}{column}"),
        )
        for edge in EDGES
    }


def compound_word(blocks, word):
    return sp.expand(
        sum(
            blocks[e][word[e[0]], word[e[1]]] * blocks[f][word[f[0]], word[f[1]]]
            for e, f in MATCHINGS
        )
    )


def cross_word(left, right, word):
    return sp.expand(
        sum(
            left[e][word[e[0]], word[e[1]]] * right[f][word[f[0]], word[f[1]]]
            + right[e][word[e[0]], word[e[1]]] * left[f][word[f[0]], word[f[1]]]
            for e, f in MATCHINGS
        )
    )


def cancellation_word(diagonal, channel, q_by_edge, word):
    value = 0
    for edge, complement in MATCHINGS:
        value += (
            diagonal[edge][word[edge[0]], word[edge[1]]]
            * diagonal[complement][word[complement[0]], word[complement[1]]]
            + q_by_edge[complement]
            * diagonal[edge][word[edge[0]], word[edge[1]]]
            * channel[complement][word[complement[0]], word[complement[1]]]
            + q_by_edge[edge]
            * channel[edge][word[edge[0]], word[edge[1]]]
            * diagonal[complement][word[complement[0]], word[complement[1]]]
        )
    return sp.expand(value)


def verify_eighteen_word_formulas() -> None:
    diagonal = symbolic_diagonal_blocks("D")
    channel = symbolic_full_blocks("K")
    q_by_edge = {
        edge: sp.symbols(f"q{edge[0]}{edge[1]}", nonzero=True) for edge in EDGES
    }
    first, second = (0, 1), (2, 3)
    checked: set[tuple[int, int, int, int]] = set()

    for a, b in product(COLORS, repeat=2):
        if a == b:
            continue
        c = next(color for color in COLORS if color not in (a, b))

        word_first = (a, b, c, c)
        actual_first = cancellation_word(diagonal, channel, q_by_edge, word_first)
        expected_first = (
            q_by_edge[first] * channel[first][a, b] * diagonal[second][c, c]
        )
        assert sp.expand(actual_first - expected_first) == 0
        checked.add(word_first)

        word_second = (c, c, a, b)
        actual_second = cancellation_word(diagonal, channel, q_by_edge, word_second)
        expected_second = (
            q_by_edge[second] * diagonal[first][c, c] * channel[second][a, b]
        )
        assert sp.expand(actual_second - expected_second) == 0
        checked.add(word_second)

    for c, d in product(COLORS, repeat=2):
        if c == d:
            continue
        word = (c, c, d, d)
        actual = cancellation_word(diagonal, channel, q_by_edge, word)
        expected = (
            diagonal[first][c, c] * diagonal[second][d, d]
            + q_by_edge[second] * diagonal[first][c, c] * channel[second][d, d]
            + q_by_edge[first] * channel[first][c, c] * diagonal[second][d, d]
        )
        assert sp.expand(actual - expected) == 0
        checked.add(word)

    assert len(checked) == 18
    assert all(len(set(word)) > 1 for word in checked)


def verify_ratio_system() -> None:
    rows = []
    for first_color, second_color in product(COLORS, repeat=2):
        if first_color == second_color:
            continue
        row = [0] * 6
        row[first_color] = 1
        row[3 + second_color] = 1
        rows.append(row)
    coefficient = sp.Matrix(rows)
    augmented = coefficient.row_join(sp.ones(6, 1))
    assert coefficient.rank() == augmented.rank() == 5
    particular = sp.Matrix([0, 0, 0, 1, 1, 1])
    direction = sp.Matrix([1, 1, 1, -1, -1, -1])
    assert coefficient * particular == sp.ones(6, 1)
    assert coefficient * direction == sp.zeros(6, 1)


def diagonal_matrix(values):
    return sp.ImmutableMatrix.diag(*map(sp.Rational, values))


def outer(left, right):
    return sp.ImmutableMatrix(left) * sp.ImmutableMatrix([right])


def physical_blocks(first, second):
    return {
        edge: sp.ImmutableMatrix(
            outer(first[edge[0]], second[edge[1]])
            + outer(second[edge[0]], first[edge[1]])
        )
        for edge in EDGES
    }


def add_blocks(left, right, scales):
    return {
        edge: sp.ImmutableMatrix(left[edge] + scales[edge] * right[edge])
        for edge in EDGES
    }


def tensor_compound(blocks):
    return {word: compound_word(blocks, word) for word in product(COLORS, repeat=4)}


def tensor_cross(left, right):
    return {word: cross_word(left, right, word) for word in product(COLORS, repeat=4)}


def response_tensor(direct, channel, t):
    compound = tensor_compound(direct)
    cross = tensor_cross(direct, channel)
    return {word: sp.expand(compound[word] + t * cross[word]) for word in compound}


def assert_pure(tensor, expected):
    assert tuple(tensor[(color,) * 4] for color in COLORS) == tuple(
        map(sp.Rational, expected)
    )
    assert all(value == 0 for word, value in tensor.items() if len(set(word)) > 1)


def gamma(slopes, t, edge, complement):
    return sp.expand(
        slopes[edge] * slopes[complement] - t * (slopes[edge] + slopes[complement])
    )


def verify_edge_dependent_detector_control() -> None:
    t = sp.Rational(1)
    slopes = {
        (0, 1): sp.Rational(3, 2),
        (2, 3): sp.Rational(3),
        (0, 2): sp.Rational(0),
        (1, 3): sp.Rational(0),
        (0, 3): sp.Rational(2),
        (1, 2): sp.Rational(2),
    }
    assert all(
        gamma(slopes, t, edge, complement) == 0 for edge, complement in MATCHINGS
    )
    first = ((1, 1, 0),) * 4
    second = ((1, -1, 0),) * 4
    channel = physical_blocks(first, second)
    selected = {edge: diagonal_matrix((2, -2, 1)) for edge in EDGES}
    direct = add_blocks(selected, channel, {edge: -slopes[edge] for edge in EDGES})
    response = response_tensor(direct, channel, t)
    assert response[(2, 2, 0, 0)] == -2
    assert channel[(0, 1)].rank() == 2


def verify_support_drop_control() -> None:
    t = sp.Rational(1)
    slopes = {
        (0, 1): sp.Rational(2),
        (2, 3): sp.Rational(2),
        (0, 2): sp.Rational(3),
        (1, 3): sp.Rational(3, 2),
        (0, 3): sp.Rational(4),
        (1, 2): sp.Rational(4, 3),
    }
    assert all(
        gamma(slopes, t, edge, complement) == 0 for edge, complement in MATCHINGS
    )
    first = ((1, 0, 0),) * 4
    second = ((1, 0, 0),) * 4
    channel = physical_blocks(first, second)
    color_one = {(0, 1), (1, 2), (2, 3)}
    color_two = {(0, 2), (1, 3)}
    direct = {
        edge: diagonal_matrix((-2, int(edge in color_one), int(edge in color_two)))
        for edge in EDGES
    }
    selected = add_blocks(direct, channel, slopes)
    response = response_tensor(direct, channel, t)
    assert_pure(response, (-12, 1, 1))
    assert all(
        any(
            selected[edge][color, color] == 0 or selected[complement][color, color] == 0
            for color in COLORS
        )
        for edge, complement in MATCHINGS
    )


def verify_noncancellation_control() -> None:
    t = sp.Rational(0)
    slopes = {edge: sp.Rational(1) for edge in EDGES}
    first = ((1, 1, 0),) * 4
    second = ((1, -1, 0),) * 4
    channel = physical_blocks(first, second)
    color_matchings = {
        0: {(0, 1), (2, 3)},
        1: {(0, 2), (1, 3)},
        2: {(0, 3), (1, 2)},
    }
    direct = {
        edge: diagonal_matrix(
            tuple(int(edge in color_matchings[color]) for color in COLORS)
        )
        for edge in EDGES
    }
    selected = add_blocks(direct, channel, slopes)
    response = response_tensor(direct, channel, t)
    assert_pure(response, (1, 1, 1))
    assert selected[(0, 3)] == selected[(1, 2)] == diagonal_matrix((2, -2, 1))
    assert all(
        gamma(slopes, t, edge, complement) == 1 for edge, complement in MATCHINGS
    )


def verify_cancellation_split() -> None:
    pe, pf, t = sp.symbols("pe pf t")
    expression = pe * pf - t * (pe + pf)
    assert sp.expand(expression - ((pe - t) * (pf - t) - t**2)) == 0
    assert expression.subs(t, 0) == pe * pf
    phi = t * pe / (pe - t)
    assert sp.factor(t * phi / (phi - t) - pe) == 0
    assert sp.factor(phi - pe + pe * (pe - 2 * t) / (pe - t)) == 0


def verify_decomposable_channel_formulas() -> None:
    q, r = sp.symbols("q r", nonzero=True)
    vectors = {port: sp.ImmutableMatrix(sp.symbols(f"a{port}_0:3")) for port in PORTS}
    channel = {
        edge: sp.ImmutableMatrix(vectors[edge[0]] * vectors[edge[1]].T)
        for edge in EDGES
    }
    diagonal = symbolic_diagonal_blocks("E")

    word_22 = (0, 0, 1, 1)
    actual_22 = (
        compound_word(diagonal, word_22)
        + q * cross_word(diagonal, channel, word_22)
        + r * compound_word(channel, word_22)
    )
    expected_22 = (
        diagonal[(0, 1)][0, 0] * diagonal[(2, 3)][1, 1]
        + q
        * (
            diagonal[(0, 1)][0, 0] * channel[(2, 3)][1, 1]
            + channel[(0, 1)][0, 0] * diagonal[(2, 3)][1, 1]
        )
        + 3 * r * channel[(0, 1)][0, 0] * channel[(2, 3)][1, 1]
    )
    assert sp.expand(actual_22 - expected_22) == 0

    word_211 = (0, 0, 1, 2)
    actual_211 = (
        compound_word(diagonal, word_211)
        + q * cross_word(diagonal, channel, word_211)
        + r * compound_word(channel, word_211)
    )
    expected_211 = channel[(2, 3)][1, 2] * (
        q * diagonal[(0, 1)][0, 0] + 3 * r * channel[(0, 1)][0, 0]
    )
    assert sp.expand(actual_211 - expected_211) == 0

    forced_diagonal = {
        edge: sp.ImmutableMatrix.diag(
            *(-3 * r * channel[edge][color, color] / q for color in COLORS)
        )
        for edge in EDGES
    }
    word_31 = (0, 0, 0, 1)
    actual_31 = sp.factor(
        compound_word(forced_diagonal, word_31)
        + q * cross_word(forced_diagonal, channel, word_31)
        + r * compound_word(channel, word_31)
    )
    monomial = vectors[0][0] * vectors[1][0] * vectors[2][0] * vectors[3][1]
    assert sp.factor(actual_31 + 6 * r * monomial) == 0


def verify_decomposable_support_control() -> None:
    p, t = sp.symbols("p t")
    first = ((1, 0, 0),) * 4
    second = ((sp.Rational(1, 2), 0, 0),) * 4
    channel = physical_blocks(first, second)
    expected_channel = diagonal_matrix((1, 0, 0))
    assert all(block == expected_channel for block in channel.values())

    color_one = {(0, 1), (1, 2), (2, 3)}
    color_two = {(0, 2), (1, 3)}
    shifted = {
        edge: diagonal_matrix((0, int(edge in color_one), int(edge in color_two)))
        for edge in EDGES
    }
    direct = add_blocks(shifted, channel, {edge: -t for edge in EDGES})
    selected = add_blocks(direct, channel, {edge: p for edge in EDGES})
    response = response_tensor(direct, channel, t)
    assert response[(0, 0, 0, 0)] == -3 * t**2
    assert response[(1, 1, 1, 1)] == response[(2, 2, 2, 2)] == 1
    assert all(value == 0 for word, value in response.items() if len(set(word)) > 1)
    assert all(selected[edge][0, 0] == p - t for edge in EDGES)
    activity = (
        selected[(0, 3)][0, 0] * selected[(1, 2)][1, 1],
        selected[(0, 1)][1, 1] * selected[(2, 3)][0, 0],
        selected[(0, 2)][2, 2] * selected[(1, 3)][0, 0],
    )
    assert all(sp.expand(value - (p - t)) == 0 for value in activity)
    assert all(not (selected[edge][1, 1] and selected[edge][2, 2]) for edge in EDGES)


def main() -> None:
    verify_visibility_and_chart_minors()
    verify_variable_slope_identity()
    verify_eighteen_word_formulas()
    verify_ratio_system()
    verify_edge_dependent_detector_control()
    verify_support_drop_control()
    verify_noncancellation_control()
    verify_cancellation_split()
    verify_decomposable_channel_formulas()
    verify_decomposable_support_control()
    print("response-visible edge-dependent cancellation primary replay: PASS")


if __name__ == "__main__":
    main()
