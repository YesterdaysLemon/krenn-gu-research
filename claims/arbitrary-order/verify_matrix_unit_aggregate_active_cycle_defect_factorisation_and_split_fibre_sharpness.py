"""Primary exact checks for aggregate active-cycle defect factorisation."""

from __future__ import annotations

from collections import Counter
from functools import cache, reduce
from operator import mul

from sympy import QQ, Expr, Rational, groebner, simplify, symbols

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Word = tuple[int, ...]
Table = dict[Edge, tuple[int, int, Expr]]


def edge(left: int, right: int) -> Edge:
    """Return a canonically ordered physical pair."""

    return (left, right) if left < right else (right, left)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Enumerate perfect matchings by deleting the first vertex."""

    if not vertices:
        return ((),)
    first = vertices[0]
    records: list[Matching] = []
    for index, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            records.append((edge(first, partner),) + matching)
    return tuple(records)


def transition_data() -> tuple[
    tuple[Word, ...], tuple[Matching, ...], tuple[Matching, ...], tuple[Matching, ...]
]:
    """Return the three words and selected cross, bridge, and residual edges."""

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


def build_table(parameter: Expr) -> tuple[Table, Expr]:
    """Build the complete 28-edge aggregate-cycle family."""

    words, cross, bridges, residual = transition_data()
    selected_weight = -(1 + 2 * parameter) / 2
    cross_weights = (
        (selected_weight, Rational(1)),
        (Rational(-1), Rational(1)),
        (Rational(-1), Rational(1)),
    )
    table: Table = {}
    for index, old_word in enumerate(words):
        new_word = words[(index + 1) % len(words)]
        for position, item in enumerate(cross[index]):
            left, right = item
            labels = old_word[left], old_word[right]
            assert labels[0] != labels[1]
            table[item] = *labels, cross_weights[index][position]
        for item in bridges[index]:
            left, right = item
            labels = new_word[left], new_word[right]
            assert labels[0] == labels[1]
            table[item] = *labels, Rational(1)
        for item in residual[index]:
            left, right = item
            labels = old_word[left], old_word[right]
            assert labels[0] == labels[1]
            table[item] = *labels, Rational(1)

    aggregate_edges = {
        (0, 3): (0, 0, Rational(1)),
        (1, 6): (0, 1, Rational(1)),
        (2, 5): (0, 1, Rational(1)),
        (4, 7): (1, 1, parameter),
    }
    completion_edges = {
        (0, 5): (1, 2, Rational(1)),
        (0, 6): (2, 2, Rational(1)),
        (0, 7): (1, 0, Rational(1)),
        (1, 7): (2, 2, Rational(1)),
        (2, 7): (2, 0, Rational(1)),
        (3, 4): (2, 2, Rational(1)),
    }
    assert not (set(table) & set(aggregate_edges))
    table.update(aggregate_edges)
    assert not (set(table) & set(completion_edges))
    table.update(completion_edges)
    assert len(table) == 28
    return table, selected_weight


def matching_record(matching: Matching, table: Table) -> tuple[Word, Expr, bool]:
    """Return the induced word, scalar product, and diagonal flag."""

    word = [-1] * 8
    values: list[Expr] = []
    diagonal = True
    for left, right in matching:
        left_label, right_label, value = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        values.append(value)
        diagonal &= left_label == right_label
    assert all(label >= 0 for label in word)
    return tuple(word), reduce(mul, values, Rational(1)), diagonal


def compatible_terms(table: Table, word: Word) -> tuple[tuple[Matching, Expr, bool], ...]:
    """Enumerate the complete physical matching fibre of a word."""

    records = []
    for matching in perfect_matchings(tuple(range(8))):
        induced, value, diagonal = matching_record(matching, table)
        if induced == word:
            records.append((tuple(sorted(matching)), simplify(value), diagonal))
    return tuple(records)


def matching_weight(matching: Matching, table: Table) -> Expr:
    """Multiply the physical weights of a matching."""

    return simplify(reduce(mul, (table[item][2] for item in matching), Rational(1)))


def endpoint_character(matching: Matching, table: Table) -> Counter[tuple[int, int]]:
    """Return the endpoint-label character of one matching."""

    result: Counter[tuple[int, int]] = Counter()
    for left, right in matching:
        left_label, right_label, _ = table[(left, right)]
        result[(left, left_label)] += 1
        result[(right, right_label)] += 1
    return result


def assert_complete_family() -> dict[str, object]:
    """Check support, local labels, complete fibres, defects, and holonomy."""

    parameter = symbols("t")
    table, selected_weight = build_table(parameter)
    words, cross, bridges, residual = transition_data()

    assert set(table) == {
        edge(left, right) for left in range(8) for right in range(left + 1, 8)
    }
    local_labels = {
        vertex: {
            labels[0] if item[0] == vertex else labels[1]
            for item, labels in table.items()
            if vertex in item
        }
        for vertex in range(8)
    }
    assert all(labels == {0, 1, 2} for labels in local_labels.values())

    expected_matchings = (
        {
            ((0, 1), (2, 4), (3, 5), (6, 7)),
            ((0, 2), (1, 3), (4, 6), (5, 7)),
            ((0, 2), (1, 6), (3, 5), (4, 7)),
            ((0, 3), (1, 6), (2, 4), (5, 7)),
            ((0, 3), (1, 6), (2, 5), (4, 7)),
        },
        {
            ((0, 1), (2, 3), (4, 5), (6, 7)),
            ((0, 4), (1, 2), (3, 7), (5, 6)),
        },
        {
            ((0, 2), (1, 4), (3, 6), (5, 7)),
            ((0, 4), (1, 5), (2, 6), (3, 7)),
        },
    )
    expected_weights = (
        sorted((Rational(1), selected_weight, parameter, selected_weight, parameter), key=str),
        sorted((Rational(1), Rational(-1)), key=str),
        sorted((Rational(1), Rational(-1)), key=str),
    )

    fibre_terms = tuple(compatible_terms(table, word) for word in words)
    for index, terms in enumerate(fibre_terms):
        assert {record[0] for record in terms} == expected_matchings[index]
        assert sorted((record[1] for record in terms), key=str) == expected_weights[index]
        assert simplify(sum((record[1] for record in terms), Rational(0))) == 0
    assert tuple(len(terms) for terms in fibre_terms) == (5, 2, 2)

    full_cross = tuple(tuple(sorted(cross[i] + residual[i])) for i in range(3))
    full_bridge = tuple(tuple(sorted(bridges[i] + residual[i])) for i in range(3))
    holonomy = simplify(
        reduce(mul, (matching_weight(item, table) for item in full_bridge), Rational(1))
        / reduce(mul, (matching_weight(item, table) for item in full_cross), Rational(1))
    )
    assert simplify(holonomy - 1 / selected_weight) == 0
    assert simplify(holonomy + 2 / (1 + 2 * parameter)) == 0

    incoming = full_bridge[2]
    outgoing = full_cross[0]
    extras = tuple(
        record for record in fibre_terms[0] if record[0] not in {incoming, outgoing}
    )
    defect = simplify(sum((record[1] for record in extras), Rational(0)) / selected_weight)
    assert simplify(defect - (selected_weight + 2 * parameter) / selected_weight) == 0
    assert simplify(-1 * (1 + defect) - holonomy) == 0

    outgoing_character = endpoint_character(outgoing, table)
    for matching, _, _ in extras:
        assert endpoint_character(matching, table) == outgoing_character

    pure_counts = tuple(len(compatible_terms(table, (colour,) * 8)) for colour in range(3))
    assert pure_counts == (0, 0, 0)

    split_values = sorted(
        (simplify(record[1].subs(parameter, Rational(1, 2))) for record in extras)
    )
    assert split_values == [Rational(-1), Rational(1, 2), Rational(1, 2)]
    assert simplify(defect.subs(parameter, Rational(1, 2))) == 0
    assert simplify(holonomy.subs(parameter, Rational(1, 2))) == -1

    assert simplify(defect.subs(parameter, Rational(1))) == Rational(-1, 3)
    assert simplify(holonomy.subs(parameter, Rational(1))) == Rational(-2, 3)

    return {
        "physical_edges": len(table),
        "local_label_sets": tuple(sorted(labels) for labels in local_labels.values()),
        "cycle_fibre_sizes": tuple(len(terms) for terms in fibre_terms),
        "holonomy": holonomy,
        "aggregate_defect": defect,
        "pure_fibre_sizes": pure_counts,
    }


def assert_endpoint_circulation() -> dict[str, object]:
    """Check that the selected holonomy exponent lies in the character kernel."""

    parameter = symbols("t")
    table, _ = build_table(parameter)
    _, cross, bridges, _ = transition_data()
    exponent: Counter[Edge] = Counter()
    for matching in bridges:
        exponent.update(matching)
    for matching in cross:
        exponent.subtract(matching)
    exponent = Counter({item: value for item, value in exponent.items() if value})
    assert set(exponent.values()) == {-1, 1}

    endpoint: Counter[tuple[int, int]] = Counter()
    for item, value in exponent.items():
        left_label, right_label, _ = table[item]
        endpoint[(item[0], left_label)] += value
        endpoint[(item[1], right_label)] += value
    assert all(value == 0 for value in endpoint.values())
    return {
        "circulation_edges": len(exponent),
        "endpoint_character_zero": True,
    }


def assert_zero_elimination() -> dict[str, object]:
    """Check the small polynomial elimination before Laurent localization."""

    selected_weight, parameter, holonomy = symbols("x t H")
    basis = groebner(
        [1 + 2 * selected_weight + 2 * parameter, holonomy * selected_weight - 1],
        selected_weight,
        parameter,
        holonomy,
        order="lex",
        domain=QQ,
    )
    holonomy_only = [
        polynomial.as_expr()
        for polynomial in basis.polys
        if not polynomial.as_expr().has(selected_weight, parameter)
    ]
    assert holonomy_only == []
    substituted = simplify((-2 / (1 + 2 * parameter)) * (-(1 + 2 * parameter) / 2))
    assert substituted == 1
    return {
        "groebner_basis": tuple(polynomial.as_expr() for polynomial in basis.polys),
        "holonomy_only_generators": tuple(holonomy_only),
        "elimination_ideal": "zero",
    }


def main() -> None:
    family = assert_complete_family()
    circulation = assert_endpoint_circulation()
    elimination = assert_zero_elimination()
    print("complete aggregate-cycle family:", family)
    print("endpoint circulation:", circulation)
    print("holonomy elimination:", elimination)
    print("aggregate active-cycle defect factorisation primary checks: PASS")


if __name__ == "__main__":
    main()
