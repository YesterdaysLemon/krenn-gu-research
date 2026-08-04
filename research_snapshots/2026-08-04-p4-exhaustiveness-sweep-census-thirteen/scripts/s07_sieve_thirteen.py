#!/usr/bin/env python3
"""The complete semicontinuity sieve of the (b2) rank-2 branch samples
against all ELEVEN certified components, calibrated as in
branch_invariants_and_sieve.py, plus the closed-invariant cross-checks
used by the twelfth/thirteenth separations:

  - triple-span invariant: dim(U_I+U_J+U_L) <= 3 on all of closure(tenth)
    (verified on the family), while every mode-triple spans C^4 at the
    Zb1/Zb2/Za2/Za3 samples: these branches lie in NO census image of the
    tenth's closure (independent of the sieve);
  - coordinate-plane invariant (step29): every point of closure(C10) has
    a coordinate 2-plane among its planes; the Zb/Za2/Za3 samples have
    none: not in the eleventh's orbit closure;
  - the seventh is excluded at every branch sample by rank monotonicity
    through its generic rank-2 edge (all branch pair ranks are >= 3 at
    Za*/Zb*).

Sieve verdicts (necessary-condition filter over all 24x24 alignments):
  Za1 -> only 'tenth' passes (it IS a tenth wall: s05);
  Za2, Za3 -> only 'tenth' passes, but the triple-span invariant excludes
    the tenth: no certified closure contains them;
  Zb1, Zb2 -> only 'dq' passes, and dq is excluded by the componenthood/
    profile argument of s06 (and Zc -> 'first'/'seventh' pass; s09).
"""
import itertools, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def proportional(u, w):
    return all(sp.simplify(u[i]*w[j] - u[j]*w[i]) == 0
               for i, j in itertools.combinations(range(4), 2))


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
    uvec = tuple(sp.simplify(uc[0]*planes[a_][0][j] + uc[1]*planes[a_][1][j]) for j in range(4))
    yvec = tuple(sp.simplify(yc[0]*planes[b_][0][j] + yc[1]*planes[b_][1][j]) for j in range(4))
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
                kA = [sp.simplify(c_) for c_ in null[0]]
                kB = [sp.simplify(c_) for c_ in null[1]]
                A2 = sp.Matrix([[kA[0], kA[1]], [kA[2], kA[3]]])
                B2 = sp.Matrix([[kB[0], kB[1]], [kB[2], kB[3]]])
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
    return {"label": label, "ranks": ranks, "lows": lows}


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


# ---------------- eleven certified component samples ------------------------
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
DOCUMENTED_PROFILES = {
    "first": (4, 4, 4, 3, 3, 3), "dq": (4, 4, 3, 4, 3, 3),
    "L1": (4, 4, 3, 4, 3, 3), "L2": (4, 4, 3, 4, 3, 3), "L3": (4, 4, 3, 4, 3, 3),
    "sixth": (4, 4, 3, 4, 3, 3), "seventh": (4, 3, 2, 4, 4, 3),
    "eighth": (4, 4, 3, 4, 3, 3), "ninth": (4, 4, 4, 3, 3, 3),
    "tenth": (3, 3, 4, 3, 4, 4), "eleventh": (4, 4, 3, 4, 3, 3),
}
packages = {}
for name, planes in samples.items():
    pkg = analyse(planes, name)
    prof = tuple(pkg["ranks"][e_] for e_ in COORD_PAIRS)
    assert prof == DOCUMENTED_PROFILES[name], (name, prof)
    packages[name] = pkg
print("eleven component packages computed; profiles match the documents")

# calibration 1: the tenth family point in sweep-mode order aligns with tenth
cal = analyse([[(1, 7, 0, 0), (0, 11, 1, -5)], [(1, -1, 0, 0), (0, 1, 2, -10)],
               [(1, -1, 0, 0), (0, 1, 3, -15)], [(1, 1, 0, 0), (0, 0, 1, 5)]],
              "tenth-sweep-modes")
assert sieve(cal, packages["tenth"])
# calibration 2: Za1 (a proven tenth wall, s05) must pass vs tenth
z = sp.symbols("z0:4")
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)
za1 = [[U3v, (0, 0, 1, 5)], [YBAR, (0, 1, 2, -10)], [YBAR, (0, 1, 3, -15)],
       [U3v, (0, 7, 1, -5)]]
pkg_za1 = analyse(za1, "Za1")
assert sieve(pkg_za1, packages["tenth"])
print("calibrations PASSED (tenth self-alignment; Za1 vs tenth)")

# ---------------- branch samples --------------------------------------------
branches = {
    "Za1": za1,
    "Za2": [[U3v, (1, 0, -1, 7)], [YBAR, (0, 1, 2, -10)], [YBAR, (0, 1, 3, -15)],
            [U3v, (0, sp.Rational(1, 6), 1, 7)]],
    "Za3": [[U3v, (-1, 0, -1, 7)], [YBAR, (0, 1, 2, -10)], [YBAR, (0, 1, 3, -15)],
            [U3v, (0, sp.Rational(-1, 6), 1, 7)]],
    "Zb1": [[U3v, (0, 0, -1, 2)], [YBAR, (0, 1, 3, -1)], [YBAR, (0, 1, 5, -15)],
            [U3v, (0, 0, 1, 2)]],
    "Zb2": [[U3v, (0, 0, -1, 2)], [YBAR, (0, 1, 3, -1)], [YBAR, (0, 1, 5, 17)],
            [U3v, (0, 0, 1, 2)]],
    "Zc1": [[U3v, (-10, 0, 29, 0)], [YBAR, (0, 1, 2, 3)], [YBAR, (0, 1, 5, 7)],
            [U3v, (0, sp.Rational(-10, 29), 1, 0)]],
    "Zc2": [[U3v, (10, 0, 29, 0)], [YBAR, (0, 1, 2, 3)], [YBAR, (0, 1, 5, 7)],
            [U3v, (0, sp.Rational(10, 29), 1, 0)]],
}
verdicts = {}
for bname, planes in branches.items():
    qpkg = analyse(planes, bname)
    row = {}
    for xname, X in packages.items():
        res = sieve(qpkg, X)
        row[xname] = len(res)
    verdicts[bname] = row
    passing = {kk: n for kk, n in row.items() if n}
    print(f"  {bname}: passing alignments: {passing if passing else 'NONE'}")
assert set(kk for kk, n in verdicts["Za1"].items() if n) == {"tenth"}
assert set(kk for kk, n in verdicts["Za2"].items() if n) == {"tenth"}
assert set(kk for kk, n in verdicts["Za3"].items() if n) == {"tenth"}
assert set(kk for kk, n in verdicts["Zb1"].items() if n) == {"dq"}
assert set(kk for kk, n in verdicts["Zb2"].items() if n) == {"dq"}
assert set(kk for kk, n in verdicts["Zc1"].items() if n) <= {"first", "seventh"}
assert set(kk for kk, n in verdicts["Zc2"].items() if n) <= {"first", "seventh"}

# ---------------- the triple-span closed invariant of the tenth --------------
b, e, k, m, r = sp.symbols("b e k m r")
tenth_fam = [[(1, -1, 0, 0), (0, 1, b, -b*k)],
             [(1, -1, 0, 0), (0, 1, e, -e*k)],
             [(1, 1, 0, 0), (0, 0, 1, k)],
             [(1, m, 0, 0), (0, r, 1, -k)]]
stack = sp.Matrix([list(row) for pl in (tenth_fam[0], tenth_fam[1], tenth_fam[3])
                   for row in pl])
for rows in itertools.combinations(range(6), 4):
    assert sp.expand(stack[rows, :].det()) == 0
print("triple-span invariant: dim(U_I+U_J+U_L) <= 3 identically on the")
print("tenth's family (hence on its closure).")
for bname in ("Za2", "Za3", "Zb1", "Zb2"):
    planes = branches[bname]
    for tri in itertools.combinations(range(4), 3):
        M6 = sp.Matrix([list(row) for mmode in tri for row in planes[mmode]])
        assert M6.rank() == 4, (bname, tri)
    print(f"  {bname}: every mode-triple spans C^4 -> not in any census image")
    print(f"        of closure(tenth).")

# coordinate-plane invariant (eleventh): none of the Za2/Za3/Zb planes is a
# coordinate plane
def is_coordinate_plane(rows, pair):
    comp = tuple(i for i in range(4) if i not in pair)
    off = sp.Matrix([[rows[r_][c] for c in comp] for r_ in range(2)])
    on = sp.Matrix([[rows[r_][c] for c in pair] for r_ in range(2)])
    return off.is_zero_matrix and on.det() != 0


for bname in ("Za2", "Za3", "Zb1", "Zb2", "Zc1", "Zc2"):
    for pl in branches[bname]:
        assert not any(is_coordinate_plane([list(pl[0]), list(pl[1])], pair)
                       for pair in COORD_PAIRS), (bname, pl)
print("coordinate-plane invariant: no branch sample has a coordinate plane:")
print("none lies in the eleventh's orbit closure (step29 invariant).")
print()
print("ALL CHECKS PASSED")
