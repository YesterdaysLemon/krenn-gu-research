"""Primary exact checks for determinant-cleared P7 hafnian integrability.

The replay uses fixed exact matrices and one fixed weighted graph.  It does
not search supports, targets, cofactor vectors, or parameter families.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from itertools import combinations

import sympy as sp

Edge = tuple[int, int]
Hafnian = Callable[[tuple[int, ...]], sp.Expr]

PIVOT_ROWS = (0, 1, 2, 3, 4, 10, 20, 35)


def edge_list(n: int) -> list[Edge]:
    return list(combinations(range(n), 2))


def cached_hafnian(weights: dict[Edge, sp.Expr]) -> Hafnian:
    @cache
    def evaluate(vertices: tuple[int, ...]) -> sp.Expr:
        if not vertices:
            return sp.Integer(1)
        first = vertices[0]
        total = sp.Integer(0)
        for partner in vertices[1:]:
            remainder = tuple(
                vertex for vertex in vertices[1:] if vertex != partner
            )
            total += weights[tuple(sorted((first, partner)))] * evaluate(
                remainder
            )
        return sp.expand(total)

    return evaluate


def fixed_weights() -> dict[Edge, sp.Expr]:
    weights = dict.fromkeys(edge_list(9), sp.Integer(1))
    weights[(0, 1)] = sp.Integer(2)
    return weights


def numerator_decks(beta: sp.Integer) -> dict[tuple[int, ...], sp.Expr]:
    hafnian = cached_hafnian(fixed_weights())
    return {
        subset: beta * hafnian(subset)
        for order in (4, 6, 8)
        for subset in combinations(range(9), order)
    }


def pinned_cramer_data(
    numerators: dict[tuple[int, ...], sp.Expr], pin: int
) -> tuple[sp.Expr, dict[int, sp.Expr], sp.Matrix, sp.Matrix]:
    other_vertices = tuple(vertex for vertex in range(9) if vertex != pin)
    row_subsets = list(combinations(other_vertices, 5))
    matrix = sp.Matrix(
        [
            [
                numerators[tuple(vertex for vertex in subset if vertex != partner)]
                if partner in subset
                else 0
                for partner in other_vertices
            ]
            for subset in row_subsets
        ]
    )
    right_hand_side = sp.Matrix(
        [numerators[tuple(sorted((pin, *subset)))] for subset in row_subsets]
    )
    selected_matrix = matrix[list(PIVOT_ROWS), :]
    selected_rhs = right_hand_side[list(PIVOT_ROWS), :]
    determinant = sp.expand(selected_matrix.det())
    cramer_vector = selected_matrix.adjugate() * selected_rhs
    assert selected_matrix * cramer_vector == determinant * selected_rhs
    return (
        determinant,
        dict(zip(other_vertices, cramer_vector, strict=True)),
        matrix,
        right_hand_side,
    )


def all_pinned_data(
    numerators: dict[tuple[int, ...], sp.Expr], pins: range
) -> tuple[dict[int, sp.Expr], dict[int, dict[int, sp.Expr]]]:
    determinants: dict[int, sp.Expr] = {}
    cramer_vectors: dict[int, dict[int, sp.Expr]] = {}
    for pin in pins:
        determinant, vector, _, _ = pinned_cramer_data(numerators, pin)
        assert determinant != 0
        determinants[pin] = determinant
        cramer_vectors[pin] = vector
    return determinants, cramer_vectors


def verify_target_incidence_cramer_identity() -> None:
    gamma = sp.Matrix(
        [
            [2, 1, 0],
            [0, 1, 1],
            [1, 0, 1],
            [3, -1, 2],
            [1, 4, -2],
        ]
    )
    cofactor_vector = sp.Matrix([5, -2, 7])
    target = gamma * cofactor_vector
    selected = gamma[:3, :]
    beta = selected.det()
    assert beta != 0
    numerator = selected.adjugate() * target[:3, :]
    assert numerator == beta * cofactor_vector
    for row in range(3, 5):
        assert beta * target[row] - (gamma[row, :] * numerator)[0] == 0

    perturbed = target.copy()
    perturbed[4] += 1
    assert beta * perturbed[4] - (gamma[4, :] * numerator)[0] == beta


def verify_reconstructed_edges(
    determinants: dict[int, sp.Expr],
    cramer_vectors: dict[int, dict[int, sp.Expr]],
) -> None:
    weights = fixed_weights()
    for (left, right), weight in weights.items():
        recovered = sp.cancel(
            cramer_vectors[left][right] / determinants[left]
        )
        assert recovered == weight


def hadamard_residual(
    upper_set: tuple[int, ...],
    pin: int,
    numerators: dict[tuple[int, ...], sp.Expr],
    determinants: dict[int, sp.Expr],
    cramer_vectors: dict[int, dict[int, sp.Expr]],
) -> sp.Expr:
    return sp.expand(
        determinants[pin] * numerators[upper_set]
        - sum(
            cramer_vectors[pin][partner]
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
    )


def four_realization_residual(
    subset: tuple[int, int, int, int],
    beta: sp.Expr,
    numerators: dict[tuple[int, ...], sp.Expr],
    determinants: dict[int, sp.Expr],
    cramer_vectors: dict[int, dict[int, sp.Expr]],
) -> sp.Expr:
    i, j, k, ell = subset
    denominator = determinants[i] * determinants[j] * determinants[k]
    matching_numerator = (
        determinants[j]
        * cramer_vectors[i][j]
        * cramer_vectors[k][ell]
        + determinants[k]
        * cramer_vectors[i][k]
        * cramer_vectors[j][ell]
        + determinants[k]
        * cramer_vectors[i][ell]
        * cramer_vectors[j][k]
    )
    return sp.expand(
        denominator * numerators[subset] - beta * matching_numerator
    )


def denominator_product(
    subset: tuple[int, ...], determinants: dict[int, sp.Expr]
) -> sp.Expr:
    maximum = max(subset)
    return sp.prod(
        determinants[vertex] for vertex in subset if vertex != maximum
    )


def euler_residual(
    subset: tuple[int, ...],
    numerators: dict[tuple[int, ...], sp.Expr],
    determinants: dict[int, sp.Expr],
    cramer_vectors: dict[int, dict[int, sp.Expr]],
) -> sp.Expr:
    denominator = denominator_product(subset, determinants)
    order_factor = len(subset) // 2
    edge_sum = sp.Integer(0)
    maximum = max(subset)
    for left, right in combinations(subset, 2):
        remaining_denominator = sp.prod(
            determinants[vertex]
            for vertex in subset
            if vertex not in (maximum, left)
        )
        edge_sum += (
            cramer_vectors[left][right]
            * remaining_denominator
            * numerators[
                tuple(
                    vertex for vertex in subset if vertex not in (left, right)
                )
            ]
        )
    return sp.expand(
        order_factor * denominator * numerators[subset] - edge_sum
    )


def verify_integrability_hierarchy() -> None:
    beta = sp.Integer(7)
    numerators = numerator_decks(beta)
    determinants, cramer_vectors = all_pinned_data(numerators, range(9))
    verify_reconstructed_edges(determinants, cramer_vectors)

    for left, right in combinations(range(9), 2):
        overlap = (
            determinants[right] * cramer_vectors[left][right]
            - determinants[left] * cramer_vectors[right][left]
        )
        assert overlap == 0

    for subset in combinations(range(9), 4):
        assert (
            four_realization_residual(
                subset, beta, numerators, determinants, cramer_vectors
            )
            == 0
        )

    for order in (6, 8):
        for subset in combinations(range(9), order):
            for pin in subset:
                assert (
                    hadamard_residual(
                        subset,
                        pin,
                        numerators,
                        determinants,
                        cramer_vectors,
                    )
                    == 0
                )
            assert (
                euler_residual(
                    subset, numerators, determinants, cramer_vectors
                )
                == 0
            )

    wrong_beta_residuals = [
        four_realization_residual(
            subset, beta + 1, numerators, determinants, cramer_vectors
        )
        for subset in combinations(range(9), 4)
    ]
    assert any(residual != 0 for residual in wrong_beta_residuals)


def verify_low_degree_detection() -> None:
    beta = sp.Integer(7)
    numerators = numerator_decks(beta)
    determinants, cramer_vectors = all_pinned_data(numerators, range(8))

    other_vertices = tuple(range(1, 9))
    unselected_five_set = list(combinations(other_vertices, 5))[5]
    perturbed_six_set = tuple(sorted((0, *unselected_five_set)))
    perturbed_six = dict(numerators)
    perturbed_six[perturbed_six_set] += 1
    new_determinants, new_vectors = all_pinned_data(perturbed_six, range(8))
    assert new_determinants[0] == determinants[0]
    assert new_vectors[0] == cramer_vectors[0]
    assert (
        hadamard_residual(
            perturbed_six_set,
            0,
            perturbed_six,
            new_determinants,
            new_vectors,
        )
        == determinants[0]
    )

    perturbed_eight = dict(numerators)
    eight_set = tuple(range(8))
    perturbed_eight[eight_set] += 1
    assert (
        hadamard_residual(
            eight_set,
            0,
            perturbed_eight,
            determinants,
            cramer_vectors,
        )
        == determinants[0]
    )


def main() -> None:
    verify_target_incidence_cramer_identity()
    print("PASS: determinant-cleared target-incidence Cramer identity")
    verify_integrability_hierarchy()
    print("PASS: all fixed four/hadamard/euler/h8 integrability identities")
    verify_low_degree_detection()
    print("PASS: degree-nine residual detects unselected h6 and h8 perturbations")
    print("SCOPE: companion data are relative; GHZ forcing remains UNKNOWN")
    print("searches=0 eliminations=0 project_imports=0 finite_fields=0")


if __name__ == "__main__":
    main()
