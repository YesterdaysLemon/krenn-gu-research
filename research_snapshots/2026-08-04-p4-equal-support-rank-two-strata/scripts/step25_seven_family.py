#!/usr/bin/env python3
"""Test the U3-deformation: U3 = span((0,0,1,0)+a3*(v0,v1,0,0),
(0,0,0,1)+b3*(v0,v1,0,0)).  Compute purity minors on the extended family."""
import itertools, sympy as sp

c0, c1, c2, t, a3, b3 = sp.symbols("c0 c1 c2 t a3 b3")
v = sp.symbols("v0:4")
x2, x3 = sp.symbols("x2 x3")
PERMS4 = tuple(itertools.permutations(range(4)))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

w01 = (v[0], v[1], 0, 0)
xrow = (t*v[0], t*v[1], x2, x3)
planes = [
    [(v[0], -v[1], 0, 0), (0, 0, 1, -c0)],
    [(0, 0, 1, -c1), tuple(v)],
    [(0, 0, 1, -c2), tuple(xrow)],
    [(a3*v[0], a3*v[1], 1, 0), (b3*v[0], b3*v[1], 0, 1)],
]
T = {}
for bits in itertools.product((0, 1), repeat=4):
    T[bits] = sp.expand(perm4(tuple(planes[m][bits[m]] for m in range(4))))
nz = [(b, sp.factor(val)) for b, val in T.items() if val != 0]
print("nonzero entries:", len(nz))
for b, val in nz:
    print("  T%s = %s" % ("".join(map(str, b)), val))

minors = set()
for left, right in (((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))):
    mat = {}
    for bits in itertools.product((0,1), repeat=4):
        mat[((bits[left[0]], bits[left[1]]), (bits[right[0]], bits[right[1]]))] = T[bits]
    rk = sorted({k[0] for k in mat}); ck = sorted({k[1] for k in mat})
    for r1, r2 in itertools.combinations(rk, 2):
        for cc1, cc2 in itertools.combinations(ck, 2):
            mm = sp.expand(mat[(r1, cc1)]*mat[(r2, cc2)] - mat[(r1, cc2)]*mat[(r2, cc1)])
            if mm != 0:
                minors.add(sp.factor(mm))
print("\nnonzero purity minors:", len(minors))
for mm in sorted(minors, key=lambda z: len(str(z)))[:12]:
    print("  ", mm)
