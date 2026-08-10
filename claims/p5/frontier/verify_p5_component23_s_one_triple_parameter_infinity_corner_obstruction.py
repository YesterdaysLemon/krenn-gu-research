#!/usr/bin/env python3
"""Close component 23's s=1 simultaneous k,r,t infinity corner."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys
from pathlib import Path

for _repo_parent in Path(__file__).resolve().parents:
    if (_repo_parent / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_repo_parent / "src"))
        break
else:
    raise RuntimeError("could not locate repository src directory")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402
from krenn_gu.p5_weighted_h22_contraction import build_model
REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h22/common-center-kernel-star")

from verify_p5_h22_common_center_kernel_star_component_partial import (
    coefficient_row,
    singular_command,
)
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
    permanent,
)



ROOT = Path(__file__).resolve().parent
NOTE = ROOT / "P5_COMPONENT23_S_ONE_TRIPLE_PARAMETER_INFINITY_CORNER_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))

q, u, v = sp.symbols("q u v")
h = sp.symbols("h0:4")
x = sp.symbols("x0:8")
w = sp.Symbol("w")
axis = sp.Symbol("z")
lam = sp.Symbol("lam")

A = (1, 1, 0, 0)
C = (1, -1, 0, 0)
B = (0, 0, 1, 1)
D = (0, 0, 1, -1)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def shifted(alpha, beta, marking=h):
    return tuple(
        add(beta[index], scale(marking[index], alpha[index])) for index in range(4)
    )


def compactified_rows():
    return (
        (
            A,
            add(scale(q, A), D),
            add(scale(u, add(A, scale(-1, C), B)), D),
            add(scale(v, add(scale(-1, A), scale(-1, C), B)), D),
        ),
        (B, add(B, C), C, C),
    )


def corner_rows():
    return (A, D, D, D), (B, add(B, C), C, C)


def symmetric_product(left, right):
    return sp.Matrix([left[i] * right[j] + left[j] * right[i] for i, j in PAIRS])


def pair_matrix(left, right):
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def compactification_and_geometry():
    original = 1 - 1 / (u * v) - (1 / q) * (1 / v - 1 / u)
    closure = sp.factor(q * u * v * original)
    assert closure == q * u * v - q - u + v
    gradient = tuple(
        sp.diff(closure, variable).subs({q: 0, u: 0, v: 0}) for variable in (q, u, v)
    )
    assert gradient == (-1, -1, 1)

    family_alpha, family_beta = compactified_rows()
    alpha, beta = corner_rows()
    assert (
        tuple(
            tuple(sp.sympify(entry).subs({q: 0, u: 0, v: 0}) for entry in row)
            for row in family_alpha
        )
        == alpha
    )
    assert family_beta == beta
    assert all(sp.Matrix((alpha[index], beta[index])).rank() == 2 for index in range(4))

    coefficients = {
        word: sp.factor(
            permanent(
                tuple(
                    alpha[index] if bit == 0 else beta[index]
                    for index, bit in enumerate(word)
                )
            )
        )
        for word in WORDS
    }
    assert coefficients[(1, 1, 1, 1)] == -4
    assert all(
        value == 0 for word, value in coefficients.items() if word != (1, 1, 1, 1)
    )

    planes = tuple((alpha[index], beta[index]) for index in range(4))
    matrices = tuple(pair_matrix(planes[left], planes[right]) for left, right in PAIRS)
    profile = tuple(matrix.rank() for matrix in matrices)
    assert profile == (3, 2, 2, 3, 3, 3)
    assert matrices[1].nullspace() == [sp.Matrix((0, 1, 0, 0)), sp.Matrix((0, 0, 1, 0))]
    assert matrices[2].nullspace() == [sp.Matrix((0, 1, 0, 0)), sp.Matrix((0, 0, 1, 0))]
    return {
        "reciprocal_equation": str(closure),
        "gradient_at_corner": tuple(map(int, gradient)),
        "smooth_unique_corner": True,
        "pair_profile": profile,
        "rank_two_edges": ("02", "03"),
        "pure_coefficient": "T1111=-4",
    }


def singular_text(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def run_singular(label, program, expected, timeout=300):
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


def h31_projection(deletion):
    alpha, beta = corner_rows()
    marked = shifted(alpha, beta)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    extension = sp.Matrix(x)
    equations = (
        *tuple(mixed * extension),
        (diagonal_a * extension)[0] - 1,
        w * (diagonal_b * extension)[0] - 1,
    )
    eliminated = x + (w,)
    variables = eliminated + h
    expected = (
        (h[0], h[2] * h[3], h[1] * h[3], h[1] * h[2])
        if deletion in (0, 1)
        else (sp.Integer(1),)
    )
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_text, equations)) + "; I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(map(singular_text, expected)) + "; E=std(E);",
            "ideal JE=simplify(reduce(J,E),2); ideal EJ=simplify(reduce(E,J),2);",
            'print("RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J)));',
            "quit;",
        )
    )
    run_singular(f"deletion {deletion}", program, f"RESULT:1:{len(expected)}")
    return {"deletion": deletion, "projected_ideal": tuple(map(str, expected))}


def global_one_marked(deletion, extension, alpha, marked):
    pure = one_marked_map(0, alpha, marked).row_join(sp.zeros(8, 1))
    neighbour = marked_extension(deletion, extension, alpha, marked, 0)
    embedded = sp.zeros(8, 5)
    for column, coordinate in enumerate(
        index for index in range(4) if index != deletion
    ):
        embedded[:, coordinate] = neighbour[:, column]
    embedded[:, 4] = neighbour[:, 3]
    return pure.col_join(embedded)


def branch_certificate(deletion, name, marking, localized_nonzero=()):
    alpha, beta = corner_rows()
    marked = shifted(alpha, beta, marking)
    mixed, diagonal_a, diagonal_b = mixed_matrix(deletion, alpha, marked)
    assert mixed.rank() == 6
    frame = mixed.nullspace()
    assert len(frame) == 2 and sp.Matrix.hstack(*frame).rank() == 2
    c0, c1 = sp.symbols("c0 c1")
    extension = frame[0] * c0 + frame[1] * c1
    actual_a = sp.factor((diagonal_a * extension)[0])
    actual_b = sp.factor((diagonal_b * extension)[0])
    rows = (1, 3, 7, 8, 9)
    determinant = sp.factor(
        global_one_marked(deletion, extension, alpha, marked)
        .extract(rows, range(5))
        .det(method="domain-ge")
    )
    sign = -1 if deletion == 0 else 1
    assert sp.factor(determinant - sign * 32 * actual_a) == 0
    return {
        "deletion": deletion,
        "branch": name,
        "marking": tuple(map(str, marking)),
        "localized_nonzero": tuple(map(str, localized_nonzero)),
        "mixed_rank": 6,
        "kernel_frame": tuple(tuple(map(str, vector)) for vector in frame),
        "diagonals": (str(actual_a), str(actual_b)),
        "stacked_mode": 0,
        "stacked_rows": rows,
        "stacked_determinant": str(determinant),
        "determinant_over_A": str(sign * 32),
    }


def h31_branches():
    output = []
    markings = (
        ("origin", (0, 0, 0, 0), ()),
        ("h1_axis", (0, axis, 0, 0), (axis,)),
        ("h2_axis", (0, 0, axis, 0), (axis,)),
        ("h3_axis", (0, 0, 0, axis), (axis,)),
    )
    for deletion in (0, 1):
        output.extend(
            branch_certificate(deletion, name, marking, nonzero)
            for name, marking, nonzero in markings
        )
    return tuple(output)


FINITE_MODULE = (
    "gen(1)",
    "gen(3)",
    "gen(4)",
    "(lam+1)*gen(2)",
    "(lam-1)*gen(5)",
    "(lam+1)*gen(6)",
    "(lam+1)*gen(7)",
    "(lam+1)*gen(8)",
)


def h22_module(chart):
    alpha, beta = corner_rows()
    marked = shifted(alpha, beta)
    slope = lam if chart == "finite" else None
    models = tuple(
        build_model(alpha, marked, x, direction, chart, slope)
        for direction in ("D01", "D23")
    )
    generators = ",".join(
        coefficient_row(expression, x)
        for model in models
        for expression in model["mixed"]
    )
    diagonals = tuple(
        coefficient_row(model[key], x) for model in models for key in ("A", "B")
    )
    expected = (
        FINITE_MODULE
        if chart == "finite"
        else tuple(f"gen({index})" for index in range(1, 9))
    )
    membership = (True, False, True, False) if chart == "finite" else (True,) * 4
    variables = h + ((lam,) if chart == "finite" else ())
    program = "\n".join(
        (
            "ring R=0,(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + ",".join(expected) + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            *(f"vector d{index}={value};" for index, value in enumerate(diagonals)),
            *(f"int z{index}=reduce(d{index},M)==0;" for index in range(4)),
            'print("RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(z0)+":"+string(z1)+":"+string(z2)+":"+string(z3)+":"+string(size(M)));',
            "quit;",
        )
    )
    marker = (
        "RESULT:1:"
        + ":".join("1" if value else "0" for value in membership)
        + f":{len(expected)}"
    )
    run_singular(chart, program, marker)
    return {
        "chart": chart,
        "module_generators": expected,
        "diagonal_order": ("A01", "B01", "A23", "B23"),
        "diagonal_membership": membership,
    }


def main():
    geometry = compactification_and_geometry()
    projections = tuple(h31_projection(deletion) for deletion in range(4))
    branches = h31_branches()
    modules = tuple(h22_module(chart) for chart in ("finite", "infinity"))
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "component": 23,
                "boundary": "s=1, k=r=t=infinity",
                "geometry": geometry,
                "h31_projections": projections,
                "h31_branches": branches,
                "h22_modules": modules,
                "fixed_order_marked_H31_empty": True,
                "fixed_order_weighted_H22_empty": True,
                "finite_field_proof_used": False,
                "arbitrary_order_claimed": False,
                "global_conjecture_resolved": False,
                "theorem_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
