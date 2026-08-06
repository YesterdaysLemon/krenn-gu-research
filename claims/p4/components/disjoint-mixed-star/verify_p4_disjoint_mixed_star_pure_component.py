#!/usr/bin/env python3
"""Verify the disjoint mixed-star pure-P4 component."""

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

from verify_p4_mixed_orientation_pure_component import (  # noqa: E402
    coefficients,
    directed_relation_signature,
    family_planes as overlapping_family,
    jump_signature,
    pair_data,
    product_matrix,
)


THEOREM = HERE / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
OVERLAPPING = REPO_ROOT / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md"
PRIME_CLASSIFICATION = (
    REPO_ROOT / "P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md")
RADICAL_STAR = (
    REPO_ROOT / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md")
H31_OBSTRUCTION = (
    REPO_ROOT
    / "P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PIVOTS = ((0, 2), (0, 1), (0, 1), (0, 2))
SAMPLE = {
    "a": sp.Integer(-12),
    "b": sp.Integer(-10),
    "f": sp.Rational(3, 4),
    "phi": sp.Rational(-5, 28),
    "t0": sp.Integer(1),
    "t1": sp.Integer(1),
    "t2": sp.Integer(1),
}
EXPECTED_FAMILY_MINOR = sp.Rational(4129, 365226400)
EXPECTED_INCIDENCE_MINOR = sp.Rational(46800000, 34179505129)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relation(a, b, f, phi):
    return sp.expand(
        a**2 * b * f * phi**2
        + a**2 * f**2
        - b**2 * f**2
        + b**2 * phi**2
        - b * f
        - 1
    )


def family(a, b, f, phi, scales=(1, 1, 1)):
    j = f + b * phi**2
    kappa = phi * (b * f + 1)
    eta = -(b * f + 1)
    raw = (
        sp.Matrix(((0, 0, 1, -1), (a + b, a - b, 0, 2))),
        sp.Matrix(
            (
                (-a * f + 1, -a * f - 1, f + phi, f - phi),
                (1, 1, 0, 0),
            )
        ),
        sp.Matrix(
            (
                (
                    -a * j + eta,
                    -a * j - eta,
                    j + kappa,
                    j - kappa,
                ),
                (1, 1, 0, 0),
            )
        ),
        sp.Matrix(((1, -1, 0, 0), (0, 0, 1, 1))),
    )
    source = sp.diag(*scales, 1)
    return tuple(plane * source for plane in raw)


def reduce_in_charts(planes):
    reduced = []
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        chart = sp.simplify(plane[:, pivots].inv() * plane)
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        reduced.append(chart)
        coordinates.extend(
            chart[row, column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(reduced), tuple(coordinates)


def universal_planes(variables):
    result = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        plane = sp.zeros(2, 4)
        plane[0, pivots[0]] = 1
        plane[1, pivots[1]] = 1
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        result.append(plane)
    return tuple(result)


def squarefree_product(left, right):
    return tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i])
        for i, j in itertools.combinations(range(4), 2)
    )


def support(row):
    return tuple(index for index, value in enumerate(row) if value != 0)


def rank_one_relation_supports(planes):
    result = []
    for edge in itertools.combinations(range(4), 2):
        image_rank, relation_ranks = pair_data(planes)[edge]
        if image_rank != 3 or relation_ranks != (1,):
            continue
        left, right = edge
        relation = product_matrix(planes[left], planes[right]).nullspace()[0]
        matrix = sp.Matrix(2, 2, tuple(relation))
        row, column = next(
            (i, j)
            for i in range(2)
            for j in range(2)
            if matrix[i, j] != 0
        )
        left_factor = matrix[:, column]
        left_vector = tuple(left_factor.T * planes[left])
        result.append(support(left_vector))
    return tuple(result)


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "lower bound is therefore eight" in theorem_text
    assert "not a classification" in theorem_text.lower()
    assert "excludes the generic marked `H31` fibre" in theorem_text
    assert "generic weighted `H22` incidence" in theorem_text

    a, b, f, phi, t0, t1, t2 = sp.symbols(
        "a b f phi t0 t1 t2"
    )
    hypersurface = relation(a, b, f, phi)
    planes = family(a, b, f, phi)
    tensor = coefficients(planes)
    assert all(
        sp.factor(
            tensor[word]
            - {
                (1, 0, 0, 1): -4 * hypersurface,
                (1, 1, 1, 1): 4,
            }.get(word, 0)
        )
        == 0
        for word in WORDS
    )

    matrix = sp.Matrix(
        (
            (0, 1, phi),
            (b * f + 1, 1 - b * phi, f + phi),
            (a**2 * f + b, 0, b * f + 1),
        )
    )
    assert sp.factor(matrix.det() - hypersurface) == 0
    kernel_vector = sp.Matrix(
        (
            f + b * phi**2,
            phi * (b * f + 1),
            -(b * f + 1),
        )
    )
    assert all(
        sp.expand(value) == 0
        for value in matrix[:2, :] * kernel_vector
    )
    assert sp.factor((matrix[2, :] * kernel_vector)[0] - hypersurface) == 0

    leading = sp.factor(f * (b * phi**2 + f))
    constant = sp.factor(b**2 * f**2 - b**2 * phi**2 + b * f + 1)
    assert sp.gcd(leading, constant) == 1
    assert leading.as_poly(f).as_dict().get((1,), 0).subs(f, 0) != 0
    assert constant.subs(f, 0) == 1 - b**2 * phi**2 != 0
    assert sp.Poly(hypersurface, a, b, f, phi).is_irreducible

    sample = {
        symbol: SAMPLE[str(symbol)]
        for symbol in (a, b, f, phi, t0, t1, t2)
    }
    assert hypersurface.subs(sample) == 0
    assert sp.diff(hypersurface, phi).subs(sample) == 350
    point_planes = tuple(
        plane.subs(sample)
        for plane in family(a, b, f, phi, (t0, t1, t2))
    )
    assert all(plane.rank() == 2 for plane in point_planes)
    assert all(
        point_planes[mode][:, PIVOTS[mode]].det() != 0
        for mode in range(4)
    )

    # Exact five-dimensional family tangent on the hypersurface.
    scaled_planes = family(a, b, f, phi, (t0, t1, t2))
    reduced, chart_coordinates = reduce_in_charts(scaled_planes)
    ambient_jacobian = sp.Matrix(chart_coordinates).jacobian(
        (a, b, f, phi, t0, t1, t2)
    ).subs(sample)
    gradient = sp.Matrix(
        [
            sp.diff(hypersurface, variable).subs(sample)
            for variable in (a, b, f, phi)
        ]
    )
    tangent_columns = []
    for column in range(3):
        direction = sp.zeros(7, 1)
        direction[column, 0] = 1
        direction[3, 0] = -gradient[column] / gradient[3]
        tangent_columns.append(ambient_jacobian * direction)
    tangent_columns.extend(
        ambient_jacobian[:, column] for column in (4, 5, 6)
    )
    family_tangent = sp.Matrix.hstack(*tangent_columns)
    family_rows = (0, 1, 3, 4, 5)
    family_columns = (0, 1, 2, 3, 5)
    family_minor = sp.factor(
        family_tangent.extract(family_rows, family_columns).det()
    )
    assert family_tangent.rank() == 5
    assert family_minor == EXPECTED_FAMILY_MINOR

    # Independent local dimension upper bound in universal incidence.
    plane_variables = sp.symbols("z0:16")
    target_variables = sp.symbols("r0:4")
    universal = universal_planes(plane_variables)
    universal_tensor = coefficients(universal)
    reduced_point = tuple(plane.subs(sample) for plane in reduced)
    point_tensor = coefficients(reduced_point)
    anchor = (0, 0, 0, 1)
    assert point_tensor[anchor] != 0
    target_ratios = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        target_ratios.append(
            sp.factor(point_tensor[tuple(adjacent)] / point_tensor[anchor])
        )
    assert target_ratios == [0, sp.Rational(-5, 4), sp.Rational(44, 5), 0]
    incidence_equations = []
    for word in WORDS:
        if word == anchor:
            continue
        monomial = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != anchor[mode]
        )
        incidence_equations.append(
            sp.expand(
                universal_tensor[word] - universal_tensor[anchor] * monomial
            )
        )
    all_variables = (*plane_variables, *target_variables)
    coordinate_point = tuple(value.subs(sample) for value in chart_coordinates)
    incidence_point = coordinate_point + tuple(target_ratios)
    incidence_substitution = dict(
        zip(all_variables, incidence_point, strict=True)
    )
    assert all(
        equation.subs(incidence_substitution) == 0
        for equation in incidence_equations
    )
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(all_variables)
        .subs(incidence_substitution)
    )
    incidence_columns = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        13,
        14,
        16,
        19,
    )
    incidence_minor = sp.factor(
        incidence_jacobian[:, incidence_columns].det()
    )
    assert incidence_jacobian.rank() == 15
    assert incidence_minor == EXPECTED_INCIDENCE_MINOR

    # Generic geometry and the support-intersection invariant.
    pair_information = pair_data(point_planes)
    pair_profile = tuple(
        pair_information[edge][0]
        for edge in itertools.combinations(range(4), 2)
    )
    assert pair_profile == (4, 4, 3, 4, 3, 3)
    assert directed_relation_signature(point_planes) == (
        3,
        0,
        (2, 1, 0, 0),
    )
    assert jump_signature(point_planes) == (1, 0)
    raw_point = tuple(plane.subs(sample) for plane in planes)
    zero_products = (
        (raw_point[1].row(1), raw_point[3].row(0)),
        (raw_point[2].row(1), raw_point[3].row(0)),
        (raw_point[0].row(0), raw_point[3].row(1)),
    )
    assert all(
        squarefree_product(tuple(left), tuple(right)) == (0,) * 6
        for left, right in zero_products
    )
    support_pairs = tuple(
        support(tuple(left)) for left, _right in zero_products
    )
    assert support_pairs == ((0, 1), (0, 1), (2, 3))
    assert not set(support_pairs[0]) & set(support_pairs[2])
    overlapping_supports = rank_one_relation_supports(
        overlapping_family(1, 2, 3)
    )
    assert overlapping_supports == ((2, 3), (2, 3), (0, 2))
    assert len(set(overlapping_supports[0]) & set(overlapping_supports[2])) == 1

    result = {
        "verified": True,
        "field": "C",
        "method": (
            "squarefree zero-product support geometry, irreducible "
            "determinantal hypersurface, and smooth Segre incidence"
        ),
        "pure_coefficients": {
            "1001": "-4*Phi",
            "1111": "4",
        },
        "hypersurface": str(hypersurface),
        "hypersurface_irreducible": True,
        "kernel_matrix_determinant": str(sp.factor(matrix.det())),
        "sample": {key: str(value) for key, value in SAMPLE.items()},
        "Grassmann_pivots": [list(pivots) for pivots in PIVOTS],
        "family_tangent_rank": 5,
        "family_tangent_minor_rows": list(family_rows),
        "family_tangent_minor_columns": [
            "a",
            "b",
            "f",
            "t0",
            "t2",
        ],
        "family_tangent_minor": str(family_minor),
        "incidence_anchor": "0001",
        "incidence_target_ratios": [str(value) for value in target_ratios],
        "incidence_jacobian_rank": 15,
        "incidence_tangent_dimension": 5,
        "incidence_minor_columns": list(incidence_columns),
        "incidence_minor": str(incidence_minor),
        "component_dimension": 5,
        "pair_profile": list(pair_profile),
        "directed_relation_signature": [3, 0, [2, 1, 0, 0]],
        "diagonal_quadric_jump_signature": [1, 0],
        "zero_product_supports": [
            "".join(map(str, pair)) for pair in support_pairs
        ],
        "distinct_support_intersection_size": 0,
        "overlapping_component_distinct_support_intersection_size": 1,
        "inequivalent_to_previous_seven": True,
        "certified_pure_component_orbit_count": 8,
        "generic_H31_excluded": True,
        "generic_weighted_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (
                THEOREM,
                OVERLAPPING,
                PRIME_CLASSIFICATION,
                RADICAL_STAR,
                H31_OBSTRUCTION,
            )
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_disjoint_mixed_star_pure_component_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
