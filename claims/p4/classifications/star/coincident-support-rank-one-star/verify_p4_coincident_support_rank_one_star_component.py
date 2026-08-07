#!/usr/bin/env python3
"""Exact certificate for the coincident-support rank-one star component."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 1), (0, 1), (0, 1), (0, 2))
ALPHA = (0, 0, 0, 0)
SELECTED_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14)
SELECTED_COLUMNS = (0, 1, 2, 4, 5, 6, 7, 8, 10, 12, 13, 14, 19)
FREE_COLUMNS = (3, 9, 11, 15, 16, 17, 18)


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def pair_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            pair_product(left.row(i).T, right.row(j).T)
            for i, j in itertools.product(range(2), repeat=2)
        )
    )


def raw_family(
    p: sp.Expr, q: sp.Expr, kappa: sp.Expr, ell: sp.Expr
) -> tuple[sp.Matrix, ...]:
    basis = tuple(sp.eye(4).row(index) for index in range(4))
    a = basis[0] + basis[1]
    c = basis[0] - basis[1]
    b = basis[2] + basis[3]
    d = basis[2] - basis[3]
    return (
        sp.Matrix.vstack(a + p * b, c + q * b),
        sp.Matrix.vstack(a, c),
        sp.Matrix.vstack(c, b + kappa * a),
        sp.Matrix.vstack(a + ell * c, d),
    )


def homogeneous_family(
    p: sp.Expr, q: sp.Expr, kappa: sp.Expr, r: sp.Expr, s: sp.Expr
) -> tuple[sp.Matrix, ...]:
    basis = tuple(sp.eye(4).row(index) for index in range(4))
    a = basis[0] + basis[1]
    c = basis[0] - basis[1]
    b = basis[2] + basis[3]
    d = basis[2] - basis[3]
    return (
        sp.Matrix.vstack(a + p * b, c + q * b),
        sp.Matrix.vstack(a, c),
        sp.Matrix.vstack(c, b + kappa * a),
        sp.Matrix.vstack(r * a + s * c, d),
    )


def coefficients(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent([planes[mode].row(word[mode]) for mode in range(4)])
        for word in WORDS
    }


def reduce_in_charts(planes: tuple[sp.Matrix, ...]) -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.simplify(plane[:, pivot].inv() * plane)
        for plane, pivot in zip(planes, PIVOTS, strict=True)
    )


def chart_coordinates(planes: tuple[sp.Matrix, ...]) -> tuple[sp.Expr, ...]:
    result: list[sp.Expr] = []
    for plane, pivot in zip(planes, PIVOTS, strict=True):
        nonpivots = tuple(column for column in range(4) if column not in pivot)
        result.extend(plane[row, column] for row in range(2) for column in nonpivots)
    return tuple(result)


def chart_planes(variables: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, ...]:
    result: list[sp.Matrix] = []
    for mode, pivot in enumerate(PIVOTS):
        nonpivots = tuple(column for column in range(4) if column not in pivot)
        plane = sp.zeros(2, 4)
        plane[0, pivot[0]] = 1
        plane[1, pivot[1]] = 1
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        result.append(plane)
    return tuple(result)


def plucker(plane: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(plane[:, columns].det())
        for columns in itertools.combinations(range(4), 2)
    )


def main() -> None:
    p, q, kappa, ell = sp.symbols("p q kappa ell")
    planes = raw_family(p, q, kappa, ell)

    tensor = coefficients(planes)
    expected = {
        (0, 0, 1, 0): 4 * p,
        (0, 1, 1, 0): -4 * ell * p,
        (1, 0, 1, 0): 4 * q,
        (1, 1, 1, 0): -4 * ell * q,
    }
    assert all(
        sp.expand(value - expected.get(word, 0)) == 0 for word, value in tensor.items()
    )

    relations = {
        (0, 1): sp.Matrix((1, -q / p, -p / q, 1)),
        (1, 2): sp.Matrix((1, 0, 0, 0)),
        (1, 3): sp.Matrix((ell, 0, 1, 0)),
    }
    for edge, relation in relations.items():
        matrix = pair_matrix(planes[edge[0]], planes[edge[1]])
        assert sp.simplify(matrix * relation) == sp.zeros(6, 1)
        assert matrix.rank() == 3
        assert sp.Matrix(2, 2, tuple(relation)).rank() == 1

    exterior_minors = {
        (0, 2): ((0, 1, 3, 5), -8 * p * q),
        (0, 3): ((0, 1, 2, 3), -8 * (ell + 1) * (ell * p + q)),
        (2, 3): ((0, 1, 2, 3), -8 * kappa * ell * (ell + 1)),
    }
    for edge, (rows, expected_minor) in exterior_minors.items():
        matrix = pair_matrix(planes[edge[0]], planes[edge[1]])
        actual = sp.factor(matrix.extract(rows, range(4)).det())
        assert sp.expand(actual - expected_minor) == 0

    sample_raw = tuple(plane.subs({p: 2, q: 3, kappa: 1, ell: 2}) for plane in planes)
    profile = tuple(
        pair_matrix(sample_raw[left], sample_raw[right]).rank() for left, right in PAIRS
    )
    assert profile == (3, 4, 4, 3, 3, 4)

    # Restore the projective diagonal source torus.  Seven written
    # parameters have a one-dimensional stabilizer in the image.
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    parameters = (p, q, kappa, ell, t0, t1, t2)
    diagonal = sp.diag(t0, t1, t2, 1)
    reduced = reduce_in_charts(tuple(plane * diagonal for plane in planes))
    coordinates = chart_coordinates(reduced)
    sigma = sp.symbols("sigma", nonzero=True)
    stabilizer = {
        p: sigma * p,
        q: sigma * q,
        kappa: kappa / sigma,
        t0: sigma * t0,
        t1: sigma * t1,
    }
    assert all(
        sp.factor(coordinate.subs(stabilizer, simultaneous=True) - coordinate) == 0
        for coordinate in coordinates
    )
    sample = {
        p: 2,
        q: 3,
        kappa: 1,
        ell: 2,
        t0: 1,
        t1: 1,
        t2: 1,
    }
    family_jacobian = sp.Matrix(coordinates).jacobian(parameters).subs(sample)
    family_rows = (0, 1, 2, 8, 10, 12)
    family_columns = (0, 1, 2, 3, 4, 6)
    family_minor = sp.factor(family_jacobian.extract(family_rows, family_columns).det())
    assert family_minor == -sp.Rational(5, 72)
    assert family_jacobian.rank() == 6

    # Universal Segre incidence in the four indicated Grassmann charts.
    chart_symbols = tuple(sp.symbols("g0:16"))
    universal = coefficients(chart_planes(chart_symbols))
    chart_sample = {
        chart_symbols[index]: sp.factor(coordinates[index].subs(sample))
        for index in range(16)
    }
    normalized_support = {
        word: sp.factor(value.subs(chart_sample))
        for word, value in universal.items()
        if value.subs(chart_sample) != 0
    }
    assert normalized_support == {
        (0, 0, 0, 0): -sp.Rational(5, 6),
        (0, 0, 1, 0): -sp.Rational(5, 6),
        (0, 1, 0, 0): sp.Rational(5, 2),
        (0, 1, 1, 0): sp.Rational(5, 2),
        (1, 0, 0, 0): sp.Rational(1, 6),
        (1, 0, 1, 0): sp.Rational(1, 6),
        (1, 1, 0, 0): -sp.Rational(1, 2),
        (1, 1, 1, 0): -sp.Rational(1, 2),
    }

    z = tuple(sp.symbols("z0:4"))
    target_ratios = (-sp.Rational(1, 5), -3, 1, 0)
    incidence_bits: list[tuple[int, int, int, int]] = []
    incidence_equations: list[sp.Expr] = []
    for word in WORDS:
        if word == ALPHA:
            continue
        incidence_bits.append(word)
        monomial = sp.prod(z[mode] for mode in range(4) if word[mode] != ALPHA[mode])
        incidence_equations.append(
            sp.expand(universal[word] - universal[ALPHA] * monomial)
        )

    incidence_variables = list(chart_symbols) + list(z)
    incidence_point = chart_sample | dict(zip(z, target_ratios, strict=True))
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(incidence_variables)
        .subs(incidence_point)
    )
    incidence_minor = sp.factor(
        incidence_jacobian.extract(SELECTED_ROWS, SELECTED_COLUMNS).det()
    )
    assert incidence_minor == 100
    assert incidence_jacobian.rank() == 13

    # The six actual family directions lift to incidence and project with
    # rank six to six of the seven regular free coordinates.
    independent_parameters = (p, q, kappa, ell, t0, t2)
    family_plane_lift = (
        sp.Matrix(coordinates).jacobian(independent_parameters).subs(sample)
    )
    normalized_tensor = coefficients(reduced)
    ratio_expressions = []
    for mode in range(4):
        adjacent = list(ALPHA)
        adjacent[mode] = 1
        ratio_expressions.append(
            sp.factor(normalized_tensor[tuple(adjacent)] / normalized_tensor[ALPHA])
        )
    ratio_lift = (
        sp.Matrix(ratio_expressions).jacobian(independent_parameters).subs(sample)
    )
    family_lift = family_plane_lift.col_join(ratio_lift)
    assert family_lift.rank() == 6
    assert incidence_jacobian * family_lift == sp.zeros(15, 6)
    fixed_free_columns = FREE_COLUMNS[:-1]
    free_projection_minor = sp.factor(
        family_lift.extract(fixed_free_columns, range(6)).det()
    )
    assert free_projection_minor == sp.Rational(1, 50)

    # The thirteen selected equations form a regular sevenfold.  Fix six
    # free coordinates and put z2=1+h.  The two omitted equations are
    # quadratically nonzero on the resulting transverse formal curve.
    h = sp.symbols("h")
    fixed_free = {
        incidence_variables[index]: (
            incidence_point[incidence_variables[index]] + h
            if index == 18
            else incidence_point[incidence_variables[index]]
        )
        for index in FREE_COLUMNS
    }
    selected_variables = [incidence_variables[index] for index in SELECTED_COLUMNS]
    selected_equations = sp.Matrix(
        [incidence_equations[index].subs(fixed_free) for index in SELECTED_ROWS]
    )
    selected_base = {
        variable: incidence_point[variable] for variable in selected_variables
    }
    selected_jacobian = selected_equations.jacobian(selected_variables).subs(
        selected_base | {h: 0}
    )
    assert sp.factor(selected_jacobian.det()) == incidence_minor

    first_residual = sp.Matrix(
        [
            sp.expand(equation.subs(selected_base)).coeff(h, 1)
            for equation in selected_equations
        ]
    )
    first_correction = -selected_jacobian.inv() * first_residual
    first_series = {
        variable: selected_base[variable] + first_correction[index] * h
        for index, variable in enumerate(selected_variables)
    }
    second_residual = sp.Matrix(
        [
            sp.expand(equation.subs(first_series)).coeff(h, 2)
            for equation in selected_equations
        ]
    )
    second_correction = -selected_jacobian.inv() * second_residual
    second_series = {
        variable: first_series[variable] + second_correction[index] * h**2
        for index, variable in enumerate(selected_variables)
    }
    assert all(
        sp.expand(equation.subs(second_series)).coeff(h, 2) == 0
        for equation in selected_equations
    )

    omitted_rows = (9, 13)
    omitted_quadratics = []
    for row in omitted_rows:
        expansion = sp.expand(
            incidence_equations[row].subs(fixed_free).subs(second_series)
        )
        assert expansion.coeff(h, 1) == 0
        omitted_quadratics.append(sp.factor(expansion.coeff(h, 2)))
    assert incidence_bits[9] == (1, 0, 1, 0)
    assert incidence_bits[13] == (1, 1, 1, 0)
    assert omitted_quadratics == [sp.Rational(7, 60), -sp.Rational(7, 20)]

    # The complete mixed-chain vertical fibre is the homogeneous boundary
    # kappa=0, [r:s]=[0:1].
    epsilon = sp.symbols("epsilon")
    arc = homogeneous_family(p, q, 0, epsilon, 1)
    target = homogeneous_family(p, q, 0, 0, 1)
    for arc_plane, target_plane in zip(arc, target, strict=True):
        arc_plucker = plucker(arc_plane)
        target_plucker = plucker(target_plane)
        assert all(
            sp.expand(value.subs(epsilon, 0) - expected_value) == 0
            for value, expected_value in zip(arc_plucker, target_plucker, strict=True)
        )
    target_tensor = coefficients(target)
    target_expected = {
        (0, 1, 1, 0): -4 * p,
        (1, 1, 1, 0): -4 * q,
    }
    assert all(
        sp.expand(value - target_expected.get(word, 0)) == 0
        for word, value in target_tensor.items()
    )

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "characteristic zero",
                "component": "coincident-support rank-one star",
                "component_number": 21,
                "component_dimension": 6,
                "generic_pair_profile": list(profile),
                "generic_relation_ranks": [1, 1, 1],
                "family_minor": str(family_minor),
                "incidence_rank": incidence_jacobian.rank(),
                "incidence_minor": str(incidence_minor),
                "free_projection_minor": str(free_projection_minor),
                "omitted_quadratics": [str(value) for value in omitted_quadratics],
                "mixed_chain_vertical_boundary": "verified",
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
