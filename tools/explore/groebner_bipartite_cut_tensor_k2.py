#!/usr/bin/env python3
"""Exact SymPy Groebner basis for the full-word cut-tensor system at |P| = |Q| = 2.

Owner: docs/strategy/cut-tensor-rigidity-attempt-2026-10-09.md.  A second
exact check of the k = 2 case by a different route (elimination, no
saturation) from the hand proof.  It is by the same author, so it is not an
independent audit.  Unknowns are the 36 entries of the four 3x3 blocks;
equations are per(A_a) - [a constant] for the 81 words.  Expected output:
GB [1].  Recorded run cut-gb-k2-a: 738 s.  Use the bounded runner:

    python tools/research/run_bounded.py --run-id <id> --timeout-seconds 1200 --memory-mb 4000 -- \
      python tools/explore/groebner_bipartite_cut_tensor_k2.py
"""
import itertools
import time

import sympy as sp

k = 2
W = {(p, q, a, b): sp.Symbol(f"w{p}{q}_{a}{b}") for p in range(k) for q in range(k) for a in range(3) for b in range(3)}
gens = list(W.values())
eqs = []
for word in itertools.product(range(3), repeat=2 * k):
    P = word[:k]; Q = word[k:]
    val = sum(sp.Mul(*[W[(p, s[p], P[p], Q[s[p]])] for p in range(k)]) for s in itertools.permutations(range(k)))
    tgt = 1 if len(set(word)) == 1 else 0
    eqs.append(sp.expand(val - tgt))
t = time.time()
G = sp.groebner(eqs, *gens, order="grevlex")
print("GB:", list(G.exprs)[:5], "len", len(G.exprs), "time", round(time.time() - t, 1))
