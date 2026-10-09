"""Exact finite checks for the AP' arc-lemma attempt (2026-10-08).

Companion of docs/strategy/arc-lemma-attempt-2026-10-08.md.  This script is a
cross-check of finitely many instances; the statements themselves are proved
by hand in the note, at every even order.

Part A (hole model, Theorem A of the note).  For n in {6, 8, 10, 12} it builds
G_1 = K_n - M_0 and

    S_1 = {empty, V} + {even A : A not an M_0-union and A not {0,1,x,y}
                         with x, y outside {0,1} and xy not in M_0},

and checks by brute force: (a), (S), (F), (L), that no proper nonempty
M_0-union lies in S_1, and that for every perfect matching N of G_1 with
M_0 + N a Hamiltonian cycle some N-ended arc of that cycle is missing from
S_1 (and that the 4-arc through the M_0-edge 01 is one of them).

Part B (adjacent-crossing lemma, Lemma C of the note).  For every even n in
[6, 16], with C the cycle 0-1-...-(n-1), M_0 = {2i, 2i+1}, N = {2i+1, 2i+2}:
every perfect matching F of the same-parity pairs has an even vertex x whose
chord crosses the chord of x+1; for every such x the complement of the four
endpoints is a union of even runs of C with at most one N-tiled run; the
clockwise-length identity and the crossing criterion used by the hand proof
hold; for n = 2 (mod 4) no such F exists.

Part C (sharpness model T(n), Theorem D of the note).  For n in {8, 12}:
G_0 = M_0, G_2 = N_2 with S_0, S_2 their unions, G_1 = all same-parity
pairs and S_1 = {empty, V} + {A : |A cap X|, |A cap Y| even, A not
alternating}.  Checks every AP' axiom by brute force, (H2) over all ordered
partitions, except (F) in colour 1, which is checked to fail.

Exit code 0 and "result": "PASS" when every check holds.
"""

from __future__ import annotations

import itertools
import json
import sys
import time


def m0_closed(A):
    return all((v ^ 1) in A for v in A)


def hole_family(n):
    V = frozenset(range(n))
    G = {frozenset(p) for p in itertools.combinations(range(n), 2) if p[0] ^ 1 != p[1]}

    def member(A):
        A = frozenset(A)
        if not A or A == V:
            return True
        if len(A) % 2 or m0_closed(A):
            return False
        if len(A) == 2:
            return A in G
        if len(A) == 4 and {0, 1} <= A:
            x, y = sorted(A - {0, 1})
            if x ^ 1 != y:
                return False
        return True
    return V, G, member


def count_pm(A, G, cap=2):
    """Number of perfect matchings of G[A], counted up to cap."""
    A = sorted(A)
    if not A:
        return 1
    v, rest = A[0], A[1:]
    total = 0
    for u in rest:
        if frozenset((v, u)) in G:
            total += count_pm([w for w in rest if w != u], G, cap - total)
            if total >= cap:
                return total
    return total


def hamiltonian_orders(n):
    m = n // 2
    for perm in itertools.permutations(range(1, m)):
        for flips in itertools.product((0, 1), repeat=m - 1):
            order = [0, 1]
            for k, f in zip(perm, flips):
                order += [2 * k + 1, 2 * k] if f else [2 * k, 2 * k + 1]
            yield order


def part_a(n):
    V, G, member = hole_family(n)
    bad = []
    evens = [frozenset(A) for k in range(0, n + 1, 2) for A in itertools.combinations(range(n), k)]
    for A in evens:
        inS = member(A)
        if len(A) == 2 and inS != (A in G):
            bad.append(("a", sorted(A)))
        if A and A != V and m0_closed(A) and inS:
            bad.append(("M0-union in S_1", sorted(A)))
        if len(A) >= 2:
            c = count_pm(A, G)
            if inS and c == 0:
                bad.append(("S", sorted(A)))
            if c == 1 and not inS:
                bad.append(("F", sorted(A)))
        if inS and A:
            for v in A:
                if not any(frozenset((v, u)) in G and member(A - {v, u}) for u in A if u != v):
                    bad.append(("L", sorted(A), v))
    cycles = holes = 0
    for order in hamiltonian_orders(n):
        N = [frozenset((order[i], order[(i + 1) % n])) for i in range(1, n, 2)]
        if not all(e in G for e in N):
            continue
        cycles += 1
        arcs = {frozenset(order[(i + j) % n] for j in range(2 * k))
                for i in range(1, n, 2) for k in range(1, n // 2)}
        missing = [A for A in arcs if not member(A)]
        pos = {v: i for i, v in enumerate(order)}
        through01 = frozenset((order[n - 1], 0, 1, order[2]))
        if not missing:
            bad.append(("arc lemma holds", order))
        elif through01 not in missing:
            bad.append(("4-arc through 01 present", order))
        holes += len(missing)
    return {"n": n, "violations": [str(b) for b in bad[:5]], "hamiltonian_cycles": cycles,
            "missing_arc_incidences": holes, "ok": not bad}


def same_parity_pms(n):
    def pms(vs):
        if not vs:
            yield ()
            return
        a, rest = vs[0], vs[1:]
        for k, b in enumerate(rest):
            for t in pms(rest[:k] + rest[k + 1:]):
                yield ((a, b),) + t
    X = list(range(0, n, 2))
    Y = list(range(1, n, 2))
    if len(X) % 2:
        return
    for fx in pms(X):
        for fy in pms(Y):
            yield fx, fy


def crosses(e, f, n):
    a, c = sorted(e)
    return sum(1 for x in f if a < x < c) == 1


def runs_ok(A, n):
    """Complement of A: maximal cyclic runs, all of even length; return the
    number of N-tiled runs (runs starting at an odd vertex) or None."""
    A = sorted(A)
    nruns_N = 0
    for i, a in enumerate(A):
        b = A[(i + 1) % len(A)]
        length = (b - a - 1) % n
        if length % 2:
            return None
        if length and (a + 1) % 2 == 1:
            nruns_N += 1
    return nruns_N


def part_b(n):
    """Lemma C of the note: some M_0-edge {x, x+1} (x even) carries crossing
    chords of F, and then the complement of the four endpoints is a union of
    even runs with at most one N-tiled run.  Also: for every crossing pair of
    opposite-parity chords the complement is a union of even runs (at most two
    N-tiled), and the length identity behind the counting proof."""
    count = 0
    bad = []
    for fx, fy in same_parity_pms(n):
        count += 1
        F = {}
        for a, b in fx + fy:
            F[a], F[b] = b, a
        ell = {v: (F[v] - v) % n for v in range(n)}
        if sum(ell[v] for v in range(0, n, 2)) != n * n // 4 or \
                sum(ell[v] for v in range(1, n, 2)) != n * n // 4:
            bad.append(("length identity", fx, fy))
        adjacent = []
        for x in range(0, n, 2):
            e, f = (x, F[x]), (x + 1, F[x + 1])
            cross = crosses(e, f, n)
            if cross != (ell[x + 1] >= ell[x]):        # non-crossing iff ell(x+1) <= ell(x) - 2
                bad.append(("crossing criterion", x, fx, fy))
            if cross:
                adjacent.append((e, f))
        if not adjacent:
            bad.append(("no M0-adjacent crossing", fx, fy))
        for e, f in adjacent:
            r = runs_ok(set(e) | set(f), n)
            if r is None or r > 1:
                bad.append(("adjacent runs", e, f, r))
        for e in fx:
            for f in fy:
                if crosses(e, f, n):
                    r = runs_ok(set(e) | set(f), n)
                    if r is None or r > 2:
                        bad.append(("runs", e, f, r))
    expect_none = (n % 4 == 2)
    if expect_none and count:
        bad.append(("matching exists at n = 2 mod 4",))
    return {"n": n, "same_parity_perfect_matchings": count, "violations": [str(b) for b in bad[:5]],
            "ok": not bad}


def alternating(A, n):
    A = sorted(A)
    return all((A[(i + 1) % len(A)] - A[i]) % 2 == 1 for i in range(len(A)))


def part_c(n):
    """Model T(n) (Theorem D of the note): every AP' axiom except colour-1 (F)."""
    V = frozenset(range(n))
    M0 = {frozenset((2 * i, 2 * i + 1)) for i in range(n // 2)}
    N2 = {frozenset((2 * i + 1, (2 * i + 2) % n)) for i in range(n // 2)}
    G = {0: M0, 2: N2,
         1: {frozenset(p) for p in itertools.combinations(range(n), 2) if p[0] % 2 == p[1] % 2}}

    def union_of(A, M):
        return all(any(v in e and e <= A for e in M) for v in A)

    def member(c, A):
        A = frozenset(A)
        if not A or A == V:
            return True
        if len(A) % 2:
            return False
        if c == 0:
            return union_of(A, M0)
        if c == 2:
            return union_of(A, N2)
        if sum(1 for v in A if v % 2 == 0) % 2:
            return False
        return not alternating(A, n)

    bad = []
    f_failures = 0
    evens = [frozenset(A) for k in range(2, n + 1, 2) for A in itertools.combinations(range(n), k)]
    for c in (0, 1, 2):
        for A in evens:
            inS = member(c, A)
            if len(A) == 2 and inS != (A in G[c]):
                bad.append(("a", c, sorted(A)))
            cnt = count_pm(A, G[c])
            if inS and cnt == 0:
                bad.append(("S", c, sorted(A)))
            if cnt == 1 and not inS:
                if c == 1:
                    f_failures += 1
                else:
                    bad.append(("F", c, sorted(A)))
            if inS:
                for v in A:
                    if not any(frozenset((v, u)) in G[c] and member(c, A - {v, u}) for u in A if u != v):
                        bad.append(("L", c, sorted(A), v))
    h2 = 0
    for word in itertools.product(range(3), repeat=n):
        cl = [frozenset(v for v in range(n) if word[v] == c) for c in range(3)]
        if any(len(A) % 2 for A in cl) or sum(1 for A in cl if A) < 2:
            continue
        h2 += 1
        if all(member(c, cl[c]) for c in range(3)):
            bad.append(("H2", [sorted(A) for A in cl]))
    if f_failures == 0:
        bad.append(("colour-1 forcing unexpectedly holds",))
    return {"n": n, "partitions_checked": h2, "colour1_forcing_failures": f_failures,
            "violations": [str(b) for b in bad[:5]], "ok": not bad}


def main() -> int:
    t0 = time.time()
    a = [part_a(n) for n in (6, 8, 10, 12)]
    b = [part_b(n) for n in range(6, 17, 2)]
    c = [part_c(n) for n in (8, 12)]
    ok = all(r["ok"] for r in a + b + c)
    print(json.dumps({"part_a_hole_model": a, "part_b_crossing_lemma": b,
                      "part_c_model_without_colour1_forcing": c,
                      "result": "PASS" if ok else "FAIL",
                      "seconds": round(time.time() - t0, 1)}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
