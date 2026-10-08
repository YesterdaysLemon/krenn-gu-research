"""Exact refutation of three six-vertex support-level survivor patterns.

Scope (see SIX_VERTEX_SUPPORT_SURVIVOR_PATTERNS_EXACT_REFUTATION.md):
d = 3, n = 6.  For each of three zero/nonzero patterns of the fifteen
3x3 blocks W_ij (i < j), every listed entry is a nonzero unknown and every
other entry is zero.  The script

1. rebuilds all 729 word equations T_W(a) = [a constant] exactly with sympy
   (integer coefficients; no floating point anywhere);
2. reports the term census and checks the two single-term facts the
   support model already guarantees (every constant word has a live
   matching term; no non-constant word has exactly one live term);
3. decides exactly, by integer lattice reduction, whether the binomial
   equations x^u + x^v = 0 of the non-constant words are jointly solvable on
   the torus (the sign-holonomy test);
4. replays the displayed short refutations by exact substitution on the
   torus, printing every equation used and the final contradiction;
5. runs the exact "binomial propagation" calculus on the full system; and
6. with --minimality, checks exhaustively that no shorter refutation exists
   inside that calculus and counts the refuting triangles/squares.

This is NOT a new six-vertex theorem: the six-vertex exclusion is already
recorded in SIX_VERTEX_CERTIFICATE.md.  The script only identifies which
quantitative relation the support abstraction cannot see.

Usage:
    python claims/finite/n06/verify_six_vertex_support_survivor_patterns.py
    python claims/finite/n06/verify_six_vertex_support_survivor_patterns.py --minimality

Exit status 0 iff every check passes.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from collections import Counter
from fractions import Fraction

import sympy as sp

N = 6
D = 3

ALL9 = " ".join(f"{a}{b}" for a in range(D) for b in range(D))
PATTERNS = {
    "P27": (
        "01: 00 20 | 02: 11 | 03: 00 20 | 04: 02 22 | 05: 00 02 20 22 | "
        "12: 00 02 | 13: 22 | 14: 11 | 15: 20 | 23: 00 20 | 24: 02 22 | "
        "25: 00 02 20 22 | 34: 20 | 35: 11 | 45: 00"
    ),
    "P41": (
        "01: 00 02 10 11 12 20 21 22 | 02: 12 22 | 03: 01 11 21 | "
        "04: 02 10 11 20 21 | 05: 00 | 12: 02 22 | 13: 11 | "
        "14: 00 01 02 12 20 21 22 | 15: 00 10 20 | 23: 00 | 24: 22 | "
        "25: 11 | 34: 10 11 12 | 35: 22 | 45: 00 10"
    ),
    "P63": (
        f"01: {ALL9} | 02: 02 | 03: 00 | 04: 11 | 05: {ALL9} | 12: {ALL9} | "
        f"13: 20 | 14: 01 | 15: 12 | 23: {ALL9} | 24: 21 | 25: 22 | "
        f"34: {ALL9} | 35: 01 | 45: {ALL9}"
    ),
}
EXPECTED_SIZE = {"P27": 27, "P41": 41, "P63": 63}

# Displayed refutations: (pattern, label, ordered words).  All but the last
# word are binomials used to eliminate one unknown each; the last word is
# the equation that collapses.
REFUTATIONS = [
    ("P27", "K23 odd triangle (3 equations)", ["002000", "002200", "012010"]),
    ("P27", "constant-word square (4 equations)",
     ["002000", "200000", "202000", "000000"]),
    ("P41", "K23 odd triangle (3 equations)", ["000010", "001111", "002110"]),
    ("P63", "rank-one square, trinomial kill (4 equations)",
     ["000100", "000102", "002100", "002102"]),
    ("P63", "rank-one square, constant word (4 equations)",
     ["111121", "112111", "112121", "111111"]),
]

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        FAILURES.append(msg)
        print("  FAIL:", msg)


# ---------------------------------------------------------------- equations

Entry = tuple[int, int, int, int]  # (i, j, colour at i, colour at j), i < j


def parse(spec: str) -> set[Entry]:
    sup: set[Entry] = set()
    for part in spec.split("|"):
        key, vals = part.split(":")
        key = key.strip()
        i, j = int(key[0]), int(key[1])
        assert i < j
        for e in vals.split():
            sup.add((i, j, int(e[0]), int(e[1])))
    return sup


def matchings(vs: list[int]):
    if not vs:
        yield ()
        return
    a = vs[0]
    for k in range(1, len(vs)):
        rest = vs[1:k] + vs[k + 1:]
        for m in matchings(rest):
            yield ((a, vs[k]),) + m


MATCHINGS = list(matchings(list(range(N))))
assert len(MATCHINGS) == 15
WORDS = list(itertools.product(range(D), repeat=N))


def wname(e: Entry) -> str:
    i, j, a, b = e
    return f"w{i}{j}_{a}{b}"


def is_constant(word) -> bool:
    return len(set(word)) == 1


def live_terms(sup: set[Entry]) -> dict[tuple, list[tuple[Entry, ...]]]:
    """word -> list of live matching monomials (sorted entry tuples)."""
    out = {}
    for w in WORDS:
        terms = []
        for m in MATCHINGS:
            mono = tuple(sorted((i, j, w[i], w[j]) for i, j in m))
            if all(e in sup for e in mono):
                terms.append(mono)
        if terms:
            out[w] = terms
    return out


def sympy_equations(sup, terms, syms):
    """word -> sympy expression lhs - rhs (rhs = 1 on constant words)."""
    eqs = {}
    for w in WORDS:
        lhs = sp.Integer(0)
        for mono in terms.get(w, []):
            lhs += sp.Mul(*[syms[e] for e in mono])
        rhs = sp.Integer(1) if is_constant(w) else sp.Integer(0)
        eqs[w] = sp.expand(lhs - rhs)
    return eqs


def wstr(w) -> str:
    return "".join(map(str, w))


def wparse(s: str):
    return tuple(int(c) for c in s)


# ------------------------------------------------------- exact torus lattice

class Contradiction(Exception):
    pass


class TorusLattice:
    """Imposed relations x^b = val (val a nonzero rational), kept as an
    integer echelon basis.  Exact for the question whether a system of
    binomial equations x^{u_k} = zeta_k is solvable on the complex torus:
    it is solvable iff every integer relation sum c_k u_k = 0 has
    prod zeta_k^{c_k} = 1, and the Euclidean insertion below detects any
    violating relation as a zero row with value != 1."""

    def __init__(self, n: int):
        self.n = n
        self.rows: dict[int, tuple[list[int], Fraction]] = {}

    def value(self, u):
        u = list(u)
        val = Fraction(1)
        for p in sorted(self.rows):
            if u[p] == 0:
                continue
            b, bv = self.rows[p]
            if u[p] % b[p]:
                return None
            q = u[p] // b[p]
            u = [x - q * y for x, y in zip(u, b)]
            val = val * (bv ** q)  # x^(q b) = bv^q
        return val if not any(u) else None

    def add(self, u, val):
        u = list(u)
        val = Fraction(val)
        while True:
            nz = [i for i in range(self.n) if u[i]]
            if not nz:
                if val != 1:
                    raise Contradiction(val)
                return
            p = nz[0]
            if p not in self.rows:
                if u[p] < 0:
                    u = [-x for x in u]
                    val = 1 / val
                self.rows[p] = (u, val)
                return
            b, bv = self.rows[p]
            if u[p] % b[p] == 0:
                q = u[p] // b[p]
                u = [x - q * y for x, y in zip(u, b)]
                val = val / (bv ** q)
                continue
            q = b[p] // u[p]
            r = [x - q * y for x, y in zip(b, u)]
            rv = bv / (val ** q)
            del self.rows[p]
            if u[p] < 0:
                u = [-x for x in u]
                val = 1 / val
            self.rows[p] = (u, val)
            u, val = r, rv


def exponent(mono, index, n):
    v = [0] * n
    for e in mono:
        v[index[e]] += 1
    return v


def calculus_polys(terms, var, words=None):
    index = {e: k for k, e in enumerate(var)}
    n = len(var)
    polys = []
    for w in (terms if words is None else words):
        ts = [(exponent(m, index, n), Fraction(1)) for m in terms[w]]
        if is_constant(w):
            ts.append(([0] * n, Fraction(-1)))
        polys.append((w, ts))
    return polys, n


def propagate(terms, var, words=None):
    """Binomial-propagation calculus.  Every step is a valid deduction on
    the torus (all unknowns nonzero):
      * terms whose exponent difference d has a known value x^d = zeta are
        merged exactly;
      * an equation left with one live class says c * x^u = 0, c != 0:
        contradiction (monomial kill);
      * an equation left with two live classes is a new binomial relation
        x^d = zeta, inserted into the lattice; an inconsistent insertion is
        a contradiction (holonomy).
    Returns None if no contradiction is reached, else a description."""
    polys, n = calculus_polys(terms, var, words)
    lat = TorusLattice(n)
    changed = True
    while changed:
        changed = False
        for w, ts in polys:
            classes: list[list] = []
            for u, c in ts:
                for cl in classes:
                    val = lat.value([x - y for x, y in zip(u, cl[0])])
                    if val is not None:
                        cl[1] += c * val
                        break
                else:
                    classes.append([u, c])
            live = [cl for cl in classes if cl[1] != 0]
            if not live:
                continue
            if len(live) == 1:
                return ("monomial kill", w, live[0][1])
            if len(live) == 2:
                d = [x - y for x, y in zip(live[0][0], live[1][0])]
                zeta = -live[1][1] / live[0][1]
                if lat.value(d) is None:
                    try:
                        lat.add(d, zeta)
                    except Contradiction as exc:
                        return ("holonomy", w, exc.args[0])
                    changed = True
    return None


# ------------------------------------------------- sign-holonomy (binomials)

def integer_left_kernel(rows):
    m = len(rows)
    n = len(rows[0])
    a = [list(rows[i]) + [int(i == j) for j in range(m)] for i in range(m)]
    r = 0
    for col in range(n):
        while True:
            nz = [i for i in range(r, m) if a[i][col] != 0]
            if not nz:
                break
            p = min(nz, key=lambda i: abs(a[i][col]))
            a[r], a[p] = a[p], a[r]
            done = True
            for i in range(r + 1, m):
                if a[i][col]:
                    q = a[i][col] // a[r][col]
                    a[i] = [x - q * y for x, y in zip(a[i], a[r])]
                    if a[i][col]:
                        done = False
            if done:
                r += 1
                break
    return [row[n:] for row in a[r:]]


def sign_holonomy(terms, var):
    index = {e: k for k, e in enumerate(var)}
    n = len(var)
    binw = [w for w in terms if len(terms[w]) == 2 and not is_constant(w)]
    vecs = [[x - y for x, y in zip(exponent(terms[w][0], index, n),
                                    exponent(terms[w][1], index, n))]
            for w in binw]
    ker = integer_left_kernel(vecs)
    for c in ker:  # sanity: genuine integer relations
        assert all(sum(c[k] * vecs[k][j] for k in range(len(vecs))) == 0
                   for j in range(n))
    odd = [c for c in ker if sum(c) % 2]
    return len(binw), len(ker), odd


# ------------------------------------------------------------ exact replay

def strip_monomial_content(expr, syms_list):
    num, den = sp.fraction(sp.factor(sp.together(expr)))
    poly = sp.Poly(sp.expand(num), *syms_list)
    _, prim = poly.terms_gcd()
    return prim, den


def replay(label, eqs, words, syms_list):
    print(f"  -- {label}")
    subs: dict = {}
    for k, s in enumerate(words):
        w = wparse(s)
        raw = eqs[w]
        shown = (f"{sp.expand(raw + 1)} = 1" if is_constant(w)
                 else f"{raw} = 0")
        print(f"     [{s}]  {shown}")
        cur = sp.together(raw.subs(subs))
        last = k == len(words) - 1
        if not last:
            prim, _ = strip_monomial_content(cur, syms_list)
            check(len(prim.terms()) == 2,
                  f"{label}: step {s} is not a binomial after substitution")
            (m1, c1), (m2, c2) = prim.terms()
            pivot = None
            for idx, e in enumerate(m1):
                if e == 1 and m2[idx] == 0 and syms_list[idx] not in subs:
                    pivot = syms_list[idx]
                    break
            check(pivot is not None, f"{label}: no pivot at {s}")
            sol = sp.solve(prim.as_expr(), pivot)
            check(len(sol) == 1, f"{label}: pivot not linear at {s}")
            value = sp.factor(sol[0])
            subs = {key: sp.factor(v.subs(pivot, value))
                    for key, v in subs.items()}
            subs[pivot] = value
            print(f"            => {pivot} = {value}")
        else:
            final = sp.factor(sp.together(cur))
            if is_constant(w):
                print(f"            after substitution: LHS - 1 = {final}")
                check(final == -1,
                      f"{label}: constant word does not collapse to 0 = 1")
                print("            the two live terms cancel exactly: 0 = 1."
                      "  CONTRADICTION")
            else:
                num, den = sp.fraction(final)
                pnum = sp.Poly(sp.expand(num), *syms_list)
                pden = sp.Poly(sp.expand(den), *syms_list)
                ok = len(pnum.terms()) == 1 and len(pden.terms()) == 1
                check(ok, f"{label}: final equation is not c * monomial")
                coeff = pnum.terms()[0][1] if ok else None
                check(coeff not in (None, 0), f"{label}: zero coefficient")
                print(f"            after substitution: {final} = 0")
                print(f"            = {coeff} * (Laurent monomial in nonzero "
                      "unknowns) = 0.  CONTRADICTION")
    # cross-check: the substitution really solves the binomial steps
    for s in words[:-1]:
        val = sp.simplify(eqs[wparse(s)].subs(subs))
        check(val == 0, f"{label}: substitution fails to solve {s}")


# ------------------------------------------------------- minimality checks

def contradicts(terms, var, words):
    return propagate(terms, var, list(words)) is not None


def minimality(name, terms, var):
    words = list(terms)
    singles = sum(contradicts(terms, var, [w]) for w in words)
    pairs = sum(contradicts(terms, var, p)
                for p in itertools.combinations(words, 2))
    print(f"  refuting single equations: {singles}; refuting pairs: {pairs}")
    check(singles == 0 and pairs == 0, f"{name}: a <=2-equation refutation")
    index = {e: k for k, e in enumerate(var)}
    n = len(var)

    def cterms(w):
        ts = [exponent(m, index, n) for m in terms[w]]
        if is_constant(w):
            ts.append([0] * n)
        return ts

    binw = [w for w in words if len(cterms(w)) == 2]
    nonb = [w for w in words if len(cterms(w)) > 2]
    if name in ("P27", "P41"):
        tri = [c for c in itertools.combinations(binw, 3)
               if contradicts(terms, var, c)]
        print(f"  refuting triples (all equations two-term): {len(tri)}")
        # every refuting triple is a K_{2,3} odd triangle: six entries,
        # each used by exactly two of the three reduced binomials
        shapes = Counter()
        for c in tri:
            cnt = Counter()
            for w in c:
                t1, t2 = map(set, terms[w])
                com = t1 & t2
                for e in (t1 | t2) - com:
                    cnt[e] += 1
            deg = Counter()
            for e in cnt:
                deg[e[0]] += 1
                deg[e[1]] += 1
            shapes[(len(cnt), tuple(sorted(cnt.values())),
                    tuple(sorted(deg.values())))] += 1
        print(f"  triple shapes (entries, multiplicities, vertex degrees): "
              f"{dict(shapes)}")
        check(set(shapes) == {(6, (2,) * 6, (2, 2, 2, 3, 3))},
              f"{name}: a refuting triple is not a K_{{2,3}} triangle")
        check(len(tri) > 0, f"{name}: no 3-equation refutation")
    else:
        # A 3-equation refutation inside the calculus needs a non-binomial
        # equation P two of whose terms differ by an element of the lattice
        # generated by at most two binomial exponent vectors (the full
        # binomial subsystem is consistent, and nothing merges otherwise).
        bvec = {w: tuple(x - y for x, y in zip(*cterms(w))) for w in binw}

        def prim(v):
            g = 0
            for x in v:
                g = sp.igcd(g, x)
            v = tuple(x // g for x in v)
            first = next(x for x in v if x)
            return v if first > 0 else tuple(-x for x in v)

        lookup: dict = {}
        for w, v in bvec.items():
            lookup.setdefault(prim(v), []).append(w)
        hit_single, hit_pair = set(), set()
        for P in nonb:
            ts = cterms(P)
            for i, j in itertools.combinations(range(len(ts)), 2):
                d = tuple(x - y for x, y in zip(ts[i], ts[j]))
                for w in lookup.get(prim(d), []):
                    hit_single.add((P, w))
                supp = [k for k in range(n) if d[k]]
                for w1, v1 in bvec.items():
                    if not any(v1[k] for k in supp):
                        continue
                    # binomial vectors and d are 0/+-1 valued, so Cramer
                    # bounds the coefficient of v1 by 2 in absolute value
                    for a in (-2, -1, 1, 2):
                        r = tuple(x - a * y for x, y in zip(d, v1))
                        if any(r):
                            for w2 in lookup.get(prim(r), []):
                                if w2 != w1:
                                    hit_pair.add((P, w1, w2))
        check(all(x in (-1, 0, 1) for v in bvec.values() for x in v),
              f"{name}: Cramer bound assumption violated")
        found = [t for t in hit_pair if contradicts(terms, var, t)]
        for P, w1 in hit_single:
            found += [(P, w1, Q) for Q in words
                      if Q not in (P, w1) and contradicts(terms, var,
                                                          (P, w1, Q))]
        print(f"  non-binomial term pairs reachable from <=2 binomials: "
              f"{len(hit_single)} single / {len(hit_pair)} pair; "
              f"refuting triples: {len(found)}")
        check(not found, f"{name}: a 3-equation refutation exists")
    # 2x2 word squares (two vertices, two colours each, rest fixed)
    squares = set()
    for u, v in itertools.combinations(range(N), 2):
        others = [k for k in range(N) if k not in (u, v)]
        for cu in itertools.combinations(range(D), 2):
            for cv in itertools.combinations(range(D), 2):
                for rest in itertools.product(range(D), repeat=N - 2):
                    ws = []
                    for a in cu:
                        for b in cv:
                            w = [0] * N
                            w[u], w[v] = a, b
                            for k, c in zip(others, rest):
                                w[k] = c
                            ws.append(tuple(w))
                    if not all(w in terms for w in ws):
                        continue
                    if contradicts(terms, var, ws) and all(
                            not contradicts(terms, var,
                                            [x for x in ws if x != y])
                            for y in ws):
                        squares.add(frozenset(ws))
    kinds = Counter()
    for sq in squares:
        kind = ("constant word" if any(is_constant(w) for w in sq)
                else "trinomial kill"
                if any(len(terms[w]) > 2 for w in sq) else "binomial only")
        kinds[kind] += 1
    print(f"  inclusion-minimal refuting 2x2 word squares: {len(squares)} "
          f"{dict(kinds)}")


# -------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minimality", action="store_true",
                    help="also run the exhaustive minimality checks (~1 min)")
    args = ap.parse_args()

    for name, spec in PATTERNS.items():
        sup = parse(spec)
        print(f"== {name}: {len(sup)} nonzero unknowns")
        check(len(sup) == EXPECTED_SIZE[name], f"{name}: wrong size")
        var = sorted(sup)
        syms = {e: sp.Symbol(wname(e)) for e in var}
        syms_list = [syms[e] for e in var]
        terms = live_terms(sup)
        eqs = sympy_equations(sup, terms, syms)
        census = Counter((len(terms.get(w, [])), is_constant(w))
                         for w in WORDS)
        nontrivial = sum(1 for w in WORDS if eqs[w] != 0)
        print(f"  729 word equations rebuilt; nontrivial: {nontrivial}")
        print("  census (live terms, constant word): count = "
              + ", ".join(f"{k}: {v}" for k, v in sorted(census.items())))
        check(census[(0, True)] == 0,
              f"{name}: a constant word has no live term")
        check(census[(1, False)] == 0,
              f"{name}: a forbidden word is a single monomial")
        print("  no forbidden word is a single monomial; every constant word "
              "is live (support-level facts hold)")
        nb, rank, odd = sign_holonomy(terms, var)
        print(f"  forbidden-word binomials: {nb}; integer relations: {rank}; "
              f"odd relations: {len(odd)} -> binomial subsystem "
              + ("INCONSISTENT on the torus (sign holonomy -1)" if odd
                 else "consistent on the torus"))
        res = propagate(terms, var)
        print(f"  binomial-propagation calculus on all equations: {res}")
        check(res is not None, f"{name}: calculus finds no contradiction")
        for pname, label, words in REFUTATIONS:
            if pname == name:
                replay(label, eqs, words, syms_list)
                check(contradicts(terms, var, [wparse(s) for s in words]),
                      f"{name}: calculus does not confirm {label}")
        if args.minimality:
            minimality(name, terms, var)
    print()
    if FAILURES:
        print(f"FAILED ({len(FAILURES)} issues)")
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
