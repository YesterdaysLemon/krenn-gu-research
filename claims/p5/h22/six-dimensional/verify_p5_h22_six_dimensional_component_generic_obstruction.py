#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on the P4 sixfold."""

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
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from krenn_gu.singular_runtime import singular_command_with_timeout


ROOT = REPO_ROOT
THEOREM = (
    HERE / "P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "six-dimensional"
    / "P4_SIX_DIMENSIONAL_PURE_COMPONENT.md")
COMPONENT_PRIMARY = (
    ROOT / "claims" / "p4" / "components" / "six-dimensional"
    / "verify_p4_six_dimensional_pure_component.py")
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    bits
    for bits in WORDS
    if bits not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
EXPECTED_PROJECTIONS = {
    "01": ("1",),
    "23": (
        "(u-v)*t2+(-s*v)",
        "(u-v)*t1+(u-1)",
        "t0",
    ),
}
FITTING_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7))


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


def diagonal_row(row, extension, diagonal: str, slope):
    if diagonal == "01":
        return (
            slope * row[0] + row[1],
            row[2],
            row[3],
            extension,
        )
    if diagonal == "23":
        return (
            row[0],
            row[1],
            slope * row[2] + row[3],
            extension,
        )
    raise ValueError(diagonal)


def diagonal_coefficients(
    alpha,
    beta,
    extensions,
    diagonal: str,
    slope,
) -> dict[tuple[int, ...], sp.Expr]:
    alpha_d = tuple(
        diagonal_row(
            alpha[mode],
            extensions[mode],
            diagonal,
            slope,
        )
        for mode in range(4)
    )
    beta_d = tuple(
        diagonal_row(
            beta[mode],
            extensions[4 + mode],
            diagonal,
            slope,
        )
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


def one_marked_map(mode: int, alpha, beta) -> sp.Matrix:
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other] if bits[bit_index] else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate) for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_projection(diagonal: str) -> tuple[str, ...]:
    alpha, beta = canonical_basis()
    slope = sp.Symbol("r")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        diagonal,
        slope,
    )
    equations = [
        coefficients[bits]
        for bits in MIXED_WORDS
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
            "ring R=(0,s,d,u,v,r),("
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
                "Singular weighted projection failure",
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


def weighted_23_kernel_certificate():
    s, d, u, v, r, p = sp.symbols("s d u v r p")
    alpha, beta = canonical_basis()
    shifts = (0, (1 - u) / (u - v), s * v / (u - v), p)
    marked_beta = shifted_basis(alpha, beta, shifts)
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    coefficients = diagonal_coefficients(
        alpha,
        marked_beta,
        extensions,
        "23",
        r,
    )
    mixed = sp.Matrix([
        [
            sp.diff(coefficients[bits], extension)
            for extension in extensions
        ]
        for bits in MIXED_WORDS
    ])
    first = sp.Matrix([[
        sp.diff(coefficients[(0, 0, 0, 0)], extension)
        for extension in extensions
    ]])
    second = sp.Matrix([[
        sp.diff(coefficients[(1, 1, 1, 1)], extension)
        for extension in extensions
    ]])

    pivot_rows = (0, 1, 5, 6, 7, 8)
    pivot_columns = (0, 1, 2, 3, 4, 7)
    pivot_determinant = sp.factor(
        mixed[pivot_rows, pivot_columns].det()
    )
    expected_pivot = (
        -2
        * s**2
        * u**2
        * (r - 1) ** 2
        * (r + 1) ** 3
        * (u - 1)
        * (u - v) ** 2
        * (p * r - p + 1)
    )
    assert sp.factor(pivot_determinant - expected_pivot) == 0

    helper = (
        p * r**2 * u
        - p * r**2
        - p * r * v
        + p * r
        - p * u
        + p * v
        + r * u
        - r * v
        + u
        - v
    )
    genuine = sp.Matrix(
        (
            -p
            * r
            * (r - 1)
            / (s * u * (r + 1) * (p * r - p + 1)),
            0,
            -(p - 1)
            * (r - 1)
            * (u - v)
            / (
                s
                * u
                * (r + 1)
                * (u - 1)
                * (p * r - p + 1)
            ),
            -(r - 1)
            * helper
            / (
                s
                * u
                * (r + 1) ** 2
                * (u - 1)
                * (p * r - p + 1)
            ),
            helper
            / (
                s
                * u
                * (r + 1)
                * (u - 1)
                * (p * r - p + 1)
            ),
            1,
            0,
            -p
            * (p - 1)
            * (r - 1) ** 2
            * (r * u - r + u - v)
            / (
                s
                * u
                * (r + 1) ** 2
                * (u - 1)
                * (p * r - p + 1)
            ),
        )
    )
    reconstruction = sp.Matrix((0, u - v, 0, 0, 0, 0, 1, 0))
    assert all(
        sp.factor(entry) == 0
        for vector in (genuine, reconstruction)
        for entry in mixed * vector
    )
    genuine_diagonals = (
        sp.factor((first * genuine)[0]),
        sp.factor((second * genuine)[0]),
    )
    reconstruction_diagonals = (
        sp.factor((first * reconstruction)[0]),
        sp.factor((second * reconstruction)[0]),
    )
    expected_diagonals = (
        -2
        * r
        * (r - 1)
        * (u - v) ** 2
        / (
            s
            * u
            * (r + 1)
            * (u - 1)
            * (p * r - p + 1)
        ),
        2 * (r * u - r + u - v) / (u - 1),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(
            genuine_diagonals,
            expected_diagonals,
            strict=True,
        )
    )
    assert reconstruction_diagonals == (0, 0)
    return {
        "pivot_rows": list(pivot_rows),
        "pivot_columns": list(pivot_columns),
        "pivot_determinant": str(pivot_determinant),
        "kernel_dimension": 2,
        "genuine_direction_diagonals": [
            str(value) for value in genuine_diagonals
        ],
        "reconstruction_direction_diagonals": [0, 0],
    }


def run_fitting_certificate() -> dict[str, object]:
    s, d, u, v, r, p = sp.symbols("s d u v r p")
    alpha, beta = canonical_basis()
    shifts = (0, (1 - u) / (u - v), s * v / (u - v), p)
    marked_beta = shifted_basis(alpha, beta, shifts)
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
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
    coefficients = {
        bits: permanent(
            tuple(
                beta_d[mode] if bits[mode] else alpha_d[mode]
                for mode in range(4)
            )
        )
        for bits in WORDS
    }
    mixed = [coefficients[bits] for bits in MIXED_WORDS]
    first = coefficients[(0, 0, 0, 0)]
    second = coefficients[(1, 1, 1, 1)]
    marked = one_marked_map(0, alpha_d, beta_d)
    determinant_matrices = tuple(
        marked[list(rows), :] for rows in FITTING_ROWS
    )
    base_generators = [
        *(singular(expression) for expression in mixed),
        singular(inverse * first * second - 1),
    ]
    determinant_offset = len(mixed)
    inverse_index = determinant_offset + len(determinant_matrices)
    program = "\n".join(
        (
            "ring R=(0,s,d,u,v,r,p),("
            + ",".join(map(str, extensions + (inverse,)))
            + "),dp;",
            *(
                f"poly g{index}={generator};"
                for index, generator in enumerate(base_generators[:-1])
            ),
            *tuple(
                "matrix D"
                + str(index)
                + "[4][4]="
                + ",".join(
                    singular(matrix[row, column])
                    for row in range(4)
                    for column in range(4)
                )
                + ";\npoly g"
                + str(determinant_offset + index)
                + "=det(D"
                + str(index)
                + ");"
                for index, matrix in enumerate(determinant_matrices)
            ),
            f"poly g{inverse_index}={base_generators[-1]};",
            "ideal I="
            + ",".join(
                f"g{index}" for index in range(inverse_index + 1)
            )
            + ";",
            "I=std(I);",
            "int unit=(reduce(1,I)==0);",
            '"CODEX_RESULT:"+string(unit)+":"+string(size(I));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command_with_timeout(300),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=305,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular weighted Fitting failure",
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    lines = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert lines == ["CODEX_RESULT:1:1"], completed.stdout
    return {
        "marked_mode": 0,
        "minor_rows": [list(rows) for rows in FITTING_ROWS],
        "saturated_fitting_ideal_unit": True,
    }


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

    projections = {
        diagonal: run_projection(diagonal)
        for diagonal in ("01", "23")
    }
    assert projections == EXPECTED_PROJECTIONS
    kernel = weighted_23_kernel_certificate()
    fitting = run_fitting_certificate()

    result = {
        "verified": True,
        "field": "C(s,d,u,v,r)",
        "method": (
            "weighted diagonal-hyperplane projection, exact extension "
            "kernel, and a two-minor ternary Fitting obstruction"
        ),
        "pure_coefficient": "2*s*u",
        "weighted_source_columns": {
            "01": ["r*x0+x1", "x2", "x3", "x4"],
            "23": ["x0", "x1", "r*x2+x3", "x4"],
        },
        "saturated_projection_ideals": {
            diagonal: list(projection)
            for diagonal, projection in projections.items()
        },
        "weighted_01_generic_binary_Delta2_extension_exists": False,
        "weighted_23_generic_marking_sheet": [
            "t0=0",
            "(u-v)*t1+u-1=0",
            "(u-v)*t2-s*v=0",
            "t3=p free",
        ],
        "weighted_23_kernel_certificate": kernel,
        "weighted_23_ternary_fitting_certificate": fitting,
        "generic_H22_incidence_on_six_dimensional_component_empty": True,
        "weighted_slope_and_parameter_boundaries_closed": False,
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
        / "p5_h22_six_dimensional_component_generic_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
