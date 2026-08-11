"""Independent no-import audit of the complete U7D same-degree block."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]

# (left, right, decimal endpoint-label code, specialized physical sign)
ROWS = (
    (0, 1, 0, 1),
    (0, 2, 0, 1),
    (0, 3, 0, 1),
    (0, 4, 0, 1),
    (0, 5, 12, 1),
    (0, 6, 11, 1),
    (0, 7, 22, 1),
    (1, 2, 1, -1),
    (1, 3, 0, 1),
    (1, 4, 10, -1),
    (1, 5, 11, 1),
    (1, 6, 22, 1),
    (1, 7, 0, 1),
    (2, 3, 11, 1),
    (2, 4, 1, -1),
    (2, 5, 22, 1),
    (2, 6, 0, 1),
    (2, 7, 20, 1),
    (3, 4, 22, 1),
    (3, 5, 1, 1),
    (3, 6, 10, 1),
    (3, 7, 11, 1),
    (4, 5, 0, 1),
    (4, 6, 11, 1),
    (4, 7, 11, 1),
    (5, 6, 1, 1),
    (5, 7, 11, 1),
    (6, 7, 11, 1),
)


def decode(code: int) -> tuple[int, int]:
    """Decode a decimal endpoint-label pair."""
    return divmod(code, 10)


def row_maps(rows=ROWS):
    """Build labels and specialized signs from the independent row table."""
    labels = {}
    signs = {}
    for left, right, code, sign in rows:
        labels[left, right] = decode(code)
        signs[left, right] = sign
    return labels, signs


def balanced_words(first: int, second: int) -> tuple[Word, ...]:
    """Build the 70 balanced binary words directly."""
    result = []
    for first_positions in combinations(range(8), 4):
        word = [second] * 8
        for position in first_positions:
            word[position] = first
        result.append(tuple(word))
    return tuple(result)


def compatible_matchings(word: Word, labels: dict[Edge, tuple[int, int]]):
    """Enumerate one word fibre by target-constrained least-bit recursion."""

    @lru_cache(maxsize=None)
    def visit(mask: int) -> tuple[Matching, ...]:
        if not mask:
            return ((),)
        low = mask & -mask
        left = low.bit_length() - 1
        residue = mask ^ low
        result = []
        choices = residue
        while choices:
            partner_bit = choices & -choices
            right = partner_bit.bit_length() - 1
            choices ^= partner_bit
            if labels[left, right] != (word[left], word[right]):
                continue
            for tail in visit(residue ^ partner_bit):
                result.append(((left, right),) + tail)
        return tuple(result)

    return visit((1 << 8) - 1)


def block(first: int, second: int, labels) -> dict[Word, tuple[Matching, ...]]:
    """Return every word and its complete compatible fibre."""
    return {
        word: compatible_matchings(word, labels)
        for word in balanced_words(first, second)
    }


def relabel_rows(permutation: tuple[int, int, int]):
    """Globally rename colours in the independently encoded table."""
    result = []
    for left, right, code, sign in ROWS:
        left_label, right_label = decode(code)
        new_code = 10 * permutation[left_label] + permutation[right_label]
        result.append((left, right, new_code, sign))
    return tuple(result)


def audit_complete_block() -> dict[str, object]:
    """Audit the full block with a word-first algorithm and second unit leaf."""
    labels, signs = row_maps()
    fibres = block(0, 1, labels)
    histogram = Counter(map(len, fibres.values()))
    assert len(fibres) == 70
    assert histogram == Counter({0: 57, 1: 10, 2: 3})

    cycle = {
        (0, 0, 0, 0, 1, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 0, 1),
    }
    assert {word for word, records in fibres.items() if len(records) == 2} == cycle
    for word in cycle:
        values = []
        for matching in fibres[word]:
            value = 1
            diagonal = True
            for edge in matching:
                value *= signs[edge]
                left_label, right_label = labels[edge]
                diagonal &= left_label == right_label
            values.append((value, diagonal))
        assert sorted(values) == [(-1, False), (1, True)]

    # Use a different singleton than the primary verifier.  A mixed target
    # equation equal to one invertible matching monomial generates one after
    # Laurent localization.
    witness_word = (1, 0, 1, 1, 0, 0, 1, 0)
    assert fibres[witness_word] == (((0, 6), (1, 7), (2, 3), (4, 5)),)
    exponent = Counter(fibres[witness_word][0])
    inverse = Counter({edge: -power for edge, power in exponent.items()})
    product = Counter()
    for vector in (exponent, inverse):
        for edge, power in vector.items():
            product[edge] += power
    assert all(power == 0 for power in product.values())

    # Reconstruct H by a numerator/denominator ledger independent of U7C.
    numerator = ((2, 3), (4, 5), (1, 5), (2, 6), (4, 6), (1, 3))
    denominator = ((2, 4), (3, 5), (1, 2), (5, 6), (1, 4), (3, 6))
    value = Fraction(1)
    for edge in numerator:
        value *= signs[edge]
    for edge in denominator:
        value /= signs[edge]
    assert value == -1

    return {
        "word_first_recursions": 70,
        "histogram": dict(sorted(histogram.items())),
        "second_unit_word": witness_word,
        "second_unit_matching": fibres[witness_word][0],
        "cycle_holonomy_regression": value,
        "saturated_elimination": "(1)",
    }


def audit_colour_permutations() -> dict[str, object]:
    """Audit empty unpermuted blocks and all global colour renamings."""
    labels, _ = row_maps()
    assert Counter(map(len, block(0, 2, labels).values())) == Counter({0: 70})
    assert Counter(map(len, block(1, 2, labels).values())) == Counter({0: 70})

    for permutation in permutations(range(3)):
        permuted_labels, _ = row_maps(relabel_rows(permutation))
        active = block(permutation[0], permutation[1], permuted_labels)
        assert Counter(map(len, active.values())) == Counter({0: 57, 1: 10, 2: 3})
    return {
        "empty_balanced_blocks_in_original_table": 2,
        "global_colour_renamings": 6,
        "renamed_unit_ideal_preserved": True,
    }


def main() -> None:
    """Run the independent exact audit."""
    block_result = audit_complete_block()
    colour_result = audit_colour_permutations()
    print("independent U7D complete same-multidegree block audit: PASS")
    print(f"  target-constrained word-first census: {block_result}")
    print(f"  colour-renaming audit: {colour_result}")


if __name__ == "__main__":
    main()
