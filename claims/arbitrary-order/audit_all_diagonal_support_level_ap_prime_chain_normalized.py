"""Independent audit encoding for AP' under the chain normalization.

Differs from the exploratory search in representation and solver: it lists
perfect matchings explicitly (the WB2 primary representation: one variable per
present perfect matching of each even set) instead of recursive matchability,
encodes (F) and (S) through those variables, enumerates rainbow clauses from
set partitions instead of colour words, uses no lex-leader clauses, and solves
with Glucose 4.1 instead of CaDiCaL.  The only shared ingredient is the
chain normalization of Lemma 2: {2i-2,2i-1} in G_0 and {2i,...,n-1} in S_0.

Usage: python audit_...py N [--fprime] [--proof PREFIX]
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
from pysat.solvers import Glucose4


def matchings(vs):
    vs = tuple(vs)
    if not vs:
        yield ()
        return
    a, rest = vs[0], vs[1:]
    for k, b in enumerate(rest):
        for tail in matchings(rest[:k] + rest[k + 1:]):
            yield ((a, b),) + tail


def even_partitions(V, parts=3):
    """Ordered partitions of V into `parts` classes, each of even size."""
    V = tuple(V)
    for word in itertools.product(range(parts), repeat=len(V)):
        classes = tuple(frozenset(v for v, w in zip(V, word) if w == c) for c in range(parts))
        if all(len(A) % 2 == 0 for A in classes):
            yield classes


def build(n, fprime):
    V = tuple(range(n))
    pool, cnf = IDPool(), CNF()
    pairs = [tuple(p) for p in itertools.combinations(V, 2)]
    g = {(c, e): pool.id(("g", c, e)) for c in range(3) for e in pairs}
    sets = [frozenset(A) for k in range(4, n + 1, 2) for A in itertools.combinations(V, k)]
    s = {(c, A): pool.id(("s", c, A)) for c in range(3) for A in sets}

    def svar(c, A):
        A = frozenset(A)
        if len(A) == 0:
            return None
        if len(A) == 2:
            return g[(c, tuple(sorted(A)))]
        return s[(c, A)]

    for c in range(3):
        for A in sets:
            As = sorted(A)
            present = []
            for M in matchings(As):
                p = pool.id(("p", c, A, M))
                present.append(p)
                es = [g[(c, e)] for e in M]
                for ev in es:
                    cnf.append([-p, ev])
                cnf.append([p] + [-ev for ev in es])
            sA = s[(c, A)]
            cnf.append([-sA] + present)                                     # (S)
            for i, p in enumerate(present):                                  # (F)
                cnf.append([-p, sA] + [q for j, q in enumerate(present) if j != i])
            for v in As:                                                     # (L), (F')
                kids = []
                for u in As:
                    if u == v:
                        continue
                    b = pool.id(("b", c, A, v, u))
                    kids.append(b)
                    sub = svar(c, A - {v, u})
                    cnf.append([-b, g[(c, (min(v, u), max(v, u)))]])
                    cnf.append([-b, sub])
                    cnf.append([b, -g[(c, (min(v, u), max(v, u)))], -sub])
                cnf.append([-sA] + kids)
                if fprime:
                    for b in kids:
                        cnf.append([sA, -b] + [o for o in kids if o != b])
        cnf.append([s[(c, frozenset(V))]])                                   # (H1)
    rainbow = 0
    for classes in even_partitions(V):                                       # (H2)
        if sum(1 for A in classes if A) < 2:
            continue
        cnf.append([-svar(c, classes[c]) for c in range(3) if classes[c]])
        rainbow += 1
    for i in range(1, n // 2 + 1):                                           # chain normalization
        cnf.append([g[(0, (2 * i - 2, 2 * i - 1))]])
        rest = frozenset(range(2 * i, n))
        if len(rest) >= 4:
            cnf.append([s[(0, rest)]])
    return cnf, pool, rainbow


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--fprime", action="store_true")
    ap.add_argument("--proof", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    cnf, pool, rainbow = build(args.n, args.fprime)
    record = {"n": args.n, "fprime": args.fprime, "variables": pool.top, "clauses": len(cnf.clauses),
              "rainbow_clauses": rainbow, "encode_seconds": round(time.time() - t0, 1),
              "solver": "Glucose 4.1 via python-sat", "encoding": "explicit perfect-matching listing"}
    if args.proof:
        args.proof.parent.mkdir(parents=True, exist_ok=True)
        cnf_path = args.proof.with_suffix(".cnf")
        cnf.to_file(str(cnf_path))
        record["dimacs_sha256"] = hashlib.sha256(cnf_path.read_bytes()).hexdigest()
    print(json.dumps(record), flush=True)
    t1 = time.time()
    with Glucose4(bootstrap_with=cnf.clauses, with_proof=bool(args.proof)) as solver:
        sat = solver.solve()
        if args.proof and not sat:
            drat_path = args.proof.with_suffix(".drat")
            with drat_path.open("w", encoding="ascii") as handle:
                for line in solver.get_proof():
                    handle.write(line + "\n")
            record["drat_sha256"] = hashlib.sha256(drat_path.read_bytes()).hexdigest()
            record["drat_bytes"] = drat_path.stat().st_size
    record["result"] = "SAT" if sat else "UNSAT"
    record["solve_seconds"] = round(time.time() - t1, 1)
    print(json.dumps(record), flush=True)
    if args.out:
        args.out.write_text(json.dumps(record, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
