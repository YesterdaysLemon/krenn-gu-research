#!/usr/bin/env python3
"""Verify generic H31 exclusion on directed-triangle components 16 and 17."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p4/classifications")
ROOT = REPO_ROOT

from verify_p4_directed_zero_divisor_triangle_components import (
    coefficients,
    raw_family,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
)


MINOR_ROWS = tuple(itertools.combinations(range(8), 4))


def pure_bases(kind: str, u: sp.Expr, v: sp.Expr):
    planes = raw_family(kind, u, v)
    alpha = []
    beta = []
    for mode, plane in enumerate(planes):
        if kind == "path" and mode == 0:
            alpha.append(tuple(plane.row(0) + plane.row(1)))
            beta.append(tuple(plane.row(1)))
        else:
            alpha.append(tuple(plane.row(0)))
            beta.append(tuple(plane.row(1)))
    return tuple(alpha), tuple(beta)


def shifted(beta, alpha, shifts):
    return tuple(
        tuple(
            beta[mode][coordinate]
            + shifts[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def projection_ideal(kind, distinguished, alpha, marked_beta, expected):
    u, v = sp.symbols("u v")
    shifts = sp.symbols("t0:4")
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inverse * (diagonal_b * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    lines = [
        "ring R=(0,u,v),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
        "J=std(J);",
    ]
    if expected is None:
        lines.extend(("int same=(reduce(1,J)==0);", '"CODEX_RESULT:"+string(same);'))
    else:
        lines.extend(
            (
                "ideal E=" + ",".join(map(singular, expected)) + ";",
                "E=std(E);",
                "ideal JE=reduce(J,E);",
                "ideal EJ=reduce(E,J);",
                "JE=simplify(JE,2);",
                "EJ=simplify(EJ,2);",
                "int same=((size(JE)==0)&&(size(EJ)==0));",
                '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
            )
        )
    lines.append("quit;")
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=65,
        check=False,
    )
    assert completed.returncode == 0, completed
    assert not completed.stderr.strip(), completed.stderr
    results = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(results) == 1, completed.stdout
    fields = results[0].split(":")
    assert fields[1] == "1", completed.stdout
    return {
        "kind": kind,
        "distinguished": distinguished,
        "unit": expected is None,
        "basis_size": None if expected is None else int(fields[2]),
    }


def sheet_data(kind, u, v, shifts):
    alpha, beta = pure_bases(kind, u, v)
    marked_beta = shifted(beta, alpha, shifts)
    return alpha, marked_beta


def binary_sheet_certificate(
    kind,
    distinguished,
    substitutions,
    marked_mode,
    first_rows,
    second_rows,
):
    u, v = sp.symbols("u v", nonzero=True)
    shifts = sp.symbols("t0:4")
    alpha, marked_beta = sheet_data(kind, u, v, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    mixed = mixed.subs(substitutions)
    diagonal_a = diagonal_a.subs(substitutions)
    diagonal_b = diagonal_b.subs(substitutions)
    marked_beta = tuple(
        tuple(entry.subs(substitutions) for entry in row)
        for row in marked_beta
    )
    kernel = mixed.nullspace()
    assert len(kernel) == 2
    pencil = sp.symbols("z0:2")
    extension = pencil[0] * kernel[0] + pencil[1] * kernel[1]
    diagonal_left = sp.factor((diagonal_a * extension)[0])
    diagonal_right = sp.factor((diagonal_b * extension)[0])
    marked = marked_extension(
        distinguished, extension, alpha, marked_beta, marked_mode
    )
    first = sp.factor(marked[list(first_rows), :].det())
    second = sp.factor(marked[list(second_rows), :].det())
    common = sp.factor(sp.gcd(first, second))
    ratio = sp.factor(common / (diagonal_left * diagonal_right))
    assert ratio != 0
    assert not (ratio.free_symbols & set(pencil))
    return {
        "kind": kind,
        "distinguished": distinguished,
        "marked_mode": marked_mode,
        "minor_rows": [list(first_rows), list(second_rows)],
        "gcd_over_diagonal_product": str(ratio),
    }


def star_central_line_certificate(u, v, h):
    shifts = sp.symbols("t0:4")
    substitutions = {shifts[0]: h, shifts[1]: 0, shifts[2]: 0, shifts[3]: 0}
    alpha, marked_beta = sheet_data("star", u, v, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(2, alpha, marked_beta)
    mixed = mixed.subs(substitutions)
    diagonal_a = diagonal_a.subs(substitutions)
    diagonal_b = diagonal_b.subs(substitutions)
    marked_beta = tuple(
        tuple(entry.subs(substitutions) for entry in row)
        for row in marked_beta
    )
    kernel = mixed.nullspace()
    assert len(kernel) == 3
    pencil = sp.symbols("z0:3")
    extension = sum(
        (pencil[index] * kernel[index] for index in range(3)),
        sp.zeros(8, 1),
    )
    diagonal_left = sp.factor((diagonal_a * extension)[0])
    diagonal_right = sp.factor((diagonal_b * extension)[0])

    marked_one = marked_extension(2, extension, alpha, marked_beta, 1)
    residual_rows = (
        (0, 2, 4, 7),
        (0, 3, 4, 7),
        (0, 3, 6, 7),
    )
    residuals = tuple(
        sp.factor(
            marked_one[list(rows), :].det()
            / (diagonal_left * diagonal_right)
        )
        for rows in residual_rows
    )
    expected = (
        -2 * h * u * pencil[0],
        -2 * h * u * pencil[2],
        2 * h * u * pencil[1],
    )
    assert all(sp.factor(left - right) == 0 for left, right in zip(residuals, expected, strict=True))

    # At h=0 the kernel basis stays three-dimensional, but a different
    # marked mode supplies one determinant proportional to A*B^2.
    marked_two = marked_extension(2, extension, alpha, marked_beta, 2)
    endpoint_minor = sp.factor(marked_two[[0, 4, 5, 7], :].det().subs(h, 0))
    endpoint_a = sp.factor(diagonal_left.subs(h, 0))
    endpoint_b = sp.factor(diagonal_right.subs(h, 0))
    endpoint_ratio = sp.factor(endpoint_minor / (endpoint_a * endpoint_b**2))
    assert endpoint_ratio == -(v - 1)
    return {
        "punctured_residuals": [str(residual) for residual in residuals],
        "endpoint_minor_over_A_B_squared": str(endpoint_ratio),
    }


def main() -> None:
    u, v = sp.symbols("u v", nonzero=True)
    shifts = sp.symbols("t0:4")

    # Confirm the pure factor bases before studying their marked fibres.
    for kind in ("star", "path"):
        alpha, beta = pure_bases(kind, u, v)
        planes = tuple(
            sp.Matrix((alpha[index], beta[index])) for index in range(4)
        )
        tensor = coefficients(planes)
        assert tensor[(1, 1, 1, 1)] != 0
        assert all(
            value == 0
            for word, value in tensor.items()
            if word != (1, 1, 1, 1)
        )

    expected_projection = {
        ("star", 0): (
            shifts[3],
            u * shifts[1] - v * shifts[2] - v,
            shifts[0],
            (shifts[2] + 1) * (v * shifts[2] + u + v),
        ),
        ("star", 1): (
            shifts[2],
            (u - v) * shifts[1] + (1 - u) * shifts[3] + u - v,
            u * shifts[0] + v,
            shifts[3] * (shifts[3] + 1),
        ),
        ("star", 2): (shifts[3], shifts[2], shifts[1]),
        ("star", 3): (
            shifts[2] + (v - 1) * (shifts[3] + 1),
            shifts[1],
            (u - 1) * shifts[0] + v - 1,
            (shifts[3] + 1) * ((v - 1) * shifts[3] + v - 2),
        ),
        ("path", 0): (shifts[3], shifts[2], shifts[1]),
        ("path", 1): None,
        ("path", 2): (shifts[3], shifts[1], shifts[0] * shifts[2]),
        ("path", 3): (
            (u + v) * shifts[3] + u + v - 1,
            shifts[2],
            shifts[1],
            (u + v - 1) * shifts[0] + v - 1,
        ),
    }
    projections = []
    for kind in ("star", "path"):
        alpha, beta = pure_bases(kind, u, v)
        marked_beta = shifted(beta, alpha, shifts)
        for distinguished in range(4):
            projections.append(
                projection_ideal(
                    kind,
                    distinguished,
                    alpha,
                    marked_beta,
                    expected_projection[(kind, distinguished)],
                )
            )

    point_sheets = (
        (
            "star",
            0,
            {shifts[0]: 0, shifts[1]: 0, shifts[2]: -1, shifts[3]: 0},
            2,
            (0, 1, 3, 7),
            (0, 1, 4, 7),
        ),
        (
            "star",
            0,
            {
                shifts[0]: 0,
                shifts[1]: -1,
                shifts[2]: -(u + v) / v,
                shifts[3]: 0,
            },
            2,
            (0, 1, 2, 7),
            (0, 1, 4, 7),
        ),
        (
            "star",
            1,
            {shifts[0]: -v / u, shifts[1]: -1, shifts[2]: 0, shifts[3]: 0},
            1,
            (0, 2, 3, 7),
            (0, 2, 4, 7),
        ),
        (
            "star",
            1,
            {
                shifts[0]: -v / u,
                shifts[1]: (v + 1 - 2 * u) / (u - v),
                shifts[2]: 0,
                shifts[3]: -1,
            },
            1,
            (0, 1, 2, 7),
            (0, 1, 4, 7),
        ),
        (
            "star",
            3,
            {
                shifts[0]: -(v - 1) / (u - 1),
                shifts[1]: 0,
                shifts[2]: 0,
                shifts[3]: -1,
            },
            1,
            (0, 1, 2, 7),
            (0, 1, 4, 7),
        ),
        (
            "star",
            3,
            {
                shifts[0]: -(v - 1) / (u - 1),
                shifts[1]: 0,
                shifts[2]: -1,
                shifts[3]: -(v - 2) / (v - 1),
            },
            1,
            (0, 1, 2, 7),
            (0, 1, 4, 7),
        ),
        (
            "path",
            3,
            {
                shifts[0]: -(v - 1) / (u + v - 1),
                shifts[1]: 0,
                shifts[2]: 0,
                shifts[3]: -(u + v - 1) / (u + v),
            },
            1,
            (0, 1, 2, 7),
            (0, 1, 3, 7),
        ),
    )
    binary_certificates = [
        binary_sheet_certificate(*sheet) for sheet in point_sheets
    ]

    h = sp.Symbol("h", nonzero=True)
    line_sheets = (
        (
            "path",
            0,
            {shifts[0]: h, shifts[1]: 0, shifts[2]: 0, shifts[3]: 0},
            1,
            (0, 2, 3, 7),
            (0, 2, 6, 7),
        ),
        (
            "path",
            2,
            {shifts[0]: 0, shifts[1]: 0, shifts[2]: h, shifts[3]: 0},
            2,
            (0, 1, 3, 7),
            (0, 1, 4, 7),
        ),
        (
            "path",
            2,
            {shifts[0]: h, shifts[1]: 0, shifts[2]: 0, shifts[3]: 0},
            1,
            (0, 2, 3, 7),
            (0, 2, 4, 7),
        ),
    )
    binary_certificates.extend(
        binary_sheet_certificate(*sheet) for sheet in line_sheets
    )
    central_line = star_central_line_certificate(u, v, h)

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(u,v)",
                "projection_ideals": projections,
                "marked_sheets": {"star": 7, "path": 4},
                "binary_pencil_certificates": binary_certificates,
                "star_central_line_certificate": central_line,
                "components_excluded_generically_for_H31": [16, 17],
                "parameter_search_used": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
