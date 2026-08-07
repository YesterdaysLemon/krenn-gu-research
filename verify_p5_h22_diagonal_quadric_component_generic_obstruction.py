#!/usr/bin/env python3
"""Verify the generic weighted H22 diagonal-quadric obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "diagonal-quadric"
    / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md")
WORKING_NOTE = ROOT / "P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md"
EIGHTH_COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "disjoint-mixed-star"
    / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md")
WORDS = tuple(itertools.product((0, 1), repeat=4))
SPECIALIZATION = (
    sp.Rational(-2, 3),
    sp.Rational(-1, 4),
    sp.Integer(2),
    sp.Integer(2),
)
EXPECTED_MINORS = {
    "01": sp.Integer(3107727),
    "23": sp.Rational(6284849697, 256),
}
RANK_ROWS = (0, 1, 2, 3, 4, 5, 6, 10)
EXCEPTIONAL_ROWS = (0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 15)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(len(rows)))
            for permutation in itertools.permutations(range(len(rows)))
        )
    )


def normal_form():
    C, E, l = sp.symbols("C E l")
    relation = (
        -C**2 * E**2
        + C**2 * l**2
        + C * E**2 * l
        - C * l
        - l**2
        + 1
    )
    denominator = 1 - l**2
    y1 = (1, 0, 0, -1)
    y2 = (0, 1, -1, 0)
    k0 = (1, 0, 0, 1)
    k1 = (0, 1, 1, 0)
    x1 = (1, C + 1, C - 1, 1)
    u0 = (E, -1, -1, -E)
    u1 = (1, -1, 1, 1)
    x2_scaled = (
        C * (l**2 - E**2) + E * denominator,
        denominator,
        denominator,
        C * (l**2 - E**2) - E * denominator,
    )
    alpha = (
        tuple(sp.expand(u0[j] + l * u1[j]) for j in range(4)),
        y1,
        y2,
        tuple(sp.expand(l * k0[j] - k1[j]) for j in range(4)),
    )
    beta = (u0, x1, x2_scaled, k0)
    return (C, E, l), relation, alpha, beta


def project_rows(
    rows: tuple[tuple[sp.Expr, ...], ...],
    diagonal: str,
    slope: sp.Expr,
) -> tuple[tuple[sp.Expr, ...], ...]:
    if diagonal == "01":
        return tuple(
            (slope * row[0] + row[1], row[2], row[3]) for row in rows
        )
    if diagonal == "23":
        return tuple(
            (row[0], row[1], slope * row[2] + row[3]) for row in rows
        )
    raise ValueError(diagonal)


def extension_coefficients(
    rows: tuple[tuple[tuple[sp.Expr, ...], ...], ...],
    word: tuple[int, ...],
) -> tuple[sp.Expr, ...]:
    coefficients = []
    for extension_type in (0, 1):
        for mode in range(4):
            if word[mode] != extension_type:
                coefficients.append(sp.Integer(0))
                continue
            other_rows = tuple(
                rows[word[other]][other]
                for other in range(4)
                if other != mode
            )
            coefficients.append(permanent(other_rows))
    return tuple(coefficients)


def fixed_data(diagonal: str):
    (C, E, l), relation, alpha, beta = normal_form()
    slope = sp.Symbol("r")
    substitution = dict(
        zip((C, E, l, slope), SPECIALIZATION, strict=True)
    )
    projected = (
        project_rows(alpha, diagonal, slope),
        project_rows(beta, diagonal, slope),
    )
    extension = sp.Matrix(
        [extension_coefficients(projected, word) for word in WORDS]
    ).subs(substitution)
    return relation.subs(substitution), alpha, beta, substitution, extension


def chart_equations(
    annihilator: sp.Matrix, chart: tuple[int, ...]
) -> tuple[sp.Expr, ...]:
    x = sp.symbols("x0:4")
    q = sp.Symbol("q")
    factors = tuple(
        (
            (sp.Integer(1), x[mode])
            if normalized == 0
            else (x[mode], sp.Integer(1))
        )
        for mode, normalized in enumerate(chart)
    )
    decomposable = sp.Matrix(
        [
            sp.prod(factors[mode][bit] for mode, bit in enumerate(word))
            for word in WORDS
        ]
    )
    endpoint = sp.zeros(16, 1)
    endpoint[15, 0] = 1
    return tuple(
        sp.expand(value)
        for value in annihilator * (decomposable + q * endpoint)
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_chart_cover(
    diagonal: str, annihilator: sp.Matrix
) -> list[dict[str, object]]:
    charts = tuple(itertools.product((0, 1), repeat=4))
    lines = [
        "ring R=0,(x0,x1,x2,x3,q),dp;",
        "option(redSB);",
    ]
    for index, chart in enumerate(charts):
        equations = chart_equations(annihilator, chart)
        lines.extend(
            (
                f"ideal I{index}=" + ",".join(map(singular, equations)) + ";",
                f"I{index}=std(I{index});",
                f"int u{index}=(reduce(1,I{index})==0);",
                (
                    f'"CODEX_CHART:{diagonal}:{index}:'
                    + "".join(map(str, chart))
                    + f':"+string(u{index})+":"+string(size(I{index}));'
                ),
            )
        )
        if index == 15:
            lines.extend(
                (
                    "int b0=(reduce(x0,I15)==0);",
                    "int b1=(reduce(x1,I15)==0);",
                    "int b2=(reduce(x2,I15)==0);",
                    "int b3=(reduce(x3,I15)==0);",
                    "int b4=(reduce(q+1,I15)==0);",
                    (
                        f'"CODEX_BASE:{diagonal}:"+string(b0)+":"'
                        '+string(b1)+":"+string(b2)+":"+string(b3)+":"'
                        '+string(b4);'
                    ),
                )
            )
    lines.append("quit;")
    completed = subprocess.run(
        singular_command_with_timeout(120),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=125,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular chart cover",
                diagonal,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    result_lines = [
        line.strip()
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("CODEX_CHART:")
    ]
    expected_lines = [
        (
            f"CODEX_CHART:{diagonal}:{index}:"
            + "".join(map(str, chart))
            + (":1:1" if index < 15 else ":0:5")
        )
        for index, chart in enumerate(charts)
    ]
    assert result_lines == expected_lines, completed.stdout
    base_lines = [
        line.strip()
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("CODEX_BASE:")
    ]
    assert base_lines == [f"CODEX_BASE:{diagonal}:1:1:1:1:1"]

    maximal = {
        sp.Symbol("x0"): 0,
        sp.Symbol("x1"): 0,
        sp.Symbol("x2"): 0,
        sp.Symbol("x3"): 0,
        sp.Symbol("q"): -1,
    }
    assert all(
        equation.subs(maximal) == 0
        for equation in chart_equations(annihilator, charts[-1])
    )
    return [
        {
            "chart": "".join(map(str, chart)),
            "unit_ideal": index < 15,
            "base_point_ideal": (
                ["x0", "x1", "x2", "x3", "q+1"]
                if index == 15
                else None
            ),
        }
        for index, chart in enumerate(charts)
    ]


def verify_direction(diagonal: str) -> dict[str, object]:
    relation_value, _alpha, _beta, _substitution, extension = fixed_data(
        diagonal
    )
    assert relation_value == 0
    assert extension.shape == (16, 8)
    assert extension.rank() == 8
    extension_minor = sp.factor(extension[list(RANK_ROWS), :].det())
    assert extension_minor == EXPECTED_MINORS[diagonal]

    endpoint = sp.zeros(16, 1)
    endpoint[15, 0] = 1
    assert extension.row_join(endpoint).rank() == 9

    nullspace = extension.T.nullspace()
    assert len(nullspace) == 8
    annihilator = sp.Matrix.hstack(*nullspace).T
    assert annihilator.shape == (8, 16)
    assert annihilator * extension == sp.zeros(8, 8)

    charts = run_chart_cover(diagonal, annihilator)

    tangent_indices = (7, 11, 13, 14, 15)
    exceptional = sp.zeros(16, 5)
    for column, row in enumerate(tangent_indices):
        exceptional[row, column] = 1
    combined = extension.row_join(exceptional)
    assert exceptional.rank() == 5
    assert combined.rank() == 13
    exceptional_minor = sp.factor(
        combined[list(EXCEPTIONAL_ROWS), :].det()
    )
    assert exceptional_minor == -EXPECTED_MINORS[diagonal]

    return {
        "direction": diagonal,
        "extension_rank": 8,
        "extension_minor_rows": list(RANK_ROWS),
        "extension_minor": str(extension_minor),
        "endpoint_augmented_rank": 9,
        "left_annihilator_shape": list(annihilator.shape),
        "Segre_charts": charts,
        "unit_charts": 15,
        "only_affine_survivor_is_zero_join_base_point": True,
        "exceptional_space_basis_words": [
            "0111",
            "1011",
            "1101",
            "1110",
            "1111",
        ],
        "exceptional_space_rank": 5,
        "extension_plus_exceptional_rank": 13,
        "exceptional_minor_rows": list(EXCEPTIONAL_ROWS),
        "exceptional_minor": str(exceptional_minor),
        "projective_join_intersection_empty_at_specialization": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "all seven" in theorem_text
    assert "eighth component" in theorem_text
    assert "does **not** classify" in theorem_text
    assert "proper" in theorem_text

    (C, E, l), relation, alpha, beta = normal_form()
    r = sp.Symbol("r")
    substitution = dict(
        zip((C, E, l, r), SPECIALIZATION, strict=True)
    )
    assert sp.Poly(relation, C, E, l).is_irreducible
    assert relation.subs(substitution) == 0
    assert sp.factor((C * (C - l) * (1 - l**2) * r).subs(substitution))
    assert all(
        sp.Matrix([alpha[mode], beta[mode]]).subs(substitution).rank() == 2
        for mode in range(4)
    )
    pure = {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        ).subs(substitution)
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == 5
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    directions = [verify_direction(diagonal) for diagonal in ("01", "23")]
    result = {
        "verified": True,
        "field": "characteristic zero",
        "method": (
            "empty projective Segre-join fibre plus proper projection"
        ),
        "quadratic_base_relation_irreducible": True,
        "specialization_C_E_l_r": [str(value) for value in SPECIALIZATION],
        "specialization_on_base": True,
        "dense_chart_gates_nonzero": True,
        "all_plane_ranks_two": True,
        "pure_nonzero_coefficient": "T_1111=5",
        "directions": directions,
        "properness_generic_transport": True,
        "diagonal_quadric_component_generic_weighted_H22_empty": True,
        "known_components_generic_weighted_H22_empty_count": 7,
        "seven_previously_certified_components_generic_H22_empty": True,
        "certified_pure_component_orbit_count_current": 8,
        "eighth_component_generic_weighted_H22_empty": False,
        "all_current_certified_components_generic_H22_empty": False,
        "special_parameter_and_slope_divisors_closed": False,
        "all_pure_components_classified": False,
        "all_H22_excluded": False,
        "global_problem_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (
                THEOREM,
                COMPONENT,
                WORKING_NOTE,
                EIGHTH_COMPONENT,
            )
        },
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h22_diagonal_quadric_component_generic_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
