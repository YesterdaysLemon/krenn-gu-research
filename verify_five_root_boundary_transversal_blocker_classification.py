#!/usr/bin/env python3
"""Replay the tangent-space and blocker calculations in the boundary theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp

VERTICES = tuple(range(5))
EDGES = tuple(itertools.combinations(VERTICES, 2))


def cyclic_regular_tournament() -> dict[tuple[int, int], int]:
    """Orient i--j toward j exactly when j-i is 1 or 2 modulo five."""
    heads: dict[tuple[int, int], int] = {}
    for i, j in EDGES:
        heads[i, j] = j if (j - i) % 5 in (1, 2) else i
    assert all(sum(head == i for head in heads.values()) == 2 for i in VERTICES)
    return heads


def tangent_matrix(
    endpoint_gradients: dict[tuple[tuple[int, int], int], tuple[int, int]],
) -> sp.Matrix:
    rows = []
    for edge in EDGES:
        row = [0] * 10
        for vertex in edge:
            gradient = endpoint_gradients[edge, vertex]
            row[2 * vertex] = gradient[0]
            row[2 * vertex + 1] = gradient[1]
        rows.append(row)
    return sp.Matrix(rows)


def chart_jacobian(
    endpoint_gradients: dict[tuple[tuple[int, int], int], tuple[int, int]],
) -> sp.Matrix:
    """Realize the endpoint data by bilinear blocks on affine P^2 charts."""
    chart_variables = sp.symbols("s0 t0 s1 t1 s2 t2 s3 t3 s4 t4")
    chart_vectors = [
        sp.Matrix([chart_variables[2 * vertex], chart_variables[2 * vertex + 1], 1])
        for vertex in VERTICES
    ]
    equations = []
    origin = {variable: 0 for variable in chart_variables}
    for left, right in EDGES:
        block = sp.zeros(3, 3)
        left_gradient = endpoint_gradients[(left, right), left]
        right_gradient = endpoint_gradients[(left, right), right]
        block[0, 2], block[1, 2] = left_gradient
        block[2, 0], block[2, 1] = right_gradient
        # The bottom-right entry is zero, so ([e_2],...,[e_2]) is a
        # common projective zero.  The other four entries are immaterial.
        assert block[2, 2] == 0
        equation = (chart_vectors[left].T * block * chart_vectors[right])[0]
        assert equation.subs(origin) == 0
        equations.append(equation)
    return sp.Matrix(equations).jacobian(chart_variables).subs(origin)


def transverse_model() -> tuple[sp.Matrix, dict]:
    heads = cyclic_regular_tournament()
    incoming = {
        vertex: sorted(edge for edge, head in heads.items() if head == vertex)
        for vertex in VERTICES
    }
    gradients = {}
    for edge in EDGES:
        for vertex in edge:
            if heads[edge] != vertex:
                gradients[edge, vertex] = (0, 0)
            else:
                slot = incoming[vertex].index(edge)
                gradients[edge, vertex] = (1, 0) if slot == 0 else (0, 1)
    matrix = tangent_matrix(gradients)
    affine_chart_matrix = chart_jacobian(gradients)
    assert affine_chart_matrix == matrix
    assert matrix.rank() == 10
    assert abs(int(matrix.det())) == 1
    for vertex in VERTICES:
        local = sp.Matrix(
            [gradients[edge, vertex] for edge in EDGES if vertex in edge]
        )
        assert local.rank() == 2
    return matrix, gradients


def check_supported_tangent_kernel(base_gradients: dict) -> None:
    for vertex in VERTICES:
        gradients = dict(base_gradients)
        coefficient = 1
        for edge in EDGES:
            if vertex in edge:
                gradients[edge, vertex] = (coefficient, 0)
                coefficient += 1
        matrix = tangent_matrix(gradients)
        assert chart_jacobian(gradients) == matrix
        tangent = sp.zeros(10, 1)
        tangent[2 * vertex + 1, 0] = 1
        assert tangent != sp.zeros(10, 1)
        assert matrix * tangent == sp.zeros(10, 1)
        assert matrix.rank() <= 9


def in_row_span(matrix: sp.Matrix, vector: sp.Matrix) -> bool:
    return matrix.rank() == matrix.col_join(vector.T).rank()


def check_coordinate_annihilators() -> list[dict]:
    records = []
    for mask in range(1, 1 << 3):
        x = sp.Matrix([1 if mask & (1 << colour) else 0 for colour in range(3)])
        basis_columns = x.T.nullspace()
        annihilator = sp.Matrix.hstack(*basis_columns).T
        assert annihilator.rank() == 2
        blockers = []
        for colour in range(3):
            coordinate = sp.zeros(3, 1)
            coordinate[colour, 0] = 1
            membership = in_row_span(annihilator, coordinate)
            assert membership == (x[colour, 0] == 0)
            if membership:
                blockers.append(colour)
        records.append(
            {
                "support": [i for i in range(3) if x[i, 0] != 0],
                "internal_blocker_type": blockers,
            }
        )
    return records


def main() -> None:
    matrix, gradients = transverse_model()
    check_supported_tangent_kernel(gradients)
    support_records = check_coordinate_annihilators()

    print(
        json.dumps(
            {
                "verified": True,
                "ambient_tangent_dimension": 10,
                "equations": len(EDGES),
                "transverse_model_rank": matrix.rank(),
                "transverse_model_determinant": int(matrix.det()),
                "rank_one_local_span_tests": len(VERTICES),
                "projective_coordinate_support_types": support_records,
                "conclusion": (
                    "at a transverse five-root zero, each internal covector "
                    "span equals x_i^perp and its coordinate blocker type "
                    "equals the zero-coordinate set of x_i"
                ),
                "coordinate_boundary_excluded": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
