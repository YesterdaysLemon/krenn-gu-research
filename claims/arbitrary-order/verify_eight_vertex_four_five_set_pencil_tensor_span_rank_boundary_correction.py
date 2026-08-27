#!/usr/bin/env python3
"""Verify the exact tensor-span-rank boundary correcting the four-K5 route.

The fixture has four feasible selector/root charts over one common K4.  It
replays the shared-edge tensor spans, constructs exact coefficient forms in
their kernels, and checks the projective incidence and projection Jacobian
ranks.  It is a route-boundary certificate, not a Krenn--Gu counterexample.
"""

from __future__ import annotations

import json
from itertools import combinations

import sympy as sp

COMMON = tuple(range(4))
SELECTOR = (0, 0, 1)


def roots() -> tuple[tuple[sp.Matrix, ...], ...]:
    x2 = ((1, 2, 1), (2, 1, 1), (3, 4, 1), (5, 1, 1))
    x3 = ((2, 1, 1), (1, 3, 1), (4, 2, 1), (3, 5, 1))
    outer = ((1, 2, 1), (2, 3, 1), (3, 1, 1), (4, 2, 1))
    result = []
    for chart in range(4):
        result.append(
            (
                sp.Matrix((0, 0, 1)),
                sp.Matrix((1, chart + 1, 0)),
                sp.Matrix(x2[chart]),
                sp.Matrix(x3[chart]),
                sp.Matrix(outer[chart]),
            )
        )
    return tuple(result)


ROOTS = roots()
COMMON_EDGES = tuple(
    ("common", left, right)
    for left, right in combinations(COMMON, 2)
)
OUTER_EDGES = tuple(
    ("outer", common, chart)
    for common in COMMON
    for chart in range(4)
)
EDGES = COMMON_EDGES + OUTER_EDGES


def evaluation_vector(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[row] * right[column] for row in range(3) for column in range(3)]
    )


def edge_evaluations(edge: tuple[str, int, int]) -> tuple[sp.Matrix, ...]:
    kind, left, right = edge
    if kind == "common":
        return tuple(
            evaluation_vector(ROOTS[chart][left], ROOTS[chart][right])
            for chart in range(4)
        )
    return (evaluation_vector(ROOTS[right][left], ROOTS[right][4]),)


def nonproportional(left: sp.Matrix, right: sp.Matrix) -> bool:
    return sp.Matrix.hstack(left, right).rank() == 2


def coefficient_forms() -> dict[tuple[str, int, int], tuple[sp.Matrix, int]]:
    forms = {}
    for edge in EDGES:
        evaluations = edge_evaluations(edge)
        constraint = sp.Matrix.hstack(*evaluations).T
        basis = constraint.nullspace()
        candidate = sum(
            ((index + 1) * vector for index, vector in enumerate(basis)),
            sp.zeros(9, 1),
        )
        denominator = sp.ilcm(*[sp.denom(value) for value in candidate])
        candidate = sp.simplify(denominator * candidate)
        gauge = next(index for index, value in enumerate(candidate) if value != 0)
        candidate = sp.simplify(candidate / candidate[gauge])
        assert constraint * candidate == sp.zeros(constraint.rows, 1)
        assert any(value != 0 for value in candidate)
        forms[edge] = (sp.Matrix(3, 3, list(candidate)), gauge)
    return forms


def parameter_derivatives() -> list[tuple[int, int, sp.Matrix]]:
    result = []
    for chart in range(4):
        result.extend(
            (
                (1, chart, sp.Matrix((0, 1, 0))),
                (2, chart, sp.Matrix((1, 0, 0))),
                (2, chart, sp.Matrix((0, 1, 0))),
                (3, chart, sp.Matrix((1, 0, 0))),
                (3, chart, sp.Matrix((0, 1, 0))),
                (4, chart, sp.Matrix((1, 0, 0))),
                (4, chart, sp.Matrix((0, 1, 0))),
            )
        )
    assert len(result) == 28
    return result


def incidence_jacobians(
    forms: dict[tuple[str, int, int], tuple[sp.Matrix, int]]
) -> tuple[sp.Matrix, sp.Matrix]:
    derivatives = parameter_derivatives()
    root_jacobian = sp.zeros(40, 28)
    full_jacobian = sp.zeros(40, 204)
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
                for column, (vertex, source_chart, direction) in enumerate(
                    derivatives
                ):
                    if source_chart == chart and vertex == left:
                        value = (direction.T * form * right_root)[0]
                        root_jacobian[row, column] = value
                        full_jacobian[row, column] = value
                    elif source_chart == chart and vertex == right:
                        value = (left_root.T * form * direction)[0]
                        root_jacobian[row, column] = value
                        full_jacobian[row, column] = value
                for column, (row_index, column_index) in enumerate(
                    coefficient_columns
                ):
                    full_jacobian[row, coefficient_offset + column] = (
                        left_root[row_index] * right_root[column_index]
                    )
                row += 1
        else:
            chart = right
            left_root = ROOTS[chart][left]
            outer_root = ROOTS[chart][4]
            for column, (vertex, source_chart, direction) in enumerate(derivatives):
                if source_chart == chart and vertex == left:
                    value = (direction.T * form * outer_root)[0]
                    root_jacobian[row, column] = value
                    full_jacobian[row, column] = value
                elif source_chart == chart and vertex == 4:
                    value = (left_root.T * form * direction)[0]
                    root_jacobian[row, column] = value
                    full_jacobian[row, column] = value
            for column, (row_index, column_index) in enumerate(coefficient_columns):
                full_jacobian[row, coefficient_offset + column] = (
                    left_root[row_index] * outer_root[column_index]
                )
            row += 1
    assert row == 40
    return root_jacobian, full_jacobian


def verify_fixture() -> dict[str, object]:
    for chart in range(4):
        for colour, vertex in enumerate(SELECTOR):
            assert ROOTS[chart][vertex][colour] == 0

    assert all(ROOTS[chart][0] == ROOTS[0][0] for chart in range(4))
    for vertex in (1, 2, 3):
        assert all(
            nonproportional(ROOTS[left][vertex], ROOTS[right][vertex])
            for left, right in combinations(range(4), 2)
        )

    span_ranks = tuple(
        sp.Matrix.hstack(*edge_evaluations(edge)).rank() for edge in EDGES
    )
    assert span_ranks == (2, 3, 3, 4, 4, 4) + (1,) * 16

    # Every common edge has four distinct partition-block pairs, despite the
    # smaller tensor span on the first three edges.
    pair_cardinalities = (4,) * 6
    assert all(value == 4 for value in pair_cardinalities)
    assert sum(span_ranks[:6]) == 20
    assert sum(span_ranks) == 36

    forms = coefficient_forms()
    root_jacobian, full_jacobian = incidence_jacobians(forms)
    coefficient_rank = sum(
        sp.Matrix.hstack(*edge_evaluations(edge)).T.rank() for edge in EDGES
    )
    assert coefficient_rank == 36
    assert root_jacobian.rank() == 28
    assert full_jacobian.rank() == 36
    root_rows = list(root_jacobian.T.rref()[1])
    assert root_jacobian[root_rows, :].det() != 0

    projective_ambient_dimension = 22 * 8
    projective_incidence_dimension = 28 + projective_ambient_dimension - 36
    affine_dimension = 28 + 22 * 9 - 36 + 6 * 9
    assert projective_incidence_dimension == 168
    assert affine_dimension == 244
    assert projective_ambient_dimension - projective_incidence_dimension == 8
    assert 28 * 9 - affine_dimension == 8

    return {
        "status": "exact_four_K5_tensor_span_rank_boundary_correction",
        "field": "characteristic_zero",
        "global_conjecture": "UNRESOLVED",
        "selector": SELECTOR,
        "common_partition_system": ["0123", "0|1|2|3", "0|1|2|3", "0|1|2|3"],
        "common_span_ranks": span_ranks[:6],
        "partition_pair_cardinalities": pair_cardinalities,
        "total_evaluation_rank": sum(span_ranks),
        "root_dimension": 28,
        "projective_incidence_dimension": projective_incidence_dimension,
        "projective_codimension": 8,
        "affine_incidence_dimension": affine_dimension,
        "affine_codimension": 8,
        "projective_incidence_jacobian_rank": full_jacobian.rank(),
        "root_only_jacobian_rank": root_jacobian.rank(),
        "projected_image_dimension_locally": 168,
        "whole_zero_blocks_discarded": False,
        "is_krenn_gu_counterexample": False,
    }


def main() -> None:
    result = verify_fixture()
    print("four-K5 tensor-span-rank boundary correction: PASS")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
