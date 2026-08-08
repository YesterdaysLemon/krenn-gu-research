#!/usr/bin/env python3
"""Verify the generic weighted H22 obstruction on P4 component fifteen."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

from verify_p5_h31_disjoint_secant_component_generic_obstruction import (
    normalized_family,
    shifted_beta,
    singular,
)
from verify_p5_h31_marked_basis_open_branch import mixed_matrix as h31_mixed_matrix
from verify_p5_h31_marked_basis_open_branch import marked_extension
from verify_p5_h22_full_support_tangent_component_generic_obstruction import (
    marked_matrix,
    permanent3,
    weighted_row,
)


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = tuple(
    word for word in WORDS if word not in ((0, 0, 0, 0), (1, 1, 1, 1))
)
PIVOT_ROWS = (0, 1, 2, 3, 7, 11)
PIVOT_COLUMNS = (0, 1, 2, 3, 4, 5)
MINOR_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7), (0, 1, 5, 7))


def build_model(direction, p, q, rho, slope, shifts):
    _, alpha, canonical_beta = normalized_family(p, q, rho)
    beta = shifted_beta(alpha, canonical_beta, shifts)
    extensions = sp.symbols("z0:8")
    alpha_d = tuple(
        weighted_row(alpha[mode], extensions[mode], direction, slope)
        for mode in range(4)
    )
    beta_d = tuple(
        weighted_row(beta[mode], extensions[4 + mode], direction, slope)
        for mode in range(4)
    )

    def coefficient(word):
        selected = tuple(
            beta_d[mode] if word[mode] else alpha_d[mode]
            for mode in range(4)
        )
        return sp.expand(
            sum(
                selected[mode][3]
                * permanent3(
                    tuple(
                        selected[other]
                        for other in range(4)
                        if other != mode
                    )
                )
                for mode in range(4)
            )
        )

    coefficients = {word: coefficient(word) for word in WORDS}
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], extension) for extension in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "alpha": alpha,
        "beta": beta,
        "extensions": extensions,
        "alpha_d": alpha_d,
        "beta_d": beta_d,
        "mixed_matrix": mixed,
        "diagonal_a": coefficients[(0, 0, 0, 0)],
        "diagonal_b": coefficients[(1, 1, 1, 1)],
    }


def finite_total_projection():
    p, q, rho, u = sp.symbols("p q rho u")
    shifts = sp.symbols("h0:4")
    model = build_model("01", p, q, rho, u, shifts)
    extensions = model["extensions"]
    inverse = sp.Symbol("w")
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(model["mixed_matrix"] * extension),
        model["diagonal_a"] - 1,
        inverse * model["diagonal_b"] - 1,
    )
    eliminated = extensions + (inverse,)
    target = (u,) + shifts
    variables = eliminated + target
    expected = (shifts[3], rho * shifts[2] - p * q - 1, shifts[1], shifts[0])
    lines = [
        "ring R=(0,p,q,rho),("
        + ",".join(map(str, variables))
        + "),(dp(9),dp(5));",
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
        timeout=100,
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
        "direction": "01",
        "slope_mode": "finite_total",
        "basis_size": int(fields[2]),
        "ideal": [str(value) for value in expected],
    }


def exceptional_slope_obstruction(slope):
    p, q, rho = sp.symbols("p q rho")
    shifts = sp.symbols("h0:4")
    model = build_model("01", p, q, rho, sp.Integer(slope), shifts)
    extensions = model["extensions"]
    inverse_a, inverse_b = sp.symbols("wa wb")
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(model["mixed_matrix"] * extension),
        inverse_a * model["diagonal_a"] - 1,
        inverse_b * model["diagonal_b"] - 1,
    )
    variables = extensions + (inverse_a, inverse_b) + shifts
    lines = [
        "ring R=(0,p,q,rho),(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "int empty=(reduce(1,I)==0);",
        '"CODEX_RESULT:"+string(empty);',
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
    assert "CODEX_RESULT:1" in completed.stdout, completed.stdout
    return {"slope": slope, "genuine_binary_incidence": "empty"}


def finite_pencil_certificate():
    p, q, rho, u, x, y = sp.symbols("p q rho u x y")
    point = (0, 0, (p * q + 1) / rho, 0)
    model = build_model("01", p, q, rho, u, point)
    first = sp.Matrix((0, 0, 0, -rho, 0, 0, 1, 0))
    second = sp.Matrix(
        (-(u + 1), 0, -(u + 1), 0, 0, u - 1, 0, q * (u - 1))
    )
    assert all(
        sp.cancel(value) == 0
        for value in model["mixed_matrix"] * first
    )
    assert all(
        sp.cancel(value) == 0
        for value in model["mixed_matrix"] * second
    )
    pivot = model["mixed_matrix"].extract(PIVOT_ROWS, PIVOT_COLUMNS)
    pivot_determinant = sp.factor(pivot.det())
    expected_pivot = (
        64
        * p**2
        * q
        * rho
        * (u - 1) ** 3
        * (u + 1) ** 3
        * (p * q + 1) ** 2
    )
    assert sp.factor(pivot_determinant - expected_pivot) == 0

    extension = x * first + y * second
    substitution = dict(zip(model["extensions"], extension, strict=True))
    diagonal_a = sp.factor(model["diagonal_a"].subs(substitution))
    diagonal_b = sp.factor(model["diagonal_b"].subs(substitution))
    factor_f = (p * q + rho + 1) * u + p * q - rho + 1
    expected_a = 2 * (u + 1) * (
        rho * x
        + ((p * q + 1) * (u + 1) + rho * (1 - u)) * y
    )
    expected_b = 2 * (u - 1) / rho * (
        rho * x
        + (
            2 * p * q * rho * (u - 1)
            + (p * q + 1) * (u + 1)
            + rho * (u - 1)
        )
        * y
    )
    assert sp.factor(diagonal_a - expected_a) == 0
    assert sp.factor(diagonal_b - expected_b) == 0

    marked = marked_matrix(model, 0).subs(substitution)
    determinants = tuple(
        sp.factor(marked[list(rows), :].det()) for rows in MINOR_ROWS
    )
    residuals = tuple(
        sp.factor(determinant / (diagonal_a * diagonal_b))
        for determinant in determinants
    )
    expected_residuals = (
        -4 * q * x * (u - 1) * factor_f / (u + 1),
        2
        * q**2
        * (u - 1) ** 2
        * (rho * x + factor_f * y)
        / (rho * (u + 1)),
        4 * q**2 * y * (u - 1) ** 3 / (u + 1),
    )
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(residuals, expected_residuals, strict=True)
    )
    assert sp.factor(factor_f.subs(u, 1) - 2 * (p * q + 1)) == 0
    assert sp.factor(factor_f.subs(u, -1) + 2 * rho) == 0
    return {
        "direction": "01",
        "slope_range": "finite u with u^2 != 1",
        "marking_point": [str(value) for value in point],
        "kernel_basis": [
            [str(value) for value in first],
            [str(value) for value in second],
        ],
        "pivot_rows": list(PIVOT_ROWS),
        "pivot_columns": list(PIVOT_COLUMNS),
        "pivot_determinant": str(pivot_determinant),
        "diagonal_a": str(diagonal_a),
        "diagonal_b": str(diagonal_b),
        "factor_F": str(factor_f),
        "marked_mode": 0,
        "minor_rows": [list(rows) for rows in MINOR_ROWS],
        "minor_residuals_over_A_B": [str(value) for value in residuals],
        "projective_cover": "F!=0: x,y; F=0: rho*x,y",
    }


def infinity_h31_identity():
    p, q, rho = sp.symbols("p q rho")
    point = (0, 0, (p * q + 1) / rho, 0)
    h22 = build_model("01_inf", p, q, rho, sp.Integer(0), point)
    _, alpha, canonical_beta = normalized_family(p, q, rho)
    beta = shifted_beta(alpha, canonical_beta, point)
    h31_mixed, h31_a, h31_b = h31_mixed_matrix(1, alpha, beta)
    assert all(
        sp.cancel(value) == 0 for value in h22["mixed_matrix"] - h31_mixed
    )
    extension = sp.Matrix(h22["extensions"])
    assert sp.cancel(h22["diagonal_a"] - (h31_a * extension)[0]) == 0
    assert sp.cancel(h22["diagonal_b"] - (h31_b * extension)[0]) == 0
    h31_marked = marked_extension(1, extension, alpha, beta, 0)
    assert all(
        sp.cancel(value) == 0 for value in marked_matrix(h22, 0) - h31_marked
    )
    return {
        "slope": "infinity",
        "identified_H31_deleted_coordinate": 1,
        "identified_H31_marking_point": [str(value) for value in point],
    }


def main():
    projection = finite_total_projection()
    exceptional = tuple(
        exceptional_slope_obstruction(slope) for slope in (-1, 1)
    )
    finite = finite_pencil_certificate()
    infinity = infinity_h31_identity()
    print(
        json.dumps(
            {
                "status": "verified",
                "field": "C(p,q,rho)",
                "proof_method": "projective weighted Fitting projection and three-minor cover",
                "finite_projection": projection,
                "finite_pencil_certificate": finite,
                "exceptional_slopes": exceptional,
                "infinity_certificate": infinity,
                "generic_H22_fibre_component_15": "empty",
                "all_known_components_generic_H31_H22": "empty",
                "global_conjecture": "unresolved",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
