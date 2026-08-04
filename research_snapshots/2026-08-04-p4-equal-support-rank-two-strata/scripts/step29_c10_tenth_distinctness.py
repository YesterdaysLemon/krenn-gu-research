#!/usr/bin/env python3
"""C10 is NOT the coincident-support tenth component: a closed
symmetry-stable invariant separates them.

Invariant.  Let S be the set of plane 4-tuples in which at least one
mode's plane IS a coordinate 2-plane span(e_a, e_b).  Each condition
"U_m = span(e_a, e_b)" says all Pluecker coordinates of U_m except
p_ab vanish, so S is Zariski-closed; S is stable under mode
permutations, source-coordinate permutations, and the diagonal source
torus (monomial maps send coordinate planes to coordinate planes), and
in-plane basis changes fix planes.  These generate the census
equivalences.

Certificates below (exact rational arithmetic):
 (1) every parametrized C10 point has U_3 = span(e_2, e_3) -- for ALL
     parameter values -- hence closure(C10) is contained in S;
 (2) at the generic C10 sample the other three planes are not
     coordinate planes (the coordinate-plane count is exactly one);
 (3) the tenth-component certificate point (b,e,k,m,r) = (2,3,5,7,11)
     restricts P4 to a nonzero pure tensor (grounding: it is the
     certified tuple) and NONE of its four planes is a coordinate
     plane, so the tenth's closure is NOT contained in S.
Conclusion: for every census symmetry g, closure(C10) != g(tenth):
if they were equal, tenth = g^{-1}(closure(C10)) would lie inside
g^{-1}(S) = S, contradicting (3) since containment in the closed set S
would hold at every point of the tenth's closure.

Together with dimension >= 6 (excludes the eight fivefold components
and the fivefold ninth) and rank monotonicity against the seventh
(C10 sample rank-profile sum 21 > 20, replayed here), C10 lies in no
certified component closure.  Its componenthood is the local-dimension
certificate of step26/step28; granted that, C10 is an ELEVENTH
pure-compression component orbit."""
import itertools, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))

def rmul(u, w):
    return {ab: sp.expand(u[ab[0]]*w[ab[1]] + u[ab[1]]*w[ab[0]]) for ab in COORD_PAIRS}

def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))

def is_coordinate_plane(rows, pair):
    """U = rowspan(rows) equals span(e_a,e_b) iff both rows vanish off
    {a,b} and the on-pair 2x2 block is invertible."""
    comp = tuple(i for i in range(4) if i not in pair)
    off = sp.Matrix([[rows[r][c] for c in comp] for r in range(2)])
    on = sp.Matrix([[rows[r][c] for c in pair] for r in range(2)])
    return off.is_zero_matrix and on.det() != 0

def coordinate_plane_count(planes):
    cnt = 0
    for rows in planes:
        if any(is_coordinate_plane(rows, pair) for pair in COORD_PAIRS):
            cnt += 1
    return cnt

# ---------------------------------------------------------------- C10
c0, c1, c2, t = sp.symbols("c0 c1 c2 t")
v = sp.symbols("v0:4")
x2, x3 = sp.symbols("x2 x3")
xrow = (t*v[0], t*v[1], x2, x3)
c10_sym = [
    [(v[0], -v[1], 0, 0), (0, 0, 1, -c0)],
    [(0, 0, 1, -c1), tuple(v)],
    [(0, 0, 1, -c2), xrow],
    [(0, 0, 1, 1), (0, 0, 1, -1)],
]
# (1) U_3 = span(e2, e3) identically: both rows vanish on coordinates
# 0,1 for all parameter values, and the (2,3)-block is invertible.
u3 = c10_sym[3]
assert all(sp.simplify(u3[r][c]) == 0 for r in range(2) for c in (0, 1))
assert sp.Matrix([[u3[r][c] for c in (2, 3)] for r in range(2)]).det() != 0
print("(1) C10 has U_3 = span(e2,e3) for ALL parameter values: closure(C10) in S")

# (2) generic sample: the other three planes are NOT coordinate planes
sample = {c0: 3, c1: -2, c2: 5, t: 2, v[0]: 3, v[1]: -7, v[2]: 2, v[3]: 5, x2: -1, x3: 4}
c10_planes = [[tuple(sp.nsimplify(sp.sympify(e_).subs(sample)) for e_ in row) for row in pl]
              for pl in c10_sym]
for m in range(3):
    assert not any(is_coordinate_plane(c10_planes[m], pair) for pair in COORD_PAIRS)
assert coordinate_plane_count(c10_planes) == 1
print("(2) at the generic C10 sample the coordinate-plane count is exactly 1")

# ------------------------------------------------- tenth (family Z)
b, e, k, m, r = 2, 3, 5, 7, 11
ybar = (1, -1, 0, 0)
u3v = (1, 1, 0, 0)
tenth_planes = [
    [ybar, (0, 1, b, -b*k)],
    [ybar, (0, 1, e, -e*k)],
    [u3v, (0, 0, 1, k)],
    [(1, m, 0, 0), (0, r, 1, -k)],
]
T = {bits: sp.nsimplify(perm4(tuple(tenth_planes[mm][bits[mm]] for mm in range(4))))
     for bits in itertools.product((0, 1), repeat=4)}
support = {bits for bits, val in T.items() if val != 0}
assert support == {(1, 1, 0, 0), (1, 1, 0, 1)}, support
assert T[(1, 1, 0, 0)] == -2*b*e*k*(m+1)
assert T[(1, 1, 0, 1)] == -2*k*(b*e*r + b + e)
for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
    for bits1 in itertools.product((0, 1), repeat=4):
        for bits2 in itertools.product((0, 1), repeat=4):
            mixed1 = tuple(bits1[i] if i in left else bits2[i] for i in range(4))
            mixed2 = tuple(bits2[i] if i in left else bits1[i] for i in range(4))
            assert sp.expand(T[bits1]*T[bits2] - T[mixed1]*T[mixed2]) == 0
print("(3a) tenth certificate point restricts P4 to a nonzero pure tensor")
assert coordinate_plane_count(tenth_planes) == 0
print("(3b) NO plane of the tenth certificate point is a coordinate plane:"
      " tenth not contained in S")

# ------------------------------------- rank monotonicity vs the seventh
profile = []
for a_, b_ in itertools.combinations(range(4), 2):
    rows_ = []
    for pa in c10_planes[a_]:
        for pb in c10_planes[b_]:
            prod = rmul(pa, pb)
            rows_.append([prod[ab] for ab in COORD_PAIRS])
    profile.append(sp.Matrix(rows_).rank())
assert tuple(profile) == (4, 4, 3, 4, 3, 3), profile
assert sum(profile) == 21
print("(4) C10 sample pair profile (4,4,3,4,3,3), rank sum 21 > 20:"
      " rank monotonicity excludes the seventh component's closure")

print()
print("CONCLUSION: closure(C10) != g(tenth component) for every census")
print("symmetry g; C10 lies in no certified component closure.  With the")
print("local-dimension-six certificate (step26/step28), closure(C10) is an")
print("ELEVENTH pure-compression component orbit.")
