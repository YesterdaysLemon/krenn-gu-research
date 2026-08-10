#!/usr/bin/env python3
"""Verify generic weighted H22 obstruction on the three 1+3 branches."""

from __future__ import annotations

import hashlib
import itertools
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

expose_claim_package(
    REPO_ROOT, "claims/p5/h22/mixed-orientation")
expose_claim_package(REPO_ROOT, "claims/p5/h31/one-three")

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
from verify_p5_h31_one_three_component_generic_obstruction import (
    canonical_basis,
)


ROOT = REPO_ROOT
THEOREM = HERE / "P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md"
CANONICAL_PRIMARY = (
    ROOT / "claims/p5/h31/one-three"
    / "verify_p5_h31_one_three_component_generic_obstruction.py"
)
EXPECTED_PROJECTIONS = {
    "L1": {
        "01": ("1",),
        "23": (
            "(S)*t2+(-S*G+D*G)*t3+(-S^2+S*D-S*G+D*G)",
            "(S-D+G)*t1+(S*D-D^2)*t3+(-S^2+2*S*D-S*G-D^2+D*G)",
            "(S+G)*t0+1",
            "t3^2+t3",
        ),
    },
    "L2": {
        "01": ("1",),
        "23": (
            "(D+G)*t0+1",
            "t2*t3",
            "t1*t3+t1",
            "t1*t2",
        ),
    },
    "L3": {
        "01": ("1",),
        "23": ("1",),
    },
}
FITTING_ROWS = (0, 2, 4, 7)


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
            (
                f"Singular failure in {label}",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return completed.stdout


def run_projection(branch: str, diagonal: str) -> tuple[str, ...]:
    S, D, G, r = sp.symbols("S D G r")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    alpha, beta = canonical_basis(branch, S, D, G)
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        diagonal,
        r,
    )
    equations = [coefficients[bits] for bits in MIXED_WORDS]
    equations.extend(
        (
            coefficients[(0, 0, 0, 0)] - 1,
            inverse * coefficients[(1, 1, 1, 1)] - 1,
        )
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    program = "\n".join(
        (
            "ring R=(0,S,D,G,r),("
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
    output = run_singular(program, f"{branch} {diagonal} projection")
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def sheet_data(branch: str, sheet: str, S, D, G, t):
    if branch == "L1" and sheet == "A":
        return (
            (
                -1 / (S + G),
                S - D,
                (S - D) * (S + G) / S,
                0,
            ),
            (),
        )
    if branch == "L1" and sheet == "B":
        return (
            (
                -1 / (S + G),
                (S - D) * (S + G) / (S - D + G),
                S - D,
                -1,
            ),
            (),
        )
    if branch == "L2" and sheet == "A":
        return ((-1 / (D + G), 0, 0, t[3]), (t[3],))
    if branch == "L2" and sheet == "B":
        return ((-1 / (D + G), 0, t[2], 0), (t[2],))
    if branch == "L2" and sheet == "C":
        return ((-1 / (D + G), t[1], 0, -1), (t[1],))
    raise ValueError((branch, sheet))


def run_fitting(branch: str, sheet: str) -> dict[str, object]:
    S, D, G, r = sp.symbols("S D G r")
    t = sp.symbols("t0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    shifts, free_shifts = sheet_data(branch, sheet, S, D, G, t)
    alpha, beta = canonical_basis(branch, S, D, G)
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        "23",
        r,
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
            marked_beta[mode],
            extensions[4 + mode],
            "23",
            r,
        )
        for mode in range(4)
    )
    marked = one_marked_map(0, alpha_d, beta_d)
    matrix = marked[list(FITTING_ROWS), :]
    determinant_index = len(mixed)
    inverse_index = determinant_index + 1
    variables = extensions + free_shifts + (inverse,)
    program = "\n".join(
        (
            "ring R=(0,S,D,G,r),("
            + ",".join(map(str, variables))
            + "),dp;",
            "option(redSB);",
            *(
                f"poly g{index}={singular(generator)};"
                for index, generator in enumerate(mixed)
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
                f'"CODEX_RESULT:{branch}:{sheet}:"+string(unit)+":"'
                '+string(size(I));'
            ),
            "quit;",
        )
    )
    output = run_singular(program, f"{branch}-{sheet} Fitting")
    markers = [
        line.strip()
        for line in output.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert markers == [f"CODEX_RESULT:{branch}:{sheet}:1:1"], output
    return {
        "branch": branch,
        "sheet": sheet,
        "free_marking_parameters": [str(value) for value in free_shifts],
        "mode_zero_0247_saturated_ideal_unit": True,
    }


def verify_projection_decompositions() -> dict[str, object]:
    S, D, G = sp.symbols("S D G")
    t = sp.symbols("t0:4")
    l1_generators = (
        S * t[2] + G * (D - S) * t[3] + (D - S) * (S + G),
        (S - D + G) * t[1]
        + D * (S - D) * t[3]
        + (D - S) * (S - D + G),
        (S + G) * t[0] + 1,
        t[3] * (t[3] + 1),
    )
    l1_sheets = {
        sheet: sheet_data("L1", sheet, S, D, G, t)[0]
        for sheet in ("A", "B")
    }
    assert all(
        sp.factor(generator.subs(dict(zip(t, marking, strict=True)))) == 0
        for marking in l1_sheets.values()
        for generator in l1_generators
    )

    l2_generators = (
        (D + G) * t[0] + 1,
        t[2] * t[3],
        t[1] * (t[3] + 1),
        t[1] * t[2],
    )
    l2_sheets = {
        sheet: sheet_data("L2", sheet, S, D, G, t)[0]
        for sheet in ("A", "B", "C")
    }
    assert all(
        sp.factor(generator.subs(dict(zip(t, marking, strict=True)))) == 0
        for marking in l2_sheets.values()
        for generator in l2_generators
    )
    return {
        "L1_two_rational_sheets_verified": True,
        "L2_three_affine_line_closures_verified": True,
    }


def main() -> None:
    theorem_text = THEOREM.read_text(encoding="utf-8")
    assert "five of the" in theorem_text
    assert "seven currently certified" in theorem_text
    assert "global prize problem" in theorem_text

    S, D, G = sp.symbols("S D G")
    expected_pure = {
        "L1": 4 * D * G,
        "L2": 4 * D * (D + G - S),
        "L3": -4 * D * S,
    }
    pure_coefficients = {}
    canonical = {}
    for branch in ("L1", "L2", "L3"):
        alpha, beta = canonical_basis(branch, S, D, G)
        canonical[branch] = (alpha, beta)
        tensor = {
            word: permanent(
                tuple(
                    beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
            for word in WORDS
        }
        assert sp.factor(
            tensor[(1, 1, 1, 1)] - expected_pure[branch]
        ) == 0
        assert all(
            sp.factor(value) == 0
            for word, value in tensor.items()
            if word != (1, 1, 1, 1)
        )
        pure_coefficients[branch] = str(expected_pure[branch])

    projection_jobs = tuple(
        (branch, diagonal)
        for branch in ("L1", "L2", "L3")
        for diagonal in ("01", "23")
    )
    with ThreadPoolExecutor(max_workers=4) as executor:
        projection_values = list(
            executor.map(lambda item: run_projection(*item), projection_jobs)
        )
    projections = {
        branch: {
            diagonal: value
            for (job_branch, diagonal), value in zip(
                projection_jobs,
                projection_values,
                strict=True,
            )
            if job_branch == branch
        }
        for branch in ("L1", "L2", "L3")
    }
    assert projections == EXPECTED_PROJECTIONS

    decomposition = verify_projection_decompositions()
    fitting_jobs = (
        ("L1", "A"),
        ("L1", "B"),
        ("L2", "A"),
        ("L2", "B"),
        ("L2", "C"),
    )
    with ThreadPoolExecutor(max_workers=4) as executor:
        fitting = list(
            executor.map(lambda item: run_fitting(*item), fitting_jobs)
        )

    result = {
        "verified": True,
        "field": "C(S,D,G,r)",
        "canonical_pure_coefficients": pure_coefficients,
        "function_field_projection_ideals": {
            branch: {
                diagonal: list(ideal)
                for diagonal, ideal in branch_projections.items()
            }
            for branch, branch_projections in projections.items()
        },
        "projection_decompositions": decomposition,
        "mode_zero_minor_rows": list(FITTING_ROWS),
        "fitting_certificates": fitting,
        "three_one_three_components_generic_weighted_H22_empty": True,
        "known_components_generic_weighted_H22_empty_count": 5,
        "all_seven_known_components_generic_H22_empty": False,
        "parameter_and_slope_divisors_closed": False,
        "projective_boundaries_closed": False,
        "all_pure_components_classified": False,
        "all_H22_excluded": False,
        "global_problem_resolved": False,
        "dependencies": {
            path.name: sha256(path)
            for path in (THEOREM, COMPONENT, CANONICAL_PRIMARY)
        },
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h22_one_three_components_generic_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
