#!/usr/bin/env python3
"""Independent no-import audit of the four-root source trichotomy.

This program deliberately imports no repository module and does not read the
focused primary verifier.  It uses only the Python standard library.  The
arbitrary-witness implications remain the written consequences of GLS4,
GLD5, GLD7, and GLD13; the finite checks below audit their linear-algebra
logic and reconstruct the exact off-target physical boundary graph.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations, product
from pathlib import Path

Q = Fraction


def transpose(rows: list[list[Fraction]]) -> list[list[Fraction]]:
    if not rows:
        return []
    return [list(column) for column in zip(*rows, strict=True)]


def rref(rows: list[list[int | Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    """Exact first-available-pivot reduction, implemented locally."""

    a = [[Q(entry) for entry in row] for row in rows]
    if not a:
        return a, []
    width = len(a[0])
    assert all(len(row) == width for row in a)
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(width):
        chosen = next(
            (row for row in range(pivot_row, len(a)) if a[row][column]),
            None,
        )
        if chosen is None:
            continue
        a[pivot_row], a[chosen] = a[chosen], a[pivot_row]
        pivot = a[pivot_row][column]
        a[pivot_row] = [entry / pivot for entry in a[pivot_row]]
        for row in range(len(a)):
            if row == pivot_row or not a[row][column]:
                continue
            scale = a[row][column]
            a[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(a[row], a[pivot_row], strict=True)
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(a):
            break
    return a, pivot_columns


def matrix_rank(rows: list[list[int | Fraction]], width: int | None = None) -> int:
    if not rows:
        return 0
    if width is not None:
        assert all(len(row) == width for row in rows)
    return len(rref(rows)[1])


def column_rank(columns: list[tuple[int | Fraction, ...]], dimension: int) -> int:
    if not columns:
        return 0
    assert all(len(column) == dimension for column in columns)
    return matrix_rank(
        transpose([[Q(entry) for entry in column] for column in columns])
    )


def nullspace(rows: list[list[int | Fraction]]) -> list[tuple[Fraction, ...]]:
    reduced, pivots = rref(rows)
    width = len(rows[0]) if rows else 0
    free_columns = [column for column in range(width) if column not in pivots]
    basis: list[tuple[Fraction, ...]] = []
    for free in free_columns:
        vector = [Q(0) for _ in range(width)]
        vector[free] = Q(1)
        for row, pivot in reversed(list(enumerate(pivots))):
            vector[pivot] = -sum(
                reduced[row][column] * vector[column] for column in free_columns
            )
        basis.append(tuple(vector))
    return basis


def bareiss_determinant(rows: list[list[int]]) -> int:
    """Fraction-free exact determinant with explicit row-pivot signs."""

    size = len(rows)
    assert size and all(len(row) == size for row in rows)
    a = [row[:] for row in rows]
    sign = 1
    previous = 1
    for k in range(size - 1):
        chosen = next((row for row in range(k, size) if a[row][k]), None)
        if chosen is None:
            return 0
        if chosen != k:
            a[k], a[chosen] = a[chosen], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def normalized_circuit(
    columns: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[int, ...], tuple[Fraction, ...]] | None:
    """Find an inclusion-minimal dependence containing column zero."""

    dimension = len(columns[0])
    for size in range(2, len(columns) + 1):
        for tail in combinations(range(1, len(columns)), size - 1):
            support = (0, *tail)
            selected = [columns[index] for index in support]
            if column_rank(selected, dimension) == size:
                continue
            if any(
                column_rank(
                    [columns[index] for index in support if index != removed],
                    dimension,
                )
                != size - 1
                for removed in support
            ):
                continue
            kernel = nullspace(
                [
                    [columns[index][coordinate] for index in support]
                    for coordinate in range(dimension)
                ]
            )
            assert len(kernel) == 1 and kernel[0][0]
            coefficients = tuple(value / kernel[0][0] for value in kernel[0])
            assert coefficients[0] == 1 and all(coefficients)
            assert all(
                sum(
                    coefficients[position] * columns[index][coordinate]
                    for position, index in enumerate(support)
                )
                == 0
                for coordinate in range(dimension)
            )
            return support, coefficients
    return None


def normalized_separator(
    first: tuple[Fraction, ...], others: tuple[tuple[Fraction, ...], ...]
) -> tuple[Fraction, ...] | None:
    """Return lambda with lambda(first)=1 and lambda(others)=0, if possible."""

    dimension = len(first)
    annihilator = nullspace([list(column) for column in others])
    for functional in annihilator:
        value = dot(functional, first)
        if value:
            answer = tuple(entry / value for entry in functional)
            assert dot(answer, first) == 1
            assert all(dot(answer, column) == 0 for column in others)
            return answer
    assert column_rank(list(others), dimension) == column_rank(
        [*others, first], dimension
    )
    return None


def audit_pair_split() -> tuple[int, int, int]:
    """Directly enumerate O/C controls and replay their scalar readings."""

    first = (Q(1), Q(0), Q(0))
    pool = (
        (Q(0), Q(1), Q(0)),
        (Q(0), Q(0), Q(1)),
        (Q(0), Q(1), Q(1)),
        (Q(1), Q(1), Q(0)),
        (Q(1), Q(0), Q(1)),
        (Q(1), Q(1), Q(1)),
    )
    observable = 0
    circuit = 0
    nonzero_readings = 0
    epsilon = (Q(2), Q(-1), Q(3))
    for tail in product(pool, repeat=3):
        columns = (first, *tail)
        separator = normalized_separator(first, tail)
        dependence = normalized_circuit(columns)
        assert (separator is None) != (dependence is None)
        if separator is not None:
            observable += 1
            continue
        circuit += 1
        support, coefficients = dependence
        readings = tuple(dot(epsilon, columns[index]) for index in support)
        assert (
            sum(
                (
                    coefficient * reading
                    for coefficient, reading in zip(coefficients, readings, strict=True)
                ),
                Q(0),
            )
            == 0
        )
        if readings[0]:
            assert any(reading for reading in readings[1:])
            nonzero_readings += 1

        # A circuit gives linear deck-coordinate nonuniqueness.  Removing the
        # named coordinate preserves the represented vector.
        deck = [Q(index + 2) for index in range(len(columns))]
        represented = tuple(
            sum(
                (
                    deck[index] * columns[index][coordinate]
                    for index in range(len(columns))
                ),
                Q(0),
            )
            for coordinate in range(3)
        )
        shift = -deck[0]
        for position, index in enumerate(support):
            deck[index] += shift * coefficients[position]
        assert deck[0] == 0
        assert represented == tuple(
            sum(
                (
                    deck[index] * columns[index][coordinate]
                    for index in range(len(columns))
                ),
                Q(0),
            )
            for coordinate in range(3)
        )
    assert observable and circuit and nonzero_readings
    return observable, circuit, nonzero_readings


def rank_with_columns(columns: list[tuple[int, ...]], row_count: int) -> int:
    return column_rank(
        [tuple(Q(entry) for entry in column) for column in columns], row_count
    )


def classify_target_family(
    responses: list[bool],
    nuisances: list[list[tuple[int, ...]]],
    desired: list[tuple[int, ...]],
) -> str:
    assert len(responses) == len(nuisances) == len(desired) == 7
    if not all(responses):
        return "R"
    increments = []
    for columns, target in zip(nuisances, desired, strict=True):
        row_count = len(target)
        rank_b = rank_with_columns(columns, row_count)
        rank_augmented = rank_with_columns([*columns, target], row_count)
        assert rank_augmented - rank_b in (0, 1)
        increments.append(rank_augmented - rank_b)
    return "E" if all(increment == 1 for increment in increments) else "A"


def audit_response_rank_trichotomy() -> tuple[int, int, int]:
    """Check exhaustive bits and independent concrete R/E/A matrices."""

    counts = defaultdict(int)
    for response_bits in product((False, True), repeat=7):
        for increments in product((0, 1), repeat=7):
            if not all(response_bits):
                label = "R"
            elif all(increment == 1 for increment in increments):
                label = "E"
            else:
                label = "A"
            counts[label] += 1
    assert sum(counts.values()) == 2**14
    assert all(counts[label] for label in "REA")

    # E: a one-dimensional nuisance line, a surviving desired column, and
    # three pure columns spanning the same one-dimensional quotient line.
    e_nuisance = [[(1, 0, 0)] for _ in range(7)]
    e_desired = [(0, 1, 0) for _ in range(7)]
    e_pure = [[(0, 1, 0), (0, 2, 0), (0, -3, 0)] for _ in range(7)]
    assert classify_target_family([True] * 7, e_nuisance, e_desired) == "E"
    for nuisance, desired, pure in zip(e_nuisance, e_desired, e_pure, strict=True):
        assert rank_with_columns([*nuisance, desired], 3) == 2
        assert rank_with_columns([*nuisance, desired, *pure], 3) == 2
        assert rank_with_columns([*nuisance, *pure], 3) == 2

    # A: at one target the desired and all pure columns lie in nuisance.
    a_nuisance = [columns[:] for columns in e_nuisance]
    a_desired = e_desired[:]
    a_pure = [columns[:] for columns in e_pure]
    a_nuisance[3] = [(1, 0, 0), (0, 1, 0)]
    a_desired[3] = (2, -1, 0)
    a_pure[3] = [(3, 4, 0), (-2, 5, 0), (0, 0, 0)]
    assert classify_target_family([True] * 7, a_nuisance, a_desired) == "A"
    assert rank_with_columns(a_nuisance[3], 3) == 2
    assert rank_with_columns([*a_nuisance[3], a_desired[3], *a_pure[3]], 3) == 2

    # R is decided before any generic desired-rank pattern.
    assert (
        classify_target_family(
            [True, True, False, True, True, True, True], e_nuisance, e_desired
        )
        == "R"
    )

    # A denominator-cleared generic absorption may fail exactly on its
    # divisor: B(t)=[t,0]^T absorbs g=[1,0]^T over Q(t), but at t=0 the
    # nuisance rank drops and g survives.  No division at t=0 is made.
    def exceptional_columns(t: int) -> list[tuple[int, int]]:
        return [(t, 0)]

    generic_point = 2
    divisor_point = 0
    g = (1, 0)
    assert rank_with_columns(exceptional_columns(generic_point), 2) == 1
    assert rank_with_columns([*exceptional_columns(generic_point), g], 2) == 1
    assert rank_with_columns(exceptional_columns(divisor_point), 2) == 0
    assert rank_with_columns([*exceptional_columns(divisor_point), g], 2) == 1
    return counts["R"], counts["E"], counts["A"]


ROOTS = tuple(range(4))
OUTSIDE = tuple(range(4, 10))


ROOT_OUTSIDE_COLOURS: tuple[tuple[int | None, ...], ...] = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)


OUTSIDE_COLOURS = {
    (0, 1): 0,
    (0, 2): 2,
    (0, 3): 0,
    (0, 4): 2,
    (0, 5): 0,
    (1, 2): 1,
    (1, 3): 1,
    (1, 4): 2,
    (1, 5): 0,
    (2, 3): 0,
    (2, 4): 1,
    (2, 5): 2,
    (3, 4): 1,
    (3, 5): 0,
    (4, 5): 0,
}


def edge_colour(left: int, right: int) -> int | None:
    if left > right:
        left, right = right, left
    if right < 4:
        return None
    if left < 4:
        return ROOT_OUTSIDE_COLOURS[left][right - 4]
    return OUTSIDE_COLOURS[(left - 4, right - 4)]


def matching_count(vertices: tuple[int, ...], word: tuple[int, ...]) -> int:
    """Vertex-deletion recurrence for one fixed full or induced word."""

    position = {vertex: index for index, vertex in enumerate(vertices)}

    @cache
    def recurse(mask: int) -> int:
        if not mask:
            return 1
        first_bit = mask & -mask
        i = first_bit.bit_length() - 1
        left = vertices[i]
        rest = mask ^ first_bit
        total = 0
        candidates = rest
        while candidates:
            bit = candidates & -candidates
            j = bit.bit_length() - 1
            right = vertices[j]
            colour = edge_colour(left, right)
            if (
                colour is not None
                and word[position[left]] == colour == word[position[right]]
            ):
                total += recurse(rest ^ bit)
            candidates ^= bit
        return total

    return recurse((1 << len(vertices)) - 1)


def contracted_matching_tensor(
    open_vertices: tuple[int, ...], contracted_vertices: tuple[int, ...]
) -> dict[tuple[int, ...], int]:
    """Contract named vertices with (1,1,1), retaining exact open words."""

    vertices = (*open_vertices, *contracted_vertices)
    answer: dict[tuple[int, ...], int] = {}
    for open_word in product(range(3), repeat=len(open_vertices)):
        coefficient = 0
        for contracted_word in product(range(3), repeat=len(contracted_vertices)):
            coefficient += matching_count(vertices, (*open_word, *contracted_word))
        if coefficient:
            answer[open_word] = coefficient
    return answer


def order_two_sensor_column(deleted_pair: tuple[int, int]) -> tuple[int, ...]:
    retained = tuple(vertex for vertex in OUTSIDE if vertex not in deleted_pair)
    answer: list[int] = []
    for root_word in product(range(3), repeat=4):
        # Contract retained outside modes against (1,1,1).  Because all
        # root-root blocks vanish and |retained|=|R|, only root/outside
        # bijections can contribute.
        total = 0
        for outside_word in product(range(3), repeat=4):
            total += matching_count((*ROOTS, *retained), (*root_word, *outside_word))
        answer.append(total)
    return tuple(answer)


def audit_physical_graph() -> dict[str, object]:
    # R is a torus-zero set; every outside mode has the three coordinate
    # covectors and one zero root incidence, while every outside pair edge is
    # a nonzero coordinate monomial.  This is the complete maximum-root and
    # rank-three-blocker incidence argument.
    assert all(edge_colour(i, j) is None for i, j in combinations(ROOTS, 2))
    assert all(
        sorted(colour for colour in column if colour is not None) == [0, 1, 2]
        and sum(colour is None for colour in column) == 1
        for column in zip(*ROOT_OUTSIDE_COLOURS, strict=True)
    )
    assert all(edge_colour(i, j) is not None for i, j in combinations(OUTSIDE, 2))

    vertices = (*ROOTS, *OUTSIDE)
    pure_coefficients = [
        matching_count(vertices, (colour,) * 10) for colour in range(3)
    ]
    assert pure_coefficients == [1, 1, 1]
    hamming_one = []
    for base_colour in range(3):
        for vertex in range(10):
            for replacement in range(3):
                if replacement == base_colour:
                    continue
                word = [base_colour] * 10
                word[vertex] = replacement
                hamming_one.append(matching_count(vertices, tuple(word)))
    assert len(hamming_one) == 60 and not any(hamming_one)

    # Those pure/Hamming-one entries give an identity 3x3 minor in each
    # one-mode flattening, hence local concision at every vertex.
    flattening_minors = []
    for vertex in range(10):
        minor = []
        for row_colour in range(3):
            row = []
            for column_colour in range(3):
                word = [column_colour] * 10
                word[vertex] = row_colour
                row.append(matching_count(vertices, tuple(word)))
            minor.append(row)
        assert minor == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        flattening_minors.append(minor)

    outside_pairs = tuple(combinations(OUTSIDE, 2))
    columns = [order_two_sensor_column(pair) for pair in outside_pairs]
    selected_words = (
        "0000",
        "0001",
        "0010",
        "0020",
        "0021",
        "0022",
        "0100",
        "0101",
        "0110",
        "0200",
        "1000",
        "1001",
        "1010",
        "1101",
        "2010",
    )
    row_index = {
        "".join(map(str, word)): index
        for index, word in enumerate(product(range(3), repeat=4))
    }
    minor = [
        [columns[column][row_index[word]] for column in range(15)]
        for word in selected_words
    ]
    determinant = bareiss_determinant(minor)
    assert determinant == -1
    assert (
        column_rank([tuple(Q(entry) for entry in column) for column in columns], 81)
        == 15
    )

    # Every higher grade needs a root-root edge, so all such companions are
    # zero for this graph.  This is structural, not a sampled assertion.
    assert all(edge_colour(i, j) is None for i, j in combinations(ROOTS, 2))

    q_pair = (8, 9)
    assert edge_colour(*q_pair) == 0
    q_column = columns[outside_pairs.index(q_pair)]
    word_1111 = tuple(product(range(3), repeat=4)).index((1, 1, 1, 1))
    assert q_column[word_1111] == 1

    raw_p = []
    for i, j in combinations(ROOTS, 2):
        first = edge_colour(i, 8)
        second = edge_colour(j, 9)
        third = edge_colour(i, 9)
        fourth = edge_colour(j, 8)
        raw_p.append(
            int(first is not None and second is not None)
            + int(third is not None and fourth is not None)
        )
    assert raw_p == [2, 1, 1, 1, 1, 1]

    # Reconstruct every same-Q physical response as the principal matching
    # tensor on Q union S, contracted at q0,q1=(1,1,1).
    u_vertices = OUTSIDE[:4]
    target_sets = [tuple(pair) for pair in combinations(u_vertices, 2)] + [u_vertices]
    response_sums = []
    response_supports = []
    for target in target_sets:
        tensor = contracted_matching_tensor(target, q_pair)
        assert tensor
        response_sums.append(sum(tensor.values()))
        response_supports.append(len(tensor))
    assert response_sums == [3, 3, 3, 3, 3, 3, 15]

    # For pair targets g_S requires one root-root edge; for U it requires
    # two.  Hence all seven desired tensors, and therefore their quotient
    # classes, are exactly zero.
    assert all(edge_colour(i, j) is None for i, j in combinations(ROOTS, 2))

    mixed_word = tuple(map(int, "1200100020"))
    mixed_coefficient = matching_count(vertices, mixed_word)
    assert mixed_coefficient == 1
    expected_matching = ((0, 4), (1, 8), (2, 6), (3, 7), (5, 9))
    assert all(
        edge_colour(left, right) == mixed_word[left] == mixed_word[right]
        for left, right in expected_matching
    )

    return {
        "sensor_minor_determinant": determinant,
        "sensor_rank": 15,
        "pure_coefficients": pure_coefficients,
        "response_sums": response_sums,
        "response_supports": response_supports,
        "raw_p": raw_p,
        "mixed_coefficient": mixed_coefficient,
    }


def audit_written_scope() -> None:
    theorem = (
        Path(__file__)
        .with_name(
            "FOUR_ROOT_MAXIMAL_ROOT_SUPPLY_TO_ATTACHMENT_TRICHOTOMY_AND_OBSERVABLE_NONSELECTOR_BOUNDARY_THEOREM.md"
        )
        .read_text(encoding="utf-8")
    )
    required_scope_guards = (
        "The R and A leaves are not excluded here.",
        "This is a four-root source reduction, not coverage of root orders three or",
        "that the four R/A leaves are empty.",
        "Both leaves \\(O\\times E\\) and \\(C\\times E\\) reach",
        "Exceptional fibres on",
        "may still escape.",
        "The coefficients in (11)--(12) are rational functions.",
        "global Krenn--Gu conjecture remains **UNRESOLVED**",
    )
    for phrase in required_scope_guards:
        assert phrase in theorem, phrase
    assert "Exactly one of the following holds." in theorem
    assert theorem.count("#### O. Observable") == 1
    assert theorem.count("#### C. Quotient circuit") == 1
    assert theorem.count("#### R. Response-identically-zero") == 1
    assert theorem.count("#### E. Common seven-target escape") == 1
    assert theorem.count("#### A. Function-field desired-plus-pure absorption") == 1


def main() -> None:
    audit_written_scope()
    observable, circuit, nonzero_readings = audit_pair_split()
    response_counts = audit_response_rank_trichotomy()
    physical = audit_physical_graph()
    print("NO-IMPORT AUDIT PASS")
    print(
        "pair split controls:",
        f"O={observable}",
        f"C={circuit}",
        f"C with nonzero named scalar reading={nonzero_readings}",
    )
    print(
        "R/E/A bit controls:",
        f"R={response_counts[0]}",
        f"E={response_counts[1]}",
        f"A={response_counts[2]}",
    )
    print("physical reconstruction:", physical)
    print(
        "scope: finite controls audited; arbitrary-witness source implication remains written; "
        "R/A leaves and the strategic node remain open; global conjecture UNRESOLVED"
    )


if __name__ == "__main__":
    main()
