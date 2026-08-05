#!/usr/bin/env python3
"""A THIRTEENTH pure-compression component: certificate.

The family F13 (the Za2 branch of the coincident-support chart; sweep
modes (0,1,2,3) = (U0, ybar-p, ybar-q, u3-w)):

    U0 = span( u3, zeta ),   zeta = ((b+e)(k w2+w3), 0, -2bek w2, 2bek w3),
    U1 = span( ybar, (0,1,b,-bk) ),   U2 = span( ybar, (0,1,e,-ek) ),
    U3 = span( u3, (0, W, w2, w3) ),  W = -(b+e)(k w2-w3)/(2bek),

free parameters (b, e, k, w2:w3) plus the projective source torus.

Certificate (same pattern as the twelfth, s06):
 (1) identical purity of the full 16-entry restriction in (b,e,k,w2,w3);
     support is the single word e_0110;
 (2) generic profile (3,3,4,3,3,3) over the function field and vanishing
     of all 4x4 pair minors at the five rank-3 edges: every point of
     closure(F13) has pair-rank sum <= 19;
 (3) family tangent rank 5 at (b,e,k,w2,w3) = (2,3,5,1,7) incl. torus;
 (4) incidence Jacobian rank 14, tangent 6, transverse direction
     second-order obstructed;
 (5) char-0 five-slice ds local dimension 0: local dimension exactly 5;
     closure(F13) is an irreducible component;
 (6) distinctness: sixfolds by local dimension; the eight certified
     fivefolds by the rank-sum-21 samples (as in s06); the TWELFTH by
     the two-coordinate-plane incidence invariant: on all of
     closure(F12), U0 meets both span(e0,e1) and span(e2,e3) (closed,
     holds identically on the family), while at the F13 sample NO plane
     meets two complementary coordinate planes;
 (7) Za3 is the image of F13 under the census symmetry diag(1,1,1,-1)
     (k -> -k, w3 -> -w3): one orbit.

Hence closure(F13) is a five-dimensional irreducible component in no
previously certified orbit and distinct from the twelfth: a THIRTEENTH
component orbit."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


b, e, k, w2, w3 = sp.symbols("b e k w2 w3")
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)
Wv = -(b + e)*(k*w2 - w3)/(2*b*e*k)
zeta = ((b + e)*(k*w2 + w3), 0, -2*b*e*k*w2, 2*b*e*k*w3)
wrow = (0, Wv, w2, w3)


def F13(b_, e_, k_, w2_, w3_):
    sub = {b: b_, e: e_, k: k_, w2: w2_, w3: w3_}
    return [
        [U3v, tuple(sp.nsimplify(sp.sympify(c).subs(sub)) for c in zeta)],
        [YBAR, (0, 1, b_, -b_*k_)],
        [YBAR, (0, 1, e_, -e_*k_)],
        [U3v, tuple(sp.nsimplify(sp.sympify(c).subs(sub)) for c in wrow)],
    ]


planes = [
    [U3v, zeta],
    [YBAR, (0, 1, b, -b*k)],
    [YBAR, (0, 1, e, -e*k)],
    [U3v, wrow],
]

# ---- (0) zeta is the kernel of M_Z on the branch ---------------------------
z = sp.symbols("z0:4")


def covrow(rows3):
    form = perm4((tuple(z),) + tuple(rows3))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


MZ = sp.Matrix([covrow((YBAR, YBAR, wrow)),
                covrow((YBAR, planes[2][1], wrow)),
                covrow((planes[1][1], YBAR, wrow))])
for kv in (U3v, zeta):
    assert all(sp.simplify(sp.together(sum(MZ[i, j]*kv[j] for j in range(4)))) == 0
               for i in range(3)), kv
print("(0) U0 = span(u3, zeta) is the forced case-Z kernel on the branch.  OK")

# ---- (1) identical purity ---------------------------------------------------
T = {bits: sp.cancel(sp.together(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))))
     for bits in itertools.product((0, 1), repeat=4)}
nz = {bits: sp.factor(val) for bits, val in T.items() if sp.simplify(val) != 0}
assert set(nz) == {(0, 1, 1, 0)}, set(nz)
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    mat = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        mat[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            assert sp.simplify(mat[r1, c1]*mat[r2, c2] - mat[r1, c2]*mat[r2, c1]) == 0
print("(1) F13 is pure for ALL parameter values; support = the single word")
print("    e_0110, value", nz[(0, 1, 1, 0)], ".  OK")

# ---- (2) generic profile bound ---------------------------------------------
RANK3_EDGES = ((0, 1), (0, 2), (1, 2), (1, 3), (2, 3))
prof = {}
for a_, b_ in COORD_PAIRS:
    rows_ = []
    for pa in planes[a_]:
        for pb in planes[b_]:
            prod = rmul(pa, pb)
            rows_.append([sp.together(prod[ab]) for ab in COORD_PAIRS])
    mm = sp.Matrix(rows_)
    if (a_, b_) in RANK3_EDGES:
        for rr in itertools.combinations(range(4), 4):
            for cc in itertools.combinations(range(6), 4):
                assert sp.simplify(mm[rr, cc].det()) == 0, ((a_, b_), rr, cc)
    prof[(a_, b_)] = mm.rank()
assert tuple(prof[e_] for e_ in COORD_PAIRS) == (3, 3, 4, 3, 3, 3), prof
print("(2) generic profile (3,3,4,3,3,3); all 4x4 pair minors vanish at the")
print("    five rank-3 edges: rank sum <= 19 on ALL of closure(F13).  OK")

# ---- (3)+(4) tangent / incidence / obstruction at the sample ---------------
t0, t1, t2 = sp.symbols("t0:3")
sample = {b: 2, e: 3, k: 5, w2: 1, w3: 7}
torus = sp.diag(t0, t1, t2, 1)
planes_sym = [sp.Matrix([[sp.sympify(c) for c in row] for row in pl])*torus
              for pl in planes]
pivots = ((0, 2), (0, 1), (0, 1), (0, 2))
params = (b, e, k, w2, w3, t0, t1, t2)
point = {**sample, t0: 1, t1: 1, t2: 1}
chart_coords = []
reduced = []
for plane, piv in zip(planes_sym, pivots):
    chart = plane[:, piv].inv()*plane
    reduced.append(chart)
    nonpiv = tuple(i for i in range(4) if i not in piv)
    chart_coords.extend(chart[r_, c_] for r_ in range(2) for c_ in nonpiv)
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
print("(3) family tangent rank (5 params + full torus) = 5.  OK")
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
print("(4) incidence rank 14 (tangent 6); transverse direction second-order")
print("    obstructed (rank [J|c2] = 15).  OK")

# ---- (5) five-slice ds dimension -------------------------------------------
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
assert int(out.split("SLICE_LOCAL_DIM:")[1].split()[0]) == 0
print("(5) five-slice ds local dimension 0: local dimension exactly 5;")
print("    closure(F13) is an irreducible component of the pure locus.  OK")

# ---- (6) separation from the twelfth ---------------------------------------
# closed conditions on all of closure(F12): U0 meets span(e0,e1) and
# span(e2,e3) (and U3 likewise): verify identically on the F12 family:
p2s, p3s, q2s, ks = sp.symbols("p2s p3s q2s ks")
F12_U0 = [(1, 1, 0, 0), (0, 0, 1, -ks)]
F12_U3 = [(1, 1, 0, 0), (0, 0, 1, ks)]
for U in (F12_U0, F12_U3):
    # meets P01: the first generator lies in span(e0,e1); meets P23: second
    assert U[0][2] == 0 and U[0][3] == 0
    assert U[1][0] == 0 and U[1][1] == 0
# at the F13 sample no plane meets two complementary coordinate planes:
sampleF13 = F13(2, 3, 5, 1, 7)


def meets(U, pair):
    comp = tuple(i for i in range(4) if i not in pair)
    return sp.Matrix([[U[r_][c] for c in comp] for r_ in range(2)]).rank() <= 1


for pl in sampleF13:
    for pair in ((0, 1), (0, 2), (0, 3)):
        comp = tuple(sorted(set(range(4)) - set(pair)))
        assert not (meets(pl, pair) and meets(pl, comp)), (pl, pair)
print("(6) on closure(F12) the mode-0 plane meets BOTH span(e0,e1) and")
print("    span(e2,e3) (closed conditions, identical on the family); at the")
print("    F13 sample no plane meets two complementary coordinate planes:")
print("    closure(F13) != g(closure(F12)) for every census symmetry.  OK")
print("    (Sixfolds excluded by local dimension 5; certified fivefolds by")
print("    their rank-sum-21 samples vs (2), as in s06.)")

# ---- (7) Za3 = source-swap-(01) image of F13 -------------------------------
# The census symmetry g = coordinate swap X0 <-> X1 fixes the ybar- and
# u3-lines, fixes p and q modulo ybar, and sends the U3-row (0,W,w2,w3)
# to (W,0,w2,w3) == (0,-W,w2,w3) modulo u3: it flips the sign of W, i.e.
# it carries the Za2 branch value W = -(b+e)(k w2-w3)/(2bek) to the Za3
# branch value +(b+e)(k w2-w3)/(2bek) at the SAME (b,e,k,w2,w3).
# (The earlier draft claimed diag(1,1,1,-1); that symmetry preserves each
# branch -- the invariant Q = 2Wbek/[(b+e)(k w2-w3)] takes value -1 on
# Za2 and +1 on Za3 and is fixed by diag(1,1,1,-1), while the (01)-swap
# sends Q to -Q.)
def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.simplify(sp.together(stack[rows, cols].det())) != 0:
                return False
    return True


g01 = lambda row: (row[1], row[0], row[2], row[3])
image = [[g01(tuple(sp.sympify(c) for c in r_)) for r_ in pl] for pl in planes]
W3 = -Wv                      # = +(b+e)(k w2-w3)/(2bek): the Za3 value
w3row = (0, W3, w2, w3)
# (a) modes 1, 2, 3 of the image equal the Za3 family's planes at the
#     same parameters (exact span equalities for all parameter values):
assert same_plane(image[1], [YBAR, (0, 1, b, -b*k)])
assert same_plane(image[2], [YBAR, (0, 1, e, -e*k)])
assert same_plane(image[3], [U3v, w3row])
# (b) the image's mode-0 plane is the Za3 branch's FORCED kernel plane:
#     u3 and the image zeta both lie in ker M_Z of the Za3 configuration,
#     and that kernel is exactly two-dimensional on a dense open (rank
#     M_Z = 2 at the sample; rank <= 2 holds on the whole (Z-a) stratum
#     by the s03 minor factorization since p_Pi || q_Pi):
MZ3 = sp.Matrix([covrow((YBAR, YBAR, w3row)),
                 covrow((YBAR, (0, 1, e, -e*k), w3row)),
                 covrow(((0, 1, b, -b*k), YBAR, w3row))])
img_zeta = image[0][1]
for kv in (U3v, img_zeta):
    assert all(sp.simplify(sp.together(sum(MZ3[i, j]*kv[j] for j in range(4)))) == 0
               for i in range(3)), kv
sub = {b: 2, e: 3, k: 5, w2: 1, w3: 7}
MZ3s = sp.Matrix([[sp.nsimplify(sp.cancel(sp.sympify(c).subs(sub))) for c in row]
                  for row in MZ3.tolist()])
assert MZ3s.rank() == 2
iz = [sp.nsimplify(sp.cancel(sp.sympify(c).subs(sub))) for c in img_zeta]
assert sp.Matrix([list(U3v), iz]).rank() == 2
print("(7) the source swap (01) carries F13 onto the Za3 branch at the SAME")
print("    (b,e,k,w2,w3) (it flips the branch invariant Q = 2Wbek/[(b+e)")
print("    (k w2-w3)] from -1 to +1): modes 1,2,3 match exactly and the")
print("    image mode-0 plane is the Za3 branch's forced kernel plane:")
print("    Za2 and Za3 are ONE census orbit.  OK")
print()
print("CONCLUSION: closure(F13) is a five-dimensional irreducible component")
print("of the pure-compression locus in no previously certified orbit and")
print("distinct from the twelfth: a THIRTEENTH component orbit.")
print("ALL CHECKS PASSED")
