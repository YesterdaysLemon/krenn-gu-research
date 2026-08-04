#!/usr/bin/env python3
"""Exploration: H31 frames of the TENTH (coincident-support) component.

Family (P4_INOUT_PATH_STRATUM_WORKING_NOTE.md, branch_ambient_certificates.py),
with the working note's parameter r renamed to c (r is reserved for the H22
slope), and the concentrated pure-factor bases derived here:

    raw planes (rows = (bit0 row, bit1 row)):
      U_0 = span(ybar, (0,1,b,-bk)),   U_1 = span(ybar, (0,1,e,-ek)),
      U_2 = span(u3,  (0,0,1,k)),      U_3 = span((1,m,0,0),(0,c,1,-k)),
      ybar=(1,-1,0,0), u3=(1,1,0,0).
    raw support: T_1100 = -2bek(m+1) =: -2kQ,  T_1101 = -2k(bec+b+e) =: -2kP.

Concentration: swap mode-2 rows, and replace mode-3 alpha by
P*(1,m,0,0) - Q*(0,c,1,-k); then the support is the single word 1111 with
T_1111 = -2kP.
"""
from __future__ import annotations

import itertools
import random
import sys

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS = tuple(itertools.permutations(range(4)))
PERMS3 = tuple(itertools.permutations(range(3)))

b, e, k, m, c = sp.symbols("b e k m c")
P = b * e * c + b + e
Q = b * e * (m + 1)


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS))


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def concentrated_basis(kval=None):
    kk = k if kval is None else kval
    alpha = (
        (1, -1, 0, 0),
        (1, -1, 0, 0),
        (0, 0, 1, kk),
        (P, P * m - Q * c, -Q, Q * kk),
    )
    beta = (
        (0, 1, b, -b * kk),
        (0, 1, e, -e * kk),
        (1, 1, 0, 0),
        (0, c, 1, -kk),
    )
    return alpha, beta


def check_purity():
    alpha, beta = concentrated_basis()
    T = {w: perm4(tuple(beta[i] if w[i] else alpha[i] for i in range(4))) for w in WORDS}
    pure = sp.expand(T[(1, 1, 1, 1)] + 2 * k * P)
    assert pure == 0, T[(1, 1, 1, 1)]
    for w, val in T.items():
        if w != (1, 1, 1, 1):
            assert sp.expand(val) == 0, (w, val)
    # marking invariance
    t = sp.symbols("t0:4")
    betat = tuple(tuple(beta[i][j] + t[i] * alpha[i][j] for j in range(4)) for i in range(4))
    Tt = {w: perm4(tuple(betat[i] if w[i] else alpha[i] for i in range(4))) for w in WORDS}
    for w in WORDS:
        assert sp.expand(Tt[w] - T[w]) == 0, w
    print("purity + marking invariance OK; T_1111 = -2*k*(b*e*c+b+e)")


def frame_system(q, kval=1):
    """Return (M, Arow, Brow) symbolic in t for distinguished coordinate q.

    Rows of the 14x8 mixed matrix are indexed by MIXED; columns by
    z=(x0..x3,y0..y3).  Entry = coefficient of the z-variable in the word
    coefficient of the extended tensor.
    """
    t = sp.symbols("t0:4")
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(sp.expand(beta[i][j] + t[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)

    def row_of(i, bit):
        return tuple((betat[i] if bit else alpha[i])[j] for j in common)

    def coeff(w, i):
        # coefficient of the extension variable of row i in word w
        others = tuple(row_of(j, w[j]) for j in range(4) if j != i)
        return perm3(others)

    def var_index(w, i):
        return i + (4 if w[i] else 0)

    M = sp.zeros(len(MIXED), 8)
    for ridx, w in enumerate(MIXED):
        for i in range(4):
            M[ridx, var_index(w, i)] += coeff(w, i)
    Arow = sp.zeros(1, 8)
    for i in range(4):
        Arow[0, var_index((0, 0, 0, 0), i)] += coeff((0, 0, 0, 0), i)
    Brow = sp.zeros(1, 8)
    for i in range(4):
        Brow[0, var_index((1, 1, 1, 1), i)] += coeff((1, 1, 1, 1), i)
    return M, Arow, Brow, t


def reconstruction_vector(q, tvals, kval=1):
    t = sp.symbols("t0:4")
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(beta[i][j] + t[i] * alpha[i][j] for j in range(4)) for i in range(4))
    sub = dict(zip(t, tvals))
    return sp.Matrix([alpha[i][q] for i in range(4)]
                     + [sp.expand(betat[i][q].subs(sub)) for i in range(4)])


def main():
    check_purity()
    # rational sample point, k=1 gauge
    sample = {b: 2, e: 3, m: 7, c: 11}
    tsample = {sp.Symbol(f"t{i}"): v for i, v in enumerate((5, -4, 9, sp.Rational(3, 7)))}
    print("\n== generic ranks at (b,e,m,c)=(2,3,7,11), k=1, random t ==")
    for q in range(4):
        M, Arow, Brow, t = frame_system(q, kval=1)
        Ms = M.subs(sample).subs(tsample)
        rank = Ms.rank()
        ns = Ms.nullspace()
        zrec = reconstruction_vector(q, tuple(tsample[sp.Symbol(f"t{i}")] for i in range(4)))
        zrec = zrec.subs(sample)
        Mzrec = (Ms * zrec).applyfunc(sp.expand)
        As = Arow.subs(sample).subs(tsample)
        Bs = Brow.subs(sample).subs(tsample)
        Azr = sp.expand((As * zrec)[0])
        Bzr = sp.expand((Bs * zrec)[0])
        genuine = []
        for v in ns:
            Av = sp.expand((As * v)[0])
            Bv = sp.expand((Bs * v)[0])
            genuine.append((Av, Bv))
        print(f" q={q}: mixed rank {rank}, kernel dim {len(ns)}, "
              f"M*zrec==0: {all(x == 0 for x in Mzrec)}, A(zrec)={Azr}, B(zrec)={Bzr}")
        for i, (Av, Bv) in enumerate(genuine):
            print(f"     kernel[{i}]: A={sp.nsimplify(Av)}, B={sp.nsimplify(Bv)}")
    # A-row t-freeness check
    print("\n== A row (word 0000) t-dependence ==")
    for q in range(4):
        M, Arow, Brow, t = frame_system(q, kval=1)
        dep = any(sp.expand(sp.diff(Arow[0, j], ti)) != 0 for j in range(8) for ti in t)
        print(f" q={q}: A depends on t: {dep};  A = {[sp.factor(Arow[0, j]) for j in range(8)]}")


if __name__ == "__main__":
    main()
