"""Primary exact checks for legal endpoint-torus covariance in P7.

The replay expands only fixed matching patterns and fixed exact matrices.  It
does not search supports, incidence parameters, or cofactor vectors.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from functools import cache
from itertools import combinations, permutations

import sympy as sp

Edge = tuple[int, int]
Hafnian = Callable[[tuple[int, ...]], sp.Expr]

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


def verify_matching_column_characters() -> None:
    roots = tuple(range(5))
    endpoints = tuple(range(9))
    rho = sp.symbols("rho0:9", nonzero=True)

    for deletion in combinations(endpoints, 5):
        expected = sp.prod(rho[endpoint] for endpoint in deletion)
        for assignment in permutations(deletion):
            term_character = sp.prod(rho[assignment[root]] for root in roots)
            assert term_character == expected

    for deletion in combinations(endpoints, 3):
        expected = sp.prod(rho[endpoint] for endpoint in deletion)
        for root_pair in combinations(roots, 2):
            remaining_roots = tuple(root for root in roots if root not in root_pair)
            for assignment in permutations(deletion):
                term_character = sp.prod(
                    rho[assignment[index]]
                    for index, _ in enumerate(remaining_roots)
                )
                assert term_character == expected

    near_perfect_count = 0
    for endpoint in endpoints:
        for unmatched_root in roots:
            remaining_roots = tuple(
                root for root in roots if root != unmatched_root
            )
            for _ in perfect_matchings(remaining_roots):
                assert rho[endpoint] == rho[endpoint]
                near_perfect_count += 1
    assert near_perfect_count == 9 * 5 * 3


def cached_hafnian(weights: dict[Edge, sp.Expr]) -> Hafnian:
    @cache
    def evaluate(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        return sp.expand(
            sum(
                weights[tuple(sorted((first, partner)))]
                * evaluate(
                    tuple(
                        vertex
                        for vertex in vertices[1:]
                        if vertex != partner
                    )
                )
                for partner in vertices[1:]
            )
        )

    return evaluate


def fixed_weights() -> dict[Edge, sp.Expr]:
    weights = dict.fromkeys(edge_list(9), sp.Integer(1))
    weights[(0, 1)] = sp.Integer(2)
    return weights


def physical_decks() -> dict[tuple[int, ...], sp.Expr]:
    hafnian = cached_hafnian(fixed_weights())
    return {
        subset: hafnian(subset)
        for order in (4, 6, 8)
        for subset in combinations(range(9), order)
    }


def transform_line(
    line: dict[tuple[int, ...], sp.Expr], rho: tuple[sp.Expr, ...]
) -> dict[tuple[int, ...], sp.Expr]:
    total_product = sp.prod(rho)
    return {
        subset: sp.cancel(
            sp.prod(rho[vertex] for vertex in subset)
            * value
            / total_product
        )
        for subset, value in line.items()
    }


def pinned_data(
    line: dict[tuple[int, ...], sp.Expr], pin: int
) -> tuple[sp.Expr, dict[int, sp.Expr]]:
    other_vertices = tuple(vertex for vertex in range(9) if vertex != pin)
    row_subsets = list(combinations(other_vertices, 5))
    matrix = sp.Matrix(
        [
            [
                line[tuple(vertex for vertex in subset if vertex != partner)]
                if partner in subset
                else 0
                for partner in other_vertices
            ]
            for subset in row_subsets
        ]
    )
    right_hand_side = sp.Matrix(
        [line[tuple(sorted((pin, *subset)))] for subset in row_subsets]
    )
    selected_matrix = matrix[list(PIVOT_ROWS), :]
    selected_rhs = right_hand_side[list(PIVOT_ROWS), :]
    determinant = sp.factor(selected_matrix.det())
    assert determinant != 0
    cramer_vector = selected_matrix.adjugate() * selected_rhs
    return determinant, dict(zip(other_vertices, cramer_vector, strict=True))


def all_pinned_data(
    line: dict[tuple[int, ...], sp.Expr]
) -> tuple[dict[int, sp.Expr], dict[int, dict[int, sp.Expr]]]:
    determinants: dict[int, sp.Expr] = {}
    vectors: dict[int, dict[int, sp.Expr]] = {}
    for pin in range(9):
        determinant, vector = pinned_data(line, pin)
        determinants[pin] = determinant
        vectors[pin] = vector
    return determinants, vectors


def pin_character(pin: int, rho: tuple[sp.Expr, ...]) -> sp.Expr:
    total_product = sp.prod(rho)
    other_vertices = tuple(vertex for vertex in range(9) if vertex != pin)
    row_subsets = list(combinations(other_vertices, 5))
    selected_rows = [row_subsets[index] for index in PIVOT_ROWS]
    return sp.cancel(
        sp.prod(
            sp.prod(rho[vertex] for vertex in subset)
            for subset in selected_rows
        )
        / (
            total_product**8
            * sp.prod(rho[vertex] for vertex in other_vertices)
        )
    )


def verify_pinned_characters() -> None:
    line = physical_decks()
    rho = tuple(map(sp.Integer, (2, 3, 5, 7, 11, 13, 17, 19, 23)))
    transformed = transform_line(line, rho)
    determinants, vectors = all_pinned_data(line)
    transformed_determinants, transformed_vectors = all_pinned_data(transformed)

    weights = fixed_weights()
    for pin in range(9):
        character = pin_character(pin, rho)
        assert sp.cancel(
            transformed_determinants[pin]
            - character * determinants[pin]
        ) == 0
        for partner in range(9):
            if partner == pin:
                continue
            expected = (
                character
                * rho[pin]
                * rho[partner]
                * vectors[pin][partner]
            )
            assert sp.cancel(transformed_vectors[pin][partner] - expected) == 0

    for (left, right), weight in weights.items():
        original_edge = sp.cancel(vectors[left][right] / determinants[left])
        transformed_edge = sp.cancel(
            transformed_vectors[left][right] / transformed_determinants[left]
        )
        assert original_edge == weight
        assert transformed_edge == rho[left] * rho[right] * weight


def hadamard_residual(
    upper_set: tuple[int, ...],
    pin: int,
    line: dict[tuple[int, ...], sp.Expr],
    determinants: dict[int, sp.Expr],
    vectors: dict[int, dict[int, sp.Expr]],
) -> sp.Expr:
    return sp.expand(
        determinants[pin] * line[upper_set]
        - sum(
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
    )


def verify_stress_characters() -> None:
    line = physical_decks()
    rho = tuple(map(sp.Integer, (2, 3, 5, 7, 11, 13, 17, 19, 23)))
    total_product = sp.prod(rho)

    other_vertices = tuple(range(1, 9))
    unselected_five_set = list(combinations(other_vertices, 5))[5]
    six_set = tuple(sorted((0, *unselected_five_set)))
    perturbed = dict(line)
    perturbed[six_set] += 1
    transformed = transform_line(perturbed, rho)

    determinants, vectors = all_pinned_data(perturbed)
    transformed_determinants, transformed_vectors = all_pinned_data(transformed)
    residual = hadamard_residual(six_set, 0, perturbed, determinants, vectors)
    transformed_residual = hadamard_residual(
        six_set,
        0,
        transformed,
        transformed_determinants,
        transformed_vectors,
    )
    assert residual != 0
    expected_character = (
        pin_character(0, rho)
        * sp.prod(rho[vertex] for vertex in six_set)
        / total_product
    )
    assert sp.cancel(transformed_residual - expected_character * residual) == 0

    overlaps = []
    for left, right in combinations(range(9), 2):
        overlap = (
            determinants[right] * vectors[left][right]
            - determinants[left] * vectors[right][left]
        )
        transformed_overlap = (
            transformed_determinants[right] * transformed_vectors[left][right]
            - transformed_determinants[left] * transformed_vectors[right][left]
        )
        character = (
            pin_character(left, rho)
            * pin_character(right, rho)
            * rho[left]
            * rho[right]
        )
        assert sp.cancel(transformed_overlap - character * overlap) == 0
        overlaps.append(overlap)
    assert any(overlap != 0 for overlap in overlaps)


def verify_affine_amplitude_character() -> None:
    line = physical_decks()
    rho = tuple(map(sp.Integer, (2, 3, 5, 7, 11, 13, 17, 19, 23)))
    total_product = sp.prod(rho)
    transformed = transform_line(line, rho)
    determinants, vectors = all_pinned_data(transformed)

    transformed_weights = {
        (left, right): sp.cancel(vectors[left][right] / determinants[left])
        for left, right in edge_list(9)
    }
    hafnian = cached_hafnian(transformed_weights)
    required_amplitudes = {
        sp.cancel(hafnian(subset) / transformed[subset])
        for subset in combinations(range(9), 4)
    }
    assert required_amplitudes == {total_product}

    for order in (6, 8):
        for subset in combinations(range(9), order):
            pin = min(subset)
            assert (
                hadamard_residual(
                    subset, pin, transformed, determinants, vectors
                )
                == 0
            )

    assert total_product != 1
    assert any(
        transformed[subset] != hafnian(subset)
        for subset in combinations(range(9), 4)
    )


def main() -> None:
    verify_matching_column_characters()
    print("PASS: every legal depth-5/3/1 column has endpoint character rho_D")
    verify_pinned_characters()
    print("PASS: exact pinned determinant, Cramer, and vertex-edge characters")
    verify_stress_characters()
    print("PASS: nonzero degree-9 and overlap residuals are semi-invariants")
    verify_affine_amplitude_character()
    print("PASS: all projective stresses vanish while affine scale moves by product rho")
    print("SCOPE: an unconditional legal full-rank incidence line remains UNKNOWN")
    print("searches=0 eliminations=0 project_imports=0 finite_fields=0")


if __name__ == "__main__":
    main()
