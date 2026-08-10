#!/usr/bin/env python3
"""Verify generic marked-H31 exclusion on pure-P4 component nineteen."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
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

from krenn_gu.p5_marked_basis import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)

ROOT = REPO_ROOT
THEOREM = (
    HERE / "P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = REPO_ROOT / "claims/p4/classifications/P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md"
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


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(coefficient * entry) for entry in row)


def pure_bases(
    p: sp.Symbol,
    q: sp.Symbol,
    phi: sp.Symbol,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    a_bar = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    b_bar = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    row_00 = add(a_bar, scale(p, b))
    row_01 = add(b_bar, scale(q, b))
    alpha_0 = add(scale(q - phi, row_00), scale(-p, row_01))
    alpha = (alpha_0, b, b_bar, a_bar)
    beta = (row_00, a, a, add(b, scale(phi, b_bar)))
    return alpha, beta


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
            "ring R=(0,p,q,phi),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
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
        timeout=120,
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


def assert_zero(expressions: sp.Matrix) -> None:
    assert all(sp.factor(entry) == 0 for entry in expressions)


def assert_equal(left: sp.Expr, right: sp.Expr) -> None:
    assert sp.factor(left - right) == 0, (sp.factor(left), sp.factor(right))


def punctured_line_certificate(
    distinguished: int,
    branch: str,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, object]:
    p, q, phi = sp.symbols("p q phi")
    r = q - phi
    t = sp.Symbol("t")
    a, b, c, d = sp.symbols("a b c d")
    h = sp.symbols("h0:4")
    if branch == "h1_zero":
        substitutions = {h[0]: -1 / r, h[1]: 0, h[2]: t, h[3]: 0}
        marked_mode = 1
        if distinguished == 2:
            extension = sp.Matrix((-p * d, c, a, 0, b, 0, t * c, d))
            residuals = (a * (phi - 1) + d, c * (phi - 1) + d)
        else:
            extension = sp.Matrix((p * d, -c, a, 0, b, 0, t * c, d))
            residuals = (a * (phi + 1) + d, c * (phi + 1) + d)
    elif branch == "h2_zero":
        substitutions = {h[0]: -1 / r, h[1]: t, h[2]: 0, h[3]: 0}
        marked_mode = 2
        if distinguished == 2:
            extension = sp.Matrix((-p * d, a, c, 0, b, t * c, 0, d))
            residuals = (a * (phi - 1) - d, c * (phi - 1) - d)
        else:
            extension = sp.Matrix((p * d, a, -c, 0, b, t * c, 0, d))
            residuals = (a * (phi + 1) + d, c * (phi + 1) + d)
    else:
        raise ValueError(branch)

    marked_beta = shifted_basis(alpha, beta, h)
    marked_beta = tuple(
        tuple(entry.subs(substitutions) for entry in row) for row in marked_beta
    )
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    assert mixed.rank() == 4
    assert_zero(mixed * extension)
    kernel_frame = extension.jacobian((a, b, c, d))
    assert kernel_frame.rank() == 4

    first_diagonal = sp.factor((diagonal_alpha * extension)[0])
    second_diagonal = sp.factor((diagonal_beta * extension)[0])
    if distinguished == 2:
        binary_factor = p * d * (q - 1) - b * r * (phi - 1)
        expected_second = 2 * binary_factor / r
        if branch == "h1_zero":
            expected_first = -2 * r * (a - c)
        else:
            expected_first = 2 * r * (a - c)
    else:
        binary_factor = p * d * (q + 1) + b * r * (phi + 1)
        expected_second = 2 * binary_factor / r
        expected_first = -2 * r * (a - c)
    assert_equal(first_diagonal, expected_first)
    assert_equal(second_diagonal, expected_second)

    marked = marked_extension(distinguished, extension, alpha, marked_beta, marked_mode)
    rows = ((0, 1, 2, 7), (0, 2, 3, 7))
    determinants = tuple(sp.factor(marked[list(row_set), :].det()) for row_set in rows)
    ratios = tuple(
        sp.factor(sp.cancel(determinant / (first_diagonal * second_diagonal)))
        for determinant in determinants
    )
    expected_ratios = (
        -2 * t * r**2 * residuals[0],
        2 * t**2 * r**2 * residuals[1],
    )
    for observed, expected in zip(ratios, expected_ratios, strict=True):
        assert_equal(observed, expected)

    common_factor = phi - 1 if distinguished == 2 else phi + 1
    assert_equal(residuals[0] - residuals[1], common_factor * (a - c))
    pure_marked = one_marked_map(marked_mode, alpha, marked_beta)
    transverse_entry = sp.factor(pure_marked[0, distinguished])
    expected_transverse = {
        (2, "h1_zero"): 2 * r,
        (2, "h2_zero"): -2 * r,
        (3, "h1_zero"): -2 * r,
        (3, "h2_zero"): -2 * r,
    }[(distinguished, branch)]
    assert_equal(transverse_entry, expected_transverse)
    return {
        "distinguished_coordinate": distinguished,
        "marking_line": branch,
        "marked_mode": marked_mode,
        "mixed_rank": 4,
        "kernel_dimension": 4,
        "minor_rows": [list(row_set) for row_set in rows],
        "minor_over_diagonal_product": [str(value) for value in ratios],
        "common_zero_forces_first_diagonal_zero": True,
        "pure_transverse_entry": {
            "row": 0,
            "column": distinguished,
            "value": str(transverse_entry),
        },
        "global_third_row_forced_zero": True,
        "scope": "t!=0",
    }


def endpoint_certificate(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, object]:
    p, q, phi = sp.symbols("p q phi")
    r = q - phi
    a, b, c, d = sp.symbols("a b c d")
    h = sp.symbols("h0:4")
    substitutions = {h[0]: -1 / r, h[1]: 0, h[2]: 0, h[3]: 0}
    marked_beta = shifted_basis(alpha, beta, h)
    marked_beta = tuple(
        tuple(entry.subs(substitutions) for entry in row) for row in marked_beta
    )

    if distinguished == 2:
        extension = sp.Matrix((-p * d, a, c, 0, b, 0, 0, d))
        expected_first = 2 * r * (a - c)
        binary_factor = p * d * (q - 1) - b * r * (phi - 1)
        residuals = (a * (phi - 1) + d, a * p * (q - 1) + b * r)
        syzygy = p * (q - 1) * residuals[0] - (phi - 1) * residuals[1]
        signs = (sp.Integer(2), sp.Integer(2))
    else:
        extension = sp.Matrix((p * d, a, c, 0, b, 0, 0, d))
        expected_first = -2 * r * (a + c)
        binary_factor = p * d * (q + 1) + b * r * (phi + 1)
        residuals = (a * (phi + 1) - d, a * p * (q + 1) + b * r)
        syzygy = (phi + 1) * residuals[1] - p * (q + 1) * residuals[0]
        signs = (sp.Integer(-2), sp.Integer(-2))

    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    assert mixed.rank() == 4
    assert_zero(mixed * extension)
    kernel_frame = extension.jacobian((a, b, c, d))
    assert kernel_frame.rank() == 4
    first_diagonal = sp.factor((diagonal_alpha * extension)[0])
    second_diagonal = sp.factor((diagonal_beta * extension)[0])
    assert_equal(first_diagonal, expected_first)
    assert_equal(second_diagonal, 2 * binary_factor / r)
    assert_equal(binary_factor, syzygy)

    marked = marked_extension(distinguished, extension, alpha, marked_beta, 3)
    rows = ((0, 1, 3, 7), (0, 3, 5, 7))
    determinants = tuple(sp.factor(marked[list(row_set), :].det()) for row_set in rows)
    ratios = tuple(
        sp.factor(sp.cancel(determinant / (first_diagonal * second_diagonal)))
        for determinant in determinants
    )
    expected_ratios = (
        signs[0] * p**2 * residuals[0],
        signs[1] * p * residuals[1] / r,
    )
    for observed, expected in zip(ratios, expected_ratios, strict=True):
        assert_equal(observed, expected)

    pure_marked = one_marked_map(3, alpha, marked_beta)
    transverse_entry = sp.factor(pure_marked[3, distinguished])
    expected_transverse = (
        -2 * p * (phi - 1) if distinguished == 2 else -2 * p * (phi + 1)
    )
    assert_equal(transverse_entry, expected_transverse)

    return {
        "distinguished_coordinate": distinguished,
        "marking_point": "h1=h2=h3=0, (q-phi)*h0=-1",
        "marked_mode": 3,
        "mixed_rank": 4,
        "kernel_dimension": 4,
        "minor_rows": [list(row_set) for row_set in rows],
        "minor_over_diagonal_product": [str(value) for value in ratios],
        "binary_factor_syzygy": str(sp.factor(syzygy)),
        "common_zero_forces_second_diagonal_zero": True,
        "pure_transverse_entry": {
            "row": 3,
            "column": distinguished,
            "value": str(transverse_entry),
        },
        "global_third_row_forced_zero": True,
    }


def main() -> None:
    p, q, phi = sp.symbols("p q phi")
    h = sp.symbols("h0:4")
    alpha, beta = pure_bases(p, q, phi)

    tensor = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert tensor[(1, 1, 1, 1)] == 4 * p
    assert all(value == 0 for word, value in tensor.items() if word != (1, 1, 1, 1))
    marked_beta = shifted_basis(alpha, beta, h)
    marked_tensor = {
        word: sp.factor(
            permanent(
                tuple(
                    marked_beta[mode] if word[mode] else alpha[mode]
                    for mode in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert marked_tensor == tensor

    expected_projection = {
        0: (sp.Integer(1),),
        1: (sp.Integer(1),),
        2: (h[3], (q - phi) * h[0] + 1, h[1] * h[2]),
        3: (h[3], (q - phi) * h[0] + 1, h[1] * h[2]),
    }
    projections = [
        projection_certificate(
            distinguished, alpha, beta, expected_projection[distinguished]
        )
        for distinguished in range(4)
    ]

    punctured = [
        punctured_line_certificate(distinguished, branch, alpha, beta)
        for distinguished in (2, 3)
        for branch in ("h1_zero", "h2_zero")
    ]
    endpoints = [
        endpoint_certificate(distinguished, alpha, beta) for distinguished in (2, 3)
    ]

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(p,q,phi)",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
                "pure_support": {"1111": "4*p"},
                "all_affine_markings": True,
                "projection_certificates": projections,
                "residual_marking_lines": 4,
                "punctured_line_certificates": punctured,
                "shared_endpoint_certificates": endpoints,
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
