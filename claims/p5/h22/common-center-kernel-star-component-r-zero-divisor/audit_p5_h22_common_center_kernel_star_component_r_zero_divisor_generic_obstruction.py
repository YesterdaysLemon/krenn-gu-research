#!/usr/bin/env python3
"""Independent exact-Q audit of component 23's r=0 divisor theorem."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
lam = sp.Symbol("lam")


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(3))
            for permutation in itertools.permutations(range(3))
        )
    )


def component_rows():
    # Independent specialization of k=(1-r*t)/(t-r) at (r,t)=(0,3).
    k = sp.Rational(1, 3)
    A = (1, 1, 0, 0)
    B = (0, 0, 1, 1)
    C = (1, -1, 0, 0)
    D = (0, 0, 1, -1)
    alpha = (
        A,
        add(A, D, k),
        add(add(A, C, -1), B),
        add(add(add(tuple(-entry for entry in A), C, -1), B), D, 3),
    )
    beta = (B, add(B, C), C, C)
    marked = tuple(add(beta[index], alpha[index], h[index]) for index in range(4))
    return alpha, beta, marked


def project(row, extension, direction, chart, slope=None):
    if (direction, chart) == ("D01", "finite"):
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if (direction, chart) == ("D23", "finite"):
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if (direction, chart) == ("D01", "infinity"):
        return (row[0], row[2], row[3], extension)
    if (direction, chart) == ("D23", "infinity"):
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def build_model(direction, chart, slope=None):
    alpha, _, marked = component_rows()
    alpha_rows = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta_rows = tuple(
        project(marked[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != index))
                for index in range(4)
            )
        )
    return {
        "mixed": tuple(coefficients[word] for word in MIXED),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def combined_matrix(slope):
    models = (
        build_model("D01", "finite", slope),
        build_model("D23", "finite", slope),
    )
    return sp.Matrix(
        [
            [sp.diff(equation, variable) for variable in x]
            for model in models
            for equation in model["mixed"]
        ]
    )


def exact_minor(matrix, rows, substitutions, expected):
    actual = sp.factor(
        matrix.subs(substitutions, simultaneous=True)
        .extract(rows, range(8))
        .det(method="domain-ge")
    )
    assert sp.cancel(actual - expected) == 0, (rows, actual, expected)


def ordinary_minor_audit():
    matrix = combined_matrix(lam)
    exact_minor(
        matrix,
        (0, 1, 3, 7, 8, 9, 11, 12),
        {},
        -2048 * h[3] * lam * (lam - 1) ** 2 * (lam + 1) ** 3 * (h[0] * (lam + 1) - 2),
    )
    exact_minor(
        matrix,
        (0, 1, 3, 4, 7, 8, 9, 11),
        {h[0]: 2 / (lam + 1)},
        -2048 * h[3] * lam * (lam - 1) ** 2 * (lam + 1) ** 4,
    )
    exact_minor(
        matrix,
        (1, 3, 4, 5, 7, 8, 9, 11),
        {h[3]: 0},
        -2048 * h[2] * lam * (h[1] - 1) * (lam - 1) ** 2 * (lam + 1) ** 4,
    )
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 12),
        {h[2]: 0, h[3]: 0},
        2048 * lam * (lam - 1) ** 3 * (lam + 1) ** 3 * (h[0] - h[1] - 1),
    )
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 13),
        {h[0]: h[1] + 1, h[2]: 0, h[3]: 0},
        -2048 * lam * (h[1] - 1) * (lam - 1) ** 3 * (lam + 1) ** 3,
    )
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 14),
        {h[0]: 2, h[1]: 1, h[2]: 0, h[3]: 0},
        sp.Rational(1024, 3)
        * lam
        * (lam - 1) ** 3
        * (lam + 1) ** 3
        * (3 * (lam + 1) - 2),
    )
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 16),
        {h[0]: 2, h[1]: 1, h[2]: 0, h[3]: 0, lam: sp.Rational(-1, 3)},
        sp.Rational(1048576, 19683),
    )

    G = 2 * h[0] * h[2] * lam - h[0] * lam + h[0] - 2 * h[2] * lam + 2 * lam - 2
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 12),
        {h[1]: 1, h[3]: 0},
        -2048 * lam * (lam - 1) ** 2 * (lam + 1) ** 3 * G,
    )
    h2_solution = (lam - 1) * (h[0] - 2) / (2 * lam * (h[0] - 1))
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 14),
        {h[1]: 1, h[2]: h2_solution, h[3]: 0},
        sp.Rational(512, 3)
        * (lam - 1) ** 3
        * (lam + 1) ** 3
        * (h[0] * (lam + 1) - 2)
        * (3 * (lam + 1) - 2),
    )
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 17),
        {h[0]: 2 / (lam + 1), h[1]: 1, h[2]: 1, h[3]: 0},
        -sp.Rational(16384, 3) * lam * (lam - 1) ** 3 * (lam + 1) ** 3,
    )
    terminal_weight = sp.Rational(-1, 3)
    terminal_h2 = sp.cancel(h2_solution.subs(lam, terminal_weight))
    L = -h[0] + 6
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 17),
        {h[1]: 1, h[2]: terminal_h2, h[3]: 0, lam: terminal_weight},
        -sp.Rational(8388608, 19683) * L,
    )
    exact_minor(
        matrix,
        (1, 3, 4, 7, 8, 9, 11, 16),
        {h[0]: 6, h[1]: 1, h[2]: sp.Rational(8, 5), h[3]: 0, lam: terminal_weight},
        -sp.Rational(1048576, 6561),
    )
    return 12


def coefficient_row(expression):
    return (
        "["
        + ",".join(
            str(sp.cancel(sp.diff(expression, variable))).replace("**", "^")
            for variable in x
        )
        + "]"
    )


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def module_audit(
    label,
    chart,
    slope,
    substitutions,
    variables,
    expected_indices,
    expected_membership,
):
    models = (
        build_model("D01", chart, slope),
        build_model("D23", chart, slope),
    )
    generators = ",".join(
        coefficient_row(equation.subs(substitutions, simultaneous=True))
        for model in models
        for equation in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(equation.subs(substitutions, simultaneous=True))
        for model in models
        for equation in (model["A"], model["B"])
    )
    expected = ",".join(f"gen({index})" for index in expected_indices)
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2);",
            "module EM=simplify(reduce(E,M),2);",
            "vector A01=" + diagonals[0] + ";",
            "vector B01=" + diagonals[1] + ";",
            "vector A23=" + diagonals[2] + ";",
            "vector B23=" + diagonals[3] + ";",
            (
                '"RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"'
                '+string(reduce(A01,M)==0)+":"+string(reduce(A23,M)==0)+":"'
                '+string(reduce(B01,M)==0)+":"+string(reduce(B23,M)==0)+":"'
                "+string(size(M));"
            ),
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
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    expected_marker = (
        "RESULT:1:"
        + ":".join("1" if value else "0" for value in expected_membership)
        + f":{len(expected_indices)}"
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [expected_marker], (label, completed.stdout)
    return label


def main():
    alpha, beta, _ = component_rows()
    coordinate_pairs = tuple(itertools.combinations(range(4), 2))

    def symmetric_product(left, right):
        return sp.Matrix(
            [left[i] * right[j] + left[j] * right[i] for i, j in coordinate_pairs]
        )

    planes = tuple((alpha[index], beta[index]) for index in range(4))
    pair_profile = []
    for left, right in itertools.combinations(range(4), 2):
        matrix = sp.Matrix.hstack(
            *(
                symmetric_product(planes[left][i], planes[right][j])
                for i in range(2)
                for j in range(2)
            )
        )
        pair_profile.append(matrix.rank())
    assert tuple(pair_profile) == (3, 3, 3, 4, 4, 4)

    minor_count = ordinary_minor_audit()
    lambda_zero_matrix = combined_matrix(0)
    exact_minor(
        lambda_zero_matrix,
        (0, 1, 3, 4, 7, 8, 9, 14),
        {},
        -sp.Rational(256, 3) * h[3] * (20 * h[3] - 1),
    )
    H0_solution = sp.Rational(1, 20)
    endpoint_certificates = (
        "lambda_zero_dense_minor",
        module_audit(
            "lambda_zero_h2_zero",
            "finite",
            0,
            {h[2]: 0},
            (h[0], h[1], h[3]),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_audit(
            "lambda_zero_h3_zero",
            "finite",
            0,
            {h[3]: 0},
            (h[0], h[1], h[2]),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_audit(
            "lambda_zero_H_zero",
            "finite",
            0,
            {h[3]: H0_solution},
            (h[0], h[1], h[2]),
            tuple(range(1, 9)),
            (True,) * 4,
        ),
        module_audit(
            "lambda_one",
            "finite",
            1,
            {},
            h,
            (1, 2, 3, 4, 6, 7, 8),
            (True, True, True, False),
        ),
        module_audit(
            "lambda_minus_one", "finite", -1, {}, h, tuple(range(1, 9)), (True,) * 4
        ),
        module_audit(
            "projective_weight",
            "infinity",
            None,
            {},
            h,
            tuple(range(1, 9)),
            (True,) * 4,
        ),
    )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"r": 0, "t": 3, "k": "1/3"},
                "independent_no_repository_imports": True,
                "pure_pair_profile": pair_profile,
                "all_pair_open_checked": True,
                "ordinary_minor_tree_nodes_checked": minor_count,
                "endpoint_and_projective_certificates": endpoint_certificates,
                "audit_only_not_divisor_generic_proof": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
