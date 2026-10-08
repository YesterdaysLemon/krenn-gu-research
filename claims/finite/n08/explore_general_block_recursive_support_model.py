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

A SAT answer is re-checked by an independent brute-force checker.  An UNSAT
answer means no witness exists at this order (the model is implied by every
witness); this script records no proof trace, use --proof for a DIMACS file.

Usage: python explore_...py N [--killers] [--noncoordinate-killer]
       [--no-symmetry] [--proof PREFIX] [--out PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

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

        generator_tags = iter(range(10**6))

        def lex_leader(image):
            tag = next(generator_tags)   # distinct per generator (never id(), which CPython reuses)
            eq_prev = self.true
            for key in order:
                x, y = self.g[key], self.g[image(key)]
                if x == y:
                    continue
                cnf.append([-eq_prev, -x, y])
                eq = self.pool.id(("eq", tag, key))
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
            lex_leader(tau)

        def sigma(key):
            i, j, x, y = key
            s = {0: 0, 1: 2, 2: 1}
            return (i, j, s[x], s[y])
        lex_leader(sigma)

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
    print(json.dumps(rec), flush=True)
    t1 = time.time()
    with Cadical153(bootstrap_with=enc.cnf.clauses) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
    rec["result"] = "SAT" if sat else "UNSAT"
    rec["solve_seconds"] = round(time.time() - t1, 1)
    if sat:
        pos = {l for l in model if l > 0}
        gsup = {k for k, v in enc.g.items() if v in pos}
        msup = {k for k, v in enc.m.items() if v in pos}
        bad = check_model(args.n, gsup, msup)
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
