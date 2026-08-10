#!/usr/bin/env python3
"""Verify generic weighted H22 obstruction on the first component."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sympy as sp

# Stage 9 moved the H22 mixed-orientation generic package into
# claims/p5/h22/mixed-orientation/; expose it through the shared
# helper so the bare-name import below resolves.
for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/disputed-ownership/first-second-component-provenance/marked-basis-fibre-classification")

expose_claim_package(
    REPO_ROOT, "claims/p5/h22/mixed-orientation")

from krenn_gu.singular_runtime import (  # noqa: E402
    singular_command_with_timeout,
)
from verify_p5_h22_mixed_orientation_component_generic_obstruction import (
    MIXED_WORDS,
    WORDS,
    diagonal_coefficients,
    diagonal_row,
    one_marked_map,
    permanent,
    shifted_basis,
    singular,
)
from verify_p5_h31_marked_basis_fibre_classification import rows


ROOT = REPO_ROOT
THEOREM = HERE / "P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md"
COMPONENT = (
    ROOT / "claims/p4/classifications/pair-geometry/pure-rank-two"
    / "P4_PURE_RANK_TWO_COMPONENT_THEOREM.md"
)
EXPECTED_D23_PROJECTION = (
    "(L^2*Q^2*C*r^2+2*L^2*Q^2*C*r+L^2*Q^2*C+L*Q^2*C^2*r^2+2*L*Q^2*C^2*r+L*Q^2*C^2-L*Q*C*r^2+L*Q*C*r+2*L*Q*C+Q*C^2*r+Q*C^2-C*r+C)*t2+(L^3*Q*r^2-L^3*Q+L^2*Q*C*r^2-L^2*Q*C+L^2*r-L^2)*t3+(-L^2*Q*C*r-L^2*Q*C-L*Q*C^2*r-L*Q*C^2+L*C*r-L*C)",
    "t1",
    "(L^2*Q^3*r+L^2*Q^3+L*Q^3*C*r+L*Q^3*C+2*L*Q^2+Q^2*C*r+Q^2*C-Q*r+Q)*t0+(r-1)*t3+(L^2*Q^2*r+L^2*Q^2+L*Q^2*C*r+L*Q^2*C+2*L*Q+Q*C*r+Q*C-r+1)",
    "(r-1)*t3^2+(L*Q*r+L*Q+Q*C*r+Q*C-r+1)*t3",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_singular(program: str, label: str) -> str:
    completed = subprocess.run(
        singular_command_with_timeout(600),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=605,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (label, completed.returncode, completed.stdout, completed.stderr)
        )
    return completed.stdout


def run_d01_chart(stage: str, chart: int) -> dict[str, object]:
    L, Q, C, r = sp.symbols("L Q C r")
    t = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    alpha, beta = rows(L, Q, C, (0, 0, 0, 0))
    marked_beta = shifted_basis(alpha, beta, t)
    coefficients = diagonal_coefficients(
        alpha, marked_beta, extensions, "01", r
    )
    zero_indices = {
        "first": (),
        "middle": (2, 3),
        "residual": (2, 3, 6, 7),
    }[stage]
    substitutions = {
        **{extensions[index]: 0 for index in zero_indices},
        extensions[chart]: 1,
    }
    equations = [
        sp.expand(coefficients[bits].subs(substitutions))
        for bits in MIXED_WORDS
    ]
    affine = tuple(
        extension
        for index, extension in enumerate(extensions)
        if index not in zero_indices and index != chart
    )
    variables = affine + t
    program = "\n".join(
        (
            "ring R=(0,L,Q,C,r),("
            + ",".join(map(str, variables))
            + f"),(dp({len(affine)}),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "int unit=(reduce(1,I)==0);",
            (
                f'"CODEX_RESULT:{stage}:{chart}:"+string(unit)+":"'
                '+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(program, f"D01 {stage} {chart}")
    assert [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ] == [f"CODEX_RESULT:{stage}:{chart}:1:1"], output
    return {
        "stage": stage,
        "normalized_coordinate": str(extensions[chart]),
        "coordinates_already_zero": [
            str(extensions[index]) for index in zero_indices
        ],
        "ideal_unit": True,
    }


def run_d23_projection() -> tuple[str, ...]:
    L, Q, C, r = sp.symbols("L Q C r")
    t = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    alpha, beta = rows(L, Q, C, (0, 0, 0, 0))
    marked_beta = shifted_basis(alpha, beta, t)
    coefficients = diagonal_coefficients(
        alpha, marked_beta, extensions, "23", r
    )
    equations = [coefficients[bits] for bits in MIXED_WORDS]
    equations.extend(
        (
            coefficients[(0, 0, 0, 0)] - 1,
            inverse * coefficients[(1, 1, 1, 1)] - 1,
        )
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + t
    program = "\n".join(
        (
            "ring R=(0,L,Q,C,r),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal incidence=" + ",".join(map(singular, equations)) + ";",
            "ideal basis=std(incidence);",
            "ideal marking=eliminate(basis,"
            + "*".join(map(str, eliminated))
            + ");",
            "marking=std(marking);",
            '"MARKING";',
            "marking;",
            "quit;",
        )
    )
    output = run_singular(program, "D23 projection")
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def run_fitting(branch: str) -> dict[str, object]:
    L, Q, C, r = sp.symbols("L Q C r")
    t = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    alpha, beta = rows(L, Q, C, (0, 0, 0, 0))
    marked_beta = shifted_basis(alpha, beta, t)
    coefficients = diagonal_coefficients(
        alpha, marked_beta, extensions, "23", r
    )
    mixed = [coefficients[bits] for bits in MIXED_WORDS]
    first = coefficients[(0, 0, 0, 0)]
    second = coefficients[(1, 1, 1, 1)]
    alpha_d = tuple(
        diagonal_row(alpha[mode], extensions[mode], "23", r)
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(
            marked_beta[mode], extensions[4 + mode], "23", r
        )
        for mode in range(4)
    )
    marked = one_marked_map(2, alpha_d, beta_d)
    minor_rows = {
        "A": (0, 1, 4, 7),
        "B": (0, 1, 3, 7),
    }[branch]
    matrix = marked[list(minor_rows), :]
    helper = Q * (L + C) * (r + 1) - r + 1
    branch_equation = {
        "A": t[3],
        "B": (r - 1) * t[3] + helper,
    }[branch]
    generators = mixed + [t[1], branch_equation]
    determinant_index = len(generators)
    inverse_index = determinant_index + 1
    variables = extensions + t + (inverse,)
    program = "\n".join(
        (
            "ring R=(0,L,Q,C,r),("
            + ",".join(map(str, variables))
            + "),dp;",
            "option(redSB);",
            *(
                f"poly g{index}={singular(generator)};"
                for index, generator in enumerate(generators)
            ),
            "matrix M[4][4]="
            + ",".join(
                singular(matrix[row, column])
                for row in range(4)
                for column in range(4)
            )
            + ";",
            f"poly g{determinant_index}=det(M);",
            f"poly g{inverse_index}="
            + singular(inverse * first * second - 1)
            + ";",
            "ideal I="
            + ",".join(
                f"g{index}" for index in range(inverse_index + 1)
            )
            + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            (
                f'"CODEX_RESULT:{branch}:"+string(unit)+":"'
                '+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(program, f"D23 Fitting {branch}")
    assert [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ] == [f"CODEX_RESULT:{branch}:1:1"], output
    return {
        "sheet": branch,
        "marked_mode": 2,
        "minor_rows": list(minor_rows),
        "saturated_ideal_unit": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "six of the seven" in theorem_text
    assert "global prize problem" in theorem_text

    L, Q, C = sp.symbols("L Q C")
    alpha, beta = rows(L, Q, C, (0, 0, 0, 0))
    pure = {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] - 2 * (C + L)) == 0
    assert all(
        sp.factor(value) == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    chart_jobs = (
        ("first", 2),
        ("first", 3),
        ("middle", 6),
        ("middle", 7),
        ("residual", 0),
        ("residual", 1),
        ("residual", 4),
        ("residual", 5),
    )
    with ThreadPoolExecutor(max_workers=4) as executor:
        charts = list(
            executor.map(lambda item: run_d01_chart(*item), chart_jobs)
        )
    projection = run_d23_projection()
    assert projection == EXPECTED_D23_PROJECTION
    with ThreadPoolExecutor(max_workers=2) as executor:
        fitting = list(executor.map(run_fitting, ("A", "B")))

    result = {
        "verified": True,
        "field": "C(L,Q,C,r)",
        "pure_nonzero_coefficient": "2*(C+L)",
        "D01_projective_kernel_cover": charts,
        "D01_full_column_rank_for_every_marking": True,
        "D23_projection_ideal": list(projection),
        "D23_sheet_cover": [
            "t3=0",
            "(r-1)*t3+Q*(L+C)*(r+1)-r+1=0",
        ],
        "D23_fitting_certificates": fitting,
        "first_component_generic_weighted_H22_empty": True,
        "known_components_generic_weighted_H22_empty_count": 6,
        "all_seven_known_components_generic_H22_empty": False,
        "parameter_and_slope_divisors_closed": False,
        "projective_boundary_closed": False,
        "all_pure_components_classified": False,
        "all_H22_excluded": False,
        "global_problem_resolved": False,
        "dependencies": {
            path.name: sha256(path) for path in (THEOREM, COMPONENT)
        },
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h22_first_rank_two_component_generic_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
