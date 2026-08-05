#!/usr/bin/env python3
"""The extended six-parameter family through the W-branch:

  U0 = span((v0,-v1,0,0), (0,0,1,-c0)),
  U1 = span((0,0,1,-c1), v),
  U2 = span((0,0,1,-c2), x),      x = (t v0, t v1, x2, x3),
  U3 = Pi = span(X2, X3),

with moduli (c0, c1, c2, t, v-2, x-1) = 6.  Verify purity symbolically,
then invariants, family tangent rank, and incidence Jacobian rank at a
generic exact sample."""
import itertools, sympy as sp

c0, c1, c2, t = sp.symbols("c0 c1 c2 t")
v = sp.symbols("v0:4")
x2, x3 = sp.symbols("x2 x3")
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

xrow = (t*v[0], t*v[1], x2, x3)
planes_sym = [
    [(v[0], -v[1], 0, 0), (0, 0, 1, -c0)],
    [(0, 0, 1, -c1), tuple(v)],
    [(0, 0, 1, -c2), xrow],
    [(0, 0, 1, 1), (0, 0, 1, -1)],   # basis of Pi (any basis)
]
T = {}
for bits in itertools.product((0, 1), repeat=4):
    T[bits] = sp.expand(perm4(tuple(planes_sym[m][bits[m]] for m in range(4))))
print("nonzero entries (symbolic):")
for bits, val in T.items():
    if val != 0:
        print("  T%s = %s" % ("".join(map(str, bits)), sp.factor(val)))
# purity: all pair flattening 2x2 minors vanish identically
ok = True
for left, right in (((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))):
    mat = {}
    for bits in itertools.product((0,1), repeat=4):
        mat[((bits[left[0]], bits[left[1]]), (bits[right[0]], bits[right[1]]))] = T[bits]
    rk = sorted({k[0] for k in mat}); ck = sorted({k[1] for k in mat})
    for r1, r2 in itertools.combinations(rk, 2):
        for cc1, cc2 in itertools.combinations(ck, 2):
            mm = sp.expand(mat[(r1, cc1)]*mat[(r2, cc2)] - mat[(r1, cc2)]*mat[(r2, cc1)])
            if sp.simplify(mm) != 0:
                ok = False
                print("NONZERO MINOR", left, right, r1, r2, cc1, cc2, mm)
print("pure for ALL parameter values:", ok)

# generic exact sample
sample = {c0: 3, c1: -2, c2: 5, t: 2, v[0]: 3, v[1]: -7, v[2]: 2, v[3]: 5, x2: -1, x3: 4}
planes = [[[sp.nsimplify(sp.sympify(e_).subs(sample)) for e_ in row] for row in pl] for pl in planes_sym]
Tp = {bits: sp.nsimplify(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))) for bits in itertools.product((0,1), repeat=4)}
assert any(val != 0 for val in Tp.values())
kernels = []
for m in range(4):
    mat = sp.zeros(2, 8)
    for bits in itertools.product((0,1), repeat=4):
        rest = tuple(bits[j] for j in range(4) if j != m)
        mat[bits[m], rest[0]*4 + rest[1]*2 + rest[2]] = Tp[bits]
    assert mat.rank() == 1
    l = sp.Matrix(mat.T).nullspace()[0]
    kernels.append([sp.expand(l[0]*planes[m][0][t_] + l[1]*planes[m][1][t_]) for t_ in range(4)])
print("kernels:", [[sp.nsimplify(c_) for c_ in k] for k in kernels])
profile = []
rels = []
kk = False
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
        K = sp.Matrix(2, 2, k)
        rk2 = K.rank()
        entry = {"edge": (a_, b_), "rank": rk2}
        if rk2 == 1:
            lv = K[:, 0] if any(c_ != 0 for c_ in K[:, 0]) else K[:, 1]
            rv = (K[0, :] if any(c_ != 0 for c_ in K[0, :]) else K[1, :]).T
            ua = [sp.expand(lv[0]*planes[a_][0][t_] + lv[1]*planes[a_][1][t_]) for t_ in range(4)]
            ub = [sp.expand(rv[0]*planes[b_][0][t_] + rv[1]*planes[b_][1][t_]) for t_ in range(4)]
            ina = sp.Matrix([ua, kernels[a_]]).rank() == 1
            inb = sp.Matrix([ub, kernels[b_]]).rank() == 1
            entry["dirs"] = (ina, inb)
            entry["supports"] = (tuple(i for i in range(4) if sp.simplify(ua[i]) != 0),
                                 tuple(i for i in range(4) if sp.simplify(ub[i]) != 0))
            kk = kk or (ina and inb)
    rels.append(entry) if r == 3 else None
print("profile:", tuple(profile), " kernel-kernel:", kk)
for entry in rels:
    print("  ", entry)
