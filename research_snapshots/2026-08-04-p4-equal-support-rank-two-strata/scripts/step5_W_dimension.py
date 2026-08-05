#!/usr/bin/env python3
"""W-branch: family tangent rank (with full projective torus) and universal
Segre-incidence Jacobian rank at the exact sample."""
import itertools, sympy as sp

e = sp.Symbol("e")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
z = sp.symbols("z0:4")
t0, t1, t2 = sp.symbols("t0:3")

U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab))) for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def pairing(P, Q):
    return sp.expand(sum(P[ab]*Q[COMPLEMENT[ab]] for ab in COORD_PAIRS))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

# --- family on W: x0 = v0*x1/v1 (so v1*x0-v0*x1=0), U0 = Cramer kernel (0,2)-pivot
x0_val = v[0]*x[1]/v[1]
subsW = {x[0]: x0_val}
xxW = [sp.sympify(c).subs(subsW) for c in x]

def covector_matrix(xrow):
    rows = []
    for c in (rmul([0, 0, 1, -e], Y3), rmul(list(xrow), Y3)):
        form = pairing(rmul(list(z), list(v)), c)
        rows.append([sp.expand(sp.diff(form, zi)) for zi in z])
    return sp.Matrix(rows)

M = covector_matrix(xxW)
piv02 = sp.together(M[0, 0]*M[1, 2] - M[0, 2]*M[1, 0])
wA = (-(M[0,1]*M[1,2]-M[0,2]*M[1,1]), piv02, -(M[0,0]*M[1,1]-M[0,1]*M[1,0]), 0)
wB = (-(M[0,3]*M[1,2]-M[0,2]*M[1,3]), 0, -(M[0,0]*M[1,3]-M[0,3]*M[1,0]), piv02)
for w in (wA, wB):
    assert all(sp.simplify(sum(M[r_, c_]*w[c_] for c_ in range(4))) == 0 for r_ in range(2))

planes = (
    sp.Matrix([list(wA), list(wB)]),
    sp.Matrix([list(U1_A), list(v)]),
    sp.Matrix([[0, 0, 1, -e], list(xxW)]),
    sp.Matrix([list(Y3), [0, 0, 1, e]]),
)
torus = sp.diag(t0, t1, t2, 1)
planes = tuple(p*torus for p in planes)
pivots = ((0, 2), (0, 2), (0, 2), (2, 3))
sample = {e: 3, v[0]: 2, v[1]: 5, v[2]: 7, v[3]: -11, x[1]: 5, x[2]: 13, x[3]: -4,
          t0: 1, t1: 1, t2: 1}

chart_coords = []
reduced = []
for plane, piv in zip(planes, pivots):
    chart = plane[:, piv].inv() * plane
    nonpiv = tuple(i for i in range(4) if i not in piv)
    reduced.append(chart)
    chart_coords.extend(chart[r_, c_] for r_ in range(2) for c_ in nonpiv)

params = (e, v[0], v[1], v[2], v[3], x[1], x[2], x[3], t0, t1, t2)
jac = sp.Matrix(chart_coords).jacobian(params).subs(sample)
jac = sp.Matrix([[sp.nsimplify(sp.cancel(c)) for c in row] for row in jac.tolist()])
print("W-branch family tangent rank (with full projective torus):", jac.rank())

# --- universal Segre-incidence at the sample
reduced_point = tuple(p.subs(sample) for p in reduced)
T_point = {}
for bits in itertools.product((0,1), repeat=4):
    T_point[bits] = sp.nsimplify(perm4(tuple(tuple(reduced_point[m][bits[m], j] for j in range(4)) for m in range(4))))
nz = [b for b, val in T_point.items() if val != 0]
print("nonzero words at sample:", nz)
anchor = nz[0]
zvars = sp.symbols("Z0:16")
rvars = sp.symbols("R0:4")
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
T_universal = {}
for bits in itertools.product((0,1), repeat=4):
    T_universal[bits] = perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4)) for m in range(4)))
ratios = tuple(T_point[tuple((1-anchor[m_] if m_ == mode else anchor[m_]) for m_ in range(4))] / T_point[anchor]
               for mode in range(4))
equations = []
for word in itertools.product((0,1), repeat=4):
    if word == anchor:
        continue
    monomial = sp.prod(rvars[m] for m in range(4) if word[m] != anchor[m])
    equations.append(sp.expand(T_universal[word] - T_universal[anchor]*monomial))
coordinate_point = tuple(sp.nsimplify(sp.cancel(c.subs(sample))) for c in chart_coords)
substitution = dict(zip(tuple(zvars)+tuple(rvars), coordinate_point + ratios))
assert all(sp.simplify(eq.subs(substitution)) == 0 for eq in equations)
inc_jac = sp.Matrix(equations).jacobian(tuple(zvars)+tuple(rvars)).subs(substitution)
r = inc_jac.rank()
print("universal Segre-incidence Jacobian rank:", r, " => local dim >=", 20 - r, "(= dim if smooth/15)")
