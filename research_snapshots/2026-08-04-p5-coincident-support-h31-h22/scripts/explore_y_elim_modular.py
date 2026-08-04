#!/usr/bin/env python3
"""Reduced survivor-locus elimination mod 101 (and 11) for q=2:
eliminate x from (G(t)x, Ax-1), then t; factor the parameter locus.
"""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
SINGLE = tuple(tuple(1 if j == i else 0 for j in range(4)) for i in range(4))
PERMS3 = tuple(itertools.permutations(range(3)))

b, e, m, c = sp.symbols("b e m c")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
X = sp.symbols("x0:4")
Y = sp.symbols("y0:4")
Z = X + Y


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


def reduced_system(q):
    forms = word_forms(q)
    ysolve = {}
    denominators = []
    for i in range(4):
        wd = SINGLE[i]
        expr = forms[wd]
        ai = sp.expand(sp.diff(expr, Y[i]))
        rest = sp.expand(expr - ai * Y[i])
        ysolve[Y[i]] = sp.cancel(-rest / ai)
        denominators.append(sp.factor(ai))
    remaining = [wd for wd in MIXED if wd not in SINGLE]
    numerators = []
    for wd in remaining:
        expr = sp.together(forms[wd].subs(ysolve))
        num, _ = sp.fraction(sp.cancel(expr))
        numerators.append(sp.expand(num))
    arow = sp.expand(forms[(0, 0, 0, 0)])
    return numerators, arow, denominators


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run(program, timeout=540):
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0
    return cp.stdout, time.time() - t0


def modular_locus(q, char):
    numerators, arow, denominators = reduced_system(q)
    eqs = numerators + [arow - 1]
    variables = list(map(str, X)) + list(map(str, T)) + ["b", "e", "m", "c"]
    program = "\n".join((
        f"ring R={char},(" + ",".join(variables) + "),(dp(4),dp(4),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal J=std(I);",
        "ideal D=eliminate(J,x0*x1*x2*x3*t0*t1*t2*t3);",
        "D=std(D);",
        '"PARAMLOCUS";', "D;",
        "LIB \"primdec.lib\";",
        "list pr=minAssGTZ(D);",
        '"MINPRIMES";', "pr;",
        "quit;",
    ))
    out, dt = run(program)
    print(f"q={q} char={char}: {dt:.1f}s")
    if out is None:
        print("  TIMEOUT")
    else:
        print(out)


def main():
    numerators, arow, denominators = reduced_system(2)
    print("y-solve denominators (t-free):", denominators)
    for char in (101, 11):
        modular_locus(2, char)


if __name__ == "__main__":
    main()
