"""No-import audit of the four-root paired-grade selector theorem.

The audit imports neither SymPy nor the primary verifier.  It compares a full
perfect-matching ledger with an independently generated root-partition ledger
and uses only standard-library rational arithmetic for the controls.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations, permutations

ROOTS = ("r0", "r1", "r2", "r3")
Q = ("q0", "q1")
U = ("u0", "u1", "u2", "u3")
VERTICES = ROOTS + Q + U
Edge = tuple[str, str]
Matching = frozenset[Edge]


def edge(left: str, right: str) -> Edge:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[str, ...]) -> tuple[Matching, ...]:
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(rest):
            result.append(tail | {edge(first, partner)})
    return tuple(result)


def assignments(left: tuple[str, ...], right: tuple[str, ...]) -> tuple[Matching, ...]:
    return tuple(
        frozenset(
            edge(source, target) for source, target in zip(left, image, strict=True)
        )
        for image in permutations(right)
    )


def complement(pair: tuple[str, str], universe: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(item for item in universe if item not in pair)


def combine(*families: tuple[Matching, ...]) -> set[Matching]:
    result = {frozenset()}
    for family in families:
        result = {prefix | suffix for prefix in result for suffix in family}
    return result


def singleton_matching(left: str, right: str) -> tuple[Matching, ...]:
    return (frozenset({edge(left, right)}),)


def one_grade_partition() -> dict[str, set[Matching]]:
    categories = {name: set() for name in ("omega", "direct", "corrected", "cross")}
    for internal in combinations(ROOTS, 2):
        active = complement(internal, ROOTS)
        root_edge = singleton_matching(*internal)

        categories["omega"] |= combine(
            root_edge, assignments(active, Q), perfect_matchings(U)
        )

        for active_ports in combinations(U, 2):
            remaining_ports = complement(active_ports, U)
            root_assignment = assignments(active, active_ports)
            categories["direct"] |= combine(
                root_edge,
                root_assignment,
                singleton_matching(*Q),
                singleton_matching(*remaining_ports),
            )
            categories["corrected"] |= combine(
                root_edge,
                root_assignment,
                assignments(Q, remaining_ports),
            )

        for residual in Q:
            other_q = Q[1] if residual == Q[0] else Q[0]
            for port in U:
                remaining = (other_q,) + tuple(item for item in U if item != port)
                categories["cross"] |= combine(
                    root_edge,
                    assignments(active, (residual, port)),
                    perfect_matchings(remaining),
                )
    return categories


def zero_grade_partition() -> dict[str, set[Matching]]:
    categories = {name: set() for name in ("hV", "pU", "cross")}
    categories["hV"] = combine(assignments(ROOTS, U), singleton_matching(*Q))

    for residual_roots in combinations(ROOTS, 2):
        active = complement(residual_roots, ROOTS)
        for remaining_ports in combinations(U, 2):
            active_ports = complement(remaining_ports, U)
            categories["pU"] |= combine(
                assignments(residual_roots, Q),
                assignments(active, active_ports),
                singleton_matching(*remaining_ports),
            )

    for residual in Q:
        other_q = Q[1] if residual == Q[0] else Q[0]
        for leftover_port in U:
            assigned = (residual,) + tuple(item for item in U if item != leftover_port)
            categories["cross"] |= combine(
                assignments(ROOTS, assigned),
                singleton_matching(other_q, leftover_port),
            )
    return categories


def root_grade(matching: Matching) -> int:
    return sum(left in ROOTS and right in ROOTS for left, right in matching)


def assert_disjoint_partition(
    target: set[Matching],
    categories: dict[str, set[Matching]],
    expected_sizes: dict[str, int],
) -> None:
    assert {name: len(items) for name, items in categories.items()} == expected_sizes
    names = tuple(categories)
    for left, right in combinations(names, 2):
        assert categories[left].isdisjoint(categories[right])
    assert set().union(*categories.values()) == target


def check_grade_partitions() -> None:
    all_matchings = set(perfect_matchings(VERTICES))
    assert len(all_matchings) == 945
    grade_zero = {matching for matching in all_matchings if root_grade(matching) == 0}
    grade_one = {matching for matching in all_matchings if root_grade(matching) == 1}
    grade_two = {matching for matching in all_matchings if root_grade(matching) == 2}
    assert (len(grade_zero), len(grade_one), len(grade_two)) == (360, 540, 45)

    assert_disjoint_partition(
        grade_one,
        one_grade_partition(),
        {"omega": 36, "direct": 72, "corrected": 144, "cross": 288},
    )
    assert_disjoint_partition(
        grade_zero,
        zero_grade_partition(),
        {"hV": 24, "pU": 144, "cross": 192},
    )


def row_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        divisor = work[rank][column]
        work[rank] = [entry / divisor for entry in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
    return rank


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    answer = Fraction(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            factor = work[row][column] / pivot_value
            for item in range(column, len(work)):
                work[row][item] -= factor * work[column][item]
    return answer


def alignment_record(root_pair: tuple[int, int]) -> dict[tuple[int, ...], int]:
    incidence = {(2, 2): 0, (3, 3): 0, (0, 2): 1, (1, 3): 1}
    active = tuple(root for root in range(4) if root not in root_pair)
    answer: dict[tuple[int, ...], int] = {}
    for image in permutations((2, 3)):
        colours = [0, 0, -1, -1]
        for root, port in zip(active, image, strict=True):
            colour = incidence.get((root, port))
            if colour is None:
                break
            colours[port] = colour
        else:
            word = tuple(colours)
            answer[word] = answer.get(word, 0) + 1
    return answer


def check_assignment_and_linear_controls() -> None:
    vectors = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(1)),
    )
    columns: list[list[Fraction]] = []
    for left, right in combinations(range(4), 2):
        symmetric = [
            [
                vectors[left][row] * vectors[right][column]
                + vectors[right][row] * vectors[left][column]
                for column in range(3)
            ]
            for row in range(3)
        ]
        columns.append(
            [
                symmetric[0][0],
                symmetric[1][1],
                symmetric[2][2],
                symmetric[0][1],
                symmetric[0][2],
                symmetric[1][2],
            ]
        )
    assignment = [list(row) for row in zip(*columns, strict=True)]
    assert row_rank(assignment) == 6
    assert abs(determinant(assignment)) == 8

    root_pairs = tuple(combinations(range(4), 2))
    root_edges = {pair: int(pair == (0, 1)) for pair in root_pairs}
    root_q = {(2, 0): 1, (3, 1): 1}
    p_values = {
        pair: root_q.get((pair[0], 0), 0) * root_q.get((pair[1], 1), 0)
        + root_q.get((pair[1], 0), 0) * root_q.get((pair[0], 1), 0)
        for pair in root_pairs
    }
    omega = sum(
        root_edges[pair]
        * p_values[tuple(root for root in range(4) if root not in pair)]
        for pair in root_pairs
    )
    assert omega == 1
    assert alignment_record((0, 1)) == {(0, 0, 0, 0): 1}
    assert alignment_record((2, 3)) == {(0, 0, 1, 1): 1}

    q = (Fraction(1), Fraction(1))
    port = (Fraction(1), Fraction(-1))
    zero = (Fraction(0), Fraction(0))

    def pairing(
        left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
    ) -> Fraction:
        return left[0] * right[1] + left[1] * right[0]

    assert pairing(q, q) == 2
    assert pairing(q, port) == 0
    assert pairing(port, port) == -2
    assert pairing(port, zero) == 0

    # Exact Laurent-exponent audit of (zv1/zv0)*(zu0*zv0)=zu0*zv1.
    target_exponent = (1, 1, 0)
    selector_exponent = (0, -1, 1)
    assert tuple(
        left + right
        for left, right in zip(target_exponent, selector_exponent, strict=True)
    ) == (1, 0, 1)


CONTROL = {
    edge("r0", "r1"): Fraction(1),
    edge("r0", "q0"): Fraction(1),
    edge("r1", "q1"): Fraction(1),
    edge("r2", "q0"): Fraction(1),
    edge("r3", "q1"): Fraction(1),
    edge("r0", "u0"): Fraction(1, 2),
    edge("r1", "u1"): Fraction(1),
    edge("r2", "u2"): Fraction(1),
    edge("r3", "u3"): Fraction(1),
    edge("q0", "q1"): Fraction(1),
    edge("q0", "u1"): Fraction(1),
    edge("q1", "u0"): Fraction(-3),
    edge("u0", "u1"): Fraction(1),
    edge("u2", "u3"): Fraction(2),
}


def check_nested_cancellation() -> None:
    grade_terms: dict[int, list[Fraction]] = {0: [], 1: [], 2: []}
    for matching in perfect_matchings(VERTICES):
        weight = Fraction(1)
        for item in matching:
            weight *= CONTROL.get(item, Fraction(0))
        if weight:
            grade_terms[root_grade(matching)].append(weight)
    assert sorted(grade_terms[0]) == sorted(
        [Fraction(1), Fraction(-3), Fraction(1, 2), Fraction(1), Fraction(1, 2)]
    )
    assert sorted(grade_terms[1]) == sorted([Fraction(2), Fraction(1), Fraction(-3)])
    assert grade_terms[2] == []
    assert sum(grade_terms[0]) == 0
    assert sum(grade_terms[1]) == 0


def upgraded_blocks() -> dict[Edge, dict[tuple[int, int], Fraction]]:
    blocks: dict[Edge, dict[tuple[int, int], Fraction]] = {}

    def add(
        left: str,
        right: str,
        left_colour: int,
        right_colour: int,
        coefficient: Fraction,
    ) -> None:
        ordered = edge(left, right)
        colours = (
            (left_colour, right_colour)
            if ordered == (left, right)
            else (right_colour, left_colour)
        )
        block = blocks.setdefault(ordered, {})
        block[colours] = block.get(colours, Fraction(0)) + coefficient

    for left_colour, left_sign in ((0, 1), (1, -1)):
        for right_colour, right_sign in ((0, 1), (1, -1)):
            add("r0", "r1", left_colour, right_colour, Fraction(left_sign * right_sign))

    for item in (
        ("r0", "q0", 0, 0, Fraction(1)),
        ("r1", "q1", 0, 0, Fraction(1)),
        ("r2", "q0", 1, 0, Fraction(1)),
        ("r3", "q1", 1, 0, Fraction(1)),
        ("r0", "u0", 0, 0, Fraction(1, 2)),
        ("r1", "u1", 0, 0, Fraction(1)),
        ("r2", "u2", 1, 1, Fraction(1)),
        ("r3", "u3", 1, 1, Fraction(1)),
    ):
        add(*item)

    for outside in ("q0", "q1", "u0", "u1"):
        add("r2", outside, 0, 1, Fraction(1))
        add("r3", outside, 0, 2, Fraction(1))
    for outside in ("u2", "u3"):
        add("r0", outside, 1, 0, Fraction(1))
        add("r1", outside, 1, 2, Fraction(1))

    selected = {
        edge("q0", "q1"): (0, Fraction(1)),
        edge("q0", "u1"): (0, Fraction(1)),
        edge("q1", "u0"): (0, Fraction(-3)),
        edge("u0", "u1"): (0, Fraction(1)),
        edge("u2", "u3"): (1, Fraction(2)),
    }
    for left, right in combinations(Q + U, 2):
        colour, coefficient = selected.get(edge(left, right), (2, Fraction(1)))
        add(left, right, colour, colour, coefficient)
    return blocks


def upgraded_coefficient(
    word: tuple[int, ...], blocks: dict[Edge, dict[tuple[int, int], Fraction]]
) -> Fraction:
    @cache
    def recurse(mask: int) -> Fraction:
        if mask == 0:
            return Fraction(1)
        left_index = (mask & -mask).bit_length() - 1
        left = VERTICES[left_index]
        rest = mask ^ (1 << left_index)
        partners = rest
        answer = Fraction(0)
        while partners:
            bit = partners & -partners
            right_index = bit.bit_length() - 1
            partners ^= bit
            right = VERTICES[right_index]
            ordered = edge(left, right)
            colours = (
                (word[left_index], word[right_index])
                if ordered == (left, right)
                else (word[right_index], word[left_index])
            )
            scalar = blocks.get(ordered, {}).get(colours, Fraction(0))
            if scalar:
                answer += scalar * recurse(rest ^ bit)
        return answer

    return recurse((1 << len(VERTICES)) - 1)


def check_maximal_triple_upgrade() -> None:
    blocks = upgraded_blocks()
    for outside in Q + U:
        rows: list[list[Fraction]] = []
        for root in ROOTS:
            ordered = edge(root, outside)
            row = [Fraction(0)] * 3
            for colours, coefficient in blocks.get(ordered, {}).items():
                root_colour, outside_colour = (
                    colours if ordered == (root, outside) else tuple(reversed(colours))
                )
                assert root_colour in (0, 1, 2)
                row[outside_colour] += coefficient
            rows.append(row)
        assert row_rank(rows) == 3

    assert upgraded_coefficient(tuple(map(int, "0011000011")), blocks) == 0
    assert all(upgraded_coefficient((colour,) * 10, blocks) == 0 for colour in range(3))
    assert upgraded_coefficient(tuple(map(int, "0000001211")), blocks) == 4


def main() -> None:
    check_grade_partitions()
    check_assignment_and_linear_controls()
    check_nested_cancellation()
    check_maximal_triple_upgrade()
    print("four-root paired-grade constant-selector no-import audit: PASS")


if __name__ == "__main__":
    main()
