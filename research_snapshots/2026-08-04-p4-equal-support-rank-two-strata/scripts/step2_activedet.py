#!/usr/bin/env python3
"""Equal-support in-out chart: Cramer kernel, active determinant, Singular factorization."""
import itertools, subprocess, sympy as sp

e = sp.Symbol("e")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")
z = sp.symbols("z0:4")

U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
U3_B = (0, 0, 1, e)
Y2 = (0, 0, 1, -e)

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab))) for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def pairing(P, Q):
    return sp.expand(sum(P[ab]*Q[COMPLEMENT[ab]] for ab in COORD_PAIRS))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

def covector_matrix():
    rows = []
    for c in (rmul(Y2, Y3), rmul(list(x), Y3)):
        form = pairing(rmul(list(z), list(v)), c)
        rows.append([sp.expand(sp.diff(form, zi)) for zi in z])
    return sp.Matrix(rows)

M = covector_matrix()
minors = {}
for a_, b_ in itertools.combinations(range(4), 2):
    minors[(a_, b_)] = sp.expand(M[0, a_]*M[1, b_] - M[0, b_]*M[1, a_])
pivot = minors[(0, 1)]
# pivot identity
target_pivot = sp.expand(-(e-1)*(v[2]+v[3])*(v[1]*x[0]-v[0]*x[1]))
assert sp.expand(pivot - target_pivot) == 0
w2 = (minors[(1, 2)], -minors[(0, 2)], minors[(0, 1)], 0)
w3 = (minors[(1, 3)], -minors[(0, 3)], 0, minors[(0, 1)])
for w in (w2, w3):
    assert all(sp.expand(sum(M[r_, c_]*w[c_] for c_ in range(4))) == 0 for r_ in range(2))
print("Cramer kernel rows OK; pivot = -(e-1)*(v2+v3)*(v1*x0-v0*x1)")

B = sp.zeros(2, 2)
for i0, u0row in enumerate((w2, w3)):
    for i1, u1row in enumerate((U1_A, tuple(v))):
        B[i0, i1] = perm4((tuple(u0row), u1row, tuple(x), U3_B))
det = sp.expand(B.det())
print("deg(det) monomials:", len(det.as_ordered_terms()))
with open("activedet_equal.txt", "w") as f:
    f.write(str(det))

program = "\n".join((
    "ring R=0,(e,v0,v1,v2,v3,x0,x1,x2,x3),dp;",
    f"poly f={str(det).replace('**', '^')};",
    "list L=factorize(f);",
    '"CODEX_FACTORS";',
    "L;",
    "quit;",
))
completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                           encoding="utf-8", errors="replace",
                           capture_output=True, timeout=600, check=False)
print(completed.stdout)
if completed.stderr.strip():
    print("STDERR:", completed.stderr)
