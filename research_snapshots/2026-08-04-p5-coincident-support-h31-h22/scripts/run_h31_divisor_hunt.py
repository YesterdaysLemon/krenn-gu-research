#!/usr/bin/env python3
"""Sharpen the H31 q=2,3 exclusions for the tenth component.

(1) Over-Z elimination: params as ring variables; eliminate (z,w) from
    (mixed rows, A z - 1, w*Bz - 1); the result in Q[b,e,m,c,t] is the
    closure of the genuine-survivor locus -> explicit divisor list.
(2) Rowspan test: is A in rowspan(M(t)) over Q(b,e,m,c,t)?  Tested at
    random rational parameter samples with t symbolic, then (if it holds)
    solved exactly.
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


def mixed_matrix(q):
    coeffs = word_coeffs(q)
    M = sp.Matrix([[sp.diff(coeffs[wd], zz) for zz in Z] for wd in MIXED])
    A = sp.Matrix([[sp.diff(coeffs[(0, 0, 0, 0)], zz) for zz in Z]])
    B = sp.Matrix([[sp.diff(coeffs[(1, 1, 1, 1)], zz) for zz in Z]])
    return M, A, B


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
        return None, time.time() - t0, f"ERR rc={cp.returncode} stderr={cp.stderr[:400]}"
    return cp.stdout, time.time() - t0, "OK"


def over_z_elimination(q, timeout=550):
    coeffs = word_coeffs(q)
    eqs = [coeffs[wd] for wd in MIXED]
    eqs.append(coeffs[(0, 0, 0, 0)] - 1)
    eqs.append(W * coeffs[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T + (b, e, m, c)
    program = "\n".join((
        "ring R=0,(" + ",".join(map(str, variables)) + "),(dp(9),dp(8));",
        "option(redSB);",
        "ideal incidence=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal basis=std(incidence);",
        "ideal locus=eliminate(basis," + "*".join(map(str, eliminated)) + ");",
        "locus=std(locus);",
        '"LOCUS";',
        "locus;",
        '"MINPRIMES";',
        "LIB \"primdec.lib\";",
        "list pr=minAssGTZ(locus);",
        "pr;",
        "quit;",
    ))
    out, dt, status = run_singular(program, timeout)
    print(f"[over-Z elim] q={q}: {status} in {dt:.1f}s")
    if out is not None:
        print(out)
    return out


def rowspan_test(q):
    M, A, B = mixed_matrix(q)
    import random
    random.seed(7)
    ok_samples = 0
    for trial in range(2):
        subs = {b: sp.Rational(random.randint(2, 19)), e: sp.Rational(random.randint(2, 19)),
                m: sp.Rational(random.randint(2, 19)), c: sp.Rational(random.randint(2, 19))}
        Ms = M.subs(subs)
        As = A.subs(subs)
        lam = sp.symbols(f"lam0:{len(MIXED)}")
        eqs = []
        for col in range(8):
            expr = sum(lam[i] * Ms[i, col] for i in range(len(MIXED))) - As[0, col]
            eqs.append(sp.expand(expr))
        # each eq is polynomial in t and linear in lam; solve over Q(t)
        sol = sp.solve(eqs, lam, dict=True)
        print(f"[rowspan] q={q} sample {tuple(subs.values())}: "
              f"{'SOLVABLE' if sol else 'NO SOLUTION'}")
        if sol:
            ok_samples += 1
    return ok_samples == 2


def main():
    for q in (2, 3):
        over_z_elimination(q)
    for q in (2, 3):
        rowspan_test(q)


if __name__ == "__main__":
    main()
