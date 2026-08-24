"""Independent no-import audit for the GLD64 variable-slope detector.

This script imports only the Python standard library and does not import the
primary replay or GLD18.  It uses a custom sparse-polynomial representation,
constructs the physical response directly from B=D-pK, and independently
enumerates all endpoint-support patterns used in the theorem's boundary
argument.
"""

from fractions import Fraction
from itertools import combinations, permutations, product

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


def endpoint(port, color):
    return variable(f"a{port}_{color}")


def diagonal(edge, row, column):
    if row != column:
        return {}
    return variable(f"d{edge[0]}{edge[1]}_{row}")


def channel(edge, row, column):
    return mul(endpoint(edge[0], row), endpoint(edge[1], column))


def slope(edge):
    return variable(f"p{edge[0]}{edge[1]}")


T_SLOPE = variable("t")


def direct(edge, row, column):
    return sub(
        diagonal(edge, row, column), mul(slope(edge), channel(edge, row, column))
    )


def entry(block, edge, word):
    return block(edge, word[edge[0]], word[edge[1]])


def original_response(word):
    terms = []
    for edge, complement in MATCHINGS:
        terms.append(mul(entry(direct, edge, word), entry(direct, complement, word)))
        terms.append(
            mul(
                T_SLOPE,
                mul(entry(direct, edge, word), entry(channel, complement, word)),
            )
        )
        terms.append(
            mul(
                T_SLOPE,
                mul(entry(channel, edge, word), entry(direct, complement, word)),
            )
        )
    return sum_polys(terms)


def gamma(edge, complement):
    return sub(
        mul(slope(edge), slope(complement)),
        mul(T_SLOPE, add(slope(edge), slope(complement))),
    )


AGGREGATE = sum_polys(gamma(edge, complement) for edge, complement in MATCHINGS)


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
    ledger = two_one_one | two_two | three_one
    assert (len(two_one_one), len(two_two), len(three_one), len(ledger)) == (
        36,
        6,
        1,
        43,
    )
    assert all(len(set(word)) > 1 for word in ledger)
    return two_one_one, two_two, three_one, ledger


def verify_direct_word_syzygies() -> None:
    two_one_one, two_two, _, ledger = detector_words()

    for word in two_one_one:
        repeated = next(edge for edge in EDGES if word[edge[0]] == word[edge[1]])
        complement = COMPLEMENT[repeated]
        color = word[repeated[0]]
        bracket = add(
            mul(
                sub(T_SLOPE, slope(complement)),
                diagonal(repeated, color, color),
            ),
            mul(AGGREGATE, channel(repeated, color, color)),
        )
        expected = mul(entry(channel, complement, word), bracket)
        assert sub(original_response(word), expected) == {}

    for word in two_two:
        first, second = word[0], word[2]
        d_edge = diagonal(NAMED_EDGE, first, first)
        d_complement = diagonal(NAMED_COMPLEMENT, second, second)
        k_edge = channel(NAMED_EDGE, first, first)
        k_complement = channel(NAMED_COMPLEMENT, second, second)
        expected = sum_polys(
            (
                mul(d_edge, d_complement),
                mul(
                    sub(T_SLOPE, slope(NAMED_COMPLEMENT)),
                    mul(d_edge, k_complement),
                ),
                mul(
                    sub(T_SLOPE, slope(NAMED_EDGE)),
                    mul(k_edge, d_complement),
                ),
                mul(AGGREGATE, mul(k_edge, k_complement)),
            )
        )
        assert sub(original_response(word), expected) == {}

    word = (0, 0, 0, 1)
    relation_sum = {}
    for edge, complement in MATCHINGS:
        if word[edge[0]] == word[edge[1]]:
            same, mixed = edge, complement
        else:
            same, mixed = complement, edge
        color = word[same[0]]
        relation = add(
            mul(
                sub(T_SLOPE, slope(mixed)),
                diagonal(same, color, color),
            ),
            mul(AGGREGATE, channel(same, color, color)),
        )
        relation_sum = add(relation_sum, mul(entry(channel, mixed, word), relation))
    four_port_monomial = constant(1)
    for port, color in enumerate(word):
        four_port_monomial = mul(four_port_monomial, endpoint(port, color))
    expected = sub(relation_sum, scale(mul(AGGREGATE, four_port_monomial), 2))
    assert sub(original_response(word), expected) == {}

    # The forty-three words are distinct and all direct polynomials were built.
    assert (
        len({tuple(sorted(original_response(word).items())) for word in ledger}) == 43
    )


def verify_support_cover() -> dict[str, int]:
    supports = [
        frozenset(color for color in COLORS if mask & (1 << color)) for mask in range(8)
    ]
    counts = {"distinct_zero": 0, "edge_zero": 0, "complement_zero": 0, "full": 0}

    for port_supports in product(supports, repeat=4):
        edge_support = port_supports[0] & port_supports[1]
        complement_support = port_supports[2] & port_supports[3]
        edge_zeros = set(COLORS) - set(edge_support)
        complement_zeros = set(COLORS) - set(complement_support)

        distinct = next(
            (
                (first, second)
                for first in edge_zeros
                for second in complement_zeros
                if first != second
            ),
            None,
        )
        if distinct is not None:
            counts["distinct_zero"] += 1
            continue

        if edge_zeros:
            color = next(iter(edge_zeros))
            other_colors = set(COLORS) - {color}
            assert complement_zeros <= {color}
            assert other_colors <= set(port_supports[2])
            assert other_colors <= set(port_supports[3])
            counts["edge_zero"] += 1
            continue

        if complement_zeros:
            color = next(iter(complement_zeros))
            other_colors = set(COLORS) - {color}
            assert edge_zeros <= {color}
            assert other_colors <= set(port_supports[0])
            assert other_colors <= set(port_supports[1])
            counts["complement_zero"] += 1
            continue

        assert all(set(support) == set(COLORS) for support in port_supports)
        counts["full"] += 1

    assert sum(counts.values()) == 8**4
    assert counts["full"] == 1
    return counts


def evaluate(poly, values):
    result = Fraction(0)
    for monomial, coefficient in poly.items():
        term = coefficient
        for name in monomial:
            term *= values[name]
        result += term
    return result


def verify_exact_fixtures(ledger) -> None:
    for seed in range(1, 8):
        values = {"t": Fraction(seed - 4, 2)}
        for edge_index, edge in enumerate(EDGES):
            values[f"p{edge[0]}{edge[1]}"] = Fraction(seed + edge_index - 3, 3)
            for color in COLORS:
                # Both named blocks are automatically three-full, and all
                # endpoint coordinates are nonzero.
                values[f"d{edge[0]}{edge[1]}_{color}"] = Fraction(
                    1 + seed + edge_index + 2 * color
                )
        for port in PORTS:
            for color in COLORS:
                values[f"a{port}_{color}"] = Fraction(1 + seed + port + color)
        coefficients = [evaluate(original_response(word), values) for word in ledger]
        assert any(value for value in coefficients)


def main() -> None:
    _, _, _, ledger = detector_words()
    verify_direct_word_syzygies()
    support_counts = verify_support_cover()
    verify_exact_fixtures(ledger)
    print("GLD64 independent no-import audit: PASS")
    print("  43 direct physical response polynomials checked")
    print(f"  4096 endpoint-support patterns covered: {support_counts}")
    print("  7 exact rational divisor fixtures checked")


if __name__ == "__main__":
    main()
