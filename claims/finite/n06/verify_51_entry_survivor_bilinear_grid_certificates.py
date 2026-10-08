#!/usr/bin/env python3
"""Exact replay: the 51-entry survivor is killed by explicit multilinear certificates.

Scope: exact finite computation on fixed six-vertex supports.  It instantiates
claims/arbitrary-order/THREE_COLUMN_BILINEAR_GRID_THEOREM.md at n = 6 and
replays every instance as a polynomial identity among the *actual* word
polynomials of the support (not only the reduced bilinear forms).  The
six-vertex exclusion is already a theorem; nothing here is a new exclusion.

Supports:
  BL51   tests/fixtures/bl_full_word_survivor_n6_51.json
  HOL51  the holonomy-model survivor (docs/strategy/holonomy-support-model-2026-10-08.md,
         Section 5.4), isomorphic to BL51
  HOL50  the 50-entry no-symmetry holonomy survivor (control)
  P27, P41, P63  the three patterns of SIX_VERTEX_SUPPORT_SURVIVOR_PATTERNS_EXACT_REFUTATION.md (controls)

(G) Theorem 2 instances (three-column bilinear grid, degree-2 cofactors in the
    grid matrix, multiplier degree 4 in the entries).  Data: an unordered pair
    {a, b}; a word c on R = V - {a, b}; C subset R, |C| = 3, r = R - C; colours
    b0 != b1 at a and g0 != g1 at b; p, q in C.  Support-level hypotheses: C is
    independent at c (W_uv[c_u, c_v] unsupported for u, v in C), r is joined to
    all of C at c, the four grid words are mixed, and det[y_b0, y_b1, e_p],
    det[z_g0, z_g1, e_q] are monomials (exactly one of the two products in the
    support).  Replay: sum_ij g_ij T(w_ij) = +-2 * monomial, exactly.
(K) Proposition 4 instances (2x2x2 cube, multiplier degree 3) on 3-vs-3 cuts
    T | U with U independent at a pinned colouring sigma: two colours per inner
    vertex, minors that are monomials with two equal row pairs; replay of the
    closed-form identity against the actual word polynomials.

Run:
    python claims/finite/n06/verify_51_entry_survivor_bilinear_grid_certificates.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

import sympy as sp  # noqa: E402

N = 6
ALL9 = " ".join(f"{a}{b}" for a in range(3) for b in range(3))
SPECS = {
    "HOL51": ("01: ALL|02: 00 10 20|03: ALL|04: 22|05: 01 11 21|12: 00 10 20|13: ALL|"
              "14: 02 12 22|15: 11|23: 00|24: 11|25: 22|34: 02 12 22|35: 01 11 21|45: 00"),
    "HOL50": ("01: ALL|02: 01 11 21|03: 02 12 22|04: 00|05: 00 02 10 11 12 20 21 22|"
              "12: 01 11 21|13: 22|14: 00 10 20|15: ALL|23: 00|24: 22|25: 11|34: 11|"
              "35: 20 21 22|45: 00 01 02"),
    # verbatim from claims/finite/n06/verify_six_vertex_support_survivor_patterns.py
    "P27": ("01: 00 20 | 02: 11 | 03: 00 20 | 04: 02 22 | 05: 00 02 20 22 | 12: 00 02 | 13: 22 | "
            "14: 11 | 15: 20 | 23: 00 20 | 24: 02 22 | 25: 00 02 20 22 | 34: 20 | 35: 11 | 45: 00"),
    "P41": ("01: 00 02 10 11 12 20 21 22 | 02: 12 22 | 03: 01 11 21 | 04: 02 10 11 20 21 | 05: 00 | "
            "12: 02 22 | 13: 11 | 14: 00 01 02 12 20 21 22 | 15: 00 10 20 | 23: 00 | 24: 22 | "
            "25: 11 | 34: 10 11 12 | 35: 22 | 45: 00 10"),
    "P63": (f"01: {ALL9} | 02: 02 | 03: 00 | 04: 11 | 05: {ALL9} | 12: {ALL9} | 13: 20 | 14: 01 | "
            f"15: 12 | 23: {ALL9} | 24: 21 | 25: 22 | 34: {ALL9} | 35: 01 | 45: {ALL9}"),
}
EXPECTED = {"BL51": 51, "HOL51": 51, "HOL50": 50, "P27": 27, "P41": 41, "P63": 63}


def parse(spec):
    out = set()
    for tok in spec.split("|"):
        key, val = tok.split(":")
        i, j = int(key.strip()[0]), int(key.strip()[1])
        vals = ALL9 if val.strip().upper() == "ALL" else val
        out.update((i, j, int(x[0]), int(x[1])) for x in vals.split())
    return out


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


class Support:
    def __init__(self, entries):
        self.S = set(entries)
        self.cache = {}

    def live(self, i, j, a, b):
        return ((i, j, a, b) if i < j else (j, i, b, a)) in self.S

    def W(self, i, j, a, b):
        if i > j:
            i, j, a, b = j, i, b, a
        if (i, j, a, b) not in self.S:
            return sp.Integer(0)
        return sp.Symbol(f"W{i}{j}_{a}{b}")

    def T(self, w):
        w = tuple(w)
        if w not in self.cache:
            self.cache[w] = sp.expand(sp.Add(*[sp.Mul(*[self.W(i, j, w[i], w[j]) for i, j in m])
                                               for m in MATCHINGS]))
        return self.cache[w]


def is_monomial(expr):
    expr = sp.expand(expr)
    return expr != 0 and len(sp.Add.make_args(expr)) == 1


def grid_instances(sup):
    """Theorem 2 instances; every one is replayed exactly.  Returns (count, example)."""
    count, example = 0, None
    for a, b in itertools.combinations(range(N), 2):
        R = [v for v in range(N) if v not in (a, b)]
        for cR in itertools.product(range(3), repeat=4):
            c = dict(zip(R, cR))
            for C in itertools.combinations(R, 3):
                r = next(v for v in R if v not in C)
                if any(sup.live(u, v, c[u], c[v]) for u, v in itertools.combinations(C, 2)):
                    continue
                if not all(sup.live(r, u, c[r], c[u]) for u in C):
                    continue
                Hm = sp.zeros(3, 3)
                for (k, u), (l, v) in itertools.permutations(list(enumerate(C)), 2):
                    w_ = next(x for x in C if x not in (u, v))
                    Hm[k, l] = sup.W(r, w_, c[r], c[w_])
                for bb in itertools.permutations(range(3), 2):
                    for gg in itertools.permutations(range(3), 2):
                        if bb[0] > bb[1] or gg[0] > gg[1]:
                            continue
                        words = {}
                        ok = True
                        for i, j in itertools.product(range(2), repeat=2):
                            w = [0] * N
                            for v in R:
                                w[v] = c[v]
                            w[a], w[b] = bb[j], gg[i]
                            if len(set(w)) == 1:
                                ok = False
                            words[i, j] = tuple(w)
                        if not ok:
                            continue
                        y = [sp.Matrix([sup.W(a, u, beta, c[u]) for u in C]) for beta in bb]
                        z = [sp.Matrix([sup.W(b, u, gam, c[u]) for u in C]) for gam in gg]
                        E = sp.eye(3)
                        for p, q in itertools.product(range(3), repeat=2):
                            Y = sp.Matrix.hstack(y[0], y[1], E[:, p])
                            Z = sp.Matrix.hstack(z[0], z[1], E[:, q])
                            dY, dZ = sp.expand(Y.det()), sp.expand(Z.det())
                            if not (is_monomial(dY) and is_monomial(dZ)):
                                continue
                            G = Z.T * Hm * Y
                            g = {(0, 0): G[1, 1] * G[2, 2] - G[1, 2] * G[2, 1],
                                 (0, 1): -(G[1, 0] * G[2, 2] - G[1, 2] * G[2, 0]),
                                 (1, 0): G[0, 2] * G[2, 1],
                                 (1, 1): -G[0, 2] * G[2, 0]}
                            lhs = sp.expand(sum(g[i, j] * sup.T(words[i, j])
                                                for i, j in itertools.product(range(2), repeat=2)))
                            rhs = sp.expand(dZ * 2 * Hm[0, 1] * Hm[0, 2] * Hm[1, 2] * dY)
                            assert lhs == rhs and is_monomial(rhs), (a, b, c, C, bb, gg, p, q)
                            count += 1
                            if example is None:
                                example = (a, b, c, C, bb, gg, [words[k] for k in sorted(words)], rhs)
    return count, example


def cube_instances(sup):
    """Proposition 4 instances on 3-vs-3 cuts; each replayed exactly against T(w)."""
    count, example = 0, None
    for T in itertools.combinations(range(N), 3):
        U = [v for v in range(N) if v not in T]
        for sig in itertools.product(range(3), repeat=3):
            s = dict(zip(U, sig))
            if any(sup.live(u, v, s[u], s[v]) for u, v in itertools.combinations(U, 2)):
                continue
            rows = {(t, col): sp.Matrix([sup.W(t, u, col, s[u]) for u in U]) for t in T for col in range(3)}
            pairs = list(itertools.combinations(range(3), 2))
            for cols in itertools.product(pairs, repeat=3):
                Ys = [sp.Matrix.hstack(rows[t, cp[0]], rows[t, cp[1]]) for t, cp in zip(T, cols)]
                words = {}
                mixed = True
                for i, j, k in itertools.product(range(2), repeat=3):
                    w = [0] * N
                    for u in U:
                        w[u] = s[u]
                    for t, cp, x in zip(T, cols, (i, j, k)):
                        w[t] = cp[x]
                    mixed &= len(set(w)) > 1
                    words[i, j, k] = tuple(w)
                if not mixed:
                    continue
                for order in itertools.permutations(range(3)):  # Y0, Y1 share the pair; Y2 is the third
                    for m in itertools.permutations(range(3)):  # coordinate map 1,2,3 -> m0,m1,m2
                        Yo = [Ys[o] for o in order]

                        def minor(M, I):
                            return M[I[0], 0] * M[I[1], 1] - M[I[1], 0] * M[I[0], 1]
                        mins = [minor(Yo[0], (m[0], m[1])), minor(Yo[1], (m[0], m[1])),
                                minor(Yo[2], (m[0], m[2]))]
                        if not all(is_monomial(x) for x in mins):
                            continue

                        def phi(a_, b_, c_):
                            return c_[m[0]] * (a_[m[0]] * b_[m[1]] + a_[m[1]] * b_[m[0]]) - a_[m[0]] * b_[m[0]] * c_[m[1]]
                        lhs = 0
                        for idx in itertools.product(range(2), repeat=3):
                            # idx is indexed in the reordered frame; map back to the word key
                            key = [0, 0, 0]
                            for pos, o in enumerate(order):
                                key[o] = idx[pos]
                            lhs += ((-1) ** sum(idx) * phi(Yo[0][:, 1 - idx[0]], Yo[1][:, 1 - idx[1]],
                                                           Yo[2][:, 1 - idx[2]]) * sup.T(words[tuple(key)]))
                        lhs = sp.expand(lhs)
                        rhs = sp.expand(2 * mins[0] * mins[1] * mins[2])
                        assert lhs == rhs, (T, U, sig, cols, order, m)
                        count += 1
                        if example is None:
                            example = (T, s, cols, sorted(set(words.values())), rhs)
    return count, example


def wstr(w):
    return "".join(map(str, w))


def main() -> int:
    data = json.loads((REPO_ROOT / "tests" / "fixtures" / "bl_full_word_survivor_n6_51.json").read_text(encoding="utf-8"))
    supports = {"BL51": {tuple(e) for e in data["entries"]}}
    supports.update({k: parse(v) for k, v in SPECS.items()})
    for k, S in supports.items():
        assert len(S) == EXPECTED[k], (k, len(S))
    for name, S in supports.items():
        sup = Support(S)
        gc, gex = grid_instances(sup)
        kc, kex = cube_instances(sup)
        print(f"{name}: Theorem 2 (bilinear grid, degree 4) instances = {gc}; "
              f"Proposition 4 (cube, degree 3) instances = {kc}")
        if name == "BL51":
            a, b, c, C, bb, gg, words, rhs = gex
            print(f"  example grid: pair (a,b) = ({a},{b}), background {c}, columns C = {C}, "
                  f"colours {bb} at {a}, {gg} at {b}")
            print(f"    words {' '.join(wstr(w) for w in words)};  sum g_ij T(w_ij) = {rhs}")
            T, s, cols, words, rhs = kex
            print(f"  example cube: inner {T}, pinned {s}, colour pairs {cols}")
            print(f"    words {' '.join(wstr(w) for w in words)};  certificate = {rhs}")
    print("RESULT: every listed instance replays exactly against the actual word polynomials")
    return 0


if __name__ == "__main__":
    sys.exit(main())
