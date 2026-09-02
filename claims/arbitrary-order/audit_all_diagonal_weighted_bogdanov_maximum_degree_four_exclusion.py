"""Independent audit of the all-diagonal weighted-Bogdanov degree-four exclusion.

Differences from the primary verifier: hafnians by Laplace recursion with
memoization instead of matching enumeration; perfect matchings by bitmask
dynamic programming; the noncancellation lemma checked against the explicit
component-factorization formula; Bogdanov checked by counting perfect
matchings of the cubic union (at least four); and the factorization (F)
controlled numerically with complex floating-point weights via einsum.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import numpy as np


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hafnian_laplace(Z, vertices):
    """Exact hafnian by Laplace recursion on the first vertex."""
    vertices = tuple(sorted(vertices))

    @lru_cache(maxsize=None)
    def rec(vs):
        if not vs:
            return Fraction(1)
        if len(vs) % 2:
            return Fraction(0)
        first, rest = vs[0], vs[1:]
        total = Fraction(0)
        for k, u in enumerate(rest):
            w = Z[first][u]
            if w:
                total += w * rec(rest[:k] + rest[k + 1:])
        return total

    return rec(vertices)


def pm_bitmask(n, edges):
    edges = {tuple(sorted(e)) for e in edges}

    @lru_cache(maxsize=None)
    def rec(mask):
        if mask == (1 << n) - 1:
            return [()]
        first = (~mask & (mask + 1)).bit_length() - 1
        out = []
        for v in range(first + 1, n):
            if mask >> v & 1 or (first, v) not in edges:
                continue
            for tail in rec(mask | 1 << first | 1 << v):
                out.append(((first, v),) + tail)
        return out

    return rec(0)


def rnd(rng):
    v = 0
    while v == 0:
        v = rng.randint(-6, 6)
    return Fraction(v, rng.randint(1, 3))


def audit_noncancellation(rng, n, trials):
    """Compare brute-force hafnians with the path/cycle factorization formula."""
    done = 0
    for _ in range(trials):
        verts = list(range(n)); rng.shuffle(verts)
        P = {tuple(sorted((verts[2 * k], verts[2 * k + 1]))) for k in range(n // 2)}
        pool = list(range(n)); rng.shuffle(pool)
        R = set()
        while len(pool) >= 2:
            e = tuple(sorted((pool.pop(), pool.pop())))
            if e not in P and rng.random() < 0.7:
                R.add(e)
        Z = [[Fraction(0)] * n for _ in range(n)]
        for (i, j) in P | R:
            Z[i][j] = Z[j][i] = rnd(rng)
        # components of P + R
        adj = {v: set() for v in range(n)}
        for (i, j) in P | R:
            adj[i].add(j); adj[j].add(i)
        seen, comps = set(), []
        for v in range(n):
            if v in seen:
                continue
            stack, comp = [v], set()
            while stack:
                x = stack.pop()
                if x in comp:
                    continue
                comp.add(x); stack.extend(adj[x] - comp)
            seen |= comp; comps.append(comp)
        # factorization formula for haf(V)
        formula = Fraction(1)
        for comp in comps:
            pe = [e for e in P if e[0] in comp]
            re = [e for e in R if e[0] in comp]
            wp = Fraction(1)
            for (i, j) in pe:
                wp *= Z[i][j]
            is_cycle = len(re) == len(pe)  # every vertex has R-degree one
            if is_cycle:
                wr = Fraction(1)
                for (i, j) in re:
                    wr *= Z[i][j]
                formula *= wp + wr
            else:
                formula *= wp
        total = hafnian_laplace(Z, range(n))
        if total != formula:
            raise AssertionError("component factorization formula disagrees with hafnian")
        if total == 0:
            continue
        for size in range(2, n + 1, 2):
            for A in itertools.combinations(range(n), size):
                sub = {e for e in P | R if e[0] in A and e[1] in A}
                if pm_bitmask(len(A), {(A.index(i), A.index(j)) for (i, j) in sub}) and hafnian_laplace(Z, A) == 0:
                    raise AssertionError("noncancellation failed")
        done += 1
    if done == 0:
        raise AssertionError("no instance with nonzero total")
    return done


def audit_odd_component(rng, n=8, trials=6):
    for _ in range(trials):
        Z = [[Fraction(0)] * n for _ in range(n)]
        k = rng.choice([3, 5])  # odd cycle length
        cyc = list(range(k))
        for t in range(k):
            i, j = cyc[t], cyc[(t + 1) % k]
            Z[i][j] = Z[j][i] = rnd(rng)
        for i in range(k, n):
            for j in range(i + 1, n):
                if rng.random() < 0.6:
                    Z[i][j] = Z[j][i] = rnd(rng)
        if hafnian_laplace(Z, range(n)) != 0:
            raise AssertionError("odd component with nonzero total hafnian")
    return trials


def audit_bogdanov(n):
    pms = [frozenset(m) for m in pm_bitmask(n, {(i, j) for i in range(n) for j in range(i + 1, n)})]
    count = 0
    for a, b, c in itertools.combinations(range(len(pms)), 3):
        if pms[a] & pms[b] or pms[a] & pms[c] or pms[b] & pms[c]:
            continue
        edges = pms[a] | pms[b] | pms[c]
        count += 1
        if len(pm_bitmask(n, edges)) < 4:
            raise AssertionError(f"n={n}: three-matching cubic graph with fewer than four perfect matchings")
    return count


def audit_factorization_numeric(rng, n=6, trials=3):
    letters = "abcdefgh"
    pms = pm_bitmask(n, {(i, j) for i in range(n) for j in range(i + 1, n)})
    worst = 0.0
    for _ in range(trials):
        Z = np.zeros((3, n, n), complex)
        for c in range(3):
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < 0.7:
                        w = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
                        Z[c, i, j] = Z[c, j, i] = w
        W = {(i, j): np.diag(Z[:, i, j]) for i in range(n) for j in range(i + 1, n)}
        T = np.zeros((3,) * n, complex)
        for m in pms:
            sub = ",".join(letters[i] + letters[j] for (i, j) in m)
            T += np.einsum(sub + "->" + letters[:n], *[W[e] for e in m])
        for word in itertools.product(range(3), repeat=n):
            prod = 1.0 + 0j
            for c in range(3):
                cls = [v for v in range(n) if word[v] == c]
                if cls:
                    Zc = [[Fraction(0)] * n for _ in range(n)]  # placeholder, numeric below
                    sub_pms = pm_bitmask(len(cls), {(a, b) for a in range(len(cls)) for b in range(a + 1, len(cls))})
                    val = 0j
                    for m in sub_pms:
                        term = 1.0 + 0j
                        for (a, b) in m:
                            term *= Z[c, cls[a], cls[b]]
                        val += term
                    prod *= val
            worst = max(worst, abs(T[word] - prod))
    if worst > 1e-9:
        raise AssertionError(f"numeric factorization control off by {worst}")
    return worst


def main() -> None:
    rng = random.Random(1234)
    report = {
        "noncancellation_n6": audit_noncancellation(rng, 6, 30),
        "noncancellation_n8": audit_noncancellation(rng, 8, 6),
        "odd_component_trials": audit_odd_component(rng),
        "bogdanov_triples_n6": audit_bogdanov(6),
        "bogdanov_triples_n8": audit_bogdanov(8),
        "numeric_factorization_max_error": audit_factorization_numeric(rng),
    }
    for k, v in report.items():
        print(f"{k}: {v}")
    out_dir = Path("tmp"); out_dir.mkdir(exist_ok=True)
    out = out_dir / "all_diagonal_degree_four_audit.json"
    out.write_text(json.dumps({"audit": Path(__file__).name, "audit_sha256": sha256_file(Path(__file__)),
                               "report": report, "verified": True}, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print("AUDIT PASS: independent routes confirm the lemma checks")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"AUDIT FAILED: {error}")
        sys.exit(1)
