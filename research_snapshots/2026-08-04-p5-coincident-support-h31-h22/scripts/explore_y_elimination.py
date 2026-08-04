#!/usr/bin/env python3
"""t-free y-elimination for the tenth component's q=2,3 frames (repo pattern),
then the small survivor-locus eliminations that were intractable directly.

Single-1 word e_i:  A_i * y_i + sum_j C_ij(t) x_j = 0 with A_i the t-free
0000-row entries.  Reduced system G(t)x=0 (10x4) after clearing the unit
denominators.  Survivor locus: eliminate x from (G x, A x - 1); then
eliminate t -> parameter divisor.
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


def reduce_frame(q):
    forms = word_forms(q)
    # A_i: coefficient of y_i in single-1 word e_i (t-free)
    Acoef = []
    ysolve = {}
    for i in range(4):
        wd = SINGLE[i]
        expr = forms[wd]
        ai = sp.expand(sp.diff(expr, Y[i]))
        assert all(sp.diff(ai, ti) == 0 for ti in T), (q, i)
        assert all(sp.diff(expr, Y[j]) == 0 for j in range(4) if j != i), (q, i)
        rest = sp.expand(expr - ai * Y[i])
        assert all(sp.diff(rest, yy) == 0 for yy in Y)
        ysolve[Y[i]] = sp.cancel(-rest / ai)
        Acoef.append(ai)
    print(f"q={q}: single-1 y-coefficients (t-free): {[sp.factor(a) for a in Acoef]}")
    remaining = [wd for wd in MIXED if wd not in SINGLE]
    Grows = []
    for wd in remaining:
        expr = sp.together(forms[wd].subs(ysolve))
        num, den = sp.fraction(sp.cancel(expr))
        den_f = sp.factor(den)
        num = sp.expand(num)
        assert all(sp.diff(num, yy) == 0 for yy in Y)
        Grows.append((wd, num, den_f))
    # A row on x
    arow = sp.expand(forms[(0, 0, 0, 0)])
    assert all(sp.diff(arow, yy) == 0 for yy in Y)
    return Acoef, Grows, arow, ysolve, forms


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run(program, timeout=550):
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, time.time() - t0
    if cp.returncode != 0:
        print("ERR", cp.stderr[:300])
        return None, time.time() - t0
    return cp.stdout, time.time() - t0


def survivor_locus(q):
    Acoef, Grows, arow, _, _ = reduce_frame(q)
    eqs = [num for (_, num, _) in Grows]
    eqs.append(arow - 1)
    variables = list(map(str, X)) + list(map(str, T)) + ["b", "e", "m", "c"]
    program = "\n".join((
        "ring R=0,(" + ",".join(variables) + "),(dp(4),dp(4),dp(4));",
        "option(redSB);",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal J=std(I);",
        "ideal L=eliminate(J,x0*x1*x2*x3);",
        "L=std(L);",
        '"TLOCUS";', "L;",
        "ideal D=eliminate(J,x0*x1*x2*x3*t0*t1*t2*t3);",
        "D=std(D);",
        '"PARAMLOCUS";', "D;",
        "LIB \"primdec.lib\";",
        "list pr=minAssGTZ(D);",
        '"MINPRIMES";', "pr;",
        "quit;",
    ))
    out, dt = run(program)
    print(f"q={q} survivor-locus elimination: {dt:.1f}s")
    if out is None:
        print("  TIMEOUT (null)")
        return
    print(out)


def main():
    for q in (2, 3):
        survivor_locus(q)


if __name__ == "__main__":
    main()
