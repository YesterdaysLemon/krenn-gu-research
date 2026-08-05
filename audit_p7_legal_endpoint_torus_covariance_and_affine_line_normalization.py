"""Independent stdlib audit of P7 legal endpoint-torus covariance."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from fractions import Fraction
from functools import cache
from itertools import combinations, permutations
from math import prod

Edge = tuple[int, int]
Hafnian = Callable[[tuple[int, ...]], Fraction]

PIVOT_ROWS = (0, 1, 2, 3, 4, 10, 20, 35)


def edge_list(n: int) -> list[Edge]:
    return list(combinations(range(n), 2))


def perfect_matchings(vertices: tuple[int, ...]) -> Iterator[tuple[Edge, ...]]:
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for partner in vertices[1:]:
        remainder = tuple(
            vertex for vertex in vertices[1:] if vertex != partner
        )
        for matching in perfect_matchings(remainder):
            yield ((first, partner), *matching)


def audit_matching_column_characters() -> None:
    roots = tuple(range(5))
    endpoints = tuple(range(9))
    rho = (2, 3, 5, 7, 11, 13, 17, 19, 23)

    for deletion in combinations(endpoints, 5):
        expected = prod(rho[endpoint] for endpoint in deletion)
        assert all(
            prod(rho[assignment[root]] for root in roots) == expected
            for assignment in permutations(deletion)
        )

    for deletion in combinations(endpoints, 3):
        expected = prod(rho[endpoint] for endpoint in deletion)
        for root_pair in combinations(roots, 2):
            remaining_roots = tuple(root for root in roots if root not in root_pair)
            assert all(
                prod(
                    rho[assignment[index]]
                    for index, _ in enumerate(remaining_roots)
                )
                == expected
                for assignment in permutations(deletion)
            )

    near_perfect_count = 0
    for endpoint in endpoints:
        for unmatched_root in roots:
            remaining_roots = tuple(
                root for root in roots if root != unmatched_root
            )
            for _ in perfect_matchings(remaining_roots):
                assert rho[endpoint] != 0
                near_perfect_count += 1
    assert near_perfect_count == 135


def cached_hafnian(weights: dict[Edge, Fraction]) -> Hafnian:
    @cache
    def evaluate(vertices: tuple[int, ...]) -> Fraction:
        if not vertices:
            return Fraction(1)
        first = vertices[0]
        return sum(
            weights.get(tuple(sorted((first, partner))), Fraction(0))
            * evaluate(
                tuple(
                    vertex
                    for vertex in vertices[1:]
                    if vertex != partner
                )
            )
            for partner in vertices[1:]
        )

    return evaluate


def fraction_determinant(matrix: list[list[Fraction]]) -> Fraction:
    size = len(matrix)
    assert size and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    determinant = Fraction(1)
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant *= -1
        pivot_value = work[column][column]
        determinant *= pivot_value
        for entry in range(column, size):
            work[column][entry] /= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column]
            if not factor:
                continue
            for entry in range(column, size):
                work[row][entry] -= factor * work[column][entry]
    return determinant


def replace_column(
    matrix: list[list[Fraction]], column: int, vector: list[Fraction]
) -> list[list[Fraction]]:
    return [
        [vector[row] if entry == column else value for entry, value in enumerate(line)]
        for row, line in enumerate(matrix)
    ]


def fixed_weights() -> dict[Edge, Fraction]:
    weights = dict.fromkeys(edge_list(9), Fraction(1))
    weights[(0, 1)] = Fraction(2)
    return weights


def physical_decks() -> dict[tuple[int, ...], Fraction]:
    hafnian = cached_hafnian(fixed_weights())
    return {
        subset: hafnian(subset)
        for order in (4, 6, 8)
        for subset in combinations(range(9), order)
    }


def transform_line(
    line: dict[tuple[int, ...], Fraction], rho: tuple[int, ...]
) -> dict[tuple[int, ...], Fraction]:
    total_product = prod(rho)
    return {
        subset: Fraction(prod(rho[vertex] for vertex in subset), total_product)
        * value
        for subset, value in line.items()
    }


def pinned_data(
    line: dict[tuple[int, ...], Fraction], pin: int
) -> tuple[Fraction, dict[int, Fraction]]:
    other_vertices = tuple(vertex for vertex in range(9) if vertex != pin)
    row_subsets = list(combinations(other_vertices, 5))
    full_matrix = [
        [
            line[tuple(vertex for vertex in subset if vertex != partner)]
            if partner in subset
            else Fraction(0)
            for partner in other_vertices
        ]
        for subset in row_subsets
    ]
    full_rhs = [line[tuple(sorted((pin, *subset)))] for subset in row_subsets]
    matrix = [full_matrix[row] for row in PIVOT_ROWS]
    right_hand_side = [full_rhs[row] for row in PIVOT_ROWS]
    determinant = fraction_determinant(matrix)
    assert determinant
    vector = [
        fraction_determinant(replace_column(matrix, column, right_hand_side))
        for column in range(8)
    ]
    return determinant, dict(zip(other_vertices, vector, strict=True))


def all_pinned_data(
    line: dict[tuple[int, ...], Fraction]
) -> tuple[dict[int, Fraction], dict[int, dict[int, Fraction]]]:
    determinants: dict[int, Fraction] = {}
    vectors: dict[int, dict[int, Fraction]] = {}
    for pin in range(9):
        determinant, vector = pinned_data(line, pin)
        determinants[pin] = determinant
        vectors[pin] = vector
    return determinants, vectors


def pin_character(pin: int, rho: tuple[int, ...]) -> Fraction:
    total_product = prod(rho)
    other_vertices = tuple(vertex for vertex in range(9) if vertex != pin)
    rows = list(combinations(other_vertices, 5))
    selected_rows = [rows[index] for index in PIVOT_ROWS]
    numerator = prod(
        prod(rho[vertex] for vertex in subset) for subset in selected_rows
    )
    denominator = total_product**8 * prod(
        rho[vertex] for vertex in other_vertices
    )
    return Fraction(numerator, denominator)


def hadamard_residual(
    upper_set: tuple[int, ...],
    pin: int,
    line: dict[tuple[int, ...], Fraction],
    determinants: dict[int, Fraction],
    vectors: dict[int, dict[int, Fraction]],
) -> Fraction:
    return determinants[pin] * line[upper_set] - sum(
        vectors[pin][partner]
        * line[
            tuple(
                vertex
                for vertex in upper_set
                if vertex not in (pin, partner)
            )
        ]
        for partner in upper_set
        if partner != pin
    )


def audit_pinned_and_stress_characters() -> None:
    line = physical_decks()
    rho = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    total_product = prod(rho)
    transformed = transform_line(line, rho)
    determinants, vectors = all_pinned_data(line)
    transformed_determinants, transformed_vectors = all_pinned_data(transformed)

    for pin in range(9):
        character = pin_character(pin, rho)
        assert transformed_determinants[pin] == character * determinants[pin]
        for partner in range(9):
            if partner == pin:
                continue
            assert transformed_vectors[pin][partner] == (
                character
                * rho[pin]
                * rho[partner]
                * vectors[pin][partner]
            )

    other_vertices = tuple(range(1, 9))
    unselected_five_set = list(combinations(other_vertices, 5))[5]
    six_set = tuple(sorted((0, *unselected_five_set)))
    perturbed = dict(line)
    perturbed[six_set] += 1
    transformed_perturbed = transform_line(perturbed, rho)
    perturbed_determinants, perturbed_vectors = all_pinned_data(perturbed)
    transformed_pd, transformed_pv = all_pinned_data(transformed_perturbed)

    residual = hadamard_residual(
        six_set, 0, perturbed, perturbed_determinants, perturbed_vectors
    )
    transformed_residual = hadamard_residual(
        six_set, 0, transformed_perturbed, transformed_pd, transformed_pv
    )
    assert residual
    expected_character = (
        pin_character(0, rho)
        * Fraction(prod(rho[vertex] for vertex in six_set), total_product)
    )
    assert transformed_residual == expected_character * residual

    overlaps = []
    for left, right in combinations(range(9), 2):
        overlap = (
            perturbed_determinants[right] * perturbed_vectors[left][right]
            - perturbed_determinants[left] * perturbed_vectors[right][left]
        )
        transformed_overlap = (
            transformed_pd[right] * transformed_pv[left][right]
            - transformed_pd[left] * transformed_pv[right][left]
        )
        character = (
            pin_character(left, rho)
            * pin_character(right, rho)
            * rho[left]
            * rho[right]
        )
        assert transformed_overlap == character * overlap
        overlaps.append(overlap)
    assert any(overlaps)


def audit_affine_amplitude_character() -> None:
    line = physical_decks()
    rho = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    total_product = prod(rho)
    transformed = transform_line(line, rho)
    determinants, vectors = all_pinned_data(transformed)
    transformed_weights = {
        (left, right): vectors[left][right] / determinants[left]
        for left, right in edge_list(9)
    }
    hafnian = cached_hafnian(transformed_weights)
    amplitudes = {
        hafnian(subset) / transformed[subset]
        for subset in combinations(range(9), 4)
    }
    assert amplitudes == {Fraction(total_product)}

    for order in (6, 8):
        assert all(
            hadamard_residual(
                subset, min(subset), transformed, determinants, vectors
            )
            == 0
            for subset in combinations(range(9), order)
        )
    assert total_product != 1
    assert any(
        transformed[subset] != hafnian(subset)
        for subset in combinations(range(9), 4)
    )


def main() -> None:
    audit_matching_column_characters()
    print("AUDIT PASS: independent depth-5/3/1 endpoint characters")
    audit_pinned_and_stress_characters()
    print("AUDIT PASS: independent pinned and nonzero stress semi-invariants")
    audit_affine_amplitude_character()
    print("AUDIT PASS: independent projective/affine normalization split")
    print("AUDIT SCOPE: no unconditional legal target-incidence line")
    print("searches=0 eliminations=0 project_imports=0 computer_algebra=0")


if __name__ == "__main__":
    main()
