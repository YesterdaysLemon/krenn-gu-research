#!/usr/bin/env python3
"""Equal-support chart: on s=v0*x1+v1*x0=0 the whole restriction vanishes;
then the (0,2)-pivot chart for the sheets."""
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

# Claim 1: if U0 = span(X2,X3) (the coordinate plane, = U3), the full 16-entry
# restriction is identically zero for ALL v, x, e.
planes = [
    [(0,0,1,0),(0,0,0,1)],
    [list(U1_A), list(v)],
    [list(Y2), list(x)],
    [list(Y3), list(U3_B)],
]
s = v[0]*x[1] + v[1]*x[0]
all_mult_of_s = True
for bits in itertools.product((0,1), repeat=4):
    val = sp.expand(perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4))))
    if val != 0:
        q = sp.simplify(sp.cancel(val / s))
        if s in sp.sympify(q).free_symbols or not q.is_polynomial(*v, *x):
            all_mult_of_s = False
        print("entry", bits, "=", val, " = s *", q)
print("every entry of T(U0=span(X2,X3)) is a multiple of s:", all_mult_of_s)
# on s=0 the Cramer kernel w2=(v0*s,-v1*s,P,0), w3=(v0*s,-v1*s,0,P) IS span(X2,X3)

# Claim 3: (0,2)-pivot chart active determinant.
def covector_matrix():
    rows = []
    for c in (rmul(Y2, Y3), rmul(list(x), Y3)):
        form = pairing(rmul(list(z), list(v)), c)
        rows.append([sp.expand(sp.diff(form, zi)) for zi in z])
    return sp.Matrix(rows)

M = covector_matrix()
m = {}
for a_, b_ in itertools.combinations(range(4), 2):
    m[(a_, b_)] = sp.expand(M[0, a_]*M[1, b_] - M[0, b_]*M[1, a_])
# kernel vectors for pivot columns (0,2): non-pivot columns 1,3
# w_1: supported on {0,2,1}: solve M[:, (0,2)] * (w0,w2) = -M[:,1]*1
# use cofactor pattern: w_1 = (m[(1,2)], -m[(0,2)], ... ) careful; do it directly:
piv02 = m[(0, 2)]
# w for column 1: entries (a0, 1, a2, 0) with M0: M00 a0 + M02 a2 = -M01, M1 likewise
# Cramer: a0 = -det([[M01, M02],[M11, M12]])/piv02 ... clear denominators:
wA = (-(M[0,1]*M[1,2]-M[0,2]*M[1,1]), piv02, -(M[0,0]*M[1,1]-M[0,1]*M[1,0]), 0)
wB = (-(M[0,3]*M[1,2]-M[0,2]*M[1,3]), 0, -(M[0,0]*M[1,3]-M[0,3]*M[1,0]), piv02)
wA = tuple(sp.expand(c) for c in wA)
wB = tuple(sp.expand(c) for c in wB)
for w in (wA, wB):
    assert all(sp.expand(sum(M[r_, c_]*w[c_] for c_ in range(4))) == 0 for r_ in range(2)), w
print("(0,2)-pivot Cramer kernel rows OK; pivot m02 =", sp.factor(piv02))

B = sp.zeros(2, 2)
for i0, u0row in enumerate((wA, wB)):
    for i1, u1row in enumerate((U1_A, tuple(v))):
        B[i0, i1] = perm4((tuple(u0row), u1row, tuple(x), U3_B))
det = sp.expand(B.det())
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
