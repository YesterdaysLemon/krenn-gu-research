"""Primary exact checks for the matrix-unit GHZ moment-balanced gauge."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Edge = tuple[int, int]
Labels = tuple[int, int]
Word = tuple[int, ...]
Matching = tuple[Edge, ...]
Eisenstein = tuple[Fraction, Fraction]
Table = dict[Edge, tuple[int, int, Eisenstein]]

ZERO: Eisenstein = (Fraction(0), Fraction(0))
ONE: Eisenstein = (Fraction(1), Fraction(0))
MINUS_ONE: Eisenstein = (Fraction(-1), Fraction(0))
MINUS_OMEGA: Eisenstein = (Fraction(0), Fraction(-1))
MINUS_OMEGA_SQUARED: Eisenstein = (Fraction(1), Fraction(1))


def eis_add(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    """Add elements represented in the basis 1, omega."""
    return left[0] + right[0], left[1] + right[1]


def eis_mul(left: Eisenstein, right: Eisenstein) -> Eisenstein:
    """Multiply modulo omega^2 + omega + 1."""
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def eis_scale(value: Eisenstein, scalar: Fraction) -> Eisenstein:
    """Scale an Eisenstein element by a rational number."""
    return scalar * value[0], scalar * value[1]


def eis_norm(value: Eisenstein) -> Fraction:
    """Return the exact squared complex modulus a^2-ab+b^2."""
    a, b = value
    return a * a - a * b + b * b


def perfect_matchings(vertices: tuple[int, ...]):
    """Generate labelled perfect matchings recursively."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        partner = vertices[index]
        residue = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(residue):
            yield ((first, partner),) + tail


def label_table() -> dict[Edge, Labels]:
    """Return the complete balanced eight-vertex endpoint-label table."""
    return {
        (0, 1): (0, 0),
        (0, 2): (2, 0),
        (0, 3): (0, 0),
        (0, 4): (0, 1),
        (0, 5): (1, 1),
        (0, 6): (2, 2),
        (0, 7): (1, 0),
        (1, 2): (0, 0),
        (1, 3): (2, 2),
        (1, 4): (1, 1),
        (1, 5): (1, 2),
        (1, 6): (0, 2),
        (1, 7): (2, 1),
        (2, 3): (2, 0),
        (2, 4): (0, 0),
        (2, 5): (2, 2),
        (2, 6): (1, 1),
        (2, 7): (1, 2),
        (3, 4): (1, 0),
        (3, 5): (0, 0),
        (3, 6): (2, 1),
        (3, 7): (1, 1),
        (4, 5): (0, 0),
        (4, 6): (2, 0),
        (4, 7): (2, 2),
        (5, 6): (1, 0),
        (5, 7): (0, 0),
        (6, 7): (0, 0),
    }


def unit_phase_table() -> Table:
    """Attach exact unit Eisenstein phases to the balanced label table."""
    weights = {edge: ONE for edge in label_table()}
    weights[(0, 1)] = MINUS_OMEGA
    weights[(1, 2)] = MINUS_OMEGA_SQUARED
    weights[(0, 4)] = MINUS_ONE
    weights[(0, 7)] = MINUS_ONE
    return {
        edge: (*labels, weights[edge]) for edge, labels in label_table().items()
    }


def matching_record(
    matching: Matching,
    table: Table,
    order: int,
) -> tuple[Word, Eisenstein, bool]:
    """Return the word, exact weight, and diagonal flag of a matching."""
    word = [-1] * order
    weight = ONE
    diagonal = True
    for left, right in matching:
        left_label, right_label, scalar = table[(left, right)]
        word[left] = left_label
        word[right] = right_label
        weight = eis_mul(weight, scalar)
        diagonal = diagonal and left_label == right_label
    return tuple(word), weight, diagonal


def coefficient_ledgers(table: Table, order: int):
    """Enumerate total, diagonal, offdiagonal, and term ledgers."""
    total: dict[Word, Eisenstein] = {}
    diagonal: dict[Word, Eisenstein] = {}
    offdiagonal: dict[Word, Eisenstein] = {}
    terms: dict[Word, list[tuple[Matching, Eisenstein, bool]]] = {}
    for matching in perfect_matchings(tuple(range(order))):
        word, weight, is_diagonal = matching_record(matching, table, order)
        total[word] = eis_add(total.get(word, ZERO), weight)
        target = diagonal if is_diagonal else offdiagonal
        target[word] = eis_add(target.get(word, ZERO), weight)
        terms.setdefault(word, []).append((matching, weight, is_diagonal))
    return total, diagonal, offdiagonal, terms


def endpoint_loads(
    table: Table,
    squared_magnitudes: dict[Edge, Fraction],
    order: int,
) -> tuple[tuple[Fraction, Fraction, Fraction], ...]:
    """Return the actual squared-magnitude loads at every labelled endpoint."""
    loads = [[Fraction(0), Fraction(0), Fraction(0)] for _ in range(order)]
    for (left, right), (left_label, right_label, _) in table.items():
        magnitude = squared_magnitudes[(left, right)]
        loads[left][left_label] += magnitude
        loads[right][right_label] += magnitude
    return tuple(tuple(row) for row in loads)


def zero_colour_sum_basis(order: int) -> list[tuple[int, int]]:
    """Index the basis e_(v,c)-e_(order-1,c) of the GHZ Lie algebra."""
    return [(vertex, colour) for colour in range(3) for vertex in range(order - 1)]


def restricted_incidence_matrix(table: Table, order: int) -> list[list[Fraction]]:
    """Return the edge-exponent map on the zero-colour-sum basis."""
    anchor = order - 1
    basis = zero_colour_sum_basis(order)
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
    """Compute rational row rank by full Gaussian elimination."""
    work = [row[:] for row in matrix]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
    return pivot_row


def gram_matrix(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    """Return R^T R, the Hessian at a unit-magnitude balanced point up to 4."""
    width = len(matrix[0])
    return [
        [sum(row[left] * row[right] for row in matrix) for right in range(width)]
        for left in range(width)
    ]


def edge_exponents(
    table: Table,
    beta: dict[tuple[int, int], int],
) -> dict[Edge, int]:
    """Evaluate the physical edge exponent of a diagonal GHZ scaling."""
    result = {}
    for edge, (left_label, right_label, _) in table.items():
        left, right = edge
        result[edge] = beta.get((left, left_label), 0) + beta.get(
            (right, right_label), 0
        )
    return result


def power_of_two(exponent: int) -> Fraction:
    """Return 2^exponent exactly for an integral exponent."""
    if exponent >= 0:
        return Fraction(2**exponent)
    return Fraction(1, 2 ** (-exponent))


def nonrigidity_sets(table: Table, order: int) -> tuple[frozenset[int], ...]:
    """Compute S_c from its oriented half-edge definition."""
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


def assert_moment_linear_algebra(table: Table) -> dict[str, object]:
    """Check exact moment balance and quotient Hessian rank at the phase table."""
    magnitudes = {edge: eis_norm(data[2]) for edge, data in table.items()}
    assert set(magnitudes.values()) == {Fraction(1)}
    loads = endpoint_loads(table, magnitudes, 8)
    assert loads == ((Fraction(3), Fraction(2), Fraction(2)),) * 8

    incidence = restricted_incidence_matrix(table, 8)
    gradient = tuple(sum(row[column] for row in incidence) for column in range(21))
    assert gradient == (Fraction(0),) * 21
    incidence_rank = matrix_rank(incidence)
    hessian_rank = matrix_rank(gram_matrix(incidence))
    assert incidence_rank == hessian_rank == 20

    return {
        "squared_magnitude_loads": loads[0],
        "zero_sum_lie_dimension": 21,
        "edge_exponent_rank": incidence_rank,
        "edgewise_stabilizer_dimension": 21 - incidence_rank,
    }


def assert_nontrivial_exact_gauge(table: Table) -> dict[str, object]:
    """Undo a rational GHZ scaling and restore the balanced table exactly."""
    beta = {(0, 0): 1, (1, 0): -1}
    colour_sums = tuple(
        sum(beta.get((vertex, colour), 0) for vertex in range(8))
        for colour in range(3)
    )
    assert colour_sums == (0, 0, 0)
    exponents = edge_exponents(table, beta)
    assert any(value for value in exponents.values())

    initial: Table = {}
    restored: Table = {}
    for edge, (left_label, right_label, weight) in table.items():
        initial_weight = eis_scale(weight, power_of_two(-exponents[edge]))
        initial[edge] = left_label, right_label, initial_weight
        restored_weight = eis_scale(
            initial_weight,
            power_of_two(exponents[edge]),
        )
        restored[edge] = left_label, right_label, restored_weight
    assert restored == table

    initial_magnitudes = {
        edge: eis_norm(data[2]) for edge, data in initial.items()
    }
    initial_loads = endpoint_loads(initial, initial_magnitudes, 8)
    assert initial_loads != (initial_loads[0],) * 8
    restored_loads = endpoint_loads(
        restored,
        {edge: eis_norm(data[2]) for edge, data in restored.items()},
        8,
    )
    assert restored_loads == ((Fraction(3), Fraction(2), Fraction(2)),) * 8

    local_products = []
    for colour in range(3):
        product = Fraction(1)
        for vertex in range(8):
            product *= power_of_two(beta.get((vertex, colour), 0))
        local_products.append(product)
    assert local_products == [Fraction(1)] * 3
    return {
        "nonzero_edge_exponents": sum(value != 0 for value in exponents.values()),
        "colour_products": tuple(local_products),
        "restored_loads": restored_loads[0],
    }


def term_dictionary(
    records: list[tuple[Matching, Eisenstein, bool]],
) -> dict[Matching, tuple[Eisenstein, bool]]:
    """Index a word fibre by its compatible matching."""
    return {matching: (weight, diagonal) for matching, weight, diagonal in records}


def assert_unit_phase_sharpness(table: Table) -> dict[str, object]:
    """Check pure targets, active transport, proper flags, and the exposed word."""
    assert set(table) == set(combinations(range(8), 2))
    total, diagonal, offdiagonal, terms = coefficient_ledgers(table, 8)
    assert sum(len(records) for records in terms.values()) == 105

    pure_terms = {
        0: {
            ((0, 1), (2, 4), (3, 5), (6, 7)): (MINUS_OMEGA, True),
            ((0, 3), (1, 2), (4, 5), (6, 7)): (
                MINUS_OMEGA_SQUARED,
                True,
            ),
        },
        1: {((0, 5), (1, 4), (2, 6), (3, 7)): (ONE, True)},
        2: {((0, 6), (1, 3), (2, 5), (4, 7)): (ONE, True)},
    }
    for colour in range(3):
        word = (colour,) * 8
        assert total[word] == ONE
        assert diagonal[word] == ONE
        assert offdiagonal.get(word, ZERO) == ZERO
        assert term_dictionary(terms[word]) == pure_terms[colour]

    chi_0 = (0, 1, 2, 0, 1, 2, 0, 0)
    chi_1 = (1, 2, 0, 2, 0, 1, 0, 0)
    expected_active = {
        chi_0: {
            ((0, 3), (1, 4), (2, 5), (6, 7)): (ONE, True),
            ((0, 4), (1, 5), (2, 3), (6, 7)): (MINUS_ONE, False),
        },
        chi_1: {
            ((0, 5), (1, 3), (2, 4), (6, 7)): (ONE, True),
            ((0, 7), (1, 3), (2, 4), (5, 6)): (MINUS_ONE, False),
        },
    }
    for word in (chi_0, chi_1):
        assert total[word] == ZERO
        assert diagonal[word] == ONE
        assert offdiagonal[word] == MINUS_ONE
        assert term_dictionary(terms[word]) == expected_active[word]

    expected_bridges = {
        (0, 4): (0, 1),
        (1, 5): (1, 2),
        (2, 3): (2, 0),
        (2, 4): (0, 0),
        (0, 5): (1, 1),
        (1, 3): (2, 2),
    }
    for edge, labels in expected_bridges.items():
        assert table[edge][:2] == labels

    exposed = (0, 0, 0, 0, 0, 0, 2, 0)
    exposed_matching = ((0, 3), (1, 6), (2, 4), (5, 7))
    assert total[exposed] == ONE
    assert term_dictionary(terms[exposed]) == {exposed_matching: (ONE, False)}

    sets = nonrigidity_sets(table, 8)
    assert sets == (
        frozenset({0, 2, 3, 4, 5, 6}),
        frozenset({0, 1, 3, 4, 5, 6, 7}),
        frozenset({1, 2, 3, 6, 7}),
    )
    assert all(sets) and all(len(active) < 8 for active in sets)
    return {
        "pure_coefficients": (ONE, ONE, ONE),
        "active_fibres": {
            chi_0: (diagonal[chi_0], offdiagonal[chi_0]),
            chi_1: (diagonal[chi_1], offdiagonal[chi_1]),
        },
        "proper_nonrigidity_sets": tuple(tuple(sorted(active)) for active in sets),
        "exposed_mixed_word": exposed,
        "perfect_matchings": 105,
    }


def main() -> None:
    table = unit_phase_table()
    moment = assert_moment_linear_algebra(table)
    gauge = assert_nontrivial_exact_gauge(table)
    sharpness = assert_unit_phase_sharpness(table)
    print("matrix-unit GHZ moment-balanced gauge primary checks: PASS")
    print(f"  exact moment linear algebra: {moment}")
    print(f"  nontrivial exact GHZ gauge: {gauge}")
    print(f"  unit-phase active-transport sharpness: {sharpness}")


if __name__ == "__main__":
    main()
