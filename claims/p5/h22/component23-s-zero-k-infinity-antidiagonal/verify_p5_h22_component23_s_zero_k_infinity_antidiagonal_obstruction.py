#!/usr/bin/env python3
"""Close weighted H22 on component 23's punctured finite antidiagonal."""

from __future__ import annotations

import itertools
import json
import subprocess

import sympy as sp

from derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate import (
    build_model,
)
from verify_p5_h22_common_center_kernel_star_component_partial import singular_command
from verify_p5_h31_marked_basis_open_branch import permanent

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
r, lam, u, w = sp.symbols("r lam u w")

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


def geometry_certificate():
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
    assert set(nonzero) == {16 * r * (r**2 + 1), -16 * r * (r**2 + 1)}
    gcd = sp.factor(sp.gcd_list(nonzero))
    assert gcd == 16 * r * (r**2 + 1)
    root_planes = tuple(
        tuple(tuple(sp.sympify(entry).subs(r, sp.I) for entry in row) for row in plane)
        for plane in planes
    )
    root_profile = tuple(
        pair_matrix(root_planes[left], root_planes[right]).rank()
        for left, right in PAIRS
    )
    assert root_profile == (3, 3, 3, 3, 3, 3)
    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    beta[index] if word[index] else alpha[index] for index in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[WORDS[-1]] == -4
    assert all(value == 0 for word, value in coefficients.items() if word != WORDS[-1])
    projective_markings = tuple(
        coefficients[tuple(0 if index == mode else 1 for index in range(4))]
        for mode in range(4)
    )
    assert projective_markings == (0, 0, 0, 0)
    assert all(sp.Matrix(plane).rank() == 2 for plane in planes)
    return {
        "generic_profile": profile,
        "r_squared_minus_one_profile": root_profile,
        "edge23_four_minor_gcd": str(gcd),
        "pure": "T1111=-4",
    }


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


def chart_certificate(chart, alpha_branch):
    alpha, beta = rows()
    marked = shifted_beta(alpha, beta)
    slope = lam if chart == "finite" else None
    d01 = build_model(alpha, marked, x, "D01", chart, slope)
    d23 = build_model(alpha, marked, x, "D23", chart, slope)
    diagonals = (d01["A"], d23["A"], d01["B"], d23["B"])
    equations = (
        *d01["mixed"],
        *d23["mixed"],
        diagonals[alpha_branch] - 1,
        w * diagonals[2] * diagonals[3] - 1,
        u * r - 1,
    )
    variables = x + (w, u) + h + ((r, lam) if chart == "finite" else (r,))
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
    run_singular(f"{chart}_alpha_{alpha_branch}", program)
    return {
        "chart": chart,
        "alpha_normalization": "A01=1" if alpha_branch == 0 else "A23=1",
        "beta_product_inverted": True,
        "r_inverted": True,
        "standard_basis": "(1)",
    }


def main():
    geometry = geometry_certificate()
    charts = tuple(
        chart_certificate(chart, alpha_branch)
        for chart in ("finite", "infinity")
        for alpha_branch in (0, 1)
    )
    print(
        json.dumps(
            {
                "status": "VERIFIED",
                "field": "Q",
                "scope": "component 23 normalized s=0,k=infinity, t=-r, r!=0",
                "geometry": geometry,
                "charts": charts,
                "finite_field_used": False,
                "limitations": "fixed normalized order only; arbitrary bases, arbitrary order, gluing, and global conjecture not claimed",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
