#!/usr/bin/env python3
"""Exact verifier for the unequal-complement common-kernel P4 component."""

from __future__ import annotations

import itertools
import json

import sympy as sp

BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def cubic(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    values: list[sp.Expr] = []
    for missing in range(4):
        support = [index for index in range(4) if index != missing]
        values.append(
            sp.expand(
                sum(
                    left[support[permutation[0]]]
                    * middle[support[permutation[1]]]
                    * right[support[permutation[2]]]
                    for permutation in itertools.permutations(range(3))
                )
            )
        )
    return sp.Matrix(values)


def product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]
    )


def pair_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            product(left.row(i).T, right.row(j).T)
            for i in range(2)
            for j in range(2)
        )
    )


def chart_coordinates(
    planes: tuple[sp.Matrix, ...], diagonal: sp.Matrix
) -> list[sp.Expr]:
    coordinates: list[sp.Expr] = []
    for plane in planes:
        moved = plane * diagonal
        normalized = sp.simplify(moved[:, (0, 1)].inv() * moved)
        coordinates.extend(
            sp.factor(normalized[row, column])
            for row in range(2)
            for column in (2, 3)
        )
    return coordinates


def independent_rows(matrix: sp.Matrix) -> tuple[int, ...]:
    return tuple(matrix.T.rref()[1])


def main() -> None:
    A, B, R, G, D = sp.symbols("A B R G D")
    a = sp.Matrix((1, 1, 0, 0))
    c = sp.Matrix((1, -1, 0, 0))
    b = sp.Matrix((0, 0, 1, 1))
    u = (1 - D) / 2
    v = (1 + D) / 2
    t = sp.Matrix((0, 0, u, v))
    m = A * a + B * c + b
    m_r = m + R * c
    d = G * a + t

    columns = sp.Matrix.hstack(
        cubic(m, m_r, c),
        cubic(m, m_r, d),
        cubic(m, a, d),
    )
    minors = tuple(
        sp.factor(columns[list(rows), :].det())
        for rows in itertools.combinations(range(4), 3)
    )
    H = A**2 + B**2 + B * R + 2 * A * G
    Q = A**2 + 2 * A * G - 3 * B**2 - 3 * B * R + 4 * G**2 - R**2
    expected_minors = (
        -4 * (Q + D * H),
        -4 * (Q - D * H),
        -4 * D * (A - B) * (A - B - R) * (2 * B - 2 * G + R),
        -4 * D * (A + B) * (A + B + R) * (2 * B + 2 * G + R),
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(minors, expected_minors)
    )

    # Intrinsic full-support direction calculation before normalizing the
    # sums of the complementary coefficients.
    uu, vv, pp, qq = sp.symbols("u v p q")
    s_general = sp.Matrix((0, 0, uu, vv))
    t_general = sp.Matrix((0, 0, pp, qq))
    m_general = A * a + B * c + s_general
    mr_general = m_general + R * c
    d_general = G * a + t_general
    general_columns = sp.Matrix.hstack(
        cubic(m_general, mr_general, c),
        cubic(m_general, mr_general, d_general),
        cubic(a, m_general, d_general),
    )
    general_minors = tuple(
        sp.factor(general_columns[list(rows), :].det())
        for rows in itertools.combinations(range(4), 3)
    )
    U = uu * vv
    S = pp * vv + qq * uu
    Qsplit = pp * vv - qq * uu
    synchronizer = 2 * B + R
    norm = 3 * B**2 + 3 * B * R + R**2
    E = S**2 * (norm - A**2) - 2 * S * U * A * G - 4 * U**2 * G**2
    J = S * (A**2 + B * (B + R)) + 2 * U * A * G
    expected_general_minors = (
        4 * vv * (E + Qsplit * J),
        4 * uu * (E - Qsplit * J),
        4
        * Qsplit
        * (A - B)
        * (A - B - R)
        * (synchronizer * S - 2 * G * U),
        4
        * Qsplit
        * (A + B)
        * (A + B + R)
        * (synchronizer * S + 2 * G * U),
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(general_minors, expected_general_minors)
    )

    # The nonzero split-polar boundary S=0.  Choosing t=(u,-v) loses no
    # generality after its row scaling.  The only possible active escapes
    # have a second exact leaf relation and are lower-pair.
    polar_t = sp.Matrix((0, 0, uu, -vv))
    polar_m = A * a + B * c + s_general
    polar_mr = polar_m + R * c
    polar_d = polar_t
    polar_C1 = cubic(polar_m, polar_mr, polar_d)
    polar_C2 = cubic(a, polar_m, polar_d)
    polar_X = cubic(a, a, polar_d)
    assert sp.simplify(polar_C1 - (A**2 - B * (B + R)) * polar_X) == sp.zeros(4, 1)
    assert sp.simplify(polar_C2 - A * polar_X) == sp.zeros(4, 1)
    lower_pair_first = sp.Matrix.vstack(s_general.T, a.T)
    lower_pair_second = sp.Matrix.vstack(c.T, polar_t.T)
    assert pair_matrix(lower_pair_first, lower_pair_second).rank() == 2

    # Coordinate-supported s.  The transverse q-chart forces k=0; the
    # active escape can occur only when the synchronized pair already drops
    # to rank two.
    coordinate_s = sp.Matrix((0, 0, uu, 0))
    coordinate_t = sp.Matrix((0, 0, pp, qq))
    coordinate_m = A * a + B * c + coordinate_s
    coordinate_mr = coordinate_m + R * c
    coordinate_d = G * a + coordinate_t
    coordinate_columns = sp.Matrix.hstack(
        cubic(coordinate_m, coordinate_mr, c),
        cubic(coordinate_m, coordinate_mr, coordinate_d),
        cubic(a, coordinate_m, coordinate_d),
    )
    coordinate_minors = tuple(
        sp.factor(coordinate_columns[list(rows), :].det())
        for rows in itertools.combinations(range(4), 3)
    )
    expected_coordinate_minors = (
        0,
        4 * qq**2 * uu**3 * synchronizer**2,
        4
        * qq**2
        * uu**2
        * (A - B)
        * synchronizer
        * (-A + B + R),
        -4
        * qq**2
        * uu**2
        * (A + B)
        * synchronizer
        * (A + B + R),
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(coordinate_minors, expected_coordinate_minors)
    )
    coordinate_C1 = coordinate_columns[:, 1].subs(R, -2 * B)
    coordinate_C2 = coordinate_columns[:, 2].subs(R, -2 * B)
    coordinate_X = cubic(a, a, coordinate_d)
    assert sp.simplify(
        coordinate_C1
        - 2 * A * coordinate_C2
        + (A**2 - B**2) * coordinate_X
    ) == sp.zeros(4, 1)
    for exceptional_alpha in (B, -B):
        first = sp.Matrix.vstack(
            coordinate_m.subs(A, exceptional_alpha).T,
            a.T,
        )
        second = sp.Matrix.vstack(
            coordinate_mr.subs({A: exceptional_alpha, R: -2 * B}).T,
            a.T,
        )
        assert pair_matrix(first, second).rank() == 2
    embedded_rows = sp.Matrix.vstack(
        coordinate_m.T,
        a.T,
        coordinate_mr.T,
        c.T,
        coordinate_d.subs(qq, 0).T,
    ).subs(qq, 0)
    assert embedded_rows.rank() <= 3
    zero_s_first = sp.Matrix.vstack((A * a + B * c).T, a.T)
    zero_s_second = sp.Matrix.vstack((A * a + (B + R) * c).T, a.T)
    assert pair_matrix(zero_s_first, zero_s_second).rank() <= 2
    assert cubic(a, a, G * a) == sp.zeros(4, 1)

    # With D nonzero, the first two minors give H=Q=0.  Selecting one
    # factor from each remaining product gives nine exact branches.
    left_factors = (A - B, A - B - R, 2 * B + R - 2 * G)
    right_factors = (A + B, A + B + R, 2 * B + R + 2 * G)
    branch_bases = {}
    for i, left in enumerate(left_factors):
        for j, right in enumerate(right_factors):
            basis = tuple(
                sp.factor(polynomial.as_expr())
                for polynomial in sp.groebner(
                    (H, Q, left, right), G, R, B, A, order="lex"
                ).polys
            )
            branch_bases[f"{i}{j}"] = tuple(map(str, basis))

    expected_branch_bases = {
        "00": ("(2*G - R)*(2*G + R)", "B", "A"),
        "01": ("G**2", "A*G", "2*A + R", "-A + B"),
        "02": ("2*A + 2*G + R", "-A + B"),
        "10": ("G**2", "A*G", "-2*A + R", "A + B"),
        "11": ("-(B - 2*G)*(B + 2*G)", "B + R", "A"),
        "12": ("A + B + 2*G", "-A + B + R"),
        "20": ("2*A + 2*G - R", "A + B"),
        "21": ("A - B + 2*G", "A + B + R"),
        "22": ("G", "2*B + R", "-(A - B)*(A + B)"),
    }
    assert branch_bases == expected_branch_bases

    sheets = (
        {B: A, G: -(2 * A + R) / 2},
        {B: -A, G: -(2 * A - R) / 2},
        {R: A - B, G: -(A + B) / 2},
        {R: -A - B, G: -(A - B) / 2},
    )
    for sheet in sheets:
        assert all(sp.factor(minor.subs(sheet)) == 0 for minor in minors)

    # The first sheet is a representative of the single symmetry orbit.
    t0, t1, t2 = sp.symbols("t0 t1 t2", nonzero=True)
    u1 = (1 - D) / 2
    v1 = (1 + D) / 2
    G1 = -(2 * A + R) / 2
    m1 = sp.Matrix((2 * A, 0, 1, 1))
    mr1 = m1 + R * c
    d1 = G1 * a + sp.Matrix((0, 0, u1, v1))
    y0 = sp.Matrix((0, D * (2 * A + R), -u1, v1))
    x0 = sp.Matrix((-A * v1, A * (u1 + 1) + R, 1, 0))
    planes = (
        sp.Matrix.vstack(y0.T, x0.T),
        sp.Matrix.vstack(m1.T, a.T),
        sp.Matrix.vstack(mr1.T, a.T),
        sp.Matrix.vstack(c.T, d1.T),
    )

    coefficients = {
        bits: sp.factor(
            permanent([planes[mode].row(bits[mode]) for mode in range(4)])
        )
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    assert support == {(1, 1, 1, 1): D + 1}

    wedge = sp.Matrix(
        [
            y0[i] * x0[j] - y0[j] * x0[i]
            for i, j in itertools.combinations(range(4), 2)
        ]
    )
    extended_wedge = tuple(sp.factor(value / (D + 1)) for value in wedge)
    expected_extended_wedge = (
        A * D * (2 * A + R) / 2,
        A * (D - 1) / 4,
        A * (D + 1) / 4,
        (A * D + 3 * A + 2 * R) / 4,
        (A * D - 3 * A - 2 * R) / 4,
        sp.Rational(-1, 2),
    )
    assert all(
        sp.factor(observed - expected) == 0
        for observed, expected in zip(extended_wedge, expected_extended_wedge)
    )

    sample = {A: 1, R: 1, D: 2, t0: 1, t1: 1, t2: 1}
    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]]) for edge in PAIRS
    }
    pair_profile = tuple(
        pair_matrices[edge].subs(sample).rank() for edge in PAIRS
    )
    assert pair_profile == (4, 4, 4, 3, 3, 3)
    relation_ranks = []
    for edge in ((1, 2), (1, 3), (2, 3)):
        kernel = pair_matrices[edge].subs(sample).nullspace()
        assert len(kernel) == 1
        relation_ranks.append(sp.Matrix(2, 2, list(kernel[0])).rank())
    assert relation_ranks == [2, 1, 1]

    diagonal = sp.diag(t0, t1, t2, 1)
    coordinates = chart_coordinates(planes, diagonal)
    family_parameters = (A, R, D, t0, t1, t2)
    family_jacobian = sp.Matrix(coordinates).jacobian(family_parameters).subs(sample)
    family_columns = tuple(family_jacobian.rref()[1])
    family_rows = independent_rows(family_jacobian[:, family_columns])
    family_minor = sp.factor(
        family_jacobian.extract(family_rows, family_columns).det()
    )
    assert family_columns == (0, 1, 2, 3, 5)
    assert family_rows == (0, 1, 2, 3, 4)
    assert family_minor == -sp.Rational(1, 5184)

    chart_symbols = sp.symbols("g0:16")
    generic_planes = []
    index = 0
    for _mode in range(4):
        plane = sp.zeros(2, 4)
        plane[0, 0] = plane[1, 1] = 1
        for row in range(2):
            for column in (2, 3):
                plane[row, column] = chart_symbols[index]
                index += 1
        generic_planes.append(plane)
    universal_coefficients = {
        bits: permanent(
            [generic_planes[mode].row(bits[mode]) for mode in range(4)]
        )
        for bits in BITS
    }
    chart_sample = {
        chart_symbols[index]: coordinates[index].subs(sample) for index in range(16)
    }
    anchor = (0, 1, 0, 0)
    anchor_value = sp.factor(universal_coefficients[anchor].subs(chart_sample))
    assert anchor_value == sp.Rational(1, 6)
    z = sp.symbols("z0:4")
    z_sample = {z[0]: 0, z[1]: 0, z[2]: 3, z[3]: 1}
    incidence_equations = []
    for bits in BITS:
        if bits == anchor:
            continue
        monomial = sp.prod(z[mode] for mode in range(4) if bits[mode] != anchor[mode])
        incidence_equations.append(
            sp.expand(universal_coefficients[bits] - universal_coefficients[anchor] * monomial)
        )
    assert all(
        equation.subs(chart_sample | z_sample) == 0
        for equation in incidence_equations
    )
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(list(chart_symbols) + list(z))
        .subs(chart_sample | z_sample)
    )
    assert incidence_jacobian.rank() == 15
    incidence_columns = tuple(incidence_jacobian.rref()[1])
    incidence_rows = independent_rows(incidence_jacobian[:, incidence_columns])
    incidence_minor = sp.factor(
        incidence_jacobian.extract(incidence_rows, incidence_columns).det()
    )
    assert incidence_minor == sp.Rational(1, 23328)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "component": "unequal-complement common-kernel triangle",
                "component_orbit_number": 22,
                "rank_locus_sheets": 4,
                "sheets_form_one_symmetry_orbit": True,
                "complete_CC_orientation_classified": True,
                "direction_boundaries": [
                    "component 13",
                    "lower-pair",
                    "embedded P3",
                    "zero",
                ],
                "sample_pair_profile": pair_profile,
                "sample_relation_ranks": relation_ranks,
                "family_tangent_rank": len(family_columns),
                "family_tangent_minor": str(family_minor),
                "incidence_rank": incidence_jacobian.rank(),
                "incidence_minor": str(incidence_minor),
                "incidence_local_dimension": 5,
                "finite_field_proof_used": False,
                "all_pure_components_classified": False,
                "generic_P5_fibres_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
