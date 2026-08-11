"""Primary exact checks for the complete U7D same-multidegree block."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations

from verify_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness import (
    complete_table,
    matching_record,
    perfect_matchings,
    transition_data,
)

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]


EXPECTED_SUPPORTED: dict[Word, tuple[Matching, ...]] = {
    (0, 0, 0, 0, 1, 1, 1, 1): (
        ((0, 1), (2, 4), (3, 5), (6, 7)),
        ((0, 2), (1, 3), (4, 6), (5, 7)),
    ),
    (0, 0, 0, 1, 1, 0, 1, 1): (((0, 1), (2, 4), (3, 7), (5, 6)),),
    (0, 0, 0, 1, 1, 1, 0, 1): (((0, 1), (2, 4), (3, 6), (5, 7)),),
    (0, 0, 1, 0, 0, 1, 1, 1): (((0, 4), (1, 2), (3, 5), (6, 7)),),
    (0, 0, 1, 0, 1, 0, 1, 1): (((0, 3), (1, 2), (4, 7), (5, 6)),),
    (0, 0, 1, 1, 0, 0, 1, 1): (
        ((0, 1), (2, 3), (4, 5), (6, 7)),
        ((0, 4), (1, 2), (3, 7), (5, 6)),
    ),
    (0, 0, 1, 1, 0, 1, 0, 1): (((0, 4), (1, 2), (3, 6), (5, 7)),),
    (0, 1, 0, 0, 0, 1, 1, 1): (((0, 2), (1, 4), (3, 5), (6, 7)),),
    (0, 1, 0, 0, 1, 1, 0, 1): (((0, 3), (1, 5), (2, 6), (4, 7)),),
    (0, 1, 0, 1, 0, 0, 1, 1): (((0, 2), (1, 4), (3, 7), (5, 6)),),
    (0, 1, 0, 1, 0, 1, 0, 1): (
        ((0, 2), (1, 4), (3, 6), (5, 7)),
        ((0, 4), (1, 5), (2, 6), (3, 7)),
    ),
    (1, 0, 0, 0, 1, 1, 1, 0): (((0, 6), (1, 7), (2, 4), (3, 5)),),
    (1, 0, 1, 1, 0, 0, 1, 0): (((0, 6), (1, 7), (2, 3), (4, 5)),),
}


def support_fibres(table) -> dict[Word, tuple[Matching, ...]]:
    """Group all physical perfect matchings by their endpoint-label word."""
    fibres: dict[Word, list[Matching]] = {}
    for matching in perfect_matchings(tuple(range(8))):
        word, _, _ = matching_record(matching, table, 8)
        fibres.setdefault(word, []).append(matching)
    return {word: tuple(records) for word, records in fibres.items()}


def balanced_words(first: int, second: int) -> tuple[Word, ...]:
    """Return all eight-letter words with four copies of each named colour."""
    records = []
    for first_positions in combinations(range(8), 4):
        word = [second] * 8
        for position in first_positions:
            word[position] = first
        records.append(tuple(word))
    return tuple(records)


def block_histogram(
    fibres: dict[Word, tuple[Matching, ...]], first: int, second: int
) -> Counter[int]:
    """Count complete fibre sizes throughout one balanced binary block."""
    return Counter(len(fibres.get(word, ())) for word in balanced_words(first, second))


def edge_exponent(matching: Matching) -> Counter[Edge]:
    """Return the square-free Laurent exponent vector of one matching."""
    return Counter(matching)


def add_exponents(*vectors: Counter[Edge]) -> Counter[Edge]:
    """Add Laurent exponent vectors without Counter's positive-part truncation."""
    result: Counter[Edge] = Counter()
    for vector in vectors:
        for edge, exponent in vector.items():
            result[edge] += exponent
    return Counter({edge: exponent for edge, exponent in result.items() if exponent})


def permuted_table(table, permutation: tuple[int, int, int]):
    """Globally rename all three endpoint colours."""
    return {
        edge: (permutation[left], permutation[right], weight)
        for edge, (left, right, weight) in table.items()
    }


def assert_complete_same_degree_block() -> dict[str, object]:
    """Check the exact 70-word census and one Laurent-unit certificate."""
    table = complete_table()
    fibres = support_fibres(table)
    words = balanced_words(0, 1)
    assert len(words) == 70
    assert block_histogram(fibres, 0, 1) == Counter({0: 57, 1: 10, 2: 3})

    supported = {word: fibres[word] for word in words if word in fibres}
    assert supported == EXPECTED_SUPPORTED

    cycle_words, crosses, bridges, _ = transition_data()
    assert {word for word, records in supported.items() if len(records) == 2} == set(
        cycle_words
    )
    for word in cycle_words:
        records = [matching_record(matching, table, 8) for matching in fibres[word]]
        assert sorted((weight, diagonal) for _, weight, diagonal in records) == [
            (-1, False),
            (1, True),
        ]

    # This one complete target equation is a monomial.  Its formal inverse is
    # present in the Laurent ring, so their product is the exponent-zero unit.
    singleton_word = (0, 0, 0, 1, 1, 0, 1, 1)
    singleton_matching = fibres[singleton_word][0]
    assert singleton_matching == ((0, 1), (2, 4), (3, 7), (5, 6))
    monomial = edge_exponent(singleton_matching)
    inverse = Counter({edge: -exponent for edge, exponent in monomial.items()})
    assert not add_exponents(monomial, inverse)
    assert all(table[edge][2] for edge in singleton_matching)

    # Reconstruct the already-proved holonomy exponent and its specialized
    # value only as an upstream regression.  The singleton makes the enlarged
    # same-degree ideal the unit ideal before any elimination is needed.
    holonomy_exponent: Counter[Edge] = Counter()
    holonomy_value = Fraction(1)
    for bridge, cross in zip(bridges, crosses, strict=True):
        holonomy_exponent = add_exponents(
            holonomy_exponent,
            edge_exponent(bridge),
            Counter({edge: -1 for edge in cross}),
        )
        for edge in bridge:
            holonomy_value *= table[edge][2]
        for edge in cross:
            holonomy_value /= table[edge][2]
    assert len(holonomy_exponent) == 12
    assert holonomy_value == -1

    return {
        "multidegree": (4, 4, 0),
        "words": len(words),
        "empty_fibres": 57,
        "singleton_fibres": 10,
        "binomial_fibres": 3,
        "cycle_is_all_binomials": True,
        "unit_certificate_word": singleton_word,
        "unit_certificate_matching": singleton_matching,
        "saturated_ideal": "(1)",
        "elimination_in_Q[H]": "(1)",
    }


def assert_colour_permutation_boundary() -> dict[str, object]:
    """Separate empty blocks in this table from globally permuted copies."""
    table = complete_table()
    fibres = support_fibres(table)
    assert block_histogram(fibres, 0, 2) == Counter({0: 70})
    assert block_histogram(fibres, 1, 2) == Counter({0: 70})

    checked = 0
    for permutation in permutations(range(3)):
        relabelled = permuted_table(table, permutation)
        relabelled_fibres = support_fibres(relabelled)
        first, second, absent = (
            permutation[0],
            permutation[1],
            permutation[2],
        )
        assert {first, second, absent} == {0, 1, 2}
        assert block_histogram(relabelled_fibres, first, second) == Counter(
            {0: 57, 1: 10, 2: 3}
        )
        transformed_singleton = tuple(
            permutation[colour] for colour in (0, 0, 0, 1, 1, 0, 1, 1)
        )
        assert len(relabelled_fibres[transformed_singleton]) == 1
        checked += 1

    return {
        "unpermuted_02_block": "70 empty fibres",
        "unpermuted_12_block": "70 empty fibres",
        "global_colour_permutations_checked": checked,
        "permuted_active_block_elimination": "(1)",
    }


def main() -> None:
    """Run the primary exact finite checks."""
    block = assert_complete_same_degree_block()
    colours = assert_colour_permutation_boundary()
    print("U7D complete same-multidegree target-block primary checks: PASS")
    print(f"  complete (4,4,0) census and Laurent unit: {block}")
    print(f"  colour-permutation boundary: {colours}")


if __name__ == "__main__":
    main()
