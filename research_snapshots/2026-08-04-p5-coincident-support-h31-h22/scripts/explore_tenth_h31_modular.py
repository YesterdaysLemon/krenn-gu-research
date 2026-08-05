#!/usr/bin/env python3
"""Modular census of H31 marking loci for the tenth component (q=2,3).

Also: symbolic proof (full params incl. k) that the q=0,1 A-rows vanish
identically, and precomputation of M(t) as multilinear t-expansion for fast
finite-field evaluation.
"""
from __future__ import annotations

import itertools
import sys

import sympy as sp

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))
PERMS3 = tuple(itertools.permutations(range(3)))

b, e, k, m, c = sp.symbols("b e k m c")
P = b * e * c + b + e
Q = b * e * (m + 1)
T = sp.symbols("t0:4")


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


def frame_rows(q, kval=None):
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    return alph, bett


def word_rows(q, kval=None):
    """entries[w][i] = coefficient of extension var of row i in word w."""
    alph, bett = frame_rows(q, kval)
    out = {}
    for w in WORDS:
        entry = []
        for i in range(4):
            others = tuple((bett[j] if w[j] else alph[j]) for j in range(4) if j != i)
            entry.append(perm3(others))
        out[w] = entry
    return out


def zvar(w, i):
    return i + (4 if w[i] else 0)


def a_row_identities():
    for q in (0, 1):
        rows = word_rows(q, kval=None)  # symbolic k
        assert all(sp.expand(x) == 0 for x in rows[(0, 0, 0, 0)]), (q, rows[(0, 0, 0, 0)])
    print("IDENTITY: for q in {0,1}, the 0000-diagonal row A vanishes identically"
          " (all params, k symbolic, all markings t).")
    for q in (2, 3):
        rows = word_rows(q, kval=None)
        a = [sp.factor(x) for x in rows[(0, 0, 0, 0)]]
        assert all(sp.expand(sp.diff(x, ti)) == 0 for x in a for ti in T)
        print(f" q={q}: A (t-free) = {a}")


def multilinear_expansion(rows_dict):
    """Return {w: [ {S: coeff} for i in 0..3 ]} with S subset of t-indices."""
    out = {}
    for w, entry in rows_dict.items():
        lst = []
        for expr in entry:
            poly = sp.Poly(sp.expand(expr), *T)
            d = {}
            for monom, coeff in poly.terms():
                S = tuple(i for i, ex in enumerate(monom) if ex)
                assert all(ex <= 1 for ex in monom), (w, monom)
                d[S] = coeff
            lst.append(d)
        out[w] = lst
    return out


def census(q, p, sample, max_report=40):
    """All markings t in F_p^4: mixed rank, kernel, genuine directions."""
    rows = word_rows(q, kval=1)
    subs = {b: sample[0], e: sample[1], m: sample[2], c: sample[3]}
    ml = {}
    for w, entry in rows.items():
        lst = []
        for expr in entry:
            poly = sp.Poly(sp.expand(expr.subs(subs)), *T)
            d = {}
            for monom, coeff in poly.terms():
                S = tuple(i for i, ex in enumerate(monom) if ex)
                d[S] = int(coeff) % p
            lst.append(d)
        ml[w] = lst

    def eval_entry(d, t):
        s = 0
        for S, co in d.items():
            v = co
            for i in S:
                v = (v * t[i]) % p
            s = (s + v) % p
        return s

    def build(t, wlist):
        Mat = []
        for w in wlist:
            row = [0] * 8
            for i in range(4):
                row[zvar(w, i)] = (row[zvar(w, i)] + eval_entry(ml[w][i], t)) % p
            Mat.append(row)
        return Mat

    def rank_and_kernel(Mat):
        # Gaussian elimination mod p; returns rank and kernel basis
        rows_ = [r[:] for r in Mat]
        ncols = 8
        piv = []
        r = 0
        for col in range(ncols):
            sel = None
            for i in range(r, len(rows_)):
                if rows_[i][col] % p:
                    sel = i
                    break
            if sel is None:
                continue
            rows_[r], rows_[sel] = rows_[sel], rows_[r]
            inv = pow(rows_[r][col], p - 2, p)
            rows_[r] = [(x * inv) % p for x in rows_[r]]
            for i in range(len(rows_)):
                if i != r and rows_[i][col] % p:
                    f = rows_[i][col]
                    rows_[i] = [(x - f * y) % p for x, y in zip(rows_[i], rows_[r])]
            piv.append(col)
            r += 1
            if r == len(rows_):
                break
        free = [ccc for ccc in range(ncols) if ccc not in piv]
        kernel = []
        for fc in free:
            vec = [0] * ncols
            vec[fc] = 1
            for ri, pc in enumerate(piv):
                vec[pc] = (-rows_[ri][fc]) % p
            kernel.append(vec)
        return r, kernel

    results = {}
    count_kernel_ge2 = 0
    genuine_markings = []
    for t in itertools.product(range(p), repeat=4):
        Mat = build(t, MIXED)
        r, kern = rank_and_kernel(Mat)
        if r <= 6:
            count_kernel_ge2 += 1
        # genuine: some kernel z with A z != 0 and B z != 0
        Arow_ = [0] * 8
        for i in range(4):
            Arow_[zvar((0, 0, 0, 0), i)] = (Arow_[zvar((0, 0, 0, 0), i)]
                                            + eval_entry(ml[(0, 0, 0, 0)][i], t)) % p
        Brow_ = [0] * 8
        for i in range(4):
            Brow_[zvar((1, 1, 1, 1), i)] = (Brow_[zvar((1, 1, 1, 1), i)]
                                            + eval_entry(ml[(1, 1, 1, 1)][i], t)) % p
        # scan projective kernel for genuine directions
        found = False
        if kern:
            dimk = len(kern)
            # projective scan only if small
            if dimk <= 3:
                for coeffs in itertools.product(range(p), repeat=dimk):
                    if all(x == 0 for x in coeffs):
                        continue
                    # normalize first nonzero to 1
                    fi = next(i for i, x in enumerate(coeffs) if x)
                    if coeffs[fi] != 1:
                        continue
                    z = [0] * 8
                    for co, vec in zip(coeffs, kern):
                        for j in range(8):
                            z[j] = (z[j] + co * vec[j]) % p
                    Az = sum(a * x for a, x in zip(Arow_, z)) % p
                    Bz = sum(a * x for a, x in zip(Brow_, z)) % p
                    if Az and Bz:
                        found = True
                        break
        if found:
            genuine_markings.append((t, r))
    print(f" q={q} p={p} sample(b,e,m,c)={sample}: markings with rank<=6: "
          f"{count_kernel_ge2}; genuine survivor markings: {len(genuine_markings)}")
    for t, r in genuine_markings[:max_report]:
        print(f"    t={t} rank={r}")
    return genuine_markings


def main():
    a_row_identities()
    for p, sample in ((11, (2, 3, 7, 5)), (13, (2, 3, 7, 5))):
        for q in (2, 3):
            census(q, p, sample)


if __name__ == "__main__":
    main()
