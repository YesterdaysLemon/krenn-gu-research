#!/usr/bin/env python3
"""TASK B. The case-Z rank-2 branch families of the coincident-support
chart: derivation, samples, exact purity and invariants.

On each rank-2 stratum of M_Z, U0 = ker M_Z is forced (u3 in U0 always)
and purity is det B_Z = 0.  The strata and their branch equations:

 (Z-a) p_Pi || q_Pi (gauge p=(0,1,b,-bk), q=(0,1,e,-ek)), w=(0,W,w2,w3):
     det B_Z ~ (k w2+w3) * ((b+e)(k w2-w3) - 2Wbek) * ((b+e)(k w2-w3)+2Wbek)
     giving branches Za1 (w3 = -k w2), Za2, Za3;
 (Z-b) w in Pi (gauge w=(0,0,1,kp)), p,q free: U0 = span(u3,(0,0,1,-kp))
     forced, det B_Z ~ (kp(p2+q2)+(p3+q3)) * (kp(p2+q2)-(p3+q3)):
     branches Zb1, Zb2;
 (Z-c) w3 = 0 (gauge w=(0,W,w2,0)), p,q free: det B_Z ~
     ((p2q3+p3q2)W + (p3+q3)w2) * (-(p2q3+p3q2)W + (p3+q3)w2):
     branches Zc1, Zc2  (the w2=0 mirror is the coordinate swap 2<->3).

For each branch: an exact rational sample, the FULL 16-entry restriction,
fail-closed purity, pair profile, kernels, relation table, triple-span
dimensions and coordinate-plane incidences."""
import itertools, sympy as sp

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


def MZ_of(p, q, w):
    return sp.Matrix([covrow((YBAR, YBAR, tuple(w))),
                      covrow((YBAR, tuple(q), tuple(w))),
                      covrow((tuple(p), YBAR, tuple(w)))])


def proportional(u, w):
    return all(sp.simplify(u[i]*w[j] - u[j]*w[i]) == 0
               for i, j in itertools.combinations(range(4), 2))


def analyse(planes, label):
    planes = [[tuple(sp.nsimplify(c) for c in row) for row in pl] for pl in planes]
    for pl in planes:
        assert sp.Matrix([list(pl[0]), list(pl[1])]).rank() == 2, (label, "degenerate")
    T = {bits: perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
         for bits in itertools.product((0, 1), repeat=4)}
    assert any(val != 0 for val in T.values()), (label, "zero")
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            m[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        assert m.rank() == 1, (label, left, right)
    kerns = []
    for mode in range(4):
        mat = sp.zeros(2, 8)
        for bits in itertools.product((0, 1), repeat=4):
            rest = tuple(bits[j] for j in range(4) if j != mode)
            mat[bits[mode], rest[0]*4 + rest[1]*2 + rest[2]] = T[bits]
        l = sp.Matrix(mat.T).nullspace()[0]
        kerns.append(tuple(sp.expand(l[0]*planes[mode][0][j] + l[1]*planes[mode][1][j])
                           for j in range(4)))
    profile = []
    rels = []
    for a_, b_ in COORD_PAIRS:
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        r = mm.rank()
        profile.append(r)
        if r == 3:
            kv = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
            M2 = sp.Matrix([[kv[0], kv[1]], [kv[2], kv[3]]])
            rels.append(((a_, b_), M2.rank()))
        elif r == 2:
            rels.append(((a_, b_), "rank-2 edge"))
    tri = {t_: sp.Matrix([list(planes[m][0]) for m in t_]
                         + [list(planes[m][1]) for m in t_]).rank()
           for t_ in itertools.combinations(range(4), 3)}
    inc = {}
    for mode in range(4):
        hits = []
        for pair in COORD_PAIRS:
            comp = tuple(i for i in range(4) if i not in pair)
            Mm = sp.Matrix([[planes[mode][r_][c] for c in comp] for r_ in range(2)])
            if Mm.rank() <= 1:
                hits.append(pair)
        inc[mode] = tuple(hits)
    return {"profile": tuple(profile), "kernels": kerns, "rels": tuple(rels),
            "tri": tri, "inc": inc, "T": T}


def kernel_plane_exact(p, q, w):
    M = MZ_of(p, q, w)
    ns = M.nullspace()
    assert len(ns) == 2, "not rank 2"
    U0 = []
    for vec in ns:
        vec = [sp.nsimplify(sp.cancel(c)) for c in vec]
        den = sp.lcm([sp.denom(c) for c in vec])
        U0.append(tuple(c*den for c in vec))
    return U0


b, e, k, W, w2, w3, p2, p3, q2, q3, kp = sp.symbols("b e k W w2 w3 p2 p3 q2 q3 kp")

# symbolic branch equations
pZ = (0, 1, b, -b*k)
qZ = (0, 1, e, -e*k)
wZ = (0, W, w2, w3)
MZa = MZ_of(pZ, qZ, wZ)
assert MZa.rank() == 2
# kernel = span(u3, zeta) with zeta from the (z1=0)-chart:
a_, c_, d_ = sp.symbols("kz0 kz2 kz3")
zz = sp.Matrix([a_, 0, c_, d_])
sol = sp.solve([sp.expand((MZa[i, :]*zz)[0, 0]) for i in range(3)], [a_, c_], dict=True)
zeta = [sp.expand(sp.cancel(sp.together(sp.sympify(cc).subs(sol[0])).subs(d_, 1)))
        for cc in (a_, 0, c_, d_)]
# zeta = (-W(k w2+w3), 0, -w2(k w2-w3), w3(k w2-w3)) / w3(k w2 - w3)-scale;
# clear the common content:
den = sp.lcm([sp.denom(cc) for cc in zeta])
zeta = [sp.expand(sp.cancel(cc*den)) for cc in zeta]
BZa = sp.Matrix(2, 2, lambda i, j: perm4(((U3v, tuple(zeta))[i], pZ, qZ, (U3v, wZ)[j])))
target = sp.expand((k*w2 + w3)*((b+e)*(k*w2-w3) - 2*W*b*e*k)
                   * ((b+e)*(k*w2-w3) + 2*W*b*e*k))
ratio = sp.cancel(sp.expand(BZa.det())/target)
num, denr = sp.fraction(sp.together(ratio))
# the only denominator allowed is a product of the chart-pivot factors
# w3, (k w2 - w3) (nonzero on the (Z-a) chart) and a constant:
rem = sp.cancel(denr/sp.gcd(denr, sp.expand((w3*(k*w2 - w3))**3)))
assert num.is_number and num != 0 and rem.is_number, (num, denr)
print("(Z-a) det B_Z ~ (k w2+w3) * ((b+e)(k w2-w3)-2Wbek)")
print("      * ((b+e)(k w2-w3)+2Wbek)  (up to chart-pivot factors")
print("      w3, k w2-w3 nonzero on the chart): branches Za1, Za3, Za2.  OK")

MZb = MZ_of((0, 1, p2, p3), (0, 1, q2, q3), (0, 0, 1, kp))
nsb = MZb.nullspace()
U0b = [tuple(sp.expand(c*sp.lcm([sp.denom(sp.cancel(cc)) for cc in vec]))
             for c in [sp.cancel(cc) for cc in vec]) for vec in nsb]
BZb = sp.Matrix(2, 2, lambda i, j: perm4((tuple(U0b[i]), (0, 1, p2, p3),
                                          (0, 1, q2, q3), (U3v, (0, 0, 1, kp))[j])))
detZb = sp.factor(sp.expand(BZb.det()))
tb = sp.expand((kp*(p2+q2) + (p3+q3))*(kp*(p2+q2) - (p3+q3)))
rb = sp.cancel(sp.expand(BZb.det())/tb)
assert sp.simplify(rb + 1/kp) == 0 or sp.simplify(rb - 1/kp) == 0 or rb.is_number
print("(Z-b) U0 = span(u3, (0,0,1,-kp)) forced; det B_Z ~")
print("      (kp(p2+q2)+(p3+q3)) * (kp(p2+q2)-(p3+q3)).  OK")

MZc = MZ_of((0, 1, p2, p3), (0, 1, q2, q3), (0, W, w2, 0))
nsc = MZc.nullspace()
U0c = [tuple(sp.expand(c*sp.lcm([sp.denom(sp.cancel(cc)) for cc in vec]))
             for c in [sp.cancel(cc) for cc in vec]) for vec in nsc]
BZc = sp.Matrix(2, 2, lambda i, j: perm4((tuple(U0c[i]), (0, 1, p2, p3),
                                          (0, 1, q2, q3), (U3v, (0, W, w2, 0))[j])))
detZc = sp.expand(BZc.det())
tc = sp.expand(((p2*q3+p3*q2)*W + (p3+q3)*w2)*(-(p2*q3+p3*q2)*W + (p3+q3)*w2))
rc = sp.cancel(detZc/tc)
numc, denc = sp.fraction(sp.together(rc))
remc = sp.cancel(denc/sp.gcd(denc, sp.expand(w2**4)))
assert numc.is_number and numc != 0 and remc.is_number, (numc, denc)
print("(Z-c) det B_Z ~ ((p2q3+p3q2)W + (p3+q3)w2) * (-(p2q3+p3q2)W + (p3+q3)w2).  OK")

# ---------------- samples ---------------------------------------------------
samples = {
    "Za1": ((0, 1, 2, -10), (0, 1, 3, -15), (0, 7, 1, -5),
            (3, 3, 4, 3, 3, 3)),
    "Za2": ((0, 1, 2, -10), (0, 1, 3, -15), (0, sp.Rational(1, 6), 1, 7),
            (3, 3, 4, 3, 3, 3)),
    "Za3": ((0, 1, 2, -10), (0, 1, 3, -15), (0, sp.Rational(-1, 6), 1, 7),
            (3, 3, 4, 3, 3, 3)),
    "Zb1": ((0, 1, 3, -1), (0, 1, 5, -15), (0, 0, 1, 2),
            (3, 3, 3, 4, 3, 3)),
    "Zb2": ((0, 1, 3, -1), (0, 1, 5, 17), (0, 0, 1, 2),
            (3, 3, 3, 4, 3, 3)),
    "Zc1": ((0, 1, 2, 3), (0, 1, 5, 7), (0, sp.Rational(-10, 29), 1, 0),
            (3, 3, 2, 4, 3, 3)),
    "Zc2": ((0, 1, 2, 3), (0, 1, 5, 7), (0, sp.Rational(10, 29), 1, 0),
            (3, 3, 2, 4, 3, 3)),
}
# branch-equation membership checks
bv, ev, kv = 2, 3, 5
assert samples["Za1"][2][3] == -kv*samples["Za1"][2][2]
Wa = sp.Rational(-(bv+ev)*(kv*1 - 7), 2*bv*ev*kv)
assert samples["Za2"][2][1] == Wa and samples["Za3"][2][1] == -Wa
assert 2*(3+5) + (-1-15) == 0          # Zb1: kp(p2+q2)+(p3+q3)=0
assert 2*(3+5) - (-1+17) == 0          # Zb2
assert sp.Rational(-10, 29)*(2*7+3*5) + (3+7)*1 == 0   # Zc1
for name, (p_, q_, w_, prof) in samples.items():
    U0 = kernel_plane_exact(p_, q_, w_)
    planes = [U0, [YBAR, p_], [YBAR, q_], [U3v, w_]]
    pkg = analyse(planes, name)
    assert pkg["profile"] == prof, (name, pkg["profile"])
    assert proportional(pkg["kernels"][1], YBAR) and proportional(pkg["kernels"][2], YBAR)
    print(f"[{name}] pure OK; profile {prof} (sum {sum(prof)});")
    print(f"   U0 = {U0}")
    print(f"   kernels K0 = {pkg['kernels'][0]}, K3 = {pkg['kernels'][3]}  (K1 = K2 = ybar)")
    print(f"   rank-3 relation coefficient ranks: {pkg['rels']}")
    print(f"   triple spans: {pkg['tri']}")
    print(f"   coordinate-plane incidences per mode: {pkg['inc']}")
print()
print("Branch invariant headlines: Za* profile (3,3,4,3,3,3), Zb* profile")
print("(3,3,3,4,3,3), Zc* profile (3,3,2,4,3,3) (a rank-2 pair edge at {0,3});")
print("all have K1 = K2 = ybar and rank sums 19/19/18 < 20,21.")
print("ALL CHECKS PASSED")
