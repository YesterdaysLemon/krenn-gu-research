"""Exploratory relaxations of AP' with one colour's support graph a perfect matching.

Research tool, not a verifier.  It reuses the WB4 encoder
(``explore_all_diagonal_support_level_ap_prime_bounded_search.Encoder``) and
adds the hypothesis that the colour-0 support graph G_0 is the perfect
matching M_0 = {01, 23, ..., (n-2)(n-1)}.  This is without loss of generality
for the statement "G_0 is a perfect matching" (relabel the vertices); no
lex-leader symmetry breaking is used, so asymmetric relaxations stay sound.

Optional relaxations, per colour c in {1, 2} (comma-separated key=value):

  fmax=k   impose forcing (F) only on sets of size <= k (2-sets are edges);
  lmin=k   impose Laplace accessibility (L) only on sets of size >= k.

Optional rainbow filters keep only some (H2) partitions (U, A_1, A_2) with U
an M_0-union (when G_0 = M_0 the other partitions are implied by (S)):

  all       every partition (default; equivalent to full (H2));
  onesmall  min(|A_1|, |A_2|) <= 2;
  onesmall4 min(|A_1|, |A_2|) <= 4.

An UNSAT answer is evidence at one order only and carries no proof trace; a
SAT answer for a relaxation says only that the relaxation has a model at that
order (it is not decoded or re-checked).

Usage: python explore_..._matching_colour_relaxations.py N [--top]
       [--relax1 SPEC] [--relax2 SPEC] [--filter NAME]
"""

from __future__ import annotations

import argparse
import itertools
import json
import time

from pysat.solvers import Cadical153

from explore_all_diagonal_support_level_ap_prime_bounded_search import Encoder


def parse(spec):
    return {k: int(v) for k, v in (o.split("=") for o in (spec or "").split(",") if o)}


FILTERS = {
    "all": lambda U, A1, A2: True,
    "onesmall": lambda U, A1, A2: min(len(A1), len(A2)) <= 2,
    "onesmall4": lambda U, A1, A2: min(len(A1), len(A2)) <= 4,
}


class MatchingColourEncoder(Encoder):
    def __init__(self, n, relax_map, rb_filter, **kw):
        self.relax_map = {c: parse(s) for c, s in relax_map.items()}
        self.rb_filter = rb_filter
        self.l_dropped = 0
        super().__init__(n, symmetry=False, **kw)
        for e in self.pairs:                      # G_0 = M_0
            if not (e[0] % 2 == 0 and e[1] == e[0] + 1):
                self.cnf.append([-self.g[(0, e)]])

    def _colour(self, c):
        opts = self.relax_map.get(c, {})
        fmax = opts.get("fmax", 10 ** 6)
        lmin = opts.get("lmin", 0)
        start = len(self.cnf.clauses)
        self.relax = "no_forcing"
        super()._colour(c)
        self.relax = None
        drop = set()
        for A in self.sets:
            if len(A) < lmin:
                for v in A:
                    drop.add(tuple([-self.m[(c, A)]]
                                   + [self.t[(c, A, v, u)] for u in sorted(A) if u != v]))
        if drop:
            kept = [cl for cl in self.cnf.clauses[start:] if tuple(cl) not in drop]
            self.l_dropped += len(self.cnf.clauses) - start - len(kept)
            self.cnf.clauses = self.cnf.clauses[:start] + kept
        for A in self.sets:
            if len(A) <= fmax:
                self.cnf.append([-self.uq[(c, A)], self.m[(c, A)]])

    def _rainbow(self):
        n = self.n
        M0 = [frozenset((2 * i, 2 * i + 1)) for i in range(n // 2)]

        def closed(A):
            return all(e <= A or not (e & A) for e in M0)

        for word in itertools.product(range(3), repeat=n):
            cl = [frozenset(v for v in self.V if word[v] == c) for c in range(3)]
            if any(len(A) % 2 for A in cl) or sum(1 for A in cl if A) < 2:
                continue
            if not closed(cl[0]) or not self.rb_filter(*cl):
                continue
            self.cnf.append([-self.mvar(c, cl[c]) for c in range(3) if cl[c]])
            self.rainbow += 1


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--top", action="store_true",
                    help="also impose the WB4 top-matching hypothesis")
    ap.add_argument("--relax1", default="")
    ap.add_argument("--relax2", default="")
    ap.add_argument("--filter", default="all", choices=sorted(FILTERS))
    args = ap.parse_args()
    t0 = time.time()
    enc = MatchingColourEncoder(args.n, {1: args.relax1, 2: args.relax2}, FILTERS[args.filter],
                                top_matching=args.top)
    with Cadical153(bootstrap_with=enc.cnf.clauses) as solver:
        sat = solver.solve()
    print(json.dumps({
        "n": args.n, "G0_perfect_matching": True, "top_matching": args.top,
        "relax1": args.relax1, "relax2": args.relax2, "filter": args.filter,
        "variables": enc.pool.top, "clauses": len(enc.cnf.clauses),
        "laplace_clauses_dropped": enc.l_dropped,
        "result": "SAT" if sat else "UNSAT", "seconds": round(time.time() - t0, 1),
        "solver": "CaDiCaL 1.5.3 via python-sat",
    }), flush=True)


if __name__ == "__main__":
    main()
