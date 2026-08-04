#!/usr/bin/env python3
"""TASK B. The x2 = 0 third deep sub-branch of the DISJOINT chart lies in
the ELEVENTH component orbit (exact identification).

Disjoint-chart double-deep stratum (working note): u1 = (0,0,1,-1),
y3 = (0,0,1,1), u3 = (1,1,0,0), y2 = (1,-1,0,0), v3 = -v2, x3 = -x2,
U0 = span(k1 + al*k3, k2 + be*k3) with (k1,k2,k3) = (e0, e1, (0,0,1,-1)),
active determinant 4(be-al)(v0+v1)x2^2.  The squared factor x2 = 0 is the
third deep sub-branch: there

    U0 = span((1,0,al,-al),(0,1,be,-be)),
    U1 = span((0,0,1,-1),(v0,v1,v2,-v2)),
    U2 = span((1,-1,0,0),(x0,x1,0,0)) = P01   (x0+x1 != 0),
    U3 = span((0,0,1,1),(1,1,0,0)),

and this script proves, exactly:
 (1) the restriction is IDENTICALLY PURE for all (al,be,v,x):
     T = -2(x0+x1) * (al,be) x (1,v2) x e_x-slot x e_u3-slot
     (support {0011,0111,1011,1111}), nonzero iff (x0+x1)(al,be) != 0;
 (2) the whole family is the image of the C10/eleventh family under the
     census symmetry g = [source swap (0 2)(1 3)] with mode bijection
     (0,1,2,3) -> (2,1,3,0):  exact span equalities for all parameters:
         C10 parameters  a = (1,-1)  [i.e. (a0,-a1) = (1,1) = pi(y3)-part],
         c0 = -1, c1 = -v1/v0, c2 = al/be, vv = (1,-1,0,0),
         xx = (al,-al,1,0) -- the tie xx-{01} = t*(a0,a1) holds with t = al;
     hence the x2 = 0 sub-branch produces NO new component: it lies in
     the ELEVENTH component orbit."""
import itertools, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


def same_plane(P, Q):
    stack = sp.Matrix([list(P[0]), list(P[1]), list(Q[0]), list(Q[1])])
    for rows in itertools.combinations(range(4), 3):
        for cols in itertools.combinations(range(4), 3):
            if sp.expand(stack[rows, cols].det()) != 0:
                return False
    return True


al, be = sp.symbols("al be")
v = sp.symbols("v0:4")
x0, x1 = sp.symbols("x0 x1")

planes = [
    [(1, 0, al, -al), (0, 1, be, -be)],
    [(0, 0, 1, -1), (v[0], v[1], v[2], -v[2])],
    [(1, -1, 0, 0), (x0, x1, 0, 0)],
    [(0, 0, 1, 1), (1, 1, 0, 0)],
]

# (1) identical purity + closed form
T = {bits: perm4(tuple(tuple(planes[m][bits[m]]) for m in range(4)))
     for bits in itertools.product((0, 1), repeat=4)}
expected = {(0, 0, 1, 1): -2*al*(x0+x1), (0, 1, 1, 1): -2*al*v[2]*(x0+x1),
            (1, 0, 1, 1): -2*be*(x0+x1), (1, 1, 1, 1): -2*be*v[2]*(x0+x1)}
for bits, val in T.items():
    tgt = expected.get(bits, 0)
    assert sp.expand(val - tgt) == 0, (bits, val)
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    mat = sp.zeros(4, 4)
    for bits in itertools.product((0, 1), repeat=4):
        mat[2*bits[left[0]] + bits[left[1]], 2*bits[right[0]] + bits[right[1]]] = T[bits]
    for r1, r2 in itertools.combinations(range(4), 2):
        for c1, c2 in itertools.combinations(range(4), 2):
            assert sp.expand(mat[r1, c1]*mat[r2, c2] - mat[r1, c2]*mat[r2, c1]) == 0
print("(1) x2=0 sub-branch: identically pure, T = -2(x0+x1) *")
print("    [(al,be) (x) (1,v2)] on the (x-slot, u3-slot) words.  OK")

# (2) exact identification with the eleventh
# g = source swap (0 2)(1 3); mode bijection (our -> C10): (0,1,2,3)->(2,1,3,0)


def pi_swap(row):
    return (row[2], row[3], row[0], row[1])


imgs = [[pi_swap(tuple(sp.sympify(c) for c in row)) for row in pl] for pl in planes]


def C10(a0_, a1_, c0_, c1_, c2_, vvrow, t_, x2_, x3_):
    return [
        [(a0_, -a1_, 0, 0), (0, 0, 1, -c0_)],
        [(0, 0, 1, -c1_), tuple(vvrow)],
        [(0, 0, 1, -c2_), (t_*a0_, t_*a1_, x2_, x3_)],
        [(0, 0, 1, 1), (0, 0, 1, -1)],
    ]


c10 = C10(sp.Integer(1), sp.Integer(-1), sp.Integer(-1), -v[1]/v[0],
          al/be, (1, -1, 0, 0), al, sp.Integer(1), sp.Integer(0))
modemap = (2, 1, 3, 0)   # our mode m plays C10-mode modemap[m]
assert all(same_plane(imgs[mm], c10[modemap[mm]]) for mm in range(4))
print("(2) [source swap (02)(13)] carries the x2=0 sub-branch tuple onto the")
print("    C10 family with (c0,c1,c2,t) = (-1, -v1/v0, al/be, al),")
print("    vv = ybar-image, under the mode bijection (0,1,2,3)->(2,1,3,0):")
print("    exact span equalities for all parameters.")
print()
print("CONCLUSION: the disjoint chart's third deep sub-branch x2 = 0 lies")
print("inside the ELEVENTH component orbit closure(C10); no new component.")
print("ALL CHECKS PASSED")
