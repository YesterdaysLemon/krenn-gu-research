"""Independent audit: support-level exclusion of all-diagonal witnesses at n = 6, 8.

Independent of the primary in encoding and solver:
  * no explicit support clause: the Laplace clauses imply support inductively;
  * forcing encoded through a cardinality constraint on present perfect
    matchings (exactly one present -> m), via python-sat's CardEnc;
  * rainbow clauses generated from set partitions rather than colour words;
  * solved with Glucose 4.1 instead of CaDiCaL.
Also checks the maximum-D-degree-four restriction at n = 8.  This is a
finite consequence of the unrestricted n = 8 result, not an all-order
consequence of WB1: WB1's numerical witness argument does not transfer to
the support abstraction through the one-way bridge.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from functools import lru_cache
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose4


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matchings_bitmask(vertices):
    vertices = tuple(sorted(vertices))
    idx = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)

    @lru_cache(maxsize=None)
    def rec(mask):
        if mask == (1 << n) - 1:
            return [()]
        first = (~mask & (mask + 1)).bit_length() - 1
        out = []
        for v in range(first + 1, n):
            if mask >> v & 1:
                continue
            for tail in rec(mask | 1 << first | 1 << v):
                out.append(((vertices[first], vertices[v]),) + tail)
        return out

    return rec(0)


def even_partitions(V):
    """Ordered partitions (A0, A1, A2) of V into even classes, at least two nonempty."""
    V = tuple(V)
    for k0 in range(0, len(V) + 1, 2):
        for A0 in itertools.combinations(V, k0):
            rest = [v for v in V if v not in A0]
            for k1 in range(0, len(rest) + 1, 2):
                for A1 in itertools.combinations(rest, k1):
                    A2 = tuple(v for v in rest if v not in A1)
                    if sum(1 for A in (A0, A1, A2) if A) >= 2:
                        yield frozenset(A0), frozenset(A1), frozenset(A2)


def build(n, max_degree=None):
    pool = IDPool()
    cnf = CNF()
    V = tuple(range(n))
    pairs = [tuple(p) for p in itertools.combinations(V, 2)]
    g = {(c, e): pool.id(("G", c, e)) for c in range(3) for e in pairs}
    sets = [frozenset(A) for k in range(4, n + 1, 2) for A in itertools.combinations(V, k)]
    h = {(c, A): pool.id(("H", c, A)) for c in range(3) for A in sets}

    def hv(c, A):
        if not A:
            return None
        if len(A) == 2:
            return g[(c, tuple(sorted(A)))]
        return h[(c, frozenset(A))]

    for c in range(3):
        for A in sets:
            # Laplace: h -> for each v exists u: g(vu) & h(A - vu)
            for v in sorted(A):
                choices = []
                for u in sorted(A):
                    if u == v:
                        continue
                    y = pool.id(("Y", c, A, v, u))
                    choices.append(y)
                    cnf.append([-y, g[(c, tuple(sorted((v, u))))]])
                    rest = hv(c, A - {v, u})
                    if rest is not None:
                        cnf.append([-y, rest])
                cnf.append([-h[(c, A)]] + choices)
            # forcing via cardinality: present(M) vars, exactly one present -> h
            present = []
            for M in matchings_bitmask(A):
                q = pool.id(("Q", c, A, M))
                present.append(q)
                lits = [g[(c, tuple(sorted(e)))] for e in M]
                for lit in lits:
                    cnf.append([-q, lit])
                cnf.append([q] + [-lit for lit in lits])
            # z <-> (sum present == 1); then z -> h
            z = pool.id(("Z", c, A))
            eq = CardEnc.equals(lits=present, bound=1, vpool=pool, encoding=EncType.seqcounter)
            # eq.clauses encode sum == 1 unconditionally; guard them by -z:
            for clause in eq.clauses:
                cnf.append([-z] + clause)
            # converse: sum == 1 -> z, i.e. for each M: (q_M and no other q) -> z
            for i, q in enumerate(present):
                cnf.append([-q] + [present[j] for j in range(len(present)) if j != i] + [z])
            cnf.append([-z, h[(c, A)]])
    for c in range(3):
        cnf.append([h[(c, frozenset(V))]])
    rainbow = 0
    for A0, A1, A2 in even_partitions(V):
        clause = [-lit for lit in (hv(0, A0), hv(1, A1), hv(2, A2)) if lit is not None]
        cnf.append(clause)
        rainbow += 1
    if max_degree is not None:
        d = {}
        for e in pairs:
            dv = pool.id(("D", e))
            d[e] = dv
            for c in range(3):
                cnf.append([-g[(c, e)], dv])
            cnf.append([-dv] + [g[(c, e)] for c in range(3)])
        for v in V:
            card = CardEnc.atmost(lits=[d[e] for e in pairs if v in e], bound=max_degree,
                                  vpool=pool, encoding=EncType.seqcounter)
            cnf.extend(card.clauses)
    return cnf, pool, rainbow


def run(n, max_degree=None):
    t0 = time.time()
    cnf, pool, rainbow = build(n, max_degree)
    with Glucose4(bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
    rec = {"n": n, "max_degree": max_degree, "variables": pool.top, "clauses": len(cnf.clauses),
           "rainbow_clauses": rainbow, "result": "SAT" if sat else "UNSAT",
           "seconds": round(time.time() - t0, 1)}
    print(json.dumps(rec), flush=True)
    return rec


def main() -> None:
    records = [run(6), run(8, max_degree=4), run(8)]
    if any(r["result"] != "UNSAT" for r in records):
        raise AssertionError("audit expected UNSAT in every run")
    out_dir = Path("tmp")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "all_diagonal_support_level_audit.json"
    out.write_text(json.dumps({"audit": Path(__file__).name, "audit_sha256": sha256_file(Path(__file__)),
                               "solver": "Glucose 4.1 via python-sat", "records": records,
                               "verified": True}, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print("AUDIT PASS: independent encoding and solver confirm UNSAT at n = 6, 8")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"AUDIT FAILED: {error}")
        sys.exit(1)
