#!/usr/bin/env python3
"""Verify the marked H31 obstruction on the diagonal-quadric E-curve."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md"
POINT_THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md"
)
C_CURVE_THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md"
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

EXPECTED_RELATIVE_PROJECTIONS = {
    0: (
        "t3-1",
        "t2-1",
        "t0-t1+1",
        "t1*e-e",
        "t1^2-t1",
    ),
    1: ("1",),
    2: ("t3", "t2-1", "t1-e", "2*t0+1", "e^2-1"),
    3: (
        "t3-1",
        "t2-1",
        "t0+t1+1",
        "t1*e+e",
        "t1^2+t1",
    ),
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


def singular(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def run_relative_projection(
    distinguished: int,
    alpha,
    beta,
    parameter: sp.Symbol,
    timeout: float = 120,
) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("ub")
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        beta,
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.extend(
        (
            (diagonal_a * extension)[0] - 1,
            inverse * (diagonal_b * extension)[0] - 1,
        )
    )
    eliminated = extensions + (inverse,)
    retained = shifts + (parameter,)
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring r=0,("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));",
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
    completed = subprocess.run(
        singular_command_with_timeout(timeout),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout + 5,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular relative projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    output = completed.stdout.replace("\r\n", "\n")
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in output.splitlines()
        if line.startswith("marking[")
    )


def verify_case(
    *,
    label: str,
    distinguished: int,
    alpha,
    beta,
    shifts,
    kernel,
    expected_diagonals,
    marked_mode: int,
    marked_rows: list[int],
    expected_minor,
) -> dict:
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    substitutions = dict(zip(t, shifts, strict=True))
    marked_beta = tuple(
        tuple(sp.factor(entry.subs(substitutions)) for entry in row)
        for row in beta
    )
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished,
        alpha,
        marked_beta,
    )
    assert mixed.rank() == 6
    assert all(
        all(sp.factor(entry) == 0 for entry in mixed * vector)
        for vector in kernel
    )
    assert sp.Matrix.hstack(*kernel).rank() == 2

    extension = u * kernel[0] + v * kernel[1]
    actual_diagonals = (
        sp.factor((diagonal_a * extension)[0]),
        sp.factor((diagonal_b * extension)[0]),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(
            actual_diagonals,
            expected_diagonals,
            strict=True,
        )
    )

    marked = marked_extension(
        distinguished,
        extension,
        alpha,
        marked_beta,
        marked_mode,
    )
    actual_minor = sp.factor(marked[marked_rows, :].det())
    assert sp.factor(actual_minor - expected_minor) == 0
    pure_column = one_marked_map(
        marked_mode,
        alpha,
        marked_beta,
    )[:, distinguished]
    assert any(entry != 0 for entry in pure_column)

    return {
        "label": label,
        "distinguished_coordinate": distinguished,
        "marking": [str(entry) for entry in shifts],
        "mixed_rank": mixed.rank(),
        "kernel_dimension": 2,
        "binary_diagonals": [str(entry) for entry in actual_diagonals],
        "marked_mode": marked_mode,
        "marked_rows": marked_rows,
        "marked_minor": str(actual_minor),
        "pure_transverse_column": [str(entry) for entry in pure_column],
    }


def specialize(rows, parameter: sp.Symbol, value):
    return tuple(
        tuple(sp.factor(sp.sympify(entry).subs(parameter, value)) for entry in row)
        for row in rows
    )


def main() -> None:
    e = sp.Symbol("e")
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    alpha = (
        (e + 1, -2, 0, 1 - e),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (1, -1, -1, 1),
    )
    canonical = (
        (1, -1, 1, 1),
        (1, 1, -1, 1),
        (e + 1, 1, 1, 1 - e),
        (0, 1, 1, 0),
    )
    beta = tuple(
        tuple(
            canonical[mode][coordinate]
            + t[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )

    pure = {
        word: permanent(
            tuple(
                canonical[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert pure[(1, 1, 1, 1)] == 4
    assert all(
        value == 0
        for word, value in pure.items()
        if word != (1, 1, 1, 1)
    )

    relative_projections = {
        distinguished: run_relative_projection(
            distinguished,
            alpha,
            beta,
            e,
        )
        for distinguished in range(4)
    }
    assert relative_projections == EXPECTED_RELATIVE_PROJECTIONS

    cases = [
        verify_case(
            label="all_e_q0",
            distinguished=0,
            alpha=alpha,
            beta=beta,
            shifts=(0, 1, 1, 1),
            kernel=(
                sp.Matrix((0, 0, -1, 0, 0, 1, 0, 0)),
                sp.Matrix((e + 1, 1, 2, 1, 1, 0, e + 1, 1)),
            ),
            expected_diagonals=(2 * (u - 2 * v), 2 * u),
            marked_mode=1,
            marked_rows=[0, 1, 5, 7],
            expected_minor=-8 * u * (u - 2 * v) ** 2,
        ),
        verify_case(
            label="all_e_q3",
            distinguished=3,
            alpha=alpha,
            beta=beta,
            shifts=(0, -1, 1, 1),
            kernel=(
                sp.Matrix((0, 0, -1, 0, 0, 1, 0, 0)),
                sp.Matrix((1 - e, -1, 2, 1, 1, 0, 1 - e, 1)),
            ),
            expected_diagonals=(-2 * (u - 2 * v), 2 * u),
            marked_mode=1,
            marked_rows=[0, 1, 5, 7],
            expected_minor=-8 * u * (u - 2 * v) ** 2,
        ),
    ]

    alpha_e0 = specialize(alpha, e, 0)
    beta_e0 = specialize(beta, e, 0)
    cases.extend(
        (
            verify_case(
                label="e0_extra_q0",
                distinguished=0,
                alpha=alpha_e0,
                beta=beta_e0,
                shifts=(-1, 0, 1, 1),
                kernel=(
                    sp.Matrix((1, 0, 0, 1, 0, 1, 1, 0)),
                    sp.Matrix((0, 1, 0, 0, 0, 0, 0, 1)),
                ),
                expected_diagonals=(-2 * (u - v), 2 * (u + v)),
                marked_mode=0,
                marked_rows=[0, 2, 4, 7],
                expected_minor=8 * (u - v) * (u + v) ** 2,
            ),
            verify_case(
                label="e0_extra_q3",
                distinguished=3,
                alpha=alpha_e0,
                beta=beta_e0,
                shifts=(-1, 0, 1, 1),
                kernel=(
                    sp.Matrix((1, 0, 0, 1, 0, 1, 1, 0)),
                    sp.Matrix((0, -1, 0, 0, 0, 0, 0, 1)),
                ),
                expected_diagonals=(2 * (u - v), 2 * (u + v)),
                marked_mode=0,
                marked_rows=[0, 2, 4, 7],
                expected_minor=8 * (u - v) * (u + v) ** 2,
            ),
        )
    )

    alpha_e1 = specialize(alpha, e, 1)
    beta_e1 = specialize(beta, e, 1)
    cases.append(
        verify_case(
            label="e1_q2",
            distinguished=2,
            alpha=alpha_e1,
            beta=beta_e1,
            shifts=(sp.Rational(-1, 2), 1, 1, 0),
            kernel=(
                sp.Matrix((0, 1, 0, -1, 1, 0, 0, 0)),
                sp.Matrix((0, -1, -1, 0, 0, -1, 0, 1)),
            ),
            expected_diagonals=(4 * (u - v), 4 * v),
            marked_mode=0,
            marked_rows=[0, 2, 3, 7],
            expected_minor=64 * v * (u - v) ** 2,
        )
    )

    alpha_em1 = specialize(alpha, e, -1)
    beta_em1 = specialize(beta, e, -1)
    cases.append(
        verify_case(
            label="em1_q2",
            distinguished=2,
            alpha=alpha_em1,
            beta=beta_em1,
            shifts=(sp.Rational(-1, 2), -1, 1, 0),
            kernel=(
                sp.Matrix((0, -1, 0, -1, 1, 0, 0, 0)),
                sp.Matrix((0, 1, -1, 0, 0, -1, 0, 1)),
            ),
            expected_diagonals=(-4 * (u - v), 4 * v),
            marked_mode=0,
            marked_rows=[0, 2, 3, 7],
            expected_minor=64 * v * (u - v) ** 2,
        )
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "global relative binary projection and all-extension "
            "one-marked minors"
        ),
        "curve_parameter": "e",
        "nonzero_pure_locus": "all e",
        "pure_coefficient": "4",
        "relative_projection_runs": len(relative_projections),
        "relative_binary_projection_ideals": {
            str(key): list(value)
            for key, value in relative_projections.items()
        },
        "hidden_complex_special_fibres_possible": False,
        "verified_survivor_cases": cases,
        "all_curve_markings_binary_classified": True,
        "all_genuine_binary_extensions_ternarily_excluded": True,
        "curve_H31_lift_possible": False,
        "second_component_generic_fibre_closed": False,
        "second_component_complete_marked_fibre_closed": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            POINT_THEOREM.name: sha256(POINT_THEOREM),
            C_CURVE_THEOREM.name: sha256(C_CURVE_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_diagonal_quadric_e_curve_marked_fibre_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
