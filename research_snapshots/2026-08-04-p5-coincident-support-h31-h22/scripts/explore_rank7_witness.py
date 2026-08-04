#!/usr/bin/env python3
"""Rank-7 witnesses for q=2,3 and D_23; marking-forcing check.

Witness strategy: a nonzero 7x7 minor of M(t) at t=0 proves generic mixed
rank >= 7 over the function field (rank 8 impossible: z_rec universal).
Factor the minor -> informational divisor.  Also: forcing kappa_i=0 for
marked bases (kernel row must be proportional to alpha_i).
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


def h31_mixed(q, kval=1, tvals=None):
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    if tvals is not None:
        sub = dict(zip(T, tvals))
        betat = tuple(tuple(x.subs(sub) for x in row) for row in betat)
    common = tuple(j for j in range(4) if j != q)
    alph = tuple(tuple(alpha[i][j] for j in common) for i in range(4))
    bett = tuple(tuple(betat[i][j] for j in common) for i in range(4))
    M = sp.zeros(len(MIXED), 8)
    for ridx, wd in enumerate(MIXED):
        for i in range(4):
            others = tuple((bett[j] if wd[j] else alph[j]) for j in range(4) if j != i)
            M[ridx, i + (4 if wd[i] else 0)] += perm3(others)
    return M


def d23_mixed(kval=1, tvals=None):
    alpha, beta = concentrated_basis(kval)
    betat = tuple(tuple(sp.expand(beta[i][j] + T[i] * alpha[i][j]) for j in range(4))
                  for i in range(4))
    if tvals is not None:
        sub = dict(zip(T, tvals))
        betat = tuple(tuple(x.subs(sub) for x in row) for row in betat)

    def drow(row, ext):
        return (row[0], row[1], r * row[2] + row[3], ext)

    alpha_d = tuple(drow(alpha[i], Z[i]) for i in range(4))
    beta_d = tuple(drow(betat[i], Z[4 + i]) for i in range(4))
    words = {wd: perm4(tuple(beta_d[i] if wd[i] else alpha_d[i] for i in range(4)))
             for wd in WORDS}
    M = sp.Matrix([[sp.diff(words[wd], zz) for zz in Z] for wd in MIXED])
    return M


def find_minor(M, label):
    import itertools as it
    # find a 7x7 nonzero minor with small row/col sets, prefer t=0 matrix
    ncols = 8
    for cols in it.combinations(range(ncols), 7):
        sub = M[:, list(cols)]
        # quick numeric rank probe
        probe = sub.subs({b: 2, e: 3, m: 7, c: 11, r: sp.Rational(5, 3)})
        if probe.rank() < 7:
            continue
        for rows in it.combinations(range(M.rows), 7):
            pr = probe[list(rows), :]
            if pr.rank() == 7:
                det = sp.factor(sub[list(rows), :].det())
                if det != 0:
                    print(f"{label}: rows {rows} cols {cols}")
                    print(f"   det = {det}")
                    return rows, cols, det
    print(f"{label}: NO 7x7 minor found")
    return None


def marking_forcing():
    alpha, beta = concentrated_basis()
    ka = sp.symbols("ka0:4")  # kappa_i: alpha-coefficient... (beta-coefficient of K_i)
    nu = sp.symbols("nu0:4")
    si = sp.symbols("si0:4")
    ta = sp.symbols("ta0:4")
    K = tuple(tuple(si[i] * alpha[i][j] + ka[i] * beta[i][j] for j in range(4))
              for i in range(4))
    B = tuple(tuple(ta[i] * alpha[i][j] + nu[i] * beta[i][j] for j in range(4))
              for i in range(4))
    words = {wd: perm4(tuple(B[i] if wd[i] else K[i] for i in range(4))) for wd in WORDS}
    # near-words: exactly one zero bit
    for i in range(4):
        wd = tuple(0 if j == i else 1 for j in range(4))
        val = sp.expand(words[wd])
        expected = sp.expand(-2 * k * P * ka[i] * sp.prod(nu[j] for j in range(4) if j != i))
        assert sp.expand(val - expected) == 0, (i, val)
    val = sp.expand(words[(1, 1, 1, 1)])
    assert sp.expand(val + 2 * k * P * sp.prod(nu)) == 0
    print("marking forcing: T'_(1..0..1) = -2kP * kappa_i * prod_{j!=i} nu_j and "
          "T'_1111 = -2kP prod nu_j;")
    print("  => nonzero pure marked basis requires kappa_i = 0 for all i "
          "(kernel row proportional to alpha_i), nu_i != 0.")


def main():
    marking_forcing()
    for q in (2, 3):
        M0 = h31_mixed(q, kval=1, tvals=(0, 0, 0, 0))
        find_minor(M0, f"H31 q={q} t=0")
    M0 = d23_mixed(kval=1, tvals=(0, 0, 0, 0))
    find_minor(M0, "D23 t=0")


if __name__ == "__main__":
    main()
