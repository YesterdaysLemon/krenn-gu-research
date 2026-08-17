"""Primary exact replay for the unequal-slope eighteen-word detector.

The arbitrary-field support and rank argument in the theorem is load-bearing.
This script uses exact SymPy arithmetic to replay its bounded identities,
displayed word formulas, ternary ratio system, and physical sharp controls.
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


def verify_general_slope_identity() -> None:
    p, t = sp.symbols("p t")
    direct = {edge: sp.symbols(f"B{edge[0]}{edge[1]}") for edge in EDGES}
    channel = {edge: sp.symbols(f"K{edge[0]}{edge[1]}") for edge in EDGES}
    selected = {edge: direct[edge] + p * channel[edge] for edge in EDGES}

    def compound(blocks):
        return sum(blocks[e] * blocks[f] for e, f in MATCHINGS)

    def cross(left, right):
        return sum(left[e] * right[f] + right[e] * left[f] for e, f in MATCHINGS)

    response = compound(direct) + t * cross(direct, channel)
    claimed = (
        compound(selected)
        + (t - p) * cross(selected, channel)
        + p * (p - 2 * t) * compound(channel)
    )
    assert sp.expand(response - claimed) == 0
    assert sp.expand((t - p).subs(p, 0)) == t
    assert sp.expand((t - p).subs(p, 2 * t)) == -t


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


def verify_eighteen_word_formulas() -> None:
    diagonal = symbolic_diagonal_blocks("D")
    channel = symbolic_full_blocks("K")
    q = sp.symbols("q", nonzero=True)
    first, second = (0, 1), (2, 3)
    checked: set[tuple[int, int, int, int]] = set()

    for a, b in product(COLORS, repeat=2):
        if a == b:
            continue
        c = next(color for color in COLORS if color not in (a, b))

        word_first = (a, b, c, c)
        actual_first = compound_word(diagonal, word_first) + q * cross_word(
            diagonal, channel, word_first
        )
        expected_first = q * channel[first][a, b] * diagonal[second][c, c]
        assert sp.expand(actual_first - expected_first) == 0
        checked.add(word_first)

        word_second = (c, c, a, b)
        actual_second = compound_word(diagonal, word_second) + q * cross_word(
            diagonal, channel, word_second
        )
        expected_second = q * diagonal[first][c, c] * channel[second][a, b]
        assert sp.expand(actual_second - expected_second) == 0
        checked.add(word_second)

    for c, d in product(COLORS, repeat=2):
        if c == d:
            continue
        word = (c, c, d, d)
        actual = compound_word(diagonal, word) + q * cross_word(diagonal, channel, word)
        expected = diagonal[first][c, c] * diagonal[second][d, d] + q * (
            diagonal[first][c, c] * channel[second][d, d]
            + channel[first][c, c] * diagonal[second][d, d]
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
    nullspace = coefficient.nullspace()
    assert len(nullspace) == 1
    assert sp.Matrix.hstack(nullspace[0], direction).rank() == 1

    r, q = sp.symbols("r q", nonzero=True)
    d0, d1, d2 = sp.symbols("d0:3", nonzero=True)
    first_det = sp.det(sp.diag(*(-r * value / q for value in (d0, d1, d2))))
    second_det_at_zero = sp.det(sp.diag(*(-value / q for value in (d0, d1, d2))))
    assert sp.factor(first_det) == -d0 * d1 * d2 * r**3 / q**3
    assert sp.factor(second_det_at_zero) == -d0 * d1 * d2 / q**3


def diagonal_matrix(values):
    return sp.ImmutableMatrix.diag(*map(sp.Rational, values))


def outer(left, right):
    return sp.ImmutableMatrix(left) * sp.ImmutableMatrix([right])


def corrected_blocks(first, second):
    return {
        edge: sp.ImmutableMatrix(
            outer(first[edge[0]], second[edge[1]])
            + outer(second[edge[0]], first[edge[1]])
        )
        for edge in EDGES
    }


def add_blocks(left, right, right_scale=1):
    scalar = sp.Rational(right_scale)
    return {
        edge: sp.ImmutableMatrix(left[edge] + scalar * right[edge]) for edge in EDGES
    }


def tensor_compound(blocks):
    return {word: compound_word(blocks, word) for word in product(COLORS, repeat=4)}


def tensor_cross(left, right):
    return {word: cross_word(left, right, word) for word in product(COLORS, repeat=4)}


def add_tensors(left, right, right_scale=1):
    scalar = sp.Rational(right_scale)
    return {
        word: sp.expand(left[word] + scalar * right[word])
        for word in product(COLORS, repeat=4)
    }


def active_colors(pairs, fixed_port):
    answer = set()
    for color in COLORS:
        for partner in PORTS:
            if partner == fixed_port:
                continue
            edge = tuple(sorted((fixed_port, partner)))
            other = tuple(port for port in PORTS if port not in edge)
            complement = tuple(sorted(other))
            if any(
                pairs[edge][color, color] * pairs[complement][delta, delta]
                for delta in COLORS
                if delta != color
            ):
                answer.add(color)
    return answer


def assert_pure(tensor, expected):
    assert tuple(tensor[(color,) * 4] for color in COLORS) == tuple(
        map(sp.Rational, expected)
    )
    assert all(value == 0 for word, value in tensor.items() if len(set(word)) > 1)


def verify_missing_three_full_control() -> None:
    channel = {edge: diagonal_matrix((2, 0, 0)) for edge in EDGES}
    color_one = {(0, 1), (1, 2), (2, 3)}
    color_two = {(0, 2), (1, 3)}
    selected = {
        edge: diagonal_matrix((2, int(edge in color_one), int(edge in color_two)))
        for edge in EDGES
    }
    direct = add_blocks(selected, channel, -2)
    response = add_tensors(tensor_compound(direct), tensor_cross(direct, channel))
    assert_pure(response, (-12, 1, 1))
    assert active_colors(selected, 0) == {0, 1, 2}
    assert all(
        any(selected[edge][color, color] == 0 for color in COLORS) for edge in EDGES
    )


def rank_two_channel():
    first = ((1, 1, 0),) * 4
    second = ((1, -1, 0),) * 4
    channel = corrected_blocks(first, second)
    expected = diagonal_matrix((2, -2, 0))
    assert all(block == expected and block.rank() == 2 for block in channel.values())
    return channel


def verify_all_eighteen_nonzero_slope_control() -> None:
    channel = rank_two_channel()
    direct = {edge: diagonal_matrix((0, 0, 1)) for edge in EDGES}
    selected = add_blocks(direct, channel)
    assert all(selected[edge] == diagonal_matrix((2, -2, 1)) for edge in EDGES)
    response = tensor_compound(direct)
    assert_pure(response, (0, 0, 3))
    assert active_colors(selected, 0) == {0, 1, 2}
    assert 1 * (1 - 2 * 0) != 0


def verify_pure_normalized_slope_control() -> None:
    channel = rank_two_channel()
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
    selected = add_blocks(direct, channel)
    response = tensor_compound(direct)
    assert_pure(response, (1, 1, 1))
    assert active_colors(selected, 0) == {0, 1, 2}
    assert selected[(0, 3)] == selected[(1, 2)] == diagonal_matrix((2, -2, 1))


def main() -> None:
    verify_general_slope_identity()
    verify_eighteen_word_formulas()
    verify_ratio_system()
    verify_missing_three_full_control()
    verify_all_eighteen_nonzero_slope_control()
    verify_pure_normalized_slope_control()
    print("unequal-slope quadratic-cancellation primary replay: PASS")


if __name__ == "__main__":
    main()
