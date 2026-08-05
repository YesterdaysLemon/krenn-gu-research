#!/usr/bin/env python3
"""Triangle stratum sample: (n2,n3,kappa)=(2,3,2); kernel of Lambda, cone
section, U_0 candidates, full invariants for each."""
import itertools, json, pathlib, sympy as sp

kappa, n2, n3 = sp.symbols("kappa n2 n3")
rsym = sp.Symbol("r")
tw = {eval(k): sp.sympify(v) for k, v in json.loads(pathlib.Path("triangle_data.json").read_text()).items()}
p = sp.symbols("p0:4")
Lam = sp.zeros(4, 4)
for w in range(4):
    for j in range(4):
        Lam[w, j] = sp.expand(sp.diff(tw[(0, w)], p[j]))

point = {n2: 2, n3: 3, kappa: 2}
assert sp.simplify((kappa**2 + n2*(n3-1)*(n2-n3)).subs(point)) == 0
L = Lam.subs(point)
L = sp.Matrix([[sp.nsimplify(c) for c in row] for row in L.tolist()])
print("rank Lambda at sample:", L.rank())
ker = L.nullspace()
print("kernel dim:", len(ker), " kernel:", [list(k.T) for k in ker])
# left kernel (covectors vanishing on Im Lambda)
lker = L.T.nullspace()
print("left-kernel covectors:", [list(k.T) for k in lker])
# cone section: phi.(1,r,r^2,r^3) = 0 for each left-kernel covector phi
sols = None
for phi in lker:
    poly = sp.Poly(sum(phi[i]*rsym**i for i in range(4)), rsym)
    print("cubic:", poly.as_expr(), " roots:", sp.roots(poly))
    sols = sp.roots(poly)
# for each rational root r0: geometric vector g=(1,r0,r0^2,r0^3); w = solve L w = g
results = {}
for r0 in list(sols) + ["inf"]:
    if r0 == "inf":
        g = sp.Matrix([0, 0, 0, 1])
        # check (0,0,0,1) in Im L: phi.(0,0,0,1)=0?
        if any(sp.simplify(phi[3]) != 0 for phi in lker):
            print("r=inf: (0,0,0,1) not in image; skip")
            continue
    else:
        g = sp.Matrix([1, r0, r0**2, r0**3])
    try:
        wsol = L.solve(g)
    except Exception:
        # least squares fallback: solve augmented
        aug = L.row_join(g)
        if aug.rank() > L.rank():
            print(f"r={r0}: g not in image; skip")
            continue
        wsol = L.pinv()*g
    wsol = sp.Matrix([sp.nsimplify(sp.cancel(c)) for c in wsol])
    print(f"r={r0}: w =", list(wsol.T))
    results[str(r0)] = wsol

# build planes and invariants for each candidate
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

n2v, n3v, kv = 2, 3, 2
Y3 = sp.Matrix([1, 1, 1, 1]); X3 = sp.Matrix([0, 1, n2v, n3v])
un = sp.symbols("a0:4 b0:4")
y0v = sp.Matrix(un[:4]); x0v = sp.Matrix(un[4:])
eqs = [sp.expand(y0v[a]*X3[b] + y0v[b]*X3[a] - x0v[a]*Y3[b] - x0v[b]*Y3[a]) for a, b in COORD_PAIRS]
Msys = sp.Matrix([[sp.diff(er, u) for u in un] for er in eqs])
ns = Msys.nullspace()
triv = sp.Matrix(list(Y3) + list(X3))
nontriv = next(vec for vec in ns if sp.Matrix.hstack(sp.Matrix([sp.nsimplify(c) for c in vec]), triv).rank() == 2)
scale = (n2 - n3)*n2
a_vec = sp.Matrix([sp.nsimplify(sp.cancel(c*scale.subs({n2: n2v, n3: n3v}))) for c in nontriv[:4]])
b_vec = sp.Matrix([sp.nsimplify(sp.cancel(c*scale.subs({n2: n2v, n3: n3v}))) for c in nontriv[4:]])
print("\n(a,b) =", list(a_vec.T), list(b_vec.T))

def invariants(U0rows, name):
    planes = [
        [list(U0rows[0].T), list(U0rows[1].T)],
        [list(a_vec.T), list(b_vec.T)],
        [list((a_vec + kv*Y3).T), list((b_vec + kv*X3).T)],
        [list(Y3.T), list(X3.T)],
    ]
    T = {}
    for bits in itertools.product((0, 1), repeat=4):
        T[bits] = sp.nsimplify(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4))))
    nzero = sum(1 for v_ in T.values() if v_ != 0)
    print(f"[{name}] nonzero entries: {nzero}")
    if nzero == 0:
        return
    for left, right in (((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0,1), repeat=4):
            m[2*bits[left[0]]+bits[left[1]], 2*bits[right[0]]+bits[right[1]]] = T[bits]
        assert m.rank() == 1, (name, left, right, "NOT PURE")
    profile = []
    rels = []
    for a_, b_ in itertools.combinations(range(4), 2):
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        rk = mm.rank()
        profile.append(rk)
        if rk == 3:
            k = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
            rels.append(((a_, b_), sp.Matrix(2, 2, k).rank()))
    print(f"[{name}] profile: {tuple(profile)}  relations: {rels}")
    json.dump({"planes": [[[str(c) for c in row] for row in pl] for pl in planes]},
              open(f"triangle_sample_{name}.json", "w"), indent=1)

for tag, wv in results.items():
    for kvec in ker:
        U0 = (sp.Matrix([sp.nsimplify(c) for c in kvec]), wv)
        invariants(U0, f"r{tag.replace('/', '_')}")
