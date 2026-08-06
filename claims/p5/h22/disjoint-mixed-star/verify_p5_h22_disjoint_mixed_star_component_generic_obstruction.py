#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the eighth component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
# The disjoint-mixed-star P4 component package moved in Stage 3; expose
# its directory so the bare-name import below resolves.
sys.path.insert(
    0, str(REPO_ROOT / "claims" / "p4" / "components"
           / "disjoint-mixed-star"))
from p5_high_coordinate_tree_chart_cegar import (
    singular_command_with_timeout,
)
from verify_p4_disjoint_mixed_star_pure_component import (  # noqa: E402
    family, relation)


THEOREM = (
    HERE / "P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    REPO_ROOT / "claims" / "p4" / "components" / "disjoint-mixed-star"
    / "P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md")
WORKING_NOTE = HERE / "P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md"
MIXED_WORDS = tuple(
    word
    for word in itertools.product((0, 1), repeat=4)
    if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
D23_BASE_ROWS = (0, 1, 3, 5, 7, 8, 10)
D23_EXTRA_ROWS = (2, 4, 6, 9, 11, 12, 13)
D01_BASE_ROWS = (0, 1, 2, 3, 7, 8, 10)
D01_EXTRA_ROWS = (4, 5, 6, 9, 11, 12, 13)
D01_PIVOT_COLUMNS = (0, 1, 2, 4, 5, 6, 7)
FITTING_0137 = (0, 1, 3, 7)
FITTING_0157 = (0, 1, 5, 7)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent3(rows, columns=(0, 1, 2)) -> sp.Expr:
    return sp.expand(
        sum(
            rows[0][columns[permutation[0]]]
            * rows[1][columns[permutation[1]]]
            * rows[2][columns[permutation[2]]]
            for permutation in PERMUTATIONS3
        )
    )


def weighted_row(row, extension, direction: str, slope):
    if direction == "01":
        return (
            slope * row[0] + row[1],
            row[2],
            row[3],
            extension,
        )
    if direction == "23":
        return (
            row[0],
            row[1],
            slope * row[2] + row[3],
            extension,
        )
    raise ValueError(direction)


def build_model(direction: str) -> dict[str, object]:
    a, b, f, phi, r = sp.symbols("a b f phi r")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("z0:8")
    planes = family(a, b, f, phi)
    alpha = tuple(tuple(plane.row(0)) for plane in planes)
    canonical_beta = tuple(tuple(plane.row(1)) for plane in planes)
    beta = tuple(
        tuple(
            sp.expand(
                canonical_beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )
    alpha_d = tuple(
        weighted_row(
            alpha[mode],
            extensions[mode],
            direction,
            r,
        )
        for mode in range(4)
    )
    beta_d = tuple(
        weighted_row(
            beta[mode],
            extensions[4 + mode],
            direction,
            r,
        )
        for mode in range(4)
    )

    def coefficient(word) -> sp.Expr:
        selected = tuple(
            beta_d[mode] if word[mode] else alpha_d[mode]
            for mode in range(4)
        )
        return sp.expand(
            sum(
                selected[mode][3]
                * permanent3(
                    tuple(
                        selected[other]
                        for other in range(4)
                        if other != mode
                    )
                )
                for mode in range(4)
            )
        )

    mixed = tuple(coefficient(word) for word in MIXED_WORDS)
    mixed_matrix = sp.Matrix(
        [
            [
                sp.diff(mixed[row], extensions[column])
                for column in range(8)
            ]
            for row in range(14)
        ]
    )
    marked_rows = []
    for word in itertools.product((0, 1), repeat=3):
        selected = tuple(
            beta_d[mode + 1] if word[mode] else alpha_d[mode + 1]
            for mode in range(3)
        )
        marked_rows.append(
            tuple(
                permanent3(
                    selected,
                    tuple(
                        coordinate
                        for coordinate in range(4)
                        if coordinate != marked_coordinate
                    ),
                )
                for marked_coordinate in range(4)
            )
        )
    return {
        "parameters": (a, b, f, phi, r),
        "shifts": shifts,
        "extensions": extensions,
        "component": relation(a, b, f, phi),
        "mixed": mixed,
        "mixed_matrix": mixed_matrix,
        "diagonal_a": coefficient((0, 0, 0, 0)),
        "diagonal_b": coefficient((1, 1, 1, 1)),
        "marked": sp.Matrix(marked_rows),
    }


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def matrix_declaration(name: str, matrix: sp.Matrix) -> str:
    return (
        f"matrix {name}[{matrix.rows}][{matrix.cols}]="
        + ",".join(
            singular(matrix[row, column])
            for row in range(matrix.rows)
            for column in range(matrix.cols)
        )
        + ";"
    )


def determinant_declarations(
    matrix: sp.Matrix,
    base_rows: tuple[int, ...],
    extra_rows: tuple[int, ...],
) -> list[str]:
    lines = []
    for index, extra in enumerate(extra_rows):
        square = matrix.extract(base_rows + (extra,), range(8))
        lines.extend(
            (
                matrix_declaration(f"D{index}", square),
                f"poly q{index}=det(D{index});",
            )
        )
    return lines


def run_singular(program: str, label: str, timeout: int = 180) -> str:
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 10,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                f"Singular failure in {label}",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return completed.stdout


def markers(output: str) -> list[str]:
    return [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]


def d01_cover_relations(model) -> tuple[sp.Expr, sp.Expr]:
    a, b, f, _phi, r = model["parameters"]
    _t0, _t1, t2, t3 = model["shifts"]
    l3 = (
        f * (a - b) * (a + b) * (r - 1) * t3
        - b * (b * f + 1) * (a * r + a + b * r - b)
    )
    l2 = (
        (b * f + 1)
        * (
            a**2 * f * r
            - a**2 * f
            + a * b * f * r
            + a * b * f
            + a * r
            + a
            + b * r
            - b
        )
        * t2
        - (r + 1) * (a**2 * f + b)
    )
    return sp.expand(l3), sp.expand(l2)


def verify_d23_rank_locus(model) -> dict[str, object]:
    a, b, f, phi, r = model["parameters"]
    shifts = model["shifts"]
    matrix = model["mixed_matrix"]
    w = sp.Symbol("w")
    lines = [
        "ring R=(0,a,b,f,r),(phi,t0,t1,t2,t3,w),dp;",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
        *determinant_declarations(
            matrix,
            D23_BASE_ROWS,
            D23_EXTRA_ROWS,
        ),
    ]
    determinants = ",".join(
        f"q{index}" for index in range(len(D23_EXTRA_ROWS))
    )
    for index, shift in enumerate(shifts[1:], start=1):
        lines.extend(
            (
                f"ideal I{index}=C,{determinants},w*{shift}-1;",
                f"I{index}=slimgb(I{index});",
                f"int u{index}=(reduce(1,I{index})==0);",
            )
        )
    lines.extend(
        (
            (
                '"CODEX_RESULT:"+string(u1)+":"'
                '+string(u2)+":"+string(u3);'
            ),
            "quit;",
        )
    )
    output = run_singular("\n".join(lines), "D23 rank locus")
    assert markers(output) == ["CODEX_RESULT:1:1:1"], output
    return {
        "base_rows": list(D23_BASE_ROWS),
        "extra_rows": list(D23_EXTRA_ROWS),
        "saturated_marking_coordinates": ["t1", "t2", "t3"],
        "forced_marking_line": ["t1=0", "t2=0", "t3=0"],
    }


def fitting_matrix_lines(model, substitutions, fitting_rows):
    extensions = model["extensions"]
    mixed = tuple(
        sp.expand(expression.subs(substitutions))
        for expression in model["mixed"]
    )
    diagonal_a = sp.expand(model["diagonal_a"].subs(substitutions))
    diagonal_b = sp.expand(model["diagonal_b"].subs(substitutions))
    marked = model["marked"].subs(substitutions)
    lines = [
        f"poly g{index}={singular(expression)};"
        for index, expression in enumerate(mixed)
    ]
    for index, rows in enumerate(fitting_rows):
        minor = marked.extract(rows, range(4))
        lines.extend(
            (
                matrix_declaration(f"H{index}", minor),
                f"poly h{index}=det(H{index});",
            )
        )
    lines.extend(
        (
            "poly da=" + singular(diagonal_a) + "-1;",
            "poly db=w*(" + singular(diagonal_b) + ")-1;",
        )
    )
    return lines, extensions


def verify_d23_fitting(model) -> dict[str, object]:
    _a, _b, _f, _phi, _r = model["parameters"]
    _t0, t1, t2, t3 = model["shifts"]
    fitting_rows = (FITTING_0137, FITTING_0157)
    lines, extensions = fitting_matrix_lines(
        model,
        {t1: 0, t2: 0, t3: 0},
        fitting_rows,
    )
    variables = extensions + (sp.Symbol("w"), sp.Symbol("phi"), sp.Symbol("t0"))
    program = [
        "ring R=(0,a,b,f,r),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(2));",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
        *lines,
        "ideal I=C,"
        + ",".join(f"g{index}" for index in range(14))
        + ",da,db,h0,h1;",
        "I=std(I);",
        (
            '"CODEX_RESULT:"+string(reduce(1,I)==0)+":"'
            '+string(size(I));'
        ),
        "quit;",
    ]
    output = run_singular("\n".join(program), "D23 Fitting line")
    assert markers(output) == ["CODEX_RESULT:1:1"], output
    return {
        "marking_line": ["t1=0", "t2=0", "t3=0"],
        "minor_rows": [list(rows) for rows in fitting_rows],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "fitting_ideal_unit": True,
    }


def verify_d01_rank_locus(model) -> dict[str, object]:
    matrix = model["mixed_matrix"]
    _a, _b, _f, _phi, _r = model["parameters"]
    _t0, t1, t2, t3 = model["shifts"]
    l3, l2 = d01_cover_relations(model)
    pivot = matrix.extract(
        D01_BASE_ROWS,
        D01_PIVOT_COLUMNS,
    )
    lines = [
        "ring R=(0,a,b,f,r),(phi,t0,t1,t2,t3),dp;",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
        matrix_declaration("P", pivot),
        "poly pivot=det(P);",
        *determinant_declarations(
            matrix,
            D01_BASE_ROWS,
            D01_EXTRA_ROWS,
        ),
        "ideal I=C,"
        + ",".join(
            f"q{index}" for index in range(len(D01_EXTRA_ROWS))
        )
        + ";",
        "I=slimgb(I);",
        "int product_relation=(reduce(t1*t2,I)==0);",
        "ideal J=I,pivot;",
        "J=slimgb(J);",
        "int pivot_unit=(reduce(1,J)==0);",
        "ideal K=I,t1;",
        "K=slimgb(K);",
        "poly l3=" + singular(l3) + ";",
        "poly l2=" + singular(l2) + ";",
        "int l3_relation=(reduce(t3*l3,K)==0);",
        "int l2_relation=(reduce(t3*l2,K)==0);",
        (
            '"CODEX_RESULT:"+string(dim(I))+":"'
            '+string(vdim(I))+":"+string(size(I))+":"'
            '+string(product_relation)+":"+string(pivot_unit)+":"'
            '+string(l3_relation)+":"+string(l2_relation);'
        ),
        "quit;",
    ]
    output = run_singular("\n".join(lines), "D01 rank locus")
    assert markers(output) == ["CODEX_RESULT:0:10:14:1:1:1:1"], output
    return {
        "base_rows": list(D01_BASE_ROWS),
        "extra_rows": list(D01_EXTRA_ROWS),
        "pivot_columns": list(D01_PIVOT_COLUMNS),
        "dimension_over_parameter_field": 0,
        "vector_space_dimension_over_parameter_field": 10,
        "degree_over_component_field": 5,
        "pivot_nonzero_on_scheme": True,
        "relations": ["t1*t2", "t3*L3 on t1=0", "t3*L2 on t1=0"],
        "cover": [
            ["t2"],
            ["t1", "t3"],
            ["t1", "L3", "L2"],
        ],
    }


def verify_d01_fitting_branch(
    model,
    branch: str,
) -> dict[str, object]:
    extensions = model["extensions"]
    _t0, t1, t2, t3 = model["shifts"]
    l3, l2 = d01_cover_relations(model)
    branch_generators, fitting_rows = {
        "t2_zero": ((t2,), (FITTING_0137, FITTING_0157)),
        "t1_t3_zero": ((t1, t3), (FITTING_0137,)),
        "t1_nonzero_t3": ((t1, l3, l2), (FITTING_0137,)),
    }[branch]
    lines = [
        "ring R=(0,a,b,f,r),("
        + ",".join(map(str, extensions))
        + ",w,phi,t0,t1,t2,t3),(dp(9),dp(5));",
        "option(redSB);",
        "poly C=" + singular(model["component"]) + ";",
        *(
            f"poly g{index}={singular(expression)};"
            for index, expression in enumerate(model["mixed"])
        ),
    ]
    for index, rows in enumerate(fitting_rows):
        minor = model["marked"].extract(rows, range(4))
        lines.extend(
            (
                matrix_declaration(f"H{index}", minor),
                f"poly h{index}=det(H{index});",
            )
        )
    lines.extend(
        (
            "poly da=" + singular(model["diagonal_a"]) + "-1;",
            "poly db=w*(" + singular(model["diagonal_b"]) + ")-1;",
        )
    )
    for index, generator in enumerate(branch_generators):
        lines.append(f"poly b{index}={singular(generator)};")
    ideal_generators = [
        "C",
        *(f"b{index}" for index in range(len(branch_generators))),
        *(f"g{index}" for index in range(14)),
        "da",
        "db",
        *(f"h{index}" for index in range(len(fitting_rows))),
    ]
    lines.extend(
        (
            "ideal I=" + ",".join(ideal_generators) + ";",
            "I=std(I);",
            (
                f'"CODEX_RESULT:{branch}:"+'
                'string(reduce(1,I)==0)+":"+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(
        "\n".join(lines),
        f"D01 Fitting branch {branch}",
    )
    assert markers(output) == [f"CODEX_RESULT:{branch}:1:1"], output
    return {
        "branch": branch,
        "branch_generators": [
            str(generator) for generator in branch_generators
        ],
        "minor_rows": [list(rows) for rows in fitting_rows],
        "normalized_first_diagonal": True,
        "inverted_second_diagonal": True,
        "maximal_rank_minors_redundant_after_normalization": True,
        "fitting_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "exact characteristic-zero theorem" in theorem_text
    assert "degree five over" in theorem_text
    assert "global Krenn--Gu conjecture remains unresolved" in theorem_text

    d23_model = build_model("23")
    d01_model = build_model("01")
    result = {
        "statement": (
            "The generic weighted H22 incidence on the disjoint "
            "mixed-star pure-P4 component is empty."
        ),
        "scope": "dense open subset over characteristic zero",
        "component_relation": str(d01_model["component"]),
        "D23": {
            "rank_locus": verify_d23_rank_locus(d23_model),
            "fitting": verify_d23_fitting(d23_model),
        },
        "D01": {
            "rank_locus": verify_d01_rank_locus(d01_model),
            "fitting_branches": [
                verify_d01_fitting_branch(d01_model, branch)
                for branch in (
                    "t2_zero",
                    "t1_t3_zero",
                    "t1_nonzero_t3",
                )
            ],
        },
        "proof_boundary": {
            "special_parameter_slope_projective_boundaries": "open",
            "component_exhaustiveness": "open",
            "global_prize_conjecture": "unresolved",
        },
        "sha256": {
            "theorem": sha256(THEOREM),
            "component": sha256(COMPONENT),
            "working_note": sha256(WORKING_NOTE),
        },
        "verified": True,
    }
    output = (
        REPO_ROOT / "tmp"
        / "p5_h22_disjoint_mixed_star_component_generic_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
