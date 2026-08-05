#!/usr/bin/env python3
"""Independent exact-Q audit of the component-23 ordinary F=h2=0 branch."""

from __future__ import annotations

import functools
import itertools
import json
import subprocess

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMS3 = tuple(itertools.permutations(range(3)))
x = sp.symbols("x0:8")
h0, h1, h2, h3, lam, u = sp.symbols("h0 h1 h2 h3 lam u")


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
    beta = tuple(add(beta[i], alpha[i], (h0, h1, h2, h3)[i]) for i in range(4))
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
        return (lam * row[0] + row[1], row[2], row[3], extension)
    return (row[0], row[1], lam * row[2] + row[3], extension)


def model(alpha, beta, direction):
    ap = tuple(project(alpha[i], x[i], direction) for i in range(4))
    bp = tuple(project(beta[i], x[4 + i], direction) for i in range(4))
    values = {}
    for word in WORDS:
        selected = tuple(bp[i] if word[i] else ap[i] for i in range(4))
        values[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    return values


def cleared_vector(expression, substitutions):
    entries = [
        sp.diff(expression.subs(substitutions, simultaneous=True), variable)
        for variable in x
    ]
    denominators = [sp.factor(sp.fraction(sp.together(entry))[1]) for entry in entries]
    multiplier = functools.reduce(sp.lcm, denominators, sp.Integer(1))
    cleared = [sp.cancel(multiplier * entry) for entry in entries]
    assert all(sp.fraction(entry)[1] == 1 for entry in cleared)
    return (
        "["
        + ",".join(str(sp.expand(entry)).replace("**", "^") for entry in cleared)
        + "]"
    )


def main():
    r, t = sp.Integer(2), sp.Integer(4)
    F = (
        (-2 * r**4 * t**2 + 2 * r**3 * t + 2 * r**2 * t**2 - 2 * r * t) * h0 * h2 * lam
        + (-(r**4) * t**2 + r**3 * t**3 + r**3 * t - r * t**3 - r * t + t**2)
        * h0
        * h3
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
        * h0
        * h3
        + (r**4 * t**2 - r**3 * t - r**2 * t**2 + r * t) * h0 * lam
        + (-(r**3) * t + r**2 * t**2 + r**2 - r * t) * h1 * lam
        + (2 * r**4 - 2 * r**3 * t - 2 * r**2 + 2 * r * t) * h2 * lam
        + (-(r**4) * t**2 + r**3 * t + r**2 * t**2 - r * t) * h0
        + (r**3 * t - r**2 * t**2 - r**2 + r * t) * h1
        + (-2 * r**3 * t + 2 * r**2 * t**2 + 2 * r * t - 2 * t**2) * h3
        + (-(r**3) * t + r**2 * t**2 + r**2 - r * t) * lam
        + (r**3 * t - r**2 * t**2 - r**2 + r * t)
    )
    F0 = sp.factor(F.subs(h2, 0))
    coefficient = sp.factor(sp.diff(F0, h1))
    assert sp.expand(coefficient - (-2 * (lam - 1) * (2 - 4) * (2 * 4 - 1))) == 0
    h1_solution = sp.cancel(-F0.subs(h1, 0) / coefficient)
    assert sp.cancel(F0.subs(h1, h1_solution)) == 0

    alpha, beta = component_rows()
    models = (model(alpha, beta, "D01"), model(alpha, beta, "D23"))
    substitutions = {h2: 0, h1: h1_solution}
    generators = [
        cleared_vector(values[word], substitutions)
        for values in models
        for word in MIXED
    ]
    relation = "u*lam*(lam-1)*(lam+1)-1"
    generators.extend(
        "[" + ",".join(relation if column == row else "0" for column in range(8)) + "]"
        for row in range(8)
    )
    program = "\n".join(
        (
            "ring Q=0,(h0,h3,lam,u),dp;",
            "option(redSB);",
            "module M=" + ",".join(generators) + "; M=std(M);",
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
        timeout=120,
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
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "Q",
                "specialization": {"r": 2, "t": 4},
                "independent_no_repository_imports": True,
                "F_solved_exactly": True,
                "ordinary_weight_localization": True,
                "localized_mixed_module_full": True,
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
