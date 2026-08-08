#!/usr/bin/env python3
"""Verify the generic H31 obstruction on component twenty-four."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import sympy as sp

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
)


def add(*rows):
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(coefficient, row):
    return tuple(sp.expand(coefficient * entry) for entry in row)


def rows(k, s, t):
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    c = (t - k * s) / (1 - k * s * t)
    alpha = (
        A,
        add(A, scale(k, D)),
        add(A, scale(c, C), scale(k, B), scale(-k, D)),
        D,
    )
    beta = (B, add(B, scale(s, C)), C, add(scale(t, A), C, scale(-k * t, B)))
    return alpha, beta


def shifted(beta, alpha, marking):
    return tuple(add(beta[index], scale(marking[index], alpha[index])) for index in range(4))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.expand(sp.fraction(sp.cancel(expression))[0])).replace("**", "^")


def clear_row(entries):
    multiplier = sp.prod(sp.fraction(sp.together(entry))[1] for entry in entries)
    return tuple(sp.expand(sp.fraction(sp.cancel(multiplier * entry))[0]) for entry in entries)


def run_singular(program, timeout=180):
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=timeout, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    return [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]


def row_module_certificate(alpha, beta):
    h = sp.symbols("h0:4")
    marked = shifted(beta, alpha, h)
    mixed, d0, d1 = mixed_matrix(2, alpha, marked)
    generators = ",".join(
        "[" + ",".join(map(sg, clear_row(tuple(mixed[row, col] for col in range(8))))) + "]"
        for row in range(14)
    )
    diagonal0 = "[" + ",".join(map(sg, clear_row(tuple(d0[0, col] for col in range(8))))) + "]"
    diagonal1 = "[" + ",".join(map(sg, clear_row(tuple(d1[0, col] for col in range(8))))) + "]"
    program = "\n".join(
        (
            "ring R=(0,k,s,t),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector d0=" + diagonal0 + ";",
            "vector d1=" + diagonal1 + ";",
            "vector a=reduce(d0,M); vector b=reduce(d1,M);",
            '"RESULT:"+string(a==0)+":"+string(b!=0)+":"+string(size(M));',
            "quit;",
        )
    )
    assert run_singular(program) == ["RESULT:1:1:8"]
    return {"distinguished": 2, "all_alpha_in_module": True, "basis_size": 8}


def projection_certificate(q, alpha, beta, expected):
    h = sp.symbols("h0:4")
    extension = sp.symbols("x0:8")
    inverse = sp.Symbol("u")
    marked = shifted(beta, alpha, h)
    mixed, d0, d1 = mixed_matrix(q, alpha, marked)
    vector = sp.Matrix(extension)
    equations = (*tuple(mixed * vector), (d0 * vector)[0] - 1, inverse * (d1 * vector)[0] - 1)
    eliminated = extension + (inverse,)
    variables = eliminated + h
    program = "\n".join(
        (
            "ring R=(0,k,s,t),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(sg(value) for value in equations) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(sg(value) for value in expected) + "; E=std(E);",
            "ideal A=simplify(reduce(J,E),2); ideal B=simplify(reduce(E,J),2);",
            '"RESULT:"+string(size(J))+":"+string(size(A))+":"+string(size(B));',
            "quit;",
        )
    )
    assert run_singular(program, 300) == ["RESULT:4:0:0"]
    return {"distinguished": q, "ideal": list(map(str, expected))}


def q3_radical_certificate(k, s, t, h):
    expected = (
        h[3] - k * t,
        k * (k * s * t - 1) * h[1] + 2 * t * (k**2 * s**2 - 1) * h[2] + k * s * t - 1,
        h[0],
        2 * t * (k**2 * s**2 - 1) * h[2] ** 2 + (k**2 * s**2 * t**2 - 1) * h[2],
    )
    p1 = (h[3] - k * t, h[2], k * h[1] + 1, h[0])
    p2 = (
        h[3] - k * t,
        2 * t * (k**2 * s**2 - 1) * h[2] + k**2 * s**2 * t**2 - 1,
        h[1] - s * t,
        h[0],
    )
    program = "\n".join(
        (
            "ring R=(0,k,s,t),(h0,h1,h2,h3),dp;",
            "ideal J=" + ",".join(map(sg, expected)) + "; J=std(J);",
            "ideal P1=" + ",".join(map(sg, p1)) + ";",
            "ideal P2=" + ",".join(map(sg, p2)) + ";",
            "ideal I=std(intersect(P1,P2));",
            "ideal A=simplify(reduce(J,I),2); ideal B=simplify(reduce(I,J),2);",
            '"RESULT:"+string(size(J))+":"+string(size(I))+":"+string(size(A))+":"+string(size(B));',
            "quit;",
        )
    )
    assert run_singular(program) == ["RESULT:4:4:0:0"]
    return expected


def branch_unit_certificate(label, q, marking, alpha, beta):
    extension = sp.symbols("x0:8")
    inverse = sp.Symbol("u")
    marked = shifted(beta, alpha, marking)
    mixed, d0, d1 = mixed_matrix(q, alpha, marked)
    vector = sp.Matrix(extension)
    one_marked = marked_extension(q, vector, alpha, marked, 0)
    minor = one_marked.extract((0, 1, 3, 7), range(4)).det(method="domain-ge")
    equations = (
        *tuple(mixed * vector),
        (d0 * vector)[0] - 1,
        inverse * (d1 * vector)[0] - 1,
        minor,
    )
    variables = extension + (inverse,)
    program = "\n".join(
        (
            "ring R=(0,k,s,t),(" + ",".join(map(str, variables)) + "),dp;",
            "option(redSB);",
            "ideal I=" + ",".join(sg(value) for value in equations) + ";",
            "I=slimgb(I);",
            '"RESULT:"+string(size(std(I)))+":"+string(reduce(1,std(I))==0);',
            "quit;",
        )
    )
    assert run_singular(program, 300) == ["RESULT:1:1"]
    return {"branch": label, "distinguished": q, "minor": "N0[0137]", "unit_ideal": True}


def main():
    k, s, t = sp.symbols("k s t")
    h = sp.symbols("h0:4")
    alpha, beta = rows(k, s, t)
    module = row_module_certificate(alpha, beta)
    q0_expected = (h[3] - k * t, h[2], k * (t + 1) * h[1] - 2 * k * s * t - t + 1, h[0])
    q1_expected = (h[3] - k * t, h[2], k * (t - 1) * h[1] + 2 * k * s * t - t - 1, h[0])
    q3_expected = q3_radical_certificate(k, s, t, h)
    projections = [
        projection_certificate(0, alpha, beta, q0_expected),
        projection_certificate(1, alpha, beta, q1_expected),
        projection_certificate(3, alpha, beta, q3_expected),
    ]
    h2b = -(k**2 * s**2 * t**2 - 1) / (2 * t * (k**2 * s**2 - 1))
    branches = [
        ("q0", 0, (0, (2 * k * s * t + t - 1) / (k * (t + 1)), 0, k * t)),
        ("q1", 1, (0, (t + 1 - 2 * k * s * t) / (k * (t - 1)), 0, k * t)),
        ("q3a", 3, (0, -1 / k, 0, k * t)),
        ("q3b", 3, (0, s * t, h2b, k * t)),
    ]
    units = [branch_unit_certificate(*branch, alpha, beta) for branch in branches]
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(k,s,t)",
                "component": 24,
                "row_module_obstruction": module,
                "projection_ideals": projections,
                "q3_radical_prime_count": 2,
                "branch_unit_ideals": units,
                "generic_H31_fibre_empty": True,
                "generic_H22_fibre_closed_by_this_verifier": False,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
