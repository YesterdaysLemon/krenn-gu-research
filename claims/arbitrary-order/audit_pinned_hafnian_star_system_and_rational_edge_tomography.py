"""Independent stdlib audit of pinned hafnian rational edge tomography."""

from __future__ import annotations

from collections.abc import Callable
from fractions import Fraction
from functools import cache
from itertools import combinations

Edge = tuple[int, int]
Hafnian = Callable[[tuple[int, ...]], Fraction]

PINNED_PIVOTS = {
    (7, 3): (0, 1, 2, 3, 4, 5),
    (8, 3): (0, 1, 2, 3, 6, 10, 15),
    (9, 3): (0, 1, 2, 3, 4, 10, 20, 35),
    (11, 5): tuple(range(10)),
}


def edge_list(n: int) -> list[Edge]:
    return list(combinations(range(n), 2))


def cached_hafnian(weights: dict[Edge, Fraction]) -> Hafnian:
    @cache
    def evaluate(vertices: tuple[int, ...]) -> Fraction:
        if not vertices:
            return Fraction(1)
        first = vertices[0]
        total = Fraction(0)
        for partner in vertices[1:]:
            remainder = tuple(
                vertex for vertex in vertices[1:] if vertex != partner
            )
            edge = tuple(sorted((first, partner)))
            total += weights.get(edge, Fraction(0)) * evaluate(remainder)
        return total

    return evaluate


def one_inclusion_matrix(vertex_count: int, subset_size: int) -> list[list[int]]:
    return [
        [int(vertex in subset) for vertex in range(vertex_count)]
        for subset in combinations(range(vertex_count), subset_size)
    ]


def two_inclusion_matrix(vertex_count: int, subset_size: int) -> list[list[int]]:
    edges = edge_list(vertex_count)
    return [
        [int(edge[0] in subset and edge[1] in subset) for edge in edges]
        for subset in combinations(range(vertex_count), subset_size)
    ]


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
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
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][entry] - factor * work[pivot_row][entry]
                for entry in range(column_count)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(pivot_index, size)
                if work[row][pivot_index]
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = (
                work[pivot_row],
                work[pivot_index],
            )
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def solve_square(
    matrix: list[list[Fraction]], right_hand_side: list[Fraction]
) -> list[Fraction]:
    size = len(matrix)
    work = [row[:] + [rhs] for row, rhs in zip(matrix, right_hand_side, strict=True)]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        assert pivot is not None
        work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [value / pivot_value for value in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][entry] - factor * work[column][entry]
                for entry in range(size + 1)
            ]
    return [work[row][-1] for row in range(size)]


def audit_fixed_partner_and_euler_orders() -> None:
    for k in (1, 2, 3, 4, 5):
        n = 2 * k
        vertices = tuple(range(n))
        weights = {
            edge: Fraction((edge[0] + 2) * (edge[1] + 3) - 1)
            for edge in edge_list(n)
        }
        hafnian = cached_hafnian(weights)
        pin = 0
        others = tuple(range(1, n))
        partner_sum = sum(
            weights[(pin, partner)]
            * hafnian(tuple(vertex for vertex in others if vertex != partner))
            for partner in others
        )
        assert partner_sum == hafnian(vertices)

        euler_sum = sum(
            weight
            * hafnian(tuple(vertex for vertex in vertices if vertex not in edge))
            for edge, weight in weights.items()
        )
        assert euler_sum == k * hafnian(vertices)


def audit_pinned_inclusion_certificates() -> None:
    cases = (
        (6, 5, (0, 1, 2, 3, 4, 5), 5),
        (7, 5, (0, 1, 2, 3, 6, 10, 15), 5),
        (8, 5, (0, 1, 2, 3, 4, 10, 20, 35), 5),
        (10, 9, tuple(range(10)), 9),
    )
    for vertex_count, subset_size, pivots, expected_determinant in cases:
        matrix = one_inclusion_matrix(vertex_count, subset_size)
        assert rational_rank(matrix) == vertex_count
        selected = [matrix[row] for row in pivots]
        assert bareiss_determinant(selected) == expected_determinant


def audit_first_deck_hierarchy() -> None:
    for n, order, expected_rank in ((7, 4, 21), (10, 8, 45), (11, 8, 55)):
        matrix = two_inclusion_matrix(n, order)
        assert rational_rank(matrix) == expected_rank

    for n, order, fibre_dimension in ((9, 8, 27), (13, 12, 65)):
        edges = edge_list(n)
        matrix = two_inclusion_matrix(n, order)
        assert rational_rank(matrix) == n
        assert len(edges) - n == fibre_dimension

        test_values = {
            edge: Fraction((edge[0] + 1) * (edge[1] + 2)) for edge in edges
        }
        total = sum(test_values.values())
        degrees = {
            vertex: sum(
                value for edge, value in test_values.items() if vertex in edge
            )
            for vertex in range(n)
        }
        row_subsets = list(combinations(range(n), order))
        row_values = [
            sum(
                Fraction(entry) * test_values[edge]
                for entry, edge in zip(row, edges, strict=True)
            )
            for row in matrix
        ]
        expected_rows = [
            total
            - degrees[next(vertex for vertex in range(n) if vertex not in subset)]
            for subset in row_subsets
        ]
        assert row_values == expected_rows

        for prescribed in edges:
            u, v = prescribed
            other_vertices = [
                vertex for vertex in range(n) if vertex not in prescribed
            ]
            a, b = other_vertices[:2]
            tangent = dict.fromkeys(edges, Fraction(0))
            tangent[tuple(sorted((u, v)))] = Fraction(1)
            tangent[tuple(sorted((v, a)))] = Fraction(-1)
            tangent[tuple(sorted((a, b)))] = Fraction(1)
            tangent[tuple(sorted((b, u)))] = Fraction(-1)
            assert tangent[prescribed] == 1
            assert all(
                sum(
                    Fraction(entry) * tangent[edge]
                    for entry, edge in zip(row, edges, strict=True)
                )
                == 0
                for row in matrix
            )


def fixed_weights(n: int) -> dict[Edge, Fraction]:
    weights = dict.fromkeys(edge_list(n), Fraction(1))
    weights[(0, 1)] = Fraction(2)
    return weights


def pinned_system(
    n: int, k: int, pin: int, hafnian: Hafnian
) -> tuple[tuple[int, ...], list[list[Fraction]], list[Fraction]]:
    other_vertices = tuple(vertex for vertex in range(n) if vertex != pin)
    rows: list[list[Fraction]] = []
    right_hand_side: list[Fraction] = []
    for subset in combinations(other_vertices, 2 * k - 1):
        rows.append(
            [
                hafnian(tuple(vertex for vertex in subset if vertex != partner))
                if partner in subset
                else Fraction(0)
                for partner in other_vertices
            ]
        )
        right_hand_side.append(hafnian(tuple(sorted((pin, *subset)))))
    return other_vertices, rows, right_hand_side


def audit_all_star_reconstruction(n: int, k: int) -> None:
    weights = fixed_weights(n)
    hafnian = cached_hafnian(weights)
    pivots = PINNED_PIVOTS[(n, k)]
    for pin in range(n):
        other_vertices, matrix, right_hand_side = pinned_system(
            n, k, pin, hafnian
        )
        expected = [
            weights[tuple(sorted((pin, partner)))] for partner in other_vertices
        ]
        assert all(
            sum(coefficient * value for coefficient, value in zip(row, expected, strict=True)) == rhs
            for row, rhs in zip(matrix, right_hand_side, strict=True)
        )
        selected_matrix = [matrix[row] for row in pivots]
        selected_rhs = [right_hand_side[row] for row in pivots]
        assert solve_square(selected_matrix, selected_rhs) == expected


def all_deck_values(
    n: int, order: int, hafnian: Hafnian
) -> dict[tuple[int, ...], Fraction]:
    return {
        subset: hafnian(subset) for subset in combinations(range(n), order)
    }


def audit_sparse_matching_tori() -> None:
    cases = (
        (2, (Fraction(7), Fraction(1, 7))),
        (4, (Fraction(2), Fraction(3), Fraction(5), Fraction(1, 30))),
    )
    for q, parameters in cases:
        n = 2 * q + 2
        weights = {
            (2 * index, 2 * index + 1): parameter
            for index, parameter in enumerate(parameters)
        }
        hafnian = cached_hafnian(weights)
        lower_deck = all_deck_values(n, 2 * q, hafnian)
        supported_vertices = tuple(range(2 * q))
        assert lower_deck[supported_vertices] == 1
        assert sum(value != 0 for value in lower_deck.values()) == 1
        assert all(
            value == 0
            for value in all_deck_values(n, 2 * q + 2, hafnian).values()
        )


def audit_capacities() -> None:
    cases = (
        (42, 3, False),
        (98, 4, False),
        (210, 5, True),
        (99, 4, False),
        (219, 5, True),
        (176, 3, False),
        (45, 2, False),
        (9, 1, False),
        (46, 2, False),
        (13, 1, False),
    )
    for deck_size, roots, expected_to_fit in cases:
        assert (deck_size <= 3**roots) is expected_to_fit


def main() -> None:
    audit_fixed_partner_and_euler_orders()
    print("AUDIT PASS: independent pinned and Euler identities at k=1..5")
    audit_pinned_inclusion_certificates()
    print("AUDIT PASS: independent pinned ranks and Bareiss minors")
    audit_first_deck_hierarchy()
    print("AUDIT PASS: independent r>=2 ranks and r=1 tangent kernels")
    for n, k in PINNED_PIVOTS:
        audit_all_star_reconstruction(n, k)
    print("AUDIT PASS: every fixed P5/P6/P7 star reconstructed")
    audit_sparse_matching_tori()
    print("AUDIT PASS: nonzero sparse matching tori at q=2,4")
    audit_capacities()
    print("AUDIT PASS: exact formal direct-label capacity counts")
    print("AUDIT SCOPE: legal exposure and determinant forcing are not proved")
    print("searches=0 project_imports=0 computer_algebra=0 finite_fields=0")


if __name__ == "__main__":
    main()
