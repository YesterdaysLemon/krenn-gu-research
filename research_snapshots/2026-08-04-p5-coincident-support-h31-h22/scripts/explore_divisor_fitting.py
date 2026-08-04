#!/usr/bin/env python3
"""Diagnostic + char-0 Fitting closures for the divisor sheets.

(1) Rational-point diagnostics: on each divisor sheet, compute the genuine
    kernel direction(s) and the ranks of all four one-marked maps, and find
    nonzero 4x4 minors.
(2) Char-0 certificates over the divisor function fields.
"""
from __future__ import annotations

import itertools
import subprocess
import time

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
WORDS3 = tuple(itertools.product((0, 1), repeat=3))
PERMS3 = tuple(itertools.permutations(range(3)))
PERMS4 = tuple(itertools.permutations(range(4)))

b, e, m, c = sp.symbols("b e m c")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")
Z = sp.symbols("x0:4") + sp.symbols("y0:4")
W = sp.Symbol("w")


def perm3(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(3)) for p in PERMS3))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[i][p[i]] for i in range(4)) for p in PERMS4))


def concentrated_basis(sub):
    alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1), (P, P * m - Q * c, -Q, Q))
    beta = ((0, 1, b, -b), (0, 1, e, -e), (1, 1, 0, 0), (0, c, 1, -1))
    alpha = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in alpha)
    beta = tuple(tuple(sp.expand(sp.sympify(x).subs(sub)) for x in row) for row in beta)
    return alpha, beta


def frame_data(q, sub, tvals):
    alpha, beta = concentrated_basis(sub)
    betat = tuple(tuple(sp.expand(beta[i][j] + tvals[i] * alpha[i][j]) for j in range(4))
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
    alpha_p = tuple(alph[i] + (Z[i],) for i in range(4))
    beta_p = tuple(bett[i] + (Z[4 + i],) for i in range(4))
    return forms, alpha_p, beta_p


def one_marked_map(mode, alpha_p, beta_p):
    rows = []
    for bits in WORDS3:
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta_p[other] if bits[bit_index] else alpha_p[other])
                bit_index += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(idx == coordinate) for idx in range(4))
            row.append(perm4(tuple(basis if other == mode else selected[other]
                                   for other in range(4))))
        rows.append(row)
    return sp.Matrix(rows)


def diagnostic(label, q, sub, tvals):
    forms, alpha_p, beta_p = frame_data(q, sub, tvals)
    M = sp.Matrix([[sp.diff(forms[wd], zz) for zz in Z] for wd in MIXED])
    A = sp.Matrix([[sp.diff(forms[(0, 0, 0, 0)], zz) for zz in Z]])
    B = sp.Matrix([[sp.diff(forms[(1, 1, 1, 1)], zz) for zz in Z]])
    ns = M.nullspace()
    print(f"{label}: mixed rank {M.rank()}, kernel dim {len(ns)}")
    genuine = None
    for v in ns:
        Av = sp.simplify((A * v)[0])
        Bv = sp.simplify((B * v)[0])
        print(f"   kernel dir: A={Av}, B={Bv}")
    # search a genuine combination
    lam = sp.symbols("lam0:%d" % len(ns))
    vec = sum((lam[i] * ns[i] for i in range(len(ns))), sp.zeros(8, 1))
    Aval = sp.expand((A * vec)[0])
    Bval = sp.expand((B * vec)[0])
    sol = None
    for probe in itertools.product((0, 1, 2, -1), repeat=len(ns)):
        subs = dict(zip(lam, probe))
        if Aval.subs(subs) != 0 and Bval.subs(subs) != 0:
            sol = vec.subs(subs)
            break
    if sol is None:
        print("   NO genuine direction found (binary already dead here)")
        return
    print(f"   genuine z: {list(sol.T)} with A={sp.simplify((A*sol)[0])}, B={sp.simplify((B*sol)[0])}")
    zsubs = dict(zip(Z, list(sol)))
    for mode in range(4):
        marked = one_marked_map(mode, alpha_p, beta_p)
        mk = marked.subs(zsubs)
        rank = mk.rank()
        nz = []
        if rank >= 4:
            for rows_ in itertools.combinations(range(8), 4):
                det = mk[list(rows_), :].det()
                if sp.simplify(det) != 0:
                    nz.append(rows_)
                if len(nz) >= 3:
                    break
        print(f"   mode-{mode} one-marked rank {rank}; sample nonzero minors {nz}")


def main():
    # {b+e=0} sheets at (b,m,c)=(4,3,7): t=(1,0,0,-1/32) and (0,1,0,-1/32)
    sub = {e: -b}
    point = {b: 4, m: 3, c: 7}
    subp = {kk: vv.subs(point) if hasattr(vv, "subs") else vv
            for kk, vv in sub.items()}
    subp.update(point)
    for t1val, name in ((0, "sheet t1=0"), (1, "sheet t1=1")):
        tvals = (1 - t1val, t1val, 0, sp.Rational(-1, 32))
        diagnostic(f"b+e=0 {name} q=2", 2, subp, tvals)
    # {c=0} at (b,e,m)=(2,5,3): sheets t3=t2=0, 100t0+16t1=9, 32t1^2-102t1+91=0
    t1r = sp.symbols("t1r")
    quad = 32 * t1r**2 - 102 * t1r + 91
    t1root = sp.RootOf(quad.subs(t1r, sp.Symbol("x")), 0)
    t0val = sp.Rational(9, 100) - sp.Rational(16, 100) * t1root
    subc = {b: 2, e: 5, m: 3, c: 0}
    diagnostic("c=0 sheet (RootOf) q=2", 2, subc, (t0val, t1root, 0, 0))


if __name__ == "__main__":
    main()
