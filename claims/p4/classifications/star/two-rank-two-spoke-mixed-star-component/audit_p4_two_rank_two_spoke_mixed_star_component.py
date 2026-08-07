#!/usr/bin/env python3
"""Crossed-coordinate exact audit of the two-rank-two-spoke component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))
SOURCE_PERMUTATION = (1, 0, 3, 2)


def permanent_dp(rows: list[sp.Matrix]) -> sp.Expr:
    values: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row_index, row in enumerate(rows):
        next_values: dict[int, sp.Expr] = {}
        for mask, value in values.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_values[new_mask] = next_values.get(new_mask, 0) + value * row[column]
        values = next_values
    return sp.expand(values[15])


def squarefree_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    entries = []
    for i in range(4):
        for j in range(i + 1, 4):
            entries.append(sp.expand(left[i] * right[j] + left[j] * right[i]))
    return sp.Matrix(entries)


def crossed_family(s: sp.Expr, t: sp.Expr) -> list[sp.Matrix]:
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    total = s + t
    original = [
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
    return [plane[:, SOURCE_PERMUTATION] for plane in original]


def pair_rank(left: sp.Matrix, right: sp.Matrix) -> int:
    matrix = sp.Matrix.hstack(
        *(
            squarefree_product(left.row(i).T, right.row(j).T)
            for i in range(2)
            for j in range(2)
        )
    )
    return matrix.rank()


def chart_13(plane: sp.Matrix) -> sp.Matrix:
    reduced = plane[:, (1, 3)].inv() * plane
    return sp.Matrix((reduced[0, 0], reduced[0, 2], reduced[1, 0], reduced[1, 2]))


def universal_chart_planes(variables: tuple[sp.Symbol, ...]) -> list[tuple[sp.Matrix, sp.Matrix]]:
    planes = []
    for mode in range(4):
        a, b, c, d = variables[4 * mode : 4 * mode + 4]
        planes.append((sp.Matrix((a, 1, b, 0)), sp.Matrix((c, 0, d, 1))))
    return planes


def main() -> None:
    s, t = sp.symbols("S T")
    planes = crossed_family(s, t)
    coefficients = {
        bits: sp.factor(
            permanent_dp([planes[mode].row(bits[mode]) for mode in range(4)])
        )
        for bits in BITS
    }
    assert sp.factor(coefficients[(1, 1, 1, 1)] + 4 * (s + t)) == 0
    assert sum(value != 0 for value in coefficients.values()) == 1

    sample = [plane.subs({s: 2, t: 3}) for plane in planes]
    ranks = [pair_rank(sample[i], sample[j]) for i, j in itertools.combinations(range(4), 2)]
    assert ranks == [3, 3, 3, 4, 4, 4]

    q0, q1, q2 = sp.symbols("Q0 Q1 Q2")
    # The crossed source order sends diag(q0,q1,q2,1) to this diagonal.
    torus = sp.diag(q1, q0, 1, q2)
    coordinates = sp.Matrix.vstack(*(chart_13(plane * torus) for plane in planes))
    point = {s: 2, t: 3, q0: 1, q1: 1, q2: 1}
    family_jacobian = coordinates.jacobian((s, t, q0, q1, q2)).subs(point)
    assert family_jacobian.rank() == 5

    variables = sp.symbols("b0:16")
    targets = sp.symbols("w0:4")
    universal = universal_chart_planes(variables)
    tensor = {
        bits: permanent_dp([universal[mode][bits[mode]] for mode in range(4)])
        for bits in BITS
    }
    chart_point = list(coordinates.subs(point))
    substitution = dict(zip(variables, chart_point))
    values = {bits: sp.factor(value.subs(substitution)) for bits, value in tensor.items()}
    anchor = next(bits for bits in BITS if values[bits] != 0)
    target_point = []
    for mode in range(4):
        flipped = list(anchor)
        flipped[mode] = 1 - flipped[mode]
        target_point.append(sp.factor(values[tuple(flipped)] / values[anchor]))

    equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        monomial = sp.Integer(1)
        for mode in range(4):
            if bits[mode] != anchor[mode]:
                monomial *= targets[mode]
        equations.append(sp.expand(tensor[bits] - tensor[anchor] * monomial))
    substitution.update(dict(zip(targets, target_point)))
    jacobian = sp.Matrix(equations).jacobian(variables + targets).subs(substitution)
    assert jacobian.rank() == 15
    pivot_columns = jacobian.rref()[1]
    determinant = sp.factor(jacobian[:, pivot_columns].det())
    assert determinant != 0

    result = {
        "audit_source_order": [1, 0, 3, 2],
        "family_tangent_rank": family_jacobian.rank(),
        "incidence_pivot_determinant": str(determinant),
        "incidence_rank": jacobian.rank(),
        "independent_permanent": "subset dynamic programming",
        "pair_profile": ranks,
        "search_used": False,
        "verified": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
