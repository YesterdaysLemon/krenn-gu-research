#!/usr/bin/env python3
"""Replay the displayed identities of TWO_TERM_RELATION_CLOSURE_THEOREMS.md.

This replays identities; it is not the proof of Theorems C and D, whose
arguments are in the document.  Checks (exact, SymPy / integer):

A. two-matching grid: T00*x1*u1, T00*y1*v1, T00*x1*v1, T00*y1*u1 lie in the
   ideal (T01, T10, T11) for Tab = x_a*u_b + y_a*v_b; the explicit
   division-free combination for T00*x1*u1 is checked by expansion.
B. odd opposite-ratio cycle: for k = 3, 5, 7, 9
       sum_t (-1)^(t+1) p_t prod_{j not in {t,t+1}} B_j = 2 A_1 prod_{j != 1} B_j,
   p_t = A_t B_{t+1} + A_{t+1} B_t (indices mod k); for even k the same
   alternating sum is identically zero (no obstruction).
D. distinct (word, perfect matching) pairs give distinct physical monomials
   at n = 4, 6, 8 (the combinatorial input of the inertness criterion).
"""

from __future__ import annotations

import itertools
import sys

import sympy as sp


def check_a() -> None:
    x0, x1, y0, y1, u0, u1, v0, v1 = sp.symbols("x0 x1 y0 y1 u0 u1 v0 v1")
    t = {(a, b): [x0, x1][a] * [u0, u1][b] + [y0, y1][a] * [v0, v1][b]
         for a in range(2) for b in range(2)}
    lhs = t[0, 0] * x1 * u1
    rhs = (t[0, 0] * t[1, 1] - x0 * u0 * t[1, 1] - t[0, 1] * t[1, 0]
           + x0 * u1 * t[1, 0] + x1 * u0 * t[0, 1])
    assert sp.expand(lhs - rhs) == 0
    G = sp.groebner([t[0, 1], t[1, 0], t[1, 1]], x0, x1, y0, y1, u0, u1, v0, v1, order="grevlex")
    for mono in (x1 * u1, y1 * v1, x1 * v1, y1 * u1):
        assert G.contains(sp.expand(t[0, 0] * mono)), mono
    assert not G.contains(t[0, 0])
    print("A: grid identity and the four corner products: PASS")


def check_b() -> None:
    for k in (3, 4, 5, 6, 7, 9):
        A = sp.symbols(f"A0:{k}")
        B = sp.symbols(f"B0:{k}")
        total = 0
        for t in range(k):
            s = (t + 1) % k
            p = A[t] * B[s] + A[s] * B[t]
            rest = sp.Mul(*[B[j] for j in range(k) if j not in (t, s)])
            total += (-1) ** t * p * rest
        total = sp.expand(total)
        if k % 2:
            assert sp.expand(total - 2 * A[0] * sp.Mul(*B[1:])) == 0, k
        else:
            assert total == 0, k
    print("B: odd-cycle identity (k=3,5,7,9) and even-cycle vanishing (k=4,6): PASS")


def matchings(vertices):
    if not vertices:
        yield ()
        return
    v = vertices[0]
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1:]
        for m in matchings(rest):
            yield ((v, vertices[k]),) + m


def check_d() -> None:
    for n in (4, 6, 8):
        M = list(matchings(tuple(range(n))))
        seen = set()
        count = 0
        for w in itertools.product(range(3), repeat=n):
            for m in M:
                mono = frozenset((i, j, w[i], w[j]) for i, j in m)
                seen.add(mono)
                count += 1
        assert len(seen) == count, n
        print(f"D: n={n}: {count} (word, matching) pairs, all monomials distinct: PASS")


def main() -> int:
    check_a()
    check_b()
    check_d()
    return 0


if __name__ == "__main__":
    sys.exit(main())
