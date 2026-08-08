#!/usr/bin/env python3
"""Verify the generic marked H31 obstruction on P4 component fifteen."""

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
ROOT = REPO_ROOT

from verify_p4_directed_zero_divisor_triangle_components import coefficients
from verify_p5_h31_marked_basis_open_branch import marked_extension, mixed_matrix


MINOR_ROWS = {
    0: ((0, 1, 2, 7), (0, 1, 3, 7)),
    1: ((0, 1, 2, 7), (0, 1, 3, 7)),
    2: ((0, 1, 2, 7), (0, 2, 3, 7)),
    3: ((0, 1, 2, 7), (0, 2, 3, 7)),
}


def normalized_family(p, q, rho):
    a = (1, 1, 0, 0)
    a_bar = (1, -1, 0, 0)
    b = (0, 0, 1, 1)
    b_bar = (0, 0, 1, -1)
    ell = tuple(a[index] + b_bar[index] for index in range(4))
    ell_bar = tuple(a[index] - b_bar[index] for index in range(4))
    k = tuple(a_bar[index] + p * b[index] for index in range(4))
    k_bar = tuple(b[index] + q * a_bar[index] for index in range(4))
    other = tuple(ell_bar[index] + rho * a_bar[index] for index in range(4))
    alpha_3 = tuple(
        p * rho * k_bar[index] - (p * q + 1) * other[index]
        for index in range(4)
    )
    planes = ((a, b), (a_bar, b_bar), (k, ell), (k_bar, other))
    alpha = (a, b_bar, ell, alpha_3)
    beta = (b, a_bar, k, k_bar)
    return planes, alpha, beta


def shifted_beta(alpha, beta, point):
    return tuple(
        tuple(
            beta[mode][coordinate] + point[mode] * alpha[mode][coordinate]
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def source_torus_certificate():
    s, t, lam, m, n, rho = sp.symbols("s t lambda m n rho", nonzero=True)
    p = m / lam
    q = lam * n
    diagonal = (1, 1 / s, 1 / lam, 1 / (lam * t))
    a = (1, s, 0, 0)
    a_bar = (1, -s, 0, 0)
    b = (0, 0, 1, t)
    b_bar = (0, 0, 1, -t)
    ell = tuple(a[index] + lam * b_bar[index] for index in range(4))
    ell_bar = tuple(a[index] - lam * b_bar[index] for index in range(4))
    k = tuple(a_bar[index] + m * b[index] for index in range(4))
    k_bar = tuple(b[index] + n * a_bar[index] for index in range(4))
    other = tuple(ell_bar[index] + rho * a_bar[index] for index in range(4))
    original = ((a, b), (a_bar, b_bar), (k, ell), (k_bar, other))
    transformed = []
    for mode, plane in enumerate(original):
        rows = [
            tuple(sp.cancel(row[index] * diagonal[index]) for index in range(4))
            for row in plane
        ]
        if mode in (0, 1):
            rows[1] = tuple(sp.cancel(lam * entry) for entry in rows[1])
        if mode == 3:
            rows[0] = tuple(sp.cancel(lam * entry) for entry in rows[0])
        transformed.append(tuple(rows))
    expected, _, _ = normalized_family(p, q, rho)
    assert transformed == list(expected)
    return {
        "source_diagonal": [str(value) for value in diagonal],
        "quotient_parameters": {"p": "m/lambda", "q": "lambda*n", "rho": "rho"},
    }


def projection_ideal(distinguished, alpha, beta):
    p, q, rho = sp.symbols("p q rho")
    shifts = sp.symbols("h0:4")
    marked_beta = shifted_beta(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extensions = sp.symbols("z0:8")
    inverse = sp.Symbol("w")
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        inverse * (diagonal_b * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    expected = (shifts[3], rho * shifts[2] - p * q - 1, shifts[1], shifts[0])
    lines = [
        "ring R=(0,p,q,rho),("
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
    ]
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input="\n".join(lines),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=80,
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
        "distinguished": distinguished,
        "basis_size": int(fields[2]),
        "ideal": [str(value) for value in expected],
    }


def kernel_basis(distinguished, p, q, rho):
    first = {
        0: (0, 0, 0, -rho, 0, 0, 1, 0),
        1: (0, 0, 0, -rho, 0, 0, 1, 0),
        2: (0, 0, 0, rho, 0, 0, 1, 0),
        3: (0, 0, 0, rho, 0, 0, 1, 0),
    }[distinguished]
    second = {
        0: (1 / q, 0, 1 / q, 0, 0, 1 / q, 0, 1),
        1: (-1 / q, 0, -1 / q, 0, 0, 1 / q, 0, 1),
        2: (0, 1, 1, 0, 1, 0, 0, 1),
        3: (0, -1, -1, 0, 1, 0, 0, 1),
    }[distinguished]
    return sp.Matrix(first), sp.Matrix(second)


def pencil_certificate(distinguished, p, q, rho, alpha, beta):
    x, y = sp.symbols("x y")
    point = (0, 0, (p * q + 1) / rho, 0)
    marked_beta = shifted_beta(alpha, beta, point)
    mixed, diagonal_a_row, diagonal_b_row = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    first, second = kernel_basis(distinguished, p, q, rho)
    assert mixed.rank() == 6
    assert all(sp.cancel(value) == 0 for value in mixed * first)
    assert all(sp.cancel(value) == 0 for value in mixed * second)
    extension = x * first + y * second
    diagonal_a = sp.factor((diagonal_a_row * extension)[0])
    diagonal_b = sp.factor((diagonal_b_row * extension)[0])
    marked = marked_extension(
        distinguished, extension, alpha, marked_beta, 0
    )
    rows = MINOR_ROWS[distinguished]
    determinants = tuple(
        sp.factor(marked[list(row_set), :].det()) for row_set in rows
    )
    residuals = tuple(
        sp.factor(determinant / (diagonal_a * diagonal_b))
        for determinant in determinants
    )
    expected_residuals = {
        0: (
            4 * q * x * (p * q - rho + 1),
            2 * q * (q * rho * x + (rho - p * q - 1) * y) / rho,
        ),
        1: (
            -4 * q * x * (p * q + rho + 1),
            2 * q * (q * rho * x + (p * q + rho + 1) * y) / rho,
        ),
        2: (
            4 * q * y * (p * q - rho + 1) * (p * q + rho + 1) / rho,
            -2
            * q
            * (p * q - rho + 1)
            * (p * q + rho + 1)
            * (rho * x + (p * q - p * rho + 1) * y)
            / rho**2,
        ),
        3: (
            -4 * q * y * (p * q - rho + 1) * (p * q + rho + 1) / rho,
            -2
            * q
            * (p * q - rho + 1)
            * (p * q + rho + 1)
            * (rho * x - (p * q + p * rho + 1) * y)
            / rho**2,
        ),
    }[distinguished]
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(residuals, expected_residuals, strict=True)
    )
    field = sp.QQ.frac_field(p, q, rho)
    residual_polynomials = tuple(
        sp.Poly(value, x, y, domain=field) for value in residuals
    )
    residual_gcd = sp.gcd(*residual_polynomials)
    assert residual_gcd.total_degree() == 0
    return {
        "distinguished": distinguished,
        "marking_point": [str(value) for value in point],
        "mixed_rank": 6,
        "kernel_basis": [
            [str(sp.factor(value)) for value in first],
            [str(sp.factor(value)) for value in second],
        ],
        "diagonal_a": str(diagonal_a),
        "diagonal_b": str(diagonal_b),
        "marked_mode": 0,
        "minor_rows": [list(value) for value in rows],
        "minor_residuals_over_A_B": [str(value) for value in residuals],
        "residual_gcd_degree": residual_gcd.total_degree(),
    }


def main():
    p, q, rho = sp.symbols("p q rho", nonzero=True)
    torus = source_torus_certificate()
    planes, alpha, beta = normalized_family(p, q, rho)
    tensor = coefficients(tuple(sp.Matrix(plane) for plane in planes))
    assert sp.factor(tensor[(1, 0, 0, 0)] + 4 * (p * q + 1)) == 0
    assert sp.factor(tensor[(1, 0, 0, 1)] + 4 * p * rho) == 0
    assert all(
        sp.factor(value) == 0
        for word, value in tensor.items()
        if word not in ((1, 0, 0, 0), (1, 0, 0, 1))
    )
    pure_tensor = coefficients(
        tuple(sp.Matrix((alpha[mode], beta[mode])) for mode in range(4))
    )
    assert sp.factor(pure_tensor[(1, 1, 1, 1)] + 4 * (p * q + 1)) == 0
    assert all(
        sp.factor(value) == 0
        for word, value in pure_tensor.items()
        if word != (1, 1, 1, 1)
    )
    projections = tuple(
        projection_ideal(distinguished, alpha, beta)
        for distinguished in range(4)
    )
    pencils = tuple(
        pencil_certificate(distinguished, p, q, rho, alpha, beta)
        for distinguished in range(4)
    )
    print(
        json.dumps(
            {
                "status": "verified",
                "field": "C(p,q,rho)",
                "source_torus_quotient_dimension": 3,
                "source_torus_certificate": torus,
                "projected_marking_sheets": 4,
                "projections": projections,
                "pencil_certificates": pencils,
                "generic_H31_fibre_component_15": "empty",
                "global_conjecture": "unresolved",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
