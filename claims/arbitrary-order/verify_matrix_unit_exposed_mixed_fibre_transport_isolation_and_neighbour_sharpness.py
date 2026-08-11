"""Primary exact checks for exposed-fibre isolation and neighbour sharpness."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from verify_matrix_unit_complete_pure_target_moment_compatible_odd_holonomy_sharpness import (
    auxiliary_balance,
    complete_table,
    endpoint_loads,
    perfect_matchings,
    transition_data,
)

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Monomial = tuple[Fraction, int]
Laurent = dict[int, Fraction]
SymbolicTable = dict[Edge, tuple[int, int, Monomial]]

ETA: Word = (0, 0, 0, 0, 0, 1, 0, 0)
NU: Word = (0, 2, 0, 0, 1, 1, 2, 1)


def normalized(poly: Laurent) -> Laurent:
    """Remove zero Laurent coefficients."""
    return {exponent: coefficient for exponent, coefficient in poly.items() if coefficient}


def add_term(poly: Laurent, term: Monomial) -> None:
    """Add one Laurent monomial to a sparse polynomial."""
    coefficient, exponent = term
    poly[exponent] = poly.get(exponent, Fraction(0)) + coefficient
    if not poly[exponent]:
        del poly[exponent]


def multiply(left: Monomial, right: Monomial) -> Monomial:
    """Multiply two Laurent monomials in the parameter t."""
    return left[0] * right[0], left[1] + right[1]


def divide(left: Monomial, right: Monomial) -> Monomial:
    """Divide two nonzero Laurent monomials."""
    assert right[0]
    return left[0] / right[0], left[1] - right[1]


def family_table() -> SymbolicTable:
    """Return the exact Q(t) deformation of the U7D label table."""
    labels = complete_table()
    weights: dict[Edge, Monomial] = {
        edge: (Fraction(1), 0) for edge in labels
    }
    weights.update(
        {
            (0, 6): (Fraction(1), 2),
            (1, 2): (Fraction(-1), 0),
            (1, 4): (Fraction(-1), 0),
            (2, 4): (Fraction(-1), -1),
            (3, 5): (Fraction(1), 1),
            (4, 7): (Fraction(1), -2),
        }
    )
    return {
        edge: (left_label, right_label, weights[edge])
        for edge, (left_label, right_label, _) in labels.items()
    }


def matching_record(
    matching: Matching,
    table: SymbolicTable,
) -> tuple[Word, Monomial, bool]:
    """Return the induced word, Laurent weight, and diagonal flag."""
    word = [-1] * 8
    weight: Monomial = (Fraction(1), 0)
    diagonal = True
    for edge in matching:
        left, right = edge
        left_label, right_label, scalar = table[edge]
        word[left] = left_label
        word[right] = right_label
        weight = multiply(weight, scalar)
        diagonal = diagonal and left_label == right_label
    return tuple(word), weight, diagonal


def coefficient_ledgers(table: SymbolicTable):
    """Enumerate exact Laurent coefficient and term ledgers."""
    total: dict[Word, Laurent] = {}
    diagonal: dict[Word, Laurent] = {}
    offdiagonal: dict[Word, Laurent] = {}
    terms: dict[Word, list[tuple[Matching, Monomial, bool]]] = {}
    for matching in perfect_matchings(tuple(range(8))):
        word, weight, is_diagonal = matching_record(matching, table)
        add_term(total.setdefault(word, {}), weight)
        target = diagonal if is_diagonal else offdiagonal
        add_term(target.setdefault(word, {}), weight)
        terms.setdefault(word, []).append((matching, weight, is_diagonal))
    return total, diagonal, offdiagonal, terms


def word_multiplicities(word: Word) -> tuple[int, int, int]:
    """Return the three colour multiplicities of a word."""
    return tuple(word.count(colour) for colour in range(3))


def matching_weight(matching: Matching, table: SymbolicTable) -> Monomial:
    """Multiply the Laurent weights of a physical matching."""
    result: Monomial = (Fraction(1), 0)
    for edge in matching:
        result = multiply(result, table[edge][2])
    return result


def evaluate(term: Monomial, parameter: Fraction) -> Fraction:
    """Evaluate one Laurent monomial at a nonzero rational parameter."""
    coefficient, exponent = term
    return coefficient * parameter**exponent


def assert_exposed_fibre_isolation(table: SymbolicTable) -> dict[str, object]:
    """Check the complete exposed fibre and its transport obstruction."""
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table)
    exposed_matching = ((0, 4), (1, 7), (2, 6), (3, 5))
    assert terms[ETA] == [(exposed_matching, (Fraction(1), 1), False)]
    assert total[ETA] == {1: Fraction(1)}
    assert diagonal.get(ETA, {}) == {}
    assert offdiagonal[ETA] == {1: Fraction(1)}

    pure_residual = ((0, 4), (1, 7), (2, 6))
    cross_core = ((3, 5),)
    assert matching_weight(pure_residual, table) == (Fraction(1), 0)
    assert matching_weight(cross_core, table) == (Fraction(1), 1)
    assert word_multiplicities(ETA) == (7, 1, 0)

    words, _, _, _ = transition_data()
    assert {word_multiplicities(word) for word in words} == {(4, 4, 0)}
    assert word_multiplicities(ETA) != word_multiplicities(words[0])

    # One 0--1 cross edge leaves even residual shores, but the original
    # cross counts (1,0,0) do not have the common parity required by U7B.
    cross_counts = (1, 0, 0)
    assert len({count % 2 for count in cross_counts}) == 2

    return {
        "word": ETA,
        "multiplicities": word_multiplicities(ETA),
        "complete_fibre_terms": 1,
        "active_cycle_terms": 0,
        "diagonal_rematching_terms": 0,
        "aggregate_extra_terms": 0,
        "cross_core": cross_core,
        "pure_shore_residual": pure_residual,
        "target_monomial": "t",
        "transport_parity_available": False,
    }


def assert_neighbour_subsystem(table: SymbolicTable) -> dict[str, object]:
    """Check the smallest satisfiable extra mixed equation and holonomy."""
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table)
    words, cross, bridges, _ = transition_data()
    expected_cycle = {
        words[0]: {
            ((0, 1), (2, 4), (3, 5), (6, 7)): (Fraction(-1), 0),
            ((0, 2), (1, 3), (4, 6), (5, 7)): (Fraction(1), 0),
        },
        words[1]: {
            ((0, 1), (2, 3), (4, 5), (6, 7)): (Fraction(1), 0),
            ((0, 4), (1, 2), (3, 7), (5, 6)): (Fraction(-1), 0),
        },
        words[2]: {
            ((0, 2), (1, 4), (3, 6), (5, 7)): (Fraction(-1), 0),
            ((0, 4), (1, 5), (2, 6), (3, 7)): (Fraction(1), 0),
        },
    }
    for word in words:
        assert total[word] == {}
        actual = {matching: weight for matching, weight, _ in terms[word]}
        assert actual == expected_cycle[word]

    first = ((0, 2), (1, 6), (3, 5), (4, 7))
    second = ((0, 3), (1, 6), (2, 4), (5, 7))
    assert terms[NU] == [
        (first, (Fraction(1), -1), False),
        (second, (Fraction(-1), -1), False),
    ]
    assert total[NU] == {}
    assert diagonal.get(NU, {}) == {}
    assert offdiagonal[NU] == {}
    assert word_multiplicities(NU) == (3, 3, 2)
    assert set(first) & set(second) == {(1, 6)}

    zero_words = {word for word, coefficient in total.items() if not coefficient}
    assert zero_words == set(words) | {NU}

    holonomy: Monomial = (Fraction(1), 0)
    circulation: Counter[Edge] = Counter()
    for bridge_matching, cross_matching in zip(bridges, cross):
        holonomy = multiply(
            holonomy,
            divide(
                matching_weight(bridge_matching, table),
                matching_weight(cross_matching, table),
            ),
        )
        circulation.update(bridge_matching)
        circulation.subtract(cross_matching)
    assert holonomy == (Fraction(-1), 0)
    assert len(+circulation) == 6
    assert len(-circulation) == 6

    # At t=2 this is a nonzero complete physical table satisfying all four
    # selected mixed equations and the pure targets, while eta stays nonzero.
    sample = Fraction(2)
    assert all(evaluate(data[2], sample) for data in table.values())
    assert all(not total[word] for word in words + (NU,))
    assert evaluate((Fraction(1), 1), sample) == 2

    labels = complete_table()
    loads = endpoint_loads(labels, auxiliary_balance(), 8)
    assert loads == ((Fraction(7), Fraction(7), Fraction(7)),) * 8

    return {
        "cycle_equations": 3,
        "additional_mixed_equations": 1,
        "neighbour_word": NU,
        "neighbour_multiplicities": word_multiplicities(NU),
        "neighbour_terms": ("t^-1", "-t^-1"),
        "neighbour_diagonal_aggregate": 0,
        "neighbour_offdiagonal_aggregate": 0,
        "holonomy": "-1",
        "nonzero_parameter_sample": sample,
        "exposed_coefficient_at_sample": sample,
        "strict_support_balance_preserved": True,
    }


def assert_pure_targets(table: SymbolicTable) -> dict[str, object]:
    """Check the exact pure normalizations throughout the Q(t) family."""
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table)
    expected = {
        0: ((0, 3), (1, 7), (2, 6), (4, 5)),
        1: ((0, 6), (1, 5), (2, 3), (4, 7)),
        2: ((0, 7), (1, 6), (2, 5), (3, 4)),
    }
    for colour, matching in expected.items():
        word = (colour,) * 8
        assert terms[word] == [(matching, (Fraction(1), 0), True)]
        assert total[word] == {0: Fraction(1)}
        assert diagonal[word] == {0: Fraction(1)}
        assert offdiagonal.get(word, {}) == {}
    return {
        "pure_coefficients": (1, 1, 1),
        "parameter_domain": "t!=0",
        "field": "Q(t)",
    }


def main() -> None:
    """Run all exact checks and print a compact certificate summary."""
    table = family_table()
    pure = assert_pure_targets(table)
    exposed = assert_exposed_fibre_isolation(table)
    neighbour = assert_neighbour_subsystem(table)
    print("matrix-unit exposed-fibre isolation primary checks: PASS")
    print(f"  exact Laurent family and pure targets: {pure}")
    print(f"  exposed mixed fibre: {exposed}")
    print(f"  transport-closed neighbour subsystem: {neighbour}")


if __name__ == "__main__":
    main()
