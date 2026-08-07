#!/usr/bin/env python3
"""Verify the generically smooth P4 pure rank-two component theorem."""

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
THEOREM = HERE / "P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
FAMILY_THEOREM = (
    REPO_ROOT / "claims" / "p4" / "classifications" / "pair-geometry"
    / "decomposable-rank-two-family"
    / "P4_DECOMPOSABLE_RANK_TWO_FAMILY.md")
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: list[sp.Matrix]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def main() -> None:
    plane_symbols = sp.symbols("a b c d e f g h i j k l m n o p")
    (
        a, b, c, d, e, f, g, h,
        i, j, k, ell, m, n, o, p,
    ) = plane_symbols
    z = sp.symbols("z0:4")
    variables = (*plane_symbols, *z)

    rows = (
        sp.Matrix(((1, 0, a, b), (0, 1, c, d))),
        sp.Matrix(((e, 1, 0, f), (g, 0, 1, h))),
        sp.Matrix(((i, 1, 0, j), (k, 0, 1, ell))),
        sp.Matrix(((1, m, n, 0), (0, o, p, 1))),
    )
    words = tuple(itertools.product((0, 1), repeat=4))
    coefficients = {
        word: permanent([rows[mode][word[mode], :] for mode in range(4)])
        for word in words
    }

    anchor = (1, 0, 0, 0)
    equations = []
    equation_words = []
    for word in words:
        if word == anchor:
            continue
        factor_ratio = sp.prod(
            z[mode]
            for mode in range(4)
            if word[mode] != anchor[mode]
        )
        equations.append(
            sp.expand(coefficients[word] - coefficients[anchor] * factor_ratio)
        )
        equation_words.append("".join(map(str, word)))

    point_values = (
        -1, -2, 1, 0,
        1, 0, 0, 1,
        0, 1, -1, 0,
        0, 1, 0, -1,
        -1, 1, 0, 0,
    )
    point = dict(zip(variables, point_values, strict=True))
    assert coefficients[anchor].subs(point) == 2
    assert all(equation.subs(point) == 0 for equation in equations)

    expected_coefficients = {}
    for word in words:
        expected_coefficients[word] = (
            2
            * ((-1) if word[0] == 0 else 1)
            * 1
            * (1 if word[1] in (0, 1) else 0)
            * (1 if word[2] == 0 else 0)
            * (1 if word[3] == 0 else 0)
        )
    actual_coefficients = {
        word: coefficients[word].subs(point)
        for word in words
    }
    assert actual_coefficients == expected_coefficients

    jacobian = sp.Matrix(equations).jacobian(variables).subs(point)
    pivot_columns = jacobian.rref()[1]
    expected_pivots = (
        0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 18, 19
    )
    assert pivot_columns == expected_pivots
    incidence_minor = jacobian[:, list(expected_pivots)]
    incidence_determinant = incidence_minor.det()
    assert incidence_determinant == -4096
    assert jacobian.rank() == 15

    E, I, L, Q, C = sp.symbols("E I L Q C")
    G = E * I * L
    upper = (
        (0, 1, (C + G) / E, C),
        (0, 0, 1, E),
        (0, 1, 0, G),
        (1, 0, I, 0),
    )
    lower = (
        (1, Q, 0, -E * I * (1 + L * Q)),
        (L, 1, -I * L, -G),
        (-1 / I, 0, 1, 0),
        (0, 0, -1 / E, 1),
    )
    pivot_pairs = ((0, 1), (1, 2), (1, 2), (0, 3))
    chart_coordinates = []
    reduced_rows = []
    for upper_row, lower_row, pivot_pair in zip(
        upper, lower, pivot_pairs, strict=True
    ):
        matrix = sp.Matrix((upper_row, lower_row))
        reduced = sp.simplify(matrix[:, pivot_pair].inv() * matrix)
        reduced_rows.append(reduced)
        chart_coordinates.extend(
            reduced[row, column]
            for row in range(2)
            for column in range(4)
            if column not in pivot_pair
        )

    expected_chart_coordinates = (
        -Q * (C + E * I * L) / E,
        -C * Q - E * I * (L * Q + 1),
        C / E + I * L,
        C,
        L, 0, 0, E,
        0, E * I * L, -1 / I, 0,
        0, I, 0, -1 / E,
    )
    assert all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(
            chart_coordinates, expected_chart_coordinates, strict=True
        )
    )

    family_point = {E: 1, I: 1, L: 1, Q: 1, C: 0}
    assert tuple(
        coordinate.subs(family_point)
        for coordinate in chart_coordinates
    ) == point_values[:16]
    family_jacobian = sp.Matrix(chart_coordinates).jacobian(
        (E, I, L, Q, C)
    ).subs(family_point)
    family_determinant = family_jacobian[:5, :].det()
    assert family_determinant == 2
    assert family_jacobian.rank() == 5

    output = {
        "verified": True,
        "field": "C",
        "grassmann_chart_dimension": 16,
        "segre_projective_codimension": 11,
        "incidence_variables": 20,
        "incidence_equations": len(equations),
        "anchor_word": "1000",
        "anchor_coefficient": int(coefficients[anchor].subs(point)),
        "incidence_jacobian_rank": jacobian.rank(),
        "incidence_minor_columns": [
            str(variables[index]) for index in expected_pivots
        ],
        "incidence_minor_determinant": int(incidence_determinant),
        "local_dimension": 20 - jacobian.rank(),
        "family_parameter_count": 5,
        "family_tangent_rank": family_jacobian.rank(),
        "family_tangent_minor_rows": [
            str(symbol) for symbol in plane_symbols[:5]
        ],
        "family_tangent_minor_determinant": int(family_determinant),
        "equation_words": equation_words,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "dependencies": {
            FAMILY_THEOREM.name: sha256(FAMILY_THEOREM),
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "all_components_classified": False,
        "global_conjecture_resolved": False,
    }
    output_path = REPO_ROOT / "tmp" / "p4_pure_rank_two_component_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
