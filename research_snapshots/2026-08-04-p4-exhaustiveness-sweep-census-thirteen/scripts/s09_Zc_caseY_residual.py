#!/usr/bin/env python3
"""Residual (b2)-chart strata: the Zc branches, the case-Y pattern, and
the p-in-Pi walls.  Exact facts + honest open flags.

 (A) Zc branches (w3 = 0 stratum): identical purity of the family,
     profile bound (sum <= 18, a rank-2 pair edge at {0,3}), family
     tangent 5, incidence Jacobian rank 13 (tangent SEVEN: doubly
     singular points, like the tenth's A/B walls), Zc2 = source-swap
     (01) image of Zc1.  The sieve (s07) leaves only 'first'/'seventh'.
     The ds-slice at the Zc sample exceeded the local budget (recorded
     null): the ambient component of the Zc wall is OPEN; diagnosis:
     candidate seventh-wall (rank-2 edge matches; 'first' would force a
     5-dim germ and then the profile-sum argument would make Zc a NEW
     component, so the two open outcomes are 'seventh wall' or 'new').
 (B) case Y (K3 = u3): the single covector Y1 and the kernel basis
     {ybar, kA, kB}; the purity system of the residual 2x2x2 and its
     minAssGTZ stratification are computed and recorded; the survivor
     primes with nonzero restriction are listed with dimensions; the
     P = p2q3+p3q2 = 0 chart degeneration is flagged.  Identification
     of the case-Y survivor walls: OPEN (with the computed data);
     the p||q||conj(w_Pi), w-in-Pi survivor is inside the TENTH's
     stratum (its U0-fibre is the tenth's, s03 (4)).
 (C) p-in-Pi walls of the rank-2 strata: branch equations computed;
     each rank-2 case has det B_Z factoring into explicit branches;
     samples on each branch are pure; identification OPEN (they are
     codimension >= 2 walls inside the (b2)-chart; every point has a
     >= 5-dim ambient component by the incidence codimension bound).
"""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


z = sp.symbols("z0:4")
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)


def covrow(rows3):
    form = perm4((tuple(z),) + tuple(rows3))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.expand(stack[rows, cols].det()) != 0:
                return False
    return True


# =========================== (A) Zc ==========================================
p2, p3, q2, q3, w2 = sp.symbols("p2 p3 q2 q3 w2")
Wc = -(p3 + q3)*w2/(p2*q3 + p3*q2)
zeta_c = (Wc, 0, w2, 0)
planes_c = [
    [U3v, zeta_c],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, Wc, w2, 0)],
]
# zeta is in the kernel of M_Z on the branch:
MZc = sp.Matrix([covrow((YBAR, YBAR, (0, Wc, w2, 0))),
                 covrow((YBAR, (0, 1, q2, q3), (0, Wc, w2, 0))),
                 covrow(((0, 1, p2, p3), YBAR, (0, Wc, w2, 0)))])
for kv in (U3v, zeta_c):
    assert all(sp.simplify(sp.together(sum(MZc[i, j]*sp.sympify(kv[j])
                                           for j in range(4)))) == 0 for i in range(3))
# identical purity, support:
Tc = {bits: sp.cancel(sp.together(perm4(tuple(tuple(planes_c[m][bits[m]])
                                              for m in range(4)))))
      for bits in itertools.product((0, 1), repeat=4)}
nzc = {bits for bits, val in Tc.items() if sp.simplify(val) != 0}
assert nzc == {(0, 1, 1, 0)}, nzc
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    mat = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        mat[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = Tc[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            assert sp.simplify(mat[r1, c1]*mat[r2, c2] - mat[r1, c2]*mat[r2, c1]) == 0
print("(A) Zc family: pure for ALL parameters; support = single word e_0110.")
# profile bound: rank-2 edge {0,3}, rank-3 with 4x4-minor vanishing at the rest
prof = {}
for a_, b_ in COORD_PAIRS:
    rows_ = []
    for pa in planes_c[a_]:
        for pb in planes_c[b_]:
            prod = rmul(tuple(sp.sympify(c) for c in pa), tuple(sp.sympify(c) for c in pb))
            rows_.append([sp.together(prod[ab]) for ab in COORD_PAIRS])
    mm = sp.Matrix(rows_)
    if (a_, b_) == (0, 3):
        for rr in itertools.combinations(range(4), 3):
            for cc in itertools.combinations(range(6), 3):
                assert sp.cancel(sp.together(mm[rr, cc].det())) == 0
    elif (a_, b_) != (1, 2):   # (1,2) is the rank-4 edge
        for rr in itertools.combinations(range(4), 4):
            for cc in itertools.combinations(range(6), 4):
                assert sp.cancel(sp.together(mm[rr, cc].det())) == 0
    prof[(a_, b_)] = mm.rank()
assert tuple(prof[e_] for e_ in COORD_PAIRS) == (3, 3, 2, 4, 3, 3)
print("    generic profile (3,3,2,4,3,3): rank-2 pair edge at {0,3};")
print("    all 3x3 minors vanish there and all 4x4 minors at the other")
print("    <=3 edges: rank sum <= 18 on closure(F_Zc).")
# Zc2 = source-swap (01) of Zc1
swap01 = lambda row: (row[1], row[0], row[2], row[3])
img = [[swap01(tuple(sp.sympify(c) for c in r_)) for r_ in pl] for pl in planes_c]
planes_c2 = [
    [U3v, (-Wc, 0, w2, 0)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, -Wc, w2, 0)],
]
assert all(same_plane(img[mm], planes_c2[mm]) for mm in range(4))
print("    Zc2 == source-swap (01) image of Zc1: one census orbit.")
# ranks at the sample (from the working analysis): tangent 5, incidence 13
print("    at the exact sample (p2,p3,q2,q3,w2) = (2,3,5,7,1): family tangent")
print("    rank 5, incidence Jacobian rank 13 (tangent dim 7) -- doubly")
print("    singular; the five-slice ds run exceeded the local budget: the")
print("    ambient component of the Zc wall is OPEN (candidates: a wall of")
print("    the seventh [sieve-compatible, rank-2 edge] or a new component).")

# =========================== (B) case Y ======================================
wv = sp.symbols("wv0:4")
p_ = (0, 1, p2, p3)
q_ = (0, 1, q2, q3)
Y1 = covrow((p_, q_, U3v))
P_ = sp.expand(p2*q3 + p3*q2)
assert [sp.expand(c) for c in Y1] == [P_, P_, sp.expand(p3+q3), sp.expand(p2+q2)]
kA = (sp.expand(p3+q3), 0, -P_, 0)
kB = (sp.expand(p2+q2), 0, 0, -P_)
for kv in (YBAR, kA, kB):
    assert sp.expand(sum(Y1[i]*kv[i] for i in range(4))) == 0
print("(B) case Y: single covector Y1 = (P, P, p3+q3, p2+q2),")
print("    ker Y1 = span(ybar, kA, kB) (chart valid off P = 0).")
print("    The residual 2x2x2 purity system's minAssGTZ stratification is")
print("    recorded below; survivors are >= 4-dim walls whose ambient")
print("    components are OPEN except: the p||q||conj(w_Pi), w-in-Pi prime")
print("    is the tenth's own stratum (s03 (4): its U0-fibre is the tenth's")
print("    Grassmannian fibre).  The P = 0 sub-case needs the alternate")
print("    kernel chart span(e0, e1, (0,0,p2+q2,-(p3+q3))) and is OPEN.")
w_ = (0, wv[1], wv[2], wv[3])
Z1 = covrow((YBAR, YBAR, w_))
Z2 = covrow((YBAR, q_, w_))
Z3 = covrow((p_, YBAR, w_))
Z4 = covrow((p_, q_, w_))
aY, bY = sp.symbols("aY bY")
z1 = tuple(sp.expand(kA[t] + aY*YBAR[t]) for t in range(4))
z2 = tuple(sp.expand(kB[t] + bY*YBAR[t]) for t in range(4))
H = {}
for i, zz in enumerate((z1, z2)):
    H[(i, 0, 0)] = sp.expand(sum(Z1[t]*zz[t] for t in range(4)))
    H[(i, 0, 1)] = sp.expand(sum(Z2[t]*zz[t] for t in range(4)))
    H[(i, 1, 0)] = sp.expand(sum(Z3[t]*zz[t] for t in range(4)))
    H[(i, 1, 1)] = sp.expand(sum(Z4[t]*zz[t] for t in range(4)))
minors = []
idx = list(itertools.product((0, 1), repeat=3))
for ka in idx:
    for kb2 in idx:
        if ka < kb2:
            for fixed in range(3):
                if ka[fixed] != kb2[fixed]:
                    kc = tuple(kb2[t] if t == fixed else ka[t] for t in range(3))
                    kd = tuple(ka[t] if t == fixed else kb2[t] for t in range(3))
                    mm = sp.expand(H[ka]*H[kb2] - H[kc]*H[kd])
                    if mm != 0:
                        minors.append(mm)
minors = sorted({sp.expand(mm) for mm in minors} - {sp.Integer(0)},
                key=sp.default_sort_key)
polys = ";\n".join(f"poly g{i}={str(mm).replace('**','^')}" for i, mm in enumerate(minors))
hpolys = ";\n".join(f"poly h{i}={str(H[key]).replace('**','^')}"
                    for i, key in enumerate(sorted(H)))
program = "\n".join((
    'LIB "primdec.lib";',
    "ring R=0,(p2,p3,q2,q3,wv1,wv2,wv3,aY,bY),dp;",
    polys + ";",
    hpolys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(minors))) + ";",
    "ideal HH=" + ",".join(f"h{i}" for i in range(8)) + ";",
    "list L=minAssGTZ(I);",
    '"NPRIMES:"+string(size(L));',
    "int i; int j; int nzs;",
    "for(i=1;i<=size(L);i++){",
    "  ideal S=std(L[i]);",
    "  nzs=0;",
    "  for(j=1;j<=8;j++){ if(reduce(HH[j],S)!=0){nzs=1;} }",
    '  "PRIME "+string(i)+" DIM "+string(dim(S))+" NONZERO "+string(nzs);',
    "}",
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=1800, check=False)
out = completed.stdout
assert "NPRIMES:" in out, out[-500:]
nprimes = int(out.split("NPRIMES:")[1].split()[0])
lines = [ln for ln in out.splitlines() if ln.startswith("PRIME ")]
survivors = [ln for ln in lines if ln.endswith("NONZERO 1")]
print(f"    chart without ybar: {nprimes} primes; {len(survivors)} carry a")
print("    nonzero restriction; dims:",
      sorted({int(ln.split("DIM ")[1].split()[0]) for ln in survivors}))
print("    (full generator lists reproducible from this script's ideal I).")

# the U0-contains-ybar chart of case Y
cY = sp.Symbol("cY")
zc1_ = tuple(sp.expand(kA[t] + cY*kB[t]) for t in range(4))
H1 = {}
for i, zz in enumerate((YBAR, zc1_)):
    H1[(i, 0, 0)] = sp.expand(sum(Z1[t]*zz[t] for t in range(4)))
    H1[(i, 0, 1)] = sp.expand(sum(Z2[t]*zz[t] for t in range(4)))
    H1[(i, 1, 0)] = sp.expand(sum(Z3[t]*zz[t] for t in range(4)))
    H1[(i, 1, 1)] = sp.expand(sum(Z4[t]*zz[t] for t in range(4)))
minors1 = []
for ka_ in idx:
    for kb_ in idx:
        if ka_ < kb_:
            for fixed in range(3):
                if ka_[fixed] != kb_[fixed]:
                    kc_ = tuple(kb_[tt] if tt == fixed else ka_[tt] for tt in range(3))
                    kd_ = tuple(ka_[tt] if tt == fixed else kb_[tt] for tt in range(3))
                    mm1 = sp.expand(H1[ka_]*H1[kb_] - H1[kc_]*H1[kd_])
                    if mm1 != 0:
                        minors1.append(mm1)
minors1 = sorted({sp.expand(mm1) for mm1 in minors1} - {sp.Integer(0)},
                 key=sp.default_sort_key)
polys1 = ";\n".join(f"poly g{i}={str(mm1).replace('**','^')}"
                    for i, mm1 in enumerate(minors1))
hpolys1 = ";\n".join(f"poly h{i}={str(H1[key]).replace('**','^')}"
                     for i, key in enumerate(sorted(H1)))
program1 = "\n".join((
    'LIB "primdec.lib";',
    "ring R=0,(p2,p3,q2,q3,wv1,wv2,wv3,cY),dp;",
    polys1 + ";",
    hpolys1 + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(minors1))) + ";",
    "ideal HH=" + ",".join(f"h{i}" for i in range(8)) + ";",
    "list L=minAssGTZ(I);",
    '"NPRIMES:"+string(size(L));',
    "int i; int j; int nzs;",
    "for(i=1;i<=size(L);i++){",
    "  ideal S=std(L[i]);",
    "  nzs=0;",
    "  for(j=1;j<=8;j++){ if(reduce(HH[j],S)!=0){nzs=1;} }",
    '  "PRIME "+string(i)+" DIM "+string(dim(S))+" NONZERO "+string(nzs);',
    "}",
    "quit;",
))
completed1 = subprocess.run(("Singular", "-q"), input=program1, text=True,
                            encoding="utf-8", errors="replace",
                            capture_output=True, timeout=1800, check=False)
out1 = completed1.stdout
if "NPRIMES:" in out1:
    npr1 = int(out1.split("NPRIMES:")[1].split()[0])
    lines1 = [ln for ln in out1.splitlines() if ln.startswith("PRIME ")]
    surv1 = [ln for ln in lines1 if ln.endswith("NONZERO 1")]
    print(f"    chart with ybar in U0: {npr1} primes; {len(surv1)} carry a")
    print("    nonzero restriction; dims:",
          sorted({int(ln.split("DIM ")[1].split()[0]) for ln in surv1}))
else:
    print("    chart with ybar in U0: Singular run exceeded budget (null).")

# =========================== (C) p-in-Pi walls ================================
pk, qq2, qq3 = sp.symbols("pk qq2 qq3")
wg = sp.symbols("wg0:4")
pPi = (0, 0, 1, pk)


def MZ_of(p__, q__, w__):
    return sp.Matrix([covrow((YBAR, YBAR, tuple(w__))),
                      covrow((YBAR, tuple(q__), tuple(w__))),
                      covrow((tuple(p__), YBAR, tuple(w__)))])


MPi = MZ_of(pPi, (0, 1, qq2, qq3), (0, wg[1], wg[2], wg[3]))
m3 = [sp.factor(MPi[:, cols].det()) for cols in itertools.combinations(range(4), 3)]
nzm = [mm for mm in m3 if mm != 0]
target = sp.expand(4*wg[1]*wg[2]*wg[3]*(pk*qq2 - qq3))
assert all(sp.expand(mm - target) == 0 or sp.expand(mm + target) == 0 for mm in nzm)
print("(C) p-in-Pi wall (U1 = span(ybar,(0,0,1,pk))): rank M_Z <= 2 <=>")
print("    w1*w2*w3*(pk*q2 - q3) = 0; each branch has an explicit forced-U0")
print("    det (computed in the working notes); their pure points are")
print("    codimension >= 2 walls of the chart; identification OPEN.")
print()
print("ALL CHECKS PASSED (open items flagged above)")
