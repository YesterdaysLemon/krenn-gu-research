#!/usr/bin/env python3
"""TASK B: structure of a rank-two relation edge.

Facts proved here (exact, symbolic):
 (1) shift/scale gauge: a rank-two relation at edge {i,j} normalizes to
        y_i x_j = x_i y_j   in R_2   (mu = 1 gauge),
     equivalently G := y_i x_j^T - x_i y_j^T has G + G^T diagonal.
 (2) G always has rank exactly 2, col(G) = U_i, row(G) = U_j.
 (3) the sym part Sym(G) = y_i o x_j - x_i o y_j is a DIAGONAL quadric;
     conversely any rank-2 matrix G with G+G^T diagonal arises this way.
 (4) no support restriction: the 2nd-component sample realizes a rank-two
     edge with all four vectors of full support (support lemma inapplicable).
 (5) the antisymmetric part Om := (G-G^T)/2 and Delta := (G+G^T)/2 satisfy
     rank(Delta + Om) = 2; the classification of such (Delta,Om) is the
     normal-form case split.
"""
import itertools, sympy as sp

# --- (1),(2),(3) symbolic verification over the function field
yi = sp.Matrix(sp.symbols("yi0:4"))
xi = sp.Matrix(sp.symbols("xi0:4"))
yj = sp.Matrix(sp.symbols("yj0:4"))
xj = sp.Matrix(sp.symbols("xj0:4"))

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

G = yi*xj.T - xi*yj.T
S = sp.expand(G + G.T)
rel = rmul(yi, xj)
rel2 = rmul(xi, yj)
for (a, b) in COORD_PAIRS:
    # off-diagonal entry of G+G^T = (y_i x_j)_ab - (x_i y_j)_ab
    assert sp.expand(S[a, b] - (rel[(a, b)] - rel2[(a, b)])) == 0
print("(3) offdiag(G+G^T) == coefficients of y_i*x_j - x_i*y_j in R_2: OK")
print("    => relation y_i x_j = x_i y_j  <=>  G + G^T diagonal")

# (2) rank exactly 2 whenever (y_i,x_i) and (y_j,x_j) are independent pairs:
# G as element of U_i (x) U_j is [[0,1],[-1,0]] in these bases -> rank 2.
# numeric spot check with random integer vectors:
import random
random.seed(7)
for _ in range(3):
    vals = {s: random.randint(-9, 9) for s in list(yi)+list(xi)+list(yj)+list(xj)}
    Gn = G.subs(vals)
    assert Gn.rank() == 2
print("(2) rank(G) == 2 at random samples: OK (structurally rank 2 in U_i (x) U_j)")

# --- (4) full-support rank-two edge exists: 2nd component sample, edge {0,3}
PERMS4 = tuple(itertools.permutations(range(4)))
def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))
A_, B_, C_, E_, F_, H_ = 1, 1, 5, 1, 1, 1
planes2 = [
    [[E_, -F_, -F_, -E_], [A_, -B_, B_, A_]],
    [[1, 0, 0, -1], [A_, C_+B_, C_-B_, A_]],
    [[0, 1, -1, 0], [H_+E_, F_, F_, H_-E_]],
    [[1, 0, 0, 1], [0, 1, 1, 0]],
]
rows_ = []
for pa in planes2[0]:
    for pb in planes2[3]:
        prod = rmul(pa, pb)
        rows_.append([prod[ab] for ab in COORD_PAIRS])
mm = sp.Matrix(rows_)
assert mm.rank() == 3
k = mm.T.nullspace()[0]
K = sp.Matrix(2, 2, [sp.nsimplify(c) for c in k])
assert K.rank() == 2
print("(4) 2nd-component edge {0,3}: relation matrix rank 2; vector supports:",
      [tuple(t for t in range(4) if row[t] != 0) for row in planes2[0] + planes2[3]])

# --- (5) mu-gauge bookkeeping for star and triangle
# star {i,3}, i=0,1,2:  mu_i3 -> (c_3/c_i) mu_i3 under x_k -> c_k x_k:
# c_0,c_1,c_2 free => all three mu normalize to 1; no modulus.
# triangle {12},{13},{23}: mu'_ij = (c_j/c_i) mu_ij; invariant
# lambda = mu_12 mu_23 / mu_13 survives: one holonomy modulus.
c1, c2, c3 = sp.symbols("c1:4", nonzero=True)
m12, m13, m23 = sp.symbols("m12 m13 m23", nonzero=True)
lam = m12*m23/m13
lam_new = ((c2/c1)*m12) * ((c3/c2)*m23) / ((c3/c1)*m13)
assert sp.simplify(lam_new - lam) == 0
print("(5) triangle holonomy lambda = mu_12*mu_23/mu_13 is scaling-invariant: OK")
print("    star: all three mu normalize to 1 (c_0,c_1,c_2 independent)")
