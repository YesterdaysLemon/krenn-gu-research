#!/usr/bin/env python3
"""Local dimension at the generic six-fold sample: R-eliminated incidence
equations (11) in the 16 chart vars, ds ordering, char 31991 (then char 0 by
hand if feasible).  Equations: T[word]*T[anchor]^{k-1} - prod(T[flip_m]) over
the flipped modes -- the standard multi-flip elimination of the ratios."""
import itertools, subprocess, sys, sympy as sp

c0, c1, c2, t = sp.symbols("c0 c1 c2 t")
v = sp.symbols("v0:4")
x2, x3 = sp.symbols("x2 x3")
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
pivots = ((0, 2), (0, 2), (0, 2), (2, 3))
sample = {c0: 3, c1: -2, c2: 5, t: 2, v[0]: 3, v[1]: -7, v[2]: 2, v[3]: 5, x2: -1, x3: 4}
coordinate_point = []
for plane, piv in zip(planes_sym, pivots):
    chart = (plane[:, piv].inv() * plane).subs(sample)
    nonpiv = tuple(i for i in range(4) if i not in piv)
    coordinate_point.extend(sp.nsimplify(chart[r_, cc]) for r_ in range(2) for cc in nonpiv)

zvars = sp.symbols("Z0:16")
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
T_u = {}
for bits in itertools.product((0, 1), repeat=4):
    T_u[bits] = perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4)) for m in range(4)))
anchor = (1, 0, 0, 0)
equations = []
for word in itertools.product((0, 1), repeat=4):
    flips = [m for m in range(4) if word[m] != anchor[m]]
    if len(flips) < 2:
        continue
    lhs = sp.expand(T_u[word] * T_u[anchor]**(len(flips)-1))
    rhs = sp.prod(T_u[tuple((1-anchor[m] if m == mm else anchor[m]) for m in range(4))] for mm in flips)
    equations.append(sp.expand(lhs - sp.expand(rhs)))
print("equations:", len(equations), file=sys.stderr)
subs0 = dict(zip(zvars, coordinate_point))
assert all(sp.simplify(eq.subs(subs0)) == 0 for eq in equations)
shifted = []
for eq in equations:
    poly = sp.expand(eq.subs({zv: zv + val for zv, val in subs0.items()}))
    den = 1
    for coeff in sp.Poly(poly, *zvars).coeffs():
        den = sp.lcm(den, sp.denom(sp.nsimplify(coeff)))
    shifted.append(sp.expand(poly*den))
char = sys.argv[1] if len(sys.argv) > 1 else "31991"
varnames = ",".join(str(w) for w in zvars)
polys = ";\n".join(f"poly g{i}={str(p_).replace('**','^')}" for i, p_ in enumerate(shifted))
program = "\n".join((
    f"ring R={char},({varnames}),ds;",
    polys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(shifted))) + ";",
    "option(redSB);",
    "ideal J=std(I);",
    '"CODEX_LOCAL_DIM:"+string(dim(J));',
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=480, check=False)
print(completed.stdout)
if completed.stderr.strip():
    print("STDERR:", completed.stderr[-1200:])
