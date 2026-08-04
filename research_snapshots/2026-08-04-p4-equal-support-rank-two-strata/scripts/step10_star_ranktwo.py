#!/usr/bin/env python3
"""TASK B: the all-rank-two STAR stratum.

Structure theorem (derived + verified here):
  - mu-gauge: all three relations become y_i x_3 = x_i y_3 in R_2 (i=0,1,2).
  - q_i := y_i o x_3 - x_i o y_3 (Sym^2) is diagonal and vanishes on U_i-perp
    and U_3-perp; the diagonal quadrics vanishing on a generic plane-perp form
    a LINE, so q_i = rho_i * Delta(U_3); y-x pair rescale normalizes rho_i = 1.
  - q_i - q_j = 0 exactly in Sym^2 forces (unique factorization)
        y_i - y_j = sigma_ij y_3,   x_i - x_j = sigma_ij x_3.
  - hence all leaves lie in the pencil (y,x) = (a,b) + sigma (y_3,x_3), where
    (a,b) spans the nontrivial solution of y a ... i.e. the 2-dim solution
    space of  y0*x3 = x0*y3  (6 linear equations in 8 unknowns).
Then purity is imposed on the pencil family.
"""
import itertools, sympy as sp

n2, n3 = sp.symbols("n2 n3")
s0, s1, s2 = sp.symbols("sigma0:3")
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

Y3 = sp.Matrix([1, 1, 1, 1])
X3 = sp.Matrix([0, 1, n2, n3])

# dim of diagonal quadrics vanishing on U3-perp is 1 (generic):
# U3-perp = {y3.X = x3.X = 0}: basis of the perp plane:
perp = sp.Matrix([[Y3.T], [X3.T]]).nullspace()
assert len(perp) == 2
d0, d1, d2, d3 = sp.symbols("d0:4")
Xv = sp.symbols("X0:4")
delta = sum(sp.Symbol(f"d{k}")*Xv[k]**2 for k in range(4))
conds = set()
for c_, d_ in ((1, 0), (0, 1), (1, 1)):
    w = c_*perp[0] + d_*perp[1]
    conds.add(sp.expand(sum(sp.Symbol(f"d{k}")*w[k]**2 for k in range(4))))
Mc = sp.Matrix([[sp.diff(c, sp.Symbol(f"d{k}")) for k in range(4)] for c in conds])
print("dim of diagonal quadrics vanishing on generic U3-perp:", 4 - Mc.rank())

# solution space of y0*x3 = x0*y3 (unknowns y0,x0):
un = sp.symbols("a0:4 b0:4")
y0 = sp.Matrix(un[:4]); x0 = sp.Matrix(un[4:])
eqs = [sp.expand(y0[a]*X3[b] + y0[b]*X3[a] - x0[a]*Y3[b] - x0[b]*Y3[a]) for a, b in COORD_PAIRS]
Msys = sp.Matrix([[sp.diff(e, u) for u in un] for e in eqs])
ns = Msys.nullspace()
print("solution dim of y0*x3=x0*y3:", len(ns))
# identify trivial solution (y3,x3) and pick nontrivial (a,b)
sols = [sp.Matrix([sp.simplify(c) for c in vec]) for vec in ns]
# find combination equal to (y3;x3):
comb = sp.Matrix.hstack(*sols)
triv = sp.Matrix(list(Y3) + list(X3))
lam = comb.solve_least_squares(triv)
# choose a nontrivial basis vector independent of triv
nontriv = None
for vec in sols:
    if sp.Matrix.hstack(vec, triv).rank() == 2:
        nontriv = vec
        break
a_vec = sp.Matrix([sp.cancel(c) for c in nontriv[:4]])
b_vec = sp.Matrix([sp.cancel(c) for c in nontriv[4:]])
print("nontrivial pencil generator a =", list(a_vec.T), " b =", list(b_vec.T))
# check it satisfies the relation and is independent
pr = rmul(list(a_vec), list(X3)); pr2 = rmul(list(b_vec), list(Y3))
assert all(sp.simplify(pr[ab] - pr2[ab]) == 0 for ab in COORD_PAIRS)

# the pencil family and purity
planes = []
for s in (s0, s1, s2):
    yi = a_vec + s*Y3
    xi = b_vec + s*X3
    planes.append([list(yi.T), list(xi.T)])
planes.append([list(Y3.T), list(X3.T)])

T = {}
for bits in itertools.product((0, 1), repeat=4):
    T[bits] = perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
nz = {b: sp.factor(val) for b, val in T.items() if sp.expand(val) != 0}
print("\nnonzero entries of T on the pencil family (factored):")
for b, val in sorted(nz.items()):
    print("  T%s = %s" % ("".join(map(str, b)), val))
