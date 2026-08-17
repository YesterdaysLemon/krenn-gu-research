"""Independent no-import audit for GLD18.

This script imports only the Python standard library and does not import the
primary replay.  It independently uses sparse polynomial dictionaries,
Fraction elimination, direct perfect-matching evaluation, and raw endpoint
vectors.  The theorem's full-nuisance and arbitrary-field proofs remain
load-bearing.
"""

from fractions import Fraction
from itertools import combinations, product

PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def clean(poly):
    return {
        monomial: coefficient for monomial, coefficient in poly.items() if coefficient
    }


def constant(value):
    value = Fraction(value)
    return {} if not value else {(): value}


def variable(name):
    return {(name,): Fraction(1)}


def add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return clean(result)


def neg(poly):
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def sub(left, right):
    return add(left, neg(right))


def mul(left, right):
    result = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            monomial = tuple(sorted(first + second))
            result[monomial] = result.get(monomial, Fraction(0)) + (
                first_coefficient * second_coefficient
            )
    return clean(result)


def scale(poly, scalar):
    return clean(
        {
            monomial: Fraction(scalar) * coefficient
            for monomial, coefficient in poly.items()
        }
    )


def sum_polys(polys):
    result = {}
    for poly in polys:
        result = add(result, poly)
    return result


def fraction_rank(rows):
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [value / pivot_value for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def verify_visibility_controls() -> None:
    nuisance = [[1], [0], [0]]
    desired_m = [0, 1, 0]
    desired_z = [2, 2, 0]
    assert fraction_rank(nuisance) == 1
    assert (
        fraction_rank(
            [[nuisance[row][0], desired_m[row], desired_z[row]] for row in range(3)]
        )
        == 2
    )
    mu = Fraction(1) * Fraction(1) - Fraction(0) * Fraction(0)
    zeta = Fraction(1) * Fraction(2) - Fraction(0) * Fraction(2)
    assert (mu, zeta) == (1, 2)
    assert -2 * mu + zeta == 0

    visible_one = [-2, 1]
    visible_two = [-3, 1]
    assert fraction_rank([visible_one]) == 1
    assert fraction_rank([visible_one, visible_two]) == 2
    assert fraction_rank([[0, 0]]) == 0

    assert 6 * 6 + 78 == 114
    assert 114 * 113 // 2 == 6441
    assert 6441 - 6 * (6 * 5 // 2) - 78 * 77 // 2 == 3348


def compound_scalars(blocks):
    return sum_polys(
        mul(blocks[edge], blocks[complement]) for edge, complement in MATCHINGS
    )


def cross_scalars(left, right):
    return sum_polys(
        add(
            mul(left[edge], right[complement]),
            mul(right[edge], left[complement]),
        )
        for edge, complement in MATCHINGS
    )


def verify_variable_identity() -> None:
    direct = {edge: variable(f"B{edge}") for edge in EDGES}
    channel = {edge: variable(f"K{edge}") for edge in EDGES}
    slopes = {edge: variable(f"p{edge}") for edge in EDGES}
    t = variable("t")
    selected = {
        edge: add(direct[edge], mul(slopes[edge], channel[edge])) for edge in EDGES
    }
    response = add(compound_scalars(direct), mul(t, cross_scalars(direct, channel)))
    claimed_terms = []
    for edge, complement in MATCHINGS:
        gamma = sub(
            mul(slopes[edge], slopes[complement]),
            mul(t, add(slopes[edge], slopes[complement])),
        )
        claimed_terms.extend(
            (
                mul(selected[edge], selected[complement]),
                mul(
                    sub(t, slopes[complement]),
                    mul(selected[edge], channel[complement]),
                ),
                mul(
                    sub(t, slopes[edge]),
                    mul(channel[edge], selected[complement]),
                ),
                mul(gamma, mul(channel[edge], channel[complement])),
            )
        )
    assert sub(response, sum_polys(claimed_terms)) == {}

    ae, be, af, bf, au, bu = map(variable, ("ae", "be", "af", "bf", "au", "bu"))
    gamma_projective = sub(
        mul(au, mul(be, bf)),
        mul(bu, add(mul(be, af), mul(ae, bf))),
    )
    a = variable("a")
    b = variable("b")
    expected = sub(mul(au, mul(b, b)), scale(mul(bu, mul(a, b)), 2))
    common = {
        "ae": a,
        "af": a,
        "be": b,
        "bf": b,
    }

    def substitute_common(poly):
        result = {}
        for monomial, coefficient in poly.items():
            factors = [common.get(name, variable(name)) for name in monomial]
            term = constant(coefficient)
            for factor in factors:
                term = mul(term, factor)
            result = add(result, term)
        return result

    assert sub(substitute_common(gamma_projective), expected) == {}


def zero_matrix():
    return [[{} for _ in COLORS] for _ in COLORS]


def symbolic_diagonal(prefix):
    blocks = {}
    for edge in EDGES:
        matrix = zero_matrix()
        for color in COLORS:
            matrix[color][color] = variable(f"{prefix}{edge}{color}")
        blocks[edge] = matrix
    return blocks


def symbolic_full(prefix):
    return {
        edge: [
            [variable(f"{prefix}{edge}{row}{column}") for column in COLORS]
            for row in COLORS
        ]
        for edge in EDGES
    }


def word_entry(blocks, edge, word):
    return blocks[edge][word[edge[0]]][word[edge[1]]]


def word_compound(blocks, word):
    return sum_polys(
        mul(word_entry(blocks, edge, word), word_entry(blocks, complement, word))
        for edge, complement in MATCHINGS
    )


def word_cross(left, right, word):
    return sum_polys(
        add(
            mul(word_entry(left, edge, word), word_entry(right, complement, word)),
            mul(word_entry(right, edge, word), word_entry(left, complement, word)),
        )
        for edge, complement in MATCHINGS
    )


def cancellation_word(diagonal, channel, q_by_edge, word):
    terms = []
    for edge, complement in MATCHINGS:
        terms.extend(
            (
                mul(
                    word_entry(diagonal, edge, word),
                    word_entry(diagonal, complement, word),
                ),
                mul(
                    q_by_edge[complement],
                    mul(
                        word_entry(diagonal, edge, word),
                        word_entry(channel, complement, word),
                    ),
                ),
                mul(
                    q_by_edge[edge],
                    mul(
                        word_entry(channel, edge, word),
                        word_entry(diagonal, complement, word),
                    ),
                ),
            )
        )
    return sum_polys(terms)


def verify_eighteen_words() -> None:
    diagonal = symbolic_diagonal("D")
    channel = symbolic_full("K")
    q_by_edge = {edge: variable(f"q{edge}") for edge in EDGES}
    first, second = (0, 1), (2, 3)
    words = set()
    for a, b in product(COLORS, repeat=2):
        if a == b:
            continue
        c = next(color for color in COLORS if color not in (a, b))
        first_word = (a, b, c, c)
        first_expected = mul(
            q_by_edge[first],
            mul(channel[first][a][b], diagonal[second][c][c]),
        )
        assert (
            sub(
                cancellation_word(diagonal, channel, q_by_edge, first_word),
                first_expected,
            )
            == {}
        )
        words.add(first_word)

        second_word = (c, c, a, b)
        second_expected = mul(
            q_by_edge[second],
            mul(diagonal[first][c][c], channel[second][a][b]),
        )
        assert (
            sub(
                cancellation_word(diagonal, channel, q_by_edge, second_word),
                second_expected,
            )
            == {}
        )
        words.add(second_word)

    for c, d in product(COLORS, repeat=2):
        if c == d:
            continue
        word = (c, c, d, d)
        expected = sum_polys(
            (
                mul(diagonal[first][c][c], diagonal[second][d][d]),
                mul(
                    q_by_edge[second],
                    mul(diagonal[first][c][c], channel[second][d][d]),
                ),
                mul(
                    q_by_edge[first],
                    mul(channel[first][c][c], diagonal[second][d][d]),
                ),
            )
        )
        assert (
            sub(cancellation_word(diagonal, channel, q_by_edge, word), expected) == {}
        )
        words.add(word)
    assert len(words) == 18

    ratio_rows = []
    for c, d in product(COLORS, repeat=2):
        if c == d:
            continue
        row = [Fraction(0)] * 6
        row[c] = Fraction(1)
        row[3 + d] = Fraction(1)
        ratio_rows.append(row)
    assert fraction_rank(ratio_rows) == 5
    assert fraction_rank([row + [1] for row in ratio_rows]) == 5

    def wick_involution(t, slope):
        return t * slope / (slope - t)

    assert wick_involution(Fraction(2), Fraction(3)) == 6
    assert wick_involution(Fraction(2), Fraction(6)) == 3
    assert wick_involution(Fraction(2), Fraction(0)) == 0
    assert wick_involution(Fraction(2), Fraction(4)) == 4


def numeric_diag(values):
    matrix = [[Fraction(0) for _ in COLORS] for _ in COLORS]
    for color, value in enumerate(values):
        matrix[color][color] = Fraction(value)
    return matrix


def numeric_outer(left, right):
    return [
        [Fraction(left[row]) * Fraction(right[column]) for column in COLORS]
        for row in COLORS
    ]


def numeric_add(left, right):
    return [
        [left[row][column] + right[row][column] for column in COLORS] for row in COLORS
    ]


def numeric_scale(matrix, scalar):
    scalar = Fraction(scalar)
    return [[scalar * value for value in row] for row in matrix]


def physical_blocks(first, second):
    blocks = {}
    for edge in EDGES:
        blocks[edge] = numeric_add(
            numeric_outer(first[edge[0]], second[edge[1]]),
            numeric_outer(second[edge[0]], first[edge[1]]),
        )
    return blocks


def numeric_word_entry(blocks, edge, word):
    return blocks[edge][word[edge[0]]][word[edge[1]]]


def numeric_compound(blocks, word):
    return sum(
        numeric_word_entry(blocks, edge, word)
        * numeric_word_entry(blocks, complement, word)
        for edge, complement in MATCHINGS
    )


def numeric_cross(left, right, word):
    return sum(
        numeric_word_entry(left, edge, word)
        * numeric_word_entry(right, complement, word)
        + numeric_word_entry(right, edge, word)
        * numeric_word_entry(left, complement, word)
        for edge, complement in MATCHINGS
    )


def numeric_response(direct, channel, t):
    return {
        word: numeric_compound(direct, word)
        + Fraction(t) * numeric_cross(direct, channel, word)
        for word in product(COLORS, repeat=4)
    }


def numeric_gamma(slopes, t, edge, complement):
    return slopes[edge] * slopes[complement] - Fraction(t) * (
        slopes[edge] + slopes[complement]
    )


def assert_pure(tensor, expected):
    assert tuple(tensor[(color,) * 4] for color in COLORS) == tuple(
        map(Fraction, expected)
    )
    assert all(value == 0 for word, value in tensor.items() if len(set(word)) > 1)


def verify_physical_controls() -> None:
    rank_two = physical_blocks(((1, 1, 0),) * 4, ((1, -1, 0),) * 4)
    slopes = {
        (0, 1): Fraction(3, 2),
        (2, 3): Fraction(3),
        (0, 2): Fraction(0),
        (1, 3): Fraction(0),
        (0, 3): Fraction(2),
        (1, 2): Fraction(2),
    }
    assert all(
        numeric_gamma(slopes, 1, edge, complement) == 0
        for edge, complement in MATCHINGS
    )
    selected = {edge: numeric_diag((2, -2, 1)) for edge in EDGES}
    direct = {
        edge: numeric_add(selected[edge], numeric_scale(rank_two[edge], -slopes[edge]))
        for edge in EDGES
    }
    assert numeric_response(direct, rank_two, 1)[(2, 2, 0, 0)] == -2

    rank_one = physical_blocks(((1, 0, 0),) * 4, ((1, 0, 0),) * 4)
    sparse_slopes = {
        (0, 1): Fraction(2),
        (2, 3): Fraction(2),
        (0, 2): Fraction(3),
        (1, 3): Fraction(3, 2),
        (0, 3): Fraction(4),
        (1, 2): Fraction(4, 3),
    }
    assert all(
        numeric_gamma(sparse_slopes, 1, edge, complement) == 0
        for edge, complement in MATCHINGS
    )
    color_one = {(0, 1), (1, 2), (2, 3)}
    color_two = {(0, 2), (1, 3)}
    sparse_direct = {
        edge: numeric_diag((-2, int(edge in color_one), int(edge in color_two)))
        for edge in EDGES
    }
    sparse_selected = {
        edge: numeric_add(
            sparse_direct[edge], numeric_scale(rank_one[edge], sparse_slopes[edge])
        )
        for edge in EDGES
    }
    assert_pure(numeric_response(sparse_direct, rank_one, 1), (-12, 1, 1))
    assert all(
        any(
            sparse_selected[edge][color][color] == 0
            or sparse_selected[complement][color][color] == 0
            for color in COLORS
        )
        for edge, complement in MATCHINGS
    )

    color_matchings = {
        0: {(0, 1), (2, 3)},
        1: {(0, 2), (1, 3)},
        2: {(0, 3), (1, 2)},
    }
    noncancel_direct = {
        edge: numeric_diag(
            tuple(int(edge in color_matchings[color]) for color in COLORS)
        )
        for edge in EDGES
    }
    assert_pure(numeric_response(noncancel_direct, rank_two, 0), (1, 1, 1))


def verify_decomposable_formulas() -> None:
    vectors = {
        port: [variable(f"a{port}{color}") for color in COLORS] for port in PORTS
    }
    channel = {
        edge: [
            [mul(vectors[edge[0]][row], vectors[edge[1]][column]) for column in COLORS]
            for row in COLORS
        ]
        for edge in EDGES
    }
    diagonal = symbolic_diagonal("E")
    q = variable("q")
    r = variable("r")

    word_22 = (0, 0, 1, 1)
    actual_22 = sum_polys(
        (
            word_compound(diagonal, word_22),
            mul(q, word_cross(diagonal, channel, word_22)),
            mul(r, word_compound(channel, word_22)),
        )
    )
    expected_22 = sum_polys(
        (
            mul(diagonal[(0, 1)][0][0], diagonal[(2, 3)][1][1]),
            mul(
                q,
                add(
                    mul(diagonal[(0, 1)][0][0], channel[(2, 3)][1][1]),
                    mul(channel[(0, 1)][0][0], diagonal[(2, 3)][1][1]),
                ),
            ),
            scale(
                mul(r, mul(channel[(0, 1)][0][0], channel[(2, 3)][1][1])),
                3,
            ),
        )
    )
    assert sub(actual_22, expected_22) == {}

    word_211 = (0, 0, 1, 2)
    actual_211 = sum_polys(
        (
            word_compound(diagonal, word_211),
            mul(q, word_cross(diagonal, channel, word_211)),
            mul(r, word_compound(channel, word_211)),
        )
    )
    expected_211 = mul(
        channel[(2, 3)][1][2],
        add(
            mul(q, diagonal[(0, 1)][0][0]),
            scale(mul(r, channel[(0, 1)][0][0]), 3),
        ),
    )
    assert sub(actual_211, expected_211) == {}

    numeric_vectors = {
        0: (1, 2, 3),
        1: (2, 3, 5),
        2: (3, 5, 7),
        3: (5, 7, 11),
    }
    numeric_channel = {
        edge: numeric_outer(numeric_vectors[edge[0]], numeric_vectors[edge[1]])
        for edge in EDGES
    }
    q_value = Fraction(2)
    r_value = Fraction(3)
    forced = {
        edge: numeric_diag(
            tuple(
                -3 * r_value * numeric_channel[edge][color][color] / q_value
                for color in COLORS
            )
        )
        for edge in EDGES
    }
    word_31 = (0, 0, 0, 1)
    actual_31 = (
        numeric_compound(forced, word_31)
        + q_value * numeric_cross(forced, numeric_channel, word_31)
        + r_value * numeric_compound(numeric_channel, word_31)
    )
    monomial = (
        numeric_vectors[0][0]
        * numeric_vectors[1][0]
        * numeric_vectors[2][0]
        * numeric_vectors[3][1]
    )
    assert actual_31 == -6 * r_value * monomial

    p = variable("p")
    t = variable("t")
    # The all-word symbolic camouflage is audited with polynomial entries.
    a_blocks = {}
    first_family = {(0, 1), (1, 2), (2, 3)}
    second_family = {(0, 2), (1, 3)}
    for edge in EDGES:
        matrix = zero_matrix()
        matrix[1][1] = constant(int(edge in first_family))
        matrix[2][2] = constant(int(edge in second_family))
        a_blocks[edge] = matrix
    b_blocks = {}
    k_blocks = {}
    for edge in EDGES:
        k_matrix = zero_matrix()
        k_matrix[0][0] = constant(1)
        k_blocks[edge] = k_matrix
        b_matrix = [[dict(entry) for entry in row] for row in a_blocks[edge]]
        b_matrix[0][0] = neg(t)
        b_blocks[edge] = b_matrix
    for word in product(COLORS, repeat=4):
        response = add(
            word_compound(b_blocks, word), mul(t, word_cross(b_blocks, k_blocks, word))
        )
        if word == (0, 0, 0, 0):
            assert sub(response, scale(mul(t, t), -3)) == {}
        elif word == (1, 1, 1, 1) or word == (2, 2, 2, 2):
            assert response == constant(1)
        else:
            assert response == {}
    d_blocks = {}
    for edge in EDGES:
        d_matrix = [[dict(entry) for entry in row] for row in a_blocks[edge]]
        d_matrix[0][0] = sub(p, t)
        d_blocks[edge] = d_matrix
    activity = (
        mul(d_blocks[(0, 3)][0][0], d_blocks[(1, 2)][1][1]),
        mul(d_blocks[(0, 1)][1][1], d_blocks[(2, 3)][0][0]),
        mul(d_blocks[(0, 2)][2][2], d_blocks[(1, 3)][0][0]),
    )
    assert all(sub(value, sub(p, t)) == {} for value in activity)
    assert all(not (d_blocks[edge][1][1] and d_blocks[edge][2][2]) for edge in EDGES)


def main() -> None:
    verify_visibility_controls()
    verify_variable_identity()
    verify_eighteen_words()
    verify_physical_controls()
    verify_decomposable_formulas()
    print("response-visible edge-dependent cancellation independent audit: PASS")


if __name__ == "__main__":
    main()
