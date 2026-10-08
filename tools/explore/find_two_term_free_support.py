#!/usr/bin/env python3
"""Find a physical support with no two-term full-word fibre (BL-inert exhibit).

Experiment.  SAT for a support S at order n such that

  * every constant word has at least one live perfect matching;
  * every mixed word has 0 or at least 3 live perfect matchings;
  * (--killers) for every vertex v and colour c some block W_vu has only its
    column c (colour at u) nonzero, with a nonzero entry in that column.

By the BL-inertness criterion in
claims/arbitrary-order/TWO_TERM_RELATION_CLOSURE_THEOREMS.md, the full-word
binomial-linear closure derives no contradiction and no binomial on such S.
The model is re-checked by brute force and by running the closure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).resolve().parent))
from binomial_linear_closure import Geometry, closure  # noqa: E402
from bl_support_cegar import oriented  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--killers", action="store_true")
    ap.add_argument("--kmax", type=int, default=None)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args(argv)
    geo = Geometry(args.n)
    clauses = []
    nvar = len(geo.entries)
    for wi, w in enumerate(geo.words):
        lits = []
        for m in geo.terms[wi]:
            nvar += 1
            for k in m:
                clauses.append([-nvar, k + 1])
            clauses.append([nvar] + [-(k + 1) for k in m])
            lits.append(nvar)
        if geo.pure(w):
            clauses.append(lits)
        else:
            # forbid exactly one and exactly two live matchings
            for x in lits:
                clauses.append([-x] + [u for u in lits if u != x])
            for i, x in enumerate(lits):
                for y in lits[i + 1:]:
                    clauses.append([-x, -y] + [u for u in lits if u not in (x, y)])
    if args.killers:
        for v in range(geo.n):
            for c in range(3):
                options = []
                for u in range(geo.n):
                    if u == v:
                        continue
                    nvar += 1
                    options.append(nvar)
                    for a in range(3):
                        for b in range(3):
                            if b != c:
                                clauses.append([-nvar, -(oriented(geo, v, u, a, b) + 1)])
                    clauses.append([-nvar] + [oriented(geo, v, u, a, c) + 1 for a in range(3)])
                clauses.append(options)
    if args.kmax is not None:
        card = CardEnc.atmost(lits=list(range(1, len(geo.entries) + 1)), bound=args.kmax,
                              top_id=nvar, encoding=EncType.seqcounter)
        clauses += card.clauses
    with Solver(name="cadical153", bootstrap_with=clauses) as s:
        sat = s.solve()
        if not sat:
            print(json.dumps({"n": args.n, "killers": args.killers, "kmax": args.kmax, "result": "UNSAT"}))
            return 0
        model = s.get_model()
    support = sorted(e for e in range(len(geo.entries)) if model[e] > 0)
    S = set(support)
    hist = {}
    for wi, w in enumerate(geo.words):
        cnt = sum(all(k in S for k in m) for m in geo.terms[wi])
        hist[cnt] = hist.get(cnt, 0) + 1
        assert (cnt >= 1) if geo.pure(w) else (cnt == 0 or cnt >= 3)
    if args.killers:
        for v in range(geo.n):
            for c in range(3):
                assert any(
                    all(oriented(geo, v, u, a, b) not in S for a in range(3) for b in range(3) if b != c)
                    and any(oriented(geo, v, u, a, c) in S for a in range(3))
                    for u in range(geo.n) if u != v), (v, c)
    status, info = closure(geo, S)
    out = {"n": args.n, "killers": args.killers, "kmax": args.kmax, "result": "SAT",
           "size": len(support), "fibre_histogram": dict(sorted(hist.items())),
           "closure": status, "closure_info": {k: str(v) for k, v in info.items()},
           "entries": [list(geo.entries[e]) for e in support]}
    print(json.dumps({k: v for k, v in out.items() if k != "entries"}))
    if args.output:
        if args.output.exists():
            raise SystemExit("output path must be new")
        args.output.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
