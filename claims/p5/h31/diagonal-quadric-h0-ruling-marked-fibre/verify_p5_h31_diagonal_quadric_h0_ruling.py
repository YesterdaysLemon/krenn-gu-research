#!/usr/bin/env python3
"""Verify the marked H31 obstruction on the H=0 diagonal ruling."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.singular_runtime import singular_command_with_timeout
from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md"
)
COMPONENT = (
    REPO_ROOT / 'claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md')
SLICE_THEOREM = (
    REPO_ROOT / 'claims/p5/h31/diagonal-quadric-pure-direction-curve-marked-fibre/P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md'
)
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
EXPECTED_RELATIVE_PROJECTIONS = {
    0: ("1",),
    1: ("t3", "t2-1", "t1-e", "t0*e+1"),
    2: ("t3", "t2+1", "t1-e", "t0*e+1"),
    3: ("t3-1", "t2-e", "t1-e", "2*t0+e", "e^2-1"),
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


def pluecker(plane: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.factor(plane[:, (left, right)].det())
        for left, right in itertools.combinations(range(4), 2)
    )


def proportional(left, right) -> bool:
    return all(
        sp.factor(left[i] * right[j] - left[j] * right[i]) == 0
        for i in range(len(left))
        for j in range(len(left))
    )


def run_relative_projection(
    distinguished: int,
    alpha,
    beta,
    parameter: sp.Symbol,
    timeout: float = 120,
) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    diagonal_inverse = sp.Symbol("ub")
    pure_inverse = sp.Symbol("up")
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
            diagonal_inverse * (diagonal_b * extension)[0] - 1,
            pure_inverse * parameter - 1,
        )
    )
    eliminated = extensions + (diagonal_inverse, pure_inverse)
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
        tuple(
            sp.factor(sp.sympify(entry).subs(parameter, value))
            for entry in row
        )
        for row in rows
    )


def normal_planes(C, E):
    return (
        sp.Matrix(((E, -1, -1, -E), (1, -1, 1, 1))),
        sp.Matrix(((1, 0, 0, -1), (1, C + 1, C - 1, 1))),
        sp.Matrix(((E, 1, 1, -E), (0, 1, -1, 0))),
        sp.Matrix(((1, 0, 0, 1), (0, 1, 1, 0))),
    )


def main() -> None:
    e = sp.Symbol("e")
    t = sp.symbols("t0:4")
    u, v = sp.symbols("u v")
    alpha = (
        (2 * e, -e - 1, e - 1, 0),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (e, -1, -1, e),
    )
    canonical = (
        (1, -1, 1, 1),
        (e, e + 1, 1 - e, e),
        (e, 1, 1, -e),
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
    planes = tuple(
        sp.Matrix.vstack(
            sp.Matrix(alpha[mode]).T,
            sp.Matrix(canonical[mode]).T,
        )
        for mode in range(4)
    )
    fixed_minors = (
        sp.factor(planes[0][:, (1, 2)].det()),
        sp.factor(planes[1][:, (0, 3)].det()),
        sp.factor(planes[2][:, (1, 2)].det()),
        sp.factor(planes[3][:, (0, 1)].det()),
    )
    assert fixed_minors == (-2, 2 * e, 2, e)

    pure = {
        word: permanent(
            tuple(
                canonical[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert sp.factor(pure[(1, 1, 1, 1)] - 4 * e) == 0
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
            label="all_e_q1",
            distinguished=1,
            alpha=alpha,
            beta=beta,
            shifts=(-1 / e, e, 1, 0),
            kernel=(
                sp.Matrix((0, -1 / e, 0, 0, 0, 0, 1, 0)),
                sp.Matrix((-e - 1, 2 / e, 1, -1, 1 / e, e + 1, 0, 1)),
            ),
            expected_diagonals=(2 * e * (u - 2 * v), 2 * e * u),
            marked_mode=2,
            marked_rows=[0, 4, 5, 7],
            expected_minor=-8 * u * (u - 2 * v) ** 2,
        ),
        verify_case(
            label="all_e_q2",
            distinguished=2,
            alpha=alpha,
            beta=beta,
            shifts=(-1 / e, e, -1, 0),
            kernel=(
                sp.Matrix((0, -1 / e, 0, 0, 0, 0, 1, 0)),
                sp.Matrix((e - 1, 2 / e, -1, -1, 1 / e, 1 - e, 0, 1)),
            ),
            expected_diagonals=(-2 * e * (u - 2 * v), 2 * e * u),
            marked_mode=2,
            marked_rows=[0, 4, 5, 7],
            expected_minor=-8 * u * (u - 2 * v) ** 2,
        ),
    ]

    alpha_e1 = specialize(alpha, e, 1)
    beta_e1 = specialize(beta, e, 1)
    cases.append(
        verify_case(
            label="e1_q3",
            distinguished=3,
            alpha=alpha_e1,
            beta=beta_e1,
            shifts=(sp.Rational(-1, 2), 1, 1, 1),
            kernel=(
                sp.Matrix((0, 0, 1, 1, 1, 0, 0, 0)),
                sp.Matrix((0, -1, -1, 0, 0, 0, -1, 1)),
            ),
            expected_diagonals=(4 * (u - v), 4 * v),
            marked_mode=0,
            marked_rows=[0, 4, 5, 7],
            expected_minor=-64 * v * (u - v) ** 2,
        )
    )

    alpha_em1 = specialize(alpha, e, -1)
    beta_em1 = specialize(beta, e, -1)
    cases.append(
        verify_case(
            label="em1_q3",
            distinguished=3,
            alpha=alpha_em1,
            beta=beta_em1,
            shifts=(sp.Rational(1, 2), -1, -1, 1),
            kernel=(
                sp.Matrix((0, 0, 1, -1, 1, 0, 0, 0)),
                sp.Matrix((0, 1, 1, 0, 0, 0, -1, 1)),
            ),
            expected_diagonals=(4 * (u + v), 4 * v),
            marked_mode=0,
            marked_rows=[0, 4, 5, 7],
            expected_minor=-64 * v * (u + v) ** 2,
        )
    )

    C, E = sp.symbols("C E")
    h0_slice = sp.factor(1 - C**2 * E**2)
    assert sp.factor(
        h0_slice + (C * E - 1) * (C * E + 1)
    ) == 0
    source_swap = sp.Matrix(
        (
            (0, 0, 0, 1),
            (0, 1, 0, 0),
            (0, 0, 1, 0),
            (1, 0, 0, 0),
        )
    )
    plus_planes = normal_planes(1 / e, e)
    minus_planes = normal_planes(1 / e, -e)
    assert all(
        proportional(
            pluecker(plus_planes[mode] * source_swap),
            pluecker(minus_planes[mode]),
        )
        for mode in range(4)
    )

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "saturated relative binary projection, all-extension marked "
            "minors, and opposite-ruling source symmetry"
        ),
        "curve_parameter": "e",
        "nonzero_pure_locus": "e!=0",
        "pure_coefficient": "4*e",
        "relative_projection_runs": len(relative_projections),
        "relative_binary_projection_ideals": {
            str(key): list(value)
            for key, value in relative_projections.items()
        },
        "hidden_complex_special_fibres_possible": False,
        "verified_survivor_cases": cases,
        "all_genuine_binary_extensions_ternarily_excluded": True,
        "H0_slice_equation": str(h0_slice),
        "opposite_ruling_source_symmetric": True,
        "complete_nonzero_H0_slice_excluded": True,
        "second_component_generic_fibre_closed": False,
        "second_component_complete_marked_fibre_closed": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            SLICE_THEOREM.name: sha256(SLICE_THEOREM),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_diagonal_quadric_h0_ruling_verified.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
