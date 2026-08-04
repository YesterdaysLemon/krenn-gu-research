#!/usr/bin/env python3
"""det7 divisors via Singular determinant+factorize."""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, m, c, r = sp.symbols("b e m c r")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")

ROWS7 = (0, 1, 3, 4, 5, 7, 8)
COLS7 = (0, 1, 2, 3, 4, 5, 6)


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis():
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (P, P * m - Q * c, -Q, Q))
    beta = ((0, 1, b, -b), (0, 1, e, -e), (1, 1, 0, 0), (0, c, 1, -1))
    return alpha, beta


def marked_rows():
    alpha, beta = concentrated_basis()
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    return alpha, betat


def h31_mixed(q):
    alpha, betat = marked_rows()
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    M = sp.zeros(len(MIXED), 8)
    for ridx, wd in enumerate(MIXED):
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            M[ridx, i + (4 if wd[i] else 0)] += perm3(others)
    return M


def d23_mixed():
    alpha, betat = marked_rows()

    def drow(row, ext):
        return (row[0], row[1], r * row[2] + row[3], ext)

    alpha_d = tuple(drow(alpha[i], Z[i]) for i in range(4))
    beta_d = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    words = {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i] for i in range(4)))
             for wd in WORDS}
    return sp.Matrix([[sp.diff(words[wd], zz) for zz in Z] for wd in MIXED])


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run(program, timeout=540):
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


def det7(label, M):
    sub = M[list(ROWS7), list(COLS7)]
    entries = ",".join(sing(sub[i, j]) for i in range(7) for j in range(7))
    program = "\n".join((
        "ring R=0,(t0,t1,t2,t3,b,e,m,c,r),dp;",
        f"matrix S[7][7]={entries};",
        "poly d=det(S);",
        '"DET";', "d;",
        '"FACTORS";',
        "list f=factorize(d);",
        "f;",
        "quit;",
    ))
    out, dt = run(program)
    print(f"== {label} ({dt:.1f}s) ==")
    if out is None:
        print("TIMEOUT/ERR")
    else:
        print(out)


def main():
    for q in (2, 3):
        det7(f"H31 q={q}", h31_mixed(q))
    det7("D_23", d23_mixed())


if __name__ == "__main__":
    main()
