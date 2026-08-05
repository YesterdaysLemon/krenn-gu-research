"""Independent stdlib audit of determinant-cleared P7 integrability."""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from itertools import combinations
from math import prod

Edge = tuple[int, int]
Hafnian = Callable[[tuple[int, ...]], int]

PIVOT_ROWS = (0, 1, 2, 3, 4, 10, 20, 35)


def edge_list(n: int) -> list[Edge]:
    return list(combinations(range(n), 2))


def cached_hafnian(weights: dict[Edge, int]) -> Hafnian:
    @cache
    def evaluate(vertices: tuple[int, ...]) -> int:
        if not vertices:
            return 1
        first = vertices[0]
        total = 0
        for partner in vertices[1:]:
            remainder = tuple(
                vertex for vertex in vertices[1:] if vertex != partner
            )
            total += weights.get(tuple(sorted((first, partner))), 0) * evaluate(
                remainder
            )
        return total

    return evaluate


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


def replace_column(
    matrix: list[list[int]], column: int, vector: list[int]
) -> list[list[int]]:
    return [
        [vector[row] if entry == column else value for entry, value in enumerate(line)]
        for row, line in enumerate(matrix)
    ]


def matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(value * coordinate for value, coordinate in zip(row, vector, strict=True))
        for row in matrix
    ]


def fixed_weights() -> dict[Edge, int]:
    weights = dict.fromkeys(edge_list(9), 1)
    weights[(0, 1)] = 2
    return weights


def numerator_decks(beta: int) -> dict[tuple[int, ...], int]:
    hafnian = cached_hafnian(fixed_weights())
    return {
        subset: beta * hafnian(subset)
        for order in (4, 6, 8)
        for subset in combinations(range(9), order)
    }


def pinned_cramer_data(
    numerators: dict[tuple[int, ...], int], pin: int
) -> tuple[int, dict[int, int]]:
    other_vertices = tuple(vertex for vertex in range(9) if vertex != pin)
    row_subsets = list(combinations(other_vertices, 5))
    full_matrix = [
        [
            numerators[tuple(vertex for vertex in subset if vertex != partner)]
            if partner in subset
            else 0
            for partner in other_vertices
        ]
        for subset in row_subsets
    ]
    full_rhs = [
        numerators[tuple(sorted((pin, *subset)))] for subset in row_subsets
    ]
    matrix = [full_matrix[row] for row in PIVOT_ROWS]
    right_hand_side = [full_rhs[row] for row in PIVOT_ROWS]
    determinant = bareiss_determinant(matrix)
    assert determinant != 0
    cramer_vector = [
        bareiss_determinant(replace_column(matrix, column, right_hand_side))
        for column in range(8)
    ]
    assert matrix_vector(matrix, cramer_vector) == [
        determinant * value for value in right_hand_side
    ]
    return determinant, dict(zip(other_vertices, cramer_vector, strict=True))


def all_pinned_data(
    numerators: dict[tuple[int, ...], int], pins: range
) -> tuple[dict[int, int], dict[int, dict[int, int]]]:
    determinants: dict[int, int] = {}
    vectors: dict[int, dict[int, int]] = {}
    for pin in pins:
        determinant, vector = pinned_cramer_data(numerators, pin)
        determinants[pin] = determinant
        vectors[pin] = vector
    return determinants, vectors


def audit_target_incidence() -> None:
    gamma = [
        [2, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [3, -1, 2],
        [1, 4, -2],
    ]
    cofactor_vector = [5, -2, 7]
    target = matrix_vector(gamma, cofactor_vector)
    selected = gamma[:3]
    selected_target = target[:3]
    beta = bareiss_determinant(selected)
    numerator = [
        bareiss_determinant(replace_column(selected, column, selected_target))
        for column in range(3)
    ]
    assert numerator == [beta * value for value in cofactor_vector]
    for row in range(3, 5):
        assert beta * target[row] == sum(
            value * coordinate
            for value, coordinate in zip(gamma[row], numerator, strict=True)
        )
    perturbed = target[:]
    perturbed[4] += 1
    residual = beta * perturbed[4] - sum(
        value * coordinate
        for value, coordinate in zip(gamma[4], numerator, strict=True)
    )
    assert residual == beta


def hadamard_residual(
    upper_set: tuple[int, ...],
    pin: int,
    numerators: dict[tuple[int, ...], int],
    determinants: dict[int, int],
    vectors: dict[int, dict[int, int]],
) -> int:
    return determinants[pin] * numerators[upper_set] - sum(
        vectors[pin][partner]
        * numerators[
            tuple(
                vertex
                for vertex in upper_set
                if vertex not in (pin, partner)
            )
        ]
        for partner in upper_set
        if partner != pin
    )


def four_residual(
    subset: tuple[int, int, int, int],
    beta: int,
    numerators: dict[tuple[int, ...], int],
    determinants: dict[int, int],
    vectors: dict[int, dict[int, int]],
) -> int:
    i, j, k, ell = subset
    denominator = determinants[i] * determinants[j] * determinants[k]
    matching_numerator = (
        determinants[j] * vectors[i][j] * vectors[k][ell]
        + determinants[k] * vectors[i][k] * vectors[j][ell]
        + determinants[k] * vectors[i][ell] * vectors[j][k]
    )
    return denominator * numerators[subset] - beta * matching_numerator


def euler_residual(
    subset: tuple[int, ...],
    numerators: dict[tuple[int, ...], int],
    determinants: dict[int, int],
    vectors: dict[int, dict[int, int]],
) -> int:
    maximum = max(subset)
    denominator = prod(
        determinants[vertex] for vertex in subset if vertex != maximum
    )
    edge_sum = 0
    for left, right in combinations(subset, 2):
        remaining_denominator = prod(
            determinants[vertex]
            for vertex in subset
            if vertex not in (maximum, left)
        )
        lower_set = tuple(
            vertex for vertex in subset if vertex not in (left, right)
        )
        edge_sum += (
            vectors[left][right]
            * remaining_denominator
            * numerators[lower_set]
        )
    return len(subset) // 2 * denominator * numerators[subset] - edge_sum


def audit_integrability_hierarchy() -> None:
    beta = 7
    numerators = numerator_decks(beta)
    determinants, vectors = all_pinned_data(numerators, range(9))
    weights = fixed_weights()
    for (left, right), weight in weights.items():
        assert vectors[left][right] == determinants[left] * weight
        assert (
            determinants[right] * vectors[left][right]
            == determinants[left] * vectors[right][left]
        )

    assert all(
        four_residual(subset, beta, numerators, determinants, vectors) == 0
        for subset in combinations(range(9), 4)
    )
    for order in (6, 8):
        for subset in combinations(range(9), order):
            assert all(
                hadamard_residual(
                    subset, pin, numerators, determinants, vectors
                )
                == 0
                for pin in subset
            )
            assert (
                euler_residual(subset, numerators, determinants, vectors) == 0
            )

    assert any(
        four_residual(subset, beta + 1, numerators, determinants, vectors)
        != 0
        for subset in combinations(range(9), 4)
    )


def audit_low_degree_detection() -> None:
    beta = 7
    numerators = numerator_decks(beta)
    determinants, vectors = all_pinned_data(numerators, range(8))
    other_vertices = tuple(range(1, 9))
    unselected_five_set = list(combinations(other_vertices, 5))[5]
    six_set = tuple(sorted((0, *unselected_five_set)))
    perturbed_six = dict(numerators)
    perturbed_six[six_set] += 1
    new_determinants, new_vectors = all_pinned_data(perturbed_six, range(8))
    assert new_determinants[0] == determinants[0]
    assert new_vectors[0] == vectors[0]
    assert (
        hadamard_residual(
            six_set, 0, perturbed_six, new_determinants, new_vectors
        )
        == determinants[0]
    )

    eight_set = tuple(range(8))
    perturbed_eight = dict(numerators)
    perturbed_eight[eight_set] += 1
    assert (
        hadamard_residual(
            eight_set, 0, perturbed_eight, determinants, vectors
        )
        == determinants[0]
    )


def main() -> None:
    audit_target_incidence()
    print("AUDIT PASS: independent determinant-cleared target incidence")
    audit_integrability_hierarchy()
    print("AUDIT PASS: independent four/hadamard/euler/h8 hierarchy")
    audit_low_degree_detection()
    print("AUDIT PASS: independent degree-nine perturbation detection")
    print("AUDIT SCOPE: relative companion data and GHZ forcing remain open")
    print("searches=0 eliminations=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
