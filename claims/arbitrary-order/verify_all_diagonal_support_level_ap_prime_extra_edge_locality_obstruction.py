"""Exact checks for the locality obstruction to the AP' extra-edge sub-lemma.

Companion to ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_TOP_MATCHING_EXTRA_EDGE_LEMMA.md.

The obstruction (Theorem 2 of that document) uses a simple cubic graph K whose
edge set is the disjoint union of three perfect matchings M_0, N_1, N_2 and
whose girth is at least 10.  This script

1. rebuilds two explicit bipartite examples from embedded permutation data
   (A-vertex i is joined to B-vertices i, p1[i], p2[i]; colour classes are
   M_0 = {A_i B_i}, N_1 = {A_i B_p1[i]}, N_2 = {A_i B_p2[i]}),
   and checks exactly that each colour class is a perfect matching, that the
   classes are pairwise disjoint (so K is simple and cubic), and that the
   girth of K is at least 10 (exact breadth-first search from every vertex);
2. cross-checks the counting argument of Theorem 2 by a SAT search (CaDiCaL
   via python-sat) for a perfect matching F of K with F not in {M_0, N_1, N_2}
   and |F ∩ N_c| in {0, 1, 2, m-2, m-1, m} for c = 1, 2 (m = n/2), which is
   exactly a rainbow partition whose classes lie in the relaxed families of
   Theorem 2.  The expected answer is UNSAT.  This is a second route to the
   same statement, not the proof: the proof is the hand argument in the
   document, which needs only the girth bound checked in step 1;
3. runs the same SAT search on two small controls of low girth (K_{3,3} and
   the cube Q_3, each with a proper 3-edge-colouring), where the expected
   answer is SAT, so the search is not vacuous.

The two orders n = 2m and n = 2m + 2 have coprime halves, so disjoint unions
of copies of the two examples give such graphs at every even order
n >= 2 m (m - 1) (Frobenius); the document states this corollary.
"""

from __future__ import annotations

import collections
import json
import sys

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical153

EXAMPLES = {
    80: (
        [72, 4, 15, 58, 44, 17, 9, 69, 25, 67, 50, 19, 36, 77, 27, 75, 68, 48, 52, 21, 47, 23, 38, 20,
         42, 79, 73, 8, 35, 61, 45, 18, 40, 16, 78, 29, 33, 74, 3, 1, 12, 22, 28, 59, 70, 53, 76, 13,
         43, 24, 64, 55, 34, 54, 65, 2, 10, 39, 37, 41, 51, 46, 26, 31, 0, 7, 49, 5, 62, 30, 56, 14,
         60, 57, 63, 11, 32, 71, 66, 6],
        [2, 75, 58, 23, 62, 45, 12, 46, 64, 26, 4, 55, 42, 1, 29, 16, 7, 68, 54, 57, 10, 25, 70, 36,
         48, 44, 28, 5, 79, 31, 15, 6, 13, 59, 67, 30, 27, 17, 9, 63, 56, 72, 53, 3, 61, 21, 78, 19,
         76, 41, 37, 43, 22, 32, 74, 14, 35, 69, 34, 40, 18, 0, 71, 20, 77, 38, 73, 39, 52, 60, 51, 24,
         47, 50, 66, 49, 8, 65, 33, 11],
    ),
    81: (
        [67, 4, 11, 0, 51, 61, 36, 65, 53, 72, 50, 39, 75, 78, 54, 25, 29, 47, 5, 21, 77, 42, 45, 10,
         57, 48, 9, 69, 23, 56, 16, 71, 22, 52, 55, 80, 43, 76, 62, 1, 35, 6, 28, 31, 60, 26, 27, 13,
         64, 24, 70, 15, 41, 37, 66, 8, 20, 7, 17, 19, 14, 44, 46, 34, 74, 59, 18, 49, 3, 79, 12, 40,
         68, 33, 30, 63, 2, 32, 73, 58, 38],
        [2, 76, 58, 27, 8, 48, 78, 16, 11, 6, 18, 41, 3, 25, 52, 39, 69, 7, 51, 57, 10, 67, 79, 43, 9,
         71, 28, 60, 80, 61, 1, 70, 31, 46, 23, 30, 0, 50, 77, 26, 68, 20, 53, 24, 55, 56, 19, 42, 59,
         63, 72, 62, 22, 40, 64, 32, 35, 73, 34, 4, 49, 12, 37, 29, 17, 36, 21, 74, 15, 38, 65, 14, 47,
         44, 33, 66, 54, 13, 45, 5, 75],
    ),
}


def bipartite_classes(m, p1, p2):
    """Colour classes as lists of edges (u, v) on vertices 0..2m-1 (A = 0..m-1, B = m..2m-1)."""
    return [[(i, m + p[i]) for i in range(m)] for p in (list(range(m)), p1, p2)]


def check_proper_cubic(nv, classes):
    for X in classes:
        covered = collections.Counter(v for e in X for v in e)
        assert len(X) * 2 == nv and set(covered) == set(range(nv)) and max(covered.values()) == 1, \
            "a colour class is not a perfect matching"
    edges = [frozenset(e) for X in classes for e in X]
    assert len(set(edges)) == len(edges), "colour classes overlap (multigraph)"
    return edges


def girth(nv, edges):
    adj = collections.defaultdict(list)
    for e in edges:
        u, v = tuple(e)
        adj[u].append(v)
        adj[v].append(u)
    best = float("inf")
    for s in range(nv):
        dist = {s: 0}
        par = {s: -1}
        queue = collections.deque([s])
        while queue:
            v = queue.popleft()
            for w in adj[v]:
                if w == par[v]:
                    continue
                if w in dist:
                    best = min(best, dist[v] + dist[w] + 1)
                else:
                    dist[w] = dist[v] + 1
                    par[w] = v
                    queue.append(w)
    return best


def relaxed_rainbow_exists(nv, classes):
    """SAT: perfect matching F of K, F not a colour class, |F ∩ N_c| <= 2 or >= m-2 (c = 1, 2)."""
    m = nv // 2
    pool = IDPool()
    var = {}
    for c, X in enumerate(classes):
        for e in X:
            var[(c, e)] = pool.id(("x", c, e))
    clauses = []
    incident = collections.defaultdict(list)
    for (c, e), x in var.items():
        for v in e:
            incident[v].append(x)
    for v, xs in incident.items():                        # exactly one edge of F at v
        clauses.append(xs)
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                clauses.append([-xs[i], -xs[j]])
    for c, X in enumerate(classes):                       # F is not the colour class X
        clauses.append([-var[(c, e)] for e in X])
    for c in (1, 2):                                      # |F ∩ N_c| in {0,1,2} or {m-2,m-1,m}
        lits = [var[(c, e)] for e in classes[c]]
        small = pool.id(("small", c))
        lo = CardEnc.atmost(lits, bound=2, vpool=pool, encoding=EncType.seqcounter)
        hi = CardEnc.atleast(lits, bound=max(m - 2, 0), vpool=pool, encoding=EncType.seqcounter)
        clauses += [cl + [-small] for cl in lo.clauses]
        clauses += [cl + [small] for cl in hi.clauses]
    with Cadical153(bootstrap_with=clauses) as solver:
        return solver.solve()


def controls():
    # K_{3,3}: A = 0,1,2 ; B = 3,4,5 ; colour classes by cyclic shift
    k33 = [[(i, 3 + (i + s) % 3) for i in range(3)] for s in range(3)]
    # cube Q_3: vertices 0..7, colour class d = edges flipping bit d
    q3 = [[(v, v ^ (1 << d)) for v in range(8) if not v & (1 << d)] for d in range(3)]
    return {"K33": (6, k33), "Q3": (8, q3)}


def main() -> int:
    report = {"examples": [], "controls": []}
    ok = True
    for m, (p1, p2) in sorted(EXAMPLES.items()):
        assert sorted(p1) == list(range(m)) and sorted(p2) == list(range(m))
        classes = bipartite_classes(m, p1, p2)
        edges = check_proper_cubic(2 * m, classes)
        g = girth(2 * m, edges)
        sat = relaxed_rainbow_exists(2 * m, classes)
        row = {"n": 2 * m, "edges": len(edges), "girth": g, "girth_at_least_10": g >= 10,
               "relaxed_rainbow_partition": "SAT" if sat else "UNSAT"}
        report["examples"].append(row)
        ok &= g >= 10 and not sat
    for name, (nv, classes) in controls().items():
        edges = check_proper_cubic(nv, classes)
        g = girth(nv, edges)
        sat = relaxed_rainbow_exists(nv, classes)
        report["controls"].append({"name": name, "n": nv, "girth": g,
                                   "relaxed_rainbow_partition": "SAT" if sat else "UNSAT"})
        ok &= sat
    halves = sorted(EXAMPLES)
    report["frobenius_bound_n"] = 2 * (halves[0] * halves[1] - halves[0] - halves[1] + 1)
    report["result"] = "PASS" if ok else "FAIL"
    print(json.dumps(report, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
