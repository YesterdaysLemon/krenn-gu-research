#!/usr/bin/env python3
"""Local dimension of the pure locus at the W-sample: flattening-minors ideal
in the 16 plane-chart variables, local ordering ds, char p then char 0.
Pure locus near the sample = {three 4x4 pair flattenings rank <= 1}; the
nonzero-tensor condition holds in a neighbourhood (T_anchor != 0)."""
import itertools, subprocess, sys, sympy as sp

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

sample = {e: 3, v[0]: 2, v[1]: 5, v[2]: 7, v[3]: -11, x[0]: 2, x[1]: 5, x[2]: 13, x[3]: -4}
vv = tuple(sample[k] for k in v); xx = tuple(sample[k] for k in x); ee = sample[e]
rows = []
for c in (rmul([0, 0, 1, -ee], Y3), rmul(list(xx), Y3)):
    form = pairing(rmul(list(z), list(vv)), c)
    rows.append([sp.nsimplify(sp.diff(form, zi)) for zi in z])
M = sp.Matrix(rows)
ker = M.nullspace(); assert len(ker) == 2
planes = (
    sp.Matrix([[sp.nsimplify(c) for c in k] for k in ker]),
    sp.Matrix([list(U1_A), list(vv)]),
    sp.Matrix([[0, 0, 1, -ee], list(xx)]),
    sp.Matrix([list(Y3), [0, 0, 1, ee]]),
)
pivots = ((0, 2), (0, 2), (0, 2), (2, 3))
coordinate_point = []
for plane, piv in zip(planes, pivots):
    chart = plane[:, piv].inv() * plane
    nonpiv = tuple(i for i in range(4) if i not in piv)
    coordinate_point.extend(sp.nsimplify(chart[r_, c_]) for r_ in range(2) for c_ in nonpiv)

zvars = sp.symbols("Z0:16")
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
for bits in itertools.product((0, 1), repeat=4):
    T_universal[bits] = perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4)) for m in range(4)))

minors = set()
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    mat = {}
    for bits in itertools.product((0, 1), repeat=4):
        r_ = (bits[left[0]], bits[left[1]])
        c_ = (bits[right[0]], bits[right[1]])
        mat[(r_, c_)] = T_universal[bits]
    rk = sorted({k[0] for k in mat}); ck = sorted({k[1] for k in mat})
    for r1, r2 in itertools.combinations(rk, 2):
        for c1, c2 in itertools.combinations(ck, 2):
            mm = sp.expand(mat[(r1, c1)]*mat[(r2, c2)] - mat[(r1, c2)]*mat[(r2, c1)])
            if mm != 0:
                minors.add(mm)
minors = sorted(minors, key=sp.default_sort_key)
print("distinct nonzero flattening 2x2 minors:", len(minors), file=sys.stderr)

# verify they vanish at the sample point
subs0 = dict(zip(zvars, coordinate_point))
assert all(sp.simplify(m.subs(subs0)) == 0 for m in minors)

# shift to origin, clear denominators
shifted = []
for m in minors:
    poly = sp.expand(m.subs({zv: zv + val for zv, val in subs0.items()}))
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
    "ideal J=std(I);",
    '"CODEX_LOCAL_DIM:"+string(dim(J));',
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=520, check=False)
print(completed.stdout)
if completed.stderr.strip():
    print("STDERR:", completed.stderr[-1500:])
