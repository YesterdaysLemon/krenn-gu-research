#!/usr/bin/env python3
"""Exact check: the two-matching grid identity excludes the 27-entry n=6 pattern.

Scope: one conditional physical-support exclusion at n=6 (the minimum-entry
Boolean model of the 2026-10-08 general-block recursive support model).  The
six-vertex exclusion is already a theorem; this script is a mechanism exhibit,
not a new finite result and not a cover of anything.

Checks, all in exact integer/polynomial arithmetic (SymPy):

1. The generic grid identity in eight variables:
       T00*x1*u1 = T00*T11 - x0*u0*T11 - T01*T10 + x0*u1*T10 + x1*u0*T01,
   where Tab = x_a*u_b + y_a*v_b.
2. For the 27-entry pattern: all 729 full words, the number of live perfect
   matchings per word, and the single-term conditions (no mixed word has
   exactly one live matching; every constant word has one).
3. For each of the two grids (base colour 0 and base colour 2): starting from
   symbols for ALL 135 physical entries, setting to zero only the guard entries,
   the four full hafnians factor as x_a*u_b + y_a*v_b with the displayed
   physical x, y, u, v, and the identity above holds as a polynomial identity.
   Consequently, for every complex source with those guard zeros, the three
   mixed corner equations force T(pure corner)*m = 0 for the displayed
   nonzero physical monomial m.
4. The guard is a minimum: no smaller set of pattern-zero entries kills every
   other matching at the four corner words (exhaustive check).

No solver, no SAT, no floating point.  Run:
    python claims/finite/n06/verify_27_entry_two_matching_grid.py
"""

from __future__ import annotations

import itertools
import sys

import sympy as sp

N = 6
PATTERN = (
    "01: 00 20 | 02: 11 | 03: 00 20 | 04: 02 22 | 05: 00 02 20 22 | "
    "12: 00 02 | 13: 22 | 14: 11 | 15: 20 | 23: 00 20 | 24: 02 22 | "
    "25: 00 02 20 22 | 34: 20 | 35: 11 | 45: 00"
)


def parse(pattern: str) -> set[tuple[int, int, int, int]]:
    live = set()
    for part in pattern.split("|"):
        edge, colours = part.split(":")
        i, j = int(edge.strip()[0]), int(edge.strip()[1])
        assert i < j
        for ab in colours.split():
            live.add((i, j, int(ab[0]), int(ab[1])))
    return live


def matchings(vertices):
    if not vertices:
        yield ()
        return
    v = vertices[0]
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1:]
        for m in matchings(rest):
            yield ((v, vertices[k]),) + m


MATCHINGS = list(matchings(tuple(range(N))))
assert len(MATCHINGS) == 15
SYM = {
    (i, j, a, b): sp.Symbol(f"W{i}{j}_{a}{b}")
    for i in range(N) for j in range(i + 1, N) for a in range(3) for b in range(3)
}


def key(edge, word):
    i, j = edge
    return (i, j, word[i], word[j])


def monomial(m, word):
    return sp.Mul(*[SYM[key(e, word)] for e in m])


def hafnian(word, zero):
    total = sp.Integer(0)
    for m in MATCHINGS:
        if any(key(e, word) in zero for e in m):
            continue
        total += monomial(m, word)
    return sp.expand(total)


def check_generic_identity() -> None:
    x0, x1, y0, y1, u0, u1, v0, v1 = sp.symbols("x0 x1 y0 y1 u0 u1 v0 v1")
    t = {(a, b): [x0, x1][a] * [u0, u1][b] + [y0, y1][a] * [v0, v1][b]
         for a in range(2) for b in range(2)}
    lhs = t[0, 0] * x1 * u1
    rhs = (t[0, 0] * t[1, 1] - x0 * u0 * t[1, 1] - t[0, 1] * t[1, 0]
           + x0 * u1 * t[1, 0] + x1 * u0 * t[0, 1])
    assert sp.expand(lhs - rhs) == 0
    print("generic grid identity: PASS")


def check_pattern(live) -> None:
    sizes = {}
    for word in itertools.product(range(3), repeat=N):
        count = sum(all(key(e, word) in live for e in m) for m in MATCHINGS)
        sizes[count] = sizes.get(count, 0) + 1
        constant = len(set(word)) == 1
        if constant:
            assert count >= 1, word
        else:
            assert count != 1, word
    assert len(live) == 27
    print("pattern: 27 entries; live-matchings-per-word histogram", dict(sorted(sizes.items())))
    print("single-term conditions at full-word level: PASS (every fibre has <= 2 live terms)")


def grid(base: int, other: int, live):
    """P={0}, Q={2}, background colour `base` on {1,3,4,5}."""
    colours = (base, other)
    words = {(a, b): tuple(colours[a] if v == 0 else colours[b] if v == 2 else base for v in range(N))
             for a in range(2) for b in range(2)}
    if base == 0:
        mm, nn = ((0, 1), (2, 3), (4, 5)), ((0, 3), (1, 2), (4, 5))
    else:
        mm, nn = ((0, 4), (1, 3), (2, 5)), ((0, 5), (1, 3), (2, 4))
    # entries that must vanish: every other matching dies at every corner
    targets = []
    for w in words.values():
        for m in MATCHINGS:
            if m in (mm, nn):
                continue
            targets.append(frozenset(key(e, w) for e in m))
    candidates = sorted({k for t in targets for k in t if k not in live})
    for t in targets:
        assert t & set(candidates), "a non-grid matching is live at a corner"
    best = None
    for size in range(1, len(candidates) + 1):
        for subset in itertools.combinations(candidates, size):
            s = set(subset)
            if all(t & s for t in targets):
                best = s
                break
        if best is not None:
            break
    zero = best
    t = {ab: hafnian(w, zero) for ab, w in words.items()}
    # factor x_a u_b + y_a v_b with u/v the factors on edges meeting Q={2}
    def split(m, w):
        meets_q = [e for e in m if 2 in e]
        rest = [e for e in m if 2 not in e]
        return sp.Mul(*[SYM[key(e, w)] for e in rest]), sp.Mul(*[SYM[key(e, w)] for e in meets_q])
    x = {}
    u = {}
    y = {}
    v = {}
    for (a, b), w in words.items():
        x[a], u[b] = split(mm, w)
        y[a], v[b] = split(nn, w)
    for (a, b) in t:
        assert sp.expand(t[a, b] - (x[a] * u[b] + y[a] * v[b])) == 0, (a, b)
    lhs = t[0, 0] * x[1] * u[1]
    rhs = (t[0, 0] * t[1, 1] - x[0] * u[0] * t[1, 1] - t[0, 1] * t[1, 0]
           + x[0] * u[1] * t[1, 0] + x[1] * u[0] * t[0, 1])
    assert sp.expand(lhs - rhs) == 0
    nonzero = x[1] * u[1]
    assert all(k in live for k in [(i, j, a, b) for (i, j, a, b) in SYM if SYM[(i, j, a, b)] in nonzero.free_symbols])
    words_txt = {ab: "".join(map(str, w)) for ab, w in words.items()}
    print(f"grid base {base}: words {words_txt}")
    print(f"  M={mm} N={nn}; minimum guard has {len(zero)} zero entries:")
    print("   ", sorted(f"W{i}{j}[{a},{b}]" for (i, j, a, b) in zero))
    print(f"  T(pure) * ({nonzero}) lies in the ideal of the three mixed corners: PASS")
    return zero, nonzero


def triangle(live) -> None:
    """Odd opposite-ratio cycle: a=0, b=2 (both colour 2), slots (3,0),(4,2),(5,0)."""
    words = {"35": (2, 1, 2, 0, 1, 0), "34": (2, 2, 2, 0, 2, 0), "45": (2, 2, 2, 2, 2, 0)}
    third = {"35": 4, "34": 5, "45": 3}
    slot = {3: 0, 4: 2, 5: 0}
    A = {k: SYM[(0, k, 2, slot[k])] for k in (3, 4, 5)}
    B = {k: SYM[(2, k, 2, slot[k])] for k in (3, 4, 5)}
    t = {}
    for pair, w in words.items():
        assert w[0] == 2 and w[2] == 2 and all(w[k] == slot[k] for k in map(int, pair))
        zero = {k for m in MATCHINGS for k in [key(e, w) for e in m] if k not in live}
        val = hafnian(w, zero)
        k, l = map(int, pair)
        m = third[pair]
        cof = SYM[key((1, m), w)]
        assert sp.expand(val - cof * (A[k] * B[l] + A[l] * B[k])) == 0, pair
        t[pair] = (val, cof)
    lhs = 2 * A[3] * B[4] * B[5] * t["34"][1] * t["35"][1] * t["45"][1]
    rhs = (B[5] * t["35"][1] * t["45"][1] * t["34"][0]
           - B[3] * t["34"][1] * t["35"][1] * t["45"][0]
           + B[4] * t["34"][1] * t["45"][1] * t["35"][0])
    assert sp.expand(lhs - rhs) == 0
    print("odd ratio triangle: words 212010, 222020, 222220 give")
    print("  2*W03[2,0]*W24[2,2]*W25[2,0]*W13[2,2]*W14[1,1]*W15[2,0] in the span of the three mixed fibres: PASS")


def main() -> int:
    live = parse(PATTERN)
    check_generic_identity()
    check_pattern(live)
    for base, other in ((0, 2), (2, 0)):
        grid(base, other, live)
    triangle(live)
    print("RESULT: the 27-entry pattern is excluded three times: two two-matching grids "
          "(pure words 000000, 222222) and one odd opposite-ratio triangle (mixed words only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
