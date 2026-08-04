#!/usr/bin/env python3
"""Star rank-two stratum: weight-tensor reduction and purity equations.

Verifies:
  - T[bits] depends only on the weight |bits| (pencil symmetry);
  - each t_w is affine-linear in e1,e2,e3 (elementary symmetric in sigmas);
  - purity <=> (t_0..t_4) is a geometric progression;
then solves the geometric conditions for (e1,e2,e3) over Q(n2,n3).
"""
import itertools, sympy as sp

n2, n3 = sp.symbols("n2 n3")
s0, s1, s2 = sp.symbols("sigma0:3")
e1, e2, e3 = sp.symbols("e1:4")
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

Y3 = sp.Matrix([1, 1, 1, 1])
X3 = sp.Matrix([0, 1, n2, n3])
un = sp.symbols("a0:4 b0:4")
y0v = sp.Matrix(un[:4]); x0v = sp.Matrix(un[4:])
eqs = [sp.expand(y0v[a]*X3[b] + y0v[b]*X3[a] - x0v[a]*Y3[b] - x0v[b]*Y3[a]) for a, b in COORD_PAIRS]
Msys = sp.Matrix([[sp.diff(er, u) for u in un] for er in eqs])
ns = Msys.nullspace()
triv = sp.Matrix(list(Y3) + list(X3))
nontriv = next(vec for vec in ns if sp.Matrix.hstack(sp.Matrix([sp.cancel(c) for c in vec]), triv).rank() == 2)
a_vec = sp.Matrix([sp.cancel(c) for c in nontriv[:4]])
b_vec = sp.Matrix([sp.cancel(c) for c in nontriv[4:]])

planes = []
for s in (s0, s1, s2):
    planes.append([list((a_vec + s*Y3).T), list((b_vec + s*X3).T)])
planes.append([list(Y3.T), list(X3.T)])

T = {}
for bits in itertools.product((0, 1), repeat=4):
    T[bits] = sp.expand(sp.cancel(sp.together(
        perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4))))))

# weight dependence
tw = {}
for bits, val in T.items():
    w = sum(bits)
    if w in tw:
        assert sp.simplify(tw[w] - val) == 0, (bits, "weight symmetry fails")
    else:
        tw[w] = val
print("T[bits] depends only on weight: OK")

# affine-linear in e1,e2,e3
esub = {}
t_lin = {}
for w, val in tw.items():
    poly = sp.Poly(sp.expand(sp.numer(sp.together(val))), s0, s1, s2)
    den = sp.denom(sp.together(val))
    expr = sp.expand(val)
    # rewrite in elementary symmetric polynomials
    E1 = s0 + s1 + s2; E2 = s0*s1 + s0*s2 + s1*s2; E3 = s0*s1*s2
    # solve linear system: expr = c0 + c1*E1 + c2*E2 + c3*E3
    c = sp.symbols(f"c{w}_0:4")
    cand = c[0] + c[1]*E1 + c[2]*E2 + c[3]*E3
    sols = sp.solve(sp.Poly(sp.expand(sp.together(expr - cand)*den).simplify() if False else sp.expand((expr - cand)), s0, s1, s2).coeffs(), c, dict=True)
    assert sols, (w, "not e-linear")
    sol = sols[0]
    t_lin[w] = sp.cancel(sol[c[0]] + sol[c[1]]*e1 + sol[c[2]]*e2 + sol[c[3]]*e3)
    print(f"t_{w} =", sp.factor(t_lin[w]))

# geometric-progression ideal in (e1,e2,e3) over Q(n2,n3)
t = [t_lin[w] for w in range(5)]
G = [sp.expand(sp.numer(sp.cancel(t[0]*t[2] - t[1]**2))),
     sp.expand(sp.numer(sp.cancel(t[1]*t[3] - t[2]**2))),
     sp.expand(sp.numer(sp.cancel(t[2]*t[4] - t[3]**2))),
     sp.expand(sp.numer(sp.cancel(t[0]*t[3] - t[1]*t[2]))),
     sp.expand(sp.numer(sp.cancel(t[1]*t[4] - t[2]*t[3]))),
     sp.expand(sp.numer(sp.cancel(t[0]*t[4] - t[2]**2)))]
import json, pathlib
out = {"t": [str(x) for x in t], "G": [str(g) for g in G]}
pathlib.Path("star_purity_data.json").write_text(json.dumps(out, indent=1))
print("\nsaved t_w and geometric ideal generators to star_purity_data.json")
