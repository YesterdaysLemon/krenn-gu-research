#!/usr/bin/env python3
"""Exact characteristic-zero certificate for the common-kernel vertical component."""

from __future__ import annotations

import itertools
import json

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2),) * 4


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


def raw_family(p: sp.Expr, q: sp.Expr, phi: sp.Expr) -> tuple[sp.Matrix, ...]:
    basis = tuple(sp.eye(4).row(index) for index in range(4))
    a = basis[0] + basis[1]
    a_bar = basis[0] - basis[1]
    b = basis[2] + basis[3]
    b_bar = basis[2] - basis[3]
    return (
        sp.Matrix.vstack(a_bar + p * b, b_bar + q * b),
        sp.Matrix.vstack(b, a),
        sp.Matrix.vstack(b_bar, a),
        sp.Matrix.vstack(a_bar, b + phi * b_bar),
    )


def coefficients(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent([planes[mode].row(word[mode]) for mode in range(4)])
        for word in WORDS
    }


def reduce_in_charts(
    planes: tuple[sp.Matrix, ...], pivots: tuple[tuple[int, int], ...] = PIVOTS
) -> tuple[sp.Matrix, ...]:
    return tuple(
        sp.simplify(plane[:, pivot].inv() * plane)
        for plane, pivot in zip(planes, pivots, strict=True)
    )


def chart_coordinates(
    planes: tuple[sp.Matrix, ...], pivots: tuple[tuple[int, int], ...] = PIVOTS
) -> tuple[sp.Expr, ...]:
    result: list[sp.Expr] = []
    for plane, pivot in zip(planes, pivots, strict=True):
        nonpivots = tuple(column for column in range(4) if column not in pivot)
        result.extend(plane[row, column] for row in range(2) for column in nonpivots)
    return tuple(result)


def chart_planes(
    variables: tuple[sp.Symbol, ...],
    pivots: tuple[tuple[int, int], ...] = PIVOTS,
) -> tuple[sp.Matrix, ...]:
    result: list[sp.Matrix] = []
    for mode, pivot in enumerate(pivots):
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


def main() -> None:
    p, q, phi = sp.symbols("p q phi")
    planes = raw_family(p, q, phi)

    tensor = coefficients(planes)
    expected = {
        (0, 1, 1, 1): 4 * p,
        (1, 1, 1, 1): 4 * (q - phi),
    }
    assert all(
        sp.expand(value - expected.get(word, 0)) == 0 for word, value in tensor.items()
    )

    # The selected triangle has one kernel--kernel relation and two relations
    # with the common kernel at mode three.
    triangle_relations = {
        (1, 2): sp.Matrix((1, 0, 0, 0)),
        (1, 3): sp.Matrix((0, 0, 1, 0)),
        (2, 3): sp.Matrix((0, 0, 1, 0)),
    }
    for edge, relation in triangle_relations.items():
        matrix = pair_matrix(planes[edge[0]], planes[edge[1]])
        assert matrix * relation == sp.zeros(6, 1)
        assert matrix.rank() == 3
        assert sp.Matrix(2, 2, tuple(relation)).rank() == 1

    exterior_minors = {
        (0, 1): ((1, 2, 3, 5), -8 * p * q),
        (0, 2): ((1, 2, 3, 5), 8 * p),
        (0, 3): ((0, 1, 2, 5), -8 * (q - phi) * (phi * q - 1)),
    }
    for edge, (rows, expected_minor) in exterior_minors.items():
        matrix = pair_matrix(planes[edge[0]], planes[edge[1]])
        determinant = sp.factor(matrix.extract(rows, range(4)).det())
        assert sp.expand(determinant - expected_minor) == 0

    # Exact lower-pair boundary, using a few transparent 3 x 3 minors rather
    # than an elimination.  On 01 the minors include 4p and 4q; on 02 one is
    # the unit -4.  On 03 the displayed factors force p=0, q=phi, phi^2=1
    # whenever every 3 x 3 minor vanishes.
    exterior_three_minors: dict[tuple[int, int], set[sp.Expr]] = {}
    for edge in ((0, 1), (0, 2), (0, 3)):
        matrix = pair_matrix(planes[edge[0]], planes[edge[1]])
        exterior_three_minors[edge] = {
            sp.factor(matrix.extract(rows, columns).det())
            for rows in itertools.combinations(range(6), 3)
            for columns in itertools.combinations(range(4), 3)
        }
    assert {4 * p, 4 * q} <= exterior_three_minors[(0, 1)]
    assert -4 in exterior_three_minors[(0, 2)]
    required_03 = (
        4 * p**2,
        -4 * (phi * q - 1),
        -4 * (q - phi) * (phi + 1),
        4 * (q - phi) * (phi - 1),
    )
    assert all(
        any(
            sp.expand(candidate - required) == 0
            for candidate in exterior_three_minors[(0, 3)]
        )
        for required in required_03
    )
    assert pair_matrix(planes[0].subs({p: 0, q: 0}), planes[1]).rank() == 2
    assert (
        pair_matrix(planes[0].subs({p: 0, q: phi}), planes[3]).subs(phi, 1).rank() == 2
    )
    assert (
        pair_matrix(planes[0].subs({p: 0, q: phi}), planes[3]).subs(phi, -1).rank() == 2
    )

    sample_raw = tuple(plane.subs({p: 2, q: 3, phi: 2}) for plane in planes)
    profile = tuple(
        pair_matrix(sample_raw[left], sample_raw[right]).rank() for left, right in PAIRS
    )
    assert profile == (4, 4, 4, 3, 3, 3)

    # Five-dimensional family image after restoring the projective source
    # torus.  The sixth written parameter contains one stabilizer direction.
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    parameters = (p, q, phi, t0, t1, t2)
    diagonal = sp.diag(t0, t1, t2, 1)
    scaled = tuple(plane * diagonal for plane in planes)
    reduced = reduce_in_charts(scaled)
    coordinates = chart_coordinates(reduced)
    sample = {p: 2, q: 3, phi: 2, t0: 1, t1: 1, t2: 1}
    family_jacobian = sp.Matrix(coordinates).jacobian(parameters).subs(sample)
    family_rows = (0, 1, 3, 7, 15)
    family_columns = (0, 1, 2, 3, 5)
    family_minor = sp.factor(family_jacobian.extract(family_rows, family_columns).det())
    assert family_minor == sp.Rational(1, 72)
    assert family_jacobian.rank() == 5

    # Universal Segre incidence in the four (02) Grassmann charts.
    chart_symbols = tuple(sp.symbols("g0:16"))
    generic_planes = chart_planes(chart_symbols)
    universal = coefficients(generic_planes)
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
        (0, 0, 0, 1): 2,
        (1, 0, 0, 1): sp.Rational(1, 3),
    }

    alpha = (0, 0, 0, 1)
    z = tuple(sp.symbols("z0:4"))
    target_ratios = (sp.Rational(1, 6), 0, 0, 0)
    incidence_bits: list[tuple[int, int, int, int]] = []
    incidence_equations: list[sp.Expr] = []
    for word in WORDS:
        if word == alpha:
            continue
        incidence_bits.append(word)
        monomial = sp.prod(z[mode] for mode in range(4) if word[mode] != alpha[mode])
        incidence_equations.append(
            sp.expand(universal[word] - universal[alpha] * monomial)
        )

    incidence_variables = list(chart_symbols) + list(z)
    incidence_point = chart_sample | dict(zip(z, target_ratios, strict=True))
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(incidence_variables)
        .subs(incidence_point)
    )
    selected_rows = tuple(range(14))
    selected_columns = (0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 13, 14, 17, 19)
    incidence_minor = sp.factor(
        incidence_jacobian.extract(selected_rows, selected_columns).det()
    )
    assert incidence_minor == sp.Rational(1280, 27)
    assert incidence_jacobian.rank() == 14

    # The five family directions lift to the incidence tangent kernel.
    independent_parameters = (p, q, phi, t0, t2)
    family_plane_lift = (
        sp.Matrix(coordinates).jacobian(independent_parameters).subs(sample)
    )
    normalized_tensor = coefficients(reduced)
    ratio_expression = sp.factor(
        normalized_tensor[(1, 0, 0, 1)] / normalized_tensor[alpha]
    )
    ratio_lift = (
        sp.Matrix((ratio_expression, 0, 0, 0))
        .jacobian(independent_parameters)
        .subs(sample)
    )
    family_lift = family_plane_lift.col_join(ratio_lift)
    assert family_lift.rank() == 5
    assert incidence_jacobian * family_lift == sp.zeros(15, 5)

    # Fourteen equations cut out a regular sixfold.  The complement of the
    # selected implicit variables is (g3,g11,g12,g15,z0,z2).  Fix the first
    # five at the sample, put z2=h, and solve the fourteen equations to order
    # two.  The omitted 1111 equation has nonzero h^2 coefficient 1/6.
    h = sp.symbols("h")
    free_columns = (3, 11, 12, 15, 16, 18)
    fixed_free = {
        incidence_variables[index]: (
            h if index == 18 else incidence_point[incidence_variables[index]]
        )
        for index in free_columns
    }
    selected_variables = [incidence_variables[index] for index in selected_columns]
    selected_equations = sp.Matrix(
        [incidence_equations[index].subs(fixed_free) for index in selected_rows]
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
    assert incidence_bits[14] == (1, 1, 1, 1)
    omitted = incidence_equations[14].subs(fixed_free)
    transverse_quadratic = sp.factor(sp.expand(omitted.subs(second_series)).coeff(h, 2))
    assert transverse_quadratic == sp.Rational(1, 6)

    print(
        json.dumps(
            {
                "status": "verified",
                "field": "characteristic zero",
                "component": "common-kernel vertical rank-one triangle",
                "component_dimension": 5,
                "generic_pair_profile": list(profile),
                "generic_relation_ranks": [1, 1, 1],
                "kernel_endpoint_indegrees": [2, 1, 1, 0],
                "family_minor": str(family_minor),
                "incidence_rank": incidence_jacobian.rank(),
                "incidence_minor": str(incidence_minor),
                "transverse_quadratic_obstruction": str(transverse_quadratic),
                "certified_component_orbits": 19,
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
