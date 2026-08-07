#!/usr/bin/env python3
"""Verify the second pure-rank-two P4 component theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md"
KNOWN_COMPONENT = REPO_ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
KNOWN_CLOSURE = REPO_ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
PERMUTATIONS = tuple(itertools.permutations(range(4)))
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: list[sp.Matrix] | tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def normal_form(
    A: sp.Expr,
    B: sp.Expr,
    C: sp.Expr,
    E: sp.Expr,
    F: sp.Expr,
    H: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    y1 = sp.Matrix([1, 0, 0, -1])
    y2 = sp.Matrix([0, 1, -1, 0])
    k0 = sp.Matrix([1, 0, 0, 1])
    k1 = sp.Matrix([0, 1, 1, 0])
    x1 = sp.Matrix([A, C + B, C - B, A])
    x2 = sp.Matrix([H + E, F, F, H - E])
    u0 = sp.Matrix([E, -F, -F, -E])
    u1 = sp.Matrix([A, -B, B, A])
    return (
        sp.Matrix.vstack(u0.T, u1.T),
        sp.Matrix.vstack(y1.T, x1.T),
        sp.Matrix.vstack(x2.T, y2.T),
        sp.Matrix.vstack(k0.T, k1.T),
    )


def coefficients(planes: tuple[sp.Matrix, ...]) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(
                tuple(planes[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in WORDS
    }


def chart_coordinates(
    planes: tuple[sp.Matrix, ...],
) -> tuple[tuple[sp.Matrix, ...], tuple[sp.Expr, ...]]:
    reduced = []
    coordinates = []
    for plane in planes:
        pivot = plane[:, (0, 1)]
        assert sp.factor(pivot.det()) != 0
        chart = sp.simplify(pivot.inv() * plane)
        reduced.append(chart)
        coordinates.extend((chart[0, 2], chart[0, 3], chart[1, 2], chart[1, 3]))
    return tuple(reduced), tuple(coordinates)


def diagonal_quadric_dimension(plane: sp.Matrix) -> int:
    line = plane.nullspace()
    assert len(line) == 2
    first, second = line
    restriction = sp.Matrix(
        (
            tuple(first[index] ** 2 for index in range(4)),
            tuple(2 * first[index] * second[index] for index in range(4)),
            tuple(second[index] ** 2 for index in range(4)),
        )
    )
    return 4 - restriction.rank()


def main() -> None:
    A, B, C, E, F, H = sp.symbols("A B C E F H")
    planes = normal_form(A, B, C, E, F, H)
    tensor = coefficients(planes)

    expected_nonzero = {
        (0, 1, 0, 0): -4 * F * (A * F + C * H),
        (0, 1, 0, 1): -4 * (A * F * H + C * E**2),
        (1, 1, 0, 0): 4 * (A * C * F + B**2 * H),
        (1, 1, 0, 1): 4 * A * (A * F + C * H),
    }
    assert all(
        sp.factor(tensor[word] - expected_nonzero.get(word, 0)) == 0
        for word in WORDS
    )
    active_matrix = sp.Matrix(
        (
            (
                tensor[(0, 1, 0, 0)],
                tensor[(0, 1, 0, 1)],
            ),
            (
                tensor[(1, 1, 0, 0)],
                tensor[(1, 1, 0, 1)],
            ),
        )
    )
    psi = sp.expand(
        A**3 * F**3
        + A**2 * C * F**2 * H
        - A * B**2 * F * H**2
        - A * C**2 * E**2 * F
        + A * C**2 * F * H**2
        - B**2 * C * E**2 * H
    )
    assert sp.factor(active_matrix.det() + 16 * psi) == 0
    assert sp.Poly(psi, A, B, C, E, F, H).total_degree() == 6

    P = sp.expand(
        A
        * F
        * (A**2 * F**2 + A * C * F * H - C**2 * E**2 + C**2 * H**2)
    )
    Q = sp.expand(H * (A * F * H + C * E**2))
    assert sp.expand(psi - (P - B**2 * Q)) == 0
    assert sp.gcd(P, Q) == 1
    assert sp.factor(psi) == psi
    leading_at_A = sp.factor(sp.cancel(P / A).subs(A, 0))
    denominator_at_A = sp.factor(Q.subs(A, 0))
    assert sp.expand(leading_at_A - C**2 * F * (-E + H) * (E + H)) == 0
    assert sp.expand(denominator_at_A - C * E**2 * H) == 0

    # The radical-plane derivation.
    y1 = sp.Matrix([1, 0, 0, -1])
    y2 = sp.Matrix([0, 1, -1, 0])
    k0 = sp.Matrix([1, 0, 0, 1])
    k1 = sp.Matrix([0, 1, 1, 0])
    standard = tuple(sp.eye(4).row(index) for index in range(4))
    double_contraction = sp.Matrix(
        4,
        4,
        lambda row, column: permanent(
            (standard[row], y1.T, y2.T, standard[column])
        ),
    )
    expected_double = sp.Matrix(
        (
            (0, 1, -1, 0),
            (1, 0, 0, -1),
            (-1, 0, 0, 1),
            (0, -1, 1, 0),
        )
    )
    assert double_contraction == expected_double
    assert double_contraction.rank() == 2
    assert double_contraction * k0 == sp.zeros(4, 1)
    assert double_contraction * k1 == sp.zeros(4, 1)

    # Rational component point.
    point_parameters = {A: 1, B: 1, C: 0, E: 2, F: 1, H: 1}
    assert psi.subs(point_parameters) == 0
    point_planes = tuple(plane.subs(point_parameters) for plane in planes)
    expected_planes = (
        sp.Matrix(((2, -1, -1, -2), (1, -1, 1, 1))),
        sp.Matrix(((1, 0, 0, -1), (1, 1, -1, 1))),
        sp.Matrix(((3, 1, 1, -1), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )
    assert point_planes == expected_planes
    assert all(plane[:, (0, 1)].det() != 0 for plane in point_planes)
    point_tensor = coefficients(point_planes)
    assert {
        word: value for word, value in point_tensor.items() if value != 0
    } == {
        (0, 1, 0, 0): -4,
        (0, 1, 0, 1): -4,
        (1, 1, 0, 0): 4,
        (1, 1, 0, 1): 4,
    }

    reduced_point, point_chart = chart_coordinates(point_planes)
    expected_chart = (
        -2,
        -3,
        -3,
        -4,
        0,
        -1,
        -1,
        2,
        sp.Rational(2, 3),
        sp.Rational(-1, 3),
        -1,
        0,
        0,
        1,
        1,
        0,
    )
    assert point_chart == expected_chart

    # Rank-five family tangent.  Work on B=F=1 and solve Psi=0 for H.
    t0, t1 = sp.symbols("t0 t1")
    family_planes = normal_form(A, 1, C, E, 1, H)
    source_scale = sp.diag(t0, t1, 1, 1)
    family_planes = tuple(plane * source_scale for plane in family_planes)
    family_reduced, family_chart = chart_coordinates(family_planes)
    family_variables = (A, C, E, H, t0, t1)
    family_base = {A: 1, C: 0, E: 2, H: 1, t0: 1, t1: 1}
    raw_family_jacobian = sp.Matrix(family_chart).jacobian(family_variables).subs(
        family_base
    )
    # dH/d(A,C,E)=(1,-3/2,0) follows from dPsi=0 at the point.
    implicit_chain = sp.Matrix(
        (
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 1, 0, 0),
            (1, sp.Rational(-3, 2), 0, 0, 0),
            (0, 0, 0, 1, 0),
            (0, 0, 0, 0, 1),
        )
    )
    family_tangent_planes = raw_family_jacobian * implicit_chain
    family_minor = family_tangent_planes.extract((0, 1, 2, 3, 6), range(5))
    assert family_minor.det() == -24
    assert family_tangent_planes.rank() == 5

    # Incidence equations in the all-01 Grassmann chart.
    plane_variables = sp.symbols("a0:16")
    chart_planes = []
    for mode in range(4):
        a, b, c, d = plane_variables[4 * mode : 4 * mode + 4]
        chart_planes.append(sp.Matrix(((1, 0, a, b), (0, 1, c, d))))
    chart_tensor = coefficients(tuple(chart_planes))
    z = sp.symbols("z0:4")
    all_variables = (*plane_variables, *z)
    anchor = (0, 1, 0, 0)
    equations = []
    equation_words = []
    for word in WORDS:
        if word == anchor:
            continue
        ratio = sp.prod(
            z[mode] for mode in range(4) if word[mode] != anchor[mode]
        )
        equations.append(
            sp.expand(chart_tensor[word] - chart_tensor[anchor] * ratio)
        )
        equation_words.append("".join(map(str, word)))

    point_z = (sp.Rational(3, 2), 0, 0, 1)
    incidence_point = (*point_chart, *point_z)
    incidence_substitution = dict(
        zip(all_variables, incidence_point, strict=True)
    )
    assert chart_tensor[anchor].subs(incidence_substitution) == sp.Rational(
        -8, 3
    )
    assert all(
        equation.subs(incidence_substitution) == 0 for equation in equations
    )
    incidence_jacobian = (
        sp.Matrix(equations).jacobian(all_variables).subs(incidence_substitution)
    )
    assert incidence_jacobian.rank() == 14
    minor_rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14)
    minor_columns = (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 15, 17, 18)
    incidence_minor = incidence_jacobian.extract(minor_rows, minor_columns)
    assert incidence_minor.det() == sp.Rational(1048576, 243)

    tangent = sp.Matrix(
        (
            15,
            21,
            21,
            33,
            -11,
            11,
            15,
            -21,
            4,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        )
    )
    cokernel = sp.Matrix(
        (9, 0, 6, 0, 0, 0, 0, -6, 0, -4, 0, 0, 0, 0, 0)
    )
    assert incidence_jacobian * tangent == sp.zeros(15, 1)
    assert incidence_jacobian.T * cokernel == sp.zeros(20, 1)

    # Include the target-factor derivatives in the family tangent.
    family_tensor = coefficients(family_reduced)
    family_anchor = family_tensor[anchor]
    family_z = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        family_z.append(
            sp.factor(family_tensor[tuple(adjacent)] / family_anchor)
        )
    family_incidence_map = sp.Matrix((*family_chart, *family_z))
    raw_family_incidence_jacobian = family_incidence_map.jacobian(
        family_variables
    ).subs(family_base)
    family_tangent = raw_family_incidence_jacobian * implicit_chain
    assert family_tangent.rank() == 5
    assert family_tangent.row_join(tangent).rank() == 6

    parameter = sp.symbols("tau")
    tangent_substitution = {
        variable: incidence_substitution[variable] + parameter * tangent[index]
        for index, variable in enumerate(all_variables)
    }
    quadratic_terms = sp.Matrix(
        [
            sp.expand(equation.subs(tangent_substitution)).coeff(parameter, 2)
            for equation in equations
        ]
    )
    quadratic_obstruction = sp.factor((cokernel.T * quadratic_terms)[0])
    assert quadratic_obstruction == -132

    new_quadric_dimensions = tuple(
        diagonal_quadric_dimension(plane) for plane in point_planes
    )
    assert new_quadric_dimensions == (1, 1, 1, 2)

    # Three planes in the known component lie on the closed block-line locus.
    a, d, e, h, n = sp.symbols("a d e h n", nonzero=True)
    D = d + h * n * e
    known_planes = (
        sp.Matrix(((1, 0, a, h * (a - n)), (0, 1, D / h, d))),
        sp.Matrix(((e, 1, 0, 0), (0, 0, 1, h))),
        sp.Matrix(((0, 1, 0, h * n * e), (-1 / n, 0, 1, 0))),
        sp.Matrix(((1, 0, n, 0), (0, 0, -1 / h, 1))),
    )
    known_block_dimensions = tuple(
        diagonal_quadric_dimension(plane) for plane in known_planes[1:]
    )
    assert all(dimension >= 2 for dimension in known_block_dimensions)

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "squarefree Frobenius algebra, diagonal quadrics, "
            "exact tangent-cone certificate"
        ),
        "normal_form_parameters": ["A", "B", "C", "E", "F", "H"],
        "parameter_hypersurface_bidegree": [3, 3],
        "parameter_hypersurface_irreducible": True,
        "nonzero_coefficient_words": [
            "".join(map(str, word)) for word in expected_nonzero
        ],
        "active_determinant_factor": "-16*Psi",
        "family_tangent_rank": family_tangent.rank(),
        "family_tangent_minor_determinant": int(family_minor.det()),
        "incidence_anchor": "0100",
        "incidence_anchor_coefficient": str(
            chart_tensor[anchor].subs(incidence_substitution)
        ),
        "incidence_jacobian_rank": incidence_jacobian.rank(),
        "incidence_tangent_dimension": 20 - incidence_jacobian.rank(),
        "incidence_minor_rows": [equation_words[index] for index in minor_rows],
        "incidence_minor_columns": [
            str(all_variables[index]) for index in minor_columns
        ],
        "incidence_minor_determinant": str(incidence_minor.det()),
        "family_plus_transverse_tangent_rank": family_tangent.row_join(
            tangent
        ).rank(),
        "quadratic_tangent_obstruction": int(quadratic_obstruction),
        "local_dimension": 5,
        "component_dimension": 5,
        "new_point_diagonal_quadric_dimensions": list(new_quadric_dimensions),
        "known_component_fixed_block_plane_dimensions": list(
            known_block_dimensions
        ),
        "distinct_from_known_component_orbit": True,
        "additional_component_exists": True,
        "new_component_marked_fibre_closed": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            KNOWN_COMPONENT.name: sha256(KNOWN_COMPONENT),
            KNOWN_CLOSURE.name: sha256(KNOWN_CLOSURE),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / "tmp" / "p4_diagonal_quadric_pure_component_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
