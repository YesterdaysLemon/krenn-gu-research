"""Independent no-import audit for aggregate-extra target attachment.

This audit deliberately imports neither repository code nor a symbolic-algebra
package.  It uses edge-index bitmasks, exact coefficient tuples, and separate
pure-residual fixtures.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations

Edge = tuple[int, int]
Matching = tuple[Edge, ...]
Word = tuple[int, ...]
Polynomial = tuple[Fraction, ...]
Table = dict[Edge, tuple[int, int, Polynomial]]
Weights = dict[Edge, Fraction]

ZERO: Polynomial = (Fraction(0),)
ONE: Polynomial = (Fraction(1),)
PARAMETER: Polynomial = (Fraction(0), Fraction(1))
SELECTED: Polynomial = (Fraction(-1), Fraction(-1))


def trim(value: tuple[Fraction, ...]) -> Polynomial:
    """Remove trailing zero coefficients."""

    records = list(value)
    while len(records) > 1 and records[-1] == 0:
        records.pop()
    return tuple(records)


def add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add exact coefficient tuples."""

    size = max(len(left), len(right))
    return trim(
        tuple(
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        )
    )


def scale(value: Polynomial, scalar: Fraction | int) -> Polynomial:
    """Scale an exact coefficient tuple."""

    return trim(tuple(Fraction(scalar) * item for item in value))


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply exact coefficient tuples."""

    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return trim(tuple(result))


def power(value: Polynomial, exponent: int) -> Polynomial:
    """Raise an exact polynomial to a nonnegative power."""

    result = ONE
    for _ in range(exponent):
        result = multiply(result, value)
    return result


def edge(left: int, right: int) -> Edge:
    """Return one canonically ordered edge."""

    return (left, right) if left < right else (right, left)


def constant(value: int | Fraction) -> Polynomial:
    """Return one constant polynomial."""

    return (Fraction(value),)


def parallel_table() -> Table:
    """Build the ten-vertex table independently."""

    raw: Table = {
        (0, 1): (0, 0, ONE),
        (0, 2): (0, 0, ONE),
        (0, 3): (0, 0, ONE),
        (0, 4): (0, 0, ONE),
        (0, 5): (2, 2, ONE),
        (0, 6): (1, 1, ONE),
        (0, 7): (2, 2, ONE),
        (1, 2): (0, 1, constant(-1)),
        (1, 3): (0, 0, ONE),
        (1, 4): (1, 0, constant(-1)),
        (1, 5): (1, 1, ONE),
        (1, 6): (2, 2, ONE),
        (1, 7): (0, 0, ONE),
        (2, 3): (1, 1, ONE),
        (2, 4): (0, 1, SELECTED),
        (2, 5): (0, 1, PARAMETER),
        (2, 6): (0, 0, ONE),
        (2, 7): (2, 0, ONE),
        (3, 4): (0, 1, ONE),
        (3, 5): (0, 1, ONE),
        (3, 6): (1, 0, ONE),
        (3, 7): (1, 1, ONE),
        (4, 5): (0, 0, ONE),
        (4, 6): (1, 1, ONE),
        (4, 7): (2, 2, ONE),
        (5, 6): (0, 1, ONE),
        (5, 7): (1, 1, ONE),
        (6, 7): (1, 1, ONE),
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
        raw[(vertex, 8)] = (*special.get((vertex, 8), (2, 0)), ONE)
        raw[(vertex, 9)] = (*special.get((vertex, 9), (2, 1)), ONE)
    raw[(8, 9)] = (2, 2, ONE)
    return raw


EDGES_10 = tuple(combinations(range(10), 2))
EDGE_INDEX_10 = {item: index for index, item in enumerate(EDGES_10)}


@cache
def matching_masks(vertex_mask: int) -> tuple[int, ...]:
    """Enumerate perfect matchings as 45-bit edge masks."""

    if vertex_mask == 0:
        return (0,)
    first_bit = vertex_mask & -vertex_mask
    first = first_bit.bit_length() - 1
    residue = vertex_mask ^ first_bit
    records: list[int] = []
    partners = residue
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        item_mask = 1 << EDGE_INDEX_10[edge(first, partner)]
        for tail in matching_masks(residue ^ partner_bit):
            records.append(item_mask | tail)
        partners ^= partner_bit
    return tuple(records)


def decode(mask: int) -> Matching:
    """Decode one physical edge mask."""

    return tuple(item for index, item in enumerate(EDGES_10) if mask & (1 << index))


def mask_record(mask: int, table: Table) -> tuple[Word, Polynomial, bool]:
    """Compute word, custom polynomial weight, and diagonal flag."""

    word = [-1] * 10
    value = ONE
    diagonal = True
    for item in decode(mask):
        left, right = item
        left_label, right_label, weight = table[item]
        word[left] = left_label
        word[right] = right_label
        value = multiply(value, weight)
        diagonal &= left_label == right_label
    return tuple(word), value, diagonal


def exact_rank(matrix: list[list[Fraction]]) -> int:
    """Compute rational row rank by a separate Gaussian routine."""

    work = [row[:] for row in matrix]
    if not work:
        return 0
    row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work)) if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        pivot_value = work[row][column]
        work[row] = [value / pivot_value for value in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(work[index], work[row], strict=True)
            ]
        row += 1
        if row == len(work):
            break
    return row


def assert_parallel_ledger() -> dict[str, object]:
    """Audit the complete table, symbolic fibres, parallel route, and elimination."""

    table = parallel_table()
    assert set(table) == set(EDGES_10)
    local_labels = {vertex: set() for vertex in range(10)}
    for (left, right), (left_label, right_label, _) in table.items():
        local_labels[left].add(left_label)
        local_labels[right].add(right_label)
    assert all(labels == {0, 1, 2} for labels in local_labels.values())

    ledger: defaultdict[Word, list[tuple[Matching, Polynomial, bool]]] = defaultdict(list)
    for mask in matching_masks((1 << 10) - 1):
        word, value, diagonal = mask_record(mask, table)
        ledger[word].append((decode(mask), value, diagonal))
    assert len(matching_masks((1 << 10) - 1)) == 945
    assert len(ledger) == 776

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
    expected = (
        {outgoing[0], incoming[2], extra},
        {incoming[0], outgoing[1]},
        {outgoing[2], incoming[1]},
    )
    for index, word in enumerate(words):
        records = ledger[word]
        assert {record[0] for record in records} == expected[index]
        total = ZERO
        for _, value, _ in records:
            total = add(total, value)
        assert total == ZERO

    pure = (
        ((0, 9), (1, 7), (2, 6), (3, 8), (4, 5)),
        ((0, 8), (1, 9), (2, 3), (4, 6), (5, 7)),
        ((0, 5), (1, 6), (2, 8), (3, 9), (4, 7)),
    )
    for colour, expected_matching in enumerate(pure):
        assert ledger[(colour,) * 10] == [(expected_matching, ONE, True)]

    unit_word = (0, 0, 1, 1, 1, 1, 1, 1, 2, 2)
    unit_matching = ((0, 1), (2, 3), (4, 6), (5, 7), (8, 9))
    assert ledger[unit_word] == [(unit_matching, ONE, True)]

    zero_words = set()
    for word, records in ledger.items():
        total = ZERO
        for _, value, _ in records:
            total = add(total, value)
        if total == ZERO:
            zero_words.add(word)
    assert zero_words == set(words)

    residual = ((0, 1), (6, 7), (8, 9))
    bridge = ((2, 3), (4, 5))
    assert table[(2, 3)][:2] == (1, 1)
    assert table[(4, 5)][:2] == (0, 0)
    assert tuple(sorted(residual + bridge)) == incoming[0]

    source = Counter(extra)
    source.subtract(outgoing[0])
    source = Counter({item: coefficient for item, coefficient in source.items() if coefficient})
    target = Counter(tuple(sorted(residual + bridge)))
    target.subtract(incoming[0])
    assert source
    assert set(source.values()) == {-1, 1}
    target = Counter({item: coefficient for item, coefficient in target.items() if coefficient})
    assert not target

    outgoing_product = ONE
    incoming_product = ONE
    for matching in outgoing:
        value = ONE
        for item in matching:
            value = multiply(value, table[item][2])
        outgoing_product = multiply(outgoing_product, value)
    for matching in incoming:
        value = ONE
        for item in matching:
            value = multiply(value, table[item][2])
        incoming_product = multiply(incoming_product, value)
    assert outgoing_product == SELECTED
    assert incoming_product == ONE
    assert add(SELECTED, PARAMETER) == constant(-1)
    assert scale(add(SELECTED, PARAMETER), -1) == ONE

    one_plus_t = (Fraction(1), Fraction(1))
    for degree in range(1, 9):
        columns = [scale(power(one_plus_t, degree - exponent), (-1) ** exponent) for exponent in range(degree + 1)]
        matrix = [
            [column[row] if row < len(column) else Fraction(0) for column in columns]
            for row in range(degree + 1)
        ]
        assert exact_rank(matrix) == degree + 1

    return {
        "edge_masks": len(matching_masks((1 << 10) - 1)),
        "cycle_sizes": tuple(len(ledger[word]) for word in words),
        "pure_sizes": tuple(len(ledger[(colour,) * 10]) for colour in range(3)),
        "parallel_target_direction": 0,
        "triangular_degrees": 8,
        "unit_word": unit_word,
    }


@cache
def pairings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Separate generic pairing enumeration for pure residuals."""

    if not vertices:
        return ((),)
    root = vertices[-1]
    records: list[Matching] = []
    for index, partner in enumerate(vertices[:-1]):
        remainder = vertices[:index] + vertices[index + 1 : -1]
        for tail in pairings(remainder):
            records.append(tuple(sorted((edge(root, partner),) + tail)))
    return tuple(records)


def supported(vertices: tuple[int, ...], weights: Weights) -> tuple[Matching, ...]:
    """Return supported matchings in a scalar graph."""

    return tuple(
        matching
        for matching in pairings(vertices)
        if all(weights.get(item, Fraction(0)) for item in matching)
    )


def value(matching: Matching, weights: Weights) -> Fraction:
    """Multiply scalar matching weights."""

    result = Fraction(1)
    for item in matching:
        result *= weights.get(item, Fraction(0))
    return result


def hafnian(vertices: tuple[int, ...], weights: Weights) -> Fraction:
    """Evaluate a scalar hafnian through the separate pairing route."""

    return sum((value(matching, weights) for matching in supported(vertices, weights)), Fraction(0))


def conformal_minimum(shore: tuple[int, ...], weights: Weights) -> tuple[int, ...]:
    """Recover the least zero with matchable complement."""

    for size in range(2, len(shore) + 1, 2):
        for candidate in combinations(shore, size):
            complement = tuple(vertex for vertex in shore if vertex not in candidate)
            if supported(candidate, weights) and supported(complement, weights) and not hafnian(candidate, weights):
                return candidate
    raise AssertionError("missing conformal residual")


def graph_connected(vertices: tuple[int, ...], items: set[Edge]) -> bool:
    """Check connectivity by repeated set expansion."""

    reached = {vertices[0]}
    while True:
        enlarged = reached | {
            endpoint
            for item in items
            if set(item) & reached
            for endpoint in item
        }
        if enlarged == reached:
            return reached == set(vertices)
        reached = enlarged


def assert_conformal_fixtures() -> dict[str, object]:
    """Audit the conformal-minimal proof mechanism on disjoint exact fixtures."""

    cycle_weights: Weights = {
        (0, 1): Fraction(1),
        (1, 2): Fraction(1),
        (2, 3): Fraction(1),
        (3, 4): Fraction(1),
        (4, 5): Fraction(1),
        (0, 5): Fraction(-1),
        (6, 7): Fraction(7),
        (8, 9): Fraction(11),
    }
    fan_weights: Weights = {
        (0, 1): Fraction(2),
        (2, 3): Fraction(3),
        (0, 2): Fraction(1),
        (1, 3): Fraction(5),
        (0, 3): Fraction(1),
        (1, 2): Fraction(-11),
        (4, 5): Fraction(7),
        (6, 7): Fraction(11),
    }
    aggregate_weights: Weights = {
        (left, right): Fraction(
            -4 if (left, right) == (0, 3) else 3 if (left, right) == (0, 5) else 1
        )
        for left in range(3)
        for right in range(3, 6)
    }
    aggregate_weights[(6, 7)] = Fraction(7)
    aggregate_weights[(8, 9)] = Fraction(11)
    fixtures = (
        ("cycle", tuple(range(8)), tuple(range(6)), cycle_weights, (1, 1)),
        ("fan", tuple(range(6)), tuple(range(4)), fan_weights, (1, 1, 1)),
        ("aggregate", tuple(range(8)), tuple(range(6)), aggregate_weights, (2, 2, 2)),
    )

    result: dict[str, object] = {}
    for name, shore, expected, weights, expected_ports in fixtures:
        residual = conformal_minimum(shore, weights)
        assert residual == expected
        matchings = supported(residual, weights)
        allowed = {item for matching in matchings for item in matching}
        active = {
            item
            for item in allowed
            if weights[item]
            * hafnian(tuple(vertex for vertex in residual if vertex not in item), weights)
            != 0
        }
        assert active == allowed
        assert graph_connected(residual, allowed)

        root = residual[0]
        root_edges = sorted(item for item in allowed if root in item)
        ports = tuple(
            tuple(matching for matching in matchings if item in matching) for item in root_edges
        )
        assert tuple(sorted(len(port) for port in ports)) == expected_ports
        assert all(sum((value(matching, weights) for matching in port), Fraction(0)) for port in ports)

        complement = tuple(vertex for vertex in shore if vertex not in residual)
        exterior = tuple(
            sorted({vertex for item in weights for vertex in item} - set(shore))
        )
        common = supported(complement, weights)[0] + supported(exterior, weights)[0]
        extended = tuple(tuple(sorted(matching + common)) for matching in matchings)
        assert sum((value(matching, weights) for matching in extended), Fraction(0)) == 0
        for matching, extension in zip(matchings, extended, strict=True):
            assert set(extension) - set(common) == set(matching)
        result[name] = {"matchings": len(matchings), "ports": expected_ports}
    return result


def assert_eight_vertex_obstruction() -> dict[str, object]:
    """Audit the no-pure-2 matching obstruction without using the primary route."""

    used = {
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (5, 6),
        (5, 7),
        (6, 7),
    }
    unused = set(combinations(range(8), 2)) - used
    assert {item for item in unused if 2 in item} == {(2, 7)}
    assert {item for item in unused if 4 in item} == {(4, 7)}
    assert not [matching for matching in pairings(tuple(range(8))) if set(matching) <= unused]
    return {"forced_collision_vertex": 7, "minimum_even_extension": 2}


def main() -> None:
    """Run the independent exact audit."""

    family = assert_parallel_ledger()
    residuals = assert_conformal_fixtures()
    obstruction = assert_eight_vertex_obstruction()
    print("aggregate-extra target attachment independent audit: PASS")
    print(f"  bitmask/custom-polynomial family: {family}")
    print(f"  alternate conformal fixtures: {residuals}")
    print(f"  order-eight obstruction: {obstruction}")


if __name__ == "__main__":
    main()
