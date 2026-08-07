#!/usr/bin/env python3
"""Verify the six-dimensional pure-P4 compression component."""

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
THEOREM = HERE / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md"
MIXED = (
    REPO_ROOT / "claims" / "p4" / "components" / "mixed-orientation"
    / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md")
RADICAL_STAR = (
    REPO_ROOT / "claims" / "p4" / "classifications" / "star"
    / "radical-star" / "P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md")
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 2), (0, 2), (0, 1), (0, 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def coefficients(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: sp.factor(
            permanent(
                tuple(planes[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in WORDS
    }


def family_planes(
    a: sp.Expr,
    c: sp.Expr,
    d: sp.Expr,
    b: sp.Expr,
    e: sp.Expr,
    scales: tuple[sp.Expr, sp.Expr, sp.Expr] = (1, 1, 1),
) -> tuple[sp.Matrix, ...]:
    h = a + c - d
    planes = (
        sp.Matrix(((1, 0, 0, -1), (0, 0, 1, 1))),
        sp.Matrix(
            ((1, b, 0, 1 - b * h), (0, e, 1, 1 - e * h))
        ),
        sp.Matrix(((1, 0, -1, 0), (0, 1, -a - c, -d))),
        sp.Matrix(((1, 0, 0, 1), (0, 0, 1, -1))),
    )
    source_scale = sp.diag(*scales, 1)
    return tuple(plane * source_scale for plane in planes)


def lower_prime_planes(
    a: sp.Expr,
    c: sp.Expr,
    d: sp.Expr,
) -> tuple[sp.Matrix, ...]:
    return (
        sp.Matrix(((1, 0, 1, 0), (-1, 0, 0, 1))),
        sp.Matrix(((0, 0, 1, 1), (a, 1, c, d))),
        sp.Matrix(((-a - c, 1, 0, -d), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )


def reduce_in_charts(
    planes: tuple[sp.Matrix, ...],
) -> tuple[tuple[sp.Matrix, ...], tuple[sp.Expr, ...]]:
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


def chart_planes(variables: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, ...]:
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


def product_matrix(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = []
    for left_row in range(2):
        for right_row in range(2):
            columns.append(
                sp.Matrix(
                    tuple(
                        left[left_row, first] * right[right_row, second]
                        + left[left_row, second] * right[right_row, first]
                        for first, second in PAIRS
                    )
                )
            )
    return sp.Matrix.hstack(*columns)


def pair_data(
    planes: tuple[sp.Matrix, ...],
) -> dict[tuple[int, int], tuple[int, tuple[int, ...]]]:
    result = {}
    for left, right in PAIRS:
        matrix = product_matrix(planes[left], planes[right])
        result[left, right] = (
            matrix.rank(),
            tuple(
                sp.Matrix(2, 2, tuple(vector)).rank()
                for vector in matrix.nullspace()
            ),
        )
    return result


def diagonal_quadric_space(plane: sp.Matrix) -> tuple[sp.Matrix, ...]:
    first, second = plane.nullspace()
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
        if any(
            all(vector[index] == 0 for vector in quadrics)
            for index in range(4)
        ):
            one_three += 1
        else:
            two_two += 1
    return two_two, one_three


def same_plane(left: sp.Matrix, right: sp.Matrix) -> bool:
    left_coordinates = tuple(
        sp.factor(left[:, pair].det()) for pair in PAIRS
    )
    right_coordinates = tuple(
        sp.factor(right[:, pair].det()) for pair in PAIRS
    )
    pivot = next(
        index
        for index in range(6)
        if left_coordinates[index] != 0 and right_coordinates[index] != 0
    )
    return all(
        sp.factor(
            left_coordinates[index] * right_coordinates[pivot]
            - right_coordinates[index] * left_coordinates[pivot]
        )
        == 0
        for index in range(6)
    )


def main() -> None:
    a, c, d, b, e = sp.symbols("a c d b e")
    planes = family_planes(a, c, d, b, e)
    tensor = coefficients(planes)
    expected = {
        (1, 0, 1, 0): 2 * (1 - b * (a + c)),
        (1, 1, 1, 0): 2 * (1 - e * (a + c)),
    }
    observed = {
        word: sp.factor(value)
        for word, value in tensor.items()
        if value != 0
    }
    assert set(observed) == set(expected)
    assert all(
        sp.factor(observed[word] - expected[word]) == 0
        for word in expected
    )

    t0, t1, t2 = sp.symbols("t0 t1 t2")
    parameters = (a, c, d, b, e, t0, t1, t2)
    scaled = family_planes(a, c, d, b, e, (t0, t1, t2))
    reduced, family_coordinates = reduce_in_charts(scaled)
    reduced_tensor = coefficients(reduced)
    anchor = (1, 0, 1, 0)
    family_ratios = []
    for mode in range(4):
        adjacent = list(anchor)
        adjacent[mode] = 1 - adjacent[mode]
        family_ratios.append(
            sp.factor(
                reduced_tensor[tuple(adjacent)] / reduced_tensor[anchor]
            )
        )
    expected_ratios = [
        0,
        t0 * (e * (a + c) - 1) / (t2 * (b * (a + c) - 1)),
        0,
        0,
    ]
    assert all(
        sp.factor(observed_value - expected_value) == 0
        for observed_value, expected_value in zip(
            family_ratios, expected_ratios, strict=True
        )
    )

    base = {
        a: 1,
        c: 2,
        d: 4,
        b: 1,
        e: 2,
        t0: 1,
        t1: 1,
        t2: 1,
    }
    family_map = sp.Matrix((*family_coordinates, *family_ratios))
    family_jacobian = family_map.jacobian(parameters).subs(base)
    family_rows = (1, 3, 4, 5, 6, 10)
    family_columns = (0, 2, 3, 4, 5, 7)
    family_minor = family_jacobian.extract(
        family_rows, family_columns
    )
    assert family_jacobian.rank() == 6
    assert family_minor.det() == 1

    sample = tuple(plane.subs(base) for plane in scaled)
    reduced_sample, sample_coordinates = reduce_in_charts(sample)
    sample_tensor = coefficients(reduced_sample)
    ratios = tuple(value.subs(base) for value in family_ratios)
    assert sample_tensor[anchor] == -4
    assert ratios == (0, sp.Rational(5, 2), 0, 0)

    chart_variables = sp.symbols("x0:16")
    target_variables = sp.symbols("z0:4")
    all_variables = chart_variables + target_variables
    chart_tensor = coefficients(chart_planes(chart_variables))
    equations = []
    for word in WORDS:
        if word == anchor:
            continue
        product = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != anchor[mode]
        )
        equations.append(
            sp.expand(chart_tensor[word] - chart_tensor[anchor] * product)
        )
    substitution = dict(
        zip(
            all_variables,
            (*sample_coordinates, *ratios),
            strict=True,
        )
    )
    assert all(equation.subs(substitution) == 0 for equation in equations)
    incidence_jacobian = sp.Matrix(equations).jacobian(
        all_variables
    ).subs(substitution)
    incidence_rows = tuple(range(14))
    incidence_columns = (
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        8,
        9,
        12,
        14,
        16,
        18,
        19,
    )
    incidence_minor = incidence_jacobian.extract(
        incidence_rows, incidence_columns
    )
    assert incidence_jacobian.rank() == 14
    assert incidence_minor.det() == -215040

    profile_data = pair_data(sample)
    pair_profile = tuple(
        profile_data[pair][0] for pair in PAIRS
    )
    relation_ranks = {
        pair: profile_data[pair][1]
        for pair in PAIRS
        if profile_data[pair][0] < 4
    }
    assert pair_profile == (4, 3, 2, 4, 4, 3)
    assert relation_ranks == {
        (0, 2): (1,),
        (0, 3): (1, 1),
        (2, 3): (1,),
    }
    sample_jump_signature = jump_signature(sample)
    assert sample_jump_signature == (0, 2)

    # The two rank-three exceptional relations point to the same
    # pure-kernel endpoint in mode two.
    relation_02 = product_matrix(sample[0], sample[2]).nullspace()[0]
    relation_23 = product_matrix(sample[2], sample[3]).nullspace()[0]
    assert sp.Matrix(2, 2, tuple(relation_02)).rank() == 1
    assert sp.Matrix(2, 2, tuple(relation_23)).rank() == 1
    assert tuple(relation_02) == (1, 0, 1, 0)
    assert tuple(relation_23) == (1, 1, 0, 0)

    lower = lower_prime_planes(a, c, d)
    embedded = family_planes(a, c, d, 1 / a, 0)
    assert all(
        same_plane(left, right)
        for left, right in zip(lower, embedded, strict=True)
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "squarefree-apolar lower-pair-rank normal form and smooth "
            "Segre-incidence certificate"
        ),
        "nonzero_coefficients": {
            "".join(map(str, word)): str(value)
            for word, value in expected.items()
        },
        "family_parameters": [str(parameter) for parameter in parameters],
        "family_tangent_rank": family_jacobian.rank(),
        "family_minor_rows": list(family_rows),
        "family_minor_columns": [
            str(parameters[index]) for index in family_columns
        ],
        "family_minor_determinant": int(family_minor.det()),
        "incidence_anchor": "1010",
        "incidence_target_ratios": [str(value) for value in ratios],
        "incidence_jacobian_rank": incidence_jacobian.rank(),
        "incidence_minor_rows": list(incidence_rows),
        "incidence_minor_columns": list(incidence_columns),
        "incidence_minor_determinant": int(incidence_minor.det()),
        "component_dimension": 6,
        "pair_profile": list(pair_profile),
        "exceptional_relation_ranks": {
            "".join(map(str, pair)): list(ranks)
            for pair, ranks in relation_ranks.items()
        },
        "jump_signature_two_two_one_three": [0, 2],
        "directed_relation_signature": {
            "rank_one_edges": 2,
            "rank_two_relation_edges": 0,
            "sorted_kernel_endpoint_indegrees": [2, 0, 0, 0],
        },
        "lower_determinantal_prime_embedded": True,
        "lower_prime_embedding": {"b": "1/a", "e": "0"},
        "known_pure_component_orbits_at_least": 7,
        "all_pure_components_classified": False,
        "H31_new_component_marked_fibre_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            path.name: sha256(path) for path in (MIXED, RADICAL_STAR)
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / "tmp" / "p4_six_dimensional_component_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
