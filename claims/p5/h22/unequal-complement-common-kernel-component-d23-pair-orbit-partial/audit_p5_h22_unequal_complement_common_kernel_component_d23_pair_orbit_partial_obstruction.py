#!/usr/bin/env python3
"""Independent exact-Q spot audit for the component-22 D23 partial cover.

No construction/verifier module is imported.  The component rows, projection,
permanents, mixed equations, and one-marked maps are rebuilt locally.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import subprocess

import sympy as sp

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
PERMS4 = tuple(itertools.permutations(range(4)))
x = sp.symbols("x0:8")
w = sp.Symbol("w")


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows(A, R, D):
    u = (1 - D) / 2
    v = (1 + D) / 2
    G = -(2 * A + R) / 2
    a = (1, 1, 0, 0)
    c = (1, -1, 0, 0)
    m = (2 * A, 0, 1, 1)
    mr = add(m, c, R)
    d = (G, G, u, v)
    y0 = (0, D * (2 * A + R), -u, v)
    x0 = (-A * v, A * (u + 1) + R, 1, 0)
    return (y0, m, mr, c), (x0, a, a, d)


def permanent(rows):
    return sp.expand(sum(
        sp.prod(rows[row][permutation[row]] for row in range(4))
        for permutation in PERMS4
    ))


def projected_rows(A, R, D, shifts, rho):
    alpha, beta = component_rows(A, R, D)
    beta = tuple(add(beta[i], alpha[i], shifts[i]) for i in range(4))
    alpha_p = tuple((row[0], row[1], rho * row[2] + row[3], x[i]) for i, row in enumerate(alpha))
    beta_p = tuple((row[0], row[1], rho * row[2] + row[3], x[4+i]) for i, row in enumerate(beta))
    return alpha_p, beta_p


def coefficients(alpha, beta):
    return {
        bits: permanent(tuple(beta[i] if bits[i] else alpha[i] for i in range(4)))
        for bits in BITS4
    }


def one_marked_map(mode, alpha, beta):
    rows = []
    for bits in BITS3:
        selected = []
        cursor = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if bits[cursor] else alpha[other])
                cursor += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(int(index == coordinate) for index in range(4))
            coefficient_row.append(permanent(tuple(
                basis if other == mode else selected[other] for other in range(4)
            )))
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def sg(expression):
    return str(sp.fraction(sp.together(expression))[0]).replace("**", "^")


def matrix_declaration(name, matrix):
    return f"matrix {name}[4][4]=" + ",".join(
        sg(matrix[row, column]) for row in range(4) for column in range(4)
    ) + ";"


def unit_case(label, shifts, rho, minor_specs, free_markers=()):
    alpha, beta = projected_rows(sp.Integer(2), sp.Integer(1), sp.Integer(3), shifts, rho)
    values = coefficients(alpha, beta)
    equations = [values[bits] for bits in BITS4[1:-1]]
    equations.extend((values[BITS4[0]] - 1, w * values[BITS4[-1]] - 1))
    matrices = [
        one_marked_map(mode, alpha, beta).extract(rows, range(4))
        for mode, rows in minor_specs
    ]
    variables = [*x, *free_markers, w]
    program = "\n".join([
        "ring Q=0,(" + ",".join(map(str, variables)) + "),dp;",
        "option(redSB);",
        *[matrix_declaration(f"N{i}", matrix) for i, matrix in enumerate(matrices)],
        "ideal I=" + ",".join(map(sg, equations)) + ","
        + ",".join(f"det(N{i})" for i in range(len(matrices))) + ";",
        "I=slimgb(I); ideal J=std(I);",
        '"RESULT:"+string(size(J))+":"+string(reduce(1,J)==0);',
        "quit;",
    ])
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label, completed.stdout, completed.stderr
    )
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1"], (label, completed.stdout)
    return label


def main():
    h0, h2, h3 = sp.symbols("h0 h2 h3")
    results = [
        unit_case("Q1_at_A2_R1_D3", (-sp.Rational(1, 15), 0, 0, sp.Rational(5, 2)), sp.Rational(37, 11), ((0, (0, 1, 3, 7)),)),
        unit_case("Q2_at_A2_R1_D3", (-sp.Rational(1, 2), 0, -sp.Rational(1, 5), -sp.Rational(5, 2)), sp.Rational(1, 3), ((1, (0, 1, 2, 7)),)),
        unit_case("Q3_at_A2_R1_D3", (1, 1, 1, sp.Rational(5, 2)), -1, ((1, (0, 1, 4, 7)),)),
        unit_case(
            "h1_zero_rho_zero_factor_slice_at_A2_R1_D3",
            (h0, 0, h2, h3),
            0,
            ((0, (0, 1, 3, 7)), (1, (0, 1, 2, 7)), (1, (0, 1, 4, 7))),
            (h0, h2, h3),
        ),
    ]
    print(json.dumps({
        "status": "pass",
        "field": "Q",
        "specialization": {"A": 2, "R": 1, "D": 3},
        "independent_no_repository_imports": True,
        "exact_unit_cases": results,
        "finite_field_proof_used": False,
        "generic_weighted_H22_fibre_closed": False,
        "global_conjecture_resolved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
