#!/usr/bin/env python3
"""Exact Macaulay search for monomial certificates on the 51-entry six-vertex survivor.

Scope: an exact finite computation on one fixed physical support at n = 6.
The support is tests/fixtures/bl_full_word_survivor_n6_51.json (the full-word
BL survivor); the holonomy-model survivor of
docs/strategy/holonomy-support-model-2026-10-08.md is checked to be the same
support up to a vertex relabelling and a common colour permutation, so one
computation covers both.  The six-vertex exclusion is already a theorem; this
script only measures the *shape and degree* of the cheapest polynomial
certificate of non-realizability.  It is not a new exclusion.

Setting.  Every supported entry W_ij[a,b] is an unknown; unsupported entries
are 0.  For a word w the equation is E_w = T(w) (mixed w) or T(w) - 1
(constant w).  A *degree-D certificate* is an identity

    sum_w g_w E_w = c * mu,      c in Q \\ {0},  mu a monomial in the unknowns,

with every g_w of degree <= D in the unknowns.  On the torus (all supported
entries nonzero) such an identity is a contradiction, so it certifies that no
witness has exactly this support.  The search is a Macaulay-matrix test:
the products m * E_w (m a monomial, deg m <= D) are split into blocks by the
multigrading of the vertex-colour torus (W_ij[a,b] has degree e_(i,a)+e_(j,b);
for the full system the three constant-word degrees are quotiented out so
that T(c) - 1 is homogeneous), and in each block a monomial lies in the row
span iff some row of the exact reduced row echelon form over Q is a unit
vector.  All arithmetic is exact (python-flint fmpq_mat).

Modes:
  --system slice   the 27 words with (w1,w4,w5) = (2,0,1) (the 3-vs-3 cut
                   {0,2,3} | {1,4,5}); homogeneous, so deg m = D exactly.
  --system full    all 108 nonzero mixed equations and the 3 constant ones.

Run:
    python claims/finite/n06/search_51_entry_survivor_multilinear_certificates.py --system slice --max-degree 3
    python claims/finite/n06/search_51_entry_survivor_multilinear_certificates.py --system full --max-degree 2
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

import flint  # noqa: E402

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "bl_full_word_survivor_n6_51.json"

# Holonomy-model survivor, transcribed from Section 5.4 of
# docs/strategy/holonomy-support-model-2026-10-08.md ("ij: ab" = colour a at i,
# colour b at j).
HOLONOMY_SURVIVOR = (
    "01: ALL|02: 00 10 20|03: ALL|04: 22|05: 01 11 21|12: 00 10 20|13: ALL|"
    "14: 02 12 22|15: 11|23: 00|24: 11|25: 22|34: 02 12 22|35: 01 11 21|45: 00"
)

N = 6
SLICE_PIN = {1: 2, 4: 0, 5: 1}  # outer vertex -> pinned colour, fixture labelling


def parse_blocks(spec: str) -> set:
    out = set()
    for tok in spec.split("|"):
        key, val = tok.split(":")
        i, j = int(key.strip()[0]), int(key.strip()[1])
        val = val.strip()
        if val.upper() == "ALL":
            pairs = [(a, b) for a in range(3) for b in range(3)]
        else:
            pairs = [(int(x[0]), int(x[1])) for x in val.split()]
        out.update((i, j, a, b) for a, b in pairs)
    return out


def relabel(support, perm, cperm):
    out = set()
    for i, j, a, b in support:
        i2, j2, a2, b2 = perm[i], perm[j], cperm[a], cperm[b]
        if i2 > j2:
            i2, j2, a2, b2 = j2, i2, b2, a2
        out.add((i2, j2, a2, b2))
    return frozenset(out)


def isomorphisms(src, dst):
    dst = frozenset(dst)
    return [(p, c) for p in itertools.permutations(range(N)) for c in itertools.permutations(range(3))
            if relabel(src, p, c) == dst]


def matchings(vs):
    if not vs:
        yield ()
        return
    v = vs[0]
    for k in range(1, len(vs)):
        rest = vs[1:k] + vs[k + 1:]
        for m in matchings(rest):
            yield ((v, vs[k]),) + m


MATCHINGS = list(matchings(tuple(range(N))))


class System:
    """Word polynomials on a fixed support; monomials are sorted tuples of variable ids."""

    def __init__(self, support):
        self.vars = sorted(support)
        self.index = {e: k for k, e in enumerate(self.vars)}

    def var(self, i, j, a, b):
        if i > j:
            i, j, a, b = j, i, b, a
        return self.index.get((i, j, a, b))

    def word_poly(self, w):
        poly = defaultdict(int)
        for m in MATCHINGS:
            mono = []
            for i, j in m:
                v = self.var(i, j, w[i], w[j])
                if v is None:
                    break
                mono.append(v)
            else:
                poly[tuple(sorted(mono))] += 1
        if len(set(w)) == 1:
            poly[()] -= 1
        return {k: c for k, c in poly.items() if c}

    def degree(self, mono, quotient):
        d = [0] * (3 * N)
        for v in mono:
            i, j, a, b = self.vars[v]
            d[3 * i + a] += 1
            d[3 * j + b] += 1
        if quotient:  # canonical representative modulo the constant-word degrees kappa_c
            for c in range(3):
                lo = min(d[3 * v + c] for v in range(N))
                for v in range(N):
                    d[3 * v + c] -= lo
        return tuple(d)

    def name(self, v):
        i, j, a, b = self.vars[v]
        return f"W{i}{j}[{a}{b}]"

    def mono_name(self, mono):
        return "*".join(self.name(v) for v in mono) if mono else "1"


def mul(mono, poly):
    return {tuple(sorted(mono + k)): c for k, c in poly.items()}


def search(system, equations, max_degree, homogeneous, quotient, log):
    """Return the first (degree, block) containing a monomial certificate, else None."""
    nv = len(system.vars)
    for D in range(max_degree + 1):
        t0 = time.time()
        degs = [D] if homogeneous else range(D + 1)
        buckets = defaultdict(list)
        nrows = 0
        for d in degs:
            for m in itertools.combinations_with_replacement(range(nv), d):
                for wi, (w, poly) in enumerate(equations):
                    lead = next(iter(poly))
                    key = system.degree(tuple(sorted(m + lead)), quotient)
                    buckets[key].append((m, wi))
                    nrows += 1
        best = None
        allhits = []
        for key, rows in buckets.items():
            polys = [mul(m, equations[wi][1]) for m, wi in rows]
            cols = sorted({k for p in polys for k in p})
            cidx = {k: n for n, k in enumerate(cols)}
            mat = flint.fmpq_mat(len(polys), len(cols))
            for r, p in enumerate(polys):
                for k, c in p.items():
                    mat[r, cidx[k]] = c
            rref, rank = mat.rref()
            hits = []
            for r in range(rank):
                nz = [c for c in range(len(cols)) if rref[r, c] != 0]
                if len(nz) == 1:
                    hits.append(cols[nz[0]])
            if hits:
                cand = (len(rows), key, hits, rows)
                allhits.append(cand)
                if best is None or cand[0] < best[0]:
                    best = cand
        log(f"D={D}: {nrows} rows in {len(buckets)} blocks, "
            f"{'monomial FOUND' if best else 'no monomial in any block'} ({time.time() - t0:.1f} s)")
        if best:
            log(f"  blocks at D={D} whose span contains a monomial: {len(allhits)}; "
                f"monomials found: {sum(len(h[2]) for h in allhits)}")
            return D, best, allhits
    return None


def in_span(equations, rows, target):
    """Exact test: is the monomial `target` in the Q-span of the products m * E_w in `rows`?"""
    if not rows:
        return False
    polys = [mul(m, equations[wi][1]) for m, wi in rows]
    cols = sorted({k for p in polys for k in p} | {target})
    cidx = {k: n for n, k in enumerate(cols)}
    mat = flint.fmpq_mat(len(polys) + 1, len(cols))
    for r, p in enumerate(polys):
        for k, c in p.items():
            mat[r, cidx[k]] = c
    base = flint.fmpq_mat(len(polys), len(cols))
    for r in range(len(polys)):
        for c in range(len(cols)):
            base[r, c] = mat[r, c]
    mat[len(polys), cidx[target]] = 1
    return mat.rank() == base.rank()


def extract(system, equations, rows, target):
    """Solve sum x_r (m_r E_{w_r}) = target exactly; return {word index: multiplier poly}."""
    polys = [mul(m, equations[wi][1]) for m, wi in rows]
    cols = sorted({k for p in polys for k in p} | {target})
    cidx = {k: n for n, k in enumerate(cols)}
    # A^T x = e_target, A rows = products
    at = flint.fmpq_mat(len(cols), len(polys))
    for r, p in enumerate(polys):
        for k, c in p.items():
            at[cidx[k], r] = c
    aug = flint.fmpq_mat(len(cols), len(polys) + 1)
    for i in range(len(cols)):
        for j in range(len(polys)):
            aug[i, j] = at[i, j]
    aug[cidx[target], len(polys)] = 1
    rref, rank = aug.rref()
    x = [flint.fmpq(0)] * len(polys)
    for r in range(rank):
        piv = next(c for c in range(len(polys) + 1) if rref[r, c] != 0)
        assert piv < len(polys), "target not in span"
        x[piv] = rref[r, len(polys)]
    g = defaultdict(lambda: defaultdict(lambda: flint.fmpq(0)))
    for (m, wi), xr in zip(rows, x):
        if xr != 0:
            g[wi][m] += xr
    # exact replay
    total = defaultdict(lambda: flint.fmpq(0))
    for wi, mp in g.items():
        for m, c in mp.items():
            for k, e in equations[wi][1].items():
                total[tuple(sorted(m + k))] += c * e
    total = {k: c for k, c in total.items() if c != 0}
    assert total == {target: flint.fmpq(1)}, "certificate replay failed"
    return {wi: {m: c for m, c in mp.items() if c != 0} for wi, mp in g.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", choices=["slice", "full"], default="slice")
    ap.add_argument("--max-degree", type=int, default=4)
    args = ap.parse_args()

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    support = {tuple(e) for e in data["entries"]}
    assert data["n"] == N and len(support) == 51
    hol = parse_blocks(HOLONOMY_SURVIVOR)
    iso = isomorphisms(hol, support)
    print(f"holonomy survivor ({len(hol)} entries) -> BL fixture: {len(iso)} isomorphisms, e.g. "
          f"vertex map {iso[0][0]}, colour map {iso[0][1]}" if iso else "NOT isomorphic")
    assert len(hol) == 51 and iso
    print(f"automorphism group of the fixture support: order {len(isomorphisms(support, support))}")

    system = System(support)
    if args.system == "slice":
        words = []
        for w0, w2, w3 in itertools.product(range(3), repeat=3):
            w = [0] * N
            w[0], w[2], w[3] = w0, w2, w3
            for u, c in SLICE_PIN.items():
                w[u] = c
            words.append(tuple(w))
        homogeneous, quotient = True, False
    else:
        words = list(itertools.product(range(3), repeat=N))
        homogeneous, quotient = False, True
    equations = [(w, system.word_poly(w)) for w in words]
    equations = [(w, p) for w, p in equations if p]
    used_vars = sorted({v for _, p in equations for k in p for v in k})
    print(f"system={args.system}: {len(equations)} nonzero equations in {len(used_vars)} unknowns")
    res = search(system, equations, args.max_degree, homogeneous, quotient, print)
    if res is None:
        print(f"RESULT: no monomial certificate with multiplier degree <= {args.max_degree}")
        return 0
    D, (nrows, key, hits, rows), allhits = res
    print(f"all blocks at D={D} containing a monomial (words of the block, target monomials):")
    for nr, _, hs, rs in sorted(allhits, key=lambda h: (h[0], h[2])):
        ws = sorted({"".join(map(str, equations[wi][0])) for _, wi in rs})
        print(f"  {nr} rows, words {' '.join(ws)}; targets {[system.mono_name(h) for h in hs]}")
    # Minimal number of words: a certificate with target mu lies in mu's block,
    # so test every word subset of every hit block.
    min_words = None
    for _, _, hs, rs in allhits:
        ws = sorted({wi for _, wi in rs})
        for k in range(1, len(ws) + 1):
            if any(in_span(equations, [r for r in rs if r[1] in sub], hs[0])
                   for sub in itertools.combinations(ws, k)):
                min_words = k if min_words is None else min(min_words, k)
                break
    print(f"minimal number of word equations in a degree-{D} certificate: {min_words}")
    target = min(hits, key=lambda k: (len(k), k))
    cert = extract(system, equations, rows, target)
    print(f"RESULT: minimal multiplier degree D = {D}; block of {nrows} rows; "
          f"{len(hits)} monomial(s) in its span")
    print(f"target monomial: {system.mono_name(target)}")
    print(f"certificate uses {len(cert)} word equation(s):")
    for wi, mp in sorted(cert.items(), key=lambda t: equations[t[0]][0]):
        w = "".join(map(str, equations[wi][0]))
        terms = len(equations[wi][1])
        degs = sorted({len(m) for m in mp})
        print(f"  word {w} ({terms} live terms): {len(mp)} multiplier monomials, degrees {degs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
