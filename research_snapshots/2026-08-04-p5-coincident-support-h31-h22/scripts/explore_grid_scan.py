#!/usr/bin/env python3
"""Char-0 grid scan: point-check the q=2 marking ideal over an integer box.
Reports any NONUNIT/TIMEOUT points (evidence for/against an empty char-0
survivor locus).  Batches many points into single Singular processes.
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


def main():
    forms = word_forms(2)
    eqs = [forms[wd] for wd in MIXED]
    eqs.append(forms[(0, 0, 0, 0)] - 1)
    eqs.append(W * forms[(1, 1, 1, 1)] - 1)
    gens = ",".join(str(sp.expand(x)).replace("**", "^") for x in eqs)
    variables = list(map(str, Z + (W,) + T))

    values = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
    mvalues = [-5, -3, -1, 0, 1, 2, 3, 5]
    cvalues = [-5, -3, -1, 0, 1, 2, 3, 5]
    points = [pt for pt in itertools.product(values, values, mvalues, cvalues)]
    print(f"scanning {len(points)} integer points (b,e !=0)")

    header = "\n".join((
        "ring S=(0,b,e,m,c),(" + ",".join(variables) + "),(dp(9),dp(4));",
        "ideal I=" + gens + ";",
        "ring R0=0,(" + ",".join(variables) + "),(dp(9),dp(4));",
    ))
    bad = []
    t0 = time.time()
    batch_size = 400
    for start in range(0, len(points), batch_size):
        batch = points[start:start + batch_size]
        body = [header]
        for bb, ee, mm, cc in batch:
            body.append("setring S;")
            body.append(f"ideal Ipt=subst(I,b,{bb},e,{ee},m,{mm},c,{cc});")
            body.append("setring R0;")
            body.append("ideal J=imap(S,Ipt);")
            body.append("J=std(J);")
            body.append(f'"PT {bb} {ee} {mm} {cc} UNIT:"+string(reduce(1,J)==0);')
        body.append("quit;")
        try:
            cp = subprocess.run(["Singular", "-q"], input="\n".join(body), text=True,
                                capture_output=True, timeout=550)
        except subprocess.TimeoutExpired:
            print(f"batch at {start}: TIMEOUT")
            bad.append(("BATCH_TIMEOUT", start))
            continue
        for line in cp.stdout.splitlines():
            if line.startswith("PT ") and not line.endswith("UNIT:1"):
                bad.append(line)
                print("NONUNIT:", line)
    print(f"done in {time.time()-t0:.0f}s; nonunit/timeout entries: {len(bad)}")
    if not bad:
        print("ALL POINTS UNIT")


if __name__ == "__main__":
    main()
