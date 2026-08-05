#!/usr/bin/env python3
"""Independent exact-Q audit for the component-23 finite dense-open supplement."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMS3 = tuple(itertools.permutations(range(3)))
x = sp.symbols("x0:8")
h = sp.symbols("h0:4")
lam = sp.Symbol("lam")


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows(r, t):
    k = sp.Rational(1 - r * t, t - r)
    A, C = (1, 1, 0, 0), (1, -1, 0, 0)
    B, D = (0, 0, 1, 1), (0, 0, 1, -1)
    alpha = (
        A,
        add(A, D, k),
        add(add(add(A, C, -1), B), D, r),
        add(add(add(tuple(-entry for entry in A), C, -1), B), D, t),
    )
    beta = (B, add(B, C), C, C)
    beta = tuple(add(beta[i], alpha[i], h[i]) for i in range(4))
    return alpha, beta


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(3))
            for permutation in PERMS3
        )
    )


def project(row, extension, direction, slope):
    if direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    return (row[0], row[1], slope * row[2] + row[3], extension)


def model(alpha, beta, direction, slope):
    ap = tuple(project(alpha[i], x[i], direction, slope) for i in range(4))
    bp = tuple(project(beta[i], x[4 + i], direction, slope) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(bp[i] if word[i] else ap[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    return coefficients


def row_matrix(alpha, beta, slope):
    equations = []
    for direction in ("D01", "D23"):
        values = model(alpha, beta, direction, slope)
        equations.extend(values[word] for word in MIXED)
    return sp.Matrix(
        [[sp.diff(equation, variable) for variable in x] for equation in equations]
    )


def sg(expression):
    return str(sp.expand(expression)).replace("**", "^")


def lambda_minus_one_module(matrix):
    generators = ",".join(
        "[" + ",".join(sg(matrix[row, column]) for column in range(8)) + "]"
        for row in range(28)
    )
    program = "\n".join(
        (
            "ring Q=0,(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E="
            + ",".join(f"gen({index})" for index in range(1, 9))
            + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            '"RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        ("wsl.exe", "--exec", "/usr/bin/Singular", "-q"),
        input=program,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == ["RESULT:1:8"], completed.stdout
    return "lambda_minus_one_full_module_at_r2_t4"


def main():
    alpha, beta = component_rows(2, 4)
    matrix = row_matrix(alpha, beta, lam)
    first = matrix.extract((0, 1, 3, 7, 8, 9, 11, 12), range(8)).det(method="domain-ge")
    second = matrix.extract((0, 1, 2, 3, 7, 8, 9, 14), range(8)).det(method="domain-ge")

    r, t = sp.Integer(2), sp.Integer(4)
    F = (
        (-2 * r**4 * t**2 + 2 * r**3 * t + 2 * r**2 * t**2 - 2 * r * t)
        * h[0]
        * h[2]
        * lam
        + (-(r**4) * t**2 + r**3 * t**3 + r**3 * t - r * t**3 - r * t + t**2)
        * h[0]
        * h[3]
        * lam
        + (
            r**4 * t**2
            + r**3 * t**3
            - r**3 * t
            - 2 * r**2 * t**2
            - r * t**3
            + r * t
            + t**2
        )
        * h[0]
        * h[3]
        + (r**4 * t**2 - r**3 * t - r**2 * t**2 + r * t) * h[0] * lam
        + (-(r**3) * t + r**2 * t**2 + r**2 - r * t) * h[1] * lam
        + (2 * r**4 - 2 * r**3 * t - 2 * r**2 + 2 * r * t) * h[2] * lam
        + (-(r**4) * t**2 + r**3 * t + r**2 * t**2 - r * t) * h[0]
        + (r**3 * t - r**2 * t**2 - r**2 + r * t) * h[1]
        + (-2 * r**3 * t + 2 * r**2 * t**2 + 2 * r * t - 2 * t**2) * h[3]
        + (-(r**3) * t + r**2 * t**2 + r**2 - r * t) * lam
        + (r**3 * t - r**2 * t**2 - r**2 + r * t)
    )
    H = (
        (2 * r**2 - 2 * r * t - 2 * r + 4 * t**2 + 2 * t - 4) * h[3] * lam
        + (4 * r**2 - 2 * r * t - 2 * r + 2 * t**2 + 2 * t - 4) * h[3]
        + (r**2 - r * t + r - t) * lam
        + (-(r**2) - r * t + r - t + 2)
    )
    expected_first = lam * (lam - 1) ** 2 * (lam + 1) ** 3 * F
    expected_second = h[2] * h[3] * H * (lam - 1) ** 3 * (lam + 1) ** 4
    quotient_first = sp.cancel(first / expected_first)
    quotient_second = sp.cancel(second / expected_second)
    assert not quotient_first.free_symbols and quotient_first != 0
    assert not quotient_second.free_symbols and quotient_second != 0

    minus_one = lambda_minus_one_module(row_matrix(alpha, beta, sp.Integer(-1)))
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"r": 2, "t": 4},
                "independent_no_repository_imports": True,
                "first_minor_associate": True,
                "second_minor_associate": True,
                "exact_module_case": minus_one,
                "audit_only_not_generic_proof": True,
                "finite_field_proof_used": False,
                "generic_finite_all_markings_closed": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
