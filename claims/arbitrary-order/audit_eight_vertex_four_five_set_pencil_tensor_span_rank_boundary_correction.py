#!/usr/bin/env python3
"""Independent modular audit of the tensor-span-rank boundary correction.

This audit does not import the SymPy verifier.  It rebuilds the evaluation
spans, coefficient nullspaces, and incidence Jacobian over one large prime.
Nonzero ranks modulo the prime corroborate the exact characteristic-zero
calculation; the audit is deliberately labelled modular rather than exact.
"""

from __future__ import annotations

import json
from itertools import combinations

PRIME = 1_000_003
COMMON = tuple(range(4))
SELECTOR = (0, 0, 1)
X2 = ((1, 2, 1), (2, 1, 1), (3, 4, 1), (5, 1, 1))
X3 = ((2, 1, 1), (1, 3, 1), (4, 2, 1), (3, 5, 1))
OUTER = ((1, 2, 1), (2, 3, 1), (3, 1, 1), (4, 2, 1))
ROOTS = tuple(
    (
        (0, 0, 1),
        (1, chart + 1, 0),
        X2[chart],
        X3[chart],
        OUTER[chart],
    )
    for chart in range(4)
)
COMMON_EDGES = tuple(
    ("common", left, right) for left, right in combinations(COMMON, 2)
)
OUTER_EDGES = tuple(
    ("outer", common, chart)
    for common in COMMON
    for chart in range(4)
)
EDGES = COMMON_EDGES + OUTER_EDGES


def mod_rank(matrix: list[list[int]]) -> int:
    rows = [[value % PRIME for value in row] for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    pivot_row = 0
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], PRIME - 2, PRIME)
        rows[pivot_row] = [value * inverse % PRIME for value in rows[pivot_row]]
        for row in range(height):
            if row != pivot_row and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(rows[row], rows[pivot_row])
                ]
        pivot_row += 1
        rank += 1
        if pivot_row == height:
            break
    return rank


def reduced_rows(matrix: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    rows = [[value % PRIME for value in row] for row in matrix]
    height = len(rows)
    width = len(rows[0]) if rows else 0
    pivots: list[int] = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], PRIME - 2, PRIME)
        rows[pivot_row] = [value * inverse % PRIME for value in rows[pivot_row]]
        for row in range(height):
            if row != pivot_row and rows[row][column]:
                factor = rows[row][column]
                rows[row] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(rows[row], rows[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == height:
            break
    return rows, pivots


def nullspace(matrix: list[list[int]]) -> list[list[int]]:
    reduced, pivots = reduced_rows(matrix)
    width = len(matrix[0])
    free_columns = [column for column in range(width) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free] % PRIME
        basis.append(vector)
    return basis


def tensor_vector(left: tuple[int, ...], right: tuple[int, ...]) -> list[int]:
    return [left[row] * right[column] % PRIME for row in range(3) for column in range(3)]


def edge_evaluations(edge: tuple[str, int, int]) -> list[list[int]]:
    kind, left, right = edge
    if kind == "common":
        return [tensor_vector(ROOTS[chart][left], ROOTS[chart][right]) for chart in range(4)]
    return [tensor_vector(ROOTS[right][left], ROOTS[right][4])]


def coefficient_forms() -> dict[tuple[str, int, int], tuple[list[int], int]]:
    forms = {}
    for edge in EDGES:
        constraint = edge_evaluations(edge)
        basis = nullspace(constraint)
        candidate = [0] * 9
        for index, vector in enumerate(basis):
            for column, value in enumerate(vector):
                candidate[column] = (candidate[column] + (index + 1) * value) % PRIME
        gauge = next(index for index, value in enumerate(candidate) if value)
        inverse = pow(candidate[gauge], PRIME - 2, PRIME)
        candidate = [value * inverse % PRIME for value in candidate]
        assert all(
            sum(left * right for left, right in zip(row, candidate)) % PRIME == 0
            for row in constraint
        )
        forms[edge] = (candidate, gauge)
    return forms


def parameter_derivatives() -> list[tuple[int, int, tuple[int, int, int]]]:
    result = []
    for chart in range(4):
        result.extend(
            (
                (1, chart, (0, 1, 0)),
                (2, chart, (1, 0, 0)),
                (2, chart, (0, 1, 0)),
                (3, chart, (1, 0, 0)),
                (3, chart, (0, 1, 0)),
                (4, chart, (1, 0, 0)),
                (4, chart, (0, 1, 0)),
            )
        )
    return result


def bilinear_derivative(
    direction: tuple[int, int, int], form: list[int], other: tuple[int, ...]
) -> int:
    return sum(
        direction[row] * form[3 * row + column] * other[column]
        for row in range(3)
        for column in range(3)
    ) % PRIME


def right_bilinear_derivative(
    left: tuple[int, ...], form: list[int], direction: tuple[int, int, int]
) -> int:
    return sum(
        left[row] * form[3 * row + column] * direction[column]
        for row in range(3)
        for column in range(3)
    ) % PRIME


def incidence_jacobians(
    forms: dict[tuple[str, int, int], tuple[list[int], int]]
) -> tuple[list[list[int]], list[list[int]]]:
    derivatives = parameter_derivatives()
    root_jacobian = [[0] * 28 for _ in range(40)]
    full_jacobian = [[0] * 204 for _ in range(40)]
    row = 0
    for edge_index, edge in enumerate(EDGES):
        kind, left, right = edge
        form, gauge = forms[edge]
        coefficient_columns = [
            (row_index, column_index)
            for row_index in range(3)
            for column_index in range(3)
            if 3 * row_index + column_index != gauge
        ]
        coefficient_offset = 28 + 8 * edge_index
        if kind == "common":
            for chart in range(4):
                left_root = ROOTS[chart][left]
                right_root = ROOTS[chart][right]
                for column, (vertex, source_chart, direction) in enumerate(derivatives):
                    if source_chart == chart and vertex == left:
                        value = bilinear_derivative(direction, form, right_root)
                    elif source_chart == chart and vertex == right:
                        value = right_bilinear_derivative(left_root, form, direction)
                    else:
                        continue
                    root_jacobian[row][column] = value
                    full_jacobian[row][column] = value
                for column, (row_index, column_index) in enumerate(coefficient_columns):
                    full_jacobian[row][coefficient_offset + column] = (
                        left_root[row_index] * right_root[column_index] % PRIME
                    )
                row += 1
        else:
            chart = right
            left_root = ROOTS[chart][left]
            outer_root = ROOTS[chart][4]
            for column, (vertex, source_chart, direction) in enumerate(derivatives):
                if source_chart == chart and vertex == left:
                    value = bilinear_derivative(direction, form, outer_root)
                elif source_chart == chart and vertex == 4:
                    value = right_bilinear_derivative(left_root, form, direction)
                else:
                    continue
                root_jacobian[row][column] = value
                full_jacobian[row][column] = value
            for column, (row_index, column_index) in enumerate(coefficient_columns):
                full_jacobian[row][coefficient_offset + column] = (
                    left_root[row_index] * outer_root[column_index] % PRIME
                )
            row += 1
    assert row == 40
    return root_jacobian, full_jacobian


def verify_fixture() -> dict[str, object]:
    for chart in range(4):
        for colour, vertex in enumerate(SELECTOR):
            assert ROOTS[chart][vertex][colour] == 0
    for vertex in (1, 2, 3):
        assert all(
            mod_rank(
                [
                    [ROOTS[left][vertex][coordinate] for coordinate in range(3)],
                    [ROOTS[right][vertex][coordinate] for coordinate in range(3)],
                ]
            )
            == 2
            for left, right in combinations(range(4), 2)
        )

    span_ranks = tuple(mod_rank(edge_evaluations(edge)) for edge in EDGES)
    assert span_ranks == (2, 3, 3, 4, 4, 4) + (1,) * 16

    partitions = ((0, 0, 0, 0), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3))
    pair_cardinalities = tuple(
        len({(partitions[left][chart], partitions[right][chart]) for chart in range(4)})
        for left, right in combinations(range(4), 2)
    )
    assert pair_cardinalities == (4,) * 6

    forms = coefficient_forms()
    root_jacobian, full_jacobian = incidence_jacobians(forms)
    assert mod_rank(root_jacobian) == 28
    assert mod_rank(full_jacobian) == 36

    projective_dimension = 28 + 22 * 8 - 36
    affine_dimension = 28 + 22 * 9 - 36 + 6 * 9
    assert projective_dimension == 168
    assert affine_dimension == 244
    return {
        "status": "independent_modular_audit_of_tensor_span_rank_boundary",
        "prime": PRIME,
        "selector": SELECTOR,
        "common_partition_system": ["0123", "0|1|2|3", "0|1|2|3", "0|1|2|3"],
        "common_span_ranks": span_ranks[:6],
        "partition_pair_cardinalities": pair_cardinalities,
        "total_evaluation_rank_mod_prime": sum(span_ranks),
        "root_dimension": 28,
        "projective_incidence_dimension": projective_dimension,
        "affine_incidence_dimension": affine_dimension,
        "projective_incidence_jacobian_rank_mod_prime": mod_rank(full_jacobian),
        "root_only_jacobian_rank_mod_prime": mod_rank(root_jacobian),
        "whole_zero_blocks_discarded": False,
        "is_krenn_gu_counterexample": False,
    }


def main() -> None:
    result = verify_fixture()
    print("independent modular tensor-span-rank boundary audit: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
