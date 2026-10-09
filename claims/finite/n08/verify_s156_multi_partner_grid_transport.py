"""Exact checks for the multi-partner grid-rank transport and its (non-)firing on
the eight-vertex support patterns S156 and S128.

Findings: docs/strategy/multi-partner-grid-transport-2026-10-09.md.
Patterns: docs/strategy/hyperdeterminant-crossing-2026-10-09.md, Sections 3.4
(S156) and 4.2 (S128), copied verbatim below.

Convention (as in explore_general_block_recursive_support_model.py): W_ij[a,b]
for i<j, a = colour at i, b = colour at j; T_A(w) = sum over perfect matchings
of A of the product of the block entries.

Checked here (exact integer / rational arithmetic; sympy for part A):

A. Transport identity.  For vectors a_0..a_r, b_0..b_s in F^k (k = r+s), with
   E_ij = a_i . b_j, and every r-subset I of the k coordinates,
       p_I(a_1..a_r) * q_{I^c}(b_1..b_s) * E_00  lies in  ( E_ij : (i,j) != (0,0) ),
   p_I, q_{I^c} the maximal minors on the columns I and I^c.  Checked by
   solving for multilinear cofactors for (k,r) in {(2,1),(3,1),(3,2),(4,2)},
   all I; and the adjugate block that the general proof needs is checked to
   vanish at E' = 0 for every k <= 6.
B. S156 support facts: F (full blocks) is 4-regular, the other twelve blocks
   are single entries; for every pair {p,u}, F restricted to V-{p,u} has at
   least two perfect matchings (so every Laplace coefficient T_{V-{p,u}}(c),
   for every colouring c, is a nonzero polynomial on S156 with at least two
   monomials); the single entries at vertex 2 are W02[0,2], W24[2,1], W25[2,2].
C. Single-vertex form (hub-flattening matroid clause) at an explicit integer
   point W* on S156: for every hub p, row set A of colours at p, and colouring
   c of V-p with c != a^7 (a in A), the live coordinates L(c) form a cyclic set
   of the column matroid of the rows A.  Zero violations; every |L| >= 4.
D. Two-vertex form (grid transport clause): census of premise instances under
   the Laplace supports of W*; the support-level clause needs an r x r
   single-transversal minor of the hub rows and an s x s single-transversal
   minor of the coefficient block on complementary columns.  On S128 the
   clause fires (k = 2, the H3 instance of the S128 identity is found); on
   S156 every premise instance has k = 4 and the clause never fires.
"""

from __future__ import annotations

import itertools
import random
from fractions import Fraction

import sympy as sp

S156 = ("01: ALL | 02: 02 | 03: 00 | 04: 11 | 05: ALL | 06: ALL | 07: ALL | 12: ALL | 13: ALL | 14: ALL | "
        "15: 11 | 16: 22 | 17: 20 | 23: ALL | 24: 21 | 25: 22 | 26: ALL | 27: ALL | 34: ALL | 35: ALL | "
        "36: 02 | 37: 11 | 45: ALL | 46: 10 | 47: ALL | 56: ALL | 57: 00 | 67: ALL")
S128 = ("01: 00 01 02 10 11 20 21 22 | 02: 01 02 | 03: 00 | 04: 01 11 21 | 05: 00 01 10 11 12 20 21 | 06: 22 | 07: ALL | "
        "12: 21 | 13: 00 01 02 10 11 20 21 | 14: 00 | 15: ALL | 16: 12 | 17: ALL | 23: ALL | 24: 00 02 10 11 12 20 21 22 | "
        "25: 21 | 26: 00 01 02 | 27: 01 02 10 12 22 | 34: 21 | 35: 12 | 36: 00 01 02 11 12 20 21 22 | 37: 10 11 12 | "
        "45: 00 02 11 12 20 22 | 46: 00 01 02 10 12 20 21 22 | 47: 21 | 56: 00 01 02 12 20 21 | 57: 00 | "
        "67: 00 01 02 10 11 12 20 22")
N = 8
V = tuple(range(N))
C = 3


def parse(spec):
    sup = set()
    for part in spec.split("|"):
        key, vals = part.split(":")
        i, j = int(key.strip()[0]), int(key.strip()[1])
        items = [f"{a}{b}" for a in range(C) for b in range(C)] if vals.strip() == "ALL" else vals.split()
        sup |= {(i, j, int(e[0]), int(e[1])) for e in items}
    return sup


def matchings(vs):
    vs = tuple(vs)
    if not vs:
        yield ()
        return
    for k in range(1, len(vs)):
        for m in matchings(vs[1:k] + vs[k + 1:]):
            yield ((vs[0], vs[k]),) + m


def rank(rows):
    M = [[Fraction(x) for x in r] for r in rows]
    r = 0
    for c in range(len(M[0]) if M else 0):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


# ---------------------------------------------------------------- part A
def identity_in_ideal(k, r, I):
    s = k - r
    a = [[sp.Symbol(f"a{i}_{l}") for l in range(k)] for i in range(r + 1)]
    b = [[sp.Symbol(f"b{j}_{l}") for l in range(k)] for j in range(s + 1)]
    E = {(i, j): sum(a[i][l] * b[j][l] for l in range(k)) for i in range(r + 1) for j in range(s + 1)}
    Ic = [l for l in range(k) if l not in I]
    p = sp.Matrix([[a[i][l] for l in I] for i in range(1, r + 1)]).det()
    q = sp.Matrix([[b[j][l] for l in Ic] for j in range(1, s + 1)]).det()
    target = sp.expand(p * q * E[(0, 0)])
    unknowns, expr = [], 0
    for (i, j), e in E.items():
        if (i, j) == (0, 0):
            continue
        vecs = [a[t] for t in range(r + 1) if t != i] + [b[t] for t in range(s + 1) if t != j]
        for mono in itertools.product(*vecs):
            c = sp.Symbol(f"c{len(unknowns)}")
            unknowns.append(c)
            expr += c * sp.Mul(*mono) * e
    eqs = sp.Poly(sp.expand(expr - target), *[x for row in a + b for x in row]).coeffs()
    return sp.linsolve(eqs, unknowns) != sp.EmptySet


def adjugate_block_vanishes(k, r):
    """General proof step: N = [[E', A'_I], [B'_{I^c}^T, 0]] (rows a_1..a_r,
    e_{I^c}; columns b_1..b_s, e_I).  The block of adj(N) with row index in the
    e_I columns and column index in the e_{I^c} rows vanishes at E' = 0."""
    s = k - r
    e = sp.Matrix(r, s, lambda i, j: sp.Symbol(f"e{i}_{j}"))
    A = sp.Matrix(r, r, lambda i, j: sp.Symbol(f"x{i}_{j}"))
    B = sp.Matrix(s, s, lambda i, j: sp.Symbol(f"y{i}_{j}"))
    Nm = sp.zeros(k, k)
    Nm[:r, :s] = e
    Nm[:r, s:] = A
    Nm[r:, :s] = B.T
    adj = Nm.adjugate()
    blk = adj[s:, r:]          # rows: e_I columns of N; columns: e_{I^c} rows of N
    sub = {x: 0 for x in e}
    return all(sp.expand(z.subs(sub)) == 0 for z in blk)


def part_a():
    for k, r in [(2, 1), (3, 1), (3, 2), (4, 2)]:
        for I in itertools.combinations(range(k), r):
            assert identity_in_ideal(k, r, list(I)), (k, r, I)
    print("PASS A1 p_I q_{I^c} E00 in (other E_ij) for (k,r) = (2,1),(3,1),(3,2),(4,2), all I")
    for k in range(2, 7):
        for r in range(1, k):
            assert adjugate_block_vanishes(k, r), (k, r)
    print("PASS A2 adjugate block of [[E',A'],[B'^T,0]] vanishes at E'=0 for all 1 <= r < k <= 6")


# ---------------------------------------------------------------- helpers on patterns
class Pattern:
    def __init__(self, spec, seed=1):
        self.sup = parse(spec)
        rng = random.Random(seed)
        self.W = {key: rng.randint(1, 97) * rng.choice((1, -1)) for key in sorted(self.sup)}
        self.cache = {}

    def g(self, i, j, a, b):
        return ((i, j, a, b) in self.sup) if i < j else ((j, i, b, a) in self.sup)

    def w(self, i, j, a, b):
        return self.W.get((i, j, a, b), 0) if i < j else self.W.get((j, i, b, a), 0)

    def T(self, A, col):
        A = tuple(sorted(A))
        key = (A, tuple(col[x] for x in A))
        if key in self.cache:
            return self.cache[key]
        if not A:
            return 1
        p, tot = A[0], 0
        for u in A[1:]:
            x = self.w(p, u, col[p], col[u])
            if x:
                tot += x * self.T(tuple(z for z in A if z not in (p, u)), col)
        self.cache[key] = tot
        return tot


# ---------------------------------------------------------------- part B
def part_b(P):
    from collections import Counter
    cnt = Counter((i, j) for i, j, a, b in P.sup)
    assert len(P.sup) == 156
    F = {e for e, m in cnt.items() if m == 9}
    singles = {e for e, m in cnt.items() if m == 1}
    assert len(F) == 16 and len(singles) == 12 and len(F) + len(singles) == 28
    deg = Counter(x for e in F for x in e)
    assert all(deg[v] == 4 for v in V)
    npm = {}
    for p, u in itertools.combinations(V, 2):
        rest = [x for x in V if x not in (p, u)]
        npm[(p, u)] = sum(all(tuple(sorted(e)) in F for e in M) for M in matchings(rest))
    # >= 2 F-perfect matchings: every Laplace coefficient has >= 2 monomials at
    # every colouring, so no coefficient is a single (support-certified) monomial
    assert min(npm.values()) == 2, min(npm.values())
    # hub 2: the H-dead colourings C_gamma of V-2 form the box c0 != 0, c4 != 1,
    # c5 != 2 (eight colourings, none constant) for every gamma on F(2)
    h2 = sorted(((j if i == 2 else i), (a, b)) for (i, j, a, b) in P.sup if cnt[(i, j)] == 1 and 2 in (i, j))
    assert h2 == [(0, (0, 2)), (4, (2, 1)), (5, (2, 2))], h2
    # rows of vertex 2 at colours 0,1 and of vertex 4 at colours 0,2 meet only full blocks
    fonly = {p: [x for x in range(C) if all(not ((min(p, u), max(p, u)) in singles and
                                                 any(P.g(p, u, x, z) for z in range(C))) for u in V if u != p)]
             for p in V}
    assert fonly[2] == [0, 1] and fonly[4] == [0, 2]
    print("PASS B  S156: F 4-regular (16 full blocks), 12 single entries; every F[V-{p,u}] has "
          f">= {min(npm.values())} F-perfect matchings; hub-2 single entries W02[0,2], W24[2,1], W25[2,2]; "
          "F-only rows:", {p: r for p, r in fonly.items() if r})


# ---------------------------------------------------------------- part C
def part_c(P):
    viol, inst, minL = 0, 0, 99
    for p in V:
        others = [x for x in V if x != p]
        for c in itertools.product(range(C), repeat=7):
            col = dict(zip(others, c))
            phi = {u: P.T([x for x in others if x != u], col) for u in others}
            for r in range(1, 4):
                for A in itertools.combinations(range(C), r):
                    if any(all(z == a for z in c) for a in A):
                        continue
                    L = [[P.w(p, u, a, col[u]) for a in A] for u in others
                         if phi[u] != 0 and any(P.w(p, u, a, col[u]) for a in A)]
                    inst += 1
                    minL = min(minL, len(L))
                    if L:
                        rk = rank(L)
                        if any(rank(L[:i] + L[i + 1:]) != rk for i in range(len(L))):
                            viol += 1
    assert viol == 0
    print(f"PASS C  S156 hub-flattening matroid clause at W*: {inst} instances, 0 non-cyclic live sets, "
          f"min |L| = {minL}")
    return minL


# ---------------------------------------------------------------- part D
def unique_transversal(mask_rows):
    """mask_rows: square 0/1 matrix; True iff exactly one permutation is supported."""
    n = len(mask_rows)
    return sum(all(mask_rows[i][s[i]] for i in range(n)) for s in itertools.permutations(range(n))) == 1


def grid_census(P):
    """Premise instances of the grid transport clause (Shape II) with the
    Laplace supports of W*.  Returns {(r,s): (premises, fired)} and the fired
    instances."""
    from collections import defaultdict
    out = defaultdict(lambda: [0, 0])
    fired = []
    for p in V:
        for v in V:
            if v == p:
                continue
            R = [x for x in V if x not in (p, v)]
            for c in itertools.product(range(C), repeat=6):
                base = dict(zip(R, c))
                h = P.T(R, base)
                live, coef, const = {}, {}, set()
                for x in range(C):
                    for y in range(C):
                        col = dict(base)
                        col[p], col[v] = x, y
                        if len(set(col.values())) == 1:
                            const.add((x, y))
                        L = set()
                        for u in R:
                            t = P.T([z for z in V if z not in (p, u)], col)
                            coef[(u, y)] = t
                            if P.g(p, u, x, base[u]) and t:
                                L.add(u)
                        if P.g(p, v, x, y) and h:
                            L.add("v")
                        live[(x, y)] = L
                for x0, y0 in itertools.product(range(C), repeat=2):
                    xs = [x for x in range(C) if x != x0]
                    ys = [y for y in range(C) if y != y0]
                    for r in (1, 2):
                        for Xp in itertools.combinations(xs, r):
                            for s in (1, 2):
                                for Yp in itertools.combinations(ys, s):
                                    corners = [(x, y) for x in Xp + (x0,) for y in Yp + (y0,)]
                                    if any(cc in const for cc in corners):
                                        continue
                                    K = set().union(*(live[cc] for cc in corners if cc != (x0, y0)))
                                    if "v" in K or len(K) != r + s or len(live[(x0, y0)] - K) != 1:
                                        continue
                                    out[(r, s)][0] += 1
                                    Ks = sorted(K)
                                    ok = False
                                    for I in itertools.combinations(Ks, r):
                                        Ic = [u for u in Ks if u not in I]
                                        ma = [[P.g(p, u, x, base[u]) for u in I] for x in Xp]
                                        mb = [[coef[(u, y)] != 0 for u in Ic] for y in Yp]
                                        if unique_transversal(ma) and unique_transversal(mb):
                                            ok = True
                                            break
                                    if ok:
                                        out[(r, s)][1] += 1
                                        fired.append((p, v, c, x0, y0, Xp, Yp, tuple(Ks)))
    return dict(out), fired


def part_d(P156, P128):
    cen128, fired128 = grid_census(P128)
    # the S128 identity: hub 0, v = 2, colours 1,1,0,1,0,1 at 1,3,4,5,6,7, corner (0,1), K = {5,7}
    target = (0, 2, (1, 1, 0, 1, 0, 1), 0, 1, (1,), (0,), (5, 7))
    assert target in fired128, "S128 identity instance not found"
    print("PASS D1 S128 grid clause census (r,s): (premises, fired) =", sorted(cen128.items()),
          "; contains the S128 identity instance")
    cen156, fired156 = grid_census(P156)
    assert not fired156
    assert set(cen156) <= {(2, 2)}
    print("PASS D2 S156 grid clause census (r,s): (premises, fired) =", sorted(cen156.items()),
          "; every premise instance has k = 4 and none fires at the support level")
    return cen156


def main():
    part_a()
    P156, P128 = Pattern(S156), Pattern(S128)
    part_b(P156)
    part_c(P156)
    part_d(P156, P128)
    print("ALL PASS")


if __name__ == "__main__":
    main()
