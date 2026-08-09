#!/usr/bin/env python3
"""Independent exact-Q audit of the component-23 lambda=1 H22 obstruction."""

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


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def component_rows():
    r, t = sp.Integer(2), sp.Integer(4)
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


def project(row, extension, direction):
    if direction == "D01":
        return (row[0] + row[1], row[2], row[3], extension)
    return (row[0], row[1], row[2] + row[3], extension)


def model(alpha, beta, direction):
    ap = tuple(project(alpha[i], x[i], direction) for i in range(4))
    bp = tuple(project(beta[i], x[4 + i], direction) for i in range(4))
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


def coefficient_vector(expression):
    return (
        "["
        + ",".join(
            str(sp.expand(sp.diff(expression, variable))).replace("**", "^")
            for variable in x
        )
        + "]"
    )


def main():
    alpha, beta = component_rows()
    models = (model(alpha, beta, "D01"), model(alpha, beta, "D23"))
    generators = ",".join(
        coefficient_vector(values[word]) for values in models for word in MIXED
    )
    diagonals = tuple(
        coefficient_vector(values[word])
        for values in models
        for word in (WORDS[0], WORDS[-1])
    )
    expected = ",".join(f"gen({index})" for index in (1, 2, 3, 4, 6, 7, 8))
    program = "\n".join(
        (
            "ring Q=0,(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + "; M=std(M);",
            "module E=" + expected + "; E=std(E);",
            "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
            "vector A01=" + diagonals[0] + "; vector B01=" + diagonals[1] + ";",
            "vector A23=" + diagonals[2] + "; vector B23=" + diagonals[3] + ";",
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
    assert markers == ["RESULT:1:1:1:1:0:7"], completed.stdout

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"r": 2, "t": 4},
                "independent_no_repository_imports": True,
                "mixed_module": ["e1", "e2", "e3", "e4", "e6", "e7", "e8"],
                "module_equality_bidirectional": True,
                "diagonal_membership_A01_A23_B01_B23": [True, True, True, False],
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
