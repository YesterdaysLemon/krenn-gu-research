#!/usr/bin/env python3
"""Exact certificate for the transverse common-factor pure-P4 component."""

from __future__ import annotations

import itertools
import json

import sympy as sp


BITS = tuple(itertools.product(range(2), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
TRIPLES = tuple(itertools.combinations(range(4), 3))
PIVOTS = ((2, 1), (0, 2), (0, 2), (2, 0))
DEGREE_THREE_MASKS = (14, 13, 11, 7)


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in itertools.permutations(range(4))
        )
    )


def squarefree_multiply(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(
                result.get(mask, sp.Integer(0)) + left_value * right_value
            )
    return result


def linear_form(row: sp.Matrix) -> dict[int, sp.Expr]:
    return {1 << index: row[index] for index in range(4) if row[index] != 0}


def triple_covector(*rows: sp.Matrix) -> sp.Matrix:
    value: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in rows:
        value = squarefree_multiply(value, linear_form(row))
    return sp.Matrix([sp.expand(value.get(mask, 0)) for mask in DEGREE_THREE_MASKS])


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
    a = sp.Matrix((1, 1, 0, 0))
    c = sp.Matrix((1, -1, 0, 0))
    zero6 = sp.zeros(6, 1)
    assert product(a, c) == zero6

    # The binary-polarity factorization of the three-cubic apolar condition.
    beta, rho, u, v, p, q, gamma, delta = sp.symbols(
        "beta rho u v p q gamma delta"
    )
    s = sp.Matrix((0, 0, u, v))
    t = sp.Matrix((0, 0, p, q))
    m_general = beta * c + s
    partner_general = m_general + rho * c
    d_general = gamma * a + delta * c + t
    cubic_matrix = sp.Matrix.hstack(
        triple_covector(a, a, d_general),
        triple_covector(a, m_general, d_general),
        triple_covector(m_general, partner_general, d_general),
    )
    polar = u * q + v * p
    determinant = u * q - v * p
    energy = (2 * beta + rho) * polar
    polarity_minors = tuple(
        sp.factor(cubic_matrix.extract(rows, range(3)).det())
        for rows in itertools.combinations(range(4), 3)
    )
    expected_polarity_minors = (
        4 * q * polar * (energy + 2 * delta * u * v),
        4 * p * polar * (energy + 2 * delta * u * v),
        -4
        * (gamma - delta)
        * determinant
        * (energy - 2 * gamma * u * v),
        4
        * (gamma + delta)
        * determinant
        * (energy + 2 * gamma * u * v),
    )
    assert all(
        sp.factor(left - right) == 0
        for left, right in zip(polarity_minors, expected_polarity_minors)
    )

    # The transverse coordinate-polar family.
    r, k = sp.symbols("r k")
    b = sp.Matrix((0, 0, 1, 1))
    m = b + c
    m_r = b + (1 + r) * c
    d = sp.Matrix((0, (r + 2) * (k + 1), 1, k))
    n = sp.Matrix((-(k - 1) * (r + 2), 0, -1, k))
    planes = ((n, c), (a, m), (a, m_r), (d, c))

    coefficients = {
        bits: sp.factor(permanent([planes[mode][bits[mode]] for mode in range(4)]))
        for bits in BITS
    }
    support = {bits: value for bits, value in coefficients.items() if value != 0}
    assert support == {(1, 1, 1, 1): -4}

    pair_matrices = {
        edge: pair_matrix(planes[edge[0]], planes[edge[1]]) for edge in PAIRS
    }
    relations = {
        (0, 1): sp.Matrix((0, 0, 1, 0)),
        (0, 2): sp.Matrix((0, 0, 1, 0)),
        (1, 2): sp.Matrix((0, -1, 1, 0)),
        (1, 3): sp.Matrix((0, 1, 0, 0)),
        (2, 3): sp.Matrix((0, 1, 0, 0)),
    }
    for edge, relation in relations.items():
        assert pair_matrices[edge] * relation == zero6
    relation_ranks = {
        edge: sp.Matrix(2, 2, list(relation)).rank()
        for edge, relation in relations.items()
    }
    assert sorted(relation_ranks.values()) == [1, 1, 1, 1, 2]

    pair_minor_data = (
        ((0, 1), (0, 1, 3), (0, 1, 3), -(k * r + 2 * k - r) * (k * r + 2 * k - r - 4)),
        ((0, 2), (0, 1, 3), (0, 1, 3), -(k * r + 2 * k + r) * (k * r + 2 * k - 3 * r - 4)),
        ((0, 3), (0, 1, 2, 3), (0, 1, 2, 3), 8 * k**2 * (r + 2)),
        ((1, 2), (0, 1, 3), (0, 1, 3), -4 * (r + 2)),
        ((1, 3), (0, 1, 3), (0, 2, 3), -(k * r + 2 * k + r) * (k * r + 2 * k + r + 4)),
        ((2, 3), (0, 1, 3), (0, 2, 3), -(k * r + 2 * k - r) * (k * r + 2 * k + 3 * r + 4)),
    )
    for edge, rows, columns, expected in pair_minor_data:
        actual = sp.factor(pair_matrices[edge].extract(rows, columns).det())
        assert sp.factor(actual - expected) == 0

    sample = {r: -sp.Rational(4, 3), k: 2}
    pair_profile = [matrix.subs(sample).rank() for matrix in pair_matrices.values()]
    assert pair_profile == [3, 3, 4, 3, 3, 3]

    # Every three-mode subset has a two-dimensional kernel-rich cubic span.
    triple_span_ranks: dict[str, int] = {}
    for triple in TRIPLES:
        columns = []
        for local_bits in itertools.product(range(2), repeat=3):
            if local_bits == (1, 1, 1):
                continue
            columns.append(
                triple_covector(
                    *(planes[triple[index]][local_bits[index]] for index in range(3))
                ).subs(sample)
            )
        rank = sp.Matrix.hstack(*columns).rank()
        triple_span_ranks["".join(map(str, triple))] = rank
    assert set(triple_span_ranks.values()) == {2}

    # Restore the projective source torus and certify five visible directions.
    t0, t1, t2 = sp.symbols("t0 t1 t2", nonzero=True)
    diagonal = sp.diag(t0, t1, t2, 1)
    raw_matrices = [sp.Matrix.vstack(*[row.T for row in plane]) for plane in planes]
    normalized = [
        normalize(matrix * diagonal, pivot)
        for matrix, pivot in zip(raw_matrices, PIVOTS)
    ]
    coordinates = chart_coordinates(normalized)
    parameters = (r, k, t0, t1, t2)
    tangent_sample = sample | {t0: 1, t1: 1, t2: 1}
    family_jacobian = sp.Matrix(coordinates).jacobian(parameters).subs(tangent_sample)
    family_rows = (0, 1, 2, 6, 7)
    family_minor = sp.factor(family_jacobian.extract(family_rows, range(5)).det())
    assert family_minor == 2
    assert family_jacobian.rank() == 5

    # Universal Segre-incidence Jacobian at the transverse point.
    chart_symbols = sp.symbols("g0:16")
    generic_planes = generic_chart_matrices(chart_symbols)
    universal_coefficients = {
        bits: permanent([generic_planes[mode].row(bits[mode]) for mode in range(4)])
        for bits in BITS
    }
    chart_sample = {
        chart_symbols[index]: coordinates[index].subs(tangent_sample)
        for index in range(16)
    }
    normalized_support = {
        bits: sp.factor(value.subs(chart_sample))
        for bits, value in universal_coefficients.items()
        if value.subs(chart_sample) != 0
    }
    assert normalized_support == {(1, 1, 1, 1): 4}

    z = sp.symbols("z0:4")
    alpha = (1, 1, 1, 1)
    incidence_bits: list[tuple[int, int, int, int]] = []
    incidence_equations: list[sp.Expr] = []
    for bits in BITS:
        if bits == alpha:
            continue
        incidence_bits.append(bits)
        monomial = sp.prod(z[index] for index, bit in enumerate(bits) if bit == 0)
        incidence_equations.append(
            sp.expand(
                universal_coefficients[bits]
                - universal_coefficients[alpha] * monomial
            )
        )
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(list(chart_symbols) + list(z))
        .subs(chart_sample | {variable: 0 for variable in z})
    )
    selected_rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14)
    selected_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 15, 16, 17, 19)
    incidence_minor = sp.factor(
        incidence_jacobian.extract(selected_rows, selected_columns).det()
    )
    assert incidence_minor == -131072
    assert incidence_jacobian.rank() == 14

    family_lift = sp.zeros(20, 5)
    family_lift[:16, :] = family_jacobian
    assert incidence_jacobian * family_lift == sp.zeros(15, 5)
    assert family_lift.rank() == 5
    assert len(incidence_jacobian.nullspace()) == 6

    # Fourteen equations cut out a smooth sixfold, but the fifteenth is a
    # genuine quadratic transverse obstruction.  Use z2=h as the sixth
    # implicit coordinate, hold the other five free coordinates fixed, and
    # solve the selected equations through order two.  The omitted 1001 row
    # then has nonzero h^2 coefficient 12.  Hence the full incidence has local
    # dimension at most five, while the family supplies five actual directions.
    h = sp.symbols("h")
    incidence_variables = list(chart_symbols) + list(z)
    selected_variables = [incidence_variables[index] for index in selected_columns]
    free_substitution = {
        chart_symbols[10]: chart_sample[chart_symbols[10]],
        chart_symbols[11]: chart_sample[chart_symbols[11]],
        chart_symbols[12]: chart_sample[chart_symbols[12]],
        chart_symbols[13]: chart_sample[chart_symbols[13]],
        chart_symbols[14]: chart_sample[chart_symbols[14]],
        z[2]: h,
    }
    selected_equations = sp.Matrix(
        [incidence_equations[index].subs(free_substitution) for index in selected_rows]
    )
    selected_base = {
        variable: (
            chart_sample[variable] if variable in chart_sample else sp.Integer(0)
        )
        for variable in selected_variables
    }
    selected_jacobian = selected_equations.jacobian(selected_variables).subs(
        selected_base | {h: 0}
    )
    assert sp.factor(selected_jacobian.det()) == incidence_minor

    fixed_series = {variable: value for variable, value in selected_base.items()}
    first_residual = sp.Matrix(
        [sp.expand(value.subs(fixed_series)).coeff(h, 1) for value in selected_equations]
    )
    first_correction = -selected_jacobian.inv() * first_residual
    first_series = {
        variable: selected_base[variable] + first_correction[index] * h
        for index, variable in enumerate(selected_variables)
    }
    second_residual = sp.Matrix(
        [sp.expand(value.subs(first_series)).coeff(h, 2) for value in selected_equations]
    )
    second_correction = -selected_jacobian.inv() * second_residual
    second_series = {
        variable: first_series[variable] + second_correction[index] * h**2
        for index, variable in enumerate(selected_variables)
    }
    omitted_equation = incidence_equations[9].subs(free_substitution)
    transverse_quadratic = sp.factor(
        sp.expand(omitted_equation.subs(second_series)).coeff(h, 2)
    )
    assert transverse_quadratic == 12

    print(
        json.dumps(
            {
                "status": "pass",
                "component": "transverse binary-polarity common-factor component",
                "certified_component_orbits": 12,
                "component_dimension": 5,
                "pure_support": {"1111": "-4"},
                "generic_pair_profile": pair_profile,
                "relation_ranks": sorted(relation_ranks.values()),
                "all_triple_kernel_rich_span_ranks": triple_span_ranks,
                "family_tangent_minor": str(family_minor),
                "incidence_minor": str(incidence_minor),
                "incidence_rank": incidence_jacobian.rank(),
                "transverse_quadratic_obstruction": str(transverse_quadratic),
                "binary_polarity_factors": [str(value) for value in expected_polarity_minors],
                "search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
