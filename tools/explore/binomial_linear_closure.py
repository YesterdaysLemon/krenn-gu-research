#!/usr/bin/env python3
"""Full-word binomial-linear (BL) closure of a fixed physical support.

Discovery/diagnostic tool, not a certificate checker.  For a physical support
S (a set of entries W_ij[a,b], i<j, assumed nonzero; every other entry zero)
the full-word equations of T_W = Delta are

    sum_{M live at w} X^{m_M(w)} = delta_w          (one per word w),

where X ranges over the complex torus (C^*)^S and m_M(w) is the exponent
vector of the matching monomial.  BL derives only *two-term* information:

* a lattice Lambda of exponent vectors r with a known value X^r = c(r) in Q^*
  (integer Hermite insertion; a nonzero value != 1 on the zero vector is a
  contradiction, e.g. an odd sign circuit);
* the linear row space of all fibre equations after replacing each monomial
  by c * Y_[class], where classes are cosets of Lambda;
* every linear consequence of the form Y = 0 (contradiction, since monomials
  do not vanish on the torus; Y_0 = 1 is the constant) or Y_u = c Y_v (a new
  binomial, inserted into Lambda), iterated to a fixed point.

Every deduction is valid for every complex source with exactly the support S.
A CLOSED result is not a realization claim: BL ignores every consequence that
needs a product of two non-monomial equations (Groebner-type reasoning).
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from fractions import Fraction

import flint


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    v = vertices[0]
    for k in range(1, len(vertices)):
        rest = vertices[1:k] + vertices[k + 1:]
        for m in perfect_matchings(rest):
            yield ((v, vertices[k]),) + m


class Geometry:
    def __init__(self, n: int):
        self.n = n
        self.entries = [(i, j, a, b) for i in range(n) for j in range(i + 1, n)
                        for a in range(3) for b in range(3)]
        self.index = {e: k for k, e in enumerate(self.entries)}
        self.matchings = list(perfect_matchings(tuple(range(n))))
        self.words = list(itertools.product(range(3), repeat=n))
        self.terms = []  # per word: list of sorted entry-index tuples, one per matching
        for w in self.words:
            self.terms.append([tuple(sorted(self.index[(i, j, w[i], w[j])] for i, j in m))
                               for m in self.matchings])

    def pure(self, w):
        return len(set(w)) == 1

    def name(self, k):
        i, j, a, b = self.entries[k]
        return f"W{i}{j}[{a},{b}]"


def xgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a - (a // b) * b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0


def axpy(q, b, v):
    """v + q*b for sparse dict vectors."""
    out = dict(v)
    for k, x in b.items():
        y = out.get(k, 0) + q * x
        if y:
            out[k] = y
        else:
            out.pop(k, None)
    return out


class Contradiction(Exception):
    pass


class Lattice:
    """Echelon integer basis of Lambda with values X^row = value."""

    def __init__(self):
        self.rows = {}

    def insert(self, vec, val):
        vec = {k: x for k, x in vec.items() if x}
        val = Fraction(val)
        changed = False
        while vec:
            p = min(vec)
            if p not in self.rows:
                if vec[p] < 0:
                    vec = {k: -x for k, x in vec.items()}
                    val = 1 / val
                self.rows[p] = (vec, val)
                return True
            b, bv = self.rows[p]
            if vec[p] % b[p] == 0:
                q = vec[p] // b[p]
                vec = axpy(-q, b, vec)
                val = val / bv ** q
                continue
            g, s, t = xgcd(b[p], vec[p])
            if g < 0:
                g, s, t = -g, -s, -t
            newb = axpy(s, b, {k: t * x for k, x in vec.items()}) if s else {k: t * x for k, x in vec.items()}
            newbv = bv ** s * val ** t
            newv = axpy(-(b[p] // g), vec, {k: (vec[p] // g) * x for k, x in b.items()})
            newvv = bv ** (vec[p] // g) / val ** (b[p] // g)
            self.rows[p] = (newb, newbv)
            vec, val = newv, newvv
            changed = True
        if val != 1:
            raise Contradiction(f"lattice inconsistency: X^0 = {val}")
        return changed

    def residue(self, vec):
        vec = dict(vec)
        val = Fraction(1)
        for p in sorted(self.rows):
            x = vec.get(p, 0)
            if not x:
                continue
            b, bv = self.rows[p]
            q = x // b[p]
            if q:
                vec = axpy(-q, b, vec)
                val = val * bv ** q
        return tuple(sorted(vec.items())), val


def closure(geo: Geometry, support, words=None, max_rounds=200):
    """Return (status, info).  status in {'CONTRADICTION', 'CLOSED'}."""
    support = set(support)
    if words is None:
        words = range(len(geo.words))
    fibres = []
    for wi in words:
        live = [m for m in geo.terms[wi] if all(k in support for k in m)]
        target = 1 if geo.pure(geo.words[wi]) else 0
        if not live and not target:
            continue
        fibres.append((wi, live, target))
    for wi, live, target in fibres:
        if target and not live:
            return "CONTRADICTION", {"kind": "pure word has no live matching", "word": wi}
        if not target and len(live) == 1:
            return "CONTRADICTION", {"kind": "mixed word has one live matching", "word": wi}
    lat = Lattice()
    rounds = 0
    try:
        while True:
            rounds += 1
            if rounds > max_rounds:
                return "ROUND_LIMIT", {"rounds": rounds}
            cols = {(): None}
            rows = []
            for wi, live, target in fibres:
                row = {}
                for m in live:
                    res, val = lat.residue({k: 1 for k in m})
                    row[res] = row.get(res, 0) + val
                if target:
                    row[()] = row.get((), 0) - 1
                row = {k: v for k, v in row.items() if v}
                if not row:
                    continue
                if len(row) == 1:
                    (res,) = row
                    return "CONTRADICTION", {"kind": "one surviving class", "word": wi, "rounds": rounds}
                rows.append(row)
                for k in row:
                    cols.setdefault(k, None)
            order = [k for k in cols if k != ()] + [()]
            colix = {k: c for c, k in enumerate(order)}
            if not rows:
                return "CLOSED", {"rounds": rounds, "classes": len(order), "lattice_rank": len(lat.rows)}
            mat = flint.fmpq_mat(len(rows), len(order))
            for r, row in enumerate(rows):
                for k, v in row.items():
                    mat[r, colix[k]] = flint.fmpq(v.numerator, v.denominator)
            rref, rank = mat.rref()
            pivots = []
            pivset = set()
            for r in range(rank):
                for c in range(len(order)):
                    if rref[r, c] != 0:
                        pivots.append(c)
                        pivset.add(c)
                        break
            free = [c for c in range(len(order)) if c not in pivset]
            freeix = {c: t for t, c in enumerate(free)}
            expr = {}
            for r, c in enumerate(pivots):
                vec = tuple((freeix[f], -rref[r, f]) for f in free if rref[r, f] != 0)
                expr[c] = vec
            for f in free:
                expr[f] = ((freeix[f], flint.fmpq(1)),)
            groups = {}
            for c, vec in expr.items():
                if not vec:
                    return "CONTRADICTION", {"kind": "row space forces a monomial class to vanish",
                                             "class_is_constant": order[c] == (), "rounds": rounds}
                lead = vec[0][1]
                key = tuple((t, x / lead) for t, x in vec)
                groups.setdefault(key, []).append((c, lead))
            new = False
            for members in groups.values():
                c0, l0 = members[0]
                for c1, l1 in members[1:]:
                    # Y_c1 / Y_c0 = l1 / l0
                    ratio = l1 / l0
                    r0, r1 = order[c0], order[c1]
                    vec = dict(r1)
                    for k, x in r0:
                        vec[k] = vec.get(k, 0) - x
                    if lat.insert(vec, Fraction(int(ratio.p), int(ratio.q))):
                        new = True
            if not new:
                return "CLOSED", {"rounds": rounds, "classes": len(order), "lattice_rank": len(lat.rows),
                                  "rank": rank}
    except Contradiction as exc:
        return "CONTRADICTION", {"kind": str(exc), "rounds": rounds}


def parse_pattern(geo, text):
    live = set()
    for part in text.split("|"):
        edge, colours = part.split(":")
        i, j = int(edge.strip()[0]), int(edge.strip()[1])
        for ab in colours.split():
            live.add(geo.index[(i, j, int(ab[0]), int(ab[1]))])
    return live


PATTERN27 = (
    "01: 00 20 | 02: 11 | 03: 00 20 | 04: 02 22 | 05: 00 02 20 22 | "
    "12: 00 02 | 13: 22 | 14: 11 | 15: 20 | 23: 00 20 | 24: 02 22 | "
    "25: 00 02 20 22 | 34: 20 | 35: 11 | 45: 00"
)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--pattern27", action="store_true")
    ap.add_argument("--full", action="store_true", help="every entry nonzero")
    ap.add_argument("--support-json", help="JSON list of [i,j,a,b] entries, or an object with 'entries'")
    args = ap.parse_args(argv)
    geo = Geometry(args.n)
    if args.pattern27:
        support = parse_pattern(geo, PATTERN27)
    elif args.full:
        support = set(range(len(geo.entries)))
    else:
        data = json.load(open(args.support_json, encoding="utf-8"))
        if isinstance(data, dict):
            data = data["entries"]
        support = {geo.index[tuple(e)] for e in data}
    t = time.monotonic()
    status, info = closure(geo, support)
    print(json.dumps({"status": status, **{k: str(v) for k, v in info.items()},
                      "seconds": round(time.monotonic() - t, 3)}))


if __name__ == "__main__":
    sys.exit(main())
