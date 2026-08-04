#!/usr/bin/env python3
"""Char-0 function-field H31 marking projections for the tenth component.

For q in {2,3}: eliminate (z,w) from
    ideal( 14 mixed rows, A z - 1, w*(B z) - 1 )
over C(b,e,m,c) (gauge k=1), keeping the marking t.  Ordering
(dp(9),dp(4)), std + eliminate, timeout 550 s, fail-closed.
"""
from __future__ import annotations

import itertools
import subprocess
import sys
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS3 = tuple(itertools.permutations(range(3)))

b, e, m, c = sp.symbols("b e m c")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def concentrated_basis():
    alpha = (
        (1, -1, 0, 0),
        (1, -1, 0, 0),
        (0, 0, 1, 1),
        (P, P * m - Q * c, -Q, Q),
    )
    beta = (
        (0, 1, b, -b),
        (0, 1, e, -e),
        (1, 1, 0, 0),
        (0, c, 1, -1),
    )
    return alpha, beta


def word_coeffs(q):
    alpha, beta = concentrated_basis()
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    out = {}
    for wd in WORDS:
        expr = 0
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            zv = Z[i + (4 if wd[i] else 0)]
            expr += perm3(others) * zv
        out[wd] = sp.expand(expr)
    return out


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run_singular(program, timeout):
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0, "TIMEOUT"
    if cp.returncode != 0 or cp.stderr.strip():
        return None, time.time() - t0, f"ERR rc={cp.returncode} stderr={cp.stderr[:500]}"
    return cp.stdout, time.time() - t0, "OK"


def projection(q, timeout=550):
    coeffs = word_coeffs(q)
    eqs = [coeffs[wd] for wd in MIXED]
    eqs.append(coeffs[(0, 0, 0, 0)] - 1)
    eqs.append(W * coeffs[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    program = "\n".join((
        "ring R=(0,b,e,m,c),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal incidence=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal basis=std(incidence);",
        "ideal marking=eliminate(basis," + "*".join(map(str, eliminated)) + ");",
        "marking=std(marking);",
        '"MARKING";',
        "marking;",
        "quit;",
    ))
    out, dt, status = run_singular(program, timeout)
    print(f"q={q}: {status} in {dt:.1f}s")
    if out is not None:
        for line in out.splitlines():
            if line.startswith("marking[") or line == "MARKING":
                print("   ", line.strip())
    return out


def main():
    for q in (2, 3):
        projection(q)


if __name__ == "__main__":
    main()
