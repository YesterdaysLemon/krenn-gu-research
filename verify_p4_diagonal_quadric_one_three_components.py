#!/usr/bin/env python3
"""Verify three 1+3 diagonal-quadric pure-rank-two P4 components."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
KNOWN_FIRST = ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
KNOWN_SECOND = (
    ROOT / "claims" / "p4" / "components" / "diagonal-quadric"
    / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md")
PERMUTATIONS = tuple(itertools.permutations(range(4)))
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2), (0, 1), (0, 1), (1, 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...] | list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
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


def branch_planes(
    branch: str,
    S: sp.Expr,
    D: sp.Expr,
    G: sp.Expr,
    source_scales: tuple[sp.Expr, sp.Expr, sp.Expr] = (1, 1, 1),
) -> tuple[sp.Matrix, ...]:
    branch_t = {
        "L1": -D + G + S,
        "L2": D + G - S,
        "L3": -D - G - S,
    }
    T = branch_t[branch]
    P = G - T
    Q = D - S
    raw = (
        sp.Matrix(((2, P + Q, Q - P, 0), (0, 0, 1, 1))),
        sp.Matrix(((0, 1, -1, 0), (1, 0, S, D))),
        sp.Matrix(((1, 0, G, T), (0, 1, 0, -1))),
        sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
    )
    t0, t1, t2 = source_scales
    source_scale = sp.diag(t0, t1, t2, 1)
    return tuple(plane * source_scale for plane in raw)


def reduce_in_charts(
    planes: tuple[sp.Matrix, ...],
) -> tuple[tuple[sp.Matrix, ...], tuple[sp.Expr, ...]]:
    reduced: list[sp.Matrix] = []
    coordinates: list[sp.Expr] = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        pivot = plane[:, pivots]
        assert sp.factor(pivot.det()) != 0
        chart = sp.simplify(pivot.inv() * plane)
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        reduced.append(chart)
        coordinates.extend(
            chart[row, column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(reduced), tuple(coordinates)


def chart_planes(variables: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, ...]:
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


def diagonal_quadric_space(plane: sp.Matrix) -> tuple[sp.Matrix, ...]:
    annihilator_line = plane.nullspace()
    assert len(annihilator_line) == 2
    first, second = annihilator_line
    restriction = sp.Matrix(
        (
            tuple(first[index] ** 2 for index in range(4)),
            tuple(
                2 * first[index] * second[index] for index in range(4)
            ),
            tuple(second[index] ** 2 for index in range(4)),
        )
    )
    return tuple(restriction.nullspace())


def jump_signature(planes: tuple[sp.Matrix, ...]) -> tuple[int, int]:
    two_two = 0
    one_three = 0
    for plane in planes:
        quadrics = diagonal_quadric_space(plane)
        if len(quadrics) == 1:
            continue
        assert len(quadrics) == 2
        contained_in_coordinate_hyperplane = any(
            all(vector[index] == 0 for vector in quadrics)
            for index in range(4)
        )
        if contained_in_coordinate_hyperplane:
            one_three += 1
        else:
            two_two += 1
    return two_two, one_three


def pair_image_rank(left: sp.Matrix, right: sp.Matrix) -> int:
    squarefree_pairs = tuple(itertools.combinations(range(4), 2))
    products = []
    for left_row in range(2):
        for right_row in range(2):
            products.append(
                [
                    sp.expand(
                        left[left_row, i] * right[right_row, j]
                        + left[left_row, j] * right[right_row, i]
                    )
                    for i, j in squarefree_pairs
                ]
            )
    return sp.Matrix(products).rank()


def pair_profile(planes: tuple[sp.Matrix, ...]) -> tuple[int, ...]:
    return tuple(pair_image_rank(planes[i], planes[j]) for i, j in PAIRS)


def known_component_samples() -> tuple[tuple[sp.Matrix, ...], ...]:
    a, d, e, h, n = map(sp.Integer, (2, 3, 5, 7, 11))
    cap_d = d + h * n * e
    first = (
        sp.Matrix(((1, 0, a, h * (a - n)), (0, 1, cap_d / h, d))),
        sp.Matrix(((e, 1, 0, 0), (0, 0, 1, h))),
        sp.Matrix(((0, 1, 0, h * n * e), (-1 / n, 0, 1, 0))),
        sp.Matrix(((1, 0, n, 0), (0, 0, -1 / h, 1))),
    )
    second = (
        sp.Matrix(((2, -1, -1, -2), (1, -1, 1, 1))),
        sp.Matrix(((1, 0, 0, -1), (1, 1, -1, 1))),
        sp.Matrix(((3, 1, 1, -1), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )
    return first, second


def main() -> None:
    # The cubic Cremona map from a line to its generic diagonal quadric.
    line_first = sp.symbols("r0:4")
    line_second = sp.symbols("s0:4")
    restriction = sp.Matrix(
        (
            tuple(line_first[index] ** 2 for index in range(4)),
            tuple(
                2 * line_first[index] * line_second[index]
                for index in range(4)
            ),
            tuple(line_second[index] ** 2 for index in range(4)),
        )
    )
    plucker = {
        (i, j): sp.expand(
            line_first[i] * line_second[j]
            - line_first[j] * line_second[i]
        )
        for i, j in PAIRS
    }
    cubic_quadric = []
    for omitted in range(4):
        complement = tuple(index for index in range(4) if index != omitted)
        product = sp.prod(
            plucker[tuple(sorted(pair))]
            for pair in itertools.combinations(complement, 2)
        )
        cofactor = sp.factor(
            (-1) ** omitted * restriction[:, complement].det()
        )
        assert sp.factor(cofactor - 2 * (-1) ** omitted * product) == 0
        cubic_quadric.append((-1) ** omitted * product)
    assert all(
        sp.factor(entry) == 0
        for entry in restriction * sp.Matrix(cubic_quadric)
    )

    # The 1+3 radical plane.
    y1 = sp.Matrix([0, 1, -1, 0])
    y2 = sp.Matrix([0, 1, 0, -1])
    z1 = sp.Matrix([0, 1, 1, 0])
    z2 = sp.Matrix([0, 1, 0, 1])
    standard = tuple(sp.eye(4).row(index) for index in range(4))
    double_contraction = sp.Matrix(
        4,
        4,
        lambda row, column: permanent(
            (standard[row], y1.T, y2.T, standard[column])
        ),
    )
    expected_double = sp.Matrix(
        ((0, 1, -1, -1), (1, 0, 0, 0), (-1, 0, 0, 0), (-1, 0, 0, 0))
    )
    assert double_contraction == expected_double
    assert double_contraction.rank() == 2
    assert double_contraction * z1 == sp.zeros(4, 1)
    assert double_contraction * z2 == sp.zeros(4, 1)

    S, D, G, T = sp.symbols("S D G T")
    P = G - T
    Q = D - S
    u0 = sp.Matrix([2, P + Q, Q - P, 0])
    u1 = sp.Matrix([0, 0, 1, 1])
    covector_p = sp.Matrix([P, -1, 1, -1])
    covector_q = sp.Matrix([Q, -1, -1, 1])
    assert covector_p.dot(u0) == covector_p.dot(u1) == 0
    assert covector_q.dot(u0) == covector_q.dot(u1) == 0

    raw_planes = (
        sp.Matrix.vstack(u0.T, u1.T),
        sp.Matrix.vstack(y1.T, sp.Matrix([1, 0, S, D]).T),
        sp.Matrix.vstack(sp.Matrix([1, 0, G, T]).T, y2.T),
        sp.Matrix.vstack(z1.T, z2.T),
    )
    raw_tensor = coefficients(raw_planes)
    expected_nonzero = {
        (0, 1, 0, 0): 2 * D * (D + G - S + T),
        (0, 1, 0, 1): (
            D**2
            + 2 * D * G
            + 2 * D * T
            + G**2
            - 2 * G * T
            - S**2
            + T**2
        ),
        (1, 1, 0, 0): D + G + S + T,
        (1, 1, 0, 1): D + G + S + T,
    }
    assert all(
        sp.factor(raw_tensor[word] - expected_nonzero.get(word, 0)) == 0
        for word in WORDS
    )
    active = sp.Matrix(
        (
            (raw_tensor[(0, 1, 0, 0)], raw_tensor[(0, 1, 0, 1)]),
            (raw_tensor[(1, 1, 0, 0)], raw_tensor[(1, 1, 0, 1)]),
        )
    )
    linear_factors = (
        D - G - S + T,
        D + G - S - T,
        D + G + S + T,
    )
    assert sp.factor(active.det() - sp.prod(linear_factors)) == 0

    branch_expected = {
        "L1": {
            (0, 1, 0, 0): 4 * D * G,
            (0, 1, 0, 1): 4 * D * G,
            (1, 1, 0, 0): 2 * (G + S),
            (1, 1, 0, 1): 2 * (G + S),
        },
        "L2": {
            (0, 1, 0, 0): 4 * D * (D + G - S),
            (0, 1, 0, 1): 4 * D * (D + G - S),
            (1, 1, 0, 0): 2 * (D + G),
            (1, 1, 0, 1): 2 * (D + G),
        },
        "L3": {
            (0, 1, 0, 0): -4 * D * S,
            (0, 1, 0, 1): 4 * G * (D + G + S),
        },
    }
    for branch, expected in branch_expected.items():
        tensor = coefficients(branch_planes(branch, S, D, G))
        assert all(
            sp.factor(tensor[word] - expected.get(word, 0)) == 0
            for word in WORDS
        )

    samples = {
        "L1": (sp.Integer(1), sp.Integer(3), sp.Integer(4)),
        "L2": (sp.Integer(1), sp.Integer(3), sp.Integer(4)),
        "L3": (sp.Integer(1), sp.Integer(2), sp.Integer(3)),
    }
    expected_raw_planes = {
        "L1": (
            sp.Matrix(((2, 4, 0, 0), (0, 0, 1, 1))),
            sp.Matrix(((0, 1, -1, 0), (1, 0, 1, 3))),
            sp.Matrix(((1, 0, 4, 2), (0, 1, 0, -1))),
            sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
        ),
        "L2": (
            sp.Matrix(((2, 0, 4, 0), (0, 0, 1, 1))),
            sp.Matrix(((0, 1, -1, 0), (1, 0, 1, 3))),
            sp.Matrix(((1, 0, 4, 6), (0, 1, 0, -1))),
            sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
        ),
        "L3": (
            sp.Matrix(((2, 10, -8, 0), (0, 0, 1, 1))),
            sp.Matrix(((0, 1, -1, 0), (1, 0, 1, 2))),
            sp.Matrix(((1, 0, 3, -6), (0, 1, 0, -1))),
            sp.Matrix(((0, 1, 1, 0), (0, 1, 0, 1))),
        ),
    }
    for branch, values in samples.items():
        point_planes = branch_planes(branch, *values)
        assert point_planes == expected_raw_planes[branch]
        assert all(plane.rank() == 2 for plane in point_planes)
        assert any(value != 0 for value in coefficients(point_planes).values())

    # Family tangent certificates in the mixed Grassmann charts.
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    family_variables = (S, D, G, t0, t1, t2)
    expected_family_certificates = {
        "L1": ((0, 3, 4, 5, 8), (0, 1, 2, 4, 5), -2),
        "L2": ((1, 3, 4, 6, 8), (0, 1, 2, 4, 5), -1),
        "L3": ((0, 1, 3, 4, 5), (0, 1, 2, 4, 5), 5),
    }
    family_data = {}
    for branch, values in samples.items():
        family = branch_planes(branch, S, D, G, (t0, t1, t2))
        reduced, coordinates = reduce_in_charts(family)
        base = {
            S: values[0],
            D: values[1],
            G: values[2],
            t0: 1,
            t1: 1,
            t2: 1,
        }
        jacobian = sp.Matrix(coordinates).jacobian(family_variables).subs(base)
        rows, columns, expected_determinant = expected_family_certificates[
            branch
        ]
        minor = jacobian.extract(rows, columns)
        assert minor.det() == expected_determinant
        assert jacobian.rank() == 5
        family_data[branch] = {
            "reduced": reduced,
            "coordinates": coordinates,
            "base": base,
            "rank": jacobian.rank(),
            "minor_rows": rows,
            "minor_columns": columns,
            "minor_determinant": int(minor.det()),
        }

    # Smooth five-dimensional Segre-incidence certificates.
    plane_variables = sp.symbols("a0:16")
    z = sp.symbols("z0:4")
    all_variables = (*plane_variables, *z)
    universal_planes = chart_planes(plane_variables)
    universal_tensor = coefficients(universal_planes)
    anchor = (0, 0, 0, 0)
    equations = []
    equation_words = []
    for word in WORDS:
        if word == anchor:
            continue
        ratio = sp.prod(z[mode] for mode in range(4) if word[mode] == 1)
        equations.append(
            sp.expand(universal_tensor[word] - universal_tensor[anchor] * ratio)
        )
        equation_words.append("".join(map(str, word)))
    expected_incidence_columns = {
        "L1": (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 17, 18, 19),
        "L2": (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 17, 18, 19),
        "L3": (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 14, 16, 17, 18),
    }
    expected_incidence_determinants = {
        "L1": 163840,
        "L2": 6193152,
        "L3": -737280,
    }
    incidence_data = {}
    for branch in samples:
        reduced = family_data[branch]["reduced"]
        coordinates = family_data[branch]["coordinates"]
        base = family_data[branch]["base"]
        reduced_tensor = coefficients(reduced)
        target_ratios = []
        for mode in range(4):
            adjacent = list(anchor)
            adjacent[mode] = 1
            target_ratios.append(
                sp.factor(
                    reduced_tensor[tuple(adjacent)] / reduced_tensor[anchor]
                )
            )
        point = tuple(entry.subs(base) for entry in coordinates) + tuple(
            entry.subs(base) for entry in target_ratios
        )
        substitution = dict(zip(all_variables, point, strict=True))
        assert universal_tensor[anchor].subs(substitution) != 0
        assert all(equation.subs(substitution) == 0 for equation in equations)
        jacobian = (
            sp.Matrix(equations).jacobian(all_variables).subs(substitution)
        )
        columns = expected_incidence_columns[branch]
        minor = jacobian[:, columns]
        assert jacobian.rank() == 15
        assert minor.det() == expected_incidence_determinants[branch]
        incidence_data[branch] = {
            "point": point,
            "anchor_coefficient": universal_tensor[anchor].subs(substitution),
            "target_ratios": tuple(entry.subs(base) for entry in target_ratios),
            "rank": jacobian.rank(),
            "columns": columns,
            "determinant": int(minor.det()),
        }

    # Generic jump signatures and pair-image profiles separate all five orbits.
    first_known, second_known = known_component_samples()
    component_samples = {
        "known_first": first_known,
        "known_second": second_known,
        **{
            branch: branch_planes(branch, *values)
            for branch, values in samples.items()
        },
    }
    signatures = {
        name: jump_signature(planes)
        for name, planes in component_samples.items()
    }
    expected_signatures = {
        "known_first": (2, 1),
        "known_second": (1, 0),
        "L1": (1, 1),
        "L2": (0, 2),
        "L3": (0, 1),
    }
    assert signatures == expected_signatures
    assert len(set(signatures.values())) == len(signatures)

    profiles = {
        name: pair_profile(planes)
        for name, planes in component_samples.items()
    }
    assert profiles["known_first"] == (4, 4, 4, 3, 3, 3)
    for name in ("known_second", "L1", "L2", "L3"):
        assert profiles[name] == (4, 4, 3, 4, 3, 3)
    for profile in profiles.values():
        for left, right in ((0, 5), (1, 4), (2, 3)):
            assert profile[left] + profile[right] <= 7

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "squarefree Frobenius algebra, cubic diagonal-quadric map, "
            "radical-plane factorization, and smooth incidence certificates"
        ),
        "cubic_diagonal_quadric_map_verified": True,
        "double_contraction_rank": double_contraction.rank(),
        "active_determinant_factors": [
            "D-G-S+T",
            "D+G-S-T",
            "D+G+S+T",
        ],
        "branches": {
            branch: {
                "sample_parameters": [int(value) for value in samples[branch]],
                "family_tangent_rank": family_data[branch]["rank"],
                "family_tangent_minor_rows": list(
                    family_data[branch]["minor_rows"]
                ),
                "family_tangent_minor_columns": [
                    str(family_variables[index])
                    for index in family_data[branch]["minor_columns"]
                ],
                "family_tangent_minor_determinant": family_data[branch][
                    "minor_determinant"
                ],
                "incidence_anchor": "0000",
                "incidence_anchor_coefficient": str(
                    incidence_data[branch]["anchor_coefficient"]
                ),
                "target_ratios": [
                    str(entry)
                    for entry in incidence_data[branch]["target_ratios"]
                ],
                "incidence_jacobian_rank": incidence_data[branch]["rank"],
                "incidence_tangent_dimension": (
                    20 - incidence_data[branch]["rank"]
                ),
                "incidence_minor_columns": [
                    str(all_variables[index])
                    for index in incidence_data[branch]["columns"]
                ],
                "incidence_minor_determinant": incidence_data[branch][
                    "determinant"
                ],
                "jump_signature_two_two_one_three": list(
                    signatures[branch]
                ),
                "pair_image_profile_01_02_03_12_13_23": list(
                    profiles[branch]
                ),
                "component_dimension": 5,
            }
            for branch in samples
        },
        "known_component_jump_signatures": {
            name: list(signatures[name])
            for name in ("known_first", "known_second")
        },
        "three_new_symmetry_inequivalent_components": True,
        "known_pure_component_orbits_at_least": 5,
        "all_pure_components_classified": False,
        "new_components_marked_H31_fibres_closed": False,
        "H31_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            KNOWN_FIRST.name: sha256(KNOWN_FIRST),
            KNOWN_SECOND.name: sha256(KNOWN_SECOND),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_diagonal_quadric_one_three_components_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
