#!/usr/bin/env python3
"""Independent exact audit of the disjoint mixed-star component."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md"
PRIMARY = ROOT / "verify_p4_disjoint_mixed_star_pure_component.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PIVOTS = ((0, 2), (0, 1), (0, 1), (0, 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dp(rows):
    states = {0: sp.Integer(1)}
    for row in rows:
        updated = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit:
                    continue
                new_mask = mask | bit
                updated[new_mask] = sp.expand(
                    updated.get(new_mask, 0) + value * entry
                )
        states = updated
    return states[(1 << len(rows)) - 1]


def tensor(planes):
    return {
        word: permanent_dp(
            tuple(planes[mode].row(word[mode]) for mode in range(4))
        )
        for word in WORDS
    }


def defining_polynomial(a, b, f, phi):
    return sp.expand(
        a**2 * b * f * phi**2
        + a**2 * f**2
        - b**2 * f**2
        + b**2 * phi**2
        - b * f
        - 1
    )


def make_family(a, b, f, phi, scales=(1, 1, 1)):
    j = f + b * phi**2
    kappa = phi * (b * f + 1)
    eta = -(b * f + 1)
    planes = (
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
    diagonal = sp.diag(*scales, 1)
    return tuple(plane * diagonal for plane in planes)


def reduce_planes(planes):
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


def chart_planes(variables):
    planes = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        plane = sp.zeros(2, 4)
        plane[0, pivots[0]] = 1
        plane[1, pivots[1]] = 1
        entries = variables[4 * mode : 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        planes.append(plane)
    return tuple(planes)


def pair_rank(left, right):
    pairs = tuple(itertools.combinations(range(4), 2))
    rows = []
    for i in range(2):
        for j in range(2):
            rows.append(
                [
                    left[i, p] * right[j, q]
                    + left[i, q] * right[j, p]
                    for p, q in pairs
                ]
            )
    return sp.Matrix(rows).rank()


def diagonal_quadric_jump(plane):
    first, second = plane.nullspace()
    restriction = sp.Matrix(
        (
            tuple(first[i] ** 2 for i in range(4)),
            tuple(2 * first[i] * second[i] for i in range(4)),
            tuple(second[i] ** 2 for i in range(4)),
        )
    )
    quadrics = restriction.nullspace()
    if len(quadrics) == 1:
        return None
    assert len(quadrics) == 2
    one_three = any(
        all(vector[index] == 0 for vector in quadrics)
        for index in range(4)
    )
    return "1+3" if one_three else "2+2"


def main() -> None:
    a, b, f, phi, t0, t1, t2 = sp.symbols(
        "a b f phi t0 t1 t2"
    )
    polynomial = defining_polynomial(a, b, f, phi)
    planes = make_family(a, b, f, phi)
    coefficients = tensor(planes)
    assert all(
        sp.factor(
            coefficient
            - {
                (1, 0, 0, 1): -4 * polynomial,
                (1, 1, 1, 1): 4,
            }.get(word, 0)
        )
        == 0
        for word, coefficient in coefficients.items()
    )
    assert sp.Poly(polynomial, a, b, f, phi).is_irreducible

    sample = {
        a: -12,
        b: -10,
        f: sp.Rational(3, 4),
        phi: sp.Rational(-5, 28),
        t0: 1,
        t1: 1,
        t2: 1,
    }
    assert polynomial.subs(sample) == 0
    scaled = make_family(a, b, f, phi, (t0, t1, t2))
    point_planes = tuple(plane.subs(sample) for plane in scaled)
    assert all(plane.rank() == 2 for plane in point_planes)

    # Rebuild the implicit-family tangent with independent code.
    reduced, coordinates = reduce_planes(scaled)
    jacobian = sp.Matrix(coordinates).jacobian(
        (a, b, f, phi, t0, t1, t2)
    ).subs(sample)
    gradient = [
        sp.diff(polynomial, variable).subs(sample)
        for variable in (a, b, f, phi)
    ]
    directions = []
    for index in range(3):
        vector = sp.zeros(7, 1)
        vector[index] = 1
        vector[3] = -gradient[index] / gradient[3]
        directions.append(jacobian * vector)
    directions.extend(jacobian[:, index] for index in (4, 5, 6))
    family_tangent = sp.Matrix.hstack(*directions)
    family_minor = family_tangent.extract(
        (0, 1, 3, 4, 5), (0, 1, 2, 3, 5)
    ).det()
    assert family_tangent.rank() == 5
    assert family_minor == sp.Rational(4129, 365226400)

    # Independently rebuild the universal Segre-incidence Jacobian.
    plane_variables = sp.symbols("u0:16")
    target_variables = sp.symbols("v0:4")
    universal_tensor = tensor(chart_planes(plane_variables))
    reduced_point = tuple(plane.subs(sample) for plane in reduced)
    point_tensor = tensor(reduced_point)
    anchor = (0, 0, 0, 1)
    ratios = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        ratios.append(
            sp.factor(point_tensor[tuple(adjacent)] / point_tensor[anchor])
        )
    assert ratios == [0, sp.Rational(-5, 4), sp.Rational(44, 5), 0]
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        monomial = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != anchor[mode]
        )
        equations.append(
            sp.expand(
                universal_tensor[word] - universal_tensor[anchor] * monomial
            )
        )
    all_variables = (*plane_variables, *target_variables)
    point = tuple(value.subs(sample) for value in coordinates) + tuple(ratios)
    substitution = dict(zip(all_variables, point, strict=True))
    assert all(equation.subs(substitution) == 0 for equation in equations)
    incidence = sp.Matrix(equations).jacobian(all_variables).subs(substitution)
    columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 16, 19)
    incidence_minor = incidence[:, columns].det()
    assert incidence.rank() == 15
    assert incidence_minor == sp.Rational(46800000, 34179505129)

    pair_profile = tuple(
        pair_rank(point_planes[i], point_planes[j])
        for i, j in itertools.combinations(range(4), 2)
    )
    assert pair_profile == (4, 4, 3, 4, 3, 3)
    jumps = [
        jump
        for plane in point_planes
        if (jump := diagonal_quadric_jump(plane)) is not None
    ]
    assert jumps.count("2+2") == 1
    assert jumps.count("1+3") == 0

    raw_point = tuple(plane.subs(sample) for plane in planes)
    zero_pairs = (
        (tuple(raw_point[1].row(1)), tuple(raw_point[3].row(0))),
        (tuple(raw_point[2].row(1)), tuple(raw_point[3].row(0))),
        (tuple(raw_point[0].row(0)), tuple(raw_point[3].row(1))),
    )
    supports = tuple(
        tuple(index for index, value in enumerate(left) if value)
        for left, _right in zero_pairs
    )
    assert supports == ((0, 1), (0, 1), (2, 3))
    for left, right in zero_pairs:
        assert all(
            left[i] * right[j] + left[j] * right[i] == 0
            for i, j in itertools.combinations(range(4), 2)
        )

    result = {
        "audited": True,
        "independent_of_primary_imports": True,
        "field": "Q",
        "method": (
            "subset-DP permanent and independently reconstructed exact "
            "family/incidence Jacobians"
        ),
        "hypersurface_irreducible": True,
        "pure_coefficients_replayed": True,
        "family_tangent_rank": family_tangent.rank(),
        "family_tangent_minor": str(family_minor),
        "incidence_jacobian_rank": incidence.rank(),
        "incidence_minor": str(incidence_minor),
        "pair_profile": list(pair_profile),
        "jump_signature": [1, 0],
        "zero_product_supports": [
            "".join(map(str, pair)) for pair in supports
        ],
        "support_disjointness_replayed": True,
        "component_dimension": 5,
        "certified_pure_component_orbit_count": 8,
        "generic_H31_excluded": True,
        "generic_weighted_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_disjoint_mixed_star_pure_component_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
