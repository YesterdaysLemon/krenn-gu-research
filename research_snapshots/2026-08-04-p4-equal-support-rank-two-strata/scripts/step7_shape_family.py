#!/usr/bin/env python3
"""Shape-family derivation of the W-branch.

Family: U0=span((a,b,0,0),u1), U1=span(u1,v), U2=span((0,0,1,-c),x),
U3 = coordinate plane {2,3} = span(y3=(0,0,1,1), u3=(0,0,1,e)).
(e is basis bookkeeping for U3, not a modulus.)
Derive the exact pure conditions.
"""
import itertools, sympy as sp

a, b, c, e = sp.symbols("a b c e")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")

U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
PERMS4 = tuple(itertools.permutations(range(4)))

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

planes = [
    [(a, b, 0, 0), U1_A],
    [U1_A, tuple(v)],
    [(0, 0, 1, -c), tuple(x)],
    [Y3, (0, 0, 1, e)],
]
T = {}
for bits in itertools.product((0,1), repeat=4):
    T[bits] = perm4(tuple(planes[m][bits[m]] for m in range(4)))
print("entries:")
for bits, val in T.items():
    if val != 0:
        print("  T%s = %s" % ("".join(map(str, bits)), sp.factor(val)))

# structural zeros claimed: every word except (0011),(0100),(0101),(0110),(0111),(1111)
nonzero_words = {(0,0,1,1),(0,1,0,0),(0,1,0,1),(0,1,1,0),(0,1,1,1),(1,1,1,1)}
for bits, val in T.items():
    if bits not in nonzero_words:
        assert val == 0, (bits, val)

# Pure conditions: all three flattenings rank <= 1.
# Claimed: pure & T1111 != 0  <=>  a*v1+b*v0 = 0, v1*x0-v0*x1 = 0 (up to scale of (a,b))
# derive 2x2 minor conditions of mode-3 flattening containing row (0,0,1,*) = (0, T0011):
m3 = sp.Matrix([[T[w+(0,)], T[w+(1,)]] for w in itertools.product((0,1), repeat=3)])
minors3 = set()
for r1, r2 in itertools.combinations(range(8), 2):
    minors3.add(sp.expand(m3[r1,0]*m3[r2,1] - m3[r1,1]*m3[r2,0]))
minors3.discard(0)
print("\nmode-3 flattening 2x2 minors (factored):")
for mm in sorted(minors3, key=str):
    print("  ", sp.factor(mm))

# Now impose K0 shape (a,b)=(v0,-v1) and W: v1*x0-v0*x1=0 and check ALL flattening
# minors vanish identically => pure for every remaining parameter value.
sub = {a: v[0], b: -v[1], x[0]: v[0]*x[1]/v[1]}
Tsub = {bits: sp.cancel(sp.together(val.subs(sub))) for bits, val in T.items()}
print("\nafter (a,b)=(v0,-v1), x0=v0*x1/v1:")
for bits, val in Tsub.items():
    if val != 0:
        print("  T%s = %s" % ("".join(map(str, bits)), sp.factor(val)))
ok = True
for left in (((0,), (1,2,3)), ((1,), (0,2,3)), ((2,), (0,1,3)), ((3,), (0,1,2)),
             ((0,1),(2,3)), ((0,2),(1,3)), ((0,3),(1,2))):
    li, ri = left
    mrows = {}
    for bits in itertools.product((0,1), repeat=4):
        r_ = tuple(bits[i] for i in li); c_ = tuple(bits[i] for i in ri)
        mrows.setdefault(r_, {})[c_] = Tsub[bits]
    keys_r = sorted(mrows); keys_c = sorted(mrows[keys_r[0]])
    mat = sp.Matrix([[mrows[r_][c_] for c_ in keys_c] for r_ in keys_r])
    for i, j in itertools.combinations(range(mat.rows), 2):
        for k, l in itertools.combinations(range(mat.cols), 2):
            det = sp.simplify(sp.together(mat[i,k]*mat[j,l] - mat[i,l]*mat[j,k]))
            if det != 0:
                ok = False
                print("nonvanishing minor", li, ri, det)
print("\nall flattening 2x2 minors vanish identically on the W-form:", ok)
print("T0111 =", sp.factor(Tsub[(0,1,1,1)]))
print("T1111 =", sp.factor(Tsub[(1,1,1,1)]))

# And the CONVERSE: pure + T1111 != 0 forces the two conditions (T0011=0, T0100=0,
# T0101=0, T0110=0 are needed; then factor structure):
# from row (0,T0011): T0100=0 forces (1-c)(a v1 + b v0)=0; T0101=0 forces (e-c)(a v1+ b v0)=0
# c=1 collapses K2 into u1-direction AND still needs a*x1+b*x0=0 & a*v1+b*v0=0 (shown in notes)
print("\nT0100 =", sp.factor(T[(0,1,0,0)]))
print("T0101 =", sp.factor(T[(0,1,0,1)]))
print("T0011 =", sp.factor(T[(0,0,1,1)]))
print("T0110 =", sp.factor(T[(0,1,1,0)]))
