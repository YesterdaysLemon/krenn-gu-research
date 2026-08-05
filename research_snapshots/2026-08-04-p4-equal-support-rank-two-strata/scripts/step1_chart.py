#!/usr/bin/env python3
"""Equal-support in-out chart: derivation of covectors, pivot, active det.

Chart: u1=(0,0,1,-1), y3=(0,0,1,1), u3=(0,0,1,e), y2=(0,0,1,-e),
U1=span(u1,v), U2=span(y2,x), U3=span(y3,u3)=coordinate plane {2,3}.
Relations: u1*y3=0, y2*u3=0 (in-out at mode 3, equal supports {2,3}).
"""
import itertools, sympy as sp

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

# 0. the two zero products hold
zp1 = rmul(U1_A, Y3); zp2 = rmul(Y2, U3_B)
assert all(val == 0 for val in zp1.values()), zp1
assert all(val == 0 for val in zp2.values()), zp2
print("zero products u1*y3=0, y2*u3=0: OK")

# 1. vanishing conditions on U0.
# words with y3 in slot 3: <z w, c y3>=0 for w in {u1,v}, c in {y2,x}
# words with y2 in slot 2: <z w, y2 u>=0 for w in {u1,v}, u in {y3,u3}
print("\n-- y3-slot conditions --")
rows = []
for wname, w in (("u1", U1_A), ("v", tuple(v))):
    for cname, c in (("y2", Y2), ("x", tuple(x))):
        form = pairing(rmul(list(z), list(w)), rmul(list(c), Y3))
        row = [sp.expand(sp.diff(form, zi)) for zi in z]
        iszero = all(r == 0 for r in row)
        print(f"  <z {wname}, {cname} y3>: {'identically 0' if iszero else row}")
        if not iszero:
            rows.append((f"<z {wname},{cname} y3>", row))
print("-- y2-slot conditions --")
for wname, w in (("u1", U1_A), ("v", tuple(v))):
    for uname, u in (("y3", Y3), ("u3", U3_B)):
        form = pairing(rmul(list(z), list(w)), rmul(list(Y2), list(u)))
        row = [sp.expand(sp.diff(form, zi)) for zi in z]
        iszero = all(r == 0 for r in row)
        dup = any(all(sp.expand(a - b) == 0 or sp.simplify(sp.cancel(a/b - rows[0][1][0]/rows[0][1][0]))==0 for a,b in zip(row, rr)) for _, rr in rows)
        print(f"  <z {wname}, y2 {uname}>: {'identically 0' if iszero else row}")
print()
M = sp.Matrix([r for _, r in rows])
print("covector matrix M (rows scaled):")
sp.pprint(M)
# scale row 0 by 1/(1-e) if it came out with the (1-e) factor
M0 = [sp.factor(c) for c in M.row(0)]
print("row0 factored:", M0)
# check col2 == col3
print("col2-col3:", [sp.expand(M[i,2]-M[i,3]) for i in range(M.rows)])
# u1 in kernel
print("M*(0,0,1,-1)^T:", [sp.expand(sum(M[i,j]*u for j,u in enumerate(U1_A))) for i in range(M.rows)])

# 2. Cramer pivots
minors = {}
for a_, b_ in itertools.combinations(range(4), 2):
    minors[(a_, b_)] = sp.factor(sp.expand(M[0, a_]*M[1, b_] - M[0, b_]*M[1, a_]))
for k, val in minors.items():
    print("minor", k, "=", val)
