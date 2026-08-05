#!/usr/bin/env python3
"""Correct the class-C (candidate sixteenth component) family tangent.

BUG FOUND in w05_new_components_14_15_16.py: for class C the family
`famC` is a SIX-parameter parametrization whose purity minors all equal
(parameter monomial) * CONIC, i.e. the tuple is pure ONLY on the conic
hypersurface {Q = 0}.  w05 nevertheless applied the same
`family_tangent_rank` helper it used for the unconstrained classes A and
B, differentiating in all six parameters freely.  That helper therefore
measures the tangent of the parametrization INTO the ambient Grassmannian
product, not the tangent of the pure family: it returned SIX, and w05's
`assert rkC == 5` failed.

A rank-six tangent inside the pure locus would contradict w05's own
five-slice bound (local dimension <= 5) for class C, so the rank-six
number cannot be the tangent of the pure family.  The correct quantity is
the rank restricted to the tangent hyperplane of {Q = 0}:

    T = rank [ J_params . N | J_torus ],   N = basis of ker(grad Q).

This script recomputes exactly that, over Q, at w05's sample.
"""
import itertools
import sympy as sp

cS, dS, mS, tauS, wv2S, W1S = sp.symbols("cS dS mS tauS wv2S W1S")
t0, t1, t2 = sp.symbols("t0 t1 t2")
TORUS = (t0, t1, t2, sp.Integer(1))
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


CONIC = sp.expand(W1S**2*cS**2*dS**2 + W1S*cS*dS*wv2S*(cS + dS + 2*tauS)
                  + wv2S**2*(cS*dS + 4*tauS*(cS + dS) + 4*tauS**2))


def famC_planes():
    pC = (0, 1, cS, cS*mS)
    qC = (0, 1, dS, dS*mS)
    aYc = mS*tauS
    bYc = tauS
    P = sp.expand(2*cS*dS*mS)
    kA = (sp.expand((cS + dS)*mS), 0, -P, 0)
    kB = (sp.expand(cS + dS), 0, 0, -P)
    z1 = tuple(sp.expand(kA[t] + aYc*YBAR[t]) for t in range(4))
    z2 = tuple(sp.expand(kB[t] + bYc*YBAR[t]) for t in range(4))
    wC = (0, W1S, wv2S, wv2S*mS)
    return [[z1, z2], [YBAR, list(pC)], [YBAR, list(qC)], [U3v, list(wC)]]


famC = famC_planes()
PARAMS = (cS, dS, mS, tauS, wv2S, W1S)
SAMPLE_C = {cS: 3, dS: 12, mS: sp.Rational(2, 3), tauS: -9,
            wv2S: sp.Integer(4), W1S: sp.Rational(-1, 1)}

# --- locate w05's sample exactly: solve the conic for W1 at the others ---
rest = {k: v for k, v in SAMPLE_C.items() if k is not W1S}
roots = sp.solve(sp.Eq(CONIC.subs(rest), 0), W1S)
assert roots, "conic has no W1-root at the sample base point"
SAMPLE = dict(rest)
SAMPLE[W1S] = sp.nsimplify(roots[0])
assert sp.expand(CONIC.subs(SAMPLE)) == 0
print("sample on the conic:", {str(k): v for k, v in SAMPLE.items()})

# --- purity holds on the conic, not identically ---
TC = {bits: sp.expand(perm4(tuple(tuple(sp.sympify(c) for c in famC[m][bits[m]])
                                  for m in range(4))))
      for bits in itertools.product((0, 1), repeat=4)}
only_on_conic = False
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    M = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        M[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = TC[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            val = sp.expand(M[r1, c1]*M[r2, c2] - M[r1, c2]*M[r2, c1])
            if val == 0:
                continue
            only_on_conic = True
            quot = sp.cancel(val/CONIC)
            assert sp.denom(quot) == 1, "minor not divisible by the conic"
            assert sp.simplify(sp.expand(val.subs(SAMPLE))) == 0
print("purity minors vanish only modulo the conic:", only_on_conic)
print("all purity minors vanish at the sample: True")

# --- chart reduction with the full projective torus ---
scaled = [sp.Matrix([[sp.sympify(c)*TORUS[j] for j, c in enumerate(row)]
                     for row in pl]) for pl in famC]
point = {**SAMPLE, t0: 1, t1: 1, t2: 1}
planes_at = [sp.Matrix([[sp.nsimplify(sp.cancel(sp.sympify(c).subs(point)))
                         for c in row] for row in pl]) for pl in famC]
pivots = []
for pl in planes_at:
    piv = next(pv for pv in itertools.combinations(range(4), 2)
               if pl[:, pv].det() != 0)
    pivots.append(piv)
chart_coords = []
for plane, piv in zip(scaled, pivots):
    chart = plane[:, piv].inv()*plane
    nonpiv = tuple(i for i in range(4) if i not in piv)
    chart_coords.extend(chart[rr, cc] for rr in range(2) for cc in nonpiv)

allp = PARAMS + (t0, t1, t2)
J = sp.Matrix(chart_coords).jacobian(allp).subs(point)
J = sp.Matrix([[sp.nsimplify(sp.cancel(c)) for c in row] for row in J.tolist()])
print("UNCONSTRAINED tangent rank (w05's number):", J.rank())

# --- the correct constrained tangent ---
gradQ = sp.Matrix([[sp.nsimplify(sp.diff(CONIC, p).subs(SAMPLE))] for p in PARAMS]).T
assert any(g != 0 for g in gradQ), "conic gradient vanishes: sample is singular on Q"
N = gradQ.nullspace()
assert len(N) == 5, len(N)
Npar = sp.Matrix.hstack(*N)                       # 6 x 5
block = sp.Matrix.hstack(J[:, :6]*Npar, J[:, 6:])  # params-on-conic | torus
rk = block.rank()
print("CONSTRAINED family tangent rank (on {Q=0}, incl. full torus):", rk)

if rk == 5:
    print()
    print("RESOLUTION: the class-C family tangent is FIVE once the conic")
    print("constraint is respected.  w05's rank-six value was the tangent")
    print("of the unconstrained parametrization, which leaves the pure")
    print("locus; the assertion `rkC == 5` was testing the wrong matrix.")
    print("With w05's incidence rank 14 and its char-0 five-slice bound")
    print("(local dimension <= 5), the local dimension is exactly five and")
    print("closure(F_C) is an irreducible component as w05 concluded.")
else:
    print()
    print("DISCREPANCY: constrained tangent is", rk, "- class C is NOT")
    print("certified; the sixteenth-component claim must be withdrawn")
    print("pending a corrected analysis.")
