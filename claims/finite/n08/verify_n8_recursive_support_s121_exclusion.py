"""Exact verifier: the 121-entry n=8 recursive-support-model pattern S121 is not
fibre-realizable (four-word rank-one grid identity, rule H3).

S121 is the SAT model of
`explore_general_block_recursive_support_model.py 8 --killers --anchors --plane-rigidity`
recorded in the S156 anchor note (branch claude/s156-trichotomy-20261009,
docs/strategy/s156-hub-trichotomy-2026-10-09.md, Section 5).  It is copied
verbatim below and cross-checked against
docs/strategy/s121-exclusion-2026-10-09.md, which records the findings.

Convention (as in the model script): W_ij[a,b] for i<j, a = colour at i,
b = colour at j; T_W(w) = sum over the 105 perfect matchings M of K_8 of
prod_{ij in M} W_ij[w_i, w_j].

Checked here, in exact integer polynomial arithmetic (sympy):

A. S121 satisfies the column-killer theorem and the diagonal-anchor lemma at
   every (v, c) (a census from the support alone), so neither excludes it.
B. With every entry outside S121 set to zero, the four mixed words
   E_ab = T(w_ab), w_ab = (a, 0, 0, 2, b, 1, 0, 1) (colour a at vertex 0,
   colour b at vertex 4; a in {0,1}, b in {1,2}) have Laplace expansions at
   the hub p = 0 with exactly the partners 2 and 3 at the three corners
   (0,1), (0,2), (1,1), and partners 2, 3, 5 at (1,2):
     t2(a,b) = W02[a,0] * P_b,  P_b = W13[02] W45[b1] W67[01]   (one monomial)
     t3(a,b) = W03[a,2] * Q_b,  Q_b = W12[00] W45[b1] W67[01] + W14[0b] W27[01] W56[10]
     t5      = W05[11] * Z,     Z   = W13[02] W24[02] W67[01]   (one monomial)
   and they satisfy the polynomial identity

     t2(0,1) t5 = t2(0,1) E_12 - E_02 E_11 + E_02 t3(1,1) + t3(0,2) E_11 - E_01 t3(1,2).

   At a GHZ witness all four words are mixed, so the right side is 0, while
   the left side is the product of the six support entries
   W02[00], W05[11], W13[02], W24[02], W45[11], W67[01] (W13[02] and W67[01]
   squared).  Hence no configuration supported within S121 with those six
   entries nonzero has matching tensor GHZ(8,3) up to the torus (any field;
   no division).  This is a Shape II instance of the rank-one grid transport
   H3 (hub 0, partners {2,3}, varied vertices 0 and 4), equivalently the
   (k,r,s) = (2,1,1) case of identity (2) of the multi-partner grid note.
C. A greedy reduction of the zero hypotheses on K_8 (as in the S128
   verifier): only some of the outside entries occurring in the four
   unrestricted word polynomials need to vanish for the identity.
D. (--census) The number of top-level H3 squares on S121 whose premises are
   structural (every other Laplace term at the hub has an entry outside S121
   or an identically zero complementary coefficient) and whose two conclusion
   factors are single monomials: 2285 such squares, at 7 (hub, partner-pair)
   classes.  Each one is an identity of the shape of B.
"""

from __future__ import annotations

import argparse
import itertools
import re
from functools import lru_cache
from pathlib import Path

import sympy as sp

S121 = ("01: ALL | 02: ALL | 03: ALL | 04: 00 10 20 | 05: 00 10 11 20 21 22 | 06: 11 | 07: 02 12 22 | "
        "12: ALL | 13: ALL | 14: ALL | 15: 00 10 20 | 16: 02 12 22 | 17: 11 | 23: 00 10 20 | "
        "24: 02 12 22 | 25: 22 | 26: 22 | 27: 01 11 21 | 34: 10 11 | 35: 11 | 36: 00 | "
        "37: 22 | 45: 00 01 02 10 11 12 21 22 | 46: 22 | 47: 00 10 20 | 56: ALL | 57: 00 | 67: ALL")
N = 8
C = 3
V = tuple(range(N))
SOURCE = Path(__file__).resolve().parents[3] / "docs" / "strategy" / "s121-exclusion-2026-10-09.md"


def parse(spec):
    sup = set()
    for part in spec.split("|"):
        k, vals = part.split(":")
        i, j = int(k.strip()[0]), int(k.strip()[1])
        items = [f"{a}{b}" for a in range(C) for b in range(C)] if vals.strip() == "ALL" else vals.split()
        sup |= {(i, j, int(e[0]), int(e[1])) for e in items}
    return sup


def key(v, u, x, y):
    """Entry with colour x at v and colour y at u, in the i<j convention."""
    return (v, u, x, y) if v < u else (u, v, y, x)


@lru_cache(maxsize=None)
def matchings(vs):
    if not vs:
        return ((),)
    out = []
    for k in range(1, len(vs)):
        for m in matchings(vs[1:k] + vs[k + 1:]):
            out.append(((vs[0], vs[k]),) + m)
    return tuple(out)


X = {(i, j, a, b): sp.Symbol(f"W{i}{j}_{a}{b}")
     for i, j in itertools.combinations(V, 2) for a in range(C) for b in range(C)}
assert len(matchings(V)) == 105


def T(A, w, zero):
    """T_A(w) as a sympy polynomial; w maps vertices to colours; entries in zero are 0."""
    tot = 0
    for M in matchings(tuple(A)):
        ks = [key(i, j, w[i], w[j]) for i, j in M]
        if any(k in zero for k in ks):
            continue
        tot += sp.Mul(*[X[k] for k in ks])
    return sp.expand(tot)


def word(a, b):
    return {0: a, 1: 0, 2: 0, 3: 2, 4: b, 5: 1, 6: 0, 7: 1}


def nterms(p):
    return len(sp.Add.make_args(p)) if p != 0 else 0


# ---------------------------------------------------------------- part A
def part_a(sup):
    def G(v, u, a, b):
        return key(v, u, a, b) in sup

    killers = {(v, c): [u for u in V if u != v
                        and any(G(v, u, a, c) for a in range(C))
                        and not any(G(v, u, a, d) for a in range(C) for d in range(C) if d != c)]
               for v in V for c in range(C)}
    anchors = {(v, c): [u for u in V if u != v and G(v, u, c, c)
                        and not any(G(v, u, c, d) for d in range(C) if d != c)]
               for v in V for c in range(C)}
    assert all(killers.values()), [t for t, us in killers.items() if not us]
    assert all(anchors.values()), [t for t, us in anchors.items() if not us]
    print("PASS A  S121 satisfies the column-killer theorem and the diagonal-anchor lemma at all 24 (v,c)")


# ---------------------------------------------------------------- part B
def laplace_terms(w, zero):
    """{k: (entry symbol, complementary coefficient)} at hub 0, nonzero terms only."""
    out = {}
    for k in V[1:]:
        e = key(0, k, w[0], w[k])
        if e in zero:
            continue
        B = [x for x in V if x not in (0, k)]
        H = T(B, w, zero)
        if H != 0:
            out[k] = (X[e], H)
    return out


def identity_residual(zero, t2, t3, t5):
    E = {(a, b): T(V, word(a, b), zero) for a in (0, 1) for b in (1, 2)}
    lhs = t2[(0, 1)] * t5
    rhs = (t2[(0, 1)] * E[(1, 2)] - E[(0, 2)] * E[(1, 1)] + E[(0, 2)] * t3[(1, 1)]
           + t3[(0, 2)] * E[(1, 1)] - E[(0, 1)] * t3[(1, 2)])
    return sp.expand(lhs - rhs), E


def part_b(sup):
    outside = set(X) - sup
    t2, t3 = {}, {}
    for a in (0, 1):
        for b in (1, 2):
            w = word(a, b)
            tm = laplace_terms(w, outside)
            expected = {2, 3, 5} if (a, b) == (1, 2) else {2, 3}
            assert set(tm) == expected, ((a, b), sorted(tm))
            assert len(set(w.values())) > 1
            t2[(a, b)] = sp.expand(tm[2][0] * tm[2][1])
            t3[(a, b)] = sp.expand(tm[3][0] * tm[3][1])
            if (a, b) == (1, 2):
                t5 = sp.expand(tm[5][0] * tm[5][1])
    P1 = X[(1, 3, 0, 2)] * X[(4, 5, 1, 1)] * X[(6, 7, 0, 1)]
    Z = X[(1, 3, 0, 2)] * X[(2, 4, 0, 2)] * X[(6, 7, 0, 1)]
    assert t2[(0, 1)] == X[(0, 2, 0, 0)] * P1
    assert t5 == X[(0, 5, 1, 1)] * Z
    res, E = identity_residual(outside, t2, t3, t5)
    for (a, b), poly in sorted(E.items()):
        print(f"        E{a}{b} = T({''.join(str(word(a, b)[v]) for v in V)}) has {nterms(poly)} monomials on S121")
    assert res == 0, "identity fails on S121"
    lhs = sp.factor(t2[(0, 1)] * t5)
    needed = [(0, 2, 0, 0), (0, 5, 1, 1), (1, 3, 0, 2), (2, 4, 0, 2), (4, 5, 1, 1), (6, 7, 0, 1)]
    assert all(k in sup for k in needed)
    assert set(lhs.free_symbols) == {X[k] for k in needed} and nterms(sp.expand(lhs)) == 1
    print(f"PASS B  t2(0,1)*t5 = {lhs} lies in the span of the four mixed words (exact on S121)")
    return t2, t3, t5, outside


# ---------------------------------------------------------------- part C
def part_c(t2, t3, t5, outside):
    relevant = set()
    for a in (0, 1):
        for b in (1, 2):
            w = word(a, b)
            for M in matchings(V):
                relevant |= {key(i, j, w[i], w[j]) for i, j in M}
    zero = sorted(outside & relevant)
    kept = list(zero)
    for k in zero:
        trial = set(kept) - {k}
        if identity_residual(trial, t2, t3, t5)[0] == 0:
            kept.remove(k)
    assert identity_residual(set(kept), t2, t3, t5)[0] == 0
    print(f"PASS C  reduced zero hypotheses: {len(kept)} of {len(zero)} relevant outside entries:")
    print("        " + " ".join(f"W{i}{j}[{a}{b}]" for i, j, a, b in kept))


# ---------------------------------------------------------------- part D
def part_d(sup):
    """Structural top-level H3 squares with monomial conclusion factors (pure Python)."""

    @lru_cache(maxsize=None)
    def mons(A, w):
        col = dict(zip(A, w))
        out = 0
        for M in matchings(A):
            if all(key(i, j, col[i], col[j]) in sup for i, j in M):
                out += 1
        return out

    def live(w, p):
        out = {}
        for k in V:
            if k == p or key(p, k, w[p], w[k]) not in sup:
                continue
            B = tuple(x for x in V if x not in (p, k))
            m = mons(B, tuple(w[x] for x in B))
            if m:
                out[k] = m
        return out

    squares, classes = 0, set()
    for p in V:
        for k1, k2 in itertools.combinations([x for x in V if x != p], 2):
            pairs = [(k1, k2)] + [tuple(sorted((p, v))) for v in V if v not in (p, k1, k2)]
            for u, v in pairs:
                others = [x for x in V if x not in (u, v)]
                for rc in itertools.product(range(C), repeat=len(others)):
                    lv = {}
                    for x in range(C):
                        for y in range(C):
                            w = [0] * N
                            for s, c in zip(others, rc):
                                w[s] = c
                            w[u], w[v] = x, y
                            lv[(x, y)] = (tuple(w), live(tuple(w), p))
                    E = {xy for xy, (w, L) in lv.items() if len(set(w)) > 1 and set(L) == {k1, k2}}
                    for (x, y), (x2, y2) in itertools.product(E, lv):
                        if x2 == x or y2 == y or (x, y2) not in E or (x2, y) not in E or (x2, y2) in E:
                            continue
                        w2, L2 = lv[(x2, y2)]
                        oth = [k for k in L2 if k not in (k1, k2)]
                        if not ({k1, k2} <= set(L2) and len(set(w2)) > 1 and len(oth) == 1 and L2[oth[0]] == 1):
                            continue
                        L = lv[(x, y)][1]
                        if L[k1] == 1 or L[k2] == 1:
                            squares += 1
                            classes.add((p, k1, k2))
    assert squares == 2285 and len(classes) == 7, (squares, sorted(classes))
    print(f"PASS D  {squares} structural top-level H3 squares with monomial conclusion, "
          f"(hub, partners) classes {sorted(classes)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--census", action="store_true", help="also run part D (about a minute)")
    args = ap.parse_args()
    sup = parse(S121)
    assert len(sup) == 121
    if SOURCE.exists():
        text = SOURCE.read_text(encoding="utf-8")
        start = text.index("01: ALL | 02: ALL")
        block = " | ".join(re.sub(r"\s+", " ", line.strip()) for line in text[start:].split("```")[0].strip().splitlines())
        assert parse(block) == sup, "S121 differs from the source note"
        print("PASS    S121 matches docs/strategy/s121-exclusion-2026-10-09.md")
    part_a(sup)
    t2, t3, t5, outside = part_b(sup)
    part_c(t2, t3, t5, outside)
    if args.census:
        part_d(sup)
    print("ALL PASS")


if __name__ == "__main__":
    main()
