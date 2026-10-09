"""Exact verifier: the 156-entry n=8 recursive-support-model pattern S156 is not
fibre-realizable with exact support (diagonal-anchor identity).

Pattern S156 is printed in docs/strategy/hyperdeterminant-crossing-2026-10-09.md,
Section 3.4; it is copied verbatim below and cross-checked against that text.
Findings: docs/strategy/s156-hub-trichotomy-2026-10-09.md.

Convention (as in explore_general_block_recursive_support_model.py): W_ij[a,b]
for i<j, a = colour at i, b = colour at j; T_W(w) = sum over the 105 perfect
matchings M of K_8 of prod_{ij in M} W_ij[w_i, w_j].  For a vertex v and a
partner u, "row c of the block at v" is the vector (W_vu[c, d])_d, oriented
with the colour of v first.

Diagonal-anchor lemma (docs/research-notes.md, "Diagonal-anchor refinement"):
contract v with e_c and every other vertex u with a vector y_u in ker(l_u),
l_u = row c at v of W_vu.  Every perfect matching uses one edge vu, whose
factor is l_u . y_u = 0, so

    sum_{w : w_v = c} T(w) prod_{u != v} y_u[w_u] = 0      (as a polynomial).  (*)

At a GHZ witness (nonconstant words 0, constant words lambda_c != 0) the left
side is lambda_c prod_u y_u[c].  So some l_u is a nonzero multiple of e_c.

Checked here, in exact integer polynomial arithmetic (sympy):

A. (*) on the generic K_8 configuration (all 252 entries independent) for
   (v,c) = (0,0) and y_u = W_0u[0,1] e_0 - W_0u[0,0] e_1 for all seven u:
   128 words, identically zero.
B. Anchor census on S156: the (v,c) with no partner u whose row c at v is
   supported exactly on colour c of u.  Ten tasks; vertex 5 is the only
   vertex with all three anchors.
C. For each anchor-less task, (*) restricted to S156 with explicit polynomial
   y_u: y_u = W(c,d_u) e_c - W(c,c) e_{d_u} on a full row (d_u the least
   off-diagonal colour), y_u = W(c,d) e_c on a row whose only entry is
   off-diagonal, y_u = e_c on a zero row.  The identity is exact with every
   entry outside S156 set to zero, and the constant-word coefficient is the
   monomial prod_u y_u[c] of support entries.  Hence

     lambda_c * prod_{u : row c at v nonzero} W_vu[c, d_u] = 0

   at any witness supported within S156: no configuration supported within
   S156 in which these (at most seven) entries are nonzero has matching
   tensor GHZ(8,3).  For the task (2,0) the four entries are
   W12[1,0], W23[0,1], W26[0,1], W27[0,1] and the identity has 16 words.
D. Cross-check (printed, not asserted): S128, excluded separately by
   verify_n8_recursive_support_s128_grid_identity.py, also has anchor-less
   tasks (eleven), so the same lemma excludes it with exact support too.
"""

from __future__ import annotations

import itertools
from pathlib import Path

import sympy as sp

S156 = ("01: ALL | 02: 02 | 03: 00 | 04: 11 | 05: ALL | 06: ALL | 07: ALL | 12: ALL | 13: ALL | 14: ALL | "
        "15: 11 | 16: 22 | 17: 20 | 23: ALL | 24: 21 | 25: 22 | 26: ALL | 27: ALL | 34: ALL | 35: ALL | "
        "36: 02 | 37: 11 | 45: ALL | 46: 10 | 47: ALL | 56: ALL | 57: 00 | 67: ALL")
S128 = ("01: 00 01 02 10 11 20 21 22 | 02: 01 02 | 03: 00 | 04: 01 11 21 | 05: 00 01 10 11 12 20 21 | 06: 22 | 07: ALL | "
        "12: 21 | 13: 00 01 02 10 11 20 21 | 14: 00 | 15: ALL | 16: 12 | 17: ALL | 23: ALL | 24: 00 02 10 11 12 20 21 22 | "
        "25: 21 | 26: 00 01 02 | 27: 01 02 10 12 22 | 34: 21 | 35: 12 | 36: 00 01 02 11 12 20 21 22 | 37: 10 11 12 | "
        "45: 00 02 11 12 20 22 | 46: 00 01 02 10 12 20 21 22 | 47: 21 | 56: 00 01 02 12 20 21 | 57: 00 | "
        "67: 00 01 02 10 11 12 20 22")
N = 8
C = 3
V = tuple(range(N))
SOURCE = Path(__file__).resolve().parents[3] / "docs" / "strategy" / "hyperdeterminant-crossing-2026-10-09.md"


def parse(spec):
    sup = set()
    for part in spec.split("|"):
        key, vals = part.split(":")
        i, j = int(key.strip()[0]), int(key.strip()[1])
        items = [f"{a}{b}" for a in range(C) for b in range(C)] if vals.strip() == "ALL" else vals.split()
        sup |= {(i, j, int(e[0]), int(e[1])) for e in items}
    return sup


def matchings(vs):
    if not vs:
        yield ()
        return
    for k in range(1, len(vs)):
        for m in matchings(vs[1:k] + vs[k + 1:]):
            yield ((vs[0], vs[k]),) + m


X = {(i, j, a, b): sp.Symbol(f"W{i}{j}_{a}{b}")
     for i, j in itertools.combinations(V, 2) for a in range(C) for b in range(C)}
PM = list(matchings(V))
assert len(PM) == 105


def key(v, u, x, y):
    """Entry with colour x at v and colour y at u, in the i<j convention."""
    return (v, u, x, y) if v < u else (u, v, y, x)


def T(w, sup=None):
    tot = 0
    for M in PM:
        keys = [key(i, j, w[i], w[j]) for i, j in M]
        if sup is not None and any(k not in sup for k in keys):
            continue
        tot += sp.Mul(*[X[k] for k in keys])
    return tot


def contraction(v, c, ys, sup=None):
    """sum over words with w_v = c of T(w) prod_u y_u[w_u]; ys[u] = {colour: poly}."""
    others = [u for u in V if u != v]
    total = 0
    count = 0
    for cols in itertools.product(*[sorted(ys[u]) for u in others]):
        w = [0] * N
        w[v] = c
        for u, z in zip(others, cols):
            w[u] = z
        weight = sp.Mul(*[ys[u][z] for u, z in zip(others, cols)])
        total += weight * T(w, sup)
        count += 1
    return sp.expand(total), count


# ---------------------------------------------------------------- part A
def part_a():
    v, c = 0, 0
    ys = {u: {0: X[key(v, u, 0, 1)], 1: -X[key(v, u, 0, 0)]} for u in V if u != v}
    res, count = contraction(v, c, ys)
    assert count == 128 and res == 0
    print("PASS A  generic K_8: sum_{w_0=0} T(w) prod_u y_u[w_u] == 0 for y_u in ker(row 0 of W_0u) "
          f"({count} words, 252 independent entries)")


# ---------------------------------------------------------------- part B
def anchor_census(sup):
    """For each (v,c): the partners whose row c at v is supported exactly on colour c."""
    out = {}
    for v in V:
        for c in range(C):
            out[(v, c)] = [u for u in V if u != v
                           and key(v, u, c, c) in sup
                           and all(key(v, u, c, d) not in sup for d in range(C) if d != c)]
    return out


def part_b(sup):
    cen = anchor_census(sup)
    missing = sorted(t for t, us in cen.items() if not us)
    expected = [(0, 2), (1, 0), (2, 0), (2, 1), (3, 2), (4, 0), (4, 2), (6, 0), (6, 1), (7, 2)]
    assert missing == expected, missing
    assert all(cen[(5, c)] for c in range(C))
    print(f"PASS B  S156 anchor census: {len(missing)} tasks with no diagonal anchor: {missing}")
    return missing


# ---------------------------------------------------------------- part C
def task_identity(v, c, sup):
    ys, needed = {}, []
    for u in V:
        if u == v:
            continue
        offd = [d for d in range(C) if d != c and key(v, u, c, d) in sup]
        diag = key(v, u, c, c) in sup
        if offd:
            d = offd[0]
            y = {c: X[key(v, u, c, d)]}
            if diag:
                y[d] = -X[key(v, u, c, c)]
            needed.append(key(v, u, c, d))
        else:
            assert not diag, "task has an anchor"
            y = {c: sp.Integer(1)}
        ys[u] = y
    res, count = contraction(v, c, ys, sup)
    lead = sp.Mul(*[X[k] for k in needed])
    tconst = sp.expand(T([c] * N, sup))
    assert tconst != 0
    return res, count, needed, lead, tconst


def part_c(sup, missing):
    for v, c in missing:
        res, count, needed, lead, tconst = task_identity(v, c, sup)
        assert res == 0, (v, c)
        assert all(k in sup for k in needed)
        names = " ".join(f"W{i}{j}[{a}{b}]" for i, j, a, b in needed)
        print(f"PASS C  task ({v},{c}): identity over {count} words is exact on S156; "
              f"T({c}^8) ({len(sp.Add.make_args(tconst))} monomials) * prod of {len(needed)} entries "
              f"{names} lies in the span of the nonconstant words")
        if (v, c) == (2, 0):
            assert count == 16
            assert needed == [(1, 2, 1, 0), (2, 3, 0, 1), (2, 6, 0, 1), (2, 7, 0, 1)], needed


def part_d():
    cen = anchor_census(parse(S128))
    missing = sorted(t for t, us in cen.items() if not us)
    print(f"INFO D  S128 anchor census: {len(missing)} tasks with no diagonal anchor: {missing}")


def main():
    sup = parse(S156)
    assert len(sup) == 156
    if SOURCE.exists():
        text = SOURCE.read_text(encoding="utf-8")
        start = text.index("01: ALL | 02: 02")
        block = " | ".join(line.strip() for line in text[start:].split("```")[0].strip().splitlines())
        assert parse(block) == sup, "S156 differs from the source note"
        print("PASS    S156 matches docs/strategy/hyperdeterminant-crossing-2026-10-09.md Section 3.4")
    part_a()
    missing = part_b(sup)
    part_c(sup, missing)
    part_d()
    print("ALL PASS")


if __name__ == "__main__":
    main()
