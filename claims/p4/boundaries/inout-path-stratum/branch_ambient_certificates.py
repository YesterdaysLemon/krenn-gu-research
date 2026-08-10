#!/usr/bin/env python3
"""Deliverable 3: the ambient component of the two singular deep branches.

Main theorem-grade certificates (all asserted below, exact rational/symbolic):

 (Z) The "coincident-support double-arrow" family
        U_I = span(ybar, (0,1,b,-b*k)),   U_J = span(ybar, (0,1,e,-e*k)),
        U_K = span(u3,   (0,0,1,k)),      U_L = span((1,m,0,0),(0,r,1,-k)),
     with ybar=(1,-1,0,0), u3=(1,1,0,0), parameters (b,e,k,m,r) and the
     projective source torus diag(t0,t1,t2,1), restricts P4 to the pure
     tensor supported on exactly two words:
        T1100 = -2*b*e*k*(m+1),      T1101 = -2*k*(b*e*r + b + e),
     all other 14 coefficients vanish IDENTICALLY.  At the exact sample
     (b,e,k,m,r)=(2,3,5,7,11):
       * the family tangent (5 params + 3 torus) has rank 6;
       * the universal Segre-incidence Jacobian has rank 14, so the
         incidence locus is SMOOTH of dimension 20-14=6 there;
     hence the closure of the saturated family is a six-dimensional
     irreducible component of the pure locus (the same certificate
     pattern as the six-dimensional seventh component).
     Its generic invariants: pair profile (3,3,4,3,4,4) (triangle
     {I,J},{I,K},{J,K}; all L-edges rank 4), shared kernel line
     kernel_I = kernel_J = ybar, two rank-one relations ybar(x)u3 at
     {I,K} and {J,K} with COINCIDENT coordinate-pair supports
     {0,1},{0,1} and coincident factors (the case left open by
     P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md), and a rank-two-
     coefficient relation at {I,J}.  It is distinct from all nine
     certified components: dimension 6 excludes the eight fivefolds,
     and the seventh (rank profile sum 20 with a rank-2 edge on a dense
     open) cannot contain a family whose generic profile sum is 21 by
     rank monotonicity.  => a TENTH component orbit.

 (A) Branch A ({alpha=beta} deep branch) equals the sub-family
        Z(b=alpha, e=x2/(x0+x1), k=1, m=v1/v0, r=0)
     EXACTLY as plane tuples (symbolic identity, mode correspondence
     chart (I,J,K,L) <-> branch modes (0,2,3,1)): branch A lies IN the
     new component, in its smooth-chart interior boundary {r=0}.

 (B) Branch B ({v0+v1=0} deep branch) is the EXACT boundary limit
     b -> oo of Z(b, e, 1, -alpha/beta, 1/beta): the U_I-plane
     span(ybar,(0,1,b,-b)) converges to span(ybar,u1) and all other
     planes match identically (mode correspondence (I,J,K,L) <->
     (1,2,3,0)).  Hence branch B lies in the closure of the new
     component as well.

 Also certified here:
 (a) both branch saturations have family tangent rank 5 (walls of
     dimension 5 inside the six-dimensional component);
 (b) the universal Segre-incidence Jacobian at generic branch samples
     has rank 13 (tangent dimension 7): the branch points are singular
     points of the incidence, which is why the ninth-component-style
     smooth-point argument cannot be applied at the branches themselves;
 (c) structural dichotomy ingredients: ybar in U0 <=> alpha=beta
     (branch A's defining condition), ybar in U1 <=> v0+v1=0
     (branch B's defining condition).
"""
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import itertools
import sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]] * w[ab[1]] + u[ab[1]] * w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[kk][pi[kk]] for kk in range(4)) for pi in PERMS4))


def tensor_of(planes):
    return {bits: perm4(tuple(tuple(planes[md][bits[md]]) for md in range(4)))
            for bits in itertools.product((0, 1), repeat=4)}


def same_plane(P, Q):
    return sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])]).rank() == 2


def Zplanes(b, e, k, m, r):
    return [
        [(1, -1, 0, 0), (0, 1, b, -b * k)],
        [(1, -1, 0, 0), (0, 1, e, -e * k)],
        [(1, 1, 0, 0), (0, 0, 1, k)],
        [(1, m, 0, 0), (0, r, 1, -k)],
    ]


# ---------------- (Z) symbolic purity of the family ----------------
b, e, k, m, r = sp.symbols("b e k m r")
Tsym = tensor_of(Zplanes(b, e, k, m, r))
for bits, val in Tsym.items():
    if bits == (1, 1, 0, 0):
        assert sp.expand(val + 2 * b * e * k * (m + 1)) == 0, val
    elif bits == (1, 1, 0, 1):
        assert sp.expand(val + 2 * k * (b * e * r + b + e)) == 0, val
    else:
        assert sp.expand(val) == 0, (bits, val)
print("Z family: T is supported on {1100, 1101} identically =>")
print("  T = -2k * [ b*e*(m+1) * e_1100 + (b*e*r+b+e) * e_1101 ]  is pure.")

# ---------------- (Z) tangent rank 6 and incidence rank 14 ----------------
t0, t1, t2 = sp.symbols("t0:3")


def torus_rows(rows):
    return sp.Matrix([[t0 * rr[0], t1 * rr[1], t2 * rr[2], rr[3]] for rr in rows])


def family_and_incidence(planes_sym, params, point, pivots):
    chart_coords = []
    reduced = []
    for plane, piv in zip(planes_sym, pivots):
        chart = plane[:, piv].inv() * plane
        nonpiv = tuple(i for i in range(4) if i not in piv)
        reduced.append(chart)
        chart_coords.extend(chart[r_, c_] for r_ in range(2) for c_ in nonpiv)
    jac = sp.Matrix(chart_coords).jacobian(params).subs(point)
    jac = sp.Matrix([[sp.nsimplify(sp.cancel(x)) for x in row] for row in jac.tolist()])
    fam_rank = jac.rank()
    reduced_point = tuple(plane.subs(point) for plane in reduced)
    T_point = {}
    for bits in itertools.product((0, 1), repeat=4):
        T_point[bits] = sp.nsimplify(perm4(tuple(
            tuple(reduced_point[md][bits[md], j] for j in range(4)) for md in range(4))))
    anchor = next(bb for bb in itertools.product((0, 1), repeat=4) if T_point[bb] != 0)
    zvars = sp.symbols("W0:16")
    rvars = sp.symbols("S0:4")
    universal = []
    for mode, piv in enumerate(pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        plane = sp.zeros(2, 4)
        plane[0, piv[0]] = 1
        plane[1, piv[1]] = 1
        entries = zvars[4 * mode: 4 * mode + 4]
        for r_ in range(2):
            for o_, c_ in enumerate(nonpiv):
                plane[r_, c_] = entries[2 * r_ + o_]
        universal.append(plane)
    T_univ = {}
    for bits in itertools.product((0, 1), repeat=4):
        T_univ[bits] = perm4(tuple(tuple(universal[md][bits[md], j] for j in range(4))
                                   for md in range(4)))
    ratios = tuple(T_point[tuple((1 - anchor[mm] if mm == mode else anchor[mm])
                                 for mm in range(4))] / T_point[anchor]
                   for mode in range(4))
    eqs = []
    for word in itertools.product((0, 1), repeat=4):
        if word == anchor:
            continue
        mono = sp.prod(rvars[mm] for mm in range(4) if word[mm] != anchor[mm])
        eqs.append(sp.expand(T_univ[word] - T_univ[anchor] * mono))
    coord_pt = []
    for plane, piv in zip(reduced_point, pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        coord_pt.extend(sp.nsimplify(plane[r_, c_]) for r_ in range(2) for c_ in nonpiv)
    subst = dict(zip(tuple(zvars) + tuple(rvars), tuple(coord_pt) + ratios))
    assert all(sp.simplify(eq.subs(subst)) == 0 for eq in eqs)
    inc_rank = sp.Matrix(eqs).jacobian(tuple(zvars) + tuple(rvars)).subs(subst).rank()
    return fam_rank, inc_rank


bs, es, ks, ms, rs = sp.symbols("bs es ks ms rs")
Zsym = [torus_rows(rows) for rows in Zplanes(bs, es, ks, ms, rs)]
Zpoint = {bs: 2, es: 3, ks: 5, ms: 7, rs: 11, t0: 1, t1: 1, t2: 1}
Zpivots = ((0, 1), (0, 1), (0, 2), (0, 2))
famZ, incZ = family_and_incidence(Zsym, (bs, es, ks, ms, rs, t0, t1, t2), Zpoint, Zpivots)
print(f"Z at (2,3,5,7,11): family tangent rank = {famZ}, incidence Jacobian rank = {incZ}")
assert famZ == 6 and incZ == 14
print("  => smooth incidence point of dimension 6 = family dimension:")
print("     the closure of the Z family is a SIX-DIMENSIONAL IRREDUCIBLE")
print("     COMPONENT of the pure locus, distinct from all nine certified")
print("     components (dimension excludes the eight fivefolds; rank-sum")
print("     21 > 20 with no rank-2 edge excludes the seventh).")

# generic profile of Z (two samples)
for smp in ((2, 3, 5, 7, 11), (-3, 4, sp.Rational(1, 2), -6, sp.Rational(2, 7))):
    T = tensor_of(Zplanes(*smp))
    prof = []
    for a_, b_ in COORD_PAIRS:
        rows_ = []
        for pa in Zplanes(*smp)[a_]:
            for pb in Zplanes(*smp)[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        prof.append(sp.Matrix(rows_).rank())
    assert tuple(prof) == (3, 3, 4, 3, 4, 4), prof
print("Z generic profile (3,3,4,3,4,4): triangle {I,J},{I,K},{J,K}; L-edges rank 4")

# ---------------- (A) branch A is an exact sub-family of Z ----------------
v0, v1, v2, x0, x1, x2, al, be = sp.symbols("v0 v1 v2 x0 x1 x2 al be")
brA = [
    [(1, 0, al, -al), (0, 1, al, -al)],
    [(0, 0, 1, -1), (v0, v1, v2, -v2)],
    [(1, -1, 0, 0), (x0, x1, x2, -x2)],
    [(0, 0, 1, 1), (1, 1, 0, 0)],
]
Zp = Zplanes(al, x2 / (x0 + x1), 1, v1 / v0, 0)
reorder = [Zp[0], Zp[3], Zp[1], Zp[2]]  # chart (I,J,K,L) <-> branch modes (0,2,3,1)
assert all(same_plane(brA[i], reorder[i]) for i in range(4))
print("branch A == Z(alpha, x2/(x0+x1), 1, v1/v0, 0) EXACTLY (symbolic identity):")
print("  branch A lies inside the new six-dimensional component.")

# ---------------- (B) branch B is an exact boundary limit of Z -------------
eB, w0, w2, y0, y1 = sp.symbols("eB w0 w2 y0 y1")
brB = [
    [(1, 0, al, -al), (0, 1, be, -be)],
    [(0, 0, 1, -1), (w0, -w0, w2, -w2)],
    [(1, -1, 0, 0), (y0, y1, (y0 + y1) * eB, -(y0 + y1) * eB)],
    [(0, 0, 1, 1), (1, 1, 0, 0)],
]
ZB = Zplanes(sp.Symbol("bb"), eB, 1, -al / be, 1 / be)
UI_lim = [(1, -1, 0, 0), (0, 0, 1, -1)]  # lim_{b->oo} span(ybar,(0,1,b,-b))
reorderB = [ZB[3], UI_lim, ZB[1], ZB[2]]  # chart (I,J,K,L) <-> branch modes (1,2,3,0)
assert all(same_plane(brB[i], reorderB[i]) for i in range(4))
# the U_I limit really is the limit of Z's U_I plane: for finite b the plane
# span(ybar,(0,1,b,-b)) = span(ybar,(0,1/b,1,-1)) -> span(ybar,(0,0,1,-1)):
bb = sp.Symbol("bb")
gen_scaled = (0, 1 / bb, 1, -1)
assert same_plane([(1, -1, 0, 0), (0, 1, bb, -bb)], [(1, -1, 0, 0), gen_scaled])
assert tuple(sp.limit(gc, bb, sp.oo) for gc in gen_scaled) == (0, 0, 1, -1)
print("branch B == lim_{b->oo} Z(b, e, 1, -alpha/beta, 1/beta) EXACTLY:")
print("  branch B lies in the closure of the new six-dimensional component.")

# ---------------- (a)+(b) branch-level ranks -------------------------------
pivots = ((0, 1), (0, 2), (0, 2), (0, 2))
brA_sym = [
    torus_rows([(1, 0, al, -al), (0, 1, al, -al)]),
    torus_rows([(0, 0, 1, -1), (v0, v1, v2, -v2)]),
    torus_rows([(1, -1, 0, 0), (x0, x1, x2, -x2)]),
    torus_rows([(0, 0, 1, 1), (1, 1, 0, 0)]),
]
famA, incA = family_and_incidence(
    brA_sym, (v0, v1, v2, x0, x1, x2, al, t0, t1, t2),
    {v0: 3, v1: 5, v2: 7, x0: 2, x1: -9, x2: 4, al: sp.Rational(2, 3),
     t0: 1, t1: 1, t2: 1}, pivots)
brB_sym = [
    torus_rows([(1, 0, al, -al), (0, 1, be, -be)]),
    torus_rows([(0, 0, 1, -1), (v0, -v0, v2, -v2)]),
    torus_rows([(1, -1, 0, 0), (x0, x1, x2, -x2)]),
    torus_rows([(0, 0, 1, 1), (1, 1, 0, 0)]),
]
famB, incB = family_and_incidence(
    brB_sym, (v0, v2, x0, x1, x2, al, be, t0, t1, t2),
    {v0: 2, v2: 5, x0: 3, x1: 7, x2: 4, al: sp.Rational(1, 2),
     be: sp.Rational(-3, 5), t0: 1, t1: 1, t2: 1}, pivots)
print(f"branch A: family tangent rank {famA}, incidence Jacobian rank {incA}")
print(f"branch B: family tangent rank {famB}, incidence Jacobian rank {incB}")
assert (famA, incA) == (5, 13) and (famB, incB) == (5, 13)
print("  the branches are 5-dimensional walls; their points are singular on the")
print("  incidence (tangent dimension 7), so no smooth-point identification was")
print("  possible at the branches themselves -- the Z family resolves them.")

# ---------------- (c) dichotomy ingredients --------------------------------
alpha, beta = sp.symbols("alpha beta")
k3 = (0, 0, 1, -1)
u0a = (1, 0, alpha, -alpha)
u0b = (0, 1, beta, -beta)
ybar = (1, -1, 0, 0)
stack = sp.Matrix([list(u0a), list(u0b), list(ybar)])
mins = [sp.factor(stack[:, cols].det()) for cols in itertools.combinations(range(4), 3)]
assert all(mm in (0,) or sp.simplify(mm / (alpha - beta)) in (1, -1) for mm in mins)
vv = sp.symbols("vv0:4")
stackB = sp.Matrix([[0, 0, 1, -1], list(vv), list(ybar)])
minsB = [sp.expand(stackB[:, cols].det()) for cols in itertools.combinations(range(4), 3)]
assert all(sp.expand(mm.subs({vv[1]: -vv[0], vv[3]: -vv[2]})) == 0 for mm in minsB)
assert any(sp.expand(mm.subs({vv[3]: -vv[2]})) != 0 for mm in minsB)
print("dichotomy: ybar in U0 <=> alpha=beta (branch A);  ybar in U1 <=> v0+v1=0")
print("  (branch B) -- both branches are exactly the 'ybar-incidence' walls of")
print("  the deep stratum, matching their embedding into the Z family.")
print("ALL CHECKS PASSED")
