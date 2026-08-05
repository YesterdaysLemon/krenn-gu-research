#!/usr/bin/env python3
"""THREE NEW PURE-COMPRESSION COMPONENTS from the case-Y survivor walls
(tail 2 of the census-thirteen sweep): the census lower bound moves from
THIRTEEN to SIXTEEN.

Setting (s09): the coincident-support (b2)-chart, case Y (K3 = u3):
    ybar = (1,-1,0,0), u3 = (1,1,0,0),
    U1 = span(ybar, p),  p = (0,1,p2,p3),   U2 = span(ybar, q),
    q = (0,1,q2,q3),     U3 = span(u3, w),  w = (0,wv1,wv2,wv3),
    U0 in Gr(2, ker Y1), Y1 = (P, P, p3+q3, p2+q2), P = p2 q3 + p3 q2,
    U0 = span(kA + aY ybar, kB + bY ybar) on the (aY,bY)-chart,
    kA = (p3+q3, 0, -P, 0), kB = (p2+q2, 0, 0, -P).
The minAssGTZ stratification of the residual 2x2x2 purity system has 35
primes (s09); this sweep's pipeline (w04) shows exactly SEVEN of its
nonzero-restriction primes -- #11, #12, #13, #15, #16, #26, #28 -- pass
the calibrated semicontinuity sieve against NO census image of any of
the thirteen certified components.  They form THREE orbit classes under
the chart symmetries [(12): p <-> q; (23): source swap 2 <-> 3 with
aY <-> bY; (01): source swap 0 <-> 1 with aY -> -(p3+q3)-aY,
bY -> -(p2+q2)-bY, wv1 -> -wv1]:

  class A = {#11, #12, #26, #28},  class B = {#15, #16},  class C = {#13}.

NORMAL FORMS (this script, all exact):

  F_A(p2, p3, lam, al; wv1):   q = (0, 1, lam*p2, lam*p3)  [q_Pi || p_Pi],
      aY = al*p3,  bY = be*p2 with  al + be + lam = 0,
      w = (0, wv1, 2*wv1*be*p2/(1+lam), 2*wv1*aY.../(1+lam))
        ~ (0, 1+lam, 2*be*p2, 2*al*p3);
  F_B(p2, p3, q2, q3):  wv1 = 0 (w in Pi) and the rational solve
      aY = (q3*(p2*p3+p3*q2+p2*q3) - p3*q2*q3)/(q2*p3 - q3*p2),
      bY = (p2*q2*q3 - q2*(p2*p3+p3*q2+p2*q3))/(q2*p3 - q3*p2),
      (wv2 : wv3) = (bY : p3+q3+aY);
  F_C(c, d, m, tau, wv2, W1):  p = (0,1,c,c*m), q = (0,1,d,d*m),
      w = (0, W1, wv2, wv2*m)  [p_Pi || q_Pi || w_Pi], aY = m*tau,
      bY = tau, subject to the CONIC
      Q = W1^2 c^2 d^2 + W1 c d wv2 (c + d + 2 tau)
          + wv2^2 (c d + 4 tau (c+d) + 4 tau^2) = 0.

CERTIFICATES:
  * each family is identically pure and generically nonzero (exact);
  * family tangent rank 5 at exact rational samples (with the full
    projective source torus);
  * classes A and B: the universal Segre-incidence Jacobian has rank
    FIFTEEN at the samples -- smooth five-dimensional points of the
    pure locus (the first/ninth-component certificate pattern): the
    closure of each (irreducible) family is an irreducible COMPONENT;
  * class C: incidence rank 14 (singular) and the char-0 FIVE-slice
    `ds` standard basis of the 28 mode-anchor flattening minors has
    local dimension ZERO: local dimension exactly 5 => COMPONENT
    (the twelfth/thirteenth certificate pattern, with the w02 minor
    system);
  * distinctness from the THIRTEEN census orbits: the calibrated sieve
    passes NO alignment for any of the three samples;
  * mutual distinctness: B vs A and B vs C by the sieve (no alignment
    in either direction); A vs C by a closed kernel-support invariant:
    on all of closure(F_C) at least TWO mode kernels lie in coordinate
    2-planes (K3 = u3 and K0 in Pi identically -- proved mod the conic),
    while the class-A sample has kernel supports {3,3,4,2} (exactly ONE
    in a coordinate 2-plane);
  * class C irreducibility: the conic's W1-discriminant
    c^2 d^2 [(c-d)^2 - 12 tau (c+d) - 12 tau^2] is not a square in the
    parameter function field (the bracket is squarefree in tau), so Q
    is irreducible.

VERDICT: FOURTEENTH (class A), FIFTEENTH (class B), SIXTEENTH (class C)
pure-compression component orbits.  All three have K1 = span(p) and
K3 = u3 identically; profiles at the samples: A (4,4,4,3,3,3) sum 21,
B (4,4,3,4,3,3) sum 21, C (4,4,4,3,3,3) sum 21."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def proportional(u, w):
    return all(sp.simplify(u[i]*w[j] - u[j]*w[i]) == 0
               for i, j in itertools.combinations(range(4), 2))


YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)


# ---------------------------------------------------------------------------
# sieve machinery (s07 pattern, verbatim conventions)
# ---------------------------------------------------------------------------
def kernel_lines(planes, T):
    kerns = []
    for mode in range(4):
        mat = sp.zeros(2, 8)
        for bits in itertools.product((0, 1), repeat=4):
            rest = tuple(bits[j] for j in range(4) if j != mode)
            mat[bits[mode], rest[0]*4 + rest[1]*2 + rest[2]] = T[bits]
        l = sp.Matrix(mat.T).nullspace()[0]
        kerns.append(tuple(sp.expand(l[0]*planes[mode][0][j] + l[1]*planes[mode][1][j])
                           for j in range(4)))
    return kerns


def rank1_item(M2, planes, a_, b_, kerns):
    uc = M2.columnspace()[0]
    yc = M2.T.columnspace()[0]
    uvec = tuple(sp.simplify(uc[0]*planes[a_][0][j] + uc[1]*planes[a_][1][j])
                 for j in range(4))
    yvec = tuple(sp.simplify(yc[0]*planes[b_][0][j] + yc[1]*planes[b_][1][j])
                 for j in range(4))
    assert all(sp.simplify(val) == 0 for val in rmul(uvec, yvec).values())
    ker_sides = []
    if proportional(uvec, kerns[a_]):
        ker_sides.append(a_)
    if proportional(yvec, kerns[b_]):
        ker_sides.append(b_)
    return {"supp": {a_: frozenset(j for j in range(4) if sp.simplify(uvec[j]) != 0),
                     b_: frozenset(j for j in range(4) if sp.simplify(yvec[j]) != 0)},
            "kernel_sides": tuple(ker_sides)}


def analyse(planes, label):
    planes = [[tuple(sp.nsimplify(c) for c in row) for row in pl] for pl in planes]
    for pl in planes:
        assert sp.Matrix([list(pl[0]), list(pl[1])]).rank() == 2, (label, "degenerate")
    T = {bits: perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
         for bits in itertools.product((0, 1), repeat=4)}
    assert any(t != 0 for t in T.values()), label
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        mfl = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            mfl[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        assert mfl.rank() == 1, (label, left, right)
    kerns = kernel_lines(planes, T)
    ranks = {}
    lows = {}
    for a_, b_ in COORD_PAIRS:
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        rk = mm.rank()
        ranks[(a_, b_)] = rk
        if rk <= 3:
            null = mm.T.nullspace()
            items = []
            m2ranks = []
            if rk == 3:
                kv = [sp.simplify(c_) for c_ in null[0]]
                M2 = sp.Matrix([[kv[0], kv[1]], [kv[2], kv[3]]])
                m2ranks.append(M2.rank())
                if m2ranks[-1] == 1:
                    items.append(rank1_item(M2, planes, a_, b_, kerns))
            elif rk == 2:
                kA_ = [sp.simplify(c_) for c_ in null[0]]
                kB_ = [sp.simplify(c_) for c_ in null[1]]
                A2 = sp.Matrix([[kA_[0], kA_[1]], [kA_[2], kA_[3]]])
                B2 = sp.Matrix([[kB_[0], kB_[1]], [kB_[2], kB_[3]]])
                cc, dd = sp.symbols("cc dd")
                det = sp.expand((cc*A2 + dd*B2).det())
                sols = []
                pc = sp.Poly(det.subs(dd, 1), cc)
                if pc.degree() >= 1:
                    sols += [(rt, sp.Integer(1)) for rt in sp.roots(pc, multiple=True)]
                if sp.expand(det.subs({cc: 1, dd: 0})) == 0:
                    sols.append((sp.Integer(1), sp.Integer(0)))
                for (cv, dv) in sols:
                    M2 = cv*A2 + dv*B2
                    if M2.rank() == 1:
                        items.append(rank1_item(M2, planes, a_, b_, kerns))
            lows[(a_, b_)] = {"rank": rk, "m2ranks": m2ranks, "rank1": items}
    return {"label": label, "ranks": ranks, "lows": lows, "kerns": kerns}


def sieve(q, X):
    ok = []
    for sigma in PERMS4:
        def se(e_):
            return tuple(sorted((sigma[e_[0]], sigma[e_[1]])))
        if any(q["ranks"][e_] > X["ranks"][se(e_)] for e_ in COORD_PAIRS):
            continue
        for pi in PERMS4:
            good = True
            for e_ in COORD_PAIRS:
                if X["ranks"][se(e_)] == 4:
                    continue
                Xlow = X["lows"][se(e_)]
                qlow = q["lows"].get(e_)
                if qlow is None:
                    good = False
                    break
                for itX in Xlow["rank1"]:
                    found = False
                    for itq in qlow["rank1"]:
                        cond = all(sigma.index(h) in itq["kernel_sides"]
                                   for h in itX["kernel_sides"])
                        if cond:
                            for mmode in e_:
                                sX = itX["supp"][sigma[mmode]]
                                if not itq["supp"][mmode] <= frozenset(pi[j] for j in sX):
                                    cond = False
                                    break
                        if cond:
                            found = True
                            break
                    if not found:
                        good = False
                        break
                if not good:
                    break
            if good:
                ok.append((sigma, pi))
    return ok


def census_samples():
    samples = {}
    samples["first"] = [[(1, 0, -1, -2), (0, 1, 1, 0)], [(1, 1, 0, 0), (0, 0, 1, 1)],
                        [(0, 1, 0, 1), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
    samples["dq"] = [[(2, -1, -1, -2), (1, -1, 1, 1)], [(1, 0, 0, -1), (1, 1, -1, 1)],
                     [(3, 1, 1, -1), (0, 1, -1, 0)], [(1, 0, 0, 1), (0, 1, 1, 0)]]
    samples["L1"] = [[(2, 4, 0, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                     [(1, 0, 4, 2), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
    samples["L2"] = [[(2, 0, 4, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                     [(1, 0, 4, 6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
    samples["L3"] = [[(2, 10, -8, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 2)],
                     [(1, 0, 3, -6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
    dd, pp, qq = 2, 3, 5
    n6 = qq*(dd + pp + qq)
    samples["sixth"] = [[(-dd*pp, dd + qq, n6, 0), (dd*pp, -dd - qq, 0, n6)],
                        [(0, 0, 1, 1), (-dd, 1, -pp - qq, dd)],
                        [(pp, 1, 0, qq), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
    a7, c7, d7, b7, e7 = 1, 2, 4, 1, 2
    h7 = a7 + c7 - d7
    samples["seventh"] = [[(1, 0, 0, -1), (0, 0, 1, 1)],
                          [(1, b7, 0, 1 - b7*h7), (0, e7, 1, 1 - e7*h7)],
                          [(1, 0, -1, 0), (0, 1, -a7 - c7, -d7)],
                          [(1, 0, 0, 1), (0, 0, 1, -1)]]
    a8, b8, f8, ph8 = sp.Integer(-12), sp.Integer(-10), sp.Rational(3, 4), sp.Rational(-5, 28)
    j8 = f8 + b8*ph8**2
    kap8 = ph8*(b8*f8 + 1)
    eta8 = -(b8*f8 + 1)
    samples["eighth"] = [[(0, 0, 1, -1), (a8 + b8, a8 - b8, 0, 2)],
                         [(-a8*f8 + 1, -a8*f8 - 1, f8 + ph8, f8 - ph8), (1, 1, 0, 0)],
                         [(-a8*j8 + eta8, -a8*j8 - eta8, j8 + kap8, j8 - kap8), (1, 1, 0, 0)],
                         [(1, -1, 0, 0), (0, 0, 1, 1)]]
    d9, v90, v91, v92, x91, x92 = 2, 3, 5, 7, 11, -4
    x90 = sp.Rational(-(d9*v90*x91 + v91*x92), d9*v91)
    c9 = (-d9*v91, -d9*v90, v91, v91)
    k19, k29, k39 = (-c9[1], c9[0], 0, 0), (-c9[2], 0, c9[0], 0), (-c9[3], 0, 0, c9[0])
    al9, be9 = sp.Rational(2, 3), sp.Rational(-1, 2)
    samples["ninth"] = [[tuple(k19[j] + al9*k39[j] for j in range(4)),
                         tuple(k29[j] + be9*k39[j] for j in range(4))],
                        [(0, 0, 1, -1), (v90, v91, v92, -v92)],
                        [(1, 0, -d9, 0), (x90, x91, x92, 0)],
                        [(0, 0, 1, 1), (1, 0, d9, 0)]]
    samples["tenth"] = [[(1, -1, 0, 0), (0, 1, 2, -10)],
                        [(1, -1, 0, 0), (0, 1, 3, -15)],
                        [(1, 1, 0, 0), (0, 0, 1, 5)],
                        [(1, 7, 0, 0), (0, 11, 1, -5)]]
    samples["eleventh"] = [[(3, 7, 0, 0), (0, 0, 1, -3)],
                           [(0, 0, 1, 2), (3, -7, 2, 5)],
                           [(0, 0, 1, -5), (6, -14, -1, 4)],
                           [(0, 0, 1, 1), (0, 0, 1, -1)]]
    k12 = 2
    q3_12 = -k12*(3 + 5) - (-1)
    samples["twelfth"] = [[(1, 1, 0, 0), (0, 0, 1, -k12)],
                          [(1, -1, 0, 0), (0, 1, 3, -1)],
                          [(1, -1, 0, 0), (0, 1, 5, q3_12)],
                          [(1, 1, 0, 0), (0, 0, 1, k12)]]
    b13, e13, k13, w2_13, w3_13 = 2, 3, 5, 1, 7
    W13 = sp.Rational(-(b13 + e13)*(k13*w2_13 - w3_13), 2*b13*e13*k13)
    zeta13 = ((b13 + e13)*(k13*w2_13 + w3_13), 0, -2*b13*e13*k13*w2_13,
              2*b13*e13*k13*w3_13)
    samples["thirteenth"] = [[(1, 1, 0, 0), zeta13],
                             [(1, -1, 0, 0), (0, 1, b13, -b13*k13)],
                             [(1, -1, 0, 0), (0, 1, e13, -e13*k13)],
                             [(1, 1, 0, 0), (0, W13, w2_13, w3_13)]]
    return samples


DOCUMENTED_PROFILES = {
    "first": (4, 4, 4, 3, 3, 3), "dq": (4, 4, 3, 4, 3, 3),
    "L1": (4, 4, 3, 4, 3, 3), "L2": (4, 4, 3, 4, 3, 3), "L3": (4, 4, 3, 4, 3, 3),
    "sixth": (4, 4, 3, 4, 3, 3), "seventh": (4, 3, 2, 4, 4, 3),
    "eighth": (4, 4, 3, 4, 3, 3), "ninth": (4, 4, 4, 3, 3, 3),
    "tenth": (3, 3, 4, 3, 4, 4), "eleventh": (4, 4, 3, 4, 3, 3),
    "twelfth": (3, 3, 3, 4, 3, 3), "thirteenth": (3, 3, 4, 3, 3, 3),
}


def assert_pure_ff(planes, label):
    """identical purity over the function field; returns T."""
    T = {bits: sp.expand(sp.together(perm4(tuple(tuple(sp.sympify(c)
                                                       for c in planes[m][bits[m]])
                                                 for m in range(4)))))
         for bits in itertools.product((0, 1), repeat=4)}
    assert any(sp.simplify(v) != 0 for v in T.values()), (label, "zero")
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            m[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
        for r1, r2 in itertools.combinations(range(4), 2):
            for c1, c2 in itertools.combinations(range(4), 2):
                assert sp.simplify(sp.together(
                    m[r1, c1]*m[r2, c2] - m[r1, c2]*m[r2, c1])) == 0, (label, "not pure")
    return T


# ---------------------------------------------------------------------------
# the three normal forms
# ---------------------------------------------------------------------------
p2, p3, lam, al, wv1 = sp.symbols("p2 p3 lam al wv1")


def famA_planes():
    be = -al - lam
    aYv = al*p3
    bYv = be*p2
    q2v, q3v = lam*p2, lam*p3
    P = sp.expand(p2*q3v + p3*q2v)
    kA = (sp.expand(p3 + q3v), 0, -P, 0)
    kB = (sp.expand(p2 + q2v), 0, 0, -P)
    z1 = tuple(sp.expand(kA[t] + aYv*YBAR[t]) for t in range(4))
    z2 = tuple(sp.expand(kB[t] + bYv*YBAR[t]) for t in range(4))
    wA = (0, 1 + lam, 2*bYv, 2*aYv)
    return [[z1, z2], [YBAR, (0, 1, p2, p3)], [YBAR, (0, 1, q2v, q3v)], [U3v, wA]]


TA = assert_pure_ff(famA_planes(), "F_A")
nzA = {b for b, v in TA.items() if sp.simplify(v) != 0}
assert all(b[1] == 0 and b[3] == 1 for b in nzA)
print("F_A: identically pure over Q(p2,p3,lam,al); support words have")
print("     mode-1 bit 0 and mode-3 bit 1: K1 = span(p), K3 = u3.  OK")

p2b, p3b, q2b, q3b = sp.symbols("p2b p3b q2b q3b")


def famB_planes():
    det = q2b*p3b - q3b*p2b
    S = p2b*p3b + p3b*q2b + p2b*q3b
    aYb = sp.together((-q2b*q3b*p3b + q3b*S)/det)
    bYb = sp.together((p2b*q2b*q3b - q2b*S)/det)
    P = sp.expand(p2b*q3b + p3b*q2b)
    kA = (sp.expand(p3b + q3b), 0, -P, 0)
    kB = (sp.expand(p2b + q2b), 0, 0, -P)
    z1 = tuple(sp.together(kA[t] + aYb*YBAR[t]) for t in range(4))
    z2 = tuple(sp.together(kB[t] + bYb*YBAR[t]) for t in range(4))
    wv2v = bYb
    wv3v = sp.together(p3b + q3b + aYb)
    return [[z1, z2], [YBAR, (0, 1, p2b, p3b)], [YBAR, (0, 1, q2b, q3b)],
            [U3v, (0, 0, wv2v, wv3v)]], aYb, bYb


famB, aYb_, bYb_ = famB_planes()
# the two defining linear identities of class B:
assert sp.simplify(q2b*q3b + q2b*aYb_ + q3b*bYb_) == 0
assert sp.simplify(p2b*p3b + p3b*q2b + p2b*q3b + p2b*aYb_ + p3b*bYb_) == 0
TB = assert_pure_ff(famB, "F_B")
nzB = {b for b, v in TB.items() if sp.simplify(v) != 0}
assert all(b[1] == 0 and b[3] == 1 for b in nzB)
print("F_B: identically pure over Q(p2,p3,q2,q3) (wv1 = 0: w in Pi).  OK")

cS, dS, mS, tauS, wv2S, W1S = sp.symbols("cS dS mS tauS wv2S W1S")
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
# purity minors all factor as (unit monomial) * CONIC:
TC = {bits: sp.expand(perm4(tuple(tuple(sp.sympify(c) for c in famC[m][bits[m]])
                                  for m in range(4))))
      for bits in itertools.product((0, 1), repeat=4)}
minsC = set()
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    m = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        m[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = TC[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            val = sp.expand(m[r1, c1]*m[r2, c2] - m[r1, c2]*m[r2, c1])
            if val != 0:
                minsC.add(val)
for val in minsC:
    quot = sp.cancel(val/CONIC)
    num, den = sp.fraction(sp.together(quot))
    assert den.is_number or sp.Poly(den, W1S, wv2S).total_degree() == 0
    assert sp.Poly(num, W1S, wv2S).total_degree() == 0, "minor not monomial*CONIC"
print("F_C: every purity minor = (parameter monomial) * CONIC: the family")
print("     is identically pure exactly on the conic Q = 0.  OK")
# conic irreducibility: the W1-discriminant's bracket is squarefree in tau
disc = sp.expand((cS*dS*wv2S*(cS + dS + 2*tauS))**2
                 - 4*cS**2*dS**2*wv2S**2*(cS*dS + 4*tauS*(cS + dS) + 4*tauS**2))
bracket = sp.cancel(disc/(cS**2*dS**2*wv2S**2))
assert sp.expand(bracket - ((cS - dS)**2 - 12*tauS*(cS + dS) - 12*tauS**2)) == 0
tdisc = sp.expand(sp.discriminant(sp.Poly(bracket, tauS)))
assert sp.simplify(tdisc) != 0
assert sp.expand(tdisc - (144*(cS + dS)**2 + 48*(cS - dS)**2)) == 0
print("     conic W1-discriminant bracket (c-d)^2-12tau(c+d)-12tau^2 is")
print("     squarefree in tau (tau-discriminant 144(c+d)^2+48(c-d)^2 != 0):")
print("     Q is irreducible; F_C is an irreducible conic bundle.  OK")

# ---------------------------------------------------------------------------
# samples (= the w04 pipeline samples, re-expressed in the normal forms)
# ---------------------------------------------------------------------------
SAMPLE_A = {p2: sp.Rational(-8, 13), p3: sp.Rational(16, 221), lam: -13,
            al: sp.Rational(221, 8), wv1: -4}
SAMPLE_B = {p2b: sp.Rational(-2601, 161), p3b: -9, q2b: 9, q3b: sp.Rational(9, 17)}
SAMPLE_C = {cS: 3, dS: 12, mS: sp.Rational(2, 3), tauS: -9,
            wv2S: sp.Rational(21, 2), W1S: sp.Rational(35, 8)}
assert sp.expand(CONIC.subs(SAMPLE_C)) == 0


def eval_planes(planes, sub):
    out = []
    for pl in planes:
        rows = []
        for row in pl:
            row = [sp.nsimplify(sp.cancel(sp.together(sp.sympify(c).subs(sub))))
                   for c in row]
            den = sp.lcm([sp.denom(c) for c in row])
            rows.append(tuple(sp.expand(c*den) for c in row))
        out.append(rows)
    return out


plA = eval_planes(famA_planes(), SAMPLE_A)
plB = eval_planes(famB, SAMPLE_B)
plC = eval_planes(famC, SAMPLE_C)

# cross-check: class A sample = the w04 prime-#11 sample (aY = 2, bY = 9,
# q = (0,1,8,-16/17), w ~ (0,-4,6,4/3))
assert sp.expand((al*p3).subs(SAMPLE_A) - 2) == 0
assert sp.expand(((-al - lam)*p2).subs(SAMPLE_A) - 9) == 0

packages = {}
for name, planes in census_samples().items():
    pkg = analyse(planes, name)
    prof = tuple(pkg["ranks"][e_] for e_ in COORD_PAIRS)
    assert prof == DOCUMENTED_PROFILES[name], (name, prof)
    packages[name] = pkg
# calibrations
cal = analyse([[(1, 7, 0, 0), (0, 11, 1, -5)], [(1, -1, 0, 0), (0, 1, 2, -10)],
               [(1, -1, 0, 0), (0, 1, 3, -15)], [(1, 1, 0, 0), (0, 0, 1, 5)]],
              "tenth-sweep-modes")
assert sieve(cal, packages["tenth"])
zb1 = analyse([[U3v, (0, 0, -1, 2)], [YBAR, (0, 1, 3, -1)], [YBAR, (0, 1, 5, -15)],
               [U3v, (0, 0, 1, 2)]], "Zb1")
assert sieve(zb1, packages["twelfth"])
for nm in packages:
    assert sieve(packages[nm], packages[nm]), ("self-alignment", nm)
print("thirteen census packages + calibrations (tenth alignment, Zb1 vs")
print("twelfth, all self-alignments).  OK")

pkgA = analyse(plA, "F_A sample")
pkgB = analyse(plB, "F_B sample")
pkgC = analyse(plC, "F_C sample")
assert tuple(pkgA["ranks"][e] for e in COORD_PAIRS) == (4, 4, 4, 3, 3, 3)
assert tuple(pkgB["ranks"][e] for e in COORD_PAIRS) == (4, 4, 3, 4, 3, 3)
assert tuple(pkgC["ranks"][e] for e in COORD_PAIRS) == (4, 4, 4, 3, 3, 3)
for nm, pk_ in (("A", pkgA), ("B", pkgB), ("C", pkgC)):
    for xn, X in packages.items():
        assert not sieve(pk_, X), (nm, "unexpected pass", xn)
print("SEPARATION: all three samples pass NO alignment of the sieve against")
print("any of the THIRTEEN certified component orbits.  OK")
# mutual: B vs A, B vs C (both directions)
assert not sieve(pkgB, pkgA) and not sieve(pkgA, pkgB)
assert not sieve(pkgB, pkgC) and not sieve(pkgC, pkgB)
print("MUTUAL: class B is sieve-separated from classes A and C (both")
print("directions).  OK")

# A vs C: closed kernel-support invariant.
# (i) on F_C, K3 = u3 (all support words have mode-3 bit 1: w-row) and
#     K0 lies in Pi identically: prove the kernel vector's coords 0,1
#     vanish modulo the conic.
assert all(b[3] == 1 for b, v in TC.items() if sp.expand(v) != 0)
# mode-0 flattening kernel: for column rest = (bits1,bits2,bits3) with
# T[0,rest] or T[1,rest] nonzero, K0 ~ T[(1,)+rest]*z1 - T[(0,)+rest]*z2:
z1C, z2C = famC[0]
found = False
for rest in itertools.product((0, 1), repeat=3):
    Ta = TC[(0,) + rest]
    Tb = TC[(1,) + rest]
    if sp.expand(Ta) == 0 and sp.expand(Tb) == 0:
        continue
    K0 = [sp.expand(Tb*sp.sympify(z1C[j]) - Ta*sp.sympify(z2C[j])) for j in range(4)]
    r0 = sp.rem(sp.Poly(K0[0], W1S), sp.Poly(CONIC, W1S))
    r1 = sp.rem(sp.Poly(K0[1], W1S), sp.Poly(CONIC, W1S))
    assert sp.expand(sp.expand(r0.as_expr())) == 0, "K0 coord 0 not in Pi mod conic"
    assert sp.expand(sp.expand(r1.as_expr())) == 0, "K0 coord 1 not in Pi mod conic"
    found = True
    break
assert found
print("A-vs-C invariant, step 1: on F_C the mode-0 kernel K0 lies in Pi")
print("IDENTICALLY (coords 0,1 vanish modulo the conic), and K3 = u3: at")
print("least TWO mode kernels in coordinate 2-planes on all of")
print("closure(F_C) (a closed census-stable condition on pure points).  OK")
# (ii) the class-A sample has kernel supports {3,3,4,2}: exactly one small
suppsA = sorted(len([j for j in range(4) if sp.simplify(kv[j]) != 0])
                for kv in pkgA["kerns"])
assert suppsA == [2, 3, 3, 4], suppsA
print("step 2: class-A sample kernel supports {2,3,3,4}: exactly ONE mode")
print("kernel in a coordinate 2-plane => the A-sample lies in NO census")
print("image of closure(F_C): classes A and C are DISTINCT orbits.  OK")

# ---------------------------------------------------------------------------
# tangent rank 5 and incidence certificates
# ---------------------------------------------------------------------------
t0, t1, t2 = sp.symbols("t0:3")
TORUS = (t0, t1, t2, 1)


def family_tangent_rank(planes_sym, params, sample, constraint=None):
    """Family tangent rank at `sample`, including the full projective torus.

    `constraint`, when given, is a polynomial in `params` cutting out the
    locus on which the parametrization is actually pure (class C is pure
    only on its conic).  The parameter differentials are then restricted
    to the tangent hyperplane of {constraint = 0}: without that
    restriction the Jacobian measures the tangent of the map into the
    ambient Grassmannian product, which for a constrained family counts
    directions that leave the pure locus.  (The first draft of this
    script omitted the restriction for class C and read six instead of
    five; see w06_classC_constrained_tangent.py for the standalone
    diagnosis.)
    """
    scaled = [sp.Matrix([[sp.sympify(c)*TORUS[j] for j, c in enumerate(row)]
                         for row in pl]) for pl in planes_sym]
    point = {**sample, t0: 1, t1: 1, t2: 1}
    planes_at = [sp.Matrix([[sp.nsimplify(sp.cancel(sp.together(sp.sympify(c).subs(point))))
                             for c in row] for row in pl]) for pl in planes_sym]
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
    allp = tuple(params) + (t0, t1, t2)
    J = sp.Matrix(chart_coords).jacobian(allp).subs(point)
    J = sp.Matrix([[sp.nsimplify(sp.cancel(c)) for c in row] for row in J.tolist()])
    if constraint is None:
        return J.rank(), pivots, planes_at
    grad = sp.Matrix([[sp.nsimplify(sp.diff(constraint, p).subs(sample))
                       for p in params]])
    assert any(g != 0 for g in grad), "sample is a singular point of the constraint"
    null = grad.nullspace()
    assert len(null) == len(params) - 1, (len(null), len(params))
    tangent_basis = sp.Matrix.hstack(*null)
    block = sp.Matrix.hstack(J[:, :len(params)]*tangent_basis, J[:, len(params):])
    return block.rank(), pivots, planes_at


def incidence_data(planes_at, pivots):
    reduced_point = [pl[:, piv].inv()*pl for pl, piv in zip(planes_at, pivots)]
    T_point = {bits: sp.nsimplify(sp.cancel(perm4(tuple(tuple(reduced_point[m][bits[m], j]
                                                              for j in range(4))
                                                        for m in range(4)))))
               for bits in itertools.product((0, 1), repeat=4)}
    anchor = next(bb for bb in itertools.product((0, 1), repeat=4)
                  if T_point[bb] != 0)
    zvars = sp.symbols("ZI0:16")
    rvars = sp.symbols("RI0:4")
    universal = []
    for mode, piv in enumerate(pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        plane = sp.zeros(2, 4)
        plane[0, piv[0]] = 1
        plane[1, piv[1]] = 1
        entries = zvars[4*mode: 4*mode + 4]
        for rr in range(2):
            for o_, cc in enumerate(nonpiv):
                plane[rr, cc] = entries[2*rr + o_]
        universal.append(plane)
    T_univ = {bits: perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4))
                                for m in range(4)))
              for bits in itertools.product((0, 1), repeat=4)}
    eqs = []
    for word in itertools.product((0, 1), repeat=4):
        if word == anchor:
            continue
        mono = sp.prod(rvars[mm] for mm in range(4) if word[mm] != anchor[mm])
        eqs.append(sp.expand(T_univ[word] - T_univ[anchor]*mono))
    coord_pt = []
    for plane, piv in zip(reduced_point, pivots):
        nonpiv = tuple(i for i in range(4) if i not in piv)
        coord_pt.extend(sp.nsimplify(plane[rr, cc]) for rr in range(2) for cc in nonpiv)
    ratios = tuple(T_point[tuple((1 - anchor[mm] if mm == mode else anchor[mm])
                                 for mm in range(4))]/T_point[anchor]
                   for mode in range(4))
    subst = dict(zip(tuple(zvars) + tuple(rvars), tuple(coord_pt) + ratios))
    assert all(sp.simplify(eq.subs(subst)) == 0 for eq in eqs)
    J = sp.Matrix(eqs).jacobian(tuple(zvars) + tuple(rvars)).subs(subst)
    return J.rank(), (T_univ, anchor, zvars, dict(zip(zvars, coord_pt)))


rkA, pivA, planesA_at = family_tangent_rank(famA_planes(), (p2, p3, lam, al, wv1),
                                            SAMPLE_A)
assert rkA == 5
incA, _ = incidence_data(planesA_at, pivA)
assert incA == 15
print("CLASS A: family tangent rank 5 (incl. full torus); incidence")
print("Jacobian rank FIFTEEN: a smooth 5-dimensional point.  The rational")
print("irreducible 5-fold closure(F_A) is the unique component through it:")
print("a FOURTEENTH pure-compression component orbit.  OK")

rkB, pivB, planesB_at = family_tangent_rank(famB, (p2b, p3b, q2b, q3b), SAMPLE_B)
assert rkB == 5
incB, _ = incidence_data(planesB_at, pivB)
assert incB == 15
print("CLASS B: family tangent rank 5; incidence rank FIFTEEN: smooth")
print("point; closure(F_B) is a FIFTEENTH component orbit.  OK")

rkC, pivC, planesC_at = family_tangent_rank(famC, (cS, dS, mS, tauS, wv2S, W1S),
                                            SAMPLE_C, constraint=CONIC)
assert rkC == 5, ("class-C constrained tangent", rkC)
incC, (T_univC, anchorC, zvarsC, subs0C) = incidence_data(planesC_at, pivC)
assert incC == 14
print("CLASS C: family tangent rank 5; incidence rank 14 (tangent 6):")
print("singular point; certifying by the char-0 five-slice instead...")

# the 28 mode-anchor minors five-slice at the C sample (w02 system)
minors = []
for mode in range(4):
    others = tuple(j for j in range(4) if j != mode)
    anch_rest = tuple(anchorC[j] for j in others)

    def word(im, rest):
        w = [0]*4
        w[mode] = im
        for j, bitv in zip(others, rest):
            w[j] = bitv
        return tuple(w)
    for rest in itertools.product((0, 1), repeat=3):
        if rest == anch_rest:
            continue
        mm = sp.expand(T_univC[word(0, anch_rest)]*T_univC[word(1, rest)]
                       - T_univC[word(0, rest)]*T_univC[word(1, anch_rest)])
        minors.append(mm)
assert len(minors) == 28
assert all(sp.simplify(mm.subs(subs0C)) == 0 for mm in minors)
shifted = []
for eq in minors:
    poly = sp.expand(eq.subs({zv: zv + val for zv, val in subs0C.items()}))
    den = 1
    for coeff in sp.Poly(poly, *zvarsC).coeffs():
        den = sp.lcm(den, sp.denom(sp.nsimplify(coeff)))
    shifted.append(sp.expand(poly*den))
SLICES = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
)
slices = [sum(cc*zz for cc, zz in zip(row, zvarsC)) for row in SLICES]
varnames = ",".join(str(vv) for vv in zvarsC)
gens = shifted + slices
polys = ";\n".join(f"poly g{i}={str(pp).replace('**','^')}" for i, pp in enumerate(gens))
program = "\n".join((
    f"ring R=0,({varnames}),ds;", polys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(gens))) + ";",
    "ideal J=std(I);", '"SLICE_LOCAL_DIM:"+string(dim(J));', "quit;"))
try:
    completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                               encoding="utf-8", errors="replace",
                               capture_output=True, timeout=1800, check=False)
    out = completed.stdout
    dimC = (int(out.split("SLICE_LOCAL_DIM:")[1].split()[0])
            if "SLICE_LOCAL_DIM:" in out else None)
except subprocess.TimeoutExpired:
    dimC = None
print("char-0 five-slice ds local dimension at the C sample:",
      "NULL (timeout)" if dimC is None else dimC)
assert dimC == 0, "class C slice certificate did not close (null recorded)"
print("CLASS C: local dimension <= 5, hence exactly 5: closure(F_C) is an")
print("irreducible component: a SIXTEENTH component orbit.  OK")

# ---------------------------------------------------------------------------
# orbit structure of the seven pass-NONE chart primes (documentation-level
# check: the three classes are single census orbits)
# ---------------------------------------------------------------------------
GENS = {
    11: ["wv2*aY-wv3*bY", "q2*q3+q2*aY+q3*bY", "2*p3*wv1*bY-p3*wv2-q3*wv2",
         "2*p3*wv1*aY-p3*wv3-q3*wv3", "p3*q2+p2*aY+p3*bY",
         "2*p3*q2*wv1+2*p3*wv1*bY+p2*wv3+q2*wv3", "2*p2*wv1*bY-p2*wv2-q2*wv2",
         "p2*q3+p2*aY+p3*bY"],
    16: ["q2*q3+q2*aY+q3*bY", "p3*wv2+q3*wv2+wv2*aY-wv3*bY",
         "p2*wv3+q2*wv3-wv2*aY+wv3*bY", "p2*p3+p3*q2+p2*q3+p2*aY+p3*bY", "wv1"],
}
p2s_, p3s_, q2s_, q3s_ = sp.symbols("p2 p3 q2 q3")
wv1s_, wv2s_, wv3s_ = sp.symbols("wv1 wv2 wv3")
aYs_, bYs_ = sp.symbols("aY bY")
# F_A satisfies prime #11's generators identically:
subA = {p2s_: p2, p3s_: p3, q2s_: lam*p2, q3s_: lam*p3, aYs_: al*p3,
        bYs_: (-al - lam)*p2, wv1s_: wv1,
        wv2s_: 2*wv1*(-al - lam)*p2/(1 + lam), wv3s_: 2*wv1*al*p3/(1 + lam)}
for g in GENS[11]:
    val = sp.simplify(sp.together(sp.sympify(g).subs(subA)))
    assert val == 0, ("A gen", g)
# F_B satisfies prime #16's generators identically:
detB = q2b*p3b - q3b*p2b
SB = p2b*p3b + p3b*q2b + p2b*q3b
subB = {p2s_: p2b, p3s_: p3b, q2s_: q2b, q3s_: q3b,
        aYs_: (-q2b*q3b*p3b + q3b*SB)/detB, bYs_: (p2b*q2b*q3b - q2b*SB)/detB,
        wv1s_: 0, wv2s_: bYb_*1, wv3s_: sp.together(p3b + q3b + aYb_)}
for g in GENS[16]:
    val = sp.simplify(sp.together(sp.sympify(g).subs(subB)))
    assert val == 0, ("B gen", g)
print("normal forms satisfy the w04 prime generators (#11 for A, #16 for")
print("B) identically: the classes are the sweep's pass-NONE primes.  OK")
print()
print("VERDICT: the pure-P4 compression census lower bound is SIXTEEN:")
print("  14th = closure(F_A): dim 5, profile (4,4,4,3,3,3), K1 = p,")
print("         K3 = u3, q_Pi || p_Pi;   orbit of primes {11,12,26,28};")
print("  15th = closure(F_B): dim 5, profile (4,4,3,4,3,3), w in Pi;")
print("         orbit of primes {15,16};")
print("  16th = closure(F_C): dim 5, profile (4,4,4,3,3,3), p||q||w in Pi,")
print("         conic-bundle family, singular certificate; prime {13}.")
print()
print("ALL CHECKS PASSED")
