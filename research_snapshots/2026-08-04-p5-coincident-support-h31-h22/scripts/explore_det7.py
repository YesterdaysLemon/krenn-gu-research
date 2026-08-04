#!/usr/bin/env python3
"""Symbolic 7x7 pivot determinants (marking-coupled divisors) for q=2,3, D_23.

On {det7 != 0} the mixed kernel is exactly the universal reconstruction line,
so genuine survivors need det7 = 0.  Factor det7 -> explicit divisor list.
Check which factors vanish at the p=11 modular survivor (b,e,m,c;t)=(2,3,7,5;1,0,0,2).
"""
from __future__ import annotations

import itertools

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


def report(label, M):
    sub = M[list(ROWS7), list(COLS7)]
    det = sub.det(method="berkowitz")
    det = sp.factor(det)
    print(f"{label}: det7 = {det}")
    point = {b: 2, e: 3, m: 7, c: 5, T[0]: 1, T[1]: 0, T[2]: 0, T[3]: 2}
    factors = sp.factor_list(det)
    print("  factor evaluation at p=11 survivor point (mod 11):")
    for fac, mult in factors[1]:
        val = sp.expand(fac.subs(point))
        if val.free_symbols:
            print(f"    {fac}^{mult}: depends on {val.free_symbols}, value {val}")
        else:
            print(f"    {fac}^{mult}: value {val} == {int(val) % 11} mod 11")
    return det


def main():
    for q in (2, 3):
        report(f"H31 q={q}", h31_mixed(q))
    report("D_23", d23_mixed())


if __name__ == "__main__":
    main()
