#!/usr/bin/env python3
"""Test parameter-divisor hypotheses for H31 q=2,3 survivor markings, mod 13/17.

Hypotheses from the p=11 hit at (b,e,m,c)=(2,3,7,5): bm-e=0 or be+c=0 (both
vanish mod 11 there).  Census all t in F_p^4 on each hypothesis divisor and on
a control point, count genuine survivors.  Also run the FULL parameter-space
elimination over small fields in Singular to extract the modular divisor.
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


def word_polys(q):
    alpha, beta = concentrated_basis()
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    out = {}
    for wd in WORDS:
        entry = []
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            entry.append(perm3(others))
        out[wd] = entry
    return out


def census(q, p, sample):
    rows = word_polys(q)
    subs = {b: sample[0], e: sample[1], m: sample[2], c: sample[3]}
    ml = {}
    for wd, entry in rows.items():
        lst = []
        for expr in entry:
            poly = sp.Poly(sp.expand(expr.subs(subs)), *T)
            d = {}
            for monom, coeff in poly.terms():
                S = tuple(i for i, ex in enumerate(monom) if ex)
                d[S] = int(coeff) % p
            lst.append(d)
        ml[wd] = lst

    def eval_entry(d, t):
        s = 0
        for S, co in d.items():
            v = co
            for i in S:
                v = (v * t[i]) % p
            s = (s + v) % p
        return s

    def zvar(wd, i):
        return i + (4 if wd[i] else 0)

    def rank_kernel(Mat):
        rows_ = [r[:] for r in Mat]
        piv = []
        rr = 0
        for col in range(8):
            sel = None
            for i in range(rr, len(rows_)):
                if rows_[i][col] % p:
                    sel = i
                    break
            if sel is None:
                continue
            rows_[rr], rows_[sel] = rows_[sel], rows_[rr]
            inv = pow(rows_[rr][col], p - 2, p)
            rows_[rr] = [(x * inv) % p for x in rows_[rr]]
            for i in range(len(rows_)):
                if i != rr and rows_[i][col] % p:
                    f = rows_[i][col]
                    rows_[i] = [(x - f * y) % p for x, y in zip(rows_[i], rows_[rr])]
            piv.append(col)
            rr += 1
        free = [ccc for ccc in range(8) if ccc not in piv]
        kern = []
        for fc in free:
            vec = [0] * 8
            vec[fc] = 1
            for ri, pc in enumerate(piv):
                vec[pc] = (-rows_[ri][fc]) % p
            kern.append(vec)
        return rr, kern

    genuine = []
    for t in itertools.product(range(p), repeat=4):
        Mat = []
        for wd in MIXED:
            row = [0] * 8
            for i in range(4):
                row[zvar(wd, i)] = (row[zvar(wd, i)] + eval_entry(ml[wd][i], t)) % p
            Mat.append(row)
        rr, kern = rank_kernel(Mat)
        if not kern:
            continue
        Arow = [0] * 8
        Brow = [0] * 8
        for i in range(4):
            Arow[zvar((0, 0, 0, 0), i)] = (Arow[zvar((0, 0, 0, 0), i)]
                                           + eval_entry(ml[(0, 0, 0, 0)][i], t)) % p
            Brow[zvar((1, 1, 1, 1), i)] = (Brow[zvar((1, 1, 1, 1), i)]
                                           + eval_entry(ml[(1, 1, 1, 1)][i], t)) % p
        found = False
        if len(kern) <= 3:
            for coeffs in itertools.product(range(p), repeat=len(kern)):
                if all(x == 0 for x in coeffs):
                    continue
                fi = next(i for i, x in enumerate(coeffs) if x)
                if coeffs[fi] != 1:
                    continue
                z = [0] * 8
                for co, vec in zip(coeffs, kern):
                    for j in range(8):
                        z[j] = (z[j] + co * vec[j]) % p
                Az = sum(a * x for a, x in zip(Arow, z)) % p
                Bz = sum(a * x for a, x in zip(Brow, z)) % p
                if Az and Bz:
                    found = True
                    break
        if found:
            genuine.append(t)
    return genuine


def modular_param_elimination(q, char):
    """Eliminate z,w,t over F_char -> ideal in (b,e,m,c)."""
    rows = word_polys(q)
    eqs = []
    for wd in MIXED:
        expr = sum(rows[wd][i] * Z[i + (4 if wd[i] else 0)] for i in range(4))
        eqs.append(sp.expand(expr))
    eqs.append(sp.expand(sum(rows[(0, 0, 0, 0)][i] * Z[i] for i in range(4)) - 1))
    eqs.append(sp.expand(
        W * sum(rows[(1, 1, 1, 1)][i] * Z[4 + i] for i in range(4)) - 1))

    def sing(expr):
        return str(expr).replace("**", "^")

    variables = list(map(str, Z + (W,) + T)) + ["b", "e", "m", "c"]
    program = "\n".join((
        f"ring R={char},(" + ",".join(variables) + "),(dp(13),dp(4));",
        "ideal I=" + ",".join(sing(x) for x in eqs) + ";",
        "ideal J=std(I);",
        "ideal K=eliminate(J," + "*".join(map(str, Z + (W,) + T)) + ");",
        "K=std(K);",
        '"PARAMLOCUS";', "K;",
        "LIB \"primdec.lib\";",
        "list pr=minAssGTZ(K);",
        '"MINPRIMES";', "pr;",
        "quit;",
    ))
    t0 = time.time()
    try:
        cp = subprocess.run(["Singular", "-q"], input=program, text=True,
                            capture_output=True, timeout=540)
    except subprocess.TimeoutExpired:
        print(f"  modular param elimination q={q} char={char}: TIMEOUT")
        return
    print(f"  modular param elimination q={q} char={char} ({time.time()-t0:.1f}s):")
    print("   ", "\n    ".join(cp.stdout.splitlines()))


def main():
    p = 13
    cases = [
        ("bm=e divisor", (2, 6, 3, 5)),
        ("be+c=0 divisor", (2, 3, 7, -6 % 13)),
        ("control", (2, 3, 7, 5)),
    ]
    for q in (2, 3):
        for label, samp in cases:
            gen = census(q, p, samp)
            print(f"q={q} p={p} {label} {samp}: genuine survivor markings = {len(gen)}"
                  + (f"  e.g. {gen[:6]}" if gen else ""))
    for q in (2, 3):
        modular_param_elimination(q, 101)


if __name__ == "__main__":
    main()
