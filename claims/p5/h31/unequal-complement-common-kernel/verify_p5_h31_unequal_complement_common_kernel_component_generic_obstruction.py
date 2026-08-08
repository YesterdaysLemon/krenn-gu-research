#!/usr/bin/env python3
"""Verify generic H31 obstruction on component twenty-two."""

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
    one_marked_map,
)


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
    return sp.expand(sp.fraction(sp.together(expression))[0])


def clear_row(entries):
    denominators = [sp.fraction(sp.together(entry))[1] for entry in entries]
    multiplier = sp.prod(denominators)
    return tuple(
        sp.expand(sp.fraction(sp.together(multiplier * entry))[0]) for entry in entries
    )


def projection_certificate(distinguished, alpha, beta, expected):
    shifts = sp.symbols("h0:4")
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    marked = shifted(beta, alpha, shifts)
    mixed, diagonal0, diagonal1 = mixed_matrix(distinguished, alpha, marked)
    vector = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * vector),
        (diagonal0 * vector)[0] - 1,
        inverse * (diagonal1 * vector)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    program = "\n".join(
        (
            "ring RR=(0,A,R,D),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
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
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=240,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert len(markers) == 1 and markers[0].split(":")[1] == "1", completed.stdout
    return {"distinguished": distinguished, "ideal": list(map(sg, expected))}


def row_module_certificate(distinguished, alpha, beta):
    shifts = sp.symbols("h0:4")
    marked = shifted(beta, alpha, shifts)
    mixed, diagonal0, _diagonal1 = mixed_matrix(distinguished, alpha, marked)
    generators = ",".join(
        "[" + ",".join(map(sg, clear_row(tuple(mixed[row, column] for column in range(8))))) + "]"
        for row in range(14)
    )
    diagonal = "[" + ",".join(map(sg, clear_row(tuple(diagonal0[0, column] for column in range(8))))) + "]"
    program = "\n".join(
        (
            "ring RR=(0,A,R,D),(h0,h1,h2,h3),dp;",
            "option(redSB);",
            "module M=" + generators + ";",
            "M=std(M);",
            "vector d=" + diagonal + ";",
            "vector r=reduce(d,M);",
            '"RESULT:"+string(r==0)+":"+string(size(M));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(), input=program, text=True, capture_output=True, timeout=120, check=False
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:10"], completed.stdout
    return {"distinguished": distinguished, "all_kernel_in_mixed_module": True, "basis_size": 10}


def main():
    A, R, D, p, w = sp.symbols("A R D p w", nonzero=True)
    h = sp.symbols("h0:4")
    s = 2 * A + R
    alpha, canonical = component_rows(A, R, D)
    projections = (
        projection_certificate(
            0,
            alpha,
            canonical,
            (
                h[2],
                h[1],
                8 * D * s * h[0] - 2 * (D + 1) * h[3] + (5 - 3 * D) * s,
                4 * (h[3] + s / 2) * (h[3] + (2 * A + 3 * R) / 2),
            ),
        ),
        projection_certificate(
            1,
            alpha,
            canonical,
            (
                2 * h[3] - s,
                h[1],
                4 * D * h[0] - R * (D + 1) * h[2] + 3 - D,
                h[2] * (R * h[2] + 1),
            ),
        ),
    )
    modules = tuple(
        row_module_certificate(q, alpha, canonical) for q in (2, 3)
    )

    branches = (
        {
            "label": "q0a",
            "q": 0,
            "h": ((D - 3) / (4 * D), 0, 0, -s / 2),
            "e0": (-D * s, -R, 0, 1, R * (D + 1) / 4, 1, 1, 0),
            "e1": (-D, -1, -1, 0, (D + 1) / 4, 0, 0, 1),
            "d0": 4 * D * (s * p + w),
            "d1": (D + 1) * p,
            "rows": (0, 1, 3, 7),
            "minor": -2 * D,
            "pure_row": 1,
        },
        {
            "label": "q0b",
            "q": 0,
            "h": ((A * (D - 3) - 2 * R) / (2 * D * s), 0, 0, -(2 * A + 3 * R) / 2),
            "e0": (-2 * D * (A + R), 0, R, 1, -A * R * (D + 1) / (2 * s), 1, 1, 0),
            "e1": (-D, -A / (A + R), -A / (A + R), 0, A**2 * (D + 1) / (2 * (A + R) * s), 0, 0, 1),
            "d0": 2 * D * s * (2 * (A + R) * p + w) / (A + R),
            "d1": (D + 1) * p,
            "rows": (0, 1, 3, 7),
            "minor": -2 * D,
            "pure_row": 1,
        },
        {
            "label": "q1a",
            "q": 1,
            "h": ((D - 3) / (4 * D), 0, 0, s / 2),
            "e0": (0, -s, -2 * (A + R), -1, (A + R) * (D + 1) / 2, 1, 1, 0),
            "e1": (-D, -1, -1, 0, (D + 1) / 4, 0, 0, 1),
            "d0": -4 * D * (s * p + w),
            "d1": (D + 1) * p,
            "rows": (0, 1, 3, 7),
            "minor": 2 * D,
            "pure_row": 1,
        },
        {
            "label": "q1b",
            "q": 1,
            "h": (-1 / D, 0, -1 / R, s / 2),
            "e0": (0, -s, R * (A + R) / (2 * A), (A + R) / (2 * A), (A + R) * (D + 1) / 4, -(A + R) / (2 * A), 1, 0),
            "e1": (-D, -2, R / A, 1 / A, (D + 1) / 2, -1 / A, 0, 1),
            "d0": D * R * (s * p + 2 * w) / A,
            "d1": (D + 1) * p / 2,
            "rows": (0, 2, 3, 7),
            "minor": D,
            "pure_row": 2,
        },
    )

    branch_output = []
    for branch in branches:
        marked = shifted(canonical, alpha, branch["h"])
        mixed, diagonal0, diagonal1 = mixed_matrix(branch["q"], alpha, marked)
        z = sp.Matrix(branch["e0"]) * p + sp.Matrix(branch["e1"]) * w
        assert all(sp.factor(value) == 0 for value in mixed * z)
        actual_d0 = sp.factor((diagonal0 * z)[0])
        actual_d1 = sp.factor((diagonal1 * z)[0])
        assert sp.factor(actual_d0 - branch["d0"]) == 0
        assert sp.factor(actual_d1 - branch["d1"]) == 0
        one_marked = marked_extension(branch["q"], z, alpha, marked, 3)
        actual_minor = sp.factor(one_marked.extract(branch["rows"], range(4)).det())
        expected_minor = sp.factor(branch["minor"] * actual_d0 * actual_d1 * p)
        assert sp.factor(actual_minor - expected_minor) == 0
        pure_map = one_marked_map(3, alpha, marked)
        assert sp.factor(pure_map[branch["pure_row"], branch["q"]] - D) == 0
        branch_output.append(
            {
                "label": branch["label"],
                "distinguished": branch["q"],
                "marking": list(map(str, branch["h"])),
                "kernel_dimension": 2,
                "one_marked_minor": str(expected_minor),
            }
        )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(A,R,D)",
                "component": 22,
                "projection_ideals": projections,
                "row_module_obstructions": modules,
                "binary_survivor_branches": branch_output,
                "generic_H31_fibre_empty": True,
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
