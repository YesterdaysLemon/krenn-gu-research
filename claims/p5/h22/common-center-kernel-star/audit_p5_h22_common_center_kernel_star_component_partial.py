#!/usr/bin/env python3
"""Independent exact-Q audit of the component-23 partial H22 module pattern."""

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


def add(left, right, coefficient=1):
    return tuple(sp.expand(left[i] + coefficient * right[i]) for i in range(4))


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in itertools.permutations(range(3))
    ))


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


def model(alpha, beta, extension, direction, chart, slope=None):
    aa = tuple(project(alpha[i], extension[i], direction, chart, slope) for i in range(4))
    bb = tuple(project(beta[i], extension[4 + i], direction, chart, slope) for i in range(4))
    coefficients = {}
    for word in WORDS:
        selected = tuple(bb[i] if word[i] else aa[i] for i in range(4))
        coefficients[word] = sp.expand(sum(
            selected[i][3] * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
            for i in range(4)
        ))
    return coefficients


def component_rows(r, t, h):
    k = (1 - r * t) / (t - r)
    A, C = (1, 1, 0, 0), (1, -1, 0, 0)
    B, D = (0, 0, 1, 1), (0, 0, 1, -1)
    alpha = (
        A,
        add(A, D, k),
        add(add(add(A, C, -1), B), D, r),
        add(add(add(tuple(-entry for entry in A), C, -1), B), D, t),
    )
    beta = (B, add(B, C), C, C)
    marked = tuple(add(beta[i], alpha[i], h[i]) for i in range(4))
    return alpha, marked


def row(expression, extension):
    return "[" + ",".join(
        str(sp.expand(sp.diff(expression, variable))).replace("**", "^")
        for variable in extension
    ) + "]"


def check_point(r, t, chart):
    h = sp.symbols("h0:4")
    slope = sp.Symbol("lam") if chart == "finite" else None
    extension = sp.symbols("x0:8")
    alpha, beta = component_rows(sp.Integer(r), sp.Integer(t), h)
    c01 = model(alpha, beta, extension, "D01", chart, slope)
    c23 = model(alpha, beta, extension, "D23", chart, slope)
    variables = ("h0", "h1", "h2", "h3", "lam") if chart == "finite" else ("h0", "h1", "h2", "h3")
    expected = (
        ("gen(1)", "gen(2)", "gen(3)", "gen(4)", "gen(6)", "gen(7)", "gen(8)", "(lam-1)*gen(5)")
        if chart == "finite" else tuple(f"gen({index})" for index in range(1, 9))
    )
    lines = [
        "ring R=0,(" + ",".join(variables) + "),dp;",
        "option(redSB);",
        "module M=" + ",".join(row(c01[word], extension) for word in MIXED)
        + "," + ",".join(row(c23[word], extension) for word in MIXED) + ";",
        "M=std(M);",
        "module E=" + ",".join(expected) + "; E=std(E);",
        "module ME=simplify(reduce(M,E),2); module EM=simplify(reduce(E,M),2);",
        'print("RESULT:"+string((size(ME)==0)&&(size(EM)==0))+":"+string(size(M)));',
        "quit;",
    ]
    native = shutil.which("Singular")
    command = (native, "-q") if native else ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    completed = subprocess.run(
        command,
        input="\n".join(lines),
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed.stderr
    markers = [line for line in completed.stdout.splitlines() if line.startswith("RESULT:")]
    assert markers == ["RESULT:1:8"], (r, t, chart, completed.stdout)
    return {"r": r, "t": t, "chart": chart, "module_equality": True}


def main():
    points = [(2, 3), (2, 4), (3, 5)]
    checks = [check_point(r, t, chart) for r, t in points for chart in ("finite", "infinity")]
    print(json.dumps({
        "status": "pass",
        "field": "Q",
        "component": 23,
        "checks": checks,
        "role": "exact specialization audit only",
        "generic_finite_all_markings_proved_by_audit": False,
        "finite_field_proof_used": False,
        "global_conjecture_resolved": False,
    }, indent=2))


if __name__ == "__main__":
    main()
