#!/usr/bin/env python3
"""Identify the universal kernels and the A==0 identity mechanisms exactly.

(1) q in {0,1} / D_01: decompose the A-row vanishing into the two row-level
    mechanisms (coincident ybar supports; apolar mode-2/3 alpha tails).
(2) q in {2,3}: the kernel line is the coordinate-restoration z_rec; verify
    M z_rec = 0, A z_rec = 0, B z_rec = -2kP symbolically in t.
(3) D_23 pencil: find the universal kernel direction symbolically (guess from
    rational sample, verify identically in t and slope).
"""
from __future__ import annotations

import itertools

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, k, m, c, r = sp.symbols("b e k m c r")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis(kval=None):
    kk = k if kval is None else kval
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, kk),
             (P, P * m - Q * c, -Q, Q * kk))
    beta = ((0, 1, b, -b * kk), (0, 1, e, -e * kk), (1, 1, 0, 0), (0, c, 1, -kk))
    return alpha, beta


def marked(kval=None):
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    return alpha, betat


def h31_words(q, kval=None):
    alpha, betat = marked(kval)
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    out = {}
    for wd in WORDS:
        expr = 0
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            expr += perm3(others) * Z[i + (4 if wd[i] else 0)]
        out[wd] = sp.expand(expr)
    return out


def mechanism_q01():
    alpha, _ = concentrated_basis()
    # tails in columns (2,3)
    a2t = (alpha[2][2], alpha[2][3])
    a3t = (alpha[3][2], alpha[3][3])
    apolar = sp.expand(a2t[0] * a3t[1] + a2t[1] * a3t[0])
    assert apolar == 0
    print("mechanism: perm2(alpha_2|{2,3}, alpha_3|{2,3}) =",
          f"(1)({sp.factor(a3t[1])}) + ({alpha[2][3]})({sp.factor(a3t[0])}) = 0",
          "(apolar tails; equivalent to the mode-3 concentration T_1110=0)")
    print("mechanism: alpha_0 = alpha_1 = ybar supported in columns {0,1}:",
          "any 3x3 all-alpha permanent containing both dies on one common column")


def q23_reconstruction():
    for q in (2, 3):
        words = h31_words(q, kval=None)
        alpha, betat = marked(kval=None)
        zrec = {Z[i]: alpha[i][q] for i in range(4)}
        zrec.update({Z[4 + i]: betat[i][q] for i in range(4)})
        for wd in WORDS:
            val = sp.expand(words[wd].subs(zrec))
            if wd == (1, 1, 1, 1):
                assert sp.expand(val + 2 * k * P) == 0, (q, val)
            else:
                assert val == 0, (q, wd, val)
        print(f"q={q}: z_rec (restore column {q}) has M z=0, A z=0, B z=-2kP"
              " identically in (t, params, k)")


def d23_kernel():
    alpha, betat = marked(kval=None)

    def drow(row, ext):
        return (row[0], row[1], r * row[2] + row[3], ext)

    alpha_d = tuple(drow(alpha[i], Z[i]) for i in range(4))
    beta_d = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    words = {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i] for i in range(4)))
             for wd in WORDS}
    # guess: restore the lost column-(2,3) direction transverse to (r,1):
    # ext_i = s*row_i[2] + row_i[3] would give a second diagonal deletion D^s;
    # the permanent-multilinear expansion suggests ext = row[3] (s=0) plus
    # correction.  Test the one-parameter family ext_i = row_i[3]:
    for label, extfun in (("col3", lambda row: row[3]),
                          ("col2", lambda row: row[2]),
                          ("col3-r*col2? no: (k)-weighted", None)):
        if extfun is None:
            continue
        sub = {Z[i]: extfun(alpha[i]) for i in range(4)}
        sub.update({Z[4 + i]: extfun(betat[i]) for i in range(4)})
        vals = {wd: sp.expand(words[wd].subs(sub)) for wd in WORDS}
        nz = {wd: sp.factor(v) for wd, v in vals.items() if sp.expand(v) != 0}
        print(f"D_23 ext={label}: nonzero words -> {nz}")


def main():
    mechanism_q01()
    q23_reconstruction()
    d23_kernel()


if __name__ == "__main__":
    main()
