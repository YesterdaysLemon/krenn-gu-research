"""Exact verifier: the 128-entry n=8 recursive-support-model pattern is not
fibre-realizable (four-word rank-one grid identity).

Pattern S128 is the SAT model of
`explore_general_block_recursive_support_model.py 8 --killers --plane-rigidity`
printed in docs/strategy/hyperdeterminant-crossing-2026-10-09.md, Section 4.2.
Findings: docs/strategy/n8-support-realizability-2026-10-09.md.

Convention (as in the model script): W_ij[a,b] for i<j, a = colour at i,
b = colour at j; T_W(w) = sum over the 105 perfect matchings M of K_8 of
prod_{ij in M} W_ij[w_i, w_j].

Checked here, in exact integer polynomial arithmetic (sympy):

1. With every entry outside S128 set to zero, the four word polynomials
   E00 = T(01010101), E10 = T(11010101), E01 = T(01110101), E11 = T(11110101)
   (vertex 0 colour a, vertex 2 colour b; other colours 1,1,0,1,0,1 at
   vertices 1,3,4,5,6,7) satisfy the identity

     p1*Y0*Z = p1*Y0*E01 - p0*Y0*E11 + p0*Y1*E10 - p1*Y1*E00,

   p_a = W05[a,1], Y_b = W15[1,1] W23[b,1] W46[0,0],
   Z = W02[0,1] W15[1,1] W37[1,1] W46[0,0].
   At a GHZ witness all four words are nonconstant, so the right side is 0,
   while the left side is a product of six support entries.  Hence no
   configuration supported within S128 with those six entries nonzero has
   matching tensor GHZ(8,3) (any field; no division).
2. A greedy reduction of the zero hypotheses: starting from the full complex
   K_8 configuration, the script re-zeroes only the entries needed for the
   identity and prints that smaller zero set.
"""

from __future__ import annotations

import itertools

import sympy as sp

S128 = ("01: 00 01 02 10 11 20 21 22 | 02: 01 02 | 03: 00 | 04: 01 11 21 | 05: 00 01 10 11 12 20 21 | 06: 22 | 07: ALL | "
        "12: 21 | 13: 00 01 02 10 11 20 21 | 14: 00 | 15: ALL | 16: 12 | 17: ALL | 23: ALL | 24: 00 02 10 11 12 20 21 22 | "
        "25: 21 | 26: 00 01 02 | 27: 01 02 10 12 22 | 34: 21 | 35: 12 | 36: 00 01 02 11 12 20 21 22 | 37: 10 11 12 | "
        "45: 00 02 11 12 20 22 | 46: 00 01 02 10 12 20 21 22 | 47: 21 | 56: 00 01 02 12 20 21 | 57: 00 | "
        "67: 00 01 02 10 11 12 20 22")
N = 8


def parse(spec):
    sup = set()
    for part in spec.split("|"):
        key, vals = part.split(":")
        i, j = int(key.strip()[0]), int(key.strip()[1])
        items = [f"{a}{b}" for a in range(3) for b in range(3)] if vals.strip() == "ALL" else vals.split()
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
     for i, j in itertools.combinations(range(N), 2) for a in range(3) for b in range(3)}
PM = list(matchings(tuple(range(N))))


def T(word, zero):
    w = [int(c) for c in word]
    tot = 0
    for M in PM:
        keys = [(i, j, w[i], w[j]) for i, j in M]
        if any(k in zero for k in keys):
            continue
        tot += sp.Mul(*[X[k] for k in keys])
    return sp.expand(tot)


def identity_residual(zero):
    E = {(0, 0): T("01010101", zero), (1, 0): T("11010101", zero),
         (0, 1): T("01110101", zero), (1, 1): T("11110101", zero)}
    p = {a: X[(0, 5, a, 1)] for a in (0, 1)}
    Y = {b: X[(1, 5, 1, 1)] * X[(2, 3, b, 1)] * X[(4, 6, 0, 0)] for b in (0, 1)}
    Z = X[(0, 2, 0, 1)] * X[(1, 5, 1, 1)] * X[(3, 7, 1, 1)] * X[(4, 6, 0, 0)]
    lhs = p[1] * Y[0] * Z
    rhs = p[1] * Y[0] * E[(0, 1)] - p[0] * Y[0] * E[(1, 1)] + p[0] * Y[1] * E[(1, 0)] - p[1] * Y[1] * E[(0, 0)]
    return sp.expand(lhs - rhs), E


def main():
    sup = parse(S128)
    assert len(sup) == 128
    outside = set(X) - sup
    res, E = identity_residual(outside)
    for key, poly in sorted(E.items()):
        print(f"E{key[0]}{key[1]} ({len(poly.args) if poly.is_Add else 1} terms):", poly)
    assert res == 0, "identity fails on S128"
    needed_nonzero = [(0, 5, 1, 1), (1, 5, 1, 1), (2, 3, 0, 1), (4, 6, 0, 0), (0, 2, 0, 1), (3, 7, 1, 1)]
    assert all(k in sup for k in needed_nonzero)
    print("PASS identity p1*Y0*Z = p1*Y0*E01 - p0*Y0*E11 + p0*Y1*E10 - p1*Y1*E00 on S128")
    # greedy: try to drop zero hypotheses one at a time (only entries that occur
    # in the four unrestricted word polynomials matter)
    words = ["01010101", "11010101", "01110101", "11110101"]
    relevant = set()
    for wd in words:
        w = [int(c) for c in wd]
        for M in PM:
            relevant |= {(i, j, w[i], w[j]) for i, j in M}
    zero = sorted(outside & relevant)
    kept = list(zero)
    for k in zero:
        trial = set(kept) - {k}
        if identity_residual(trial)[0] == 0:
            kept.remove(k)
    print(f"PASS reduced zero hypotheses: {len(kept)} of {len(zero)} relevant outside entries:")
    print("  " + " ".join(f"W{i}{j}[{a}{b}]" for i, j, a, b in kept))
    assert identity_residual(set(kept))[0] == 0


if __name__ == "__main__":
    main()
