#!/usr/bin/env python3
"""A TWELFTH pure-compression component: certificate.

The family F12 (the Zb1 branch of the coincident-support chart; sweep
modes (0,1,2,3) = (U0, ybar-p, ybar-q, u3-w)):

    U0 = span( u3, (0,0,1,-k) ),          u3 = (1,1,0,0),
    U1 = span( ybar, (0,1,p2,p3) ),       ybar = (1,-1,0,0),
    U2 = span( ybar, (0,1,q2,q3) ),
    U3 = span( u3, (0,0,1,k) ),
    with the single tie   k(p2+q2) + (p3+q3) = 0,

free parameters (p2, p3, q2, k) [q3 eliminated], plus the projective
source torus diag(t0,t1,t2,1).

Certificate (all exact, characteristic zero, fail-closed):
 (1) identical purity: the full 16-entry restriction satisfies every
     flattening 2x2 minor identically in (p2,p3,q2,k); the nonzero
     entries are T0110 and T1110 (a two-word tensor);
 (2) generic nonzeroness and the generic pair profile over the function
     field Q(p2,p3,q2,k): profile (3,3,3,4,3,3), and at the five rank-3
     edges ALL 4x4 minors of the 4x6 pair-product matrices vanish
     identically, so every point of closure(F12) has profile at most
     (3,3,3,4,3,3) entrywise (rank sum <= 19);
 (3) family tangent rank 5 at the exact sample (p2,p3,q2,k)=(3,-1,5,2)
     including the full projective torus: dim closure(F12) >= 5;
 (4) the universal Segre-incidence Jacobian at the sample has rank 14
     (tangent dimension 6) and the transverse tangent direction is
     SECOND-ORDER OBSTRUCTED (rank [J|c2] = 15): the sample is a
     singular point of the incidence, so the smooth-point argument does
     not apply and the local dimension is certified by a slice instead;
 (5) char-0 five-hyperplane slice of the eleven ratio-eliminated purity
     equations at the sample has ds-local dimension ZERO, hence
     (Krull) the pure locus has local dimension <= 5 at the sample;
     with (3): local dimension EXACTLY 5, and closure(F12) is an
     irreducible COMPONENT of the pure locus (any irreducible closed
     subset of the pure locus containing it has local dimension <= 5 at
     the sample, hence dimension 5, hence equals closure(F12));
 (6) distinctness from all ELEVEN certified component orbits:
     - the three sixfolds (seventh, tenth, eleventh) cannot pass
       through the sample: an irreducible 6-dim variety has local
       dimension 6 > 5 at each of its points, contradicting (5);
     - the eight fivefolds X (first, dq, L1, L2, L3, sixth, eighth,
       ninth): closure(F12) = g(closure(X)) would put g(sample of X),
       whose pair-rank sum is 21 (verified), inside closure(F12), whose
       points all have pair-rank sum <= 19 by (2): contradiction;
 (7) the mirror branch Zb2 (k(p2+q2)-(p3+q3) = 0) is the image of F12
     under the census symmetry (mode swap 0<->3): one orbit.

Hence closure(F12) is a five-dimensional irreducible component of the
pure-compression locus lying in no previously certified component
orbit: a TWELFTH component orbit."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


p2, p3, q2, k = sp.symbols("p2 p3 q2 k")
q3e = -k*(p2 + q2) - p3
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)


def F12(p2_, p3_, q2_, k_):
    q3_ = -k_*(p2_ + q2_) - p3_
    return [
        [U3v, (0, 0, 1, -k_)],
        [YBAR, (0, 1, p2_, p3_)],
        [YBAR, (0, 1, q2_, q3_)],
        [U3v, (0, 0, 1, k_)],
    ]


planes = F12(p2, p3, q2, k)

# ---- (1) identical purity ---------------------------------------------------
T = {bits: perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
     for bits in itertools.product((0, 1), repeat=4)}
nz = {bits: sp.factor(val) for bits, val in T.items() if sp.expand(val) != 0}
assert set(nz) == {(0, 1, 1, 0), (1, 1, 1, 0)}, nz
assert sp.expand(nz[(0, 1, 1, 0)] - 2*(p2*q3e + p3*q2)) == 0
assert sp.expand(nz[(1, 1, 1, 0)] + 2*k*(p2 + q2)) == 0
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    mat = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        mat[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            assert sp.expand(mat[r1, c1]*mat[r2, c2] - mat[r1, c2]*mat[r2, c1]) == 0
print("(1) F12 is pure for ALL parameter values; support {0110, 1110}.  OK")

# ---- (2) generic profile bound over the function field ---------------------
RANK3_EDGES = ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3))
profile = {}
for a_, b_ in COORD_PAIRS:
    rows_ = []
    for pa in planes[a_]:
        for pb in planes[b_]:
            prod = rmul(pa, pb)
            rows_.append([prod[ab] for ab in COORD_PAIRS])
    mm = sp.Matrix(rows_)
    if (a_, b_) in RANK3_EDGES:
        for rr in itertools.combinations(range(4), 4):
            for cc in itertools.combinations(range(6), 4):
                assert sp.expand(mm[rr, cc].det()) == 0, ((a_, b_), rr, cc)
    profile[(a_, b_)] = mm.rank()   # rank over Q(p2,p3,q2,k)
assert tuple(profile[e_] for e_ in COORD_PAIRS) == (3, 3, 3, 4, 3, 3)
print("(2) generic profile (3,3,3,4,3,3); at the five rank-3 edges all 4x4")
print("    pair-minors vanish identically: profile <= (3,3,3,4,3,3)")
print("    entrywise (sum <= 19) on ALL of closure(F12).  OK")

# ---- (3)+(4) tangent, incidence, obstruction at the sample -----------------
t0, t1, t2 = sp.symbols("t0:3")
sample = {p2: 3, p3: -1, q2: 5, k: 2}
torus = sp.diag(t0, t1, t2, 1)
planes_sym = [sp.Matrix([list(r_) for r_ in pl])*torus for pl in planes]
pivots = ((0, 2), (0, 1), (0, 1), (0, 2))
params = (p2, p3, q2, k, t0, t1, t2)
point = {**sample, t0: 1, t1: 1, t2: 1}
chart_coords = []
reduced = []
for plane, piv in zip(planes_sym, pivots):
    chart = plane[:, piv].inv()*plane
    reduced.append(chart)
    nonpiv = tuple(i for i in range(4) if i not in piv)
    chart_coords.extend(chart[r_, c_] for r_ in range(2) for c_ in nonpiv)
jac = sp.Matrix(chart_coords).jacobian(params).subs(point)
jac = sp.Matrix([[sp.nsimplify(sp.cancel(c)) for c in row] for row in jac.tolist()])
assert jac.rank() == 5
print("(3) family tangent rank (4 params + full projective torus) = 5.  OK")

reduced_point = tuple(pl.subs(point) for pl in reduced)
T_point = {}
for bits in itertools.product((0, 1), repeat=4):
    T_point[bits] = sp.nsimplify(perm4(tuple(tuple(reduced_point[m][bits[m], j]
                                                   for j in range(4)) for m in range(4))))
anchor = next(bb for bb in itertools.product((0, 1), repeat=4) if T_point[bb] != 0)
zvars = sp.symbols("ZI0:16")
rvars = sp.symbols("RI0:4")
universal = []
for mode, piv in enumerate(pivots):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    plane = sp.zeros(2, 4)
    plane[0, piv[0]] = 1
    plane[1, piv[1]] = 1
    entries = zvars[4*mode: 4*mode+4]
    for r_ in range(2):
        for o_, c_ in enumerate(nonpiv):
            plane[r_, c_] = entries[2*r_ + o_]
    universal.append(plane)
T_univ = {}
for bits in itertools.product((0, 1), repeat=4):
    T_univ[bits] = perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4))
                               for m in range(4)))
ratios = tuple(T_point[tuple((1-anchor[mm] if mm == mode else anchor[mm])
                             for mm in range(4))]/T_point[anchor] for mode in range(4))
eqs = []
for word in itertools.product((0, 1), repeat=4):
    if word == anchor:
        continue
    mono = sp.prod(rvars[mm] for mm in range(4) if word[mm] != anchor[mm])
    eqs.append(sp.expand(T_univ[word] - T_univ[anchor]*mono))
coord_pt = []
for plane, piv in zip(reduced_point, pivots):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    coord_pt.extend(sp.nsimplify(plane[r_, c_]) for r_ in range(2) for c_ in nonpiv)
allvars = tuple(zvars) + tuple(rvars)
subst = dict(zip(allvars, tuple(coord_pt) + ratios))
assert all(sp.simplify(eq.subs(subst)) == 0 for eq in eqs)
J = sp.Matrix(eqs).jacobian(allvars).subs(subst)
assert J.rank() == 14
NS = J.nullspace()
assert len(NS) == 6
# family tangent inside the 20-var space (chart coords + ratios):
Tsym = {}
for bits in itertools.product((0, 1), repeat=4):
    Tsym[bits] = perm4(tuple(tuple(reduced[m][bits[m], j] for j in range(4))
                             for m in range(4)))
ratio_sym = [sp.cancel(Tsym[tuple((1-anchor[mm] if mm == mode else anchor[mm])
                                  for mm in range(4))]/Tsym[anchor]) for mode in range(4)]
full_sym = list(chart_coords) + ratio_sym
famJ = sp.Matrix(full_sym).jacobian(params).subs(point)
famJ = sp.Matrix([[sp.nsimplify(sp.cancel(c)) for c in row] for row in famJ.tolist()])
assert famJ.rank() == 5
trans = None
for vec in NS:
    if sp.Matrix.hstack(famJ, vec).rank() > 5:
        trans = vec
        break
assert trans is not None
eps = sp.Symbol("eps")
shift = {var: subst[var] + eps*trans[i] for i, var in enumerate(allvars)}
c2vec = []
for eq in eqs:
    poly = sp.Poly(sp.expand(eq.subs(shift)), eps)
    assert poly.coeff_monomial(1) == 0 and poly.coeff_monomial(eps) == 0
    c2vec.append(sp.nsimplify(poly.coeff_monomial(eps**2)))
assert sp.Matrix.hstack(J, sp.Matrix(c2vec)).rank() == 15
print("(4) incidence Jacobian rank 14 (tangent 6); the transverse tangent")
print("    is SECOND-ORDER OBSTRUCTED (rank [J|c2] = 15).  OK")

# ---- (5) char-0 five-slice ds local dimension ------------------------------
elim = []
for word in itertools.product((0, 1), repeat=4):
    flips = [mm for mm in range(4) if word[mm] != anchor[mm]]
    if len(flips) < 2:
        continue
    lhs = sp.expand(T_univ[word]*T_univ[anchor]**(len(flips)-1))
    rhs = sp.prod(T_univ[tuple((1-anchor[mm] if mm == mmm else anchor[mm])
                               for mm in range(4))] for mmm in flips)
    elim.append(sp.expand(lhs - sp.expand(rhs)))
assert len(elim) == 11
subs0 = dict(zip(zvars, coord_pt))
assert all(sp.simplify(eq.subs(subs0)) == 0 for eq in elim)
shifted = []
for eq in elim:
    poly = sp.expand(eq.subs({zv: zv + val for zv, val in subs0.items()}))
    den = 1
    for coeff in sp.Poly(poly, *zvars).coeffs():
        den = sp.lcm(den, sp.denom(sp.nsimplify(coeff)))
    shifted.append(sp.expand(poly*den))
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
)
slices = [sum(cc*zz for cc, zz in zip(row, zvars)) for row in SLICE_COEFFS]
varnames = ",".join(str(vv) for vv in zvars)
polys = ";\n".join(f"poly g{i}={str(pp).replace('**','^')}"
                   for i, pp in enumerate(shifted + slices))
program = "\n".join((
    f"ring R=0,({varnames}),ds;",
    polys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(shifted) + len(slices))) + ";",
    "option(redSB);",
    "ideal J=std(I);",
    '"SLICE_LOCAL_DIM:"+string(dim(J));',
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=3000, check=False)
out = completed.stdout
assert "SLICE_LOCAL_DIM:" in out, out[-500:]
dim_val = int(out.split("SLICE_LOCAL_DIM:")[1].split()[0])
assert dim_val == 0, dim_val
print("(5) five-slice ds local dimension 0 (char 0): the pure locus has")
print("    local dimension <= 5 at the sample; with (3), EXACTLY 5, and")
print("    closure(F12) is an irreducible component of the pure locus.  OK")

# ---- (6) fivefold sample rank sums = 21 ------------------------------------
fivefolds = {}
fivefolds["first"] = [[(1, 0, -1, -2), (0, 1, 1, 0)], [(1, 1, 0, 0), (0, 0, 1, 1)],
                      [(0, 1, 0, 1), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
fivefolds["dq"] = [[(2, -1, -1, -2), (1, -1, 1, 1)], [(1, 0, 0, -1), (1, 1, -1, 1)],
                   [(3, 1, 1, -1), (0, 1, -1, 0)], [(1, 0, 0, 1), (0, 1, 1, 0)]]
fivefolds["L1"] = [[(2, 4, 0, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                   [(1, 0, 4, 2), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
fivefolds["L2"] = [[(2, 0, 4, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                   [(1, 0, 4, 6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
fivefolds["L3"] = [[(2, 10, -8, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 2)],
                   [(1, 0, 3, -6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
dd, pp, qq = 2, 3, 5
n6 = qq*(dd + pp + qq)
fivefolds["sixth"] = [[(-dd*pp, dd + qq, n6, 0), (dd*pp, -dd - qq, 0, n6)],
                      [(0, 0, 1, 1), (-dd, 1, -pp - qq, dd)],
                      [(pp, 1, 0, qq), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
a8, b8, f8, ph8 = sp.Integer(-12), sp.Integer(-10), sp.Rational(3, 4), sp.Rational(-5, 28)
j8 = f8 + b8*ph8**2
kap8 = ph8*(b8*f8 + 1)
eta8 = -(b8*f8 + 1)
fivefolds["eighth"] = [[(0, 0, 1, -1), (a8 + b8, a8 - b8, 0, 2)],
                       [(-a8*f8 + 1, -a8*f8 - 1, f8 + ph8, f8 - ph8), (1, 1, 0, 0)],
                       [(-a8*j8 + eta8, -a8*j8 - eta8, j8 + kap8, j8 - kap8), (1, 1, 0, 0)],
                       [(1, -1, 0, 0), (0, 0, 1, 1)]]
d9, v90, v91, v92, x91, x92 = 2, 3, 5, 7, 11, -4
x90 = sp.Rational(-(d9*v90*x91 + v91*x92), d9*v91)
c9 = (-d9*v91, -d9*v90, v91, v91)
k19, k29, k39 = (-c9[1], c9[0], 0, 0), (-c9[2], 0, c9[0], 0), (-c9[3], 0, 0, c9[0])
al9, be9 = sp.Rational(2, 3), sp.Rational(-1, 2)
fivefolds["ninth"] = [[tuple(k19[j] + al9*k39[j] for j in range(4)),
                       tuple(k29[j] + be9*k39[j] for j in range(4))],
                      [(0, 0, 1, -1), (v90, v91, v92, -v92)],
                      [(1, 0, -d9, 0), (x90, x91, x92, 0)],
                      [(0, 0, 1, 1), (1, 0, d9, 0)]]
for name, pls in fivefolds.items():
    tot = 0
    for a_, b_ in COORD_PAIRS:
        rows_ = []
        for pa in pls[a_]:
            for pb in pls[b_]:
                prod = rmul(tuple(pa), tuple(pb))
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        tot += sp.Matrix(rows_).rank()
    assert tot == 21, (name, tot)
print("(6) all eight certified fivefold samples have pair-rank sum 21 > 19:")
print("    none of their orbits can equal closure(F12); the three sixfolds")
print("    are excluded by local dimension at the sample.  OK")

# ---- (7) Zb2 = (03)-mode swap of F12 ---------------------------------------
def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.expand(stack[rows, cols].det()) != 0:
                return False
    return True


kM = sp.Symbol("kM")
zb2 = [
    [U3v, (0, 0, 1, -kM)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, kM*(p2 + q2) - p3)],
    [U3v, (0, 0, 1, kM)],
]
f12_at = F12(p2, p3, q2, -kM)
swapped = [f12_at[3], f12_at[1], f12_at[2], f12_at[0]]
assert all(same_plane(zb2[mm], swapped[mm]) for mm in range(4))
print("(7) Zb2 == (03)-mode swap of F12 at k -> -k: one census orbit.  OK")
print()
print("CONCLUSION: closure(F12) is a five-dimensional irreducible component")
print("of the pure-compression locus, distinct from all ELEVEN certified")
print("component orbits: a TWELFTH component orbit.  The certificate is the")
print("char-0 slice standard-basis pattern (singular point, tangent 6,")
print("obstructed normal), the same pattern as the eleventh.")
print("ALL CHECKS PASSED")
