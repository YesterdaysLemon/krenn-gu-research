#!/usr/bin/env python3
"""Verify component 24 and the split-center mixed star reverse theorem."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def coefficients(planes):
    return {
        bits: sp.factor(permanent([planes[i].row(bits[i]) for i in range(4)]))
        for bits in BITS
    }


def product(left, right):
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


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


def reverse_purity_ledger(A, C, B, D):
    a, c, e, f, g, h, j, k, n, s = sp.symbols("a c e f g h j k n s")
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack((a * A + c * C + e * B + f * D).T, C.T),
        sp.Matrix.vstack(D.T, (g * A + h * C + j * B + n * D).T),
    )
    observed = coefficients(planes)
    expected = {
        (0, 0, 0, 0): -4 * (a * k + f),
        (0, 0, 0, 1): -4 * (a * k * n - e * j + f * g * k + f * n),
        (0, 1, 0, 1): 4 * (a * j + e * g),
        (1, 0, 0, 1): 4 * (a * j + e * g),
        (1, 1, 0, 1): 4 * (a * g - c * h - c * j * s - e * h * s),
        (1, 1, 1, 1): -4 * (h + j * s),
    }
    assert all(sp.factor(observed[bits] - expected.get(bits, 0)) == 0 for bits in BITS)

    delta = e**2 - a**2 * k**2
    matrix = sp.Matrix(((e, a * k**2), (a, e)))
    assert sp.factor(matrix.det() - delta) == 0
    # On Delta != 0, j=g=0 and purity gives c=-e*s; U0*U3 then has rank two.
    lower_u3 = sp.Matrix.vstack(D.T, C.T)
    assert pair_matrix(planes[0], lower_u3).rank() == 2

    for epsilon in (1, -1):
        branch = {e: epsilon * a * k, f: -a * k, j: -epsilon * k * g}
        relation = c * (h - epsilon * k * s * g) - a * (
            g - epsilon * k * s * h
        )
        assert sp.factor(observed[(0, 1, 0, 1)].subs(branch)) == 0
        assert sp.factor(observed[(0, 0, 0, 1)].subs(branch)) == 0
        assert sp.factor(observed[(1, 1, 0, 1)].subs(branch) + 4 * relation) == 0


def main():
    k, s, tau = sp.symbols("k s tau")
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    reverse_purity_ledger(A, C, B, D)

    c = (tau - k * s) / (1 - k * s * tau)
    planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack((A + c * C + k * B - k * D).T, C.T),
        sp.Matrix.vstack(D.T, (tau * A + C - k * tau * B).T),
    )
    tensor = coefficients(planes)
    assert sp.factor(tensor[(1, 1, 1, 1)] - 4 * (k * s * tau - 1)) == 0
    assert all(value == 0 for bits, value in tensor.items() if bits != (1, 1, 1, 1))

    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]]) for edge in PAIRS
    }
    sample = {k: 2, s: 3, tau: 2}
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
        8 * k * (k * s - 1) * (k * s + 1),
        8 * s * tau * (tau + 1) * (k * s - 1),
        8 * k * (tau - 1) * (tau + 1),
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(minors, expected_minors)
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
    family_jacobian = sp.Matrix(coordinates).jacobian((k, s, tau, q0, q1, q2)).subs(
        torus_sample
    )
    family_rows = (0, 3, 4, 5, 12)
    family_columns = (0, 1, 2, 3, 5)
    family_minor = sp.factor(
        family_jacobian.extract(family_rows, family_columns).det()
    )
    assert family_jacobian.rank() == 5
    assert family_minor == -sp.Rational(1, 81)

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
    anchor = (1, 0, 0, 0)
    assert universal[anchor].subs(chart_sample) == sp.Rational(7, 9)
    z = sp.symbols("z0:4")
    z_sample = {z[0]: 0, z[1]: -1, z[2]: -sp.Rational(15, 7), z[3]: 0}
    incidence_equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        monomial = sp.prod(z[mode] for mode in range(4) if bits[mode] != anchor[mode])
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
    incidence_columns = tuple(range(12)) + (14, 16, 19)
    incidence_minor = sp.factor(incidence_jacobian[:, incidence_columns].det())
    assert incidence_jacobian.rank() == 15
    assert incidence_minor == -sp.Rational(57671680, 6561)

    # The h=0 endpoint is a genuine point of the same projective sheet.
    endpoint_c = -sp.Rational(1, 6)
    endpoint_planes = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + 2 * D).T, (B + 3 * C).T),
        sp.Matrix.vstack((A + endpoint_c * C + 2 * B - 2 * D).T, C.T),
        sp.Matrix.vstack(D.T, (A - 2 * B).T),
    )
    endpoint_tensor = coefficients(endpoint_planes)
    assert endpoint_tensor[(1, 1, 1, 1)] == 24
    assert all(
        value == 0 for bits, value in endpoint_tensor.items() if bits != (1, 1, 1, 1)
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "component_orbit_number": 24,
                "orientation": "split-center mixed star-(2,1,1)",
                "sample_pair_profile": profile,
                "sample_relation_ranks": relation_ranks,
                "family_tangent_rank": 5,
                "family_tangent_minor": str(family_minor),
                "incidence_rank": 15,
                "incidence_minor": str(incidence_minor),
                "projective_leaf_endpoint_checked": True,
                "sign_sheets_one_source_orbit": True,
                "all_pure_components_classified": False,
                "generic_P5_fibres_closed": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
