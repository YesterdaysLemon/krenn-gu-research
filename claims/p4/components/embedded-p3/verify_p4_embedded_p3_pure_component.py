#!/usr/bin/env python3
"""Verify the embedded-P3 six-dimensional pure-P4 component."""

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
THEOREM = HERE / "P4_EMBEDDED_P3_PURE_COMPONENT.md"
P3_THEOREM = REPO_ROOT / "claims/p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))
PIVOTS = ((0, 1), (1, 2), (1, 2), (1, 2))
ANCHOR = (0, 0, 1, 0)
INCIDENCE_ROWS = tuple(range(14))
INCIDENCE_COLUMNS = (
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    16,
    18,
    19,
)
EXPECTED_INCIDENCE_MINOR = sp.Rational(114688, 2187)


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


def family_planes(r, s, t, u, cap_a, cap_b) -> tuple[sp.Matrix, ...]:
    return (
        sp.Matrix(((1, 0, r, t), (0, 1, s, u))),
        sp.Matrix(
            ((0, 1, 0, -1 / cap_b), (0, 0, 1, -cap_a / cap_b))
        ),
        sp.Matrix(
            ((0, 1, 0, 1 / cap_b), (0, 0, 1, -cap_a / cap_b))
        ),
        sp.Matrix(
            ((0, 1, 0, -1 / cap_b), (0, 0, 1, cap_a / cap_b))
        ),
    )


def chart_coordinates(
    planes: tuple[sp.Matrix, ...],
) -> tuple[sp.Expr, ...]:
    result = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        assert plane[:, pivots] == sp.eye(2)
        nonpivots = tuple(index for index in range(4) if index not in pivots)
        result.extend(
            plane[row, column]
            for row in range(2)
            for column in nonpivots
        )
    return tuple(result)


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


def pair_profile(planes: tuple[sp.Matrix, ...]) -> tuple[int, ...]:
    return tuple(
        product_matrix(planes[left], planes[right]).rank()
        for left, right in PAIRS
    )


def main() -> None:
    r, s, t, u, cap_a = sp.symbols("r s t u A")
    cap_b = sp.symbols("B", nonzero=True)
    family = family_planes(r, s, t, u, cap_a, cap_b)
    tensor = coefficients(family)
    expected = {
        (0, 0, 1, 0): -2 / cap_b,
        (0, 1, 1, 0): -2 * cap_a / cap_b,
    }
    assert all(
        sp.factor(value - expected.get(word, 0)) == 0
        for word, value in tensor.items()
    )

    family_variables = (r, s, t, u, cap_a, cap_b)
    family_coordinates = chart_coordinates(family)
    family_jacobian = sp.Matrix(family_coordinates).jacobian(
        family_variables
    )
    family_rows = (0, 1, 2, 3, 5, 7)
    family_minor = sp.factor(
        family_jacobian.extract(family_rows, range(6)).det()
    )
    assert family_minor == -(cap_b ** -3)

    sample_values = {
        r: sp.Rational(3, 2),
        s: sp.Rational(1, 2),
        t: 1,
        u: 2,
        cap_a: 2,
        cap_b: 3,
    }
    sample = tuple(plane.subs(sample_values) for plane in family)
    sample_coordinates = chart_coordinates(sample)
    sample_tensor = coefficients(sample)
    assert sample_tensor[ANCHOR] == -sp.Rational(2, 3)
    ratios = []
    for mode in range(4):
        adjacent = list(ANCHOR)
        adjacent[mode] = 1 - adjacent[mode]
        ratios.append(
            sp.simplify(
                sample_tensor[tuple(adjacent)] / sample_tensor[ANCHOR]
            )
        )
    assert ratios == [0, 2, 0, 0]

    chart_variables = sp.symbols("v0:16")
    target_variables = sp.symbols("z0:4")
    chart_tensor = coefficients(chart_planes(chart_variables))
    equations = []
    equation_words = []
    for word in WORDS:
        if word == ANCHOR:
            continue
        product = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != ANCHOR[mode]
        )
        equations.append(chart_tensor[word] - chart_tensor[ANCHOR] * product)
        equation_words.append(word)

    all_variables = chart_variables + target_variables
    substitution = {
        **dict(zip(chart_variables, sample_coordinates, strict=True)),
        **dict(zip(target_variables, ratios, strict=True)),
    }
    incidence_jacobian = sp.Matrix(equations).jacobian(
        all_variables
    ).subs(substitution)
    incidence_minor = incidence_jacobian.extract(
        INCIDENCE_ROWS, INCIDENCE_COLUMNS
    )
    assert incidence_jacobian.rank() == 14
    assert sp.factor(incidence_minor.det()) == EXPECTED_INCIDENCE_MINOR

    profile = pair_profile(sample)
    assert profile == (4, 4, 4, 2, 2, 2)

    result = {
        "verified": True,
        "field": "C",
        "method": "embedded pure P3, exact family tangent, and smooth Segre incidence",
        "component_dimension": 6,
        "family_tangent_minor": str(family_minor),
        "sample": {
            "r": "3/2",
            "s": "1/2",
            "t": "1",
            "u": "2",
            "A": "2",
            "B": "3",
        },
        "Grassmann_pivots": [list(pair) for pair in PIVOTS],
        "pure_coefficients": {
            "0010": "-2/B",
            "0110": "-2*A/B",
        },
        "incidence_anchor": "".join(map(str, ANCHOR)),
        "incidence_target_ratios": [str(value) for value in ratios],
        "incidence_jacobian_rank": incidence_jacobian.rank(),
        "incidence_tangent_dimension": 20 - incidence_jacobian.rank(),
        "incidence_minor_rows": list(INCIDENCE_ROWS),
        "incidence_minor_columns": list(INCIDENCE_COLUMNS),
        "incidence_minor": str(EXPECTED_INCIDENCE_MINOR),
        "pair_profile": list(profile),
        "pair_rank_multiset": sorted(profile),
        "certified_pure_component_orbit_count": 9,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "dependencies": {
            P3_THEOREM.name: sha256(P3_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
