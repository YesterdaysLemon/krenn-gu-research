"""Primary exact checks for complete moment-compatible odd holonomy."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Table = dict[Edge, tuple[int, int, Fraction]]


def complete_table() -> Table:
    """Return the complete eight-vertex matrix-unit phase table."""
    raw = {
        (0, 1): (0, 0, 1),
        (0, 2): (0, 0, 1),
        (0, 3): (0, 0, 1),
        (0, 4): (0, 0, 1),
        (0, 5): (1, 2, 1),
        (0, 6): (1, 1, 1),
        (0, 7): (2, 2, 1),
        (1, 2): (0, 1, -1),
        (1, 3): (0, 0, 1),
        (1, 4): (1, 0, -1),
        (1, 5): (1, 1, 1),
        (1, 6): (2, 2, 1),
        (1, 7): (0, 0, 1),
        (2, 3): (1, 1, 1),
        (2, 4): (0, 1, -1),
        (2, 5): (2, 2, 1),
        (2, 6): (0, 0, 1),
        (2, 7): (2, 0, 1),
        (3, 4): (2, 2, 1),
        (3, 5): (0, 1, 1),
        (3, 6): (1, 0, 1),
        (3, 7): (1, 1, 1),
        (4, 5): (0, 0, 1),
        (4, 6): (1, 1, 1),
        (4, 7): (1, 1, 1),
        (5, 6): (0, 1, 1),
        (5, 7): (1, 1, 1),
        (6, 7): (1, 1, 1),
    }
    return {
        edge: (left_label, right_label, Fraction(weight))
        for edge, (left_label, right_label, weight) in raw.items()
    }


def auxiliary_balance() -> dict[Edge, Fraction]:
    """Return the strictly positive incidence-dual certificate."""
    values = (
        1,
        1,
        4,
        1,
        6,
        1,
        7,
        4,
        1,
        3,
        4,
        7,
        1,
        3,
        2,
        1,
        4,
        6,
        7,
        2,
        3,
        1,
        3,
        1,
        4,
        4,
        1,
        1,
    )
    edges = tuple(combinations(range(8), 2))
    return dict(zip(edges, map(Fraction, values), strict=True))


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate all perfect matchings recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        residue = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(residue):
            yield ((first, partner),) + tail


def matching_record(
    matching: Matching,
    table: Table,
    order: int,
) -> tuple[Word, Fraction, bool]:
    """Return the induced word, scalar, and diagonal flag."""
    word = [-1] * order
    weight = Fraction(1)
    diagonal = True
    for left, right in matching:
        left_label, right_label, scalar = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        weight *= scalar
        diagonal = diagonal and left_label == right_label
    return tuple(word), weight, diagonal


def coefficient_ledgers(table: Table, order: int):
    """Enumerate complete total, diagonal, offdiagonal, and term ledgers."""
    total: dict[Word, Fraction] = {}
    diagonal: dict[Word, Fraction] = {}
    offdiagonal: dict[Word, Fraction] = {}
    terms: dict[Word, list[tuple[Matching, Fraction, bool]]] = {}
    for matching in perfect_matchings(tuple(range(order))):
        word, weight, is_diagonal = matching_record(matching, table, order)
        total[word] = total.get(word, Fraction(0)) + weight
        target = diagonal if is_diagonal else offdiagonal
        target[word] = target.get(word, Fraction(0)) + weight
        terms.setdefault(word, []).append((matching, weight, is_diagonal))
    return total, diagonal, offdiagonal, terms


def endpoint_loads(
    table: Table,
    edge_values: dict[Edge, Fraction],
    order: int,
) -> tuple[tuple[Fraction, Fraction, Fraction], ...]:
    """Collect an edge value at its two labelled endpoints."""
    loads = [[Fraction(0), Fraction(0), Fraction(0)] for _ in range(order)]
    for (left, right), (left_label, right_label, _) in table.items():
        value = edge_values[(left, right)]
        loads[left][left_label] += value
        loads[right][right_label] += value
    return tuple(tuple(row) for row in loads)


def restricted_incidence_matrix(table: Table, order: int) -> list[list[Fraction]]:
    """Return edge exponents on a zero-colour-sum GHZ basis."""
    anchor = order - 1
    basis = [
        (vertex, colour)
        for colour in range(3)
        for vertex in range(order - 1)
    ]
    rows: list[list[Fraction]] = []
    for (left, right), (left_label, right_label, _) in table.items():
        row = []
        for vertex, colour in basis:
            value = int((left, left_label) == (vertex, colour))
            value += int((right, right_label) == (vertex, colour))
            value -= int((left, left_label) == (anchor, colour))
            value -= int((right, right_label) == (anchor, colour))
            row.append(Fraction(value))
        rows.append(row)
    return rows


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    """Compute exact rational row rank by Gaussian elimination."""
    work = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def term_dictionary(
    records: list[tuple[Matching, Fraction, bool]],
) -> dict[Matching, tuple[Fraction, bool]]:
    """Index a compatible fibre by its physical matching."""
    return {matching: (weight, diagonal) for matching, weight, diagonal in records}


def transition_data():
    """Return the words, cross cores, bridges, and residual matchings."""
    words = (
        (0, 0, 0, 0, 1, 1, 1, 1),
        (0, 0, 1, 1, 0, 0, 1, 1),
        (0, 1, 0, 1, 0, 1, 0, 1),
    )
    cross = (
        ((2, 4), (3, 5)),
        ((1, 2), (5, 6)),
        ((1, 4), (3, 6)),
    )
    bridges = (
        ((2, 3), (4, 5)),
        ((1, 5), (2, 6)),
        ((4, 6), (1, 3)),
    )
    residual = (
        ((0, 1), (6, 7)),
        ((0, 4), (3, 7)),
        ((0, 2), (5, 7)),
    )
    return words, cross, bridges, residual


def laurent_value(exponents: Counter[Edge], table: Table) -> Fraction:
    """Evaluate an integral Laurent edge monomial exactly."""
    value = Fraction(1)
    for edge, exponent in exponents.items():
        value *= table[edge][2] ** exponent
    return value


def power_of_two(exponent: int) -> Fraction:
    """Return an exact integral power of two."""
    if exponent >= 0:
        return Fraction(2**exponent)
    return Fraction(1, 2 ** (-exponent))


def scaled_table(table: Table, beta: dict[tuple[int, int], int]) -> Table:
    """Apply an exact diagonal GHZ scaling to every physical amplitude."""
    result = {}
    for (left, right), (left_label, right_label, weight) in table.items():
        exponent = beta[(left, left_label)] + beta[(right, right_label)]
        result[(left, right)] = (
            left_label,
            right_label,
            weight * power_of_two(exponent),
        )
    return result


def word_character(word: Word, beta: dict[tuple[int, int], int]) -> Fraction:
    """Evaluate the exact character of one word under a power-of-two gauge."""
    exponent = sum(beta[(vertex, colour)] for vertex, colour in enumerate(word))
    return power_of_two(exponent)


def nonrigidity_sets(table: Table) -> tuple[frozenset[int], ...]:
    """Compute all three oriented colour-nonrigidity sets."""
    result = []
    for colour in range(3):
        active = set()
        for (left, right), (left_label, right_label, _) in table.items():
            if left_label != colour and right_label == colour:
                active.add(left)
            if right_label != colour and left_label == colour:
                active.add(right)
        result.append(frozenset(active))
    return tuple(result)


def assert_complete_balance(table: Table) -> dict[str, object]:
    """Check complete support and the strict integral balance certificate."""
    edges = set(combinations(range(8), 2))
    assert set(table) == edges
    assert {data[2] for data in table.values()} == {Fraction(-1), Fraction(1)}
    assert {edge for edge, data in table.items() if data[2] < 0} == {
        (1, 2),
        (1, 4),
        (2, 4),
    }

    balance = auxiliary_balance()
    assert set(balance) == edges
    assert all(value > 0 and value.denominator == 1 for value in balance.values())
    loads = endpoint_loads(table, balance, 8)
    assert loads == ((Fraction(7), Fraction(7), Fraction(7)),) * 8

    incidence = restricted_incidence_matrix(table, 8)
    assert matrix_rank(incidence) == 18
    pairing = tuple(
        sum(balance[edge] * incidence[index][column] for index, edge in enumerate(table))
        for column in range(21)
    )
    assert pairing == (Fraction(0),) * 21

    unit_loads = endpoint_loads(table, {edge: Fraction(1) for edge in table}, 8)
    assert len(set(unit_loads)) > 1
    return {
        "physical_pairs": len(table),
        "common_auxiliary_loads": loads[0],
        "incidence_rank": 18,
        "edgewise_stabilizer_dimension": 3,
        "unit_amplitudes_initially_balanced": False,
    }


def assert_fibres_and_holonomy(table: Table) -> dict[str, object]:
    """Check pure targets, the complete binomial cycle, and exposed failure."""
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table, 8)
    assert sum(len(records) for records in terms.values()) == 105
    assert len(terms) == 101
    assert sum(value == 0 for value in total.values()) == 4

    expected_pure = {
        0: {((0, 3), (1, 7), (2, 6), (4, 5)): (Fraction(1), True)},
        1: {((0, 6), (1, 5), (2, 3), (4, 7)): (Fraction(1), True)},
        2: {((0, 7), (1, 6), (2, 5), (3, 4)): (Fraction(1), True)},
    }
    for colour in range(3):
        word = (colour,) * 8
        assert total[word] == Fraction(1)
        assert diagonal[word] == Fraction(1)
        assert offdiagonal.get(word, Fraction(0)) == 0
        assert term_dictionary(terms[word]) == expected_pure[colour]

    words, cross, bridges, residual = transition_data()
    expected_cycle = {
        words[0]: {
            ((0, 1), (2, 4), (3, 5), (6, 7)): (Fraction(-1), False),
            ((0, 2), (1, 3), (4, 6), (5, 7)): (Fraction(1), True),
        },
        words[1]: {
            ((0, 1), (2, 3), (4, 5), (6, 7)): (Fraction(1), True),
            ((0, 4), (1, 2), (3, 7), (5, 6)): (Fraction(-1), False),
        },
        words[2]: {
            ((0, 2), (1, 4), (3, 6), (5, 7)): (Fraction(-1), False),
            ((0, 4), (1, 5), (2, 6), (3, 7)): (Fraction(1), True),
        },
    }
    for word in words:
        assert total[word] == 0
        assert diagonal[word] == 1
        assert offdiagonal[word] == -1
        assert term_dictionary(terms[word]) == expected_cycle[word]

    circulation: Counter[Edge] = Counter()
    for bridge_matching, cross_matching in zip(bridges, cross):
        circulation.update(bridge_matching)
        circulation.subtract(cross_matching)
    circulation = Counter(
        {edge: exponent for edge, exponent in circulation.items() if exponent}
    )
    assert len(circulation) == 12
    assert set(circulation.values()) == {-1, 1}

    endpoint_character: Counter[tuple[int, int]] = Counter()
    for (left, right), exponent in circulation.items():
        left_label, right_label, _ = table[(left, right)]
        endpoint_character[(left, left_label)] += exponent
        endpoint_character[(right, right_label)] += exponent
    assert not +endpoint_character
    assert laurent_value(circulation, table) == Fraction(-1)

    exposed = (0, 0, 0, 0, 0, 1, 0, 0)
    exposed_matching = ((0, 4), (1, 7), (2, 6), (3, 5))
    assert total[exposed] == 1
    assert term_dictionary(terms[exposed]) == {
        exposed_matching: (Fraction(1), False)
    }

    sets = nonrigidity_sets(table)
    assert sets == (
        frozenset({1, 2, 3, 4, 5, 6}),
        frozenset({1, 2, 3, 4, 5, 6}),
        frozenset({0, 7}),
    )
    assert all(sets) and all(len(active) < 8 for active in sets)
    return {
        "perfect_matchings": 105,
        "induced_words": len(terms),
        "pure_coefficients": (Fraction(1),) * 3,
        "binomial_cycle_length": 3,
        "holonomy": Fraction(-1),
        "exposed_mixed_word": exposed,
        "proper_nonrigidity_sets": tuple(tuple(sorted(active)) for active in sets),
    }


def assert_character_covariance(table: Table) -> dict[str, object]:
    """Replay exact coefficient and holonomy covariance under one GHZ gauge."""
    beta_rows = (
        (1, 0, 0),
        (-1, 1, 0),
        (0, -1, 1),
        (0, 0, -1),
        (2, -2, 0),
        (-2, 2, 0),
        (1, 0, -1),
        (-1, 0, 1),
    )
    assert tuple(sum(row[colour] for row in beta_rows) for colour in range(3)) == (
        0,
        0,
        0,
    )
    beta = {
        (vertex, colour): beta_rows[vertex][colour]
        for vertex in range(8)
        for colour in range(3)
    }
    gauged = scaled_table(table, beta)
    original_total, _, _, _ = coefficient_ledgers(table, 8)
    gauged_total, _, _, _ = coefficient_ledgers(gauged, 8)
    for word, coefficient in original_total.items():
        assert gauged_total[word] == word_character(word, beta) * coefficient

    words, cross, bridges, _ = transition_data()
    circulation: Counter[Edge] = Counter()
    for bridge_matching, cross_matching in zip(bridges, cross):
        circulation.update(bridge_matching)
        circulation.subtract(cross_matching)
    assert laurent_value(circulation, gauged) == laurent_value(circulation, table)
    assert all(gauged_total[word] == 0 for word in words)
    assert all(gauged_total[(colour,) * 8] == 1 for colour in range(3))
    exposed = (0, 0, 0, 0, 0, 1, 0, 0)
    assert gauged_total[exposed] != 0
    return {
        "sample_gauge_nontrivial": gauged != table,
        "pure_coefficients_fixed": True,
        "cycle_zeros_preserved": True,
        "holonomy_fixed": True,
        "exposed_coefficient_nonzero": True,
    }


def main() -> None:
    """Run all exact checks and print a compact certificate summary."""
    table = complete_table()
    balance = assert_complete_balance(table)
    fibres = assert_fibres_and_holonomy(table)
    covariance = assert_character_covariance(table)
    print("matrix-unit complete moment-compatible odd-holonomy checks: PASS")
    print(f"  complete strict support balance: {balance}")
    print(f"  pure/binomial/exposed fibres: {fibres}")
    print(f"  exact GHZ character covariance: {covariance}")


if __name__ == "__main__":
    main()
