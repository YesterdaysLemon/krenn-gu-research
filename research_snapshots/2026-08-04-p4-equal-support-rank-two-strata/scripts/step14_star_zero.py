#!/usr/bin/env python3
"""Verify: on the star-purity prime, all five weight entries vanish identically.
Hence the generic-chart all-rank-two star stratum contains NO nonzero pure
restriction."""
import json, pathlib, sympy as sp

n2, n3, e1, e2, e3 = sp.symbols("n2 n3 e1 e2 e3")
data = json.loads(pathlib.Path("star_purity_data.json").read_text())
t = [sp.sympify(s) for s in data["t"]]

# curve parametrization from the prime (step12):
e1_sol = -3*n2*(n2 - n3)*e3/(n3 - 1)
e2_sol = sp.solve(sp.sympify(
    "(n2^2*n3-n2^2-n2*n3^2+n2*n3)*e2+(2*n2^3*n3-4*n2^3-2*n2^2*n3^2+6*n2^2*n3-2*n2*n3^2)*e3+(-n3^2+2*n3-1)"
    .replace("^", "**")), e2)[0]
sub = {e1: e1_sol, e2: e2_sol}
allzero = True
for w, tv in enumerate(t):
    val = sp.simplify(sp.together(tv.subs(sub)))
    print(f"t_{w} on curve:", val)
    if val != 0:
        allzero = False
print("\nall five entries vanish identically on the purity curve:", allzero)

# conversely: the ideal (t_0..t_4) of the ZERO locus equals the curve:
# check each curve generator is in the radical by asserting the linear system
# t_w = 0 (5 linear eqs in e1,e2,e3) has solution set exactly the curve:
M = sp.Matrix([[sp.diff(tv, e1), sp.diff(tv, e2), sp.diff(tv, e3)] for tv in t])
rhs = sp.Matrix([-tv.subs({e1: 0, e2: 0, e3: 0}) for tv in t])
aug = M.row_join(rhs)
print("rank coefficient matrix:", M.rank(), " rank augmented:", aug.rank())
# rank 2 = rank 2 -> affine solution line == the curve

# rank of the common diagonal quadric Delta(U_3) for generic (n2,n3):
# q = y_0 o x_3 - x_0 o y_3 with (y_0,x_0)=(a,b) the nontrivial pencil generator
import itertools
Y3 = sp.Matrix([1, 1, 1, 1]); X3 = sp.Matrix([0, 1, n2, n3])
un = sp.symbols("a0:4 b0:4")
y0v = sp.Matrix(un[:4]); x0v = sp.Matrix(un[4:])
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
eqs = [sp.expand(y0v[a]*X3[b] + y0v[b]*X3[a] - x0v[a]*Y3[b] - x0v[b]*Y3[a]) for a, b in COORD_PAIRS]
Msys = sp.Matrix([[sp.diff(er, u) for u in un] for er in eqs])
ns = Msys.nullspace()
triv = sp.Matrix(list(Y3) + list(X3))
nontriv = next(vec for vec in ns if sp.Matrix.hstack(sp.Matrix([sp.cancel(c) for c in vec]), triv).rank() == 2)
a_vec = sp.Matrix([sp.cancel(c) for c in nontriv[:4]])
b_vec = sp.Matrix([sp.cancel(c) for c in nontriv[4:]])
deltas = [sp.factor(sp.expand(a_vec[k]*X3[k] - b_vec[k]*Y3[k])) for k in range(4)]
print("\nDelta(U_3) diagonal entries (a_k x3_k - b_k y3_k):", deltas)
