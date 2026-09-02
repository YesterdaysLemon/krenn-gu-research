"""Primary verifier: support-level exclusion of all-diagonal witnesses at n = 6, 8.

Encodes the support abstraction (AP') of an all-diagonal witness as CNF:
  g[c][e]   : Z^c_e != 0
  m[c][A]   : haf(Z^c[A]) != 0 for even |A| >= 4  (2-sets are the g's)
  p[c][A,M] : every edge of the perfect matching M of A is present in colour c
with the proved necessary conditions
  (H1) m[c][V];
  (H2) for every ordered partition of V into even classes, at least two nonempty,
       some class has m false;
  (S)  m[c][A] -> some perfect matching of A is present;
  (F)  exactly one perfect matching of A present -> m[c][A];
  (L)  m[c][A] -> for every v in A some u in A with g[c][vu] and m[c][A-{v,u}].
Writes DIMACS with SHA-256, solves with CaDiCaL 1.5.3 (python-sat), and records
the sharpness relaxations at n = 8 (each single dropped ingredient is SAT).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical153


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def perfect_matchings(vs):
    vs = tuple(vs)
    if not vs:
        yield ()
        return
    a, rest = vs[0], vs[1:]
    for k, b in enumerate(rest):
        for m in perfect_matchings(rest[:k] + rest[k + 1:]):
            yield ((a, b),) + m


def build(n, *, two_part_only=False, no_forcing=False, no_laplace=False):
    pool = IDPool()
    cnf = CNF()
    V = tuple(range(n))
    pairs = [tuple(p) for p in itertools.combinations(V, 2)]
    g = {(c, e): pool.id(("g", c, e)) for c in range(3) for e in pairs}
    even_sets = [frozenset(A) for k in range(4, n + 1, 2) for A in itertools.combinations(V, k)]
    m = {(c, A): pool.id(("m", c, A)) for c in range(3) for A in even_sets}

    def mvar(c, A):
        A = frozenset(A)
        if not A:
            return None
        if len(A) == 2:
            return g[(c, tuple(sorted(A)))]
        return m[(c, A)]

    for c in range(3):
        for A in even_sets:
            As = tuple(sorted(A))
            pvars = []
            for M in perfect_matchings(As):
                pv = pool.id(("p", c, A, M))
                pvars.append(pv)
                edges = [g[(c, tuple(sorted(e)))] for e in M]
                for ev in edges:
                    cnf.append([-pv, ev])
                cnf.append([pv] + [-ev for ev in edges])
            mA = m[(c, A)]
            cnf.append([-mA] + pvars)                                   # (S)
            if not no_forcing:                                          # (F)
                for i, pv in enumerate(pvars):
                    cnf.append([-pv] + [pvars[j] for j in range(len(pvars)) if j != i] + [mA])
            if not no_laplace:                                          # (L)
                for v in As:
                    lits = []
                    for u in As:
                        if u == v:
                            continue
                        t = pool.id(("t", c, A, v, u))
                        lits.append(t)
                        cnf.append([-t, g[(c, tuple(sorted((v, u))))]])
                        mr = mvar(c, A - {v, u})
                        if mr is not None:
                            cnf.append([-t, mr])
                    cnf.append([-mA] + lits)
    for c in range(3):                                                  # (H1)
        cnf.append([m[(c, frozenset(V))]])
    rainbow = 0
    for word in itertools.product(range(3), repeat=n):                   # (H2)
        classes = [frozenset(v for v in V if word[v] == c) for c in range(3)]
        if any(len(A) % 2 for A in classes):
            continue
        nonempty = sum(1 for A in classes if A)
        if nonempty < 2 or (two_part_only and nonempty == 3):
            continue
        clause = [-mvar(c, classes[c]) for c in range(3) if classes[c]]
        cnf.append(clause)
        rainbow += 1
    return cnf, pool, g, rainbow


def decode_supports(model, g, n):
    pos = {l for l in model if l > 0}
    return {c: [e for e in itertools.combinations(range(n), 2) if g[(c, e)] in pos] for c in range(3)}


def run(n, out_dir, **flags):
    t0 = time.time()
    cnf, pool, g, rainbow = build(n, **flags)
    tag = "_".join([f"n{n}"] + [k for k, v in flags.items() if v]) or f"n{n}"
    dimacs = out_dir / f"all_diagonal_support_{tag}.cnf"
    cnf.to_file(str(dimacs))
    with Cadical153(bootstrap_with=cnf.clauses) as solver:
        sat = solver.solve()
        supports = decode_supports(solver.get_model(), g, n) if sat else None
    record = {
        "n": n, "flags": {k: v for k, v in flags.items() if v},
        "variables": pool.top, "clauses": len(cnf.clauses), "rainbow_clauses": rainbow,
        "dimacs_sha256": sha256_file(dimacs), "result": "SAT" if sat else "UNSAT",
        "seconds": round(time.time() - t0, 1),
    }
    if supports is not None:
        record["model_supports"] = {str(c): [list(e) for e in es] for c, es in supports.items()}
    dimacs.unlink()  # generated artifact; only its hash is kept
    print(json.dumps(record), flush=True)
    return record


def main() -> None:
    out_dir = Path("tmp")
    out_dir.mkdir(exist_ok=True)
    records = []
    records.append(run(6, out_dir))
    records.append(run(8, out_dir))
    for flag in ("two_part_only", "no_forcing", "no_laplace"):
        records.append(run(8, out_dir, **{flag: True}))
    main_results = {(r["n"], tuple(sorted(r["flags"]))): r["result"] for r in records}
    if main_results[(6, ())] != "UNSAT" or main_results[(8, ())] != "UNSAT":
        raise AssertionError("expected UNSAT for the full support abstraction at n = 6, 8")
    for flag in ("two_part_only", "no_forcing", "no_laplace"):
        if main_results[(8, (flag,))] != "SAT":
            raise AssertionError(f"expected SAT when dropping {flag} at n = 8")
    payload = {
        "verifier": Path(__file__).name,
        "verifier_sha256": sha256_file(Path(__file__)),
        "solver": "CaDiCaL 1.5.3 via python-sat",
        "records": records,
        "verified": True,
    }
    out = out_dir / "all_diagonal_support_level_verified.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print("VERIFIED: support abstraction UNSAT at n = 6, 8; each single relaxation SAT at n = 8")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"FAILED: {error}")
        sys.exit(1)
