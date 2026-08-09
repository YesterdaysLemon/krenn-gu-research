#!/usr/bin/env python3
"""Verify the equal-weight H22 binary obstruction on the P4 sixfold."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from p5_high_coordinate_tree_chart_cegar import (  # noqa: E402
    singular_command_with_timeout,
)

ROOT = REPO_ROOT
THEOREM = (
    HERE
    / "P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md"
)
COMPONENT = (
    REPO_ROOT / "claims" / "p4" / "components" / "six-dimensional"
    / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md")
COMPONENT_PRIMARY = (
    REPO_ROOT / "claims" / "p4" / "components" / "six-dimensional"
    / "verify_p4_six_dimensional_pure_component.py")
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
DIAGONAL_COLUMNS = {
    "01": ("x0+x1", "x2", "x3", "x4"),
    "23": ("x0", "x1", "x2+x3", "x4"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def canonical_basis():
    s, d, u, v = sp.symbols("s d u v")
    h = s - d
    planes = (
        ((1, 0, 0, -1), (0, 0, 1, 1)),
        (
            (s, 1 - u, 0, d + u * h),
            (0, 1 - v, s, d + v * h),
        ),
        ((1, 0, -1, 0), (0, 1, -s, -d)),
        ((1, 0, 0, 1), (0, 0, 1, -1)),
    )
    alpha = (
        planes[0][0],
        tuple(
            sp.expand(
                v * planes[1][0][coordinate]
                - u * planes[1][1][coordinate]
            )
            for coordinate in range(4)
        ),
        planes[2][0],
        planes[3][1],
    )
    beta = (
        planes[0][1],
        planes[1][0],
        planes[2][1],
        planes[3][0],
    )
    return alpha, beta


def diagonal_row(row, extension, diagonal: str):
    if diagonal == "01":
        return (row[0] + row[1], row[2], row[3], extension)
    if diagonal == "23":
        return (row[0], row[1], row[2] + row[3], extension)
    raise ValueError(diagonal)


def shifted_basis(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.factor(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def diagonal_coefficients(
    alpha,
    beta,
    extensions,
    diagonal: str,
) -> dict[tuple[int, ...], sp.Expr]:
    alpha_d = tuple(
        diagonal_row(alpha[mode], extensions[mode], diagonal)
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(beta[mode], extensions[4 + mode], diagonal)
        for mode in range(4)
    )
    return {
        bits: permanent(
            tuple(
                beta_d[mode] if bits[mode] else alpha_d[mode]
                for mode in range(4)
            )
        )
        for bits in WORDS
    }


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_projection(diagonal: str) -> tuple[str, ...]:
    alpha, beta = canonical_basis()
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        diagonal,
    )
    equations = [
        coefficients[bits]
        for bits in WORDS
        if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
    ]
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
            "ring r=(0,s,d,u,v),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal incidence="
            + ",".join(map(singular, equations))
            + ";",
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
                "Singular diagonal projection failure",
                diagonal,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def main() -> None:
    s, d, u, v = sp.symbols("s d u v")
    alpha, beta = canonical_basis()
    pure = {
        bits: permanent(
            tuple(
                beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for bits in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] - 2 * s * u) == 0
    assert all(
        sp.factor(value) == 0
        for bits, value in pure.items()
        if bits != (1, 1, 1, 1)
    )

    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    marked_beta = shifted_basis(alpha, beta, shifts)
    diagonal_23 = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        "23",
    )

    def coefficient_row(bits):
        return sp.Matrix([[
            sp.diff(diagonal_23[bits], extension)
            for extension in extensions
        ]])

    first_diagonal = coefficient_row((0, 0, 0, 0))
    row_1000 = coefficient_row((1, 0, 0, 0))
    row_1110 = coefficient_row((1, 1, 1, 0))
    assert tuple(first_diagonal) == (
        0,
        0,
        0,
        2 * (u - v),
        0,
        0,
        0,
        0,
    )
    assert all(
        sp.factor(entry) == 0
        for entry in row_1000 - (shifts[0] - 1) * first_diagonal
    )
    obstruction_factor = (
        s * shifts[0] * shifts[1] * v
        - s * shifts[0] * u
        + s * shifts[0]
        - s * shifts[1] * v
        - s
        - shifts[0] * shifts[1] * shifts[2] * u
        + shifts[0] * shifts[1] * shifts[2] * v
        - shifts[0] * shifts[2] * u
        + shifts[0] * shifts[2]
        + shifts[1] * shifts[2] * u
        - shifts[1] * shifts[2] * v
        + shifts[2] * u
        - shifts[2]
    )
    assert all(
        sp.factor(entry) == 0
        for entry in (
            (u - v) * row_1110
            + obstruction_factor * first_diagonal
        )
    )
    assert sp.factor(obstruction_factor.subs(shifts[0], 1) + s * u) == 0

    projections = {
        diagonal: run_projection(diagonal)
        for diagonal in DIAGONAL_COLUMNS
    }
    assert projections == {"01": ("1",), "23": ("1",)}

    result = {
        "verified": True,
        "field": "C(s,d,u,v)",
        "method": (
            "squarefree-apolar diagonal-hyperplane extensions and exact "
            "saturated function-field projections"
        ),
        "pure_coefficient": "2*s*u",
        "diagonal_source_columns": DIAGONAL_COLUMNS,
        "marking_parameters": ["t0", "t1", "t2", "t3"],
        "extension_parameters": [
            "x0",
            "x1",
            "x2",
            "x3",
            "y0",
            "y1",
            "y2",
            "y3",
        ],
        "mixed_equations_per_diagonal": 14,
        "diagonal_23_two_row_obstruction": {
            "row_1000_over_first_diagonal": "t0-1",
            "row_1110_cleared_factor": "-G/(u-v)",
            "G_at_t0_equals_1": "-s*u",
        },
        "saturated_projection_ideals": {
            diagonal: list(projection)
            for diagonal, projection in projections.items()
        },
        "diagonal_01_binary_Delta2_extension_exists": False,
        "diagonal_23_binary_Delta2_extension_exists": False,
        "equal_weight_H22_binary_incidence_empty": True,
        "weighted_source_slopes_closed": False,
        "generic_H22_incidence_on_six_dimensional_component_empty": False,
        "component_parameter_boundaries_closed": False,
        "all_pure_components_classified": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output = (
        ROOT
        / "tmp"
        / "p5_h22_six_dimensional_equal_weight_binary_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
