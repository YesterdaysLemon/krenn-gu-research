#!/usr/bin/env python3
"""Exact local-dimension upper bound for C10 at the generic sample, char 0.

Slice certificate: with V the variety cut out near the sample by the
ratio-eliminated purity equations (the same eleven multi-flip equations
as step26, shifted so the sample is the origin), intersect with SIX
fixed rational linear forms through the origin and compute the LOCAL
dimension at the origin with a ds standard basis.

Logic (valid for ANY choice of the six forms, genericity not needed):
    dim_0(V cap L) >= dim_0(V) - 6,
so if the sliced local dimension is ZERO then dim_0(V) <= 6.  The pure
locus is contained in V (the multi-flip equations are flattening-minor
consequences), so the pure locus has local dimension <= 6 at the
sample; the C10 family tangent has rank 6 there (step23), so the local
dimension is EXACTLY six and closure(C10) is an irreducible component
of the pure locus.

Default char 0 (exact).  Optional argv prime replays the same slice
modulo p."""
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
assert len(equations) == 11
subs0 = dict(zip(zvars, coordinate_point))
assert all(sp.simplify(eq.subs(subs0)) == 0 for eq in equations)
shifted = []
for eq in equations:
    poly = sp.expand(eq.subs({zv: zv + val for zv, val in subs0.items()}))
    den = 1
    for coeff in sp.Poly(poly, *zvars).coeffs():
        den = sp.lcm(den, sp.denom(sp.nsimplify(coeff)))
    shifted.append(sp.expand(poly*den))

# six fixed rational linear slices through the origin (small deterministic
# integer coefficients; validity of the upper bound needs no genericity)
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
    (2, 1, 1, -1, 3, -2, 1, 1, 2, -1, 1, 1, -2, 3, 1, 1),
)
slices = [sum(cc*zz for cc, zz in zip(row, zvars)) for row in SLICE_COEFFS]

char = sys.argv[1] if len(sys.argv) > 1 else "0"
varnames = ",".join(str(w) for w in zvars)
polys = ";\n".join(f"poly g{i}={str(p_).replace('**','^')}" for i, p_ in enumerate(shifted + slices))
program = "\n".join((
    f"ring R={char},({varnames}),ds;",
    polys + ";",
    "ideal I=" + ",".join(f"g{i}" for i in range(len(shifted) + len(slices))) + ";",
    "option(redSB);",
    "ideal J=std(I);",
    '"SLICE_LOCAL_DIM:"+string(dim(J));',
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=3000, check=False)
print(completed.stdout)
if completed.stderr.strip():
    print("STDERR:", completed.stderr[-1200:])
out = completed.stdout
assert "SLICE_LOCAL_DIM:" in out, "Singular did not return a dimension"
dim_val = int(out.split("SLICE_LOCAL_DIM:")[1].split()[0])
print("sliced local dimension at the sample (char %s): %d" % (char, dim_val))
if dim_val == 0:
    print("CERTIFIED: local dim of the purity variety at the sample <= 6;")
    print("with family tangent rank 6 (step23): local dimension EXACTLY 6,")
    print("so closure(C10) is an irreducible component of the pure locus.")
else:
    print("INCONCLUSIVE at this slice: upper bound is %d + 6" % dim_val)
