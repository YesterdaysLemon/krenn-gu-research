#!/usr/bin/env python3
"""Verify the generic marked-H31 obstruction on component twenty-three."""

from __future__ import annotations

import json
import shutil
import subprocess

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def rows(r, t):
    k = (1 - r * t) / (t - r)
    A = (1, 1, 0, 0)
    C = (1, -1, 0, 0)
    B = (0, 0, 1, 1)
    D = (0, 0, 1, -1)
    alpha = (
        A,
        add(A, D, k),
        add(add(add(A, C, -1), B), D, r),
        add(add(add(tuple(-entry for entry in A), C, -1), B), D, t),
    )
    beta = (B, add(B, C), C, C)
    return alpha, beta


def shifted(beta, alpha, shifts):
    return tuple(add(beta[i], alpha[i], shifts[i]) for i in range(4))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")


def sg(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def clear_expression(expression):
    return sp.expand(sp.fraction(sp.cancel(expression))[0])


def clear_row(entries):
    denominators = [sp.fraction(sp.together(entry))[1] for entry in entries]
    multiplier = sp.prod(denominators)
    return tuple(clear_expression(multiplier * entry) for entry in entries)


def row_module_certificate(q, alpha, beta):
    h = sp.symbols("h0:4")
    marked = shifted(beta, alpha, h)
    mixed, diagonal0, diagonal1 = mixed_matrix(q, alpha, marked)
    generators = ",".join(
        "[" + ",".join(map(sg, clear_row(tuple(mixed[row, column] for column in range(8))))) + "]"
        for row in range(14)
    )
    d0 = "[" + ",".join(map(sg, clear_row(tuple(diagonal0[0, column] for column in range(8))))) + "]"
    d1 = "[" + ",".join(map(sg, clear_row(tuple(diagonal1[0, column] for column in range(8))))) + "]"
    program = "\n".join(
        (
            "ring RR=(0,r,t),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector d0=" + d0 + ";",
            "vector d1=" + d1 + ";",
            "vector a=reduce(d0,M);",
            "vector b=reduce(d1,M);",
            '"RESULT:"+string(a==0)+":"+string(b!=0)+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=120, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:1:10"], completed.stdout
    return {"distinguished": q, "all_alpha_in_row_module": True, "all_beta_in_row_module": False, "basis_size": 10}


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
            "ring RR=(0,r,t),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(sg(clear_expression(value)) for value in equations) + ";",
            "I=slimgb(I);",
            "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
            "ideal E=" + ",".join(sg(clear_expression(value)) for value in expected) + ";",
            "E=std(E);",
            "ideal JE=simplify(reduce(J,E),2);",
            "ideal EJ=simplify(reduce(E,J),2);",
            '"RESULT:"+string((size(JE)==0)&&(size(EJ)==0))+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=180, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:4"], completed.stdout
    return {"distinguished": q, "ideal": list(map(sg, expected)), "bidirectional": True}


def determinant_certificate(matrix, expected):
    entries = ",".join(sg(entry) for entry in matrix)
    program = "\n".join(
        (
            "ring RR=(0,r,t),(p,w),dp;",
            "matrix M[4][4]=" + entries + ";",
            "poly observed=det(M);",
            "poly expected=" + sg(expected) + ";",
            '"RESULT:"+string(observed-expected==0);',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=30, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1"], completed.stdout


def main():
    r, t, p, w = sp.symbols("r t p w", nonzero=True)
    h = sp.symbols("h0:4")
    alpha, beta = rows(r, t)
    modules = [row_module_certificate(q, alpha, beta) for q in (0, 1)]
    projections = [
        projection_certificate(2, alpha, beta, (h[3], h[2], (r + t - 2) * h[1] - r + t, h[0])),
        projection_certificate(3, alpha, beta, (h[3], h[2], (r + t + 2) * h[1] - r + t, h[0])),
    ]
    branches = (
        {
            "q": 2,
            "h": (0, (r - t) / (r + t - 2), 0, 0),
            "e0": (0, (r * t - 1) / (r - t), (r - 1) ** 2 / (r + t - 2), (t - 1) ** 2 / (r + t - 2), 1, 0, 0, 0),
            "e1": (0, 0, 1, 1, 0, 1, 0, 0),
            "d0": 2 * ((r * t + r + t - 3) * p - (r + t - 2) * w),
            "d1": 2 * ((r - 1) * (t - 1) * p / (r + t - 2) - w),
            "factor": -2 * (r - 1) * (t - 1) * (r * t - 1) / ((r - t) * (r + t - 2)),
            "pure": 2 * (1 - r * t) / (r - t),
        },
        {
            "q": 3,
            "h": (0, (r - t) / (r + t + 2), 0, 0),
            "e0": (0, -(r * t - 1) / (r - t), -(r + 1) ** 2 / (r + t + 2), -(t + 1) ** 2 / (r + t + 2), 1, 0, 0, 0),
            "e1": (0, 0, 1, 1, 0, 1, 0, 0),
            "d0": 2 * ((r * t - r - t - 3) * p + (r + t + 2) * w),
            "d1": -2 * ((r + 1) * (t + 1) * p / (r + t + 2) + w),
            "factor": -2 * (r + 1) * (t + 1) * (r * t - 1) / ((r - t) * (r + t + 2)),
            "pure": 2 * (r * t - 1) / (r - t),
        },
    )
    output = []
    for branch in branches:
        marked = shifted(beta, alpha, branch["h"])
        mixed, diagonal0, diagonal1 = mixed_matrix(branch["q"], alpha, marked)
        z = sp.Matrix(branch["e0"]) * p + sp.Matrix(branch["e1"]) * w
        assert all(sp.factor(value) == 0 for value in mixed * z)
        d0 = sp.factor((diagonal0 * z)[0])
        d1 = sp.factor((diagonal1 * z)[0])
        assert sp.factor(d0 - branch["d0"]) == 0
        assert sp.factor(d1 - branch["d1"]) == 0
        marked_map = marked_extension(branch["q"], z, alpha, marked, 0)
        expected_determinant = branch["factor"] * d0 * d1**2
        determinant_certificate(
            marked_map.extract((0, 3, 4, 7), range(4)), expected_determinant
        )
        pure_map = one_marked_map(0, alpha, marked)
        assert sp.factor(pure_map[1, branch["q"]] - branch["pure"]) == 0
        output.append(
            {
                "distinguished": branch["q"],
                "marking": list(map(str, branch["h"])),
                "kernel_dimension": 2,
                "one_marked_minor": str(sp.factor(expected_determinant)),
                "pure_transverse_entry": str(branch["pure"]),
            }
        )
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(r,t)",
                "component": 23,
                "row_module_deletions": modules,
                "projection_ideals": projections,
                "survivor_branches": output,
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
