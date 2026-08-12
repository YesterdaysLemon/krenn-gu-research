"""Primary exact checks for aggregate-extra target attachment."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache, reduce
from itertools import combinations
from operator import mul

from sympy import Expr, Rational, groebner, simplify, symbols

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Word = tuple[int, ...]
Table = dict[Edge, tuple[int, int, Expr]]
Weights = dict[Edge, Fraction]


def edge(left: int, right: int) -> Edge:
    """Return one canonically ordered edge."""

    return (left, right) if left < right else (right, left)


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Enumerate perfect matchings by first-vertex deletion."""

    if not vertices:
        return ((),)
    first = vertices[0]
    records: list[Matching] = []
    for index, partner in enumerate(vertices[1:], start=1):
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            records.append((edge(first, partner),) + tail)
    return tuple(records)


def matching_weight(matching: Matching, table: Table) -> Expr:
    """Multiply the weights of a physical matching."""

    return simplify(reduce(mul, (table[item][2] for item in matching), Rational(1)))


def matching_record(matching: Matching, table: Table, order: int) -> tuple[Word, Expr, bool]:
    """Return induced word, weight, and diagonal flag."""

    word = [-1] * order
    diagonal = True
    for left, right in matching:
        left_label, right_label, _ = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        diagonal &= left_label == right_label
    assert all(label >= 0 for label in word)
    return tuple(word), matching_weight(matching, table), diagonal


def complete_ledger(
    table: Table, order: int
) -> dict[Word, tuple[tuple[Matching, Expr, bool], ...]]:
    """Build the complete exact word-fibre ledger."""

    ledger: defaultdict[Word, list[tuple[Matching, Expr, bool]]] = defaultdict(list)
    for matching in perfect_matchings(tuple(range(order))):
        word, value, diagonal = matching_record(matching, table, order)
        ledger[word].append((tuple(sorted(matching)), value, diagonal))
    return {word: tuple(records) for word, records in ledger.items()}


def parallel_family(parameter: Expr) -> tuple[Table, Expr]:
    """Return the complete ten-vertex pure-anchor parallel family."""

    selected = -(1 + parameter)
    raw: dict[Edge, tuple[int, int, Expr]] = {
        (0, 1): (0, 0, Rational(1)),
        (0, 2): (0, 0, Rational(1)),
        (0, 3): (0, 0, Rational(1)),
        (0, 4): (0, 0, Rational(1)),
        (0, 5): (2, 2, Rational(1)),
        (0, 6): (1, 1, Rational(1)),
        (0, 7): (2, 2, Rational(1)),
        (1, 2): (0, 1, Rational(-1)),
        (1, 3): (0, 0, Rational(1)),
        (1, 4): (1, 0, Rational(-1)),
        (1, 5): (1, 1, Rational(1)),
        (1, 6): (2, 2, Rational(1)),
        (1, 7): (0, 0, Rational(1)),
        (2, 3): (1, 1, Rational(1)),
        (2, 4): (0, 1, selected),
        (2, 5): (0, 1, parameter),
        (2, 6): (0, 0, Rational(1)),
        (2, 7): (2, 0, Rational(1)),
        (3, 4): (0, 1, Rational(1)),
        (3, 5): (0, 1, Rational(1)),
        (3, 6): (1, 0, Rational(1)),
        (3, 7): (1, 1, Rational(1)),
        (4, 5): (0, 0, Rational(1)),
        (4, 6): (1, 1, Rational(1)),
        (4, 7): (2, 2, Rational(1)),
        (5, 6): (0, 1, Rational(1)),
        (5, 7): (1, 1, Rational(1)),
        (6, 7): (1, 1, Rational(1)),
    }
    special = {
        (0, 8): (1, 1),
        (2, 8): (2, 2),
        (3, 8): (0, 0),
        (0, 9): (0, 0),
        (1, 9): (1, 1),
        (3, 9): (2, 2),
    }
    for vertex in range(8):
        labels_8 = special.get((vertex, 8), (2, 0))
        labels_9 = special.get((vertex, 9), (2, 1))
        raw[(vertex, 8)] = (*labels_8, Rational(1))
        raw[(vertex, 9)] = (*labels_9, Rational(1))
    raw[(8, 9)] = (2, 2, Rational(1))
    return raw, selected


def transition_data() -> tuple[
    tuple[Word, ...], tuple[Matching, ...], tuple[Matching, ...], Matching
]:
    """Return cycle words, selected outgoing/incoming terms, and the extra term."""

    words = (
        (0, 0, 0, 0, 1, 1, 1, 1, 2, 2),
        (0, 0, 1, 1, 0, 0, 1, 1, 2, 2),
        (0, 1, 0, 1, 0, 1, 0, 1, 2, 2),
    )
    outgoing = (
        ((0, 1), (2, 4), (3, 5), (6, 7), (8, 9)),
        ((0, 4), (1, 2), (3, 7), (5, 6), (8, 9)),
        ((0, 2), (1, 4), (3, 6), (5, 7), (8, 9)),
    )
    incoming = (
        ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9)),
        ((0, 4), (1, 5), (2, 6), (3, 7), (8, 9)),
        ((0, 2), (1, 3), (4, 6), (5, 7), (8, 9)),
    )
    extra = ((0, 1), (2, 5), (3, 4), (6, 7), (8, 9))
    return words, outgoing, incoming, extra


def endpoint_character(matching: Matching, table: Table) -> Counter[tuple[int, int]]:
    """Return the endpoint-label character of a matching."""

    result: Counter[tuple[int, int]] = Counter()
    for left, right in matching:
        left_label, right_label, _ = table[(left, right)]
        result[(left, left_label)] += 1
        result[(right, right_label)] += 1
    return result


def incidence_difference(left: Matching, right: Matching) -> Counter[Edge]:
    """Return 1_left - 1_right."""

    result: Counter[Edge] = Counter(left)
    result.subtract(right)
    return Counter({item: value for item, value in result.items() if value})


def pure_hafnian(table: Table, vertices: tuple[int, ...], colour: int) -> Expr:
    """Evaluate one exact pure-colour shore hafnian."""

    value = Rational(0)
    for matching in perfect_matchings(vertices):
        if all(table[item][0] == table[item][1] == colour for item in matching):
            value += matching_weight(matching, table)
    return simplify(value)


def assert_parallel_family() -> dict[str, object]:
    """Check the pure anchors, parallel extra, unit exit, and holonomy."""

    parameter = symbols("t")
    table, selected = parallel_family(parameter)
    words, outgoing, incoming, extra = transition_data()
    all_edges = {edge(left, right) for left in range(10) for right in range(left + 1, 10)}
    assert set(table) == all_edges

    local_labels = {
        vertex: {
            labels[0] if item[0] == vertex else labels[1]
            for item, labels in table.items()
            if vertex in item
        }
        for vertex in range(10)
    }
    assert all(labels == {0, 1, 2} for labels in local_labels.values())

    ledger = complete_ledger(table, 10)
    assert len(perfect_matchings(tuple(range(10)))) == 945
    assert len(ledger) == 776

    expected_cycle = (
        {outgoing[0], incoming[2], extra},
        {incoming[0], outgoing[1]},
        {outgoing[2], incoming[1]},
    )
    for index, word in enumerate(words):
        records = ledger[word]
        assert {record[0] for record in records} == expected_cycle[index]
        assert simplify(sum((record[1] for record in records), Rational(0))) == 0
    assert tuple(len(ledger[word]) for word in words) == (3, 2, 2)

    expected_pure = (
        ((0, 9), (1, 7), (2, 6), (3, 8), (4, 5)),
        ((0, 8), (1, 9), (2, 3), (4, 6), (5, 7)),
        ((0, 5), (1, 6), (2, 8), (3, 9), (4, 7)),
    )
    for colour, matching in enumerate(expected_pure):
        records = ledger[(colour,) * 10]
        assert records == ((matching, Rational(1), True),)

    singleton_word = (0, 0, 1, 1, 1, 1, 1, 1, 2, 2)
    singleton = ((0, 1), (2, 3), (4, 6), (5, 7), (8, 9))
    assert ledger[singleton_word] == ((singleton, Rational(1), True),)

    identically_zero = {
        word
        for word, records in ledger.items()
        if simplify(sum((record[1] for record in records), Rational(0))) == 0
    }
    assert identically_zero == set(words)

    cross_core = tuple(
        item for item in extra if table[item][0] != table[item][1]
    )
    residual = tuple(item for item in extra if item not in cross_core)
    assert set(cross_core) == {(2, 5), (3, 4)}
    assert set(residual) == {(0, 1), (6, 7), (8, 9)}
    assert tuple(
        pure_hafnian(table, vertices, colour)
        for vertices, colour in (((0, 1), 0), ((6, 7), 1), ((8, 9), 2))
    ) == (1, 1, 1)

    bridge = ((2, 3), (4, 5))
    assert table[(2, 3)][:2] == (1, 1)
    assert table[(4, 5)][:2] == (0, 0)
    transported = tuple(sorted(bridge + residual))
    assert transported == incoming[0]
    assert tuple(
        pure_hafnian(table, vertices, colour)
        for vertices, colour in (((0, 1, 4, 5), 0), ((2, 3, 6, 7), 1), ((8, 9), 2))
    ) == (1, 1, 1)

    source_difference = incidence_difference(extra, outgoing[0])
    target_difference = incidence_difference(transported, incoming[0])
    assert source_difference
    assert set(source_difference.values()) == {-1, 1}
    assert not target_difference
    assert endpoint_character(extra, table) == endpoint_character(outgoing[0], table)

    holonomy = simplify(
        reduce(mul, (matching_weight(item, table) for item in incoming), Rational(1))
        / reduce(mul, (matching_weight(item, table) for item in outgoing), Rational(1))
    )
    defect = simplify(matching_weight(extra, table) / matching_weight(outgoing[0], table))
    assert simplify(holonomy + 1 / (1 + parameter)) == 0
    assert simplify(defect + parameter / (1 + parameter)) == 0
    assert simplify(-(1 + defect) - holonomy) == 0

    x_var, t_var, h_var = symbols("x t_var H")
    basis = groebner((1 + x_var + t_var, h_var * x_var - 1), t_var, x_var, h_var)
    assert not [
        polynomial
        for polynomial in basis.polys
        if polynomial.as_expr().free_symbols <= {h_var}
    ]
    assert simplify((-1 / (1 + t_var)) * (-(1 + t_var)) - 1) == 0

    return {
        "physical_edges": len(table),
        "matching_census": len(perfect_matchings(tuple(range(10)))),
        "cycle_fibre_sizes": tuple(len(ledger[word]) for word in words),
        "pure_fibre_sizes": tuple(len(ledger[(colour,) * 10]) for colour in range(3)),
        "parallel_target_difference": dict(target_difference),
        "holonomy": holonomy,
        "singleton_unit_word": singleton_word,
    }


def scalar_weight(matching: Matching, weights: Weights) -> Fraction:
    """Multiply scalar support weights."""

    return reduce(mul, (weights.get(item, Fraction(0)) for item in matching), Fraction(1))


def supported_matchings(vertices: tuple[int, ...], weights: Weights) -> tuple[Matching, ...]:
    """List supported scalar perfect matchings."""

    return tuple(
        matching
        for matching in perfect_matchings(vertices)
        if all(weights.get(item, Fraction(0)) for item in matching)
    )


def hafnian(vertices: tuple[int, ...], weights: Weights) -> Fraction:
    """Evaluate a sparse exact scalar hafnian."""

    return sum(
        (scalar_weight(matching, weights) for matching in supported_matchings(vertices, weights)),
        Fraction(0),
    )


def conformal_minimal_zero(vertices: tuple[int, ...], weights: Weights) -> tuple[int, ...]:
    """Find the least zero whose complement still has a support matching."""

    for size in range(2, len(vertices) + 1, 2):
        for subset in combinations(vertices, size):
            complement = tuple(vertex for vertex in vertices if vertex not in subset)
            if (
                supported_matchings(subset, weights)
                and supported_matchings(complement, weights)
                and hafnian(subset, weights) == 0
            ):
                return subset
    raise AssertionError("no conformally minimal zero")


def allowed_edges(vertices: tuple[int, ...], weights: Weights) -> set[Edge]:
    """Return the union of all supported perfect matchings."""

    return {
        item for matching in supported_matchings(vertices, weights) for item in matching
    }


def active_edges(vertices: tuple[int, ...], weights: Weights) -> set[Edge]:
    """Return nonzero first-cofactor edges."""

    return {
        item
        for item, value in weights.items()
        if set(item) <= set(vertices)
        and value
        and value
        * hafnian(tuple(vertex for vertex in vertices if vertex not in item), weights)
        != 0
    }


def connected(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    """Test connectivity of a finite graph."""

    seen = {vertices[0]}
    frontier = [vertices[0]]
    while frontier:
        vertex = frontier.pop()
        for item in items:
            if vertex not in item:
                continue
            neighbour = item[0] if item[1] == vertex else item[1]
            if neighbour not in seen:
                seen.add(neighbour)
                frontier.append(neighbour)
    return seen == set(vertices)


def port_sizes(vertices: tuple[int, ...], weights: Weights, root: int) -> tuple[int, ...]:
    """Return matching-port sizes at one root."""

    records = supported_matchings(vertices, weights)
    ports = {
        item: tuple(matching for matching in records if item in matching)
        for item in allowed_edges(vertices, weights)
        if root in item
    }
    assert all(
        sum((scalar_weight(matching, weights) for matching in records), Fraction(0))
        != 0
        for records in ports.values()
    )
    return tuple(sorted(len(records) for records in ports.values()))


def assert_conformal_residual_mechanisms() -> dict[str, object]:
    """Check primitive-cycle, sparse-fan, aggregate-port, and exact embedding fixtures."""

    fixtures: list[tuple[str, tuple[int, ...], Weights, tuple[int, ...]]] = []

    cycle = (0, 1, 2, 3)
    cycle_weights = {
        (0, 1): Fraction(1),
        (1, 2): Fraction(1),
        (2, 3): Fraction(1),
        (0, 3): Fraction(-1),
        (4, 5): Fraction(3),
        (6, 7): Fraction(5),
    }
    fixtures.append(("cycle", tuple(range(6)), cycle_weights, cycle))

    fan = (0, 1, 2, 3)
    fan_weights = {
        edge(left, right): Fraction(-2 if edge(left, right) == (1, 2) else 1)
        for left in fan
        for right in fan
        if left < right
    }
    fan_weights[(4, 5)] = Fraction(3)
    fan_weights[(6, 7)] = Fraction(5)
    fixtures.append(("fan", tuple(range(6)), fan_weights, fan))

    aggregate = tuple(range(6))
    aggregate_weights = {
        (left, right): Fraction(-2 if (left, right) == (0, 3) else 1)
        for left in range(3)
        for right in range(3, 6)
    }
    aggregate_weights[(6, 7)] = Fraction(3)
    aggregate_weights[(8, 9)] = Fraction(5)
    fixtures.append(("aggregate", tuple(range(8)), aggregate_weights, aggregate))

    results: dict[str, object] = {}
    for name, shore, weights, expected in fixtures:
        residual = conformal_minimal_zero(shore, weights)
        assert residual == expected
        allowed = allowed_edges(residual, weights)
        assert allowed == active_edges(residual, weights)
        assert connected(residual, allowed)

        complement = tuple(vertex for vertex in shore if vertex not in residual)
        complement_matching = supported_matchings(complement, weights)[0]
        outside_vertices = tuple(
            vertex for vertex in sorted({v for item in weights for v in item}) if vertex not in shore
        )
        outside_matching = supported_matchings(outside_vertices, weights)[0]
        common = tuple(sorted(complement_matching + outside_matching))
        residual_matchings = supported_matchings(residual, weights)
        extended = tuple(tuple(sorted(matching + common)) for matching in residual_matchings)
        assert sum((scalar_weight(matching, weights) for matching in extended), Fraction(0)) == 0
        for left, right in zip(residual_matchings[1:], extended[1:]):
            assert incidence_difference(left, residual_matchings[0]) == incidence_difference(
                right, extended[0]
            )

        if name == "cycle":
            assert len(residual_matchings) == 2
            assert set(incidence_difference(*residual_matchings).values()) == {-1, 1}
        elif name == "fan":
            assert port_sizes(residual, weights, 0) == (1, 1, 1)
        else:
            assert port_sizes(residual, weights, 0) == (2, 2, 2)
        results[name] = {
            "residual_order": len(residual),
            "matching_count": len(residual_matchings),
            "extended_count": len(extended),
        }
    return results


def assert_minimal_template_extension() -> dict[str, object]:
    """Check why the parallel 3/2/2 template cannot keep a pure-2 anchor at order eight."""

    words, outgoing, incoming, extra = transition_data()
    used = {
        item
        for matching in (*outgoing, *incoming, extra)
        for item in matching
        if max(item) < 8
    }
    unused = {
        edge(left, right) for left in range(8) for right in range(left + 1, 8)
    } - used
    assert unused == {
        (0, 3),
        (0, 5),
        (0, 6),
        (0, 7),
        (1, 6),
        (1, 7),
        (2, 7),
        (4, 7),
    }
    assert not [
        matching
        for matching in perfect_matchings(tuple(range(8)))
        if set(matching) <= unused
    ]
    assert {right for left, right in unused if left == 2} == {7}
    assert {right for left, right in unused if left == 4} == {7}
    return {"unused_edges": len(unused), "pure_two_perfect_matching": False, "next_even_order": 10}


def main() -> None:
    """Run all primary exact checks."""

    family = assert_parallel_family()
    residuals = assert_conformal_residual_mechanisms()
    minimality = assert_minimal_template_extension()
    print("aggregate-extra target attachment primary checks: PASS")
    print(f"  parallel family: {family}")
    print(f"  conformal residuals: {residuals}")
    print(f"  template minimality: {minimality}")


if __name__ == "__main__":
    main()
