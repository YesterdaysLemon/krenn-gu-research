#!/usr/bin/env python3
"""Bounded CEGAR: do two-term (BL) relations refute every n=6 physical support?

Experiment, not a proof.  The SAT side enumerates physical supports S (sets of
nonzero entries W_ij[a,b]) satisfying the exact full-word single-term
conditions

  * every constant word has at least one live perfect matching;
  * no mixed word has exactly one live perfect matching;

and, with --killers, the column-killer theorem at the physical level
(THREE_COLOUR_HYPERPLANE_ANNIHILATION consequence: for every vertex v and
colour c some block W_vu, rows = colour at v, has only its column c nonzero).
Optionally |S| <= --kmax.  Each model is tested by the full-word
binomial-linear closure (``binomial_linear_closure.py``).  A contradiction is
shrunk to a small set of words; the cut fixes the exact live/dead status of
every matching at those words (positive literals for live monomials, one zero
entry per dead matching), and all vertex/common-colour images are added.
A support on which the closure stops without contradiction is reported as a
BL survivor (not a weight realization).
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).resolve().parent))
from binomial_linear_closure import Geometry, closure  # noqa: E402


def oriented(geo, v, u, a, b):
    """Entry index of W_vu[a,b] with colour a at v and b at u."""
    return geo.index[(v, u, a, b)] if v < u else geo.index[(u, v, b, a)]


def build(geo, killers):
    clauses = []
    nvar = len(geo.entries)
    for wi, w in enumerate(geo.words):
        lits = []
        for m in geo.terms[wi]:
            nvar += 1
            v = nvar
            for k in m:
                clauses.append([-v, k + 1])
            clauses.append([v] + [-(k + 1) for k in m])
            lits.append(v)
        if geo.pure(w):
            clauses.append(lits)
        else:
            for v in lits:
                clauses.append([-v] + [u for u in lits if u != v])
    if killers:
        n = geo.n
        for v in range(n):
            for c in range(3):
                options = []
                for u in range(n):
                    if u == v:
                        continue
                    nvar += 1
                    kv = nvar
                    options.append(kv)
                    for a in range(3):
                        for b in range(3):
                            if b != c:
                                clauses.append([-kv, -(oriented(geo, v, u, a, b) + 1)])
                    clauses.append([-kv] + [oriented(geo, v, u, a, c) + 1 for a in range(3)])
                clauses.append(options)
    return nvar, clauses


def symmetries(geo):
    out = []
    for perm in itertools.permutations(range(geo.n)):
        for cp in itertools.permutations(range(3)):
            table = []
            for (i, j, a, b) in geo.entries:
                pi, pj, ca, cb = perm[i], perm[j], cp[a], cp[b]
                if pi > pj:
                    pi, pj, ca, cb = pj, pi, cb, ca
                table.append(geo.index[(pi, pj, ca, cb)])
            out.append(table)
    return out


def guard(geo, support, words):
    pos, neg = set(), set()
    for wi in words:
        for m in geo.terms[wi]:
            if all(k in support for k in m):
                pos.update(m)
    for wi in words:
        for m in geo.terms[wi]:
            if all(k in support for k in m):
                continue
            zeros = [k for k in m if k not in support]
            pick = next((k for k in zeros if k in neg), zeros[0])
            neg.add(pick)
    return pos, neg


def shrink(geo, support, words):
    words = list(words)
    chunk = max(1, len(words) // 2)
    while chunk >= 1:
        i = 0
        while i < len(words):
            trial = words[:i] + words[i + chunk:]
            if trial and closure(geo, support, trial)[0] == "CONTRADICTION":
                words = trial
            else:
                i += chunk
        chunk //= 2
    return words


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--killers", action="store_true")
    ap.add_argument("--kmax", type=int, default=None)
    ap.add_argument("--max-iterations", type=int, default=100000)
    ap.add_argument("--seconds", type=float, default=1e9)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    if args.output.exists():
        raise SystemExit("output path must be new")
    started = time.monotonic()
    geo = Geometry(args.n)
    nvar, clauses = build(geo, args.killers)
    if args.kmax is not None:
        card = CardEnc.atmost(lits=list(range(1, len(geo.entries) + 1)), bound=args.kmax,
                              top_id=nvar, encoding=EncType.seqcounter)
        clauses += card.clauses
    syms = symmetries(geo)
    solver = Solver(name="cadical153", bootstrap_with=clauses)
    report = {"n": args.n, "killers": args.killers, "kmax": args.kmax, "cuts": [], "status": "RUNNING"}
    it = 0
    seen = set()
    while True:
        if time.monotonic() - started > args.seconds:
            report["status"] = "TIME_BOUND"
            break
        if it >= args.max_iterations:
            report["status"] = "ITERATION_BOUND"
            break
        if not solver.solve():
            report["status"] = "UNSAT_AFTER_BL_CUTS"
            break
        it += 1
        model = solver.get_model()
        support = {e for e in range(len(geo.entries)) if model[e] > 0}
        status, info = closure(geo, support)
        if status != "CONTRADICTION":
            report["status"] = "BL_SURVIVOR"
            report["survivor"] = {"size": len(support), "closure": {a: str(b) for a, b in info.items()},
                                  "entries": [list(geo.entries[e]) for e in sorted(support)]}
            print("SURVIVOR", len(support), info, flush=True)
            break
        informative = [wi for wi in range(len(geo.words))
                       if geo.pure(geo.words[wi]) or
                       sum(all(x in support for x in m) for m in geo.terms[wi]) >= 2]
        words = shrink(geo, support, informative)
        pos, neg = guard(geo, support, words)
        cut = [-(e + 1) for e in sorted(pos)] + [e + 1 for e in sorted(neg)]
        report["cuts"].append({"support_size": len(support), "kind": info.get("kind"),
                               "words": ["".join(map(str, geo.words[w])) for w in words],
                               "nonzero": [geo.name(e) for e in sorted(pos)],
                               "zero": [geo.name(e) for e in sorted(neg)]})
        for table in syms:
            img = tuple(sorted((-(table[-lit - 1] + 1) if lit < 0 else table[lit - 1] + 1) for lit in cut))
            if img not in seen:
                seen.add(img)
                solver.add_clause(list(img))
        print("iter", it, "|S|", len(support), "kind", info.get("kind"), "words", len(words),
              "cut", len(cut), "images", len(seen), round(time.monotonic() - started, 1), flush=True)
    report["iterations"] = it
    report["unique_cut_images"] = len(seen)
    report["seconds"] = round(time.monotonic() - started, 1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k2: v for k2, v in report.items() if k2 not in ("cuts", "survivor")}), flush=True)


if __name__ == "__main__":
    sys.exit(main())
