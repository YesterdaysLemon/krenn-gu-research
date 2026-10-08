"""Exploratory bounded SAT search for the all-diagonal support abstraction (AP').

This is a research tool, not a verifier.  It encodes AP' (WB2) and, optionally,
the singleton-noncancellation strengthening (F') used by the ten-vertex RZP
theorem, with two sound reductions of the search space:

* chain normalization: relabel so that one colour-0 Laplace chain from V is
  V, V-{0,1}, V-{0,1,2,3}, ..., {} (every AP' model has such a chain, and
  relabelling preserves every axiom), and lex-leader clauses for the symmetries
  that preserve that chain (endpoint swaps inside chain edges, colour swap 1-2);
* optional support normalization (--normalize): every member of S_c is either
  reachable from V by supported Laplace descent or uniquely matchable.  This is
  without loss of generality for AP' (shrinking S_c to that subfamily keeps
  every axiom and every rainbow clause) but NOT for AP'+(F'), so it is refused
  together with --fprime.

Encoding.  g[c][e]: e in G_c.  m[c][A]: A in S_c (|A|>=4; 2-sets are g; the
empty set is a true constant).  t[c][A,v,u] <-> g[vu] and m[A-vu].  mt/uq:
G_c[A] has a perfect matching / exactly one, defined recursively along min(A).
(L) m[A] -> OR_u t[A,v,u] for every v.  (S) m[A] -> mt[A].  (F) uq[A] -> m[A].
(F') not m[A] and t[A,v,u] -> OR_{u'!=u} t[A,v,u'].  (H1) m[c][V].  (H2) every
ordered even partition with at least two nonempty classes has a class outside
its family.

A SAT answer is re-checked against the axioms by an independent brute-force
checker before it is reported; an UNSAT answer is only as strong as the
encoding and the solver, and this script records no proof trace.

Usage: python explore_...py N [--fprime] [--normalize] [--no-symmetry]
       [--relax two_part_only|no_forcing|no_laplace] [--out PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical153


def perfect_matchings(vs):
    vs = tuple(vs)
    if not vs:
        yield ()
        return
    a, rest = vs[0], vs[1:]
    for k, b in enumerate(rest):
        for tail in perfect_matchings(rest[:k] + rest[k + 1:]):
            yield ((a, b),) + tail


class Encoder:
    def __init__(self, n, *, fprime=False, normalize=False, symmetry=True, relax=None,
                 top_matching=False):
        if fprime and normalize:
            raise ValueError("support normalization is not sound together with (F')")
        self.top_matching = top_matching
        self.n = n
        self.V = tuple(range(n))
        self.pairs = [tuple(p) for p in itertools.combinations(self.V, 2)]
        self.pool = IDPool()
        self.cnf = CNF()
        self.true = self.pool.id(("TRUE",))
        self.cnf.append([self.true])
        self.g = {(c, e): self.pool.id(("g", c, e)) for c in range(3) for e in self.pairs}
        self.sets = [frozenset(A) for k in range(4, n + 1, 2) for A in itertools.combinations(self.V, k)]
        self.m = {(c, A): self.pool.id(("m", c, A)) for c in range(3) for A in self.sets}
        self.mt = {}
        self.uq = {}
        self.t = {}
        self.fprime = fprime
        self.normalize = normalize
        self.relax = relax
        self.rainbow = 0
        for c in range(3):
            self._colour(c)
        for c in range(3):
            self.cnf.append([self.m[(c, frozenset(self.V))]])          # (H1)
        if top_matching:
            # extra hypothesis (not an AP' axiom): every top-active graph
            # E_c = {e : V - e in S_c} is a matching
            Vset = frozenset(self.V)
            for c in range(3):
                for v in self.V:
                    tops = [self.t[(c, Vset, v, u)] for u in self.V if u != v]
                    for a, b in itertools.combinations(tops, 2):
                        self.cnf.append([-a, -b])
        self._rainbow()                                                 # (H2)
        if symmetry:
            self._symmetry()

    # -- variable helpers -------------------------------------------------
    def mvar(self, c, A):
        if not A:
            return self.true
        if len(A) == 2:
            return self.g[(c, tuple(sorted(A)))]
        return self.m[(c, A)]

    def mtvar(self, c, A):
        if not A:
            return self.true
        if len(A) == 2:
            return self.g[(c, tuple(sorted(A)))]
        return self.mt[(c, A)]

    def uqvar(self, c, A):
        if not A:
            return self.true
        if len(A) == 2:
            return self.g[(c, tuple(sorted(A)))]
        return self.uq[(c, A)]

    def gvar(self, c, v, u):
        return self.g[(c, (min(v, u), max(v, u)))]

    # -- per-colour axioms ------------------------------------------------
    def _colour(self, c):
        cnf, pool = self.cnf, self.pool
        for A in self.sets:                                             # increasing size
            As = sorted(A)
            mA = self.m[(c, A)]
            mtA = pool.id(("mt", c, A))
            uqA = pool.id(("uq", c, A))
            self.mt[(c, A)] = mtA
            self.uq[(c, A)] = uqA
            # t[A,v,u] <-> g[vu] and m[A-vu]
            for v in As:
                lits = []
                for u in As:
                    if u == v:
                        continue
                    tv = pool.id(("t", c, A, v, u))
                    self.t[(c, A, v, u)] = tv
                    lits.append(tv)
                    gv, mr = self.gvar(c, v, u), self.mvar(c, A - {v, u})
                    cnf.append([-tv, gv])
                    cnf.append([-tv, mr])
                    cnf.append([tv, -gv, -mr])
                if self.relax != "no_laplace":
                    cnf.append([-mA] + lits)                            # (L)
                if self.fprime:                                         # (F')
                    for tv in lits:
                        cnf.append([mA, -tv] + [o for o in lits if o != tv])
            # matchability and unique matchability along v0 = min(A)
            v0 = As[0]
            ws = []
            for u in As[1:]:
                w = pool.id(("w", c, A, u))
                ws.append((u, w))
                gv, sub = self.gvar(c, v0, u), self.mtvar(c, A - {v0, u})
                cnf.append([-w, gv])
                cnf.append([-w, sub])
                cnf.append([w, -gv, -sub])
            cnf.append([-mtA] + [w for _, w in ws])
            for _, w in ws:
                cnf.append([mtA, -w])
            # uq <-> exactly one w true and that branch uniquely matchable
            cnf.append([-uqA] + [w for _, w in ws])
            for (_, w1), (_, w2) in itertools.combinations(ws, 2):
                cnf.append([-uqA, -w1, -w2])
            for u, w in ws:
                cnf.append([-uqA, -w, self.uqvar(c, A - {v0, u})])
                cnf.append([uqA, -w, -self.uqvar(c, A - {v0, u})]
                           + [o for uu, o in ws if uu != u])
            cnf.append([-mA, mtA])                                      # (S)
            if self.relax != "no_forcing":
                cnf.append([-uqA, mA])                                  # (F)
        if self.normalize:
            self._normalize(c)

    def _normalize(self, c):
        """m[A] -> reachable from V through S_c, or uniquely matchable."""
        cnf, pool = self.cnf, self.pool
        Vset = frozenset(self.V)
        r = {}
        for A in self.sets:
            r[A] = pool.id(("r", c, A))
        for e in self.pairs:
            r[frozenset(e)] = pool.id(("r", c, frozenset(e)))
        cnf.append([r[Vset]])
        for A, rA in r.items():
            if A == Vset:
                continue
            outside = [v for v in self.V if v not in A]
            lits = []
            for e in itertools.combinations(outside, 2):
                B = A | set(e)
                a = pool.id(("a", c, A, e))
                lits.append(a)
                cnf.append([-a, r[B]])
                cnf.append([-a, self.gvar(c, *e)])
            cnf.append([-rA] + lits)
            cnf.append([-self.mvar(c, A), rA, self.uqvar(c, A)])

    # -- rainbow clauses --------------------------------------------------
    def _rainbow(self):
        n = self.n
        for word in itertools.product(range(3), repeat=n):
            classes = [frozenset(v for v in self.V if word[v] == c) for c in range(3)]
            if any(len(A) % 2 for A in classes):
                continue
            nonempty = sum(1 for A in classes if A)
            if nonempty < 2 or (self.relax == "two_part_only" and nonempty == 3):
                continue
            self.cnf.append([-self.mvar(c, classes[c]) for c in range(3) if classes[c]])
            self.rainbow += 1

    # -- symmetry breaking ------------------------------------------------
    def _symmetry(self):
        n, cnf = self.n, self.cnf
        # chain normalization: colour-0 chain V, V-{0,1}, V-{0,1,2,3}, ...
        for k in range(1, n // 2 + 1):
            cnf.append([self.g[(0, (2 * k - 2, 2 * k - 1))]])
            rest = frozenset(range(2 * k, n))
            if len(rest) >= 4:
                cnf.append([self.m[(0, rest)]])
        order = [(c, e) for c in range(3) for e in self.pairs]

        def lex_leader(image):
            """Impose var-vector <=lex its image under a symmetry (g-prefix only)."""
            eq_prev = self.true
            for key in order:
                x, y = self.g[key], self.g[image(key)]
                if x == y:
                    continue
                cnf.append([-eq_prev, -x, y])
                eq = self.pool.id(("eq", id(image), key))
                cnf.append([-eq, eq_prev])
                cnf.append([-eq, -x, y])
                cnf.append([-eq, x, -y])
                cnf.append([eq, -eq_prev, -x, -y])
                cnf.append([eq, -eq_prev, x, y])
                eq_prev = eq

        for k in range(n // 2):
            a, b = 2 * k, 2 * k + 1

            def tau(key, a=a, b=b):
                c, (x, y) = key
                f = lambda z: b if z == a else a if z == b else z
                return (c, tuple(sorted((f(x), f(y)))))
            lex_leader(tau)

        def sigma(key):
            c, e = key
            return ({0: 0, 1: 2, 2: 1}[c], e)
        lex_leader(sigma)


# -- independent brute-force checker of a decoded model ----------------------
def check_model(n, supports, families, *, fprime=False, relax=None):
    """supports[c] = set of edges; families[c] = set of frozensets (|A|>=4).
    Returns a list of axiom violations (empty if the model satisfies AP')."""
    V = frozenset(range(n))
    bad = []

    def S(c, A):
        A = frozenset(A)
        if not A:
            return True
        if len(A) == 2:
            return tuple(sorted(A)) in supports[c]
        return A in families[c]

    def pms(c, A):
        return [M for M in perfect_matchings(sorted(A)) if all(tuple(sorted(e)) in supports[c] for e in M)]

    evens = [frozenset(A) for k in range(4, n + 1, 2) for A in itertools.combinations(sorted(V), k)]
    for c in range(3):
        if not S(c, V):
            bad.append(("H1", c))
        for A in evens:
            count = len(pms(c, A))
            if S(c, A) and count == 0:
                bad.append(("S", c, A))
            if relax != "no_forcing" and count == 1 and not S(c, A):
                bad.append(("F", c, A))
            for v in A:
                kids = [u for u in A if u != v and S(c, (v, u)) and S(c, A - {v, u})]
                if relax != "no_laplace" and S(c, A) and not kids:
                    bad.append(("L", c, A, v))
                if fprime and not S(c, A) and len(kids) == 1:
                    bad.append(("F'", c, A, v))
    for word in itertools.product(range(3), repeat=n):
        classes = [frozenset(v for v in V if word[v] == c) for c in range(3)]
        if any(len(A) % 2 for A in classes):
            continue
        nonempty = sum(1 for A in classes if A)
        if nonempty < 2 or (relax == "two_part_only" and nonempty == 3):
            continue
        if all(S(c, classes[c]) for c in range(3)):
            bad.append(("H2", tuple(sorted(map(sorted, classes)))))
    return bad


def decode(enc, model):
    pos = {l for l in model if l > 0}
    supports = {c: {e for e in enc.pairs if enc.g[(c, e)] in pos} for c in range(3)}
    families = {c: {A for A in enc.sets if enc.m[(c, A)] in pos} for c in range(3)}
    return supports, families


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--fprime", action="store_true")
    ap.add_argument("--normalize", action="store_true")
    ap.add_argument("--no-symmetry", action="store_true")
    ap.add_argument("--relax", choices=["two_part_only", "no_forcing", "no_laplace"])
    ap.add_argument("--top-matching", action="store_true",
                    help="extra hypothesis: every top-active graph E_c is a matching")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--proof", type=Path, help="write DIMACS to PROOF.cnf and a DRAT trace to PROOF.drat")
    args = ap.parse_args()
    t0 = time.time()
    enc = Encoder(args.n, fprime=args.fprime, normalize=args.normalize,
                  symmetry=not args.no_symmetry, relax=args.relax,
                  top_matching=args.top_matching)
    digest = hashlib.sha256()
    for clause in enc.cnf.clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    record = {
        "n": args.n, "fprime": args.fprime, "normalize": args.normalize,
        "symmetry": not args.no_symmetry, "relax": args.relax,
        "top_matching": args.top_matching,
        "variables": enc.pool.top, "clauses": len(enc.cnf.clauses),
        "rainbow_clauses": enc.rainbow, "cnf_sha256": digest.hexdigest(),
        "encode_seconds": round(time.time() - t0, 1), "solver": "CaDiCaL 1.5.3 via python-sat",
    }
    print(json.dumps(record), flush=True)
    t1 = time.time()
    if args.proof:
        args.proof.parent.mkdir(parents=True, exist_ok=True)
        cnf_path = args.proof.with_suffix(".cnf")
        enc.cnf.to_file(str(cnf_path))
        record["dimacs_file"] = str(cnf_path)
        record["dimacs_sha256"] = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    with Cadical153(bootstrap_with=enc.cnf.clauses, with_proof=bool(args.proof)) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
        if args.proof and not sat:
            drat_path = args.proof.with_suffix(".drat")
            with drat_path.open("w", encoding="ascii") as handle:
                for line in solver.get_proof():
                    handle.write(line + "\n")
            record["drat_file"] = str(drat_path)
            record["drat_sha256"] = hashlib.sha256(drat_path.read_bytes()).hexdigest()
            record["drat_bytes"] = drat_path.stat().st_size
    record["result"] = "SAT" if sat else "UNSAT"
    record["solve_seconds"] = round(time.time() - t1, 1)
    if sat:
        supports, families = decode(enc, model)
        violations = check_model(args.n, supports, families, fprime=args.fprime, relax=args.relax)
        record["model_supports"] = {str(c): sorted(map(list, supports[c])) for c in range(3)}
        record["model_families"] = {str(c): sorted(sorted(A) for A in families[c]) for c in range(3)}
        record["independent_check_violations"] = [str(b) for b in violations[:20]]
        record["independent_check"] = "PASS" if not violations else "FAIL"
    print(json.dumps({k: v for k, v in record.items() if not k.startswith("model_")}), flush=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(record, indent=1), encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
