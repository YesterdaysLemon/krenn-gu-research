#!/usr/bin/env python3
"""No-import audit of weighted H22 on component 23's antidiagonal."""

from __future__ import annotations

import itertools
import json
import shutil
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))

h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
r, lam, u, v, s = sp.symbols("r lam u v s")

A = (sp.Integer(1), 1, 0, 0)
C = (sp.Integer(1), -1, 0, 0)
B = (0, 0, sp.Integer(1), 1)
D = (0, 0, sp.Integer(1), -1)


def add(left, right, coefficient=1):
    return tuple(
        sp.expand(left[index] + coefficient * right[index]) for index in range(4)
    )


def rows():
    return (A, D, add(B, D, r), add(B, D, -r)), (B, B, C, C)


def shifted_beta(alpha, beta):
    return tuple(add(beta[index], alpha[index], h[index]) for index in range(4))


def permanent3(rows0):
    return sp.expand(
        sum(
            sp.prod(rows0[index][permutation[index]] for index in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def permanent4(rows0):
    return sp.expand(
        sum(
            sp.prod(rows0[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def symmetric_product(left, right):
    return sp.Matrix(
        [
            left[first] * right[second] + left[second] * right[first]
            for first, second in PAIRS
        ]
    )


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def project(row, extension, direction, chart, slope=None):
    if chart == "finite" and direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if chart == "finite" and direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity" and direction == "D01":
        return (row[0], row[2], row[3], extension)
    if chart == "infinity" and direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def h22_model(alpha, beta, direction, chart, slope=None):
    alpha4 = tuple(
        project(alpha[index], x[index], direction, chart, slope) for index in range(4)
    )
    beta4 = tuple(
        project(beta[index], x[4 + index], direction, chart, slope)
        for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta4[index] if word[index] else alpha4[index] for index in range(4)
        )
        coefficients[word] = sp.expand(
            sum(
                selected[index][3]
                * permanent3(
                    tuple(selected[other][:3] for other in range(4) if other != index)
                )
                for index in range(4)
            )
        )
    return {
        "mixed": tuple(coefficients[word] for word in MIXED_WORDS),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular_text(expression):
    return str(sp.expand(expression)).replace("**", "^")


def run_singular(label, program, expected="RESULT:1:1", timeout=900):
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        label,
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert markers == [expected], (label, completed.stdout, expected)
    return label


def geometry_audit():
    alpha, beta = rows()
    planes = tuple((alpha[index], beta[index]) for index in range(4))
    profile = tuple(
        pair_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
    )
    assert profile == (3, 3, 3, 3, 3, 4)
    edge23 = pair_matrix(planes[2], planes[3])
    minors = tuple(
        sp.factor(edge23.extract(row_set, range(4)).det())
        for row_set in itertools.combinations(range(6), 4)
    )
    nonzero = tuple(value for value in minors if value != 0)
    assert sp.factor(sp.gcd_list(nonzero)) == 16 * r * (r**2 + 1)
    root_planes = tuple(
        tuple(tuple(sp.sympify(entry).subs(r, sp.I) for entry in row) for row in plane)
        for plane in planes
    )
    assert tuple(
        pair_matrix(root_planes[left], root_planes[right]).rank()
        for left, right in PAIRS
    ) == (3, 3, 3, 3, 3, 3)
    coefficients = {
        word: sp.factor(
            permanent4(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[WORDS[-1]] == -4
    assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
    assert all(sp.Matrix(plane).rank() == 2 for plane in planes)
    return f"profile={profile};edge23_gcd=16*r*(r^2+1);pure=T1111=-4"


def opposite_chart_audit(chart, alpha_branch):
    alpha, beta = rows()
    marked = shifted_beta(alpha, beta)
    slope = lam if chart == "finite" else None
    models = tuple(
        h22_model(alpha, marked, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    a01, a23 = models[0]["A"], models[1]["A"]
    b01, b23 = models[0]["B"], models[1]["B"]
    selected_alpha = (a01, a23)[alpha_branch]
    equations = (
        *models[0]["mixed"],
        *models[1]["mixed"],
        b01 - 1,
        u * b23 - 1,
        v * selected_alpha - 1,
        s * r - 1,
    )
    variables = x + (u, v, s) + h + ((r, lam) if chart == "finite" else (r,))
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + ";",
            "I=slimgb(I); I=std(I);",
            "int unit=reduce(1,I)==0;",
            '"RESULT:"+string(unit)+":"+string(size(I));',
            "quit;",
        )
    )
    run_singular(f"audit_{chart}_alpha_{alpha_branch}", program)
    return {
        "chart": chart,
        "normalization": "B01=1",
        "B23_inverted": True,
        "alpha_inverted": "A01" if alpha_branch == 0 else "A23",
        "r_inverted": True,
        "standard_basis": "(1)",
    }


def main():
    geometry = geometry_audit()
    charts = tuple(
        opposite_chart_audit(chart, alpha_branch)
        for chart in ("finite", "infinity")
        for alpha_branch in (0, 1)
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q",
                "scope": "no-import antidiagonal weighted-H22 audit",
                "geometry": geometry,
                "opposite_normalization_charts": charts,
                "project_imports": False,
                "finite_field_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
