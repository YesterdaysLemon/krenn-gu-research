#!/usr/bin/env python3
"""Exact certificate for the two-rank-two-spoke mixed-star component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.expand(left[i] * right[j] + left[j] * right[i])
            for i, j in itertools.combinations(range(4), 2)
        ]
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            product(left.row(i).T, right.row(j).T)
            for i in range(2)
            for j in range(2)
        )
    )


def family(s: sp.Expr, t: sp.Expr) -> list[sp.Matrix]:
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    total = s + t
    return [
        sp.Matrix.vstack((a + b).T, b.T),
        sp.Matrix.vstack((a + b - b_bar - s * a_bar).T, (b - s * a_bar).T),
        sp.Matrix.vstack((a + b + b_bar - t * a_bar).T, (b - t * a_bar).T),
        sp.Matrix.vstack(
            b_bar.T,
            sp.Matrix(
                (total - 1 - s * t, total + 1 + s * t, -total, -total)
            ).T,
        ),
    ]


def chart_02(plane: sp.Matrix) -> sp.Matrix:
    reduced = sp.simplify(plane[:, (0, 2)].inv() * plane)
    return sp.Matrix((reduced[0, 1], reduced[0, 3], reduced[1, 1], reduced[1, 3]))


def chart_planes(variables: tuple[sp.Symbol, ...]) -> list[tuple[sp.Matrix, sp.Matrix]]:
    planes = []
    for mode in range(4):
        a, b, c, d = variables[4 * mode : 4 * mode + 4]
        planes.append((sp.Matrix((1, a, 0, b)), sp.Matrix((0, c, 1, d))))
    return planes


def main() -> None:
    s, t = sp.symbols("s t")
    planes = family(s, t)

    coefficients = {
        bits: sp.factor(permanent([planes[mode].row(bits[mode]) for mode in range(4)]))
        for bits in BITS
    }
    assert sp.factor(coefficients[(1, 1, 1, 1)] + 4 * (s + t)) == 0
    assert all(
        value == 0 for bits, value in coefficients.items() if bits != (1, 1, 1, 1)
    )

    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]])
        for edge in itertools.combinations(range(4), 2)
    }
    alternating = sp.Matrix((0, -1, 1, 0))
    rank_one = sp.Matrix((0, 0, 1, 0))
    assert pair_matrices[(0, 1)] * alternating == sp.zeros(6, 1)
    assert pair_matrices[(0, 2)] * alternating == sp.zeros(6, 1)
    assert pair_matrices[(0, 3)] * rank_one == sp.zeros(6, 1)
    assert sp.Matrix(2, 2, list(alternating)).rank() == 2
    assert sp.Matrix(2, 2, list(rank_one)).rank() == 1

    assert sp.factor(
        pair_matrices[(0, 1)].extract((0, 1, 3), (0, 1, 3)).det() - 4 * s
    ) == 0
    assert sp.factor(
        pair_matrices[(0, 2)].extract((0, 1, 3), (0, 1, 3)).det() - 4 * t
    ) == 0
    assert sp.factor(
        pair_matrices[(0, 3)].extract((0, 1, 2), (0, 1, 3)).det()
        - 4 * (s - 1) * (s + t) * (t - 1)
    ) == 0

    leaf_minors = {
        edge: sp.factor(matrix.extract((0, 1, 2, 3), range(4)).det())
        for edge, matrix in pair_matrices.items()
        if edge in ((1, 2), (1, 3), (2, 3))
    }
    assert sp.factor(leaf_minors[(1, 2)] - 8 * (s + t) ** 2) == 0
    assert sp.factor(
        leaf_minors[(1, 3)]
        + 8 * s * (s - 1) * (s + 1) * (s + t) * (t - 1)
    ) == 0
    assert sp.factor(
        leaf_minors[(2, 3)]
        + 8 * t * (s - 1) * (s + t) * (t - 1) * (t + 1)
    ) == 0

    cayley_s = (s - 1) / (s + 1)
    cayley_t = (t - 1) / (t + 1)
    d = (1 + s * t) / (s + t)
    assert sp.factor((d - 1) / (d + 1) - cayley_s * cayley_t) == 0

    # Five-dimensional family tangent: two chart parameters plus the
    # projective diagonal source torus.
    q0, q1, q2 = sp.symbols("q0 q1 q2")
    torus = sp.diag(q0, q1, q2, 1)
    chart_coordinates = sp.Matrix.vstack(*(chart_02(plane * torus) for plane in planes))
    family_point = {s: 2, t: 3, q0: 1, q1: 1, q2: 1}
    family_jacobian = chart_coordinates.jacobian((s, t, q0, q1, q2)).subs(
        family_point
    )
    tangent_rows = (0, 3, 4, 5, 8)
    tangent_determinant = sp.factor(
        family_jacobian.extract(tangent_rows, range(5)).det()
    )
    assert tangent_determinant == -sp.Rational(1, 2)

    # Exact smooth incidence certificate in the all-(02) Grassmann chart.
    plane_variables = sp.symbols("a0:16")
    target_variables = sp.symbols("z0:4")
    universal_planes = chart_planes(plane_variables)
    universal_coefficients = {
        bits: permanent(
            [universal_planes[mode][bits[mode]] for mode in range(4)]
        )
        for bits in BITS
    }
    chart_point = list(chart_coordinates.subs(family_point))
    chart_substitution = dict(zip(plane_variables, chart_point))
    coefficient_point = {
        bits: sp.factor(value.subs(chart_substitution))
        for bits, value in universal_coefficients.items()
    }
    anchor = (0, 1, 0, 0)
    assert coefficient_point[anchor] == 5
    target_point = (-1, 0, 1, 0)
    for mode in range(4):
        flipped = list(anchor)
        flipped[mode] = 1 - flipped[mode]
        assert (
            sp.factor(coefficient_point[tuple(flipped)] / coefficient_point[anchor])
            == target_point[mode]
        )

    equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        target_monomial = sp.Integer(1)
        for mode in range(4):
            if bits[mode] != anchor[mode]:
                target_monomial *= target_variables[mode]
        equations.append(
            sp.expand(
                universal_coefficients[bits]
                - universal_coefficients[anchor] * target_monomial
            )
        )

    incidence_substitution = dict(chart_substitution)
    incidence_substitution.update(dict(zip(target_variables, target_point)))
    incidence_jacobian = sp.Matrix(equations).jacobian(
        plane_variables + target_variables
    ).subs(incidence_substitution)
    incidence_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 17, 19)
    incidence_determinant = sp.factor(
        incidence_jacobian[:, incidence_columns].det()
    )
    assert incidence_determinant == 345600000

    result = {
        "component_dimension": 5,
        "exceptional_graph": "star centered at mode 0",
        "exceptional_relation_ranks": [2, 2, 1],
        "family_tangent_determinant": str(tangent_determinant),
        "incidence_determinant": str(incidence_determinant),
        "pair_profile": [3, 3, 3, 4, 4, 4],
        "pure_coefficient": "T_1111=-4*(s+t)",
        "toric_law": "c((1+s*t)/(s+t))=c(s)c(t)",
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
