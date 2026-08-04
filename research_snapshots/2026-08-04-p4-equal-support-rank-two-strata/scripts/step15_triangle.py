#!/usr/bin/env python3
"""TASK B: the all-rank-two TRIANGLE stratum.

Derived structure (unique-factorization arguments in Sym^2):
  - pairwise differences of the three diagonal relations force holonomy
    lambda = 1 and (y_2,x_2) = (y_1+y_3, x_1+x_3) after gauges;
  - so U_1, U_2, U_3 are the pencil members sigma = 0, 1, oo of
    {span(a + sigma y_3, b + sigma x_3)}, with (a,b) the nontrivial solution
    of a*x_3 = b*y_3 in R_2;
  - U_0 = span(p,q) is free; purity conditions computed here.
"""
import itertools, sympy as sp

n2, n3 = sp.symbols("n2 n3")
p = sp.symbols("p0:4")
q = sp.symbols("q0:4")
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
a_vec = sp.Matrix([sp.cancel(c*(n2 - n3)*n2) for c in nontriv[:4]])   # clear denominators
b_vec = sp.Matrix([sp.cancel(c*(n2 - n3)*n2) for c in nontriv[4:]])
# recheck relation
pr1 = rmul(list(a_vec), list(X3)); pr2 = rmul(list(b_vec), list(Y3))
assert all(sp.simplify(pr1[ab] - pr2[ab]) == 0 for ab in COORD_PAIRS)
print("a =", list(a_vec.T))
print("b =", list(b_vec.T))

planes = [
    [list(p), list(q)],                                    # U_0 free
    [list(a_vec.T), list(b_vec.T)],                        # U_1 (sigma=0)
    [list((a_vec + Y3).T), list((b_vec + X3).T)],          # U_2 (sigma=1)  -- note scale of (Y3,X3) vs (a,b) matters: kept
    [list(Y3.T), list(X3.T)],                              # U_3 (sigma=oo)
]
# NOTE: after clearing denominators in (a,b), the normalization
# (y_2,x_2) = (y_1,x_1) + kappa (y_3,x_3) carries a scale kappa; the honest
# pencil member is sigma arbitrary; include kappa symbolically.
kappa = sp.Symbol("kappa")
planes[2] = [list((a_vec + kappa*Y3).T), list((b_vec + kappa*X3).T)]

T = {}
for bits in itertools.product((0, 1), repeat=4):
    T[bits] = sp.expand(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4))))

# how do entries depend on (bits1,bits2,bits3)? check partial weight symmetry in modes 1,2,3
import collections
groups = collections.defaultdict(list)
for bits, val in T.items():
    groups[(bits[0], bits[1]+bits[2]+bits[3])].append((bits, val))
sym = True
for key, lst in groups.items():
    for (b1, v1), (b2, v2) in itertools.combinations(lst, 2):
        if sp.simplify(v1 - v2) != 0:
            sym = False
print("entries depend only on (bit0, weight of bits 1-3):", sym)

if sym:
    tw = {}
    for bits, val in T.items():
        tw[(bits[0], bits[1]+bits[2]+bits[3])] = sp.expand(val)
    for key in sorted(tw):
        print(f"t[{key}] deg-in-kappa {sp.degree(tw[key], kappa) if tw[key] != 0 else '-'}; nterms {len(sp.Add.make_args(tw[key]))}")
    import json, pathlib
    pathlib.Path("triangle_data.json").write_text(json.dumps(
        {str(k): str(v) for k, v in tw.items()}, indent=1))
    print("saved to triangle_data.json")
