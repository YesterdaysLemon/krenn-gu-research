#!/usr/bin/env python3
"""Char-0 point checks: at fixed rational (b,e,m,c), is the q=2 marking ideal
unit?  Uses the full (M z, A z - 1, w*Bz - 1) system with params substituted.
Points: the p=11-suspect (2,3,7,5) and a probe grid.
"""
from __future__ import annotations

import itertools
import subprocess
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
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (P, P * m - Q * c, -Q, Q))
    beta = ((0, 1, b, -b), (0, 1, e, -e), (1, 1, 0, 0), (0, c, 1, -1))
    return alpha, beta


def word_forms(q):
    alpha, beta = concentrated_basis()
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    forms = {}
    for wd in WORDS:
        expr = 0
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            expr += perm3(others) * Z[i + (4 if wd[i] else 0)]
        forms[wd] = sp.expand(expr)
    return forms


FORMS2 = word_forms(2)


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def point_check(point, timeout=120):
    sub = dict(zip((b, e, m, c), point))
    eqs = [FORMS2[wd].subs(sub) for wd in MIXED]
    eqs.append(FORMS2[(0, 0, 0, 0)].subs(sub) - 1)
    eqs.append(W * FORMS2[(1, 1, 1, 1)].subs(sub) - 1)
    variables = list(map(str, Z + (W,) + T))
    program = "\n".join((
        "ring R=0,(" + ",".join(variables) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal J=std(I);",
        "ideal L=eliminate(J,x0*x1*x2*x3*y0*y1*y2*y3*w);",
        "L=std(L);",
        '"TIDEAL";', "L;", "quit;",
    ))
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0
    lines = [ln.split("=", 1)[1].replace(" ", "") for ln in cp.stdout.splitlines()
             if ln.startswith("L[")]
    return lines, time.time() - t0


def main():
    points = [
        (2, 3, 7, 5),          # the p=11-suspect point
        (2, 3, 7, sp.Rational(16, 3)),
        (2, 3, 8, 5),
        (1, 1, 1, 1),
        (2, 2, 3, 3),
        (3, 4, 5, 6),
        (1, 2, 3, 4),
        (2, 3, -7, 5),
        (2, -3, 7, 5),
        (5, 7, 2, 3),
    ]
    for point in points:
        result, dt = point_check(point)
        label = "TIMEOUT" if result is None else (
            "UNIT" if result == ["1"] else f"NONUNIT {result}")
        print(f"(b,e,m,c)={point}: {label}  ({dt:.1f}s)")


if __name__ == "__main__":
    main()
