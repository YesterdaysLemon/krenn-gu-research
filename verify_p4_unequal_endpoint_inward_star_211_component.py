#!/usr/bin/env python3
"""Verify component 25 from the unequal-endpoint inward star-(2,1,1)."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes):
    return {
        bits: sp.factor(permanent([planes[index].row(bits[index]) for index in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(product(left.row(i), right.row(j)) for i in range(2) for j in range(2))
    )


def chart_coordinates(plane, pivot, diagonal):
    moved = plane * diagonal
    remaining = tuple(index for index in range(4) if index not in pivot)
    normalized = sp.simplify(moved[:, pivot].inv() * moved)
    return [
        sp.factor(normalized[row, column])
        for row in range(2)
        for column in remaining
    ]


def main():
    e, j, k, s = sp.symbols("e j k s")
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack(C.T, (A + e * B - k * D).T),
        sp.Matrix.vstack(D.T, (A - s * j * C + j * B).T),
    )

    tensor = coefficients(planes)
    expected = {
        (0, 0, 1, 1): 4 * (e * j + k**2),
        (0, 1, 1, 1): 4 * (e + j),
        (1, 0, 1, 1): 4 * (e + j),
        (1, 1, 1, 1): 4 * (1 + e * j * s**2),
    }
    assert all(sp.factor(tensor[bits] - expected.get(bits, 0)) == 0 for bits in BITS)
    hypersurface = sp.expand(
        (e * j + k**2) * (1 + e * j * s**2) - (e + j) ** 2
    )
    segre_minor = sp.factor(
        tensor[(0, 0, 1, 1)] * tensor[(1, 1, 1, 1)]
        - tensor[(0, 1, 1, 1)] * tensor[(1, 0, 1, 1)]
    )
    assert sp.factor(segre_minor - 16 * hypersurface) == 0

    # Irreducibility over characteristic zero: as a quadratic in k, a factor
    # would make -constant/leading_coefficient a square in C(e,j,s).  Its
    # valuation along 1+e*j*s^2 is -1.
    leading = 1 + e * j * s**2
    numerator = (e + j) ** 2 - e * j * leading
    assert sp.factor(leading) == leading
    assert sp.gcd(leading, numerator) == 1
    assert sp.factor(hypersurface) == hypersurface

    sample = {e: -5, j: 2, k: 3, s: -1}
    assert hypersurface.subs(sample) == 0
    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]]) for edge in PAIRS
    }
    profile = tuple(pair_matrices[edge].subs(sample).rank() for edge in PAIRS)
    assert profile == (3, 3, 3, 4, 4, 4)
    relation_ranks = []
    for edge in ((0, 1), (0, 2), (0, 3)):
        kernel = pair_matrices[edge].subs(sample).nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert relation_ranks == [2, 1, 1]

    minors = tuple(
        sp.factor(pair_matrices[edge].extract((0, 1, 2, 3), range(4)).det())
        for edge in ((1, 2), (1, 3), (2, 3))
    )
    expected_minors = (
        8 * k * (e * s - 1) * (e * s + 1),
        8 * s * (j * s - 1) * (j * s + 1),
        -8 * j * (e * s - 1) * (j * s - 1),
    )
    assert all(
        sp.factor(observed - expected_value) == 0
        for observed, expected_value in zip(minors, expected_minors)
    )

    q0, q1, q2 = sp.symbols("q0 q1 q2")
    diagonal = sp.diag(q0, q1, q2, 1)
    pivots = ((0, 2), (0, 1), (0, 1), (0, 2))
    coordinates = [
        coordinate
        for plane, pivot in zip(planes, pivots)
        for coordinate in chart_coordinates(plane, pivot, diagonal)
    ]
    torus_sample = sample | {q0: 1, q1: 1, q2: 1}
    variables = (e, j, k, s, q0, q1, q2)
    ambient_jacobian = sp.Matrix(coordinates).jacobian(variables).subs(torus_sample)
    gradient = sp.Matrix(
        [[sp.diff(hypersurface, variable).subs(torus_sample) for variable in variables]]
    )
    assert list(gradient[:, :4]) == [-14, 56, -54, -20]
    tangent = sp.zeros(7, 6)
    free_variables = (0, 1, 3, 4, 5, 6)
    for column, variable_index in enumerate(free_variables):
        tangent[variable_index, column] = 1
        tangent[2, column] = -gradient[0, variable_index] / gradient[0, 2]
    family_jacobian = sp.simplify(ambient_jacobian * tangent)
    family_rows = (0, 3, 4, 5, 8)
    family_columns = (0, 1, 2, 3, 5)
    family_minor = sp.factor(
        family_jacobian.extract(family_rows, family_columns).det()
    )
    assert family_jacobian.rank() == 5
    assert family_minor == -sp.Rational(7, 27)

    g_variables = sp.symbols("g0:16")
    generic_planes = []
    cursor = 0
    for pivot in pivots:
        remaining = tuple(index for index in range(4) if index not in pivot)
        plane = sp.zeros(2, 4)
        plane[0, pivot[0]] = plane[1, pivot[1]] = 1
        for row in range(2):
            for column in remaining:
                plane[row, column] = g_variables[cursor]
                cursor += 1
        generic_planes.append(plane)
    universal = coefficients(tuple(generic_planes))
    chart_sample = {
        g_variables[index]: coordinates[index].subs(torus_sample) for index in range(16)
    }
    anchor = (0, 0, 0, 0)
    assert universal[anchor].subs(chart_sample) == sp.Rational(2, 3)
    z = sp.symbols("z0:4")
    z_sample = {z[0]: 3, z[1]: -2, z[2]: 1, z[3]: 0}
    incidence_equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        monomial = sp.prod(
            z[mode] for mode in range(4) if bits[mode] != anchor[mode]
        )
        incidence_equations.append(
            sp.expand(universal[bits] - universal[anchor] * monomial)
        )
    incidence_sample = chart_sample | z_sample
    assert all(equation.subs(incidence_sample) == 0 for equation in incidence_equations)
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian((*g_variables, *z))
        .subs(incidence_sample)
    )
    incidence_columns = tuple(range(13)) + (14, 19)
    incidence_minor = sp.factor(
        incidence_jacobian[:, incidence_columns].det()
    )
    assert incidence_jacobian.rank() == 15
    assert incidence_minor == sp.Rational(81920, 3)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "component_orbit_number": 25,
                "orientation": "unequal-center-endpoint two-inward star-(2,1,1)",
                "irreducible_hypersurface": True,
                "sample_pair_profile": profile,
                "sample_relation_ranks": relation_ranks,
                "family_tangent_rank": 5,
                "family_tangent_minor": str(family_minor),
                "incidence_rank": 15,
                "incidence_minor": str(incidence_minor),
                "reverse_boundary_classification_complete": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
