#!/usr/bin/env python3
"""Exact check: one 27-word slice excludes the 51-entry full-word BL survivor.

Scope: a conditional physical-support exclusion at n=6, recorded as the first
datum above two-term relations.  The support in
tests/fixtures/bl_full_word_survivor_n6_51.json satisfies the full-word
single-term conditions and the column-killer condition, and the full-word
binomial-linear closure (tools/explore/binomial_linear_closure.py) stops on it
without contradiction.  The six-vertex exclusion is already a theorem; this
script only exhibits *which* relation beyond two-term transport is used.

Checks (SymPy, exact):

1. On the 27 words with colours (w1,w4,w5) = (2,0,1) and (w0,w2,w3) free,
   the full hafnian of a source with the fixture's support equals
   F[w0,w2,w3] for the six-term tensor
       F = c01(x)c24(x)c35 + c01(x)c25(x)c34 + c04(x)c21(x)c35
         + c04(x)c25(x)c31 + c05(x)c21(x)c34 + c05(x)c24(x)c31,
   with c_tu[a] = W_tu[a, sigma(u)], sigma(1)=2, sigma(4)=0, sigma(5)=1
   (vertex t in {0,2,3} carries the free colour a).  The vectors c24, c05,
   c31 are coordinate vectors (e0, e1, e2 times one entry).
2. After the torus normalization c01=c21=c34=(1,1,1), c24=e0, c05=e1 (valid:
   every one of the 27 words is mixed, and the eleven conditions are solved
   successively by t_0a, t_2b, t_40, t_3a, t_51 with t_12 = 0), the 27
   equations generate an ideal containing s = W13[2,2] (normalized).  So the
   slice alone forces an entry of the support to vanish.

Run:
    python claims/finite/n06/verify_51_entry_bl_survivor_slice.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import sympy as sp

FIXTURE = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "bl_full_word_survivor_n6_51.json"


def matchings(vertices):
    if not vertices:
        yield ()
        return
    v = vertices[0]
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1:]
        for m in matchings(rest):
            yield ((v, vertices[k]),) + m


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    live = {tuple(e) for e in data["entries"]}
    assert data["n"] == 6 and len(live) == 51
    sym = {}

    def W(i, j, a, b):
        """W_ij[a,b], colour a at i and b at j; zero off the support."""
        if i > j:
            i, j, a, b = j, i, b, a
        if (i, j, a, b) not in live:
            return sp.Integer(0)
        return sym.setdefault((i, j, a, b), sp.Symbol(f"W{i}{j}_{a}{b}"))

    sigma = {1: 2, 4: 0, 5: 1}
    T, U = (0, 2, 3), (1, 4, 5)
    c = {(t, u): [W(t, u, a, sigma[u]) for a in range(3)] for t in T for u in U}
    # coordinate structure
    assert c[2, 4][1] == 0 and c[2, 4][2] == 0 and c[2, 4][0] != 0
    assert c[0, 5][0] == 0 and c[0, 5][2] == 0 and c[0, 5][1] != 0
    assert c[3, 1][0] == 0 and c[3, 1][1] == 0 and c[3, 1][2] != 0
    for key in [(0, 1), (2, 1), (3, 4), (0, 4), (2, 5), (3, 5)]:
        assert all(x != 0 for x in c[key]), key
    M = list(matchings(tuple(range(6))))
    for w0, w2, w3 in itertools.product(range(3), repeat=3):
        w = {0: w0, 1: 2, 2: w2, 3: w3, 4: 0, 5: 1}
        haf = sp.expand(sum(sp.Mul(*[W(i, j, w[i], w[j]) for i, j in m]) for m in M))
        F = 0
        for perm in itertools.permutations(U):
            F += sp.Mul(*[c[t, u][w[t]] for t, u in zip(T, perm)])
        assert sp.expand(haf - F) == 0, (w0, w2, w3)
    print("slice: 27 full hafnians equal the six-term permanent tensor F: PASS")

    p = sp.symbols("p0:3")
    q = sp.symbols("q0:3")
    r = sp.symbols("r0:3")
    s = sp.Symbol("s")
    one = (1, 1, 1)
    vec = {(0, 1): one, (2, 1): one, (3, 4): one, (2, 4): (1, 0, 0), (0, 5): (0, 1, 0),
           (3, 1): (0, 0, s), (0, 4): p, (2, 5): q, (3, 5): r}
    eqs = []
    for w0, w2, w3 in itertools.product(range(3), repeat=3):
        w = {0: w0, 2: w2, 3: w3}
        eqs.append(sp.expand(sum(sp.Mul(*[vec[t, u][w[t]] for t, u in zip(T, perm)])
                                 for perm in itertools.permutations(U))))
    G = sp.groebner([e for e in eqs if e != 0], *p, *q, *r, s, order="grevlex")
    assert G.contains(s)
    assert G.contains(2 * s)
    print("normalized slice ideal contains s (the W13[2,2] coordinate): PASS")
    print("RESULT: the 51-entry BL survivor is excluded by one 27-word slice;"
          " the derivation multiplies three-term relations by monomials (beyond two-term transport)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
