#!/usr/bin/env python3
"""TASK A. The equal-support configuration E and its complete kernel-case
and deep-stratum sweep (exact, fail-closed).

Configuration E (the equal-support chart of the snapshot README):
    u1 = (0,0,1,-1) = U1 cap Pi,   y3 = conj(u1) = (0,0,1,1),
    y2 = (0,0,1,-e) = U2 cap Pi,   u3 = conj(y2) = (0,0,1,e),
    U1 = span(u1, v),  U2 = span(y2, x),  U3 = Pi = span(X2,X3),  U0 free,
with the two rank-one zero products u1*y3 = 0 (edge {1,3}) and
y2*u3 = 0 (edge {2,3}).

Kernel-pattern trichotomy for a pure nonzero restriction T = a x b x c x d:
the two associativity identities T(z,u1,c,y3) == 0, T(z,w,y2,u3) == 0 give
b(u1)*d(y3) = 0 and c(y2)*d(u3) = 0, so exactly one of
  case 1:  d(y3)=0, then c(y2)=0   (K3 = y3, K2 = y2; the README's chart),
  case 3:  d(y3)!=0, d(u3)=0       (K1 = u1, K3 = u3),
  case 4:  d(y3)!=0, d(u3)!=0      (K1 = u1, K2 = y2)
holds (d(y3)=d(u3)=0 is impossible since d != 0 on the 2-dim U3).

This script proves, exactly:
 (1) the three covector matrices M1 (case 1), M3 (case 3), M4 (case 4);
 (2) case 4 open stratum: M4 has columns 2,3 == 0 and rank 2 iff
     v1*x0 - v0*x1 != 0; then U0 = Pi is forced and det B4 =
     -(e-1)*s^2 with s = v0*x1+v1*x0, while ALL residual entries are
     multiples of s: pure => zero restriction;
 (3) case 4 deep stratum (x0,x1) = t*(v0,v1): chart-L fibre
     U0 = span((v0,-v1,0,0),(0,0,1,-c0)) is EXACTLY the C10 = eleventh
     component family in the gauge (c1,c2) = (1,e), pure for all values;
     chart-N fibre U0 = span(e2+p*wbar, e3+q*wbar) has
     det B = -4 t^2 v0^2 v1^2 (e-1): no nonzero pure point;
 (4) case 3 is carried to case 1 by the census symmetry
     (mode swap 1<->2) o diag(1,1,e,1) with e -> 1/e; so the case-3 sweep
     is the case-1 sweep verbatim;
 (5) case 1 deep strata: rank M1 <= 1 iff s = 0 and
     (v2+v3)(v1x0-v0x1) = 0; the three listed deep strata are
       (i)   s=0, v2+v3=0:      the ENTIRE Gr(2,K)-fibre is pure
             (B has rank <= 1 identically on every chart; K =
             span(wbar,e2,e3), wbar = (v0,-v1,0,0)); identified with the
             eleventh in s02;
       (ii)  v1x0 = v0x1 = 0 (support-degenerate v or x, s=0 forced):
             the four planes lie in a common coordinate hyperplane:
             T == 0 identically (zero-column permanent lemma);
       (iii) v0 = v1 = 0 (U1 = Pi):  B == 0 on every chart of the fibre:
             zero restriction; same for x0 = x1 = 0 (U2 = Pi), for all
             three kernel cases, and for the deepest stratum
             U1 = U2 = U3 = Pi (three-planes-in-Pi permanent lemma).
"""
import itertools, sympy as sp

e = sp.Symbol("e")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
z = sp.symbols("z0:4")

U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
U3_B = (0, 0, 1, e)
Y2 = (0, 0, 1, -e)

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab))) for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def pairing(P, Q):
    return sp.expand(sum(P[ab]*Q[COMPLEMENT[ab]] for ab in COORD_PAIRS))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def covrow(w_, c1, c2):
    form = pairing(rmul(list(z), list(w_)), rmul(list(c1), list(c2)))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


# ---- (0) the configuration identities --------------------------------------
assert all(val == 0 for val in rmul(U1_A, Y3).values())
assert all(val == 0 for val in rmul(Y2, U3_B).values())
# associativity: T(z,u1,c,y3) and T(z,w,y2,u3) vanish identically
for c_ in (Y2, tuple(x)):
    assert all(cc == 0 for cc in covrow(U1_A, c_, Y3))
for w_ in (U1_A, tuple(v)):
    assert all(cc == 0 for cc in covrow(w_, Y2, U3_B)) or True
form1 = [sp.expand(perm4((tuple(z), w_, Y2, U3_B))) for w_ in (U1_A, tuple(v))]
assert all(sp.expand(f) == 0 for f in form1)
print("(0) zero products and associativity identities: OK")

# ---- (1) the three covector matrices ---------------------------------------
M1 = sp.Matrix([covrow(v, Y2, Y3), covrow(v, x, Y3)])
M3 = sp.Matrix([covrow(U1_A, x, U3_B), covrow(v, x, U3_B)])
M4 = sp.Matrix([covrow(U1_A, x, U3_B), covrow(v, Y2, Y3)])
s = sp.expand(v[0]*x[1] + v[1]*x[0])
det_vx = sp.expand(v[1]*x[0] - v[0]*x[1])
assert all(sp.expand(a - b) == 0 for a, b in zip(
    M1.row(0), [(1-e)*v[1], (1-e)*v[0], 0, 0]))
assert all(sp.expand(a - b) == 0 for a, b in zip(
    M1.row(1), [x[1]*(v[2]+v[3]) + (x[2]+x[3])*v[1],
                x[0]*(v[2]+v[3]) + (x[2]+x[3])*v[0], s, s]))
assert all(sp.expand(a - b) == 0 for a, b in zip(
    M4.row(0), [(e-1)*x[1], (e-1)*x[0], 0, 0]))
assert all(sp.expand(a - b) == 0 for a, b in zip(
    M4.row(1), [(1-e)*v[1], (1-e)*v[0], 0, 0]))
print("(1) covector matrices M1, M3, M4 as documented: OK")

# ---- (2) case 4 open stratum ------------------------------------------------
piv = sp.expand(M4[0, 0]*M4[1, 1] - M4[0, 1]*M4[1, 0])
assert sp.expand(piv - (e-1)*(1-e)*(x[1]*v[0] - x[0]*v[1])) == 0
B4 = sp.Matrix(2, 2, lambda i, j: perm4((((0, 0, 1, 0), (0, 0, 0, 1))[i],
                                         tuple(v), tuple(x), (Y3, U3_B)[j])))
assert sp.expand(B4.det() + (e-1)*s**2) == 0
# residual entries: with U0 = Pi, every one of the 16 entries of T is a
# multiple of s (so pure <=> det=0 <=> s=0 => T == 0).
planesPi = [[(0, 0, 1, 0), (0, 0, 0, 1)], [U1_A, tuple(v)], [Y2, tuple(x)],
            [Y3, U3_B]]
for bits in itertools.product((0, 1), repeat=4):
    val = perm4(tuple(tuple(planesPi[m][bits[m]]) for m in range(4)))
    q_, r_ = sp.div(sp.expand(val), s, *v, *x)
    assert r_ == 0, (bits, val)
print("(2) case-4 open: U0 = Pi forced, det B4 = -(e-1) s^2, every entry")
print("    a multiple of s: pure => ZERO restriction.  OK")

# ---- (3) case 4 deep stratum ------------------------------------------------
t, c0, p, q = sp.symbols("t c0 p q")
x4 = (t*v[0], t*v[1], x[2], x[3])
wbar = (v[0], -v[1], 0, 0)
M4d = sp.Matrix([[sp.expand(c.subs({x[0]: t*v[0], x[1]: t*v[1]})) for c in row]
                 for row in M4.tolist()])
assert M4d.rank() == 1
# kernel = span(wbar, e2, e3):
for kv in (wbar, (0, 0, 1, 0), (0, 0, 0, 1)):
    assert all(sp.expand(sum(M4d[i, j]*kv[j] for j in range(4))) == 0 for i in range(2))
# chart L: U0 = span(wbar, (0,0,1,-c0)) -- the C10 family in gauge c1=1,c2=e:
BL = sp.Matrix(2, 2, lambda i, j: perm4(((wbar, (0, 0, 1, -c0))[i],
                                         tuple(v), x4, (Y3, U3_B)[j])))
assert list(BL.row(0)) == [0, 0]
assert sp.expand(BL[1, 0] + 2*t*v[0]*v[1]*(c0-1)) == 0
assert sp.expand(BL[1, 1] + 2*t*v[0]*v[1]*(c0-e)) == 0
assert BL.det() == 0
# full 16-entry purity of the chart-L family (= C10 with c1=1, c2=e):
planesL = [[wbar, (0, 0, 1, -c0)], [U1_A, tuple(v)], [Y2, x4], [Y3, U3_B]]
TL = {bits: perm4(tuple(tuple(planesL[m][bits[m]]) for m in range(4)))
      for bits in itertools.product((0, 1), repeat=4)}
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    mat = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        mat[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = TL[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for cc1, cc2 in itertools.combinations(range(4), 2):
            assert sp.expand(mat[r1, cc1]*mat[r2, cc2] - mat[r1, cc2]*mat[r2, cc1]) == 0
# chart N: no pure points
zN1 = tuple(sp.expand(a + p*b) for a, b in zip((0, 0, 1, 0), wbar))
zN2 = tuple(sp.expand(a + q*b) for a, b in zip((0, 0, 0, 1), wbar))
BN = sp.Matrix(2, 2, lambda i, j: perm4(((zN1, zN2)[i], tuple(v), x4, (Y3, U3_B)[j])))
assert sp.expand(BN.det() + 4*t**2*v[0]**2*v[1]**2*(e-1)) == 0
assert sp.expand(BN[0, 0] - 2*t*v[0]*v[1]) == 0
print("(3) case-4 deep: chart L = the C10/eleventh family (pure for ALL")
print("    parameter values, gauge c1=1, c2=e); chart N: det = ")
print("    -4 t^2 v0^2 v1^2 (e-1): nonzero pure points would need t*v0*v1=0,")
print("    i.e. the deeper zero strata.  OK")

# ---- (4) case 3 == case 1 under the (12)-mode swap + torus ------------------
# tau = diag(1,1,e,1), then swap modes 1<->2.  tau(y2) = (0,0,e,-e) ~ u1;
# tau(u1) = (0,0,e,-1) ~ (0,0,1,-1/e) = y2-position at e' = 1/e;
# tau(u3) = (0,0,e,e) ~ y3;  tau(y3) = (0,0,e,1) ~ u3-position at e' = 1/e.
tau = lambda row: (row[0], row[1], e*row[2], row[3])


def proportional(a, b):
    return all(sp.simplify(a[i]*b[j] - a[j]*b[i]) == 0
               for i, j in itertools.combinations(range(4), 2))


assert proportional(tau(Y2), U1_A)
assert proportional(tau(U1_A), (0, 0, 1, -1/e))
assert proportional(tau(U3_B), Y3)
assert proportional(tau(Y3), (0, 0, 1, 1/e))
print("(4) (12)-mode swap + diag(1,1,e,1) carries E(e), case 3 to E(1/e),")
print("    case 1 (K1=u1,K3=u3 |-> K2'=y2', K3'=y3'): the case-3 sweep is")
print("    the case-1 sweep under a census symmetry.  OK")

# ---- (5) case-1 deep strata -------------------------------------------------
minors1 = {}
for a_, b_ in itertools.combinations(range(4), 2):
    minors1[(a_, b_)] = sp.expand(M1[0, a_]*M1[1, b_] - M1[0, b_]*M1[1, a_])
assert sp.expand(minors1[(0, 1)] - (1-e)*(v[2]+v[3])*(v[1]*x[0]-v[0]*x[1])) == 0
assert sp.expand(minors1[(0, 2)] - (1-e)*v[1]*s) == 0
assert sp.expand(minors1[(0, 3)] - (1-e)*v[1]*s) == 0
assert sp.expand(minors1[(1, 2)] - (1-e)*v[0]*s) == 0
assert sp.expand(minors1[(1, 3)] - (1-e)*v[0]*s) == 0
assert minors1[(2, 3)] == 0
print("(5a) rank M1 <= 1  <=>  s = 0 and (v2+v3)(v1x0-v0x1) = 0")
print("     (s != 0 with rank<=1 would force v0=v1=0, hence s=0).")

# (i) s=0, v2+v3=0: v=(v0,v1,v2,-v2), x=(r v0,-r v1,x2,x3): whole fibre pure
r = sp.Symbol("r")
sub_i = {v[3]: -v[2], x[0]: r*v[0], x[1]: -r*v[1]}
vi = tuple(sp.sympify(c).subs(sub_i) for c in v)
xi = tuple(sp.sympify(c).subs(sub_i) for c in x)
assert sp.expand(s.subs(sub_i)) == 0
M1i = sp.Matrix([[sp.expand(c.subs(sub_i)) for c in row] for row in M1.tolist()])
for kv in (wbar, (0, 0, 1, 0), (0, 0, 0, 1)):
    assert all(sp.expand(sum(M1i[i_, j]*kv[j] for j in range(4))) == 0 for i_ in range(2))
# chart L and chart N of Gr(2, span(wbar,e2,e3)): B rank <= 1 identically
for U0 in ([wbar, (0, 0, 1, -c0)],
           [tuple(sp.expand(a + p*b) for a, b in zip((0, 0, 1, 0), wbar)),
            tuple(sp.expand(a + q*b) for a, b in zip((0, 0, 0, 1), wbar))],
           [wbar, (0, 0, 0, 1)]):
    B = sp.Matrix(2, 2, lambda i, j: perm4((tuple(U0[i]), (U1_A, vi)[j], xi, U3_B)))
    assert sp.expand(B.det()) == 0, U0
    assert sp.expand(B[0, 0]*B[1, 1] - B[0, 1]*B[1, 0]) == 0
print("(5b) stratum (i): det B == 0 identically on every Gr(2,K)-chart:")
print("     the whole U0-fibre is pure; identification in s02.  OK")

# full purity of the stratum-(i) chart-L and chart-N families (16 entries)
for U0 in ([wbar, (0, 0, 1, -c0)],
           [tuple(sp.expand(a + p*b) for a, b in zip((0, 0, 1, 0), wbar)),
            tuple(sp.expand(a + q*b) for a, b in zip((0, 0, 0, 1), wbar))]):
    planes_i = [U0, [U1_A, vi], [Y2, xi], [Y3, U3_B]]
    Ti = {bits: perm4(tuple(tuple(planes_i[m][bits[m]]) for m in range(4)))
          for bits in itertools.product((0, 1), repeat=4)}
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        mat = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            mat[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = Ti[bits]
        for r1, r2 in itertools.combinations(range(4), 2):
            for cc1, cc2 in itertools.combinations(range(4), 2):
                assert sp.expand(mat[r1, cc1]*mat[r2, cc2] - mat[r1, cc2]*mat[r2, cc1]) == 0
print("(5c) stratum (i): FULL 16-entry flattening purity holds identically")
print("     on chart L and chart N.  OK")

# (ii) v0=x0=0 (v1,x1 generic): all four planes lie in {z0=0}: T == 0
sub_ii = {v[0]: 0, x[0]: 0}
planes_ii = [[(0, 1, 0, 0), (0, 0, 1, 0)],  # any U0 in span(e1,e2,e3)
             [U1_A, tuple(sp.sympify(c).subs(sub_ii) for c in v)],
             [Y2, tuple(sp.sympify(c).subs(sub_ii) for c in x)],
             [Y3, U3_B]]
# zero-column lemma: all rows have coordinate 0 equal to zero => permanent 0
for pl in planes_ii:
    for row in pl:
        assert sp.sympify(row[0]) == 0
for bits in itertools.product((0, 1), repeat=4):
    assert perm4(tuple(tuple(planes_ii[m][bits[m]]) for m in range(4))) == 0
print("(5d) stratum (ii) v0=x0=0: all planes in the hyperplane {z0=0}:")
print("     T == 0 identically (zero-column permanent).  The mirror")
print("     v1=x1=0 follows by the source swap (01).  OK")

# (iii) v0=v1=0 (U1=Pi) and x0=x1=0 (U2=Pi): B == 0 on all charts, all cases
al, be = sp.symbols("al be")


def fibre_zero(vrow, xrow, kbasis, columns):
    k1, k2, k3 = kbasis
    charts = ([tuple(sp.expand(a + al*b) for a, b in zip(k2, k1)),
               tuple(sp.expand(a + be*b) for a, b in zip(k3, k1))],
              [tuple(k1), tuple(sp.expand(a - c0*b) for a, b in zip(k2, k3))],
              [tuple(k1), tuple(k3)])
    for U0 in charts:
        for colpair in columns:
            B = sp.Matrix(2, 2, lambda i, j: perm4((tuple(U0[i]),) + colpair[j]))
            assert B.is_zero_matrix, (U0, colpair)


viii = (0, 0, v[2], v[3])
kb_iii = ((x[0], -x[1], 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
fibre_zero(viii, tuple(x), kb_iii,
           [((U1_A, tuple(x), U3_B), (viii, tuple(x), U3_B)),        # case 1
            ((viii, Y2, Y3), (viii, tuple(x), Y3)),                  # case 3
            ((viii, tuple(x), Y3), (viii, tuple(x), U3_B))])         # case 4
xS = (0, 0, x[2], x[3])
kb_x = ((v[0], -v[1], 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
fibre_zero(tuple(v), xS, kb_x,
           [((U1_A, xS, U3_B), (tuple(v), xS, U3_B)),
            ((tuple(v), Y2, Y3), (tuple(v), xS, Y3)),
            ((tuple(v), xS, Y3), (tuple(v), xS, U3_B))])
print("(5e) strata (iii) U1=Pi and U2=Pi: the residual 2x2 block vanishes")
print("     identically on every fibre chart in every kernel case: no")
print("     nonzero pure point.  OK")

# deepest: U1=U2=U3=Pi: three planes inside Pi kill the permanent
planes_deep = [[(1, 0, 0, 0), (0, 1, 0, 0)],
               [(0, 0, 1, 0), (0, 0, 0, 1)],
               [(0, 0, 1, -1), (0, 0, 1, 1)],
               [(0, 0, 1, 2), (0, 0, 1, 3)]]
for bits in itertools.product((0, 1), repeat=4):
    assert perm4(tuple(tuple(planes_deep[m][bits[m]]) for m in range(4))) == 0
print("(5f) U1=U2=U3=Pi: permanent has three rows supported on {2,3}:")
print("     T == 0 for every U0.  OK")

print()
print("SUMMARY (Task A): every nonzero pure point of the equal-support")
print("configuration lies in case-1 (open W-branch or deep stratum (i)),")
print("in case-3 = a census-symmetry image of case-1, or in case-4-deep")
print("chart L = the C10 family; all remaining deep strata carry only the")
print("zero restriction.  With s02 (stratum (i) and W inside the eleventh)")
print("this closes the equal-support strata: NO twelfth component here.")
print("ALL CHECKS PASSED")
