"""Independent no-import audit of complete moment-compatible odd holonomy."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from itertools import combinations

# Each row is (left, right, decimal endpoint code, physical sign, balance).
# For example, code 12 means label 1 at the left endpoint and 2 at the right.
ROWS = (
    (0, 1, 0, 1, 1),
    (0, 2, 0, 1, 1),
    (0, 3, 0, 1, 4),
    (0, 4, 0, 1, 1),
    (0, 5, 12, 1, 6),
    (0, 6, 11, 1, 1),
    (0, 7, 22, 1, 7),
    (1, 2, 1, -1, 4),
    (1, 3, 0, 1, 1),
    (1, 4, 10, -1, 3),
    (1, 5, 11, 1, 4),
    (1, 6, 22, 1, 7),
    (1, 7, 0, 1, 1),
    (2, 3, 11, 1, 3),
    (2, 4, 1, -1, 2),
    (2, 5, 22, 1, 1),
    (2, 6, 0, 1, 4),
    (2, 7, 20, 1, 6),
    (3, 4, 22, 1, 7),
    (3, 5, 1, 1, 2),
    (3, 6, 10, 1, 3),
    (3, 7, 11, 1, 1),
    (4, 5, 0, 1, 3),
    (4, 6, 11, 1, 1),
    (4, 7, 11, 1, 4),
    (5, 6, 1, 1, 4),
    (5, 7, 11, 1, 1),
    (6, 7, 11, 1, 1),
)


def unpack(code: int) -> tuple[int, int]:
    """Decode a decimal endpoint-label pair."""
    return divmod(code, 10)


def pack_word(digits: tuple[int, ...]) -> int:
    """Encode a ternary word with vertex zero as the least-significant digit."""
    return sum(digit * 3**vertex for vertex, digit in enumerate(digits))


def edge_bit_map() -> dict[tuple[int, int], int]:
    """Give every physical pair an independent bit position."""
    return {edge: 1 << index for index, edge in enumerate(combinations(range(8), 2))}


def matching_bits(edges: tuple[tuple[int, int], ...]) -> int:
    """Encode a physical matching as a 28-bit set."""
    bits = edge_bit_map()
    return sum(bits[edge] for edge in edges)


def row_maps(rows=ROWS):
    """Build lookup maps from the independently encoded row table."""
    labels = {}
    weights = {}
    balances = {}
    for left, right, code, sign, balance in rows:
        labels[(left, right)] = unpack(code)
        weights[(left, right)] = Fraction(sign)
        balances[(left, right)] = Fraction(balance)
    return labels, weights, balances


def enumerate_fibres(rows=ROWS):
    """Traverse all matchings by least-set-bit deletion and pack their words."""
    labels, weights, _ = row_maps(rows)
    bits = edge_bit_map()
    fibres: dict[int, list[tuple[int, Fraction, bool]]] = defaultdict(list)

    def visit(
        mask: int,
        word: list[int],
        scalar: Fraction,
        diagonal: bool,
        selected: int,
    ) -> None:
        if mask == 0:
            fibres[pack_word(tuple(word))].append((selected, scalar, diagonal))
            return
        low = mask & -mask
        left = low.bit_length() - 1
        remainder = mask ^ low
        partners = remainder
        while partners:
            partner_bit = partners & -partners
            right = partner_bit.bit_length() - 1
            partners ^= partner_bit
            edge = (left, right)
            left_label, right_label = labels[edge]
            next_word = word[:]
            next_word[left] = left_label
            next_word[right] = right_label
            visit(
                remainder ^ partner_bit,
                next_word,
                scalar * weights[edge],
                diagonal and left_label == right_label,
                selected | bits[edge],
            )

    visit((1 << 8) - 1, [-1] * 8, Fraction(1), True, 0)
    return fibres


def fibre_total(records: list[tuple[int, Fraction, bool]]) -> Fraction:
    """Sum the exact physical weights in one packed fibre."""
    return sum((record[1] for record in records), Fraction(0))


def assert_support_and_balance() -> dict[str, object]:
    """Audit completeness and the all-positive endpoint ledger directly."""
    labels, weights, balances = row_maps()
    expected_edges = set(combinations(range(8), 2))
    assert set(labels) == expected_edges
    assert len(ROWS) == len(expected_edges) == 28
    assert all(value != 0 for value in weights.values())
    assert all(value > 0 for value in balances.values())

    loads = {(vertex, colour): Fraction(0) for vertex in range(8) for colour in range(3)}
    counts = {(vertex, colour): 0 for vertex in range(8) for colour in range(3)}
    for edge, (left_label, right_label) in labels.items():
        left, right = edge
        loads[left, left_label] += balances[edge]
        loads[right, right_label] += balances[edge]
        counts[left, left_label] += 1
        counts[right, right_label] += 1
    assert set(loads.values()) == {Fraction(7)}
    assert len({tuple(counts[vertex, colour] for colour in range(3)) for vertex in range(8)}) > 1
    return {
        "physical_pairs": len(labels),
        "strict_balance": True,
        "common_auxiliary_colour_load": 7,
        "unit_phase_table_already_moment_balanced": False,
    }


def assert_word_fibres() -> dict[str, object]:
    """Audit the pure, cycle, and exposed fibres by packed-word lookup."""
    fibres = enumerate_fibres()
    assert sum(len(records) for records in fibres.values()) == 105
    assert len(fibres) == 101
    assert sum(fibre_total(records) == 0 for records in fibres.values()) == 4

    pure_matchings = (
        ((0, 3), (1, 7), (2, 6), (4, 5)),
        ((0, 6), (1, 5), (2, 3), (4, 7)),
        ((0, 7), (1, 6), (2, 5), (3, 4)),
    )
    for colour, matching in enumerate(pure_matchings):
        records = fibres[pack_word((colour,) * 8)]
        assert records == [(matching_bits(matching), Fraction(1), True)]

    cycle_words = (
        (0, 0, 0, 0, 1, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 0, 1),
    )
    expected_matchings = (
        (
            ((0, 1), (2, 4), (3, 5), (6, 7)),
            ((0, 2), (1, 3), (4, 6), (5, 7)),
        ),
        (
            ((0, 1), (2, 3), (4, 5), (6, 7)),
            ((0, 4), (1, 2), (3, 7), (5, 6)),
        ),
        (
            ((0, 2), (1, 4), (3, 6), (5, 7)),
            ((0, 4), (1, 5), (2, 6), (3, 7)),
        ),
    )
    for word, matching_pair in zip(cycle_words, expected_matchings):
        records = fibres[pack_word(word)]
        assert {record[0] for record in records} == {
            matching_bits(matching_pair[0]),
            matching_bits(matching_pair[1]),
        }
        assert sorted((record[1], record[2]) for record in records) == [
            (Fraction(-1), False),
            (Fraction(1), True),
        ]
        assert fibre_total(records) == 0

    exposed = (0, 0, 0, 0, 0, 1, 0, 0)
    exposed_matching = ((0, 4), (1, 7), (2, 6), (3, 5))
    assert fibres[pack_word(exposed)] == [
        (matching_bits(exposed_matching), Fraction(1), False)
    ]
    return {
        "perfect_matchings": 105,
        "induced_words": len(fibres),
        "pure_singletons": 3,
        "binomial_zero_fibres": 3,
        "exposed_mixed_coefficient": 1,
    }


def assert_holonomy_character() -> dict[str, object]:
    """Audit the Laurent ratio and its endpoint character independently."""
    labels, weights, _ = row_maps()
    numerator = ((2, 3), (4, 5), (1, 5), (2, 6), (4, 6), (1, 3))
    denominator = ((2, 4), (3, 5), (1, 2), (5, 6), (1, 4), (3, 6))
    assert len(set(numerator) | set(denominator)) == 12
    assert not set(numerator) & set(denominator)

    holonomy = Fraction(1)
    endpoint = defaultdict(int)
    for sign, edge_list in ((1, numerator), (-1, denominator)):
        for edge in edge_list:
            left, right = edge
            left_label, right_label = labels[edge]
            endpoint[left, left_label] += sign
            endpoint[right, right_label] += sign
            if sign == 1:
                holonomy *= weights[edge]
            else:
                holonomy /= weights[edge]
    assert all(value == 0 for value in endpoint.values())
    assert holonomy == -1
    return {
        "circulation_support": 12,
        "endpoint_character_zero": True,
        "holonomy": holonomy,
    }


def assert_nonlinearity_flags() -> tuple[tuple[int, ...], ...]:
    """Audit the three oriented nonrigidity sets from row codes."""
    labels, _, _ = row_maps()
    result = []
    for colour in range(3):
        active = set()
        for (left, right), (left_label, right_label) in labels.items():
            if left_label != colour and right_label == colour:
                active.add(left)
            if right_label != colour and left_label == colour:
                active.add(right)
        result.append(tuple(sorted(active)))
    expected = (
        (1, 2, 3, 4, 5, 6),
        (1, 2, 3, 4, 5, 6),
        (0, 7),
    )
    assert tuple(result) == expected
    assert all(result) and all(len(active) < 8 for active in result)
    return tuple(result)


def assert_independent_character_scaling() -> dict[str, object]:
    """Re-enumerate after a separately encoded exact GHZ character scaling."""
    exponent_rows = (
        (1, -1, 0),
        (0, 1, -1),
        (-1, 0, 1),
        (2, 0, -2),
        (-2, 2, 0),
        (0, -2, 2),
        (1, 1, -2),
        (-1, -1, 2),
    )
    assert tuple(sum(row[colour] for row in exponent_rows) for colour in range(3)) == (
        0,
        0,
        0,
    )

    scaled_rows = []
    for left, right, code, sign, balance in ROWS:
        left_label, right_label = unpack(code)
        exponent = exponent_rows[left][left_label] + exponent_rows[right][right_label]
        factor = Fraction(3) ** exponent
        scaled_rows.append((left, right, code, Fraction(sign) * factor, balance))

    original = enumerate_fibres()
    scaled = enumerate_fibres(tuple(scaled_rows))
    assert set(original) == set(scaled)
    for packed, records in original.items():
        digits = tuple((packed // 3**vertex) % 3 for vertex in range(8))
        exponent = sum(exponent_rows[vertex][digits[vertex]] for vertex in range(8))
        character = Fraction(3) ** exponent
        assert fibre_total(scaled[packed]) == character * fibre_total(records)

    pure_words = tuple(pack_word((colour,) * 8) for colour in range(3))
    cycle_words = (
        pack_word((0, 0, 0, 0, 1, 1, 1, 1)),
        pack_word((0, 0, 1, 1, 0, 0, 1, 1)),
        pack_word((0, 1, 0, 1, 0, 1, 0, 1)),
    )
    exposed = pack_word((0, 0, 0, 0, 0, 1, 0, 0))
    assert all(fibre_total(scaled[word]) == 1 for word in pure_words)
    assert all(fibre_total(scaled[word]) == 0 for word in cycle_words)
    assert fibre_total(scaled[exposed]) != 0
    return {
        "base": 3,
        "pure_coefficients_fixed": True,
        "cycle_zeros_preserved": True,
        "exposed_coefficient_nonzero": True,
    }


def main() -> None:
    """Run the independent exact audit."""
    support = assert_support_and_balance()
    fibres = assert_word_fibres()
    holonomy = assert_holonomy_character()
    flags = assert_nonlinearity_flags()
    scaling = assert_independent_character_scaling()
    print("independent complete moment-compatible odd-holonomy audit: PASS")
    print(f"  support/balance: {support}")
    print(f"  packed fibre audit: {fibres}")
    print(f"  Laurent character audit: {holonomy}")
    print(f"  proper nonrigidity sets: {flags}")
    print(f"  independent character scaling: {scaling}")


if __name__ == "__main__":
    main()
