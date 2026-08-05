#!/usr/bin/env python3
"""Local dimension of the pure-compression incidence at the W-sample via
Singular local ordering (ds).  Incidence: 15 equations in 20 vars (16 plane
chart coords + 4 ratios), translated so the sample is the origin."""
import itertools, subprocess, sympy as sp

e = sp.Symbol("e")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
z = sp.symbols("z0:4")

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

# exact W-sample planes (same as step5)
sample = {e: 3, v[0]: 2, v[1]: 5, v[2]: 7, v[3]: -11, x[0]: 2, x[1]: 5, x[2]: 13, x[3]: -4}
vv = tuple(sample[k] for k in v); xx = tuple(sample[k] for k in x); ee = sample[e]
rows = []
for c in (rmul([0,0,1,-ee], Y3), rmul(list(xx), Y3)):
    form = pairing(rmul(list(z), list(vv)), c)
    rows.append([sp.nsimplify(sp.diff(form, zi)) for zi in z])
M = sp.Matrix(rows)
ker = M.nullspace(); assert len(ker) == 2
planes = (
    sp.Matrix([[sp.nsimplify(c) for c in k] for k in ker]),
    sp.Matrix([list(U1_A), list(vv)]),
    sp.Matrix([[0,0,1,-ee], list(xx)]),
    sp.Matrix([list(Y3), [0,0,1,ee]]),
)
pivots = ((0, 2), (0, 2), (0, 2), (2, 3))
reduced = []
coordinate_point = []
for plane, piv in zip(planes, pivots):
    chart = plane[:, piv].inv() * plane
    reduced.append(chart)
    nonpiv = tuple(i for i in range(4) if i not in piv)
    coordinate_point.extend(sp.nsimplify(chart[r_, c_]) for r_ in range(2) for c_ in nonpiv)

T_point = {}
for bits in itertools.product((0,1), repeat=4):
    T_point[bits] = sp.nsimplify(perm4(tuple(tuple(reduced[m][bits[m], j] for j in range(4)) for m in range(4))))
anchor = next(b for b in itertools.product((0,1), repeat=4) if T_point[b] != 0)
ratios = tuple(T_point[tuple((1-anchor[m_] if m_ == mode else anchor[m_]) for m_ in range(4))] / T_point[anchor]
               for mode in range(4))
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
equations = []
for word in itertools.product((0,1), repeat=4):
    if word == anchor:
        continue
    monomial = sp.prod(rvars[m] for m in range(4) if word[m] != anchor[m])
    equations.append(sp.expand(T_universal[word] - T_universal[anchor]*monomial))
point_vals = dict(zip(tuple(zvars)+tuple(rvars), tuple(coordinate_point)+ratios))
assert all(sp.simplify(eq.subs(point_vals)) == 0 for eq in equations)

# translate to origin: X -> X + p ; clear denominators (point is rational)
shifted = []
for eq in equations:
    sub = {var: var + val for var, val in point_vals.items()}
    poly = sp.expand(eq.subs(sub))
    poly = sp.nsimplify(poly)
    # clear rational denominators
    denlcm = 1
    for coeff in sp.Poly(poly, *(tuple(zvars)+tuple(rvars))).coeffs():
        denlcm = sp.lcm(denlcm, sp.denom(sp.nsimplify(coeff)))
    shifted.append(sp.expand(poly*denlcm))
varnames = ",".join([str(w) for w in zvars] + [str(r) for r in rvars])
polys = ";\n".join(f"poly g{i}={str(p).replace('**','^')}" for i, p in enumerate(shifted))
program = "\n".join((
    f"ring R=0,({varnames}),ds;",
    polys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(shifted))) + ";",
    "ideal J=std(I);",
    '"CODEX_LOCAL_DIM:"+string(dim(J));',
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=590, check=False)
print(completed.stdout[-3000:])
if completed.stderr.strip():
    print("STDERR:", completed.stderr[-2000:])
