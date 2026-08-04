#!/usr/bin/env python3
"""Conditional resolution of the Zc wall's ambient component.

The Zc1 family (s04/s09; sweep modes (0,1,2,3) = (U0, ybar-p, ybar-q,
u3-w)):
    U0 = span(u3, (Wc, 0, w2, 0)),   Wc = -(p3+q3) w2 / (p2 q3 + p3 q2),
    U1 = span(ybar, (0,1,p2,p3)),    U2 = span(ybar, (0,1,q2,q3)),
    U3 = span(u3, (0, Wc, w2, 0)),
identically pure (single word e_0110), generic profile (3,3,2,4,3,3)
with rank sum <= 18 on the closure (s09), family tangent rank 5, and
incidence Jacobian rank 13 (tangent dimension 7) at the exact sample
(p2,p3,q2,q3,w2) = (2,3,5,7,1): a doubly singular wall.

This script attempts the char-0 five-slice `ds` standard basis at the
sample (the step28 pattern) under a hard Singular timeout:
  * if the sliced local dimension is 0: the pure locus has local
    dimension <= 5, hence exactly 5 (family tangent 5), closure(F_Zc)
    is an irreducible component, and the same separation arguments as
    s06/s08 (rank sum 18 < 19, 21; sixfolds by local dimension) make it
    a FOURTEENTH component orbit -- the script then asserts the full
    chain and says so;
  * if the timeout is hit (recorded null) or the sliced dimension is
    positive, the script reports the Zc ambient component as OPEN
    (candidates: a wall of the seventh -- the only sieve-compatible
    certified component with a rank-2 pair edge -- or a new component),
    and exits cleanly WITHOUT claiming a census change."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}


YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)
p2, p3, q2, q3, w2 = sp.symbols("p2 p3 q2 q3 w2")
Wc = -(p3 + q3)*w2/(p2*q3 + p3*q2)
planes_sym_raw = [
    [U3v, (Wc, 0, w2, 0)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, Wc, w2, 0)],
]
sample = {p2: 2, p3: 3, q2: 5, q3: 7, w2: 1}

# family tangent rank 5 with the full projective torus
t0, t1, t2 = sp.symbols("t0:3")
torus = sp.diag(t0, t1, t2, 1)
planes_sym = [sp.Matrix([[sp.sympify(c) for c in row] for row in pl])*torus
              for pl in planes_sym_raw]
pivots = ((0, 2), (0, 1), (0, 1), (1, 2))
params = (p2, p3, q2, q3, w2, t0, t1, t2)
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
print("family tangent rank (5 params + full torus) = 5.  OK")

# incidence rank 13 at the sample
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
assert J.rank() == 13
print("incidence Jacobian rank 13 (tangent dimension 7): doubly singular.  OK")

# the slice attempt (char 0, then char 31991 as modular evidence)
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


def run_slice(char, timeout_s):
    polys = ";\n".join(f"poly g{i}={str(pp).replace('**','^')}"
                       for i, pp in enumerate(shifted + slices))
    program = "\n".join((
        f"ring R={char},({varnames}),ds;",
        polys + ";",
        "ideal I=" + ",".join(f"g{i}" for i in range(len(shifted) + len(slices))) + ";",
        "option(redSB);",
        "ideal J=std(I);",
        '"SLICE_LOCAL_DIM:"+string(dim(J));',
        "quit;",
    ))
    try:
        completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                                   encoding="utf-8", errors="replace",
                                   capture_output=True, timeout=timeout_s, check=False)
    except subprocess.TimeoutExpired:
        return None
    out = completed.stdout
    if "SLICE_LOCAL_DIM:" not in out:
        return None
    return int(out.split("SLICE_LOCAL_DIM:")[1].split()[0])


dim0 = run_slice("0", 3600)
print("char-0 five-slice local dimension:", "NULL (timeout)" if dim0 is None else dim0)
if dim0 == 0:
    # componenthood + separations (the s06/s08 chain)
    RANK_BOUNDS = {(0, 3): 2}
    for a_, b_ in COORD_PAIRS:
        rows_ = []
        for pa in planes_sym_raw[a_]:
            for pb in planes_sym_raw[b_]:
                prod = rmul(tuple(sp.sympify(c) for c in pa),
                            tuple(sp.sympify(c) for c in pb))
                rows_.append([sp.together(prod[ab]) for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        bound = RANK_BOUNDS.get((a_, b_), 3 if (a_, b_) != (1, 2) else 4)
        if bound < 4:
            for rr in itertools.combinations(range(4), bound + 1):
                for cc in itertools.combinations(range(6), bound + 1):
                    assert sp.cancel(sp.together(mm[rr, cc].det())) == 0
    print("CERTIFIED: local dimension exactly 5; closure(F_Zc) is an")
    print("irreducible component with rank sum <= 18 on its closure:")
    print("distinct from every certified fivefold (rank-sum-21/19 samples)")
    print("and every sixfold (local dimension): a FOURTEENTH component orbit.")
else:
    dimp = run_slice("31991", 1800)
    print("char-31991 five-slice local dimension:",
          "NULL (timeout)" if dimp is None else dimp, "(modular evidence only)")
    print("VERDICT: the ambient component of the Zc wall remains OPEN")
    print("(candidates: a wall of the SEVENTH, the only sieve-compatible")
    print("certified component with a rank-2 pair edge, or a new component).")
print()
print("ALL CHECKS PASSED (conditional verdict above)")
