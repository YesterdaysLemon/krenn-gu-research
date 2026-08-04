#!/usr/bin/env python3
"""Remaining exact H22 ingredients for the tenth component.

(a) D_23 A row with k symbolic; (b) z* kernel identity with k symbolic;
(c) doubled-column identity; (d) slope-divisor eliminations at r=1, r=-1
    (k=1) and at the H31 endpoints r=0 (should match q=2).
"""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, k, m, c, r = sp.symbols("b e k m c r")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis(kk):
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, kk),
             (P, P * m - Q * c, -Q, Q * kk))
    beta = ((0, 1, b, -b * kk), (0, 1, e, -e * kk), (1, 1, 0, 0), (0, c, 1, -kk))
    return alpha, beta


def d23_words(kk, slope):
    alpha, beta = concentrated_basis(kk)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))

    def drow(row, ext):
        return (row[0], row[1], slope * row[2] + row[3], ext)

    alpha_d = tuple(drow(alpha[i], Z[i]) for i in range(4))
    beta_d = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    return alpha, betat, {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i]
                                          for i in range(4))) for wd in WORDS}


def a_row_symbolic_k():
    alpha, betat, words = d23_words(k, r)
    arow = [sp.factor(sp.diff(words[(0, 0, 0, 0)], zz)) for zz in Z]
    print("D_23 A row (k symbolic):")
    for name, val in zip(("x0", "x1", "x2", "x3", "y0", "y1", "y2", "y3"), arow):
        print(f"   {name}: {val}")
    astar = 2 * b * c * e - (b + e) * (m - 1)
    expected = (-(r + k) * k * astar, -(r + k) * k * astar,
                2 * k * Q * (r - k), -2 * k * (r + k), 0, 0, 0, 0)
    match = all(sp.expand(a_ - e_) == 0 for a_, e_ in zip(
        [sp.diff(words[(0, 0, 0, 0)], zz) for zz in Z], expected))
    print("   matches -(r+k)k(A*,A*,.,2)+2kQ(r-k) pattern:", match)


def zstar_identity():
    alpha, betat, words = d23_words(k, r)
    sub = {Z[i]: r * alpha[i][3] + k**2 * alpha[i][2] for i in range(4)}
    sub.update({Z[4 + i]: r * betat[i][3] + k**2 * betat[i][2] for i in range(4)})
    for wd in WORDS:
        val = sp.expand(words[wd].subs(sub))
        if wd == (1, 1, 1, 1):
            assert sp.expand(val + 2 * k * P * (r - k) ** 2) == 0, val
        else:
            assert val == 0, (wd, val)
    print("z* identity: ext_i = r*row_i[3] + k^2*row_i[2] gives M z*=0, A z*=0,")
    print("             B z* = -2kP(r-k)^2, identically in (t,params,k,r)")


def doubled_column_identity():
    alpha, beta = concentrated_basis(k)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    for wd in WORDS:
        rows = tuple(betat[i] if wd[i] else alpha[i] for i in range(4))
        d2 = perm4(tuple((row[0], row[1], row[2], row[2]) for row in rows))
        d3 = perm4(tuple((row[0], row[1], row[3], row[3]) for row in rows))
        val = sp.expand(d3 + k**2 * d2)
        if wd == (1, 1, 1, 1):
            assert sp.expand(val - 4 * k**2 * P) == 0, val
        else:
            assert val == 0, (wd, val)
    print("doubled-column identity: D3_w + k^2 D2_w = 0 (w != 1111), = 4k^2 P at 1111")


def sing(expr):
    return str(sp.expand(expr)).replace("**", "^")


def run_projection(label, slope_val, timeout=550):
    alpha, betat, words = d23_words(sp.Integer(1), slope_val)
    eqs = [words[wd] for wd in MIXED]
    eqs.append(words[(0, 0, 0, 0)] - 1)
    eqs.append(W * words[(1, 1, 1, 1)] - 1)
    eliminated = Z + (W,)
    variables = eliminated + T
    params = "b,e,m,c" if slope_val != r else "b,e,m,c,r"
    program = "\n".join((
        f"ring R=(0,{params}),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
        "option(redSB);",
        "ideal incidence=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal basis=std(incidence);",
        "ideal marking=eliminate(basis," + "*".join(map(str, eliminated)) + ");",
        "marking=std(marking);",
        '"MARKING";', "marking;", "quit;",
    ))
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"D_23 {label}: TIMEOUT")
        return None
    dt = time.time() - t0
    lines = [ln.split("=", 1)[1].replace(" ", "") for ln in cp.stdout.splitlines()
             if ln.startswith("marking[")]
    print(f"D_23 {label}: {dt:.1f}s -> {lines}")
    return lines


def main():
    a_row_symbolic_k()
    zstar_identity()
    doubled_column_identity()
    run_projection("slope r=1 (equal-weight analogue)", sp.Integer(1))
    run_projection("slope r=-1", sp.Integer(-1))
    run_projection("slope r=0 (H31 q=2 endpoint)", sp.Integer(0))


if __name__ == "__main__":
    main()
