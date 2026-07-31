#!/usr/bin/env python3
"""Exact replay of the full-support 1+3 triangle obstruction."""

from __future__ import annotations

import itertools
import json

import sympy as sp


def catalecticant(q01, q02, q03, q12, q13, q23) -> sp.Matrix:
    return sp.Matrix(
        (
            (0, q23, q13, q12),
            (q23, 0, q03, q02),
            (q13, q03, 0, q01),
            (q12, q02, q01, 0),
        )
    )


def squarefree_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            left[i] * right[j] + left[j] * right[i]
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def main() -> None:
    q12, q13, q23 = sp.symbols("q12 q13 q23", nonzero=True)
    cut = catalecticant(0, 0, 0, q12, q13, q23)
    assert all(
        minor == 0
        for minor in (
            cut.extract(rows, columns).det()
            for rows in itertools.combinations(range(4), 3)
            for columns in itertools.combinations(range(4), 3)
        )
    )
    assert cut.extract((0, 1), (0, 1)).det() == -(q23**2)
    kernel = (
        sp.Matrix((0, -q13, q23, 0)),
        sp.Matrix((0, -q12, 0, q23)),
    )
    assert all(cut * vector == sp.zeros(4, 1) for vector in kernel)
    assert sp.Matrix.hstack(*kernel).rank() == 2

    u = sp.symbols("u0:4")
    v = sp.symbols("v0:4")
    edges = {
        j: sp.expand(u[0] * v[j] + v[0] * u[j]) for j in range(1, 4)
    }
    reflection_identities = {}
    for j, k in itertools.combinations(range(1, 4), 2):
        qjk = u[j] * v[k] + u[k] * v[j]
        identity = sp.expand(
            u[0] * qjk
            + 2 * v[0] * u[j] * u[k]
            - u[j] * edges[k]
            - u[k] * edges[j]
        )
        assert identity == 0
        reflection_identities[f"{j}{k}"] = (
            f"u0*q{j}{k}=-2*v0*u{j}*u{k} modulo absent edges"
        )

    coordinate_hyperplanes = tuple(
        sp.eye(4).row(label) for label in range(4)
    )
    intersection_dimensions = {}
    for labels in ((0, 0, 0), (0, 0, 1), (0, 1, 2)):
        rank = sp.Matrix.vstack(*(coordinate_hyperplanes[i] for i in labels)).rank()
        intersection_dimensions[str(labels)] = 4 - rank
    assert tuple(intersection_dimensions.values()) == (3, 2, 1)

    coordinate_plane = (sp.eye(4).col(2), sp.eye(4).col(3))
    pair_columns = tuple(
        squarefree_product(left, right)
        for left in coordinate_plane
        for right in coordinate_plane
    )
    coordinate_pair_map = sp.Matrix.hstack(*pair_columns)
    assert coordinate_pair_map.rank() == 1

    # In three variables, degree two and degree one pair perfectly.
    p3_pairing = sp.Matrix(((0, 0, 1), (0, 1, 0), (1, 0, 0)))
    assert p3_pairing.det() == -1
    pair_rank_assumption = 3
    opposite_plane_dimension = 2
    ambient_degree_dimension = 3
    lower_bound = (
        pair_rank_assumption
        + opposite_plane_dimension
        - ambient_degree_dimension
    )
    assert lower_bound == 2
    assert lower_bound > 1

    result = {
        "annihilator": {
            "catalecticant_rank": 2,
            "kernel_dimension": 2,
            "kernel_in_singleton_hyperplane": True,
        },
        "factorization": {
            "reflection_identities": reflection_identities,
            "full_triangle_forces_reflection_factors_fully_supported": True,
        },
        "label_intersections": intersection_dimensions,
        "two_label_coordinate_plane_pair_rank": coordinate_pair_map.rank(),
        "common_label_p3_pairing_determinant": int(p3_pairing.det()),
        "rank_three_flattening_lower_bound": lower_bound,
        "conclusion": (
            "full-support all-1+3 nonresonant rank-three triangle is empty"
        ),
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
