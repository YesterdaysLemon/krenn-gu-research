#!/usr/bin/env python3
"""Find a rational sample on the star rank-two purity curve and compute its
invariants: profile, relation ranks, nonzeroness, kernels."""
import itertools, sympy as sp

n2, n3 = sp.symbols("n2 n3")
s2s = sp.Symbol("sigma2")
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

# constraint prime (from step12):
def constraints(e1v, e2v, e3v, n2v, n3v):
    c1 = (n2v**2*n3v - n2v**2 - n2v*n3v**2 + n2v*n3v)*e2v \
         + (2*n2v**3*n3v - 4*n2v**3 - 2*n2v**2*n3v**2 + 6*n2v**2*n3v - 2*n2v*n3v**2)*e3v \
         + (-n3v**2 + 2*n3v - 1)
    c2 = (n3v - 1)*e1v + (3*n2v**2 - 3*n2v*n3v)*e3v
    return sp.expand(c1), sp.expand(c2)

# rational sample hunt: fix sigma0, sigma1, n2; solve c2 for sigma2 (linear); then c1
# becomes a rational equation in n3: scan rational n3 candidates via roots.
found = None
for sg0, sg1, n2v in [(1, 2, 2), (1, 3, 2), (2, 3, 2), (1, 2, 3), (1, -2, 2), (2, -1, 3), (1, 4, 2), (3, 1, 2)]:
    e1s = sg0 + sg1 + s2s
    e2s = sg0*sg1 + (sg0 + sg1)*s2s
    e3s = sg0*sg1*s2s
    c1, c2 = constraints(e1s, e2s, e3s, n2v, n3)
    sol2 = sp.solve(c2, s2s)
    if not sol2:
        continue
    s2sol = sol2[0]
    poly = sp.expand(sp.numer(sp.together(c1.subs(s2s, s2sol))))
    roots = sp.roots(sp.Poly(poly, n3), filter="Q")
    for r_ in roots:
        if r_ in (0, 1) or r_ == n2v:
            continue
        s2v = sp.nsimplify(s2sol.subs(n3, r_))
        if s2v in (sg0, sg1):
            continue
        found = (sg0, sg1, s2v, n2v, r_)
        break
    if found:
        break
print("sample (sigma0, sigma1, sigma2, n2, n3):", found)
assert found
sg0, sg1, sg2, n2v, n3v = found

Y3 = sp.Matrix([1, 1, 1, 1])
X3 = sp.Matrix([0, 1, n2v, n3v])
un = sp.symbols("a0:4 b0:4")
y0v = sp.Matrix(un[:4]); x0v = sp.Matrix(un[4:])
eqs = [sp.expand(y0v[a]*X3[b] + y0v[b]*X3[a] - x0v[a]*Y3[b] - x0v[b]*Y3[a]) for a, b in COORD_PAIRS]
Msys = sp.Matrix([[sp.diff(er, u) for u in un] for er in eqs])
ns = Msys.nullspace()
triv = sp.Matrix(list(Y3) + list(X3))
nontriv = next(vec for vec in ns if sp.Matrix.hstack(sp.Matrix([sp.nsimplify(c) for c in vec]), triv).rank() == 2)
a_vec = sp.Matrix([sp.nsimplify(c) for c in nontriv[:4]])
b_vec = sp.Matrix([sp.nsimplify(c) for c in nontriv[4:]])
print("a =", list(a_vec.T), "b =", list(b_vec.T))

planes = []
for s in (sg0, sg1, sg2):
    planes.append([[sp.nsimplify(c) for c in (a_vec + s*Y3).T], [sp.nsimplify(c) for c in (b_vec + s*X3).T]])
planes.append([list(Y3.T), list(X3.T)])

T = {}
for bits in itertools.product((0, 1), repeat=4):
    T[bits] = sp.nsimplify(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4))))
nzcount = sum(1 for val in T.values() if val != 0)
print("nonzero entries:", nzcount, " weights:", sorted({sum(b) for b, val in T.items() if val != 0}))
assert nzcount > 0, "zero restriction"
for left, right in (((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))):
    m = sp.zeros(4, 4)
    for bits in itertools.product((0,1), repeat=4):
        m[2*bits[left[0]]+bits[left[1]], 2*bits[right[0]]+bits[right[1]]] = T[bits]
    print("flattening", left, right, "rank:", m.rank())

profile = []
relations = []
for a_, b_ in itertools.combinations(range(4), 2):
    rows_ = []
    for pa in planes[a_]:
        for pb in planes[b_]:
            prod = rmul(pa, pb)
            rows_.append([prod[ab] for ab in COORD_PAIRS])
    mm = sp.Matrix(rows_)
    r = mm.rank()
    profile.append(r)
    if r == 3:
        k = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
        relations.append(((a_, b_), sp.Matrix(2, 2, k).rank()))
print("profile:", tuple(profile))
print("rank-3 edge relation ranks:", relations)
import json, pathlib
pathlib.Path("star_sample.json").write_text(json.dumps({
    "sigma": [str(sg0), str(sg1), str(sg2)], "n2": str(n2v), "n3": str(n3v),
    "planes": [[[str(c) for c in row] for row in pl] for pl in planes]}, indent=1))
