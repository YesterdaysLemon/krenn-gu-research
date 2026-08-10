#!/usr/bin/env python3
"""Deliverable 2: exact invariant packages of the two singular deep branches
of the disjoint chart, of all nine certified components (at their documented
sample points), and a complete semicontinuity sieve over all mode maps sigma
(24) x source permutations pi (24).

Necessary conditions used for q in closure(X) (all are exact limit
obstructions; see the working notes for the invariance statements):
 (R)  pair-image rank monotonicity r_q(e) <= r_X(sigma(e));
 (S)  every rank-one relation of X at sigma(e) (unique at a stable rank-3
      edge, the two rank-one lines of the pencil at a rank-2 edge) limits to
      a NONZERO rank-one element of q's relation space at e whose
      kernel-endpoint sides contain sigma^{-1}(X kernel sides) and whose
      factor supports are contained in pi(X factor supports).  If q's
      relation space at e contains no rank-one element compatible with this
      (e.g. it is spanned by a rank-two matrix), the alignment fails.

The sieve is CALIBRATED on two containments proved in
P4_INOUT_PATH_STRATUM_WORKING_NOTE.md:
  * the overlap-one deep branch d*v0*x1+v1*x3=0 (U0 free) IS the first
    component -> the sieve returns exactly one alignment (sigma=pi=id) for
    "first" and excludes the other eight;
  * the F4 branch is contained in the seventh component -> the sieve
    returns alignments for "seventh".

RESULT: branch A (alpha=beta) and branch B (v0+v1=0) are excluded from ALL
NINE certified component closures.
"""
import itertools
import sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab))) for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]] * w[ab[1]] + u[ab[1]] * w[ab[0]]) for ab in COORD_PAIRS}


def pairing(P, Q):
    return sp.expand(sum(P[ab] * Q[COMPLEMENT[ab]] for ab in COORD_PAIRS))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[kk][pi[kk]] for kk in range(4)) for pi in PERMS4))


def proportional(u, w):
    return all(sp.simplify(u[i] * w[j] - u[j] * w[i]) == 0
               for i, j in itertools.combinations(range(4), 2))


def kernel_lines(planes, T):
    kerns = []
    for mode in range(4):
        phi = None
        for bits in itertools.product((0, 1), repeat=4):
            if T[bits] != 0:
                b0 = tuple(0 if kk == mode else bits[kk] for kk in range(4))
                b1 = tuple(1 if kk == mode else bits[kk] for kk in range(4))
                phi = (T[b0], T[b1])
                break
        kern = (phi[1], -phi[0])
        kerns.append(tuple(sp.expand(kern[0] * planes[mode][0][j] + kern[1] * planes[mode][1][j])
                           for j in range(4)))
    return kerns


def rank1_item(M2, planes, a_, b_, kerns):
    uc = M2.columnspace()[0]
    yc = M2.T.columnspace()[0]
    uvec = tuple(sp.simplify(uc[0] * planes[a_][0][j] + uc[1] * planes[a_][1][j]) for j in range(4))
    yvec = tuple(sp.simplify(yc[0] * planes[b_][0][j] + yc[1] * planes[b_][1][j]) for j in range(4))
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
    T = {}
    for bits in itertools.product((0, 1), repeat=4):
        T[bits] = perm4(tuple(tuple(planes[md][bits[md]]) for md in range(4)))
    assert any(t != 0 for t in T.values()), label
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        mfl = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            mfl[2 * bits[left[0]] + bits[left[1]], 2 * bits[right[0]] + bits[right[1]]] = T[bits]
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
                kA = [sp.simplify(c_) for c_ in null[0]]
                kB = [sp.simplify(c_) for c_ in null[1]]
                A2 = sp.Matrix([[kA[0], kA[1]], [kA[2], kA[3]]])
                B2 = sp.Matrix([[kB[0], kB[1]], [kB[2], kB[3]]])
                cc, dd = sp.symbols("cc dd")
                det = sp.expand((cc * A2 + dd * B2).det())
                sols = []
                pc = sp.Poly(det.subs(dd, 1), cc)
                if pc.degree() >= 1:
                    sols += [(rt, sp.Integer(1)) for rt in sp.roots(pc, multiple=True)]
                if sp.expand(det.subs({cc: 1, dd: 0})) == 0:
                    sols.append((sp.Integer(1), sp.Integer(0)))
                for (cv, dv) in sols:
                    M2 = cv * A2 + dv * B2
                    if M2.rank() == 1:
                        items.append(rank1_item(M2, planes, a_, b_, kerns))
            lows[(a_, b_)] = {"rank": rk, "m2ranks": m2ranks, "rank1": items}
    return {"label": label, "ranks": ranks, "lows": lows}


def sieve(q, X):
    """All (sigma, pi) satisfying the necessary limit conditions."""
    ok = []
    for sigma in PERMS4:
        def se(e):
            return tuple(sorted((sigma[e[0]], sigma[e[1]])))
        if any(q["ranks"][e] > X["ranks"][se(e)] for e in COORD_PAIRS):
            continue
        for pi in PERMS4:
            good = True
            for e in COORD_PAIRS:
                if X["ranks"][se(e)] == 4:
                    continue
                Xlow = X["lows"][se(e)]
                qlow = q["lows"][e]
                for itX in Xlow["rank1"]:
                    found = False
                    for itq in qlow["rank1"]:
                        cond = all(sigma.index(h) in itq["kernel_sides"]
                                   for h in itX["kernel_sides"])
                        if cond:
                            for mmode in e:
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


# ------------- nine certified component samples (from their theorem docs) ---
samples = {}
# P4_PURE_RANK_TWO_COMPONENT_THEOREM.md, chart point (3)
samples["first"] = [[(1, 0, -1, -2), (0, 1, 1, 0)], [(1, 1, 0, 0), (0, 0, 1, 1)],
                    [(0, 1, 0, 1), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
# P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md, sample (13)
samples["dq"] = [[(2, -1, -1, -2), (1, -1, 1, 1)], [(1, 0, 0, -1), (1, 1, -1, 1)],
                 [(3, 1, 1, -1), (0, 1, -1, 0)], [(1, 0, 0, 1), (0, 1, 1, 0)]]
# P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md, samples (20)
samples["L1"] = [[(2, 4, 0, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                 [(1, 0, 4, 2), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
samples["L2"] = [[(2, 0, 4, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 3)],
                 [(1, 0, 4, 6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
samples["L3"] = [[(2, 10, -8, 0), (0, 0, 1, 1)], [(0, 1, -1, 0), (1, 0, 1, 2)],
                 [(1, 0, 3, -6), (0, 1, 0, -1)], [(0, 1, 1, 0), (0, 1, 0, 1)]]
# sixth component family (verify_p4_inout_path_stratum_working_note.py) at (2,3,5)
dd, pp, qq = 2, 3, 5
n6 = qq * (dd + pp + qq)
samples["sixth"] = [[(-dd * pp, dd + qq, n6, 0), (dd * pp, -dd - qq, 0, n6)],
                    [(0, 0, 1, 1), (-dd, 1, -pp - qq, dd)],
                    [(pp, 1, 0, qq), (-1, 0, 1, 0)], [(1, 0, 1, 0), (0, 0, -1, 1)]]
# P4_SIX_DIMENSIONAL_PURE_COMPONENT.md family (1) at (a,c,d,b,e)=(1,2,4,1,2)
a7, c7, d7, b7, e7 = 1, 2, 4, 1, 2
h7 = a7 + c7 - d7
samples["seventh"] = [[(1, 0, 0, -1), (0, 0, 1, 1)],
                      [(1, b7, 0, 1 - b7 * h7), (0, e7, 1, 1 - e7 * h7)],
                      [(1, 0, -1, 0), (0, 1, -a7 - c7, -d7)],
                      [(1, 0, 0, 1), (0, 0, 1, -1)]]
# P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md family (5)-(7) at (15)
a8, b8, f8, p8 = sp.Integer(-12), sp.Integer(-10), sp.Rational(3, 4), sp.Rational(-5, 28)
assert sp.expand(a8**2 * b8 * f8 * p8**2 + a8**2 * f8**2 - b8**2 * f8**2
                 + b8**2 * p8**2 - b8 * f8 - 1) == 0
j8 = f8 + b8 * p8**2
kap8 = p8 * (b8 * f8 + 1)
eta8 = -(b8 * f8 + 1)
samples["eighth"] = [[(0, 0, 1, -1), (a8 + b8, a8 - b8, 0, 2)],
                     [(-a8 * f8 + 1, -a8 * f8 - 1, f8 + p8, f8 - p8), (1, 1, 0, 0)],
                     [(-a8 * j8 + eta8, -a8 * j8 - eta8, j8 + kap8, j8 - kap8), (1, 1, 0, 0)],
                     [(1, -1, 0, 0), (0, 0, 1, 1)]]
# ninth component: x3-branch of the overlap-one deep stratum
# (P4_INOUT_PATH_STRATUM_WORKING_NOTE.md / x3_wall_certificates sample)
d9, v90, v91, v92, x91, x92 = 2, 3, 5, 7, 11, -4
x90 = sp.Rational(-(d9 * v90 * x91 + v91 * x92), d9 * v91)
c9 = (-d9 * v91, -d9 * v90, v91, v91)
k1_9, k2_9, k3_9 = (-c9[1], c9[0], 0, 0), (-c9[2], 0, c9[0], 0), (-c9[3], 0, 0, c9[0])
al9, be9 = sp.Rational(2, 3), sp.Rational(-1, 2)
samples["ninth"] = [[tuple(k1_9[j] + al9 * k3_9[j] for j in range(4)),
                     tuple(k2_9[j] + be9 * k3_9[j] for j in range(4))],
                    [(0, 0, 1, -1), (v90, v91, v92, -v92)],
                    [(1, 0, -d9, 0), (x90, x91, x92, 0)],
                    [(0, 0, 1, 1), (1, 0, d9, 0)]]

DOCUMENTED_PROFILES = {
    "first": (4, 4, 4, 3, 3, 3), "dq": (4, 4, 3, 4, 3, 3),
    "L1": (4, 4, 3, 4, 3, 3), "L2": (4, 4, 3, 4, 3, 3), "L3": (4, 4, 3, 4, 3, 3),
    "sixth": (4, 4, 3, 4, 3, 3), "seventh": (4, 3, 2, 4, 4, 3),
    "eighth": (4, 4, 3, 4, 3, 3), "ninth": (4, 4, 4, 3, 3, 3),
}

packages = {}
for name, planes in samples.items():
    pkg = analyse(planes, name)
    prof = tuple(pkg["ranks"][ee] for ee in COORD_PAIRS)
    assert prof == DOCUMENTED_PROFILES[name], (name, prof)
    packages[name] = pkg
print("nine component packages computed; profiles match the theorem documents")


# ------------- branch samples (two generic points each) --------------------
def branch_planes(vv, xx, al, be):
    return [[(1, 0, al, -al), (0, 1, be, -be)],
            [(0, 0, 1, -1), tuple(vv)],
            [(1, -1, 0, 0), tuple(xx)],
            [(0, 0, 1, 1), (1, 1, 0, 0)]]


branchq = {
    "branchA#1": branch_planes((3, 5, 7, -7), (2, -9, 4, -4), sp.Rational(2, 3), sp.Rational(2, 3)),
    "branchA#2": branch_planes((-2, 9, 3, -3), (5, 4, -6, 6), sp.Rational(-5, 7), sp.Rational(-5, 7)),
    "branchB#1": branch_planes((2, -2, 5, -5), (3, 7, 4, -4), sp.Rational(1, 2), sp.Rational(-3, 5)),
    "branchB#2": branch_planes((-3, 3, 2, -2), (-1, 6, 5, -5), sp.Rational(4, 7), sp.Rational(1, 3)),
}
branch_packages = {name: analyse(pl, name) for name, pl in branchq.items()}
profA = tuple(branch_packages["branchA#1"]["ranks"][ee] for ee in COORD_PAIRS)
profB = tuple(branch_packages["branchB#1"]["ranks"][ee] for ee in COORD_PAIRS)
assert profA == (4, 3, 3, 4, 3, 3), profA
assert profB == (4, 4, 4, 3, 2, 3), profB
print("branch A profile:", profA, " (rank-2 relation at edge (0,2); rank-one")
print("   relations 1->3 supp{23}, 3->0 supp{01}, 3->2 supp{01})")
print("branch B profile:", profB, " (rank-2 relation at edge (1,2); r13=2 pencil")
print("   with rank-one lines 3->1 supp{01} and 1->3 supp{23}; 3->2 supp{01})")

# ------------- calibration -------------------------------------------------
d, v0_, v1_, v2_ = 2, 3, 5, 7
x1_, x2_ = 11, -4
x3_ = sp.Rational(-d * v0_ * x1_, v1_)
x0_ = sp.Rational(-(d * v0_ * x1_ + v1_ * (x2_ + x3_)), d * v1_)
alc, bec = sp.Rational(2, 3), sp.Rational(-1, 2)
cc9 = (-d * v1_, -d * v0_, v1_, v1_)
kk1, kk2, kk3 = (-cc9[1], cc9[0], 0, 0), (-cc9[2], 0, cc9[0], 0), (-cc9[3], 0, 0, cc9[0])
deep2 = [[tuple(kk1[j] + alc * kk3[j] for j in range(4)),
          tuple(kk2[j] + bec * kk3[j] for j in range(4))],
         [(0, 0, 1, -1), (v0_, v1_, v2_, -v2_)],
         [(1, 0, -d, 0), (x0_, x1_, x2_, x3_)],
         [(0, 0, 1, 1), (1, 0, d, 0)]]
q_deep2 = analyse(deep2, "overlap-one deep branch-2")
cal = {name: sieve(q_deep2, X) for name, X in packages.items()}
assert len(cal["first"]) == 1 and cal["first"][0] == ((0, 1, 2, 3), (0, 1, 2, 3)), cal["first"]
assert all(not res for name, res in cal.items() if name != "first")
print("calibration 1 PASSED: overlap-one deep branch-2 aligns ONLY with 'first'")
print("   (unique alignment sigma=id, pi=id), matching the note's identification")

zsym = sp.symbols("z0:4")
vF, xF, dF = (3, 5, -4, -9), (7, -7, -8, sp.Rational(-9, 5)), -3
Y2F, U3F = (1, 0, -dF, 0), (1, 0, dF, 0)
rowsF = []
for cpair in (rmul(Y2F, (0, 0, 1, 1)), rmul(list(xF), (0, 0, 1, 1))):
    zw = rmul(list(zsym), list(vF))
    form = pairing(zw, cpair)
    rowsF.append([sp.expand(sp.diff(form, zi)) for zi in zsym])
MF = sp.Matrix(rowsF)
mF = {}
for a_, b_ in itertools.combinations(range(4), 2):
    mF[(a_, b_)] = sp.expand(MF[0, a_] * MF[1, b_] - MF[0, b_] * MF[1, a_])
w2F = (mF[(1, 2)], -mF[(0, 2)], mF[(0, 1)], 0)
w3F = (mF[(1, 3)], -mF[(0, 3)], 0, mF[(0, 1)])
q_f4 = analyse([[w2F, w3F], [(0, 0, 1, -1), vF], [Y2F, xF], [(0, 0, 1, 1), U3F]], "F4")
resF = sieve(q_f4, packages["seventh"])
assert resF, "F4 must align with seventh"
print("calibration 2 PASSED: F4 branch point aligns with 'seventh'",
      f"({len(resF)} alignments)")

# ------------- the sieve ---------------------------------------------------
print("\nsieve of the two deep branches against all nine components:")
all_excluded = True
for qname, qpkg in branch_packages.items():
    for xname, X in packages.items():
        res = sieve(qpkg, X)
        verdict = "EXCLUDED" if not res else f"{len(res)} alignments"
        print(f"  {qname:10s} vs {xname:8s}: {verdict}")
        if res:
            all_excluded = False
assert all_excluded
print("\nRESULT: branch A and branch B are excluded from the closures of all")
print("nine certified components (every one of the 24x24 alignments fails an")
print("exact limit obstruction).  ALL CHECKS PASSED")
