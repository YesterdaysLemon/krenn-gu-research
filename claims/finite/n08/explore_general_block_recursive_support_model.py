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
  --anchors : the diagonal-anchor lemma (docs/research-notes.md, "Diagonal-
              anchor refinement"): for every vertex v and colour c some block
              W_vu has row c supported exactly on colour c at u.  Added
              2026-10-09 after S128 and S156 (both found without it) turned
              out to violate it; docs/strategy/s156-hub-trichotomy-2026-10-09.md.
  --within-pattern-file P : g = 0 outside the fixture P, g free inside it
              (sub-patterns of a survivor; use with --no-symmetry).
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

Optional valid strengthening (plane rigidity of the cut permanent; statement
and soundness proof in docs/strategy/hyperdeterminant-crossing-2026-10-09.md,
Section 3, resting on PERMANENT_PLANE_RESTRICTION_HYPERDETERMINANT_THEOREM.md):
  --plane-rigidity : (PR) at every level |A| >= 6.  Inner triple T in A,
       R = A - T coloured c, columns C in R, two colours per inner vertex.
       If m[R-C,c], every other summand of the T-expansion of the 8 cube
       words has a false g/m factor, and each inner vertex has a provably
       single-monomial 2x2 minor l_t[a_t] (rows at its two colours, columns
       C) with the a_t not all equal, then some m[A, cube word] is true.
  --plane-mode value|deg3 : 'value' uses plane rigidity (Theorem 3 of the
       bilinear-grid document); 'deg3' only patterns with an explicit
       degree-3 certificate (two-equal minors, or a permutation pattern with
       an identically zero same-parity partner).
  --plane-top-only : only A = V.   --pattern-file : fix g from a fixture.
  --max-rounds K : stop the lazy loop after K rounds (result INCONCLUSIVE).
Lazy clauses of every family are added CEGAR-style; a SAT model is accepted
only after check_model, check_holonomy and check_plane pass.

Performance flags (engineering only; they change no rule, no instance and no
clause order, so a run is the same run, only faster):
  --fast-plane : the PR violation search uses a numpy prefilter over every
       (A, T, c, pairs, Cc) for the support conditions check_plane tests
       before the minors; survivors go through the unchanged _plane_clause.
       The result is check_plane's violation list and plane_instances'
       instance dictionary, in the same order (replaces both in the loop).
  --fast-holonomy : the holonomy gate is check_holonomy_fast (numpy live
       tables from the supports; same violation list as check_holonomy);
       holonomy_instances takes its premises from a numpy scan of the
       model's t literals (same premises, same order) and does not rebuild
       clauses for keys already added (same new instances, same variable
       allocation order).
  --fast : both.   --cross-check-fast : also run the reference scans every
       round and stop on any difference (validation; slower than either).
  The final acceptance of a SAT model always uses the reference checkers.
  Validation (2026-10-09): n = 6 --killers --holonomy --plane-rigidity --fast
  --proof reproduces the final DIMACS SHA-256 2b15ae81... of Section 3a of
  docs/strategy/hyperdeterminant-crossing-2026-10-09.md exactly.

A SAT answer is re-checked by an independent brute-force checker.  An UNSAT
answer means no witness exists at this order (the model is implied by every
witness); this script records no proof trace, use --proof for a DIMACS file.

Usage: python explore_...py N [--killers] [--noncoordinate-killer]
       [--holonomy] [--holonomy-top-only] [--pattern NAME]
       [--no-symmetry] [--proof PREFIX] [--out PATH] [--fast [--cross-check-fast]]
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


def word_type(w):
    """Colour-class sizes of a word, descending, joined by '+' (e.g. '4+2')."""
    return "+".join(str(k) for k in sorted((w.count(c) for c in set(w)), reverse=True))


class GSM:
    g_drop_types = frozenset()

    def __init__(self, n, *, symmetry=True, killers=False, noncoordinate_killer=False,
                 g_drop_types=()):
        self.n = n
        self.g_drop_types = frozenset(g_drop_types)
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

    def _laplace(self, A, hubs=None):
        """(L) and (F') for every word of A at every hub in A (default), or
        only at the given hubs (used by --g-minus for the decoration sets)."""
        cnf, pool = self.cnf, self.pool
        idx = {v: k for k, v in enumerate(A)}
        for w in itertools.product(range(C), repeat=len(A)):
            mA = self.m[(A, w)]
            for v in (A if hubs is None else hubs):
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
        for w in itertools.product(range(C), repeat=len(Vt)):
            if len(set(w)) == 1:
                self.cnf.append([self.mvar(Vt, w)])
            elif word_type(w) not in self.g_drop_types:
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

    def anchors(self):
        """Valid: diagonal-anchor lemma (docs/research-notes.md, 'Diagonal-anchor
        refinement'; exact identity in verify_s156_diagonal_anchor_exclusion.py).
        For every (v,c) some block W_vu has row c (colour c at v) supported
        exactly on colour c at u: W_vu[c,c] != 0 and W_vu[c,d] = 0 for d != c."""
        cnf, pool = self.cnf, self.pool
        for v in self.V:
            for c in range(C):
                lits = []
                for u in self.V:
                    if u == v:
                        continue
                    k = pool.id(("ANC", v, u, c))
                    lits.append(k)
                    cnf.append([-k, self.gvar(v, u, c, c)])
                    for d in range(C):
                        if d != c:
                            cnf.append([-k, -self.gvar(v, u, c, d)])
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

    def _holonomy_premises(self, val, sets, rules):
        """Reference scan for holonomy_instances: in the order (A, w, p), every
        (A, w) with m false and a vertex p whose live set is exactly {a, b},
        with the hubs q (in A order) for which the (H2) premises hold.
        Yields (A, idx, w, mA, p, a, b, Ba, wa, Bb, wb, qs)."""
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
                    Ba = tuple(x for x in A if x not in (p, a))
                    wa = tuple(w[idx[x]] for x in Ba)
                    Bb = tuple(x for x in A if x not in (p, b))
                    wb = tuple(w[idx[x]] for x in Bb)
                    qs = []
                    for q in (A if "H2" in rules else ()):
                        if q in (p, a, b):
                            continue
                        la = [u for u in Ba if u != q and val(self.tlit(Ba, wa, q, u))]
                        lb = [u for u in Bb if u != q and val(self.tlit(Bb, wb, q, u))]
                        if la == [b] and lb == [a]:
                            qs.append(q)
                    yield A, idx, w, mA, p, a, b, Ba, wa, Bb, wb, qs

    def holonomy_instances(self, val, top_only=False, rules=("H2", "H3"), skip=None,
                           premises=None):
        """Instances of (H2) and (H3) whose base premises hold under val.

        val(lit) -> bool evaluates a literal in the current model.  Returns
        {key: [clauses]}; every clause is an instance of a valid rule, so it
        may be added whether or not the current model violates it.

        skip (optional, --fast-holonomy): a container of keys already added.
        Their clauses are not rebuilt and they are omitted from the result;
        every other key, its clauses, the result order and the order in which
        new sig/can variables are allocated are unchanged (a skipped key's
        variables were allocated when it was first built, and the per-family
        can dictionary is still built for every closure corner).  So
        {k: v for k, v in result if k not in skip} is the same with or
        without skip.

        premises (optional, --fast-holonomy): an iterable replacing the
        reference scan _holonomy_premises (same tuples, same order), e.g.
        holonomy_premises_fast."""
        out = {}
        families = {}
        sets = [self.V] if top_only else self.sets
        if skip is None:
            skip = ()
        if premises is None:
            premises = self._holonomy_premises(val, sets, rules)
        for A, idx, w, mA, p, a, b, Ba, wa, Bb, wb, qs in premises:
            prem = None
            # (H2) signed K_{2,3} edge with hub pair {p, q}
            for q in qs:
                key = ("H2", A, w, p, q, a, b)
                if key in skip:
                    continue
                if prem is None:
                    prem = [mA] + self.exact_neg(A, w, p, {a, b})
                prem2 = (prem + self.exact_neg(Ba, wa, q, {b})
                         + self.exact_neg(Bb, wb, q, {a}))
                h1, h2 = (p, w[idx[p]]), (q, w[idx[q]])
                h = (h1, h2) if h1 < h2 else (h2, h1)
                sa = self.pool.id(("sig", h, a, w[idx[a]]))
                sb = self.pool.id(("sig", h, b, w[idx[b]]))
                out[key] = [prem2 + [sa, sb], prem2 + [-sa, -sb]]
            # (H3) rank-one grid edges
            k1, k2 = min(a, b), max(a, b)
            pairs = [(k1, k2)] + [tuple(sorted((p, v))) for v in A
                                   if v not in (p, k1, k2)]
            for u, v in (pairs if "H3" in rules else ()):
                rest = tuple(-1 if x in (u, v) else w[idx[x]] for x in A)
                fam = (A, p, k1, k2, u, v, rest)
                xy = (w[idx[u]], w[idx[v]])
                families.setdefault(fam, set()).add(xy)
                key = ("E", fam, xy)
                if key in skip:
                    continue
                if prem is None:
                    prem = [mA] + self.exact_neg(A, w, p, {a, b})
                out[key] = [prem + [self.pool.id(("can", fam, xy))]]
        for fam, edges in families.items():
            A, p, k1, k2, u, v, rest = fam
            closure = grid_closure(edges)
            can = {xy: self.pool.id(("can", fam, xy)) for xy in closure}
            for (x, y) in closure:
                if ("C", fam, (x, y)) in skip:
                    continue
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
                        if ("S", fam, x, y, x2, y2) in skip:
                            continue
                        out[("S", fam, x, y, x2, y2)] = [
                            [-can[(x, y)], -can[(x, y2)], -can[(x2, y)], can[(x2, y2)]]]
        return out

    # ------------------------------------------------------- plane rigidity
    def plane_instances(self, val, top_only=False, mode="value"):
        """Violated instances of the plane-rigidity rule (PR) under val.

        Statement and soundness proof: docs/strategy/hyperdeterminant-crossing-
        2026-10-09.md, Section 3.  Fix an even A (|A| >= 6), an inner triple
        T = (t0,t1,t2) in A, R = A - T, a colouring c of R, three columns
        C in R, and two colours (alpha_t, alpha'_t) at each inner vertex.
        Premises (all model literals):
          * h: m[R-C, c] (T_{R-C}(c) != 0; true when R = C);
          * every other summand of the T-expansion of each of the 8 cube
            words has a zero factor (a false g or m literal);
          * for each t a column index a_t such that the 2x2 minor l_t[a_t] of
            the rows r_{t,alpha_t}|C, r_{t,alpha'_t}|C is a single nonzero
            monomial (exactly one of its two products supported), with the
            a_t not all equal (mode 'value'), or forming a degree-3
            certificate pattern (mode 'deg3').
        Conclusion: some m[A, w] of the 8 cube words is true.
        Returns {key: [clause]} for the instances violated by val."""
        out = {}
        sets = [self.V] if top_only else [A for A in self.sets if len(A) >= 6]
        for A in sets:
            idx = {v: k for k, v in enumerate(A)}
            for T in itertools.combinations(A, 3):
                R = tuple(x for x in A if x not in T)
                for c in itertools.product(range(C), repeat=len(R)):
                    col = dict(zip(R, c))
                    zero = {}
                    for al in itertools.product(range(C), repeat=3):
                        w = [0] * len(A)
                        for x in R:
                            w[idx[x]] = col[x]
                        for t, a in zip(T, al):
                            w[idx[t]] = a
                        w = tuple(w)
                        zero[al] = (w, self.mvar(A, w))
                    for pairs in itertools.product(PAIRS, repeat=3):
                        cube = list(itertools.product(*pairs))
                        if any(val(zero[al][1]) for al in cube):
                            continue
                        for Cc in itertools.combinations(R, 3):
                            cl = self._plane_clause(A, T, R, col, Cc, pairs, cube, zero, val, mode)
                            if cl is not None:
                                out[("PR", len(A), tuple(sorted(cl)))] = [cl]
        return out

    def _plane_clause(self, A, T, R, col, Cc, pairs, cube, zero, val, mode):
        RC = tuple(x for x in R if x not in Cc)
        h = self.mvar(RC, tuple(col[x] for x in RC))
        if not val(h):
            return None
        neg = []                       # literals, each false in the model
        # minors: provable single-monomial minors per inner vertex
        known = []
        for t, (al, al2) in zip(T, pairs):
            y = [self.gvar(t, u, al, col[u]) for u in Cc]
            y2 = [self.gvar(t, u, al2, col[u]) for u in Cc]
            kt = {}
            for a in range(3):
                b, d = (a + 1) % 3, (a + 2) % 3
                for (p, q), (r, s) in (((y[b], y2[d]), (y[d], y2[b])), ((y[d], y2[b]), (y[b], y2[d]))):
                    if val(p) and val(q) and not (val(r) and val(s)):
                        kt[a] = [-p, -q, r if not val(r) else s]
                        break
            known.append(kt)
        choice = _plane_choice(known, mode, self._zero_minor_lits(T, Cc, col, pairs, val) if mode == "deg3" else None)
        if choice is None:
            return None
        cl, extra = choice
        neg.extend(cl)
        neg.extend(extra)
        # every other summand of every cube word has a zero factor
        Cset = set(Cc)
        for al in cube:
            for img in itertools.permutations(R, 3):
                if set(img) == Cset:
                    continue
                rest = tuple(x for x in R if x not in img)
                mr = self.mvar(rest, tuple(col[x] for x in rest))
                if not val(mr):
                    neg.append(mr)
                    continue
                lits = [self.gvar(t, u, a, col[u]) for t, u, a in zip(T, img, al)]
                z = next((l for l in lits if not val(l)), None)
                if z is None:
                    return None
                neg.append(z)
            for i, j in ((0, 1), (0, 2), (1, 2)):
                k = 3 - i - j
                gin = self.gvar(T[i], T[j], al[i], al[j])
                if not val(gin):
                    neg.append(gin)
                    continue
                for u in R:
                    rest = tuple(x for x in R if x != u)
                    mr = self.mvar(rest, tuple(col[x] for x in rest))
                    gu = self.gvar(T[k], u, al[k], col[u])
                    if not val(gu):
                        neg.append(gu)
                    elif not val(mr):
                        neg.append(mr)
                    else:
                        return None
        clause = sorted({-h} | set(neg) | {zero[al][1] for al in cube})
        if self.true in clause:
            return None
        return clause

    def _zero_minor_lits(self, T, Cc, col, pairs, val):
        """{(t_index, a): literals} for minors l_t[a] identically zero on the
        support (neither product supported); the literals are false in val."""
        out = {}
        for ti, (t, (al, al2)) in enumerate(zip(T, pairs)):
            y = [self.gvar(t, u, al, col[u]) for u in Cc]
            y2 = [self.gvar(t, u, al2, col[u]) for u in Cc]
            for a in range(3):
                b, d = (a + 1) % 3, (a + 2) % 3
                l1 = next((l for l in (y[b], y2[d]) if not val(l)), None)
                l2 = next((l for l in (y[d], y2[b]) if not val(l)), None)
                if l1 is not None and l2 is not None:
                    out[(ti, a)] = [l1, l2]
        return out

    # ------------------------------------- fast PR scan (--fast-plane)
    def model_tables(self, model):
        """Boolean views of a solver model for the vectorized scans.

        Returns (mv, G, M): mv[id] is the value of variable id (False for ids
        the model does not mention, matching val() on the decoded model);
        G[v,u,a,b] = gvar(v,u,a,b) (False on the diagonal); M[k][s, w] =
        m[(sets_k[s], words_k[w])] for every even k >= 4."""
        import numpy as np
        cached = getattr(self, "_fast_model", None)
        if cached is not None and cached[0] is model:
            return cached[1]
        if not hasattr(self, "_fast_ids"):
            n = self.n
            gid = np.zeros((n, n, C, C), dtype=np.int64)       # id 0 is never a variable
            for v in self.V:
                for u in self.V:
                    if u != v:
                        for a in range(C):
                            for b in range(C):
                                gid[v, u, a, b] = self.gvar(v, u, a, b)
            mid, sidx = {}, {}
            for k in range(4, n + 1, 2):
                sets_k = list(itertools.combinations(self.V, k))
                words = list(itertools.product(range(C), repeat=k))
                sidx[k] = {A: i for i, A in enumerate(sets_k)}
                mid[k] = np.array([[self.m[(A, w)] for w in words] for A in sets_k], dtype=np.int64)
            self._fast_ids = (gid, mid, sidx)
        gid, mid, sidx = self._fast_ids
        arr = np.asarray(model, dtype=np.int64)
        mv = np.zeros(max(self.pool.top, int(np.abs(arr).max(initial=0))) + 1, dtype=bool)
        mv[arr[arr > 0]] = True
        mv[0] = False
        tables = (mv, mv[gid], {k: mv[ids] for k, ids in mid.items()})
        self._fast_model = (model, tables)
        return tables

    def holonomy_premises_fast(self, model, top_only=False, rules=("H2", "H3")):
        """Vectorized replacement of _holonomy_premises (same tuples, same
        order).  The live tables are read from the model's t literals (and
        g literals for two-vertex sub-configurations), exactly as tlit/val
        are read by the reference scan; m values from the m literals."""
        import numpy as np
        mv, G, M = self.model_tables(model)
        sets, sidx, lev = laplace_index(self.n)
        if not hasattr(self, "_fast_tid"):
            tid = {}
            for k in range(4, self.n + 1, 2):
                PJ = lev[k]["PJ"].tolist()
                tid[k] = np.array([[[[self.t[(A, w, A[i], A[j])] for j in PJ[i]]
                                     for i in range(k)] for w in lev[k]["Dl"]]
                                   for A in sets[k]], dtype=np.int64)
            self._fast_tid = tid
        Mt, L = laplace_live_tables(self.n, G, M, levels=(2,))   # two-vertex terms are g
        for k, ids in self._fast_tid.items():
            L[k] = mv[ids]
        for k in ([self.n] if top_only else range(4, self.n + 1, 2)):
            Dl = lev[k]["Dl"]
            S, W, I, JA, JB, Q = holonomy_scan_arrays(self.n, Mt, L, k, "H2" in rules)
            for c in range(len(S)):
                A, w, i, ia, ib = sets[k][S[c]], Dl[W[c]], I[c], JA[c], JB[c]
                p, a, b = A[i], A[ia], A[ib]
                idx = {v: t for t, v in enumerate(A)}
                qs = [A[qi] for qi, ok in enumerate(Q[c]) if ok]
                if qs:
                    Ba = tuple(x for x in A if x not in (p, a))
                    wa = tuple(w[idx[x]] for x in Ba)
                    Bb = tuple(x for x in A if x not in (p, b))
                    wb = tuple(w[idx[x]] for x in Bb)
                else:
                    Ba = wa = Bb = wb = None             # used only for H2 hubs
                yield A, idx, w, self.mvar(A, w), p, a, b, Ba, wa, Bb, wb, qs

    def _mvals(self, G, M, B, cols):
        """Values of m[B, cols-restricted word] for a sorted vertex tuple B;
        cols maps each vertex of B to an integer array of colours (all of one
        shape).  Matches mvar: true for B empty, g for |B| = 2."""
        import numpy as np
        if len(B) == 0:
            return None                          # caller treats None as all-true
        if len(B) == 2:
            return G[B[0], B[1], cols[B[0]], cols[B[1]]]
        k = len(B)
        widx = sum(cols[x] * (C ** (k - 1 - i)) for i, x in enumerate(B))
        _, _, sidx = self._fast_ids
        return M[k][sidx[k][B]][widx]

    def plane_scan_fast(self, model, val, top_only=False, mode="value"):
        """Vectorized equivalent of (check_plane, plane_instances).

        A numpy prefilter evaluates, for every (A, T, c, pairs, Cc) in the
        order of plane_instances, the support conditions that check_plane
        tests before the minors (cube words all zero, h, no other live
        injection summand, no live inner-edge summand).  Every survivor is
        then passed to the unchanged _plane_clause, which re-derives the full
        premise from val; so the returned instances are exactly those
        plane_instances returns, in the same order, and the returned list of
        violations is check_plane's 'bad' list (same tuples, same order).
        Returns (instances, bad)."""
        import numpy as np
        mv, G, M = self.model_tables(model)
        out, bad = {}, []
        sets = [self.V] if top_only else [A for A in self.sets if len(A) >= 6]
        AL = np.array(list(itertools.product(range(C), repeat=3)), dtype=np.int64)     # (27,3)
        PR3 = list(itertools.product(PAIRS, repeat=3))
        CUBE = np.array([[al[0] * 9 + al[1] * 3 + al[2] for al in itertools.product(*pr)]
                         for pr in PR3], dtype=np.int64)                                # (27,8)
        for A in sets:
            k = len(A)
            idx = {v: i for i, v in enumerate(A)}
            Mrow = M[k][self._fast_ids[2][k][A]]
            for T in itertools.combinations(A, 3):
                R = tuple(x for x in A if x not in T)
                r = len(R)
                cR = np.array(list(itertools.product(range(C), repeat=r)), dtype=np.int64)  # (NC,r)
                NC = len(cR)
                colR = {x: cR[:, s] for s, x in enumerate(R)}
                wR = sum(cR[:, s] * (C ** (k - 1 - idx[x])) for s, x in enumerate(R))
                wT = sum(AL[:, i] * (C ** (k - 1 - idx[t])) for i, t in enumerate(T))
                Mword = Mrow[wR[:, None] + wT[None, :]]                       # (NC,27)
                zero_cube = ~Mword[:, CUBE].any(axis=2)                       # (NC,27 pairs)
                if not zero_cube.any():
                    continue
                Tarr, Rarr = np.array(T), np.array(R)
                Bm = G[Tarr[None, None, :, None], Rarr[None, None, None, :],
                       AL[None, :, :, None], cR[:, None, None, :]]            # (NC,27,3,r)
                Ss = list(itertools.combinations(range(r), 3))
                ones = np.ones(NC, dtype=bool)
                live3 = np.zeros((NC, 27, len(Ss)), dtype=bool)
                hS = np.zeros((NC, len(Ss)), dtype=bool)
                for si, S in enumerate(Ss):
                    rest = tuple(x for s, x in enumerate(R) if s not in S)
                    mr = self._mvals(G, M, rest, colR)
                    mr = ones if mr is None else mr
                    hS[:, si] = mr
                    lp = np.zeros((NC, 27), dtype=bool)
                    for pi in itertools.permutations(S):
                        lp |= Bm[:, :, 0, pi[0]] & Bm[:, :, 1, pi[1]] & Bm[:, :, 2, pi[2]]
                    live3[:, :, si] = lp & mr[:, None]
                inner = np.zeros((NC, 27), dtype=bool)
                mRu = []
                for s, u in enumerate(R):
                    mr = self._mvals(G, M, tuple(x for x in R if x != u), colR)
                    mRu.append(ones if mr is None else mr)
                for i, j in ((0, 1), (0, 2), (1, 2)):
                    kk = 3 - i - j
                    gin = G[T[i], T[j], AL[:, i], AL[:, j]]                   # (27,)
                    term = np.zeros((NC, 27), dtype=bool)
                    for s in range(r):
                        term |= Bm[:, :, kk, s] & mRu[s][:, None]
                    inner |= gin[None, :] & term
                nlive = live3.sum(axis=2)
                bad_al = inner[:, :, None] | ((nlive[:, :, None] - live3) > 0)  # (NC,27,nS)
                badcube = bad_al[:, CUBE, :].any(axis=2)                      # (NC,27,nS)
                cand = zero_cube[:, :, None] & hS[:, None, :] & ~badcube
                if not cand.any():
                    continue
                Cs = list(itertools.combinations(R, 3))
                zero_cache = {}
                for ci, pi, si in zip(*np.nonzero(cand)):
                    c = tuple(int(z) for z in cR[ci])
                    col = dict(zip(R, c))
                    zero = zero_cache.get(ci)
                    if zero is None:
                        zero = {}
                        for al in itertools.product(range(C), repeat=3):
                            w = [0] * k
                            for x in R:
                                w[idx[x]] = col[x]
                            for t, a in zip(T, al):
                                w[idx[t]] = a
                            w = tuple(w)
                            zero[al] = (w, self.mvar(A, w))
                        zero_cache[ci] = zero
                    pairs = PR3[pi]
                    cube = list(itertools.product(*pairs))
                    Cc = Cs[si]
                    cl = self._plane_clause(A, T, R, col, Cc, pairs, cube, zero, val, mode)
                    if cl is not None:
                        out[("PR", len(A), tuple(sorted(cl)))] = [cl]
                        bad.append(("PR", A, T, c, pairs, Cc))
        return out, bad

    def fix_pattern(self, sup):
        """Unit assumptions fixing every g-variable to a given support."""
        return [v if k in sup else -v for k, v in self.g.items()]


class PairDecoratedGSM(GSM):
    """--g-minus: the order-n model on B = {0..n-1} with its GHZ pattern (G)
    replaced by (G-), what an order-(n+2) witness forces on B = V - {u, v}
    through the deleted pair u = n, v = n+1 (docs/strategy/support-
    induction-2026-10-09.md, Section 3).  A sound relaxation of the
    order-(n+2) model:
      * every even A in B (|A| >= 4): m[A, w] with (L), (F') at every hub; H2,
        H3 and PR (lazy) at these levels only;
      * g on every pair of V, including the attachments W_uz, W_vz, W_uv;
      * the sets V - {u, z} and V - {v, z} (z in B): m with (L), (F') at the
        hub v, resp. u, only (their other hubs are dropped);
      * V: m with (L), (F') at the hubs u and v only, and (G) on V;
      * --killers / --anchors: the order-(n+2) statements (partners in V).
    Dropped (sound): (L), (F') of V and of the decoration sets at hubs in B,
    every set containing both u and v other than V, holonomy and PR at sets
    meeting {u, v}, and the order-n (G), killers and anchors of B itself.
    No symmetry breaking.  UNSAT would exclude order n+2 at the support
    level; SAT says only that this relaxation does not."""

    def __init__(self, n, *, killers=False):
        N = n + 2
        self.n, self.N = n, N
        self.V = tuple(range(N))
        self.B = tuple(range(n))
        u, v = n, n + 1
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
        self.sets = [A for k in range(4, n + 1, 2) for A in itertools.combinations(self.B, k)]
        self.decoration = []
        for z in self.B:
            rest = tuple(x for x in self.B if x != z)
            self.decoration.append((rest + (v,), (v,)))      # V - {u, z}
            self.decoration.append((rest + (u,), (u,)))      # V - {v, z}
        self.decoration.append((self.V, (u, v)))
        for A in self.sets + [A for A, _ in self.decoration]:
            for w in itertools.product(range(C), repeat=len(A)):
                self.m[(A, w)] = self.pool.id(("m", A, w))
        for A in self.sets:
            self._laplace(A)
        for A, hubs in self.decoration:
            self._laplace(A, hubs)
        self._ghz()
        if killers:
            self._killers()


def check_model_gminus(n, gsup, msup, killers=False):
    """Independent brute-force check of a --g-minus model: (L), (F') at every
    hub of every even A in B, at the declared hub of each decoration set and
    at u, v for V; (G) on V; the order-(n+2) killers if requested."""
    N, u, v = n + 2, n, n + 1
    V, Bv = tuple(range(N)), tuple(range(n))

    def G(x, y, a, b):
        return ((x, y, a, b) in gsup) if x < y else ((y, x, b, a) in gsup)

    def M(A, w):
        if len(A) == 0:
            return True
        if len(A) == 2:
            return G(A[0], A[1], w[0], w[1])
        return (A, w) in msup

    todo = [(A, A) for k in range(4, n + 1, 2) for A in itertools.combinations(Bv, k)]
    for z in Bv:
        rest = tuple(x for x in Bv if x != z)
        todo += [(rest + (v,), (v,)), (rest + (u,), (u,))]
    todo.append((V, (u, v)))
    bad = []
    for A, hubs in todo:
        idx = {x: i for i, x in enumerate(A)}
        for w in itertools.product(range(C), repeat=len(A)):
            for p in hubs:
                kids = 0
                for q in A:
                    if q == p:
                        continue
                    R = tuple(x for x in A if x not in (p, q))
                    if G(p, q, w[idx[p]], w[idx[q]]) and M(R, tuple(w[idx[x]] for x in R)):
                        kids += 1
                if M(A, w) and kids == 0:
                    bad.append(("L", A, w, p))
                if not M(A, w) and kids == 1:
                    bad.append(("F'", A, w, p))
    for w in itertools.product(range(C), repeat=N):
        if (len(set(w)) == 1) != M(V, w):
            bad.append(("G", w))
    if killers:
        for x in V:
            for c in range(C):
                if not any(any(G(x, y, a, c) for a in range(C))
                           and not any(G(x, y, a, d) for a in range(C) for d in range(C) if d != c)
                           for y in V if y != x):
                    bad.append(("killer", x, c))
    return bad


PAIRS = ((0, 1), (0, 2), (1, 2))
PERM_SIGN = {(0, 1, 2): 1, (1, 2, 0): 1, (2, 0, 1): 1, (0, 2, 1): -1, (2, 1, 0): -1, (1, 0, 2): -1}


def _plane_choice(known, mode, zero_minors=None):
    """Pick one provably-nonzero minor coordinate a_t per inner vertex.

    known[t] maps a column index a to the clause literals certifying that the
    minor l_t[a] is a single nonzero monomial.  mode 'value': the a_t are not
    all equal (Theorem 3 / Corollary 3 of the hyperdeterminant theorem).
    mode 'deg3': a degree-3 certificate exists: exactly two a_t equal
    (Proposition 4), or the a_t are a permutation s and some other
    permutation s' of the same parity has an identically zero minor
    (binomial P_s - P_s' in J_3).  Returns (literals, extra) or None."""
    best = None
    for a in itertools.product(*[sorted(k) for k in known]):
        if len(set(a)) == 1:
            continue
        lits = [x for t in range(3) for x in known[t][a[t]]]
        if mode == "value":
            return lits, []
        if len(set(a)) == 2:
            return lits, []
        for s2, sg in PERM_SIGN.items():
            if s2 == a or sg != PERM_SIGN[a]:
                continue
            for t in range(3):
                if (t, s2[t]) in zero_minors:
                    best = best or (lits, zero_minors[(t, s2[t])])
    return best


def check_plane(n, gsup, msup, top_only=False, mode="value", stats=None, all_cubes=False):
    """Re-check of the plane-rigidity rule (PR) on a decoded model, from the
    supports alone (no SAT variables).  Returns the violated instances.
    all_cubes=True also visits cubes with a nonzero word (for soundness
    smoke tests on exact zero patterns; stats['PR_fired'] counts instances
    whose premises hold)."""
    V = tuple(range(n))

    def G(v, u, a, b):
        return ((v, u, a, b) in gsup) if v < u else ((u, v, b, a) in gsup)

    def M(B, col):
        B = tuple(sorted(B))
        if len(B) == 0:
            return True
        if len(B) == 2:
            return G(B[0], B[1], col[B[0]], col[B[1]])
        return (B, tuple(col[x] for x in B)) in msup

    def minor_status(t, al, al2, cols, col):
        """For each column index a: 'one' (single nonzero monomial),
        'zero' (identically zero on the support) or 'two'."""
        st = []
        for a in range(3):
            u1, u2 = cols[(a + 1) % 3], cols[(a + 2) % 3]
            p1 = G(t, u1, al, col[u1]) and G(t, u2, al2, col[u2])
            p2 = G(t, u2, al, col[u2]) and G(t, u1, al2, col[u1])
            st.append({0: "zero", 1: "one", 2: "two"}[p1 + p2])
        return st

    bad = []
    count = fired = 0
    reasons = {}
    sets = [V] if top_only else [A for k in range(6, n + 1, 2) for A in itertools.combinations(V, k)]
    for A in sets:
        for T in itertools.combinations(A, 3):
            R = [x for x in A if x not in T]
            for c in itertools.product(range(C), repeat=len(R)):
                base = dict(zip(R, c))
                for pairs in itertools.product(PAIRS, repeat=3):
                    words = []
                    for al in itertools.product(*pairs):
                        col = dict(base)
                        col.update(zip(T, al))
                        words.append((al, col))
                    cube_live = any(M(A, col) for _, col in words)
                    if cube_live and not all_cubes:
                        continue
                    for Cc in itertools.combinations(R, 3):
                        rest = [x for x in R if x not in Cc]
                        if not M(rest, base):
                            if not cube_live:
                                reasons["h_dead"] = reasons.get("h_dead", 0) + 1
                            continue
                        ok = True
                        for al, col in words:
                            # summands with t -> R injective, image != C
                            for img in itertools.permutations(R, 3):
                                if set(img) == set(Cc):
                                    continue
                                if (all(G(t, u, col[t], col[u]) for t, u in zip(T, img))
                                        and M([x for x in R if x not in img], base)):
                                    ok = False
                                    break
                            if not ok:
                                break
                            # summands with one inner edge
                            for i, j in ((0, 1), (0, 2), (1, 2)):
                                k = 3 - i - j
                                if not G(T[i], T[j], col[T[i]], col[T[j]]):
                                    continue
                                if any(G(T[k], u, col[T[k]], col[u]) and M([x for x in R if x != u], base)
                                       for u in R):
                                    ok = False
                                    break
                            if not ok:
                                break
                        if not ok:
                            if not cube_live:
                                reasons["other_summand_live"] = reasons.get("other_summand_live", 0) + 1
                            continue
                        status = [minor_status(t, al, al2, Cc, base) for t, (al, al2) in zip(T, pairs)]
                        known = [{a: [] for a in range(3) if status[ti][a] == "one"} for ti in range(3)]
                        zm = {(ti, a): [] for ti in range(3) for a in range(3) if status[ti][a] == "zero"}
                        count += not cube_live
                        if _plane_choice(known, mode, zm) is not None:
                            fired += 1
                            if not cube_live:
                                bad.append(("PR", A, T, tuple(c), pairs, Cc))
                        elif not cube_live:
                            if not all(known):
                                why = "some_vertex_without_single_monomial_minor"
                            elif len(set().union(*known)) == 1:
                                why = "single_minors_on_one_common_axis"
                            else:
                                why = "no_degree3_pattern"
                            reasons[why] = reasons.get(why, 0) + 1
    if stats is not None:
        stats["PR_premise_instances"] = count
        stats["PR_fired"] = fired
        stats["PR_zero_cube_reasons"] = reasons
    return bad


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


# ------------------------------------------- vectorized Laplace tables (--fast)
_LAPLACE_INDEX = {}


def laplace_index(n):
    """Combinatorial index tables of the Laplace expansion on n vertices
    (cached).  Returns (sets, sidx, lev): sets[k] lists the k-subsets in
    itertools.combinations order, sidx[k] inverts it, and for even k >= 2
    lev[k] holds D (3^k, k) the words in itertools.product order, VERT
    (|sets[k]|, k), PJ (k, k-1) the partner positions of each position,
    SUBS (|sets[k]|, k, k-1) and SUBW (3^k, k, k-1) the set and word index of
    (A - {A_i, A_j}, w restricted) at level k-2 for j = PJ[i, jj]."""
    import numpy as np
    if n in _LAPLACE_INDEX:
        return _LAPLACE_INDEX[n]
    sets = {k: list(itertools.combinations(range(n), k)) for k in range(0, n + 1, 2)}
    sidx = {k: {A: i for i, A in enumerate(s)} for k, s in sets.items()}
    lev = {}
    for k in range(2, n + 1, 2):
        D = np.array(list(itertools.product(range(C), repeat=k)), dtype=np.int64)
        part = [[j for j in range(k) if j != i] for i in range(k)]
        SUBS = np.zeros((len(sets[k]), k, k - 1), dtype=np.int64)
        SUBW = np.zeros((len(D), k, k - 1), dtype=np.int64)
        for i in range(k):
            for jj, j in enumerate(part[i]):
                keep = [x for x in range(k) if x not in (i, j)]
                SUBS[:, i, jj] = [sidx[k - 2][tuple(A[x] for x in keep)] for A in sets[k]]
                if keep:
                    SUBW[:, i, jj] = D[:, keep] @ (C ** np.arange(len(keep) - 1, -1, -1))
        lev[k] = {"D": D, "Dl": [tuple(r) for r in D.tolist()],
                  "VERT": np.array(sets[k], dtype=np.int64),
                  "PJ": np.array(part, dtype=np.int64), "SUBS": SUBS, "SUBW": SUBW,
                  "pow": [C ** (k - 1 - t) for t in range(k)]}
    _LAPLACE_INDEX[n] = (sets, sidx, lev)
    return _LAPLACE_INDEX[n]


def laplace_live_tables(n, G, Mk, levels=None):
    """Live tables of the Laplace expansion from zero-pattern arrays.

    G: bool (n, n, 3, 3) with G[v,u,a,b] the support of (colour a at v,
    colour b at u); Mk: {k: bool (|sets[k]|, 3^k)} for even k >= 4.
    Returns (M, L): M[k] for every even k (M[0] true, M[2] from G) and
    L[k][s, wi, i, jj] = G[A_i, A_j, w_i, w_j] and M[k-2][A - {A_i, A_j}, w|]
    with j = PJ[i, jj], i.e. the Laplace term of (A, w) at A_i with partner
    A_j is live (exactly check_holonomy's live_at).  levels restricts the
    levels of L that are computed (default: all)."""
    import numpy as np
    _, _, lev = laplace_index(n)
    d2 = lev[2]
    M = {0: np.ones((1, 1), dtype=bool),
         2: G[d2["VERT"][:, 0][:, None], d2["VERT"][:, 1][:, None],
              d2["D"][None, :, 0], d2["D"][None, :, 1]]}
    M.update(Mk)
    L = {}
    for k in (range(2, n + 1, 2) if levels is None else levels):
        d = lev[k]
        D, VERT, PJ = d["D"], d["VERT"], d["PJ"]
        g = G[VERT[:, None, :, None], VERT[:, PJ][:, None, :, :],
              D[None, :, :, None], D[:, PJ][None, :, :, :]]
        L[k] = g & M[k - 2][d["SUBS"][:, None, :, :], d["SUBW"][None, :, :, :]]
    return M, L


def holonomy_scan_arrays(n, M, L, k, h2=True):
    """Vectorized premise scan of one level.  Returns lists (S, W, I, JA, JB,
    Q): every (set s, word wi, position i) with M[k] false and exactly two
    live partners, in (A, w, p) order; JA < JB the positions of the two live
    partners a, b; Q[c][qi] true iff q = A[qi] is not p, a, b and the live set
    of q in (A - {p, a}) is exactly [b] and in (A - {p, b}) exactly [a]."""
    import numpy as np
    _, _, lev = laplace_index(n)
    d = lev[k]
    Lk = L[k]
    mask = (~M[k])[:, :, None] & (Lk.sum(axis=3) == 2)
    S, W, I = np.nonzero(mask)
    rows = Lk[S, W, I]
    JJ = np.argsort(~rows, axis=1, kind="stable")[:, :2]
    JJa, JJb = JJ[:, 0], JJ[:, 1]
    JA, JB = d["PJ"][I, JJa], d["PJ"][I, JJb]
    Q = np.zeros((len(S), k), dtype=bool)
    if h2 and len(S):
        Ls = L[k - 2]
        cs = Ls.sum(axis=3)
        sa, wa = d["SUBS"][S, I, JJa], d["SUBW"][W, I, JJa]
        sb, wb = d["SUBS"][S, I, JJb], d["SUBW"][W, I, JJb]
        for qi in range(k):
            ok = (I != qi) & (JA != qi) & (JB != qi)
            # (A - {p, a}): positions of q and b, and b's index among q's partners
            qa = np.where(ok, qi - (qi > I) - (qi > JA), 0)
            ba = JB - (JB > I) - (JB > JA)
            pa = np.where(ok, ba - (ba > qa), 0)
            okA = (cs[sa, wa, qa] == 1) & Ls[sa, wa, qa, pa]
            qb = np.where(ok, qi - (qi > I) - (qi > JB), 0)
            ab = JA - (JA > I) - (JA > JB)
            pb = np.where(ok, ab - (ab > qb), 0)
            okB = (cs[sb, wb, qb] == 1) & Ls[sb, wb, qb, pb]
            Q[:, qi] = ok & okA & okB
    return S.tolist(), W.tolist(), I.tolist(), JA.tolist(), JB.tolist(), Q.tolist()


def _support_tables(n, gsup, msup):
    """Zero-pattern arrays (G, Mk) of a decoded model, from the supports."""
    import numpy as np
    _, sidx, lev = laplace_index(n)
    G = np.zeros((n, n, C, C), dtype=bool)
    for (i, j, a, b) in gsup:
        G[i, j, a, b] = True
        G[j, i, b, a] = True
    Mk = {k: np.zeros((len(sidx[k]), C ** k), dtype=bool) for k in range(4, n + 1, 2)}
    for (A, w) in msup:
        k = len(A)
        Mk[k][sidx[k][A], sum(c * p for c, p in zip(w, lev[k]["pow"]))] = True
    return G, Mk


def check_holonomy_fast(n, gsup, msup, top_only=False, rules=("H2", "H3"), stats=None):
    """check_holonomy with vectorized live tables (laplace_live_tables from
    the supports, no SAT variables).  Same (H2) graphs and (H3) grids with the
    same keys built in the same order, and the same post-processing; so the
    returned list equals check_holonomy's (validated by --cross-check-fast and
    the unit tests).  Used only as the in-loop gate of --fast-holonomy; the
    final acceptance of a SAT model always runs check_holonomy."""
    sets, sidx, lev = laplace_index(n)
    G, Mk = _support_tables(n, gsup, msup)
    Mt, L = laplace_live_tables(n, G, Mk)

    def M(A, w):
        k = len(A)
        return bool(Mt[k][sidx[k][A], sum(c * p for c, p in zip(w, lev[k]["pow"]))])

    def live_at(A, w, p):
        k = len(A)
        i = A.index(p)
        row = L[k][sidx[k][A], sum(c * q for c, q in zip(w, lev[k]["pow"])), i]
        PJ = lev[k]["PJ"][i]
        return [A[PJ[jj]] for jj in range(k - 1) if row[jj]]

    k23 = {}
    grids = {}
    for k in ([n] if top_only else range(4, n + 1, 2)):
        Dl = lev[k]["Dl"]
        S, W, I, JA, JB, Q = holonomy_scan_arrays(n, Mt, L, k, "H2" in rules)
        for c in range(len(S)):
            A, w, i, ia, ib = sets[k][S[c]], Dl[W[c]], I[c], JA[c], JB[c]
            p, a, b = A[i], A[ia], A[ib]
            if "H2" in rules:
                for qi, ok in enumerate(Q[c]):
                    if ok:
                        hub = frozenset([(p, w[i]), (A[qi], w[qi])])
                        k23.setdefault(hub, []).append(((a, w[ia]), (b, w[ib])))
            if "H3" in rules:
                uv = sorted([(a, b)] + [(min(p, x), max(p, x)) for x in A if x not in (p, a, b)])
                for u, v in uv:
                    rest = tuple((x, cx) for x, cx in zip(A, w) if x != u and x != v)
                    key = (A, p, frozenset((a, b)), u, v, rest)
                    grids.setdefault(key, set()).add((w[A.index(u)], w[A.index(v)]))
    # ---- from here on verbatim from check_holonomy
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


def check_anchors(n, gsup):
    """Independent re-check of the diagonal-anchor lemma on a decoded support."""
    def G(v, u, a, b):
        return ((v, u, a, b) in gsup) if v < u else ((u, v, b, a) in gsup)

    return [("ANC", v, c) for v in range(n) for c in range(C)
            if not any(G(v, u, c, c) and not any(G(v, u, c, d) for d in range(C) if d != c)
                       for u in range(n) if u != v)]


def check_model(n, gsup, msup, drop_types=()):
    """Independent brute-force check of (L), (F'), (G) on a decoded model.
    gsup: set of (i,j,a,b) with i<j; msup: set of (A,w) with |A|>=4.
    drop_types: nonconstant word types exempt from (G) (--g-drop-types)."""
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
        if len(set(w)) > 1 and word_type(w) in drop_types:
            continue
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
    ap.add_argument("--pattern-file", type=Path,
                    help="physical-support-v1 JSON fixture whose entries fix every g")
    ap.add_argument("--anchors", action="store_true",
                    help="add the diagonal-anchor clauses (valid strengthening)")
    ap.add_argument("--within-pattern-file", type=Path,
                    help="physical-support-v1 JSON fixture; force g = 0 outside it (g free inside)")
    ap.add_argument("--plane-rigidity", action="store_true",
                    help="add the plane-rigidity clause family (PR) lazily")
    ap.add_argument("--plane-top-only", action="store_true")
    ap.add_argument("--plane-mode", choices=("value", "deg3"), default="value")
    ap.add_argument("--max-rounds", type=int)
    ap.add_argument("--max-entries", type=int)
    ap.add_argument("--no-symmetry", action="store_true")
    ap.add_argument("--proof", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--fast-plane", action="store_true",
                    help="numpy-prefiltered PR scan (same violations and instances, same order)")
    ap.add_argument("--fast-holonomy", action="store_true",
                    help="do not rebuild holonomy instances already added (same new instances)")
    ap.add_argument("--fast", action="store_true",
                    help="--fast-plane and --fast-holonomy")
    ap.add_argument("--cross-check-fast", action="store_true",
                    help="every round, also run the reference scans and fail on any difference")
    ap.add_argument("--g-minus", action="store_true",
                    help="order-n model on B with (G) replaced by (G-): the deleted pair "
                         "u=n, v=n+1 of an order-(n+2) witness (PairDecoratedGSM); "
                         "needs --no-symmetry")
    ap.add_argument("--g-drop-types", default="",
                    help="comma list of nonconstant word types (colour-class sizes, e.g. "
                         "'5+1,4+2') whose (G) zero clauses are omitted (relaxation; every "
                         "union of types is invariant under the symmetry group)")
    args = ap.parse_args()
    drop = tuple(t for t in args.g_drop_types.split(",") if t)
    if args.g_minus:
        assert args.no_symmetry, "--g-minus has no symmetry block; pass --no-symmetry"
        assert not (args.fast or args.fast_plane or args.fast_holonomy or args.holonomy_top_only
                    or args.plane_top_only or args.pattern or args.pattern_file
                    or args.within_pattern_file or args.noncoordinate_killer), \
            "--g-minus supports --killers, --anchors, --holonomy, --plane-rigidity only"
    if args.fast:
        args.fast_plane = args.fast_holonomy = True
    xcheck = {}
    t0 = time.time()
    if args.g_minus:
        enc = PairDecoratedGSM(args.n, killers=args.killers)
    else:
        enc = GSM(args.n, symmetry=not args.no_symmetry, killers=args.killers,
                  noncoordinate_killer=args.noncoordinate_killer, g_drop_types=drop)
    if args.anchors:
        enc.anchors()
    if args.within_pattern_file:
        assert args.no_symmetry, "--within-pattern-file fixes labels; use --no-symmetry"
        data = json.loads(args.within_pattern_file.read_text(encoding="utf-8"))
        assert data["n"] == args.n, "pattern file order differs from n"
        inside = {tuple(e) for e in data["entries"]}
        enc.cnf.extend([[-v] for k, v in enc.g.items() if k not in inside])
    rec = {"n": args.n, "killers": args.killers, "noncoordinate_killer": args.noncoordinate_killer,
           "anchors": args.anchors,
           "within_pattern_file": args.within_pattern_file.as_posix() if args.within_pattern_file else None,
           "symmetry": not args.no_symmetry, "g_minus": args.g_minus,
           "g_drop_types": list(drop),
           "variables": enc.pool.top, "clauses": len(enc.cnf.clauses),
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
    if args.pattern_file:
        data = json.loads(args.pattern_file.read_text(encoding="utf-8"))
        assert data["n"] == args.n, "pattern file order differs from n"
        sup = {tuple(e) for e in data["entries"]}
        assert all(i < j for i, j, _, _ in sup)
        assume = enc.fix_pattern(sup)
        rec["pattern_file"] = args.pattern_file.as_posix()
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
    rec["plane_rigidity"] = args.plane_rigidity or args.plane_top_only
    if rec["plane_rigidity"]:
        rec["plane_mode"] = args.plane_mode
        rec["plane_scope"] = "top" if args.plane_top_only else "all levels |A| >= 6"
    if args.fast_plane or args.fast_holonomy:
        rec["fast_plane"] = args.fast_plane
        rec["fast_holonomy"] = args.fast_holonomy
        rec["cross_check_fast"] = args.cross_check_fast
    print(json.dumps(rec), flush=True)
    t1 = time.time()
    added = {}
    rounds = 0
    lazy = rec["holonomy"] or rec["plane_rigidity"]
    stopped = False
    with Cadical153(bootstrap_with=enc.cnf.clauses) as solver:
        while True:
            sat = solver.solve(assumptions=assume)
            model = solver.get_model() if sat else None
            rounds += 1
            if not sat or not lazy:
                break
            pos = {l for l in model if l > 0}
            gsup = {k for k, v in enc.g.items() if v in pos}
            msup = {k for k, v in enc.m.items() if v in pos}
            val = (lambda lit: (lit in pos) if lit > 0 else (-lit not in pos))
            if rec["holonomy"] and args.fast_holonomy:
                hbad = check_holonomy_fast(args.n, gsup, msup, args.holonomy_top_only, rules)
                if args.cross_check_fast:
                    if check_holonomy(args.n, gsup, msup, args.holonomy_top_only, rules) != hbad:
                        raise RuntimeError("--fast-holonomy violation list differs from check_holonomy")
                    xcheck["holonomy_check_rounds"] = xcheck.get("holonomy_check_rounds", 0) + 1
            elif rec["holonomy"]:
                hbad = check_holonomy(args.n, gsup, msup, args.holonomy_top_only, rules)
            else:
                hbad = []
            fast_pinst = None
            if rec["plane_rigidity"] and args.fast_plane:
                fast_pinst, pbad = enc.plane_scan_fast(model, val, args.plane_top_only, args.plane_mode)
                if args.cross_check_fast:
                    ref = check_plane(args.n, gsup, msup, args.plane_top_only, args.plane_mode)
                    if ref != pbad:
                        raise RuntimeError("--fast-plane violation list differs from check_plane")
                    refi = enc.plane_instances(val, args.plane_top_only, args.plane_mode)
                    if list(refi.items()) != list(fast_pinst.items()):
                        raise RuntimeError("--fast-plane instances differ from plane_instances")
                    xcheck["plane_rounds"] = xcheck.get("plane_rounds", 0) + 1
            elif rec["plane_rigidity"]:
                pbad = check_plane(args.n, gsup, msup, args.plane_top_only, args.plane_mode)
            else:
                pbad = []
            if not hbad and not pbad:
                break
            if args.max_rounds is not None and rounds >= args.max_rounds:
                stopped = True
                break
            inst = {}
            if hbad:
                if args.fast_holonomy:
                    hinst = enc.holonomy_instances(
                        val, args.holonomy_top_only, rules, skip=added,
                        premises=enc.holonomy_premises_fast(model, args.holonomy_top_only, rules))
                    if args.cross_check_fast:
                        ref = enc.holonomy_instances(val, args.holonomy_top_only, rules)
                        refnew = {k: v for k, v in ref.items() if k not in added}
                        if list(refnew.items()) != list(hinst.items()):
                            raise RuntimeError("--fast-holonomy new instances differ")
                        xcheck["holonomy_rounds"] = xcheck.get("holonomy_rounds", 0) + 1
                    inst.update(hinst)
                else:
                    inst.update(enc.holonomy_instances(val, args.holonomy_top_only, rules))
            if pbad:
                pinst = (fast_pinst if fast_pinst is not None
                         else enc.plane_instances(val, args.plane_top_only, args.plane_mode))
                if not pinst:
                    raise RuntimeError("plane checker reports a violation but the encoder finds none; bug")
                inst.update(pinst)
            new = {k: cl for k, cl in inst.items() if k not in added}
            if not new:
                raise RuntimeError("checker reports a violation but no new instance; encoder bug")
            for k, cl in new.items():
                added[k] = cl
                for c in cl:
                    solver.add_clause(c)
            print(json.dumps({"round": rounds, "holonomy_violations": len(hbad),
                              "plane_violations": len(pbad),
                              "first_violation": str((hbad or pbad)[0])[:160],
                              "new_instances": len(new), "total_instances": len(added),
                              "seconds": round(time.time() - t1, 1)}), flush=True)
    rec["result"] = "SAT" if sat else "UNSAT"
    if stopped:
        rec["result"] = "INCONCLUSIVE (max rounds reached)"
    rec["solve_seconds"] = round(time.time() - t1, 1)
    if args.cross_check_fast:
        rec["cross_check_fast_rounds_passed"] = xcheck
    if lazy:
        rec["cegar_rounds"] = rounds
        rec["lazy_instances_added"] = len(added)
        rec["lazy_clauses_added"] = sum(len(c) for c in added.values())
        kinds = {}
        for k in added:
            kinds[k[0]] = kinds.get(k[0], 0) + 1
        rec["lazy_instances_by_rule"] = kinds
        lev = {}
        for k in added:
            if k[0] == "PR":
                lev[str(k[1])] = lev.get(str(k[1]), 0) + 1
        if lev:
            rec["plane_instances_by_level"] = lev
    if stopped:
        sat = False
    if args.proof and not sat and not stopped:
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
        if args.g_minus:
            bad = check_model_gminus(args.n, gsup, msup, killers=args.killers)
        else:
            bad = check_model(args.n, gsup, msup, drop)
        if args.anchors:
            bad += check_anchors(args.n + 2 if args.g_minus else args.n, gsup)
        if rec["holonomy"]:
            bad += check_holonomy(args.n, gsup, msup, args.holonomy_top_only, rules)
        if rec["plane_rigidity"]:
            pst = {}
            bad += check_plane(args.n, gsup, msup, args.plane_top_only, args.plane_mode, stats=pst)
            rec["plane_premise_instances_in_model"] = pst["PR_premise_instances"]
            rec["plane_zero_cube_failure_reasons"] = pst["PR_zero_cube_reasons"]
            if args.n >= 8 and not args.g_minus:
                top = {}
                check_plane(args.n, gsup, msup, True, args.plane_mode, stats=top)
                rec["plane_top_level_premise_instances"] = top["PR_premise_instances"]
                rec["plane_top_level_failure_reasons"] = top["PR_zero_cube_reasons"]
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
