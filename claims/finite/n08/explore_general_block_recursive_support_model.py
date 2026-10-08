"""Exploratory bounded SAT search: general-block recursive support model (GSM).

For a hypothetical ternary Krenn-Gu witness W on n vertices with ARBITRARY
3x3 blocks, abstract every sub-configuration to its zero pattern:

  g[i,j,a,b]   : W_ij[a,b] != 0                          (i<j; W_ji = W_ij^T)
  m[A,w]       : T_{W[A]}(w) != 0 for an even vertex set A and a word w on A,
                 where T_{W[A]} is the matching tensor of W restricted to A;
                 m[{i,j},(a,b)] is g[i,j,a,b] and m[{},()] is true.

Valid necessary conditions (exact Laplace expansion of T_{W[A]} at v in A):
  (L)  m[A,w] -> some u in A-v has g[vu,w_v,w_u] and m[A-vu, w|];
  (F') not m[A,w] -> for every v the number of such u is not one
       (a single nonzero term cannot cancel);
  (G)  m[V, c^n] for every colour c; not m[V, w] for every nonconstant w.
(F') with the base cases implies unique-supported-matching forcing.

Sound search-space reductions:
  * chain normalization along the constant word 0^n: V, V-{0,1}, V-{0,1,2,3},
    ... all have m true for the all-0 word with g[2i-2,2i-1,0,0] true
    (every model has such a chain; relabel);
  * lex-leader clauses on the g-vector for the chain-preserving symmetries
    (endpoint swaps inside chain edges; colour swap 1<->2).

Optional valid strengthening:
  --killers : the column-killer theorem (THREE_COLOUR_HYPERPLANE_ANNIHILATION):
              for every vertex v and colour c some block W_vu has only its
              column c nonzero (and nonzero).
Optional hypothesis to test (Parent C of the fibre-exact brief, negated):
  --noncoordinate-killer : some block with a single nonzero column c has a
              nonzero entry outside row c.

Optional valid strengthening (two-term "holonomy" relations; see
docs/strategy/holonomy-support-model-2026-10-08.md for statements and proofs).
A Laplace term of (A,w) at p is LIVE iff t[A,w,p,u] (entry and complementary
sub-coefficient both nonzero); a non-live term is exactly zero.
  --holonomy : both families below.
  (H2) signed K_{2,3} balance (Lemma A').  For hub data h = (p,c_p,q,c_q)
       let r_k = W_pk[c_p,c_k] / W_qk[c_q,c_k].  If not m[A,w], the live set
       at p is exactly {a,b}, the live set at q in (A-{p,a}) is exactly {b}
       and in (A-{p,b}) exactly {a}, then r_a = -r_b.  Encoded with sign
       variables sigma[h,(k,c_k)]: such an edge forces sigma_a != sigma_b,
       so every odd cycle of such edges is excluded.
  (H3) rank-one grid transport (Lemma B').  Fix (A,p,k1,k2) and varied
       vertices u<v with |{u,v} & {p,k_i}| = 1 for i = 1,2, and the colours
       of A-{u,v}.  CAN[x,y] (x at u, y at v) means the k1- and k2-terms at
       p are both nonzero and sum to zero.  Edges: not m and live set
       exactly {k1,k2} -> CAN.  Squares: CAN(x,y) CAN(x,y') CAN(x',y) ->
       CAN(x',y').  Consequence: CAN -> the k1,k2 terms are live, and the
       remaining live terms at p must be >= 1 if m, and != 1 if not m.
  --holonomy-top-only : instantiate (H2),(H3) only at A = V.
The holonomy clauses are added lazily (CEGAR): every added clause is an
instance of a valid rule, so UNSAT is sound; a SAT model is accepted only
after the independent checker verifies (L),(F'),(G) and the holonomy closure.
  --pattern P27|P41|P63 : fix the g-variables to a six-vertex survivor
       pattern of SIX_VERTEX_SUPPORT_SURVIVOR_PATTERNS_EXACT_REFUTATION.md
       (validation; use with --no-symmetry).

A SAT answer is re-checked by an independent brute-force checker.  An UNSAT
answer means no witness exists at this order (the model is implied by every
witness); this script records no proof trace, use --proof for a DIMACS file.

Usage: python explore_...py N [--killers] [--noncoordinate-killer]
       [--holonomy] [--holonomy-top-only] [--pattern NAME]
       [--no-symmetry] [--proof PREFIX] [--out PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical153

C = 3


class GSM:
    def __init__(self, n, *, symmetry=True, killers=False, noncoordinate_killer=False):
        self.n = n
        self.V = tuple(range(n))
        self.pool = IDPool()
        self.cnf = CNF()
        self.true = self.pool.id(("TRUE",))
        self.cnf.append([self.true])
        self.g = {}
        for i, j in itertools.combinations(self.V, 2):
            for a in range(C):
                for b in range(C):
                    self.g[(i, j, a, b)] = self.pool.id(("g", i, j, a, b))
        self.m = {}
        self.t = {}
        self.sets = []
        for k in range(4, n + 1, 2):
            for A in itertools.combinations(self.V, k):
                self.sets.append(A)
                for w in itertools.product(range(C), repeat=k):
                    self.m[(A, w)] = self.pool.id(("m", A, w))
        for A in self.sets:                         # increasing size
            self._laplace(A)
        self._ghz()
        if symmetry:
            self._symmetry()
        if killers:
            self._killers()
        if noncoordinate_killer:
            self._noncoordinate_killer()

    def gvar(self, v, u, a, b):
        """Support of the entry (colour a at v, colour b at u)."""
        if v < u:
            return self.g[(v, u, a, b)]
        return self.g[(u, v, b, a)]

    def mvar(self, A, w):
        if len(A) == 0:
            return self.true
        if len(A) == 2:
            return self.gvar(A[0], A[1], w[0], w[1])
        return self.m[(A, w)]

    def _laplace(self, A):
        cnf, pool = self.cnf, self.pool
        idx = {v: k for k, v in enumerate(A)}
        for w in itertools.product(range(C), repeat=len(A)):
            mA = self.m[(A, w)]
            for v in A:
                lits = []
                for u in A:
                    if u == v:
                        continue
                    B = tuple(x for x in A if x not in (v, u))
                    wB = tuple(w[idx[x]] for x in B)
                    tv = pool.id(("t", A, w, v, u))
                    self.t[(A, w, v, u)] = tv
                    lits.append(tv)
                    gv, mr = self.gvar(v, u, w[idx[v]], w[idx[u]]), self.mvar(B, wB)
                    cnf.append([-tv, gv])
                    cnf.append([-tv, mr])
                    cnf.append([tv, -gv, -mr])
                cnf.append([-mA] + lits)                                 # (L)
                for tv in lits:                                          # (F')
                    cnf.append([mA, -tv] + [o for o in lits if o != tv])

    def _ghz(self):
        Vt = self.V
        for w in itertools.product(range(C), repeat=self.n):
            if len(set(w)) == 1:
                self.cnf.append([self.mvar(Vt, w)])
            else:
                self.cnf.append([-self.mvar(Vt, w)])

    def _symmetry(self):
        n, cnf = self.n, self.cnf
        for k in range(1, n // 2 + 1):
            cnf.append([self.g[(2 * k - 2, 2 * k - 1, 0, 0)]])
            rest = tuple(range(2 * k, n))
            if len(rest) >= 4:
                cnf.append([self.m[(rest, (0,) * len(rest))]])
        order = sorted(self.g)

        def lex_leader(image, name):
            # 'name' must be unique per generator.  (The 2026-10-08 trunk-attempt
            # version keyed the chain variables by id(image); the loop-local
            # closures share an id after garbage collection, so the three swap
            # generators shared chain variables and the clauses over-constrained.)
            eq_prev = self.true
            for key in order:
                x, y = self.g[key], self.g[image(key)]
                if x == y:
                    continue
                cnf.append([-eq_prev, -x, y])
                eq = self.pool.id(("eq", name, key))
                cnf.append([-eq, eq_prev])
                cnf.append([-eq, -x, y])
                cnf.append([-eq, x, -y])
                cnf.append([eq, -eq_prev, -x, -y])
                cnf.append([eq, -eq_prev, x, y])
                eq_prev = eq

        for k in range(n // 2):
            a, b = 2 * k, 2 * k + 1

            def tau(key, a=a, b=b):
                i, j, x, y = key
                f = lambda z: b if z == a else a if z == b else z
                i2, j2 = f(i), f(j)
                if i2 < j2:
                    return (i2, j2, x, y)
                return (j2, i2, y, x)
            lex_leader(tau, ("swap", a, b))

        def sigma(key):
            i, j, x, y = key
            s = {0: 0, 1: 2, 2: 1}
            return (i, j, s[x], s[y])
        lex_leader(sigma, "colour12")

    def _killers(self):
        """Valid: for every (v,c) some block at v has exactly column c nonzero."""
        cnf, pool = self.cnf, self.pool
        for v in self.V:
            for c in range(C):
                lits = []
                for u in self.V:
                    if u == v:
                        continue
                    k = pool.id(("K", v, u, c))
                    lits.append(k)
                    for cp in range(C):
                        if cp == c:
                            continue
                        for a in range(C):
                            cnf.append([-k, -self.gvar(v, u, a, cp)])
                    cnf.append([-k] + [self.gvar(v, u, a, c) for a in range(C)])
                cnf.append(lits)

    def _noncoordinate_killer(self):
        """Hypothesis (negation of Parent C): some column-c-only block has a
        nonzero entry in a row a != c."""
        cnf, pool = self.cnf, self.pool
        lits = []
        for v in self.V:
            for u in self.V:
                if u == v:
                    continue
                for c in range(C):
                    for a in range(C):
                        if a == c:
                            continue
                        q = pool.id(("NCK", v, u, c, a))
                        lits.append(q)
                        cnf.append([-q, self.gvar(v, u, a, c)])
                        for cp in range(C):
                            if cp == c:
                                continue
                            for ap in range(C):
                                cnf.append([-q, -self.gvar(v, u, ap, cp)])
        cnf.append(lits)

    # ------------------------------------------------------------ holonomy
    def tlit(self, A, w, v, u):
        """Literal 'the Laplace term of (A,w) at v with partner u is live'."""
        if len(A) == 2:
            return self.gvar(v, u, w[A.index(v)], w[A.index(u)])
        return self.t[(A, w, v, u)]

    def exact_neg(self, A, w, p, S):
        """Clause literals falsified iff the live set at p is exactly S."""
        return [(-self.tlit(A, w, p, u) if u in S else self.tlit(A, w, p, u))
                for u in A if u != p]

    def holonomy_instances(self, val, top_only=False, rules=("H2", "H3")):
        """Instances of (H2) and (H3) whose base premises hold under val.

        val(lit) -> bool evaluates a literal in the current model.  Returns
        {key: [clauses]}; every clause is an instance of a valid rule, so it
        may be added whether or not the current model violates it."""
        out = {}
        families = {}
        sets = [self.V] if top_only else self.sets
        for A in sets:
            idx = {v: k for k, v in enumerate(A)}
            for w in itertools.product(range(C), repeat=len(A)):
                mA = self.mvar(A, w)
                if val(mA):
                    continue
                for p in A:
                    live = [u for u in A if u != p and val(self.tlit(A, w, p, u))]
                    if len(live) != 2:
                        continue
                    a, b = live
                    prem = [mA] + self.exact_neg(A, w, p, {a, b})
                    # (H2) signed K_{2,3} edge with hub pair {p, q}
                    Ba = tuple(x for x in A if x not in (p, a))
                    wa = tuple(w[idx[x]] for x in Ba)
                    Bb = tuple(x for x in A if x not in (p, b))
                    wb = tuple(w[idx[x]] for x in Bb)
                    for q in (A if "H2" in rules else ()):
                        if q in (p, a, b):
                            continue
                        la = [u for u in Ba if u != q and val(self.tlit(Ba, wa, q, u))]
                        lb = [u for u in Bb if u != q and val(self.tlit(Bb, wb, q, u))]
                        if la != [b] or lb != [a]:
                            continue
                        prem2 = (prem + self.exact_neg(Ba, wa, q, {b})
                                 + self.exact_neg(Bb, wb, q, {a}))
                        h1, h2 = (p, w[idx[p]]), (q, w[idx[q]])
                        h = (h1, h2) if h1 < h2 else (h2, h1)
                        sa = self.pool.id(("sig", h, a, w[idx[a]]))
                        sb = self.pool.id(("sig", h, b, w[idx[b]]))
                        out[("H2", A, w, p, q, a, b)] =[prem2 + [sa, sb], prem2 + [-sa, -sb]]
                    # (H3) rank-one grid edges
                    k1, k2 = min(a, b), max(a, b)
                    pairs = [(k1, k2)] + [tuple(sorted((p, v))) for v in A
                                           if v not in (p, k1, k2)]
                    for u, v in (pairs if "H3" in rules else ()):
                        rest = tuple(-1 if x in (u, v) else w[idx[x]] for x in A)
                        fam = (A, p, k1, k2, u, v, rest)
                        xy = (w[idx[u]], w[idx[v]])
                        families.setdefault(fam, set()).add(xy)
                        out[("E", fam, xy)] = [prem + [self.pool.id(("can", fam, xy))]]
        for fam, edges in families.items():
            A, p, k1, k2, u, v, rest = fam
            closure = grid_closure(edges)
            can = {xy: self.pool.id(("can", fam, xy)) for xy in closure}
            for (x, y) in closure:
                w = tuple(x if s == u else y if s == v else c for s, c in zip(A, rest))
                mA = self.mvar(A, w)
                cv = can[(x, y)]
                others = [self.tlit(A, w, p, o) for o in A if o not in (p, k1, k2)]
                cl = [[-cv, self.tlit(A, w, p, k1)], [-cv, self.tlit(A, w, p, k2)],
                      [-cv, -mA] + others]
                for o in others:
                    cl.append([-cv, mA, -o] + [z for z in others if z != o])
                out[("C", fam, (x, y))] = cl
            for (x, y) in closure:
                for (x2, y2) in closure:
                    if x2 != x and y2 != y and (x, y2) in closure and (x2, y) in closure:
                        out[("S", fam, x, y, x2, y2)] = [
                            [-can[(x, y)], -can[(x, y2)], -can[(x2, y)], can[(x2, y2)]]]
        return out

    def fix_pattern(self, sup):
        """Unit assumptions fixing every g-variable to a given support."""
        return [v if k in sup else -v for k, v in self.g.items()]


def grid_closure(edges):
    """Corners (x,y) whose row node x and column node y are connected in the
    bipartite graph with the given edges."""
    parent = {}

    def find(z):
        parent.setdefault(z, z)
        while parent[z] != z:
            parent[z] = parent[parent[z]]
            z = parent[z]
        return z

    for x, y in edges:
        parent[find(("x", x))] = find(("y", y))
    xs = {x for x, _ in edges}
    ys = {y for _, y in edges}
    return {(x, y) for x in xs for y in ys if find(("x", x)) == find(("y", y))}


PATTERNS = {   # verbatim from the six-vertex survivor refutation verifier (branch claude/n6-pattern-refutation-20261008)
    "P27": ("01: 00 20 | 02: 11 | 03: 00 20 | 04: 02 22 | 05: 00 02 20 22 | "
            "12: 00 02 | 13: 22 | 14: 11 | 15: 20 | 23: 00 20 | 24: 02 22 | "
            "25: 00 02 20 22 | 34: 20 | 35: 11 | 45: 00"),
    "P41": ("01: 00 02 10 11 12 20 21 22 | 02: 12 22 | 03: 01 11 21 | "
            "04: 02 10 11 20 21 | 05: 00 | 12: 02 22 | 13: 11 | "
            "14: 00 01 02 12 20 21 22 | 15: 00 10 20 | 23: 00 | 24: 22 | "
            "25: 11 | 34: 10 11 12 | 35: 22 | 45: 00 10"),
    "P63": ("01: ALL | 02: 02 | 03: 00 | 04: 11 | 05: ALL | 12: ALL | "
            "13: 20 | 14: 01 | 15: 12 | 23: ALL | 24: 21 | 25: 22 | "
            "34: ALL | 35: 01 | 45: ALL"),
}


def parse_pattern(spec):
    sup = set()
    for part in spec.split("|"):
        key, vals = part.split(":")
        i, j = int(key.strip()[0]), int(key.strip()[1])
        items = ([f"{a}{b}" for a in range(C) for b in range(C)]
                 if vals.strip() == "ALL" else vals.split())
        for e in items:
            sup.add((i, j, int(e[0]), int(e[1])))
    return sup


def check_holonomy(n, gsup, msup, top_only=False, rules=("H2", "H3"), stats=None):
    """Independent re-check of (H2) and (H3) on a decoded model, from the
    supports alone (no SAT variables): builds every signed K_{2,3} graph and
    every rank-one grid, and checks bipartiteness and the consequences."""
    V = tuple(range(n))

    def G(v, u, a, b):
        return ((v, u, a, b) in gsup) if v < u else ((u, v, b, a) in gsup)

    def M(A, w):
        if len(A) == 0:
            return True
        if len(A) == 2:
            return G(A[0], A[1], w[0], w[1])
        return (A, w) in msup

    def live_at(A, w, p):
        """Partners u of p whose Laplace term in (A,w) is live."""
        col = dict(zip(A, w))
        res = []
        for u in A:
            if u == p:
                continue
            B = tuple(x for x in A if x not in (p, u))
            if G(p, u, col[p], col[u]) and M(B, tuple(col[x] for x in B)):
                res.append(u)
        return res

    k23 = {}           # hub data -> list of edges between (k, colour) nodes
    grids = {}         # (A, p, {k1,k2}, u, v, rest) -> set of corners
    sets = [V] if top_only else [A for k in range(4, n + 1, 2)
                                 for A in itertools.combinations(V, k)]
    for A in sets:
        for w in itertools.product(range(C), repeat=len(A)):
            if M(A, w):
                continue
            col = dict(zip(A, w))
            for p in A:
                lv = live_at(A, w, p)
                if len(lv) != 2:
                    continue
                a, b = lv
                for q in (A if "H2" in rules else ()):
                    if q in (p, a, b):
                        continue
                    Ba = tuple(x for x in A if x not in (p, a))
                    Bb = tuple(x for x in A if x not in (p, b))
                    if (live_at(Ba, tuple(col[x] for x in Ba), q) == [b]
                            and live_at(Bb, tuple(col[x] for x in Bb), q) == [a]):
                        hub = frozenset([(p, col[p]), (q, col[q])])
                        k23.setdefault(hub, []).append(((a, col[a]), (b, col[b])))
                for u in (A if "H3" in rules else ()):
                    for v in A:
                        if u < v and all(len({u, v} & {p, k}) == 1 for k in (a, b)):
                            rest = tuple(sorted((x, col[x]) for x in A if x not in (u, v)))
                            key = (A, p, frozenset((a, b)), u, v, rest)
                            grids.setdefault(key, set()).add((col[u], col[v]))
    if stats is not None:
        stats["H2_edges"] = sum(len(e) for e in k23.values())
        stats["H3_grid_edges"] = sum(len(c) for c in grids.values())
        stats["H3_transported"] = 0
    bad = []
    for hub, edges in k23.items():
        adj = {}
        for s, t in edges:
            adj.setdefault(s, []).append(t)
            adj.setdefault(t, []).append(s)
        side = {}
        for s0 in adj:
            if s0 in side:
                continue
            side[s0] = 0
            stack = [s0]
            while stack:
                s = stack.pop()
                for t in adj[s]:
                    if t not in side:
                        side[t] = 1 - side[s]
                        stack.append(t)
                    elif side[t] == side[s]:
                        bad.append(("H2 odd cycle", tuple(sorted(hub)), s, t))
    for (A, p, ks, u, v, rest), corners in grids.items():
        # connectivity by repeated square completion (a different route from
        # the union-find used by the encoder)
        cl = set(corners)
        grew = True
        while grew:
            grew = False
            for (x, y) in list(cl):
                for (x2, y2) in list(cl):
                    if x2 != x and y2 != y and (x, y2) in cl and (x2, y) not in cl:
                        cl.add((x2, y))
                        grew = True
        if stats is not None:
            stats["H3_transported"] += len(cl) - len(corners)
        for (x, y) in cl:
            col = dict(rest)
            col[u], col[v] = x, y
            w = tuple(col[s] for s in A)
            lv = live_at(A, w, p)
            oth = [o for o in lv if o not in ks]
            if not ks <= set(lv):
                bad.append(("H3 dead cancelling term", A, p, tuple(sorted(ks)), w))
            elif M(A, w) and not oth:
                bad.append(("H3 nonzero coefficient with cancelling terms only", A, p, w))
            elif not M(A, w) and len(oth) == 1:
                bad.append(("H3 single surviving term", A, p, w, oth[0]))
    return bad


def check_model(n, gsup, msup):
    """Independent brute-force check of (L), (F'), (G) on a decoded model.
    gsup: set of (i,j,a,b) with i<j; msup: set of (A,w) with |A|>=4."""
    V = tuple(range(n))

    def G(v, u, a, b):
        return ((v, u, a, b) in gsup) if v < u else ((u, v, b, a) in gsup)

    def M(A, w):
        if len(A) == 0:
            return True
        if len(A) == 2:
            return G(A[0], A[1], w[0], w[1])
        return (A, w) in msup

    bad = []
    for k in range(4, n + 1, 2):
        for A in itertools.combinations(V, k):
            idx = {v: i for i, v in enumerate(A)}
            for w in itertools.product(range(C), repeat=k):
                for v in A:
                    kids = 0
                    for u in A:
                        if u == v:
                            continue
                        B = tuple(x for x in A if x not in (v, u))
                        wB = tuple(w[idx[x]] for x in B)
                        if G(v, u, w[idx[v]], w[idx[u]]) and M(B, wB):
                            kids += 1
                    if M(A, w) and kids == 0:
                        bad.append(("L", A, w, v))
                    if not M(A, w) and kids == 1:
                        bad.append(("F'", A, w, v))
    for w in itertools.product(range(C), repeat=n):
        if (len(set(w)) == 1) != M(V, w):
            bad.append(("G", w))
    return bad


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--killers", action="store_true")
    ap.add_argument("--noncoordinate-killer", action="store_true")
    ap.add_argument("--holonomy", action="store_true")
    ap.add_argument("--holonomy-top-only", action="store_true")
    ap.add_argument("--holonomy-rules", default="H2,H3",
                    help="comma list from H2,H3 (default both)")
    ap.add_argument("--pattern", choices=sorted(PATTERNS))
    ap.add_argument("--max-entries", type=int)
    ap.add_argument("--no-symmetry", action="store_true")
    ap.add_argument("--proof", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    enc = GSM(args.n, symmetry=not args.no_symmetry, killers=args.killers,
              noncoordinate_killer=args.noncoordinate_killer)
    rec = {"n": args.n, "killers": args.killers, "noncoordinate_killer": args.noncoordinate_killer,
           "symmetry": not args.no_symmetry, "variables": enc.pool.top, "clauses": len(enc.cnf.clauses),
           "encode_seconds": round(time.time() - t0, 1), "solver": "CaDiCaL 1.5.3 via python-sat"}
    if args.proof:
        args.proof.parent.mkdir(parents=True, exist_ok=True)
        p = args.proof.with_suffix(".cnf")
        enc.cnf.to_file(str(p))
        rec["dimacs_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
    assume = []
    if args.pattern:
        sup = parse_pattern(PATTERNS[args.pattern])
        assume = enc.fix_pattern(sup)
        rec["pattern"] = args.pattern
        rec["pattern_entries"] = len(sup)
    if args.max_entries is not None:
        card = CardEnc.atmost(list(enc.g.values()), bound=args.max_entries,
                              top_id=enc.pool.top, encoding=EncType.seqcounter)
        enc.pool.occupy(enc.pool.top + 1, card.nv)
        enc.cnf.extend(card.clauses)
        rec["max_entries"] = args.max_entries
    rec["holonomy"] = args.holonomy or args.holonomy_top_only
    rules = tuple(r for r in args.holonomy_rules.split(",") if r)
    assert set(rules) <= {"H2", "H3"}, rules
    if rec["holonomy"]:
        rec["holonomy_rules"] = list(rules)
    rec["holonomy_scope"] = ("top" if args.holonomy_top_only else "all levels") if rec["holonomy"] else None
    print(json.dumps(rec), flush=True)
    t1 = time.time()
    added = {}
    rounds = 0
    with Cadical153(bootstrap_with=enc.cnf.clauses) as solver:
        while True:
            sat = solver.solve(assumptions=assume)
            model = solver.get_model() if sat else None
            rounds += 1
            if not sat or not rec["holonomy"]:
                break
            pos = {l for l in model if l > 0}
            gsup = {k for k, v in enc.g.items() if v in pos}
            msup = {k for k, v in enc.m.items() if v in pos}
            hbad = check_holonomy(args.n, gsup, msup, args.holonomy_top_only, rules)
            if not hbad:
                break
            val = (lambda lit: (lit in pos) if lit > 0 else (-lit not in pos))
            inst = enc.holonomy_instances(val, args.holonomy_top_only, rules)
            new = {k: cl for k, cl in inst.items() if k not in added}
            if not new:
                raise RuntimeError("checker reports a violation but no new instance; encoder bug")
            for k, cl in new.items():
                added[k] = cl
                for c in cl:
                    solver.add_clause(c)
            print(json.dumps({"round": rounds, "violations": len(hbad),
                              "first_violation": str(hbad[0])[:160],
                              "new_instances": len(new), "total_instances": len(added),
                              "seconds": round(time.time() - t1, 1)}), flush=True)
    rec["result"] = "SAT" if sat else "UNSAT"
    rec["solve_seconds"] = round(time.time() - t1, 1)
    if rec["holonomy"]:
        rec["cegar_rounds"] = rounds
        rec["holonomy_instances_added"] = len(added)
        rec["holonomy_clauses_added"] = sum(len(c) for c in added.values())
        kinds = {}
        for k in added:
            kinds[k[0]] = kinds.get(k[0], 0) + 1
        rec["holonomy_instances_by_rule"] = kinds
    if args.proof and not sat:
        p = args.proof.with_suffix(".final.cnf")
        final = CNF(from_clauses=enc.cnf.clauses + [c for cl in added.values() for c in cl]
                    + [[l] for l in assume])
        final.to_file(str(p))
        rec["final_dimacs"] = str(p)
        rec["final_dimacs_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
    if sat:
        pos = {l for l in model if l > 0}
        gsup = {k for k, v in enc.g.items() if v in pos}
        msup = {k for k, v in enc.m.items() if v in pos}
        bad = check_model(args.n, gsup, msup)
        if rec["holonomy"]:
            bad += check_holonomy(args.n, gsup, msup, args.holonomy_top_only, rules)
        rec["independent_check"] = "PASS" if not bad else "FAIL"
        rec["independent_check_violations"] = [str(b) for b in bad[:10]]
        blocks = {}
        for (i, j, a, b) in sorted(gsup):
            blocks.setdefault(f"{i}{j}", []).append(f"{a}{b}")
        rec["model_blocks"] = blocks
        rec["model_nonzero_entries"] = len(gsup)
    print(json.dumps({k: v for k, v in rec.items() if k != "model_blocks"}), flush=True)
    if sat:
        print(json.dumps(rec["model_blocks"]))
    if args.out:
        args.out.write_text(json.dumps(rec, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
