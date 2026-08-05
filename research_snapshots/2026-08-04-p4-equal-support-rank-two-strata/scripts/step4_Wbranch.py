#!/usr/bin/env python3
"""Equal-support chart: invariants of the W-branch v1*x0-v0*x1=0 (s != 0)."""
import itertools, sympy as sp

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

def analyse(planes, name):
    T = {}
    for bits in itertools.product((0,1), repeat=4):
        T[bits] = sp.nsimplify(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4))))
    nz = [b for b, val in T.items() if val != 0]
    print(f"[{name}] nonzero entries: {len(nz)}")
    if not nz:
        return None
    flat_ranks = []
    for left, right in (((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0,1), repeat=4):
            r_ = 2*bits[left[0]] + bits[left[1]]
            c_ = 2*bits[right[0]] + bits[right[1]]
            m[r_, c_] = T[bits]
        flat_ranks.append(m.rank())
    print(f"[{name}] flattening ranks (must be 1,1,1 for pure):", flat_ranks)
    profile = []
    relations = []
    for a_, b_ in itertools.combinations(range(4), 2):
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(list(pa), list(pb))
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        r = mm.rank()
        profile.append(r)
        if r == 3:
            k = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
            M2 = sp.Matrix([[k[0], k[1]], [k[2], k[3]]])
            rk = M2.rank()
            rel = ((a_, b_), rk)
            if rk == 1:
                # rank-one relation K=lv*rv^T: sum K_ij a_i b_j = (lv.a)(rv.b) = 0
                K = sp.Matrix(2, 2, [k[0], k[1], k[2], k[3]])
                lv = K[:, 0] if any(c != 0 for c in K[:, 0]) else K[:, 1]
                rv = K[0, :].T if any(c != 0 for c in K[0, :]) else K[1, :].T
                scale = next(c for c in K if c != 0)
                # normalize so lv*rv^T = K: divide one by the pivot
                lv = lv / 1
                rv = rv / 1
                if lv is not None and rv is not None:
                    ua = [sp.expand(lv[0]*planes[a_][0][t] + lv[1]*planes[a_][1][t]) for t in range(4)]
                    ub = [sp.expand(rv[0]*planes[b_][0][t] + rv[1]*planes[b_][1][t]) for t in range(4)]
                    pr = rmul(ua, ub)
                    assert all(sp.simplify(val) == 0 for val in pr.values()), (rel, pr)
                    sup_a = tuple(t for t in range(4) if sp.simplify(ua[t]) != 0)
                    sup_b = tuple(t for t in range(4) if sp.simplify(ub[t]) != 0)
                    rel = ((a_, b_), rk, ("factors", [sp.nsimplify(c) for c in ua], [sp.nsimplify(c) for c in ub], sup_a, sup_b))
            relations.append(rel)
    print(f"[{name}] pair profile (r01,r02,r03,r12,r13,r23):", tuple(profile))
    for rel in relations:
        print(f"[{name}] rank-3 edge relation:", rel)
    return tuple(profile), relations

def covector_matrix(vv, xx):
    Y2l = (0, 0, 1, -e)
    rows = []
    for c in (rmul(list(Y2l), Y3), rmul(list(xx), Y3)):
        form = pairing(rmul(list(z), list(vv)), c)
        rows.append([sp.expand(sp.diff(form, zi)) for zi in z])
    return sp.Matrix(rows)

# --- W-branch sample: v1*x0 = v0*x1, s != 0, v2+v3 != 0, generic ---
sample = {e: 3, v[0]: 2, v[1]: 5, v[2]: 7, v[3]: -11, x[2]: 13, x[3]: -4}
# choose x0, x1 with v1*x0-v0*x1=0: x0=2t, x1=5t, t=1 => x0=2, x1=5 (s=2*5+5*2=20 != 0)
sample[x[0]] = 2; sample[x[1]] = 5
vv = tuple(sample[k] for k in v)
xx = tuple(sample[k] for k in x)
ee = sample[e]
Mnum = covector_matrix(vv, xx).subs({e: ee})
Mnum = sp.Matrix([[sp.nsimplify(c) for c in row] for row in Mnum.tolist()])
assert Mnum.rank() == 2, Mnum
ker = Mnum.nullspace()
assert len(ker) == 2
U0 = [[sp.nsimplify(c) for c in k] for k in ker]
print("U0 basis:", U0)
planes = [
    U0,
    [list(U1_A), list(vv)],
    [[0, 0, 1, -ee], list(xx)],
    [list(Y3), [0, 0, 1, ee]],
]
res = analyse(planes, "W-sample")
