"""No-import audit of surplus-two pair-companion sharpness.

This file imports neither SymPy nor the primary verifier.  It evaluates the
sensor as permanents of root-word incidence matrices and evaluates the full
state by a target-word bit-mask recurrence.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations, product

ROOTS = (0, 1, 2)
OUTSIDE = (3, 4, 5, 6, 7)
ALL_MASK = (1 << 8) - 1

CROSS = {
    (0, 3): 1,
    (0, 4): 0,
    (0, 5): 2,
    (1, 3): 2,
    (1, 4): 1,
    (1, 5): 0,
    (2, 5): 1,
    (2, 6): 0,
    (2, 7): 2,
}


def ordered_pair(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def outside_colour(left: int, right: int) -> int:
    pair = {left - 3, right - 3}
    if pair == {3, 4}:
        return 1
    if pair == {1, 3}:
        return 2
    return 0


def edge_value(
    left: int,
    right: int,
    colour: int,
    invisible_weights: tuple[int, int, int],
) -> int:
    left, right = ordered_pair(left, right)
    if right < 3:
        return 0
    if left < 3:
        return int(CROSS.get((left, right)) == colour)
    if outside_colour(left, right) != colour:
        return 0
    pair = (left - 3, right - 3)
    invisible = {(0, 1): 0, (0, 2): 1, (1, 2): 2}
    return invisible_weights[invisible[pair]] if pair in invisible else 1


def permanent(matrix: tuple[tuple[int, ...], ...]) -> int:
    @cache
    def recurse(row: int, columns_mask: int) -> int:
        if row == len(matrix):
            return int(columns_mask == 0)
        answer = 0
        for column in range(len(matrix)):
            if columns_mask & (1 << column):
                answer += matrix[row][column] * recurse(
                    row + 1, columns_mask ^ (1 << column)
                )
        return answer

    return recurse(0, (1 << len(matrix)) - 1)


def sensor_matrix() -> tuple[list[list[Fraction]], tuple[tuple[int, ...], ...]]:
    labels = tuple(combinations(range(5), 2)) + tuple(combinations(range(5), 4))
    rows: list[list[Fraction]] = []
    for word in product(range(3), repeat=3):
        row: list[Fraction] = []
        for label in labels:
            if len(label) == 4:
                row.append(Fraction(0))
                continue
            triple = tuple(index for index in range(5) if index not in label)
            incidence = tuple(
                tuple(
                    int(CROSS.get((root, outside + 3)) == word[root])
                    for outside in triple
                )
                for root in ROOTS
            )
            row.append(Fraction(permanent(incidence)))
        rows.append(row)
    return rows, labels


def row_rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rank = 0
    column_count = len(work[0])
    for column in range(column_count):
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


def check_sensor() -> None:
    matrix, labels = sensor_matrix()
    assert row_rank(matrix) == 7
    zero_columns = {
        label
        for column, label in enumerate(labels)
        if all(row[column] == 0 for row in matrix)
    }
    assert zero_columns == {
        (0, 1),
        (0, 2),
        (1, 2),
        (0, 1, 2, 3),
        (0, 1, 2, 4),
        (0, 1, 3, 4),
        (0, 2, 3, 4),
        (1, 2, 3, 4),
    }
    invisible = {(0, 1), (0, 2), (1, 2)}
    for residual in combinations(range(5), 2):
        desired = {
            label for label in labels if len(set(label) & set(residual)) in (0, 2)
        }
        assert desired & invisible


def structural_matchings(
    vertices: tuple[int, ...],
) -> tuple[frozenset[tuple[int, int]], ...]:
    if not vertices:
        return (frozenset(),)
    first = vertices[0]
    answer: list[frozenset[tuple[int, int]]] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in structural_matchings(rest):
            answer.append(tail | {ordered_pair(first, partner)})
    return tuple(answer)


def structural_edge_exists(left: int, right: int) -> bool:
    left, right = ordered_pair(left, right)
    if right < 3:
        return False
    if left < 3:
        return (left, right) in CROSS
    return True


def check_symbolic_physical_fibre() -> None:
    invisible = {
        ordered_pair(3, 4),
        ordered_pair(3, 5),
        ordered_pair(4, 5),
    }
    supported = []
    for matching in structural_matchings(tuple(range(8))):
        if all(structural_edge_exists(*item) for item in matching):
            supported.append(matching)
    assert supported
    assert all(matching.isdisjoint(invisible) for matching in supported)


def state_coefficient(
    word: tuple[int, ...], invisible_weights: tuple[int, int, int]
) -> int:
    @cache
    def recurse(mask: int) -> int:
        if mask == 0:
            return 1
        left = (mask & -mask).bit_length() - 1
        answer = 0
        partners = mask ^ (1 << left)
        while partners:
            bit = partners & -partners
            right = bit.bit_length() - 1
            partners ^= bit
            if word[left] != word[right]:
                continue
            scalar = edge_value(left, right, word[left], invisible_weights)
            if scalar:
                answer += scalar * recurse(mask ^ (1 << left) ^ (1 << right))
        return answer

    return recurse(ALL_MASK)


def matching_count(word: tuple[int, ...]) -> int:
    @cache
    def recurse(mask: int) -> int:
        if mask == 0:
            return 1
        left = (mask & -mask).bit_length() - 1
        answer = 0
        rest = mask ^ (1 << left)
        partners = rest
        while partners:
            bit = partners & -partners
            right = bit.bit_length() - 1
            partners ^= bit
            if word[left] == word[right] and edge_value(
                left, right, word[left], (1, 1, 1)
            ):
                answer += recurse(rest ^ (1 << right))
        return answer

    return recurse(ALL_MASK)


def check_complete_state() -> None:
    state_one: dict[tuple[int, ...], int] = {}
    state_two: dict[tuple[int, ...], int] = {}
    for word in product(range(3), repeat=8):
        state_one[word] = state_coefficient(word, (1, 1, 1))
        state_two[word] = state_coefficient(word, (2, 3, 5))
    assert state_one == state_two
    assert sum(value != 0 for value in state_one.values()) == 14

    for colour in range(3):
        pure = (colour,) * 8
        assert state_one[pure] == 1
        assert matching_count(pure) == 1
        for vertex in range(8):
            for replacement in range(3):
                if replacement == colour:
                    continue
                neighbour = list(pure)
                neighbour[vertex] = replacement
                assert state_one[tuple(neighbour)] == 0

    for vertex in range(8):
        minor = [
            [
                state_one[
                    tuple(
                        row_colour if index == vertex else column_colour
                        for index in range(8)
                    )
                ]
                for column_colour in range(3)
            ]
            for row_colour in range(3)
        ]
        assert minor == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    mixed = (0, 2, 1, 2, 0, 1, 1, 1)
    assert state_one[mixed] == 1
    assert matching_count(mixed) == 1


def nullity(matrix: list[list[Fraction]]) -> int:
    return len(matrix[0]) - row_rank(matrix)


def check_off_diagonal_lemma() -> None:
    for dimension in range(3, 9):
        for support_size in range(1, dimension + 1):
            b = [Fraction(index < support_size) for index in range(dimension)]
            equations: list[list[Fraction]] = []
            for left, right in combinations(range(dimension), 2):
                row = [Fraction(0)] * dimension
                row[left] = b[right]
                row[right] = b[left]
                equations.append(row)
            assert nullity(equations) <= 1


def check_incidence() -> None:
    outside_ranks = []
    for outside in OUTSIDE:
        colours = {
            colour for (root, vertex), colour in CROSS.items() if vertex == outside
        }
        outside_ranks.append(len(colours))
    assert outside_ranks == [2, 2, 3, 1, 1]
    assert sum(3 - rank for rank in outside_ranks) == 6


def main() -> None:
    check_sensor()
    check_symbolic_physical_fibre()
    check_complete_state()
    check_off_diagonal_lemma()
    check_incidence()
    print("surplus-two nonzero-companion no-import audit: PASS")


if __name__ == "__main__":
    main()
