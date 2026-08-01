#!/usr/bin/env python3
"""Verify component 23 and the outward common-center-kernel star ledger."""

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


def independent_rows(matrix):
    return tuple(matrix.T.rref()[1])


def assert_ledger(planes, expected):
    observed = coefficients(planes)
    for bits, value in expected.items():
        assert sp.factor(observed[bits] - value) == 0, (bits, observed[bits], value)


def boundary_ledger(A, C, B, D):
    # Center support one.
    tau, v = sp.symbols("tau v")
    e = sp.Matrix((1, 0, 0, 0))
    support_a = sp.Matrix((0, 1, 1, 0))
    support_c = sp.Matrix((0, 1, -1, 0))
    support_z = sp.Matrix((0, 0, 0, 1))
    a2, a3, c2, c3, e2, e3, z2, z3 = sp.symbols(
        "a2 a3 c2 c3 e2 e3 z2 z3"
    )
    w2 = e2 * e + a2 * support_a + c2 * support_c + z2 * support_z
    w3 = e3 * e + a3 * support_a + c3 * support_c + z3 * support_z
    p0 = sp.Matrix.vstack(e.T, support_a.T)
    p1 = sp.Matrix.vstack((e + tau * support_c).T, (v * e + support_a).T)
    common = {
        (0, 0, 1, 1): -2 * tau * (c2 * z3 + c3 * z2),
        (0, 1, 1, 1): 2 * (a2 * z3 + a3 * z2),
        (1, 0, 1, 1): 2 * (a2 * z3 + a3 * z2),
    }
    active = 2 * (v * a2 * z3 + v * a3 * z2 + e2 * z3 + e3 * z2)
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(e.T, w2.T), sp.Matrix.vstack(e.T, w3.T)),
        common | {(1, 1, 0, 1): 2 * z3, (1, 1, 1, 0): 2 * z2, (1, 1, 1, 1): active},
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(e.T, w2.T), sp.Matrix.vstack(w3.T, e.T)),
        {
            (0, 0, 1, 0): -2 * tau * (c2 * z3 + c3 * z2),
            (0, 1, 1, 0): 2 * (a2 * z3 + a3 * z2),
            (1, 0, 1, 0): 2 * (a2 * z3 + a3 * z2),
            (1, 1, 0, 0): 2 * z3,
            (1, 1, 1, 0): active,
            (1, 1, 1, 1): 2 * z2,
        },
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(w2.T, e.T), sp.Matrix.vstack(w3.T, e.T)),
        {
            (0, 0, 0, 0): -2 * tau * (c2 * z3 + c3 * z2),
            (0, 1, 0, 0): 2 * (a2 * z3 + a3 * z2),
            (1, 0, 0, 0): 2 * (a2 * z3 + a3 * z2),
            (1, 1, 0, 0): active,
            (1, 1, 0, 1): 2 * z2,
            (1, 1, 1, 0): 2 * z3,
            (1, 1, 1, 1): 0,
        },
    )

    # Center support two with a singleton complement Q=0, alpha=0.
    s, u = sp.symbols("s u")
    singleton = (B + D) / 2
    delta2, delta3 = e2 - z2, e3 - z3
    # Reuse z_i as f_i in this block.
    w2 = a2 * A + c2 * C + e2 * B + z2 * D
    w3 = a3 * A + c3 * C + e3 * B + z3 * D
    linear = a2 * delta3 + a3 * delta2
    quadratic = e2 * e3 - z2 * z3
    p0 = sp.Matrix.vstack(A.T, singleton.T)
    p1 = sp.Matrix.vstack((A + tau * singleton).T, (s * C + singleton).T)
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(C.T, w2.T), sp.Matrix.vstack(C.T, w3.T)),
        {
            (0, 0, 1, 1): 2 * (tau * linear + 2 * quadratic),
            (0, 1, 1, 1): 2 * linear,
            (1, 0, 1, 1): 2 * linear,
            (1, 1, 0, 1): -2 * s * delta3,
            (1, 1, 1, 0): -2 * s * delta2,
            (1, 1, 1, 1): -2 * s * (c2 * delta3 + c3 * delta2),
        },
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(C.T, w2.T), sp.Matrix.vstack(w3.T, C.T)),
        {
            (0, 0, 1, 0): 2 * (tau * linear + 2 * quadratic),
            (0, 1, 1, 0): 2 * linear,
            (1, 0, 1, 0): 2 * linear,
            (1, 1, 0, 0): -2 * s * delta3,
            (1, 1, 1, 0): -2 * s * (c2 * delta3 + c3 * delta2),
            (1, 1, 1, 1): -2 * s * delta2,
        },
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(w2.T, C.T), sp.Matrix.vstack(w3.T, C.T)),
        {
            (0, 0, 0, 0): 2 * (tau * linear + 2 * quadratic),
            (0, 1, 0, 0): 2 * linear,
            (1, 0, 0, 0): 2 * linear,
            (1, 1, 0, 0): -2 * s * (c2 * delta3 + c3 * delta2),
            (1, 1, 0, 1): -2 * s * delta2,
            (1, 1, 1, 0): -2 * s * delta3,
            (1, 1, 1, 1): 0,
        },
    )

    # Singleton complement, alpha=1.
    p0 = sp.Matrix.vstack(A.T, (C + singleton).T)
    p1 = sp.Matrix.vstack(
        (u * A + v * C - v * singleton).T,
        (-v * A + s * C + u * singleton).T,
    )
    assert sp.factor(
        pair_matrix(p0, p1).extract((0, 1, 3), (0, 1, 3)).det()
        + 4 * (s + u) * (u - v) * (u + v)
    ) == 0
    big_g = s * (c2 * delta3 + c3 * delta2) + 2 * s * quadratic + v * linear + u * (
        c2 * delta3 + c3 * delta2
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(C.T, w2.T), sp.Matrix.vstack(C.T, w3.T)),
        {
            (0, 0, 1, 1): 2 * (-v * linear + 2 * u * quadratic),
            (0, 1, 1, 1): 2 * (u * linear - 2 * v * quadratic),
            (1, 0, 1, 1): 2 * (u * linear - 2 * v * quadratic),
            (1, 1, 0, 1): -2 * (s + u) * delta3,
            (1, 1, 1, 0): -2 * (s + u) * delta2,
            (1, 1, 1, 1): -2 * big_g,
        },
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(C.T, w2.T), sp.Matrix.vstack(w3.T, C.T)),
        {
            (0, 0, 1, 0): 2 * (-v * linear + 2 * u * quadratic),
            (0, 1, 1, 0): 2 * (u * linear - 2 * v * quadratic),
            (1, 0, 1, 0): 2 * (u * linear - 2 * v * quadratic),
            (1, 1, 0, 0): -2 * (s + u) * delta3,
            (1, 1, 1, 0): -2 * big_g,
            (1, 1, 1, 1): -2 * (s + u) * delta2,
        },
    )
    assert_ledger(
        (p0, p1, sp.Matrix.vstack(w2.T, C.T), sp.Matrix.vstack(w3.T, C.T)),
        {
            (0, 0, 0, 0): 2 * (-v * linear + 2 * u * quadratic),
            (0, 1, 0, 0): 2 * (u * linear - 2 * v * quadratic),
            (1, 0, 0, 0): 2 * (u * linear - 2 * v * quadratic),
            (1, 1, 0, 0): -2 * big_g,
            (1, 1, 0, 1): -2 * (s + u) * delta2,
            (1, 1, 1, 0): -2 * (s + u) * delta3,
            (1, 1, 1, 1): 0,
        },
    )

    # Generic alpha*Q branch and normalized alpha=0,Q!=0 branch.
    alpha, b, d, k = sp.symbols("alpha b d k")
    complement = b * B + d * D
    generic_p0 = sp.Matrix.vstack(A.T, (alpha * C + complement).T)
    generic_p1 = sp.Matrix.vstack(A.T, (s * C + complement).T)
    generic_yy = (
        generic_p0,
        generic_p1,
        sp.Matrix.vstack(C.T, w2.T),
        sp.Matrix.vstack(C.T, w3.T),
    )
    generic_yx = generic_yy[:3] + (sp.Matrix.vstack(w3.T, C.T),)
    assert sp.factor(coefficients(generic_yy)[(1, 1, 0, 0)] + 4 * (b**2 - d**2)) == 0
    assert sp.factor(coefficients(generic_yx)[(1, 1, 0, 1)] + 4 * (b**2 - d**2)) == 0

    normalized_p0 = sp.Matrix.vstack(A.T, B.T)
    normalized_p1 = sp.Matrix.vstack((A + k * D).T, (s * C + B).T)
    normalized_xx = (
        normalized_p0,
        normalized_p1,
        sp.Matrix.vstack(w2.T, C.T),
        sp.Matrix.vstack(w3.T, C.T),
    )
    expected = {
        (0, 0, 0, 0): -4 * (k * a2 * z3 + k * a3 * z2 - e2 * e3 + z2 * z3),
        (0, 1, 0, 0): 4 * (a2 * e3 + a3 * e2),
        (1, 0, 0, 0): 4 * (a2 * e3 + a3 * e2),
        (1, 1, 0, 0): 4 * (-s * c2 * e3 - s * c3 * e2 + a2 * a3 - c2 * c3),
        (1, 1, 0, 1): -4 * (s * e2 + c2),
        (1, 1, 1, 0): -4 * (s * e3 + c3),
        (1, 1, 1, 1): -4,
    }
    observed = coefficients(normalized_xx)
    assert_ledger(normalized_xx, expected)
    assert all(observed[bits] == 0 for bits in BITS if bits not in expected)


def main():
    s, r, t, k = sp.symbols("s r t k")
    A = sp.Matrix((1, 1, 0, 0))
    C = sp.Matrix((1, -1, 0, 0))
    B = sp.Matrix((0, 0, 1, 1))
    D = sp.Matrix((0, 0, 1, -1))
    planes_polynomial = (
        sp.Matrix.vstack(A.T, B.T),
        sp.Matrix.vstack((A + k * D).T, (B + s * C).T),
        sp.Matrix.vstack((s * (A - C) + B + r * D).T, C.T),
        sp.Matrix.vstack((-s * (A + C) + B + t * D).T, C.T),
    )
    tensor = coefficients(planes_polynomial)
    assert sp.factor(
        tensor[(0, 0, 0, 0)] + 4 * (-s * k * r + s * k * t + r * t - 1)
    ) == 0
    assert tensor[(1, 1, 1, 1)] == -4
    assert all(
        value == 0
        for bits, value in tensor.items()
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    )

    k_value = (1 - r * t) / (s * (t - r))
    planes = tuple(plane.subs(k, k_value) for plane in planes_polynomial)
    sample = {s: 1, r: 2, t: 3}
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
    selected_minors = (
        sp.factor(pair_matrices[(1, 2)].extract((0, 1, 2, 3), range(4)).det()),
        sp.factor(pair_matrices[(1, 3)].extract((0, 1, 3, 4), range(4)).det()),
        sp.factor(pair_matrices[(2, 3)].extract((0, 1, 2, 3), range(4)).det()),
    )
    expected_minors = (
        16 * s * (r - 1) * (r + 1) * (r * t - 1) / (r - t) ** 2,
        -16 * s * (t - 1) * (t + 1) * (r * t - 1) / (r - t) ** 2,
        -8 * s * (r - t) ** 2,
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(selected_minors, expected_minors)
    )

    q0, q1, q2 = sp.symbols("q0 q1 q2")
    diagonal = sp.diag(q0, q1, q2, 1)
    pivots = ((0, 2), (0, 1), (0, 1), (0, 1))
    coordinates = [
        coordinate
        for plane, pivot in zip(planes, pivots)
        for coordinate in chart_coordinates(plane, pivot, diagonal)
    ]
    torus_sample = sample | {q0: 1, q1: 1, q2: 1}
    family_jacobian = sp.Matrix(coordinates).jacobian((s, r, t, q0, q1, q2)).subs(
        torus_sample
    )
    family_minor = sp.factor(
        family_jacobian.extract((0, 3, 4, 5, 8), (0, 1, 2, 3, 5)).det()
    )
    assert family_jacobian.rank() == 5
    assert family_minor == -sp.Rational(3, 4)

    g = sp.symbols("g0:16")
    generic_planes = []
    cursor = 0
    for pivot in pivots:
        remaining = tuple(index for index in range(4) if index not in pivot)
        plane = sp.zeros(2, 4)
        plane[0, pivot[0]] = plane[1, pivot[1]] = 1
        for row in range(2):
            for column in remaining:
                plane[row, column] = g[cursor]
                cursor += 1
        generic_planes.append(plane)
    universal = coefficients(tuple(generic_planes))
    chart_sample = {g[index]: coordinates[index].subs(torus_sample) for index in range(16)}
    anchor = (1, 0, 0, 1)
    assert universal[anchor].subs(chart_sample) == 2
    z = sp.symbols("z0:4")
    z_sample = {z[0]: 0, z[1]: -1, z[2]: 0, z[3]: 0}
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
        .jacobian((*g, *z))
        .subs(incidence_sample)
    )
    columns = tuple(range(10)) + (12, 13, 16, 18, 19)
    rows = independent_rows(incidence_jacobian[:, columns])
    incidence_minor = sp.factor(incidence_jacobian.extract(rows, columns).det())
    assert incidence_jacobian.rank() == 15
    assert rows == tuple(range(15))
    assert incidence_minor == -9600

    boundary_ledger(A, C, B, D)
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "component_orbit_number": 23,
                "orientation": "outward common-center-kernel star-(2,1,1)",
                "pure_hypersurface": "1-r*t=k*s*(t-r)",
                "sample_pair_profile": profile,
                "sample_relation_ranks": relation_ranks,
                "family_tangent_rank": 5,
                "family_tangent_minor": str(family_minor),
                "incidence_rank": 15,
                "incidence_minor": str(incidence_minor),
                "outward_flag_pairs_exhausted": ["YY", "YX", "XX"],
                "boundary_routes": ["component 23", "components 11/12", "lower-pair", "zero"],
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
