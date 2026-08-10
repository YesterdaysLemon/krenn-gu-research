#!/usr/bin/env python3
"""Verify the normalized q4_211 simultaneous-pencil reduction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md"
TARGET_WORDS = tuple(itertools.product(range(3), repeat=4))
INTEGER_MAPS = (
    sp.Matrix(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [-1, -1, 0],
            [0, 0, -1],
        ]
    ),
    sp.Matrix(
        [
            [1, 1, -2],
            [-2, 1, 1],
            [1, -2, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    ),
    sp.Matrix(
        [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, -1, -1],
            [-1, 0, 0],
        ]
    ),
    sp.Matrix(
        [
            [-1, -1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, 1, -1],
            [0, -2, 0],
        ]
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contracted_polynomial(
    covector: tuple[sp.Expr, ...], variables: tuple[sp.Symbol, ...]
) -> sp.Expr:
    return sp.expand(
        sum(
            covector[missing]
            * sp.prod(
                variables[index]
                for index in range(5)
                if index != missing
            )
            for missing in range(5)
        )
    )


def coefficient_vector(
    maps: tuple[sp.Matrix, ...], colours: tuple[int, ...]
) -> tuple[sp.Expr, ...]:
    values = []
    for missing in range(5):
        coordinates = tuple(
            index for index in range(5) if index != missing
        )
        values.append(
            sp.expand(
                sum(
                    sp.prod(
                        maps[mode][injection[mode], colours[mode]]
                        for mode in range(4)
                    )
                    for injection in itertools.permutations(coordinates)
                )
            )
        )
    return tuple(values)


def off_diagonal_matrix(
    maps: tuple[sp.Matrix, ...],
) -> tuple[sp.Matrix, tuple[tuple[int, ...], ...]]:
    words = tuple(word for word in TARGET_WORDS if len(set(word)) != 1)
    return (
        sp.Matrix([coefficient_vector(maps, word) for word in words]),
        words,
    )


def family_maps(u: sp.Expr, v: sp.Expr, w: sp.Expr) -> tuple[sp.Matrix, ...]:
    parameters = {0: u, 2: v, 3: w}
    special_colours = {0: 2, 2: 0, 3: 1}
    distinguished_coordinate = {0: 1, 1: 2, 2: 0}
    maps = []
    for mode in range(4):
        columns = []
        for colour in range(3):
            if mode == 1:
                source = [sp.Integer(1)] * 3
                source[distinguished_coordinate[colour]] = -2
                source.append(sp.Integer(1))
                alpha = sp.Integer(1)
            else:
                parameter = parameters[mode]
                source = [parameter] * 3
                source[distinguished_coordinate[colour]] = 1
                source.append(
                    -parameter
                    if colour == special_colours[mode]
                    else -1
                )
                alpha = (
                    parameter - 1
                    if colour == special_colours[mode]
                    else 0
                )
            columns.append(sp.Matrix(source + [alpha]))
        maps.append(sp.Matrix.hstack(*columns))
    return tuple(maps)


def polynomial_gcd(
    expressions: list[sp.Expr], variable: sp.Symbol
) -> sp.Expr:
    polynomials = [
        sp.Poly(expression, variable, domain=sp.QQ)
        for expression in expressions
        if expression != 0
    ]
    if not polynomials:
        return sp.Integer(0)
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = sp.gcd(result, polynomial)
    return sp.factor(result.as_expr())


def canonical_edge_pair(
    first: tuple[int, int], second: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    candidates = []
    for permutation in itertools.permutations(range(4)):
        transformed = tuple(
            sorted(
                (
                    tuple(sorted(permutation[index] for index in first)),
                    tuple(sorted(permutation[index] for index in second)),
                )
            )
        )
        candidates.append(transformed)
    return min(candidates)


def main() -> None:
    a, b, c = sp.symbols("a b c", nonzero=True)
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    x = sp.symbols("x0:5")
    u0 = (a, 1, 1, 0, 0)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    assert sp.Matrix([u0, u1, u2]).rank() == 3

    p0 = sp.factor(contracted_polynomial(u0, x))
    p1 = sp.factor(contracted_polynomial(u1, x))
    p2 = sp.factor(contracted_polynomial(u2, x))
    assert p0 == x[3] * x[4] * (
        a * x[1] * x[2] + x[0] * x[1] + x[0] * x[2]
    )
    assert p1 == x[1] * x[2] * x[4] * (b * x[3] + x[0])
    assert p2 == x[1] * x[2] * x[3] * (c * x[4] + x[0])

    h1 = sp.Matrix([b, 0, 0, -1, 0])
    h2 = sp.Matrix([c, 0, 0, 0, -1])
    factors1 = (
        sp.eye(5)[:, 1],
        sp.eye(5)[:, 2],
        sp.eye(5)[:, 4],
        sp.Matrix([1, 0, 0, b, 0]),
    )
    factors2 = (
        sp.eye(5)[:, 1],
        sp.eye(5)[:, 2],
        sp.eye(5)[:, 3],
        sp.Matrix([1, 0, 0, 0, c]),
    )
    assert all((h1.dot(factor) == 0) for factor in factors1)
    assert all((h2.dot(factor) == 0) for factor in factors2)
    assert sp.Matrix.hstack(h1, h2).rank() == 2

    quadratic = sp.Matrix([[0, 1, 1], [1, 0, a], [1, a, 0]])
    assert sp.factor(quadratic.det()) == 2 * a

    z = tuple(
        sp.expand(t0 * u0[index] + t1 * u1[index] + t2 * u2[index])
        for index in range(5)
    )
    assert z == (
        a * t0 + b * t1 + c * t2,
        t0,
        t0,
        t1,
        t2,
    )
    boundary = (
        ((0, c, -b), (0, 0, 0, c, -b)),
        ((c, 0, -a), (0, c, c, 0, -a)),
        ((b, -a, 0), (0, b, b, -a, 0)),
    )
    for target, expected in boundary:
        actual = tuple(
            sp.expand(
                target[0] * u0[index]
                + target[1] * u1[index]
                + target[2] * u2[index]
            )
            for index in range(5)
        )
        assert actual == expected
        assert sp.expand(
            a * target[0] + b * target[1] + c * target[2]
        ) == 0

    edges = tuple(itertools.combinations(range(4), 2))
    incidence_orbits = {
        canonical_edge_pair(first, second)
        for first in edges
        for second in edges
    }
    intersection_sizes = {
        len(set(first) & set(second))
        for first, second in incidence_orbits
    }
    assert len(incidence_orbits) == 3
    assert intersection_sizes == {0, 1, 2}

    matrix, words = off_diagonal_matrix(INTEGER_MAPS)
    assert matrix.shape == (78, 5)
    assert matrix.rank() == 4
    kernel = matrix.nullspace()
    assert len(kernel) == 1
    kernel_generator = kernel[0]
    assert kernel_generator == sp.Matrix([1, 1, 1, 1, 0])

    selected_words = (
        (0, 0, 0, 1),
        (0, 0, 1, 0),
        (0, 0, 1, 1),
        (1, 0, 0, 0),
    )
    row_indices = tuple(words.index(word) for word in selected_words)
    column_indices = (0, 1, 2, 4)
    minor = matrix.extract(row_indices, column_indices).det()
    assert minor == 128

    diagonal_matrix = sp.Matrix(
        [
            coefficient_vector(INTEGER_MAPS, (colour,) * 4)
            for colour in range(3)
        ]
    )
    diagonal_image = diagonal_matrix * kernel_generator
    assert diagonal_image == sp.Matrix([12, 12, 12])

    # Exclude every point of the published two-parameter support-four
    # family, not only its integer point.  The selected minors were
    # chosen by exact row reduction; the proof below is a two-variable
    # elimination, not an enumeration of maps.
    family_u, family_v, family_w = sp.symbols("family_u family_v family_w")
    relation = sp.expand(
        family_u * family_v * family_w
        - family_u * family_v
        - family_u * family_w
        - family_u
        - family_v * family_w
        - family_v
        - family_w
        - 1
    )
    family_matrix, family_words = off_diagonal_matrix(
        family_maps(family_u, family_v, family_w)
    )
    family_kernel_generator = sp.Matrix([1, 1, 1, 1, 0])
    for entry in family_matrix * family_kernel_generator:
        _, remainder = sp.div(entry, relation, family_w)
        assert sp.factor(remainder) == 0

    witness_rows = (
        (0, 1, 2, 3),
        (0, 1, 2, 26),
        (0, 2, 3, 5),
        (0, 1, 2, 9),
        (0, 2, 5, 8),
        (0, 1, 2, 4),
        (0, 1, 2, 27),
        (0, 2, 3, 26),
        (0, 2, 5, 11),
        (0, 2, 5, 14),
        (0, 8, 26, 70),
        (0, 2, 5, 6),
        (0, 2, 8, 26),
        (0, 1, 3, 26),
        (0, 1, 9, 26),
        (0, 2, 8, 29),
        (0, 1, 3, 27),
        (0, 2, 5, 32),
        (0, 2, 5, 26),
    )
    witness_columns = (0, 1, 2, 4)
    witness_minors = [
        sp.factor(
            family_matrix.extract(rows, witness_columns).det()
        )
        for rows in witness_rows
    ]
    denominator = sp.expand(
        family_u * family_v - family_u - family_v - 1
    )
    numerator = sp.expand((family_u + 1) * (family_v + 1))
    chart_numerators = [
        sp.factor(
            sp.together(
                minor.subs(family_w, numerator / denominator)
            ).as_numer_denom()[0]
        )
        for minor in witness_minors
    ]
    first_five_basis = sp.groebner(
        chart_numerators[:5],
        family_u,
        family_v,
        order="lex",
    )
    eliminant = sp.expand(
        family_v**4
        * (family_v - 2)
        * (family_v - 1) ** 2
        * (family_v + 1) ** 6
        * (family_v + 2)
        * (2 * family_v + 1)
        * (3 * family_v - 2)
        * (family_v**2 + family_v + 1)
    )
    assert (
        sp.Poly(
            first_five_basis.polys[-1].as_expr(), family_v
        ).monic()
        == sp.Poly(eliminant, family_v).monic()
    )

    rational_candidates = (
        sp.Integer(0),
        sp.Integer(1),
        sp.Integer(-1),
        sp.Integer(2),
        sp.Integer(-2),
        sp.Rational(-1, 2),
        sp.Rational(2, 3),
    )
    candidate_gcds = {}
    for value in rational_candidates:
        gcd = polynomial_gcd(
            [
                sp.factor(expression.subs(family_v, value))
                for expression in chart_numerators
            ],
            family_u,
        )
        candidate_gcds[str(value)] = str(gcd)
        if value == 0:
            assert gcd == (family_u + 1) ** 3
            assert sp.factor(denominator.subs(family_v, value)) == (
                -family_u - 1
            )
        elif value == -1:
            assert gcd == family_u**4
            assert sp.factor(denominator.subs(family_v, value)) == (
                -2 * family_u
            )
        else:
            assert gcd == 1

    cyclotomic_basis = sp.groebner(
        [family_v**2 + family_v + 1, *chart_numerators],
        family_u,
        family_v,
        order="grevlex",
    )
    assert any(
        polynomial.as_expr() == 1
        for polynomial in cyclotomic_basis.polys
    )

    denominator_zero_points = sp.solve_poly_system(
        [denominator, numerator], family_u, family_v
    )
    assert set(denominator_zero_points) == {(-1, 0), (0, -1)}
    exceptional_line_gcds = {}
    for point in denominator_zero_points:
        specialized = [
            sp.factor(
                minor.subs(
                    {family_u: point[0], family_v: point[1]}
                )
            )
            for minor in witness_minors
        ]
        gcd = polynomial_gcd(specialized, family_w)
        assert gcd == 1
        exceptional_line_gcds[str(point)] = str(gcd)

    output = {
        "verified": True,
        "field": "C",
        "normal_form_rank": 3,
        "noncoordinate_parameter_support_lower_bound": 2,
        "support_four_pencil_equation": "a*t0+b*t1+c*t2=0",
        "full_support_boundary_contraction_supports": [2, 3, 3],
        "singleton_p4_normals": [
            [str(entry) for entry in h1],
            [str(entry) for entry in h2],
        ],
        "minimal_two_edge_incidence_orbits": len(incidence_orbits),
        "incidence_intersection_sizes": sorted(intersection_sizes),
        "doubled_colour_quadratic_determinant": str(
            sp.factor(quadratic.det())
        ),
        "q4_required_off_diagonal_rank_upper_bound": 2,
        "known_support_four_off_diagonal_shape": list(matrix.shape),
        "known_support_four_off_diagonal_rank": matrix.rank(),
        "known_support_four_kernel": [
            [int(entry) for entry in kernel_generator]
        ],
        "known_support_four_diagonal_image": [
            int(entry) for entry in diagonal_image
        ],
        "transverse_minor_words": [list(word) for word in selected_words],
        "transverse_minor_missing_columns": list(column_indices),
        "transverse_minor_determinant": int(minor),
        "support_four_family_relation": str(relation),
        "support_four_family_witness_minors": len(witness_minors),
        "support_four_family_rank_drop_eliminant": str(
            sp.factor(eliminant)
        ),
        "support_four_family_rational_candidate_gcds": candidate_gcds,
        "support_four_family_cyclotomic_candidate_excluded": True,
        "support_four_family_denominator_zero_lines": [
            [int(entry) for entry in point]
            for point in denominator_zero_points
        ],
        "support_four_family_exceptional_line_gcds": exceptional_line_gcds,
        "known_support_four_family_all_off_diagonal_rank": 4,
        "known_support_four_family_q4_lift": False,
        "q4_211_excluded": False,
        "P5_to_Delta3_excluded": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_simultaneous_pencil_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
