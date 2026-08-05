#!/usr/bin/env python3
"""More census invariants: generic 8th sample (Gaussian rational), L2, L3,
and a second W-branch sample."""
import itertools, sympy as sp

PERMS4 = tuple(itertools.permutations(range(4)))
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def invariants(planes, name):
    planes = [[[sp.nsimplify(c) for c in row] for row in pl] for pl in planes]
    T = {}
    for bits in itertools.product((0,1), repeat=4):
        T[bits] = perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
    assert any(val != 0 for val in T.values()), (name, "zero restriction")
    kernels = []
    for m in range(4):
        mat = sp.zeros(2, 8)
        for bits in itertools.product((0,1), repeat=4):
            rest = tuple(bits[j] for j in range(4) if j != m)
            mat[bits[m], rest[0]*4 + rest[1]*2 + rest[2]] = T[bits]
        assert mat.rank() == 1, (name, m, "not pure")
        l = sp.Matrix(mat.T).nullspace()[0]
        kernels.append([sp.expand(l[0]*planes[m][0][t] + l[1]*planes[m][1][t]) for t in range(4)])
    profile = []
    kk = False
    rels = []
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
            rk = K.rank()
            entry = {"edge": (a_, b_), "rank": rk}
            if rk == 1:
                lv = K[:, 0] if any(c != 0 for c in K[:, 0]) else K[:, 1]
                rv = (K[0, :] if any(c != 0 for c in K[0, :]) else K[1, :]).T
                ua = [sp.expand(lv[0]*planes[a_][0][t] + lv[1]*planes[a_][1][t]) for t in range(4)]
                ub = [sp.expand(rv[0]*planes[b_][0][t] + rv[1]*planes[b_][1][t]) for t in range(4)]
                ina = sp.Matrix([ua, kernels[a_]]).rank() == 1
                inb = sp.Matrix([ub, kernels[b_]]).rank() == 1
                entry["dirs"] = (ina, inb)
                if ina and inb:
                    kk = True
            rels.append(entry)
    print(f"== {name}\n   profile {tuple(profile)}   kernel-kernel: {kk}")
    for entry in rels:
        print("  ", entry)
    return tuple(profile), kk

# 8th generic (a,b,f,phi) = (2,1,2,I)
I_ = sp.I
a8, b8, f8, p8 = 2, 1, 2, I_
Phi8 = sp.expand(a8**2*b8*f8*p8**2 + a8**2*f8**2 - b8**2*f8**2 + b8**2*p8**2 - b8*f8 - 1)
assert Phi8 == 0, Phi8
j8 = f8 + b8*p8**2
kap8 = p8*(b8*f8 + 1)
eta8 = -(b8*f8 + 1)
planes8 = [
    [[0, 0, 1, -1], [a8+b8, a8-b8, 0, 2]],
    [[-a8*f8+1, -a8*f8-1, f8+p8, f8-p8], [1, 1, 0, 0]],
    [[-a8*j8+eta8, -a8*j8-eta8, j8+kap8, j8-kap8], [1, 1, 0, 0]],
    [[1, -1, 0, 0], [0, 0, 1, 1]],
]
invariants(planes8, "8th generic (2,1,2,i)")

# L2: T = D+G-S ; L3: T = -D-G-S  (radical-star (10)-(14))
for name, Tv_expr in (("L2", lambda S, D, G: D + G - S), ("L3", lambda S, D, G: -D - G - S)):
    S, D, G = 2, 3, 5
    Tv = Tv_expr(S, D, G)
    P_ = G - Tv; Q_ = D - S
    planesL = [
        [[2, P_+Q_, Q_-P_, 0], [0, 0, 1, 1]],
        [[0, 1, -1, 0], [1, 0, S, D]],
        [[0, 1, 0, -1], [1, 0, G, Tv]],
        [[0, 1, 1, 0], [0, 1, 0, 1]],
    ]
    invariants(planesL, f"{name} S,D,G=(2,3,5)")

# second W sample
e_ = -2
vv = (3, -7, 2, 5); xx = (6, -14, -1, 8)   # (x0,x1) = 2*(v0,v1)
planesW = [
    [[vv[0], -vv[1], 0, 0], [0, 0, 1, -1]],
    [[0, 0, 1, -1], list(vv)],
    [[0, 0, 1, -e_], list(xx)],
    [[0, 0, 1, 1], [0, 0, 1, e_]],
]
invariants(planesW, "W-branch sample 2 (e=-2)")
