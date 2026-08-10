#!/usr/bin/env python3
"""Verify generic marked-H31 exclusion on pure-P4 component twenty."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.expand(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def pure_bases(
    p: sp.Symbol, q: sp.Symbol
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    s = p - q + 1
    e = (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0))
    alpha = (
        (sp.Integer(0), -p * (p + 1), q * (q - 1), s),
        e,
        e,
        (sp.Integer(1), sp.Integer(1), sp.Integer(1), sp.Integer(0)),
    )
    beta = (
        (-s, -p - q, p + q, sp.Integer(0)),
        (sp.Integer(0), p + 1, q - 1, sp.Integer(1)),
        (sp.Integer(0), p, q, sp.Integer(1)),
        e,
    )
    return alpha, beta


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def assert_zero(matrix: sp.Matrix) -> None:
    assert all(sp.factor(entry) == 0 for entry in matrix)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact projection replay")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def projection_certificate(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    expected: tuple[sp.Expr, ...],
) -> dict[str, object]:
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    program = "\n".join(
        (
            "ring R=(0,p,q),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
            "J=std(J);",
            "ideal E=" + ",".join(map(singular, expected)) + ";",
            "E=std(E);",
            "ideal JE=reduce(J,E);",
            "ideal EJ=reduce(E,J);",
            "JE=simplify(JE,2);",
            "EJ=simplify(EJ,2);",
            "int same=((size(JE)==0)&&(size(EJ)==0));",
            '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=180,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "distinguished_coordinate": distinguished,
        "projected_ideal": [singular(entry) for entry in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(size),
    }


def residual_cases(
    p: sp.Symbol, q: sp.Symbol, shifts: tuple[sp.Symbol, ...]
) -> tuple[dict[str, object], ...]:
    s = p - q + 1
    return (
        {
            "label": "C1",
            "distinguished": 1,
            "marking": {shifts[0]: 0, shifts[1]: 1 - q, shifts[2]: 0, shifts[3]: 0},
            "v0": (-p * (p + 1), 0, 0, 1, -p - q, p + 1, p, 0),
            "v1": (p * q, -1, -1, 0, 2 * q - 1, -q, 0, 1),
            "expected_beta": 2 * s * (sp.Symbol("T") * (p + q) - 2 * q + 1),
        },
        {
            "label": "C2",
            "distinguished": 1,
            "marking": {shifts[0]: 0, shifts[1]: 0, shifts[2]: -q, shifts[3]: 0},
            "v0": (-p * (p + 1), 0, 0, 1, -p - q, p + 1, p, 0),
            "v1": (
                0,
                -1,
                -1,
                (q - 1) / p,
                q * s / p,
                (p + 1) * (q - 1) / p,
                0,
                1,
            ),
            "expected_beta": 2
            * s
            * (sp.Symbol("T") * (p + q) - q * s / p),
        },
        {
            "label": "C3",
            "distinguished": 2,
            "marking": {
                shifts[0]: 0,
                shifts[1]: -p - 1,
                shifts[2]: 0,
                shifts[3]: 0,
            },
            "v0": (q * (q - 1), 0, 0, 1, p + q, q - 1, q, 0),
            "v1": (-p * q, -1, -1, 0, -2 * p - 1, -p, 0, 1),
            "expected_beta": 2 * s * (sp.Symbol("T") * (p + q) - 2 * p - 1),
        },
        {
            "label": "C4",
            "distinguished": 2,
            "marking": {shifts[0]: 0, shifts[1]: 0, shifts[2]: -p, shifts[3]: 0},
            "v0": (q * (q - 1), 0, 0, 1, p + q, q - 1, q, 0),
            "v1": (
                0,
                -1,
                -1,
                (p + 1) / q,
                p * s / q,
                (p + 1) * (q - 1) / q,
                0,
                1,
            ),
            "expected_beta": 2
            * s
            * (sp.Symbol("T") * (p + q) + p * s / q),
        },
    )


def residual_certificate(
    case: dict[str, object],
    alpha: tuple[tuple[sp.Expr, ...], ...],
    canonical_beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Symbol, ...],
) -> dict[str, object]:
    p, q = sp.symbols("p q")
    s = p - q + 1
    parameter = sp.Symbol("T")
    distinguished = int(case["distinguished"])
    marking = case["marking"]
    assert isinstance(marking, dict)
    beta = shifted_basis(alpha, canonical_beta, shifts)
    beta = tuple(tuple(entry.subs(marking) for entry in row) for row in beta)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
    v0 = sp.Matrix(case["v0"])
    v1 = sp.Matrix(case["v1"])
    frame = sp.Matrix.hstack(v0, v1)
    assert mixed.rank() == 6
    assert frame.rank() == 2
    assert_zero(mixed * frame)
    extension = parameter * v0 + v1
    first_diagonal = sp.factor((diagonal_alpha * extension)[0])
    second_diagonal = sp.factor((diagonal_beta * extension)[0])
    assert_equal(first_diagonal, -2 * s)
    expected_beta = case["expected_beta"]
    assert isinstance(expected_beta, sp.Expr)
    assert_equal(second_diagonal, expected_beta)

    neighbouring = marked_extension(distinguished, extension, alpha, beta, 3)
    selected_rows = (0, 1, 4, 7)
    determinant = sp.factor(neighbouring[list(selected_rows), :].det())
    determinant_over_beta = sp.factor(sp.cancel(determinant / second_diagonal))
    expected_ratio = 4 * p * q * (p + q) * s
    assert_equal(determinant_over_beta, expected_ratio)

    pure = one_marked_map(3, alpha, beta)
    transverse = sp.factor(pure[1, distinguished])
    expected_transverse = p * q if distinguished == 1 else -p * q
    assert_equal(transverse, expected_transverse)
    return {
        "label": case["label"],
        "distinguished_coordinate": distinguished,
        "marking": [str(marking[shift]) for shift in shifts],
        "mixed_rank": 6,
        "kernel_dimension": 2,
        "projective_kernel_parameterization": "z=T*v0+v1",
        "all_alpha_diagonal": str(first_diagonal),
        "all_beta_diagonal": str(second_diagonal),
        "marked_mode": 3,
        "minor_rows": list(selected_rows),
        "minor_over_beta_diagonal": str(determinant_over_beta),
        "pure_transverse_entry": {
            "row": 1,
            "column": distinguished,
            "value": str(transverse),
        },
        "global_third_row_forced_zero": True,
    }


def main() -> None:
    p, q = sp.symbols("p q")
    shifts = sp.symbols("h0:4")
    s = p - q + 1
    alpha, canonical_beta = pure_bases(p, q)

    # Reconstruct the normalized U0 rows and the simplified intrinsic kernel.
    r0 = sp.Matrix((-s / (p + q), -1, 1, 0))
    r1 = sp.Matrix((q * (q - 1) / (p + q), -p - q, 0, 1))
    assert_zero(
        sp.Matrix(alpha[0]) - (q * (q - 1) * r0 + s * r1)
    )
    assert_zero(sp.Matrix(canonical_beta[0]) - (p + q) * r0)

    beta = shifted_basis(alpha, canonical_beta, shifts)
    tensor = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert_equal(tensor[(1, 1, 1, 1)], 2 * (p + q) * s)
    assert all(value == 0 for word, value in tensor.items() if word != (1, 1, 1, 1))

    expected_projection = {
        0: (sp.Integer(1),),
        1: (
            shifts[0],
            shifts[3],
            shifts[2] * (shifts[2] + q),
            q * shifts[1] + (q - 1) * shifts[2] + q * (q - 1),
        ),
        2: (
            shifts[0],
            shifts[3],
            shifts[2] * (shifts[2] + p),
            p * shifts[1] + (p + 1) * shifts[2] + p * (p + 1),
        ),
        3: (sp.Integer(1),),
    }
    projections = [
        projection_certificate(
            distinguished, alpha, canonical_beta, expected_projection[distinguished]
        )
        for distinguished in range(4)
    ]
    residuals = [
        residual_certificate(case, alpha, canonical_beta, shifts)
        for case in residual_cases(p, q, shifts)
    ]

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(p,q)",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "pure_support": {"1111": "2*(p+q)*(p-q+1)"},
                "all_affine_markings": True,
                "projection_certificates": projections,
                "residual_marking_points": 4,
                "residual_certificates": residuals,
                "generic_marked_H31_fibre_empty": True,
                "weighted_H22_closed": False,
                "component_boundaries_closed": False,
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
