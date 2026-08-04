#!/usr/bin/env python3
"""Family tangent rank and incidence Jacobian rank at a generic sample of the
six-parameter family (candidate tenth component, dimension six)."""
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
print("family tangent rank (13 params incl. full torus):", jac.rank())

reduced_point = tuple(p.subs(sample) for p in reduced)
T_point = {}
for bits in itertools.product((0, 1), repeat=4):
    T_point[bits] = sp.nsimplify(perm4(tuple(tuple(reduced_point[m][bits[m], j] for j in range(4)) for m in range(4))))
anchor = next(b for b in itertools.product((0, 1), repeat=4) if T_point[b] != 0)
print("anchor:", anchor)
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
assert all(sp.simplify(eq.subs(substitution)) == 0 for eq in equations)
inc = sp.Matrix(equations).jacobian(tuple(zvars)+tuple(rvars)).subs(substitution)
r = inc.rank()
print("incidence Jacobian rank:", r, "=> smooth local dimension", 20 - r, "if rank corresponds")
