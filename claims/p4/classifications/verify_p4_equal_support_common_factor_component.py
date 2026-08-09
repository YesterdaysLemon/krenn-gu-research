#!/usr/bin/env python3
"""Exact characteristic-zero certificate for the equal-support component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 1), (0, 1), (0, 1), (0, 2))


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


def main() -> None:
    p, q, r = sp.symbols("p q r")
    t0, t1, t2 = sp.symbols("t0 t1 t2", nonzero=True)
    a = sp.Matrix((1, 1, 0, 0))
    a_bar = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    b_bar = sp.Matrix((0, 0, 1, -1))
    zero = sp.zeros(6, 1)
    assert product(a, a_bar) == zero
    assert product(b, b_bar) == zero

    planes = (
        (a + p * b, a_bar + q * b),
        (a, a_bar + b),
        (a, r * a_bar + b),
        (b_bar, a_bar),
    )
    coefficients = {
        bits: sp.factor(permanent([planes[mode][bits[mode]] for mode in range(4)]))
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    assert set(support) == {(0, 1, 1, 1), (1, 1, 1, 1)}
    assert sp.factor(support[(0, 1, 1, 1)] + 4 * p * (r + 1)) == 0
    assert sp.factor(support[(1, 1, 1, 1)] + 4 * (q * r + q + 1)) == 0

    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]]) for edge in PAIRS
    }
    exterior_minors = (
        sp.factor(pair_matrices[(0, 1)].extract((0, 1, 3, 5), range(4)).det()),
        sp.factor(pair_matrices[(0, 2)].extract((0, 1, 3, 5), range(4)).det()),
        sp.factor(pair_matrices[(0, 3)].extract((0, 1, 2, 3), range(4)).det()),
    )
    assert exterior_minors == (-8 * p * q, -8 * p * q, -8 * p)
    triangle_minors = (
        sp.factor(pair_matrices[(1, 2)].extract((0, 1, 3), (0, 1, 3)).det()),
        sp.factor(pair_matrices[(1, 3)].extract((0, 1, 3), (0, 2, 3)).det()),
        sp.factor(pair_matrices[(2, 3)].extract((0, 1, 3), (0, 2, 3)).det()),
    )
    assert all(
        sp.factor(left - right) == 0
        for left, right in zip(triangle_minors, (-4 * (r + 1), 4, 4 * r**2))
    )
    relations = (
        sp.Matrix((0, -1, 1, 0)),
        sp.Matrix((0, 1, 0, 0)),
        sp.Matrix((0, 1, 0, 0)),
    )
    for edge, relation in zip(((1, 2), (1, 3), (2, 3)), relations):
        assert pair_matrices[edge] * relation == zero
    relation_ranks = [sp.Matrix(2, 2, list(value)).rank() for value in relations]
    assert relation_ranks == [2, 1, 1]

    # Restore the projective diagonal source torus and normalize the four
    # Grassmann charts.
    diagonal = sp.diag(t0, t1, t2, 1)
    raw_matrices = [sp.Matrix.vstack(*[row.T for row in plane]) for plane in planes]
    normalized = [
        normalize(matrix * diagonal, pivot)
        for matrix, pivot in zip(raw_matrices, PIVOTS)
    ]
    coordinates = chart_coordinates(normalized)
    parameters = (p, q, r, t0, t1, t2)
    sample = {p: 1, q: 2, r: 2, t0: 1, t1: 1, t2: 1}
    family_jacobian = sp.Matrix(coordinates).jacobian(parameters).subs(sample)
    family_rows = (0, 1, 2, 4, 6, 8)
    family_minor = sp.factor(
        family_jacobian.extract(family_rows, range(6)).det()
    )
    assert family_minor == sp.Rational(3, 128)
    assert family_jacobian.rank() == 6

    # Universal Segre-incidence Jacobian on the same plane charts.
    chart_symbols = sp.symbols("g0:16")
    generic_planes = generic_chart_matrices(chart_symbols)
    universal_coefficients = {
        bits: permanent([generic_planes[mode].row(bits[mode]) for mode in range(4)])
        for bits in BITS
    }
    chart_sample = {
        chart_symbols[index]: coordinates[index].subs(sample) for index in range(16)
    }
    normalized_support = {
        bits: sp.factor(value.subs(chart_sample))
        for bits, value in universal_coefficients.items()
        if value.subs(chart_sample) != 0
    }
    assert universal_coefficients[(0, 0, 0, 0)].subs(chart_sample) == -sp.Rational(5, 2)

    z = sp.symbols("z0:4")
    z_sample = {z[0]: -sp.Rational(2, 5), z[1]: -1, z[2]: -1, z[3]: 0}
    incidence_rows: list[tuple[int, int, int, int]] = []
    incidence_equations: list[sp.Expr] = []
    alpha = (0, 0, 0, 0)
    for bits in BITS:
        if bits == alpha:
            continue
        incidence_rows.append(bits)
        monomial = sp.prod(z[index] for index, bit in enumerate(bits) if bit)
        incidence_equations.append(
            sp.expand(universal_coefficients[bits] - universal_coefficients[alpha] * monomial)
        )
    incidence_variables = list(chart_symbols) + list(z)
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(incidence_variables)
        .subs(chart_sample | z_sample)
    )
    selected_bits = tuple(bits for bits in incidence_rows if bits != (1, 1, 1, 0))
    selected_rows = tuple(incidence_rows.index(bits) for bits in selected_bits)
    selected_columns = (0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 17, 19)
    incidence_minor = sp.factor(
        incidence_jacobian.extract(selected_rows, selected_columns).det()
    )
    assert incidence_minor == -sp.Rational(9, 2)
    assert incidence_jacobian.rank() == 14

    print(
        json.dumps(
            {
                "status": "pass",
                "component": "equal-support common-factor (2,1,1) triangle",
                "dimension": 6,
                "pure_support": {"0111": str(support[(0, 1, 1, 1)]), "1111": str(support[(1, 1, 1, 1)])},
                "pair_profile": [4, 4, 4, 3, 3, 3],
                "relation_ranks": relation_ranks,
                "family_tangent_minor": str(family_minor),
                "incidence_minor": str(incidence_minor),
                "incidence_rank": incidence_jacobian.rank(),
                "certified_component_orbits": 11,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
