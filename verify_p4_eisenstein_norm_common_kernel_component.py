#!/usr/bin/env python3
"""Exact certificate for the Eisenstein-norm common-kernel component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2), (0, 1), (1, 0), (0, 1))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(*(product(u, v) for u in left for v in right))


def normalize(plane: sp.Matrix, pivot: tuple[int, int]) -> sp.Matrix:
    return sp.simplify(plane[:, pivot].inv() * plane)


def chart_coordinates(planes: list[sp.Matrix]) -> list[sp.Expr]:
    coordinates: list[sp.Expr] = []
    for plane, pivot in zip(planes, PIVOTS):
        nonpivots = [column for column in range(4) if column not in pivot]
        coordinates.extend(
            sp.factor(plane[row, column])
            for row in range(2)
            for column in nonpivots
        )
    return coordinates


def generic_chart_matrices(symbols: tuple[sp.Symbol, ...]) -> list[sp.Matrix]:
    matrices: list[sp.Matrix] = []
    index = 0
    for pivot in PIVOTS:
        plane = sp.zeros(2, 4)
        for row, column in enumerate(pivot):
            plane[row, column] = 1
        nonpivots = [column for column in range(4) if column not in pivot]
        for row in range(2):
            for column in nonpivots:
                plane[row, column] = symbols[index]
                index += 1
        matrices.append(plane)
    return matrices


def independent_rows(matrix: sp.Matrix) -> tuple[int, ...]:
    return tuple(matrix.T.rref()[1])


def main() -> None:
    alpha, beta, r, gamma = sp.symbols("alpha beta r gamma")
    t0, t1, t2 = sp.symbols("t0 t1 t2", nonzero=True)
    a = sp.Matrix((1, 1, 0, 0))
    c = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))

    norm_equation = sp.expand(
        alpha**2 + alpha * gamma + gamma**2
        - 3 * beta**2 - 3 * beta * r - r**2
    )
    assert sp.factor(norm_equation) == norm_equation
    assert sp.hessian(norm_equation, (alpha, beta, r, gamma)).det() == 9

    m = alpha * a + beta * c + b
    m_r = m + r * c
    d = gamma * a + b
    x0 = b - (alpha + gamma) * a - (2 * beta + r) * c
    planes = (
        (b_bar, x0),
        (m, a),
        (m_r, a),
        (c, d),
    )

    coefficients = {
        bits: sp.factor(permanent([planes[mode][bits[mode]] for mode in range(4)]))
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    assert set(support) == {(1, 0, 0, 1), (1, 1, 1, 1)}
    assert sp.factor(support[(1, 0, 0, 1)] + 4 * norm_equation) == 0
    assert support[(1, 1, 1, 1)] == 4

    # The three kernel-containing cubics reduce to two columns on the norm
    # quadric.  The displayed identity is the apolar compression directly.
    cubic0 = sp.Matrix(
        [-2, 2, -4 * beta - 2 * r, -4 * beta - 2 * r]
    )
    cubic1 = sp.Matrix(
        [
            4 * alpha - 4 * beta + 2 * gamma - 2 * r,
            4 * alpha + 4 * beta + 2 * gamma + 2 * r,
            2 * alpha**2 + 4 * alpha * gamma - 2 * beta**2 - 2 * beta * r,
            2 * alpha**2 + 4 * alpha * gamma - 2 * beta**2 - 2 * beta * r,
        ]
    )
    cubic2 = sp.Matrix([2, 2, 2 * alpha + 2 * gamma, 2 * alpha + 2 * gamma])
    residual = sp.simplify(
        cubic1 - (2 * beta + r) * cubic0 - (2 * alpha + gamma) * cubic2
    )
    assert residual == sp.Matrix([0, 0, -2 * norm_equation, -2 * norm_equation])
    assert b_bar.dot(cubic0) == 0 and b_bar.dot(cubic2) == 0
    assert x0.dot(cubic0) == 0 and x0.dot(cubic2) == 0
    active_cubic = sp.Matrix([0, 0, 2, 2])
    assert b_bar.dot(active_cubic) == 0
    assert x0.dot(active_cubic) == 4

    sample = {
        alpha: 2,
        beta: 1,
        r: 1,
        gamma: 1,
        t0: 1,
        t1: 1,
        t2: 1,
    }
    assert norm_equation.subs(sample) == 0
    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]]) for edge in PAIRS
    }
    pair_profile = [pair_matrices[edge].subs(sample).rank() for edge in PAIRS]
    assert pair_profile == [4, 4, 4, 3, 3, 3]
    relation_ranks: list[int] = []
    for edge in ((1, 2), (1, 3), (2, 3)):
        kernel = pair_matrices[edge].subs(sample).nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert relation_ranks == [2, 1, 1]

    # Restore the projective diagonal source torus.  The norm quadric has
    # tangent directions alpha,beta,r with gamma determined implicitly.
    diagonal = sp.diag(t0, t1, t2, 1)
    raw_matrices = [sp.Matrix.vstack(*[row.T for row in plane]) for plane in planes]
    normalized = [
        normalize(matrix * diagonal, pivot)
        for matrix, pivot in zip(raw_matrices, PIVOTS)
    ]
    coordinates = chart_coordinates(normalized)
    ambient_parameters = (alpha, beta, r, gamma, t0, t1, t2)
    ambient_jacobian = sp.Matrix(coordinates).jacobian(ambient_parameters).subs(sample)
    gamma_gradient = (
        -sp.Rational(5, 4),
        sp.Rational(9, 4),
        sp.Rational(5, 4),
    )
    family_jacobian = sp.Matrix.hstack(
        ambient_jacobian[:, 0] + gamma_gradient[0] * ambient_jacobian[:, 3],
        ambient_jacobian[:, 1] + gamma_gradient[1] * ambient_jacobian[:, 3],
        ambient_jacobian[:, 2] + gamma_gradient[2] * ambient_jacobian[:, 3],
        ambient_jacobian[:, 4],
        ambient_jacobian[:, 5],
        ambient_jacobian[:, 6],
    )
    family_columns = tuple(family_jacobian.rref()[1])
    assert len(family_columns) == 5
    restricted_family = family_jacobian[:, family_columns]
    family_rows = independent_rows(restricted_family)
    assert len(family_rows) == 5
    family_minor = sp.factor(
        family_jacobian.extract(family_rows, family_columns).det()
    )
    assert family_minor != 0

    # Universal Segre-incidence Jacobian in the same Grassmann charts.
    chart_symbols = sp.symbols("g0:16")
    generic_planes = generic_chart_matrices(chart_symbols)
    universal_coefficients = {
        bits: permanent([generic_planes[mode].row(bits[mode]) for mode in range(4)])
        for bits in BITS
    }
    chart_sample = {
        chart_symbols[index]: coordinates[index].subs(sample) for index in range(16)
    }
    anchor = (0, 0, 0, 0)
    anchor_value = sp.factor(universal_coefficients[anchor].subs(chart_sample))
    assert anchor_value == sp.Rational(1, 6)
    z = sp.symbols("z0:4")
    z_sample = {z[0]: 0, z[1]: -3, z[2]: 0, z[3]: 1}
    incidence_rows: list[tuple[int, int, int, int]] = []
    incidence_equations: list[sp.Expr] = []
    for bits in BITS:
        if bits == anchor:
            continue
        incidence_rows.append(bits)
        monomial = sp.prod(z[index] for index, bit in enumerate(bits) if bit)
        incidence_equations.append(
            sp.expand(universal_coefficients[bits] - universal_coefficients[anchor] * monomial)
        )
    incidence_variables = list(chart_symbols) + list(z)
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(incidence_variables)
        .subs(chart_sample | z_sample)
    )
    assert incidence_jacobian.rank() == 15
    incidence_columns = tuple(incidence_jacobian.rref()[1])
    restricted = incidence_jacobian[:, incidence_columns]
    selected_rows = independent_rows(restricted)
    incidence_minor = sp.factor(
        incidence_jacobian.extract(selected_rows, incidence_columns).det()
    )
    assert incidence_minor != 0

    print(
        json.dumps(
            {
                "status": "pass",
                "component": "Eisenstein-norm common-kernel XX triangle",
                "dimension": 5,
                "norm_quadric": str(norm_equation),
                "pure_support_on_quadric": {"1111": "4"},
                "pair_profile": pair_profile,
                "relation_ranks": relation_ranks,
                "family_rows": family_rows,
                "family_columns": family_columns,
                "family_tangent_minor": str(family_minor),
                "incidence_rows": selected_rows,
                "incidence_columns": incidence_columns,
                "incidence_minor": str(incidence_minor),
                "incidence_rank": 15,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
