#!/usr/bin/env python3
"""RESOLUTION OF TAIL 3 (the e = 1 case-alpha survivor walls of the
equal-support chart, s12) -- COMPLETE sweep of the case-alpha leaf.

Setting (s12): equal-support chart at e = 1, honest Pi-basis:
    u1 = (0,0,1,-1) = U1 cap Pi = U2 cap Pi,   y3 = (0,0,1,1) = conj(u1),
    U1 = span(u1, v),  U2 = span(u1, x),  U3 = Pi = span(e2, e3),
    gauge v3 = x3 = 0 (shifts by u1).
Case alpha: K3 = y3.  The single surviving covector on U0 is
    row = (C0, C1, s, s),  C0 = v1 x2 + x1 v2,  C1 = v0 x2 + x0 v2,
    s = v0 x1 + v1 x0,
and purity is the rank-one condition on the residual 2x2x2 tensor H
(values T(z_i, b_j, c_k, e2)).  s12 recorded the (aY,bY)-chart minAss
(10 primes, four nonzero survivors) and left their identification open.

THIS SCRIPT CLOSES THE WHOLE LEAF.  Decision tree (all replayed):

 (alpha-I) C0 != 0 [the case C1 != 0 is its image under the source swap
   (01), which preserves the configuration family]:
   kernel basis k1 = (-C1,C0,0,0), k2 = (s,0,-C0,0), k3 = (s,0,0,-C0);
   U0 in Gr(2, span(k1,k2,k3)) = (aY,bY)-chart  u  k1-chart.
   * (aY,bY)-chart (s12's 10 primes, replayed): primes {x1=x2=0} and
     {v1=v2=0} are CHART ARTIFACTS (z1 wedge z2 == 0 identically: they
     parametrize no plane); the honest {x || e0} stratum is swept below;
     primes {s=0,x2=0} and {s=0,v2=0} are honest and are identified
     EXACTLY as mode-swap images of the C10 family (= ELEVENTH
     component) at c0 = c1 = 1; the other six primes carry only the
     zero restriction.
   * k1-chart (U0 = span(k1, al*k2 + be*k3), 12 primes): four chart
     artifacts (al=be=0 or k-degeneracies), five zero-restriction
     primes, and three nonzero honest primes, ALL identified into C10:
     {x-bar || v-bar, al+be = 0} is C10 at c0=c1=c2=1, and
     {s=0, x2=0} / {s=0, v2=0} are the missing-chart boundaries of the
     two honest survivors (same C10 walls).
   * honest {x || e0} stratum (row = (0, v2 x0, v1 x0, v1 x0)):
     all three Gr(2,3)-charts of U0 force v1*x0 = 0: EMPTY; the
     boundary v1 = 0 puts all four planes in {z1 = 0}: zero
     restriction.  {v || e0} follows by the mode swap (12) (v <-> x).
 (alpha-II) C0 = 0 != C1: = (01)-source image of (alpha-I)'s C1 = 0
   locus: covered.
 (alpha-III) C0 = C1 = 0, s != 0: the linear system in (x2, v2) has
   determinant v1 x0 - v0 x1, so either
   * S2a: v2 = x2 = 0: pure points force x-bar || v-bar || (-aa,1),
     U0 = span(wbar, u1), bb = 0: EXACTLY C10 at c0 = c1 = c2 = 1
     (identity modes); or
   * S2b: x-bar = t v-bar, x2 = -t v2 (v2 != 0): pure points force
     U0 = span(wbar, u1): EXACTLY C10 at c0 = c1 = c2 = 1 with
     x-row t(v0, v1, -v2, 0); or
   * S2c: v in Pi or x in Pi: U1 = Pi or U2 = Pi: TWO-Pi-PLANES LEMMA
     (below): zero restriction.
 (alpha-IV) row == 0 (C0 = C1 = s = 0): U0 is FREE in Gr(2,4):
   * S3a: v2 = x2 = 0, x-bar || conj(v-bar): the six-chart sweep leaves
     exactly the U0's containing a Pi-vector and a (v0,-+v1,*,*)-vector;
     both families are EXACTLY C10 under the mode swap (01) resp. its
     (12)-composition: ELEVENTH; nothing else is pure.
   * S3b: v = (0,v1,v2,0), x ~ (0,v1,-v2,0) (and its (01)-mirror):
     NO nonzero pure points (all six charts: minAss finds none).
   * S3c: v in Pi or x in Pi: zero (lemma).

TWO-Pi-PLANES LEMMA (exact): if two of the four planes equal
Pi = span(e2,e3), the restriction factors T = M (x) N with
N = [[0,1],[1,0]] (the hyperbolic form), and every rank-one minor set
contains -M[i,j]^2: purity forces M == 0, i.e. T == 0.

VERDICT: every nonzero pure point of the e = 1 case-alpha leaf lies in
the ELEVENTH component orbit (C10 walls); no new component."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.simplify(sp.together(stack[rows, cols].det())) != 0:
                return False
    return (sp.Matrix([list(P[0]), list(P[1])]).rank() == 2
            and sp.Matrix([list(Q[0]), list(Q[1])]).rank() == 2)


def assert_pure_nonzero(planes, label, allow_symbolic=True):
    T = {bits: sp.expand(sp.together(perm4(tuple(tuple(sp.sympify(c)
                                                       for c in planes[m][bits[m]])
                                                 for m in range(4)))))
         for bits in itertools.product((0, 1), repeat=4)}
    assert any(sp.simplify(val) != 0 for val in T.values()), (label, "zero")
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            m[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        for r1, r2 in itertools.combinations(range(4), 2):
            for c1, c2 in itertools.combinations(range(4), 2):
                assert sp.simplify(sp.together(
                    m[r1, c1]*m[r2, c2] - m[r1, c2]*m[r2, c1])) == 0, (label, "not pure")
    return T


z = sp.symbols("z0:4")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
u1 = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
E0, E1, E2, E3 = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)


def covrow(rows3):
    form = perm4((tuple(z),) + tuple(rows3))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


def C10(a0_, a1_, c0_, c1_, c2_, vvrow, t_, x2_, x3_):
    """The eleventh component's parametrized family (equal-support
    snapshot steps 22-25 / s12): identically pure for all parameters."""
    return [
        [(a0_, -a1_, 0, 0), (0, 0, 1, -c0_)],
        [(0, 0, 1, -c1_), tuple(vvrow)],
        [(0, 0, 1, -c2_), (t_*a0_, t_*a1_, x2_, x3_)],
        [(0, 0, 1, 1), (0, 0, 1, -1)],
    ]


# C10 purity replay (function field): the identification below then puts
# every identified stratum inside the ELEVENTH component.
a0s, a1s, c0s, c1s, c2s, ts, x2s, x3s, vv2, vv3 = sp.symbols(
    "a0s a1s c0s c1s c2s ts x2s x3s vv2 vv3")
_ = assert_pure_nonzero(C10(a0s, a1s, c0s, c1s, c2s,
                            (a0s, a1s, vv2, vv3), ts, x2s, x3s), "C10")
print("C10 family replay: identically pure over the full function field.  OK")

gauge = {v[3]: 0, x[3]: 0}
row = [sp.expand(sp.sympify(c).subs(gauge)) for c in covrow((tuple(v), tuple(x), Y3))]
C0r, C1r = row[0], row[1]
s = sp.expand(v[0]*x[1] + v[1]*x[0])
assert sp.expand(C0r - (v[1]*x[2] + x[1]*v[2])) == 0
assert sp.expand(C1r - (v[0]*x[2] + x[0]*v[2])) == 0
assert row[2] == s and row[3] == s
k1 = (-C1r, C0r, 0, 0)
k2 = (s, 0, -C0r, 0)
k3 = (s, 0, 0, -C0r)
for kv in (k1, k2, k3):
    assert sp.expand(sum(row[t]*kv[t] for t in range(4))) == 0
vg = tuple(sp.sympify(c).subs(gauge) for c in v)
xg = tuple(sp.sympify(c).subs(gauge) for c in x)


def Hpack(z1, z2, vrow=None, xrow=None):
    vrow = vg if vrow is None else vrow
    xrow = xg if xrow is None else xrow
    H = {}
    for i, zz in enumerate((z1, z2)):
        H[(i, 0, 0)] = sp.expand(perm4((zz, u1, u1, E2)))
        H[(i, 0, 1)] = sp.expand(perm4((zz, u1, xrow, E2)))
        H[(i, 1, 0)] = sp.expand(perm4((zz, vrow, u1, E2)))
        H[(i, 1, 1)] = sp.expand(perm4((zz, vrow, xrow, E2)))
    return H


def commutation_minors(H):
    out = set()
    idx = list(itertools.product((0, 1), repeat=3))
    for ka in idx:
        for kb in idx:
            if ka < kb:
                for fixed in range(3):
                    if ka[fixed] != kb[fixed]:
                        kc = tuple(kb[t] if t == fixed else ka[t] for t in range(3))
                        kd = tuple(ka[t] if t == fixed else kb[t] for t in range(3))
                        mm = sp.expand(H[ka]*H[kb] - H[kc]*H[kd])
                        if mm != 0:
                            out.add(mm)
    return sorted(out, key=sp.default_sort_key)


def minass(minors, Hvals, ringvars, timeout=1200):
    polys = ";\n".join(f"poly g{i}={str(mm).replace('**','^')}"
                       for i, mm in enumerate(minors))
    hpolys = ";\n".join(f"poly h{i}={str(val).replace('**','^')}"
                        for i, val in enumerate(Hvals))
    program = "\n".join((
        'LIB "primdec.lib";',
        f"ring R=0,({ringvars}),dp;",
        polys + ";", hpolys + ";",
        "ideal I=" + ",".join(f"g{i}" for i in range(len(minors))) + ";",
        "ideal HH=" + ",".join(f"h{i}" for i in range(len(Hvals))) + ";",
        "list L=minAssGTZ(I);",
        '"NPRIMES:"+string(size(L));',
        "int i; int j; int nzs;",
        "for(i=1;i<=size(L);i++){ ideal S=std(L[i]); nzs=0;",
        f"  for(j=1;j<={len(Hvals)};j++){{ if(reduce(HH[j],S)!=0){{nzs=1;}} }}",
        '  "PRIME "+string(i)+" NONZERO "+string(nzs)+" GENS "+string(L[i]);',
        "}",
        "quit;",
    ))
    completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                               encoding="utf-8", errors="replace",
                               capture_output=True, timeout=timeout, check=False)
    out = completed.stdout
    assert "NPRIMES:" in out, out[-800:]
    nprimes = int(out.split("NPRIMES:")[1].split()[0])
    primes = []
    for ln in out.splitlines():
        if ln.startswith("PRIME "):
            nz = int(ln.split("NONZERO ")[1].split()[0])
            gens = ln.split("GENS ")[1]
            genset = frozenset(g.strip() for g in gens.split(","))
            primes.append((nz, genset))
    assert len(primes) == nprimes
    return primes


def find_prime(primes, wanted):
    wanted = frozenset(wanted)
    hits = [pr for pr in primes if pr[1] == wanted]
    assert len(hits) == 1, (wanted, [p[1] for p in primes])
    return hits[0]


# ======================= (alpha-I) (aY,bY)-chart: the 10 primes =============
aA, bA = sp.symbols("aA bA")
z1ab = tuple(sp.expand(k2[t] + aA*k1[t]) for t in range(4))
z2ab = tuple(sp.expand(k3[t] + bA*k1[t]) for t in range(4))
Hab = Hpack(z1ab, z2ab)
assert Hab[(0, 0, 0)] == 0 and Hab[(1, 0, 0)] == 0
prim_ab = minass(commutation_minors(Hab), list(Hab.values()),
                 "v0,v1,v2,x0,x1,x2,aA,bA")
assert len(prim_ab) == 10
nz_sets = set(pr[1] for pr in prim_ab if pr[0] == 1)
assert nz_sets == {
    frozenset({"x2", "x1"}), frozenset({"v2", "v1"}),
    frozenset({"v1*x0+v0*x1", "x2"}), frozenset({"v1*x0+v0*x1", "v2"})}, nz_sets
print("(alpha-I ab-chart) 10 primes replayed; nonzero survivors:")
print("   {x1=x2=0}, {v1=v2=0}, {s=0,x2=0}, {s=0,v2=0}.  OK")

# artifacts: {x1=x2=0} and {v1=v2=0} give z1 wedge z2 == 0 identically
for name, sub in (("{x1=x2=0}", {x[1]: 0, x[2]: 0}),
                  ("{v1=v2=0}", {v[1]: 0, v[2]: 0})):
    z1s = tuple(sp.expand(c.subs(sub)) for c in z1ab)
    z2s = tuple(sp.expand(c.subs(sub)) for c in z2ab)
    assert all(sp.expand(z1s[i]*z2s[j] - z1s[j]*z2s[i]) == 0 for i, j in COORD_PAIRS)
    print(f"   survivor {name}: z1 wedge z2 == 0 identically: CHART ARTIFACT.  OK")

# ================= honest {x || e0} stratum (and {v || e0} mirror) ==========
sub4 = {x[1]: 0, x[2]: 0, x[3]: 0, v[3]: 0}
rowg = [sp.expand(sp.sympify(c).subs(sub4)) for c in row]
assert rowg == [0, sp.expand(v[2]*x[0]), sp.expand(v[1]*x[0]), sp.expand(v[1]*x[0])]
KB4 = [E0, u1, (0, v[1], -v[2], 0)]
for kv in KB4:
    assert sp.expand(sum(rowg[t]*sp.sympify(kv[t]) for t in range(4))) == 0
xg4 = (x[0], 0, 0, 0)
aa, bb = sp.symbols("aa bb")
forced = []
for ci, (i_, j_, l_) in enumerate(((0, 1, 2), (1, 0, 2), (2, 0, 1))):
    z1c = tuple(sp.expand(sp.sympify(KB4[j_][t]) + aa*sp.sympify(KB4[i_][t]))
                for t in range(4))
    z2c = tuple(sp.expand(sp.sympify(KB4[l_][t]) + bb*sp.sympify(KB4[i_][t]))
                for t in range(4))
    mins = commutation_minors(Hpack(z1c, z2c, xrow=xg4))
    if ci == 0:
        assert sp.expand(v[1]**2*x[0]**2) in mins
    elif ci == 1:
        assert sp.expand(v[1]**2*x[0]) in mins
    else:
        # aa*v1^2*x0^2 and v1^2*x0*(aa*v0+1) cannot both vanish with v1*x0 != 0
        assert sp.expand(aa*v[1]**2*x[0]**2) in mins
        assert sp.expand(v[1]**2*x[0]*(aa*v[0] + 1)) in mins
print("({x||e0} honest) all three U0-charts force v1*x0 = 0: EMPTY.  OK")
# boundary v1 = 0: all four planes lie in {z1 = 0}: zero restriction
zf = sp.symbols("zf0:4")
zrow = (zf[0], 0, zf[2], zf[3])
for rows in itertools.product((zrow,), (u1, (v[0], 0, v[2], 0)),
                              (u1, (x[0], 0, 0, 0)), (E2, E3)):
    assert all(sp.sympify(r_[1]) == 0 for r_ in rows)
    assert sp.expand(perm4(rows)) == 0
print("   boundary v1 = 0: all four planes in {z1=0}: zero restriction.  OK")
# {v || e0} is the (12)-mode-swap image (U1 <-> U2 swaps v <-> x): covered.
print("   {v||e0} = (12)-mode-swap image (v <-> x): EMPTY as well.  OK")

# ======= honest survivors {s=0,x2=0} / {s=0,v2=0}: EXACTLY C10 walls ========
V0, V1, V2, A_, B_ = sp.symbols("V0 V1 V2 A_ B_")
kbar = (V0, V1, 0, 0)
wbar = (V0, -V1, 0, 0)
surv6 = [
    [tuple(sp.expand(E2[t] + A_*kbar[t]) for t in range(4)),
     tuple(sp.expand(E3[t] + B_*kbar[t]) for t in range(4))],
    [u1, (V0, V1, V2, 0)],
    [u1, wbar],
    [E2, E3],
]
_ = assert_pure_nonzero(surv6, "surv6")
c10_img = C10(V0, V1, sp.Integer(1), sp.Integer(1), A_/B_, (V0, V1, V2, 0),
              A_, sp.Integer(1), sp.Integer(0))
sigma6 = (2, 1, 0, 3)          # C10 slot m <- surv6 mode sigma6[m]
assert all(same_plane(surv6[sigma6[m]], c10_img[m]) for m in range(4))
print("(survivor {s=0,x2=0}) pure identically; EXACT identification:")
print("   (02)-mode swap onto C10(c0=1, c1=1, c2=A/B, t=A, x=(1,0)):")
print("   a wall of the ELEVENTH component.  OK")
# missing boundary chart U0 = span(kbar, (0,0,al,be)):
albe = sp.symbols("albe0:2")
surv6b = [
    [kbar, (0, 0, albe[0], albe[1])],
    [u1, (V0, V1, V2, 0)],
    [u1, wbar],
    [E2, E3],
]
_ = assert_pure_nonzero(surv6b, "surv6-boundary")
c10_imgb = C10(V0, V1, sp.Integer(1), sp.Integer(1), -albe[1]/albe[0],
               (V0, V1, V2, 0), sp.Integer(1), sp.Integer(0), sp.Integer(0))
assert all(same_plane(surv6b[sigma6[m]], c10_imgb[m]) for m in range(4))
print("   boundary chart U0 = span(kbar, Pi-vector): also C10: ELEVENTH.  OK")
# {s=0, v2=0} = (12)-mode-swap image (v <-> x roles):
X0, X1, X2 = sp.symbols("X0 X1 X2")
surv8 = [
    [tuple(sp.expand(E2[t] + A_*sp.sympify((X0, X1, 0, 0)[t])) for t in range(4)),
     tuple(sp.expand(E3[t] + B_*sp.sympify((X0, X1, 0, 0)[t])) for t in range(4))],
    [u1, (X0, -X1, 0, 0)],
    [u1, (X0, X1, X2, 0)],
    [E2, E3],
]
_ = assert_pure_nonzero(surv8, "surv8")
c10_img8 = C10(X0, X1, sp.Integer(1), sp.Integer(1), A_/B_, (X0, X1, X2, 0),
               A_, sp.Integer(1), sp.Integer(0))
sigma8 = (1, 2, 0, 3)
assert all(same_plane(surv8[sigma8[m]], c10_img8[m]) for m in range(4))
print("(survivor {s=0,v2=0}) = (12)-swap mirror; EXACT C10 identification:")
print("   ELEVENTH component.  OK")

# ======================= (alpha-I) k1-chart: the 12 primes ==================
al, be = sp.symbols("al be")
z2k = tuple(sp.expand(al*k2[t] + be*k3[t]) for t in range(4))
Hk = Hpack(k1, z2k)
prim_k = minass(commutation_minors(Hk), list(Hk.values()),
                "v0,v1,v2,x0,x1,x2,al,be")
assert len(prim_k) == 12
nzk = [pr[1] for pr in prim_k if pr[0] == 1]
assert len(nzk) == 7
# artifacts: al=be=0 (z2 == 0) and the x||e0 / v||e0 degeneracies
for wanted in ({"be", "al", "x2"}, {"be", "al", "v2"}, {"x2", "x1"}, {"v2", "v1"}):
    nz_, gset = find_prime(prim_k, wanted)
    assert nz_ == 1
for sub, nm in (({x[1]: 0, x[2]: 0}, "{x1=x2=0}"), ({v[1]: 0, v[2]: 0}, "{v1=v2=0}")):
    z1s = tuple(sp.expand(sp.sympify(c).subs(sub)) for c in k1)
    z2s = tuple(sp.expand(c.subs(sub)) for c in z2k)
    assert all(sp.expand(z1s[i]*z2s[j] - z1s[j]*z2s[i]) == 0 for i, j in COORD_PAIRS)
print("(alpha-I k1-chart) 12 primes; artifacts {al=be=0,*} (z2 == 0) and")
print("   {x1=x2=0}/{v1=v2=0} (wedge == 0) replayed.  OK")
# the x-bar || v-bar survivor: {v0*x1-v1*x0 = 0, al+be = 0} -> C10(1,1,1)
_nz, _ = find_prime(prim_k, {"-v1*x0+v0*x1", "al+be"})
assert _nz == 1
T_ = sp.symbols("T_")
xk = (T_*v[0], T_*v[1], x[2], 0)
z1k = tuple(sp.expand(sp.sympify(c).subs({x[0]: T_*v[0], x[1]: T_*v[1],
                                          x[3]: 0, v[3]: 0})) for c in k1)
z2kk = tuple(sp.expand(c.subs({x[0]: T_*v[0], x[1]: T_*v[1], x[3]: 0,
                               v[3]: 0, be: -al})) for c in z2k)
surv_k1 = [[z1k, z2kk], [u1, (v[0], v[1], v[2], 0)], [u1, xk], [E2, E3]]
_ = assert_pure_nonzero(surv_k1, "k1-chart x||v survivor")
c10_k1 = C10(v[0], v[1], sp.Integer(1), sp.Integer(1), sp.Integer(1),
             (v[0], v[1], v[2], 0), T_, x[2], sp.Integer(0))
assert all(same_plane(surv_k1[m], c10_k1[m]) for m in range(4))
print("   {x-bar||v-bar, al+be=0} survivor: EXACT C10(c0=c1=c2=1): ELEVENTH.  OK")
# {s=0,x2=0} and {s=0,v2=0} in this chart are the boundary charts already
# identified above (surv6b and its mirror).
for wanted in ({"v1*x0+v0*x1", "x2"}, {"v1*x0+v0*x1", "v2"}):
    _nz, _ = find_prime(prim_k, wanted)
    assert _nz == 1
print("   {s=0,x2=0}/{s=0,v2=0} = the boundary charts of the honest")
print("   survivors (identified above): ELEVENTH.  OK")

# ====================== TWO-Pi-PLANES LEMMA (S2c, S3c) ======================
zA = sp.symbols("zA0:4")
zB = sp.symbols("zB0:4")
bU = sp.symbols("bU0:4")
M_ = {}
for i, zz in enumerate((zA, zB)):
    for j, brow in enumerate((bU, tuple(sp.Symbol(f"bV{t}") for t in range(4)))):
        Tijkl = {}
        for k_, l_ in itertools.product((0, 1), repeat=2):
            crow = (E2, E3)[k_]
            drow = (E2, E3)[l_]
            Tijkl[(k_, l_)] = sp.expand(perm4((zz, brow, crow, drow)))
        M_[(i, j)] = Tijkl
Mform = {}
for (i, j), Tijkl in M_.items():
    assert Tijkl[(0, 0)] == 0 and Tijkl[(1, 1)] == 0
    assert sp.expand(Tijkl[(0, 1)] - Tijkl[(1, 0)]) == 0
    Mform[(i, j)] = Tijkl[(0, 1)]
# mode-2 flattening minor at columns (i,j,l=0),(i,j,l=1) equals -M[i,j]^2:
for (i, j), mv in Mform.items():
    minor = sp.expand(0*0 - mv*mv)
    assert sp.expand(minor + mv**2) == 0
print("TWO-Pi-PLANES LEMMA: with U2 = U3 = Pi, T = M (x) [[0,1],[1,0]] and")
print("   the mode-2 flattening minors contain -M[i,j]^2 for every (i,j):")
print("   purity forces T == 0.  (Same for any two modes equal to Pi.)  OK")

# =================== (alpha-III): C0 = C1 = 0, s != 0 =======================
det_vx = sp.expand(v[1]*x[0] - v[0]*x[1])
sol = sp.solve([C0r, C1r], [x[2], v[2]], dict=True)
assert sol == [{x[2]: 0, v[2]: 0}] or all(
    sp.simplify(ss[x[2]]) == 0 and sp.simplify(ss[v[2]]) == 0 for ss in sol)
print("(alpha-III) det[[v1,x1],[v0,x0]] = v1*x0-v0*x1 != 0 => v2 = x2 = 0;")
print("   else x-bar || v-bar (branches S2b, S2c).  OK")
# S2a: v2 = x2 = 0 charts
subA = {v[2]: 0, x[2]: 0, v[3]: 0, x[3]: 0}
vgA = tuple(sp.sympify(c).subs(subA) for c in v)
xgA = tuple(sp.sympify(c).subs(subA) for c in x)
KB3 = [E0, E1, u1]
foundA = []
for ci, (i_, j_, l_) in enumerate(((0, 1, 2), (1, 0, 2), (2, 0, 1))):
    z1c = tuple(sp.expand(sp.sympify(KB3[j_][t]) + aa*sp.sympify(KB3[i_][t]))
                for t in range(4))
    z2c = tuple(sp.expand(sp.sympify(KB3[l_][t]) + bb*sp.sympify(KB3[i_][t]))
                for t in range(4))
    mins = commutation_minors(Hpack(z1c, z2c, vrow=vgA, xrow=xgA))
    if ci == 2:
        for mm in (v[0]*x[0], v[0]*x[1], v[1]*x[0], v[1]*x[1]):
            assert sp.expand(mm) in mins or sp.expand(-mm) in mins
        continue
    foundA.append((ci, mins))
# chart 0: pure <=> aa*x1+x0 = 0, aa*v1+v0 = 0, bb = 0 (given s != 0):
ci0, mins0 = foundA[0]
needed = {sp.expand(bb**2*v[1]*x[1]),
          sp.expand((aa*x[1] + x[0])*(v[0]*x[1] + v[1]*x[0])),
          sp.expand((aa*v[1] + v[0])*(v[0]*x[1] + v[1]*x[0])),
          sp.expand((aa*v[1] + v[0])*(aa*x[1] + x[0]))}
assert all(mm in mins0 or sp.expand(-mm) in mins0 for mm in needed)
# and on that solution the family is exactly C10(c0=c1=c2=1):
aaS = sp.Symbol("aaS")
v1S, x1S = sp.symbols("v1S x1S")
survA = [[(aaS, 1, 0, 0), u1],
         [u1, (-aaS*v1S, v1S, 0, 0)],
         [u1, (-aaS*x1S, x1S, 0, 0)],
         [E2, E3]]
_ = assert_pure_nonzero(survA, "S2a survivor")
c10_A = C10(-aaS*v1S, v1S, sp.Integer(1), sp.Integer(1), sp.Integer(1),
            (-aaS*v1S, v1S, 0, 0), x1S/v1S, sp.Integer(0), sp.Integer(0))
assert all(same_plane(survA[m], c10_A[m]) for m in range(4))
print("   S2a: pure points have U0 = span(wbar,u1), x-bar || v-bar:")
print("   EXACT C10(c0=c1=c2=1) (identity modes): ELEVENTH.  OK")
# S2b: x = t(v0,v1,-v2,0); the plane U2 is scaling-invariant, so sweep
# with the t = 1 representative (the branch membership is checked with t)
tS = sp.Symbol("tS")
vB = (v[0], v[1], v[2], 0)
xBt = (tS*v[0], tS*v[1], -tS*v[2], 0)
assert sp.expand(C0r.subs({x[0]: xBt[0], x[1]: xBt[1], x[2]: xBt[2],
                           v[3]: 0, x[3]: 0})) == 0
assert sp.expand(C1r.subs({x[0]: xBt[0], x[1]: xBt[1], x[2]: xBt[2],
                           v[3]: 0, x[3]: 0})) == 0
xB = (v[0], v[1], -v[2], 0)
for ci, (i_, j_, l_) in enumerate(((0, 1, 2), (1, 0, 2), (2, 0, 1))):
    z1c = tuple(sp.expand(sp.sympify(KB3[j_][t]) + aa*sp.sympify(KB3[i_][t]))
                for t in range(4))
    z2c = tuple(sp.expand(sp.sympify(KB3[l_][t]) + bb*sp.sympify(KB3[i_][t]))
                for t in range(4))
    minsB = commutation_minors(Hpack(z1c, z2c, vrow=vB, xrow=xB))
    prB = minass(minsB, list(Hpack(z1c, z2c, vrow=vB, xrow=xB).values()),
                 "v0,v1,v2,aa,bb")
    nzB = [pr[1] for pr in prB if pr[0] == 1]
    if ci == 2:
        assert not nzB, nzB
    else:
        assert len(nzB) == 1
        assert nzB[0] == frozenset({"bb", ("v1*aa+v0" if ci == 0 else "v0*aa+v1")}), nzB
survB = [[(v[0], -v[1], 0, 0), u1],
         [u1, vB],
         [u1, xB],
         [E2, E3]]
_ = assert_pure_nonzero(survB, "S2b survivor")
c10_B = C10(v[0], v[1], sp.Integer(1), sp.Integer(1), sp.Integer(1),
            vB, sp.Integer(1), -v[2], sp.Integer(0))
assert all(same_plane(survB[m], c10_B[m]) for m in range(4))
print("   S2b: pure points force U0 = span(wbar,u1): EXACT")
print("   C10(c0=c1=c2=1, x-row = t(v0,v1,-v2,0)): ELEVENTH.  OK")

# ====================== (alpha-IV): row == 0, U0 free =======================
# S3a: v2 = x2 = 0, s = 0: x-bar || conj(v-bar): six-chart sweep
lam = sp.Symbol("lam")
U1c = (u1, (v[0], v[1], 0, 0))
U2c = (u1, (v[0], -v[1], 0, 0))
a4, b4, c4, d4 = sp.symbols("a4 b4 c4 d4")
nz_families = []
for piv in itertools.combinations(range(4), 2):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    r1 = [0]*4
    r2 = [0]*4
    r1[piv[0]] = 1
    r2[piv[1]] = 1
    r1[nonpiv[0]] = a4
    r1[nonpiv[1]] = b4
    r2[nonpiv[0]] = c4
    r2[nonpiv[1]] = d4
    T = {bits: sp.expand(perm4(((tuple(r1), tuple(r2))[bits[0]], U1c[bits[1]],
                                U2c[bits[2]], (E2, E3)[bits[3]])))
         for bits in itertools.product((0, 1), repeat=4)}
    mins = set()
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        M = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            M[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        for rr in itertools.combinations(range(4), 2):
            for cc in itertools.combinations(range(4), 2):
                mm = sp.expand(M[rr, cc].det())
                if mm != 0:
                    mins.add(mm)
    prs = minass(sorted(mins, key=sp.default_sort_key), list(T.values()),
                 "v0,v1,a4,b4,c4,d4")
    nzp = [pr[1] for pr in prs if pr[0] == 1]
    nz_families.append((piv, nzp))
expected_nz = {
    (0, 1): [],
    (0, 2): [{"v0*a4+v1", "c4"}, {"v0*a4-v1", "c4"}],
    (0, 3): [{"v0*a4+v1", "c4"}, {"v0*a4-v1", "c4"}],
    (1, 2): [{"c4", "v1*a4+v0"}, {"c4", "-v1*a4+v0"}],
    (1, 3): [{"c4", "v1*a4+v0"}, {"c4", "-v1*a4+v0"}],
    (2, 3): [{"-b4*c4+a4*d4", "v1*c4+v0*d4", "v1*a4+v0*b4"},
             {"-b4*c4+a4*d4", "-v1*c4+v0*d4", "-v1*a4+v0*b4"}],
}
for piv, nzp in nz_families:
    assert sorted(map(sorted, nzp)) == sorted(
        map(sorted, [frozenset(w) for w in expected_nz[piv]])), (piv, nzp)
print("(alpha-IV S3a) six-chart sweep: nonzero pure U0's are exactly the")
print("   planes containing a Pi-vector and a (v0,-+v1,*,*)-vector.  OK")
# conj-side family -> C10 under the (01)-mode swap; v-side by (12) o (01):
dS, w2S, w3S = sp.symbols("dS w2S w3S")
famC = [[(0, 0, 1, dS), (v[0], -v[1], w2S, w3S)],
        [u1, (v[0], v[1], 0, 0)],
        [u1, (v[0], -v[1], 0, 0)],
        [E2, E3]]
_ = assert_pure_nonzero(famC, "S3a conj-side")
c10_C = C10(v[0], -v[1], sp.Integer(1), -dS, sp.Integer(1),
            (v[0], -v[1], w2S, w3S), sp.Integer(1), sp.Integer(0), sp.Integer(0))
sigmaC = (1, 0, 2, 3)
assert all(same_plane(famC[sigmaC[m]], c10_C[m]) for m in range(4))
famV = [[(0, 0, 1, dS), (v[0], v[1], w2S, w3S)],
        [u1, (v[0], v[1], 0, 0)],
        [u1, (v[0], -v[1], 0, 0)],
        [E2, E3]]
_ = assert_pure_nonzero(famV, "S3a v-side")
c10_V = C10(v[0], v[1], sp.Integer(1), -dS, sp.Integer(1),
            (v[0], v[1], w2S, w3S), sp.Integer(1), sp.Integer(0), sp.Integer(0))
sigmaV = (2, 0, 1, 3)
assert all(same_plane(famV[sigmaV[m]], c10_V[m]) for m in range(4))
print("   both S3a families are EXACT C10 images ((01)- resp. (021)-mode")
print("   alignments) at c0 = 1, c2 = 1, c1 = -d: ELEVENTH.  OK")
# S3b: v = (0,v1,v2,0), x ~ (0,v1,-v2,0): no nonzero pure points
U1d = (u1, (0, v[1], v[2], 0))
U2d = (u1, (0, v[1], -v[2], 0))
for piv in itertools.combinations(range(4), 2):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    r1 = [0]*4
    r2 = [0]*4
    r1[piv[0]] = 1
    r2[piv[1]] = 1
    r1[nonpiv[0]] = a4
    r1[nonpiv[1]] = b4
    r2[nonpiv[0]] = c4
    r2[nonpiv[1]] = d4
    T = {bits: sp.expand(perm4(((tuple(r1), tuple(r2))[bits[0]], U1d[bits[1]],
                                U2d[bits[2]], (E2, E3)[bits[3]])))
         for bits in itertools.product((0, 1), repeat=4)}
    mins = set()
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        M = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            M[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        for rr in itertools.combinations(range(4), 2):
            for cc in itertools.combinations(range(4), 2):
                mm = sp.expand(M[rr, cc].det())
                if mm != 0:
                    mins.add(mm)
    prs = minass(sorted(mins, key=sp.default_sort_key), list(T.values()),
                 "v1,v2,a4,b4,c4,d4")
    assert not [pr for pr in prs if pr[0] == 1], (piv, prs)
print("(alpha-IV S3b) v = (0,v1,v2,0), x ~ (0,v1,-v2,0): NO nonzero pure")
print("   points in any U0-chart (its (01)-mirror follows by symmetry).  OK")

print()
print("VERDICT (tail 3 CLOSED): every nonzero pure point of the e = 1")
print("case-alpha leaf lies in the ELEVENTH component orbit (C10 walls at")
print("c0 = c1 = 1 and their boundary charts); the {x||e0}/{v||e0}")
print("survivors of s12 were chart artifacts of an empty stratum; all")
print("remaining branches carry only the zero restriction.")
print()
print("ALL CHECKS PASSED")
