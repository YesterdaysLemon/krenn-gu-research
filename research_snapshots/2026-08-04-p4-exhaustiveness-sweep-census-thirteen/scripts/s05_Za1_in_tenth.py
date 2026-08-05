#!/usr/bin/env python3
"""TASK B. The Za1 branch (w3 = -k*w2) lies INSIDE the tenth component's
family: exact symbolic identification.

Za1 (sweep modes 0..3 = (U0, ybar-p, ybar-q, u3-w)):
    U0 = span(u3, (0,0,1,k))   [the forced kernel on the branch],
    U1 = span(ybar, (0,1,b,-bk)),  U2 = span(ybar, (0,1,e,-ek)),
    U3 = span(u3, (0,W,w2,-k*w2)).
Tenth's family (branch_ambient_certificates Zplanes, modes (I,J,K,L)):
    U_I = span(ybar,(0,1,b,-bk)), U_J = span(ybar,(0,1,e,-ek)),
    U_K = span(u3,(0,0,1,k)),     U_L = span((1,m,0,0),(0,r,1,-k)).
Claim: Za1 = tenth's tuple under the mode bijection
    (0,1,2,3) -> (K,I,J,L)  with  m = 1,  r = W/w2:
the m = 1 wall of the tenth (where the pair ranks {I,L},{J,L} drop to 3).
Verified as exact span equalities for all parameter values; plus the zeta
identity (the branch kernel vector really is (0,0,1,k)) and a purity/
nonzero check of the tenth at m = 1."""
import itertools, sympy as sp

PERMS4 = tuple(itertools.permutations(range(4)))
COORD_PAIRS = tuple(itertools.combinations(range(4), 2))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.expand(stack[rows, cols].det()) != 0:
                return False
    return True


z = sp.symbols("z0:4")
b, e, k, W, w2 = sp.symbols("b e k W w2")
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)


def covrow(rows3):
    form = perm4((tuple(z),) + tuple(rows3))
    return [sp.expand(sp.diff(form, zi)) for zi in z]


p_ = (0, 1, b, -b*k)
q_ = (0, 1, e, -e*k)
w_ = (0, W, w2, -k*w2)
MZ = sp.Matrix([covrow((YBAR, YBAR, w_)), covrow((YBAR, q_, w_)),
                covrow((p_, YBAR, w_))])
# the branch kernel is span(u3, (0,0,1,k)):
for kv in (U3v, (0, 0, 1, k)):
    assert all(sp.expand(sum(MZ[i, j]*kv[j] for j in range(4))) == 0
               for i in range(3)), kv
print("Za1 kernel: U0 = span(u3, (0,0,1,k)) for all (b,e,k,W,w2).  OK")

# tenth's family
m, r = sp.symbols("m r")


def Zplanes(b_, e_, k_, m_, r_):
    return [
        [(1, -1, 0, 0), (0, 1, b_, -b_*k_)],
        [(1, -1, 0, 0), (0, 1, e_, -e_*k_)],
        [(1, 1, 0, 0), (0, 0, 1, k_)],
        [(1, m_, 0, 0), (0, r_, 1, -k_)],
    ]


tenth = Zplanes(b, e, k, sp.Integer(1), W/w2)
za1 = [
    [U3v, (0, 0, 1, k)],
    [YBAR, p_],
    [YBAR, q_],
    [U3v, w_],
]
# mode bijection (0,1,2,3) -> (K,I,J,L):
modemap = (2, 0, 1, 3)
assert all(same_plane(za1[mm], tenth[modemap[mm]]) for mm in range(4))
print("Za1 tuple == tenth family at (b, e, k, m=1, r=W/w2) under the mode")
print("bijection (0,1,2,3)->(K,I,J,L): exact span equalities.  OK")

# tenth at m=1 is still a nonzero pure restriction (the wall is inside the
# family, not a zero locus): T1100 = -2bek(m+1) = -4bek != 0 generically
Tm1 = {bits: perm4(tuple(tuple(Zplanes(b, e, k, sp.Integer(1), r)[mm][bits[mm]])
                         for mm in range(4)))
       for bits in itertools.product((0, 1), repeat=4)}
nz = {bits: sp.factor(val) for bits, val in Tm1.items() if sp.expand(val) != 0}
assert set(nz) == {(1, 1, 0, 0), (1, 1, 0, 1)}
assert sp.expand(nz[(1, 1, 0, 0)] + 4*b*e*k) == 0
assert sp.expand(nz[(1, 1, 0, 1)] + 2*k*(b*e*r + b + e)) == 0
print("tenth at m=1: T = -2k(2be e_1100 + (ber+b+e) e_1101) nonzero pure.  OK")
print()
print("CONCLUSION: the Za1 branch is the m = 1 wall of the TENTH component;")
print("no new component arises from it.")
print("ALL CHECKS PASSED")
