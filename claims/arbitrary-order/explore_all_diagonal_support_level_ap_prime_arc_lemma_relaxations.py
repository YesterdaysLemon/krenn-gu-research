"""Exploratory SAT search for relaxed AP' models violating the arc lemma.

Research tool, not a verifier.  Setting: an AP' model with G_0 = M_0, the
perfect matching {01, 23, ..., (n-2)(n-1)} (WLOG by relabelling; no other
symmetry breaking is used).  By Proposition 1 of the extra-edge document,
S_0 is then exactly the family of M_0-unions, so colour 0 carries no
variables, and (H2) is the two-colour condition

  (R) no partition V = U + A_1 + A_2 with U an M_0-union, A_1 in S_1,
      A_2 in S_2, and at least two of the three classes nonempty.

Colours 1 and 2 have variables g[c][e] (e in G_c) and m[c][A] (A in S_c,
|A| >= 4 even); 2-sets of S_c are the edges of G_c, the empty set and V are
in S_c.  Axioms per colour are switchable:

  L   Laplace accessibility (L) at every member;
  F   forcing (F) for every uniquely matchable set;
  S   (S) is always imposed (members are G_c-matchable).

Colour 2 may be dropped entirely (--c2 none), in which case (R) keeps only
its A_2 = empty instances, i.e. no proper nonempty M_0-union lies in S_1.

The arc-lemma negation for colour c ("--negate-arc 1", or "12" for both):
for every perfect matching N with M_0 + N a Hamiltonian cycle, N is not
contained in G_c or some N-ended arc of that cycle is not in S_c.

"--negate-arc 0" imposes no arc condition.  "--fmax1 k" keeps colour-1
forcing only for |A| <= k.  "--force-c2 arc" adds the arc lemma for colour 2
at the cycle 0-1-...-(n-1) (N_2 = {(2i+1, 2i+2)} in G_2, every N_2-ended arc
in S_2; WLOG by relabelling); "--force-c2 matching" sets G_2 = N_2 and S_2 =
the N_2-unions.  Colour-option strings without L or F (e.g. "S") keep only
(a), (S), (H1) for that colour.

A SAT answer is decoded and re-checked by an independent brute-force checker
(explicit perfect-matching enumeration, explicit Hamiltonian-cycle and arc
enumeration; the --force-c2 hypotheses are not re-checked).  An UNSAT answer
is evidence at one order only: no proof trace is recorded.

Usage: python explore_..._arc_lemma_relaxations.py N [--c1 LF] [--c2 LF|L|F|S|none]
       [--negate-arc 0|1|12] [--top] [--fmax1 K] [--force-c2 arc|matching] [--out PATH]
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical153


def m0_pairs(n):
    return [frozenset((2 * i, 2 * i + 1)) for i in range(n // 2)]


def is_m0_union(A, n):
    return all((v ^ 1) in A for v in A)


def hamiltonian_orders(n):
    """Vertex orders v_0..v_{n-1} of the Hamiltonian cycles M_0 + N, each once.

    v_{2i} v_{2i+1} are M_0-edges, v_{2i+1} v_{2i+2} (indices mod n) N-edges."""
    m = n // 2
    for perm in itertools.permutations(range(1, m)):
        for flips in itertools.product((0, 1), repeat=m - 1):
            order = [0, 1]
            for k, f in zip(perm, flips):
                a, b = 2 * k, 2 * k + 1
                order += [b, a] if f else [a, b]
            yield order


def cycle_N_and_arcs(order):
    n = len(order)
    N = [frozenset((order[i], order[(i + 1) % n])) for i in range(1, n, 2)]
    arcs = []
    for i in range(1, n, 2):
        for k in range(1, n // 2):
            arcs.append(frozenset(order[(i + j) % n] for j in range(2 * k)))
    return N, sorted(set(arcs), key=lambda A: (len(A), sorted(A)))


class ArcEncoder:
    def __init__(self, n, c1="LF", c2="LF", negate_arc="1", top=False, fmax1=None, force_c2="none"):
        self.n = n
        self.fmax = {1: fmax1 if fmax1 is not None else n, 2: n}
        self.V = frozenset(range(n))
        self.pairs = [frozenset(p) for p in itertools.combinations(range(n), 2)]
        self.pool = IDPool()
        self.cnf = CNF()
        self.true = self.pool.id("TRUE")
        self.cnf.append([self.true])
        self.colours = [1] + ([] if c2 == "none" else [2])
        self.opts = {1: c1, 2: c2}
        self.sets = [frozenset(A) for k in range(4, n + 1, 2)
                     for A in itertools.combinations(range(n), k)]
        self.g = {(c, e): self.pool.id(("g", c, tuple(sorted(e))))
                  for c in self.colours for e in self.pairs}
        self.m = {(c, A): self.pool.id(("m", c, tuple(sorted(A))))
                  for c in self.colours for A in self.sets}
        self.mt, self.uq, self.t = {}, {}, {}
        for c in self.colours:
            self._colour(c)
            self.cnf.append([self.m[(c, self.V)]])
        if top:
            for c in self.colours:
                for v in range(n):
                    tops = [self.t[(c, self.V, v, u)] for u in range(n) if u != v]
                    for a, b in itertools.combinations(tops, 2):
                        self.cnf.append([-a, -b])
        self.rainbow = 0
        self._rainbow()
        self.arc_clauses = 0
        for c in map(int, negate_arc):
            if c in self.colours:
                self._negate_arc(c)
        if force_c2 != "none":
            self._force_c2(force_c2)

    def require_nonmatching(self, c):
        """Extra hypothesis: some vertex has degree >= 2 in G_c."""
        ws = []
        for v in range(self.n):
            lits = [self.g[(c, frozenset((v, u)))] for u in range(self.n) if u != v]
            w = self.pool.id(("deg2", c, v))
            ws.append(w)
            for i in range(len(lits)):
                self.cnf.append([-w] + lits[:i] + lits[i + 1:])
        self.cnf.append(ws)

    def _force_c2(self, mode):
        """Hypotheses on colour 2 at the cycle 0-1-...-(n-1) (WLOG by relabelling
        a Hamiltonian M_0 + N_2): 'arc' puts N_2 = {(2i+1, 2i+2)} in G_2 and every
        N_2-ended arc in S_2; 'matching' sets G_2 = N_2 and S_2 = N_2-unions."""
        n = self.n
        N2 = {frozenset((2 * i + 1, (2 * i + 2) % n)) for i in range(n // 2)}
        if mode == "arc":
            for e in N2:
                self.cnf.append([self.g[(2, e)]])
            for i in range(1, n, 2):
                for k in range(2, n // 2):
                    self.cnf.append([self.m[(2, frozenset((i + j) % n for j in range(2 * k)))]])
        elif mode == "matching":
            for e in self.pairs:
                self.cnf.append([self.g[(2, e)] if e in N2 else -self.g[(2, e)]])
            for A in self.sets:
                union = all(any(v in e and e <= A for e in N2) for v in A)
                self.cnf.append([self.m[(2, A)] if union else -self.m[(2, A)]])
        else:
            raise ValueError(mode)

    def mvar(self, c, A):
        if not A:
            return self.true
        if len(A) == 2:
            return self.g[(c, frozenset(A))]
        return self.m[(c, frozenset(A))]

    def _sub(self, table, c, A):
        if not A:
            return self.true
        if len(A) == 2:
            return self.g[(c, frozenset(A))]
        return table[(c, frozenset(A))]

    def _colour(self, c):
        cnf, pool = self.cnf, self.pool
        opts = self.opts[c]
        for A in self.sets:                                   # increasing size
            As = sorted(A)
            mA = self.m[(c, A)]
            mtA, uqA = pool.id(("mt", c, tuple(As))), pool.id(("uq", c, tuple(As)))
            self.mt[(c, A)], self.uq[(c, A)] = mtA, uqA
            for v in As:
                lits = []
                for u in As:
                    if u == v:
                        continue
                    tv = pool.id(("t", c, tuple(As), v, u))
                    self.t[(c, A, v, u)] = tv
                    lits.append(tv)
                    gv, mr = self.g[(c, frozenset((v, u)))], self.mvar(c, A - {v, u})
                    cnf.extend([[-tv, gv], [-tv, mr], [tv, -gv, -mr]])
                if "L" in opts:
                    cnf.append([-mA] + lits)                  # (L)
            v0 = As[0]
            ws = []
            for u in As[1:]:
                w = pool.id(("w", c, tuple(As), u))
                ws.append((u, w))
                gv, sub = self.g[(c, frozenset((v0, u)))], self._sub(self.mt, c, A - {v0, u})
                cnf.extend([[-w, gv], [-w, sub], [w, -gv, -sub]])
            cnf.append([-mtA] + [w for _, w in ws])
            for _, w in ws:
                cnf.append([mtA, -w])
            cnf.append([-uqA] + [w for _, w in ws])
            for (_, w1), (_, w2) in itertools.combinations(ws, 2):
                cnf.append([-uqA, -w1, -w2])
            for u, w in ws:
                sub = self._sub(self.uq, c, A - {v0, u})
                cnf.append([-uqA, -w, sub])
                cnf.append([uqA, -w, -sub] + [o for uu, o in ws if uu != u])
            cnf.append([-mA, mtA])                            # (S)
            if "F" in opts and len(A) <= self.fmax[c]:
                cnf.append([-uqA, mA])                        # (F)

    def _rainbow(self):
        n = self.n
        has2 = 2 in self.colours
        for word in itertools.product(range(3), repeat=n):
            cl = [frozenset(v for v in range(n) if word[v] == c) for c in range(3)]
            if any(len(A) % 2 for A in cl) or sum(1 for A in cl if A) < 2:
                continue
            if not is_m0_union(cl[0], n):
                continue
            if cl[2] and not has2:
                continue
            lits = [-self.mvar(c, cl[c]) for c in (1, 2) if cl[c]]
            self.cnf.append(lits)
            self.rainbow += 1

    def _negate_arc(self, c):
        for order in hamiltonian_orders(self.n):
            N, arcs = cycle_N_and_arcs(order)
            lits = [-self.g[(c, e)] for e in N] + [-self.mvar(c, A) for A in arcs if len(A) > 2]
            self.cnf.append(lits)
            self.arc_clauses += 1


# -- independent brute-force checker -----------------------------------------
def perfect_matchings(vs):
    vs = tuple(vs)
    if not vs:
        yield ()
        return
    a, rest = vs[0], vs[1:]
    for k, b in enumerate(rest):
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            yield ((a, b),) + tail


def check(n, G, S, c1, c2, negate_arc, top=False, fmax1=None):
    """G[c]: set of frozenset edges; S[c]: set of frozensets (all sizes >= 4).
    Returns a list of violations of the imposed system."""
    V = frozenset(range(n))
    fmax = {1: fmax1 if fmax1 is not None else n, 2: n}
    colours = [1] + ([] if c2 == "none" else [2])
    opts = {1: c1, 2: c2}

    def inS(c, A):
        A = frozenset(A)
        if not A:
            return True
        if len(A) == 2:
            return A in G[c]
        return A in S[c]

    bad = []
    evens = [frozenset(A) for k in range(4, n + 1, 2) for A in itertools.combinations(range(n), k)]
    for c in colours:
        if not inS(c, V):
            bad.append(("H1", c))
        for A in evens:
            cnt = sum(1 for M in perfect_matchings(sorted(A)) if all(frozenset(e) in G[c] for e in M))
            if inS(c, A) and cnt == 0:
                bad.append(("S", c, sorted(A)))
            if "F" in opts[c] and len(A) <= fmax[c] and cnt == 1 and not inS(c, A):
                bad.append(("F", c, sorted(A)))
            if "L" in opts[c] and inS(c, A):
                for v in A:
                    if not any(inS(c, (v, u)) and inS(c, A - {v, u}) for u in A if u != v):
                        bad.append(("L", c, sorted(A), v))
        if top:
            for v in range(n):
                if sum(1 for u in range(n) if u != v and inS(c, (v, u)) and inS(c, V - {v, u})) > 1:
                    bad.append(("top", c, v))
    # (R), enumerated directly over M_0-unions U and splittings of V - U
    m0 = m0_pairs(n)
    for r in range(len(m0) + 1):
        for Us in itertools.combinations(m0, r):
            U = frozenset().union(*Us) if Us else frozenset()
            rest = sorted(V - U)
            for k in range(0, len(rest) + 1, 2):
                for A1 in itertools.combinations(rest, k):
                    A1 = frozenset(A1)
                    A2 = frozenset(rest) - A1
                    if len(A2) % 2 or sum(1 for X in (U, A1, A2) if X) < 2:
                        continue
                    if A2 and 2 not in colours:
                        continue
                    if inS(1, A1) and (not A2 or inS(2, A2)):
                        bad.append(("R", sorted(U), sorted(A1), sorted(A2)))
    for c in map(int, negate_arc):
        if c not in colours:
            continue
        for order in hamiltonian_orders(n):
            N, arcs = cycle_N_and_arcs(order)
            if all(e in G[c] for e in N) and all(inS(c, A) for A in arcs):
                bad.append(("arc lemma holds", c, order))
    return bad


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--c1", default="LF")
    ap.add_argument("--c2", default="LF")
    ap.add_argument("--negate-arc", default="1")
    ap.add_argument("--top", action="store_true")
    ap.add_argument("--fmax1", type=int, default=None,
                    help="impose colour-1 forcing only on sets of size <= FMAX1")
    ap.add_argument("--force-c2", default="none", choices=["none", "arc", "matching"])
    ap.add_argument("--nonmatching1", action="store_true",
                    help="extra hypothesis: G_1 is not a perfect matching (some degree >= 2)")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    enc = ArcEncoder(args.n, args.c1, args.c2, args.negate_arc, args.top,
                     fmax1=args.fmax1, force_c2=args.force_c2)
    if args.nonmatching1:
        enc.require_nonmatching(1)
    rec = {"n": args.n, "G0": "M0", "c1": args.c1, "c2": args.c2,
           "negate_arc": args.negate_arc, "top": args.top,
           "fmax1": args.fmax1, "force_c2": args.force_c2, "nonmatching1": args.nonmatching1,
           "variables": enc.pool.top, "clauses": len(enc.cnf.clauses),
           "rainbow_clauses": enc.rainbow, "arc_clauses": enc.arc_clauses,
           "encode_seconds": round(time.time() - t0, 1),
           "solver": "CaDiCaL 1.5.3 via python-sat"}
    print(json.dumps(rec), flush=True)
    t1 = time.time()
    with Cadical153(bootstrap_with=enc.cnf.clauses) as s:
        sat = s.solve()
        model = s.get_model() if sat else None
    rec["result"] = "SAT" if sat else "UNSAT"
    rec["solve_seconds"] = round(time.time() - t1, 1)
    if sat:
        pos = {l for l in model if l > 0}
        G = {c: {e for e in enc.pairs if enc.g[(c, e)] in pos} for c in enc.colours}
        S = {c: {A for A in enc.sets if enc.m[(c, A)] in pos} for c in enc.colours}
        bad = check(args.n, G, S, args.c1, args.c2, args.negate_arc, args.top, args.fmax1)
        rec["check"] = "PASS" if not bad else "FAIL"
        rec["check_violations"] = [str(b) for b in bad[:10]]
        rec["model"] = {str(c): {"G": sorted(sorted(e) for e in G[c]),
                                 "S": sorted(sorted(A) for A in S[c])} for c in enc.colours}
    print(json.dumps({k: v for k, v in rec.items() if k != "model"}), flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(rec, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
