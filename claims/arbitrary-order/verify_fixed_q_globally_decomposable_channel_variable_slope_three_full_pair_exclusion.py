"""Primary exact replay for the GLD64 variable-slope detector.

The arbitrary-field support argument and the legal GLD15 attachment are
load-bearing.  This script uses exact SymPy polynomials to replay the physical
response identity, the forty-three-word ledger, every displayed coefficient
formula, the zero-support boundary, and the final characteristic-zero
syzygy.
"""

from itertools import combinations, permutations, product

import sympy as sp

PORTS = tuple(range(4))
COLORS = tuple(range(3))
EDGES = tuple(combinations(PORTS, 2))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
COMPLEMENT = {edge: other for edge, other in MATCHINGS} | {
    other: edge for edge, other in MATCHINGS
}
NAMED_EDGE = (0, 1)
NAMED_COMPLEMENT = (2, 3)


def matrix_entry(blocks, edge, word):
    return blocks[edge][word[edge[0]], word[edge[1]]]


def compound_word(blocks, word):
    return sp.expand(
        sum(
            matrix_entry(blocks, edge, word) * matrix_entry(blocks, complement, word)
            for edge, complement in MATCHINGS
        )
    )


def cross_word(left, right, word):
    return sp.expand(
        sum(
            matrix_entry(left, edge, word) * matrix_entry(right, complement, word)
            + matrix_entry(right, edge, word) * matrix_entry(left, complement, word)
            for edge, complement in MATCHINGS
        )
    )


def setup():
    endpoint = {
        port: tuple(sp.symbols(f"a{port}_{color}") for color in COLORS)
        for port in PORTS
    }
    channel = {
        edge: sp.ImmutableMatrix(
            3,
            3,
            lambda row, column, e=edge: endpoint[e[0]][row] * endpoint[e[1]][column],
        )
        for edge in EDGES
    }
    diagonal = {
        edge: sp.ImmutableMatrix.diag(
            *(sp.symbols(f"d{edge[0]}{edge[1]}_{color}") for color in COLORS)
        )
        for edge in EDGES
    }
    slopes = {edge: sp.symbols(f"p{edge[0]}{edge[1]}") for edge in EDGES}
    t = sp.symbols("t")
    gamma = {
        (edge, complement): slopes[edge] * slopes[complement]
        - t * (slopes[edge] + slopes[complement])
        for edge, complement in MATCHINGS
    }
    aggregate = sp.expand(sum(gamma.values()))
    return endpoint, channel, diagonal, slopes, t, gamma, aggregate


def response_from_edge_identity(diagonal, channel, slopes, t, gamma, word):
    value = 0
    for edge, complement in MATCHINGS:
        d_edge = matrix_entry(diagonal, edge, word)
        d_complement = matrix_entry(diagonal, complement, word)
        k_edge = matrix_entry(channel, edge, word)
        k_complement = matrix_entry(channel, complement, word)
        value += (
            d_edge * d_complement
            + (t - slopes[complement]) * d_edge * k_complement
            + (t - slopes[edge]) * k_edge * d_complement
            + gamma[(edge, complement)] * k_edge * k_complement
        )
    return sp.expand(value)


def detector_words():
    two_one_one = set()
    for edge in EDGES:
        complement = COMPLEMENT[edge]
        for color in COLORS:
            others = tuple(value for value in COLORS if value != color)
            for ordered in permutations(others):
                word = [None] * 4
                word[edge[0]] = word[edge[1]] = color
                word[complement[0]], word[complement[1]] = ordered
                two_one_one.add(tuple(word))

    two_two = {
        (first, first, second, second)
        for first, second in product(COLORS, repeat=2)
        if first != second
    }
    three_one = {(0, 0, 0, 1)}
    assert len(two_one_one) == 36
    assert len(two_two) == 6
    assert len(three_one) == 1
    assert not (two_one_one & two_two)
    assert not (two_one_one & three_one)
    assert not (two_two & three_one)
    ledger = two_one_one | two_two | three_one
    assert len(ledger) == 43
    assert all(len(set(word)) > 1 for word in ledger)
    return two_one_one, two_two, three_one, ledger


def verify_inherited_edge_identity() -> None:
    direct = {edge: sp.symbols(f"B{edge[0]}{edge[1]}") for edge in EDGES}
    channel = {edge: sp.symbols(f"K{edge[0]}{edge[1]}") for edge in EDGES}
    slopes = {edge: sp.symbols(f"p{edge[0]}{edge[1]}") for edge in EDGES}
    t = sp.symbols("t")
    selected = {edge: direct[edge] + slopes[edge] * channel[edge] for edge in EDGES}
    original = sum(
        direct[edge] * direct[complement]
        + t * (direct[edge] * channel[complement] + channel[edge] * direct[complement])
        for edge, complement in MATCHINGS
    )
    expanded = 0
    for edge, complement in MATCHINGS:
        gamma = slopes[edge] * slopes[complement] - t * (
            slopes[edge] + slopes[complement]
        )
        expanded += (
            selected[edge] * selected[complement]
            + (t - slopes[complement]) * selected[edge] * channel[complement]
            + (t - slopes[edge]) * channel[edge] * selected[complement]
            + gamma * channel[edge] * channel[complement]
        )
    assert sp.expand(original - expanded) == 0


def verify_matching_independence(endpoint, channel) -> None:
    for word in product(COLORS, repeat=4):
        monomial = sp.prod(endpoint[port][word[port]] for port in PORTS)
        matching_values = [
            matrix_entry(channel, edge, word) * matrix_entry(channel, complement, word)
            for edge, complement in MATCHINGS
        ]
        assert all(sp.expand(value - monomial) == 0 for value in matching_values)


def verify_word_formulas(endpoint, channel, diagonal, slopes, t, gamma, aggregate):
    two_one_one, two_two, _, ledger = detector_words()

    for word in two_one_one:
        repeated = next(edge for edge in EDGES if word[edge[0]] == word[edge[1]])
        complement = COMPLEMENT[repeated]
        color = word[repeated[0]]
        k_complement = matrix_entry(channel, complement, word)
        d_value = diagonal[repeated][color, color]
        k_value = channel[repeated][color, color]
        expected = k_complement * (
            (t - slopes[complement]) * d_value + aggregate * k_value
        )
        actual = response_from_edge_identity(diagonal, channel, slopes, t, gamma, word)
        assert sp.expand(actual - expected) == 0

    for word in two_two:
        first = word[0]
        second = word[2]
        d_edge = diagonal[NAMED_EDGE][first, first]
        d_complement = diagonal[NAMED_COMPLEMENT][second, second]
        k_edge = channel[NAMED_EDGE][first, first]
        k_complement = channel[NAMED_COMPLEMENT][second, second]
        expected = (
            d_edge * d_complement
            + (t - slopes[NAMED_COMPLEMENT]) * d_edge * k_complement
            + (t - slopes[NAMED_EDGE]) * k_edge * d_complement
            + aggregate * k_edge * k_complement
        )
        actual = response_from_edge_identity(diagonal, channel, slopes, t, gamma, word)
        assert sp.expand(actual - expected) == 0

    special = (0, 0, 0, 1)
    actual = response_from_edge_identity(diagonal, channel, slopes, t, gamma, special)
    relations = 0
    for edge, complement in MATCHINGS:
        if special[edge[0]] == special[edge[1]]:
            same, mixed = edge, complement
        else:
            same, mixed = complement, edge
        color = special[same[0]]
        relation = (t - slopes[mixed]) * diagonal[same][
            color, color
        ] + aggregate * channel[same][color, color]
        relations += matrix_entry(channel, mixed, special) * relation
    monomial = sp.prod(endpoint[port][special[port]] for port in PORTS)
    assert sp.expand(actual - (relations - 2 * aggregate * monomial)) == 0

    assert all(
        sp.expand(
            response_from_edge_identity(diagonal, channel, slopes, t, gamma, word)
        ).is_polynomial()
        for word in ledger
    )


def verify_zero_support_and_final_divisors(
    endpoint, channel, diagonal, slopes, t, gamma, aggregate
):
    # One endpoint zero realizes k_01^0=0.  The other two colours on edge 23
    # remain symbolic and give the exact boundary formula (13).
    word = (0, 0, 1, 2)
    actual = response_from_edge_identity(diagonal, channel, slopes, t, gamma, word)
    zero_named = {endpoint[0][0]: 0}
    expected = (
        (t - slopes[NAMED_COMPLEMENT])
        * diagonal[NAMED_EDGE][0, 0]
        * channel[NAMED_COMPLEMENT][1, 2]
    )
    assert sp.expand((actual - expected).subs(zero_named)) == 0

    # Once the complementary slope equals t, the named 00|11 coefficient is
    # the nonzero three-full product and cannot vanish.
    word_two_two = (0, 0, 1, 1)
    actual_two_two = response_from_edge_identity(
        diagonal, channel, slopes, t, gamma, word_two_two
    )
    boundary = zero_named | {slopes[NAMED_COMPLEMENT]: t}
    expected_two_two = diagonal[NAMED_EDGE][0, 0] * diagonal[NAMED_COMPLEMENT][1, 1]
    assert sp.expand((actual_two_two - expected_two_two).subs(boundary)) == 0

    # Symmetric zero support on edge 23.
    symmetric_zero = {endpoint[2][1]: 0}
    symmetric_boundary = symmetric_zero | {slopes[NAMED_EDGE]: t}
    assert sp.expand((actual_two_two - expected_two_two).subs(symmetric_boundary)) == 0

    # After the 3+1 relation gives G=0, three-fullness forces the two named
    # complementary slopes to t, and the same coefficient is again a product.
    final_boundary = {
        slopes[NAMED_EDGE]: t,
        slopes[NAMED_COMPLEMENT]: t,
    }
    residual = sp.expand((actual_two_two - expected_two_two).subs(final_boundary))
    expected_residual = sp.expand(
        aggregate.subs(final_boundary)
        * channel[NAMED_EDGE][0, 0]
        * channel[NAMED_COMPLEMENT][1, 1]
    )
    assert sp.expand(residual - expected_residual) == 0


def main() -> None:
    verify_inherited_edge_identity()
    endpoint, channel, diagonal, slopes, t, gamma, aggregate = setup()
    verify_matching_independence(endpoint, channel)
    verify_word_formulas(endpoint, channel, diagonal, slopes, t, gamma, aggregate)
    verify_zero_support_and_final_divisors(
        endpoint, channel, diagonal, slopes, t, gamma, aggregate
    )
    print("GLD64 primary exact replay: PASS")
    print("  81 decomposable matching monomials checked")
    print("  43 mixed detector words checked")
    print("  zero-support, aggregate, and slope divisors retained")


if __name__ == "__main__":
    main()
