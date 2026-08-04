#!/usr/bin/env python3
"""The e = 1 leaf of the equal-support chart (U1 cap Pi = U2 cap Pi: the
in-out analogue of the shared-factor coincidence).

At e = 1 the chart's U3-basis (y3, u3) = ((0,0,1,1),(0,0,1,1)) is
degenerate; every (e-1)-factor in the e != 1 chart formulas is a basis
artifact (the F3-sheet lesson).  With the honest basis (e2, e3):

 case beta (K1 = K2 = the shared direction u1):
   two covectors  B1 = -(x1, x0, 0, 0),  B2 = -(v1, v0, 0, 0);
   open part (v-bar not || x-bar): U0 = Pi forced and the residual 2x2
   is [[s, 0], [s, s]] (basis (e2,e3)): det = s^2, and at s = 0 the
   whole block vanishes: pure => ZERO;
   deep part (x-bar = t v-bar): chart L (U0 contains wbar) is EXACTLY
   the C10 family at c1 = c2 = 1 (the eleventh's own c1 = c2 wall,
   already inside the family); chart N has det = -4 t^2 v0^2 v1^2 != 0:
   EMPTY (this corrects the degenerate-basis (e-1)*det == 0 artifact);
 case alpha (K3 = y3 = conj(u1)): a single covector row
   (v1(x2+x3)+x1(v2+v3), v0(x2+x3)+x0(v2+v3), s, s) (the e=1 limit of
   the case-1 matrix M1, whose first row vanishes identically at e=1);
   U0 ranges over Gr(2, ker) and purity is a 2x2x2 system; its
   minAssGTZ stratification is computed below with the nonzero-
   restriction filter; the surviving strata are recorded; their census
   identification is OPEN (flagged; they are coincidence walls of the
   equal-support chart with K3 = conj(u1))."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.expand(stack[rows, cols].det()) != 0:
                return False
    return True


z = sp.symbols("z0:4")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
u1 = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
E2, E3 = (0, 0, 1, 0), (0, 0, 0, 1)
s = sp.expand(v[0]*x[1] + v[1]*x[0])


def covrow(rows3):
    form = perm4((tuple(z),) + tuple(rows3))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


# ---- case beta ---------------------------------------------------------------
B1 = covrow((u1, tuple(x), E2))
B2 = covrow((tuple(v), u1, E2))
# the two covectors (with the honest Pi-basis); rows supported on cols {0,1}:
assert all(sp.expand(a - b) == 0 for a, b in zip(B1, (-x[1], -x[0], 0, 0)))
assert all(sp.expand(a - b) == 0 for a, b in zip(B2, (-v[1], -v[0], 0, 0)))
# and the e3-versions are proportional (same conditions):
B1b = covrow((u1, tuple(x), E3))
B2b = covrow((tuple(v), u1, E3))
assert all(sp.expand(a - b) == 0 for a, b in zip(B1b, (x[1], x[0], 0, 0)))
assert all(sp.expand(a - b) == 0 for a, b in zip(B2b, (v[1], v[0], 0, 0)))
print("case beta: covectors -(x1,x0,0,0), -(v1,v0,0,0) (for both Pi-basis")
print("  vectors): U0 = Pi forced when v-bar not || x-bar.")
Bopen = sp.Matrix(2, 2, lambda i, j: perm4(((E2, E3)[i], tuple(v), tuple(x),
                                            (E2, E3)[j])))
assert sp.expand(Bopen[0, 0]) == 0 and sp.expand(Bopen[1, 1]) == 0
assert sp.expand(Bopen[0, 1] - s) == 0 and sp.expand(Bopen[1, 0] - s) == 0
print("  open part: residual 2x2 = [[0, s],[s, 0]], det = -s^2; at s = 0 the")
print("  block vanishes: pure => ZERO restriction.  OK")
# deep part x-bar = t*v-bar
t, c0, p, q = sp.symbols("t c0 p q")
xd = (t*v[0], t*v[1], x[2], x[3])
wbar = (v[0], -v[1], 0, 0)
# chart L: U0 = span(wbar, (0,0,1,-c0)): the C10 family at c1 = c2 = 1:
def C10(a0_, a1_, c0_, c1_, c2_, vvrow, t_, x2_, x3_):
    return [
        [(a0_, -a1_, 0, 0), (0, 0, 1, -c0_)],
        [(0, 0, 1, -c1_), tuple(vvrow)],
        [(0, 0, 1, -c2_), (t_*a0_, t_*a1_, x2_, x3_)],
        [(0, 0, 1, 1), (0, 0, 1, -1)],
    ]


e1_L = [
    [wbar, (0, 0, 1, -c0)],
    [u1, tuple(v)],
    [u1, xd],
    [E2, E3],
]
img = C10(v[0], v[1], c0, sp.Integer(1), sp.Integer(1), v, t, x[2], x[3])
assert all(same_plane(e1_L[m], img[m]) for m in range(4))
print("  deep chart L == C10 at (c1, c2) = (1, 1): the eleventh's own")
print("  c1 = c2 wall (inside the parametrized family).  OK")
# chart N: honest-basis det
zN1 = tuple(sp.expand(a + p*b) for a, b in zip(E2, wbar))
zN2 = tuple(sp.expand(a + q*b) for a, b in zip(E3, wbar))
BN = sp.Matrix(2, 2, lambda i, j: perm4(((zN1, zN2)[i], tuple(v), xd, (E2, E3)[j])))
assert sp.expand(BN.det() + 4*t**2*v[0]**2*v[1]**2) == 0
print("  deep chart N: det = -4 t^2 v0^2 v1^2 (honest basis, no (e-1)")
print("  artifact): EMPTY off the zero strata.  OK")

# ---- case alpha --------------------------------------------------------------
row = covrow((tuple(v), tuple(x), Y3))
assert all(sp.expand(a - b) == 0 for a, b in zip(
    row, (v[1]*(x[2]+x[3]) + x[1]*(v[2]+v[3]),
          v[0]*(x[2]+x[3]) + x[0]*(v[2]+v[3]), s, s)))
C0r, C1r = row[0], row[1]
k1 = (-C1r, C0r, 0, 0)
k2 = (s, 0, -C0r, 0)
k3 = (s, 0, 0, -C0r)
for kv in (k1, k2, k3):
    assert sp.expand(sum(row[i]*kv[i] for i in range(4))) == 0
print("case alpha: single covector row (C0, C1, s, s); kernel basis")
print("  {(-C1,C0,0,0), (s,0,-C0,0), (s,0,0,-C0)} (C0 != 0 chart).")
# the residual 2x2x2 minors; gauge v3 = x3 = 0 to keep the system small
gauge = {v[3]: 0, x[3]: 0}
aA, bA = sp.symbols("aA bA")
z1 = tuple(sp.expand(sp.sympify(c).subs(gauge)) for c in
           (k2[0] + aA*k1[0], k2[1] + aA*k1[1], k2[2] + aA*k1[2], k2[3] + aA*k1[3]))
z2 = tuple(sp.expand(sp.sympify(c).subs(gauge)) for c in
           (k3[0] + bA*k1[0], k3[1] + bA*k1[1], k3[2] + bA*k1[2], k3[3] + bA*k1[3]))
vg = tuple(sp.sympify(c).subs(gauge) for c in v)
xg = tuple(sp.sympify(c).subs(gauge) for c in x)
H = {}
for i, zz in enumerate((z1, z2)):
    H[(i, 0, 0)] = sp.expand(perm4((zz, u1, u1, E2)))
    H[(i, 0, 1)] = sp.expand(perm4((zz, u1, xg, E2)))
    H[(i, 1, 0)] = sp.expand(perm4((zz, vg, u1, E2)))
    H[(i, 1, 1)] = sp.expand(perm4((zz, vg, xg, E2)))
    assert H[(i, 0, 0)] == 0
minors = []
idx = list(itertools.product((0, 1), repeat=3))
for ka in idx:
    for kb in idx:
        if ka < kb:
            for fixed in range(3):
                if ka[fixed] != kb[fixed]:
                    kc = tuple(kb[tt] if tt == fixed else ka[tt] for tt in range(3))
                    kd = tuple(ka[tt] if tt == fixed else kb[tt] for tt in range(3))
                    mm = sp.expand(H[ka]*H[kb] - H[kc]*H[kd])
                    if mm != 0:
                        minors.append(mm)
minors = sorted({sp.expand(mm) for mm in minors} - {sp.Integer(0)},
                key=sp.default_sort_key)
polys = ";\n".join(f"poly g{i}={str(mm).replace('**','^')}" for i, mm in enumerate(minors))
hpolys = ";\n".join(f"poly h{i}={str(H[key]).replace('**','^')}"
                    for i, key in enumerate(sorted(H)))
program = "\n".join((
    'LIB "primdec.lib";',
    "ring R=0,(v0,v1,v2,x0,x1,x2,aA,bA),dp;",
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
    '  if(nzs==1){ "SURVIVOR "+string(i)+" DIM "+string(dim(S)); L[i]; }',
    "}",
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=1500, check=False)
out = completed.stdout
if "NPRIMES:" in out:
    print("case alpha 2x2x2 purity stratification (gauge v3=x3=0, chart")
    print("  U0 = span(k2+a*k1, k3+b*k1)):")
    print(out[-2500:])
    print("  identification of the surviving strata vs the thirteen census")
    print("  orbits: OPEN (coincidence walls; every point has a >= 5-dim")
    print("  ambient component by the incidence codimension bound).")
else:
    print("case alpha minAss run exceeded the local budget: recorded null;")
    print("  the sub-sweep is OPEN (system recorded in this script).")
print()
print("ALL CHECKS PASSED (open items flagged above)")
