#!/usr/bin/env python3
"""Find the extra incidence-tangent direction at the generic six-fold sample:
basis of the incidence tangent (Z-projection) modulo the family tangent."""
import itertools, sympy as sp

c0, c1, c2, t = sp.symbols("c0 c1 c2 t")
v = sp.symbols("v0:4")
x2, x3 = sp.symbols("x2 x3")
T0, T1, T2 = sp.symbols("tt0:3")
PERMS4 = tuple(itertools.permutations(range(4)))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

xrow = (t*v[0], t*v[1], x2, x3)
planes_sym = [
    sp.Matrix([[v[0], -v[1], 0, 0], [0, 0, 1, -c0]]),
    sp.Matrix([[0, 0, 1, -c1], list(v)]),
    sp.Matrix([[0, 0, 1, -c2], list(xrow)]),
    sp.Matrix([[0, 0, 1, 1], [0, 0, 1, -1]]),
]
torus = sp.diag(T0, T1, T2, 1)
planes_sym = [p*torus for p in planes_sym]
pivots = ((0, 2), (0, 2), (0, 2), (2, 3))
sample = {c0: 3, c1: -2, c2: 5, t: 2, v[0]: 3, v[1]: -7, v[2]: 2, v[3]: 5,
          x2: -1, x3: 4, T0: 1, T1: 1, T2: 1}
chart_coords = []
reduced = []
for plane, piv in zip(planes_sym, pivots):
    chart = plane[:, piv].inv() * plane
    nonpiv = tuple(i for i in range(4) if i not in piv)
    reduced.append(chart)
    chart_coords.extend(chart[r_, c_] for r_ in range(2) for c_ in nonpiv)
params = (c0, c1, c2, t, v[0], v[1], v[2], v[3], x2, x3, T0, T1, T2)
jac = sp.Matrix(chart_coords).jacobian(params).subs(sample)
jac = sp.Matrix([[sp.nsimplify(sp.cancel(e_)) for e_ in row] for row in jac.tolist()])

reduced_point = tuple(p.subs(sample) for p in reduced)
T_point = {}
for bits in itertools.product((0, 1), repeat=4):
    T_point[bits] = sp.nsimplify(perm4(tuple(tuple(reduced_point[m][bits[m], j] for j in range(4)) for m in range(4))))
anchor = (1, 0, 0, 0)
zvars = sp.symbols("Z0:16"); rvars = sp.symbols("R0:4")
universal = []
for mode, piv in enumerate(pivots):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    plane = sp.zeros(2, 4)
    plane[0, piv[0]] = 1; plane[1, piv[1]] = 1
    entries = zvars[4*mode: 4*mode+4]
    for r_ in range(2):
        for o_, cc in enumerate(nonpiv):
            plane[r_, cc] = entries[2*r_ + o_]
    universal.append(plane)
T_universal = {}
for bits in itertools.product((0, 1), repeat=4):
    T_universal[bits] = perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4)) for m in range(4)))
ratios = tuple(T_point[tuple((1-anchor[m_] if m_ == mode else anchor[m_]) for m_ in range(4))]/T_point[anchor]
               for mode in range(4))
equations = []
for word in itertools.product((0, 1), repeat=4):
    if word == anchor:
        continue
    monomial = sp.prod(rvars[m] for m in range(4) if word[m] != anchor[m])
    equations.append(sp.expand(T_universal[word] - T_universal[anchor]*monomial))
coordinate_point = tuple(sp.nsimplify(sp.cancel(c_.subs(sample))) for c_ in chart_coords)
substitution = dict(zip(tuple(zvars)+tuple(rvars), coordinate_point + ratios))
inc = sp.Matrix(equations).jacobian(tuple(zvars)+tuple(rvars)).subs(substitution)
ktang = inc.nullspace()
print("incidence tangent dim:", len(ktang))
# project to Z-coordinates (drop R rows), stack with family tangent columns
Zproj = [sp.Matrix([sp.nsimplify(k_[i]) for i in range(16)]) for k_ in ktang]
fam = [jac[:, j] for j in range(jac.cols)]
base = sp.Matrix.hstack(*fam)
print("family tangent (Z) rank:", base.rank())
aug = sp.Matrix.hstack(base, *Zproj)
print("family + incidence-tangent rank:", aug.rank())
# find combos of Zproj outside col(base): reduce
extra = []
cur = base
for kz in Zproj:
    trial = sp.Matrix.hstack(cur, kz)
    if trial.rank() > cur.rank():
        extra.append(kz)
        cur = trial
print("number of extra directions:", len(extra))
for kz in extra:
    print("extra tangent direction (Z0..Z15):")
    print([sp.nsimplify(sp.cancel(c_)) for c_ in kz.T])
# which chart entries are these? mode m entries Z[4m..4m+3] correspond to
# nonpivot columns of the reduced planes
print("\nreduced planes at sample (rows are chart bases):")
for m, rp in enumerate(reduced_point):
    print("mode", m, [[sp.nsimplify(c_) for c_ in rp.row(r_)] for r_ in range(2)], "pivots", pivots[m])
