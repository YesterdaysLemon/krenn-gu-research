#!/usr/bin/env python3
"""Exact replay for the cut-tensor (bipartite slice) rigidity attempt.

Owner: docs/strategy/cut-tensor-rigidity-attempt-2026-10-09.md.  The proofs
are the hand arguments there; this script replays the displayed identities and
the finite facts they use.  It is a primary verifier only (no independent
audit).

Setting: P, Q disjoint, |P| = |Q| = k, blocks B_pq in F^{3x3}.  For a word a
on P u Q, A_a[p, q] = B_pq[a_p, a_q] and T(a) = per(A_a).  With vector
variables x_p, y_q, M(x, y)[p, q] = x_p^T B_pq y_q.

Checks:

[1] Word/polynomial equivalence: per(M(x, y)) = sum_a mono(a) per(A_a)
    (symbolic at k = 2; all 729 coefficients on random integer blocks at k = 3).
[2] Contraction rank bound (Lemma C) at k = 2: with x_p = delta, x_p2 = u,
    the bilinear form F(delta; y_q, y_q') has det = 0 identically (symbolic).
[3] Contraction rank bound at k = 3: with delta orthogonal to B_pq'' w, the
    3x3 coefficient matrix of F is a sum of two rank-one matrices (exact, on
    random rational blocks), i.e. rank <= 2; the right-hand side
    diag(u2_c u3_c w_c delta_c) has rank 3 when all vectors are full.
[4] Full vector in a non-coordinate hyperplane (explicit formulas, symbolic).
[5] Single-entry endgame at k = 3: three pairwise edge-disjoint perfect
    matchings of K_{3,3} cover all nine edges (exhaustive over S_3^3); for
    every resulting Latin square and nonzero symbolic weights, a mixed word has
    T(a) equal to a single nonzero monomial.
[6] Restricted-word countermodel: the n = 4 matrix-unit witness, cut
    P = {0, 1}, Q = {2, 3}.  T_W = Delta on all 81 words; on the 80 words
    where the inside matching W01 W23 vanishes, T_W = per(A_a); the constant
    word 0000 is the only excluded word and per(A_0000) = 0.

Run:
    python claims/finite/n06/verify_bipartite_cut_tensor_rigidity_small_cuts.py
"""
from __future__ import annotations

import itertools
import random
import sys

import sympy as sp

FAILS: list[str] = []


def check(cond: bool, label: str) -> None:
    print(("  PASS  " if cond else "  FAIL  ") + label)
    if not cond:
        FAILS.append(label)


def per(rows):
    k = len(rows)
    return sp.Add(*[sp.Mul(*[rows[i][s[i]] for i in range(k)])
                    for s in itertools.permutations(range(k))])


def sym_blocks(k, name="b"):
    return {(p, q): sp.Matrix(3, 3, lambda a, b: sp.Symbol(f"{name}{p}{q}_{a}{b}"))
            for p in range(k) for q in range(k)}


def rand_blocks(k, rng, lo=-4, hi=4):
    return {(p, q): sp.Matrix(3, 3, lambda a, b: sp.Rational(rng.randint(lo, hi)))
            for p in range(k) for q in range(k)}


def vec(name):
    return sp.Matrix(3, 1, lambda i, j: sp.Symbol(f"{name}{i}"))


def word_value(B, k, word):
    P, Q = word[:k], word[k:]
    return per([[B[(p, q)][P[p], Q[q]] for q in range(k)] for p in range(k)])


# ---------------------------------------------------------------------------
print("[1] word / polynomial equivalence")
for k, symbolic in ((2, True), (3, False)):
    rng = random.Random(11 + k)
    B = sym_blocks(k) if symbolic else rand_blocks(k, rng)
    xs = [vec(f"x{p}_") for p in range(k)]
    ys = [vec(f"y{q}_") for q in range(k)]
    M = [[(xs[p].T * B[(p, q)] * ys[q])[0, 0] for q in range(k)] for p in range(k)]
    poly = sp.Poly(sp.expand(per(M)), *[v for x in xs + ys for v in x])
    ok = True
    for word in itertools.product(range(3), repeat=2 * k):
        mono = [0] * (6 * k)
        for v, c in enumerate(word):
            mono[3 * v + c] = 1
        if sp.expand(poly.coeff_monomial(tuple(mono)) - word_value(B, k, word)) != 0:
            ok = False
            break
    check(ok, f"k = {k}: coefficient of every word monomial equals per(A_a) "
              f"({'symbolic' if symbolic else 'random integer blocks'})")

# ---------------------------------------------------------------------------
print("[2] Lemma C at k = 2 (symbolic)")
B = sym_blocks(2)
d, u, y, z = vec("d"), vec("u"), vec("y"), vec("z")
# P = {0 (open, delta), 1 (closed, u)}, Q = {0 (y), 1 (z)} both open
F = ((d.T * B[(0, 0)] * y)[0, 0] * (u.T * B[(1, 1)] * z)[0, 0]
     + (d.T * B[(0, 1)] * z)[0, 0] * (u.T * B[(1, 0)] * y)[0, 0])
C = sp.Matrix(3, 3, lambda i, j: sp.expand(F).coeff(y[i]).coeff(z[j]))
check(sp.expand(C.det()) == 0,
      "coefficient matrix of F(delta; y, z) has determinant 0 identically")
rhs = sp.diag(*[u[c] * d[c] for c in range(3)])
check(sp.expand(rhs.det() - sp.Mul(*[u[c] * d[c] for c in range(3)])) == 0,
      "contracted target diag(u_c delta_c) has determinant prod u_c delta_c")

# ---------------------------------------------------------------------------
print("[3] Lemma C at k = 3 (exact, random rational blocks)")
rng = random.Random(2026)
ok_rank, ok_split, trials = True, True, 25
for _ in range(trials):
    Bk = rand_blocks(3, rng)
    u2 = sp.Matrix([rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(3)])
    u3 = sp.Matrix([rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(3)])
    w = sp.Matrix([rng.choice([-3, -2, -1, 1, 2, 3]) for _ in range(3)])
    v = Bk[(0, 2)] * w                       # p = 0, q'' = 2 closed
    zt = sp.Matrix([rng.randint(-5, 5) for _ in range(3)])
    delta = v.cross(zt)                      # delta . v = 0
    xs = [delta, u2, u3]
    # open q = 0 (y), q' = 1 (z); closed q'' = 2 (w)
    M = [[None] * 3 for _ in range(3)]
    for p in range(3):
        M[p][0] = (xs[p].T * Bk[(p, 0)] * y)[0, 0]
        M[p][1] = (xs[p].T * Bk[(p, 1)] * z)[0, 0]
        M[p][2] = (xs[p].T * Bk[(p, 2)] * w)[0, 0]
    Fk = sp.expand(per(M))
    Ck = sp.Matrix(3, 3, lambda i, j: Fk.coeff(y[i]).coeff(z[j]))
    ok_rank &= Ck.rank() <= 2
    # explicit two-term split: sigma(0) = 0 and sigma(0) = 1
    r1 = sp.Matrix(3, 1, lambda i, j: (delta.T * Bk[(0, 0)])[0, i])
    l1 = sp.Matrix(3, 1, lambda i, j: ((u2.T * Bk[(1, 1)])[0, i] * (u3.T * Bk[(2, 2)] * w)[0, 0]
                                        + (u3.T * Bk[(2, 1)])[0, i] * (u2.T * Bk[(1, 2)] * w)[0, 0]))
    r2 = sp.Matrix(3, 1, lambda i, j: (delta.T * Bk[(0, 1)])[0, i])
    l2 = sp.Matrix(3, 1, lambda i, j: ((u2.T * Bk[(1, 0)])[0, i] * (u3.T * Bk[(2, 2)] * w)[0, 0]
                                        + (u3.T * Bk[(2, 0)])[0, i] * (u2.T * Bk[(1, 2)] * w)[0, 0]))
    ok_split &= (Ck - r1 * l1.T - l2 * r2.T) == sp.zeros(3, 3)
check(ok_rank, f"{trials} instances: coefficient matrix of F has rank <= 2")
check(ok_split, f"{trials} instances: F = (delta B_pq y) l(z) + (delta B_pq' z) l'(y) exactly")

# ---------------------------------------------------------------------------
print("[4] full vectors in non-coordinate hyperplanes")
v1, v2, v3, t = sp.symbols("v1 v2 v3 t")
full = sp.Matrix([1 / v1, t / v2, -(1 + t) / v3])
check(sp.simplify(full.dot(sp.Matrix([v1, v2, v3]))) == 0,
      "v full: (1/v1, t/v2, -(1+t)/v3) is orthogonal to v and full for t not in {0, -1}")
two = sp.Matrix([1 / v1, -1 / v2, 1])
check(sp.simplify(two.dot(sp.Matrix([v1, v2, 0]))) == 0,
      "v3 = 0, v1 v2 != 0: (1/v1, -1/v2, 1) is a full vector orthogonal to v")

# ---------------------------------------------------------------------------
print("[5] single-entry endgame at k = 3")
perms = list(itertools.permutations(range(3)))


def edges(s):
    return {(p, s[p]) for p in range(3)}


triples = [(a, b, c) for a in perms for b in perms for c in perms
           if not (edges(a) & edges(b)) and not (edges(a) & edges(c)) and not (edges(b) & edges(c))]
check(all(len(edges(a) | edges(b) | edges(c)) == 9 for a, b, c in triples) and len(triples) > 0,
      f"{len(triples)} ordered triples of pairwise edge-disjoint perfect matchings; each covers all 9 edges")
ok_end = True
for s0, s1, s2 in triples:
    L = {}
    for c, s in enumerate((s0, s1, s2)):
        for e in edges(s):
            L[e] = c
    beta = {e: sp.Symbol(f"beta{e[0]}{e[1]}") for e in L}
    Bk = {e: beta[e] * sp.Matrix(3, 3, lambda a, b: 1 if (a, b) == (L[e], L[e]) else 0) for e in L}
    for sg in perms:
        if sg in (s0, s1, s2):
            continue
        word = [L[(p, sg[p])] for p in range(3)] + [None] * 3
        for p in range(3):
            word[3 + sg[p]] = L[(p, sg[p])]
        mixed = len(set(word)) > 1
        val = sp.expand(word_value(Bk, 3, word))
        ok_end &= mixed and val == sp.Mul(*[beta[(p, sg[p])] for p in range(3)])
check(ok_end, "for every Latin square and every non-class permutation sigma, the word of sigma "
              "is mixed and T = prod beta (one nonzero monomial)")

# ---------------------------------------------------------------------------
print("[6] restricted-word countermodel (n = 4 matrix-unit witness)")


def E(c):
    return sp.Matrix(3, 3, lambda a, b: 1 if (a, b) == (c, c) else 0)


Wn4 = {(0, 1): E(0), (2, 3): E(0), (0, 2): E(1), (1, 3): E(1), (0, 3): E(2), (1, 2): E(2)}


def Wget(i, j, a, b):
    return Wn4[(i, j)][a, b] if (i, j) in Wn4 else Wn4[(j, i)][b, a]


ok_T, ok_slice, omega, excluded = True, True, 0, []
for wd in itertools.product(range(3), repeat=4):
    T = sum(Wget(*m[0], wd[m[0][0]], wd[m[0][1]]) * Wget(*m[1], wd[m[1][0]], wd[m[1][1]])
            for m in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))))
    ok_T &= T == (1 if len(set(wd)) == 1 else 0)
    inside = Wget(0, 1, wd[0], wd[1]) * Wget(2, 3, wd[2], wd[3])
    perA = (Wget(0, 2, wd[0], wd[2]) * Wget(1, 3, wd[1], wd[3])
            + Wget(0, 3, wd[0], wd[3]) * Wget(1, 2, wd[1], wd[2]))
    if inside == 0:
        omega += 1
        ok_slice &= perA == (1 if len(set(wd)) == 1 else 0)
    else:
        excluded.append((wd, perA))
check(ok_T, "T_W = Delta on all 81 words")
check(omega == 80 and ok_slice,
      "on the 80 words with W01 W23 = 0, per(A_a) = [a constant] (both constant words 1111, 2222 included)")
check(excluded == [((0, 0, 0, 0), 0)], "the only excluded word is 0000, and per(A_0000) = 0")

print()
if FAILS:
    print(f"FAILED: {len(FAILS)} check(s)")
    sys.exit(1)
print("ALL CHECKS PASSED")
