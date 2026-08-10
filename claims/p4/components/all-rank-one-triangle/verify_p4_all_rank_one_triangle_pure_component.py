#!/usr/bin/env python3
"""Verify the all-rank-one relation-triangle ninth pure-P4 component."""

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
from krenn_gu.bootstrap import (  # noqa: E402
    bootstrap,
    expose_claim_package,
)

REPO_ROOT, HERE = bootstrap(__file__)
# Expose the two packages whose verifiers this script imports by bare
# name (disjoint-mixed-star moved in Stage 3; mixed-orientation moves
# in this batch).
expose_claim_package(REPO_ROOT, "claims/p4/components/disjoint-mixed-star")
expose_claim_package(REPO_ROOT, "claims/p4/components/mixed-orientation")
from verify_p4_disjoint_mixed_star_pure_component import (  # noqa: E402
    family as eighth_family,
)
from verify_p4_mixed_orientation_pure_component import (
    coefficients,
    directed_relation_signature,
    family_planes as sixth_family,
    jump_signature,
    known_samples,
    pair_data,
    product_matrix,
)


THEOREM = HERE / "P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md"
WORKING_NOTE = REPO_ROOT / "claims/p4/boundaries/inout-path-stratum/P4_INOUT_PATH_STRATUM_WORKING_NOTE.md"
EIGHTH = (
    REPO_ROOT / "claims" / "p4" / "components" / "disjoint-mixed-star"
    / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md")
RADICAL_STAR = (
    REPO_ROOT / "claims" / "p4" / "classifications" / "star"
    / "radical-star" / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md")
SEVENTH = (
    REPO_ROOT / "claims" / "p4" / "components" / "six-dimensional"
    / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md")
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
COORD_PAIRS = PAIRS
PIVOTS = ((1, 2), (1, 2), (0, 1), (0, 2))
SAMPLE = {
    "p": sp.Integer(2),
    "q": sp.Integer(3),
    "t0": sp.Integer(1),
    "t1": sp.Integer(1),
    "t2": sp.Integer(1),
}
FAMILY_MINOR_ROWS = (0, 1, 2, 3, 4)
EXPECTED_FAMILY_MINOR = sp.Integer(-1)
INCIDENCE_COLUMNS = (0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 17, 18, 19)
EXPECTED_INCIDENCE_MINOR = sp.Integer(860160)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family(p, q, scales=(1, 1, 1)):
    raw = (
        sp.Matrix(
            (
                (p * q + 1, 1, p, p * q + 1),
                (q + 1, 0, 1, q),
            )
        ),
        sp.Matrix(((p, 1, 0, 0), (0, 0, 1, -1))),
        sp.Matrix(((1, 0, -1, 0), (-p, 1, 0, 0))),
        sp.Matrix(((0, 0, 1, 1), (1, 0, 1, 0))),
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


def same_plane(left, right):
    left_pluecker = tuple(sp.factor(left[:, pair].det()) for pair in PAIRS)
    right_pluecker = tuple(sp.factor(right[:, pair].det()) for pair in PAIRS)
    pivot = next(
        index
        for index in range(6)
        if left_pluecker[index] != 0 and right_pluecker[index] != 0
    )
    return all(
        sp.simplify(
            left_pluecker[index] * right_pluecker[pivot]
            - right_pluecker[index] * left_pluecker[pivot]
        )
        == 0
        for index in range(6)
    )


def wall_branch_planes():
    """The x3=0 deep-stratum branch family of the in-out path chart."""
    d = sp.Symbol("d")
    v = sp.symbols("v0:4")
    x = sp.symbols("x0:4")
    alpha, beta = sp.symbols("alpha beta")
    u1 = (0, 0, 1, -1)
    y3 = (0, 0, 1, 1)
    u3 = (1, 0, d, 0)
    y2 = (1, 0, -d, 0)
    x0_val = -(d * v[0] * x[1] + v[1] * x[2]) / (d * v[1])
    substitution = {v[3]: -v[2], x[3]: 0, x[0]: x0_val}
    covector = (-d * v[1], -d * v[0], v[1], v[1])
    k1 = (-covector[1], covector[0], 0, 0)
    k2 = (-covector[2], 0, covector[0], 0)
    k3 = (-covector[3], 0, 0, covector[0])
    u0a = tuple(sp.expand(a + alpha * c) for a, c in zip(k1, k3))
    u0b = tuple(sp.expand(b + beta * c) for b, c in zip(k2, k3))

    def sub_row(row):
        return tuple(sp.sympify(value).subs(substitution) for value in row)

    planes = (
        sp.Matrix((u0a, u0b)),
        sp.Matrix((u1, sub_row(v))),
        sp.Matrix((sub_row(y2), sub_row(x))),
        sp.Matrix((y3, sub_row(u3))),
    )
    return planes, (d, v, x, alpha, beta)


def rank_three_data(planes):
    """Rank-3 edges, their relation ranks, and the edge-graph shape."""
    data = pair_data(planes)
    edges = tuple(sorted(edge for edge in PAIRS if data[edge][0] == 3))
    ranks = tuple(sorted(data[edge][1][0] for edge in edges))
    modes = set(mode for edge in edges for mode in edge)
    shape = "triangle" if len(edges) == 3 and len(modes) == 3 else "star"
    return edges, ranks, shape


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "lower bound is therefore nine" in theorem_text
    assert "not a classification" in theorem_text.lower()
    assert "directed three-cycle" in theorem_text
    assert "open" in theorem_text

    p, q, t0, t1, t2 = sp.symbols("p q t0 t1 t2")

    # The free family: single nonzero coefficient, identically.
    planes = family(p, q)
    assert all(plane.rank() == 2 for plane in planes)
    tensor = coefficients(planes)
    assert tensor[(1, 1, 1, 1)] == -2
    assert all(
        value == 0
        for word, value in tensor.items()
        if word != (1, 1, 1, 1)
    )
    scaled = family(p, q, (t0, t1, t2))
    scaled_tensor = coefficients(scaled)
    assert sp.factor(scaled_tensor[(1, 1, 1, 1)] + 2 * t0 * t1 * t2) == 0
    assert all(
        value == 0
        for word, value in scaled_tensor.items()
        if word != (1, 1, 1, 1)
    )

    # The three zero-product relations and their supports.
    y1 = tuple(planes[1].row(0))
    x1 = tuple(planes[1].row(1))
    y2 = tuple(planes[2].row(0))
    x2 = tuple(planes[2].row(1))
    y3 = tuple(planes[3].row(0))
    x3 = tuple(planes[3].row(1))
    relations = ((y1, x2), (x1, y3), (y2, x3))
    assert all(
        squarefree_product(left, right) == (0,) * 6
        for left, right in relations
    )
    support_pairs = tuple(support(left) for left, _right in relations)
    assert support_pairs == ((0, 1), (2, 3), (0, 2))
    assert tuple(support(right) for _left, right in relations) == (
        (0, 1),
        (2, 3),
        (0, 2),
    )

    # U_0 sits inside the covector kernel span(x_2, x_3, w).
    w = sp.Matrix([[1, 0, 0, 1]])
    kernel_frame = sp.Matrix.vstack(
        sp.Matrix([x2]), sp.Matrix([x3]), w
    )
    assert sp.Matrix.vstack(kernel_frame, planes[0]).rank() == 3
    assert same_plane(
        planes[0],
        sp.Matrix.vstack(
            sp.Matrix([x2]) + w, sp.Matrix([x3]) + q * w
        ),
    )
    y0 = sp.Matrix([x2]) + p * sp.Matrix([x3]) + (p * q + 1) * w
    assert all(
        sp.expand(value) == 0 for value in (y0 - planes[0].row(0))
    )

    # Exact chart transport from the deep x3=0 wall of the note.
    branch, (d, v, x, alpha, beta) = wall_branch_planes()
    gauge = sp.diag(d, alpha, 1, 1)
    p_value = sp.cancel(d * v[0] / (v[1] * alpha))
    transported = family(p_value, beta)
    assert all(
        same_plane(branch_plane * gauge, clean_plane)
        for branch_plane, clean_plane in zip(
            branch, transported, strict=True
        )
    )
    note_sample = {
        d: 2,
        v[0]: 3,
        v[1]: 5,
        v[2]: 7,
        x[1]: 11,
        x[2]: -4,
        alpha: sp.Rational(2, 3),
        beta: sp.Rational(-1, 2),
    }
    assert p_value.subs(note_sample) == sp.Rational(9, 5)

    # Pivot minors are unit monomials on the whole scaled family.
    pivot_minors = tuple(
        sp.factor(scaled[mode][:, PIVOTS[mode]].det())
        for mode in range(4)
    )
    assert pivot_minors == (
        t1 * t2,
        t1 * t2,
        t0 * t1,
        -t0 * t2,
    )

    sample = {
        symbol: SAMPLE[str(symbol)]
        for symbol in (p, q, t0, t1, t2)
    }
    point_planes = tuple(plane.subs(sample) for plane in scaled)
    assert all(plane.rank() == 2 for plane in point_planes)

    # Exact five-dimensional family tangent.
    reduced, chart_coordinates = reduce_in_charts(scaled)
    family_tangent = sp.Matrix(chart_coordinates).jacobian(
        (p, q, t0, t1, t2)
    ).subs(sample)
    family_tangent = sp.Matrix(
        [
            [sp.nsimplify(sp.cancel(entry)) for entry in row]
            for row in family_tangent.tolist()
        ]
    )
    family_minor = family_tangent.extract(
        FAMILY_MINOR_ROWS, tuple(range(5))
    ).det()
    assert family_tangent.rank() == 5
    assert family_minor == EXPECTED_FAMILY_MINOR

    # Independent local dimension upper bound in universal incidence.
    plane_variables = sp.symbols("z0:16")
    target_variables = sp.symbols("r0:4")
    universal = universal_planes(plane_variables)
    universal_tensor = coefficients(universal)
    reduced_point = tuple(plane.subs(sample) for plane in reduced)
    point_tensor = coefficients(reduced_point)
    anchor = (0, 1, 1, 0)
    assert point_tensor[anchor] != 0
    target_ratios = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        target_ratios.append(
            sp.nsimplify(
                point_tensor[tuple(adjacent)] / point_tensor[anchor]
            )
        )
    assert target_ratios == [sp.Rational(-1, 2), 0, 0, 0]
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
    coordinate_point = tuple(
        sp.nsimplify(sp.cancel(value.subs(sample)))
        for value in chart_coordinates
    )
    assert coordinate_point == (
        -1, 1, 4, 3, 2, 0, 0, -1, -1, 0, -2, 0, 0, -1, 0, 1
    )
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
    incidence_minor = incidence_jacobian[:, INCIDENCE_COLUMNS].det()
    assert incidence_jacobian.rank() == 15
    assert incidence_minor == EXPECTED_INCIDENCE_MINOR

    # Generic invariants: the all-rank-one triangle and orientations.
    pair_information = pair_data(point_planes)
    pair_profile = tuple(
        pair_information[edge][0] for edge in PAIRS
    )
    assert pair_profile == (4, 4, 4, 3, 3, 3)
    triangle_edges, relation_ranks, shape = rank_three_data(point_planes)
    assert triangle_edges == ((1, 2), (1, 3), (2, 3))
    assert relation_ranks == (1, 1, 1)
    assert shape == "triangle"
    assert directed_relation_signature(point_planes) == (
        3,
        0,
        (1, 1, 1, 0),
    )
    assert jump_signature(point_planes) == (1, 2)

    # Edge orientations: the relation factor proportional to the kernel
    # row marks the arrow head; the three heads form the cycle
    # 2 -> 1, 1 -> 3, 3 -> 2.
    heads = {}
    for left, right in triangle_edges:
        relation = product_matrix(
            point_planes[left], point_planes[right]
        ).nullspace()[0]
        matrix = sp.Matrix(2, 2, tuple(relation))
        row, column = next(
            (i, j)
            for i in range(2)
            for j in range(2)
            if matrix[i, j] != 0
        )
        left_vector = (matrix[:, column].T * point_planes[left])
        right_vector = (matrix[row, :] * point_planes[right])
        left_is_kernel = (
            sp.Matrix.vstack(
                left_vector, point_planes[left].row(0)
            ).rank()
            == 1
        )
        right_is_kernel = (
            sp.Matrix.vstack(
                right_vector, point_planes[right].row(0)
            ).rank()
            == 1
        )
        assert left_is_kernel != right_is_kernel
        heads[(left, right)] = left if left_is_kernel else right
    assert heads == {(1, 2): 1, (1, 3): 3, (2, 3): 2}

    # Certified samples of the earlier orbits and their separators.
    known = dict(known_samples())
    known["sixth"] = sixth_family(1, 2, 3)
    known["eighth"] = eighth_family(
        sp.Integer(-12),
        sp.Integer(-10),
        sp.Rational(3, 4),
        sp.Rational(-5, 28),
    )
    comparison = {}
    for name, sample_planes in known.items():
        edges, ranks, sample_shape = rank_three_data(sample_planes)
        comparison[name] = (
            sample_shape,
            ranks,
            jump_signature(sample_planes),
        )
    assert comparison["first"] == ("triangle", (1, 1, 2), (2, 1))
    assert comparison["second"] == ("star", (1, 1, 2), (1, 0))
    assert comparison["L1"] == ("star", (1, 1, 1), (1, 1))
    assert comparison["L2"] == ("star", (1, 1, 1), (0, 2))
    assert comparison["L3"] == ("star", (1, 1, 1), (0, 1))
    assert comparison["sixth"] == ("star", (1, 1, 1), (0, 1))
    assert comparison["eighth"] == ("star", (1, 1, 1), (1, 0))
    ninth_invariants = ("triangle", (1, 1, 1), (1, 2))
    assert all(
        value != ninth_invariants for value in comparison.values()
    )
    assert all(
        value[2] != ninth_invariants[2] for value in comparison.values()
    )

    result = {
        "verified": True,
        "field": "C",
        "method": (
            "gauge-reduced free rational normal form of the deep x3=0 "
            "wall, single-word permanent identity, and smooth Segre "
            "incidence"
        ),
        "pure_coefficients": {"1111": "-2"},
        "scaled_pure_coefficient": "-2*t0*t1*t2",
        "family_free": True,
        "family_parameters": ["p", "q"],
        "component_rational": True,
        "zero_product_relations": [
            "y1*x2",
            "x1*y3",
            "y2*x3",
        ],
        "relation_supports": ["01", "23", "02"],
        "orientation_cycle": "1->3->2->1",
        "wall_transport_verified": True,
        "wall_transport": "p=d*v0/(v1*alpha), q=beta",
        "note_sample_maps_to": ["9/5", "-1/2"],
        "sample": {key: str(value) for key, value in SAMPLE.items()},
        "Grassmann_pivots": [list(pivots) for pivots in PIVOTS],
        "pivot_minors": [str(value) for value in pivot_minors],
        "family_tangent_rank": 5,
        "family_tangent_minor_rows": list(FAMILY_MINOR_ROWS),
        "family_tangent_minor": str(family_minor),
        "incidence_anchor": "0110",
        "incidence_target_ratios": [str(value) for value in target_ratios],
        "incidence_jacobian_rank": 15,
        "incidence_tangent_dimension": 5,
        "incidence_minor_columns": list(INCIDENCE_COLUMNS),
        "incidence_minor": str(incidence_minor),
        "component_dimension": 5,
        "pair_profile": list(pair_profile),
        "rank_three_edges": [list(edge) for edge in triangle_edges],
        "rank_three_shape": "triangle",
        "relation_ranks": list(relation_ranks),
        "directed_relation_signature": [3, 0, [1, 1, 1, 0]],
        "jump_signature": [1, 2],
        "earlier_orbit_invariants": {
            name: {
                "rank_three_shape": value[0],
                "relation_ranks": list(value[1]),
                "jump_signature": list(value[2]),
            }
            for name, value in comparison.items()
        },
        "seventh_separated_by_dimension": True,
        "inequivalent_to_previous_eight": True,
        "certified_pure_component_orbit_count": 9,
        "generic_H31_excluded": False,
        "generic_weighted_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (
                THEOREM,
                WORKING_NOTE,
                EIGHTH,
                RADICAL_STAR,
                SEVENTH,
            )
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_all_rank_one_triangle_pure_component_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
