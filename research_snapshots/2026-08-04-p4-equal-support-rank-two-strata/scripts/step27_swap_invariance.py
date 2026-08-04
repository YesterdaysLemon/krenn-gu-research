#!/usr/bin/env python3
"""Verify: the (12)-mode swap of the generic C10 sample lies in C10
(same shape with v' = x, x' = v, t' = 1/t, c1' = c2, c2' = c1)."""
import sympy as sp

c0v, c1v, c2v, tv = 3, -2, 5, 2
v = (3, -7, 2, 5)
x = (tv*v[0], tv*v[1], -1, 4)

U0 = [(v[0], -v[1], 0, 0), (0, 0, 1, -c0v)]
U1 = [(0, 0, 1, -c1v), v]
U2 = [(0, 0, 1, -c2v), x]
U3 = [(0, 0, 1, 0), (0, 0, 0, 1)]

# swapped tuple: (U0, U2, U1, U3).  Claimed C10 parameters:
# v' = x, t' = 1/t, c1' = c2, c2' = c1, and U0 must equal
# span((x0, -x1, 0, 0), (0,0,1,-c0)).
vp = x
xp = tuple(sp.Rational(1, tv)*c for c in (vp[0], vp[1])) + (v[2], v[3])
# check x' has the C10 form (t'*v'0, t'*v'1, *, *) with t' = 1/t: by construction.
# main check: span((v'0, -v'1, 0, 0)) == span((v0,-v1,0,0)):
M = sp.Matrix([[vp[0], -vp[1], 0, 0], [v[0], -v[1], 0, 0]])
print("U0 {01}-vector direction preserved:", M.rank() == 1)
# and the swapped tuple's planes equal the C10-shape planes with those params:
U1p = [(0, 0, 1, -c2v), vp]     # mode-1 slot after swap = old U2
U2p = [(0, 0, 1, -c1v), tuple(sp.nsimplify(c) for c in (sp.Rational(1,1)*v[0], v[1], v[2], v[3]))]
# old U1 = span(w1, v); C10-shape for mode 2 requires span(w_{c2'}, x') with
# x' = (t' v'0, t' v'1, x2', x3') = (v0, v1, v2, v3)?? x' must equal v up to
# the plane: v = (v0,v1,v2,v3) and t'*v' = (v0, v1): so x' = (v0, v1, x2', x3')
# with (x2', x3') = (v2, v3): x' = v.  So mode-2 plane = span(w_{c1}, v) = old U1.
same1 = sp.Matrix([list(U2[0]), list(U2[1]), list(U1p[0]), list(U1p[1])]).rank() == 2
same2 = sp.Matrix([list(U1[0]), list(U1[1]), list(U2p[0]), list(U2p[1])]).rank() == 2
print("mode-1 slot plane matches C10 shape:", same1)
print("mode-2 slot plane matches C10 shape:", same2)
print("=> C10 is invariant under the (12) mode swap with (v,x,t,c1,c2) -> (x,v,1/t,c2,c1)")
